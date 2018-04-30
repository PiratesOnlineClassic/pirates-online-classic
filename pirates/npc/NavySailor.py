from direct.interval.IntervalGlobal import *
from panda3d.core import *
from pirates.pirate import AvatarTypes, Human
from pirates.piratesbase import PiratesGlobals


class NavySailor(Human.Human):

    def __init__(self, avatarType=AvatarTypes.Navy):
        Human.Human.__init__(self)
        self.avatarType = avatarType

    def getEnterDeathTrack(self):
        return Human.Human.getEnterDeathTrack(self)

    def getExitDeathTrack(self):
        return Human.Human.getExitDeathTrack(self)
