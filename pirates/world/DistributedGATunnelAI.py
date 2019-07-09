from direct.directnotify import DirectNotifyGlobal

from pirates.world.DistributedGAConnectorAI import DistributedGAConnectorAI


class DistributedGATunnelAI(DistributedGAConnectorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGATunnelAI')

    def __init__(self, air):
        DistributedGAConnectorAI.__init__(self, air)

    def sendLeaveTunnelDone(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if not self.air.worldGridManager.hasInterestHandleByZoneId(self.getParentObj(), avatar, self.zoneId):
            self.notify.warning('Cannot handle leave tunnel done for avatar: %d, '
                'avatar does not have an interest handle for object with doId: %d!' % (avatar.doId, self.doId))

            return

        messenger.send(avatar.uniqueName('leave-tunnel-done'))
