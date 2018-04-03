# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.launcher.PiratesQuickLauncher
Instruction context:
-> 
 234     135  LOAD_FAST             0  'self'
            138  LOAD_ATTR             3  'notify'
            141  LOAD_ATTR             4  'info'
            144  LOAD_CONST            4  'decompressMultifile: Multifile already decompressed: %s'
            147  LOAD_FAST             1  'mfname'
            150  BINARY_MODULO    
            151  CALL_FUNCTION_1       1  None
            154  POP_TOP          
import sys, os, time, string, bz2, random
from direct.showbase.MessengerGlobal import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.EventManagerGlobal import *
from direct.task.TaskManagerGlobal import *
from direct.task.Task import Task
from direct.directnotify.DirectNotifyGlobal import *
from pandac.PandaModules import *
from otp.launcher.LauncherBase import LauncherBase
from pirates.piratesbase import PLocalizer

class PiratesQuickLauncher(LauncherBase):
    __module__ = __name__
    GameName = 'Pirates'
    ArgCount = 3
    LauncherPhases = [
     1, 2, 3, 4, 5, 6]
    TmpOverallMap = [0.16, 0.16, 0.16, 0.16, 0.16, 0.2]
    ForegroundSleepTime = 0.001
    Localizer = PLocalizer
    DecompressMultifiles = True
    launcherFileDbFilename = '%s?%s' % (os.environ.get('GAME_PATCHER_FILE_OPTIONS', 'patcher.ver'), random.randint(1, 1000000000))
    CompressionExt = 'bz2'
    PatchExt = 'pch'

    def __init__(self):
        print 'Running: PiratesQuickLauncher'
        self.heavyDownloadServerList = []
        self.heavyDownloadServer = None
        LauncherBase.__init__(self)
        self.contentDir = '/'
        self.serverDbFileHash = HashVal()
        self.launcherFileDbHash = HashVal()
        self.DECREASE_BANDWIDTH = 0
        self.httpChannel.setDownloadThrottle(0)
        self.showPhase = -1
        self.maybeStartGame()
        self.mainLoop()
        return

    def addDownloadVersion(self, serverFilePath):
        if self.heavyDownloadServer:
            url = URLSpec(self.heavyDownloadServer)
        else:
            url = URLSpec(self.downloadServer)
        origPath = url.getPath()
        if origPath[-1] == '/':
            url.setPath('%s%s' % (origPath, serverFilePath))
        else:
            url.setPath('%s/%s' % (origPath, serverFilePath))
        return url

    def downloadLauncherFileDbDone(self):
        settings = {}
        for line in self.ramfile.readlines():
            line = line.strip()
            equalIndex = line.find('=')
            if equalIndex >= 0:
                key = line[:equalIndex]
                value = line[equalIndex + 1:]
                settings[key] = value

        self.requiredInstallFiles = []
        if sys.platform == 'win32':
            fileList = settings['REQUIRED_INSTALL_FILES']
        else:
            if sys.platform == 'darwin':
                fileList = settings['REQUIRED_INSTALL_FILES_OSX']
            else:
                if sys.platform == 'linux2':
                    fileList = settings['REQUIRED_INSTALL_FILES_LINUX']
                else:
                    self.notify.warning('Unknown sys.platform: %s' % sys.platform)
                    fileList = settings['REQUIRED_INSTALL_FILES']
        for fileDesc in fileList.split():
            fileName, flag = fileDesc.split(':')
            directions = BitMask32(flag)
            extract = directions.getBit(0)
            requiredByLauncher = directions.getBit(1)
            optionalDownload = directions.getBit(2)
            self.notify.info('fileName: %s, flag:=%s directions=%s, extract=%s required=%s optDownload=%s' % (fileName, flag, directions, extract, requiredByLauncher, optionalDownload))
            if not optionalDownload:
                self.requiredInstallFiles.append(fileName)

        self.notify.info('requiredInstallFiles: %s' % self.requiredInstallFiles)
        self.mfDetails = {}
        for mfName in self.requiredInstallFiles:
            currentVer = settings['FILE_%s.current' % mfName]
            details = settings['FILE_%s.%s' % (mfName, currentVer)]
            size, hash = details.split()
            self.mfDetails[mfName] = (currentVer, int(size), hash)
            self.notify.info('mfDetails[%s] = %s' % (mfName, self.mfDetails[mfName]))

        heavyDownloadServerString = settings['PATCHER_BASE_URL_HEAVY_LIFTING']
        for name in string.split(heavyDownloadServerString, ';'):
            url = URLSpec(name, 1)
            self.heavyDownloadServerList.append(url)

        self.getNextHeavyDownloadServer()
        self.resumeInstall()

    def getNextDownloadServer(self):
        if self.heavyDownloadServer:
            return self.getNextHeavyDownloadServer()
        else:
            return LauncherBase.getNextDownloadServer(self)

    def getNextHeavyDownloadServer(self):
        if not self.heavyDownloadServerList:
            self.notify.warning('No more heavy download servers')
            self.heavyDownloadServer = None
            return 0
        self.heavyDownloadServer = self.heavyDownloadServerList.pop(0)
        self.notify.info('Using heavy download server %s.' % self.heavyDownloadServer.cStr())
        return 1

    def resumeMultifileDownload(self):
        curVer, expectedSize, expectedMd5 = self.mfDetails[self.currentMfname]
        localFilename = Filename(self.topDir, Filename('_%s.%s.%s' % (self.currentMfname, curVer, self.CompressionExt)))
        serverFilename = '%s%s.%s.%s' % (self.contentDir, self.currentMfname, curVer, self.CompressionExt)
        if localFilename.exists():
            fileSize = localFilename.getFileSize()
            self.notify.info('Previous partial download exists for: %s size=%s' % (localFilename.cStr(), fileSize))
            self.downloadMultifile(serverFilename, localFilename, self.currentMfname, self.downloadMultifileDone, 0, fileSize, self.downloadMultifileWriteToDisk)
        else:
            self.downloadMultifile(serverFilename, localFilename, self.currentMfname, self.downloadMultifileDone, 0, 0, self.downloadMultifileWriteToDisk)

    def resumeInstall(self):
        while self.requiredInstallFiles:
            self.currentMfname = self.requiredInstallFiles.pop(0)
            self.currentPhaseName = self.Localizer.LauncherPhaseNames[self.currentPhase]
            self.notify.info('currentMfname: %s currentPhase: %s currentPhaseIndex: %s' % (self.currentMfname, self.currentPhase, self.currentPhaseIndex))
            curVer, expectedSize, expectedMd5 = self.mfDetails[self.currentMfname]
            self.curPhaseFile = Filename(self.topDir, Filename(self.currentMfname))
            self.notify.info('working on: %s' % self.curPhaseFile)
            if self.curPhaseFile.exists():
                self.notify.info('file exists')
                fileSize = self.curPhaseFile.getFileSize()
                self.notify.info('clientSize: %s expectedSize: %s' % (fileSize, expectedSize))
                if fileSize == expectedSize:
                    self.notify.info('file is correct size')
                    self.finalizePhase()
                    self.currentPhase += 1
                    self.currentPhaseIndex += 1
                    continue
                else:
                    self.notify.warning('file is not correct size, attempting to resume download')
                    self.resumeMultifileDownload()
                    return
            else:
                self.notify.info('file does not exist - start download')
                self.resumeMultifileDownload()
                return
            self.currentPhase += 1
            self.currentPhaseIndex += 1

        if not self.requiredInstallFiles:
            self.notify.info('ALL PHASES COMPLETE')
            messenger.send('launcherAllPhasesComplete')
            self.cleanup()
            return
        raise StandardError, 'Some phases not listed in LauncherPhases: %s' % self.requiredInstallFiles

    def getDecompressMultifile--- This code section failed: ---

 223       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             1  'DecompressMultifiles'
           6  JUMP_IF_TRUE         14  'to 23'
           9  POP_TOP          

 224      10  LOAD_FAST             0  'self'
          13  LOAD_ATTR             2  'decompressMultifileDone'
          16  CALL_FUNCTION_0       0  None
          19  POP_TOP          
          20  JUMP_FORWARD        142  'to 165'
        23_0  COME_FROM             6  '6'
          23  POP_TOP          

 229      24  LOAD_FAST             0  'self'
          27  LOAD_ATTR             3  'notify'
          30  LOAD_ATTR             4  'info'
          33  LOAD_CONST            2  'decompressMultifile: Decompressing multifile: '
          36  LOAD_FAST             1  'mfname'
          39  BINARY_ADD       
          40  CALL_FUNCTION_1       1  None
          43  POP_TOP          

 230      44  LOAD_FAST             0  'self'
          47  LOAD_ATTR             6  'mfDetails'
          50  LOAD_FAST             0  'self'
          53  LOAD_ATTR             7  'currentMfname'
          56  BINARY_SUBSCR    
          57  UNPACK_SEQUENCE_3     3  None
          60  STORE_FAST            5  'curVer'
          63  STORE_FAST            2  'expectedSize'
          66  STORE_FAST            3  'expectedMd5'

 231      69  LOAD_GLOBAL          11  'Filename'
          72  LOAD_FAST             0  'self'
          75  LOAD_ATTR            12  'topDir'
          78  LOAD_GLOBAL          11  'Filename'
          81  LOAD_CONST            3  '_%s.%s.%s'
          84  LOAD_FAST             1  'mfname'
          87  LOAD_FAST             5  'curVer'
          90  LOAD_FAST             0  'self'
          93  LOAD_ATTR            13  'CompressionExt'
          96  BUILD_TUPLE_3         3  None
          99  BINARY_MODULO    
         100  CALL_FUNCTION_1       1  None
         103  CALL_FUNCTION_2       2  None
         106  STORE_FAST            4  'localFilename'

 232     109  LOAD_FAST             0  'self'
         112  LOAD_ATTR            15  'decompressMultifile'
         115  LOAD_FAST             1  'mfname'
         118  LOAD_FAST             4  'localFilename'
         121  LOAD_FAST             0  'self'
         124  LOAD_ATTR             2  'decompressMultifileDone'
         127  CALL_FUNCTION_3       3  None
         130  POP_TOP          
         131  JUMP_FORWARD         31  'to 165'
         134  POP_TOP          

 234     135  LOAD_FAST             0  'self'
         138  LOAD_ATTR             3  'notify'
         141  LOAD_ATTR             4  'info'
         144  LOAD_CONST            4  'decompressMultifile: Multifile already decompressed: %s'
         147  LOAD_FAST             1  'mfname'
         150  BINARY_MODULO    
         151  CALL_FUNCTION_1       1  None
         154  POP_TOP          

 235     155  LOAD_FAST             0  'self'
         158  LOAD_ATTR             2  'decompressMultifileDone'
         161  CALL_FUNCTION_0       0  None
         164  POP_TOP          
       165_0  COME_FROM           131  '131'
       165_1  COME_FROM            20  '20'

