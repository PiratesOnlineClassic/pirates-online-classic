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


if __name__ == '__main__':
    unittest.main()
