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
from pirates.battle.BattleSkillDiaryAI import BattleSkillDiaryAI
from pirates.battle.ComboDiaryAI import ComboDiaryAI
from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.battle.EnemySkills import EnemySkills
from pirates.distributed.TargetManagerAI import TargetManagerAI
from pirates.pirate import AvatarTypes
from pirates.pirate.BattleNPCGameFSMAI import BattleNPCGameFSMAI
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


def makeAvatar(cls=DistributedBattleAvatarAI, doId=100, level=10, hp=5000, isNpc=False):
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
    avatar.getWorld = Mock(return_value=Mock(getType=Mock(return_value=PiratesGlobals.INSTANCE_MAIN)))
    avatar.getDamagable = Mock(return_value=True)
    avatar.getInventory = Mock(return_value=FakeInventory())
    avatar.b_setGameState = Mock()
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
    player._pvpTeam = 0
    player._siegeTeam = 0
    player.isPaid = Mock(return_value=True)
    player.hasTempDoubleXPReward = Mock(return_value=False)
    player.sendUpdateToAvatarId = Mock()
    player.hasWeapon = Mock(return_value=True)
    return player


def makeEnemy(doId=200, level=10):
    enemy = makeAvatar(doId=doId, isNpc=True, level=level)
    enemy.avatarType = AvatarTypes.EarthUndead[0]
    enemy.getMonsterDmg = Mock(return_value=30)
    enemy.gameFSM = Mock(state='LandRoam', getCurrentOrNextState=Mock(return_value='LandRoam'))
    return enemy


class BattleFixture(unittest.TestCase):

    def setUp(self):
        self.now = 1000.0
        self.manager = BattleManagerAI.__new__(BattleManagerAI)
        self.manager.getBattleTime = lambda: self.now
        self.targetMgr = TargetManagerAI.__new__(TargetManagerAI)
        self.targetMgr.objectDict = {}
        self.targetMgr.projectiles = {}
        self.air = SimpleNamespace(doId2do={}, battleMgr=self.manager, targetMgr=self.targetMgr,
            newsManager=Mock(isHolidayActive=Mock(return_value=False)))
        self.manager.air = self.air
        self.targetMgr.air = self.air
        self.avatars = []
        self.clockPatch = patch.object(builtins, 'globalClock', Mock(getFrameTime=lambda: self.now,
            getRealTime=lambda: self.now))
        self.clockPatch.start()

    def tearDown(self):
        self.clockPatch.stop()
        for avatar in self.avatars:
            avatar.clearSkillEffects()

    def track(self, avatar):
        avatar.air = self.air
        avatar.getSkillEffectTime = lambda: self.now
        avatar.battleSkillDiary = BattleSkillDiaryAI(self.air, avatar)
        avatar.comboDiary = ComboDiaryAI(self.air, avatar)
        self.air.doId2do[avatar.doId] = avatar
        self.avatars.append(avatar)
        return avatar

    def makePlayer(self, doId=100, **kwargs):
        return self.track(makePlayer(doId=doId, **kwargs))

    def makeEnemy(self, doId=200, **kwargs):
        enemy = self.track(makeEnemy(doId=doId, **kwargs))
        self.targetMgr.addTarget(enemy)
        return enemy

    def hit(self, attacker, target, skillId=InventoryType.CutlassHack, ammoSkillId=0, areaTargets=(), result=None):
        self.manager.willWeaponHit = Mock(return_value=WeaponGlobals.RESULT_HIT if result is None else result)
        return self.manager.getTargetedSkillResult(attacker, target, skillId, ammoSkillId,
            [areaTarget.doId for areaTarget in areaTargets], 0, [0, 0, 0], 0)


