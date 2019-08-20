from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.shipparts.CabinDNA import CabinDNA
from pirates.shipparts.DistributedShippartAI import DistributedShippartAI
from pirates.destructibles.DistributedDestructibleArrayAI import DistributedDestructibleArrayAI


class DistributedCabinDNA(CabinDNA):

    def __init__(self):
        CabinDNA.__init__(self)

class DistributedCabinAI(DistributedShippartAI, DistributedDestructibleArrayAI, DistributedCabinDNA):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCabinAI')

    def __init__(self, air):
        DistributedShippartAI.__init__(self, air)
        DistributedDestructibleArrayAI.__init__(self, air)
        DistributedCabinDNA.__init__(self)

        self.maxHp = 0
        self.hp = 0
        self.maxCargo = 0

    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def d_setMaxHp(self, maxHp):
        self.sendUpdate('setMaxHp', [maxHp])

    def b_setMaxHp(self, maxHp):
        self.setMaxHp(maxHp)
        self.d_setMaxHp(maxHp)

    def getMaxHp(self):
        return self.maxHp

    def setHp(self, hp):
        self.hp = hp

    def d_setHp(self, hp):
        self.sendUpdate('setHp', [hp])

    def b_setHp(self, hp):
        self.setHp(hp)
        self.d_setHp(hp)

    def getHp(self):
        return self.hp

    def setMaxCargo(self, maxCargo):
        self.maxCargo = maxCargo

    def d_setMaxCargo(self, maxCargo):
        self.sendUpdate('setMaxCargo', [maxCargo])

    def b_setMaxCargo(self, maxCargo):
        self.setMaxCargo(maxCargo)
        self.d_setMaxCargo(maxCargo)

    def getMaxCargo(self):
        return self.maxCargo
