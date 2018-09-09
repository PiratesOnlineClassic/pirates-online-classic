import random
import string

from direct.fsm.FSM import FSM
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from otp.chat.ChatGlobals import *
from otp.otpbase import OTPLocalizer
from otp.speedchat import SCDecoders
from panda3d.core import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesgui.ChatBar import ChatBar


class ChatPanel(DirectFrame, FSM):

    NumVisible = 10
    WrapWidth = 21
    FadeTime = 0.3
    TextFadeDelay = 120
    TextFadeTime = 5

    def __init__(self, chatManager, chatEntry, whiteListEntry, speedEntry):
        optiondefs = (
         ('relief', None, None), ('state', DGG.NORMAL, self.setState), ('frameSize', (0, 0.9, 0, 0.6), None), ('frameColor', (1, 0, 1, 0.2), None))
        self.defineoptions({}, optiondefs)
        DirectFrame.__init__(self, parent=base.a2dBottomLeft)
        self.initialiseoptions(ChatPanel)
        FSM.__init__(self, 'ChatPanel')
        base.chatPanel = self
        self.chatManager = chatManager
        self.index = 0
        self.wrappedText = []
        self.wordWrapper = TextNode('wrapper')
        self.wordWrapper.setFont(PiratesGlobals.getInterfaceFont())
        self.wordWrapper.setWordwrap(self.WrapWidth)
        self.wordWrapper.setTabWidth(1.0)
        self.fadeIval = None
        self.fadeTextIval = None
        self.preferredMode = 'Short'
        self.setupGui()
        self.chatBar = ChatBar(parent=self, chatMgr=chatManager, chatEntry=chatEntry, whiteListEntry=whiteListEntry)
        self.checkEmotes()
        self.accept('NewOpenMessage', self.__handleOpenMessage)
        return

    def setupGui(self):
        self.cleanupGui()
        if hasattr(self, 'chatBar'):
            self.chatBar.detachNode()
        self.get_children().detach()
        guib = loader.loadModel('models/gui/chat_frame_b')
        guic = loader.loadModel('models/gui/chat_frame_c')
        charGui = loader.loadModel('models/gui/char_gui')
        tGui = loader.loadModel('models/gui/triangle')
        self.hideNode = self.attachNewNode('hideNode')
        cm = CardMaker('shortBg')
        cm.setColor(0, 0, 0, 1)
        cm.setFrame(0.005, 0.895, 0.09, 0.595)
        self.shortBg = self.hideNode.attachNewNode(cm.generate())
        self.shortBg.setTransparency(1)
        self.shortBg.setColor(0, 0, 0, 1)
        self.shortBg.flattenStrong()
        self.shortBg.setColorScale(1, 1, 1, 0)
        self.shortBorder = self.hideNode.attachNewNode('shortBorder')
        top = guib.find('**/pPlane8').copyTo(self.shortBorder)
        top.setZ(-0.75)
        mid = guib.find('**/pPlane9').copyTo(self.shortBorder)
        mid.setScale(1, 1, 0.68)
        mid.setZ(-0.4)
        guib.find('**/pPlane10').copyTo(self.shortBorder)
        top = guib.find('**/pPlane26').copyTo(self.shortBorder)
        top.setZ(-0.75)
        mid = guib.find('**/pPlane27').copyTo(self.shortBorder)
        mid.setScale(1, 1, 0.68)
        mid.setZ(-0.4)
        self.shortBorder.setScale(0.2)
        self.shortBorder.setPos(0.5, 0, 0.375)
        self.shortBorder.flattenStrong()
        buttonGeom = NodePath('Close')
        guib.find('**/pPlane30').copyTo(buttonGeom)
        guib.find('**/pPlane31').copyTo(buttonGeom)
        guib.find('**/pPlane32').copyTo(buttonGeom)
        buttonGeom.flattenStrong()
        self.sCloseButton = DirectButton(parent=self.shortBorder, relief=None, frameColor=(1,
                                                                                           1,
                                                                                           1,
                                                                                           1), pad=(-0.02, -0.02), borderWidth=(0,
                                                                                                                                0), geom=buttonGeom, pos=(0.5,
                                                                                                                                                          0,
                                                                                                                                                          0.225), scale=0.2, rolloverSound=None, command=self.chatManager.deactivateChat)
        buttonGeom = NodePath('Max')
        guib.find('**/pPlane22').copyTo(buttonGeom)
        guib.find('**/pPlane23').copyTo(buttonGeom)
        buttonGeom.flattenStrong()
        self.maxButton = DirectButton(parent=self.shortBorder, relief=None, frameColor=(1,
                                                                                        1,
                                                                                        1,
                                                                                        1), pad=(-0.02, -0.02), borderWidth=(0,
                                                                                                                             0), geom=buttonGeom, pos=(0.5,
                                                                                                                                                       0,
                                                                                                                                                       0.225), scale=0.2, rolloverSound=None, command=self.request, extraArgs=['Tall'])
        cm.setName('tallBg')
        cm.setFrame(0.005, 0.895, 0.09, 1.36)
        self.tallBg = self.hideNode.attachNewNode(cm.generate())
        self.tallBg.setColor(0, 0, 0, 1)
        self.tallBg.setTransparency(1)
        self.tallBg.flattenStrong()
        self.tallBg.setColorScale(1, 1, 1, 0)
        self.tallBorder = self.hideNode.attachNewNode('tallBorder')
        guic.find('**/pPlane8').copyTo(self.tallBorder)
        guic.find('**/pPlane9').copyTo(self.tallBorder)
        guic.find('**/pPlane10').copyTo(self.tallBorder)
        guic.find('**/pPlane26').copyTo(self.tallBorder)
        guic.find('**/pPlane27').copyTo(self.tallBorder)
        self.tallBorder.setScale(0.2)
        self.tallBorder.setPos(0.5, 0, 0.375)
        self.tallBorder.flattenStrong()
        buttonGeom = NodePath('Close')
        guic.find('**/pPlane30').copyTo(buttonGeom)
        guic.find('**/pPlane31').copyTo(buttonGeom)
        guic.find('**/pPlane32').copyTo(buttonGeom)
        buttonGeom.flattenStrong()
        self.tCloseButton = DirectButton(parent=self.tallBorder, relief=None, frameColor=(1,
                                                                                          1,
                                                                                          1,
                                                                                          1), pad=(-0.02, -0.02), borderWidth=(0,
                                                                                                                               0), geom=buttonGeom, pos=(0.5,
                                                                                                                                                         0,
                                                                                                                                                         0.375), scale=0.2, rolloverSound=None, command=self.chatManager.deactivateChat)
        buttonGeom = NodePath('Min')
        guic.find('**/pPlane28').copyTo(buttonGeom)
        guic.find('**/pPlane29').copyTo(buttonGeom)
        buttonGeom.flattenStrong()
        self.minButton = DirectButton(parent=self.tallBorder, relief=None, frameColor=(1,
                                                                                       1,
                                                                                       1,
                                                                                       1), pad=(-0.02, -0.02), borderWidth=(0,
                                                                                                                            0), geom=buttonGeom, pos=(0.548,
                                                                                                                                                      0,
                                                                                                                                                      0.375), scale=0.2, rolloverSound=None, command=self.request, extraArgs=['Short'])
        self.chatTextRender = TextNode('chatTextRender')
        self.chatTextRender.setFont(PiratesGlobals.getInterfaceFont())
        self.chatTextRender.setShadowColor(0, 0, 0, 0.8)
        self.chatTextRender.setShadow(0.08, 0.08)
        self.chatDisplayNP = self.hideNode.attachNewNode('chatDisplay')
        self.chatDisplayNP.setScale(0.035)
        self.chatDisplayNP.setColorScale(1, 1, 1, 1)
        self.chatDisplayNP.showThrough()
        self.slider = DirectScrollBar(parent=self, relief=None, manageButtons=0, resizeThumb=0, frameSize=(-0.1, 0.1, -0.08, 0.08), image=charGui.find('**/chargui_slider_small'), image_scale=(0.18,
                                                                                                                                                                                                0.035,
                                                                                                                                                                                                0.07), image_hpr=(0,
                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                  90), thumb_image=(charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over')), thumb_image_scale=0.06, thumb_relief=None, decButton_pos=Vec3(0, 0, -0.0825), decButton_image=(tGui.find('**/triangle'), tGui.find('**/triangle_down'), tGui.find('**/triangle_over')), decButton_image_hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    90), decButton_scale=(0.08,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          1.0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          0.125), decButton_image_scale=0.06, decButton_relief=None, incButton_pos=Vec3(0.00025, 0, 0.0825), incButton_image=(tGui.find('**/triangle'), tGui.find('**/triangle_down'), tGui.find('**/triangle_over')), incButton_image_hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            -90), incButton_scale=(0.08,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   1.0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   0.125), incButton_image_scale=0.06, incButton_relief=None, scale=5.7, pos=(0.052,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              0.7), value=0, range=(0, self.NumVisible), scrollSize=1, pageSize=1, orientation=DGG.VERTICAL_INVERTED, command=self.scrollList)
        self.slider.hide()
        self.slider.setName('chatPanel.slider')
        if hasattr(self, 'chatBar'):
            self.chatBar.reparentTo(self)
        self.request('Standby')
        self.updateDisplay()
        return

    def cleanupGui(self):
        try:
            self.sCloseButton.destroy()
            self.tCloseButton.destroy()
            self.minButton.destroy()
            self.maxButton.destroy()
        except AttributeError:
            pass

        self.shortBg = None
        self.shortBorder = None
        self.tallBg = None
        self.tallBorder = None
        self.sCloseButton = None
        self.maxButton = None
        self.tCloseButton = None
        self.minButton = None
        self.chatTextRender = None
        self.chatDisplayNP = None
        self.slider = None
        return

    def destroy(self):
        self.stopFadeIval()
        self.stopFadeTextIval()
        self.stopFadeTextTimer()
        self.slider.destroy()
        DirectFrame.destroy(self)
        self.cleanupGui()
        self.chatManager = None
        base.chatPanel = None
        return

    def activateAllChat(self):
        self.requestPreferredMode()
        self.chatBar.request('All')

    def activateCrewChat(self):
        self.requestPreferredMode()
        self.chatBar.request('Crew')

    def activateGuildChat(self):
        self.requestPreferredMode()
        self.chatBar.request('Guild')

    def activateShipPVPChat(self):
        self.requestPreferredMode()
        self.chatBar.request('ShipPVP')

    def activateWhisperChat(self, whisperId, toPlayer=False):
        self.requestPreferredMode()
        name = base.chatAssistant.findName(whisperId)
        self.chatBar.request('Whisper', name, whisperId)

    def deactivateChat(self):
        self.request('Standby')
        self.chatBar.request('Hidden')

    def updateState(self, state):
        self['state'] = state

    def setState(self):
        DirectFrame.setState(self)
        if hasattr(self, 'sCloseButton'):
            self.sCloseButton['state'] = self['state']
            self.maxButton['state'] = self['state']
            self.tCloseButton['state'] = self['state']
            self.minButton['state'] = self['state']
            self.slider['state'] = self['state']

    def startFadeInIval(self):
        self.stopFadeIval()
        self.fadeIval = Parallel(Func(self.updateState, DGG.NORMAL), Func(self.hideNode.show), self.shortBg.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 0.75), blendType='easeOut'), self.shortBorder.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 1), blendType='easeOut'), self.tallBg.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 0.75), blendType='easeOut'), self.tallBorder.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 1), blendType='easeOut'), self.slider.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 1), blendType='easeOut'))
        self.fadeIval.start()

    def startFadeOutIval(self):
        self.stopFadeIval()
        self.fadeIval = Parallel(Func(self.updateState, DGG.DISABLED), self.shortBg.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 0), blendType='easeIn'), self.shortBorder.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 0), blendType='easeIn'), self.tallBg.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 0), blendType='easeIn'), self.tallBorder.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 0), blendType='easeIn'), self.slider.colorScaleInterval(self.FadeTime, Vec4(1, 1, 1, 0), blendType='easeIn'), Sequence(Wait(self.FadeTime), Func(self.hideNode.hide)))
        self.fadeIval.start()

    def stopFadeIval(self):
        if self.fadeIval:
            self.fadeIval.pause()
        self.fadeIval = None
        return

    def startFadeTextIval(self):
        self.stopFadeTextIval()
        self.fadeTextIval = Sequence()
        self.fadeTextIval.append(self.chatDisplayNP.colorScaleInterval(self.TextFadeTime, Vec4(1, 1, 1, 0)))
        self.fadeTextIval.append(Func(self.chatDisplayNP.hide))
        self.fadeTextIval.start()

    def stopFadeTextIval(self):
        if self.fadeTextIval:
            self.fadeTextIval.pause()
        self.fadeTextIval = None
        return

    def unfadeText(self):
        self.stopFadeTextIval()
        self.chatDisplayNP.setColorScale(1, 1, 1, 1)
        self.chatDisplayNP.showThrough()

    def startFadeTextTimer(self):
        self.stopFadeTextTimer()
        taskMgr.doMethodLater(self.TextFadeDelay, self.startFadeTextIval, 'ChatPanel-fadeText', [])

    def stopFadeTextTimer(self):
        taskMgr.remove('ChatPanel-fadeText')

    def requestPreferredMode(self):
        self.request(self.preferredMode)

    def defaultFilter(self, request, args):
        if self.getCurrentOrNextState() == request:
            return
        else:
            return FSM.defaultFilter(self, request, args)
        return

    def enterStandby(self):
        messenger.send('chatPanelClose')
        self.startFadeOutIval()
        self.startFadeTextTimer()
        self.NumVisible = 10
        (self.chatDisplayNP.setPos(0.09, 0, 0.52),)
        self.index = 0
        self.slider['value'] = self.index
        self.updateDisplay()

    def exitStandby(self):
        messenger.send('chatPanelOpen')
        self.startFadeInIval()
        self.stopFadeTextTimer()
        self.unfadeText()

    def enterShort(self):
        messenger.send('chatPanelMin')
        self.slider.hide()
        self.shortBg.show()
        self.shortBorder.show()
        self.tallBg.hide()
        self.tallBorder.hide()
        self.chatDisplayNP.setPos(0.09, 0, 0.52)
        self.preferredMode = 'Short'
        self.NumVisible = 10
        self.index = 0
        self.slider['value'] = self.index
        self.updateDisplay()

    def exitShort(self):
        pass

    def enterTall(self):
        messenger.send('chatPanelMax')
        self.tallBg.show()
        self.tallBorder.show()
        self.shortBg.hide()
        self.shortBorder.hide()
        self.slider.show()
        self.chatDisplayNP.setPos(0.09, 0, 1.29)
        self.preferredMode = 'Tall'
        self.NumVisible = 32
        self.index = 0
        self.slider['value'] = self.index
        self.updateDisplay()

    def exitTall(self):
        pass

    def decodeOpenMessage(self, message):
        chatCode = None
        chatString = ''
        if message.getType() in (
        TYPEDCHAT, SPEEDCHAT_NORMAL, SPEEDCHAT_EMOTE, SPEEDCHAT_CUSTOM, AVATAR_UNAVAILABLE, GMCHAT):
            whisper = message.getWhisper()
            avName = message.getName()
            if message.getType() == SPEEDCHAT_NORMAL:
                someMessage = SCDecoders.decodeSCStaticTextMsg(message.getBody())
            elif message.getType() == SPEEDCHAT_EMOTE:
                from pirates.piratesbase import PLocalizer
                if message.sentRatherThanReceived:
                    someMessage = PLocalizer.EmoteMessagesSelf.get(message.getBody(), None)
                    if someMessage is None:
                        self.notify.warning('Invalid emote ID: %s' % message.getBody())
                        return 'Invalid emote ID: %s'

                else:
                    someMessage = PLocalizer.EmoteMessagesThirdPerson[message.getBody()] % avName
                    if someMessage is None:
                        self.notify.warning('Invalid emote ID: %s' % message.getBody())
                        return 'Invalid emote ID: %s'

            elif message.getType() == SPEEDCHAT_CUSTOM:
                someMessage = SCDecoders.decodeSCCustomMsg(message.getBody(), message.getName())
            else:
                someMessage = message.getBody()
            if message.getWhisper():
                if message.getSentRatherThanReceived():
                    avName = OTPLocalizer.WhisperToFormatName % avName
                else:
                    avName = OTPLocalizer.WhisperFromFormatName % avName

            if message.getType() in (SPEEDCHAT_EMOTE, AVATAR_UNAVAILABLE):
                fullMsg = someMessage
            else:
                fullMsg = '%s: %s' % (avName, someMessage)
            self.wordWrapper.setText(fullMsg)
            wrappedText = self.wordWrapper.getWordwrappedText().split('\n')
            tab = '    '
            for i in range(len(wrappedText)):
                if i == 0:
                    if whisper:
                        formattedName = ''
                        formattedMsg = '\x01CPOrange\x01' + wrappedText[0] + '\x02'
                        if message.getType() in (AVATAR_UNAVAILABLE,):
                            formattedMsg = '\x01slant\x01%s\x02' % (formattedMsg,)

                    elif message.getType() == GMCHAT:
                        formattedName = ''
                        formattedMsg = '\x01CPGoldGM\x01' + wrappedText[0] + '\x02'
                    else:
                        formattedName = ''
                        formattedMsg = wrappedText[0]
                    wrappedText[0] = formattedName + formattedMsg
                elif whisper:
                    wrappedText[i] = '%s%s%s%s' % ('\x01CPOrange\x01', tab, wrappedText[i], '\x02')
                elif message.getType() == GMCHAT:
                    wrappedText[i] = '%s%s%s%s' % ('\x01CPGoldGM\x01', tab, wrappedText[i], '\x02')
                else:
                    wrappedText[i] = '%s%s%s%s' % ('\x01CPWhite\x01', tab, wrappedText[i], '\x02')
                if i < len(wrappedText) - 1:
                    wrappedText[i] += '\n'
                    continue

            for text in wrappedText:
                chatString += text

        else:
            someMessage = '%s' % message.getBody()
            if message.getType() == GUILDCHAT:
                chatCode = 'CPLtBlue'
            elif message.getType() == GAMECHAT:
                chatCode = 'CPGreenSlant'
            elif message.getType() == PARTYCHAT:
                chatCode = 'CPPurple'
            elif message.getType() == SYSTEMCHAT:
                chatCode = 'CPGoldSlant'
            elif message.getType() == GUILD_UPDATE:
                chatCode = 'CPLtBlue'
            elif message.getType() == FRIEND_UPDATE:
                chatCode = 'CPYellow'
            elif message.getType() == CREW_UPDATE:
                chatCode = 'CPPurple'
            elif message.getType() == SHIPPVPCHAT:
                chatCode = 'CPLtGold'
            else:
                print 'Error no type'
            self.wordWrapper.setText(someMessage)
            wrappedText = self.wordWrapper.getWordwrappedText().split('\n')
            tab = '    '
            for i in range(len(wrappedText)):
                if i > 0:
                    wrappedText[i] = '%s%s' % (tab, wrappedText[i])

                if chatCode:
                    wrappedText[i] = '%s%s%s%s%s' % ('\x01', chatCode, '\x01', wrappedText[i], '\x02')

                if i < len(wrappedText) - 1:
                    wrappedText[i] += '\n'
                    continue

            for text in wrappedText:
                chatString += text

        return chatString

    def putText(self, startLine, numLines):
        displayText = []
        someText = base.chatAssistant.getOpenText(self.NumVisible, startLine)
        lineHeight = PiratesGlobals.getInterfaceFont().getLineHeight()
        renderedLines = []
        for line in someText:
            if not hasattr(line, 'renderedLines'):
                msg = self.decodeOpenMessage(line)
                line.renderedLines = []
                for mline in msg.split('\n'):
                    self.chatTextRender.setText(mline)
                    line.renderedLines.append(self.chatTextRender.generate())

            renderedLines = line.renderedLines + renderedLines
            if len(renderedLines) >= self.NumVisible:
                break

        renderedLines = renderedLines[-self.NumVisible:]
        self.chatDisplayNP.getChildren().detach()
        z = -lineHeight * (self.NumVisible - len(renderedLines))
        for rline in renderedLines:
            np = self.chatDisplayNP.attachNewNode(rline)
            np.setZ(z)
            z -= lineHeight

        self.updateRange()

    def __handleOpenMessage(self):
        self.index = 0
        self.updateDisplay()
        self.unfadeText()
        if self.getCurrentOrNextState() == 'Standby':
            self.startFadeTextTimer()

    def updateDisplay(self):
        if hasattr(base, 'chatAssistant'):
            self.putText(self.index, self.NumVisible)

    def updateRange(self):
        numLines = base.chatAssistant.getSizeOpenText()
        if self.getCurrentOrNextState() != 'Tall':
            self.index = 0
            return
        if numLines > self.NumVisible:
            if self.getCurrentOrNextState() == 'Tall':
                self.slider.show()
            maxRange = numLines - self.NumVisible
            self.slider['range'] = (0, maxRange)
            self.index = min(self.index, self.slider['range'][1])
            self.index = max(self.index, self.slider['range'][0])
        else:
            self.slider.hide()
            self.index = 0

    def scrollList(self):
        index = int(self.slider.getValue())
        if self.index != index:
            self.index = index
            self.updateDisplay()

    def enableCrewChat(self):
        self.chatBar.refreshTabStates()

    def disableCrewChat(self):
        self.chatBar.refreshTabStates()

    def enableGuildChat(self):
        self.chatBar.refreshTabStates()

    def disableGuildChat(self):
        self.chatBar.refreshTabStates()

    def disableShipPVPChat(self):
        self.chatBar.refreshTabStates()

    def enableShipPVPChat(self):
        self.chatBar.refreshTabStates()

    def enableWhiteListChat(self):
        self.chatBar.enableWhiteListChat()

    def disableWhiteListChat(self):
        self.chatBar.disableWhiteListChat()

    def checkEmotes(self):
        for id in PLocalizer.emotes.keys():
            pass

        for id in PLocalizer.EmoteCommands.values():
            pass

        for id in PLocalizer.nonMenuEmoteAnimations.keys():
            pass

    def hide(self):
        NodePath.hide(self)
        self.chatDisplayNP.hide()

    tpMgr = TextPropertiesManager.getGlobalPtr()
    CPYellow = tpMgr.getProperties('yellow')
    CPYellow.setTextColor(*PiratesGuiGlobals.TextFG13)
    tpMgr.setProperties('CPYellow', CPYellow)
    CPGoldSlant = tpMgr.getProperties('gold')
    CPGoldSlant.setSlant(0.2)
    tpMgr.setProperties('CPGoldSlant', CPGoldSlant)
    CPGoldGM = tpMgr.getProperties('gold')
    CPGoldGM.setTextColor(*PiratesGuiGlobals.TextFG17)
    tpMgr.setProperties('CPGoldGM', CPGoldGM)
    CPGreenSlant = tpMgr.getProperties('green')
    CPGreenSlant.setTextColor(*PiratesGuiGlobals.TextFG4)
    CPGreenSlant.setSlant(0.2)
    tpMgr.setProperties('CPGreenSlant', CPGreenSlant)
    CPWhite = tpMgr.getProperties('white')
    tpMgr.setProperties('CPWhite', CPWhite)
    CPLtBlue = tpMgr.getProperties('blue')
    CPLtBlue.setTextColor(*PiratesGuiGlobals.TextFG5)
    tpMgr.setProperties('CPLtBlue', CPLtBlue)
    CPPurple = tpMgr.getProperties('purple')
    CPPurple.setTextColor(*PiratesGuiGlobals.TextFG12)
    tpMgr.setProperties('CPPurple', CPPurple)
    CPOrange = tpMgr.getProperties('orange')
    CPOrange.setTextColor(*PiratesGuiGlobals.TextFG11)
    tpMgr.setProperties('CPOrange', CPOrange)
    CPMaroon = tpMgr.getProperties('maroon')
    CPMaroon.setTextColor(*PiratesGuiGlobals.TextFG15)
    tpMgr.setProperties('CPMaroon', CPMaroon)
    CPLtGold = tpMgr.getProperties('lightGold')
    CPLtGold.setTextColor(*PiratesGuiGlobals.TextFG14)
    tpMgr.setProperties('CPLtGold', CPLtGold)
    del tpMgr
