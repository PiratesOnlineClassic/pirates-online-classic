import os
import subprocess
import sys
import tempfile
import textwrap
import types
import unittest

from tests import REPO_ROOT

BUILD_DIR = os.path.join(str(REPO_ROOT), 'build')


class EmbeddedClientFilesTests(unittest.TestCase):
    # the compiled client carries it's config and dc files, nothing a player
    # could edit is read from the game folder

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        sys.path.insert(0, BUILD_DIR)
        self.addCleanup(sys.path.remove, BUILD_DIR)
        import nuitka_build
        self.nuitka_build = nuitka_build
        self.module = os.path.join(self.tmp.name, 'poc_client_files.py')

    def writeModule(self):
        original = self.nuitka_build.EMBEDDED_MODULE
        self.nuitka_build.EMBEDDED_MODULE = self.module
        try:
            self.nuitka_build.write_embedded_module(types.SimpleNamespace(python=sys.executable))
        finally:
            self.nuitka_build.EMBEDDED_MODULE = original

    def test_module_holds_the_release_files(self):
        self.writeModule()
        namespace = {}
        exec(open(self.module).read(), namespace)
        files = namespace['getGameFiles']()
        self.assertEqual(sorted(files), ['astron/dclass/otp.dc', 'astron/dclass/pirates.dc',
            'config/dev.prc', 'config/general.prc', 'config/performance.prc', 'config/release.env'])

        # the release settings fill the dev.prc slot, never the developer ones
        with open(os.path.join(BUILD_DIR, 'release.prc'), 'rb') as f:
            self.assertEqual(files['config/dev.prc'], f.read())

        # and nothing is readable as plain text in the module
        self.assertNotIn(b'want-dev-access', open(self.module, 'rb').read())
        self.assertEqual([name for name, text in namespace['getPandaPrc']()], ['Config.prc', 'Confauto.prc'])

    def test_game_loads_the_embedded_files_and_ignores_the_disk(self):
        self.writeModule()
        gameDir = os.path.join(os.path.realpath(self.tmp.name), 'game')
        os.makedirs(os.path.join(gameDir, 'config'))
        with open(os.path.join(gameDir, 'config', 'personal.prc'), 'w') as f:
            f.write('want-dev-access #t\nwindow-title Hacked\n')

        script = textwrap.dedent('''
            import os, sys
            sys.path[:0] = [%(build)r, %(tmp)r]
            import client_main, poc_client_files
            os.chdir(%(game)r)
            from panda3d.core import loadPrcFile, ConfigVariableBool, ConfigVariableString, \\
                getModelPath, Filename
            from panda3d.direct import DCFile
            client_main.load_embedded_panda_prc(poc_client_files)
            client_main.mount_embedded_game_files(%(game)r, poc_client_files)
            # what PiratesStart does:
            loadPrcFile('config/general.prc')
            loadPrcFile('config/dev.prc')
            loadPrcFile('config/performance.prc')
            if os.path.exists('config/personal.prc'):
                loadPrcFile('config/personal.prc')
            dc = DCFile()
            print('title', ConfigVariableString('window-title', '').getValue())
            print('devaccess', ConfigVariableBool('want-dev-access', True).getValue())
            print('modelpath', [getModelPath().getDirectory(i).toOsSpecific()
                for i in range(getModelPath().getNumDirectories())])
            print('dc', dc.read(Filename('astron/dclass/pirates.dc')), dc.getNumClasses() > 100)
            print('ondisk', sorted(os.listdir(%(game)r + '/config')))
        ''') % {'build': BUILD_DIR, 'tmp': self.tmp.name, 'game': gameDir}

        env = dict(os.environ, PYTHONPATH=str(REPO_ROOT))
        result = subprocess.run([sys.executable, '-c', script], cwd=self.tmp.name, env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout.decode()
        self.assertEqual(result.returncode, 0, output)
        lines = dict(line.split(' ', 1) for line in output.splitlines() if ' ' in line and
                     line.split(' ', 1)[0] in ('title', 'devaccess', 'modelpath', 'dc', 'ondisk'))
        self.assertEqual(lines['title'], 'Pirates Online Classic')
        self.assertEqual(lines['devaccess'], 'False')
        # release.prc's $THIS_PRC_DIR model-path still finds ../resources beside the game folder
        self.assertIn(os.path.join(os.path.realpath(self.tmp.name), 'resources'),
            [os.path.normpath(path) for path in eval(lines['modelpath'])])
        self.assertEqual(lines['dc'], 'True True')
        # nothing was written to the game folder on disk
        self.assertEqual(lines['ondisk'], "['personal.prc']")


if __name__ == '__main__':
    unittest.main()
