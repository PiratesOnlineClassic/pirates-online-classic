
from pirates.world.DistributedDoorBaseAI import DistributedDoorBaseAI
from direct.directnotify import DirectNotifyGlobal

class DistributedInteriorDoorAI(DistributedDoorBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteriorDoorAI')

    def __init__(self, air):
        DistributedDoorBaseAI.__init__(self, air)
        self.interiorId = [0, 0, 0]
        self.exteriorId = [0, 0, 0]
        self.buildingDoorId = 0


    # setInteriorId(uint32, uint32, uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setInteriorId(self, interiorId, todo_uint32_1, todo_uint32_2):
        self.interiorId = interiorId

    def d_setInteriorId(self, interiorId, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('setInteriorId', [interiorId, todo_uint32_1, todo_uint32_2])

    def b_setInteriorId(self, interiorId, todo_uint32_1, todo_uint32_2):
        self.setInteriorId(interiorId, todo_uint32_1, todo_uint32_2)
        self.d_setInteriorId(interiorId, todo_uint32_1, todo_uint32_2)

    def getInteriorId(self):
        return self.interiorId

    # setExteriorId(uint32, uint32, uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setExteriorId(self, exteriorId, todo_uint32_1, todo_uint32_2):
        self.exteriorId = exteriorId

    def d_setExteriorId(self, exteriorId, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('setExteriorId', [exteriorId, todo_uint32_1, todo_uint32_2])

    def b_setExteriorId(self, exteriorId, todo_uint32_1, todo_uint32_2):
        self.setExteriorId(exteriorId, todo_uint32_1, todo_uint32_2)
        self.d_setExteriorId(exteriorId, todo_uint32_1, todo_uint32_2)

    def getExteriorId(self):
        return self.exteriorId

    # setBuildingDoorId(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setBuildingDoorId(self, buildingDoorId):
        self.buildingDoorId = buildingDoorId

    def d_setBuildingDoorId(self, buildingDoorId):
        self.sendUpdate('setBuildingDoorId', [buildingDoorId])

    def b_setBuildingDoorId(self, buildingDoorId):
        self.setBuildingDoorId(buildingDoorId)
        self.d_setBuildingDoorId(buildingDoorId)

    def getBuildingDoorId(self):
        return self.buildingDoorId