@unittest.skipUnless(HAVE_RESOURCES, 'the game resources are required')
class PlayerTargetTests(BattleFixture):

    def makePvpPlayers(self):
        world = Mock(getType=Mock(return_value=PiratesGlobals.INSTANCE_PVP), isDamageAllowed=Mock(return_value=True))
        attacker = self.makePlayer(doId=100, stacks={InventoryType.CutlassHack: 2})
        target = self.makePlayer(doId=101, hp=500)
        for player in (attacker, target):
            player.getWorld = Mock(return_value=world)

        return attacker, target

    def test_players_attacked_by_players_become_targets(self):
        attacker, target = self.makePvpPlayers()
        self.hit(attacker, target)
        self.assertTrue(self.targetMgr.hasTarget(target.doId))
        self.assertEqual(self.targetMgr.getAttackers(target.doId), [attacker.doId])

        # players never have their game state forced by being attacked...
        target.b_setGameState.assert_not_called()
        self.assertEqual(attacker.getCurrentTarget(), target.doId)

    def test_friendly_skills_never_make_an_attacker(self):
        attacker, target = self.makePvpPlayers()
        attacker.currentWeaponId = InventoryType.DollWeaponL1
        attacker.inventory.stacks[InventoryType.DollHeal] = 2
        self.hit(attacker, target, InventoryType.DollHeal)
        self.assertFalse(self.targetMgr.hasTarget(target.doId))

    def test_enemies_are_never_registered_as_attackers(self):
        enemy = self.makeEnemy()
        player = self.makePlayer(doId=100)
        enemy.currentWeaponId = InventoryType.CutlassWeaponL1
        enemy.isWeaponDrawn = True
        self.hit(enemy, player)
        self.assertFalse(self.targetMgr.hasTarget(player.doId))
        self.assertEqual(self.targetMgr.getAttackers(enemy.doId), [])

    def test_enemies_attacked_join_the_battle(self):
        enemy = self.makeEnemy()
        player = self.makePlayer(stacks={InventoryType.CutlassHack: 2})
        self.hit(player, enemy)
        enemy.b_setGameState.assert_called_once_with('Battle')
        self.assertEqual(self.targetMgr.getAttackers(enemy.doId), [player.doId])

    def test_clearing_a_defeated_player_clears_its_attackers(self):
        attacker, target = self.makePvpPlayers()
        self.hit(attacker, target)
        self.targetMgr.clearTarget(target)
        self.assertEqual(self.targetMgr.getAttackers(target.doId), [])
        self.assertEqual(attacker.getCurrentTarget(), 0)
        self.assertEqual(attacker.battleSkillDiary.getSkills(target.doId), {})


@unittest.skipUnless(HAVE_RESOURCES, 'the game resources are required')
class SkillDiaryTests(BattleFixture):

    def test_breaking_combat_keeps_the_reputation_of_parallel_fights(self):
        player = self.makePlayer(stacks={InventoryType.CutlassHack: 2})
        first = self.makeEnemy(doId=200)
        second = self.makeEnemy(doId=201)
        self.hit(player, first)
        self.hit(player, second)
        self.assertGreater(player.battleSkillDiary.getSkill(InventoryType.CutlassHack, second.doId)[2], 0)

        # the first enemy breaks combat, the reputation earned against the second is kept...
        self.targetMgr.clearTarget(first)
        self.assertIsNone(player.battleSkillDiary.getSkill(InventoryType.CutlassHack, first.doId))
        reputation = player.battleSkillDiary.getSkill(InventoryType.CutlassHack, second.doId)[2]
        self.assertGreater(reputation, 0)

        player.d_sendReputationMessage = Mock()
        player.getInventory = Mock(return_value=MagicMock(getReputation=Mock(return_value=0),
            getOverallRep=Mock(return_value=0)))
        player.getLevel = Mock(return_value=1)
        self.air.questMgr = Mock()
        with patch.object(battle_manager_module.random, 'random', return_value=1.0):
            self.manager.rewardAttacker(player, second)

        self.assertEqual(player.d_sendReputationMessage.call_args[0][2], [int(reputation)])

    def test_area_targets_are_credited_seperately(self):
        player = self.makePlayer(stacks={InventoryType.CutlassSweep: 2})
        enemies = [self.makeEnemy(doId=200 + i) for i in range(2)]
        self.manager.getRelativePosition = Mock(return_value=0)
        self.hit(player, enemies[0], InventoryType.CutlassSweep, areaTargets=enemies[1:])
        for enemy in enemies:
            self.assertIn(player.doId, self.targetMgr.getAttackers(enemy.doId))
            self.assertGreater(player.battleSkillDiary.getSkill(InventoryType.CutlassSweep, enemy.doId)[2], 0)

    def test_combos_are_recorded_by_the_target(self):
        player = self.makePlayer(stacks={InventoryType.CutlassHack: 2})
        first = self.makeEnemy(doId=200)
        second = self.makeEnemy(doId=201)
        self.hit(player, first)
        self.assertEqual(len(first.comboDiary.getCombos(player.doId)), 1)
        self.assertEqual(second.comboDiary.getCombos(player.doId), [])

        self.targetMgr.removeAttacker(player, first)
        self.assertEqual(first.comboDiary.getCombos(player.doId), [])

    def test_current_skill_is_tracked_per_target(self):
        diary = BattleSkillDiaryAI(None, None)
        diary.addSkill(0, InventoryType.PistolShoot, 0, 200)
        diary.addSkill(0, InventoryType.CutlassHack, 0, 201)
        self.assertEqual(diary.getCurrentSkill(), InventoryType.CutlassHack)
        self.assertEqual(diary.getCurrentSkill(200), InventoryType.PistolShoot)
        diary.clear(201)
        self.assertEqual(diary.getCurrentSkill(201), 0)
        self.assertTrue(diary.hasSkill(InventoryType.PistolShoot, 200))


