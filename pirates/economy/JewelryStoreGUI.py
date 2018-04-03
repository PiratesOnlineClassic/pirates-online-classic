# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.economy.JewelryStoreGUI
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
from pirates.makeapirate import JewelryGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.uberdog.UberDogGlobals import InventoryType
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from pirates.piratesgui import PDialog
from direct.task import Task
import random
from pirates.piratesbase import Freebooter
RBROW_CAMERA = 0
LBROW_CAMERA = 1
LEAR_CAMERA = 2
REAR_CAMERA = 3
NOSE_CAMERA = 4
MOUTH_CAMERA = 5
LHAND_CAMERA = 6
RHAND_CAMERA = 7

class JewelryStoreTab(LeftTab):
    __module__ = __name__

    def __init__(self, tabBar, name, **kw):
        optiondefs = (('suffix', '_d', None), ('borderScale', 0.38, None), ('bgBuffer', 0.15, None))
        self.defineoptions(kw, optiondefs)
        LeftTab.__init__(self, tabBar, name, **kw)
        self.initialiseoptions(JewelryStoreTab)
        return


class JewelryStoreTabBar(TabBar):
    __module__ = __name__

    def refreshTabs(self):
        for x, name in enumerate(self.tabOrder):
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
        return JewelryStoreTab(self, name, **kw)


class JewelryStoreCartList(DirectScrolledFrame):
    __module__ = __name__

    def __init__(self, parent, width, height, itemWidth, itemHeight):
        self.width = width + PiratesGuiGlobals.ScrollbarSize
        self.listItemHeight = itemHeight
        self.listItemWidth = itemWidth
        self.height = height
        self.parent = parent
        charGui = loader.loadModelOnce('models/gui/char_gui')
        DirectScrolledFrame.__init__(self, relief=None, state=DGG.NORMAL, manageScrollBars=0, autoHideScrollBars=1, frameSize=(0, self.width, 0, self.height), canvasSize=(0, self.width - 0.05, 0.025, self.height - 0.025), verticalScroll_relief=None, verticalScroll_image=charGui.find('**/chargui_slider_small'), verticalScroll_frameSize=(0, PiratesGuiGlobals.ScrollbarSize, 0, self.height), verticalScroll_image_scale=(self.height + 0.05, 1, 0.75), verticalScroll_image_hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           90), verticalScroll_image_pos=(self.width - PiratesGuiGlobals.ScrollbarSize * 0.5 - 0.004, 0, self.height * 0.5), verticalScroll_image_color=(0.61,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         0.6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         0.6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         1), verticalScroll_thumb_image=(charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over')), verticalScroll_thumb_relief=None, verticalScroll_thumb_image_scale=0.25, verticalScroll_resizeThumb=0, horizontalScroll_relief=None, sortOrder=5)
        self.initialiseoptions(JewelryStoreCartList)
        self.verticalScroll.incButton.destroy()
        self.verticalScroll.decButton.destroy()
        self.horizontalScroll.incButton.destroy()
        self.horizontalScroll.decButton.destroy()
        self.horizontalScroll.hide()
        self.panels = []
        self.purchases = []
        self.itemColor = Vec4(0.2, 0.2, 0.2, 1.0)
        charGui.removeNode()
        return

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

        self['canvasSize'] = (
         0, self.listItemWidth - 0.09, -z * (i + 1), 0)

    def addPanel(self, data, repack=1):
        uid = data[1]
        if self.parent.mode == 1:
            itemCost = int(JewelryGlobals.jewelry_id.get(uid)[3] * 0.25)
        else:
            itemCost = JewelryGlobals.jewelry_id.get(uid)[3]
        itemType = JewelryGlobals.jewelry_id.get(uid)[1]
        itemText = PLocalizer.JewelryNames.get(itemType) + ' ' + PLocalizer.Jewelry
        maxLength = 25 - len(str(itemCost))
        isDisabled = 0
        panel = DirectButton(parent=self, relief=None, text=itemText[:maxLength], text_fg=self.itemColor, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleMed, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.06,
                                                                                                                                                                                                                                    0.0), command=self.removePanel, extraArgs=[data])
        panel.costLabel = DirectLabel(parent=panel, relief=None, text=str(itemCost), text_fg=self.itemColor, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleMed, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.45,
                                                                                                                                                                                                                                        0.0), image=self.parent.CoinImage, image_scale=0.15, image_pos=(0.48,
                                                                                                                                                                                                                                                                                                        0.0,
                                                                                                                                                                                                                                                                                                        0.014))
        panel.bind(DGG.ENTER, self.highlightStart, extraArgs=[panel])
        panel.bind(DGG.EXIT, self.highlightStop, extraArgs=[panel])
        panel.data = data
        panel.price = itemCost
        panel.reparentTo(self.getCanvas())
        self.panels.append(panel)
        self.purchases.append(data)
        if repack:
            self.repackPanels()
        return

    def highlightStart(self, item, event=None):
        item['text_fg'] = PiratesGuiGlobals.TextFG6
        item.costLabel['text_fg'] = PiratesGuiGlobals.TextFG6

    def highlightStop(self, item, event=None):
        item['text_fg'] = self.itemColor
        item.costLabel['text_fg'] = self.itemColor

    def removePanel(self, data, repack=1):
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


