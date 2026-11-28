import builtins
import importlib
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, call, patch

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')


def _ensureWeaponGlobals():
    # WeaponGlobals reads WeaponGlobals.pkl from the game resources, which
    # are not available to the unit tests, so stub out what PVPGlobals needs.
    try:
        importlib.import_module('pirates.battle.WeaponGlobals')
        return
    except (IOError, OSError):
        pass

    weaponGlobals = types.ModuleType('pirates.battle.WeaponGlobals')
    weaponGlobals.getAttackHullHP = lambda *args: 0
    weaponGlobals.getAttackSailHP = lambda *args: 0
    weaponGlobals.HULL_HP_INDEX = 0
    weaponGlobals.SAIL_HP_INDEX = 1
    weaponGlobals.WEAPON_MOVIE_CLEAR = 0
    weaponGlobals.WEAPON_MOVIE_START = 1
    weaponGlobals.WEAPON_MOVIE_STOP = 2
    setattr(weaponGlobals, '__skillInfo', {})
    sys.modules['pirates.battle.WeaponGlobals'] = weaponGlobals
    importlib.import_module('pirates.battle').WeaponGlobals = weaponGlobals


_ensureWeaponGlobals()

from pirates.piratesbase import PiratesGlobals
from pirates.pvp import PVPGlobals
from pirates.pvp.SiegeManagerAI import SiegeManagerAI
from pirates.pvp.SiegeAnnouncerAI import SiegeAnnouncerAI
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.ship import ShipGlobals


class FakeTeamable:

    def __init__(self, doId, siegeTeam=0):
        self.doId = doId
        self._siegeTeam = siegeTeam
        self.b_setSiegeTeam = Mock(side_effect=self._setSiegeTeam)

    def _setSiegeTeam(self, team):
        self._siegeTeam = team

    def getSiegeTeam(self):
        return self._siegeTeam


class FakeShip(FakeTeamable):

    def __init__(self, doId, shipClass=ShipGlobals.INTERCEPTORL1, crew=(), name='Ship', siegeTeam=0):
        FakeTeamable.__init__(self, doId, siegeTeam)
        self.shipClass = shipClass
        self.crew = list(crew)
        self.name = name
        self.hp = 100
        self.maxHp = 1000
        self.sp = 100
        self.maxSp = 1000
        self.pos = (0, 0, 0)

    def getShipClass(self):
        return self.shipClass

    def getCrew(self):
        return self.crew

    def getName(self):
        return self.name

    def getHp(self):
        return self.hp

    def getMaxHp(self):
        return self.maxHp

    def b_setHp(self, hp):
        self.hp = hp

    def getSp(self):
        return self.sp

    def getMaxSp(self):
        return self.maxSp

    def b_setSp(self, sp):
        self.sp = sp

    def getPos(self):
        return self.pos

    def hasCrewMember(self, avatarId):
        return avatarId in self.crew


class FakePlayerShip(FakeShip):

    def __init__(self, *args, **kwargs):
        FakeShip.__init__(self, *args, **kwargs)
        self.repairSpots = []

    def createRepairSpots(self):
        self.repairSpots = ['spot']

    def deleteRepairSpots(self):
        self.repairSpots = []


class FakeInventory:

    def __init__(self):
        self.stacks = {}

    def getStackQuantity(self, stackType):
        return self.stacks.get(stackType, 0)

    def b_setStackQuantity(self, stackType, quantity):
        self.stacks[stackType] = quantity


class FakeAvatar(FakeTeamable):

    def __init__(self, doId, name='Pirate'):
        FakeTeamable.__init__(self, doId)
        self.name = name
        self.inventory = FakeInventory()

    def getName(self):
        return self.name

    def getDISLid(self):
        return 1000 + self.doId

    def getInventory(self):
        return self.inventory

    def getCrewShipId(self):
        return getattr(self, 'crewShipId', 0)


class FakeLandAvatar(FakeAvatar):

    def __init__(self, doId, parent=None, pos=(0, 0, 0)):
        FakeAvatar.__init__(self, doId)
        self.parent = parent
        self.pos = pos
        self.hp = 0
        self.mojo = 0
        self.skillEffects = []

    def getParentObj(self):
        return self.parent

    def getPos(self):
        return self.pos

    def getMaxHp(self):
        return 100

    def getMaxMojo(self):
        return 50

    def b_setHp(self, hp):
        self.hp = hp

    def b_setMojo(self, mojo):
        self.mojo = mojo

    def addSkillEffect(self, effectId, duration, attackerId):
        self.skillEffects.append([effectId, duration, 0, attackerId])

    def removeSkillEffect(self, effectId):
        self.skillEffects = [effect for effect in self.skillEffects if effect[0] != effectId]