Parse error at or near `LOAD_FAST' instruction at offset 135

    def decompressMultifile(self, mfname, localFilename, callback):
        self.notify.info('decompressMultifile: request: ' + localFilename.cStr())
        self.launcherMessage(self.Localizer.LauncherDecompressingFile % {'name': self.currentPhaseName, 'current': self.currentPhaseIndex, 'total': self.numPhases})
        task = Task(self.decompressMultifileTask)
        task.mfname = mfname
        task.mfFilename = Filename(self.topDir, Filename('_' + task.mfname))
        task.mfFile = open(task.mfFilename.toOsSpecific(), 'wb')
        task.localFilename = localFilename
        task.callback = callback
        task.lastUpdate = 0
        task.decompressor = bz2.BZ2File(localFilename.toOsSpecific(), 'rb')
        taskMgr.add(task, 'launcher-decompressMultifile')

    def decompressMultifileTask(self, task):
        bufferSize = config.GetInt('launcher-decompress-buffer-size', 8192)
        data = task.decompressor.read(bufferSize)
        if data:
            task.mfFile.write(data)
            now = self.getTime()
            if now - task.lastUpdate >= self.UserUpdateDelay:
                task.lastUpdate = now
                curSize = task.mfFilename.getFileSize()
                curVer, expectedSize, expectedMd5 = self.mfDetails[self.currentMfname]
                progress = curSize / float(expectedSize)
                self.launcherMessage(self.Localizer.LauncherDecompressingPercent % {'name': self.currentPhaseName, 'current': self.currentPhaseIndex, 'total': self.numPhases, 'percent': int(round(progress * 100))})
                percentProgress = int(round(progress * self.decompressPercentage))
                totalPercent = self.downloadPercentage + percentProgress
                self.setPercentPhaseComplete(self.currentPhase, totalPercent)
            self.foregroundSleep()
            return Task.cont
        else:
            task.mfFile.close()
            task.decompressor.close()
            unlinked = task.localFilename.unlink()
            if not unlinked:
                self.notify.warning('unlink failed on file: %s' % task.localFilename.cStr())
            realMf = Filename(self.topDir, Filename(self.currentMfname))
            renamed = task.mfFilename.renameTo(realMf)
            if not renamed:
                self.notify.warning('rename failed on file: %s' % task.mfFilename.cStr())
            self.launcherMessage(self.Localizer.LauncherDecompressingPercent % {'name': self.currentPhaseName, 'current': self.currentPhaseIndex, 'total': self.numPhases, 'percent': 100})
            totalPercent = self.downloadPercentage + self.decompressPercentage
            self.setPercentPhaseComplete(self.currentPhase, totalPercent)
            self.notify.info('decompressMultifileTask: Decompress multifile done: ' + task.localFilename.cStr())
            if self.dldb:
                self.dldb.setClientMultifileDecompressed(task.mfname)
            del task.decompressor
            task.callback()
            del task.callback
            return Task.done

    def decompressMultifileDone(self):
        self.finalizePhase()
        self.notify.info('Done updating multifiles in phase: %s' % self.currentPhase)
        self.progressSoFar += int(round(self.phaseOverallMap[self.currentPhase] * 100))
        self.notify.info('progress so far %s' % self.progressSoFar)
        self.currentPhase += 1
        self.currentPhaseIndex += 1
        self.resumeInstall()

    def finalizePhase(self):
        mfFilename = Filename(self.topDir, Filename(self.currentMfname))
        self.MakeNTFSFilesGlobalWriteable(mfFilename)
        vfs = VirtualFileSystem.getGlobalPtr()
        vfs.mount(mfFilename, '.', VirtualFileSystem.MFReadOnly)
        self.setPercentPhaseComplete(self.currentPhase, 100)
        messenger.send('phaseComplete-%s' % self.currentPhase)

    def getValue(self, key, default=None):
        return os.environ.get(key, default)

    def setValue(self, key, value):
        os.environ[key] = str(value)

    def getVerifyFiles(self):
        return config.GetInt('launcher-verify', 0)

    def getTestServerFlag(self):
        return self.getValue('IS_TEST_SERVER', 0)

    def getGameServer(self):
        return self.getValue('GAME_SERVER', '')

    def getLogFileName(self):
        return 'pirates'

    def getCDDownloadPath(self, origPath, serverFilePath):
        return '%s/%s/CD_%d/%s' % (origPath, self.ServerVersion, self.fromCD, serverFilePath)

    def getDownloadPath(self, origPath, serverFilePath):
        return '%s/%s' % (origPath, serverFilePath)

    def hashIsValid(self, serverHash, hashStr):
        return serverHash.setFromDec(hashStr)

    def getAccountServer(self):
        return

    def getNeedPwForSecretKey(self):
        return 0

    def getParentPasswordSet(self):
        return 0

    def canLeaveFirstIsland(self):
        return self.getPhaseComplete(4)

    def startGame(self):
        eventMgr.restart()
        from pirates.piratesbase import PiratesStart
