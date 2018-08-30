from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal


class CodeRedemptionUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('CodeRedemptionUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def sendCodeForRedemption(self, code):
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return

        self.d_notifyClientCodeRedeemStatus(avatarId, False)

    def d_notifyClientCodeRedeemStatus(self, avatarId, status):
        self.sendUpdateToAvatarId(avatarId, 'notifyClientCodeRedeemStatus', [status])
