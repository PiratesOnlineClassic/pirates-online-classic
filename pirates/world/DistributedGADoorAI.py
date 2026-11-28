from direct.directnotify import DirectNotifyGlobal

from pirates.world.DistributedGAConnectorAI import DistributedGAConnectorAI


class DistributedGADoorAI(DistributedGAConnectorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGADoorAI')

    def __init__(self, air):
        DistributedGAConnectorAI.__init__(self, air)
