from pirates.shipparts.DistributedShippartAI import DistributedShippartAI
from direct.directnotify import DirectNotifyGlobal
from pirates.shipparts.MastDNA import MastDNA
from pirates.destructibles.DistributedDestructibleArrayAI import DistributedDestructibleArrayAI


class DistributedMastDNA(MastDNA):

    def __init__(self):
        MastDNA.__init__(self)

class DistributedMastAI(DistributedShippartAI, DistributedDestructibleArrayAI, DistributedMastDNA):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMastAI')

    def __init__(self, air):
        DistributedShippartAI.__init__(self, air)
        DistributedDestructibleArrayAI.__init__(self, air)
        DistributedMastDNA.__init__(self)

    def d_setBreakAnim(self, index, animMultiplier):
        self.sendUpdate('setBreakAnim', [index, animMultiplier])
