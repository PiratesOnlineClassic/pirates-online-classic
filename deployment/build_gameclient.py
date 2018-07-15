import os
import sys

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--build-dir', default='build',
                    help='The directory of which the build was prepared.')
parser.add_argument('--output', default='PiratesClassic.exe',
                    help='The built executable file.')
parser.add_argument('--main-module', default='runtime.py',
                    help='The module to load at the start of the game.')
parser.add_argument('modules', nargs='*', default=['otp', 'pirates'],
                    help='The Pirates Online Classic modules to be included in the build.')
args = parser.parse_args()

# switch our paths to the build directory...
os.chdir(args.build_dir)

print 'Building the game client...'

cmd = sys.executable + ' -OO -m direct.showutil.pfreeze'
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

cmd += ' -o %s' % args.output
cmd += ' %s' % args.main_module
os.system(cmd)

print 'Done building game client.'
