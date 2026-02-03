from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from otp.ai.MagicWordGlobal import *

from pirates.piratesbase import PiratesGlobals


class DistributedTreasureMapAI(DistributedObjectAI):
    """
    AI-side representation of a treasure map item.
    
    This handles treasure map activation and instance creation requests.
    The treasure map is stored as an inventory item, and when activated,
    creates a treasure map instance for the players to participate in.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTreasureMapAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.mapId = 0
        self.isEnabled = 1
        self.objectiveIds = []
        self.participants = []  # Avatars who have accepted to join

    def generate(self):
        DistributedObjectAI.generate(self)

    def delete(self):
        self.participants = []
        DistributedObjectAI.delete(self)

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
        if not avatarId:
            return

        self.sendUpdateToAvatarId(avatarId, 'setIsEnabled', [self.isEnabled])

    def requestStart(self, instanceType):
        """Client requests to start the treasure map instance"""
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return

        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('requestStart from unknown avatar %d' % avatarId)
            return

        self.notify.info('Avatar %d requests to start treasure map %d (type=%d)' % (
            avatarId, self.mapId, instanceType))

        if not self.isEnabled:
            self.notify.warning('Treasure map %d is not enabled' % self.mapId)
            return

        # Add to participants
        if avatarId not in self.participants:
            self.participants.append(avatarId)

        # Get the treasure map style info
        mapStyle = PiratesGlobals.TM_GAME_STYLES.get(self.mapId, {})
        mapName = mapStyle.get('MapName', 'BlackpearlWorld')

        self.notify.info('Starting treasure map instance: %s' % mapName)

        # Request creation of the treasure map instance world
        self._createTreasureMapInstance(avatar, mapName)

    def _createTreasureMapInstance(self, avatar, mapName):
        """Create the treasure map instance and teleport the player there"""
        # Load the world file for this treasure map
        worldFile = mapName + '.py'

        self.notify.info('Creating treasure map instance from file: %s' % worldFile)

        # Use the world creator to load the treasure map world
        self.air.worldCreator.loadObjectsFromFile(worldFile)

        # The world will be created through the WorldCreatorAI callback system
        # Once created, we need to teleport the avatar there
        # Register a callback for when the instance is ready
        self.air.uidMgr.addUidCallback(self._getRegionUid(mapName), 
            lambda instanceDoId: self._onInstanceCreated(instanceDoId, avatar))

    def _getRegionUid(self, mapName):
        """Get the region UID for a map name"""
        # These are the region UIDs from the world data files
        regionUids = {
            'BlackpearlWorld': '1171761196.78sdnaik',
        }
        return regionUids.get(mapName, '')

    def _onInstanceCreated(self, instanceDoId, avatar):
        """Called when the treasure map instance is created"""
        instance = self.air.doId2do.get(instanceDoId)
        if not instance:
            self.notify.warning('Failed to find created instance %d' % instanceDoId)
            return

        self.notify.info('Treasure map instance created: %d, teleporting avatar %d' % (
            instanceDoId, avatar.doId))

        # Add the avatar as a participant
        instance.addParticipant(avatar.doId)

        # Teleport the avatar to the instance
        # Find an island to spawn at
        islands = instance.builder.getIslands()
        if islands:
            island = islands[0]
            spawnPt = instance.getSpawnPt(island.getUniqueId(), 0)
            self.air.teleportMgr.d_initiateTeleport(avatar,
                instanceType=instance.getType(),
                instanceName=instance.getFileName(),
                locationUid=island.getUniqueId(),
                spawnPt=spawnPt)
        else:
            self.notify.warning('No islands found in treasure map instance')


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def treasuremap(mapId=0):
    """Start a treasure map instance"""
    invoker = spellbook.getInvoker()
    if not invoker:
        return "No invoker found"

    air = spellbook.getManager().air

    # Create a temporary treasure map AI
    treasureMap = DistributedTreasureMapAI(air)
    treasureMap.setMapId(mapId)
    treasureMap.generateWithRequired(air.districtId, air.allocateZone())

    # Start the map
    treasureMap._createTreasureMapInstance(invoker, 'BlackpearlWorld')

    return "Starting treasure map instance (mapId=%d)" % mapId