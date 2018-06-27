import math

from panda3d.core import *

from otp.nametag import NametagGlobals
from otp.nametag.Nametag import *
from otp.nametag.NametagConstants import *


class Nametag3d(Nametag):
    WANT_DYNAMIC_SCALING = True
    SCALING_FACTOR = 0.06
    SCALING_MINDIST = 0.1
    SCALING_MAXDIST = 100000

    BILLBOARD_OFFSET = 3.0
    SHOULD_BILLBOARD = True

    CLICK_REGION_LEFT = -0.4
    CLICK_REGION_RIGHT = 0.4
    CLICK_REGION_BOTTOM = -1.2
    CLICK_REGION_TOP = 0.8

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

        # attempt to maintain the same on-screen size.
        distance = self.innerNP.getPos(NametagGlobals.camera).length()
        distance = max(min(distance, self.SCALING_MAXDIST), self.SCALING_MINDIST)

        # calculate the scale factor of the nametag based on the
        # distance from the nametag node to the camera node.
        scale = math.sqrt(distance) * self.SCALING_FACTOR
        self.innerNP.setScale(scale)

        # As 3D nametags can move around on their own, we need to update the
        # click frame constantly:
        path = NodePath.anyPath(self)
        if path.isHidden() or (path.getTop() != NametagGlobals.camera.getTop() and path.getTop() != render2d) or \
            not self.avatar or hasattr(self.avatar, 'isLocal') and self.avatar.isLocal():

            self.stashClickRegion()
        else:
            # get the bounding sphere of the avatar so we can get
            # the avatar radius to base the nametag click margins...
            bounds = self.avatar.getBounds()

            # check to see if the bounding sphere is infinite.
            if bounds.isInfinite():
                return

            scaleFactor = bounds.getRadius()

            # update the click region based on the static click region values,
            # the bounding sphere of the avatar and the distance from the nametag
            # to the local camera node...
            self.updateClickRegion((self.CLICK_REGION_LEFT * scaleFactor) * scale, (self.CLICK_REGION_RIGHT * scaleFactor) * scale,
                (self.CLICK_REGION_BOTTOM * scaleFactor) * scale, self.CLICK_REGION_TOP * scale)

    def getSpeechBalloon(self):
        return NametagGlobals.speechBalloon3d

    def getThoughtBalloon(self):
        return NametagGlobals.thoughtBalloon3d
