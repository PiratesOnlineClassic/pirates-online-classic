from direct.directnotify import DirectNotifyGlobal
from otp.friends.GuildManagerUD import GuildManagerUD
from otp.otpbase import OTPGlobals
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

    def checkGuildAccess(self, avatarId, callback):
        # Free players may join a guild, but may not start or name one. The
        # client's guild page disables those buttons, here we make sure of it.
        if not config.GetBool('want-membership', False):
            callback(True)
            return

        from pirates.piratesbase import Freebooter
        if not Freebooter.FreeGuildRestrict or Freebooter.AllAccessHoliday:
            callback(True)
            return

        def handleAvatar(doId, parentId, zoneId, dclass, fields):
            access = fields.get('setAccess', (OTPGlobals.AccessUnknown,))[0]
            callback(access == OTPGlobals.AccessFull)

        # The avatar's access is a ram field, ask the avatar object:
        self.air.getObject(avatarId, handleAvatar)

    def sendSCQuest(self, questInt, msgType, taskNum):
        avatarId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(avatarId)
        if guild:
            self.sendToOnlineMembers(guild, 'recvSCQuest', [avatarId, questInt, msgType, taskNum])
