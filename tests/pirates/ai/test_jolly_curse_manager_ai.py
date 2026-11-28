import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.core import BitMask32, NodePath, loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')

if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

with patch.object(builtins.loader, 'loadFont', Mock()):
    from pirates.battle import BattleManagerAI

from pirates.ai import JollyCurseManagerAI as curse_module
from pirates.ai.JollyCurseManagerAI import JollyCurseManagerAI
from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI
from pirates.piratesbase import PiratesGlobals, TODGlobals
from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
from pirates.world.DistributedIslandAI import DistributedIslandAI
from pirates.world.DistributedJailInteriorAI import DistributedJailInteriorAI

JOLLY = TODGlobals.TOD_JOLLYCURSE_CYCLE


def makeArea(cls, doId):
    area = cls.__new__(cls)
    area.doId = doId
    return area


def makePlayer(air, doId, parentObj, worldType=PiratesGlobals.INSTANCE_MAIN, hp=100):
    player = DistributedPlayerPirateAI.__new__(DistributedPlayerPirateAI)
    NodePath.__init__(player, 'player-%d' % doId)
    player.air = air
    player.doId = doId
    player.hp = hp
    player.quietly = False
    player.zombie = 0
    player.forcedZombie = 0
    player.teleportFlags = BitMask32()
    player.sendUpdate = Mock()
    player.getParentObj = Mock(return_value=parentObj)
    player.getWorld = Mock(return_value=Mock(getType=Mock(return_value=worldType)))
    air.doId2do[doId] = player
    return player


def sentUpdates(player, field):
    return [call[0][1] for call in player.sendUpdate.call_args_list if call[0][0] == field]


