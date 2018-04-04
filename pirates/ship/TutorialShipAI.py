
from pirates.ship.DistributedShipAI import DistributedShipAI
from direct.directnotify import DirectNotifyGlobal

class TutorialShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TutorialShipAI')

    def __init__(self, air):
        DistributedShipAI.__init__(self, air)



