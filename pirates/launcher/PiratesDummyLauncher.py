from otp.launcher.DummyLauncherBase import DummyLauncherBase
from pandac.PandaModules import loadPrcFileData
from pirates.launcher.PiratesQuickLauncher import PiratesQuickLauncher
import os

loadPrcFileData('force-offscreen', 'window-type none')


class PiratesDummyLauncher(DummyLauncherBase, PiratesQuickLauncher):
    __module__ = __name__

    def __init__(self):
        DummyLauncherBase.__init__(self)
        self.setPhaseComplete(1, 100)
        self.setPhaseComplete(2, 100)
        self.firstPhase = 3
        self.startFakeDownload()

    def getPlayToken(self):
        return os.environ.get('POC_TOKEN', None)

    def getGameServer(self):
        return os.environ.get('POC_GAMESERVER', None)
