from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal
from otp.distributed import OtpDoGlobals

class DistributedTravelAgentAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTravelAgentAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)

        self.sendUpdate('registerShard', [self.air.districtId])

    def requestInitLocUDtoAI(self, avatarId):
        if not avatarId:
            return

        if avatarId in self.air.doId2do:
            return

        def avatarArrived(avatar):
            if not avatar:
                self.notify.warning('Cannot initialize teleport loc for avatar %d, invalid generate!' % (
                    avatarId))

                return

            avatar.d_relayTeleportLoc(self.air.districtId, self.air.distributedDistrict.zoneId,
                self.air.teleportMgr.doId)

        self.__getAvatarArrival(avatarId, avatarArrived)

    def d_requestTeleportToShardAItoUD(self, avatarId, shardId, instanceType, instanceName, locationUid):
        if not avatarId:
            return

        if not shardId:
            self.notify.warning('Cannot initialize teleport to shard for avatar %d, invalid shard!' % (
                avatarId))

            return

        self.sendUpdate('requestTeleportToShardAItoUD', [avatarId, shardId, instanceType,
            instanceName, locationUid])

    def requestTeleportToShardUDtoAI(self, avatarId, shardId, instanceType, instanceName, locationUid):
        if not avatarId:
            return

        if not shardId:
            self.notify.warning('Cannot initialize teleport to shard for avatar %d, invalid shard!' % (
                avatarId))

            return

        def avatarArrived(avatar):
            if not avatar:
                self.notify.warning('Cannot initialize teleport loc for avatar %d, invalid generate!' % (
                    avatarId))

                return

            # since the avatar was deleted when we moved their AI channel,
            # we need to re-initiate their inventory on our AI channel so they
            # will have their inventory on our AI...
            self.air.inventoryManager.initiateInventory(avatar.doId)

            # tell the teleport manager to send the avatar to the requested location
            # this is the location in which the avatar was last located at before they
            # tried to move to another AI...
            self.air.teleportMgr.d_initiateTeleport(avatar, instanceType, instanceName, locationUid)

        self.__getAvatarArrival(avatarId, avatarArrived)

    def __getAvatarArrival(self, avatarId, callback):
        if not avatarId:
            return

        if not callback:
            self.notify.warning('Cannot get arrival event for avatar %d, invalid callback!' % (
                avatarId))

            return

        self.acceptOnce('generate-%d' % avatarId, callback)
        self.air.setAI(avatarId, self.air.ourChannel)
