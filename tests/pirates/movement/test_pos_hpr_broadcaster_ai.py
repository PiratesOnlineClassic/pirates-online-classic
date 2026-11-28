import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')

from direct.task import Task

from pirates.movement.PosHprBroadcasterAI import PosHprBroadcasterAI


class _Mover(PosHprBroadcasterAI):

    def __init__(self):
        PosHprBroadcasterAI.__init__(self)
        self.doId = 1000
        self.pos = (1.0, 2.0, 3.0)
        self.hpr = (90.0, 0.0, 0.0)
        self.sent = []

    def uniqueName(self, name):
        return '%s-%d' % (name, self.doId)

    def isEmpty(self):
        return False

    def getPos(self):
        return self.pos

    def getHpr(self):
        return self.hpr

    def sendUpdate(self, fieldName, args):
        # leave out the timestamp
        self.sent.append((fieldName, tuple(args[:-1])))


class PosHprBroadcasterAITests(unittest.TestCase):

    def setUp(self):
        self.taskMgr = Mock()
        self.taskMgr.doMethodLater.side_effect = lambda delay, method, name: SimpleNamespace(
            name=name, method=method, delayTime=delay)
        patcher = patch.object(builtins, 'taskMgr', self.taskMgr, create=True)
        patcher.start()
        self.addCleanup(patcher.stop)

        self.mover = _Mover()
        self.mover.sendCurrentPosition()
        self.mover.sent = []

    def tick(self):
        task = self.mover._posHprBroadcastTask
        return self.mover._posHprBroadcast(task)

    def fields(self):
        return [field for field, _ in self.mover.sent]

    def test_an_object_at_rest_sends_a_single_stop(self):
        for _ in range(5):
            self.mover.broadcastPosHprFull()

        self.assertEqual(self.fields(), ['setSmStop'])

    def test_only_the_changed_components_are_sent(self):
        self.mover.pos = (4.0, 5.0, 3.0)
        self.mover.broadcastPosHprFull()
        self.mover.hpr = (45.0, 0.0, 0.0)
        self.mover.broadcastPosHprFull()
        self.mover.pos = (6.0, 7.0, 3.0)
        self.mover.hpr = (40.0, 0.0, 0.0)
        self.mover.broadcastPosHprFull()
        self.mover.pos = (6.0, 7.0, 8.0)
        self.mover.broadcastPosHprFull()
        self.mover.hpr = (40.0, 10.0, 0.0)
        self.mover.pos = (1.0, 7.0, 8.0)
        self.mover.broadcastPosHprFull()

        self.assertEqual(self.mover.sent, [
            ('setSmXY', (4.0, 5.0)),
            ('setSmH', (45.0,)),
            ('setSmXYH', (6.0, 7.0, 40.0)),
            ('setSmZ', (8.0,)),
            ('setSmPosHpr', (1.0, 7.0, 8.0, 40.0, 10.0, 0.0))])

    def test_changes_below_the_network_precision_are_not_sent(self):
        self.mover.pos = (1.001, 2.002, 3.0)
        self.mover.hpr = (450.0, 0.0, 0.0)
        self.mover.broadcastPosHprFull()

        self.assertEqual(self.fields(), ['setSmStop'])

    def test_moving_again_after_a_stop_is_sent(self):
        self.mover.broadcastPosHprFull()
        self.mover.pos = (2.0, 2.0, 3.0)
        self.mover.broadcastPosHprFull()
        self.mover.broadcastPosHprFull()

        self.assertEqual(self.fields(), ['setSmStop', 'setSmXY', 'setSmStop'])

    def test_kicked_broadcast_stops_itself_once_at_rest(self):
        self.mover.pos = (2.0, 2.0, 3.0)
        self.mover.kickPosHprBroadcast()
        self.assertTrue(self.mover.posHprBroadcastStarted())

        self.mover.pos = (3.0, 2.0, 3.0)
        self.assertEqual(self.tick(), Task.again)
        self.assertEqual(self.tick(), Task.done)
        self.assertFalse(self.mover.posHprBroadcastStarted())
        self.assertEqual(self.fields(), ['setSmXY', 'setSmXY', 'setSmStop'])

        # nothing is sent until something moves us and kicks the broadcast again
        self.mover.pos = (4.0, 2.0, 3.0)
        self.mover.kickPosHprBroadcast()
        self.assertEqual(self.fields(), ['setSmXY', 'setSmXY', 'setSmStop', 'setSmXY'])

    def test_kicking_a_running_broadcast_does_not_start_another(self):
        self.mover.kickPosHprBroadcast()
        self.mover.kickPosHprBroadcast()

        self.assertEqual(self.taskMgr.doMethodLater.call_count, 1)

    def test_a_continuous_broadcast_keeps_running_at_rest(self):
        self.mover.startPosHprBroadcast()
        self.mover.kickPosHprBroadcast()
        for _ in range(3):
            self.assertEqual(self.tick(), Task.again)

        self.assertEqual(self.fields(), ['setSmStop'])

    def test_stopping_removes_the_task(self):
        self.mover.startPosHprBroadcast()
        task = self.mover._posHprBroadcastTask
        self.mover.stopPosHprBroadcast()

        self.taskMgr.remove.assert_called_once_with(task)
        self.assertFalse(self.mover.posHprBroadcastStarted())


if __name__ == '__main__':
    unittest.main()
