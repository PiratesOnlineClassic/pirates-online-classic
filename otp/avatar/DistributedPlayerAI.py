from otp.avatar.DistributedAvatarAI import DistributedAvatarAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPlayerAI(DistributedAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerAI')

    def __init__(self, air):
        DistributedAvatarAI.__init__(self, air)
