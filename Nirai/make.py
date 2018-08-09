import sys
import os
import argparse
import struct

from panda3d.core import *

sys.path.append('nirai/src')

from niraitools import *


parser = argparse.ArgumentParser()
parser.add_argument('--compile-cxx', '-c', action='store_true',
                    help='Compile the CXX codes and generate classic.exe into built.')
parser.add_argument('--make-nri', '-n', action='store_true',
                    help='Generate classic NRI.')
parser.add_argument('--make-mfs', '-m', action='store_true',
                    help='Make multifiles')
args = parser.parse_args()

if not os.path.exists('built'):
    os.mkdir('built')

def niraicall_obfuscate(code):
    # We'll obfuscate if len(code) % 4 == 0
    # This way we make sure both obfuscated and non-obfuscated code work.
    if len(code) % 4:
        return False, None

    # Reverse
    code = code[::-1]

    # XOR
    key = ['T', 'B', 'P', 'H', 'P', 'Q', 'J', 'A', 'H', 'A', 'P', 'Z']
    output = []

    for i in range(len(code)):
        xor_num = ord(code[i]) ^ ord(key[i % len(key)])
        output.append(chr(xor_num))

    code = ''.join(output)
    return True, code


niraimarshal.niraicall_obfuscate = niraicall_obfuscate


class SourcePackager(NiraiPackager):
    HEADER = 'CLASSIC'
    BASEDIR = '../src' + os.sep

    def __init__(self, outfile):
        NiraiPackager.__init__(self, outfile)

        self.__manglebase = self.get_mangle_base(self.BASEDIR)
        self.add_panda3d_dirs()
        self.add_default_lib()

    def add_source_dir(self, dir):
        self.add_directory(self.BASEDIR + dir, mangler=self.__mangler)

    def add_data_file(self, file):
        mb = self.get_mangle_base('data/')
        self.add_file('data/%s.py' % file, mangler=lambda x: x[mb:])

    def __mangler(self, name):
        return name[self.__manglebase:].strip('.')

    def generate_niraidata(self):
        print 'Generating niraidata'
        config_files = [
            self.get_file_contents('../src/config/general.prc'),
        ]

        config_iv = self.generate_key(16)
        config_key = self.generate_key(16)

        config_data = ''.join(config_files)
        config_data = config_iv + config_key + aes.encrypt(
            config_data, config_key, config_iv)

        niraidata = 'CONFIG = %r' % config_data
        self.add_module('niraidata', niraidata, compile=True)

    def process_modules(self):
        dg = Datagram()
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
    compiler = NiraiCompiler('classic.exe')

    compiler.add_nirai_files()
    compiler.add_source('src/classic.cxx')

    compiler.run()

# Compile the game data
if args.make_nri:
    pkg = SourcePackager('built/classic.bin')

    pkg.add_source_dir('otp')
    pkg.add_source_dir('pirates')

    pkg.add_data_file('NiraiStart')

    pkg.generate_niraidata()

    pkg.write_out()

if args.make_mfs:
    os.chdir('../src/resources')
    cmd = ''
    for phasenum in ['2', '3', '4', '5']:
        print 'phase_%s' % (phasenum)
        cmd = 'multify -cf ../build/built/resources/default/phase_%s.mf phase_%s' % (phasenum, phasenum)
        p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
        v = p.wait()

        if v != 0:
            print 'The following command returned non-zero value (%d): %s' % (v, cmd[:100] + '...')
            sys.exit(1)
