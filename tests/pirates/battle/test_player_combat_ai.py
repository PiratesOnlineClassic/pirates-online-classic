import builtins
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

from panda3d.core import Filename, NodePath, VirtualFileSystem, loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')


def _stubWeaponGlobals():
    # WeaponGlobals reads WeaponGlobals.pkl from the game resources at import
    # time; when the resources are unavailable fall back to a stub module.
    if 'pirates.battle.WeaponGlobals' in sys.modules:
        return

    searchPath = '../resources/phase_2/etc'
    if VirtualFileSystem.getGlobalPtr().exists(Filename(searchPath + '/WeaponGlobals.pkl')):
        return

    module = types.ModuleType('pirates.battle.WeaponGlobals')

    def __getattr__(name):
        if name.startswith('__'):
            raise AttributeError(name)

        value = MagicMock(name='WeaponGlobals.%s' % name)
        setattr(module, name, value)
        return value

    module.__getattr__ = __getattr__
    sys.modules['pirates.battle.WeaponGlobals'] = module
    import pirates.battle
    pirates.battle.WeaponGlobals = module


_stubWeaponGlobals()

if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

with patch.object(builtins.loader, 'loadFont', Mock()):
    from pirates.battle import BattleManagerAI as battle_manager_module
    from pirates.battle.BattleManagerAI import BattleManagerAI

from pirates.battle import EnemyGlobals
from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.battle.WeaponBaseAI import WeaponBaseAI
from pirates.distributed.TargetManagerAI import TargetManagerAI
from pirates.piratesbase import PiratesGlobals
from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI
from pirates.uberdog.UberDogGlobals import InventoryType

# patch the WeaponGlobals module the code under test actually uses...
WeaponGlobals = battle_manager_module.WeaponGlobals


INF_RANGE = -1


class FakeInventory:

    def __init__(self, stacks=None):
        self.stacks = dict(stacks or {})

    def getStackQuantity(self, stackType):
        return self.stacks.get(stackType, 0)

    def b_setStackQuantity(self, stackType, quantity):
        self.stacks[stackType] = quantity


def makePlayer(doId=100, inventory=None, weaponId=InventoryType.CutlassWeaponL1, drawn=True, hp=100, mojo=50):
    player = DistributedPlayerPirateAI.__new__(DistributedPlayerPirateAI)
    NodePath.__init__(player, 'player-%d' % doId)
    player.doId = doId
    player.isNpc = False
    player.currentWeaponId = weaponId
    player.isWeaponDrawn = drawn
    player.hp = hp
    player.maxHp = 100
    player.quietly = False
    player.mojo = mojo
    player.maxMojo = 100
    player.zombie = 0
    player.skillRechargeTimes = {}
    player.inventory = inventory or FakeInventory()
    player.getInventory = lambda: player.inventory
    player.isPaid = Mock(return_value=True)
    player.sendUpdate = Mock()
    player.air = SimpleNamespace(battleMgr=Mock(getModifiedRechargeTime=Mock(return_value=0)))
    return player


def weaponGlobalsPatches(**overrides):
    values = {
        'getRepId': Mock(return_value=InventoryType.CutlassRep),
        'isValidSkill': Mock(return_value=True),
        'isValidAttack': Mock(return_value=True),
        'isInfiniteAmmo': Mock(return_value=True),
        'getSkillAmmoInventoryId': Mock(return_value=None),
        'getMojoCost': Mock(return_value=0),
        'getAttackEffects': Mock(return_value=([0, 0, 0, 0, 0], [0, 0, 0, 0, 0])),
        'canFreeUse': Mock(return_value=True),
        'isVoodooWeapon': Mock(return_value=False),
        'getIsShipSkill': Mock(return_value=False),
        'getIsCannonSkill': Mock(return_value=False),
        'isFriendlyFire': Mock(return_value=False),
        'INF_RANGE': INF_RANGE,
    }
    values.update(overrides)
    return patch.multiple(WeaponGlobals, **values)


