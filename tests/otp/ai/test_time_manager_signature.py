import os
import subprocess
import sys
import textwrap
import unittest

from tests import REPO_ROOT

# importing TimeManagerAI builds a headless AI base that would clash with the
# graphical base other suites set up, so the check runs in it's own process
SCRIPT = textwrap.dedent('''
    import builtins
    from types import SimpleNamespace
    from unittest.mock import Mock
    class game:
        name = 'pirates'
        process = 'server'
    builtins.game = game
    from panda3d.core import HashVal
    from otp.ai.TimeManagerAI import TimeManagerAI

    def run(expected, reported, hasPycHash=False):
        air = SimpleNamespace(events=[], getAvatarIdFromSender=lambda: 5)
        air.writeServerEvent = lambda *a: air.events.append(a)
        mgr = TimeManagerAI.__new__(TimeManagerAI)
        mgr.air = air
        mgr.notify = Mock()
        builtins.base = SimpleNamespace(config=SimpleNamespace(
            GetString=lambda name, default='': expected))
        pycHash = HashVal()
        if hasPycHash:
            pycHash.hashString('test client bytecode signature')
        mgr.setSignature(reported, HashVal().asBin(), pycHash.asBin())
        return [e[0] for e in air.events], air.events

    kinds, _ = run('', 'abc123')
    assert 'client-signature' in kinds and 'suspicious' not in kinds, kinds

    kinds, _ = run('abc123', 'abc123')
    assert 'suspicious' not in kinds, kinds

    kinds, events = run('abc123', 'deadbeef')
    suspicious = [e for e in events if e[0] == 'suspicious']
    assert len(suspicious) == 1 and 'deadbeef' in suspicious[0][2], events

    kinds, events = run('', '', hasPycHash=True)
    assert 'client-py-signature' in kinds and events[-1][1] == 5, events
    print('OK')
''')


class SignatureTests(unittest.TestCase):
    def test_signature_is_logged_and_mismatch_is_flagged(self):
        env = dict(os.environ, PYTHONPATH=str(REPO_ROOT))
        result = subprocess.run([sys.executable, '-c', SCRIPT], env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(result.returncode, 0, result.stdout.decode())
        self.assertIn('OK', result.stdout.decode())


if __name__ == '__main__':
    unittest.main()
