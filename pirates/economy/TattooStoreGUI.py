from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import GuiButton, DialogButton
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.pirate import DynamicHuman
from pirates.piratesgui.TabBar import LeftTab, TabBar
from direct.interval.IntervalGlobal import *
from pirates.makeapirate import TattooGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.uberdog.UberDogGlobals import InventoryType
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from pirates.piratesgui import PDialog
from direct.task import Task
import random
from math import sin
from math import cos
from math import pi
from pirates.piratesbase import Freebooter
ZONE1 = 0
ZONE2 = 1
ZONE3 = 2
ZONE4 = 3
ZONE5 = 4
ZONE6 = 5
ZONE7 = 6
ZONE8 = 7
TYPE = 0
OFFSETX = 1
OFFSETY = 2
SCALE = 3
ROTATE = 4
COLOR = 5
TattooZones = [
    [
        ZONE1,
        PLocalizer.TattooChest],
    [
        ZONE2,
        PLocalizer.TattooLeftArm],
    [
        ZONE3,
        PLocalizer.TattooRightArm],
    [
        ZONE4,
        PLocalizer.TattooFace]]
CHEST_CAMERA = 0
LARM_CAMERA = 1
RARM_CAMERA = 2
FACE_CAMERA = 3
BODY_CAMERA = 4

class TattooStoreTab(LeftTab):

    def __init__(self, tabBar, name, **kw):
        optiondefs = (('suffix', '_d', None), ('borderScale', 0.38, None), ('bgBuffer', 0.15, None))
        self.defineoptions(kw, optiondefs)
        LeftTab.__init__(self, tabBar, name, **kw)
        self.initialiseoptions(TattooStoreTab)



class TattooStoreTabBar(TabBar):

    def refreshTabs(self):
        for (x, name) in enumerate(self.tabOrder):
            tab = self.tabs[name]
            tab.reparentTo(self.bParent)
            tab.setPos(-0.07, 0, 1.1 - 0.1 * (x + self.offset))
            (tab.setScale(0.2, 1, 0.2),)

        self.activeIndex = max(0, min(self.activeIndex, len(self.tabOrder) - 1))
        if len(self.tabOrder):
            name = self.tabOrder[self.activeIndex]
            tab = self.tabs[name]
            tab.reparentTo(self.fParent)
            tab.setX(-0.08)
            tab.setScale(0.2, 1, 0.22)

    def makeTab(self, name, **kw):
        return TattooStoreTab(self, name, **kw)



class TattooStoreCartList(DirectScrolledFrame):

    def __init__(self, parent, width, height, itemWidth, itemHeight):
        self.width = width + PiratesGuiGlobals.ScrollbarSize
        self.listItemHeight = itemHeight
        self.listItemWidth = itemWidth
        self.height = height
        self.__parent = parent
        self.pvpMode = parent.pvpMode
        charGui = loader.loadModel('models/gui/char_gui')
        DirectScrolledFrame.__init__(self,
                                     relief = None,
                                     state = DGG.NORMAL,
                                     manageScrollBars = 0,
                                     autoHideScrollBars = 1,
                                     frameSize = (0, self.width, 0, self.height),
                                     canvasSize = (0, self.width - 0.05, 0.025, self.height - 0.025),
                                     verticalScroll_relief = None,
                                     verticalScroll_image = charGui.find('**/chargui_slider_small'),
                                     verticalScroll_frameSize = (0, PiratesGuiGlobals.ScrollbarSize, 0, self.height),
                                     verticalScroll_image_scale = (self.height + 0.05, 1, 0.75),
                                     verticalScroll_image_hpr = (0, 0, 90),
                                     verticalScroll_image_pos = (self.width - PiratesGuiGlobals.ScrollbarSize * 0.5 - 0.004, 0, self.height * 0.5),
                                     verticalScroll_image_color = (0.61, 0.6, 0.6, 1),
                                     verticalScroll_thumb_image = (charGui.find('**/chargui_slider_node'),
                                                                   charGui.find('**/chargui_slider_node_down'),
                                                                   charGui.find('**/chargui_slider_node_over')),
                                     verticalScroll_thumb_relief = None,
                                     verticalScroll_thumb_image_scale = 0.25,
                                     verticalScroll_resizeThumb = 0,
                                     horizontalScroll_relief = None,
                                     sortOrder = 5
                                     )
        self.initialiseoptions(TattooStoreCartList)
        self.verticalScroll.incButton.destroy()
        self.verticalScroll.decButton.destroy()
        self.horizontalScroll.incButton.destroy()
        self.horizontalScroll.decButton.destroy()
        self.horizontalScroll.hide()
        self.panels = []
        self.purchases = []
        self.itemColor = Vec4(0.2, 0.2, 0.2, 1.0)
        charGui.removeNode()

    def destroy(self):
        self.ignoreAll()
        for panel in self.panels:
            panel.destroy()

        del self.panels
        del self.purchases
        DirectScrolledFrame.destroy(self)

    def setItemColor(self, color):
        self.itemColor = color

    def repackPanels(self):
        z = self.listItemHeight
        i = 0
        for i in range(len(self.panels)):
            self.panels[i].setPos(0.01, 0, -z * (i + 1))
            self.panels[i].origionalPos = self.panels[i].getPos(render2d)

        self['canvasSize'] = (0, self.listItemWidth - 0.09, -z * (i + 1), 0)

    def addPanel(self, data, repack = 1):
        uid = data[1]
        tattooId = data[2]
        tattoo = TattooGlobals.tattoos.get(uid)
        if tattoo is not None:
            if self.parent.mode == 1:
                itemCost = int(tattoo[4] * 0.25)
            else:
                itemCost = tattoo[4]
        else:
            return None
        itemText = tattoo[3]
        maxLength = 23 - len(str(itemCost))
        isDisabled = 0
        panel = DirectButton(parent = self, relief = None, text = itemText[:maxLength], text_fg = self.itemColor, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleMed, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0.06, 0.0), command = self.removePanel, extraArgs = [data])
        if self.parent.pvpMode:
            cImage = self.parent.RenownImage
        else:
            cImage = self.parent.CoinImage
        panel.costLabel = DirectLabel(parent = panel, relief = None, text = str(itemCost), text_fg = self.itemColor, text_align = TextNode.ARight, text_scale = PiratesGuiGlobals.TextScaleMed, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = (0.45, 0.0), image = cImage, image_scale = 0.15, image_pos = (0.48, 0.0, 0.014))
        panel.bind(DGG.ENTER, self.highlightStart, extraArgs = [panel])
        panel.bind(DGG.EXIT, self.highlightStop, extraArgs = [panel])
        panel.data = data
        panel.price = itemCost
        panel.reparentTo(self.getCanvas())
        self.panels.append(panel)
        self.purchases.append(data)
        if repack:
            self.repackPanels()

    def highlightStart(self, item, event = None):
        item['text_fg'] = PiratesGuiGlobals.TextFG6
        item.costLabel['text_fg'] = PiratesGuiGlobals.TextFG6

    def highlightStop(self, item, event = None):
        item['text_fg'] = self.itemColor
        item.costLabel['text_fg'] = self.itemColor

    def removePanel(self, data, repack = 1):
        for panel in self.panels:
            if panel.data == data:
                self.parent.updateButton(data, 1)
                self.panels.remove(panel)
                self.purchases.remove(data)
                panel.destroy()
                if repack:
                    self.repackPanels()

                self.parent.updateBalance()
                return

    def hasPanel(self, data):
        for panel in self.panels:
            if panel.data == data:
                return True

        return False

    def removeAllPanels(self):
        for panel in self.panels:
            panel.destroy()

        self.panels = []
        self.purchases = []
        self.repackPanels()

    def show(self):
        DirectScrolledFrame.show(self)

    def hide(self):
        DirectScrolledFrame.hide(self)

    def getItemQuantity(self, itemId):
        counter = 0
        for panel in self.panels:
            if panel.data[0] == itemId:
                counter += panel.data[1]

        return counter



