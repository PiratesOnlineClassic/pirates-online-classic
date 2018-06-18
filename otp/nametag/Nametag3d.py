import math

from otp.nametag import NametagGlobals
from otp.nametag.Nametag import *
from otp.nametag.NametagConstants import *
from panda3d.core import *


class Nametag3d(Nametag):
    WANT_DYNAMIC_SCALING = True
    SCALING_FACTOR = 0.06
    SCALING_MINDIST = 0.1
    SCALING_MAXDIST = 100000

    BILLBOARD_OFFSET = 3.0
    SHOULD_BILLBOARD = True

    IS_3D = True

    def __init__(self):
        Nametag.__init__(self)

        self.contents = self.CName | self.CSpeech | self.CThought

        self.bbOffset = self.BILLBOARD_OFFSET
        self._doBillboard()

    def _doBillboard(self):
        if self.SHOULD_BILLBOARD:
            self.innerNP.setEffect(BillboardEffect.make(
                Vec3(0, 0, 1),
                True,
                False,
                self.bbOffset,
                NodePath(),  # Empty; look at scene camera
                Point3(0, 0, 0)))
        else:
            self.bbOffset = 0.0

    def setBillboardOffset(self, bbOffset):
        self.bbOffset = bbOffset
        self._doBillboard()

    def tick(self):
        if not self.WANT_DYNAMIC_SCALING:
            self.innerNP.setScale(self.SCALING_FACTOR)
            return

        # Attempt to maintain the same on-screen size.
        distance = self.innerNP.getPos(NametagGlobals.camera).length()
        distance = max(min(distance, self.SCALING_MAXDIST), self.SCALING_MINDIST)

        self.innerNP.setScale(math.sqrt(distance) * self.SCALING_FACTOR)

        # As 3D nametags can move around on their own, we need to update the
        # click frame constantly:
        self.updateClickRegion(-1.25, 1.25, -1, 1)

    def getSpeechBalloon(self):
        return NametagGlobals.speechBalloon3d

    def getThoughtBalloon(self):
        return NametagGlobals.thoughtBalloon3d
