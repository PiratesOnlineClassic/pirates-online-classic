import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

from panda3d.core import Filename, NodePath, VirtualFileSystem, loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')

# these tests exercise the real skill tables, they need the game resources...
HAVE_RESOURCES = VirtualFileSystem.getGlobalPtr().exists(Filename('../resources/phase_2/etc/WeaponGlobals.pkl'))

if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

with patch.object(builtins.loader, 'loadFont', Mock()):
    from pirates.battle import BattleManagerAI as battle_manager_module
    from pirates.battle.BattleManagerAI import BattleManagerAI

from pirates.battle.BattleManagerBase import BattleManagerBase
from pirates.battle.BattleRandom import BattleRandom
from pirates.pirate import AvatarTypes
from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

WeaponGlobals = battle_manager_module.WeaponGlobals


class FakeInventory:

    def __init__(self, stacks=None):
        self.stacks = dict(stacks or {})

    def getStackQuantity(self, stackType):
        return self.stacks.get(stackType, 0)

    def b_setStackQuantity(self, stackType, quantity):
        self.stacks[stackType] = quantity


class FakeClock:

    def __init__(self):
        self.now = 1000.0

    def getFrameTime(self):
        return self.now


def makeAvatar(cls=DistributedBattleAvatarAI, doId=100, level=10, hp=500, isNpc=False, world=True):
    avatar = cls.__new__(cls)
    NodePath.__init__(avatar, 'avatar-%d' % doId)
    DistributedBattleAvatarAI.__init__(avatar, MagicMock())
    avatar.doId = doId
    avatar.isNpc = isNpc
    avatar.level = level
    avatar.hp = hp
    avatar.maxHp = hp
    avatar.mojo = 100
    avatar.maxMojo = 100
    avatar.swiftness = 1
    avatar.maxSwiftness = 1
    avatar.battleRandom = BattleRandom(doId)
    avatar.sendUpdate = Mock()
    avatar.getWorld = Mock(return_value=Mock() if world else None)
    avatar.getDamagable = Mock(return_value=True)
    avatar.getInventory = Mock(return_value=FakeInventory())
    return avatar


def makePlayer(doId=100, stacks=None, weaponId=InventoryType.CutlassWeaponL1, **kwargs):
    player = makeAvatar(DistributedPlayerPirateAI, doId=doId, **kwargs)
    player.inventory = FakeInventory(stacks)
    player.getInventory = lambda: player.inventory
    player.currentWeaponId = weaponId
    player.isWeaponDrawn = True
    player.zombie = 0
    player.stickyTargets = []
    player.skillRechargeTimes = {}
    player._team = PiratesGlobals.PLAYER_TEAM
    player.isPaid = Mock(return_value=True)
    player.hasTempDoubleXPReward = Mock(return_value=False)
    player.sendUpdateToAvatarId = Mock()
    return player


class CombatFixture(unittest.TestCase):

    def setUp(self):
        self.clock = FakeClock()
        self.manager = BattleManagerAI.__new__(BattleManagerAI)
        self.air = SimpleNamespace(doId2do={}, battleMgr=self.manager,
            targetMgr=Mock(hasTarget=Mock(return_value=False), hasAttacker=Mock(return_value=False),
                getAttackers=Mock(return_value=[])),
            newsManager=Mock(isHolidayActive=Mock(return_value=False)))
        self.manager.air = self.air
        self.avatars = []

    def tearDown(self):
        for avatar in self.avatars:
            avatar.clearSkillEffects()

    def track(self, avatar):
        avatar.air = self.air
        avatar.getSkillEffectTime = lambda: self.clock.now
        avatar.battleSkillDiary = Mock(hasSkill=Mock(return_value=True), getSkill=Mock(return_value=[0, 0, 0]))
        avatar.comboDiary = Mock(getCombo=Mock(return_value=(0, 0, 0)))
        avatar.b_setGameState = Mock()
        self.air.doId2do[avatar.doId] = avatar
        self.avatars.append(avatar)
        return avatar

    def makePlayer(self, doId=100, **kwargs):
        return self.track(makePlayer(doId=doId, **kwargs))

    def makeEnemy(self, doId=200, level=10, hp=5000):
        enemy = self.track(makeAvatar(doId=doId, isNpc=True, level=level, hp=hp))
        enemy.avatarType = AvatarTypes.EarthUndead[0]
        enemy.getMonsterDmg = Mock(return_value=30)
        return enemy


