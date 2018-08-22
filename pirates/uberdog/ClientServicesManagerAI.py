from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI


class ClientServicesManagerAI(DistributedObjectGlobalAI):

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

    def populateAvatar(self, avId, dnaString):
        avatar = self.air.doId2do.get(avId)

        if not avatar:
            return

        avatar.b_setDNAString(dnaString)
        self.sendUpdateToAvatarId(avId, 'populateAvatarResp', [])
