from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.shipparts.BowSpritDNA import BowSpritDNA
from pirates.shipparts.DistributedShippartAI import DistributedShippartAI
from pirates.destructibles.DistributedDestructibleObjectAI import DistributedDestructibleObjectAI


class DistributedBowSpritDNA(BowSpritDNA):

    def __init__(self):
        BowSpritDNA.__init__(self)

class DistributedBowSpritAI(DistributedShippartAI, DistributedDestructibleObjectAI, DistributedBowSpritDNA):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBowSpritAI')

    def __init__(self, air):
        DistributedShippartAI.__init__(self, air)
        DistributedDestructibleObjectAI.__init__(self, air)
        DistributedBowSpritDNA.__init__(self)

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
