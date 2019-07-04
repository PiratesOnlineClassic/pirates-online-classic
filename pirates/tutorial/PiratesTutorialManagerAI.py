from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from pirates.world.WorldCreatorAI import WorldCreatorAI
from pirates.world import WorldGlobals
from pirates.tutorial import TutorialGlobals
from pirates.tutorial.DistributedPiratesTutorialAI import DistributedPiratesTutorialAI


class TutorialFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('TutorialFSM')

    def __init__(self, air, avatar):
        FSM.__init__(self, 'TutorialFSM')

        self.air = air
        self.avatar = avatar

        self.island = None
        self.instance = None
        self.interior = None
        self.tutorialHandler = None

    def enterStart(self):
        self.acceptOnce(self.avatar.getDeleteEvent(), self.cleanup)
        self.air.uidMgr.addUidCallback(TutorialGlobals.RAMBLESHACK_ISLE_UID, self.__worldArrived)
        self.air.worldCreator.loadObjectsFromFile(WorldGlobals.PiratesTutorialSceneFile)

    def exitStart(self):
        pass

    def __worldArrived(self, instanceDoId):
        self.island = self.air.doId2do.get(instanceDoId)
        if not self.island:
            self.notify.warning('Failed to create tutorial island for avatar %d!' % (self.avatar.doId))
            self.cleanup()
            return

        self.instance = self.island.getParentObj()
        if not self.instance:
            self.notify.warning('Failed to create tutorial world for avatar %d!' % (self.avatar.doId))
            self.cleanup()
            return

        self.air.uidMgr.addUidCallback(TutorialGlobals.JAIL_INTERIOR, self.__interiorArrived)

    def __interiorArrived(self, interiorDoId):
        self.interior = self.air.doId2do.get(interiorDoId)
        if not self.interior:
            self.notify.warning('Failed to create tutorial interior for avatar %d!' % (self.avatar.doId))
            self.cleanup()
            return

        tutorialHandlerDoId = self.air.allocateChannel()
        self.acceptOnce('generate-%d' % tutorialHandlerDoId, self.__handlerArrived)

        self.tutorialHandlerZoneId = self.air.allocateZone()

        self.tutorialHandler = DistributedPiratesTutorialAI(self.air)
        self.tutorialHandler.generateWithRequiredAndId(tutorialHandlerDoId, self.air.districtId, self.tutorialHandlerZoneId)

    def __handlerArrived(self, tutorialHandler):
        if not tutorialHandler:
            self.notify.warning('Failed to create tutorial handler for avatar %d!' % (self.avatar.doId))
            self.cleanup()
            return

        self.acceptOnce('teleportDone-%d' % self.avatar.doId, self.__avatarArrived)
        self.air.teleportMgr.d_initiateTeleport(self.avatar, instanceType=self.instance.getType(),
            instanceName=self.instance.getFileName(), locationUid=self.interior.getUniqueId(),
            spawnPt=self.instance.getSpawnPt(self.interior.getUniqueId(), 0))

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

        del self.air.tutorialManager.avatar2fsm[self.avatar.doId]
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

        if avatar.doId in self.avatar2fsm:
            self.notify.warning('Cannot handle tutorial request for avatar %d, '
                'tutorial already in progress!' % avatar.doId)

            return

        self.avatar2fsm[avatar.doId] = TutorialFSM(self.air, avatar)
        self.avatar2fsm[avatar.doId].request('Start')

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
