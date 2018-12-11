from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.distributed import OtpDoGlobals
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PLocalizer

class CodeRedemption(DistributedObjectGlobal):
    
    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)

    def redeemCode(self, code):
        if code:
            userName = ''
            self.sendUpdate('sendCodeForRedemption', [code, userName])

    def notifyClientCodeRedeemStatus(self, status):
        if status:
            base.chatAssistant.receiveGameMessage(PLocalizer.CodeRedemptionGood)
        else:
            base.chatAssistant.receiveGameMessage(PLocalizer.CodeRedemptionBad)

