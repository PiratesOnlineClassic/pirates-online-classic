import sys
import os
import argparse

if not os.path.exists('built'):
    os.mkdir('built')

sys.path.append('nirai/src')

parser = argparse.ArgumentParser()
parser.add_argument('--compile-cxx', '-c', action='store_true',
                    help='Compile the CXX codes and generate sample.exe into built.')
parser.add_argument('--make-nri', '-n', action='store_true',
                    help='Generate sample.nri.')
parser.add_argument('--models', '-m', action='store_false',
                    help='Pack models.mf.')
args = parser.parse_args()

from direct.distributed.PyDatagram import PyDatagram
from panda3d.core import Datagram
from niraitools import *


def niraicall_obfuscate(code):
    # We'll obfuscate if len(code) % 4 == 0
    # This way we make sure both obfuscated and non-obfuscated code work.
    if len(code) % 4:
        return False, None

    # There are several ways to obfuscate it
    # For this example, we'll invert the string
    return True, code[::-1]

niraimarshal.niraicall_obfuscate = niraicall_obfuscate

class ClassicPackager(NiraiPackager):
    HEADER = 'POC'
    BASEDIR = '..' + os.sep

    def __init__(self, outfile):
        NiraiPackager.__init__(self, outfile)
        self.__manglebase = self.get_mangle_base(self.BASEDIR)

        self.add_panda3d_dirs()
        self.add_default_lib()
        self.add_directory(self.BASEDIR, mangler=self.__mangler)

    def add_source_dir(self, dir):
        self.add_directory(self.BASEDIR + dir, mangler=self.__mangler)

    def add_data_file(self, file):
        mb = self.get_mangle_base('data/')
        self.add_file('data/%s.py' % file, mangler=lambda x: x[mb:])

    def __mangler(self, name):
        excluded_files = [
            'PiratesAIRepository',
            'PiratesUberRepository',
            'OTPInternalRepository',
            'PiratesInternalRepository',
            'ServiceStart',
            'InventoryInit'
        ]

        if name.endswith('AI') or name.endswith('UD') or name in excluded_files:
            return ''

        return name[self.__manglebase:].strip('.')

    def generate_niraidata(self):
        print 'Generating niraidata...'

        config = self.get_file_contents('config.prc', True)
        niraidata = 'CONFIG = %r' % config
        self.add_module('niraidata', niraidata, compile=True)

    def process_modules(self):
        dg = PyDatagram()
        dg.addUint32(len(self.modules))

        for moduleName in self.modules:
            data, size = self.modules[moduleName]

            dg.addString(moduleName)
            dg.addInt32(size)
            dg.appendData(data)

        data = dg.getMessage()

        iv = '\0' * 16
        key = 'ExampleKey123456'
        return aes.encrypt(data, key, iv)

if args.compile_cxx:
    if sys.platform == 'win32':
        output = 'PiratesClassic.exe'

    elif sys.platform == 'darwin':
        output = 'Pirates\ Classic'

    else:
        raise Exception('The platform "%s" in use is not supported.' % (
            sys.platform))

    compiler = NiraiCompiler(output)
    compiler.add_nirai_files()
    compiler.add_source('src/classic.cxx')
    compiler.run()

if args.make_nri:
    pkg = ClassicPackager('built/gamedata.bin')
    pkg.add_source_dir('otp')
    pkg.add_source_dir('pirates')
    pkg.add_data_file('NiraiStart')
    pkg.generate_niraidata()
    pkg.write_out()

if args.models:
    os.chdir('..')
    cmd = 'multify -cf build/built/models.mf models'
    p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True)
    v = p.wait()

    if v != 0:
        print 'The following command returned non-zero value (%d): %s' % (
            v, cmd[:100] + '...')

        sys.exit(1)
