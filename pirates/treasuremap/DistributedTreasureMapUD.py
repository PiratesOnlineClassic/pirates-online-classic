from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal


class DistributedTreasureMapUD(DistributedObjectGlobalUD):
    """
    UberDOG-side treasure map manager.
    
    This handles global treasure map coordination across shards,
    tracking active instances, and managing treasure map inventory items.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTreasureMapUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        # Track active treasure map instances per shard
        # {shardId: {instanceDoId: instanceInfo}}
        self.activeInstances = {}

        # Track treasure maps owned by players
        # {avatarId: [mapIds]}
        self.playerMaps = {}

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.notify.info('DistributedTreasureMapUD generated')

    def delete(self):
        self.activeInstances = {}
        self.playerMaps = {}
        DistributedObjectGlobalUD.delete(self)

    # =========================================================================
    # Instance Tracking
    # =========================================================================

    def registerInstance(self, shardId, instanceDoId, mapId, hostAvatarId):
        """Register a new treasure map instance"""
        if shardId not in self.activeInstances:
            self.activeInstances[shardId] = {}

        self.activeInstances[shardId][instanceDoId] = {
            'mapId': mapId,
            'hostAvatarId': hostAvatarId,
            'participants': [hostAvatarId],
            'state': 'WaitClientsReady'
        }

        self.notify.info('Registered instance %d on shard %d (mapId=%d, host=%d)' % (
            instanceDoId, shardId, mapId, hostAvatarId))

    def unregisterInstance(self, shardId, instanceDoId):
        """Unregister a treasure map instance (completed or failed)"""
        if shardId in self.activeInstances:
            if instanceDoId in self.activeInstances[shardId]:
                del self.activeInstances[shardId][instanceDoId]
                self.notify.info('Unregistered instance %d on shard %d' % (instanceDoId, shardId))

    def updateInstanceState(self, shardId, instanceDoId, state):
        """Update the state of a treasure map instance"""
        if shardId in self.activeInstances:
            if instanceDoId in self.activeInstances[shardId]:
                self.activeInstances[shardId][instanceDoId]['state'] = state
                self.notify.debug('Updated instance %d state to %s' % (instanceDoId, state))

    def addParticipant(self, shardId, instanceDoId, avatarId):
        """Add a participant to an instance"""
        if shardId in self.activeInstances:
            if instanceDoId in self.activeInstances[shardId]:
                participants = self.activeInstances[shardId][instanceDoId]['participants']
                if avatarId not in participants:
                    participants.append(avatarId)
                    self.notify.debug('Added participant %d to instance %d' % (avatarId, instanceDoId))

    def removeParticipant(self, shardId, instanceDoId, avatarId):
        """Remove a participant from an instance"""
        if shardId in self.activeInstances:
            if instanceDoId in self.activeInstances[shardId]:
                participants = self.activeInstances[shardId][instanceDoId]['participants']
                if avatarId in participants:
                    participants.remove(avatarId)
                    self.notify.debug('Removed participant %d from instance %d' % (avatarId, instanceDoId))

    def getActiveInstances(self, shardId=None):
        """Get all active instances, optionally filtered by shard"""
        if shardId:
            return self.activeInstances.get(shardId, {})
        return self.activeInstances

    # =========================================================================
    # Player Map Tracking
    # =========================================================================

    def givePlayerMap(self, avatarId, mapId):
        """Give a player a treasure map"""
        if avatarId not in self.playerMaps:
            self.playerMaps[avatarId] = []

        if mapId not in self.playerMaps[avatarId]:
            self.playerMaps[avatarId].append(mapId)
            self.notify.info('Gave map %d to avatar %d' % (mapId, avatarId))

    def removePlayerMap(self, avatarId, mapId):
        """Remove a treasure map from a player (used after completion)"""
        if avatarId in self.playerMaps:
            if mapId in self.playerMaps[avatarId]:
                self.playerMaps[avatarId].remove(mapId)
                self.notify.info('Removed map %d from avatar %d' % (mapId, avatarId))

    def getPlayerMaps(self, avatarId):
        """Get all treasure maps owned by a player"""
        return self.playerMaps.get(avatarId, [])

    def playerHasMap(self, avatarId, mapId):
        """Check if a player has a specific treasure map"""
        return mapId in self.playerMaps.get(avatarId, [])