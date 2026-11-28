from direct.directnotify import DirectNotifyGlobal
from otp.friends.GuildManagerUD import GuildManagerUD
from pirates.piratesbase import PLocalizer

class PCGuildManagerUD(GuildManagerUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCGuildManagerUD')

    def __init__(self, air):
        GuildManagerUD.__init__(self, air)

    def getAvatarDClass(self):
        return self.air.dclassesByName['DistributedPlayerPirateUD']

    def getGuildDisplayName(self, guildId, guild):
        if guild['name']:
            return guild['name']

        return PLocalizer.GuildDefaultName % guildId

    def sendSCQuest(self, questInt, msgType, taskNum):
        avatarId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(avatarId)
        if guild:
            self.sendToOnlineMembers(guild, 'recvSCQuest', [avatarId, questInt, msgType, taskNum])
