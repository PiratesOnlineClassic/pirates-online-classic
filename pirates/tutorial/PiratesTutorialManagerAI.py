from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from pirates.world.WorldCreatorAI import WorldCreatorAI
from pirates.world import WorldGlobals
from pirates.tutorial import TutorialGlobals
from pirates.tutorial.DistributedPiratesTutorialAI import DistributedPiratesTutorialAI

# Region UID for the tutorial world (RambleshackWorld)
RAMBLESHACK_REGION_UID = '1115838788a.58jubutler'


class TutorialFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('TutorialFSM')

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

    def enterStart(self):
        self.acceptOnce(self.avatar.getDeleteEvent(), self.cleanup)
        self.notify.info('Starting tutorial for avatar: %s' % self.avatar.doId)

        # Register callback for the Region UID (world) first so we have it when interior arrives
        self.air.uidMgr.addUidCallback(RAMBLESHACK_REGION_UID, self.__instanceArrived)
        
        # Now load our world
        self.air.worldCreator.loadObjectsFromFile(WorldGlobals.PiratesTutorialSceneFile)

    def exitStart(self):
        pass

    def __instanceArrived(self, instanceDoId):
        self.instance = self.air.doId2do.get(instanceDoId)
        if not self.instance:
            self.notify.warning('Failed to create tutorial world for avatar %d!' % self.avatar.doId)
            self.cleanup()
            return

        self.notify.info('Tutorial world created for avatar %d: %s' % (self.avatar.doId, self.instance))

        # Now wait for the island
        self.air.uidMgr.addUidCallback(TutorialGlobals.RAMBLESHACK_ISLE_UID, self.__islandArrived)

    def __islandArrived(self, islandDoId):
        self.island = self.air.doId2do.get(islandDoId)
        if not self.island:
            self.notify.warning('Failed to create tutorial island for avatar %d!' % self.avatar.doId)
            self.cleanup()
            return

        self.notify.info('Tutorial island created for avatar %d: %s' % (self.avatar.doId, self.island))

        # Now wait for the interior
        self.air.uidMgr.addUidCallback(TutorialGlobals.JAIL_INTERIOR, self.__interiorArrived)

    def __interiorArrived(self, interiorDoId):
        self.interior = self.air.doId2do.get(interiorDoId)
        if not self.interior:
            self.notify.warning('Failed to create tutorial interior for avatar %d!' % self.avatar.doId)
            self.cleanup()
            return

        self.notify.info('Tutorial interior created for avatar %d: %s' % (self.avatar.doId, self.interior))

        tutorialHandlerDoId = self.air.allocateChannel()
        self.acceptOnce('generate-%d' % tutorialHandlerDoId, self.__handlerArrived)

        self.tutorialHandlerZoneId = self.air.allocateZone()

        self.tutorialHandler = DistributedPiratesTutorialAI(self.air)
        self.tutorialHandler.setAvatarId(self.avatar.doId)
        self.tutorialHandler.generateWithRequiredAndId(tutorialHandlerDoId, self.air.districtId, self.tutorialHandlerZoneId)

    def __handlerArrived(self, tutorialHandler):
        if not tutorialHandler:
            self.notify.warning('Failed to create tutorial handler for avatar %d!' % (self.avatar.doId))
            self.cleanup()
            return

        # Get the exterior door to find its parent location
        doorDoId = self.air.uidMgr.getDoId(TutorialGlobals.JAIL_EXTERIOR_DOOR)
        if doorDoId:
            self.exteriorDoor = self.air.doId2do.get(doorDoId)

        self.acceptOnce('teleportDone-%d' % self.avatar.doId, self.__avatarArrived)

        # New players start inside the jail, so teleport directly to the interior.
        # The exterior island zone is still loaded in the background.
        self.air.teleportMgr.d_initiateTeleport(
            self.avatar,
            instanceType=self.instance.getType(),
            instanceName=self.instance.getFileName(),
            locationUid=TutorialGlobals.JAIL_INTERIOR,
            spawnPt=self.instance.getSpawnPt(TutorialGlobals.JAIL_INTERIOR, 0))

    def __avatarArrived(self):
        self.instance.d_setTutorialHandlerId(self.tutorialHandler.doId)
        self.avatar.d_setTutorialHandlerZone(self.tutorialHandlerZoneId)
        self.air.tutorialManager.d_enterTutorial(self.avatar.doId, self.island.zoneId)

    def enterStop(self):
        if self.island:
            self.island.requestDelete()

        if self.instance:
            self.instance.requestDelete()

        if self.interior:
            self.interior.requestDelete()

        if self.tutorialHandler:
            self.air.deallocateZone(self.tutorialHandlerZoneId)
            self.tutorialHandler.requestDelete()

        self.island = None
        self.instance = None
        self.interior = None
        self.tutorialHandler = None

        # Save the values we still need before clearing state
        air = self.air
        avatarId = self.avatar.doId

        # Use pop to safely remove without KeyError if already cleaned up
        air.tutorialManager.avatar2fsm.pop(avatarId, None)
        self.demand('Off')

    def exitStop(self):
        pass

    def cleanup(self):
        self.demand('Stop')


class PiratesTutorialManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesTutorialManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.avatar2fsm = {}

    def getParentingRules(self):
        return ['', '']

    def requestTutorial(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        self._requestTutorial(avatar)

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