def makeManager(air=None):
    manager = BattleManagerAI.__new__(BattleManagerAI)
    manager.air = air or SimpleNamespace(doId2do={}, targetMgr=Mock())
    manager.AttackerDisengageRange = 100.0
    return manager


class SkillValidationTests(unittest.TestCase):

    def test_learned_skill_with_drawn_weapon_may_be_used(self):
        manager = makeManager()
        player = makePlayer(inventory=FakeInventory({InventoryType.CutlassWeaponL1: 1, InventoryType.CutlassHack: 2}))
        with weaponGlobalsPatches():
            self.assertTrue(manager.canUseSkill(player, InventoryType.CutlassHack, 0))

    def test_unlearned_skill_is_rejected(self):
        manager = makeManager()
        player = makePlayer(inventory=FakeInventory({InventoryType.CutlassWeaponL1: 1, InventoryType.CutlassCleave: 1}))
        with weaponGlobalsPatches():
            self.assertFalse(manager.canUseSkill(player, InventoryType.CutlassCleave, 0))

    def test_sheathed_or_unowned_weapon_is_rejected(self):
        manager = makeManager()
        inventory = FakeInventory({InventoryType.CutlassHack: 2})
        with weaponGlobalsPatches():
            # the avatar does not own the cutlass it claims to be using
            self.assertFalse(manager.canUseSkill(makePlayer(inventory=inventory), InventoryType.CutlassHack, 0))

            inventory.stacks[InventoryType.CutlassWeaponL1] = 1
            self.assertFalse(manager.canUseSkill(makePlayer(inventory=inventory, drawn=False), InventoryType.CutlassHack, 0))

    def test_avatar_without_weapons_cannot_attack(self):
        manager = makeManager()
        player = makePlayer(weaponId=0, drawn=False)
        with weaponGlobalsPatches():
            self.assertFalse(manager.canUseSkill(player, InventoryType.CutlassHack, 0))

    def test_not_enough_mojo_is_rejected(self):
        manager = makeManager()
        player = makePlayer(inventory=FakeInventory({InventoryType.DollWeaponL1: 1, InventoryType.DollPoke: 2}),
            weaponId=InventoryType.DollWeaponL1, mojo=10)

        with weaponGlobalsPatches(getMojoCost=Mock(return_value=-30)):
            self.assertFalse(manager.canUseSkill(player, InventoryType.DollPoke, 0))
            player.mojo = 30
            self.assertTrue(manager.canUseSkill(player, InventoryType.DollPoke, 0))

    def test_out_of_ammo_is_rejected(self):
        manager = makeManager()
        inventory = FakeInventory({InventoryType.PistolWeaponL1: 1, InventoryType.PistolShoot: 2,
            InventoryType.PistolLeadShot: 2})
        player = makePlayer(inventory=inventory, weaponId=InventoryType.PistolWeaponL1)
        with weaponGlobalsPatches(isInfiniteAmmo=Mock(side_effect=lambda skillId: skillId != InventoryType.PistolLeadShot),
                getSkillAmmoInventoryId=Mock(return_value=InventoryType.begin_WeaponPistolAmmo)):
            self.assertFalse(manager.canUseSkill(player, InventoryType.PistolShoot, InventoryType.PistolLeadShot))
            inventory.stacks[InventoryType.begin_WeaponPistolAmmo] = 1
            self.assertTrue(manager.canUseSkill(player, InventoryType.PistolShoot, InventoryType.PistolLeadShot))

    def test_recharging_skill_is_rejected(self):
        manager = makeManager()
        player = makePlayer(inventory=FakeInventory({InventoryType.CutlassWeaponL1: 1, InventoryType.CutlassSweep: 2}))
        player.air.battleMgr.getModifiedRechargeTime.return_value = 20.0
        with weaponGlobalsPatches():
            player.startSkillRecharge(InventoryType.CutlassSweep)
            self.assertFalse(manager.canUseSkill(player, InventoryType.CutlassSweep, 0))

            player.skillRechargeTimes[InventoryType.CutlassSweep] -= 20.0
            self.assertTrue(manager.canUseSkill(player, InventoryType.CutlassSweep, 0))

    def test_skill_costs_are_spent_once(self):
        manager = makeManager()
        ammoId = InventoryType.begin_WeaponPistolAmmo
        inventory = FakeInventory({ammoId: 3})
        player = makePlayer(inventory=inventory, weaponId=InventoryType.DollWeaponL1, mojo=50)
        player.b_setMojo = Mock(side_effect=player.setMojo)
        with weaponGlobalsPatches(isInfiniteAmmo=Mock(side_effect=lambda skillId: skillId != InventoryType.PistolLeadShot),
                getSkillAmmoInventoryId=Mock(return_value=ammoId),
                getAttackEffects=Mock(return_value=([0, 0, 0, -20, 0], [0, 0, 0, 0, 0]))):
            manager.useSkillCosts(player, InventoryType.PistolShoot, InventoryType.PistolLeadShot)

        self.assertEqual(inventory.getStackQuantity(ammoId), 2)
        self.assertEqual(player.getMojo(), 30)
        self.assertIn(InventoryType.PistolShoot, player.skillRechargeTimes)

    def test_npcs_are_never_validated(self):
        manager = makeManager()
        npc = SimpleNamespace(doId=5)
        self.assertTrue(manager.requestSkillUse(npc, InventoryType.CutlassHack, 0))


