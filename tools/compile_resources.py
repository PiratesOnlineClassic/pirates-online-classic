from direct.directnotify.DirectNotifyGlobal import directNotify
import subprocess
import argparse
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument('--resources', default='../resources', help='Resources folder to compile')
parser.add_argument('ignore', nargs='*', default=['.git'], help='Folders to ignore when compiling')
args = parser.parse_args()

notify = directNotify.newCategory('CompileResources')
notify.setInfo(True)

if __name__ == "__main__":
    if not os.path.exists(args.resources):
        notify.warning("Unable to locate resources folder! %s does not exist!" % args.resources)
        sys.exit()

    notify.info("Compiling folders in %s..." % args.resources)
    os.chdir(args.resources)

    phases = os.walk('.').next()[1]
    for phase in phases:

        if phase in args.ignore:
            continue

        notify.info("Compiling %s..." % phase)

        if os.path.exists('./%s.mf' % phase):
            notify.info('Found old %s multifile. Removing...' % phase)
            os.remove('%s.mf' % phase)

        cmd = 'multify -cf ./%s.mf %s' % (phase, phase)
        p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
        v = p.wait()

        if v != 0:
            notify.error('The following command returned non-zero value (%d): %s' % (v, cmd[:100] + '...'))
        else:
            notify.info('%s.mf built.' % phase)