@unittest.skipUnless(HAVE_RESOURCES, 'the game resources are required')
class SkillEffectIdTests(unittest.TestCase):

    def test_effect_ids_come_from_the_buff_list(self):
        avatar = makeAvatar()
        avatar.skillEffects = [[WeaponGlobals.C_POISON, 10, 0, 5], [WeaponGlobals.C_POISON, 10, 0, 6],
            [WeaponGlobals.C_CURSE, 60, 0, 5]]
        self.assertEqual(avatar.getSkillEffectIds(), [WeaponGlobals.C_POISON, WeaponGlobals.C_CURSE])

        # the required field getter still returns the buffs the client expects
        self.assertEqual(len(avatar.getSkillEffects()), 3)

    def test_blind_attacker_hits_less(self):
        manager = BattleManagerAI.__new__(BattleManagerAI)
        attacker = makeAvatar(isNpc=True)
        target = makePlayer(doId=200)
        attacker.battleRandom = Mock(getRandom=Mock(return_value=0.8))

        # pistol shot accuracy is 80, a roll of 0.8 still hits...
        self.assertEqual(manager.willWeaponHit(attacker, target, InventoryType.PistolShoot, 0, 0), WeaponGlobals.RESULT_HIT)
        attacker.skillEffects = [[WeaponGlobals.C_BLIND, 10, 0, 200]]
        self.assertEqual(manager.willWeaponHit(attacker, target, InventoryType.PistolShoot, 0, 0), WeaponGlobals.RESULT_MISS)

    def test_curse_and_take_cover_modify_damage(self):
        manager = BattleManagerAI.__new__(BattleManagerAI)
        attacker = makePlayer(level=10)
        target = makeAvatar(doId=200, isNpc=True, level=10)
        target.avatarType = Mock(isA=Mock(return_value=False))
        attacker.battleRandom = Mock(getRandom=Mock(return_value=1.0))
        with patch.object(battle_manager_module.EnemyGlobals, 'getMonsterClass', Mock(return_value=None)):
            base = manager.getModifiedSkillEffects(attacker, target, InventoryType.CutlassHack, 0)[1][0]
            target.skillEffects = [[WeaponGlobals.C_CURSE, 60, 0, 300]]
            cursed = manager.getModifiedSkillEffects(attacker, target, InventoryType.CutlassHack, 0)[1][0]
            target.skillEffects = [[WeaponGlobals.C_TAKECOVER, 10, 0, 300]]
            covered = manager.getModifiedSkillEffects(attacker, target, InventoryType.CutlassHack, 0)[1][0]

        self.assertLess(base, 0)
        self.assertEqual(cursed, base + int(base * WeaponGlobals.CURSED_DAM_AMP))
        # take cover zeroes the damage, the comparative level modifier still deals 1
        self.assertEqual(covered, -1)


def predictClientAttack(attacker, target, skillId, ammoSkillId, areaTargets, charge=0):
    # the attacking client's prediction, see BattleManager.doAttack and
    # LocalPirate.composeRequestTargetedSkill...
    clientManager = BattleManagerBase()
    attacker.battleRandom.advanceAttackSeed()
    result = clientManager.willWeaponHit(attacker, target, skillId, ammoSkillId, charge)
    attackerEffects, targetEffects = clientManager.getModifiedSkillEffects(attacker, target, skillId, ammoSkillId, charge)
    areaEffects = [clientManager.getModifiedSkillEffects(attacker, av, skillId, ammoSkillId, charge)[1] for av in areaTargets]
    return result, attackerEffects, targetEffects, areaEffects


