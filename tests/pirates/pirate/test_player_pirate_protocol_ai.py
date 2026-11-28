import unittest
from types import SimpleNamespace
from unittest.mock import Mock

# reuse the player harness (and its WeaponGlobals fallback / ShowBase)
from tests.pirates.pirate.test_player_pirate_ai import makePlayer

from pirates.pirate import TitleGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
from pirates.piratesbase import PiratesGlobals
from pirates.reputation import ReputationGlobals
from pirates.quest.QuestConstants import LocationIds
from pirates.ship import ShipGlobals

PORT_ROYAL = LocationIds.PORT_ROYAL_ISLAND
FORT_CHARLES = LocationIds.PORT_ROYAL_FORT_CHARLES


class BadgeIconTests(unittest.TestCase):

    def makePlayer(self, infamy=0):
        player = makePlayer(stacks={InventoryType.PVPTotalInfamyLand: infamy})
        player.badgeIcon = (-1, -1)
        player.shipBadgeIcon = (-1, -1)
        return player

    def test_earned_title_rank_is_worn(self):
        player = self.makePlayer(infamy=TitleGlobals.RenownBreakpointsLand[2])
        player.requestBadgeIcon(TitleGlobals.LandPVPTitle, 2)
        self.assertEqual(player.getBadgeIcon(), (TitleGlobals.LandPVPTitle, 2))
        player.sendUpdate.assert_called_once_with('setBadgeIcon', [TitleGlobals.LandPVPTitle, 2])

    def test_unearned_title_rank_is_refused(self):
        player = self.makePlayer(infamy=TitleGlobals.RenownBreakpointsLand[1])
        player.requestBadgeIcon(TitleGlobals.LandPVPTitle, 3)
        self.assertEqual(player.getBadgeIcon(), (-1, -1))
        player.sendUpdate.assert_not_called()
        player.air.logPotentialHacker.assert_called_once()

    def test_badge_is_taken_off(self):
        player = self.makePlayer()
        player.badgeIcon = (TitleGlobals.LandPVPTitle, 1)
        player.requestBadgeIcon(-1, -1)
        self.assertEqual(player.getBadgeIcon(), (-1, -1))

    def test_unknown_title_is_refused(self):
        player = self.makePlayer()
        player.requestShipBadgeIcon(99, 0)
        self.assertEqual(player.getShipBadgeIcon(), (-1, -1))
        player.sendUpdate.assert_not_called()

    def test_other_avatars_cannot_set_the_badge(self):
        player = self.makePlayer(infamy=TitleGlobals.RenownBreakpointsLand[2])
        player.air.getAvatarIdFromSender.return_value = player.doId + 1
        player.requestBadgeIcon(TitleGlobals.LandPVPTitle, 1)
        self.assertEqual(player.getBadgeIcon(), (-1, -1))


class AreaSphereTests(unittest.TestCase):

    def makePlayer(self):
        player = makePlayer()
        player.areaSphereStack = []
        return player

    def test_entering_a_location_echoes_it(self):
        player = self.makePlayer()
        player.enterAreaSphere(FORT_CHARLES, PORT_ROYAL)
        player.sendUpdateToAvatarId.assert_called_once_with(player.doId, 'locationChange', [FORT_CHARLES])
        self.assertEqual(player.getAreaSphereUid(), FORT_CHARLES)

    def test_leaving_a_location_returns_to_the_area(self):
        player = self.makePlayer()
        player.enterAreaSphere(FORT_CHARLES, PORT_ROYAL)
        player.leaveAreaSphere(FORT_CHARLES, PORT_ROYAL)
        player.sendUpdateToAvatarId.assert_called_with(player.doId, 'locationChange', [PORT_ROYAL])
        self.assertEqual(player.getAreaSphereUid(), '')

    def test_leaving_a_location_never_entered_is_ignored(self):
        player = self.makePlayer()
        player.leaveAreaSphere(FORT_CHARLES, PORT_ROYAL)
        player.sendUpdateToAvatarId.assert_not_called()

    def test_unknown_locations_are_ignored(self):
        player = self.makePlayer()
        player.enterAreaSphere('not-a-location', PORT_ROYAL)
        player.sendUpdateToAvatarId.assert_not_called()


