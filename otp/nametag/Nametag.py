from otp.nametag import NametagGlobals
from otp.nametag.NametagConstants import *
from otp.margins.ClickablePopup import ClickablePopup
from otp.otpbase import OTPGlobals
from panda3d.core import *


class Nametag(ClickablePopup):
    CName = 1
    CSpeech = 2
    CThought = 4

    NAME_PADDING = 0.2
    CHAT_ALPHA = 1.0

    DEFAULT_CHAT_WORDWRAP = 10.0

    IS_3D = False  # 3D variants will set this to True.

    def __init__(self):
        if self.IS_3D:
            ClickablePopup.__init__(self, NametagGlobals.camera)
        else:
            ClickablePopup.__init__(self)

        self.contents = 0  # To be set by subclass.

        self.innerNP = NodePath.anyPath(self).attachNewNode('nametag_contents')

        self.wordWrap = 7.5
        self.chatWordWrap = None

        self.font = None
        self.active = False
        self.speechFont = None
        self.name = ''
        self.displayName = ''
        self.qtColor = VBase4(1, 1, 1, 1)
        self.colorCode = CCNormal
        self.avatar = None
        self.icon = PandaNode('icon')

        self.frame = (0, 0, 0, 0)

        self.nameFg = (0, 0, 0, 1)
        self.nameBg = (1, 1, 1, 1)
        self.chatFg = (0, 0, 0, 1)
        self.chatBg = (1, 1, 1, 1)

        self.chatString = ''
        self.chatFlags = 0

    def destroy(self):
        ClickablePopup.destroy(self)

    def setContents(self, contents):
        self.contents = contents
        self.update()

    def setAvatar(self, avatar):
        self.avatar = avatar

    def setActive(self, active):
        self.active = active

    def setChatWordwrap(self, chatWordWrap):
        self.chatWordWrap = chatWordWrap

    def tick(self):
        pass  # Does nothing by default.

    def clickStateChanged(self):
        self.update()

    def update(self):
        if self.colorCode in NAMETAG_COLORS:
            cc = self.colorCode
        else:
            cc = CCNormal

        self.nameFg, self.nameBg, self.chatFg, self.chatBg = \
            NAMETAG_COLORS[cc][self.getClickState()]

        self.innerNP.node().removeAllChildren()
        if self.contents & self.CThought and self.chatFlags & CFThought:
            self.showThought()
        elif self.contents & self.CSpeech and self.chatFlags & CFSpeech:
            self.showSpeech()
        elif self.contents & self.CName and self.displayName:
            self.showName()

    def showBalloon(self, balloon, text):
        if not self.font:
            # If no font is set, we can't display anything yet...
            return

        color = self.qtColor if (
            self.chatFlags & CFQuicktalker) else self.chatBg
        if color[3] > self.CHAT_ALPHA:
            color = (color[0], color[1], color[2], self.CHAT_ALPHA)

        reversed = (self.IS_3D and (self.chatFlags & CFReversed))

        balloon, frame = balloon.generate(text, self.font, textColor=self.chatFg,
                                          balloonColor=color,
                                          wordWrap=self.chatWordWrap or
                                          self.DEFAULT_CHAT_WORDWRAP,
                                          reversed=reversed)
        balloon.reparentTo(self.innerNP)
        self.frame = frame

    def showThought(self):
        self.showBalloon(self.getThoughtBalloon(), self.chatString)

    def showSpeech(self):
        self.showBalloon(self.getSpeechBalloon(), self.chatString)

    def showName(self):
        if not self.font:
            # If no font is set, we can't display anything yet...
            return

        self.icon.reparentTo(self.innerNP)
        self.icon.setBin('fixed', 0)