@unittest.skipUnless(HAVE_RESOURCES, 'the game resources are required')
class CannonSkillTests(BattleFixture):

    def test_grape_shot_hits_without_a_drawn_weapon(self):
        player = self.makePlayer()
        player.isWeaponDrawn = False
        enemy = self.makeEnemy()
        self.manager.getRelativePosition = Mock(return_value=10)

        # the cannon has fired the shot...
        self.targetMgr.addProjectile(player.doId, InventoryType.CannonShoot, InventoryType.CannonGrapeShot, 0)
        result = self.hit(player, None, InventoryType.CannonShoot, InventoryType.CannonGrapeShot, areaTargets=[enemy])
        self.assertEqual(result[2], WeaponGlobals.RESULT_HIT)
        self.assertEqual(result[4], [enemy.doId])
        self.assertLess(enemy.hp, 5000)

        # every shot only hits once...
        self.assertFalse(self.targetMgr.hasProjectile(player.doId, InventoryType.CannonShoot,
            InventoryType.CannonGrapeShot))
        self.assertIsNone(self.hit(player, None, InventoryType.CannonShoot, InventoryType.CannonGrapeShot,
            areaTargets=[enemy]))

    def test_grape_shot_never_fired_has_no_result(self):
        player = self.makePlayer()
        enemy = self.makeEnemy()
        self.assertIsNone(self.hit(player, enemy, InventoryType.CannonShoot, InventoryType.CannonGrapeShot))
        self.assertEqual(enemy.hp, 5000)

    def test_cannon_records_the_fired_shot(self):
        from pirates.battle.DistributedPCCannonAI import DistributedPCCannonAI
        player = self.makePlayer(stacks={InventoryType.CannonGrapeShot: 2, WeaponGlobals.getSkillAmmoInventoryId(InventoryType.CannonGrapeShot): 5})
        cannon = DistributedPCCannonAI.__new__(DistributedPCCannonAI)
        cannon.air = SimpleNamespace(doId2do=self.air.doId2do, targetMgr=self.targetMgr, battleMgr=self.manager,
            getAvatarIdFromSender=lambda: player.doId, writeServerEvent=Mock())
        cannon.lastFireTimes = {}
        cannon.userId = player.doId
        cannon.doId = 700
        cannon.sendUpdate = Mock()
        cannon.requestProjectileSkill(InventoryType.CannonShoot, InventoryType.CannonGrapeShot, [0] * 6, 0, 0)
        self.assertTrue(self.targetMgr.hasProjectile(player.doId, InventoryType.CannonShoot,
            InventoryType.CannonGrapeShot))


