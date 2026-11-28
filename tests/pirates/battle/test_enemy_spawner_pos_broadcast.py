import builtins
import unittest
from types import SimpleNamespace

from unittest.mock import Mock, patch

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')

if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

with patch.object(builtins.loader, 'loadFont', Mock()):
    from pirates.battle.DistributedEnemySpawnerAI import SpawnNodeBase


class _Npc:

    def __init__(self):
        self.pos = (1.0, 2.0, 3.0)
        self.hpr = (90.0, 0.0, 0.0)
        self.sent = []

    def getPos(self):
        return self.pos

    def getHpr(self):
        return self.hpr

    def sendUpdate(self, fieldName, args):
        self.sent.append((fieldName, tuple(args[:6])))


class EnemySpawnerPosBroadcastTests(unittest.TestCase):

    def setUp(self):
        self.spawner = SpawnNodeBase.__new__(SpawnNodeBase)
        self.npc = _Npc()
        self.spawner._npc = self.npc
        self.task = SimpleNamespace(again='again', done='done')

    def update(self):
        return self.spawner._SpawnNodeBase__updateNPC(self.task)

    def test_idle_npcs_only_broadcast_their_position_once(self):
        for _ in range(5):
            self.assertEqual(self.update(), 'again')

        self.assertEqual(self.npc.sent, [('setSmPosHpr', (1.0, 2.0, 3.0, 90.0, 0.0, 0.0))])

    def test_moving_npcs_broadcast_every_change(self):
        self.update()
        self.npc.pos = (4.0, 2.0, 3.0)
        self.update()
        self.update()
        self.npc.hpr = (45.0, 0.0, 0.0)
        self.update()

        self.assertEqual([args for _, args in self.npc.sent], [
            (1.0, 2.0, 3.0, 90.0, 0.0, 0.0),
            (4.0, 2.0, 3.0, 90.0, 0.0, 0.0),
            (4.0, 2.0, 3.0, 45.0, 0.0, 0.0)])

    def test_despawned_npc_stops_the_task(self):
        self.spawner._npc = None
        self.assertEqual(self.update(), 'done')


if __name__ == '__main__':
    unittest.main()
