import builtins
import unittest


class _Ship(object):
    pass
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.core import NodePath, loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

from tests.pirates.kraken.testutil import installStubs
installStubs()

from pirates.kraken import KrakenSummonerAI as summonerModule
from pirates.kraken.KrakenSummonerAI import KrakenSummonerAI


class KrakenSummonerTests(unittest.TestCase):

    def makeShip(self, doId=500, pos=(20000, 0, 0), state='ClientSteering', crew=(7,)):
        grid = NodePath('grid')
        node = grid.attachNewNode('ship-%d' % doId)
        node.setPos(*pos)
        ship = _Ship()
        ship.doId = doId
        ship.isEmpty = node.isEmpty
        ship.getPos = node.getPos
        ship.getParentObj = lambda: grid
        ship.getCrew = lambda: list(crew)
        ship.getCurrentGameState = lambda: state
        ship.hasSpawnBuff = lambda: False
        return ship

    def makeSummoner(self, ships):
        shipManager = SimpleNamespace(world=None, getPlayerShips=lambda: ships)
        summoner = KrakenSummonerAI(SimpleNamespace(doId2do={}), shipManager)
        summoner.islandSpheres = [(0, 0, 4000)]
        return summoner

    def test_only_sailing_crewed_ships_in_open_water_are_attacked(self):
        summoner = self.makeSummoner([])
        with patch.object(summonerModule.KrakenAI, 'getKrakenForShip', return_value=None):
            self.assertTrue(summoner.canAttack(self.makeShip(), 0))
            self.assertFalse(summoner.canAttack(self.makeShip(pos=(6000, 0, 0)), 0))
            self.assertFalse(summoner.canAttack(self.makeShip(state='Docked'), 0))
            self.assertFalse(summoner.canAttack(self.makeShip(crew=()), 0))

        with patch.object(summonerModule.KrakenAI, 'getKrakenForShip', return_value=object()):
            self.assertFalse(summoner.canAttack(self.makeShip(), 0))

    def test_attacked_ship_is_left_alone_for_a_while(self):
        ship = self.makeShip()
        summoner = self.makeSummoner([ship])
        spawn = Mock(return_value=object())
        clock = SimpleNamespace(time=1000.0)
        with patch.object(summonerModule.KrakenAI, 'getKrakenForShip', return_value=None), \
                patch.object(summonerModule.KrakenAI, 'spawnKraken', spawn), \
                patch.object(builtins, 'globalClock', Mock(getFrameTime=lambda: clock.time), create=True), \
                patch('random.random', return_value=0.0):
            summoner._KrakenSummonerAI__check(SimpleNamespace(again='again'))
            summoner._KrakenSummonerAI__check(SimpleNamespace(again='again'))
            self.assertEqual(spawn.call_count, 1)

            clock.time += summoner.ShipCooldown
            summoner._KrakenSummonerAI__check(SimpleNamespace(again='again'))
            self.assertEqual(spawn.call_count, 2)


if __name__ == '__main__':
    unittest.main()
