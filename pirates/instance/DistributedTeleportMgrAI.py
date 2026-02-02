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
        # Notify the client that teleport is beginning (triggers loading screen and startedCallback)
        self.avatar.d_beginningTeleport(
            self.world.getType(),
            0,  # fromInstanceType - will be set properly by client
            self.world.getFileName(),
            -1  # gameType
        )

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
        for object in list(self.air.doId2do.values()):
            if not object or not isinstance(object, DistributedInstanceBaseAI):
                continue

            if object.getType() == instanceType and object.getFileName() == instanceName:
                return object

        return None

    def getWorldNames(self, instanceType):
        names = []
        for object in list(self.air.doId2do.values()):
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
            # If this is a tutorial world that doesn't exist yet, trigger tutorial creation
            if instanceType == PiratesGlobals.INSTANCE_TUTORIAL:
                # Verify the player actually needs the tutorial (hasn't completed it)
                tutorialState = avatar.getTutorial()
                if tutorialState >= PiratesGlobals.TUT_MET_JOLLY_ROGER:
                    self.notify.warning('Avatar %d has tutorial state %d, skipping tutorial creation' % (avatar.doId, tutorialState))
                    return

                if avatar.doId not in self.air.tutorialManager.avatar2fsm:
                    self.notify.info('Tutorial world not found, initiating tutorial creation for avatar %d (tutorialState=%d)' % (avatar.doId, tutorialState))
                    self.air.tutorialManager._requestTutorial(avatar)
                    return
                else:
                    # Tutorial is already in progress, don't recursively call
                    self.notify.warning('Tutorial already in progress for avatar %d, waiting...' % avatar.doId)
                    return

            self.notify.warning('Cannot initiate teleport for unknown world: '
                'instanceType=%r instanceName=%r' % (instanceType, instanceName))

            return

        gameArea = world.builder.getObject(uniqueId=locationUid)
        if not gameArea:
            # Try looking up the object via uidMgr (for interiors, etc.)
            objectDoId = self.air.uidMgr.getDoId(locationUid)
            if objectDoId:
                gameArea = self.air.doId2do.get(objectDoId)
                if gameArea:
                    self.notify.info('Found gameArea via uidMgr: %s' % gameArea)

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

        # check for paid status when trying to teleport to kingshead
        if gameArea.getUniqueId() == LocationIds.KINGSHEAD_ISLAND and not avatar.isPaid():
            gameArea.d_deniedEntryToIsland(avatar.doId)
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

        self.avatar2fsm[avatar.doId] = TeleportFSM(self.air, avatar, world, gameArea, spawnPt)
        self.avatar2fsm[avatar.doId].request('Teleporting')

    def initiateTeleport(self, instanceType, fromInstanceType, shardId, locationUid, instanceDoId, instanceName, gameType, friendDoId, friendAreaDoId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if shardId and shardId != self.air.districtId:
            self.air.travelAgent.d_requestTeleportToShardAItoUD(avatar.doId, shardId, instanceType,
                instanceName, locationUid)

            return

        # Import here to avoid circular imports
        from pirates.ship.DistributedShipAI import DistributedShipAI

        # If friendDoId is set, we're teleporting to a friend - get their location
        if friendDoId:
            friend = self.air.doId2do.get(friendDoId)
            if friend:
                friendParent = friend.getParentObj()
                if friendParent:
                    # Check if the friend is on a ship
                    if isinstance(friendParent, DistributedShipAI):
                        # Teleport to the ship instead
                        friendAreaDoId = friendParent.doId
                    elif hasattr(friendParent, 'getUniqueId'):
                        locationUid = friendParent.getUniqueId()

        # If friendAreaDoId is set (e.g., teleporting to a ship), handle ship teleport
        if friendAreaDoId:
            areaObj = self.air.doId2do.get(friendAreaDoId)
            if areaObj:
                if isinstance(areaObj, DistributedShipAI):
                    # Ship teleport - send the client the ship's location so they can board
                    self.d_localTeleportToIdResponse(avatar.doId, areaObj.parentId, areaObj.zoneId)
                    return
                elif hasattr(areaObj, 'getUniqueId'):
                    locationUid = areaObj.getUniqueId()

        self.d_initiateTeleport(avatar, instanceType, instanceName, locationUid)

    def requestTeleportToIsland(self, locationUid):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        self.d_initiateTeleport(avatar, locationUid=locationUid)

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
