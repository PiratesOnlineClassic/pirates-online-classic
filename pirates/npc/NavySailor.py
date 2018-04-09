# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.npc.NavySailor
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.pirate import AvatarTypes, Human
from pirates.piratesbase import PiratesGlobals


class NavySailor(Human.Human):
    __module__ = __name__

    def __init__(self, avatarType=AvatarTypes.Navy):
        Human.Human.__init__(self)
        self.avatarType = avatarType

    def getEnterDeathTrack(self):
        return Human.Human.getEnterDeathTrack(self)

    def getExitDeathTrack(self):
        return Human.Human.getExitDeathTrack(self)
# okay decompiling .\pirates\npc\NavySailor.pyc
