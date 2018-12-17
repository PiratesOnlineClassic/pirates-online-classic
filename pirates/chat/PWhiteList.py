import os
from pandac.PandaModules import *
from otp.chat.WhiteList import WhiteList

class PWhiteList(WhiteList):
    
    def __init__(self):
        vfs = VirtualFileSystem.getGlobalPtr()
        filename = Filename('pwhitelist.txt')
        searchPath = DSearchPath()
        searchPath.appendDirectory(Filename('.'))
        searchPath.appendDirectory(Filename('etc'))
        searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$PIRATES/src/chat')))
        searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('pirates/src/chat')))
        searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('pirates/chat')))
        found = vfs.resolveFilename(filename, searchPath)
        if not found:
            print "Couldn't find whitelist data file!"
        
        data = vfs.readFile(filename, 1)
        lines = data.split('\n')
        WhiteList.__init__(self, lines)