@unittest.skipUnless(HAVE_RESOURCES, 'the game resources are required')
class VolleyTests(BattleFixture):

    def makeGunner(self, weaponId=InventoryType.PistolWeaponL2):
        return self.makePlayer(stacks={InventoryType.PistolShoot: 2}, weaponId=weaponId)

    def test_volley_must_be_reloaded(self):
        player = self.makeGunner()
        volley = WeaponGlobals.getWeaponVolley(player.currentWeaponId)
        self.assertEqual(volley, 2)
        for _ in range(volley):
            self.assertTrue(self.manager.requestSkillUse(player, InventoryType.PistolShoot, 0))
            self.now += 1.0

        self.assertFalse(self.manager.requestSkillUse(player, InventoryType.PistolShoot, 0))

        # reloading takes the reload animation, see CombatAnimations.getPistolReloadAnim...
        self.assertTrue(self.manager.requestSkillUse(player, EnemySkills.PISTOL_RELOAD, 0))
        self.now += 0.1
        self.assertFalse(self.manager.requestSkillUse(player, InventoryType.PistolShoot, 0))
        self.now += WeaponGlobals.getAnimTime(EnemySkills.PISTOL_RELOAD)
        self.assertTrue(self.manager.requestSkillUse(player, InventoryType.PistolShoot, 0))

    def test_reload_is_shown_to_everyone(self):
        player = self.makeGunner()
        result = self.manager.getTargetedSkillResult(player, None, EnemySkills.PISTOL_RELOAD, 0, [], 0, [0, 0, 0], 0)
        self.assertEqual(result[0], EnemySkills.PISTOL_RELOAD)
        self.assertEqual(result[2], WeaponGlobals.RESULT_HIT)

    def test_swords_have_no_volley(self):
        player = self.makePlayer(stacks={InventoryType.CutlassHack: 2})
        for _ in range(10):
            self.assertTrue(self.manager.requestSkillUse(player, InventoryType.CutlassHack, 0))
            self.now += 1.0

        self.assertFalse(self.manager.requestSkillUse(player, EnemySkills.PISTOL_RELOAD, 0))

    def test_shots_spend_ammo(self):
        ammoId = WeaponGlobals.getSkillAmmoInventoryId(InventoryType.PistolVenomShot)
        player = self.makePlayer(stacks={InventoryType.PistolShoot: 2, InventoryType.PistolVenomShot: 2,
            ammoId: 3}, weaponId=InventoryType.PistolWeaponL3)
        self.assertTrue(self.manager.requestSkillUse(player, InventoryType.PistolShoot, InventoryType.PistolVenomShot))
        self.assertEqual(player.inventory.stacks[ammoId], 2)

    def test_changing_grenades_readies_a_new_grenade(self):
        player = self.makePlayer(weaponId=InventoryType.GrenadeWeaponL1)
        player.weaponVolley = (1, None, 0)
        player.b_setCurrentAmmo = Mock()
        player.requestCurrentAmmo(0)
        self.assertEqual(self.manager.getVolleyShots(player), 0)


