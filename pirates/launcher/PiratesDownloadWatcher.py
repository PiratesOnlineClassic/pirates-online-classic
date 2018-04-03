# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.launcher.PiratesDownloadWatcher
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectLabel import DirectLabel
from direct.gui.DirectWaitBar import DirectWaitBar
from otp.launcher import DownloadWatcher
from pandac.PandaModules import Point3, TextNode


class PiratesDownloadWatcher(DownloadWatcher.DownloadWatcher):
    __module__ = __name__
    positions = [(Point3(1.18333, 0, -0.97333), Point3(1.02333, 0, -0.9867)), (Point3(-0.549997, 0, 0.969997), Point3(-0.71333, 0, 0.95333)), (Point3(-0.636666, 0, 0.686667), Point3(-0.793333, 0, 0.67))]

    def __init__(self, phaseNames):
        self.phaseNames = phaseNames
        self.text = DirectLabel(relief=None, guiId='DownloadWatcherText', pos=(-0.1, 0, -0.98), text='                     ', text_fg=(1,
                                                                                                                                       1,
                                                                                                                                       1,
                                                                                                                                       1), text_scale=0.05, textMayChange=1, text_align=TextNode.ARight, sortOrder=5000)
        self.bar = DirectWaitBar(guiId='DownloadWatcherBar', pos=(0.55, 0, -0.96), relief=DGG.SUNKEN, frameSize=(-0.6, 0.6, -0.1, 0.1), borderWidth=(0.02,
                                                                                                                                                     0.02), scale=0.25, range=100, frameColor=(0.5,
                                                                                                                                                                                               0.5,
                                                                                                                                                                                               0.5,
                                                                                                                                                                                               0.5), barColor=(0.2,
                                                                                                                                                                                                               0.7,
                                                                                                                                                                                                               0.2,
                                                                                                                                                                                                               0.5), text='0%', text_scale=0.16, text_fg=(1,
                                                                                                                                                                                                                                                          1,
                                                                                                                                                                                                                                                          1,
                                                                                                                                                                                                                                                          1), text_align=TextNode.ACenter, text_pos=(0, -0.05), sortOrder=5000)
        self.accept('launcherPercentPhaseComplete', self.update)
        self.setStatusBarLocation(0)
        return

    def setStatusBarLocation(self, positionIndex):
        self.bar.setPos(self.positions[positionIndex][0])
        self.text.setPos(self.positions[positionIndex][1])

    def foreground(self):
        self.bar.reparentTo(aspect2dp, 5000)
        self.text.reparentTo(aspect2dp, 5000)

    def background(self):
        self.bar.reparentTo(aspect2d, 0)
        self.text.reparentTo(aspect2d, 0)
# okay decompiling .\pirates\launcher\PiratesDownloadWatcher.pyc
