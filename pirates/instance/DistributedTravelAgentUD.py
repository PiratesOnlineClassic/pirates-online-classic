import random

from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal


class DistributedTravelAgentUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTravelAgentUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        self.__shards = {}

        self.air.netMessenger.accept('registerShard', self,
            self.addShard)

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

    def getShard(self, shardId):
        for channel in self.__shards:
            if self.__shards[channel] == shardId:
                return channel

        return None

    def getRandomShard(self):
        if not self.__shards:
            return None

        return random.choice(list(self.__shards.values()))

    def requestInitLocUD(self, unused, shardId):
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return

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
