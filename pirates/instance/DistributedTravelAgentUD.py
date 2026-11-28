import random

from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

from pirates.piratesbase import PiratesGlobals


class DistributedTravelAgentUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTravelAgentUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        self.__shards = {}

        self.air.netMessenger.accept('registerShard', self,
            self.addShard)
        self.air.netMessenger.accept('unregisterShard', self,
            self.removeShard)

        # Districts report their status whenever their population changes and
        # whenever the UberDOG asks for it, this lets us know of the districts
        # that registered before the UberDOG was started:
        self.air.netMessenger.accept('districtStatus', self,
            self.handleDistrictStatus)

    def hasShard(self, shardId):
        return shardId in self.__shards

    def addShard(self, channel, shardId):
        if channel in self.__shards:
            return

        self.__shards[channel] = shardId

    def removeShard(self, channel, shardId):
        if channel not in self.__shards:
            return

        del self.__shards[channel]

    def handleDistrictStatus(self, channel, status):
        shardId = status.get('shardId')
        if shardId:
            self.addShard(channel, shardId)

    def getShard(self, shardId):
        for channel in self.__shards:
            if self.__shards[channel] == shardId:
                return channel

        return None

    def isShardFull(self, channel):
        districtTracker = getattr(self.air, 'districtTracker', None)
        if not districtTracker:
            return False

        status = districtTracker.getShards().get(channel, {})
        lowLimit, highLimit = status.get('populationLimits', (0, 0))
        return bool(highLimit) and status.get('population', 0) >= highLimit

    def getRandomShard(self, shardType=None, excludeShardId=0):
        if not self.__shards:
            return None

        districtTracker = getattr(self.air, 'districtTracker', None)
        districtStatuses = districtTracker.getShards() if districtTracker else {}
        shards = []
        for channel, shardId in list(self.__shards.items()):
            if shardId == excludeShardId:
                continue

            if shardType is not None:
                status = districtStatuses.get(channel, {})
                if status.get('shardType') != shardType:
                    continue

            shards.append((channel, shardId))

        if not shards:
            return None

        # Prefer districts that still have room, but use a full district if needed:
        availableShards = [(channel, shardId) for channel, shardId in shards
            if not self.isShardFull(channel)]
        if availableShards:
            shards = availableShards

        return random.choice(shards)[1]

    def requestInitLocUD(self, unused, shardId):
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return

        # The avatar's default shard may since have gone down, in which case
        # we'd rather send them somewhere else than leave them waiting:
        if shardId and not self.getShard(shardId):
            self.notify.info('Avatar %d asked for unknown shard %d, choosing another one.' % (
                avatarId, shardId))

            shardId = 0

        shardId = shardId or self.getRandomShard()
        if not shardId:
            self.notify.warning('Cannot initialize loc teleport for avatar %d, '
                'no shards are available!' % avatarId)

            return

        channel = self.getShard(shardId)
        if not channel:
            self.notify.warning('Cannot initialize loc teleport for avatar %d, '
                'unknown shard %d!' % (avatarId, shardId))

            return

        self.sendUpdateToChannel(channel, 'requestInitLocUDtoAI', [avatarId])

    def requestTeleportToShardAItoUD(self, avatarId, shardId, instanceType, instanceName, locationUid):
        if not avatarId:
            return

        if not shardId:
            self.notify.warning('Cannot initialize teleport to shard for avatar %d, '
                'invalid shard!' % avatarId)

            return

        channel = self.getShard(shardId)
        if not channel:
            self.notify.warning('Cannot initialize teleport to shard %d for avatar %d, '
                'unknown channel!' % (shardId, avatarId))

            return

        self.sendUpdateToChannel(channel, 'requestTeleportToShardUDtoAI', [avatarId, shardId,
            instanceType, instanceName, locationUid])

    def requestCrossShardDeployAItoUD(self, avatarId, sourceShardId, shardId, islandUid, shipId):
        if not avatarId or not islandUid or not shipId:
            self.notify.warning('Cannot route cross-shard deploy, '
                'invalid avatar, island, or ship!')
            return

        sourceChannel = self.getShard(sourceShardId)
        if not sourceChannel:
            self.notify.warning('Cannot route cross-shard deploy for avatar %d, '
                'unknown source shard %d!' % (avatarId, sourceShardId))
            return

        if not shardId:
            shardId = self.getRandomShard(
                shardType=PiratesGlobals.SHARD_MAIN, excludeShardId=sourceShardId)
        elif not self.getShard(shardId):
            self.notify.warning('Cannot route cross-shard deploy for avatar %d, '
                'unknown target shard %d!' % (avatarId, shardId))
            self.sendUpdateToChannel(sourceChannel, 'crossShardDeployFailed', [avatarId])
            return

        channel = self.getShard(shardId) if shardId else None
        if not channel:
            self.notify.warning('Cannot route cross-shard deploy for avatar %d, '
                'no eligible main-world shard is available!' % avatarId)
            self.sendUpdateToChannel(sourceChannel, 'crossShardDeployFailed', [avatarId])
            return

        self.sendUpdateToChannel(channel, 'requestCrossShardDeployUDtoAI', [
            avatarId, shardId, islandUid, shipId])
