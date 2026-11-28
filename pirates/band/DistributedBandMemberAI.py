from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from otp.chat import ChatFilter
from otp.chat.ChatRelayAI import ChatRelayAI

from pirates.chat import PChatFilter


class DistributedBandMemberAI(DistributedObjectAI, ChatRelayAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBandMemberAI')

    # Crew chat is sent on the crew member's own band member object, owned by
    # their client, and we relay it to the band zone every crew member has
    # interest in. Shared by every crew on this AI.
    chatFlood = ChatFilter.ChatFlood()

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.avatarId = 0
        self.name = ''
        self.hp = 0
        self.maxHp = 0
        self.bandManagerId = 0
        self.bandId = 0
        self.isManager = 0
        self.shipId = 0
        self.shipName = ''
        self.shipClass = 0
        self.mastInfo = []
        self.shipHasSpace = False

    def delete(self):
        self.chatFlood.clear(self.avatarId)
        DistributedObjectAI.delete(self)

    def setAvatarId(self, avatarId):
        self.avatarId = avatarId

    def getAvatarId(self):
        return self.avatarId

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def setHp(self, hp):
        self.hp = max(0, hp)

    def d_setHp(self, hp):
        self.sendUpdate('setHp', [max(0, hp)])

    def b_setHp(self, hp):
        self.setHp(hp)
        self.d_setHp(hp)

    def getHp(self):
        return self.hp

    def setMaxHp(self, maxHp):
        self.maxHp = max(0, maxHp)

    def d_setMaxHp(self, maxHp):
        self.sendUpdate('setMaxHp', [max(0, maxHp)])

    def b_setMaxHp(self, maxHp):
        self.setMaxHp(maxHp)
        self.d_setMaxHp(maxHp)

    def getMaxHp(self):
        return self.maxHp

    def setBandId(self, bandManagerId, bandId):
        self.bandManagerId = bandManagerId
        self.bandId = bandId

    def getBandId(self):
        return (self.bandManagerId, self.bandId)

    def setIsManager(self, isManager):
        self.isManager = isManager

    def d_setIsManager(self, isManager):
        self.sendUpdate('setIsManager', [isManager])

    def b_setIsManager(self, isManager):
        self.setIsManager(isManager)
        self.d_setIsManager(isManager)

    def getIsManager(self):
        return self.isManager

    def setShipInfo(self, shipId, shipName, shipClass, mastInfo):
        self.shipId = shipId
        self.shipName = shipName
        self.shipClass = shipClass
        self.mastInfo = mastInfo

    def d_setShipInfo(self, shipId, shipName, shipClass, mastInfo):
        self.sendUpdate('setShipInfo', [shipId, shipName, shipClass, mastInfo])

    def b_setShipInfo(self, shipId, shipName, shipClass, mastInfo):
        self.setShipInfo(shipId, shipName, shipClass, mastInfo)
        self.d_setShipInfo(shipId, shipName, shipClass, mastInfo)

    def getShipInfo(self):
        return (self.shipId, self.shipName, self.shipClass, self.mastInfo)

    def setShipHasSpace(self, shipHasSpace):
        self.shipHasSpace = shipHasSpace

    def d_setShipHasSpace(self, shipHasSpace):
        self.sendUpdate('setShipHasSpace', [shipHasSpace])

    def b_setShipHasSpace(self, shipHasSpace):
        self.setShipHasSpace(shipHasSpace)
        self.d_setShipHasSpace(shipHasSpace)

    def getShipHasSpace(self):
        return self.shipHasSpace

    def d_setMessage(self, fromAvatarId, message):
        self.sendUpdate('setMessage', [fromAvatarId, message])

    def d_setShipDeployMessage(self, fromAvatarId, shipName, locationName):
        self.sendUpdate('setShipDeployMessage', [fromAvatarId, shipName, locationName])

    # Crew chat:

    def _getChatSender(self, fieldName, senderId=None):
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId or avatarId != self.avatarId:
            self.chatViolation('%s sent on the band member of %d' % (fieldName, self.avatarId))
            return 0

        if senderId is not None and senderId != avatarId:
            self.chatViolation('%s claiming to be from %d' % (fieldName, senderId))
            return 0

        return avatarId

    def d_setChat(self, chatString, chatFlags, senderChannel=None):
        self.sendUpdateToLocation('setChat', [chatString, chatFlags, 0], senderChannel)

    def setChat(self, chatString, chatFlags, DISLid):
        avatarId = self._getChatSender('setChat')
        if not avatarId:
            return

        message = self._cleanTypedChat(avatarId, 'setChat', chatString)
        if message is None:
            return

        self.air.writeServerEvent('crew-chat-said', avId=avatarId, bandId=self.bandId, message=message)
        self.d_setChat(message, ChatFilter.cleanChatFlags(chatFlags), self.air.getMsgSender())

    def d_setWLChat(self, chatString, chatFlags, senderChannel=None):
        self.sendUpdateToLocation('setWLChat', [chatString, chatFlags, 0], senderChannel)

    def setWLChat(self, chatString, chatFlags, DISLid):
        avatarId = self._getChatSender('setWLChat')
        if not avatarId:
            return

        message = self._cleanTypedChat(avatarId, 'setWLChat', chatString)
        if message is None:
            return

        message = ChatFilter.filterWhiteList(message)
        self.air.writeServerEvent('crew-chat-said-wl', avId=avatarId, bandId=self.bandId, message=message)
        self.d_setWLChat(message, ChatFilter.cleanChatFlags(chatFlags), self.air.getMsgSender())

    def d_setSpeedChat(self, senderId, msgIndex, senderChannel=None):
        self.sendUpdateToLocation('setSpeedChat', [senderId, msgIndex], senderChannel)

    def setSpeedChat(self, senderId, msgIndex):
        avatarId = self._getChatSender('setSpeedChat', senderId)
        if not avatarId:
            return

        # The client's crew SpeedChat sends a custom phrase's index on this
        # field too, which the crew can't decode, so it's dropped rather than
        # treated as a hacked client.
        if not ChatFilter.isValidSpeedChat(msgIndex) or self._isFlooding(avatarId):
            return

        self.d_setSpeedChat(avatarId, msgIndex, self.air.getMsgSender())

    def d_setSCQuestChat(self, senderId, questInt, msgType, taskNum, senderChannel=None):
        self.sendUpdateToLocation('setSCQuestChat', [senderId, questInt, msgType, taskNum], senderChannel)

    def setSCQuestChat(self, senderId, questInt, msgType, taskNum):
        avatarId = self._getChatSender('setSCQuestChat', senderId)
        if not avatarId:
            return

        if not PChatFilter.isValidSpeedChatQuest(questInt, msgType, taskNum):
            self.chatViolation('invalid crew SpeedChat quest message (%d, %d, %d)' % (
                questInt, msgType, taskNum), eject=True)
            return

        if self._isFlooding(avatarId):
            return

        self.d_setSCQuestChat(avatarId, questInt, msgType, taskNum, self.air.getMsgSender())
