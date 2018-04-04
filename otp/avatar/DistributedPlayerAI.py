
from otp.avatar.DistributedAvatarAI import DistributedAvatarAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPlayerAI(DistributedAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerAI')

    def __init__(self, air):
        DistributedAvatarAI.__init__(self, air)
        self.accountName = ''
        self.friendsList = 0
        self.previousAccess = 0
        self.access = 0


    # arrivedOnDistrict(uint32) ownrecv ram

    # setAccountName(string) required ownrecv db
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAccountName(self, accountName):
        self.accountName = accountName

    def d_setAccountName(self, accountName):
        self.sendUpdate('setAccountName', [accountName])

    def b_setAccountName(self, accountName):
        self.setAccountName(accountName)
        self.d_setAccountName(accountName)

    def getAccountName(self):
        return self.accountName

    # setChat(string, uint8, uint32) broadcast ownsend

    def setChat(self, chat, todo_uint8_1, todo_uint32_2):
        self.sendUpdate('setChat', [chat, todo_uint8_1, todo_uint32_2])

    # setWLChat(string, uint8, uint32) broadcast ownsend

    def setWLChat(self, wLChat, todo_uint8_1, todo_uint32_2):
        self.sendUpdate('setWLChat', [wLChat, todo_uint8_1, todo_uint32_2])

    # setWhisperFrom(uint32, string, uint32) ownrecv clsend

    # setWhisperWLFrom(uint32, string, uint32) ownrecv clsend

    # setWhisperSCFrom(uint32, uint16) ownrecv clsend

    # setWhisperSCCustomFrom(uint32, uint16) ownrecv clsend

    # setWhisperSCEmoteFrom(uint32, uint16) ownrecv clsend

    # setSystemMessage(uint32, string) ownrecv

    # setCommonChatFlags(uint8) broadcast ownrecv ram

    def setCommonChatFlags(self, commonChatFlags):
        self.sendUpdate('setCommonChatFlags', [commonChatFlags])

    # setSC(uint16) broadcast ownsend airecv

    def setSC(self, sC):
        pass

    # setSCCustom(uint16) broadcast ownsend airecv

    def setSCCustom(self, sCCustom):
        pass

    # setFriendsList(uint32uint8array) ownrecv required db airecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setFriendsList(self, friendsList):
        self.friendsList = friendsList

    def d_setFriendsList(self, friendsList):
        self.sendUpdate('setFriendsList', [friendsList])

    def b_setFriendsList(self, friendsList):
        self.setFriendsList(friendsList)
        self.d_setFriendsList(friendsList)

    def getFriendsList(self):
        return self.friendsList

    # setDISLname(string) broadcast ownrecv ram

    def setDISLname(self, dISLname):
        self.sendUpdate('setDISLname', [dISLname])

    # setDISLid(uint32) broadcast ownrecv ram db

    def setDISLid(self, dISLid):
        self.sendUpdate('setDISLid', [dISLid])

    # OwningAccount(uint32)

    def OwningAccount(self, OwningAccount):
        self.sendUpdate('OwningAccount', [OwningAccount])

    # WishName(string) db ram

    # WishNameState(string) db ram

    # setPreviousAccess(uint8) required db airecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setPreviousAccess(self, previousAccess):
        self.previousAccess = previousAccess

    def d_setPreviousAccess(self, previousAccess):
        self.sendUpdate('setPreviousAccess', [previousAccess])

    def b_setPreviousAccess(self, previousAccess):
        self.setPreviousAccess(previousAccess)
        self.d_setPreviousAccess(previousAccess)

    def getPreviousAccess(self):
        return self.previousAccess

    # setAccess(uint8) broadcast ownrecv required ram airecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAccess(self, access):
        self.access = access

    def d_setAccess(self, access):
        self.sendUpdate('setAccess', [access])

    def b_setAccess(self, access):
        self.setAccess(access)
        self.d_setAccess(access)

    def getAccess(self):
        return self.access


