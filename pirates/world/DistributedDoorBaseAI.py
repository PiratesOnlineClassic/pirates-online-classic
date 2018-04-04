
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedDoorBaseAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDoorBaseAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.doorIndex = 0
        self.buildingUid = ''
        self.locked = 0


    # setDoorIndex(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setDoorIndex(self, doorIndex):
        self.doorIndex = doorIndex

    def d_setDoorIndex(self, doorIndex):
        self.sendUpdate('setDoorIndex', [doorIndex])

    def b_setDoorIndex(self, doorIndex):
        self.setDoorIndex(doorIndex)
        self.d_setDoorIndex(doorIndex)

    def getDoorIndex(self):
        return self.doorIndex

    # setBuildingUid(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setBuildingUid(self, buildingUid):
        self.buildingUid = buildingUid

    def d_setBuildingUid(self, buildingUid):
        self.sendUpdate('setBuildingUid', [buildingUid])

    def b_setBuildingUid(self, buildingUid):
        self.setBuildingUid(buildingUid)
        self.d_setBuildingUid(buildingUid)

    def getBuildingUid(self):
        return self.buildingUid

    # setMovie(uint8, uint32, int16) broadcast

    def setMovie(self, movie, todo_uint32_1, todo_int16_2):
        self.sendUpdate('setMovie', [movie, todo_uint32_1, todo_int16_2])

    # setLocked(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setLocked(self, locked):
        self.locked = locked

    def d_setLocked(self, locked):
        self.sendUpdate('setLocked', [locked])

    def b_setLocked(self, locked):
        self.setLocked(locked)
        self.d_setLocked(locked)

    def getLocked(self):
        return self.locked


