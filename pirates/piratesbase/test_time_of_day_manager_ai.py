import unittest
from unittest.mock import Mock, patch

from pirates.piratesbase import PiratesGlobals, TODGlobals
from pirates.piratesbase import DistributedTimeOfDayManagerAI as todModule


class TimeOfDayManagerTests(unittest.TestCase):
    def makeManager(self):
        manager = todModule.DistributedTimeOfDayManagerAI.__new__(todModule.DistributedTimeOfDayManagerAI)
        manager.doId = 1
        manager.cycleType = TODGlobals.TOD_REGULAR_CYCLE
        manager.startingState = TODGlobals.getStartingState(manager.cycleType)
        manager.startingTime = 0
        manager.cycleDuration = 100.0
        manager.currentState = manager.startingState
        manager.stateTime = 0
        manager.nextProcessStateChange = None
        manager.timeOfDayStateMethodList = []
        manager.sendUpdate = Mock()
        return manager

    def test_state_change_keeps_cycle_anchor(self):
        manager = self.makeManager()
        anchor = manager.getSync()
        nextState = TODGlobals.getNextStateId(manager.cycleType, manager.startingState)
        with patch.object(manager, '_computeCurrentState', return_value=(nextState, 1.0)), \
                patch.object(manager, '_waitForNextState'):
            manager._processStateChange()

        self.assertEqual(manager.getSync(), anchor)
        self.assertEqual(manager.getCurrentState(), nextState)

    def test_is_day_and_night_use_current_state(self):
        manager = self.makeManager()
        manager.currentState = PiratesGlobals.TOD_NIGHT
        self.assertTrue(manager.isNight())
        self.assertFalse(manager.isDay())

    def test_cycle_change_restarts_anchor_and_syncs(self):
        manager = self.makeManager()
        with patch.object(manager, '_processStateChange') as process, \
                patch.object(todModule.globalClockDelta, 'getRealNetworkTime', return_value=1234):
            manager.changeCycleType(TODGlobals.TOD_HALLOWEEN_CYCLE)

        startingState = TODGlobals.getStartingState(TODGlobals.TOD_HALLOWEEN_CYCLE)
        manager.sendUpdate.assert_called_once_with('sync', [TODGlobals.TOD_HALLOWEEN_CYCLE,
            startingState, 1234, 100.0])
        process.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
