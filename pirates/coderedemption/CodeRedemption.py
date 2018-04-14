from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from otp.distributed import OtpDoGlobals
from otp.otpbase import OTPGlobals, OTPLocalizer
from pirates.piratesbase import PLocalizer


class CodeRedemption(DistributedObjectGlobal):

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)

    def redeemCode(self, code):
        if code:
            self.sendUpdate('sendCodeForRedemption', [code])

    def notifyClientCodeRedeemStatus(self, status):
        if status:
            base.chatAssistant.receiveGameMessage(PLocalizer.CodeRedemptionGood)
            return
        base.chatAssistant.receiveGameMessage(PLocalizer.CodeRedemptionBad)
