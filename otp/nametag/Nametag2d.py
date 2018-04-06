import math

from .Nametag import *
from otp.margins.MarginPopup import *
from pandac.PandaModules import *


class Nametag2d(Nametag, MarginPopup):
    SCALE_2D = 0.25
    CHAT_ALPHA = 0.5
    ARROW_OFFSET = -1.0
    ARROW_SCALE = 1.5

    DEFAULT_CHAT_WORDWRAP = 8.0

    def __init__(self):
        Nametag.__init__(self)
        MarginPopup.__init__(self)

        self.contents = self.CName|self.CSpeech
        self.chatWordWrap = 7.5

        self.arrow = None

        self.innerNP.setScale(self.SCALE_2D)

    def showBalloon(self, balloon, text):
        text = '%s: %s' % (self.name, text)
        Nametag.showBalloon(self, balloon, text)

        # Next, center the balloon in the cell:
        balloon = NodePath.anyPath(self).find('*/balloon')

        # Calculate the center of the TextNode.
        text = balloon.find('**/+TextNode')
        t = text.node()
        left, right, bottom, top = t.getFrameActual()
        center = self.innerNP.getRelativePoint(text,
                                               ((left+right)/2., 0, (bottom+top)/2.))

        # Next translate the balloon along the inverse.
        balloon.setPos(balloon, -center)
        # Also translate the frame:
        left, right, bottom, top = self.frame
        self.frame = (left-center.getX(), right-center.getX(),
                      bottom-center.getZ(), top-center.getZ())

        # When a balloon is active, we need to be somewhat higher-priority in the
        # popup system:
        self.setPriority(1)

    def showName(self):
        Nametag.showName(self)

        # Revert our priority back to basic:
        self.setPriority(0)

    def update(self):
        Nametag.update(self)
        self.considerUpdateClickRegion()

    def marginVisibilityChanged(self):
        self.considerUpdateClickRegion()

    def considerUpdateClickRegion(self):
        pass

    def tick(self):
        pass

    def getSpeechBalloon(self):
        return NametagGlobals.speechBalloon2d

    def getThoughtBalloon(self):
        return NametagGlobals.thoughtBalloon2d
