# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.distributed.DistributedTestObject
from direct.distributed import DistributedObject


class DistributedTestObject(DistributedObject.DistributedObject):
    

    def setRequiredField(self, r):
        self.requiredField = r

    def setB(self, B):
        self.B = B

    def setBA(self, BA):
        self.BA = BA

    def setBO(self, BO):
        self.BO = BO

    def setBR(self, BR):
        self.BR = BR

    def setBRA(self, BRA):
        self.BRA = BRA

    def setBRO(self, BRO):
        self.BRO = BRO

    def setBROA(self, BROA):
        self.BROA = BROA

    def gotNonReqThatWasntSet(self):
        for field in ('B', 'BA', 'BO', 'BR', 'BRA', 'BRO', 'BROA'):
            if hasattr(self, field):
                return True

        return False
# okay decompiling .\otp\distributed\DistributedTestObject.pyc
