from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI


class TutorialShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TutorialShipAI')
