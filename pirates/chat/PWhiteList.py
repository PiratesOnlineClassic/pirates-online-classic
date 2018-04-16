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
