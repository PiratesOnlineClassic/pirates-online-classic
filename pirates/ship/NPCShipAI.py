from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI


class NPCShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('NPCShipAI')
