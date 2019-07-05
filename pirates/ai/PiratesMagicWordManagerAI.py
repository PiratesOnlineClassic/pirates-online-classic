from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from otp.ai.MagicWordManagerAI import MagicWordManagerAI

import time

class PiratesMagicWordManagerAI(MagicWordManagerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesMagicWordManagerAI')

    def __init__(self, air):
        MagicWordManagerAI.__init__(self, air)

    def requestServerTime(self):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Failed to server time request for non-existant avatar!')

            self.air.logPotentialHacker(
                message='Received requestServerTime from non-existant avatar',
                targetAvId=avatarId)
            return

        sinceEpoch = time.time()
        self.d_recvServerTime(avatar.doId, sinceEpoch)

    def d_recvServerTime(self, avatarId, sinceEpoch):
        self.sendUpdateToAvatarId(avatarId, 'recvServerTime', [sinceEpoch])