class JollyCurseManagerAITests(unittest.TestCase):

    def setUp(self):
        self.air = SimpleNamespace(doId2do={}, timeOfDayMgr=Mock())
        self.manager = JollyCurseManagerAI(self.air)
        self.air.jollyCurseMgr = self.manager
        self.island = makeArea(DistributedIslandAI, 10)
        self.interior = makeArea(DistributedGAInteriorAI, 11)
        self.jail = makeArea(DistributedJailInteriorAI, 12)

    def test_registers_for_the_moon_phases(self):
        with patch.object(self.manager, 'accept') as accept:
            self.manager.start()

        states = [call[0][0] for call in self.air.timeOfDayMgr.addTimeOfDayStateMethod.call_args_list]
        self.assertEqual(sorted(states), sorted([PiratesGlobals.TOD_FULLMOON,
            PiratesGlobals.TOD_HALF2FULLMOON, PiratesGlobals.TOD_FULL2HALFMOON]))
        accept.assert_called_once_with('timeOfDayCycleChanged', self.manager.processCycleChange)

    def test_full_moon_curses_only_pirates_outdoors_on_land(self):
        outdoors = makePlayer(self.air, 100, self.island)
        indoors = makePlayer(self.air, 101, self.interior)
        jailed = makePlayer(self.air, 102, self.jail)
        atSea = makePlayer(self.air, 103, Mock())
        tutorial = makePlayer(self.air, 104, self.island, worldType=PiratesGlobals.INSTANCE_TUTORIAL)
        defeated = makePlayer(self.air, 105, self.island, hp=0)

        self.manager.processTimeChange(JOLLY, PiratesGlobals.TOD_FULLMOON, 0)

        self.assertTrue(self.manager.isCurseActive())
        self.assertEqual(outdoors.getZombie(), 1)
        self.assertEqual(sentUpdates(outdoors, 'setZombie'), [[1, 1]])
        self.assertEqual(sentUpdates(outdoors, 'setCurseStatus'), [[curse_module.CURSE_STATUS_OUTDOORS]])
        self.assertTrue(outdoors.isUndead())

        self.assertEqual(sentUpdates(indoors, 'setCurseStatus'), [[curse_module.CURSE_STATUS_INDOORS]])
        self.assertEqual(sentUpdates(jailed, 'setCurseStatus'), [[curse_module.CURSE_STATUS_JAIL]])
        for player in (indoors, jailed, atSea, tutorial, defeated):
            self.assertEqual(player.getZombie(), 0)
            self.assertEqual(sentUpdates(player, 'setZombie'), [])

        for player in (atSea, tutorial, defeated):
            self.assertEqual(sentUpdates(player, 'setCurseStatus'), [])

    def test_full_moon_only_curses_once(self):
        outdoors = makePlayer(self.air, 100, self.island)
        self.manager.processTimeChange(JOLLY, PiratesGlobals.TOD_FULLMOON, 0)
        self.manager.processTimeChange(JOLLY, PiratesGlobals.TOD_FULLMOON, 0)
        self.assertEqual(len(sentUpdates(outdoors, 'setCurseStatus')), 1)

    def test_pirates_arriving_during_the_full_moon_stay_human(self):
        self.manager.processTimeChange(JOLLY, PiratesGlobals.TOD_FULLMOON, 0)
        late = makePlayer(self.air, 100, self.island)
        self.manager.avatarChangedLocation(late, self.island)
        self.assertEqual(late.getZombie(), 0)

    def test_waning_moon_restores_the_cursed(self):
        outdoors = makePlayer(self.air, 100, self.island)
        forced = makePlayer(self.air, 101, self.island)
        forced.forcedZombie = 1
        self.manager.processTimeChange(JOLLY, PiratesGlobals.TOD_FULLMOON, 0)
        outdoors.sendUpdate.reset_mock()

        self.manager.processTimeChange(JOLLY, PiratesGlobals.TOD_FULL2HALFMOON, 0)
        self.assertFalse(self.manager.isCurseActive())
        self.assertEqual(outdoors.getZombie(), 0)
        self.assertEqual(sentUpdates(outdoors, 'setZombie'), [[0, 0]])
        self.assertFalse(self.manager.isAvatarCursed(outdoors.doId))

        # zombies forced by the magic word stay zombies...
        self.assertEqual(forced.getZombie(), 1)

    def test_holiday_stopping_mid_curse_restores_the_cursed(self):
        outdoors = makePlayer(self.air, 100, self.island)
        self.manager.processTimeChange(JOLLY, PiratesGlobals.TOD_FULLMOON, 0)
        self.manager.processCycleChange(JOLLY)
        self.assertEqual(outdoors.getZombie(), 1)

        self.manager.processCycleChange(TODGlobals.TOD_REGULAR_CYCLE)
        self.assertEqual(outdoors.getZombie(), 0)
        self.assertFalse(self.manager.isCurseActive())

    def test_cursed_pirates_thrown_in_jail_are_restored(self):
        outdoors = makePlayer(self.air, 100, self.island)
        self.manager.processTimeChange(JOLLY, PiratesGlobals.TOD_FULLMOON, 0)
        outdoors.sendUpdate.reset_mock()

        # walking into the Kingshead fort keeps the pirate Undead...
        self.manager.avatarChangedLocation(outdoors, self.interior)
        self.assertEqual(outdoors.getZombie(), 1)

        self.manager.avatarChangedLocation(outdoors, self.jail)
        self.assertEqual(outdoors.getZombie(), 0)
        self.assertEqual(sentUpdates(outdoors, 'setZombie'), [[0, 0]])
        self.assertEqual(sentUpdates(outdoors, 'setCurseStatus'), [[curse_module.CURSE_STATUS_JAIL]])

        # and once restored they are safe for the rest of the full moon...
        outdoors.getParentObj.return_value = self.island
        self.manager.avatarChangedLocation(outdoors, self.island)
        self.assertEqual(outdoors.getZombie(), 0)

    def test_zombie_magic_word_follows_the_curse(self):
        player = makePlayer(self.air, 100, self.island)
        player.forcedZombie = 1
        player.attemptToSetCursedZombie()
        self.assertEqual(player.getZombie(), 1)

        player.forcedZombie = 0
        player.attemptToSetCursedZombie()
        self.assertEqual(player.getZombie(), 0)

        self.manager.processTimeChange(JOLLY, PiratesGlobals.TOD_FULLMOON, 0)
        player.attemptToSetCursedZombie()
        self.assertEqual(player.getZombie(), 1)

    def test_avatar_leaving_is_forgotten(self):
        player = makePlayer(self.air, 100, self.island)
        self.manager.processTimeChange(JOLLY, PiratesGlobals.TOD_FULLMOON, 0)
        self.manager.avatarLeft(player)
        self.assertFalse(self.manager.isAvatarCursed(player.doId))


