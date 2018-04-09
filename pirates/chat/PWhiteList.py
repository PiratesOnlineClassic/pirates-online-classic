# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.chat.PWhiteList
import os

from otp.chat.WhiteList import WhiteList
from pandac.PandaModules import *


class PWhiteList(WhiteList):
    

    def __init__(self):
        vfs = VirtualFileSystem.getGlobalPtr()
        filename = Filename('pwhitelist.txt')
        searchPath = DSearchPath()
        if __debug__:
            searchPath.appendDirectory(Filename.expandFrom('../resources/phase_3/etc'))
        else:
            searchPath.appendDirectory(Filename.expandFrom('phase_3/etc'))

        found = vfs.resolveFilename(filename, searchPath)
        if not found:
            print "Couldn't find whitelist data file!"

        data = vfs.readFile(filename, 1)
        lines = data.split('\n')
        WhiteList.__init__(self, lines)
# okay decompiling .\pirates\chat\PWhiteList.pyc