@unittest.skipUnless(HAVE_RESOURCES, 'the game resources are required')
class ComboChainTests(BattleFixture):

    def setUp(self):
        BattleFixture.setUp(self)
        self.player = self.makePlayer(stacks={InventoryType.CutlassHack: 2, InventoryType.CutlassSlash: 2,
            InventoryType.CutlassCleave: 2})
        self.enemy = self.makeEnemy()

    def attack(self, skillId, clientResult=WeaponGlobals.RESULT_HIT):
        self.assertTrue(self.manager.requestSkillUse(self.player, skillId, 0))
        self.manager.willWeaponHit = Mock(return_value=WeaponGlobals.RESULT_HIT)
        result = self.manager.getTargetedSkillResult(self.player, self.enemy, skillId, 0, [], 0, [0, 0, 0], 0,
            clientResult=clientResult)
        return result[2]

    def test_chain_in_time_hits(self):
        self.assertEqual(self.attack(InventoryType.CutlassHack), WeaponGlobals.RESULT_HIT)
        self.now += WeaponGlobals.getAnimTime(InventoryType.CutlassHack) * 0.7
        self.assertEqual(self.attack(InventoryType.CutlassSlash), WeaponGlobals.RESULT_HIT)
        self.now += WeaponGlobals.getAnimTime(InventoryType.CutlassSlash) * 0.7
        self.assertEqual(self.attack(InventoryType.CutlassCleave), WeaponGlobals.RESULT_HIT)

    def test_chain_after_the_attack_finished_misses(self):
        self.attack(InventoryType.CutlassHack)
        self.now += WeaponGlobals.getAnimTime(InventoryType.CutlassHack) + self.manager.ComboChainTolerance + 0.5
        hp = self.enemy.hp
        self.assertEqual(self.attack(InventoryType.CutlassSlash), WeaponGlobals.RESULT_MISS)
        self.assertEqual(self.enemy.hp, hp)

        # the chain broke, so the client's hit was never compared with our rolls...
        self.player.sendUpdateToAvatarId.assert_not_called()

    def test_chain_out_of_order_misses(self):
        self.attack(InventoryType.CutlassHack)
        self.now += 0.5
        self.assertEqual(self.attack(InventoryType.CutlassCleave), WeaponGlobals.RESULT_MISS)

    def test_mistimed_attacks_miss_without_a_resync(self):
        self.attack(InventoryType.CutlassHack)
        self.now += 0.1
        hp = self.enemy.hp
        self.assertEqual(self.attack(InventoryType.CutlassSlash, clientResult=WeaponGlobals.RESULT_MISS),
            WeaponGlobals.RESULT_MISS)

        self.assertEqual(self.enemy.hp, hp)
        self.player.sendUpdateToAvatarId.assert_not_called()

    def test_first_attack_of_the_chain_is_always_timed(self):
        self.now += 100
        self.assertEqual(self.attack(InventoryType.CutlassHack), WeaponGlobals.RESULT_HIT)


class ShipSkillEffectTests(unittest.TestCase):

    def test_renewed_effects_restart_the_buff(self):
        from pirates.ship.DistributedShipAI import DistributedShipAI
        ship = DistributedShipAI.__new__(DistributedShipAI)
        ship.skillEffects = []
        ship._skillEffectTasks = {}
        ship.doId = 1000
        ship.uniqueName = lambda name: '%s-1000' % name
        sent = []
        ship.d_setSkillEffects = lambda skillEffects: sent.append([list(effect) for effect in skillEffects])
        try:
            ship.addSkillEffect(WeaponGlobals.C_FULLSAIL, 10.5, 42)
            ship.addSkillEffect(WeaponGlobals.C_FULLSAIL, 20, 42)
        finally:
            ship.clearSkillEffectTasks()

        # the old buff is removed first so the client's buff tray restarts it...
        self.assertEqual(sent[0][0][:2], [WeaponGlobals.C_FULLSAIL, 10])
        self.assertEqual(sent[1], [])
        self.assertEqual(len(sent[2]), 1)
        self.assertEqual(sent[2][0][1], 20)
        self.assertEqual(ship.getSkillEffects(), [WeaponGlobals.C_FULLSAIL])


class EnemyAttuneTests(unittest.TestCase):

    def test_exit_battle_unattunes_the_attuned_target(self):
        attuned = Mock(doId=300)
        current = Mock(doId=301)
        fsm = BattleNPCGameFSMAI.__new__(BattleNPCGameFSMAI)
        fsm.avatar = Mock(doId=200, currentTarget=attuned)
        fsm.air = SimpleNamespace(doId2do={300: attuned, 301: current})
        fsm.attunedTargetIds = []
        fsm.attuneTarget(attuned)
        attuned.addSkillEffect.assert_called_once_with(WeaponGlobals.C_ATTUNE, 0, 200)

        # we have switched over to another target since...
        fsm.avatar.currentTarget = current
        fsm.unattuneTargets()
        attuned.removeSkillEffect.assert_called_once_with(WeaponGlobals.C_ATTUNE, 200)
        current.removeSkillEffect.assert_not_called()
        self.assertEqual(fsm.attunedTargetIds, [])