class TonicTests(unittest.TestCase):

    def test_tonic_is_used_without_a_weapon_drawn(self):
        manager = makeManager()
        player = makePlayer(weaponId=0, drawn=False)
        player.useTonic = Mock(return_value=True)
        result = manager.getTargetedSkillResult(player, None, InventoryType.UseItem, InventoryType.Potion1, [], 0, [0, 0, 0])
        player.useTonic.assert_called_once_with(InventoryType.Potion1)
        self.assertEqual(result[2], WeaponGlobals.RESULT_HIT)

    def test_tonic_does_not_effect_area_targets(self):
        manager = makeManager()
        player = makePlayer()
        player.useTonic = Mock(return_value=True)
        self.assertIsNone(manager.getTargetedSkillResult(player, makePlayer(doId=101), InventoryType.UseItem,
            InventoryType.Potion1, [], 0, [0, 0, 0]))

        player.useTonic.assert_not_called()

    def test_failed_tonic_has_no_result(self):
        manager = makeManager()
        player = makePlayer()
        player.useTonic = Mock(return_value=False)
        self.assertIsNone(manager.getTargetedSkillResult(player, None, InventoryType.UseItem,
            InventoryType.Potion1, [], 0, [0, 0, 0]))


class PlayerDamageTests(unittest.TestCase):

    def makeSkillResultManager(self, world):
        manager = makeManager()
        manager.obeysPirateCode = Mock(return_value=True)
        manager.willWeaponHit = Mock(return_value=WeaponGlobals.RESULT_NOT_AVAILABLE)
        manager.getRelativePosition = Mock(return_value=0)
        manager.getModifiedSkillEffects = Mock(return_value=([0, 0, 0, 0, 0], [-10, 0, 0, 0, 0]))
        manager.getModifiedSkillEffectsSword = manager.getModifiedSkillEffects
        manager.air.targetMgr = Mock(hasTarget=Mock(return_value=False), hasAttacker=Mock(return_value=False))
        return manager

    def makePlayers(self, world):
        attacker = makePlayer(doId=100)
        target = makePlayer(doId=101)
        attacker.battleSkillDiary = Mock(hasSkill=Mock(return_value=True))
        for player in (attacker, target):
            player.getWorld = Mock(return_value=world)

        return attacker, target

    def test_players_cannot_damage_each_other_outside_pvp(self):
        world = Mock(getType=Mock(return_value=PiratesGlobals.INSTANCE_MAIN))
        manager = self.makeSkillResultManager(world)
        attacker, target = self.makePlayers(world)
        with weaponGlobalsPatches():
            self.assertIsNone(manager._skillResult(attacker, target, InventoryType.CutlassHack, 0, [], 0, [0, 0, 0], 0))

        manager.willWeaponHit.assert_not_called()

    def test_undead_players_may_be_damaged(self):
        world = Mock(getType=Mock(return_value=PiratesGlobals.INSTANCE_MAIN))
        manager = self.makeSkillResultManager(world)
        attacker, target = self.makePlayers(world)
        target.zombie = 1
        with weaponGlobalsPatches():
            manager._skillResult(attacker, target, InventoryType.CutlassHack, 0, [], 0, [0, 0, 0], 0)

        manager.willWeaponHit.assert_called_once()

    def test_friendly_skills_may_be_used_on_players(self):
        world = Mock(getType=Mock(return_value=PiratesGlobals.INSTANCE_MAIN))
        manager = self.makeSkillResultManager(world)
        attacker, target = self.makePlayers(world)
        with weaponGlobalsPatches(isFriendlyFire=Mock(return_value=True)):
            manager._skillResult(attacker, target, InventoryType.DollHeal, 0, [], 0, [0, 0, 0], 0)

        manager.willWeaponHit.assert_called_once()

    def test_pvp_instances_decide_damage(self):
        world = Mock(getType=Mock(return_value=PiratesGlobals.INSTANCE_PVP), isDamageAllowed=Mock(return_value=True))
        manager = self.makeSkillResultManager(world)
        attacker, target = self.makePlayers(world)
        with weaponGlobalsPatches():
            manager._skillResult(attacker, target, InventoryType.CutlassHack, 0, [], 0, [0, 0, 0], 0)

        world.isDamageAllowed.assert_called_once_with(attacker, target)
        world.avatarAttacked.assert_called_once_with(attacker, target)
        manager.willWeaponHit.assert_called_once()


