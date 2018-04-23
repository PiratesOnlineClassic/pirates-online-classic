from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.piratesbase import PiratesGlobals
from direct.distributed.ClockDelta import globalClockDelta

class DistributedDoorBaseAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDoorBaseAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)

        self.doorIndex = 0
        self.buildingUid = ''
        self.locked = 0

    def handleRequestInteraction(self, avatar, interactType, instant):
        return self.ACCEPT

    def handleRequestExit(self, avatar):
        return self.ACCEPT

    def setDoorIndex(self, doorIndex):
        self.doorIndex = doorIndex

    def d_setDoorIndex(self, doorIndex):
        self.sendUpdate('setDoorIndex', [doorIndex])

    def b_setDoorIndex(self, doorIndex):
        self.setDoorIndex(doorIndex)
        self.d_setDoorIndex(doorIndex)

    def getDoorIndex(self):
        return self.doorIndex

    def setBuildingUid(self, buildingUid):
        self.buildingUid = buildingUid

    def d_setBuildingUid(self, buildingUid):
        self.sendUpdate('setBuildingUid', [buildingUid])

    def b_setBuildingUid(self, buildingUid):
        self.setBuildingUid(buildingUid)
        self.d_setBuildingUid(buildingUid)

    def getBuildingUid(self):
        return self.buildingUid

    def d_setMovie(self, mode, avId, timestamp):
        self.sendUpdate('setMovie', [mode, avId, timestamp])

    def setLocked(self, locked):
        self.locked = locked

    def d_setLocked(self, locked):
        self.sendUpdate('setLocked', [locked])

    def b_setLocked(self, locked):
        self.setLocked(locked)
        self.d_setLocked(locked)

    def getLocked(self):
        return self.locked