@unittest.skipUnless(HAVE_RESOURCES, 'the game resources are required')
class SkillResolutionTests(CombatFixture):

    def attackBothSides(self, attacker, target, skillId, ammoSkillId=0, areaTargets=()):
        # the client rolls with it's own copy of the attacker's battle random...
        serverRandom = attacker.battleRandom
        attacker.battleRandom = self.clientRandom
        try:
            prediction = predictClientAttack(attacker, target, skillId, ammoSkillId, areaTargets)
        finally:
            attacker.battleRandom = serverRandom

        result = self.manager.getTargetedSkillResult(attacker, target, skillId, ammoSkillId,
            [av.doId for av in areaTargets], 0, [0, 0, 0], 0, clientResult=prediction[0])

        return prediction, result

    def test_server_rolls_the_damage_the_client_predicts(self):
        player = self.makePlayer(stacks={InventoryType.PistolWeaponL1: 1, InventoryType.PistolShoot: 2},
            weaponId=InventoryType.PistolWeaponL1)
        enemy = self.makeEnemy(level=14)
        self.clientRandom = BattleRandom(player.doId)
        results = set()
        for _ in range(25):
            hp = enemy.hp
            (clientResult, attackerEffects, targetEffects, areaEffects), result = self.attackBothSides(
                player, enemy, InventoryType.PistolShoot)

            self.assertEqual(result[2], clientResult)
            self.assertEqual(result[6], targetEffects)
            results.add(clientResult)
            if clientResult == WeaponGlobals.RESULT_HIT:
                self.assertEqual(enemy.hp, hp + targetEffects[0])
            else:
                self.assertEqual(enemy.hp, hp)

        # the rolls really are random, a higher level enemy is missed now and then
        self.assertEqual(results, {WeaponGlobals.RESULT_HIT, WeaponGlobals.RESULT_MISS})
        player.sendUpdateToAvatarId.assert_not_called()

    def test_area_targets_share_one_result(self):
        player = self.makePlayer(stacks={InventoryType.CutlassWeaponL1: 1, InventoryType.CutlassSweep: 2})
        enemies = [self.makeEnemy(doId=200 + i, level=8) for i in range(3)]
        self.clientRandom = BattleRandom(player.doId)
        (clientResult, attackerEffects, targetEffects, areaEffects), result = self.attackBothSides(
            player, enemies[0], InventoryType.CutlassSweep, areaTargets=enemies[1:])

        skillId, ammoSkillId, skillResult, targetId, areaIdList, aEffects, tEffects, areaIdEffects = result[:8]
        self.assertEqual(skillResult, WeaponGlobals.RESULT_HIT)
        self.assertEqual(targetId, enemies[0].doId)
        self.assertEqual(areaIdList, [enemies[1].doId, enemies[2].doId])
        self.assertEqual(areaIdEffects, areaEffects)
        for enemy, effects in zip(enemies, [targetEffects] + areaEffects):
            self.assertLess(effects[0], 0)
            self.assertEqual(enemy.hp, 5000 + effects[0])

    def test_area_targets_out_of_the_skill_area_are_ignored(self):
        player = self.makePlayer(stacks={InventoryType.CutlassWeaponL1: 1, InventoryType.CutlassHack: 2})
        enemies = [self.makeEnemy(doId=200 + i) for i in range(2)]
        result = self.manager.getTargetedSkillResult(player, enemies[0], InventoryType.CutlassHack, 0,
            [enemies[1].doId], 0, [0, 0, 0], 0)

        # hack has no area, only the target is hit
        self.assertEqual(result[4], [])
        self.assertEqual(result[7], [])
        self.assertEqual(enemies[1].hp, 5000)

    def test_mismatched_rolls_resync_the_battle_random(self):
        player = self.makePlayer(stacks={InventoryType.PistolWeaponL1: 1, InventoryType.PistolShoot: 2},
            weaponId=InventoryType.PistolWeaponL1)
        enemy = self.makeEnemy(level=14)
        player.battleRandom = Mock(getRandom=Mock(return_value=0.99))
        result = self.manager.getTargetedSkillResult(player, enemy, InventoryType.PistolShoot, 0, [], 0, [0, 0, 0], 0,
            clientResult=WeaponGlobals.RESULT_HIT)

        self.assertEqual(result[2], WeaponGlobals.RESULT_MISS)
        player.battleRandom.resync.assert_called_once_with()
        player.sendUpdateToAvatarId.assert_called_once_with(player.doId, 'battleRandomSync', [])

    def test_spawn_protected_targets_are_missed(self):
        player = self.makePlayer(stacks={InventoryType.CutlassWeaponL1: 1, InventoryType.CutlassHack: 2})
        enemy = self.makeEnemy()
        enemy.addSkillEffect(WeaponGlobals.C_SPAWN, 10, enemy.doId)
        result = self.manager.getTargetedSkillResult(player, enemy, InventoryType.CutlassHack, 0, [], 0, [0, 0, 0], 0)
        self.assertEqual(result[2], WeaponGlobals.RESULT_MISS)
        self.assertEqual(enemy.hp, 5000)

    def test_parried_attacks_deal_no_damage(self):
        player = self.makePlayer(stacks={InventoryType.CutlassWeaponL1: 1, InventoryType.CutlassHack: 2})
        enemy = self.makeEnemy()
        self.manager.willWeaponHit = Mock(return_value=WeaponGlobals.RESULT_PARRY)
        result = self.manager.getTargetedSkillResult(player, enemy, InventoryType.CutlassHack, 0, [], 0, [0, 0, 0], 0)
        self.assertEqual(result[2], WeaponGlobals.RESULT_PARRY)
        self.assertEqual(enemy.hp, 5000)
        self.assertEqual(player.hp, 500)

    def test_stunned_avatars_cannot_use_skills(self):
        player = self.makePlayer(stacks={InventoryType.CutlassWeaponL1: 1, InventoryType.CutlassHack: 2})
        player.hasWeapon = Mock(return_value=True)
        player.isSkillRecharging = Mock(return_value=False)
        self.assertTrue(self.manager.canUseSkill(player, InventoryType.CutlassHack, 0))
        player.addSkillEffect(WeaponGlobals.C_STUN, 3, 200)
        self.assertFalse(self.manager.canUseSkill(player, InventoryType.CutlassHack, 0))
        self.assertFalse(self.manager.canUseSkill(player, InventoryType.UseItem, InventoryType.Potion1))


