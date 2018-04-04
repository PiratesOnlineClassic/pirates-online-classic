from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedTravelAgentUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTravelAgentUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def requestInitLocUD(self, unused, shardId):
        avatarId = self.air.getAvatarIdFromSender()

        if not avatarId:
            self.notify.warning('Cannot init UD loc, unknown avatar %d!' % avatarId)
            return

        if not shardId:
            self.sendUpdate('requestInitLocUDtoAI', [avatarId])
        else:
            self.sendUpdateToChannel(shardId, 'requestInitLocUDtoAI', [avatarId])
