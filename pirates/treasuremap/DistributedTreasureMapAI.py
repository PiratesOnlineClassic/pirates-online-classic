from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from pirates.uberdog.DistributedInventoryAI import DistributedInventoryAI
from pirates.uberdog import InventoryInit

from otp.ai.MagicWordGlobal import *

from pirates.piratesbase import PiratesGlobals


class DistributedTreasureMapAI(DistributedInventoryAI):
    """
    AI-side representation of a treasure map item.
    
    This handles treasure map activation and instance creation requests.
    The treasure map is stored as an inventory item, and when activated,
    creates a treasure map instance for the players to participate in.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTreasureMapAI')
    registerWithInventoryManager = False

    def __init__(self, air):
        DistributedInventoryAI.__init__(self, air)

        self.mapId = 0
        self.isEnabled = 1
        self.objectiveIds = []
        self.participants = []  # Avatars who have accepted to join
        self.startPending = False
        self.activeInstance = None
        self.pendingInstanceDoId = 0

    def generate(self):
        DistributedInventoryAI.generate(self)

    def delete(self):
        taskMgr.remove(self.uniqueName('instance-generation-timeout'))
        if self.pendingInstanceDoId:
            self.ignore('generate-%d' % self.pendingInstanceDoId)
        if (self.activeInstance and self.air and
                self.air.doId2do.get(self.activeInstance.doId) is self.activeInstance):
            self.activeInstance.removeParticipant(self.ownerId)
        self.activeInstance = None
        self.participants = []
        DistributedInventoryAI.delete(self)

    # =========================================================================
    # DC Fields
    # =========================================================================

    def getParentingRules(self):
        return ['', '']

    def setMapId(self, mapId):
        self.mapId = mapId

    def d_setMapId(self, mapId):
        self.sendUpdate('setMapId', [mapId])

    def b_setMapId(self, mapId):
        self.setMapId(mapId)
        self.d_setMapId(mapId)

    def getMapId(self):
        return self.mapId

    def setObjectiveIds(self, objectiveIds):
        self.objectiveIds = objectiveIds

    def d_setObjectiveIds(self, objectiveIds):
        self.sendUpdate('setObjectiveIds', [objectiveIds])

    def b_setObjectiveIds(self, objectiveIds):
        self.setObjectiveIds(objectiveIds)
        self.d_setObjectiveIds(objectiveIds)

    def getObjectiveIds(self):
        return self.objectiveIds

    def setIsEnabled(self, enabled):
        self.isEnabled = enabled

    def d_setIsEnabled(self, enabled):
        self.sendUpdate('setIsEnabled', [enabled])

    def b_setIsEnabled(self, enabled):
        self.setIsEnabled(enabled)
        self.d_setIsEnabled(enabled)

    def getIsEnabled(self):
        return self.isEnabled

    # =========================================================================
    # Client Requests
    # =========================================================================

    def requestIsEnabled(self):
        """Client requests to check if this treasure map is enabled"""
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId or avatarId != self.ownerId:
            return

        self.sendUpdateToAvatarId(avatarId, 'setIsEnabled', [self.isEnabled])

    def requestStart(self, instanceType):
        """Client requests to start the treasure map instance"""
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId or avatarId != self.ownerId:
            return

        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('requestStart from unknown avatar %d' % avatarId)
            return

        self.notify.info('Avatar %d requests to start treasure map %d (type=%d)' % (
            avatarId, self.mapId, instanceType))

        self.startInstance(avatar)

    def startInstance(self, avatar, participantIds=[]):
        """
        Starts the treasure map instance for the owner, any participants (the owner's
        crew, gathered by the lookout) are sent along to the instance with them.
        """

        if not self.isEnabled:
            self.notify.warning('Treasure map %d is not enabled' % self.mapId)
            return False

        if self.startPending:
            return False
        if (self.activeInstance and
                self.air.doId2do.get(self.activeInstance.doId) is self.activeInstance and
                avatar.doId in self.activeInstance.participants):
            return False

        # Get the treasure map style info
        mapStyle = PiratesGlobals.DYNAMIC_GAME_STYLE_PROPS[PiratesGlobals.GAME_TYPE_TM].get(self.mapId)
        if not mapStyle or not mapStyle.get('MapName'):
            self.notify.warning('Unknown treasure map style %d' % self.mapId)
            return False
        mapName = mapStyle['MapName']

        self.notify.info('Starting treasure map instance: %s' % mapName)

        # Request creation of the treasure map instance world
        self.participants = [avatarId for avatarId in participantIds if avatarId != avatar.doId]
        self.startPending = True
        try:
            if not self._createTreasureMapInstance(avatar, mapName):
                self.startPending = False
                return False
        except Exception:
            self.startPending = False
            raise

        return True

    def _createTreasureMapInstance(self, avatar, mapName):
        """Create the treasure map instance and teleport the player there"""
        regionUid = self._getRegionUid(mapName)
        if not regionUid:
            self.notify.warning('No region UID configured for treasure map %s' % mapName)
            return False

        # Load the world file for this treasure map
        worldFile = mapName + '.py'

        self.notify.info('Creating treasure map instance from file: %s' % worldFile)

        previousDoId = self.air.uidMgr.getDoId(regionUid)
        # Use the world creator to load the treasure map world
        self.air.worldCreator.loadObjectsFromFile(worldFile)

        # Capture the generated doId now; another instance uses the same authored UID.
        instanceDoId = self.air.uidMgr.getDoId(regionUid)
        if not instanceDoId or instanceDoId == previousDoId:
            self.notify.warning('Treasure map %s did not generate a world' % mapName)
            return False
        if instanceDoId in self.air.doId2do:
            self._onInstanceCreated(instanceDoId, avatar)
        else:
            self.pendingInstanceDoId = instanceDoId
            self.acceptOnce('generate-%d' % instanceDoId,
                lambda instance: self._onInstanceCreated(instance.doId, avatar))
            taskMgr.doMethodLater(30, self._instanceGenerationTimedOut,
                                  self.uniqueName('instance-generation-timeout'))
        return True

    def _instanceGenerationTimedOut(self, task):
        if self.pendingInstanceDoId:
            self.ignore('generate-%d' % self.pendingInstanceDoId)
            self.pendingInstanceDoId = 0
        self.startPending = False
        return Task.done

    def _getRegionUid(self, mapName):
        """Get the region UID for a map name"""
        # These are the region UIDs from the world data files
        regionUids = {
            'BlackpearlWorld': '1171761196.78sdnaik',
        }
        return regionUids.get(mapName, '')

    def _onInstanceCreated(self, instanceDoId, avatar):
        """Called when the treasure map instance is created"""
        taskMgr.remove(self.uniqueName('instance-generation-timeout'))
        self.pendingInstanceDoId = 0
        instance = self.air.doId2do.get(instanceDoId)
        if not instance or self.air.doId2do.get(avatar.doId) is not avatar:
            self.startPending = False
            self.notify.warning('Failed to find created instance %d' % instanceDoId)
            return

        self.startPending = False
        self.activeInstance = instance
        self.notify.info('Treasure map instance created: %d, teleporting avatar %d' % (
            instanceDoId, avatar.doId))

        participants = [avatar]
        for participantId in self.participants:
            participant = self.air.doId2do.get(participantId)
            if participant:
                participants.append(participant)

        self.participants = []
        for participant in participants:
            self._sendAvatarToInstance(instance, participant)

    def _sendAvatarToInstance(self, instance, avatar):
        instance.addParticipant(avatar.doId)
        air = self.air

        def teleport():
            if self.air is not air or air.doId2do.get(avatar.doId) is not avatar:
                instance.removeParticipant(avatar.doId)
                return
            islands = instance.builder.getIslands()
            if not islands:
                self.notify.warning('No islands found in treasure map instance %d' % instance.doId)
                instance.removeParticipant(avatar.doId)
                return
            island = islands[0]
            spawnPt = instance.getSpawnPt(island.getUniqueId(), 0)
            air.teleportMgr.d_initiateTeleport(avatar,
                instanceType=instance.getType(),
                instanceName=instance.getFileName(),
                locationUid=island.getUniqueId(),
                spawnPt=spawnPt,
                targetWorld=instance)

        if instance.isReady:
            teleport()
        else:
            instance.pendingTeleportCallbacks.append(teleport)


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def treasuremap(mapId=0):
    """Start a treasure map instance"""
    invoker = spellbook.getInvoker()
    if not invoker:
        return "No invoker found"

    air = spellbook.getManager().air

    # Create a temporary treasure map AI
    treasureMap = DistributedTreasureMapAI(air)
    treasureMap.setInventoryVersion(InventoryInit.UberDogRevision)
    treasureMap.setOwnerId(invoker.doId)
    treasureMap.setMapId(mapId)
    treasureMap.generateWithRequired(air.districtId, air.allocateZone())

    # Start the map
    treasureMap._createTreasureMapInstance(invoker, 'BlackpearlWorld')

    return "Starting treasure map instance (mapId=%d)" % mapId