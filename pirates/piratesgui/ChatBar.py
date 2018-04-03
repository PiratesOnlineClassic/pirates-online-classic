# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.ChatBar
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import FSM
from direct.showbase.PythonUtil import Functor
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.TabBar import TopTab, TabBar

class ChatTab(TopTab):
    __module__ = __name__

    def __init__(self, tabBar, name, text_xyz=None, **kw):
        optiondefs = (('suffix', '_c', None), ('frameSize', (0, 0.22, 0.0, 0.1), None), ('borderScale', 0.135, None), ('bgBuffer', 0.14, None), ('label', '', None), ('textMayChange', 1, None))
        self.defineoptions(kw, optiondefs)
        TopTab.__init__(self, tabBar, name, **kw)
        self.initialiseoptions(ChatTab)
        text_pos = (0.117, 0.04, 0)
        if text_xyz:
            text_pos = text_xyz
        DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=self['label'], text_scale=PiratesGuiGlobals.TextScaleLarge * 1.1, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=text_pos, text_font=PiratesGlobals.getInterfaceFont(), textMayChange=1)
        return


class ChatTabBar(TabBar):
    __module__ = __name__

    def refreshTabs(self):
        for x, name in enumerate(self.tabOrder):
            tab = self.tabs[name]
            tab.setPos(0.07 + 0.195 * (x + self.offset), 0, 0.06)
            tab.reparentTo(self.bParent)

        for name in reversed(self.tabOrder):
            tab = self.tabs[name]
            tab.reparentTo(self.bParent)

        self.activeIndex = max(0, min(self.activeIndex, len(self.tabOrder) - 1))
        if len(self.tabOrder):
            name = self.tabOrder[self.activeIndex]
            tab = self.tabs[name]
            tab.reparentTo(self.fParent)
            tab.setZ(0.077)

    def makeTab(self, name, **kw):
        return ChatTab(self, name, **kw)

    def stash(self):
        TabBar.stash(self)


class WhisperTab(TopTab):
    __module__ = __name__

    def __init__(self, tabBar, name, **kw):
        optiondefs = (('suffix', '_c', None), ('frameSize', (0, 0.745, 0.0, 0.11), None), ('borderScale', 0.135, None), ('bgBuffer', 0.14, None))
        self.defineoptions(kw, optiondefs)
        TopTab.__init__(self, tabBar, name, **kw)
        self.initialiseoptions(ChatTab)
        return


class WhisperTabBar(TabBar):
    __module__ = __name__

    def refreshTabs(self):
        for x, name in enumerate(self.tabOrder):
            tab = self.tabs[name]
            tab.setPos(0.07 + 0.72 * (x + self.offset), 0, 0.06)
            tab.reparentTo(self.bParent)

        for name in reversed(self.tabOrder):
            tab = self.tabs[name]
            tab.reparentTo(self.bParent)

        self.activeIndex = max(0, min(self.activeIndex, len(self.tabOrder) - 1))
        if len(self.tabOrder):
            name = self.tabOrder[self.activeIndex]
            tab = self.tabs[name]
            tab.reparentTo(self.fParent)
            tab.setZ(0.077)

    def makeTab(self, name, **kw):
        return WhisperTab(self, name, **kw)


