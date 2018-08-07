from panda3d.core import *
import __builtin__, os, sys
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

import pirates.piratesbase.PiratesStart
