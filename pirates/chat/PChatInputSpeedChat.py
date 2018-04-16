import random
import string

from direct.fsm import ClassicFSM, State
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from otp.chat.ChatGlobals import *
from otp.otpbase import OTPGlobals, OTPLocalizer
from otp.speedchat import SpeedChatGlobals
from otp.speedchat.SpeedChat import SpeedChat
from otp.speedchat.SpeedChatTypes import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.speedchat import PSpeedChatGlobals
from pirates.speedchat.PSpeedChatQuestMenu import PSpeedChatQuestMenu
from pirates.speedchat.PSpeedChatTypes import *

scStructure = [
 [
  OTPLocalizer.PSCMenuExpressions, [OTPLocalizer.PSCMenuGreetings, 50700, 50701, 50702, 50703, 50704], [OTPLocalizer.PSCMenuGoodbyes, 50800, 50801, 50802], [OTPLocalizer.PSCMenuFriendly, 50900], [OTPLocalizer.PSCMenuHappy, 51000], [OTPLocalizer.PSCMenuSad, 51100], [OTPLocalizer.PSCMenuSorry, 51200, 51201, 51202, 51203, 51204], 50105, 50100, 50101, 50102, 50103, 50104], [OTPLocalizer.PSCMenuCombat, 51300, 51301, 51302, 51303, 51304, 51305, 51306, 51307, 51308], [OTPLocalizer.PSCMenuSeaCombat, 51400, 51401, 51402, 51403, 51404, 51405, 51406, 51407, 51408, 51409, 51410, 51411, 51412, 51413, 51414, 51415, 51416, 51417, 51418, 51419, 51420, 51421], [OTPLocalizer.PSCMenuPlaces, [OTPLocalizer.PSCMenuLetsSail, 51500, 51501, 51502, 51503, 51504, 51505, 51506, 51507, 51508, 51509, 51510, 51511, 51512], [OTPLocalizer.PSCMenuLetsHeadTo, [OTPLocalizer.PSCMenuHeadToPortRoyal, 51800, 51801], 51600, 51601, 51602], [OTPLocalizer.PSCMenuWhereIs, 52500], 50400, 50401], [OTPLocalizer.PSCMenuDirections, 51700, 51701, 51702, 51703, 51704, 51705, 51706, 51707], [OTPLocalizer.PSCMenuInsults, 50200, 50201, 50202, 50203, 50204, 50205], [OTPLocalizer.PSCMenuCompliments, 50300, 50301, 50302, 50303, 50304, 50305, 50306], [OTPLocalizer.PSCMenuCardGames, [OTPLocalizer.PSCMenuPoker, 51900, 51901, 51902, 51903, 51904], [OTPLocalizer.PSCMenuBlackjack, 52600, 52601], 52400, 52401, 52402], [OTPLocalizer.PSCMenuInvitations, [OTPLocalizer.PSCMenuVersusPlayer, 52300, 52301, 52302, 52303, 52304], [OTPLocalizer.PSCMenuHunting, 52200, 52201], 52100, 52101], [PSpeedChatQuestMenu, OTPLocalizer.PSCMenuQuests], 50005, 50001, 50002, 50003, 50004]

