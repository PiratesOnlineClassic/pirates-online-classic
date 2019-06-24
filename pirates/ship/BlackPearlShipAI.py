from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI


class BlackPearlShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('BlackPearlShipAI')
