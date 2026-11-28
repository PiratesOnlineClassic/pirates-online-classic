from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal


class DistributedChatManagerUD(DistributedObjectGlobalUD):
    """
    Global chat router. The AIs keep the chat manager informed of where every
    avatar is and which crew and guild it belongs to; client chat sent to the
    chat manager is then relayed to the avatars it is meant for.

    Pirates doesn't use it: the client never calls any of the chat manager's
    send methods, its *From handlers do nothing and nothing listens for the
    adminChat event. Open chat and whispers are checked and relayed by
    DistributedPlayerAI, crew, guild and team chat by their own managers, so
    the districts don't report avatars here and the object is left dormant.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedChatManagerUD')

    MaxChatLength = 255

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.avatarLocations = {}
        self.avatarCrews = {}
        self.avatarGuilds = {}

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.notify.info('ChatManager going online')

    def delete(self):
        self.avatarLocations = {}
        self.avatarCrews = {}
        self.avatarGuilds = {}
        DistributedObjectGlobalUD.delete(self)

    def online(self):
        pass

    # AI requests:

    def setAvatarLocation(self, avatarId, parentId, zoneId):
        if not parentId and not zoneId:
            self.removeAvatar(avatarId)
            return

        self.avatarLocations[avatarId] = (parentId, zoneId)

    def setAvatarCrew(self, avatarId, crewId):
        if crewId:
            self.avatarCrews[avatarId] = crewId
        else:
            self.avatarCrews.pop(avatarId, None)

    def setAvatarGuild(self, avatarId, guildId):
        if guildId:
            self.avatarGuilds[avatarId] = guildId
        else:
            self.avatarGuilds.pop(avatarId, None)

    def removeAvatar(self, avatarId):
        self.avatarLocations.pop(avatarId, None)
        self.avatarCrews.pop(avatarId, None)
        self.avatarGuilds.pop(avatarId, None)

    # Routing helpers:

    def isAvatarOnline(self, avatarId):
        return avatarId in self.avatarLocations

    def getAvatarsAtLocation(self, location):
        return [avId for avId, loc in list(self.avatarLocations.items()) if loc == location]

    def getAvatarsInCrew(self, crewId):
        return [avId for avId, cId in list(self.avatarCrews.items()) if cId == crewId]

    def getAvatarsInGuild(self, guildId):
        return [avId for avId, gId in list(self.avatarGuilds.items()) if gId == guildId]

    def getSender(self, fieldName):
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            self.notify.warning('Received %s from a client without an avatar!' % fieldName)
            return 0

        if not self.isAvatarOnline(avatarId):
            self.notify.debug('Received %s from avatar %d with no known location.' % (fieldName, avatarId))
            return 0

        return avatarId

    def cleanMessage(self, avatarId, message):
        message = message.strip()
        if not message:
            return None

        if len(message) > self.MaxChatLength:
            self.air.writeServerEvent('suspicious', avId=avatarId, issue='Chat message too long', length=len(message))
            return None

        return message

    def sendToLocation(self, avatarId, fieldName, args):
        location = self.avatarLocations.get(avatarId)
        if location is None:
            return

        for targetId in self.getAvatarsAtLocation(location):
            self.sendUpdateToAvatarId(targetId, fieldName, args)

    # Client requests:

    def chatTo(self, message, chatFlags):
        avatarId = self.getSender('chatTo')
        if not avatarId:
            return

        message = self.cleanMessage(avatarId, message)
        if message is None:
            return

        self.air.writeServerEvent('chat-said', avId=avatarId, message=message)
        self.sendToLocation(avatarId, 'chatFrom', [avatarId, message, chatFlags])

    def speedChatTo(self, msgIndex):
        avatarId = self.getSender('speedChatTo')
        if not avatarId:
            return

        self.sendToLocation(avatarId, 'speedChatFrom', [avatarId, msgIndex])

    def speedChatCustomTo(self, msgIndex):
        avatarId = self.getSender('speedChatCustomTo')
        if not avatarId:
            return

        self.sendToLocation(avatarId, 'speedChatCustomFrom', [avatarId, msgIndex])

    def whisperTo(self, toId, message):
        avatarId = self.getSender('whisperTo')
        if not avatarId:
            return

        message = self.cleanMessage(avatarId, message)
        if message is None:
            return

        if not self.isAvatarOnline(toId):
            return

        self.air.writeServerEvent('whisper-said', avId=avatarId, toId=toId, message=message)
        self.sendUpdateToAvatarId(toId, 'whisperFrom', [avatarId, message])

    def whisperSCTo(self, toId, msgIndex):
        avatarId = self.getSender('whisperSCTo')
        if not avatarId or not self.isAvatarOnline(toId):
            return

        self.sendUpdateToAvatarId(toId, 'whisperSCFrom', [avatarId, msgIndex])

    def whisperSCCustomTo(self, toId, msgIndex):
        avatarId = self.getSender('whisperSCCustomTo')
        if not avatarId or not self.isAvatarOnline(toId):
            return

        self.sendUpdateToAvatarId(toId, 'whisperSCCustomFrom', [avatarId, msgIndex])

    def whisperSCEmoteTo(self, toId, emoteId):
        avatarId = self.getSender('whisperSCEmoteTo')
        if not avatarId or not self.isAvatarOnline(toId):
            return

        self.sendUpdateToAvatarId(toId, 'whisperSCEmoteFrom', [avatarId, emoteId])

    def crewChatTo(self, message):
        avatarId = self.getSender('crewChatTo')
        if not avatarId:
            return

        crewId = self.avatarCrews.get(avatarId)
        if not crewId:
            return

        message = self.cleanMessage(avatarId, message)
        if message is None:
            return

        self.air.writeServerEvent('crew-chat-said', avId=avatarId, crewId=crewId, message=message)
        for targetId in self.getAvatarsInCrew(crewId):
            self.sendUpdateToAvatarId(targetId, 'crewChatFrom', [avatarId, message])

    def guildChatTo(self, message):
        avatarId = self.getSender('guildChatTo')
        if not avatarId:
            return

        guildId = self.avatarGuilds.get(avatarId)
        if not guildId:
            return

        message = self.cleanMessage(avatarId, message)
        if message is None:
            return

        self.air.writeServerEvent('guild-chat-said', avId=avatarId, guildId=guildId, message=message)
        for targetId in self.getAvatarsInGuild(guildId):
            self.sendUpdateToAvatarId(targetId, 'guildChatFrom', [avatarId, message])

    # Server senders:

    def d_adminChat(self, avatarId, aboutId, message):
        self.sendUpdateToAvatarId(avatarId, 'adminChat', [aboutId, message])

    def sendAdminChatToAll(self, aboutId, message):
        for avatarId in list(self.avatarLocations.keys()):
            self.d_adminChat(avatarId, aboutId, message)

    def d_whisperIgnored(self, avatarId, fromId):
        self.sendUpdateToAvatarId(avatarId, 'whisperIgnored', [fromId])
