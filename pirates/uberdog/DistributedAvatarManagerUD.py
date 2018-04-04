
from otp.uberdog.OtpAvatarManagerUD import OtpAvatarManagerUD
from direct.directnotify import DirectNotifyGlobal

class DistributedAvatarManagerUD(OtpAvatarManagerUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAvatarManagerUD')

    def __init__(self, air):
        OtpAvatarManagerUD.__init__(self, air)




    # populateAvatarResponse(bool)

    def populateAvatarResponse(self, populateAvatarResponse):
        self.sendUpdate('populateAvatarResponse', [populateAvatarResponse])


    # patternNameResponse(bool)

    def patternNameResponse(self, patternNameResponse):
        self.sendUpdate('patternNameResponse', [patternNameResponse])


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


