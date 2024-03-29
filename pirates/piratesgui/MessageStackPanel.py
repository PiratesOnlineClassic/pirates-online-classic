from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import report, Functor
from otp.otpgui import OTPDialog
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesbase import PLocalizer
from pirates.minigame import PlayingCardGlobals
from pirates.piratesbase import CollectionMap
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.reputation import ReputationGlobals

class StackMessage(BorderFrame):
    guiLoaded = False
    corner = None
    popupSfx = None
    lootSfx = None
    CoinTex = None
    CrateTex = None
    ChestTex = None
    RoyalChestTex = None
    SkillIcons = None
    WeaponIcons = None
    TreasureGui = None
    QuestTex = None
    WeaponTex = None
    AdminTex = None
    HatTex = None
    TattooTex = None
    
    def __init__(self, parent = None, **kwargs):
        self.loadModels()
        self.cornerGeom = None
        self.text = None
        self.icon = None
        if not StackMessage.popupSfx:
            StackMessage.popupSfx = loader.loadSfx('audio/sfx_gui_zoom-io.mp3')
            StackMessage.lootSfx = loader.loadSfx('audio/treasure_hit_1.mp3')
            StackMessage.lootSfx.setVolume(0.75)
        
        optiondefs = (('relief', None, None), ('frameSize', (0, 0.8, -0.18, 0), None), ('state', DGG.DISABLED, None), ('time', 7, None), ('priority', 0, None), ('suffix', '_b', None), ('borderScale', 0.7, None), ('icon', (), self.setIcon), ('buttonStyle', None, None), ('noCallback', None, None), ('yesCallback', None, None), ('cancelCallback', None, None))
        self.defineoptions(kwargs, optiondefs, dynamicGroups = ())
        BorderFrame.__init__(self, parent, **kwargs)
        self.initialiseoptions(StackMessage)
        self.ival = None
        self.cornerGeom = self.corner.copyTo(self)
        self.cornerGeom.setScale(0.4)
        self.cornerGeom.setPos(0.068, 0, -0.066)
        self.cornerGeom.setColorScale(*PiratesGuiGlobals.TextFG1)
        self.setTransparency(True)

    def __cmp__(self, other):
        if other:
            return cmp(other['priority'], self['priority'])
        else:
            return -1

    def __hash__(self):
        return id(self)

    def destroy(self, autoDestroy = 1):
        if self.ival:
            self.ival.pause()
            self.ival = None
        
        if autoDestroy:
            BorderFrame.destroy(self)

    def loadModels(self):
        if StackMessage.guiLoaded:
            return
        
        StackMessage.TopLevel = gui = loader.loadModel('models/gui/toplevel_gui')
        StackMessage.corner = gui.find('**/topgui_general_corner')
        StackMessage.CoinTex = gui.find('**/treasure_w_coin*')
        StackMessage.SkillTex = gui.find('**/topgui_icon_skills')
        StackMessage.QuestTex = gui.find('**/topgui_icon_journal')
        StackMessage.WeaponTex = gui.find('**/topgui_icon_weapons')
        StackMessage.FriendTex = gui.find('**/friend_button_over')
        StackMessage.LookoutTex = gui.find('**/telescope_button')
        card = loader.loadModel('models/textureCards/icons')
        StackMessage.CrateTex = card.find('**/icon_crate*')
        StackMessage.ChestTex = card.find('**/icon_chest*')
        StackMessage.RoyalChestTex = card.find('**/topgui_icon_ship_chest03*')
        StackMessage.HatTex = card.find('**/icon_bandana')
        StackMessage.SkillIcons = loader.loadModel('models/textureCards/skillIcons')
        StackMessage.PorkChunkTex = StackMessage.SkillIcons.find('**/pir_t_gui_pot_porkTonic')
        StackMessage.TreasureGui = loader.loadModel('models/gui/treasure_gui')
        StackMessage.WeaponIcons = loader.loadModel('models/textureCards/weapon_icons')
        StackMessage.guiLoaded = True
        tailorIcons = loader.loadModel('models/textureCards/tailorIcons')
        StackMessage.HatIcon = tailorIcons.find('**/icon_shop_tailor_hat')
        adminGui = loader.loadModel('models/gui/chat_frame_skull')
        StackMessage.AdminTex = adminGui.find('**/chat_frame_skull_over')
        tattooGui = loader.loadModel('models/textureCards/shopCoins')
        StackMessage.TattooTex = tattooGui.find('**/shopCoin_tattoo')

    def setText(self):
        BorderFrame.setText(self)
        lines = self.component('text0').textNode.getHeight()
        textSpace = (0.0348 * lines - 0.0276) * self['text_scale'][1] / 0.035
        self['frameSize'] = (0, 0.8, -0.028 - 0.044 - 0.044 - max(0.042, textSpace), 0)

    def setIcon(self):
        if self.icon:
            self.icon.destroy()
            self.icon = None
        
        icon = self['icon']
        if icon:
            (category, detail) = icon
            imagePos = (0.1, 0, -0.08)
            extraArgs = []
            if category == 'gold':
                image = StackMessage.CoinTex
                imageScale = 0.27
                command = localAvatar.guiMgr.showCollectionMain
            elif category == 'skills':
                image = StackMessage.SkillTex
                imageScale = 0.27
                command = localAvatar.guiMgr.showSkillPage
            elif category == 'reputation':
                repId = detail
                if repId == InventoryType.OverallRep:
                    model = StackMessage.TopLevel
                    imageScale = 0.09
                elif repId == InventoryType.SailingRep:
                    model = StackMessage.SkillIcons
                    imageScale = 0.12
                else:
                    model = StackMessage.WeaponIcons
                    imageScale = 0.12
                asset = ReputationGlobals.RepIcons.get(repId)
                image = model.find('**/%s' % asset)
                command = localAvatar.guiMgr.showSkillPage
            elif category == 'card':
                suit = PlayingCardGlobals.getSuit(detail)
                rank = PlayingCardGlobals.getRank(detail)
                image = PlayingCardGlobals.getImage('standard', suit, rank)
                imageScale = 0.2
                command = localAvatar.guiMgr.showCollectionMain
            elif category == 'collect':
                name = CollectionMap.Assets[detail]
                image = StackMessage.TreasureGui.find('**/%s*' % name)
                imageScale = 0.35
                command = localAvatar.guiMgr.showCollectionMain
            elif category == 'quests':
                image = StackMessage.QuestTex
                imageScale = 0.18
                command = localAvatar.guiMgr.showQuestPanel
            elif category == 'friends':
                image = StackMessage.FriendTex
                imageScale = 0.15
                command = localAvatar.guiMgr.socialPanel.show
            elif category == 'lookout':
                image = StackMessage.LookoutTex
                imageScale = 0.18
                command = localAvatar.guiMgr.showLookoutPanel
            elif category == 'weapon':
                image = StackMessage.WeaponTex
                imageScale = 0.12
                command = localAvatar.guiMgr.showWeaponPanel
            elif category == 'loot':
                if detail == ItemId.CARGO_CRATE:
                    image = StackMessage.CrateTex
                elif detail == ItemId.CARGO_CHEST:
                    image = StackMessage.ChestTex
                elif detail == ItemId.CARGO_SKCHEST:
                    image = StackMessage.RoyalChestTex
                elif detail == ItemId.GOLD:
                    StackMessage.CoinTex
                else:
                    StackMessage.CoinTex
                
                imageScale = 0.35
                command = localAvatar.guiMgr.showShipPanel
            elif category == 'admin':
                image = StackMessage.AdminTex
                imageScale = 0.3
                command = None
            elif category == 'hat':
                image = StackMessage.HatIcon
                imageScale = 0.13
                imagePos = (0.095, 0, -0.09)
                command = localAvatar.guiMgr.showNonPayer
                extraArgs = [
                    'Restricted_Message_Stack_Panel',
                    10]
            elif category == 'tattoo':
                image = StackMessage.TattooTex
                imageScale = 0.12
                imagePos = (0.1, 0, -0.1)
                command = localAvatar.guiMgr.showNonPayer
                extraArgs = [
                    None,
                    10]
            elif category == 'pork':
                image = StackMessage.PorkChunkTex
                imageScale = 0.1
                imagePos = (0.1, 0, -0.08)
                command = localAvatar.guiMgr.showNonPayer
            
            self.icon = DirectButton(parent = self, relief = None, image = image, image_scale = imageScale, pos = imagePos, command = command, extraArgs = extraArgs)

    def getIval(self):
        return self.ival

    def createIval(self, fadeTime, doneFunc = None):
        if not self.ival:
            baseColor = Vec4(1)
            baseTransp = VBase4(baseColor[0], baseColor[1], baseColor[2], 0)
            self.ival = Sequence(LerpColorScaleInterval(self, fadeTime, baseColor, startColorScale = baseTransp, blendType = 'easeIn'), Wait(max(0.0, self['time'] - 2 * fadeTime)), LerpColorScaleInterval(self, fadeTime, baseTransp))
            if doneFunc:
                self.ival.append(Func(doneFunc))

        return self.ival

    def getHeight(self):
        frameSize = self['frameSize']
        if not frameSize:
            frameSize = self.guiItem.getFrame()
        
        return frameSize[3] - frameSize[2]



