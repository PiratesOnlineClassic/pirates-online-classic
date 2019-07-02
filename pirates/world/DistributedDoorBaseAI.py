from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm.FSM import FSM

from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.piratesbase import PiratesGlobals
from pirates.quest.QuestConstants import LocationIds
from pirates.piratesbase import Freebooter


class DistributedDoorBaseAI(DistributedInteractiveAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDoorBaseAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        FSM.__init__(self, self.__class__.__name__)

        self.doorIndex = 0
        self.buildingUid = ''
        self.locked = 0

        self.doorState = PiratesGlobals.DOOR_CLOSED
        self.avatarId = 0

        self.doorTask = None
        self.otherDoor = None

    def handleRequestInteraction(self, avatar, interactType, instant):
        if self.locked:
            return self.DENY

        if self.buildingUid == LocationIds.KINGSHEAD_DOOR and not Freebooter.getPaidStatusAI(avatar.doId):
            self.notify.warning('Freebooter (%s) attempted to force open KINGSHEAD_DOOR' % avatar.doId)
            return self.DENY

        if not self.avatarId:
            self.request('Opened', avatar.doId)

        avatarParentObj = avatar.getParentObj()
        if not avatarParentObj:
            self.notify.warning('Cannot handle interaction for avatar %d, '
                'doesn\'t have an valid parent object!' % (avatar.doId))

            return self.DENY

        if self.getParentObj().doId == avatarParentObj.doId:
            self.otherDoor.handleRequestInteraction(avatar, interactType, instant)

        return self.ACCEPT

    def handleRequestExit(self, avatar):
        if self.locked:
            return self.DENY

        return self.ACCEPT

    def setDoorState(self, doorState, avatarId):
        self.doorState = doorState
        self.avatarId = avatarId

    def d_setDoorState(self, doorState, avatarId):
        self.d_setMovie(doorState, avatarId, globalClockDelta.getFrameNetworkTime(bits=16))

    def b_setDoorState(self, doorState, avatarId):
        self.setDoorState(doorState, avatarId)
        self.d_setDoorState(doorState, avatarId)

    def getDoorState(self):
        return self.doorState

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def __open(self, avatarId, task):
        self.request('Opened', avatarId)
        return task.done

    def enterOpened(self, avatarId):
        self.b_setDoorState(PiratesGlobals.DOOR_OPEN, avatarId)
        self.doorTask = taskMgr.doMethodLater(2.0, self.__close, self.uniqueName('door-opened'))

    def exitOpened(self):
        if self.doorTask:
            taskMgr.remove(self.doorTask)
            self.doorTask = None

    def __close(self, task):
        self.request('Closed')
        return task.done

    def enterClosed(self):
        self.b_setDoorState(PiratesGlobals.DOOR_CLOSED, 0)

    def exitClosed(self):
        if self.doorTask:
            taskMgr.remove(self.doorTask)
            self.doorTask = None

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

    def setOtherDoor(self, otherDoor):
        self.otherDoor = otherDoor

    def getOtherDoor(self):
        return self.otherDoor

    def delete(self):
        if self.doorTask:
            taskMgr.remove(self.doorTask)
            self.doorTask = None

        DistributedInteractiveAI.delete(self)
