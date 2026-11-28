from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class GuildManagerAI(DistributedObjectAI):
    """
    District side handle on the guild manager UberDOG. The district does not
    keep any guild state of its own, it simply tells the UberDOG when one of
    its avatars has arrived so that the UberDOG can push that avatar's guild
    status and let the rest of the guild know they are online.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('GuildManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def d_recvAvatarOnline(self, avatarId, avatarName, bandManagerId, bandId):
        self.sendUpdate('recvAvatarOnline', [avatarId, avatarName, bandManagerId, bandId])

    def d_avatarOffline(self, avatarId):
        self.sendUpdate('avatarOffline', [avatarId])

    def d_sendAvatarBandId(self, avatarId, bandManagerId, bandId):
        self.sendUpdate('sendAvatarBandId', [avatarId, bandManagerId, bandId])

    def avatarOnline(self, av):
        self.d_recvAvatarOnline(av.doId, av.getName(), 0, 0)
