
from pirates.battle.DistributedShipCannonAI import DistributedShipCannonAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTutorialShipCannonAI(DistributedShipCannonAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTutorialShipCannonAI')

    def __init__(self, air):
        DistributedShipCannonAI.__init__(self, air)



