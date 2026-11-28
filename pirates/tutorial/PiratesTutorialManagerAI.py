import traceback

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.task import Task

from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals
from pirates.tutorial import TutorialGlobals
from pirates.tutorial.DistributedPiratesTutorialAI import DistributedPiratesTutorialAI

# Region UID for the tutorial world (RambleshackWorld)
RAMBLESHACK_REGION_UID = '1115838788a.58jubutler'


class TutorialFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('TutorialFSM')
    START_TIMEOUT_SECONDS = 60.0

    def __init__(self, air, avatar):
        FSM.__init__(self, 'TutorialFSM')

        self.air = air
        self.avatar = avatar

        self.island = None
        self.instance = None
        self.interior = None
        self.exteriorDoor = None
        self.tutorialHandler = None
        self.tutorialHandlerZoneId = None
        self._pendingUidCallbacks = {}
        self._finished = False
        self._handlerPublished = False
        self._teleportFSM = None
        self._lockedDoors = set()
        self._timeoutTaskName = 'tutorial-start-%d-%d' % (avatar.doId, id(self))

    def _waitForUid(self, uid, callback):
        def arrived(doId):
            self._pendingUidCallbacks.pop(uid, None)
            try:
                self._runCallback(callback, doId)
            except Exception:
                # UniqueIdManager removes one-shot callbacks after they return.
                self.notify.warning('Tutorial UID callback failed for avatar %d:\n%s' %
                    (self.avatar.doId, traceback.format_exc()))

        self._pendingUidCallbacks[uid] = arrived
        self.air.uidMgr.addUidCallback(uid, arrived)

    def _runCallback(self, callback, *args):
        if self._finished:
            return
        try:
            callback(*args)
        except Exception:
            try:
                self._fail('Tutorial startup failed')
            finally:
                raise

    def enterStart(self):
        self.acceptOnce(self.avatar.getDeleteEvent(), self.cleanup)
        taskMgr.doMethodLater(self.START_TIMEOUT_SECONDS, self._startTimedOut,
            self._timeoutTaskName)
        self.notify.info('Starting tutorial for avatar: %s' % self.avatar.doId)

        self._waitForUid(RAMBLESHACK_REGION_UID, self.__instanceArrived)
        if not self.air.tutorialManager._worldLoaded and not self._finished:
            self.air.tutorialManager._loadWorld()

    def exitStart(self):
        pass

    def _startTimedOut(self, task):
        if not self._finished:
            self._fail('Tutorial startup timed out')
        return Task.done

    def _fail(self, reason):
        if self._finished:
            return
        try:
            self.air.tutorialManager._notifyFailure(self.avatar, reason)
        finally:
            self.cleanup()

    def __instanceArrived(self, instanceDoId):
        self.instance = self.air.doId2do.get(instanceDoId)
        if not self.instance:
            self.notify.warning('Failed to create tutorial world for avatar %d!' % self.avatar.doId)
            self._fail('Tutorial world unavailable')
            return

        self.notify.info('Tutorial world created for avatar %d: %s' % (self.avatar.doId, self.instance))

        # Now wait for the island
        self._waitForUid(TutorialGlobals.RAMBLESHACK_ISLE_UID, self.__islandArrived)

    def __islandArrived(self, islandDoId):
        self.island = self.air.doId2do.get(islandDoId)
        if not self.island:
            self.notify.warning('Failed to create tutorial island for avatar %d!' % self.avatar.doId)
            self._fail('Tutorial island unavailable')
            return

        self.notify.info('Tutorial island created for avatar %d: %s' % (self.avatar.doId, self.island))

        # Now wait for the interior
        self._waitForUid(TutorialGlobals.JAIL_INTERIOR, self.__interiorArrived)

    def __interiorArrived(self, interiorDoId):
        self.interior = self.air.doId2do.get(interiorDoId)
        if not self.interior:
            self.notify.warning('Failed to create tutorial interior for avatar %d!' % self.avatar.doId)
            self._fail('Tutorial interior unavailable')
            return

        self.notify.info('Tutorial interior created for avatar %d: %s' % (self.avatar.doId, self.interior))

        tutorialHandlerDoId = self.air.allocateChannel()
        self.acceptOnce('generate-%d' % tutorialHandlerDoId,
            self._runCallback, [self.__handlerArrived])

        self.tutorialHandlerZoneId = self.air.allocateZone()

        self.tutorialHandler = DistributedPiratesTutorialAI(self.air)
        self.tutorialHandler.setAvatarId(self.avatar.doId)
        self.tutorialHandler.generateWithRequiredAndId(tutorialHandlerDoId, self.air.districtId, self.tutorialHandlerZoneId)

    def __handlerArrived(self, tutorialHandler):
        if not tutorialHandler:
            self.notify.warning('Failed to create tutorial handler for avatar %d!' % (self.avatar.doId))
            self._fail('Tutorial handler unavailable')
            return

        # Get the exterior door to find its parent location
        doorDoId = self.air.uidMgr.getDoId(TutorialGlobals.JAIL_EXTERIOR_DOOR)
        if doorDoId:
            self.exteriorDoor = self.air.doId2do.get(doorDoId)

        # The client sends it's login teleport as soon as the teleport manager arrives
        # in the uber zone, long before PlayGame has finished it's teleportToShard. That
        # teleport ends by placing the avatar in the district itself, which would clobber
        # the jail location (and the jail's instance interest) if we teleported first...
        if not self._avatarInDistrict():
            self.accept(DistributedObjectAI.staticGetZoneChangeEvent(self.avatar.doId),
                self._runCallback, [self.__avatarLocationChanged])
            return

        self.__startJailTeleport()

    def _avatarInDistrict(self):
        return getattr(self.avatar, 'parentId', self.air.districtId) == self.air.districtId

    def __avatarLocationChanged(self, newZoneId, oldZoneId):
        if not self._avatarInDistrict():
            return

        self.ignore(DistributedObjectAI.staticGetZoneChangeEvent(self.avatar.doId))
        self.__startJailTeleport()

    def __startJailTeleport(self):
        teleportMgr = self.air.teleportMgr
        if self.avatar.doId in teleportMgr.avatar2fsm:
            self.notify.warning('Avatar %d is already teleporting' % self.avatar.doId)
            self._fail('Avatar already teleporting')
            return

        self.acceptOnce('teleportDone-%d' % self.avatar.doId,
            self._runCallback, [self.__avatarArrived])

        jailWorld = self.interior.getParentObj()
        if not jailWorld or not jailWorld.spawnPts.get(TutorialGlobals.JAIL_INTERIOR):
            self.notify.warning('Tutorial jail instance or spawn point unavailable for avatar %d' %
                self.avatar.doId)
            self._fail('Tutorial jail spawn unavailable')
            return

        # New players start inside the jail, so teleport directly to the interior.
        # The exterior island zone is still loaded in the background.
        teleportMgr.d_initiateTeleport(
            self.avatar,
            instanceType=self.instance.getType(),
            instanceName=self.instance.getFileName(),
            locationUid=TutorialGlobals.JAIL_INTERIOR,
            spawnPt=jailWorld.getSpawnPt(TutorialGlobals.JAIL_INTERIOR, 0),
            tutorialFsm=self)
        self._teleportFSM = teleportMgr.avatar2fsm.get(self.avatar.doId)
        if not self._teleportFSM:
            self.notify.warning('Failed to initiate tutorial teleport for avatar %d' % self.avatar.doId)
            self._fail('Tutorial teleport could not start')

    def __avatarArrived(self):
        # the tutorial scene is shared by every new pirate, so the doors start
        # unlocked and are locked behind the avatar as it passes each stage...
        self._lockedDoors = set()
        self.accept(DistributedObjectAI.staticGetZoneChangeEvent(self.avatar.doId),
            self._updateDoorLocks)
        self._updateDoorLocks()

        self.instance.d_setTutorialHandlerId(self.tutorialHandler.doId)
        self._handlerPublished = True
        self.avatar.d_setTutorialHandlerZone(self.tutorialHandlerZoneId)
        self.air.tutorialManager.d_enterTutorial(self.avatar.doId, self.island.zoneId)
        taskMgr.remove(self._timeoutTaskName)

    def _getExteriorDoors(self, interior):
        if not interior:
            return []

        return [door for door in (interior.getExteriorFrontDoor(), interior.getExteriorBackDoor()) if door]

    def _getStageDoors(self):
        tavern = self.air.uidMgr.justGetMeMeObject(TutorialGlobals.TAVERN_INTERIOR)
        return (
            (self.interior, PiratesGlobals.TUT_MADE_PIRATE),
            (tavern, PiratesGlobals.TUT_GOT_SEACHEST))

    def _updateDoorLocks(self, *args):
        if self._finished:
            return

        # once the avatar has passed the stage a building belongs to and walked out
        # of it, the building's exterior doors are locked so it can't go back inside.
        # the stage comes from the avatar's tutorial checkpoint, so the doors are
        # locked again when the avatar resumes the tutorial at a later checkpoint...
        tutorial = self.avatar.getTutorial()
        parentId = getattr(self.avatar, 'parentId', 0)
        for interior, stage in self._getStageDoors():
            if not interior or tutorial < stage or parentId == interior.doId:
                continue

            for door in self._getExteriorDoors(interior):
                if door.doId not in self._lockedDoors:
                    self._lockedDoors.add(door.doId)
                    door.b_setLocked(True)

    def _unlockDoors(self):
        for doorId in getattr(self, '_lockedDoors', ()):
            door = self.air.doId2do.get(doorId)
            if door:
                door.b_setLocked(False)

        self._lockedDoors = set()

    def enterStop(self):
        taskMgr.remove(self._timeoutTaskName)
        self.ignoreAll()
        self._unlockDoors()
        for uid, callback in list(self._pendingUidCallbacks.items()):
            self.air.uidMgr.removeUidCallback(uid, callback)
        self._pendingUidCallbacks.clear()

        teleportMgr = self.air.teleportMgr
        if self._teleportFSM and teleportMgr.avatar2fsm.get(self.avatar.doId) is self._teleportFSM:
            self._teleportFSM.cleanup()
        self._teleportFSM = None

        manager = self.air.tutorialManager
        if manager.avatar2fsm.get(self.avatar.doId) is self:
            shipId = self.air.uidMgr.getDoId(TutorialGlobals.STUMPY_BOAT_UID)
            ship = self.air.doId2do.get(shipId)
            reset = getattr(ship, 'resetSailingToAuthoredPose', None)
            if reset:
                try:
                    if not reset():
                        manager._worldLoadFailed = True
                        self.notify.warning('Cannot reset tutorial ship for avatar %d' % self.avatar.doId)
                except Exception:
                    manager._worldLoadFailed = True
                    self.notify.warning('Tutorial ship reset failed for avatar %d:\n%s' %
                        (self.avatar.doId, traceback.format_exc()))

        if self._handlerPublished and self.instance:
            self.instance.d_setTutorialHandlerId(0)

        if self.tutorialHandler and getattr(self.tutorialHandler, 'doId', None):
            zoneId = self.tutorialHandlerZoneId
            air = self.air
            if zoneId is not None:
                self.acceptOnce(self.tutorialHandler.getDeleteEvent(), air.deallocateZone, [zoneId])
                self.tutorialHandlerZoneId = None
            self.tutorialHandler.requestDelete()
        elif self.tutorialHandlerZoneId is not None:
            self.air.deallocateZone(self.tutorialHandlerZoneId)
            self.tutorialHandlerZoneId = None

        self.island = None
        self.instance = None
        self.interior = None
        self.exteriorDoor = None
        self.tutorialHandler = None

        manager._tutorialFinished(self)
        self.demand('Off')

    def exitStop(self):
        pass

    def cleanup(self):
        if self._finished:
            return
        self._finished = True
        self.demand('Stop')


class PiratesTutorialManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesTutorialManagerAI')
    QUEUE_TIMEOUT_SECONDS = 120.0
    MAX_QUEUED = 64

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.avatar2fsm = {}
        self._worldLoaded = False
        self._worldLoading = False
        self._worldLoadFailed = False
        self._queued = {}
        self._queueTaskName = 'tutorial-queue-drain-%d' % id(self)
        self._drainScheduled = False
        self._deleting = False

    def getParentingRules(self):
        return ['', '']

    def delete(self):
        self._deleting = True
        taskMgr.remove(self._queueTaskName)
        self._drainScheduled = False
        for avatarId in list(self._queued):
            avatar, _ = self._removeQueued(avatarId)
            self._notifyFailure(avatar, 'Tutorial manager stopped')
        for fsm in list(self.avatar2fsm.values()):
            fsm._fail('Tutorial manager stopped')
        DistributedObjectAI.delete(self)

    def requestTutorial(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        self._requestTutorial(avatar)

    def _loadWorld(self):
        self._worldLoading = True
        try:
            self.air.worldCreator.loadObjectsFromFile(WorldGlobals.PiratesTutorialSceneFile)
            self._worldLoaded = True
        except Exception:
            # A failed load may have registered only part of the global scene.
            self._worldLoadFailed = True
            raise
        finally:
            self._worldLoading = False

    def _requestTutorial(self, avatar):
        if self._deleting or avatar.doId in self.avatar2fsm or avatar.doId in self._queued:
            return
        # Scene UIDs and the world handler ID are global, not per-avatar.
        if self._worldLoadFailed:
            self._notifyFailure(avatar, 'Tutorial world failed to load')
            return
        if self.avatar2fsm or self._worldLoading or self._queued:
            self._enqueue(avatar)
            return
        self._startTutorial(avatar)

    def _startTutorial(self, avatar):
        if self._worldLoadFailed:
            self._notifyFailure(avatar, 'Tutorial world failed to load')
            return
        if not self._worldLoaded and any(self.air.uidMgr.getDoId(uid) for uid in (
                RAMBLESHACK_REGION_UID, TutorialGlobals.RAMBLESHACK_ISLE_UID,
                TutorialGlobals.JAIL_INTERIOR)):
            self._notifyFailure(avatar, 'Tutorial scene already exists')
            return

        fsm = TutorialFSM(self.air, avatar)
        self.avatar2fsm[avatar.doId] = fsm
        try:
            fsm.request('Start')
        except Exception:
            fsm._fail('Tutorial startup failed')
            raise

    def _notifyFailure(self, avatar, reason):
        self.notify.warning('%s for avatar %d' % (reason, avatar.doId))
        if self.air.doId2do.get(avatar.doId) is avatar:
            # The manager has no failure field; eject uses the existing generic
            # connection-error dialog instead of leaving tutorialQuestion waiting.
            self.air.kickChannel(self.GetPuppetConnectionChannel(avatar.doId), 1, reason)

    def _enqueue(self, avatar):
        if len(self._queued) >= self.MAX_QUEUED:
            self._notifyFailure(avatar, 'Tutorial queue is full')
            return
        avatarId = avatar.doId
        taskName = 'tutorial-queue-%d-%d' % (avatarId, id(self))
        self._queued[avatarId] = (avatar, taskName)
        self.acceptOnce(avatar.getDeleteEvent(), self._removeQueued, [avatarId])
        taskMgr.doMethodLater(self.QUEUE_TIMEOUT_SECONDS, self._queueTimedOut,
            taskName, extraArgs=[avatarId])
        if not self.avatar2fsm and not self._worldLoading:
            self._scheduleQueue()

    def _removeQueued(self, avatarId):
        entry = self._queued.pop(avatarId, None)
        if entry:
            avatar, taskName = entry
            self.ignore(avatar.getDeleteEvent())
            taskMgr.remove(taskName)
        return entry

    def _queueTimedOut(self, avatarId):
        entry = self._removeQueued(avatarId)
        if entry:
            self._notifyFailure(entry[0], 'Tutorial queue timed out')
        return Task.done

    def _tutorialFinished(self, fsm):
        if self.avatar2fsm.get(fsm.avatar.doId) is fsm:
            del self.avatar2fsm[fsm.avatar.doId]
            self._scheduleQueue()

    def _scheduleQueue(self):
        if self._queued and not self._deleting and not self._drainScheduled:
            self._drainScheduled = True
            taskMgr.doMethodLater(0, self._drainQueue, self._queueTaskName)

    def _drainQueue(self, task):
        self._drainScheduled = False
        while self._queued and not self.avatar2fsm and not self._deleting:
            avatarId = next(iter(self._queued))
            avatar, _ = self._removeQueued(avatarId)
            if self.air.doId2do.get(avatarId) is not avatar:
                continue
            try:
                self._startTutorial(avatar)
            except Exception:
                self.notify.warning('Queued tutorial startup failed for avatar %d:\n%s' %
                    (avatarId, traceback.format_exc()))
        return Task.done

    def d_enterTutorial(self, avatarId, tutorialZone):
        self.sendUpdateToAvatarId(avatarId, 'enterTutorial', [tutorialZone])

    def allDone(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if avatar.doId not in self.avatar2fsm:
            self.notify.warning('Avatar %d requested allDone for a teleport operation, '
                'but no teleport operation was found!' % avatar.doId)

            return

        self.avatar2fsm[avatar.doId].cleanup()
