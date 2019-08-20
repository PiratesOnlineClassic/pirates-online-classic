from pirates.shipparts.DistributedShippartAI import DistributedShippartAI
from direct.directnotify import DirectNotifyGlobal
from pirates.shipparts.HullDNA import HullDNA
from pirates.destructibles.DistributedDestructibleArrayAI import DistributedDestructibleArrayAI


class DistributedHullDNA(HullDNA):

    def __init__(self):
        HullDNA.__init__(self)

class DistributedHullAI(DistributedShippartAI, DistributedDestructibleArrayAI, DistributedHullDNA):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHullAI')

    def __init__(self, air):
        DistributedShippartAI.__init__(self, air)
        DistributedDestructibleArrayAI.__init__(self, air)
        DistributedHullDNA.__init__(self)

        self.maxSp = 0
        self.sp = 0
        self.maxCargo = 0

    def setMaxSp(self, maxSp):
        self.maxSp = maxSp

    def d_setMaxSp(self, maxSp):
        self.sendUpdate('setMaxSp', [maxSp])

    def b_setMaxSp(self, maxSp):
        self.setMaxSp(maxSp)
        self.d_setMaxSp(maxSp)

    def getMaxSp(self):
        return self.maxSp

    def setSp(self, sp):
        self.sp = sp

    def d_setSp(self, sp):
        self.sendUpdate('setSp', [sp])

    def b_setSp(self, sp):
        self.setSp(sp)
        self.d_setSp(sp)

    def getSp(self):
        return self.sp

    def setMaxCargo(self, maxCargo):
        self.maxCargo = maxCargo

    def d_setMaxCargo(self, maxCargo):
        self.sendUpdate('setMaxCargo', [maxCargo])

    def b_setMaxCargo(self, maxCargo):
        self.setMaxCargo(maxCargo)
        self.d_setMaxCargo(maxCargo)

    def getMaxCargo(self):
        return self.maxCargo