class TownfolkTutorialTests(unittest.TestCase):

    def makeNpc(self, avatar, senderId=None):
        npc = DistributedNPCTownfolkAI.__new__(DistributedNPCTownfolkAI)
        npc.tutorialShipAvIds = set()
        npc.air = SimpleNamespace(
            getAvatarIdFromSender=Mock(return_value=avatar.doId if senderId is None else senderId),
            doId2do={avatar.doId: avatar}, logPotentialHacker=Mock(),
            tradeMgr=Mock(), shipLoader=Mock())
        return npc

    def makeAvatar(self, tutorial, reputation=0, ships=()):
        inventory = Mock(getReputation=Mock(return_value=reputation),
                         getShipDoIdList=Mock(return_value=list(ships)))
        avatar = SimpleNamespace(doId=100, getTutorial=lambda: tutorial, getInventory=lambda: inventory,
                                 constructedShipDoId=0)
        avatar.getConstructedShipDoId = lambda: avatar.constructedShipDoId
        avatar.setConstructedShipDoId = lambda shipId: setattr(avatar, 'constructedShipDoId', shipId)
        return avatar

    def test_cutlass_is_leveled_up(self):
        avatar = self.makeAvatar(PiratesGlobals.TUT_GOT_CUTLASS - 1)
        npc = self.makeNpc(avatar)
        npc.levelUpCutlass(avatar.doId)
        npc.air.tradeMgr.createTrade.return_value.giveReputation.assert_called_once_with(
            InventoryType.CutlassRep, ReputationGlobals.getTotalReputation(InventoryType.CutlassRep, 2))

    def test_leveled_cutlass_is_left_alone(self):
        avatar = self.makeAvatar(PiratesGlobals.TUT_GOT_CUTLASS - 1,
                                 reputation=ReputationGlobals.getTotalReputation(InventoryType.CutlassRep, 2))
        npc = self.makeNpc(avatar)
        npc.levelUpCutlass(avatar.doId)
        npc.air.tradeMgr.createTrade.assert_not_called()

    def test_cutlass_level_up_for_another_avatar_is_refused(self):
        avatar = self.makeAvatar(PiratesGlobals.TUT_GOT_CUTLASS - 1)
        npc = self.makeNpc(avatar, senderId=avatar.doId + 1)
        npc.levelUpCutlass(avatar.doId)
        npc.air.tradeMgr.createTrade.assert_not_called()
        npc.air.logPotentialHacker.assert_called_once()

    def test_tutorial_ship_is_built_with_the_chosen_name(self):
        avatar = self.makeAvatar(PiratesGlobals.TUT_GOT_SHIP - 1)
        npc = self.makeNpc(avatar)
        npc.shipTutorialPt1(avatar.doId, ['Black Gull', []])
        args, kwargs = npc.air.shipLoader.createShip.call_args
        self.assertEqual(args, (avatar, ShipGlobals.INTERCEPTORL1, 'Black Gull'))

        # the quest's ShipReward hands over the constructed ship...
        kwargs['callback'](5000)
        self.assertEqual(avatar.constructedShipDoId, 5000)

    def test_tutorial_ship_is_only_built_once(self):
        avatar = self.makeAvatar(PiratesGlobals.TUT_GOT_SHIP - 1)
        npc = self.makeNpc(avatar)
        npc.shipTutorialPt1(avatar.doId, ['Black Gull', []])
        npc.shipTutorialPt1(avatar.doId, ['Black Gull', []])
        self.assertEqual(npc.air.shipLoader.createShip.call_count, 1)

        owner = self.makeAvatar(PiratesGlobals.TUT_GOT_SHIP - 1, ships=[5000])
        npc = self.makeNpc(owner)
        npc.shipTutorialPt1(owner.doId, ['Black Gull', []])
        npc.air.shipLoader.createShip.assert_not_called()

    def test_no_tutorial_ship_after_the_tutorial(self):
        avatar = self.makeAvatar(PiratesGlobals.TUT_GOT_SHIP)
        npc = self.makeNpc(avatar)
        npc.shipTutorialPt1(avatar.doId, ['Black Gull', []])
        npc.air.shipLoader.createShip.assert_not_called()


if __name__ == '__main__':
    unittest.main()
