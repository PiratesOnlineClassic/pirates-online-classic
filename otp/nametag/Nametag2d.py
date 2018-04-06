import math

from Nametag import *
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

        self.contents = self.CName | self.CSpeech
        self.chatWordWrap = 7.5

        self.innerNP.setScale(self.SCALE_2D)

    def showBalloon(self, balloon, text):
        pass

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
