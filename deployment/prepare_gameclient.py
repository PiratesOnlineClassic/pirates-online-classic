import os
import shutil
import StringIO
import argparse
import zlib
import pyaes
import hashlib

from panda3d.core import *


parser = argparse.ArgumentParser()
parser.add_argument('--build-dir', default='build',
                    help='The directory of which the build was prepared.')
parser.add_argument('--resources-dir', default='../resources',
                    help='The directory of which the resources are located.')
parser.add_argument('--dc-files', nargs='*', default=['astron/dclass/otp.dc', 'astron/dclass/pirates.dc'],
                    help='The client distributed class files.')
parser.add_argument('--config-files', nargs='*', default=['config/general.prc'],
                    help='The client PRC configuration files.')
parser.add_argument('--resources-files', nargs='*', default=['phase_2', 'phase_3', 'phase_4', 'phase_5'],
                    help='The game resources directories.')
parser.add_argument('--resources-compression-level', default=9,
                    help='The compression level in which the multifiles will be compressed with...')
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

# create a new AES key and iv to encrypt the game data with...
IV = os.urandom(16)
KEY = os.urandom(16)

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

ignored_files = [
    'OTPInternalRepository',
    'PiratesAIRepository',
    'PiratesUberRepository',
    'ServiceStart',
    'InventoryInit'
]

def cleanup_tree(directory):

    def recurse(path):
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)

            if os.path.isdir(filepath):
                recurse(filepath)
            elif os.path.isfile(filepath):
                if (filepath.endswith('AI.py') or filepath.endswith('UD.py')) and 'CrewHUD' not in filepath:
                    os.remove(filepath)

                for filename in ignored_files:
                    if filename in filepath:
                        os.remove(filepath)
                        break

    recurse(directory)

# copy over the required game source modules
for package in args.modules:
    fullpath = os.path.join(args.build_dir, package)

    if not os.path.exists(fullpath):
        shutil.copytree(package, fullpath)

    cleanup_tree(fullpath)

RUNTIME_DATA = """import __builtin__
import sys
import os
import hashlib

def get_md5(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)

        f.close()

    return hash_md5.hexdigest()

# run checks to ensure the virtualized panda3d directory
# has not been tampered with...
if os.path.exists('panda3d/__init__.py'):
    raise SystemExit

if not os.path.exists('panda3d/__init__.pyc'):
    raise SystemExit

if get_md5('panda3d/__init__.pyc') != '{0}':
    raise SystemExit

import StringIO
import zlib
import pyaes

from panda3d.core import *


def main():
    IV = {1}
    KEY = {2}

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
            if not line or not line.strip():
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

    vfs = VirtualFileSystem.getGlobalPtr()
    mfs = [2, 3, 4, 5]

    for mf in mfs:
        filepath = 'resources/phase_%d.mf' % mf

        if not os.path.isfile(filepath):
            raise IOError('Failed to find multifile: phase_%d!' % mf)

        f = Multifile()
        f.openRead(filepath)
        f.setMultifileName('phase_%d' % mf)

        if not vfs.mount(f, '.', VirtualFileSystem.MFReadOnly):
            raise RuntimeError('Failed to mount multifile: phase_%d!' % mf)

        if not vfs.mount(f, 'phase_%d' % mf, VirtualFileSystem.MFReadOnly):
            raise RuntimeError('Failed to mount multifile: phase_%d!' % mf)

    from pirates.piratesbase import PiratesStart

    return 0

if __name__ == '__main__':
    sys.exit(main())"""

# pack the panda3d init constructor compiled file md5
def get_md5(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)

        f.close()

    return hash_md5.hexdigest()

PANDA3D_MD5 = get_md5('panda3d/__init__.pyc')

# copy over the runtime main module
with open(os.path.join(args.build_dir, args.main_module), 'w') as f:
    io = StringIO.StringIO(RUNTIME_DATA.format(
        PANDA3D_MD5, repr(IV), repr(KEY)))

    for line in io.readlines():
        f.write(line)

    io.close()
    f.close()

# change our directory paths to the resources root dir
os.chdir(args.resources_dir)

# pack up the resource files
for filename in args.resources_files:
    filepath = os.path.join(args.resources_dir, filename)

    # change our directory paths to the resource folder...
    os.chdir(filename)
    filepaths = os.listdir('./')

    if '%s.mf' % filename in filepaths:
        filepaths.remove('%s.mf' % filename)

    cmd = 'multify'
    cmd += ' -%d' % args.resources_compression_level
    cmd += ' -c'
    cmd += ' -f'
    cmd += ' ../%s.mf' % filename

    for filepath in filepaths:
        cmd += ' %s' % filepath

    os.system(cmd)

    # change our directory paths back...
    os.chdir('../')

print 'Done building game data.'