class AttackerRangeTests(unittest.TestCase):

    def checkAttacker(self, distance, attackRange=6):
        targetMgr = Mock()
        manager = makeManager(SimpleNamespace(doId2do={}, targetMgr=targetMgr))
        manager.getModifiedAttackRange = Mock(return_value=attackRange)
        manager.getRelativePosition = Mock(return_value=distance)
        attacker = SimpleNamespace(doId=100, comboDiary=Mock(getCombos=Mock(return_value=[])),
            battleSkillDiary=Mock(getCurrentSkill=Mock(return_value=InventoryType.CutlassHack),
                getSkill=Mock(return_value=[0, 0, 10])))

        target = SimpleNamespace(doId=1000)
        manager.air.doId2do.update({attacker.doId: attacker, target.doId: target})
        with weaponGlobalsPatches():
            # attacker 999 has since left the district
            manager.updateTarget(target.doId, [attacker.doId, 999])

        return targetMgr, attacker, target

    def test_update_target_with_unknown_target_is_ignored(self):
        makeManager().updateTarget(1000, [100])

    def test_melee_attacker_stepping_back_keeps_target(self):
        targetMgr, attacker, target = self.checkAttacker(distance=20)
        targetMgr.removeAttacker.assert_not_called()

    def test_attacker_leaving_the_battle_is_removed(self):
        targetMgr, attacker, target = self.checkAttacker(distance=500)
        targetMgr.removeAttacker.assert_called_once_with(attacker, target)

    def test_infinite_range_attacker_is_never_removed(self):
        targetMgr, attacker, target = self.checkAttacker(distance=5000, attackRange=INF_RANGE)
        targetMgr.removeAttacker.assert_not_called()