class PChatInputSpeedChat(DirectObject.DirectObject):
    
    DefaultSCColorScheme = SCColorScheme(arrowColor=(1, 1, 1), rolloverColor=(1, 1,
                                                                              1))
    holidayIdList = []

    def __init__(self):
        self.whisperId = None
        self.toPlayer = 0
        self.emoteNoAccessPanel = DirectFrame(parent=hidden, relief=None, state='normal', text=OTPLocalizer.SCEmoteNoAccessMsg, frameSize=(-1,
                                                                                                                                           1,
                                                                                                                                           -1,
                                                                                                                                           1), geom=DGG.getDefaultDialogGeom(), geom_color=OTPGlobals.GlobalDialogColor, geom_scale=(0.92,
                                                                                                                                                                                                                                     1,
                                                                                                                                                                                                                                     0.6), geom_pos=(0,
                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                     -0.08), text_scale=0.08)
        self.emoteNoAccessPanel.hide()
        DirectButton(parent=self.emoteNoAccessPanel, relief=None, text=OTPLocalizer.SCEmoteNoAccessOK, text_scale=0.05, text_pos=(0.0, -0.1), textMayChange=0, pos=(0.0, 0.0, -0.2), command=self.handleEmoteNoAccessDone)
        structure = []
        structure.append([SCEmoteMenu, OTPLocalizer.SCMenuEmotions])
        self.emoteMenuIdx = len(structure) - 1
        structure.append([SCCustomMenu, OTPLocalizer.SCMenuCustom])
        structure += scStructure
        if base.config.GetBool('want-emotes', 1):
            emote_structure = None
            emote_dance_structure = None
            emote_general_structure = None
            emote_music_structure = None
            emote_expressions_structure = None
            avatar_gender = base.emoteGender
            idList = PLocalizer.emotes.keys()
            idList.sort()
            for id in idList:
                emote = PLocalizer.emotes.get(id)
                emote_group = emote[3]
                emote_gender = emote[4]
                if id == PLocalizer.EMOTE_VALENTINES:
                    continue
                if not emote_structure:
                    emote_structure = [
                     OTPLocalizer.Emotes_Root]
                if not emote_dance_structure:
                    emote_dance_structure = [
                     OTPLocalizer.Emotes_Dances]
                    emote_structure.append(emote_dance_structure)
                if not emote_general_structure:
                    emote_general_structure = [
                     OTPLocalizer.Emotes_General]
                    emote_structure.append(emote_general_structure)
                if not emote_music_structure:
                    emote_music_structure = [
                     OTPLocalizer.Emotes_Music]
                    emote_structure.append(emote_music_structure)
                if not emote_expressions_structure:
                    emote_expressions_structure = [
                     OTPLocalizer.Emotes_Expressions]
                    emote_structure.append(emote_expressions_structure)
                if emote_gender == avatar_gender or emote_gender is None:
                    if emote_group == OTPLocalizer.Emotes_Dances:
                        emote_dance_structure.append(id)
                    elif emote_group == OTPLocalizer.Emotes_General:
                        emote_general_structure.append(id)
                    elif emote_group == OTPLocalizer.Emotes_Music:
                        emote_music_structure.append(id)
                    elif emote_group == OTPLocalizer.Emotes_Expressions:
                        emote_expressions_structure.append(id)

            if emote_structure:
                structure.insert(0, emote_structure)
        self.createSpeedChatObject(structure)

        def listenForSCEvent(eventBaseName, handler, self=self):
            eventName = self.speedChat.getEventName(eventBaseName)
            self.accept(eventName, handler)

        listenForSCEvent(SpeedChatGlobals.SCTerminalLinkedEmoteEvent, self.handleLinkedEmote)
        listenForSCEvent(SpeedChatGlobals.SCStaticTextMsgEvent, self.handleStaticTextMsg)
        listenForSCEvent(SpeedChatGlobals.SCCustomMsgEvent, self.handleCustomMsg)
        listenForSCEvent(SpeedChatGlobals.SCEmoteMsgEvent, self.handleEmoteMsg)
        listenForSCEvent(SpeedChatGlobals.SCEmoteNoAccessEvent, self.handleEmoteNoAccess)
        listenForSCEvent('SpeedChatStyleChange', self.handleSpeedChatStyleChange)
        listenForSCEvent(PSpeedChatGlobals.PSpeedChatQuestMsgEvent, self.handleQuestMsg)
        self.fsm = ClassicFSM.ClassicFSM('SpeedChat', [
         State.State('off', self.enterOff, self.exitOff, [
          'active']),
         State.State('active', self.enterActive, self.exitActive, [
          'off'])], 'off', 'off')
        self.fsm.enterInitialState()
        self.mode = 'AllChat'
        self.whisperId = None
        return

    def reparentTo(self, newParent):
        self.baseFrame.reparentTo(newParent)

    def delete(self):
        self.ignoreAll()
        self.emoteNoAccessPanel.destroy()
        del self.emoteNoAccessPanel
        self.speedChat.destroy()
        del self.speedChat
        del self.fsm

    def setWhisperTo(self, whisperId, toPlayer=False):
        self.whisperId = whisperId
        self.toPlayer = toPlayer

    def show(self):
        self.speedChat.show()
        self.speedChat.setPos(Point3(0.11, 0, 0.92))
        self.fsm.request('active')

    def hide(self):
        self.fsm.request('off')

    def enterOff(self):
        self.speedChat.hide()

    def exitOff(self):
        pass

    def requestMode(self, mode, whisperId=None):
        if mode == 'AllChat' and not base.chatAssistant.checkOpenSpeedChat():
            messenger.send('Chat-Failed open typed chat test')
            return
        else:
            if mode == 'PlayerWhisper':
                if not base.chatAssistant.checkWhisperSpeedChatPlayer(whisperId):
                    messenger.send('Chat-Failed player typed chat test')
                    return
            else:
                if mode == 'AvatarWhisper':
                    if not base.chatAssistant.checkWhisperSpeedChatAvatar(whisperId):
                        messenger.send('Chat-Failed avatar typed chat test')
                        return
        self.mode = mode
        self.whisperId = whisperId
        return

    def enterActive(self):

        def handleCancel():
            localAvatar.chatMgr.speedChatDone(success=False)

        self.acceptOnce('mouse1', handleCancel)

        def selectionMade(self=self):
            localAvatar.chatMgr.speedChatDone()

        self.terminalSelectedEvent = self.speedChat.getEventName(SpeedChatGlobals.SCTerminalSelectedEvent)
        self.accept(self.terminalSelectedEvent, selectionMade)
        self.speedChat.reparentTo(base.a2dBottomLeft, DGG.FOREGROUND_SORT_INDEX)
        pos = self.speedChat.getPos()
        self.speedChat.setWhisperMode(self.whisperId != None)
        self.speedChat.enter()
        return

    def exitActive(self):
        self.ignore('mouse1')
        self.ignore(self.terminalSelectedEvent)
        self.speedChat.exit()
        self.speedChat.detachNode()
        self.emoteNoAccessPanel.detachNode()

    def handleLinkedEmote(self, emoteId):
        if self.whisperId is None:
            lt = base.localAvatar
            lt.b_setEmoteState(emoteId, animMultiplier=lt.animMultiplier)
        return

    def sendChatByMode(self, msgType, textId, questInt=0, taskNum=0, questFlag=0):
        messenger.send('sentSpeedChat')
        if msgType == SPEEDCHAT_EMOTE:
            base.chatAssistant.sendAvatarOpenSpeedChat(msgType, textId)
            return
        if self.mode == 'PlayerWhisper':
            if questFlag:
                pass
            else:
                base.chatAssistant.sendPlayerWhisperSpeedChat(msgType, textId, self.whisperId)
        else:
            if self.mode == 'AvatarWhisper':
                if questFlag:
                    pass
                else:
                    base.chatAssistant.sendAvatarWhisperSpeedChat(msgType, textId, self.whisperId)
            else:
                if self.mode == 'GuildChat':
                    if questFlag:
                        pass
                    else:
                        base.chatAssistant.sendAvatarGuildSpeedChat(msgType, textId)
                else:
                    if self.mode == 'CrewChat':
                        if questFlag:
                            base.chatAssistant.sendAvatarCrewSCQuestChat(msgType, questInt, taskNum)
                        else:
                            base.chatAssistant.sendAvatarCrewSpeedChat(msgType, textId)
                    else:
                        if self.mode == 'ShipPVP':
                            if questFlag:
                                pass
                            else:
                                base.chatAssistant.sendAvatarShipPVPCrewSpeedChat(msgType, textId)
                        else:
                            if questFlag:
                                base.chatAssistant.sendAvatarSCQuestChat(msgType, questInt, taskNum)
                            else:
                                base.chatAssistant.sendAvatarOpenSpeedChat(msgType, textId)

    def handleStaticTextMsg(self, textId):
        if textId in PLocalizer.EmoteMessagesSelf:
            self.handleEmoteMsg(textId)
        else:
            if textId == PLocalizer.EMOTE_VALENTINES:
                self.handleEmoteMsg(textId)
            else:
                self.sendChatByMode(1, textId)
                self.hide()

    def handleCustomMsg(self, textId):
        self.sendChatByMode(3, textId)
        self.hide()

    def handleEmoteMsg(self, emoteId):
        sendText = True
        if emoteId == PLocalizer.EMOTE_VALENTINES:
            holidayId = PiratesGlobals.FLIRTEMOTE
            if holidayId not in PChatInputSpeedChat.holidayIdList:
                return
        if emoteId in OTPLocalizer.Emotes:
            sendText = localAvatar.requestEmote(emoteId)
        if sendText:
            if emoteId == PLocalizer.EMOTE_VALENTINES:
                emoteId = random.choice([PLocalizer.EMOTE_VALENTINES_A, PLocalizer.EMOTE_VALENTINES_B, PLocalizer.EMOTE_VALENTINES_C, PLocalizer.EMOTE_VALENTINES_D, PLocalizer.EMOTE_VALENTINES_E])
                self.sendChatByMode(1, emoteId)
            else:
                self.sendChatByMode(2, emoteId)
        self.hide()

    def handleEmoteNoAccess(self):
        if self.whisperId is None:
            self.emoteNoAccessPanel.setPos(0, 0, 0)
        else:
            self.emoteNoAccessPanel.setPos(0.37, 0, 0)
        self.emoteNoAccessPanel.reparentTo(aspect2d)
        return

    def handleEmoteNoAccessDone(self):
        self.emoteNoAccessPanel.detachNode()

    def handleQuestMsg(self, questInt, toNpcId, msgType, taskNum):
        self.sendChatByMode(msgType, '', questInt, taskNum, 1)
        self.hide()

    def handleSpeedChatStyleChange(self):
        nameKey, arrowColor, rolloverColor, frameColor = speedChatStyles[base.localAvatar.getSpeedChatStyleIndex()]
        newSCColorScheme = SCColorScheme(arrowColor=arrowColor, rolloverColor=rolloverColor, frameColor=frameColor)
        self.speedChat.setColorScheme(newSCColorScheme)

    def createSpeedChatObject(self, structure):
        if hasattr(self, 'speedChat'):
            self.speedChat.exit()
            self.speedChat.destroy()
            del self.speedChat
        self.speedChat = SpeedChat(structure=structure, backgroundModelName='models/gui/SpeedChatPanel', guiModelName='models/textureCards/speedchatIcons')
        self.speedChat.setScale(0.04)
        self.speedChat.setBin('gui-popup', 0)
        self.speedChat.setTopLevelOverlap(0.0)
        self.speedChat.setSubmenuOverlap(0.0)
        self.speedChat.setColorScheme(self.DefaultSCColorScheme)
        self.speedChat.finalizeAll()
        self.structure = structure

    def addFactoryMenu(self):
        fMenu = PSCFactoryMenu()
        fMenuHolder = SCMenuHolder(OTPLocalizer.SCMenuFactory, menu=fMenu)
        self.speedChat[2:2] = [fMenuHolder]

    def removeFactoryMenu(self):
        fMenu = self.speedChat[2]
        del self.speedChat[2]
        fMenu.destroy()

    def addCogMenu(self, indices):
        fMenu = PSCCogMenu(indices)
        fMenuHolder = SCMenuHolder(OTPLocalizer.SCMenuCog, menu=fMenu)
        self.speedChat[2:2] = [fMenuHolder]

    def removeCogMenu(self):
        fMenu = self.speedChat[2]
        del self.speedChat[2]
        fMenu.destroy()

    def addEmote(self, emoteId):
        emote = PLocalizer.emotes.get(emoteId)
        emote_group = emote[3]
        if emote is None:
            return
        for id in range(1, len(self.structure[self.emoteMenuIdx])):
            if self.structure[self.emoteMenuIdx][id][0] == emote_group:
                self.structure[self.emoteMenuIdx][id].append(emoteId)

        self.createSpeedChatObject(self.structure)
        return
# okay decompiling .\pirates\chat\PChatInputSpeedChat.pyc
