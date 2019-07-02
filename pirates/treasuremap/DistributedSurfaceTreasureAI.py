from direct.directnotify import DirectNotifyGlobal

from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.piratesbase import PiratesGlobals

class DistributedSurfaceTreasureAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSurfaceTreasureAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.withdrawType = 0
        self.opened = False
        self.belongToTeam = PiratesGlobals.INVALID_TEAM
        self.value = 0

    def setWithdrawType(self, withdrawType):
        self.widthdrawType = withdrawType

    def d_setWithdrawType(self, withdrawType):
        self.sendUpdate('setWithdrawType', [withdrawpType])

    def b_setWithdrawType(self, withdrawType):
        self.setWithdrawType(withdrawType)
        self.d_setWithdrawType(withdrawType)

    def getWithdrawType(self):
        return self.withdrawType