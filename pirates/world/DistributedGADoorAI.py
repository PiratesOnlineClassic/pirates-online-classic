
from pirates.world.DistributedGAConnectorAI import DistributedGAConnectorAI
from direct.directnotify import DirectNotifyGlobal

class DistributedGADoorAI(DistributedGAConnectorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGADoorAI')

    def __init__(self, air):
        DistributedGAConnectorAI.__init__(self, air)



