import unittest
from types import SimpleNamespace
from unittest.mock import Mock

# sets up the game resource stubs the world AI modules need
import tests.pirates.world.test_siege_world_ai

from otp.distributed.OtpDoGlobals import OTP_DO_ID_AVATAR_FRIENDS_MANAGER
from tests.otp.friends.test_friends_managers_ud import getDcFile
from pirates.world.DistributedDinghyAI import DistributedDinghyAI


class FakeShip:

    def __init__(self, doId, captainId, allowFriends=True):
        self.doId = doId
        self.captainId = captainId
        self.allowFriends = allowFriends
        self.crew = []

    def getCaptainId(self):
        return self.captainId

    def getAllowFriendState(self):
        return self.allowFriends


class TestDinghyFriendShips(unittest.TestCase):

    def setUp(self):
        self.ships = []
        self.air = SimpleNamespace(
            doId2do={},
            dclassesByName={
                'PCAvatarFriendsManager': getDcFile().getClassByName('PCAvatarFriendsManager'),
                'DistributedDinghyAI': getDcFile().getClassByName('DistributedDinghy')},
            ourChannel=4000,
            send=Mock(),
            sender=0,
            shipManager=SimpleNamespace(getPlayerShips=lambda: list(self.ships)))
        self.air.getAvatarIdFromSender = lambda: self.air.sender

        self.dinghy = DistributedDinghyAI(self.air)
        self.dinghy.doId = 5555
        self.dinghy.sendUpdateToAvatarId = Mock()
        self.dinghy.getPublicShipInfo = lambda shipId: [self.air.doId2do[shipId].captainId, shipId]
        self.dinghy.canSelectShip = lambda ship: True
        self.dinghy.sendAvatarToShip = Mock()

        self.jack = SimpleNamespace(doId=1, getDISLid=lambda: 1001)
        self.air.doId2do[1] = self.jack
        for captainId in (2, 3):
            self.air.doId2do[captainId] = SimpleNamespace(doId=captainId)

    def addShip(self, ship):
        self.ships.append(ship)
        self.air.doId2do[ship.doId] = ship
        return ship

    def test_friends_list_requested_from_uberdog(self):
        self.dinghy.d_offerPublicOptions = Mock()
        self.dinghy.handlePostRequestInteraction(self.jack)
        datagram = self.air.send.call_args[0][0]
        dclass = getDcFile().getClassByName('PCAvatarFriendsManager')
        expected = dclass.aiFormatUpdate('requestDinghyFriendsList', OTP_DO_ID_AVATAR_FRIENDS_MANAGER,
            OTP_DO_ID_AVATAR_FRIENDS_MANAGER, 4000, [5555, 1, 1001])
        self.assertEqual(datagram.getMessage(), expected.getMessage())

    def test_friend_ships_offered_and_selectable(self):
        friendShip = self.addShip(FakeShip(10, 2))
        self.addShip(FakeShip(11, 3))
        self.addShip(FakeShip(12, 2, allowFriends=False))

        self.dinghy.responseFriendsList(1, [2])
        self.dinghy.sendUpdateToAvatarId.assert_called_once_with(1, 'offerFriendOptions', [[[2, 10]]])

        self.air.sender = 1
        self.dinghy.selectFriendShip(10)
        self.dinghy.sendAvatarToShip.assert_called_once_with(self.jack, friendShip)

    def test_non_friend_ship_rejected(self):
        self.addShip(FakeShip(11, 3))
        self.dinghy.responseFriendsList(1, [2])
        self.dinghy.sendUpdateToAvatarId.assert_not_called()

        self.air.sender = 1
        self.dinghy.selectFriendShip(11)
        self.dinghy.sendAvatarToShip.assert_not_called()
        self.dinghy.sendUpdateToAvatarId.assert_called_once_with(1, 'sendAvatarToShip', [0])


if __name__ == '__main__':
    unittest.main()
