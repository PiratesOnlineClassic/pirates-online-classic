
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPiratesTutorialAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPiratesTutorialAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # clientEnterAct0Tutorial() airecv clsend

    def clientEnterAct0Tutorial(self, clientEnterAct0Tutorial):
        pass

    # tutorialSeachestFinished() airecv clsend

    def tutorialSeachestFinished(self, tutorialSeachestFinished):
        pass

    # startSailingStumpy() airecv clsend

    def startSailingStumpy(self, startSailingStumpy):
        pass

    # boardedTutorialShip() airecv clsend

    def boardedTutorialShip(self, boardedTutorialShip):
        pass

    # targetPracticeDone() airecv clsend

    def targetPracticeDone(self, targetPracticeDone):
        pass

    # giveInitQuest(uint8) airecv clsend

    def giveInitQuest(self, giveInitQuest):
        pass

    # inventoryFailed() broadcast ram

    def inventoryFailed(self, inventoryFailed):
        self.sendUpdate('inventoryFailed', [inventoryFailed])

    # autoVisit(uint32) airecv clsend

    def autoVisit(self, autoVisit):
        pass

    # makeAPirateComplete() airecv clsend

    def makeAPirateComplete(self, makeAPirateComplete):
        pass

    # makeAPirateCompleteResp() broadcast ram

    def makeAPirateCompleteResp(self, makeAPirateCompleteResp):
        self.sendUpdate('makeAPirateCompleteResp', [makeAPirateCompleteResp])