class TattooStoreGUI(DirectFrame):
    notify = directNotify.newCategory('TattooStoreGUI')
    width = (PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.06) * 2
    height = 1.5
    columnWidth = PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.05
    holidayIdList = []

    def __init__(self, npc, shopId, **kw):
        optiondefs = (('relief', None, None), ('framSize', (0, self.width, 0, self.height), None), ('sortOrder', 20, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, None, **kw)
        self.initialiseoptions(TattooStoreGUI)
        self.pirate = None
        self.camIval = None
        self.buttons = []
        self.buttonIndex = 0
        self.tattooAmount = 0
        self.currentPage = None
        self.buttonsPerPage = 4
        self.prevIdx = 0
        self.mode = 0
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.CoinImage = gui.find('**/treasure_w_coin*')
        skullModel = loader.loadModel('models/gui/avatar_chooser_rope')
        self.RenownImage = skullModel.find('**/avatar_c_B_delete')
        self.ParchmentIcon = gui.find('**/main_gui_quest_scroll')
        self.TattooIcons = loader.loadModel('models/textureCards/tattooIcons')
        self.ShirtIcon = loader.loadModel('models/gui/char_gui').find('**/chargui_cloth')
        self.LockIcon = gui.find('**/subscribers_lock')
        self.questIcon = loader.loadModel('models/gui/compass_main').find('**/icon_objective_grey')
        self.backTabParent = self.attachNewNode('backTabs', sort = 0)
        self.panel = GuiPanel.GuiPanel(None, self.width, self.height, parent = self, showClose = False)
        self.setPos(0.0, 0, -0.75)
        self.balance = 0
        self.npc = npc
        self.rootTitle = PLocalizer.TattooShop
        if Freebooter.AllAccessHoliday:
            self.paid = Freebooter.FULL
        else:
            self.paid = base.cr.isPaid()
        self.shopId = shopId
        self.pvpMode = 0
        if shopId == PiratesGlobals.PRIVATEER_TATTOOS:
            self.pvpMode = 1

        if localAvatar.gameFSM.camIval is not None:
            if localAvatar.gameFSM.camIval.isPlaying():
                localAvatar.gameFSM.camIval.finish()

        self.initialCamPos = camera.getPos()
        self.initialCamHpr = camera.getHpr()
        self.initialPirateH = 0
        self.cartWidth = self.columnWidth - 0.1
        self.cartHeight = self.height - 0.25
        self.cartFrame = DirectFrame(parent = self.panel, relief = None, frameSize = (0, self.cartWidth, 0, self.cartHeight))
        self.cartFrame.setPos(self.columnWidth + 0.025, 0, 0.08)
        self.buyParchment = DirectFrame(parent = self.cartFrame, relief = None, text = PLocalizer.TailorPurchase, text_fg = PiratesGuiGlobals.TextFG1, text_align = TextNode.ACenter, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0.0, 0.2), text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 0, image = self.ParchmentIcon, image_scale = (0.24, 0.0, 0.3), image_pos = (0.0, 0.0, 0.0), pos = (0.3, 0.0, 0.92))
        self.sellParchment = DirectFrame(parent = self.cartFrame, relief = None, text = PLocalizer.TailorSelling, text_fg = PiratesGuiGlobals.TextFG1, text_align = TextNode.ACenter, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0.0, 0.2), text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 0, image = self.ParchmentIcon, image_scale = (0.24, 0.0, 0.3), image_pos = (0.0, 0.0, 0.0), pos = (0.3, 0.0, 0.48))
        self.purchaseInventory = TattooStoreCartList(self, self.cartWidth, self.cartHeight - 0.95, self.cartWidth, self.cartHeight / 20.0)
        self.purchaseInventory.reparentTo(self.cartFrame)
        self.purchaseInventory.setPos(0.0, 0.0, 0.76)
        self.sellInventory = TattooStoreCartList(self, self.cartWidth, self.cartHeight - 0.95, self.cartWidth, self.cartHeight / 20.0)
        self.sellInventory.reparentTo(self.cartFrame)
        self.sellInventory.setPos(0.0, 0.0, 0.31)
        self.frontTabParent = self.panel.attachNewNode('frontTab', sort = 2)
        self.currentWardrobe = None
        if self.pvpMode:
            yourMoney = PLocalizer.YourPVPMoney
            currencyIcon = self.RenownImage
        else:
            yourMoney = PLocalizer.YourMoney
            currencyIcon = self.CoinImage
        self.balanceTitle = DirectFrame(parent = self.cartFrame, relief = None, text = PLocalizer.Total, text_fg = PiratesGuiGlobals.TextFG2, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0.0, 0.0), text_shadow = PiratesGuiGlobals.TextShadow, pos = (0.09, 0, 0.225))
        self.balanceValue = DirectFrame(parent = self.cartFrame, relief = None, text = str(self.balance), text_fg = PiratesGuiGlobals.TextFG2, text_align = TextNode.ARight, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (-0.055, 0.0), text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, image = currencyIcon, image_scale = 0.15, image_pos = (-.025, 0, 0.015), pos = (self.cartWidth, 0, 0.225))
        self.myGoldTitle = DirectFrame(parent = self.cartFrame, relief = None, text = yourMoney, text_fg = PiratesGuiGlobals.TextFG2, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0.0, 0.0), text_shadow = PiratesGuiGlobals.TextShadow, pos = (0.09, 0, 0.155))
        self.myGold = DirectFrame(parent = self.cartFrame, relief = None, text = str(self.getMoney()), text_fg = PiratesGuiGlobals.TextFG2, text_align = TextNode.ARight, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (-0.055, 0.0), text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1, image = currencyIcon, image_scale = 0.15, image_pos = (-.025, 0, 0.015), pos = (self.cartWidth, 0, 0.155))
        self.commitButton = DialogButton.DialogButton(command = self.handleCommitPurchase, parent = self.cartFrame, text = PLocalizer.PurchaseCommit, text_fg = PiratesGuiGlobals.TextFG2, text_pos = (0.02, -(PiratesGuiGlobals.TextScaleLarge) * 0.25), text_scale = PiratesGuiGlobals.TextScaleLarge, text_shadow = PiratesGuiGlobals.TextShadow, buttonStyle = DialogButton.DialogButton.YES)
        self.commitButton.setPos(self.cartWidth / 2, 0, 0.005)
        self.closeButton = DialogButton.DialogButton(command = self.closePanel, parent = self.cartFrame, text = PLocalizer.lClose, text_fg = PiratesGuiGlobals.TextFG2, text_pos = (0.02, -(PiratesGuiGlobals.TextScaleLarge) * 0.25), text_scale = PiratesGuiGlobals.TextScaleLarge, text_shadow = PiratesGuiGlobals.TextShadow, buttonStyle = DialogButton.DialogButton.NO)
        self.closeButton.setPos(self.cartWidth / 2 - 0.55, 0, 0.005)
        self.storeButton = DialogButton.DialogButton(command = self.changeMode, state = DGG.DISABLED, parent = self, text = PLocalizer.InteractStore, text_fg = PiratesGuiGlobals.TextFG2, text_scale = PiratesGuiGlobals.TextScaleLarge, text_shadow = PiratesGuiGlobals.TextShadow, image_color = Vec4(0.7, 0.95, 0.7, 1.0), scale = 0.9, extraArgs = [0])
        self.storeButton.setPos(0.23, 0.0, 1.21)
        self.wardrobeButton = DialogButton.DialogButton(command = self.changeMode, state = DGG.NORMAL, parent = self, text = PLocalizer.TailorWardrobe, text_fg = PiratesGuiGlobals.TextFG2, text_scale = PiratesGuiGlobals.TextScaleLarge, text_shadow = PiratesGuiGlobals.TextShadow, image_color = Vec4(0.95, 0.7, 0.7, 1.0), scale = 0.9, extraArgs = [1])
        self.wardrobeButton.setPos(0.45, 0.0, 1.21)
        tGui = loader.loadModel('models/gui/triangle')
        triangle = (tGui.find('**/triangle'), tGui.find('**/triangle_down'), tGui.find('**/triangle_over'))
        self.nextPageButton = DirectButton(parent = self.panel, relief = None, state = DGG.DISABLED, image = triangle, image_scale = 0.065, pos = (0.54, 0.0, 0.175), rolloverSound = None, command = self.nextPage)
        self.prevPageButton = DirectButton(parent = self.panel, relief = None, state = DGG.DISABLED, image = triangle, image_scale = -0.065, pos = (0.16, 0.0, 0.175), rolloverSound = None, command = self.previousPage)
        self.pageNumber = DirectFrame(parent = self.panel, relief = None, text = '', text_fg = PiratesGuiGlobals.TextFG2, text_align = TextNode.ACenter, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (0.0, 0.0), text_shadow = PiratesGuiGlobals.TextShadow, pos = (0.35, 0, 0.1625))
        self.titleLabel = DirectLabel(parent = self, relief = None, text = '', text_fg = PiratesGuiGlobals.TextFG1, text_align = TextNode.ACenter, text_scale = PiratesGuiGlobals.TextScaleLarge * 1.3, text_shadow = PiratesGuiGlobals.TextShadow, pos = (0.62, 0.0, 1.33))
        self.titleLabel.setBin('gui-fixed', 1)
        self.createPirate()
        charGui = loader.loadModel('models/gui/char_gui')
        self.rotateSlider = DirectSlider(parent = base.a2dBottomLeft, relief = None, command = self.rotatePirate, image = charGui.find('**/chargui_slider_small'), image_scale = (2.15, 2.15, 1.5), thumb_relief = None, thumb_image = (charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over')), pos = (0.8, 0.0, 0.09), text_align = TextNode.ACenter, text_scale = (0.1, 0.1), text_pos = (0.0, 0.1), text_fg = PiratesGuiGlobals.TextFG1, scale = 0.43, text = PLocalizer.RotateSlider, value = 0.5, sortOrder = -1)
        self.rotateSlider['extraArgs'] = [
            self.rotateSlider]
        self.rotateSliderOrigin = 0.5
        self.accept('mouse1', self._startMouseReadTask)
        self.accept('mouse1-up', self._stopMouseReadTask)
        self.alertDialog = None
        localAvatar.guiMgr.chatPanel.show()
        localAvatar.guiMgr.chatPanel.startFadeTextIval()
        self.accept(localAvatar.uniqueName('tattooUpdate'), self.reloadPirateDNA)
        self.model = loader.loadModel('models/gui/gui_shop_tailor')
        self.model.reparentTo(self.panel)
        self.model.setBin('gui-fixed', 0)
        self.model.setPos(0.625, 0.0, 1.05)
        self.model.setScale(0.337, 0.0, 0.327)
        self.showQuestLabel = False
        if localAvatar.guiMgr.questPage:
            if not localAvatar.guiMgr.questPage.trackedQuestLabel.isHidden():
                localAvatar.guiMgr.questPage.trackedQuestLabel.hide()
                self.showQuestLabel = True

        self.equipRequests = {
            ZONE1: None,
            ZONE2: None,
            ZONE3: None,
            ZONE4: None,
            ZONE5: None,
            ZONE6: None,
            ZONE7: None,
            ZONE8: None}
        self.initTabs()
        self.updateBalance()
        self.lastRun = 0

    def rotatePirate(self, slider):
        if self.pirate and slider:
            value = slider.getValue()
            if value != self.rotateSliderOrigin:
                diff = value - self.rotateSliderOrigin
                h = diff * 360.0 + self.pirate.getH()
                self.pirate.setH(h)
                self.rotateSliderOrigin = value

    def destroy(self):
        DirectFrame.destroy(self)
        if self.camIval:
            self.camIval.finish()
            self.camIval = None
            camera.setHpr(0, 0, 0)

        self.rotateSlider.destroy()
        self.unloadPirate()
        if self.model:
            self.model.removeNode()
            self.model = None

        if self.CoinImage:
            self.CoinImage.removeNode()
            self.CoinImage = None

        if self.RenownImage:
            self.RenownImage.removeNode()
            self.RenownImage = None

        if self.ParchmentIcon:
            self.ParchmentIcon.removeNode()
            self.ParchmentIcon = None

        if self.ShirtIcon:
            self.ShirtIcon.removeNode()
            self.ShirtIcon = None

        if self.alertDialog:
            self.alertDialog.destroy()

        if self.TattooIcons:
            self.TattooIcons.removeNode()
            self.TattooIcons = None

        if self.LockIcon:
            self.LockIcon.removeNode()
            self.LockIcon = None

        if self.questIcon:
            self.questIcon.removeNode()
            self.questIcon = None

        if localAvatar.guiMgr.questPage and len(localAvatar.guiMgr.questPage.trackedQuestLabel['text']):
            if self.showQuestLabel:
                localAvatar.guiMgr.questPage.trackedQuestLabel.show()

        localAvatar.guiMgr.chatPanel.hide()

    def createPirate(self):
        if self.pirate is None:
            self.pirate = DynamicHuman.DynamicHuman()
            self.pirate.setDNAString(localAvatar.style)
            self.pirate.generateHuman(localAvatar.style.gender)
            self.pirate.model.setupSelectionChoices('DEFAULT')
            self.pirate.mixingEnabled = True
            self.pirate.enableBlend()
            self.pirate.loop('idle')
            self.pirate.useLOD(2000)
            dummy = self.npc.attachNewNode('dummy')
            dummy.setPos(self.npc.getPos() - Vec3(0, 7, 0))
            parent = self.npc.getParent()
            self.pirate.reparentTo(parent)
            pos = dummy.getPos()
            hpr = dummy.getHpr()
            self.pirate.setPos(pos)
            self.pirate.setHpr(hpr)
            self.pirate.lookAt(self.npc)
            dummy.detachNode()
            self.initialPirateH = self.pirate.getH()
            self.pirate.style.setClothesShirt(0)
            self.pirate.style.setClothesCoat(0)
            self.pirate.style.setClothesVest(0)
            self.pirate.model.handleClothesHiding()

        self.pirate.show()
        localAvatar.stash()

    def focusCamera(self, cameraId = BODY_CAMERA):
        if localAvatar.gameFSM.camIval is not None:
            if localAvatar.gameFSM.camIval.isPlaying():
                localAvatar.gameFSM.camIval.finish()

        if self.camIval:
            self.camIval.finish()
            self.camIval = None

        if self.pirate is None:
            self.createPirate()

        self.pirate.setH(self.initialPirateH)
        self.rotateSlider['value'] = self.rotateSliderOrigin = 0.5
        dummy = self.pirate.attachNewNode('dummy')
        if cameraId == BODY_CAMERA:
            dummy.setPos(dummy, 0, 10, self.pirate.headNode.getZ(self.pirate))
        elif cameraId == CHEST_CAMERA:
            dummy.setPos(dummy, 0, 4, self.pirate.headNode.getZ(self.pirate))
        elif cameraId == LARM_CAMERA:
            dummy.setPos(dummy, -5, 2, self.pirate.headNode.getZ(self.pirate))
        elif cameraId == RARM_CAMERA:
            dummy.setPos(dummy, 5, 2, self.pirate.headNode.getZ(self.pirate))
        elif cameraId == FACE_CAMERA:
            dummy.setPos(dummy, 0, 3, self.pirate.headNode.getZ(self.pirate) * 1.1)
        else:
            dummy.setPos(dummy, 0, 0, 0)
        dummy.wrtReparentTo(render)
        if cameraId == BODY_CAMERA:
            dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 0.9)
        elif cameraId == CHEST_CAMERA:
            dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate))
        elif cameraId == LARM_CAMERA:
            dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 0.9)
        elif cameraId == RARM_CAMERA:
            dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 0.9)
        elif cameraId == FACE_CAMERA:
            dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 1.1)
        else:
            dummy.lookAt(0, 0, 0, 0)
        dummy.setH(dummy, -17)
        dummy.setP(dummy, -12)
        camPos = dummy.getPos()
        camHpr = Point3(dummy.getH(), dummy.getP(), 0)
        dummy.detachNode()
        camera.wrtReparentTo(render)
        camH = camera.getH() % 360
        h = camHpr[0] % 360
        if camH > h:
            h += 360

        if h - camH > 180:
            h -= 360

        camHpr.setX(h)
        camera.setH(camH)
        t = 1.5
        self.camIval = camera.posHprInterval(t, pos = camPos, hpr = camHpr, blendType = 'easeOut')
        localAvatar.cameraFSM.request('Control')
        self.camIval.start()

    def unloadPirate(self):
        if self.pirate:
            self.pirate.detachNode()
            self.pirate.cleanupHuman()
            self.pirate.delete()
            self.pirate = None

        localAvatar.unstash()

    def closePanel(self):
        messenger.send('exitStore')
        self.ignoreAll()
        camera.setPos(self.initialCamPos)
        camera.setHpr(self.initialCamHpr)
        equips = []
        gender = localAvatar.style.getGender()
        offsetIndex = 5
        if gender == 'm':
            offsetIndex = 5
        else:
            offsetIndex = 6
        for type in self.equipRequests.keys():
            equip = self.equipRequests.get(type)
            if equip is not None:
                zone = equip[0]
                uid = equip[1]
                tattooId = equip[2]
                tattoo = TattooGlobals.tattoos.get(uid)
                if tattoo is not None:
                    equips.append([
                        zone,
                        uid])
                    offsetx = tattoo[offsetIndex][0]
                    offsety = tattoo[offsetIndex][1]
                    scale = tattoo[offsetIndex][2]
                    rotate = tattoo[offsetIndex][3]
                    tattooId = tattoo[1]
                    color = 0
                else:
                    equips.append([
                        zone,
                        -1])
                    offsetx = 0
                    offsety = 0
                    scale = 1.0
                    rotate = 0
                    color = 0
                    tattooId = 0
                S = Vec2(1 / float(scale), 1 / float(scale))
                Iv = Vec2(offsetx, offsety)
                Vm = Vec2(sin(rotate * pi / 180.0), cos(rotate * pi / 180.0))
                Vms = Vec2(Vm[0] * S[0], Vm[1] * S[1])
                Vn = Vec2(Vm[1], -Vm[0])
                Vns = Vec2(Vn[0] * S[0], Vn[1] * S[1])
                F = Vec2(-Vns.dot(Iv) + 0.5, -Vms.dot(Iv) + 0.5)
                if zone == TattooGlobals.ZONE1:
                    localAvatar.style.setTattooChest(tattooId, F[0], F[1], S[0], rotate, color)
                elif zone == TattooGlobals.ZONE2:
                    localAvatar.style.setTattooZone2(tattooId, F[0], F[1], S[0], rotate, color)
                elif zone == TattooGlobals.ZONE3:
                    localAvatar.style.setTattooZone3(tattooId, F[0], F[1], S[0], rotate, color)
                elif zone == TattooGlobals.ZONE4:
                    localAvatar.style.setTattooZone4(tattooId, F[0], F[1], S[0], rotate, color)

        if len(equips) > 0:
            self.npc.sendRequestTattooEquip(equips)
            gender = localAvatar.style.getGender()
            localAvatar.generateHuman(gender, base.cr.human)
            localAvatar.motionFSM.off()
            localAvatar.motionFSM.on()

        self.unloadPirate()

    def handleCommitPurchase(self):
        if self.purchaseInventory == []:
            base.localAvatar.guiMgr.createWarning(PLocalizer.EmptyPurchaseWarning, PiratesGuiGlobals.TextFG6)
            return

        inventory = base.localAvatar.getInventory()
        myMoney = inventory.getStackQuantity(InventoryType.GoldInPocket)
        if self.pvpMode:
            myMoney = self.getMoney()

        if inventory:
            if myMoney < self.balance:
                base.localAvatar.guiMgr.createWarning(PLocalizer.NotEnoughMoneyWarning, PiratesGuiGlobals.TextFG6)
                return

            if self.balance < 0 and myMoney + self.balance > self.getMaxMoney(inventory):
                base.localAvatar.guiMgr.createWarning(PLocalizer.CannotHoldGoldWarning, PiratesGuiGlobals.TextFG6)
                return

        purchaseArgList = []
        sellArgList = []
        for item in self.purchaseInventory.purchases:
            uid = item[1]
            type = item[0]
            tattooId = item[2]
            purchaseArgList.append(uid)
            self.equipRequests[type] = [type, uid, tattooId]

        for item in self.sellInventory.purchases:
            uid = item[1]
            type = item[0]
            tattooId = item[2]
            sellArgList.append(uid)
            if self.equipRequests[type] == [
                type,
                uid,
                tattooId]:
                self.equipRequests[type] = None

        self.purchaseInventory.removeAllPanels()
        self.sellInventory.removeAllPanels()
        self.npc.sendRequestTattoo(purchaseArgList, sellArgList, self.pvpMode)
        self.changeMode(1, refresh = True)

    def updateBalance(self, extraArgs = None):
        self.myGold['text'] = str(self.getMoney())
        self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG2
        self.balance = 0
        for item in self.purchaseInventory.panels:
            self.balance += item.price

        for item in self.sellInventory.panels:
            self.balance -= item.price

        transactions = len(self.purchaseInventory.purchases) + len(self.sellInventory.purchases)
        if self.balance > 0:
            self.balanceTitle['text'] = PLocalizer.Total
            self.balanceValue['text'] = str(abs(self.balance))
            self.commitButton['text'] = PLocalizer.PurchaseCommit
        elif self.balance < 0:
            self.balanceTitle['text'] = PLocalizer.Gain
            self.balanceValue['text'] = str(abs(self.balance))
            self.commitButton['text'] = PLocalizer.TailorSell
        else:
            self.balanceTitle['text'] = PLocalizer.Total
            self.balanceValue['text'] = str(abs(self.balance))
            self.commitButton['text'] = PLocalizer.GenericConfirmDone
        if self.balance > self.getMoney() or transactions == 0:
            if self.balance > self.getMoney():
                self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG6

            self.commitButton['state'] = DGG.DISABLED
        elif self.balance < 0:
            self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG4
            self.commitButton['state'] = DGG.NORMAL
        else:
            self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG2
            self.commitButton['state'] = DGG.NORMAL
        inventory = base.localAvatar.getInventory()
        myMoney = inventory.getStackQuantity(InventoryType.GoldInPocket)
        if self.pvpMode:
            myMoney = self.getMoney()

        if inventory:
            if myMoney < self.balance or self.purchaseInventory.panels == []:
                self.commitButton['frameColor'] = PiratesGuiGlobals.ButtonColor3
            else:
                self.commitButton['frameColor'] = PiratesGuiGlobals.ButtonColor4

    def checkPanel(self, panel, inventory, itemId):
        purchaseQty = self.purchaseInventory.getItemQuantity(itemId)
        panel.checkPlayerInventory(itemId, purchaseQty)

    def initTabs(self):
        self.tabBar = TattooStoreTabBar(parent = self, backParent = self.backTabParent, frontParent = self.frontTabParent, offset = 0)
        self.pageNames = []
        self.createTabs()
        if len(self.pageNames) > 0:
            self.setPage(self.pageNames[0])

    def createTabs(self):
        for item in TattooZones:
            if not self.isPageAdded(item[0]):
                self.addTab(item[0])

    def addTab(self, id):
        newTab = self.tabBar.addTab(id, command = self.setPage, extraArgs = [id])
        gender = localAvatar.style.getGender()
        if id == ZONE1:
            if gender == 'm':
                tabIcon = self.TattooIcons.find('**/icon_shop_tailor_chest_male')
            else:
                tabIcon = self.TattooIcons.find('**/icon_shop_tailor_chest_female')
            tabScale = 0.4
        elif id == ZONE2:
            tabIcon = self.TattooIcons.find('**/icon_shop_tailor_arm')
            tabScale = 0.4
        elif id == ZONE3:
            tabIcon = self.TattooIcons.find('**/icon_shop_tailor_arm')
            tabScale = (-0.4, 0.4, 0.4)
        elif id == ZONE4:
            if gender == 'm':
                tabIcon = self.TattooIcons.find('**/icon_shop_tailor_face_male')
            else:
                tabIcon = self.TattooIcons.find('**/icon_shop_tailor_face_female')
            tabScale = 0.4
        else:
            tabIcon = None
            tabScale = 0.0
        newTab.nameTag = DirectLabel(parent = newTab, relief = None, state = DGG.DISABLED, pos = (0.0, 0, 0.0), image = tabIcon, image_scale = tabScale)
        self.pageNames.append(id)

    def isPageAdded(self, pageName):
        return self.pageNames.count(pageName) > 0

    def nextPage(self):
        if self.tattooAmount - (self.buttonIndex + self.buttonsPerPage) > 0:
            startIndex = self.buttonIndex + self.buttonsPerPage
            self.setPage(self.currentPage, startIndex, False)
        else:
            self.setPage(self.currentPage, 0, False)

    def previousPage(self):
        if self.buttonIndex > 0:
            startIndex = self.buttonIndex - self.buttonsPerPage
            self.setPage(self.currentPage, startIndex, False)
        else:
            remainder = self.tattooAmount % self.buttonsPerPage
            if remainder:
                startIndex = self.tattooAmount - remainder
            else:
                startIndex = self.tattooAmount - self.buttonsPerPage
            self.setPage(self.currentPage, startIndex, False)

    def addToCart(self, button, type, uid):
        item = TattooGlobals.tattoos.get(uid)
        if item is None:
            return None

        tattooId = item[1]
        data = [
            type,
            uid,
            tattooId]
        if self.mode == 0:
            if button.addToCart.buyState:
                limit = PiratesGlobals.WARDROBE_LIMIT_TATTOO
                current = 0
                for id in self.currentWardrobe:
                    item = TattooGlobals.tattoos.get(id)
                    if item:
                        itemType = item[0]
                        if itemType == type:
                            current += 1

                for item in self.purchaseInventory.panels:
                    itemType = item.data[0]
                    if itemType == type:
                        current += 1

                for item in self.sellInventory.panels:
                    itemType = item.data[0]
                    if itemType == type:
                        current -= 1

                if current >= limit:
                    self.showWardrobeLimitAlert(type)
                    return None

                self.purchaseInventory.addPanel(data)
                button.addToCart['text'] = PLocalizer.TailorRemove
                button.addToCart.buyState = 0
            else:
                button.addToCart['text'] = PLocalizer.TailorAddToCart
                button.addToCart.buyState = 1
                self.purchaseInventory.removePanel(data)
        elif self.mode == 1:
            if button.addToCart.buyState:
                self.sellInventory.addPanel(data)
                button.addToCart['text'] = PLocalizer.TailorRemove
                button.equip['state'] = DGG.DISABLED
                button.addToCart.buyState = 0
            else:
                button.addToCart['text'] = PLocalizer.TailorSell
                button.equip['state'] = DGG.NORMAL
                button.addToCart.buyState = 1
                self.sellInventory.removePanel(data)

        self.updateBalance()

    def updateButton(self, data, buyState):
        for item in self.buttons:
            if item.tattooUID == data[1]:
                if self.mode == 0 and item.tattooUID not in self.currentWardrobe:
                    item.addToCart['text'] = PLocalizer.TailorAddToCart
                elif self.mode == 1:
                    item.addToCart['text'] = PLocalizer.TailorSell
                    item.equip['state'] = DGG.NORMAL

                item.addToCart.buyState = 1
                return

    def changeMode(self, mode, refresh = False):
        if self.mode == mode and not refresh:
            return
        elif self.mode == mode and refresh:
            self.setPage(self.currentPage, 0, refreshWardrobe = refresh)
            return

        if self.mode == 0:
            self.prevIdx = self.buttonIndex
            idx = 0
        else:
            idx = self.prevIdx
        self.mode = mode
        self.setPage(self.currentPage, idx, refreshWardrobe = refresh)

    def setWardrobe(self, tattoos):
        if self.currentWardrobe:
            self.currentWardrobe = []

        self.currentWardrobe = tattoos
        self.setPage(self.currentPage, refreshWardrobe = False)

    def reloadPirateDNA(self):
        gender = localAvatar.style.getGender()
        if gender == 'm':
            offsetIndex = 5
        else:
            offsetIndex = 6
        for zone in [ZONE1, ZONE2, ZONE3, ZONE4]:
            if self.equipRequests[zone] is not None:
                uid = self.equipRequests[zone][1]
                tattoo = TattooGlobals.tattoos.get(uid)
                if tattoo:
                    offsetx = tattoo[offsetIndex][0]
                    offsety = tattoo[offsetIndex][1]
                    scale = tattoo[offsetIndex][2]
                    rotate = tattoo[offsetIndex][3]
                    tattooId = tattoo[1]
                    self.pirate.model.tattoos[zone][TYPE] = tattooId
                    S = Vec2(1 / float(scale), 1 / float(scale))
                    Iv = Vec2(offsetx, offsety)
                    Vm = Vec2(sin(rotate * pi / 180.0), cos(rotate * pi / 180.0))
                    Vms = Vec2(Vm[0] * S[0], Vm[1] * S[1])
                    Vn = Vec2(Vm[1], -Vm[0])
                    Vns = Vec2(Vn[0] * S[0], Vn[1] * S[1])
                    F = Vec2(-Vns.dot(Iv) + 0.5, -Vms.dot(Iv) + 0.5)
                    self.pirate.model.tattoos[zone][OFFSETX] = F[0]
                    self.pirate.model.tattoos[zone][OFFSETY] = F[1]
                    self.pirate.model.tattoos[zone][SCALE] = S[0]
                    self.pirate.model.tattoos[zone][ROTATE] = rotate
                elif uid == -1:
                    self.pirate.model.tattoos[zone][TYPE] = 0

            elif zone == ZONE1:
                self.pirate.model.tattoos[ZONE1] = list(localAvatar.style.getTattooChest())
            elif zone == ZONE2:
                self.pirate.model.tattoos[ZONE2] = list(localAvatar.style.getTattooZone2())
            elif zone == ZONE3:
                self.pirate.model.tattoos[ZONE3] = list(localAvatar.style.getTattooZone3())
            elif zone == ZONE4:
                self.pirate.model.tattoos[ZONE4] = list(localAvatar.style.getTattooZone4())

            self.pirate.model.updateTattoo(zone)

    def equipTattoo(self, tattoo):
        type = tattoo[1]
        uid = tattoo[2]
        item = TattooGlobals.tattoos.get(uid)
        itemButton = tattoo[0]
        if item:
            tattooId = item[1]
            self.equipRequests[type] = [type, uid, tattooId]
        else:
            self.equipRequests[type] = [type, -1, 0]
        self.reloadPirateDNA()
        for button in self.buttons:
            if button != itemButton:
                button.itemText['text'] = ''
                button.equip.show()
                button.equip['text'] = PLocalizer.TailorEquip
                button.equip['extraArgs'] = [
                    [
                        button,
                        button.tattooType,
                        button.tattooUID]]

        itemButton.itemText['text'] = PLocalizer.TattooShopOwned
        if item:
            itemButton.equip['text'] = PLocalizer.TailorTakeOff
            itemButton.equip['extraArgs'] = [
                [
                    itemButton,
                    itemButton.tattooType,
                    -1]]
        else:
            itemButton.itemText['text'] = ''
            itemButton.equip['text'] = PLocalizer.TailorEquip
            itemButton.equip['extraArgs'] = [
                [
                    itemButton,
                    itemButton.tattooType,
                    itemButton.tattooUID]]

    def sortItems(self, item1, item2):
        if item1[1] == True:
            return -1
        elif item2[1] == True:
            return 1
        elif self.mode == 0:
            if item1[4] is not None:
                return -1
            elif item2[4] is not None:
                return 1
            elif item1[2] > item2[2]:
                return 1
            elif item1[2] < item2[2]:
                return -1
            else:
                return 0
        elif self.mode == 1:
            if item1[2] < item2[2]:
                return -1
            elif item1[2] > item2[2]:
                return 1
            else:
                return 0

    def applyTattoo(self, pirate, zone, uid):
        tattoo = TattooGlobals.tattoos.get(uid)
        gender = localAvatar.style.getGender()
        if tattoo is None:
            return None

        if gender == 'm':
            offsetIndex = 5
        else:
            offsetIndex = 6
        offsetx = tattoo[offsetIndex][0]
        offsety = tattoo[offsetIndex][1]
        scale = tattoo[offsetIndex][2]
        rotate = tattoo[offsetIndex][3]
        tattooId = tattoo[1]
        if not hasattr(pirate, 'model'):
            return None

        pirate.model.tattoos[zone][TYPE] = tattooId
        S = Vec2(1 / float(scale), 1 / float(scale))
        Iv = Vec2(offsetx, offsety)
        Vm = Vec2(sin(rotate * pi / 180.0), cos(rotate * pi / 180.0))
        Vms = Vec2(Vm[0] * S[0], Vm[1] * S[1])
        Vn = Vec2(Vm[1], -Vm[0])
        Vns = Vec2(Vn[0] * S[0], Vn[1] * S[1])
        F = Vec2(-Vns.dot(Iv) + 0.5, -Vms.dot(Iv) + 0.5)
        pirate.model.tattoos[zone][OFFSETX] = F[0]
        pirate.model.tattoos[zone][OFFSETY] = F[1]
        pirate.model.tattoos[zone][SCALE] = S[0]
        pirate.model.tattoos[zone][ROTATE] = rotate
        pirate.model.updateTattoo(zone)
        currTime = globalClock.getFrameTime()
        if currTime - self.lastRun > 10:
            if zone == ZONE2:
                pirate.play('map_look_arm_left')
            elif zone == ZONE3:
                pirate.play('map_look_arm_right')

            self.lastRun = currTime

    def setPage(self, pageName, startIndex = 0, refreshWardrobe = True):
        self.tabBar.unstash()
        self.titleLabel['text'] = '\x01smallCaps\x01' + self.rootTitle + ' - ' + TattooZones[pageName][1] + '\x02'
        previousPage = self.currentPage
        if self.currentPage != pageName:
            self.prevIdx = 0

        self.currentPage = pageName
        tattooType = pageName
        self.reloadPirateDNA()
        if self.currentPage != previousPage:
            self.focusCamera(self.currentPage)

        if localAvatar.style.getGender() == 'm':
            GENDER = 'MALE'
            offsetIndex = 5
        else:
            GENDER = 'FEMALE'
            offsetIndex = 6
        if refreshWardrobe:
            self.npc.sendRequestTattooList()
            return

        if self.equipRequests[ZONE1] is None:
            currentZONE1 = localAvatar.style.getTattooChest()
        else:
            currentZONE1 = [
                self.equipRequests[ZONE1][2]]
        if self.equipRequests[ZONE2] is None:
            currentZONE2 = localAvatar.style.getTattooZone2()
        else:
            currentZONE2 = [
                self.equipRequests[ZONE2][2]]
        if self.equipRequests[ZONE3] is None:
            currentZONE3 = localAvatar.style.getTattooZone3()
        else:
            currentZONE3 = [
                self.equipRequests[ZONE3][2]]
        if self.equipRequests[ZONE4] is None:
            currentZONE4 = localAvatar.style.getTattooZone4()
        else:
            currentZONE4 = [
                self.equipRequests[ZONE4][2]]
        tattoos = []
        tattoo_tex = loader.loadModel('models/misc/tattoos')
        if self.mode == 0:
            if not self.currentWardrobe:
                return

            store = self.shopId
            set = TattooGlobals.stores.get(store)
            if set is None:
                return

            for index in set:
                item = TattooGlobals.tattoos.get(index)
                if item:
                    cost = item[4]
                    holiday = item[7]
                    tattooId = item[1]
                    type = item[0]
                    if type != tattooType:
                        continue

                    if holiday is not None:
                        if holiday in TattooStoreGUI.holidayIdList:
                            tattoos.append([
                                index,
                                False,
                                cost,
                                tattooId,
                                holiday])

                    else:
                        tattoos.append([
                            index,
                            False,
                            cost,
                            tattooId,
                            holiday])

        if self.mode == 1:
            if self.currentWardrobe:
                for id in self.currentWardrobe:
                    item = TattooGlobals.tattoos.get(id)
                    if item and item[0] == tattooType:
                        cost = item[4]
                        equipped = False
                        type = item[0]
                        tattooId = item[1]
                        holiday = item[7]
                        offset = item[offsetIndex]
                        if type == ZONE1:
                            if currentZONE1[0] == tattooId:
                                equipped = True

                        elif type == ZONE2:
                            if currentZONE2[0] == tattooId:
                                equipped = True

                        elif type == ZONE3:
                            if currentZONE3[0] == tattooId:
                                equipped = True

                        elif type == ZONE4:
                            if currentZONE4[0] == tattooId:
                                equipped = True

                        else:
                            equipped = False
                        tattoos.append([
                            id,
                            equipped,
                            cost,
                            tattooId,
                            holiday])

            else:
                return

        tattoos.sort(self.sortItems)
        for item in self.buttons:
            item.destroy()

        startPos = Vec3(0.35, 0.0, 1.05)
        buttonScale = Vec3(0.6, 0.6, 0.6)
        self.buttons = []
        self.tattooAmount = 0
        self.buttonIndex = startIndex
        if self.mode == 0:
            self.storeButton['state'] = DGG.DISABLED
            self.wardrobeButton['state'] = DGG.NORMAL
            buttonColorA = Vec4(0.7, 0.95, 0.7, 1.0)
            buttonColorB = Vec4(0.4, 0.65, 0.4, 1.0)
            self.purchaseInventory.setItemColor(Vec4(0.3, 0.95, 0.3, 1.0))
        elif self.mode == 1:
            self.storeButton['state'] = DGG.NORMAL
            self.wardrobeButton['state'] = DGG.DISABLED
            buttonColorA = Vec4(0.95, 0.7, 0.7, 1.0)
            buttonColorB = Vec4(0.65, 0.4, 0.4, 1.0)
            self.sellInventory.setItemColor(Vec4(0.95, 0.3, 0.3, 1.0))

        regionData = []
        for tattoo in tattoos:
            if self.tattooAmount - startIndex < self.buttonsPerPage and self.tattooAmount >= startIndex:
                uid = tattoo[0]
                item = TattooGlobals.tattoos.get(uid)
                type = item[0]
                desc = item[3]
                cost = item[4]
                tattooId = item[1]
                owned = False
                equipped = tattoo[1]
                questDrop = False
                img = None
                filename = 'tattoo_' + TattooGlobals.tattooNames[tattooId]
                if tattooId != 0:
                    img = tattoo_tex.find('**/' + filename)
                else:
                    img = None
                if uid in TattooGlobals.quest_items:
                    questDrop = True
                    helpText = '%s!\n\n%s' % (PLocalizer.ShopQuestItem, desc)
                else:
                    helpText = desc
                if self.mode == 1:
                    cost = int(cost * 0.25)

                for item in self.currentWardrobe:
                    if uid == item:
                        owned = True

                if self.mode == 1:
                    buttonState = DGG.DISABLED
                else:
                    buttonState = DGG.NORMAL
                tattooButton = GuiButton.GuiButton(command = self.applyTattoo, parent = self.panel, state = buttonState, text_fg = PiratesGuiGlobals.TextFG2, text_pos = (-0.02, -0.05), text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ALeft, text_shadow = PiratesGuiGlobals.TextShadow, pos = startPos, image_scale = buttonScale, image_color = buttonColorA, helpText = helpText, helpDelay = 0, helpPos = (0.0, 0.0, -0.11), helpLeftAlign = True, extraArgs = [
                    self.pirate,
                    type,
                    uid])
                if tattooId == 0:
                    tattooButton['text_pos'] = (-0.13, 0.02)
                    tattooButton['text'] = desc
                    tattooButton['text_wordwrap'] = 5
                    tattooButton['text_align'] = TextNode.ACenter

                if img:
                    cm = CardMaker('mapTexture')
                    tex = img.findAllTextures()[0]
                    height = tex.getYSize()
                    width = tex.getXSize()
                    scale = float(width) / float(height)
                    cm.setFrame(-0.22, -0.04, -0.072, 0.078)
                    geom = NodePath(cm.generate())
                    geom.setTexture(tex)
                    if scale == 1.0:
                        geom.setScale(scale, 1.0, 1.0)
                        geom.setPos(0.0, 0.0, 0.01)
                    elif scale < 1.0:
                        geom.setScale(scale, 1.0, 1.0)
                        scale = scale * -0.13
                        geom.setPos(scale, 0.0, 0.01)
                    else:
                        scale = float(height) / float(width)
                        geom.setScale(1.0, 1.0, scale)
                        geom.setPos(0.0, 0.0, 0.01)
                    geom.reparentTo(tattooButton)

                tattooButton.helpWatcher.setPos(tattooButton.getPos())
                tattooButton.itemText = DirectFrame(parent = tattooButton, relief = None, text = '', text_fg = PiratesGuiGlobals.TextFG1, text_align = TextNode.ACenter, text_scale = PiratesGuiGlobals.TextScaleSmall, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = True, pos = (-0.13, 0, -0.085))
                if self.mode == 0 and not owned:
                    tattooButton.itemText['text'] = PLocalizer.TailorPreview
                    tattooButton.itemText['image'] = None
                elif self.mode == 1 and equipped:
                    tattooButton.itemText['text'] = PLocalizer.TattooShopOwned
                    tattooButton.itemText['image'] = None
                else:
                    tattooButton.itemText['text'] = ''
                    tattooButton.itemText['image'] = None
                if questDrop is True and self.mode == 1:
                    tattooButton.itemText['image'] = self.questIcon
                    tattooButton.itemText['image_color'] = Vec4(1, 1, 0, 1)
                    tattooButton.itemText['image_scale'] = 0.2
                    tattooButton.itemText['image_pos'] = (-0.12, 0, 0.15)

                tattooButton.addToCart = GuiButton.GuiButton(command = self.addToCart, parent = tattooButton, text_fg = PiratesGuiGlobals.TextFG2, text_pos = (0.0, -0.01), text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_shadow = PiratesGuiGlobals.TextShadow, image_color = buttonColorB, pos = (0.16, 0.0, 0.055))
                tattooButton.addToCart['extraArgs'] = [
                    tattooButton,
                    type,
                    uid]
                if self.mode == 0 and not owned:
                    cImage = self.CoinImage
                    if self.pvpMode:
                        cImage = self.RenownImage

                    tattooButton.cost = DirectFrame(parent = tattooButton, relief = None, text = str(cost), text_fg = PiratesGuiGlobals.TextFG2, text_align = TextNode.ARight, text_scale = PiratesGuiGlobals.TextScaleLarge, text_pos = (-0.055, 0.0), text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 0, image = cImage, image_scale = 0.15, image_pos = (-.025, 0, 0.015), pos = (0.25, 0, -0.05))
                elif self.mode == 1:
                    if not equipped:
                        tattooButton.equip = GuiButton.GuiButton(parent = tattooButton, command = self.equipTattoo, text = PLocalizer.TailorEquip, text_fg = PiratesGuiGlobals.TextFG2, text_pos = (0.0, -0.01), text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_shadow = PiratesGuiGlobals.TextShadow, image_color = buttonColorB, pos = (0.16, 0.0, -0.05))
                        tattooButton.equip['extraArgs'] = [
                            [
                                tattooButton,
                                type,
                                uid]]
                    else:
                        tattooButton.equip = GuiButton.GuiButton(parent = tattooButton, command = self.equipTattoo, text = PLocalizer.TailorTakeOff, text_fg = PiratesGuiGlobals.TextFG2, text_pos = (0.0, -0.01), text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_shadow = PiratesGuiGlobals.TextShadow, image_color = buttonColorB, pos = (0.16, 0.0, -0.05))
                        tattooButton.equip['extraArgs'] = [
                            [
                                tattooButton,
                                type,
                                -1]]

                if self.paid == OTPGlobals.AccessVelvetRope:
                    if self.mode == 1:
                        tattooButton.equip['geom'] = self.LockIcon
                        tattooButton.equip['geom_scale'] = 0.2
                        tattooButton.equip['geom_pos'] = Vec3(-0.1, 0.0, 0.0)
                        tattooButton.equip['command'] = localAvatar.guiMgr.showNonPayer
                        tattooButton.equip['extraArgs'] = [
                            'JEWELRY_CANNOT_EQUIP',
                            10]

                    tattooButton.addToCart['geom'] = self.LockIcon
                    tattooButton.addToCart['geom_scale'] = 0.2
                    tattooButton.addToCart['geom_pos'] = Vec3(-0.1, 0.0, 0.0)
                    tattooButton.addToCart['command'] = localAvatar.guiMgr.showNonPayer
                    tattooButton.addToCart['extraArgs'] = [
                        'JEWELRY_CANNOT_BUY-SELL',
                        10]

                data = [
                    type,
                    uid,
                    tattooId]
                if self.mode == 0 and owned:
                    tattooButton.addToCart.buyState = 0
                    tattooButton.addToCart['state'] = DGG.DISABLED
                    tattooButton['state'] = DGG.DISABLED
                    tattooButton.addToCart['text'] = PLocalizer.TailorPurchased
                    tattooButton.addToCart.show()
                elif self.mode == 0 and self.purchaseInventory.hasPanel(data):
                    tattooButton.addToCart.buyState = 0
                    tattooButton.addToCart['state'] = DGG.NORMAL
                    tattooButton.addToCart['text'] = PLocalizer.TailorRemove
                    tattooButton.addToCart.show()
                elif self.mode == 1 and self.sellInventory.hasPanel(data):
                    tattooButton.addToCart.buyState = 0
                    tattooButton.addToCart['state'] = DGG.NORMAL
                    tattooButton.addToCart['text'] = PLocalizer.TailorRemove
                    tattooButton.addToCart.show()
                    tattooButton.equip['state'] = DGG.DISABLED
                else:
                    tattooButton.addToCart.buyState = 1
                    tattooButton.addToCart['state'] = DGG.NORMAL
                    tattooButton.addToCart.show()
                    if self.mode == 0:
                        tattooButton.addToCart['text'] = PLocalizer.TailorAddToCart
                    elif self.mode == 1:
                        tattooButton.equip['state'] = DGG.NORMAL
                        tattooButton.addToCart['text'] = PLocalizer.TailorSell

                startPos -= Vec3(0.0, 0.0, tattooButton.getHeight() - 0.02)
                tattooButton.tattooType = tattooType
                tattooButton.tattooUID = uid
                tattooButton.equipped = equipped
                tattooButton.questDrop = questDrop
                self.buttons.append(tattooButton)

            self.tattooAmount += 1

        if not len(tattoos):
            tattooButton = GuiButton.GuiButton(parent = self.panel, state = DGG.DISABLED, text = PLocalizer.TailorEmptyWardrobe, text_fg = PiratesGuiGlobals.TextFG2, text_pos = (0.0, 0.0), text_scale = PiratesGuiGlobals.TextScaleLarge, text_align = TextNode.ACenter, text_shadow = PiratesGuiGlobals.TextShadow, pos = startPos, image_scale = buttonScale, image_color = buttonColorA)
            tattooButton.tattooType = -1
            tattooButton.tattooUID = -1
            self.buttons.append(tattooButton)

        if self.tattooAmount <= self.buttonsPerPage:
            self.nextPageButton['state'] = DGG.DISABLED
            self.prevPageButton['state'] = DGG.DISABLED

        if startIndex:
            self.prevPageButton['state'] = DGG.NORMAL

        if startIndex + self.buttonsPerPage < self.tattooAmount:
            self.nextPageButton['state'] = DGG.NORMAL
            self.prevPageButton['state'] = DGG.NORMAL

        if self.tattooAmount > self.buttonsPerPage:
            numPages = float(self.tattooAmount) / float(self.buttonsPerPage)
            remainder = numPages - int(numPages)
            if remainder > 0:
                numPages += 1.0 - remainder

            page = startIndex / self.buttonsPerPage + 1
        else:
            numPages = 1
            page = 1
        self.pageNumber['text'] = '%s %s / %s' % (PLocalizer.TailorPage, page, int(numPages))

    def _stopMouseReadTask(self):
        taskMgr.remove('TattooStore-MouseRead')

    def _startMouseReadTask(self):
        self._stopMouseReadTask()
        mouseData = base.win.getPointer(0)
        self.lastMousePos = (mouseData.getX(), mouseData.getY())
        taskMgr.add(self._mouseReadTask, 'TattooStore-MouseRead')

    def _mouseReadTask(self, task):
        if not base.mouseWatcherNode.hasMouse():
            pass
        else:
            winSize = (base.win.getXSize(), base.win.getYSize())
            mouseData = base.win.getPointer(0)
            if mouseData.getX() > winSize[0] or mouseData.getY() > winSize[1]:
                pass
            else:
                dx = mouseData.getX() - self.lastMousePos[0]
                mouseData = base.win.getPointer(0)
                self.lastMousePos = (mouseData.getX(), mouseData.getY())
                value = self.rotateSlider['value']
                value = max(-1, min(1, value + dx * 0.004))
                self.rotateSlider['value'] = value
        return Task.cont

    def showWardrobeLimitAlert(self, type):
        self.removeAlertDialog()
        limit = str(PiratesGlobals.WARDROBE_LIMIT_TATTOO)
        text = PLocalizer.ShopLimitTattoo % limit
        self.alertDialog = PDialog.PDialog(text = text, text_align = TextNode.ACenter, style = OTPDialog.Acknowledge, pos = (-0.65, 0.0, 0.0), command = self.removeAlertDialog)
        self.alertDialog.setBin('gui-fixed', 20, 20)

    def removeAlertDialog(self, value = None):
        if self.alertDialog:
            self.alertDialog.destroy()
            self.alertDialog = None

    def getMoney(self):
        inventory = base.localAvatar.getInventory()
        if inventory:
            if self.pvpMode:
                return inventory.getStackQuantity(InventoryType.PVPCurrentInfamy)
            else:
                return inventory.getStackQuantity(InventoryType.GoldInPocket)
        else:
            return 0

    def getMaxMoney(self, inventory):
        if inventory:
            if self.pvpMode:
                return inventory.getStackLimit(InventoryType.PVPCurrentInfamy)
            else:
                return inventory.getStackLimit(InventoryType.GoldInPocket)
        else:
            return 0
