# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.speedchat.SCSettings
from otp.speedchat.SCColorScheme import SCColorScheme


class SCSettings:

    def __init__(self,
                 eventPrefix,
                 whisperMode=0,
                 colorScheme=None,
                 submenuOverlap=2.0 / 3,
                 topLevelOverlap=None):
        self.eventPrefix = eventPrefix
        self.whisperMode = whisperMode
        if colorScheme is None:
            colorScheme = SCColorScheme()
        self.colorScheme = colorScheme
        self.submenuOverlap = submenuOverlap
        self.topLevelOverlap = topLevelOverlap
        return


# okay decompiling .\otp\speedchat\SCSettings.pyc
