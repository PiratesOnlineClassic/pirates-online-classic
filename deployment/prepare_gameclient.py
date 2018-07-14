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

# copy over the runtime main module
shutil.copy2(os.path.join('deployment', args.main_module), os.path.join(
    args.build_dir, args.main_module))

print 'Done building game data.'