class UndeadCombatTests(unittest.TestCase):

    def makeManager(self):
        return BattleManagerAI.BattleManagerAI.__new__(BattleManagerAI.BattleManagerAI)

    def makeTeamPlayer(self, zombie=0, pvpTeam=0, siegeTeam=0):
        player = DistributedPlayerPirateAI.__new__(DistributedPlayerPirateAI)
        player.zombie = zombie
        player._pvpTeam = pvpTeam
        player._siegeTeam = siegeTeam
        return player

    def test_undead_players_fight_everyone(self):
        manager = self.makeManager()
        self.assertFalse(manager.isPlayerDamageAllowed(self.makeTeamPlayer(), self.makeTeamPlayer()))
        self.assertTrue(manager.isPlayerDamageAllowed(self.makeTeamPlayer(zombie=1), self.makeTeamPlayer()))
        self.assertTrue(manager.isPlayerDamageAllowed(self.makeTeamPlayer(), self.makeTeamPlayer(zombie=1)))
        self.assertTrue(manager.isPlayerDamageAllowed(self.makeTeamPlayer(zombie=1), self.makeTeamPlayer(zombie=1)))

    def test_siege_teams_decide_before_the_curse(self):
        # see TeamUtils.friendOrFoe, the siege teams are checked before the undead...
        manager = self.makeManager()
        self.assertFalse(manager.isPlayerDamageAllowed(self.makeTeamPlayer(zombie=1, siegeTeam=1),
            self.makeTeamPlayer(siegeTeam=1)))
        self.assertTrue(manager.isPlayerDamageAllowed(self.makeTeamPlayer(siegeTeam=1),
            self.makeTeamPlayer(siegeTeam=2)))


class UndeadInteractionTests(unittest.TestCase):

    def makeZombie(self):
        return SimpleNamespace(doId=100, zombie=1, getZombie=lambda: 1)

    def test_undead_cannot_board_boats(self):
        from pirates.world.DistributedDinghyAI import DistributedDinghyAI

        dinghy = DistributedDinghyAI.__new__(DistributedDinghyAI)
        dinghy.sendUpdateToAvatarId = Mock()
        self.assertEqual(dinghy.handleRequestInteraction(self.makeZombie(), 0, 0), dinghy.DENY)
        dinghy.sendUpdateToAvatarId.assert_called_once_with(100, 'denyAccess', [PiratesGlobals.ZombieNoBoats])

    def test_undead_cannot_talk_to_townsfolk(self):
        from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI

        npc = DistributedNPCTownfolkAI.__new__(DistributedNPCTownfolkAI)
        npc.air = Mock()
        self.assertEqual(npc.handleRequestInteraction(self.makeZombie(), PiratesGlobals.INTERACT_TYPE_FRIENDLY, 0), npc.DENY)
        npc.air.questMgr.requestInteract.assert_not_called()

    def test_doors_are_barricaded_except_the_kingshead_fort(self):
        from pirates.world.DistributedBuildingDoorAI import DistributedBuildingDoorAI
        from pirates.world.DistributedDoorBaseAI import DistributedDoorBaseAI

        door = DistributedBuildingDoorAI.__new__(DistributedBuildingDoorAI)
        door.buildingUid = 'some-tavern'
        door.interiorUid = 'some-tavern-interior'
        with patch.object(DistributedDoorBaseAI, 'handleRequestInteraction', return_value=0) as base:
            self.assertEqual(door.handleRequestInteraction(self.makeZombie(), 0, 0), door.DENY)
            base.assert_not_called()

            door.buildingUid = DistributedBuildingDoorAI.ZombieBuildingUid
            door.handleRequestInteraction(self.makeZombie(), 0, 0)
            base.assert_called_once()


if __name__ == '__main__':
    unittest.main()
