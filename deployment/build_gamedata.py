import os
import sys

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--build-dir', default='build',
                    help='The directory of which the build was prepared.')
parser.add_argument('--output', default='gamedata.pyd',
                    help='The built file.')
parser.add_argument('--main-module', default='pirates/piratesbase/PiratesStart.py',
                    help='The module to load at the start of the game.')
parser.add_argument('modules', nargs='*', default=['otp', 'pirates'],
                    help='The Pirates Online Rewritten modules to be included in the build.')
args = parser.parse_args()

print 'Building the game data...'

if not os.path.exists(args.build_dir):
    os.mkdir(args.build_dir)

cmd = sys.executable + ' -m direct.showutil.pfreeze'
args.modules.extend(['direct', 'pandac'])
for module in args.modules:
    cmd += ' -i %s.*.*' % module

cmd += ' -i encodings.*'
cmd += ' -i base64'
cmd += ' -i site'
cmd += ' -i pirates.leveleditor.worldData.*'

extension_modules = [
    'OpenSSL',
    'Crypto',
    'panda3d',
    'cryptography',
    'wx'
]

for extension_module in extension_modules:
    cmd += ' -x %s' % extension_module

cmd += ' -o %s/%s' % (args.build_dir, args.output)
os.system(cmd)

print 'Done building game data.'
