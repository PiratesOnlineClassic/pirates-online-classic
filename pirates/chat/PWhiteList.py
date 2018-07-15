import os

from panda3d.core import *
from otp.chat.WhiteList import WhiteList


class PWhiteList(WhiteList):

    def __init__(self):
        vfs = VirtualFileSystem.getGlobalPtr()
        filename = Filename('pwhitelist.txt')
        searchPath = DSearchPath()
        if __debug__:
            searchPath.appendDirectory(Filename.expandFrom('../resources/phase_3/etc'))
        else:
            searchPath.appendDirectory(Filename.expandFrom('phase_3/etc'))
            searchPath.appendDirectory(Filename('.'))
            searchPath.appendDirectory(Filename('etc'))

        found = vfs.resolveFilename(filename, searchPath)
        if not found:
            print "Couldn't find whitelist data file!"

        data = vfs.readFile(filename, 1)
        lines = data.split('\n')
        WhiteList.__init__(self, lines)