class ModalStackMessage(StackMessage):
    
    def __init__(self, parent = None, **kwargs):
        StackMessage.__init__(self, parent, **kwargs)
        self.initialiseoptions(ModalStackMessage)
        self.doneFunc = None
        self.fadeTime = 0
        self.setupButtons()
    
    def destroy(self, autoDestroy = 1):
        self.doneFunc = None
        if self['buttonStyle'] == OTPDialog.YesNo:
            self.yesButton.destroy()
            self.noButton.destroy()
        elif self['buttonStyle'] == OTPDialog.CancelOnly:
            self.cancelButton.destroy()
        
        StackMessage.destroy(self, autoDestroy)
    
    def setupButtons(self):
        if self['buttonStyle'] == OTPDialog.YesNo:
            self.yesButton = GuiButton(parent = self, image_scale = (0.22, 0.22, 0.15), pos = (0.275, 0, -.1), text = PLocalizer.DialogYes, command = self.handleYes)
            self.noButton = GuiButton(parent = self, image_scale = (0.22, 0.22, 0.15), pos = (0.55, 0, -.1), text = PLocalizer.DialogNo, command = self.handleNo)
            self.adjustFrameForButtons()
        elif self['buttonStyle'] == OTPDialog.CancelOnly:
            lookoutUI = loader.loadModel('models/gui/lookout_gui')
            self.cancelButton = DirectButton(parent = self, relief = None, image = (lookoutUI.find('**/lookout_close_window'), lookoutUI.find('**/lookout_close_window_down'), lookoutUI.find('**/lookout_close_window_over'), lookoutUI.find('**/lookout_close_window_disabled')), pos = (0.75, 0, -.05), scale = 0.12, command = self.handleCancel)

    def adjustFrameForButtons(self):
        zOffset = self['frameSize'][2]
        self['frameSize'] = (self['frameSize'][0], self['frameSize'][1], zOffset - 0.06, self['frameSize'][3])
        self.yesButton.setZ(zOffset)
        self.noButton.setZ(zOffset)

    def __removeIval(self):
        self.ival.pause()
        self.ival = None
    
    def createIval(self, fadeTime, doneFunc = None):
        StackMessage.createIval(self, fadeTime, doneFunc)
        self.fadeTime = fadeTime
        self.doneFunc = doneFunc
        return self.ival

    def messageDone(self, quick = False):
        if self.ival:
            self.ival.pause()
        
        if quick:
            fadeTime = 0
        else:
            fadeTime = self.fadeTime
        baseColor = Vec4(1)
        baseTransp = VBase4(baseColor[0], baseColor[1], baseColor[2], 0)
        self.ival = Sequence(LerpColorScaleInterval(self, fadeTime, baseTransp))
        if self.doneFunc:
            self.ival.append(Func(self.doneFunc))

    def handleNo(self):
        if self['noCallback']:
            self['noCallback']()
        
        self.messageDone()

    def handleYes(self):
        if self['yesCallback']:
            self['yesCallback']()
        
        self.messageDone()

    def handleCancel(self):
        if self['cancelCallback']:
            self['cancelCallback']()
        
        self.messageDone()



