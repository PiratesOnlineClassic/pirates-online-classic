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
    from pirates.world.DistributedGATunnelAI import DistributedGATunnelAI
    from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
    from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI


def makeArea(air, doId, world):
    area = DistributedGameAreaAI.__new__(DistributedGameAreaAI)
    NodePath.__init__(area, 'area-%d' % doId)
    area.doId = doId
    area.parentId = world.doId
    area.zoneId = 700 + doId
    area.cr = air
    air.doId2do[doId] = area
    return area


def makeTunnel(air, doId, area, otherLinkUid, links):
    tunnel = DistributedGATunnelAI.__new__(DistributedGATunnelAI)
    NodePath.__init__(tunnel, 'tunnel-%d' % doId)
    tunnel.air = air
    tunnel.cr = air
    tunnel.doId = doId
    tunnel.parentId = area.doId
    tunnel.zoneId = 610
    tunnel.otherLinkUid = otherLinkUid
    tunnel.links = [False, '', links]
    tunnel.sendUpdateToAvatarId = Mock()
    air.doId2do[doId] = tunnel
    return tunnel


class ConnectorPrivateAreaTests(unittest.TestCase):

    def setUp(self):
        self.avatar = SimpleNamespace(doId=42)
        self.air = SimpleNamespace(doId2do={42: self.avatar}, getAvatarIdFromSender=lambda: 42,
            worldGridManager=SimpleNamespace(handleLocationChanged=Mock()),
            logPotentialHacker=Mock())

        world = DistributedInstanceBaseAI.__new__(DistributedInstanceBaseAI)
        if isinstance(world, NodePath):
            NodePath.__init__(world, 'world')
        world.doId = 5000
        self.air.doId2do[world.doId] = world

        self.island = makeArea(self.air, 1, world)
        self.cave = makeArea(self.air, 2, world)
        self.stranger = makeArea(self.air, 3, world)

        links = [['a', self.island.doId], ['b', self.cave.doId]]
        self.islandTunnel = makeTunnel(self.air, 10, self.island, 'cave-tunnel', links)
        self.caveTunnel = makeTunnel(self.air, 11, self.cave, 'island-tunnel', links)
        uids = {'cave-tunnel': self.caveTunnel, 'island-tunnel': self.islandTunnel}
        self.air.uidMgr = SimpleNamespace(justGetMeMeObject=uids.get)

    def test_request_opens_interest_at_the_connector_in_the_requested_area(self):
        self.islandTunnel.requestPrivateArea(self.cave.doId)
        parentObj, avatar, zoneId, callback = self.air.worldGridManager.handleLocationChanged.call_args[0]
        self.assertIs(parentObj, self.cave)
        self.assertIs(avatar, self.avatar)
        self.assertEqual(zoneId, self.caveTunnel.zoneId)

        callback()
        self.islandTunnel.sendUpdateToAvatarId.assert_called_once_with(42, 'setPrivateArea',
            [5000, self.cave.zoneId, self.cave.doId, True])

    def test_turning_back_opens_interest_in_the_area_we_came_from(self):
        self.islandTunnel.requestPrivateArea(self.island.doId)
        parentObj, avatar, zoneId, callback = self.air.worldGridManager.handleLocationChanged.call_args[0]
        self.assertIs(parentObj, self.island)
        self.assertEqual(zoneId, self.islandTunnel.zoneId)

    def test_areas_the_connector_does_not_link_are_rejected(self):
        self.islandTunnel.requestPrivateArea(self.stranger.doId)
        self.air.worldGridManager.handleLocationChanged.assert_not_called()
        self.air.logPotentialHacker.assert_called_once()


if __name__ == '__main__':
    unittest.main()
