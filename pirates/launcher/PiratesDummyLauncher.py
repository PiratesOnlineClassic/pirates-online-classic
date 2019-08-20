from otp.launcher.DummyLauncherBase import DummyLauncherBase
from pirates.launcher.PiratesQuickLauncher import PiratesQuickLauncher
from pandac.PandaModules import loadPrcFileData
import os

loadPrcFileData('force-offscreen', 'window-type none')

class PiratesDummyLauncher(DummyLauncherBase, PiratesQuickLauncher):
    
    def __init__(self):
        DummyLauncherBase.__init__(self)
        self.setPhaseComplete(1, 100)
        self.setPhaseComplete(2, 100)
        self.firstPhase = 3
        self.startFakeDownload()

    def getPlayToken(self):
        return os.environ.get('POC_TOKEN', None)

    def isTestServer(self):
        return self.getValue('IS_TEST_SERVER', 0)

    def getGameServer(self):
        return os.environ.get('POC_GAMESERVER', None)