class MessageStackPanel(DirectFrame):
    popupSfx = None
    
    def __init__(self, parent = None, **kwargs):
        optiondefs = (('relief', None, None), ('state', DGG.DISABLED, None), ('maxMessages', 3, self.setMaxMessages), ('messageBorder', 0.005, self.setMessageBorder), ('posLerpTime', 0.25, self.setPosLerpTime), ('fadeLerpTime', 0.25, self.setFadeLerpTime))
        self.defineoptions(kwargs, optiondefs, dynamicGroups = ('posLerpTime', 'fadeLerpTime', 'messageBorder'))
        DirectFrame.__init__(self, parent, **kwargs)
        self.initialiseoptions(MessageStackPanel)
        if not MessageStackPanel.popupSfx:
            MessageStackPanel.popupSfx = loader.loadSfx('audio/sfx_gui_zoom-io.mp3')
        
        self.setTransparency(True)
        self.msgStack = []
        self.msgIvals = {}
        self.slideIval = None
        self.task = None
        self.lastMessage = None
        self.startPos = self.getPos()
        self.setPos(self._getSlidePos())
        self.stash()

    def destroy(self):
        self.clearMessages()
        DirectFrame.destroy(self)
    
    def clearMessages(self):
        for msg in self.msgStack[:]:
            self.removeMessage(msg)
        
        if self.slideIval:
            self.slideIval.pause()
            self.slideIval = None
        
        self._stopMessageTask()

    def setMaxMessages(self):
        self.maxMessages = self['maxMessages']
    
    def setPosLerpTime(self):
        self.posLerpTime = self['posLerpTime']
    
    def getPosLerpTime(self):
        return self['posLerpTime']
    
    def setFadeLerpTime(self):
        self.fadeLerpTime = self['fadeLerpTime']

    def getFadeLerpTime(self):
        return self['fadeLerpTime']

    def setMessageBorder(self):
        self.messageBorder = self['messageBorder']

    def getMessageBorder(self):
        return self['messageBorder']
    
    def _getSlotPos(self, slot):
        pos = Point3(0, 0, -self['messageBorder'])
        for msg in self.msgStack[:slot]:
            z = pos[2] - msg.getHeight() - 2 * self['messageBorder']
            pos.setZ(z)
        
        if slot >= self['maxMessages']:
            z = pos[2] - 10
            pos.setZ(z)
        
        return pos
    
    def _getSlidePos(self):
        pos = Point3(self.startPos)
        pos.setZ(pos[2] + self['messageBorder'])
        for msg in self.msgStack[0:self.maxMessages]:
            z = pos[2] + msg.getHeight() + 2 * self['messageBorder']
            pos.setZ(z)
        
        return pos

    def _getMessageIndex(self, msg):
        for (index, m) in enumerate(self.msgStack):
            if msg is m:
                return index
        
        raise ValueError('%s not in list' % msg)
    
    def _startMessageTask(self):
        self._stopMessageTask()
        self.task = taskMgr.add(self._messageTask, self.uniqueName('MessageStack'))

    def _messageTask(self, task):
        for (x, msg) in enumerate(self.msgStack):
            ival = msg.getIval()
            if ival:
                if x < self.maxMessages:
                    if not ival.isPlaying():
                        ival.resume()
                    
                else:
                    ival.pause()
        
        return task.cont

    def _stopMessageTask(self):
        if self.task:
            taskMgr.remove(self.task)

    def _startMsgSlideIval(self, msg, slot):
        self._removeMsgIval(msg)
        ival = Sequence(LerpPosInterval(msg, self['posLerpTime'], self._getSlotPos(slot)), Func(self._removeMsgIval, msg))
        self.msgIvals[msg] = ival
        ival.start()

    def _removeMsgIval(self, msg):
        ival = self.msgIvals.pop(msg, None)
        if ival:
            ival.pause()

    def _adjustStack(self, fromIndex):
        unstable = self.msgStack[fromIndex:]
        for msg in unstable:
            index = self._getMessageIndex(msg)
            self._startMsgSlideIval(msg, index)

    def _startSlideIval(self):
        numMessages = len(self.msgStack)
        if self.slideIval:
            self.slideIval.pause()
        
        ival = Sequence()
        if numMessages:
            ival.append(Func(self._startMessageTask))
            ival.append(Func(self.unstash))
        
        ival.append(LerpPosInterval(self, self['posLerpTime'], self._getSlidePos()))
        if not numMessages:
            ival.append(Func(self._stopMessageTask))
            ival.append(Func(self.stash))
        
        self.slideIval = ival
        self.slideIval.start()

    def addMessage(self, message, autoDestroy = 1):
        self.msgStack.append(message)
        self.msgStack.sort()
        index = self._getMessageIndex(message)
        message.setPos(self._getSlotPos(index))
        message.createIval(self['fadeLerpTime'], Functor(self.removeMessage, message, autoDestroy)).start()
        self._adjustStack(index + 1)
        self._startSlideIval()
        self.popupSfx.play()

    def removeMessage(self, message, autoDestroy = 1):
        
        try:
            text = message['text']
            if self.lastMessage == text:
                self.lastMessage = None
            
            index = self._getMessageIndex(message)
            self.msgStack.pop(index)
            self._adjustStack(index)
            self._startSlideIval()
        except ValueError:
            pass

        message.destroy(autoDestroy)

    def showLoot(self, plunder = [], gold = 0, collect = 0, card = 0, cloth = 0, color = 0, jewel = None, tattoo = None, weapon = None, bounty = 0):
        from pirates.piratesgui.LootPopupPanel import LootPopupPanel
        msg = LootPopupPanel()
        msg.reparentTo(self)
        msg.showLoot(plunder, gold, collect, card, cloth, color, jewel, tattoo, weapon, bounty)
        self.addMessage(msg)

    def addTextMessage(self, text, seconds = 7, priority = 0, color = (0, 0, 0, 1), icon = (), suffix = '_b'):
        if self.lastMessage == text:
            return
        
        msg = StackMessage(parent = self, text = text, text_wordwrap = 16.5, text_align = TextNode.ALeft, text_scale = 0.035, text_fg = color, text_pos = (0.17, -0.072, 0), textMayChange = 1, time = seconds, priority = priority, icon = icon, suffix = suffix)
        self.addMessage(msg)
        self.lastMessage = text
        return msg

    def addModalTextMessage(self, text, buttonStyle = OTPDialog.CancelOnly, noCallback = None, yesCallback = None, cancelCallback = None, seconds = 120, priority = 0, color = (1, 1, 1, 1), icon = (), suffix = '_f'):
        if self.lastMessage == text:
            return
        
        msg = ModalStackMessage(parent = self, buttonStyle = buttonStyle, noCallback = noCallback, yesCallback = yesCallback, cancelCallback = cancelCallback, text = text, text_wordwrap = 16.5, text_align = TextNode.ALeft, text_scale = 0.035, text_fg = color, text_pos = (0.17, -0.072, 0), textMayChange = 1, time = seconds, priority = priority, icon = icon, suffix = suffix)
        self.addMessage(msg)
        self.lastMessage = text
        return msg


