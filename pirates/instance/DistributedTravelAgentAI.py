from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal

from otp.distributed import OtpDoGlobals


class DistributedTravelAgentAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTravelAgentAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)

        self.air.netMessenger.send('registerShard', [self.air.ourChannel,
            self.air.districtId])

        # Should we ever go down, the UberDOG must stop sending avatars here:
        self.air.addPostRemove(self.air.netMessenger.prepare('unregisterShard',
            [self.air.ourChannel, self.air.districtId]))

    def requestInitLocUDtoAI(self, avatarId):
        if not avatarId:
            return

        def avatarArrived(avatar):
            if not avatar:
                self.notify.warning('Cannot initialize teleport loc for avatar %d, '
                    'invalid generate!' % avatarId)

                return

            avatar.d_relayTeleportLoc(self.air.districtId, self.air.distributedDistrict.zoneId, self.air.teleportMgr.doId)

        # the avatar is already being managed by this district,
        # there is no need to wait for it to arrive here...
        avatar = self.air.doId2do.get(avatarId)
        if avatar:
            avatarArrived(avatar)
            return

        self.__getAvatarArrival(avatarId, avatarArrived)

    def d_requestTeleportToShardAItoUD(self, avatarId, shardId, instanceType, instanceName, locationUid):
        if not avatarId:
            return

        if not shardId:
            self.notify.warning('Cannot initialize teleport to shard for avatar %d, '
                'invalid shard!' % avatarId)

            return

        self.sendUpdate('requestTeleportToShardAItoUD', [avatarId, shardId, instanceType, instanceName, locationUid])

    def d_requestCrossShardDeployAItoUD(self, avatarId, sourceShardId, shardId, islandUid, shipId):
        if not avatarId or not islandUid or not shipId:
            self.notify.warning('Cannot route cross-shard deploy, '
                'invalid avatar, island, or ship!')
            return

        self.sendUpdate('requestCrossShardDeployAItoUD', [
            avatarId, sourceShardId, shardId, islandUid, shipId])

    def requestCrossShardDeployUDtoAI(self, avatarId, shardId, islandUid, shipId):
        if not avatarId or not islandUid or not shipId:
            self.notify.warning('Cannot deploy cross-shard ship, '
                'invalid avatar, island, or ship!')
            return

        if shardId != self.air.districtId:
            self.notify.warning('Cannot deploy ship for avatar %d on shard %d, '
                'request was received by district %d!' % (
                    avatarId, shardId, self.air.districtId))
            return

        def avatarArrived(avatar):
            if not avatar:
                self.notify.warning('Cannot deploy ship for avatar %d, '
                    'invalid generate!' % avatarId)
                return

            self.air.teleportMgr._handleLocalCrossShardDeploy(avatar, islandUid, shipId)

        avatar = self.air.doId2do.get(avatarId)
        if avatar:
            avatarArrived(avatar)
            return

        self.__getAvatarArrival(avatarId, avatarArrived)

    def crossShardDeployFailed(self, avatarId):
        if not avatarId:
            self.notify.warning('Cannot fail cross-shard deploy, invalid avatar!')
            return

        if avatarId not in self.air.doId2do:
            self.notify.warning('Cannot fail cross-shard deploy for avatar %d, '
                'avatar is not on this district!' % avatarId)
            return

        self.air.teleportMgr.d_teleportFailed(avatarId)

    def requestTeleportToShardUDtoAI(self, avatarId, shardId, instanceType, instanceName, locationUid):
        if not avatarId:
            return

        if not shardId:
            self.notify.warning('Cannot initialize teleport to shard for avatar %d, '
                'invalid shard!' % avatarId)

            return

        def avatarArrived(avatar):
            if not avatar:
                self.notify.warning('Cannot initialize teleport loc for avatar %d, '
                    'invalid generate!' % avatarId)

                return

            self.notify.debug('Avatar %d arrived from another district, teleporting to: '
                'instanceType=%r instanceName=%r locationUid=%r' % (avatarId, instanceType,
                instanceName, locationUid))

            # only fall back on the avatar's return location when the
            # other district did not ask for a specific location...
            self.air.teleportMgr.d_initiateTeleport(avatar, instanceType, instanceName,
                locationUid, useReturnLocation=not locationUid)

        if shardId != self.air.districtId:
            self.notify.warning('Cannot teleport avatar %d to shard %d, '
                'request was received by district %d!' % (avatarId, shardId, self.air.districtId))

            return

        avatar = self.air.doId2do.get(avatarId)
        if avatar:
            avatarArrived(avatar)
            return

        self.__getAvatarArrival(avatarId, avatarArrived)

    def __getAvatarArrival(self, avatarId, callback):
        if not avatarId:
            return

        if not callback:
            self.notify.warning('Cannot get arrival event for avatar %d, invalid callback!' % avatarId)
            return

        self.acceptOnce('generate-%d' % avatarId, callback)
        self.air.setAI(avatarId, self.air.ourChannel)
