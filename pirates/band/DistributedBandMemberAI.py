
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBandMemberAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBandMemberAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.avatarId = 0
        self.name = ''
        self.hp = 0
        self.maxHp = 0
        self.bandId = [0, 0]
        self.isManager = 0
        self.shipInfo = [0, '', 0, []]
        self.shipHasSpace = False


    # setAvatarId(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAvatarId(self, avatarId):
        self.avatarId = avatarId

    def d_setAvatarId(self, avatarId):
        self.sendUpdate('setAvatarId', [avatarId])

    def b_setAvatarId(self, avatarId):
        self.setAvatarId(avatarId)
        self.d_setAvatarId(avatarId)

    def getAvatarId(self):
        return self.avatarId

    # setName(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    # setHp(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setHp(self, hp):
        self.hp = hp

    def d_setHp(self, hp):
        self.sendUpdate('setHp', [hp])

    def b_setHp(self, hp):
        self.setHp(hp)
        self.d_setHp(hp)

    def getHp(self):
        return self.hp

    # setMaxHp(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def d_setMaxHp(self, maxHp):
        self.sendUpdate('setMaxHp', [maxHp])

    def b_setMaxHp(self, maxHp):
        self.setMaxHp(maxHp)
        self.d_setMaxHp(maxHp)

    def getMaxHp(self):
        return self.maxHp

    # setBandId(uint32, uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setBandId(self, bandId, todo_uint32_1):
        self.bandId = bandId

    def d_setBandId(self, bandId, todo_uint32_1):
        self.sendUpdate('setBandId', [bandId, todo_uint32_1])

    def b_setBandId(self, bandId, todo_uint32_1):
        self.setBandId(bandId, todo_uint32_1)
        self.d_setBandId(bandId, todo_uint32_1)

    def getBandId(self):
        return self.bandId

    # setIsManager(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setIsManager(self, isManager):
        self.isManager = isManager

    def d_setIsManager(self, isManager):
        self.sendUpdate('setIsManager', [isManager])

    def b_setIsManager(self, isManager):
        self.setIsManager(isManager)
        self.d_setIsManager(isManager)

    def getIsManager(self):
        return self.isManager

    # setShipInfo(uint32, string, uint8, MastInfo []) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setShipInfo(self, shipInfo, todo_string_1, todo_uint8_2, todo_MastInfo_3):
        self.shipInfo = shipInfo

    def d_setShipInfo(self, shipInfo, todo_string_1, todo_uint8_2, todo_MastInfo_3):
        self.sendUpdate('setShipInfo', [shipInfo, todo_string_1, todo_uint8_2, todo_MastInfo_3])

    def b_setShipInfo(self, shipInfo, todo_string_1, todo_uint8_2, todo_MastInfo_3):
        self.setShipInfo(shipInfo, todo_string_1, todo_uint8_2, todo_MastInfo_3)
        self.d_setShipInfo(shipInfo, todo_string_1, todo_uint8_2, todo_MastInfo_3)

    def getShipInfo(self):
        return self.shipInfo

    # setShipHasSpace(bool) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setShipHasSpace(self, shipHasSpace):
        self.shipHasSpace = shipHasSpace

    def d_setShipHasSpace(self, shipHasSpace):
        self.sendUpdate('setShipHasSpace', [shipHasSpace])

    def b_setShipHasSpace(self, shipHasSpace):
        self.setShipHasSpace(shipHasSpace)
        self.d_setShipHasSpace(shipHasSpace)

    def getShipHasSpace(self):
        return self.shipHasSpace

    # setMessage(uint32, string) broadcast

    def setMessage(self, message, todo_string_1):
        self.sendUpdate('setMessage', [message, todo_string_1])

    # setShipDeployMessage(uint32, string, string) broadcast

    def setShipDeployMessage(self, shipDeployMessage, todo_string_1, todo_string_2):
        self.sendUpdate('setShipDeployMessage', [shipDeployMessage, todo_string_1, todo_string_2])

    # setChat(string, uint8, uint32) broadcast ownsend

    def setChat(self, chat, todo_uint8_1, todo_uint32_2):
        self.sendUpdate('setChat', [chat, todo_uint8_1, todo_uint32_2])

    # setWLChat(string, uint8, uint32) broadcast ownsend

    def setWLChat(self, wLChat, todo_uint8_1, todo_uint32_2):
        self.sendUpdate('setWLChat', [wLChat, todo_uint8_1, todo_uint32_2])

    # setSpeedChat(uint32, uint16) broadcast ownsend

    def setSpeedChat(self, speedChat, todo_uint16_1):
        self.sendUpdate('setSpeedChat', [speedChat, todo_uint16_1])

    # setSCQuestChat(uint32, uint16, uint8, uint8) broadcast ownsend

    def setSCQuestChat(self, sCQuestChat, todo_uint16_1, todo_uint8_2, todo_uint8_3):
        self.sendUpdate('setSCQuestChat', [sCQuestChat, todo_uint16_1, todo_uint8_2, todo_uint8_3])

    # teleportQuery(uint32, uint32, uint32) clsend ownrecv

    # teleportResponse(uint32, int8, uint32, uint32, uint32) clsend ownrecv


