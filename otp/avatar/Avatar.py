import random

from panda3d.core import *
from direct.actor.Actor import Actor
from direct.distributed import ClockDelta
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.avatar.ShadowCaster import ShadowCaster
from otp.otpbase import OTPGlobals, OTPLocalizer, OTPRender
from otp.nametag.Nametag import Nametag
from otp.nametag.NametagGroup import NametagGroup
from otp.nametag.NametagConstants import CFSpeech, CFThought, CFTimeout, CFPageButton, CFNoQuitButton, CFQuitButton
from otp.ai.MagicWordGlobal import *
from direct.showbase.InputStateGlobal import inputState


def reconsiderAllUnderstandable():
    for av in Avatar.ActiveAvatars:
        av.considerUnderstandable()


class Avatar(Actor, ShadowCaster):
    __module__ = __name__
    notify = directNotify.newCategory('Avatar')
    ActiveAvatars = []
    ManagesNametagAmbientLightChanged = False

    def __init__(self, other=None):
        try:
            self.Avatar_initialized
            return
        except:
            self.Avatar_initialized = 1

        Actor.__init__(self, None, None, other, flattenable=False, setFinal=True,
            mergeLODBundles=True, allowAsyncBind=True)

        ShadowCaster.__init__(self)
        self.name = ''
        self.__font = OTPGlobals.getInterfaceFont()
        self.soundChatBubble = None
        self.avatarType = ''
        self.nametagNodePath = None
        self.__nameVisible = 1
        self.nametag = NametagGroup()
        self.nametag.setAvatar(self)
        self.nametag.setFont(OTPGlobals.getInterfaceFont())
        self.nametag2dContents = Nametag.CName | Nametag.CSpeech
        self.nametag2dDist = Nametag.CName | Nametag.CSpeech
        self.nametag2dNormalContents = Nametag.CName | Nametag.CSpeech
        self.nametag3d = self.attachNewNode('nametag3d')
        self.nametag3d.setTag('cam', 'nametag')
        self.nametag3d.setLightOff()
        if not self.ManagesNametagAmbientLightChanged:
            self.acceptNametagAmbientLightChange()

        OTPRender.renderReflection(False, self.nametag3d, 'otp_avatar_nametag', None)
        self.getGeomNode().showThrough(OTPRender.ShadowCameraBitmask)
        self.nametag3d.hide(OTPRender.ShadowCameraBitmask)
        self.collTube = None
        self.battleTube = None
        self.scale = 1.0
        self.nametagScale = 1.0
        self.height = 0.0
        self.battleTubeHeight = 0.0
        self.battleTubeRadius = 0.0
        self.style = None
        self.commonChatFlags = 0
        self.understandable = 1
        self.setPlayerType(NametagGroup.CCNormal)
        self.ghostMode = 0
        self.__chatParagraph = None
        self.__chatMessage = None
        self.__chatFlags = 0
        self.__chatPageNumber = None
        self.__chatAddressee = None
        self.__chatDialogueList = []
        self.__chatSet = 0
        self.__chatLocal = 0
        self.__currentDialogue = None

    def delete(self):
        try:
            self.Avatar_deleted
            return
        except:
            self.Avatar_deleted = 1

        self.deleteNametag3d()
        Actor.cleanup(self)
        if not self.ManagesNametagAmbientLightChanged:
            self.ignoreNametagAmbientLightChange()

        del self.__font
        del self.style
        del self.soundChatBubble
        del self.nametag
        self.nametag3d.removeNode()
        ShadowCaster.delete(self)
        Actor.delete(self)

    def acceptNametagAmbientLightChange(self):
        self.accept('nametagAmbientLightChanged', self.nametagAmbientLightChanged)

    def ignoreNametagAmbientLightChange(self):
        self.ignore('nametagAmbientLightChanged')

    def isLocal(self):
        return 0

    def isPet(self):
        return False

    def isProxy(self):
        return False

    def setPlayerType(self, playerType):
        self.playerType = playerType
        if self.isUnderstandable():
            self.nametag.setColorCode(self.playerType)
        else:
            self.nametag.setColorCode(NametagGroup.CCNoChat)

    def setCommonChatFlags(self, commonChatFlags):
        self.commonChatFlags = commonChatFlags
        self.considerUnderstandable()
        if self == base.localAvatar:
            reconsiderAllUnderstandable()

    def considerUnderstandable(self):
        speed = 0
        if self.playerType in (NametagGroup.CCNormal, NametagGroup.CCFreeChat, NametagGroup.CCSpeedChat):
            self.setPlayerType(NametagGroup.CCSpeedChat)
            speed = 1
        if self == base.localAvatar:
            self.understandable = 1
            self.setPlayerType(NametagGroup.CCFreeChat)
        else:
            if self.playerType == NametagGroup.CCSuit:
                self.understandable = 1
                self.setPlayerType(NametagGroup.CCSuit)
            else:
                if self.playerType not in (NametagGroup.CCNormal, NametagGroup.CCFreeChat, NametagGroup.CCSpeedChat):
                    self.understandable = 1
                    self.setPlayerType(NametagGroup.CCNoChat)
                else:
                    if self.commonChatFlags & base.localAvatar.commonChatFlags & OTPGlobals.CommonChat:
                        self.understandable = 1
                        self.setPlayerType(NametagGroup.CCFreeChat)
                    else:
                        if self.commonChatFlags & OTPGlobals.SuperChat:
                            self.understandable = 1
                            self.setPlayerType(NametagGroup.CCFreeChat)
                        else:
                            if base.localAvatar.commonChatFlags & OTPGlobals.SuperChat:
                                self.understandable = 1
                                self.setPlayerType(NametagGroup.CCFreeChat)
                            else:
                                if base.cr.getFriendFlags(self.doId) & OTPGlobals.FriendChat:
                                    self.understandable = 1
                                    self.setPlayerType(NametagGroup.CCFreeChat)
                                else:
                                    if base.cr.playerFriendsManager.findPlayerIdFromAvId(self.doId) is not None:
                                        if base.cr.playerFriendsManager.findPlayerInfoFromAvId(self.doId).openChatFriendshipYesNo:
                                            self.understandable = 1
                                            self.nametag.setColorCode(NametagGroup.CCFreeChat)
                                        else:
                                            self.understandable = 0
                                    else:
                                        self.understandable = 0
        self.nametag.setColorCode(self.playerType)
        return

    def isUnderstandable(self):
        return self.understandable

    def setDNAString(self, dnaString):
        pass

    def setDNA(self, dna):
        pass

    def getAvatarScale(self):
        return self.scale

    def setAvatarScale(self, scale):
        if self.scale != scale:
            self.scale = scale
            self.getGeomNode().setScale(scale)
            self.setHeight(self.height)

    def getNametagScale(self):
        return self.nametagScale

    def setNametagScale(self, scale):
        self.nametagScale = scale
        self.nametag3d.setScale(scale)

    def adjustNametag3d(self, parentScale=1.0):
        self.nametag3d.setPos(0, 0, self.height + 0.5)

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        self.height = height
        self.adjustNametag3d()
        if self.collTube:
            self.collTube.setPointB(0, 0, height - self.getRadius())
            if self.collNodePath:
                self.collNodePath.forceRecomputeBounds()
        if self.battleTube:
            self.battleTube.setPointB(0, 0, height - self.getRadius())

    def getRadius(self):
        return OTPGlobals.AvatarDefaultRadius

    def getName(self):
        return self.name

    def getType(self):
        return self.avatarType

    def setName(self, name):
        if hasattr(self, 'isDisguised'):
            if self.isDisguised:
                return
        self.name = name
        if hasattr(self, 'nametag'):
            self.nametag.setName(name)

    def setDisplayName(self, str):
        if hasattr(self, 'isDisguised'):
            if self.isDisguised:
                return
        self.nametag.setDisplayName(str)

    def getFont(self):
        return self.__font

    def setFont(self, font):
        self.__font = font
        self.nametag.setFont(font)

    def getStyle(self):
        return self.style

    def setStyle(self, style):
        self.style = style

    def getDialogueArray(self):
        return

    def playCurrentDialogue(self, dialogue, chatFlags, interrupt=1):
        if interrupt and self.__currentDialogue is not None:
            self.__currentDialogue.stop()
        self.__currentDialogue = dialogue
        if dialogue:
            base.playSfx(dialogue, node=self)
        else:
            if chatFlags & CFSpeech != 0 and self.nametag.getNumChatPages() > 0:
                self.playDialogueForString(self.nametag.getChat())
                if self.soundChatBubble != None:
                    base.playSfx(self.soundChatBubble, node=self)
        return

    def playDialogueForString(self, chatString):
        searchString = chatString.lower()
        if searchString.find(OTPLocalizer.DialogSpecial) >= 0:
            type = 'special'
        else:
            if searchString.find(OTPLocalizer.DialogExclamation) >= 0:
                type = 'exclamation'
            else:
                if searchString.find(OTPLocalizer.DialogQuestion) >= 0:
                    type = 'question'
                else:
                    if random.randint(0, 1):
                        type = 'statementA'
                    else:
                        type = 'statementB'
        stringLength = len(chatString)
        if stringLength <= OTPLocalizer.DialogLength1:
            length = 1
        else:
            if stringLength <= OTPLocalizer.DialogLength2:
                length = 2
            else:
                if stringLength <= OTPLocalizer.DialogLength3:
                    length = 3
                else:
                    length = 4
        self.playDialogue(type, length)

    def playDialogue(self, type, length):
        dialogueArray = self.getDialogueArray()
        if dialogueArray == None:
            return
        sfxIndex = None
        if type == 'statementA' or type == 'statementB':
            if length == 1:
                sfxIndex = 0
            elif length == 2:
                sfxIndex = 1
            elif length >= 3:
                sfxIndex = 2
        else:
            if type == 'question':
                sfxIndex = 3
            else:
                if type == 'exclamation':
                    sfxIndex = 4
                else:
                    if type == 'special':
                        sfxIndex = 5
                    else:
                        notify.error('unrecognized dialogue type: ', type)
        if sfxIndex != None and sfxIndex < len(dialogueArray) and dialogueArray[sfxIndex] != None:
            base.playSfx(dialogueArray[sfxIndex], node=self)
        return

    def getDialogueSfx(self, type, length):
        retval = None
        dialogueArray = self.getDialogueArray()
        if dialogueArray == None:
            return
        sfxIndex = None
        if type == 'statementA' or type == 'statementB':
            if length == 1:
                sfxIndex = 0
            elif length == 2:
                sfxIndex = 1
            elif length >= 3:
                sfxIndex = 2
        else:
            if type == 'question':
                sfxIndex = 3
            else:
                if type == 'exclamation':
                    sfxIndex = 4
                else:
                    if type == 'special':
                        sfxIndex = 5
                    else:
                        notify.error('unrecognized dialogue type: ', type)
        if sfxIndex != None and sfxIndex < len(dialogueArray) and dialogueArray[sfxIndex] != None:
            retval = dialogueArray[sfxIndex]
        return retval

    def setChatAbsolute(self, chatString, chatFlags, dialogue=None, interrupt=1):
        self.nametag.setChat(chatString, chatFlags)
        self.playCurrentDialogue(dialogue, chatFlags, interrupt)

    def clearChat(self):
        self.nametag.clearChat()

    def isInView(self):
        pos = self.getPos(camera)
        eyePos = Point3(pos[0], pos[1], pos[2] + self.getHeight())
        return base.camNode.isInView(eyePos)

    def getNameVisible(self):
        return self.__nameVisible

    def setNameVisible(self, bool):
        self.__nameVisible = bool
        if bool:
            self.showName()
        if not bool:
            self.hideName()

    def hideName(self):
        self.nametag.getNametag3d().setContents(Nametag.CSpeech | Nametag.CThought)

    def showName(self):
        if self.__nameVisible and not self.ghostMode:
            self.nametag.getNametag3d().setContents(Nametag.CName | Nametag.CSpeech | Nametag.CThought)

    def hideNametag2d(self):
        self.nametag2dContents = 0
        self.nametag.getNametag2d().setContents(self.nametag2dContents & self.nametag2dDist)

    def showNametag2d(self):
        self.nametag2dContents = self.nametag2dNormalContents
        if self.ghostMode:
            self.nametag2dContents = Nametag.CSpeech
        self.nametag.getNametag2d().setContents(self.nametag2dContents & self.nametag2dDist)

    def hideNametag3d(self):
        self.nametag.getNametag3d().setContents(0)

    def showNametag3d(self):
        if self.__nameVisible and not self.ghostMode:
            self.nametag.getNametag3d().setContents(Nametag.CName | Nametag.CSpeech | Nametag.CThought)
        else:
            self.nametag.getNametag3d().setContents(0)

    def setPickable(self, flag):
        self.nametag.setActive(flag)

    def clickedNametag(self):
        if self.nametag.hasButton():
            self.advancePageNumber()
        else:
            if self.nametag.isActive():
                messenger.send('clickedNametag', [self])

    def setPageChat(self, addressee, paragraph, message, quitButton, extraChatFlags=None, dialogueList=[], pageButton=True):
        self.__chatAddressee = addressee
        self.__chatPageNumber = None
        self.__chatParagraph = paragraph
        self.__chatMessage = message
        if extraChatFlags is None:
            self.__chatFlags = CFSpeech
        else:
            self.__chatFlags = CFSpeech | extraChatFlags
        self.__chatDialogueList = dialogueList
        self.__chatSet = 0
        self.__chatLocal = 0
        self.__updatePageChat()
        if addressee == base.localAvatar.doId:
            if pageButton:
                self.__chatFlags |= CFPageButton
            if quitButton == None:
                self.__chatFlags |= CFNoQuitButton
            else:
                if quitButton:
                    self.__chatFlags |= CFQuitButton
            self.b_setPageNumber(self.__chatParagraph, 0)
        return

    def setLocalPageChat(self, message, quitButton, extraChatFlags=None, dialogueList=[]):
        self.__chatAddressee = base.localAvatar.doId
        self.__chatPageNumber = None
        self.__chatParagraph = None
        self.__chatMessage = message
        if extraChatFlags is None:
            self.__chatFlags = CFSpeech
        else:
            self.__chatFlags = CFSpeech | extraChatFlags
        self.__chatDialogueList = dialogueList
        self.__chatSet = 1
        self.__chatLocal = 1
        self.__chatFlags |= CFPageButton
        if quitButton == None:
            self.__chatFlags |= CFNoQuitButton
        else:
            if quitButton:
                self.__chatFlags |= CFQuitButton
        if len(dialogueList) > 0:
            dialogue = dialogueList[0]
        else:
            dialogue = None
        self.setChatAbsolute(message, self.__chatFlags, dialogue)
        self.setPageNumber(None, 0)
        return

    def setPageNumber(self, paragraph, pageNumber, timestamp=None):
        if timestamp == None:
            elapsed = 0.0
        else:
            elapsed = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.__chatPageNumber = [paragraph, pageNumber]
        self.__updatePageChat()
        if hasattr(self, 'uniqueName'):
            if pageNumber >= 0:
                messenger.send(self.uniqueName('nextChatPage'), [
                 pageNumber, elapsed])
            else:
                messenger.send(self.uniqueName('doneChatPage'), [
                 elapsed])
        else:
            if pageNumber >= 0:
                messenger.send('nextChatPage', [pageNumber, elapsed])
            else:
                messenger.send('doneChatPage', [elapsed])
        return

    def advancePageNumber(self):
        if self.__chatAddressee == base.localAvatar.doId and self.__chatPageNumber != None and self.__chatPageNumber[0] == self.__chatParagraph:
            pageNumber = self.__chatPageNumber[1]
            if pageNumber >= 0:
                pageNumber += 1
                if pageNumber >= self.nametag.getNumChatPages():
                    pageNumber = -1
                if self.__chatLocal:
                    self.setPageNumber(self.__chatParagraph, pageNumber)
                else:
                    self.b_setPageNumber(self.__chatParagraph, pageNumber)
        return

    def __updatePageChat(self):
        if self.__chatPageNumber != None and self.__chatPageNumber[0] == self.__chatParagraph:
            pageNumber = self.__chatPageNumber[1]
            if pageNumber >= 0:
                if not self.__chatSet:
                    if len(self.__chatDialogueList) > 0:
                        dialogue = self.__chatDialogueList[0]
                    else:
                        dialogue = None
                    self.setChatAbsolute(self.__chatMessage, self.__chatFlags, dialogue)
                    self.__chatSet = 1
                if pageNumber < self.nametag.getNumChatPages():
                    self.nametag.setPageNumber(pageNumber)
                    if pageNumber > 0:
                        if len(self.__chatDialogueList) > pageNumber:
                            dialogue = self.__chatDialogueList[pageNumber]
                        else:
                            dialogue = None
                        self.playCurrentDialogue(dialogue, self.__chatFlags)
                else:
                    self.clearChat()
            else:
                self.clearChat()
        return

    def getAirborneHeight(self):
        height = self.getPos(self.shadowPlacer.shadowNodePath)
        return height.getZ() + 0.025

    def initializeNametag3d(self):
        self.deleteNametag3d()
        nametagNode = self.nametag.getNametag3d()
        self.nametagNodePath = self.nametag3d.attachNewNode(nametagNode)
        iconNodePath = self.nametag.getNameIcon()
        for cJoint in self.getNametagJoints():
            cJoint.clearNetTransforms()
            cJoint.addNetTransform(nametagNode)

    def nametagAmbientLightChanged(self, newlight):
        self.nametag3d.setLightOff()
        if newlight:
            self.nametag3d.setLight(newlight)

    def deleteNametag3d(self):
        if self.nametagNodePath:
            self.nametagNodePath.removeNode()
            self.nametagNodePath = None
        return

    def initializeBodyCollisions(self, collIdStr):
        self.collTube = CollisionTube(0, 0, 0.5, 0, 0, self.height - self.getRadius(), self.getRadius())
        self.collNode = CollisionNode(collIdStr)
        self.collNode.addSolid(self.collTube)
        self.collNodePath = self.attachNewNode(self.collNode)
        if self.ghostMode:
            self.collNode.setCollideMask(OTPGlobals.GhostBitmask)
        else:
            self.collNode.setCollideMask(OTPGlobals.WallBitmask)

    def stashBodyCollisions(self):
        if hasattr(self, 'collNodePath'):
            self.collNodePath.stash()

    def unstashBodyCollisions(self):
        if hasattr(self, 'collNodePath'):
            self.collNodePath.unstash()

    def disableBodyCollisions(self):
        if hasattr(self, 'collNodePath'):
            self.collNodePath.removeNode()
            del self.collNodePath
        self.collTube = None
        return

    def addActive(self):
        if base.wantNametags:
            try:
                Avatar.ActiveAvatars.remove(self)
            except ValueError:
                pass
            else:
                Avatar.ActiveAvatars.append(self)
                self.nametag.manage(base.marginManager)
                self.accept(self.nametag.getUniqueId(), self.clickedNametag)

    def removeActive(self):
        if base.wantNametags:
            try:
                Avatar.ActiveAvatars.remove(self)
            except ValueError:
                pass
            else:
                self.nametag.unmanage(base.marginManager)
                self.ignore(self.nametag.getUniqueId())

    def loop(self, animName, restart=1, partName=None, fromFrame=None, toFrame=None):
        return Actor.loop(self, animName, restart, partName, fromFrame, toFrame)


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def run():
    inputState.set('debugRunning', inputState.isSet('debugRunning') != True)
    if not inputState.isSet('debugRunning'):
        return 'Debug running disabled!'
    return 'Debug running enabled!'