class ChatBar(DirectFrame, FSM):
    __module__ = __name__

    def __init__(self, parent, chatMgr, chatEntry, whiteListEntry, *args, **kw):
        optiondefs = (('relief', None, None), ('state', DGG.DISABLED, None), ('frameSize', (0, 1, 0, 0.75), None), ('frameColor', (1, 0, 1, 0.2), None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, *args, **kw)
        self.initialiseoptions(ChatBar)
        FSM.__init__(self, 'ChatBar')
        self.whiteListEnabled = base.config.GetBool('whitelist-chat-enabled', 1) and base.cr.accountDetailRecord.WLChatEnabled
        self.openChatEnabled = base.cr.accountDetailRecord.canOpenChatAndNotGetBooted()
        self.toggleEnabled = self.whiteListEnabled and self.openChatEnabled
        self.noChat = not (self.whiteListEnabled or self.openChatEnabled)
        self.chatTabs = None
        self.whisperTabs = None
        self.chatMgr = chatMgr
        self.slideIval = None
        self.whisperNameLabel = None
        self.setupGui(chatEntry, whiteListEntry)
        self.request('Hidden')
        return

    def destroy(self):
        self.cleanup()
        self.stopSlideIval()
        DirectFrame.destroy(self)
        self.cleanupGui()
        self.chatMgr = None
        return

    def setupGui(self, chatEntry, whiteListEntry):
        self.stopSlideIval()
        if self.chatTabs:
            self.chatTabs.destroy()
        if self.whisperTabs:
            self.whisperTabs.destroy()
        self.removeChildren()
        gui = loader.loadModelCopy('models/gui/chat_frame_b')
        skullbg = loader.loadModelCopy('models/gui/chat_frame_a')
        skullgui = loader.loadModelOnce('models/gui/chat_frame_skull')
        icons = loader.loadModel('models/gui/toplevel_gui')
        scale = 0.2
        offset = (0.5, 0, 0.38)
        speedChatBg = self.attachNewNode('speedChatBg')
        skullbg.find('**/pPlane11').reparentTo(speedChatBg)
        speedChatBg.setScale(scale)
        speedChatBg.setPos(*offset)
        speedChatBg.flattenStrong()
        self.chatEntryBackground = self.attachNewNode('chatEntryBackground')
        self.chatEntryBackground.setX(-0.9)
        self.backTabParent = self.chatEntryBackground.attachNewNode('backTabs')
        textEntryGeom = self.chatEntryBackground.attachNewNode('textEntryBg')
        gui.find('**/pPlane12').reparentTo(textEntryGeom)
        textEntryGeom.setScale(scale)
        textEntryGeom.setPos(*offset)
        textEntryGeom.flattenStrong()
        self.chatEntryVisNode = textEntryGeom.attachNewNode('chatEntryVis')
        self.chatEntryVisNode.hide()
        self.chatEntryVisNode.setAlphaScale(0)
        chatEntry.reparentTo(self.chatEntryVisNode)
        whiteListEntry.reparentTo(self.chatEntryVisNode)
        if self.noChat:

            def noshow():
                pass

            chatEntry.show = noshow
            whiteListEntry.show = noshow
        else:
            if self.toggleEnabled:
                chatEntry.setPos(0.185, 0, 0.036)
                whiteListEntry.setPos(0.185, 0, 0.036)
            else:
                chatEntry.setPos(0.11, 0, 0.036)
                whiteListEntry.setPos(0.11, 0, 0.036)
        self.frontTabParent = self.chatEntryBackground.attachNewNode('frontTab', sort=2)
        self.speedButton = DirectButton(parent=self, relief=None, frameSize=(-0.055, 0.045, -0.055, 0.045), geom=(skullgui.find('**/*skull'), skullgui.find('**/*skull'), skullgui.find('**/*skull_down')), geom_scale=0.2, pos=(0.049,
                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                 0.045), rolloverSound=None, command=self.chatMgr.activateSpeedChat)
        self.normalChatButton = DirectButton(parent=self, relief=None, frameSize=(-0.055, 0.045, -0.055, 0.045), geom=(icons.find('**/chat_bubble_icon'), icons.find('**/chat_bubble_icon'), icons.find('**/chat_bubble_icon_over')), geom_scale=0.25, pos=(0.136,
                                                                                                                                                                                                                                                            0,
                                                                                                                                                                                                                                                            0.045), rolloverSound=None, command=self.chatMgr.toggleWhiteListChat)
        self.normalChatButton.hide()
        self.whiteListButton = DirectButton(parent=self, relief=None, frameSize=(-0.055, 0.045, -0.055, 0.045), geom=(icons.find('**/open_chat_enabled_icon'), icons.find('**/open_chat_enabled_icon'), icons.find('**/open_chat_enabled_icon_over')), geom_scale=0.25, pos=(0.136,
                                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                                             0.045), rolloverSound=None, command=self.chatMgr.toggleWhiteListChat)
        self.whiteListButton.hide()
        self.chatEntryButton = self.normalChatButton
        if not self.toggleEnabled:

            def noshow():
                pass

            self.normalChatButton.show = noshow
            self.whiteListButton.show = noshow
        tGui = loader.loadModel('models/gui/triangle')
        triangle = (tGui.find('**/triangle'), tGui.find('**/triangle_down'), tGui.find('**/triangle_over'))
        self.startChatButton = DirectButton(parent=self, relief=None, image=triangle, image_scale=0.065, pos=(0.14,
                                                                                                              0.0,
                                                                                                              0.05), rolloverSound=None, command=self.chatMgr.activateChat)
        self.chatTabs = ChatTabBar(parent=self, backParent=self.backTabParent, frontParent=self.frontTabParent)
        allTab = self.chatTabs.addTab('All', label=PLocalizer.ChatTabAll, command=self.chatMgr.activateChat, extraArgs=['All'])
        crewTab = self.chatTabs.addTab('Crew', label=PLocalizer.ChatTabCrew, command=self.chatMgr.activateChat, extraArgs=['Crew'])
        guildTab = self.chatTabs.addTab('Guild', label=PLocalizer.ChatTabGuild, command=self.chatMgr.activateChat, extraArgs=['Guild'])
        shipPVPTab = self.chatTabs.addTab('ShipPVP', label=PLocalizer.ChatTabShipPVP, command=self.chatMgr.activateChat, frameSize=(0,
                                                                                                                                    0.24,
                                                                                                                                    0.0,
                                                                                                                                    0.1), textMayChange=1, extraArgs=['ShipPVP'])
        self.chatTabs.stash()
        self.whisperTabs = WhisperTabBar(parent=self, backParent=self.backTabParent, frontParent=self.frontTabParent)
        whisperNameTab = self.whisperTabs.addTab('Name')
        whisperCancelTab = self.whisperTabs.addTab('Cancel', command=self.whisperCanceled)
        self.whisperTabs.stash()
        whisperCancelTab['frameSize'] = (0, 0.105, 0.0, 0.11)
        DirectLabel(parent=whisperNameTab, relief=None, state=DGG.DISABLED, text=PLocalizer.AvatarPanelWhisper + ':', text_scale=PiratesGuiGlobals.TextScaleLarge * 1.1, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.033,
                                                                                                                                                                                                                                                                                           0.04,
                                                                                                                                                                                                                                                                                           0), text_font=PiratesGlobals.getInterfaceFont())
        DirectLabel(parent=whisperCancelTab, relief=None, state=DGG.DISABLED, text='X', text_scale=PiratesGuiGlobals.TextScaleLarge * 1.3, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.053,
                                                                                                                                                                                                                                                               0.043,
                                                                                                                                                                                                                                                               0), text_font=PiratesGlobals.getInterfaceFont())
        self.whisperTabs.stash()
        self.request('Hidden')
        return

    def cleanupGui(self):
        self.chatEntryBackground = None
        self.backTabParent = None
        self.frontTabParent = None
        self.speedButton = None
        self.startChatButton = None
        if self.chatTabs:
            self.chatTabs.destroy()
            self.chatTabs = None
        if self.whisperTabs:
            self.whisperTabs.destroy()
            self.whisperTabs = None
        return

    def whisperCanceled(self):
        self.chatMgr.whisperCanceled()

    def refreshTabStates(self):
        if self.getCurrentOrNextState() not in ('Off', 'Hidden', 'Whisper'):
            if not self.chatMgr.crewChatAllowed:
                self.chatTabs.getTab('Crew').stash()
            else:
                self.chatTabs.getTab('Crew').unstash()
            if not self.chatMgr.guildChatAllowed:
                self.chatTabs.getTab('Guild').stash()
            else:
                self.chatTabs.getTab('Guild').unstash()
            if not self.chatMgr.shipPVPChatAllowed:
                self.chatTabs.getTab('ShipPVP').stash()
            else:
                self.chatTabs.getTab('ShipPVP').unstash()

    def stopSlideIval(self):
        if self.slideIval and self.slideIval.isPlaying():
            self.slideIval.pause()

    def enterHidden(self):
        self.stopSlideIval()
        self.slideIval = Sequence(Func(self.chatEntryVisNode.setAlphaScale, 0), Func(self.chatEntryVisNode.hide), Func(self.chatEntryButton.hide), self.chatEntryBackground.posInterval(0.25, Point3(-0.9, 0, 0), blendType='easeIn'), Func(self.startChatButton.show), Func(self.chatEntryBackground.hide))
        self.slideIval.start()

    def exitHidden(self):
        self.stopSlideIval()
        self.slideIval = Sequence(Func(self.chatEntryVisNode.show), Func(self.chatEntryBackground.show), Func(self.startChatButton.hide), self.chatEntryBackground.posInterval(0.25, Point3(0, 0, 0), blendType='easeOut'), Func(self.chatEntryVisNode.setAlphaScale, 1), Func(self.chatEntryButton.show))
        self.slideIval.start()

    def enterAll(self):
        self.chatTabs.unstash()
        self.whisperTabs.stash()
        self.chatTabs.selectTab('All')
        self.refreshTabStates()

    def exitAll(self):
        pass

    def enterCrew(self):
        self.chatTabs.unstash()
        self.whisperTabs.stash()
        self.chatTabs.selectTab('Crew')
        self.refreshTabStates()

    def exitCrew(self):
        pass

    def enterGuild(self):
        self.chatTabs.unstash()
        self.whisperTabs.stash()
        self.chatTabs.selectTab('Guild')
        self.refreshTabStates()

    def enterShipPVP(self):
        self.chatTabs.unstash()
        self.whisperTabs.stash()
        self.chatTabs.selectTab('ShipPVP')
        self.refreshTabStates()

    def exitShipPVP(self):
        pass

    def exitGuild(self):
        pass

    def enterWhisper(self, avatarName='John Sharkbait', whisperId=0):
        self.whisperName = avatarName
        self.whisperId = whisperId
        self.chatTabs.stash()
        self.whisperTabs.unstash()
        if self.whisperNameLabel:
            self.whisperNameLabel.destroy()
        self.whisperNameLabel = DirectLabel(parent=self.whisperTabs.getTab('Name'), relief=None, state=DGG.DISABLED, text=avatarName, text_scale=PiratesGuiGlobals.TextScaleLarge * 1.1, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.21,
                                                                                                                                                                                                                                                                                                           0.04,
                                                                                                                                                                                                                                                                                                           0), text_font=PiratesGlobals.getInterfaceFont())
        return

    def exitWhisper(self):
        self.whisperName = ''
        self.whisperId = 0
        if self.whisperNameLabel and 0:
            self.whisperNameLabel.destroy()
            self.whisperNameLabel = None
        return

    def enableWhiteListChat(self):
        self.chatEntryButton.hide()
        self.chatEntryButton = self.whiteListButton
        self.chatEntryButton.show()

    def disableWhiteListChat(self):
        self.chatEntryButton.hide()
        self.chatEntryButton = self.normalChatButton
        self.chatEntryButton.show()
# okay decompiling .\pirates\piratesgui\ChatBar.pyc
