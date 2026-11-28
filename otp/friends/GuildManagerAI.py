from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class GuildManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('GuildManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def d_recvAvatarOnline(self, avatarId, avatarName, bandManagerId, bandId):
        self.sendUpdate('recvAvatarOnline', [avatarId, avatarName, bandManagerId, bandId])

    def d_sendAvatarBandId(self, avatarId, bandManagerId, bandId):
        self.sendUpdate('sendAvatarBandId', [avatarId, bandManagerId, bandId])

    def avatarOnline(self, av):
        self.d_recvAvatarOnline(av.doId, av.getName(), 0, 0)
