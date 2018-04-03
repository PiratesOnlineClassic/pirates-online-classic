# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.coderedemption.CodeRedemption
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.distributed import OtpDoGlobals
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PLocalizer

class CodeRedemption(DistributedObjectGlobal):
    __module__ = __name__

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)

    def redeemCode(self, code):
        if code:
            self.sendUpdate('sendCodeForRedemption', [code])

    def notifyClientCodeRedeemStatus(self, status):
        if status:
            base.chatAssistant.receiveGameMessage(PLocalizer.CodeRedemptionGood)
        else:
            base.chatAssistant.receiveGameMessage(PLocalizer.CodeRedemptionBad)
# okay decompiling .\pirates\coderedemption\CodeRedemption.pyc
