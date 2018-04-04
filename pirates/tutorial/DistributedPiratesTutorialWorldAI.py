
from pirates.instance.DistributedInstanceWorldAI import DistributedInstanceWorldAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPiratesTutorialWorldAI(DistributedInstanceWorldAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPiratesTutorialWorldAI')

    def __init__(self, air):
        DistributedInstanceWorldAI.__init__(self, air)


    # setTutorialHandlerId(uint32) broadcast ram

    def setTutorialHandlerId(self, tutorialHandlerId):
        self.sendUpdate('setTutorialHandlerId', [tutorialHandlerId])


