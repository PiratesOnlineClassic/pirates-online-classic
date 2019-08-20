from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from pirates.world.DistributedDoorBaseAI import DistributedDoorBaseAI
from pirates.piratesbase import PiratesGlobals


class DistributedInteriorDoorAI(DistributedDoorBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteriorDoorAI')

    def __init__(self, air):
        DistributedDoorBaseAI.__init__(self, air)

        self.interiorDoId = 0
        self.interiorParentId = 0
        self.interiorZoneId = 0

        self.exteriorDoId = 0
        self.exteriorWorldParentId = 0
        self.exteriorWorldZoneId = 0

        self.buildingDoorId = 0

    def handleRequestInteraction(self, avatar, interactType, instant):
        result = DistributedDoorBaseAI.handleRequestInteraction(self, avatar, interactType, instant)
        if not result:
            return self.DENY

        exterior = self.air.doId2do.get(self.exteriorDoId)
        if not exterior:
            self.notify.warning('Cannot handle avatar %d interact for door %d, '
                'exterior %d not found!' % (avatar.doId, self.doId, self.exteriorDoId))

            return self.DENY

        if not self.otherDoor:
            self.notify.warning('Cannot handle avatar %d interact for door %d, '
                'exterior door not found!' % (avatar.doId, self.doId))

            return self.DENY

        return self.ACCEPT

    def setInteriorId(self, interiorDoId, interiorParentId, interiorZoneId):
        self.interiorDoId = interiorDoId
        self.interiorParentId = interiorParentId
        self.interiorZoneId = interiorZoneId

    def d_setInteriorId(self, interiorDoId, interiorParentId, interiorZoneId):
        self.sendUpdate('setInteriorId', [interiorDoId, interiorParentId, interiorZoneId])

    def b_setInteriorId(self, interiorDoId, interiorParentId, interiorZoneId):
        self.setInteriorId(interiorDoId, interiorParentId, interiorZoneId)
        self.d_setInteriorId(interiorDoId, interiorParentId, interiorZoneId)

    def getInteriorId(self):
        return [self.interiorDoId, self.interiorParentId, self.interiorZoneId]

    def setExteriorId(self, exteriorDoId, exteriorWorldParentId, exteriorWorldZoneId):
        self.exteriorDoId = exteriorDoId
        self.exteriorWorldParentId = exteriorWorldParentId
        self.exteriorWorldZoneId = exteriorWorldZoneId

    def d_setExteriorId(self, exteriorDoId, exteriorWorldParentId, exteriorWorldZoneId):
        self.sendUpdate('setExteriorId', [exteriorDoId, exteriorWorldParentId, exteriorWorldZoneId])

    def b_setExteriorId(self, exteriorDoId, exteriorWorldParentId, exteriorWorldZoneId):
        self.setExteriorId(exteriorDoId, exteriorWorldParentId, exteriorWorldZoneId)
        self.d_setExteriorId(exteriorDoId, exteriorWorldParentId, exteriorWorldZoneId)

    def getExteriorId(self):
        return [self.exteriorDoId, self.exteriorWorldParentId, self.exteriorWorldZoneId]

    def setBuildingDoorId(self, buildingDoorId):
        self.buildingDoorId = buildingDoorId

    def d_setBuildingDoorId(self, buildingDoorId):
        self.sendUpdate('setBuildingDoorId', [buildingDoorId])

    def b_setBuildingDoorId(self, buildingDoorId):
        self.setBuildingDoorId(buildingDoorId)
        self.d_setBuildingDoorId(buildingDoorId)

    def getBuildingDoorId(self):
        return self.buildingDoorId
