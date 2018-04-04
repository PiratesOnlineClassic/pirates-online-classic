
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedSurfaceTreasureAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSurfaceTreasureAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.withdrawType = 0


    # setWithdrawType(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setWithdrawType(self, withdrawType):
        self.withdrawType = withdrawType

    def d_setWithdrawType(self, withdrawType):
        self.sendUpdate('setWithdrawType', [withdrawType])

    def b_setWithdrawType(self, withdrawType):
        self.setWithdrawType(withdrawType)
        self.d_setWithdrawType(withdrawType)

    def getWithdrawType(self):
        return self.withdrawType

    # setOpen(uint8(0-1)) broadcast ram

    def setOpen(self, open):
        self.sendUpdate('setOpen', [open])

    # startLooting(uint8)

    def startLooting(self, startLooting):
        self.sendUpdate('startLooting', [startLooting])

    # stopLooting()

    def stopLooting(self, stopLooting):
        self.sendUpdate('stopLooting', [stopLooting])

    # setBelongsToTeam(int16) broadcast ram

    def setBelongsToTeam(self, belongsToTeam):
        self.sendUpdate('setBelongsToTeam', [belongsToTeam])

    # setValue(int16) broadcast ram

    def setValue(self, value):
        self.sendUpdate('setValue', [value])

    # setEmpty(uint8(0-1)) broadcast ram

    def setEmpty(self, empty):
        self.sendUpdate('setEmpty', [empty])


