
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PiratesTutorialManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesTutorialManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # requestTutorial() airecv clsend

    def requestTutorial(self, requestTutorial):
        pass

    # enterTutorial(uint32)

    def enterTutorial(self, enterTutorial):
        self.sendUpdate('enterTutorial', [enterTutorial])

    # allDone() airecv clsend

    def allDone(self, allDone):
        pass


