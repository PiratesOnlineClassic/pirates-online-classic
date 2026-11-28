import os
import sys
import unittest

from tests import REPO_ROOT

BUILD_DIR = os.path.join(str(REPO_ROOT), 'build')


class ClientHardeningTests(unittest.TestCase):
    # the anti-debug and self-signature measures are off for a source checkout
    # (no __compiled__), and never raise

    def setUp(self):
        sys.path.insert(0, BUILD_DIR)
        self.addCleanup(sys.path.remove, BUILD_DIR)
        import client_main
        self.client_main = client_main

    def test_measures_are_inert_outside_a_release(self):
        self.assertFalse(self.client_main.is_release())
        # no debugger check and no signature when run from a checkout
        self.assertIsNone(self.client_main.executable_signature())
        self.client_main.apply_anti_debug()  # must not raise or exit

    def test_signature_hashes_the_executable_when_release(self):
        cm = self.client_main
        original = cm.__dict__.get('__compiled__', None)
        had = '__compiled__' in cm.__dict__
        cm.__dict__['__compiled__'] = object()
        try:
            digest = cm.executable_signature()
        finally:
            if had:
                cm.__dict__['__compiled__'] = original
            else:
                cm.__dict__.pop('__compiled__', None)
        # a 64-character sha-256 hex digest of some readable file (the interpreter)
        self.assertIsNotNone(digest)
        self.assertEqual(len(digest), 64)
        int(digest, 16)


if __name__ == '__main__':
    unittest.main()
