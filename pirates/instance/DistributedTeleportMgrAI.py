from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.task import Task

from otp.ai.MagicWordGlobal import *

from pirates.quest.QuestConstants import LocationIds
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from pirates.instance.DistributedTeleportZoneAI import DistributedTeleportZoneAI
from pirates.instance.DistributedTeleportHandlerAI import DistributedTeleportHandlerAI
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI


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
        if self.avatar.doId in self.air.teleportMgr.avatar2fsm:
            del self.air.teleportMgr.avatar2fsm[self.avatar.doId]
        self.ignoreAll()
        self.demand('Off')

class TeleportFSM(TeleportOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('TeleportFSM')

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

    def __teleportTimedOut(self, task):
        self.notify.warning('Teleport for avatar %d timed out, aborting!' % self.avatar.doId)
        if self.teleportHandler:
            self.teleportHandler.d_abortTeleport()

        self.cleanup()
        return Task.done

    def getFromInstanceType(self):
        fromInstance = self.air.teleportMgr.getInstanceFromObject(self.avatar.getParentObj())
        if not fromInstance:
            return PiratesGlobals.INSTANCE_NONE

        return fromInstance.getType()

    def enterTeleporting(self):
        # Notify the client that teleport is beginning (triggers loading screen and startedCallback)
        self.avatar.d_beginningTeleport(self.world.getType(), self.getFromInstanceType(),
            self.world.getFileName(), -1)

        # don't let a client that never finishes the teleport process
        # hold onto it's teleport zone and handler forever...
        taskMgr.doMethodLater(config.GetFloat('teleport-timeout', 300.0), self.__teleportTimedOut,
            self.avatar.uniqueName('teleport-timeout'))

        teleportZoneDoId = self.air.allocateChannel()
        self.acceptOnce('generate-%d' % teleportZoneDoId,
            self.__teleportZoneArrivedCallback)

        self.teleportZone = DistributedTeleportZoneAI(self.air)
        self.teleportZone.generateWithRequiredAndId(teleportZoneDoId,
            self.air.districtId, self.air.allocateZone())

    def exitTeleporting(self):
        taskMgr.remove(self.avatar.uniqueName('teleport-timeout'))
        if self.teleportZone:
            self.teleportZone.requestDelete()
            self.teleportZone = None

        if self.teleportHandler:
            self.teleportHandler.requestDelete()
            self.teleportHandler = None


class TeleportShipFSM(TeleportFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('TeleportShipFSM')

    def __init__(self, air, avatar, world, ship):
        TeleportFSM.__init__(self, air, avatar, world, ship, (0, 0, 0, 0))

        # the teleport handler spawns the avatar on board this ship,
        # rather than at a spawn point of a game area...
        self.ship = ship


class DistributedTeleportMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportMgrAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.avatar2fsm = {}

    def getWorld(self, instanceType, instanceName):
        worlds = []
        for object in list(self.air.doId2do.values()):
            if not object or not isinstance(object, DistributedInstanceBaseAI):
                continue

            if isinstance(object, DistributedTeleportZoneAI):
                continue

            if object.getType() != instanceType:
                continue

            if object.getFileName() == instanceName:
                return object

            worlds.append(object)

        # the client refers to the shard's main and welcome worlds by generic names
        # such as "mainWorld" or "Welcome World", rather than by the world's file name...
        if instanceType in (PiratesGlobals.INSTANCE_MAIN, PiratesGlobals.INSTANCE_WELCOME):
            for world in worlds:
                if world.getFileName().lower() == (instanceName or '').lower():
                    return world

            if worlds:
                return worlds[0]

            if instanceType == PiratesGlobals.INSTANCE_WELCOME:
                return self.getWorld(PiratesGlobals.INSTANCE_MAIN, instanceName)

        return None

    def getInstanceFromObject(self, object):
        while object is not None:
            if isinstance(object, DistributedInstanceBaseAI):
                return object

            object = object.getParentObj()

        return None

    def getWorldNames(self, instanceType):
        names = []
        for object in list(self.air.doId2do.values()):
            if not object or not isinstance(object, DistributedInstanceBaseAI):
                continue

            if object.getType() == instanceType:
                names.append(object.getFileName())

        return names

    def d_initiateTeleport(self, avatar, instanceType=None, instanceName=None,
                           locationUid=None, spawnPt=None, tutorialFsm=None,
                           targetWorld=None, useReturnLocation=True, force=False):
        if (instanceType == PiratesGlobals.INSTANCE_TUTORIAL and
                avatar.getTutorial() < PiratesGlobals.TUT_MET_JOLLY_ROGER):
            tutorialManager = self.air.tutorialManager
            # Only the owning tutorial FSM may perform its internal jail teleport.
            if (tutorialFsm is None or
                    tutorialManager.avatar2fsm.get(avatar.doId) is not tutorialFsm):
                # the tutorial manager now owns this teleport, this is not a failure;
                # failing here would make the client fall back on a mainWorld teleport
                # which then collides with the tutorial's own jail teleport...
                tutorialManager._requestTutorial(avatar)
                return True

        if avatar.doId in self.avatar2fsm:
            self.notify.warning('Cannot initiate teleport for avatar %d, '
                'already teleporting!' % avatar.doId)

            return False

        returnLocation = avatar.getReturnLocation()
        currentIsland = avatar.getCurrentIsland()

        # check to see which island the avatar exited last at,
        # then ensure this is their login teleport; not a normal teleport request...
        # The tutorial FSM supplies its own jail spawn location.
        if (useReturnLocation and returnLocation and not currentIsland and
                instanceType != PiratesGlobals.INSTANCE_TUTORIAL and
                targetWorld is None):
            locationUid = returnLocation

        gameArea = avatar.getParentObj()
        if (not force and isinstance(gameArea, DistributedGameAreaAI) and
                gameArea.getUniqueId() == locationUid and
                (targetWorld is None or
                 targetWorld.builder.getObject(uniqueId=locationUid) is gameArea)):
            self.notify.warning('Cannot initiate teleport for %d, '
                'already there, locationUid=%s!' % (avatar.doId, locationUid))

            return False

        if targetWorld is not None:
            world = targetWorld
            if self.air.doId2do.get(world.doId) is not world:
                self.notify.warning('Cannot initiate teleport for avatar %d: target world is unavailable' %
                    avatar.doId)
                return False
        elif not instanceType and not instanceName:
            world = self.getInstanceFromObject(gameArea)
            if not world and locationUid:
                world = self.getInstanceFromObject(self.air.uidMgr.justGetMeMeObject(locationUid))
        else:
            world = self.getWorld(instanceType, instanceName)

        if not world or not isinstance(world, DistributedInstanceBaseAI):
            if instanceType == PiratesGlobals.INSTANCE_TUTORIAL:
                self.notify.warning('Cannot initiate tutorial teleport for avatar %d: '
                    'tutorial world unavailable or tutorial already completed' % avatar.doId)
                return False

            self.notify.warning('Cannot initiate teleport for unknown world: '
                'instanceType=%r instanceName=%r' % (instanceType, instanceName))

            return False

        gameArea = world.builder.getObject(uniqueId=locationUid)
        if not gameArea and targetWorld is None:
            # Try looking up the object via uidMgr (for interiors, etc.)
            objectDoId = self.air.uidMgr.getDoId(locationUid)
            if objectDoId:
                gameArea = self.air.doId2do.get(objectDoId)
                if gameArea:
                    self.notify.info('Found gameArea via uidMgr: %s' % gameArea)

        if not gameArea and targetWorld is not None:
            self.notify.warning('Cannot initiate teleport for avatar %d: location %r '
                'is not in target world %d' % (avatar.doId, locationUid, world.doId))
            return False

        if not gameArea:
            # Attempt to select a default island if no area was supplied
            islands = world.builder.getIslands()
            if not len(islands):
                self.notify.warning('Cannot initiate teleport for unknown '
                    'gameArea: locationUid=%r' % locationUid)

                return False

            # Locate the first explorable island in the requested world
            for island in islands:
                if not island.getUndockable():
                    gameArea = island
                    break

            # Verify we have a game area
            if not gameArea:
                self.notify.warning('Cannot initiate teleport for unknown '
                    'gameArea: locationUid=%r' % locationUid)

                return False

        # check for paid status when trying to teleport to kingshead
        if gameArea.getUniqueId() == LocationIds.KINGSHEAD_ISLAND and not avatar.isPaid():
            gameArea.d_deniedEntryToIsland(avatar.doId)
            return False

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

            return False

        self.avatar2fsm[avatar.doId] = TeleportFSM(self.air, avatar, world, gameArea, spawnPt)
        self.avatar2fsm[avatar.doId].request('Teleporting')
        return True

    def initiateTeleport(self, instanceType, fromInstanceType, shardId, locationUid, instanceDoId, instanceName, gameType, friendDoId, friendAreaDoId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if shardId and shardId != self.air.districtId:
            self.requestTeleportToShard(avatar, shardId, instanceType, instanceName,
                locationUid, friendAreaDoId)

            return

        # Import here to avoid circular imports
        from pirates.ship.DistributedShipAI import DistributedShipAI

        # If friendDoId is set, we're teleporting to a friend - get their location
        if friendDoId:
            friend = self.air.doId2do.get(friendDoId)
            if not friend:
                self.notify.debug('Cannot teleport avatar %d to friend %d, '
                    'friend is not on this district!' % (avatar.doId, friendDoId))

                self.d_teleportFailed(avatar.doId)
                return

            friendParent = friend.getParentObj()
            if not friendParent:
                self.d_teleportFailed(avatar.doId)
                return

            friendAreaDoId = friendParent.doId

        # If friendAreaDoId is set (e.g., teleporting to a ship), handle ship teleport
        if friendAreaDoId:
            areaObj = self.air.doId2do.get(friendAreaDoId)
            if isinstance(areaObj, DistributedShipAI):
                if not self.teleportToShip(avatar, areaObj):
                    self.d_teleportFailed(avatar.doId)

                return

            if not isinstance(areaObj, DistributedGameAreaAI):
                self.notify.warning('Cannot teleport avatar %d to area %d, '
                    'invalid area object: %r!' % (avatar.doId, friendAreaDoId, areaObj))

                self.d_teleportFailed(avatar.doId)
                return

            # teleporting directly to an island (and not to a friend) requires
            # the avatar to own that island's teleport token...
            if not friendDoId and not self.canTeleportToArea(avatar, areaObj):
                self.notify.warning('Cannot teleport avatar %d to area %s, '
                    'avatar has no teleport token!' % (avatar.doId, areaObj.getUniqueId()))

                self.d_teleportFailed(avatar.doId)
                return

            if not self.teleportToArea(avatar, areaObj):
                self.d_teleportFailed(avatar.doId)

            return

        if not self.d_initiateTeleport(avatar, instanceType, instanceName, locationUid):
            self.d_teleportFailed(avatar.doId)

    def requestTeleportToShard(self, avatar, shardId, instanceType, instanceName, locationUid, areaDoId=0):
        # a remote area's uniqueId is looked up from the state server first...
        if not areaDoId:
            self.air.travelAgent.d_requestTeleportToShardAItoUD(avatar.doId, shardId, instanceType,
                instanceName, locationUid)

            return

        def _areaQueryCallback(doId, parentId, zoneId, dclass, fields):
            areaUid = (fields.get('setUniqueId') or [locationUid])[0]
            if not areaUid:
                self.notify.warning('Cannot resolve remote area %d for avatar %d, '
                    'using default location!' % (doId, avatar.doId))

            self.air.travelAgent.d_requestTeleportToShardAItoUD(avatar.doId, shardId, instanceType,
                instanceName, areaUid or '')

        self.air.getObject(areaDoId, _areaQueryCallback)

    def canTeleportToArea(self, avatar, area):
        # see LocalPirate.confirmIslandTeleport
        from pirates.world.DistributedIslandAI import DistributedIslandAI

        if not isinstance(area, DistributedIslandAI):
            return True

        areaUid = area.getUniqueId()
        if areaUid in (avatar.getReturnLocation(), avatar.getCurrentIsland()):
            return True

        if config.GetBool('teleport-all', False):
            return True

        token = InventoryType.getIslandTeleportToken(areaUid)
        inventory = avatar.getInventory()
        if token and inventory and inventory.getStackQuantity(token):
            return True

        worldCreator = getattr(self.air, 'worldCreator', None)
        return bool(worldCreator and worldCreator.isPvpIslandByUid(areaUid))

    def teleportToArea(self, avatar, area, spawnPt=None):
        if not self.getInstanceFromObject(area):
            self.notify.warning('Cannot teleport avatar %d to area %d, '
                'area has no instance!' % (avatar.doId, area.doId))

            return False

        return self.d_initiateTeleport(avatar, locationUid=area.getUniqueId(), spawnPt=spawnPt,
            useReturnLocation=False, force=True)

    def teleportToShip(self, avatar, ship):
        # the client places the avatar on deck once the ship is it's spawn parent
        if avatar.doId in self.avatar2fsm:
            self.notify.warning('Cannot teleport avatar %d to ship %d, '
                'already teleporting!' % (avatar.doId, ship.doId))

            return False

        world = self.getInstanceFromObject(ship)
        if not world or not getattr(world, 'oceanGrid', None):
            self.notify.warning('Cannot teleport avatar %d to ship %d, '
                'ship is not in a world!' % (avatar.doId, ship.doId))

            return False

        self.avatar2fsm[avatar.doId] = TeleportShipFSM(self.air, avatar, world, ship)
        self.avatar2fsm[avatar.doId].request('Teleporting')
        return True

    def teleportToAvatar(self, avatar, targetAvatar):
        from pirates.ship.DistributedShipAI import DistributedShipAI

        targetParent = targetAvatar.getParentObj()
        if isinstance(targetParent, DistributedShipAI):
            return self.teleportToShip(avatar, targetParent)

        if isinstance(targetParent, DistributedGameAreaAI):
            return self.teleportToArea(avatar, targetParent)

        return False

    def getAvatarTeleportLocation(self, avatar):
        # returns the (shardId, instanceDoId, areaDoId) the client's teleportResponse expects
        parentObj = avatar.getParentObj()
        instance = self.getInstanceFromObject(parentObj)
        if not parentObj or not instance or isinstance(instance, DistributedTeleportZoneAI):
            return None

        return (self.air.districtId, instance.doId, parentObj.doId)

    def d_teleportFailed(self, avatarId):
        # an empty location response causes the client to fail it's pending
        # teleport, and clear it's in teleport flag...
        self.d_localTeleportToIdResponse(avatarId, 0, 0)

    def requestTeleportToIsland(self, locationUid):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        island = self.air.uidMgr.justGetMeMeObject(locationUid)
        if not isinstance(island, DistributedGameAreaAI):
            self.notify.warning('Cannot teleport avatar %d to island, '
                'unknown island %r!' % (avatar.doId, locationUid))

            self.d_teleportToIslandResponse(avatar.doId, 0, 0)
            return

        world = self.getInstanceFromObject(island)
        if not world or not self.canTeleportToArea(avatar, island):
            self.d_teleportToIslandResponse(avatar.doId, 0, 0)
            return

        # the client follows up with initiateTeleport, using
        # the island as the area it wishes to teleport to...
        self.d_teleportToIslandResponse(avatar.doId, world.doId, island.doId)

    def requestCrossShardDeploy(self, shardId, islandUid, shipId):
        """
        Handle a request to deploy a ship and teleport the avatar to it on a different shard.
        This is typically used when on a Welcome Shard and selecting a ship to deploy.
        """
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if not islandUid or not shipId:
            self.notify.warning('Cannot process cross shard deploy for avatar %d, '
                'missing islandUid or shipId!' % self.air.getAvatarIdFromSender())
            return

        # If no shard specified or the shard is our own, handle locally
        if not shardId or shardId == self.air.districtId:
            # Deploy the ship locally and then teleport the avatar to it
            self._handleLocalCrossShardDeploy(avatar, islandUid, shipId)
        else:
            # Forward to the UD for cross-shard handling
            # TODO: Implement cross-shard deploy via UD
            self.notify.warning('Cross-shard deploy to different shard %d not yet implemented!' % shardId)

    def _handleLocalCrossShardDeploy(self, avatar, islandUid, shipId):
        """
        Handle deploying a ship and teleporting the avatar to it on this shard.
        """
        # Find the game area (island) for this island UID
        from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
        
        gameArea = None
        for obj in list(self.air.doId2do.values()):
            if isinstance(obj, DistributedGameAreaAI) and obj.getUniqueId() == islandUid:
                gameArea = obj
                break
        
        if not gameArea:
            self.notify.warning('Cannot process cross shard deploy for avatar %d, '
                'cannot find gameArea for islandUid %s!' % (avatar.doId, islandUid))
            return
        
        # Get the ship deployer from the island (gameArea), not the world
        if not hasattr(gameArea, 'shipDeployer') or not gameArea.shipDeployer:
            self.notify.warning('Cannot process cross shard deploy for avatar %d, '
                'no ship deployer available on island!' % avatar.doId)
            return
        
        def deployShipCallback(success):
            if not success:
                self.notify.warning('Cross shard deploy failed for avatar %d!' % avatar.doId)
                return
            
            # After deploy, teleport to the island
            self.d_initiateTeleport(avatar, locationUid=islandUid)
        
        # Deploy the ship via the island's ship deployer
        gameArea.shipDeployer.deployShip(avatar, shipId, deployShipCallback)

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

            self.d_teleportFailed(avatar.doId)
            return

        self.d_localTeleportToIdResponse(avatar.doId, target.parentId, target.zoneId)

    def d_localTeleportToIdResponse(self, avatarId, parentId, zoneId):
        self.sendUpdateToAvatarId(avatarId, '_localTeleportToIdResponse', [parentId, zoneId])

    def d_teleportToIslandResponse(self, avatarId, instanceDoId, islandDoId):
        """
        Send a teleport to island response to the client. This is an alternative
        to the full teleport flow for simple island-to-island teleports.
        """
        self.sendUpdateToAvatarId(avatarId, 'teleportToIslandResponse', [instanceDoId, islandDoId])


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def areaTeleport(locationUid):
    """
    Teleports the target based off a locations uniqueId
    """

    avatar = spellbook.getTarget()
    if not locationUid:
        return 'No location uid provided.'

    base.air.teleportMgr.d_initiateTeleport(avatar, locationUid=locationUid)
    return 'Teleporting avatar %d to area: %s...' % (avatar.doId, locationUid)

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int, str, str])
def world(instanceType, worldName, locationUid=None):
    """
    Teleport command for traveling to different worlds
    """

    names = base.air.teleportMgr.getWorldNames(instanceType)
    if worldName not in names:
        return 'Invalid world location: %s' % worldName

    avatar = spellbook.getTarget()
    base.air.teleportMgr.d_initiateTeleport(avatar, instanceType=instanceType, instanceName=worldName, locationUid=locationUid)
    return 'Teleporting avatar %d to world: %s...' % (avatar.doId, worldName)

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def tp(locationName):
    """
    Teleport command for teleporting to an object by it's location name defined
    """

    locationUid = None
    locationName = locationName.lower().replace("'", '')
    for uid, name in list(PLocalizer.LocationNames.items()):
        name = name.lower()
        name = name.replace("'", '')

        valid = any(char.isdigit() for char in uid)
        if name == locationName and valid:
            locationUid = uid
            break

    if locationUid != None:
        avatar = spellbook.getTarget()
        base.air.teleportMgr.d_initiateTeleport(avatar, locationUid=locationUid)
        return 'Teleporting avatar %d to area: %s...' % (avatar.doId, locationUid)

    return 'Unknown location %s' % locationName
