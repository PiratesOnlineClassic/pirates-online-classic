# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.seapatch.LerpSeaPatchInterval

class LerpSeaPatchInterval():
    __module__ = __name__
    lerpNum = 1

    def __init__(self, name, duration, blendType, patch, initial, target):
        if name == None:
            name = 'LerpSeaPatchInterval-%d' % self.lerpNum
            LerpSeaPatchInterval.lerpNum += 1

        blendType = self.stringBlendType(blendType)
        if target == None:
            target = SeaPatchRoot()
# okay decompiling .\pirates\seapatch\LerpSeaPatchInterval.pyc