@unittest.skipUnless(HAVE_RESOURCES, 'the game resources are required')
class StatusEffectTests(CombatFixture):

    def hit(self, attacker, target, skillId, ammoSkillId=0):
        effects = WeaponGlobals.getAttackEffects(skillId, ammoSkillId)[1]
        self.manager.applySkillHit(attacker, target, list(effects), skillId, ammoSkillId)

    def test_attack_modifiers_are_not_status_effects(self):
        player = self.makePlayer(weaponId=InventoryType.PistolWeaponL1)
        enemy = self.makeEnemy()
        self.hit(player, enemy, InventoryType.PistolShoot, InventoryType.PistolSilverShot)
        self.assertEqual(enemy.getSkillEffects(), [])

    def test_buffs_are_sent_the_way_the_buff_tray_reads_them(self):
        player = self.makePlayer(weaponId=InventoryType.PistolWeaponL1)
        enemy = self.makeEnemy()
        self.hit(player, enemy, InventoryType.PistolShoot, InventoryType.PistolVenomShot)
        effectId, duration, timestamp, attackerId = enemy.getSkillEffects()[0]
        self.assertEqual((effectId, duration, attackerId), (WeaponGlobals.C_POISON, 10, player.doId))
        self.assertTrue(-32768 <= timestamp <= 32767)
        enemy.sendUpdate.assert_called_with('setSkillEffects', [enemy.getSkillEffects()])

    def test_effect_duration_grows_with_the_skill_rank(self):
        player = self.makePlayer(stacks={InventoryType.PistolVenomShot: 5}, weaponId=InventoryType.PistolWeaponL1)
        enemy = self.makeEnemy()
        self.hit(player, enemy, InventoryType.PistolShoot, InventoryType.PistolVenomShot)

        # rank 4 venom shot: 10 + 10 * 3 / 4 seconds, see SkillButton.createHelpFrame
        self.assertEqual(enemy.getSkillEffects()[0][1], 17)
        self.clock.now += 17.4
        enemy.updateSkillEffects(self.clock.now)
        self.assertTrue(enemy.hasSkillEffect(WeaponGlobals.C_POISON))
        self.clock.now += 0.2
        enemy.updateSkillEffects(self.clock.now)
        self.assertFalse(enemy.hasSkillEffect(WeaponGlobals.C_POISON))

    def test_damage_over_time_recurs_until_it_expires(self):
        player = self.makePlayer(weaponId=InventoryType.PistolWeaponL1)
        enemy = self.makeEnemy()
        self.hit(player, enemy, InventoryType.PistolShoot, InventoryType.PistolVenomShot)
        hp = enemy.hp
        poison = WeaponGlobals.getEffects(WeaponGlobals.C_POISON)[0]
        self.clock.now += 1.9
        enemy.updateSkillEffects(self.clock.now)
        self.assertEqual(enemy.hp, hp)

        # venom shot poisons for 10 seconds, recurring every 2 seconds
        self.clock.now += 0.1
        enemy.updateSkillEffects(self.clock.now)
        self.assertEqual(enemy.hp, hp + poison)
        self.clock.now += 20
        enemy.updateSkillEffects(self.clock.now)
        self.assertEqual(enemy.hp, hp + poison * 5)
        self.assertEqual(enemy.getSkillEffects(), [])

    def test_effects_stack_per_attacker(self):
        enemy = self.makeEnemy()
        players = [self.makePlayer(doId=100 + i, weaponId=InventoryType.PistolWeaponL1) for i in range(4)]
        for player in players:
            self.hit(player, enemy, InventoryType.PistolShoot, InventoryType.PistolVenomShot)

        # poison stacks three times, see WeaponGlobals.getBuffStackNumber
        self.assertEqual(enemy.getSkillEffectAttackers(WeaponGlobals.C_POISON), [100, 101, 102])

        # the same attacker renews it's poison instead of stacking it
        self.clock.now += 5
        self.hit(players[0], enemy, InventoryType.PistolShoot, InventoryType.PistolVenomShot)
        self.assertEqual(sorted(enemy.getSkillEffectAttackers(WeaponGlobals.C_POISON)), [100, 101, 102])
        self.clock.now += 6
        enemy.updateSkillEffects(self.clock.now)
        self.assertEqual(enemy.getSkillEffectAttackers(WeaponGlobals.C_POISON), [100])

    def test_stun_takes_the_swiftness_until_it_wears_off(self):
        enemy = self.makeEnemy()
        player = self.makePlayer()
        self.hit(enemy, player, InventoryType.CutlassBrawl)
        self.assertEqual(player.swiftness, 0)
        self.clock.now += 2.5
        player.updateSkillEffects(self.clock.now)
        self.assertEqual(player.swiftness, 1)

    def test_stun_immunity(self):
        enemy = self.makeEnemy()
        player = self.makePlayer()
        player.addSkillEffect(WeaponGlobals.C_UNSTUN, 10, player.doId)
        self.hit(enemy, player, InventoryType.CutlassBrawl)
        self.assertFalse(player.hasSkillEffect(WeaponGlobals.C_STUN))

    def test_slow_and_ignore_pain(self):
        enemy = self.makeEnemy()
        player = self.makePlayer(stacks={InventoryType.GrenadeIgnorePain: 2})
        self.hit(enemy, player, InventoryType.DaggerAsp)
        self.assertEqual(player.stunMod, player.SlowStunMod)

        # rank 1 ignore pain shortens the 6 second slow by 10%
        self.clock.now += 5.5
        player.updateSkillEffects(self.clock.now)
        self.assertEqual(player.stunMod, 0)

    def test_cure_removes_hostile_effects(self):
        enemy = self.makeEnemy()
        player = self.makePlayer()
        healer = self.makePlayer(doId=300, weaponId=InventoryType.DollWeaponL1)
        self.hit(enemy, player, InventoryType.DaggerAsp)
        player.addSkillEffect(WeaponGlobals.C_SPAWN, 10, player.doId)
        self.hit(healer, player, InventoryType.DollCure)
        self.assertEqual(player.getSkillEffectIds(), [WeaponGlobals.C_SPAWN])
        self.assertEqual(player.stunMod, 0)

    def test_defeated_avatars_lose_their_effects(self):
        player = self.makePlayer(weaponId=InventoryType.PistolWeaponL1)
        enemy = self.makeEnemy(hp=30)
        self.hit(player, enemy, InventoryType.PistolShoot, InventoryType.PistolVenomShot)
        self.clock.now += 4
        enemy.updateSkillEffects(self.clock.now)
        self.assertEqual(enemy.hp, 0)
        enemy.updateSkillEffects(self.clock.now)
        self.assertEqual(enemy.getSkillEffects(), [])


