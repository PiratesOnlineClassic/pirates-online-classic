import os
import shutil
import StringIO
import argparse
import zlib
import pyaes

from panda3d.core import *


parser = argparse.ArgumentParser()
parser.add_argument('--build-dir', default='build',
                    help='The directory of which the build was prepared.')
parser.add_argument('--dc-files', nargs='*', default=['astron/dclass/otp.dc', 'astron/dclass/pirates.dc'],
                    help='The client distributed class files.')
parser.add_argument('--config-files', nargs='*', default=['config/general.prc'],
                    help='The client PRC configuration files.')
parser.add_argument('--data-file', default='gamedata.bin',
                    help='The client\'s gamedata file which contains the DClass and PRC data...')
parser.add_argument('--main-module', default='runtime.py',
                    help='The module to load at the start of the game.')
parser.add_argument('modules', nargs='*', default=['otp', 'pirates'],
                    help='The Pirates Online Classic packages to be included in the build.')
args = parser.parse_args()

# create the build directory if it doesn't already exist...
if not os.path.exists(args.build_dir):
    os.mkdir(args.build_dir)

print 'Building the game data...'

datagram = Datagram()

for filename in args.config_files:
    with open(filename, 'r') as f:
        data = f.read()
        f.close()

    data = zlib.compress(data)

    other_datagram = Datagram()
    other_datagram.add_uint16(len(data))
    other_datagram.append_data(data)

    datagram.append_data(other_datagram.get_message())

for filename in args.dc_files:
    with open(filename, 'r') as f:
        data = f.read()
        f.close()

    data = zlib.compress(data)

    other_datagram = Datagram()
    other_datagram.add_uint16(len(data))
    other_datagram.append_data(data)

    datagram.append_data(other_datagram.get_message())

IV = ''.join(['0'] * 16)
KEY = 'ExampleKey123456'

cipher = pyaes.AESModeOfOperationOFB(
    KEY, iv=IV)

data = datagram.get_message()

datagram = Datagram()
datagram.add_uint8(len(args.dc_files))
datagram.add_uint8(len(args.config_files))
datagram.append_data(data)

data = cipher.encrypt(datagram.get_message())

with open(os.path.join(args.build_dir, args.data_file), 'wb') as f:
    f.write(data)
    f.close()

# copy over the required game source modules
for package in args.modules:
    fullpath = os.path.join(args.build_dir, package)

    if os.path.exists(fullpath):
        continue

    shutil.copytree(package, fullpath)

RUNTIME_DATA = """import sys
import os
import __builtin__
import StringIO
import zlib
import pyaes

from panda3d.core import *


def main():
    IV = ''.join(['0'] * 16)
    KEY = 'ExampleKey123456'

    cipher = pyaes.AESModeOfOperationOFB(
        KEY, iv=IV)

    del IV
    del KEY

    if not os.path.exists('gamedata.bin'):
        raise SystemExit

    with open('gamedata.bin', 'rb') as f:
        data = f.read()
        f.close()

    try:
        data = cipher.decrypt(data)
    except:
        raise SystemExit

    del cipher

    datagram = Datagram(data)
    di = DatagramIterator(datagram)

    del data

    try:
        num_dc_files = di.get_uint8()
        num_config_files = di.get_uint8()
    except:
        raise SystemExit

    for _ in xrange(num_config_files):
        try:
            length = di.get_uint16()
        except:
            raise SystemExit

        if not di.get_remaining_size():
            raise SystemExit

        try:
            data = zlib.decompress(di.extract_bytes(length))
        except:
            raise SystemExit

        io = StringIO.StringIO(data)

        for line in io.readlines():
            if not line or line == '\n':
                continue

            load_prc_file_data('config data', line)

        io.close()

        del length
        del data
        del io

    __builtin__.dcStream = StringStream()

    for _ in xrange(num_dc_files):
        try:
            length = di.get_uint16()
        except:
            raise SystemExit

        if not di.get_remaining_size():
            raise SystemExit

        try:
            data = zlib.decompress(di.extract_bytes(length))
        except:
            raise SystemExit

        dcStream.set_data(dcStream.get_data() + data)

        del length
        del data

    from pirates.piratesbase import PiratesStart

    return 0

if __name__ == '__main__':
    sys.exit(main())"""

# copy over the runtime main module
with open(os.path.join(args.build_dir, args.main_module), 'w') as f:
    f.write(RUNTIME_DATA)
    f.close()

print 'Done building game data.'
