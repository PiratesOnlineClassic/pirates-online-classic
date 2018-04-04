
from otp.uberdog.OtpAvatarManagerAI import OtpAvatarManagerAI
from direct.directnotify import DirectNotifyGlobal

class DistributedAvatarManagerAI(OtpAvatarManagerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAvatarManagerAI')

    def __init__(self, air):
        OtpAvatarManagerAI.__init__(self, air)


    # requestCreateAvatar(uint32, uint32) airecv clsend

    def requestCreateAvatar(self, requestCreateAvatar, todo_uint32_1):
        pass

    # requestPopulateAvatar(uint32, uint32, HumanDNA, bool, uint16, uint16, uint16, uint16) airecv clsend

    def requestPopulateAvatar(self, requestPopulateAvatar, todo_uint32_1, todo_HumanDNA_2, todo_bool_3, todo_uint16_4, todo_uint16_5, todo_uint16_6, todo_uint16_7):
        pass

    # populateAvatarResponse(bool)

    def populateAvatarResponse(self, populateAvatarResponse):
        self.sendUpdate('populateAvatarResponse', [populateAvatarResponse])

    # requestPatternName(uint32, uint32, uint16, uint16, uint16, uint16) airecv clsend

    def requestPatternName(self, requestPatternName, todo_uint32_1, todo_uint16_2, todo_uint16_3, todo_uint16_4, todo_uint16_5):
        pass

    # patternNameResponse(bool)

    def patternNameResponse(self, patternNameResponse):
        self.sendUpdate('patternNameResponse', [patternNameResponse])

    # requestFinalize(uint32, uint32) airecv clsend

    def requestFinalize(self, requestFinalize, todo_uint32_1):
        pass

    # sendAvIdList(uint32 [])

    def sendAvIdList(self, sendAvIdList):
        self.sendUpdate('sendAvIdList', [sendAvIdList])

    # avatarListResponse(AccountInfo [], uint16)

    def avatarListResponse(self, avatarListResponse, todo_uint16_1):
        self.sendUpdate('avatarListResponse', [avatarListResponse, todo_uint16_1])

    # requestAwardableAvatars(uint32, uint32)

    def requestAwardableAvatars(self, requestAwardableAvatars, todo_uint32_1):
        self.sendUpdate('requestAwardableAvatars', [requestAwardableAvatars, todo_uint32_1])

    # requestAvatarGender(uint32, uint32)

    def requestAvatarGender(self, requestAvatarGender, todo_uint32_1):
        self.sendUpdate('requestAvatarGender', [requestAvatarGender, todo_uint32_1])


