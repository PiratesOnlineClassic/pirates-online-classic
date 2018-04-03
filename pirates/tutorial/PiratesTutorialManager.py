# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.tutorial.PiratesTutorialManager
from direct.distributed import DistributedObject


class PiratesTutorialManager(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = directNotify.newCategory('PiratesTutorialManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.accept('requestTutorial', self.d_requestTutorial)

    def disable(self):
        self.ignoreAll()
        DistributedObject.DistributedObject.disable(self)

    def d_requestTutorial(self):
        self.sendUpdate('requestTutorial', [])

    def enterTutorial(self, tutorialZone):
        base.localAvatar.inTutorial = 1
        messenger.send('startTutorial', [self.doId, tutorialZone])
        self.acceptOnce('stopTutorial', self.__handleStopTutorial)

    def __handleStopTutorial(self):
        base.localAvatar.inTutorial = 2
        self.d_allDone()

    def d_allDone(self):
        self.sendUpdate('allDone', [])

    def d_toonArrived(self):
        self.sendUpdate('toonArrived', [])
# okay decompiling .\pirates\tutorial\PiratesTutorialManager.pyc
