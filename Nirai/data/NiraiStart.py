import __builtin__
import os
import sys

from panda3d.core import *

import aes
import niraidata

# Config
prc = niraidata.CONFIG
iv, key, prc = prc[:16], prc[16:32], prc[32:]
prc = aes.decrypt(prc, key, iv)

for line in prc.split('\n'):
    line = line.strip()
    if line:
        loadPrcFileData('nirai config', line)

del prc
del iv
del key

# DC
__builtin__.dcStream = StringStream()

dc = niraidata.DC
iv, key, dc = dc[:16], dc[16:32], dc[32:]
dc = aes.decrypt(dc, key, iv)

dcStream.setData(dc)
del dc
del iv
del key

# Phases
vfs = VirtualFileSystem.getGlobalPtr()
phases = [
    2,
    3,
    4,
    5
]

for phase in phases:
    phase_name = 'phase_%d' % phase
    filepath = 'resources/%s.mf' % phase_name

    if not os.path.isfile(filepath):
        raise IOError('Failed to find multifile: %s!' % phase_name)

    f = Multifile()
    f.openRead(filepath)
    f.setMultifileName(phase_name)

    if not vfs.mount(f, '.', VirtualFileSystem.MFReadOnly):
        raise RuntimeError('Failed to mount multifile: %s!' % phase_name)

    if not vfs.mount(f, phase_name, VirtualFileSystem.MFReadOnly):
        raise RuntimeError('Failed to mount multifile: %s!' % phase_name)

import pirates.piratesbase.PiratesStart
