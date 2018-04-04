
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedChatManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedChatManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # online()

    def online(self, online):
        self.sendUpdate('online', [online])

    # adminChat(uint32, string)

    def adminChat(self, adminChat, todo_string_1):
        self.sendUpdate('adminChat', [adminChat, todo_string_1])

    # setAvatarLocation(uint32, uint32, uint32)

    def setAvatarLocation(self, avatarLocation, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('setAvatarLocation', [avatarLocation, todo_uint32_1, todo_uint32_2])

    # setAvatarCrew(uint32, uint32)

    def setAvatarCrew(self, avatarCrew, todo_uint32_1):
        self.sendUpdate('setAvatarCrew', [avatarCrew, todo_uint32_1])

    # setAvatarGuild(uint32, uint32)

    def setAvatarGuild(self, avatarGuild, todo_uint32_1):
        self.sendUpdate('setAvatarGuild', [avatarGuild, todo_uint32_1])

    # chatParentId(uint32) airecv clsend

    def chatParentId(self, chatParentId):
        pass

    # chatZoneId(uint32) airecv clsend

    def chatZoneId(self, chatZoneId):
        pass

    # chatFace(uint32) airecv clsend

    def chatFace(self, chatFace):
        pass

    # chatEmote(uint16) airecv clsend

    def chatEmote(self, chatEmote):
        pass

    # chatEmoteTarget(uint32) airecv clsend

    def chatEmoteTarget(self, chatEmoteTarget):
        pass

    # chatIndex(uint16) airecv clsend

    def chatIndex(self, chatIndex):
        pass

    # chatString(string) airecv clsend

    def chatString(self, chatString):
        pass

    # chatTo(string, uint8) airecv clsend

    def chatTo(self, chatTo, todo_uint8_1):
        pass

    # chatFrom(uint32, string, uint8)

    def chatFrom(self, chatFrom, todo_string_1, todo_uint8_2):
        self.sendUpdate('chatFrom', [chatFrom, todo_string_1, todo_uint8_2])

    # speedChatTo(uint16) airecv clsend

    def speedChatTo(self, speedChatTo):
        pass

    # speedChatFrom(uint32, uint16)

    def speedChatFrom(self, speedChatFrom, todo_uint16_1):
        self.sendUpdate('speedChatFrom', [speedChatFrom, todo_uint16_1])

    # speedChatCustomTo(uint16) airecv clsend

    def speedChatCustomTo(self, speedChatCustomTo):
        pass

    # speedChatCustomFrom(uint32, uint16)

    def speedChatCustomFrom(self, speedChatCustomFrom, todo_uint16_1):
        self.sendUpdate('speedChatCustomFrom', [speedChatCustomFrom, todo_uint16_1])

    # whisperTo(uint32, string) airecv clsend

    def whisperTo(self, whisperTo, todo_string_1):
        pass

    # whisperFrom(uint32, string)

    def whisperFrom(self, whisperFrom, todo_string_1):
        self.sendUpdate('whisperFrom', [whisperFrom, todo_string_1])

    # whisperSCTo(uint32, uint16) airecv clsend

    def whisperSCTo(self, whisperSCTo, todo_uint16_1):
        pass

    # whisperSCFrom(uint32, uint16)

    def whisperSCFrom(self, whisperSCFrom, todo_uint16_1):
        self.sendUpdate('whisperSCFrom', [whisperSCFrom, todo_uint16_1])

    # whisperSCCustomTo(uint32, uint16) airecv clsend

    def whisperSCCustomTo(self, whisperSCCustomTo, todo_uint16_1):
        pass

    # whisperSCCustomFrom(uint32, uint16)

    def whisperSCCustomFrom(self, whisperSCCustomFrom, todo_uint16_1):
        self.sendUpdate('whisperSCCustomFrom', [whisperSCCustomFrom, todo_uint16_1])

    # whisperSCEmoteTo(uint32, uint16) airecv clsend

    def whisperSCEmoteTo(self, whisperSCEmoteTo, todo_uint16_1):
        pass

    # whisperSCEmoteFrom(uint32, uint16)

    def whisperSCEmoteFrom(self, whisperSCEmoteFrom, todo_uint16_1):
        self.sendUpdate('whisperSCEmoteFrom', [whisperSCEmoteFrom, todo_uint16_1])

    # whisperIgnored(uint32)

    def whisperIgnored(self, whisperIgnored):
        self.sendUpdate('whisperIgnored', [whisperIgnored])

    # crewChatTo(string) airecv clsend

    def crewChatTo(self, crewChatTo):
        pass

    # crewChatFrom(uint32, string)

    def crewChatFrom(self, crewChatFrom, todo_string_1):
        self.sendUpdate('crewChatFrom', [crewChatFrom, todo_string_1])

    # guildChatTo(string) airecv clsend

    def guildChatTo(self, guildChatTo):
        pass

    # guildChatFrom(uint32, string)

    def guildChatFrom(self, guildChatFrom, todo_string_1):
        self.sendUpdate('guildChatFrom', [guildChatFrom, todo_string_1])