class JewelryStoreGUI(DirectFrame):
    __module__ = __name__
    notify = directNotify.newCategory('JewelryStoreGUI')
    width = (PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.06) * 2
    height = 1.5
    columnWidth = PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.05
    holidayIdList = []

    def __init__(self, npc, shopId, **kw):
        optiondefs = (
         ('relief', None, None), ('framSize', (0, self.width, 0, self.height), None), ('sortOrder', 20, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, None, **kw)
        self.initialiseoptions(JewelryStoreGUI)
        self.pirate = None
        self.camIval = None
        self.buttons = []
        self.buttonIndex = 0
        self.jewelryAmount = 0
        self.currentPage = None
        self.buttonsPerPage = 4
        self.displayRegionStates = {}
        self.prevIdx = 0
        self.mode = 0
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.CoinImage = gui.find('**/treasure_w_coin*')
        self.ParchmentIcon = gui.find('**/main_gui_quest_scroll')
        self.jewelerIconsA = loader.loadModelOnce('models/gui/char_gui')
        self.jewelerIconsB = loader.loadModelOnce('models/textureCards/shopIcons')
        self.ShirtIcon = loader.loadModelOnce('models/gui/char_gui').find('**/chargui_cloth')
        self.LockIcon = gui.find('**/subscribers_lock')
        self.backTabParent = self.attachNewNode('backTabs', sort=0)
        self.panel = GuiPanel.GuiPanel(None, self.width, self.height, parent=self, showClose=False)
        self.setPos(0.0, 0, -0.75)
        self.balance = 0
        self.npc = npc
        self.rootTitle = PLocalizer.JewelryStore
        if Freebooter.AllAccessHoliday:
            self.paid = Freebooter.FULL
        else:
            self.paid = base.cr.isPaid()
        self.shopId = shopId
        if localAvatar.gameFSM.camIval is not None:
            if localAvatar.gameFSM.camIval.isPlaying():
                localAvatar.gameFSM.camIval.finish()
        self.initialCamPos = camera.getPos()
        self.initialCamHpr = camera.getHpr()
        self.initialPirateH = 0
        self.cartWidth = self.columnWidth - 0.1
        self.cartHeight = self.height - 0.25
        self.cartFrame = DirectFrame(parent=self.panel, relief=None, frameSize=(0, self.cartWidth, 0, self.cartHeight))
        self.cartFrame.setPos(self.columnWidth + 0.025, 0, 0.08)
        self.categoryText = [
         [
          PLocalizer.Hat, PLocalizer.Hats], [PLocalizer.Shirt, PLocalizer.Shirts], [PLocalizer.Vest, PLocalizer.Vests], [PLocalizer.Coat, PLocalizer.Coats], [PLocalizer.Pants, PLocalizer.Pants], [PLocalizer.Belt, PLocalizer.Belts], [None, None], [PLocalizer.Shoe, PLocalizer.Shoes]]
        self.buyParchment = DirectFrame(parent=self.cartFrame, relief=None, text=PLocalizer.TailorPurchase, text_fg=PiratesGuiGlobals.TextFG1, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                                                   0.2), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, image=self.ParchmentIcon, image_scale=(0.24,
                                                                                                                                                                                                                                                                                                                                           0.0,
                                                                                                                                                                                                                                                                                                                                           0.3), image_pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                            0.0,
                                                                                                                                                                                                                                                                                                                                                            0.0), pos=(0.3,
                                                                                                                                                                                                                                                                                                                                                                       0.0,
                                                                                                                                                                                                                                                                                                                                                                       0.92))
        self.sellParchment = DirectFrame(parent=self.cartFrame, relief=None, text=PLocalizer.TailorSelling, text_fg=PiratesGuiGlobals.TextFG1, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                                                   0.2), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, image=self.ParchmentIcon, image_scale=(0.24,
                                                                                                                                                                                                                                                                                                                                           0.0,
                                                                                                                                                                                                                                                                                                                                           0.3), image_pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                            0.0,
                                                                                                                                                                                                                                                                                                                                                            0.0), pos=(0.3,
                                                                                                                                                                                                                                                                                                                                                                       0.0,
                                                                                                                                                                                                                                                                                                                                                                       0.48))
        self.purchaseInventory = JewelryStoreCartList(self, self.cartWidth, self.cartHeight - 0.95, self.cartWidth, self.cartHeight / 20.0)
        self.purchaseInventory.reparentTo(self.cartFrame)
        self.purchaseInventory.setPos(0.0, 0.0, 0.76)
        self.sellInventory = JewelryStoreCartList(self, self.cartWidth, self.cartHeight - 0.95, self.cartWidth, self.cartHeight / 20.0)
        self.sellInventory.reparentTo(self.cartFrame)
        self.sellInventory.setPos(0.0, 0.0, 0.31)
        self.frontTabParent = self.panel.attachNewNode('frontTab', sort=2)
        self.currentWardrobe = None
        self.balanceTitle = DirectFrame(parent=self.cartFrame, relief=None, text=PLocalizer.Total, text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                                        0.0), text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.09,
                                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                                             0.225))
        self.balanceValue = DirectFrame(parent=self.cartFrame, relief=None, text=str(self.balance), text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(-0.055, 0.0), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, image=self.CoinImage, image_scale=0.15, image_pos=(-0.025,
                                                                                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                                                                                      0.015), pos=(self.cartWidth, 0, 0.225))
        self.myGoldTitle = DirectFrame(parent=self.cartFrame, relief=None, text=PLocalizer.YourMoney, text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                                           0.0), text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.09,
                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                0.155))
        self.myGold = DirectFrame(parent=self.cartFrame, relief=None, text=str(localAvatar.getMoney()), text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(-0.055, 0.0), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, image=self.CoinImage, image_scale=0.15, image_pos=(-0.025,
                                                                                                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                                                                                                          0.015), pos=(self.cartWidth, 0, 0.155))
        self.commitButton = DialogButton.DialogButton(command=self.handleCommitPurchase, parent=self.cartFrame, text=PLocalizer.PurchaseCommit, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.02, -PiratesGuiGlobals.TextScaleLarge * 0.25), text_scale=PiratesGuiGlobals.TextScaleLarge, text_shadow=PiratesGuiGlobals.TextShadow, buttonStyle=DialogButton.DialogButton.YES)
        self.commitButton.setPos(self.cartWidth / 2, 0, 0.005)
        self.closeButton = DialogButton.DialogButton(command=self.closePanel, parent=self.cartFrame, text=PLocalizer.lClose, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.02, -PiratesGuiGlobals.TextScaleLarge * 0.25), text_scale=PiratesGuiGlobals.TextScaleLarge, text_shadow=PiratesGuiGlobals.TextShadow, buttonStyle=DialogButton.DialogButton.NO)
        self.closeButton.setPos(self.cartWidth / 2 - 0.55, 0, 0.005)
        self.storeButton = DialogButton.DialogButton(command=self.changeMode, state=DGG.DISABLED, parent=self, text=PLocalizer.InteractStore, text_fg=PiratesGuiGlobals.TextFG2, text_scale=PiratesGuiGlobals.TextScaleLarge, text_shadow=PiratesGuiGlobals.TextShadow, image_color=Vec4(0.7, 0.95, 0.7, 1.0), scale=0.9, extraArgs=[0])
        self.storeButton.setPos(0.23, 0.0, 1.21)
        self.wardrobeButton = DialogButton.DialogButton(command=self.changeMode, state=DGG.NORMAL, parent=self, text=PLocalizer.TailorWardrobe, text_fg=PiratesGuiGlobals.TextFG2, text_scale=PiratesGuiGlobals.TextScaleLarge, text_shadow=PiratesGuiGlobals.TextShadow, image_color=Vec4(0.95, 0.7, 0.7, 1.0), scale=0.9, extraArgs=[1])
        self.wardrobeButton.setPos(0.45, 0.0, 1.21)
        tGui = loader.loadModel('models/gui/triangle')
        triangle = (tGui.find('**/triangle'), tGui.find('**/triangle_down'), tGui.find('**/triangle_over'))
        self.nextPageButton = DirectButton(parent=self.panel, relief=None, state=DGG.DISABLED, image=triangle, image_scale=0.065, pos=(0.54,
                                                                                                                                       0.0,
                                                                                                                                       0.175), rolloverSound=None, command=self.nextPage)
        self.prevPageButton = DirectButton(parent=self.panel, relief=None, state=DGG.DISABLED, image=triangle, image_scale=-0.065, pos=(0.16,
                                                                                                                                        0.0,
                                                                                                                                        0.175), rolloverSound=None, command=self.previousPage)
        self.pageNumber = DirectFrame(parent=self.panel, relief=None, text='', text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                      0.0), text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.35,
                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                           0.1625))
        self.titleLabel = DirectLabel(parent=self, relief=None, text='', text_fg=PiratesGuiGlobals.TextFG1, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge * 1.3, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.62,
                                                                                                                                                                                                                                           0.0,
                                                                                                                                                                                                                                           1.33))
        self.titleLabel.setBin('gui-fixed', 1)
        self.createPirate()
        charGui = loader.loadModel('models/gui/char_gui')
        self.rotateSlider = DirectSlider(parent=base.a2dBottomLeft, relief=None, command=self.rotatePirate, image=charGui.find('**/chargui_slider_small'), image_scale=(2.15,
                                                                                                                                                                        2.15,
                                                                                                                                                                        1.5), thumb_relief=None, thumb_image=(charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over')), pos=(0.8,
                                                                                                                                                                                                                                                                                                                                                      0.0,
                                                                                                                                                                                                                                                                                                                                                      0.09), text_align=TextNode.ACenter, text_scale=(0.1,
                                                                                                                                                                                                                                                                                                                                                                                                      0.1), text_pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                                                                                      0.1), text_fg=PiratesGuiGlobals.TextFG1, scale=0.43, text=PLocalizer.RotateSlider, value=0.5, sortOrder=-1)
        self.rotateSlider['extraArgs'] = [
         self.rotateSlider]
        self.rotateSliderOrigin = 0.5
        self.accept('mouse1', self._startMouseReadTask)
        self.accept('mouse1-up', self._stopMouseReadTask)
        self.clothWindows = []
        self.clothRenders = []
        self.clothHumans = []
        self.clothCameraNPs = []
        self.clothCameras = []
        self.createDisplayRegions()
        self.alertDialog = None
        self.accept('aspectRatioChanged', self.aspectRatioChange)
        self.accept('NonPayerPanelShown', self.hideDisplayRegions)
        self.accept('NonPayerPanelHidden', self.showDisplayRegions)
        self.accept('GameOptionsShown', self.hideDisplayRegions)
        self.accept('GameOptionsHidden', self.showDisplayRegions)
        self.accept('GUIShown', self.hideDisplayRegions)
        self.accept('GUIHidden', self.showDisplayRegions)
        localAvatar.guiMgr.chatPanel.show()
        localAvatar.guiMgr.chatPanel.startFadeTextIval()
        self.accept(localAvatar.uniqueName('jewelryUpdate'), self.reloadPirateDNA, extraArgs=[self.pirate])
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
        self.equipRequests = {JewelryGlobals.RBROW: None, JewelryGlobals.LBROW: None, JewelryGlobals.LEAR: None, JewelryGlobals.REAR: None, JewelryGlobals.NOSE: None, JewelryGlobals.MOUTH: None, JewelryGlobals.LHAND: None, JewelryGlobals.RHAND: None}
        self.initTabs()
        self.updateBalance()
        return

    def hideDisplayRegions(self):
        for id in range(len(self.clothRenders)):
            if self.clothRenders[id].isHidden():
                self.displayRegionStates[id] = False
            else:
                self.displayRegionStates[id] = True
            self.clothRenders[id].hide()

    def showDisplayRegions(self):
        for id in range(len(self.clothRenders)):
            if self.displayRegionStates[id]:
                self.clothRenders[id].show()

    def aspectRatioChange(self):
        properties = base.win.getProperties()
        x = properties.getXSize()
        y = properties.getYSize()
        ar = float(x) / float(y)
        width = 0.1 * aspect2d.getScale()[0]
        height = 0.075 * aspect2d.getScale()[2]
        offsetX = 0.13 * aspect2d.getScale()[0]
        offsetY = -0.015 * aspect2d.getScale()[2]
        for id in range(len(self.buttons)):
            button = self.buttons[id]
            displayRegion = self.clothWindows[id]
            p = button.getPos(render2d) - Point3(width + offsetX, 0, height + offsetY)
            pv = Point3((p[0] + 1) / 2.0, 0.0, (p[2] + 1) / 2.0)
            displayRegion.setDimensions(pv[0], pv[0] + width, pv[2], pv[2] + height)

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
        self.cleanupRegions()
        self.unloadPirate()
        if self.model:
            self.model.removeNode()
            self.model = None
        if self.CoinImage:
            self.CoinImage.removeNode()
            self.CoinImage = None
        if self.ParchmentIcon:
            self.ParchmentIcon.removeNode()
            self.ParchmentIcon = None
        if self.ShirtIcon:
            self.ShirtIcon.removeNode()
            self.ShirtIcon = None
        if self.jewelerIconsA:
            self.jewelerIconsA.removeNode()
            self.jewelerIconsA = None
        if self.jewelerIconsB:
            self.jewelerIconsB.removeNode()
            self.jewelerIconsB = None
        if self.alertDialog:
            self.alertDialog.destroy()
        if localAvatar.guiMgr.questPage and len(localAvatar.guiMgr.questPage.trackedQuestLabel['text']):
            if self.showQuestLabel:
                localAvatar.guiMgr.questPage.trackedQuestLabel.show()
        localAvatar.guiMgr.chatPanel.hide()
        return

    def createPirate(self):
        if self.pirate is None:
            self.pirate = DynamicHuman.DynamicHuman()
            self.pirate.setDNAString(localAvatar.style)
            self.pirate.generateHuman(localAvatar.style.gender)
            self.pirate.model.setupSelectionChoices('DEFAULT')
            self.pirate.mixingEnabled = False
            self.pirate.enableBlend()
            self.pirate.loop('idle_centered')
            self.pirate.loop('idle')
            self.pirate.setControlEffect('idle_centered', 0)
            self.pirate.setControlEffect('idle', 1)
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
        self.pirate.show()
        localAvatar.stash()
        return

    def focusCamera(self, cameraId=RBROW_CAMERA):
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
        if cameraId == RBROW_CAMERA:
            dummy.setPos(dummy, 1, 2, self.pirate.headNode.getZ(self.pirate) + 0.5)
        else:
            if cameraId == LBROW_CAMERA:
                dummy.setPos(dummy, -1, 2, self.pirate.headNode.getZ(self.pirate) + 0.5)
            else:
                if cameraId == LEAR_CAMERA:
                    dummy.setPos(dummy, -2, 2, self.pirate.headNode.getZ(self.pirate) + 0.25)
                else:
                    if cameraId == REAR_CAMERA:
                        dummy.setPos(dummy, 2, 2, self.pirate.headNode.getZ(self.pirate) + 0.25)
                    else:
                        if cameraId == NOSE_CAMERA:
                            dummy.setPos(dummy, 0, 2, self.pirate.headNode.getZ(self.pirate) + 0.25)
                        else:
                            if cameraId == MOUTH_CAMERA:
                                dummy.setPos(dummy, 0, 2, self.pirate.headNode.getZ(self.pirate))
                            else:
                                if cameraId == LHAND_CAMERA:
                                    dummy.setPos(dummy, -2, 2.5, self.pirate.leftHandNode.getZ(self.pirate))
                                else:
                                    if cameraId == RHAND_CAMERA:
                                        dummy.setPos(dummy, 2, 2.5, self.pirate.rightHandNode.getZ(self.pirate))
                                    else:
                                        dummy.setPos(dummy, 0, 0, 0)
        dummy.wrtReparentTo(render)
        if cameraId == RBROW_CAMERA:
            dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 1.1)
        else:
            if cameraId == LBROW_CAMERA:
                dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 1.1)
            else:
                if cameraId == LEAR_CAMERA:
                    dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 1.1)
                else:
                    if cameraId == REAR_CAMERA:
                        dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 1.1)
                    else:
                        if cameraId == NOSE_CAMERA:
                            dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 1.1)
                        else:
                            if cameraId == MOUTH_CAMERA:
                                dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 1.075)
                            else:
                                if cameraId == LHAND_CAMERA:
                                    dummy.lookAt(self.pirate, self.pirate.leftHandNode.getX(self.pirate), self.pirate.leftHandNode.getY(self.pirate), self.pirate.leftHandNode.getZ(self.pirate) * 1.2)
                                else:
                                    if cameraId == RHAND_CAMERA:
                                        dummy.lookAt(self.pirate, self.pirate.rightHandNode.getX(self.pirate), self.pirate.rightHandNode.getY(self.pirate), self.pirate.rightHandNode.getZ(self.pirate) * 1.2)
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
        self.camIval = camera.posHprInterval(t, pos=camPos, hpr=camHpr, blendType='easeOut')
        localAvatar.cameraFSM.request('Control')
        self.camIval.start()
        return

    def unloadPirate(self):
        if self.pirate:
            self.pirate.detachNode()
            self.pirate.cleanupHuman()
            self.pirate.delete()
            self.pirate = None
        localAvatar.unstash()
        return

    def closePanel(self):
        messenger.send('exitStore')
        self.ignoreAll()
        camera.setPos(self.initialCamPos)
        camera.setHpr(self.initialCamHpr)
        equips = []
        for type in self.equipRequests.keys():
            equip = self.equipRequests.get(type)
            id = 0
            primary = 0
            secondary = 0
            if equip is not None:
                uid = equip[0]
                item = JewelryGlobals.jewelry_id.get(uid)
                if item is not None:
                    equips.append([type, uid])
                    id = item[0]
                    primary = item[4]
                    secondary = item[5]
                else:
                    equips.append([type, -1])
                    id = -1
                    primary = 0
                    secondary = 0
                if type == JewelryGlobals.RBROW:
                    localAvatar.style.setJewelryZone4(id, primary, secondary)
                elif type == JewelryGlobals.LBROW:
                    localAvatar.style.setJewelryZone3(id, primary, secondary)
                elif type == JewelryGlobals.LEAR:
                    localAvatar.style.setJewelryZone1(id, primary, secondary)
                elif type == JewelryGlobals.REAR:
                    localAvatar.style.setJewelryZone2(id, primary, secondary)
                elif type == JewelryGlobals.NOSE:
                    localAvatar.style.setJewelryZone5(id, primary, secondary)
                elif type == JewelryGlobals.MOUTH:
                    localAvatar.style.setJewelryZone6(id, primary, secondary)
                elif type == JewelryGlobals.LHAND:
                    localAvatar.style.setJewelryZone7(id, primary, secondary)
                elif type == JewelryGlobals.RHAND:
                    localAvatar.style.setJewelryZone8(id, primary, secondary)

        if len(equips) > 0:
            self.npc.sendRequestJewelryEquip(equips)
            gender = localAvatar.style.getGender()
            localAvatar.generateHuman(gender, base.cr.human)
            localAvatar.motionFSM.off()
            localAvatar.motionFSM.on()
        self.unloadPirate()
        return

    def handleCommitPurchase(self):
        if self.purchaseInventory == []:
            base.localAvatar.guiMgr.createWarning(PLocalizer.EmptyPurchaseWarning, PiratesGuiGlobals.TextFG6)
            return
        inventory = base.localAvatar.getInventory()
        if inventory:
            if inventory.getStackQuantity(InventoryType.GoldInPocket) < self.balance:
                base.localAvatar.guiMgr.createWarning(PLocalizer.NotEnoughMoneyWarning, PiratesGuiGlobals.TextFG6)
                return
            if self.balance < 0 and inventory.getStackQuantity(InventoryType.GoldInPocket) + self.balance > inventory.getStackLimit(InventoryType.GoldInPocket):
                base.localAvatar.guiMgr.createWarning(PLocalizer.CannotHoldGoldWarning, PiratesGuiGlobals.TextFG6)
                return
        purchaseArgList = []
        sellArgList = []
        for item in self.purchaseInventory.purchases:
            uid = item[1]
            item = JewelryGlobals.jewelry_id.get(uid)
            if item:
                id = item[0]
                type = item[1]
                primary = item[4]
                secondary = item[5]
                purchaseArgList.append(uid)
                self.equipRequests[type] = [
                 uid, id, primary, secondary]

        for item in self.sellInventory.purchases:
            uid = item[1]
            item = JewelryGlobals.jewelry_id.get(uid)
            if item:
                id = item[0]
                type = item[1]
                primary = item[4]
                secondary = item[5]
                sellArgList.append(uid)
                if self.equipRequests[type] == [uid, id, primary, secondary]:
                    self.equipRequests[type] = None

        self.purchaseInventory.removeAllPanels()
        self.sellInventory.removeAllPanels()
        self.npc.sendRequestJewelry(purchaseArgList, sellArgList)
        self.changeMode(1, refresh=True)
        return

    def updateBalance(self, extraArgs=None):
        self.myGold['text'] = str(localAvatar.getMoney())
        self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG2
        self.balance = 0
        for item in self.purchaseInventory.panels:
            self.balance += max(item.price, 1)

        for item in self.sellInventory.panels:
            self.balance -= max(item.price, 1)

        transactions = len(self.purchaseInventory.purchases) + len(self.sellInventory.purchases)
        if self.balance > 0:
            self.balanceTitle['text'] = PLocalizer.Total
            self.balanceValue['text'] = str(abs(self.balance))
            self.commitButton['text'] = PLocalizer.PurchaseCommit
        else:
            if self.balance < 0:
                self.balanceTitle['text'] = PLocalizer.Gain
                self.balanceValue['text'] = str(abs(self.balance))
                self.commitButton['text'] = PLocalizer.TailorSell
            else:
                self.balanceTitle['text'] = PLocalizer.Total
                self.balanceValue['text'] = str(abs(self.balance))
                self.commitButton['text'] = PLocalizer.GenericConfirmDone
        if self.balance > localAvatar.getMoney() or transactions == 0:
            if self.balance > localAvatar.getMoney():
                self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG6
            self.commitButton['state'] = DGG.DISABLED
        else:
            if self.balance < 0:
                self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG4
                self.commitButton['state'] = DGG.NORMAL
            else:
                self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG2
                self.commitButton['state'] = DGG.NORMAL
        inventory = base.localAvatar.getInventory()
        if inventory:
            if inventory.getStackQuantity(InventoryType.GoldInPocket) < self.balance or self.purchaseInventory.panels == []:
                self.commitButton['frameColor'] = PiratesGuiGlobals.ButtonColor3
            else:
                self.commitButton['frameColor'] = PiratesGuiGlobals.ButtonColor4

    def checkPanel(self, panel, inventory, itemId):
        purchaseQty = self.purchaseInventory.getItemQuantity(itemId)
        panel.checkPlayerInventory(itemId, purchaseQty)

    def initTabs(self):
        self.tabBar = JewelryStoreTabBar(parent=self, backParent=self.backTabParent, frontParent=self.frontTabParent, offset=0)
        self.pageNames = []
        self.createTabs()
        if len(self.pageNames) > 0:
            self.setPage(self.pageNames[0])

    def createTabs(self):
        for item in JewelryGlobals.JewelryTypes:
            if not self.isPageAdded(item):
                self.addTab(item)

    def addTab(self, id):
        newTab = self.tabBar.addTab(id, command=self.setPage, extraArgs=[id])
        if id == JewelryGlobals.RBROW:
            tabIcon = self.jewelerIconsB.find('**/icon_shop_tailor_brow')
            tabScale = (-0.5, 0.5, 0.5)
        else:
            if id == JewelryGlobals.LBROW:
                tabIcon = self.jewelerIconsB.find('**/icon_shop_tailor_brow')
                tabScale = (0.5, 0.5, 0.5)
            else:
                if id == JewelryGlobals.LEAR:
                    tabIcon = self.jewelerIconsA.find('**/chargui_ears')
                    tabScale = (1.7, 1.7, 1.7)
                else:
                    if id == JewelryGlobals.REAR:
                        tabIcon = self.jewelerIconsA.find('**/chargui_ears')
                        tabScale = (-1.7, 1.7, 1.7)
                    else:
                        if id == JewelryGlobals.NOSE:
                            tabIcon = self.jewelerIconsA.find('**/chargui_nose')
                            tabScale = 1.7
                        else:
                            if id == JewelryGlobals.MOUTH:
                                tabIcon = self.jewelerIconsA.find('**/chargui_mouth')
                                tabScale = 1.7
                            else:
                                if id == JewelryGlobals.LHAND:
                                    tabIcon = self.jewelerIconsB.find('**/icon_shop_tailor_hand')
                                    tabScale = (0.5, 0.5, 0.5)
                                else:
                                    if id == JewelryGlobals.RHAND:
                                        tabIcon = self.jewelerIconsB.find('**/icon_shop_tailor_hand')
                                        tabScale = (-0.5, 0.5, 0.5)
                                    else:
                                        tabIcon = None
                                        tabScale = 0.0
        tabText = PLocalizer.JewelryNames.get(id)
        newTab.nameTag = DirectLabel(parent=newTab, relief=None, state=DGG.DISABLED, pos=(0.06, 0, -0.035), text_fg=PiratesGuiGlobals.TextFG1, text_scale=0.2, image=tabIcon, image_scale=tabScale)
        self.pageNames.append(id)
        return

    def isPageAdded(self, pageName):
        return self.pageNames.count(pageName) > 0

    def nextPage(self):
        if self.jewelryAmount - (self.buttonIndex + self.buttonsPerPage) > 0:
            startIndex = self.buttonIndex + self.buttonsPerPage
            self.setPage(self.currentPage, startIndex, False)
        else:
            self.setPage(self.currentPage, 0, False)

    def previousPage(self):
        if self.buttonIndex > 0:
            startIndex = self.buttonIndex - self.buttonsPerPage
            self.setPage(self.currentPage, startIndex, False)
        else:
            remainder = self.jewelryAmount % self.buttonsPerPage
            if remainder:
                startIndex = self.jewelryAmount - remainder
            else:
                startIndex = self.jewelryAmount - self.buttonsPerPage
            self.setPage(self.currentPage, startIndex, False)

    def setJewelry(self, pirate, type, uid):
        item = JewelryGlobals.jewelry_id.get(uid)
        if not item:
            return
        idx = item[0]
        primaryColor = item[4]
        secondaryColor = item[5]
        if type == JewelryGlobals.LBROW:
            pirate.setJewelryZone3(idx, primaryColor, secondaryColor)
        else:
            if type == JewelryGlobals.RBROW:
                pirate.setJewelryZone4(idx, primaryColor, secondaryColor)
            else:
                if type == JewelryGlobals.LEAR:
                    pirate.setJewelryZone1(idx, primaryColor, secondaryColor)
                else:
                    if type == JewelryGlobals.REAR:
                        pirate.setJewelryZone2(idx, primaryColor, secondaryColor)
                    else:
                        if type == JewelryGlobals.NOSE:
                            pirate.setJewelryZone5(idx, primaryColor, secondaryColor)
                        else:
                            if type == JewelryGlobals.MOUTH:
                                pirate.setJewelryZone6(idx, primaryColor, secondaryColor)
                            else:
                                if type == JewelryGlobals.LHAND:
                                    pirate.setJewelryZone7(idx, primaryColor, secondaryColor)
                                else:
                                    if type == JewelryGlobals.RHAND:
                                        pirate.setJewelryZone8(idx, primaryColor, secondaryColor)
                                    else:
                                        print 'Unknown type'
        pirate.model.handleJewelryHiding()

    def addToCart(self, button, type, uid):
        data = [
         type, uid]
        if self.mode == 0:
            if button.addToCart.buyState:
                limit = PiratesGlobals.WARDROBE_LIMIT_JEWELER
                current = 0
                for id in self.currentWardrobe:
                    item = JewelryGlobals.jewelry_id.get(id)
                    if item:
                        itemType = item[1]
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
                    return
                self.purchaseInventory.addPanel(data)
                button.addToCart['text'] = PLocalizer.TailorRemove
                button.addToCart.buyState = 0
            else:
                button.addToCart['text'] = PLocalizer.TailorAddToCart
                button.addToCart.buyState = 1
                self.purchaseInventory.removePanel(data)
        else:
            if self.mode == 1:
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
            if item.jewelryUID == data[1]:
                if self.mode == 0 and item.jewelryUID not in self.currentWardrobe:
                    item.addToCart['text'] = PLocalizer.TailorAddToCart
                else:
                    if self.mode == 1:
                        item.addToCart['text'] = PLocalizer.TailorSell
                        item.equip['state'] = DGG.NORMAL
                item.addToCart.buyState = 1
                return

    def changeMode(self, mode, refresh=False):
        if self.mode == mode and not refresh:
            return
        else:
            if self.mode == mode and refresh:
                self.setPage(self.currentPage, 0, refreshWardrobe=refresh)
                return
        if self.mode == 0:
            self.prevIdx = self.buttonIndex
            idx = 0
        else:
            idx = self.prevIdx
        self.mode = mode
        self.setPage(self.currentPage, idx, refreshWardrobe=refresh)

    def setWardrobe(self, jewelry):
        if self.currentWardrobe:
            self.currentWardrobe = []
        self.currentWardrobe = jewelry
        self.setPage(self.currentPage, refreshWardrobe=False)

    def reloadPirateDNA(self, pirate):
        if self.equipRequests[JewelryGlobals.RBROW] is None:
            jewelryZone4 = list(localAvatar.style.getJewelryZone4())
        else:
            jewelryZone4 = list(self.equipRequests[JewelryGlobals.RBROW][1:])
        if self.equipRequests[JewelryGlobals.LBROW] is None:
            jewelryZone3 = list(localAvatar.style.getJewelryZone3())
        else:
            jewelryZone3 = list(self.equipRequests[JewelryGlobals.LBROW][1:])
        if self.equipRequests[JewelryGlobals.LEAR] is None:
            jewelryZone1 = list(localAvatar.style.getJewelryZone1())
        else:
            jewelryZone1 = list(self.equipRequests[JewelryGlobals.LEAR][1:])
        if self.equipRequests[JewelryGlobals.REAR] is None:
            jewelryZone2 = list(localAvatar.style.getJewelryZone2())
        else:
            jewelryZone2 = list(self.equipRequests[JewelryGlobals.REAR][1:])
        if self.equipRequests[JewelryGlobals.NOSE] is None:
            jewelryZone5 = list(localAvatar.style.getJewelryZone5())
        else:
            jewelryZone5 = list(self.equipRequests[JewelryGlobals.NOSE][1:])
        if self.equipRequests[JewelryGlobals.MOUTH] is None:
            jewelryZone6 = list(localAvatar.style.getJewelryZone6())
        else:
            jewelryZone6 = list(self.equipRequests[JewelryGlobals.MOUTH][1:])
        if self.equipRequests[JewelryGlobals.LHAND] is None:
            jewelryZone7 = list(localAvatar.style.getJewelryZone7())
        else:
            jewelryZone7 = list(self.equipRequests[JewelryGlobals.LHAND][1:])
        if self.equipRequests[JewelryGlobals.RHAND] is None:
            jewelryZone8 = list(localAvatar.style.getJewelryZone8())
        else:
            jewelryZone8 = list(self.equipRequests[JewelryGlobals.RHAND][1:])
        if not hasattr(pirate, 'style'):
            return
        pirate.style.setJewelryZone1(jewelryZone1[0], jewelryZone1[1], jewelryZone1[2])
        pirate.style.setJewelryZone2(jewelryZone2[0], jewelryZone2[1], jewelryZone2[2])
        pirate.style.setJewelryZone3(jewelryZone3[0], jewelryZone3[1], jewelryZone3[2])
        pirate.style.setJewelryZone4(jewelryZone4[0], jewelryZone4[1], jewelryZone4[2])
        pirate.style.setJewelryZone5(jewelryZone5[0], jewelryZone5[1], jewelryZone5[2])
        pirate.style.setJewelryZone6(jewelryZone6[0], jewelryZone6[1], jewelryZone6[2])
        pirate.style.setJewelryZone7(jewelryZone7[0], jewelryZone7[1], jewelryZone7[2])
        pirate.style.setJewelryZone8(jewelryZone8[0], jewelryZone8[1], jewelryZone8[2])
        pirate.model.handleJewelryHiding()
        return

    def equipJewelry(self, jewelry):
        type = jewelry[1]
        uid = jewelry[2]
        item = JewelryGlobals.jewelry_id.get(uid)
        itemButton = jewelry[0]
        if item:
            id = item[0]
            primary = item[4]
            secondary = item[5]
            self.equipRequests[type] = [
             uid, id, primary, secondary]
        else:
            self.equipRequests[type] = [
             -1, 0, 0, 0]
        self.reloadPirateDNA(self.pirate)
        for button in self.buttons:
            if button != itemButton:
                button.itemText['text'] = ''
                button.equip.show()
                button.equip['text'] = PLocalizer.TailorEquip
                button.equip['extraArgs'] = [[button, button.jewelryType, button.jewelryUID]]
                if button.questDrop is True:
                    button.itemText['text'] = PLocalizer.ShopQuestItem

        itemButton.itemText['text'] = PLocalizer.TattooShopOwned
        if item:
            itemButton.equip['text'] = PLocalizer.TailorTakeOff
            itemButton.equip['extraArgs'] = [[button, button.jewelryType, -1]]
        else:
            itemButton.equip['text'] = PLocalizer.TailorEquip
            itemButton.equip['extraArgs'] = [[button, button.jewelryType, button.jewelryUID]]
            if itemButton.questDrop is True:
                itemButton.itemText['text'] = PLocalizer.ShopQuestItem
            else:
                itemButton.itemText['text'] = ''

    def sortItems(self, item1, item2):
        if item1[1] == True:
            return -1
        else:
            if item2[1] == True:
                return 1
            else:
                if self.mode == 0:
                    if item1[6] is not None:
                        return -1
                    elif item2[6] is not None:
                        return 1
                    elif item1[3] > item2[3]:
                        return 1
                    elif item1[3] < item2[3]:
                        return -1
                    elif item1[4] > item2[4]:
                        return 1
                    elif item1[4] < item2[4]:
                        return -1
                    elif item1[5] > item2[5]:
                        return 1
                    elif item1[5] < item2[5]:
                        return -1
                    else:
                        return 0
                else:
                    if self.mode == 1:
                        if item1[2] < item2[2]:
                            return 1
                        elif item1[2] > item2[2]:
                            return -1
                        else:
                            return 0
        return

    def setPage(self, pageName, startIndex=0, refreshWardrobe=True):
        self.tabBar.unstash()
        self.titleLabel['text'] = '\x01smallCaps\x01' + self.rootTitle + ' - ' + PLocalizer.JewelryNames.get(pageName) + '\x02'
        previousPage = self.currentPage
        if self.currentPage != pageName:
            self.prevIdx = 0
        self.currentPage = pageName
        jewelryType = pageName
        if self.currentPage != previousPage:
            self.focusCamera(self.currentPage)
        if localAvatar.style.getGender() == 'm':
            GENDER = 'MALE'
        else:
            GENDER = 'FEMALE'
        if refreshWardrobe:
            self.npc.sendRequestJewelryList()
        if self.equipRequests[JewelryGlobals.RBROW] is None:
            currentRBROW = localAvatar.style.getJewelryZone4()
        else:
            currentRBROW = self.equipRequests[JewelryGlobals.RBROW][1:]
        if self.equipRequests[JewelryGlobals.LBROW] is None:
            currentLBROW = localAvatar.style.getJewelryZone3()
        else:
            currentLBROW = self.equipRequests[JewelryGlobals.LBROW][1:]
        if self.equipRequests[JewelryGlobals.LEAR] is None:
            currentLEAR = localAvatar.style.getJewelryZone1()
        else:
            currentLEAR = self.equipRequests[JewelryGlobals.LEAR][1:]
        if self.equipRequests[JewelryGlobals.REAR] is None:
            currentREAR = localAvatar.style.getJewelryZone2()
        else:
            currentREAR = self.equipRequests[JewelryGlobals.REAR][1:]
        if self.equipRequests[JewelryGlobals.NOSE] is None:
            currentNOSE = localAvatar.style.getJewelryZone5()
        else:
            currentNOSE = self.equipRequests[JewelryGlobals.NOSE][1:]
        if self.equipRequests[JewelryGlobals.MOUTH] is None:
            currentMOUTH = localAvatar.style.getJewelryZone6()
        else:
            currentMOUTH = self.equipRequests[JewelryGlobals.MOUTH][1:]
        if self.equipRequests[JewelryGlobals.LHAND] is None:
            currentLHAND = localAvatar.style.getJewelryZone7()
        else:
            currentLHAND = self.equipRequests[JewelryGlobals.LHAND][1:]
        if self.equipRequests[JewelryGlobals.RHAND] is None:
            currentRHAND = localAvatar.style.getJewelryZone8()
        else:
            currentRHAND = self.equipRequests[JewelryGlobals.RHAND][1:]
        jewelry = []
        if self.mode == 0:
            if not self.currentWardrobe:
                return
            startRange = 0
            if GENDER == 'MALE':
                if jewelryType == JewelryGlobals.RBROW:
                    startRange = JewelryGlobals.MALE_RBROW
                elif jewelryType == JewelryGlobals.LBROW:
                    startRange = JewelryGlobals.MALE_LBROW
                elif jewelryType == JewelryGlobals.LEAR:
                    startRange = JewelryGlobals.MALE_LEAR
                elif jewelryType == JewelryGlobals.REAR:
                    startRange = JewelryGlobals.MALE_REAR
                elif jewelryType == JewelryGlobals.NOSE:
                    startRange = JewelryGlobals.MALE_NOSE
                elif jewelryType == JewelryGlobals.MOUTH:
                    startRange = JewelryGlobals.MALE_MOUTH
                elif jewelryType == JewelryGlobals.LHAND:
                    startRange = JewelryGlobals.MALE_LHAND
                elif jewelryType == JewelryGlobals.RHAND:
                    startRange = JewelryGlobals.MALE_RHAND
            else:
                if GENDER == 'FEMALE':
                    if jewelryType == JewelryGlobals.RBROW:
                        startRange = JewelryGlobals.FEMALE_RBROW
                    elif jewelryType == JewelryGlobals.LBROW:
                        startRange = JewelryGlobals.FEMALE_LBROW
                    elif jewelryType == JewelryGlobals.LEAR:
                        startRange = JewelryGlobals.FEMALE_LEAR
                    elif jewelryType == JewelryGlobals.REAR:
                        startRange = JewelryGlobals.FEMALE_REAR
                    elif jewelryType == JewelryGlobals.NOSE:
                        startRange = JewelryGlobals.FEMALE_NOSE
                    elif jewelryType == JewelryGlobals.MOUTH:
                        startRange = JewelryGlobals.FEMALE_MOUTH
                    elif jewelryType == JewelryGlobals.LHAND:
                        startRange = JewelryGlobals.FEMALE_LHAND
                    elif jewelryType == JewelryGlobals.RHAND:
                        startRange = JewelryGlobals.FEMALE_RHAND
            store = self.shopId
            set = JewelryGlobals.stores.get(store)
            if set is None:
                return
            for index in range(startRange, startRange + 9999):
                if index in set:
                    item = JewelryGlobals.jewelry_id.get(index)
                    if item:
                        cost = item[3]
                        holiday = item[6]
                        modelId = item[0]
                        primary = item[4]
                        secondary = item[5]
                        if holiday is not None:
                            if holiday in JewelryStoreGUI.holidayIdList:
                                jewelry.append([index, False, cost, modelId, primary, secondary, holiday])
                        else:
                            jewelry.append([index, False, cost, modelId, primary, secondary, holiday])

        if self.mode == 1:
            if self.currentWardrobe:
                for id in self.currentWardrobe:
                    item = JewelryGlobals.jewelry_id.get(id)
                    if item and item[1] == jewelryType:
                        cost = item[3]
                        equipped = False
                        combo = item[0]
                        type = item[1]
                        modelId = item[0]
                        primaryColor = item[4]
                        secondaryColor = item[5]
                        holiday = item[6]
                        if type == JewelryGlobals.RBROW:
                            if currentRBROW == [combo, primaryColor, secondaryColor]:
                                equipped = True
                        else:
                            if type == JewelryGlobals.LBROW:
                                if currentLBROW == [combo, primaryColor, secondaryColor]:
                                    equipped = True
                            else:
                                if type == JewelryGlobals.LEAR:
                                    if currentLEAR == [combo, primaryColor, secondaryColor]:
                                        equipped = True
                                else:
                                    if type == JewelryGlobals.REAR:
                                        if currentREAR == [combo, primaryColor, secondaryColor]:
                                            equipped = True
                                    else:
                                        if type == JewelryGlobals.NOSE:
                                            if currentNOSE == [combo, primaryColor, secondaryColor]:
                                                equipped = True
                                        else:
                                            if type == JewelryGlobals.MOUTH:
                                                if currentMOUTH == [combo, primaryColor, secondaryColor]:
                                                    equipped = True
                                            else:
                                                if type == JewelryGlobals.LHAND:
                                                    if currentLHAND == [combo, primaryColor, secondaryColor]:
                                                        equipped = True
                                                else:
                                                    if type == JewelryGlobals.RHAND:
                                                        if currentRHAND == [combo, primaryColor, secondaryColor]:
                                                            equipped = True
                        jewelry.append([id, equipped, cost, modelId, primaryColor, secondaryColor, holiday])

            else:
                return
        jewelry.sort(self.sortItems)
        jewelryAmount = 0
        startPos = Vec3(0.35, 0.0, 1.05)
        buttonScale = Vec3(0.6, 0.6, 0.6)
        for item in self.buttons:
            item.destroy()

        self.buttons = []
        self.jewelryAmount = 0
        self.buttonIndex = startIndex
        if self.mode == 0:
            self.storeButton['state'] = DGG.DISABLED
            self.wardrobeButton['state'] = DGG.NORMAL
            buttonColorA = Vec4(0.7, 0.95, 0.7, 1.0)
            buttonColorB = Vec4(0.4, 0.65, 0.4, 1.0)
            self.purchaseInventory.setItemColor(Vec4(0.3, 0.95, 0.3, 1.0))
        else:
            if self.mode == 1:
                self.storeButton['state'] = DGG.NORMAL
                self.wardrobeButton['state'] = DGG.DISABLED
                buttonColorA = Vec4(0.95, 0.7, 0.7, 1.0)
                buttonColorB = Vec4(0.65, 0.4, 0.4, 1.0)
                self.sellInventory.setItemColor(Vec4(0.95, 0.3, 0.3, 1.0))
        self.reloadPirateDNA(self.pirate)
        regionData = []
        for jewel in jewelry:
            if self.jewelryAmount - startIndex < self.buttonsPerPage and self.jewelryAmount >= startIndex:
                uid = jewel[0]
                item = JewelryGlobals.jewelry_id.get(uid)
                type = item[1]
                combo = item[0]
                desc = item[2]
                cost = item[3]
                primaryColor = item[4]
                secondaryColor = item[5]
                owned = False
                equipped = jewel[1]
                questDrop = False
                if uid in JewelryGlobals.quest_items:
                    questDrop = True
                if self.mode == 1:
                    cost = int(cost * 0.25)
                for item in self.currentWardrobe:
                    if uid == item:
                        owned = True

                if self.mode == 1:
                    buttonState = DGG.DISABLED
                else:
                    buttonState = DGG.NORMAL
                helpText = desc
                jewelryButton = GuiButton.GuiButton(command=self.setJewelry, parent=self.panel, state=buttonState, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(-0.02, -0.05), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, pos=startPos, image_scale=buttonScale, image_color=buttonColorA, helpText=helpText, helpDelay=0, helpPos=(0.0, 0.0, -0.11), helpLeftAlign=True, extraArgs=[self.pirate, type, uid])
                jewelryButton.helpWatcher.setPos(jewelryButton.getPos())
                jewelryButton.itemText = DirectFrame(parent=jewelryButton, relief=None, text='', text_fg=PiratesGuiGlobals.TextFG1, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleSmall, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=True, pos=(-0.13, 0, -0.085))
                if self.mode == 0 and not owned:
                    jewelryButton.itemText['text'] = PLocalizer.TailorPreview
                else:
                    if self.mode == 1 and equipped:
                        jewelryButton.itemText['text'] = PLocalizer.TattooShopOwned
                    else:
                        if questDrop is True and self.mode == 1 and not equipped:
                            jewelryButton.itemText['text'] = PLocalizer.ShopQuestItem
                        else:
                            jewelryButton.itemText['text'] = ''
                jewelryButton.addToCart = GuiButton.GuiButton(command=self.addToCart, parent=jewelryButton, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, image_color=buttonColorB, pos=(0.16,
                                                                                                                                                                                                                                                                                                                         0.0,
                                                                                                                                                                                                                                                                                                                         0.055))
                jewelryButton.addToCart['extraArgs'] = [
                 jewelryButton, type, uid]
                jewelryButton.bind(DGG.ENTER, self.highlightJewelryStart, extraArgs=[self.jewelryAmount])
                jewelryButton.bind(DGG.EXIT, self.highlightJewelryStop, extraArgs=[self.jewelryAmount])
                if self.mode == 0 and not owned:
                    jewelryButton.cost = DirectFrame(parent=jewelryButton, relief=None, text=str(cost), text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(-0.055, 0.0), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, image=self.CoinImage, image_scale=0.15, image_pos=(-0.025,
                                                                                                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                                                                                                          0.015), pos=(0.25, 0, -0.05))
                else:
                    if self.mode == 1:
                        if not equipped:
                            jewelryButton.equip = GuiButton.GuiButton(parent=jewelryButton, command=self.equipJewelry, text=PLocalizer.TailorEquip, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, image_color=buttonColorB, pos=(0.16, 0.0, -0.05))
                            jewelryButton.equip['extraArgs'] = [
                             [
                              jewelryButton, type, uid]]
                        else:
                            jewelryButton.equip = GuiButton.GuiButton(parent=jewelryButton, command=self.equipJewelry, text=PLocalizer.TailorTakeOff, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, image_color=buttonColorB, pos=(0.16, 0.0, -0.05))
                            jewelryButton.equip['extraArgs'] = [
                             [
                              jewelryButton, type, -1]]
                if self.paid == OTPGlobals.AccessVelvetRope:
                    if self.mode == 1:
                        jewelryButton.equip['geom'] = self.LockIcon
                        jewelryButton.equip['geom_scale'] = 0.2
                        jewelryButton.equip['geom_pos'] = Vec3(-0.1, 0.0, 0.0)
                        jewelryButton.equip['command'] = localAvatar.guiMgr.showNonPayer
                        jewelryButton.equip['extraArgs'] = ['JEWELRY_CANNOT_EQUIP', 10]
                    jewelryButton.addToCart['geom'] = self.LockIcon
                    jewelryButton.addToCart['geom_scale'] = 0.2
                    jewelryButton.addToCart['geom_pos'] = Vec3(-0.1, 0.0, 0.0)
                    jewelryButton.addToCart['command'] = localAvatar.guiMgr.showNonPayer
                    jewelryButton.addToCart['extraArgs'] = ['JEWELRY_CANNOT_BUY-SELL', 10]
                data = [
                 type, uid]
                if self.mode == 0 and owned:
                    jewelryButton.addToCart.buyState = 0
                    jewelryButton.addToCart['state'] = DGG.DISABLED
                    jewelryButton['state'] = DGG.DISABLED
                    jewelryButton.addToCart['text'] = PLocalizer.TailorPurchased
                else:
                    if self.mode == 0 and self.purchaseInventory.hasPanel(data):
                        jewelryButton.addToCart.buyState = 0
                        jewelryButton.addToCart['state'] = DGG.NORMAL
                        jewelryButton.addToCart['text'] = PLocalizer.TailorRemove
                    else:
                        if self.mode == 1 and self.sellInventory.hasPanel(data):
                            jewelryButton.addToCart.buyState = 0
                            jewelryButton.addToCart['state'] = DGG.NORMAL
                            jewelryButton.addToCart['text'] = PLocalizer.TailorRemove
                            jewelryButton.equip['state'] = DGG.DISABLED
                        else:
                            jewelryButton.addToCart.buyState = 1
                            jewelryButton.addToCart['state'] = DGG.NORMAL
                            if self.mode == 0:
                                jewelryButton.addToCart['text'] = PLocalizer.TailorAddToCart
                            else:
                                if self.mode == 1:
                                    jewelryButton.equip['state'] = DGG.NORMAL
                                    jewelryButton.addToCart['text'] = PLocalizer.TailorSell
                startPos -= Vec3(0.0, 0.0, jewelryButton.getHeight() - 0.02)
                jewelryButton.jewelryType = jewelryType
                jewelryButton.jewelryCombo = combo
                jewelryButton.jewelryUID = uid
                jewelryButton.equipped = equipped
                jewelryButton.questDrop = questDrop
                regionData.append([jewelryType, uid])
                self.buttons.append(jewelryButton)
            self.jewelryAmount += 1

        if not len(jewelry):
            jewelryButton = GuiButton.GuiButton(parent=self.panel, state=DGG.DISABLED, text=PLocalizer.TailorEmptyWardrobe, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0,
                                                                                                                                                                         0.0), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, pos=startPos, image_scale=buttonScale, image_color=buttonColorA)
            jewelryButton.jewelryType = -1
            jewelryButton.jewelryCombo = -1
            jewelryButton.jewelryUID = -1
            self.buttons.append(jewelryButton)
        if len(jewelry):
            self.setupDisplayRegions(regionData, pageName)
        else:
            for item in self.clothRenders:
                item.hide()

            if self.jewelryAmount <= self.buttonsPerPage:
                self.nextPageButton['state'] = DGG.DISABLED
                self.prevPageButton['state'] = DGG.DISABLED
            if startIndex:
                self.prevPageButton['state'] = DGG.NORMAL
            if startIndex + self.buttonsPerPage < self.jewelryAmount:
                self.nextPageButton['state'] = DGG.NORMAL
                self.prevPageButton['state'] = DGG.NORMAL
            if self.jewelryAmount > self.buttonsPerPage:
                numPages = float(self.jewelryAmount) / float(self.buttonsPerPage)
                remainder = numPages - int(numPages)
                if remainder > 0:
                    numPages += 1.0 - remainder
                page = startIndex / self.buttonsPerPage + 1
            numPages = 1
            page = 1
        self.pageNumber['text'] = '%s %s / %s' % (PLocalizer.TailorPage, page, int(numPages))
        return

    def _stopMouseReadTask(self):
        taskMgr.remove('JewelryStore-MouseRead')

    def _startMouseReadTask(self):
        self._stopMouseReadTask()
        mouseData = base.win.getPointer(0)
        self.lastMousePos = (mouseData.getX(), mouseData.getY())
        taskMgr.add(self._mouseReadTask, 'JewelryStore-MouseRead')

    def _mouseReadTask(self, task):
        if not base.mouseWatcherNode.hasMouse():
            pass
        else:
            winSize = (
             base.win.getXSize(), base.win.getYSize())
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

    def highlightJewelryStart(self, item, event=None):
        pass

    def highlightJewelryStop(self, item, event=None):
        pass

    def cleanupRegions(self):
        for item in self.clothWindows:
            base.win.removeDisplayRegion(item)
            item = None

        self.clothWindows = []
        for item in self.clothCameras:
            del item

        self.clothCameras = []
        for item in self.clothRenders:
            item.remove()
            item.removeNode()

        self.clothRenders = []
        for item in self.clothHumans:
            item.delete()
            item.remove()
            item.removeNode()

        self.clothHumans = []
        for item in self.clothCameraNPs:
            item.remove()
            item.removeNode()

        self.clothCameraNPs = []
        return

    def createDisplayRegions(self):
        startRegion = Vec4(0.526, 0.596, 0.62, 0.69)
        for x in range(self.buttonsPerPage):
            clothWindow = base.win.makeDisplayRegion(startRegion[0], startRegion[1], startRegion[2], startRegion[3])
            clothWindow.setSort(10)
            clothCamera = Camera('clothCamera' + str(x))
            clothRender = NodePath('clothRender' + str(x))
            clothHuman = DynamicHuman.DynamicHuman()
            clothHuman.setDNAString(localAvatar.style)
            clothHuman.generateHuman(localAvatar.style.gender)
            clothCameraNP = NodePath(clothCamera)
            clothCameraNP.reparentTo(clothRender)
            clothHuman.reparentTo(clothRender)
            clothWindow.setCamera(clothCameraNP)
            clothHuman.pose('idle', 1)
            clothHuman.dropShadow.hide()
            clothCamera.getLens().setAspectRatio(base.camLens.getAspectRatio())
            clothCamera.getLens().setNear(0.1)
            self.clothCameras.append(clothCamera)
            self.clothHumans.append(clothHuman)
            self.clothWindows.append(clothWindow)
            self.clothCameraNPs.append(clothCameraNP)
            self.clothRenders.append(clothRender)
            startRegion -= Vec4(0.0, 0.0, 0.12, 0.12)
            self.displayRegionStates[x] = True

    def setupDisplayRegions(self, regionData, pageName):
        bodyShape = localAvatar.style.getBodyShape()
        if bodyShape == 0:
            bodyOffset = 0.5
        else:
            if bodyShape == 1:
                bodyOffset = 0.5
            else:
                if bodyShape == 2:
                    bodyOffset = 0.5
                else:
                    if bodyShape == 3:
                        bodyOffset = 0.5
                    else:
                        if bodyShape == 4:
                            bodyOffset = 0.5
        x = 0
        m = Mat4(Mat4.identMat())
        rightEyeHeight = None
        leftEarHeight = None
        noseHeight = None
        mouthHeight = None
        leftIndexHeight = None
        rightIndexHeight = None
        gender = localAvatar.style.getGender()
        source = localAvatar
        source.pose('idle', 1)
        source.update()
        for x in range(len(regionData)):
            if pageName == JewelryGlobals.RBROW:
                if rightEyeHeight is None:
                    source.getLOD('2000').getChild(0).node().findJoint('trs_right_eyebrow').getNetTransform(m)
                    rightEyeHeight = TransformState.makeMat(m).getPos().getZ()
                if gender == 'f':
                    offsetX = -0.3
                    offsetZ = -rightEyeHeight
                    offsetY = 0.4 + bodyOffset
                else:
                    offsetX = -0.2
                    offsetZ = -rightEyeHeight * 0.99
                    offsetY = 0.3 + bodyOffset
                offsetH = 230
            else:
                if pageName == JewelryGlobals.LBROW:
                    if rightEyeHeight is None:
                        source.getLOD('2000').getChild(0).node().findJoint('trs_right_eyebrow').getNetTransform(m)
                        rightEyeHeight = TransformState.makeMat(m).getPos().getZ()
                    if gender == 'f':
                        offsetX = 0.4
                        offsetZ = -rightEyeHeight
                        offsetY = 0.25 + bodyOffset
                    else:
                        offsetX = 0.3
                        offsetZ = -rightEyeHeight * 0.99
                        offsetY = 0.15 + bodyOffset
                    offsetH = -240
                else:
                    if pageName == JewelryGlobals.REAR:
                        if leftEarHeight is None:
                            source.getLOD('2000').getChild(0).node().findJoint('def_trs_left_ear').getNetTransform(m)
                            leftEarHeight = TransformState.makeMat(m).getPos().getZ()
                        if gender == 'f':
                            offsetZ = -leftEarHeight
                            offsetY = 0.6 + bodyOffset
                            offsetX = -0.15
                        else:
                            offsetZ = -leftEarHeight * 0.99
                            offsetY = 0.5 + bodyOffset
                            offsetX = -0.04
                        offsetH = 250
                    else:
                        if pageName == JewelryGlobals.LEAR:
                            if leftEarHeight is None:
                                source.getLOD('2000').getChild(0).node().findJoint('def_trs_left_ear').getNetTransform(m)
                                leftEarHeight = TransformState.makeMat(m).getPos().getZ()
                            if gender == 'f':
                                offsetZ = -leftEarHeight
                                offsetY = 0.4 + bodyOffset
                                offsetX = 0.15
                            else:
                                offsetZ = -leftEarHeight * 0.99
                                offsetY = 0.3 + bodyOffset
                                offsetX = 0.04
                            offsetH = -250
                        else:
                            if pageName == JewelryGlobals.NOSE:
                                if noseHeight is None:
                                    source.getLOD('2000').getChild(0).node().findJoint('def_trs_mid_nose_bot').getNetTransform(m)
                                    noseHeight = TransformState.makeMat(m).getPos().getZ()
                                if gender == 'f':
                                    offsetZ = -noseHeight - 0.01
                                    offsetY = 0.45 + bodyOffset
                                else:
                                    offsetZ = -noseHeight
                                    offsetY = 0.4 + bodyOffset
                                offsetX = 0.06
                                offsetH = 180
                            else:
                                if pageName == JewelryGlobals.MOUTH:
                                    if mouthHeight is None:
                                        source.getLOD('2000').getChild(0).node().findJoint('trs_lips_top').getNetTransform(m)
                                        mouthHeight = TransformState.makeMat(m).getPos().getZ()
                                    offsetZ = -mouthHeight + 0.02
                                    offsetY = 0.6 + bodyOffset
                                    offsetX = 0.08
                                    offsetH = 180
                                else:
                                    if pageName == JewelryGlobals.LHAND:
                                        if leftIndexHeight is None:
                                            source.getLOD('2000').getChild(0).node().findJoint('def_left_index01').getNetTransform(m)
                                            leftIndexHeight = TransformState.makeMat(m).getPos().getZ()
                                        if gender == 'f':
                                            offsetZ = -leftIndexHeight + 0.05
                                            offsetX = -0.7
                                            offsetY = 1.25 + bodyOffset
                                        else:
                                            offsetZ = -leftIndexHeight
                                            if bodyShape == 4:
                                                offsetX = -1.0
                                                offsetY = 1.75 + bodyOffset
                                            else:
                                                if bodyShape == 3:
                                                    offsetX = -0.7
                                                    offsetY = 1.25 + bodyOffset
                                                else:
                                                    if bodyShape == 1:
                                                        offsetX = -0.7
                                                        offsetY = 1.25 + bodyOffset
                                                    else:
                                                        if bodyShape == 0:
                                                            offsetX = -0.7
                                                            offsetY = 1.25 + bodyOffset
                                                        else:
                                                            offsetX = -0.8
                                                            offsetY = 1.25 + bodyOffset
                                        offsetH = 160
                                    else:
                                        if pageName == JewelryGlobals.RHAND:
                                            if rightIndexHeight is None:
                                                source.getLOD('2000').getChild(0).node().findJoint('def_right_index01').getNetTransform(m)
                                                rightIndexHeight = TransformState.makeMat(m).getPos().getZ()
                                            if gender == 'f':
                                                offsetZ = -rightIndexHeight + 0.05
                                                offsetX = 0.8
                                                offsetY = 1.25 + bodyOffset
                                            else:
                                                offsetZ = -rightIndexHeight
                                                if bodyShape == 4:
                                                    offsetX = 1.0
                                                    offsetY = 1.75 + bodyOffset
                                                else:
                                                    if bodyShape == 3:
                                                        offsetX = 0.7
                                                        offsetY = 1.25 + bodyOffset
                                                    else:
                                                        if bodyShape == 1:
                                                            offsetX = 0.7
                                                            offsetY = 1.25 + bodyOffset
                                                        else:
                                                            if bodyShape == 0:
                                                                offsetX = 0.7
                                                                offsetY = 1.25 + bodyOffset
                                                            else:
                                                                offsetX = 0.8
                                                                offsetY = 1.25 + bodyOffset
                                            offsetH = 210
                                        else:
                                            offsetZ = 0.0
                                            offsetY = 0.0
                                            offsetX = 0.0
                                            offsetH = 0
            self.clothHumans[x].setX(offsetX)
            self.clothHumans[x].setY(offsetY)
            self.clothHumans[x].setZ(offsetZ)
            self.clothHumans[x].setH(offsetH)
            self.reloadPirateDNA(self.clothHumans[x])
            type = regionData[x][0]
            uid = regionData[x][1]
            jewel = JewelryGlobals.jewelry_id.get(uid)
            combo = jewel[0]
            self.setJewelry(self.clothHumans[x], type, uid)
            self.clothHumans[x].style.setClothesHat(0, 0)
            self.clothHumans[x].model.handleHeadHiding()
            self.clothRenders[x].show()

        x = len(regionData)
        if x < self.buttonsPerPage:
            for y in range(self.buttonsPerPage - x):
                self.clothRenders[self.buttonsPerPage - 1 - y].hide()

        self.aspectRatioChange()
        return

    def showWardrobeLimitAlert(self, type):
        self.removeAlertDialog()
        limit = str(PiratesGlobals.WARDROBE_LIMIT_JEWELER)
        text = PLocalizer.ShopLimitJewelry % limit
        self.alertDialog = PDialog.PDialog(text=text, text_align=TextNode.ACenter, style=OTPDialog.Acknowledge, pos=(-0.65, 0.0, 0.0), command=self.removeAlertDialog)
        self.alertDialog.setBin('gui-fixed', 20, 20)

    def removeAlertDialog(self, value=None):
        if self.alertDialog:
            self.alertDialog.destroy()
            self.alertDialog = None
        return
# okay decompiling .\pirates\economy\JewelryStoreGUI.pyc
