from direct.directnotify import DirectNotifyGlobal

from pirates.world.DistributedGAConnectorAI import DistributedGAConnectorAI


class DistributedGADoorAI(DistributedGAConnectorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGADoorAI')
