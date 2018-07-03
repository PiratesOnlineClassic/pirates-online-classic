from pirates.shipparts.DistributedShippartAI import DistributedShippartAI
from direct.directnotify import DirectNotifyGlobal
from pirates.shipparts.DecorDNA import DecorDNA
from pirates.destructibles.DistributedDestructibleArrayAI import DistributedDestructibleArrayAI


class DistributedDecorDNA(DecorDNA):

    def __init__(self):
        DecorDNA.__init__(self)

class DistributedShipDecorAI(DistributedShippartAI, DistributedDestructibleArrayAI, DistributedDecorDNA):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipDecorAI')

    def __init__(self, air):
        DistributedShippartAI.__init__(self, air)
        DistributedDestructibleArrayAI.__init__(self, air)
        DistributedDecorDNA.__init__(self)

        self.maxHp = 0
        self.hp = 0

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
