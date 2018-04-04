
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class DistributedChatManagerUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedChatManagerUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)


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









    # chatFrom(uint32, string, uint8)

    def chatFrom(self, chatFrom, todo_string_1, todo_uint8_2):
        self.sendUpdate('chatFrom', [chatFrom, todo_string_1, todo_uint8_2])


    # speedChatFrom(uint32, uint16)

    def speedChatFrom(self, speedChatFrom, todo_uint16_1):
        self.sendUpdate('speedChatFrom', [speedChatFrom, todo_uint16_1])


    # speedChatCustomFrom(uint32, uint16)

    def speedChatCustomFrom(self, speedChatCustomFrom, todo_uint16_1):
        self.sendUpdate('speedChatCustomFrom', [speedChatCustomFrom, todo_uint16_1])


    # whisperFrom(uint32, string)

    def whisperFrom(self, whisperFrom, todo_string_1):
        self.sendUpdate('whisperFrom', [whisperFrom, todo_string_1])


    # whisperSCFrom(uint32, uint16)

    def whisperSCFrom(self, whisperSCFrom, todo_uint16_1):
        self.sendUpdate('whisperSCFrom', [whisperSCFrom, todo_uint16_1])


    # whisperSCCustomFrom(uint32, uint16)

    def whisperSCCustomFrom(self, whisperSCCustomFrom, todo_uint16_1):
        self.sendUpdate('whisperSCCustomFrom', [whisperSCCustomFrom, todo_uint16_1])


    # whisperSCEmoteFrom(uint32, uint16)

    def whisperSCEmoteFrom(self, whisperSCEmoteFrom, todo_uint16_1):
        self.sendUpdate('whisperSCEmoteFrom', [whisperSCEmoteFrom, todo_uint16_1])

    # whisperIgnored(uint32)

    def whisperIgnored(self, whisperIgnored):
        self.sendUpdate('whisperIgnored', [whisperIgnored])


    # crewChatFrom(uint32, string)

    def crewChatFrom(self, crewChatFrom, todo_string_1):
        self.sendUpdate('crewChatFrom', [crewChatFrom, todo_string_1])


    # guildChatFrom(uint32, string)

    def guildChatFrom(self, guildChatFrom, todo_string_1):
        self.sendUpdate('guildChatFrom', [guildChatFrom, todo_string_1])