class TargetManagerTests(unittest.TestCase):

    def test_damage_target_switch_without_attackers_present(self):
        targetMgr = TargetManagerAI.__new__(TargetManagerAI)
        targetMgr.air = SimpleNamespace(doId2do={})
        targetMgr.objectDict = {1000: [100, 101]}
        targetMgr.getTargetSwitchType = Mock(return_value=EnemyGlobals.TARGET_SWITCH_TYPE_DAMAGE)
        self.assertIsNone(targetMgr.findTargetableObject(1000))

    def test_remove_target_clears_every_attacker(self):
        targetMgr = TargetManagerAI.__new__(TargetManagerAI)
        attackers = [SimpleNamespace(doId=doId, b_setCurrentTarget=Mock()) for doId in (100, 101, 102)]
        targetMgr.air = SimpleNamespace(doId2do=dict((attacker.doId, attacker) for attacker in attackers),
            battleMgr=Mock())

        targetMgr.objectDict = {1000: [100, 101, 102, 103]}
        targetMgr.removeTarget(SimpleNamespace(doId=1000))
        self.assertNotIn(1000, targetMgr.objectDict)
        for attacker in attackers:
            attacker.b_setCurrentTarget.assert_called_once_with(0)


class WeaponBaseTests(unittest.TestCase):

    def makeWeaponBase(self, avatar, allowed=True):
        avatar.air = SimpleNamespace(doId2do={avatar.doId: avatar}, getAvatarIdFromSender=lambda: avatar.doId,
            battleMgr=Mock(requestSkillUse=Mock(return_value=allowed)))
        avatar.useTargetedSkill = Mock()
        return avatar

    def test_targeted_skill_costs_are_spent_once_for_area_targets(self):
        avatar = self.makeWeaponBase(makePlayer())
        for doId in (200, 201):
            avatar.air.doId2do[doId] = SimpleNamespace(doId=doId)

        WeaponBaseAI.requestTargetedSkill(avatar, InventoryType.GrenadeThrow, 0, 0, 200, [200, 201], 0, [0, 0, 0], 0)
        avatar.air.battleMgr.requestSkillUse.assert_called_once_with(avatar, InventoryType.GrenadeThrow, 0)
        self.assertEqual(avatar.useTargetedSkill.call_count, 3)

    def test_rejected_targeted_skill_has_no_result(self):
        avatar = self.makeWeaponBase(makePlayer(), allowed=False)
        WeaponBaseAI.requestTargetedSkill(avatar, InventoryType.CutlassHack, 0, 0, 0, [], 0, [0, 0, 0], 0)
        avatar.useTargetedSkill.assert_not_called()

    def test_projectile_skill_result_arguments(self):
        avatar = makePlayer()
        avatar.air = SimpleNamespace(battleMgr=Mock())
        avatar.air.battleMgr.getTargetedSkillResult.return_value = [1, 2, 0, 0, [5], [0] * 5, [0] * 5, [], 3, [0, 0, 0], 0]
        avatar.sendUpdate = Mock()
        WeaponBaseAI.useProjectileSkill(avatar, avatar, None, 1, 2, 0, 0, [5], [1, 2, 3], [0, 0, 1], [], 4)
        avatar.air.battleMgr.getTargetedSkillResult.assert_called_once_with(avatar, None, 1, 2, [5], 4, [1, 2, 3])
        self.assertEqual(avatar.sendUpdate.call_args[0][1][4], [5])


class BattleAvatarTests(unittest.TestCase):

    def makeAvatar(self, hp=10):
        avatar = DistributedBattleAvatarAI.__new__(DistributedBattleAvatarAI)
        avatar.doId = 1000
        avatar.hp = hp
        avatar.immortal = False
        avatar.quietly = False
        avatar.gameFSM = Mock(getCurrentOrNextState=Mock(return_value='LandRoam'))
        return avatar

    def test_get_game_state(self):
        self.assertEqual(self.makeAvatar().getGameState(), 'LandRoam')

    def test_hp_is_updated_before_death(self):
        avatar = self.makeAvatar()
        seen = []
        avatar.b_setGameState = Mock(side_effect=lambda state: seen.append(avatar.hp))
        avatar.setHp(-5)
        avatar.b_setGameState.assert_called_once_with('Death')
        self.assertEqual(seen, [0])

        avatar.setHp(0)
        avatar.b_setGameState.assert_called_once_with('Death')


if __name__ == '__main__':
    unittest.main()
