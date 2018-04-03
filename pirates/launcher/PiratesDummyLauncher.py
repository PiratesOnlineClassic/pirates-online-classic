# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.launcher.PiratesDummyLauncher
from otp.launcher.DummyLauncherBase import DummyLauncherBase
from pirates.launcher.PiratesQuickLauncher import PiratesQuickLauncher
from pandac.PandaModules import loadPrcFileData
loadPrcFileData('force-offscreen', 'window-type none')

class PiratesDummyLauncher(DummyLauncherBase, PiratesQuickLauncher):
    __module__ = __name__

    def __init__(self):
        DummyLauncherBase.__init__(self)
        self.setPhaseComplete(1, 100)
        self.setPhaseComplete(2, 100)
        self.firstPhase = 3
        self.startFakeDownload()
# okay decompiling .\pirates\launcher\PiratesDummyLauncher.pyc
