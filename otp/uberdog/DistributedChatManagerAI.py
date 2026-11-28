from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal


class DistributedChatManagerAI(DistributedObjectGlobalAI):
    """
    AI side of the global chat manager. The AI is the authority on where an
    avatar is and which crew and guild it is in, so it reports those to the
    UberDOG chat manager which uses them to route chat.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedChatManagerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

    def online(self):
        pass

    def d_setAvatarLocation(self, avatarId, parentId, zoneId):
        self.sendUpdate('setAvatarLocation', [avatarId, parentId, zoneId])

    def d_setAvatarCrew(self, avatarId, crewId):
        self.sendUpdate('setAvatarCrew', [avatarId, crewId])

    def d_setAvatarGuild(self, avatarId, guildId):
        self.sendUpdate('setAvatarGuild', [avatarId, guildId])

    def avatarOffline(self, avatarId):
        # A location of 0, 0 tells the chat manager the avatar has left.
        self.d_setAvatarLocation(avatarId, 0, 0)

    def d_adminChat(self, avatarId, aboutId, message):
        self.sendUpdateToAvatarId(avatarId, 'adminChat', [aboutId, message])
