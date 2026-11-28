import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.core import NodePath, loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')

if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

with patch.object(builtins.loader, 'loadFont', Mock()):
    from pirates.battle.BattleManagerAI import BattleManagerAI

from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI


def makeBattleAvatar(cls=DistributedBattleAvatarAI, doId=200, air=None):
    avatar = cls.__new__(cls)
    NodePath.__init__(avatar, 'avatar-%d' % doId)
    avatar.doId = doId
    avatar.skillEffects = []
    avatar.hp = 100
    avatar.quietly = False
    avatar.sendUpdate = Mock()
    avatar.air = air or SimpleNamespace(doId2do={})
    avatar.air.doId2do[doId] = avatar
    return avatar


def makePlayer(doId=100, air=None):
    player = makeBattleAvatar(DistributedPlayerPirateAI, doId, air)
    player.stickyTargets = []
    return player


class LeaveBattleTests(unittest.TestCase):

    def makeMovingPlayer(self, parentId):
        player = makePlayer()
        player.parentId = parentId
        player.isGenerated = lambda: True
        player.air.targetMgr = Mock()
        return player

    def test_leaving_the_area_leaves_every_battle(self):
        player = self.makeMovingPlayer(4000)
        with patch('pirates.pirate.DistributedPlayerPirateAI.DistributedPlayerAI.setLocation'), \
                patch('pirates.pirate.DistributedPlayerPirateAI.DistributedBattleAvatarAI.setLocation'), \
                patch.object(DistributedPlayerPirateAI, 'getParentObj', return_value=None):
            player.setLocation(4000, 2001)
            player.air.targetMgr.clearAttacker.assert_not_called()

            player.setLocation(5000, 2001)
            player.air.targetMgr.clearAttacker.assert_called_once_with(player)

    def test_arriving_in_the_world_is_not_leaving_a_battle(self):
        player = self.makeMovingPlayer(None)
        with patch('pirates.pirate.DistributedPlayerPirateAI.DistributedPlayerAI.setLocation'), \
                patch('pirates.pirate.DistributedPlayerPirateAI.DistributedBattleAvatarAI.setLocation'), \
                patch.object(DistributedPlayerPirateAI, 'getParentObj', return_value=None):
            player.setLocation(4000, 2001)

        player.air.targetMgr.clearAttacker.assert_not_called()


if __name__ == '__main__':
    unittest.main()
