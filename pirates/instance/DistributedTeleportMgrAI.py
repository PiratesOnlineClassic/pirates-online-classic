from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from otp.ai.MagicWordGlobal import *

from pirates.quest.QuestConstants import LocationIds
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from pirates.instance.DistributedTeleportZoneAI import DistributedTeleportZoneAI
from pirates.instance.DistributedTeleportHandlerAI import DistributedTeleportHandlerAI
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.ship.DistributedShipAI import DistributedShipAI


class TeleportOperationFSM(FSM):

    def __init__(self, air, avatar, world, gameArea, spawnPt):
        FSM.__init__(self, self.__class__.__name__)

        self.air = air
        self.avatar = avatar
        self.world = world
        self.gameArea = gameArea
        self.spawnPt = spawnPt

        self.teleportZone = None
        self.teleportHandler = None

        # just incase the avatar disconnects before we can complete the teleport
        # process, handle cleanup appropriately...
        self.acceptOnce(self.avatar.getDeleteEvent(), self.cleanup)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def cleanup(self):
        del self.air.teleportMgr.avatar2fsm[self.avatar.doId]
        self.ignoreAll()
        self.demand('Off')

class TeleportFSM(TeleportOperationFSM):

    def __teleportZoneArrivedCallback(self, teleportZone):
        if not teleportZone:
            self.notify.warning('Failed to generate the teleport zone for avatar %d, '
                'while trying to teleport!' % self.avatar.doId)

            self.cleanup()
            return

        teleportHandlerDoId = self.air.allocateChannel()
        self.acceptOnce('generate-%d' % teleportHandlerDoId,
            self.__teleportHandlerArrivedCallback)

        self.teleportHandler = DistributedTeleportHandlerAI(self.air,
            self.air.teleportMgr, self, self.avatar)

        self.teleportHandler.generateWithRequiredAndId(teleportHandlerDoId,
            self.air.districtId, self.teleportZone.zoneId)

    def __teleportHandlerArrivedCallback(self, teleportHandler):
        if not teleportHandler:
            self.notify.warning('Failed to generate the teleport handler for avatar %d, '
                'while trying to teleport!' % self.avatar.doId)

            self.cleanup()
            return

        self.avatar.d_forceTeleportStart(self.world.getFileName(), self.teleportZone.doId,
            self.teleportHandler.doId, 0, self.teleportZone.parentId, self.teleportZone.zoneId)

    def enterTeleporting(self):
        teleportZoneDoId = self.air.allocateChannel()
        self.acceptOnce('generate-%d' % teleportZoneDoId,
            self.__teleportZoneArrivedCallback)

        self.teleportZone = DistributedTeleportZoneAI(self.air)
        self.teleportZone.generateWithRequiredAndId(teleportZoneDoId,
            self.air.districtId, self.air.allocateZone())

    def exitTeleporting(self):
        if self.teleportZone:
            self.teleportZone.requestDelete()
            self.teleportZone = None

        if self.teleportHandler:
            self.teleportHandler.requestDelete()
            self.teleportHandler = None


class DistributedTeleportMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportMgrAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.avatar2fsm = {}

    def getWorld(self, instanceType, instanceName):
        for object in self.air.doId2do.values():
            if not object or not isinstance(object, DistributedInstanceBaseAI):
                continue

            if object.getType() == instanceType and object.getFileName() == instanceName:
                return object

        return None

    def getWorldNames(self, instanceType):
        names = []
        for object in self.air.doId2do.values():
            if not object or not isinstance(object, DistributedInstanceBaseAI):
                continue

            if object.getType() == instanceType:
                names.append(object.getFileName())

        return names

    def d_initiateTeleport(self, avatar, instanceType=None, instanceName=None, locationUid=None, spawnPt=None):
        if avatar.doId in self.avatar2fsm:
            self.notify.warning('Cannot initiate teleport for avatar %d, '
                'already teleporting!' % avatar.doId)

            return

        returnLocation = avatar.getReturnLocation()
        currentIsland = avatar.getCurrentIsland()

        # check to see which island the avatar exited last at,
        # then ensure this is their login teleport; not a normal teleport request...
        if returnLocation and not currentIsland:
            locationUid = returnLocation

        gameArea = avatar.getParentObj()
        if isinstance(gameArea, DistributedGameAreaAI) and gameArea.getUniqueId() == locationUid:
            self.notify.warning('Cannot initiate teleport for %d, '
                'already there, locationUid=%s!' % (avatar.doId, locationUid))

            return

        if not instanceType and not instanceName:
            world = gameArea.getParentObj()
        else:
            world = self.getWorld(instanceType, instanceName)

        if not world or not isinstance(world, DistributedInstanceBaseAI):
            self.notify.warning('Cannot initiate teleport for unknown world: '
                'instanceType=%r instanceName=%r' % (instanceType, instanceName))

            return

        gameArea = world.builder.getObject(uniqueId=locationUid)
        if not gameArea:

            # Attempt to select a default island if no area was supplied
            islands = world.builder.getIslands()
            if not len(islands):
                self.notify.warning('Cannot initiate teleport for unknown '
                    'gameArea: locationUid=%r' % locationUid)

                return

            # Locate the first explorable island in the requested world
            for island in islands:
                if not island.getUndockable():
                    gameArea = island
                    break

            # Verify we have a game area
            if not gameArea:
                self.notify.warning('Cannot initiate teleport for unknown '
                    'gameArea: locationUid=%r' % locationUid)

                return

        if not spawnPt:
            # TODO FIXME!
            # if we have no spawn point for this world and we need to retrieve one,
            # then let's assume the world is the game area's parent... When teleporting
            # from an interior to an exterior, the world is not the game area's parent...?
            world = gameArea.getParentObj()
            spawnPt = world.getSpawnPt(gameArea.getUniqueId())

        if not spawnPt:
            self.notify.warning('Cannot initiate teleport for avatar %d, no available spawn points '
                'for gameArea, locationUid=%r!' % (avatar.doId, locationUid))

            return

        self.avatar2fsm[avatar.doId] = TeleportFSM(self.air,
            avatar, world, gameArea, spawnPt)

        self.avatar2fsm[avatar.doId].request('Teleporting')

    def initiateTeleport(self, instanceType, fromInstanceType, shardId, locationUid, instanceDoId, instanceName, gameType, friendDoId, friendAreaDoId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if shardId and shardId != self.air.districtId:
            self.air.travelAgent.d_requestTeleportToShardAItoUD(avatar.doId, shardId, instanceType,
                instanceName, locationUid)

            return

        self.d_initiateTeleport(avatar, instanceType, instanceName, locationUid)

    def requestTeleportToIsland(self, locationUid):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        self.d_initiateTeleport(avatar, locationUid=locationUid)

    def d_teleportHasBegun(self, avatarId, instanceType, fromInstanceType, instanceName, gameType):
        self.sendUpdateToAvatarId(avatarId, 'teleportHasBegun', [instanceType, fromInstanceType,
            instanceName, gameType])

    def requestTargetsLocation(self, locationId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        target = self.air.doId2do.get(locationId)
        if not target:
            self.notify.debug('Cannot send target location for avatar %d, '
                'unknown target object %d!' % (avatar.doId, locationId))

            return

        self.d_localTeleportToIdResponse(avatar.doId, target.parentId, target.zoneId)

    def d_localTeleportToIdResponse(self, avatarId, parentId, zoneId):
        self.sendUpdateToAvatarId(avatarId, '_localTeleportToIdResponse', [parentId, zoneId])


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def areaTeleport(areaUid):
    avatar = spellbook.getTarget()
    simbase.air.teleportMgr.d_initiateTeleport(avatar, locationUid=locationUid)
    return 'Teleporting avatar %d to area: %s...' % (avatar.doId, locationUid)

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int, str, str])
def world(instanceType, worldName, locationUid=None):
    """
    Teleport command for traveling to different worlds
    """

    names = simbase.air.teleportMgr.getWorldNames(instanceType)
    if worldName not in names:
        return 'Invalid world location: %s' % worldName

    avatar = spellbook.getTarget()
    simbase.air.teleportMgr.d_initiateTeleport(avatar, instanceType=instanceType, instanceName=worldName, locationUid=locationUid)
    return 'Teleporting avatar %d to world: %s...' % (avatar.doId, worldName)

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def tp(locationName):
    """
    Teleport command for teleporting to an object by it's location name defined
    """

    locationUid = None
    for uid, name in PLocalizer.LocationNames.items():
        name = name.lower()
        name = name.replace("'", '')

        valid = any(char.isdigit() for char in uid)
        if name == locationName and valid:
            locationUid = uid
            break

    if locationUid != None:
        avatar = spellbook.getTarget()
        simbase.air.teleportMgr.d_initiateTeleport(avatar, locationUid=locationUid)
        return 'Teleporting avatar %d to area: %s...' % (avatar.doId, locationUid)

    return 'Unknown location %s' % locationName