class SiegeManagerAITests(unittest.TestCase):

    def tearDown(self):
        taskMgr.removeTasksMatching('*-5000')

    def makeManager(self, *objects):
        manager = SiegeManagerAI.__new__(SiegeManagerAI)
        SiegeManagerAI.__init__(manager, SimpleNamespace(
            dclassesByName={'SiegeManagerAI': None},
            doId2do={obj.doId: obj for obj in objects},
            getAvatarExitEvent=lambda avatarId: 'distObjDelete-%d' % avatarId,
            getAvatarIdFromSender=Mock(return_value=0)))
        manager.doId = 5000
        manager.sendUpdate = Mock()
        manager.sendUpdateToAvatarId = Mock()
        manager.accept = Mock()
        manager.ignore = Mock()
        manager.announcer = Mock()
        manager._wantTeamBalance = True
        return manager

    def test_required_fields_match_dc(self):
        manager = self.makeManager()
        self.assertEqual(manager.getTeamsJoinable(), [[1, True], [2, True]])
        self.assertIn(manager.getPvpEnabled(), (0, 1, True, False))
        self.assertEqual(manager.getUseIslandRegen(), PVPGlobals.WantIslandRegen.getValue())
        self.assertEqual(manager.getUseRepairSpots(), PVPGlobals.WantShipRepairSpots.getValue())
        self.assertEqual(manager.getUseRepairKit(), PVPGlobals.WantShipRepairKit.getValue())

    def test_add_ship_sets_ship_and_crew_team(self):
        avatar = FakeAvatar(10)
        ship = FakeShip(20, crew=[10])
        manager = self.makeManager(avatar, ship)

        self.assertTrue(manager.addShipToTeam(ship, 1))

        ship.b_setSiegeTeam.assert_called_once_with(1)
        avatar.b_setSiegeTeam.assert_called_once_with(1)
        self.assertEqual(manager.getShipTeam(20), 1)
        self.assertEqual(manager.getTeamAvatars(1), [10])
        manager.accept.assert_any_call('distObjDelete-20', manager._handleShipDeleted, extraArgs=[20])

    def test_invalid_team_is_rejected(self):
        ship = FakeShip(20)
        manager = self.makeManager(ship)
        self.assertFalse(manager.addShipToTeam(ship, 3))
        ship.b_setSiegeTeam.assert_not_called()
        self.assertEqual(manager.getJoinDenialCode(0), PiratesGlobals.PrivateerBothTeamFull)

    def test_full_team_is_not_joinable(self):
        ships = [FakeShip(100 + i) for i in range(PVPGlobals.MaxPrivateerShipsPerTeam.getValue())]
        manager = self.makeManager(*ships)
        manager._teamBalanceMargin = 10000
        for ship in ships:
            manager.addShipToTeam(ship, 1)

        self.assertFalse(manager.teamIsJoinable(1))
        self.assertTrue(manager.teamIsJoinable(2))
        self.assertEqual(manager.getJoinDenialCode(1), PiratesGlobals.PrivateerSingleTeamFull)
        self.assertIsNone(manager.getJoinDenialCode(2))
        manager.sendUpdate.assert_called_with('setTeamsJoinable', [[[1, False], [2, True]]])

    def test_team_balance_margin_blocks_stronger_team(self):
        ship = FakeShip(20, shipClass=ShipGlobals.WARSHIPL3)
        manager = self.makeManager(ship)
        manager._teamBalanceMargin = 5
        manager.addShipToTeam(ship, 2)

        self.assertFalse(manager.teamIsJoinable(2))
        self.assertTrue(manager.teamIsJoinable(1))

        manager._wantTeamBalance = False
        self.assertTrue(manager.teamIsJoinable(2))

    def test_ship_delete_frees_team_slot(self):
        ship = FakeShip(20)
        manager = self.makeManager(ship)
        manager.addShipToTeam(ship, 1)
        manager._handleShipDeleted(20)
        self.assertEqual(manager.getShipTeam(20), 0)
        manager.ignore.assert_any_call('distObjDelete-20')

    def test_avatars_going_ashore_keep_their_team(self):
        avatar = FakeAvatar(10)
        other = FakeAvatar(11)
        ship = FakeShip(20, crew=[10])
        manager = self.makeManager(avatar, other, ship)
        manager.addShipToTeam(ship, 1)

        ship.crew = [11]
        manager._updateTeamsTask(SimpleNamespace())

        self.assertEqual(avatar.getSiegeTeam(), 1)
        self.assertEqual(other.getSiegeTeam(), 1)
        self.assertEqual(sorted(manager.getTeamAvatars(1)), [10, 11])

    def test_update_task_removes_avatars_that_joined_another_crew(self):
        avatar = FakeAvatar(10)
        ship = FakeShip(20, crew=[10])
        manager = self.makeManager(avatar, ship)
        manager.addShipToTeam(ship, 1)

        ship.crew = []
        avatar.crewShipId = 99
        manager._updateTeamsTask(SimpleNamespace())

        self.assertEqual(avatar.getSiegeTeam(), 0)
        self.assertEqual(manager.getTeamAvatars(1), [])

    def test_avatars_ashore_lose_their_team_with_their_ship(self):
        avatar = FakeAvatar(10)
        ship = FakeShip(20, crew=[10])
        manager = self.makeManager(avatar, ship)
        manager.addShipToTeam(ship, 1)

        ship.crew = []
        manager._handleShipDeleted(20)
        self.assertEqual(avatar.getSiegeTeam(), 0)
        self.assertEqual(manager.getTeamAvatars(1), [])

    def test_repair_spots_follow_team_and_setting(self):
        ship = FakePlayerShip(20)
        manager = self.makeManager(ship)
        manager._useRepairSpots = True
        manager.addShipToTeam(ship, 1)
        self.assertEqual(ship.repairSpots, ['spot'])

        manager.setUseRepairSpots(False)
        self.assertEqual(ship.repairSpots, [])
        manager.setUseRepairSpots(True)
        self.assertEqual(ship.repairSpots, ['spot'])

        manager.removeShipFromTeam(ship)
        self.assertEqual(ship.repairSpots, [])

    def test_repair_spots_are_not_created_while_disabled(self):
        ship = FakePlayerShip(20)
        manager = self.makeManager(ship)
        manager._useRepairSpots = False
        manager.addShipToTeam(ship, 1)
        self.assertEqual(ship.repairSpots, [])

    def test_repair_kit_heals_own_team_ship(self):
        avatar = FakeAvatar(10)
        ship = FakeShip(20, crew=[10])
        manager = self.makeManager(avatar, ship)
        manager._pvpEnabled = True
        manager._useRepairKit = False
        manager.addShipToTeam(ship, 1)
        avatar.inventory.stacks[InventoryType.ShipRepairKit] = 2

        self.assertFalse(manager.useShipRepairKit(avatar, ship))

        manager._useRepairKit = True
        with patch.object(PVPGlobals.RepairKitHp, 'getValue', return_value=250), \
                patch.object(PVPGlobals.RepairKitSp, 'getValue', return_value=50):
            self.assertTrue(manager.useShipRepairKit(avatar, ship))

        self.assertEqual(avatar.inventory.getStackQuantity(InventoryType.ShipRepairKit), 1)
        self.assertEqual(ship.hp, 350)
        self.assertEqual(ship.sp, 150)

        avatar.inventory.stacks[InventoryType.ShipRepairKit] = 0
        self.assertFalse(manager.useShipRepairKit(avatar, ship))

        # a ship which is not on the avatar's team cannot be repaired
        avatar.inventory.stacks[InventoryType.ShipRepairKit] = 1
        enemy = FakeShip(21, crew=[10])
        manager.air.doId2do[21] = enemy
        manager.addShipToTeam(enemy, 2)
        manager._avatar2team[10] = 1
        self.assertFalse(manager.useShipRepairKit(avatar, enemy))

    def test_sink_hp_bonus_depends_on_damage_done(self):
        attacker = FakeShip(20, name='A')
        assist = FakeShip(22, name='B')
        friendly = FakeShip(23, name='D')
        sunk = FakeShip(21, name='C')
        manager = self.makeManager(attacker, assist, friendly, sunk)
        manager.addShipToTeam(attacker, 2)
        manager.addShipToTeam(assist, 2)
        manager.addShipToTeam(friendly, 1)
        manager.addShipToTeam(sunk, 1)
        sunk.attackerDamage = {20: 300, 22: 100, 23: 500}

        manager.handleShipSunk(sunk, attacker, assist)

        bonus = PVPGlobals.SinkHpBonusPercent.getValue()
        self.assertEqual(attacker.hp, 100 + int(300 * bonus))
        self.assertEqual(assist.hp, 100 + int(100 * bonus))
        self.assertEqual(friendly.hp, 100)

    def test_defeated_privateer_respawns_invulnerable(self):
        island = SimpleNamespace(getZoneSphereCenter=lambda: [0, 0],
            getZoneSphereSize=lambda: [1000, 2000, 3000])
        avatar = FakeLandAvatar(10, island)
        ship = FakeShip(20, crew=[10])
        manager = self.makeManager(avatar, ship)
        manager.uniqueName = lambda name: '%s-5000' % name

        self.assertFalse(manager.handleAvatarDefeated(avatar))
        manager.addShipToTeam(ship, 1)
        self.assertTrue(manager.handleAvatarDefeated(avatar))
        self.assertTrue(taskMgr.hasTaskNamed('respawn-10-5000'))

        manager._respawnAvatar(10)
        self.assertEqual(avatar.hp, 100)
        self.assertEqual(avatar.mojo, 50)
        self.assertTrue(manager.isAvatarInvulnerable(10))
        self.assertEqual(len(avatar.skillEffects), 1)
        self.assertEqual(avatar.skillEffects[0][1], PVPGlobals.MainWorldInvulnerabilityDuration.getValue())

        # still within the island's cutoff sphere...
        task = SimpleNamespace()
        manager._checkInvulnerabilityCutoff(10, task)
        self.assertTrue(manager.isAvatarInvulnerable(10))

        # ...but not once they have left it
        avatar.pos = (5000, 0, 0)
        manager._checkInvulnerabilityCutoff(10, task)
        self.assertFalse(manager.isAvatarInvulnerable(10))
        self.assertEqual(avatar.skillEffects, [])

    def test_invulnerability_expires(self):
        avatar = FakeLandAvatar(10)
        ship = FakeShip(20, crew=[10])
        manager = self.makeManager(avatar, ship)
        manager.uniqueName = lambda name: '%s-5000' % name
        manager.addShipToTeam(ship, 1)
        manager.addInvulnerability(avatar)
        self.assertTrue(manager.isAvatarInvulnerable(10))
        manager._invulnerabilityExpired(10)
        self.assertFalse(manager.isAvatarInvulnerable(10))
        self.assertEqual(avatar.skillEffects, [])

    def test_team_chat_goes_to_team_members_only(self):
        sender = FakeAvatar(10, 'Jack')
        teammate = FakeAvatar(11)
        enemy = FakeAvatar(12)
        french = FakeShip(20, crew=[10, 11])
        spanish = FakeShip(21, crew=[12])
        manager = self.makeManager(sender, teammate, enemy, french, spanish)
        manager.addShipToTeam(french, 1)
        manager.addShipToTeam(spanish, 2)
        manager.air.getAvatarIdFromSender.return_value = 10

        manager.sendChat('ahoy', 0, 0)
        manager.sendSC(100)

        self.assertEqual(manager.sendUpdateToAvatarId.call_args_list, [
            call(10, 'recvChat', [10, 'ahoy', 0, 1010, 'Jack']),
            call(11, 'recvChat', [10, 'ahoy', 0, 1010, 'Jack']),
            call(10, 'recvSpeedChat', [10, 100, 'Jack']),
            call(11, 'recvSpeedChat', [10, 100, 'Jack'])])

    def test_chat_without_team_is_ignored(self):
        sender = FakeAvatar(10)
        manager = self.makeManager(sender)
        manager.air.getAvatarIdFromSender.return_value = 10
        manager.sendWLChat('ahoy', 0, 0)
        manager.sendUpdateToAvatarId.assert_not_called()

    def test_sink_scores_announces_and_awards_infamy(self):
        captain = FakeAvatar(10)
        attacker = FakeShip(20, crew=[10], name='Le Bateau')
        sunk = FakeShip(21, shipClass=ShipGlobals.WARSHIPL1, name='El Barco')
        manager = self.makeManager(captain, attacker, sunk)
        manager.addShipToTeam(attacker, 1)
        manager.addShipToTeam(sunk, 2)

        manager.handleShipSunk(sunk, attacker)

        worth = PVPGlobals.RenownWorthValues[ShipGlobals.WARSHIPL1]
        self.assertEqual(manager.getTeamScore(1), worth)
        self.assertEqual(captain.inventory.getStackQuantity(InventoryType.PVPTotalInfamySea), worth)
        self.assertEqual(captain.inventory.getStackQuantity(InventoryType.PVPCurrentInfamy), worth)
        manager.announcer.d_announceSink.assert_called_once_with(1, 'Le Bateau', 2, 'El Barco')
        self.assertEqual(manager.getShipSinkStreak(20), 1)

    def test_sink_with_assist(self):
        attacker = FakeShip(20, name='A')
        assist = FakeShip(22, name='B')
        sunk = FakeShip(21, name='C')
        manager = self.makeManager(attacker, assist, sunk)
        manager.addShipToTeam(attacker, 2)
        manager.addShipToTeam(assist, 2)
        manager.addShipToTeam(sunk, 1)

        manager.handleShipSunk(sunk, attacker, assist)
        manager.announcer.d_announceSinkWithAssist.assert_called_once_with(2, 'A', 2, 'B', 1, 'C')
        manager.announcer.d_announceSink.assert_not_called()

    def test_sink_streak_announced_every_period(self):
        attacker = FakeShip(20, name='A')
        manager = self.makeManager(attacker)
        manager.addShipToTeam(attacker, 1)
        period = PVPGlobals.SinkStreakPeriod.getValue()
        for i in range(period):
            sunk = FakeShip(100 + i, siegeTeam=2)
            manager.handleShipSunk(sunk, attacker)

        manager.announcer.d_announceSinkStreak.assert_called_once_with(1, 'A', period)

        # being sunk resets the streak
        manager.handleShipSunk(attacker, FakeShip(30, siegeTeam=2))
        self.assertEqual(manager.getShipSinkStreak(20), 0)

    def test_friendly_and_non_siege_sinks_are_ignored(self):
        attacker = FakeShip(20, siegeTeam=1)
        manager = self.makeManager(attacker)
        manager.handleShipSunk(FakeShip(21, siegeTeam=1), attacker)
        manager.handleShipSunk(FakeShip(22), attacker)
        self.assertEqual(manager.getTeamScore(1), 0)
        manager.announcer.d_announceSink.assert_not_called()

    def test_island_regen_heals_ships_near_own_island(self):
        near = FakeShip(20)
        far = FakeShip(21)
        far.pos = (50000, 0, 0)
        enemy = FakeShip(22)
        island = SimpleNamespace(
            getSiegeTeam=lambda: 1,
            getIslandTransform=lambda: [1000, 0, 0, 90],
            getZoneSphereCenter=lambda: [0, 0],
            getZoneSphereSize=lambda: [2000, 3000, 4000])
        manager = self.makeManager(near, far, enemy)
        manager._teamIslands = [island]
        manager.addShipToTeam(near, 1)
        manager.addShipToTeam(far, 1)
        manager.addShipToTeam(enemy, 2)

        manager.applyIslandRegen(2)

        hp = int(PVPGlobals.ShipRegenHps.getValue() * 2)
        self.assertEqual(near.hp, 100 + hp)
        self.assertEqual(far.hp, 100)
        self.assertEqual(enemy.hp, 100)

    def test_settings_are_broadcast(self):
        manager = self.makeManager()
        manager.b_setUseRepairKit(not manager.getUseRepairKit())
        manager.sendUpdate.assert_called_once_with('setUseRepairKit', [manager.getUseRepairKit()])


class SiegeAnnouncerAITests(unittest.TestCase):

    def test_announcements(self):
        announcer = SiegeAnnouncerAI.__new__(SiegeAnnouncerAI)
        announcer.sendUpdate = Mock()
        announcer.d_announceSink(1, 'A', 2, 'B')
        announcer.d_announceSinkWithAssist(1, 'A', 1, 'B', 2, 'C')
        announcer.d_announceSinkStreak(2, 'A', 5)
        self.assertEqual(announcer.sendUpdate.call_args_list, [
            call('announceSink', [1, 'A', 2, 'B']),
            call('announceSinkWithAssist', [1, 'A', 1, 'B', 2, 'C']),
            call('announceSinkStreak', [2, 'A', 5])])


if __name__ == '__main__':
    unittest.main()
