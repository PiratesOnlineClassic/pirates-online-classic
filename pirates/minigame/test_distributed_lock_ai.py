import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pirates.minigame import DistributedLockAI as lock_ai_module
from pirates.minigame.DistributedLockDoorAI import DistributedLockDoorAI
from pirates.minigame.minigame_test_util import FakeTaskMgr, FakeInventory, makeAir, sentToAvatar
from pirates.uberdog.UberDogGlobals import InventoryType


class LockTests(unittest.TestCase):
    def setUp(self):
        self.fakeTaskMgr = FakeTaskMgr()
        self.clock = SimpleNamespace(time=100.0)
        self.patchers = [
            patch.object(lock_ai_module, 'taskMgr', self.fakeTaskMgr),
            patch.object(builtins, 'globalClock', SimpleNamespace(getRealTime=lambda: self.clock.time), create=True),
            patch.object(builtins, 'messenger', Mock(), create=True),
        ]
        for patcher in self.patchers:
            patcher.start()

        self.inventories = {101: FakeInventory(0), 102: FakeInventory(0)}
        self.sender = [101]
        self.air, self.avatars = makeAir(self.inventories, self.sender)
        self.lock = self.makeLock(lock_ai_module.DistributedLockAI)

    def tearDown(self):
        for patcher in self.patchers:
            patcher.stop()

    def makeLock(self, cls):
        lock = cls(self.air)
        lock.doId = 7000
        lock.sendUpdate = Mock()
        lock.sendUpdateToAvatarId = Mock()
        lock.acceptOnce = Mock()
        lock.ignore = Mock()
        lock.setDifficulty(20)
        return lock

    def interact(self, avId):
        self.sender[0] = avId
        self.lock.requestInteraction(avId, 0, False)

    def test_difficulty_rounded_to_whole_layers(self):
        self.lock.setDifficulty(25)
        self.assertEqual(self.lock.getDifficulty(), 20)
        self.lock.setDifficulty(5)
        self.assertEqual(self.lock.getNumLayers(), 1)
        self.lock.setDifficulty(500)
        self.assertEqual(self.lock.getNumLayers(), 6)

    def test_sit_down_sends_difficulty_without_seat_response(self):
        self.interact(101)
        self.assertEqual(sentToAvatar(self.lock, 'localAvatarSatDown'), [(101, [101, 20])])
        self.assertEqual(sentToAvatar(self.lock, 'requestSeatResponse'), [])
        self.assertEqual(self.lock.userId, 101)

    def test_only_one_picker_at_a_time(self):
        self.interact(101)
        self.interact(102)
        self.assertIn((102, []), sentToAvatar(self.lock, 'rejectInteraction'))

    def test_solving_opens_lock_and_rewards(self):
        self.interact(101)
        self.clock.time += 5
        self.lock.d_openLock('Pirate 101', 101)
        self.assertEqual(self.lock.getOpen(), 1)
        self.lock.sendUpdate.assert_any_call('setOpen', [1])
        # only the solver's gui shows the solved message
        self.assertEqual(sentToAvatar(self.lock, 'lockSolved'), [(101, ['Pirate 101'])])
        self.assertEqual(self.inventories[101].getReputation(InventoryType.LockpickRep), 20)

        self.fakeTaskMgr.run()
        self.assertIn((101, [2]), sentToAvatar(self.lock, 'requestSeatResponse'))
        self.assertEqual(self.lock.userId, 0)

        # an open lock can't be picked again
        self.interact(102)
        self.assertIn((102, []), sentToAvatar(self.lock, 'rejectInteraction'))

    def test_solve_from_other_avatar_is_ignored(self):
        self.interact(101)
        self.clock.time += 5
        self.sender[0] = 102
        self.lock.d_openLock('Pirate 102', 102)
        self.assertEqual(self.lock.getOpen(), 0)

    def test_instant_solve_is_ignored(self):
        self.interact(101)
        self.lock.d_openLock('Pirate 101', 101)
        self.assertEqual(self.lock.getOpen(), 0)

    def test_exit_frees_lock(self):
        self.interact(101)
        self.lock.requestExit()
        self.assertIn((101, [2]), sentToAvatar(self.lock, 'requestSeatResponse'))
        self.interact(102)
        self.assertEqual(self.lock.userId, 102)

    def test_lock_door(self):
        self.lock = self.makeLock(DistributedLockDoorAI)
        self.interact(101)
        self.clock.time += 5
        self.lock.d_openLock('Pirate 101', 101)
        self.assertEqual(self.lock.getOpen(), 1)
        self.assertEqual(self.lock.getOpenedBy(), 101)


if __name__ == '__main__':
    unittest.main()
