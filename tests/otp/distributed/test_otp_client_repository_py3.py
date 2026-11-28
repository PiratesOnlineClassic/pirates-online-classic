import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

# The login modules read the launcher and game at import time.
_addedBuiltins = []
for _name, _make in (('launcher', lambda: __import__('pirates.launcher.PiratesDummyLauncher', fromlist=['x']).PiratesDummyLauncher()),
                     ('game', lambda: SimpleNamespace(name='pirates', process='client'))):
    if not hasattr(builtins, _name):
        setattr(builtins, _name, _make())
        _addedBuiltins.append(_name)

try:
    from otp.distributed.OTPClientRepository import OTPClientRepository
except ImportError:  # libotp is not part of the repository
    OTPClientRepository = None
finally:
    for _name in _addedBuiltins:
        delattr(builtins, _name)


@unittest.skipIf(OTPClientRepository is None, 'OTPClientRepository needs libotp')
class LeakDetectionTests(unittest.TestCase):
    # Logging out runs the leak detectors, which used Disney's Python task
    # manager (taskMgr.taskList), base.GarbageCollectTaskName and an unimported
    # CConnectionRepository.

    def test_detect_leaked_tasks(self):
        name = 'test-leaked-task'
        taskMgr.add(lambda task: task.cont, name)
        try:
            self.assertGreaterEqual(OTPClientRepository.detectLeakedTasks(SimpleNamespace(notify=Mock())), 1)
        finally:
            taskMgr.remove(name)

    def test_detect_leaked_events(self):
        OTPClientRepository.detectLeakedEvents(SimpleNamespace(notify=Mock()))


@unittest.skipIf(OTPClientRepository is None, 'OTPClientRepository needs libotp')
class PendingGenerateTests(unittest.TestCase):
    # Objects that arrive while an interest is still opening are held until the
    # interest is done. A ship that sails out of view before it's parts arrive
    # removes it's parts interest, those parts must not be generated afterwards.

    def makeRepository(self, interest):
        from direct.distributed.DoInterestManager import DoInterestManager
        from panda3d.core import Datagram
        cr = OTPClientRepository.__new__(OTPClientRepository)
        cr._OTPClientRepository__pendingGenerates = {7: [(500, 400, 2, 1, Datagram(b'\0' * 16), [])]}
        cr._OTPClientRepository__pendingMessages = {7: []}
        cr._OTPClientRepository__doId2pendingInterest = {500: 7}
        cr._OTPClientRepository__doGenerate = Mock()
        cr._interests = {7: interest} if interest else {}
        return cr

    def playBack(self, cr):
        cr._OTPClientRepository__playBackGenerates(7)

    def test_generates_play_back_when_the_interest_completes(self):
        cr = self.makeRepository(SimpleNamespace(isPendingDelete=lambda: False))
        self.playBack(cr)
        cr._OTPClientRepository__doGenerate.assert_called_once()
        self.assertEqual(cr._OTPClientRepository__doId2pendingInterest, {})

    def test_generates_are_dropped_for_a_removed_interest(self):
        for interest in (None, SimpleNamespace(isPendingDelete=lambda: True)):
            cr = self.makeRepository(interest)
            self.playBack(cr)
            cr._OTPClientRepository__doGenerate.assert_not_called()
            self.assertEqual(cr._OTPClientRepository__pendingGenerates, {})
            self.assertEqual(cr._OTPClientRepository__pendingMessages, {})
            self.assertEqual(cr._OTPClientRepository__doId2pendingInterest, {})


if __name__ == '__main__':
    unittest.main()
