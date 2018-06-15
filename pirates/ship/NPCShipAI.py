from pirates.ship.DistributedShipAI import DistributedShipAI
from direct.directnotify import DirectNotifyGlobal

class NPCShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NPCShipAI')

    def __init__(self, air):
        DistributedShipAI.__init__(self, air)
