from direct.directnotify import DirectNotifyGlobal
from otp.friends.GuildManagerAI import GuildManagerAI

class PCGuildManagerAI(GuildManagerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCGuildManagerAI')

    def __init__(self, air):
        GuildManagerAI.__init__(self, air)

    def avatarOnline(self, av):
        # Our guild mates see which crew we're in:
        bandManagerId, bandId = av.getBandId()
        self.d_recvAvatarOnline(av.doId, av.getName(), bandManagerId, bandId)
