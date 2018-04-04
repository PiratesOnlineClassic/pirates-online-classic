
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class TradeAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TradeAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.firstAvatarId = 0
        self.firstAvatarStatus = 0
        self.firstAvatarGiving = []
        self.secondAvatarId = 0
        self.secondAvatarStatus = 0
        self.secondAvatarGiving = []


    # tradeCompleted()

    def tradeCompleted(self, tradeCompleted):
        self.sendUpdate('tradeCompleted', [tradeCompleted])

    # tradeCanceled()

    def tradeCanceled(self, tradeCanceled):
        self.sendUpdate('tradeCanceled', [tradeCanceled])

    # tradeFailed()

    def tradeFailed(self, tradeFailed):
        self.sendUpdate('tradeFailed', [tradeFailed])

    # requestChangeGiving(TradeSlot []) airecv clsend

    def requestChangeGiving(self, requestChangeGiving):
        pass

    # rejectChangeGiving(uint32)

    def rejectChangeGiving(self, rejectChangeGiving):
        self.sendUpdate('rejectChangeGiving', [rejectChangeGiving])

    # requestChangeStatus(uint8) airecv clsend

    def requestChangeStatus(self, requestChangeStatus):
        pass

    # rejectChangeStatus(uint32)

    def rejectChangeStatus(self, rejectChangeStatus):
        self.sendUpdate('rejectChangeStatus', [rejectChangeStatus])

    # requestRemoveTrade() airecv clsend

    def requestRemoveTrade(self, requestRemoveTrade):
        pass

    # rejectRemoveTrade(uint32)

    def rejectRemoveTrade(self, rejectRemoveTrade):
        self.sendUpdate('rejectRemoveTrade', [rejectRemoveTrade])

    # setFirstAvatarId(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setFirstAvatarId(self, firstAvatarId):
        self.firstAvatarId = firstAvatarId

    def d_setFirstAvatarId(self, firstAvatarId):
        self.sendUpdate('setFirstAvatarId', [firstAvatarId])

    def b_setFirstAvatarId(self, firstAvatarId):
        self.setFirstAvatarId(firstAvatarId)
        self.d_setFirstAvatarId(firstAvatarId)

    def getFirstAvatarId(self):
        return self.firstAvatarId

    # setFirstAvatarStatus(uint16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setFirstAvatarStatus(self, firstAvatarStatus):
        self.firstAvatarStatus = firstAvatarStatus

    def d_setFirstAvatarStatus(self, firstAvatarStatus):
        self.sendUpdate('setFirstAvatarStatus', [firstAvatarStatus])

    def b_setFirstAvatarStatus(self, firstAvatarStatus):
        self.setFirstAvatarStatus(firstAvatarStatus)
        self.d_setFirstAvatarStatus(firstAvatarStatus)

    def getFirstAvatarStatus(self):
        return self.firstAvatarStatus

    # setFirstAvatarGiving(TradeSlot []) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setFirstAvatarGiving(self, firstAvatarGiving):
        self.firstAvatarGiving = firstAvatarGiving

    def d_setFirstAvatarGiving(self, firstAvatarGiving):
        self.sendUpdate('setFirstAvatarGiving', [firstAvatarGiving])

    def b_setFirstAvatarGiving(self, firstAvatarGiving):
        self.setFirstAvatarGiving(firstAvatarGiving)
        self.d_setFirstAvatarGiving(firstAvatarGiving)

    def getFirstAvatarGiving(self):
        return self.firstAvatarGiving

    # setSecondAvatarId(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setSecondAvatarId(self, secondAvatarId):
        self.secondAvatarId = secondAvatarId

    def d_setSecondAvatarId(self, secondAvatarId):
        self.sendUpdate('setSecondAvatarId', [secondAvatarId])

    def b_setSecondAvatarId(self, secondAvatarId):
        self.setSecondAvatarId(secondAvatarId)
        self.d_setSecondAvatarId(secondAvatarId)

    def getSecondAvatarId(self):
        return self.secondAvatarId

    # setSecondAvatarStatus(uint16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setSecondAvatarStatus(self, secondAvatarStatus):
        self.secondAvatarStatus = secondAvatarStatus

    def d_setSecondAvatarStatus(self, secondAvatarStatus):
        self.sendUpdate('setSecondAvatarStatus', [secondAvatarStatus])

    def b_setSecondAvatarStatus(self, secondAvatarStatus):
        self.setSecondAvatarStatus(secondAvatarStatus)
        self.d_setSecondAvatarStatus(secondAvatarStatus)

    def getSecondAvatarStatus(self):
        return self.secondAvatarStatus

    # setSecondAvatarGiving(TradeSlot []) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setSecondAvatarGiving(self, secondAvatarGiving):
        self.secondAvatarGiving = secondAvatarGiving

    def d_setSecondAvatarGiving(self, secondAvatarGiving):
        self.sendUpdate('setSecondAvatarGiving', [secondAvatarGiving])

    def b_setSecondAvatarGiving(self, secondAvatarGiving):
        self.setSecondAvatarGiving(secondAvatarGiving)
        self.d_setSecondAvatarGiving(secondAvatarGiving)

    def getSecondAvatarGiving(self):
        return self.secondAvatarGiving