@unittest.skipUnless(HAVE_RESOURCES, 'the game resources are required')
class VoodooTests(CombatFixture):

    def test_attune_rank_limits_the_attuned_targets(self):
        player = self.makePlayer(stacks={InventoryType.DollAttune: 2}, weaponId=InventoryType.DollWeaponL1)
        enemies = [self.makeEnemy(doId=200 + i) for i in range(3)]
        self.manager.attuneTarget(player, enemies[0])
        self.manager.attuneTarget(player, enemies[1])
        self.assertEqual(player.getStickyTargets(), [enemies[1].doId])
        self.assertFalse(enemies[0].hasSkillEffect(WeaponGlobals.C_ATTUNE))
        self.assertTrue(enemies[1].hasSkillEffect(WeaponGlobals.C_ATTUNE))

        player.inventory.stacks[InventoryType.DollAttune] = 3
        self.manager.attuneTarget(player, enemies[2])
        self.assertEqual(player.getStickyTargets(), [enemies[1].doId, enemies[2].doId])

    def test_removing_sticky_targets_unattunes_them(self):
        player = self.makePlayer(stacks={InventoryType.DollAttune: 2}, weaponId=InventoryType.DollWeaponL1)
        enemy = self.makeEnemy()
        enemy.addSkillEffect(WeaponGlobals.C_ATTUNE, 0, 999)
        self.manager.attuneTarget(player, enemy)
        player.requestRemoveStickyTargets([enemy.doId])
        self.assertEqual(player.getStickyTargets(), [])
        self.assertEqual(enemy.getSkillEffectAttackers(WeaponGlobals.C_ATTUNE), [999])

    def test_hexes_only_hit_attuned_targets(self):
        player = self.makePlayer(stacks={InventoryType.DollWeaponL1: 1, InventoryType.DollAttune: 2,
            InventoryType.DollPoke: 2}, weaponId=InventoryType.DollWeaponL1)
        enemies = [self.makeEnemy(doId=200 + i) for i in range(2)]
        self.manager.attuneTarget(player, enemies[0])
        result = self.manager.getTargetedSkillResult(player, None, InventoryType.DollPoke, 0,
            [enemies[0].doId, enemies[1].doId], 0, [0, 0, 0], 0)

        self.assertEqual(result[4], [enemies[0].doId])
        self.assertLess(enemies[0].hp, 5000)
        self.assertEqual(enemies[1].hp, 5000)

    def test_unattune_skills_shatter_attunements(self):
        doll = self.makePlayer(stacks={InventoryType.DollAttune: 2}, weaponId=InventoryType.DollWeaponL1)
        attacker = self.makePlayer(doId=300, weaponId=InventoryType.DaggerWeaponL1)
        enemy = self.makeEnemy()
        self.manager.attuneTarget(doll, enemy)
        self.manager.applySkillHit(attacker, doll, list(WeaponGlobals.getAttackEffects(InventoryType.DaggerAsp)[1]),
            InventoryType.DaggerAsp, 0)

        self.assertEqual(doll.getStickyTargets(), [])
        self.assertFalse(enemy.hasSkillEffect(WeaponGlobals.C_ATTUNE))
        self.assertTrue(doll.hasSkillEffect(WeaponGlobals.C_VOODOO_STUN))


class PlayerTeamTests(unittest.TestCase):

    def test_players_are_on_the_player_team(self):
        player = DistributedPlayerPirateAI(MagicMock())
        self.assertEqual(player.getTeam(), PiratesGlobals.PLAYER_TEAM)

        other = DistributedPlayerPirateAI(MagicMock())
        manager = BattleManagerAI.__new__(BattleManagerAI)
        self.assertTrue(manager.isPVP(player, other))


if __name__ == '__main__':
    unittest.main()
