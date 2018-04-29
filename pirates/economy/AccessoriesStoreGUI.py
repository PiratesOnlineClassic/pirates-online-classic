import random

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from pandac.PandaModules import *
from pirates.makeapirate import ClothingGlobals
from pirates.pirate import DynamicHuman, HumanDNA
from pirates.piratesbase import Freebooter, PiratesGlobals, PLocalizer
from pirates.piratesgui import (DialogButton, GuiButton, GuiPanel, PDialog,
                                PiratesGuiGlobals)
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui.TabBar import LeftTab, TabBar
from pirates.uberdog.UberDogGlobals import InventoryType

BODY_CAMERA = 0

class AccessoriesStoreTab(LeftTab):

    def __init__(self, tabBar, name, **kw):
        optiondefs = (('suffix', '_d', None), ('borderScale', 0.38, None), ('bgBuffer', 0.15, None))
        self.defineoptions(kw, optiondefs)
        LeftTab.__init__(self, tabBar, name, **kw)
        self.initialiseoptions(AccessoriesStoreTab)
        return


class AccessoriesStoreTabBar(TabBar):

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
        return AccessoriesStoreTab(self, name, **kw)


class AccessoriesStoreCartList(DirectScrolledFrame):

    def __init__(self, parent, width, height, itemWidth, itemHeight):
        self.width = width + PiratesGuiGlobals.ScrollbarSize
        self.listItemHeight = itemHeight
        self.listItemWidth = itemWidth
        self.height = height
        self._parent = parent
        charGui = loader.loadModelOnce('models/gui/char_gui')
        DirectScrolledFrame.__init__(self, relief=None, state=DGG.NORMAL, manageScrollBars=0, autoHideScrollBars=1, frameSize=(0, self.width, 0, self.height), canvasSize=(0, self.width - 0.05, 0.025, self.height - 0.025), verticalScroll_relief=None, verticalScroll_image=charGui.find('**/chargui_slider_small'), verticalScroll_frameSize=(0, PiratesGuiGlobals.ScrollbarSize, 0, self.height), verticalScroll_image_scale=(self.height + 0.05, 1, 0.75), verticalScroll_image_hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           90), verticalScroll_image_pos=(self.width - PiratesGuiGlobals.ScrollbarSize * 0.5 - 0.004, 0, self.height * 0.5), verticalScroll_image_color=(0.61,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         0.6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         0.6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         1), verticalScroll_thumb_image=(charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over')), verticalScroll_thumb_relief=None, verticalScroll_thumb_image_scale=0.25, verticalScroll_resizeThumb=0, horizontalScroll_relief=None, sortOrder=5)
        self.initialiseoptions(AccessoriesStoreCartList)
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

        self['canvasSize'] = (
         0, self.listItemWidth - 0.09, -z * (i + 1), 0)

    def addPanel(self, data, repack=1):
        itemType = data[0]
        itemId = data[1]
        itemTex = data[2]
        itemColor = data[3]
        itemCost = data[4]
        itemUID = data[5]
        maxLength = 23 - len(str(itemCost))
        item = ClothingGlobals.UNIQUE_ID.get(itemUID)
        if item is None:
            return
        isDisabled = 0
        categoryId = ClothingGlobals.CLOTHING_NUMBER[itemType]
        text = self._parent.categoryText[categoryId][0]
        colorText = PLocalizer.TailorColorStrings.get(itemColor)
        if itemUID in ClothingGlobals.quest_items:
            text = item[7]
        else:
            if colorText is not None:
                text = colorText + ' ' + text
        if itemCost == 0:
            strCost = PLocalizer.ShopFree
        else:
            strCost = str(itemCost)
        panel = DirectButton(parent=self, relief=None, text=text[:maxLength], text_fg=self.itemColor, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleMed, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.06,
                                                                                                                                                                                                                                0.0), command=self.removePanel, extraArgs=[data])
        panel.costLabel = DirectLabel(parent=panel, relief=None, text=strCost, text_fg=self.itemColor, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleMed, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.45,
                                                                                                                                                                                                                                  0.0), image=self._parent.CoinImage, image_scale=0.15, image_pos=(0.48,
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
                self._parent.updateButton(data, 1)
                self.panels.remove(panel)
                self.purchases.remove(data)
                panel.destroy()
                if repack:
                    self.repackPanels()
                self._parent.updateBalance()
                return

    def hasPanel(self, data):
        for panel in self.panels:
            if panel.data[0] == data[0] and panel.data[1] == data[1] and panel.data[2] == data[2] and panel.data[3] == data[3]:
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


class AccessoriesStoreGUI(DirectFrame):
    notify = directNotify.newCategory('AccessoriesStoreGUI')
    width = (PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.06) * 2
    height = 1.5
    columnWidth = PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.05
    holidayIdList = []

    def __init__(self, npc, shopId, **kw):
        optiondefs = (
         ('relief', None, None), ('frameSize', (0, self.width, 0, self.height), None), ('sortOrder', 20, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, None, **kw)
        self.initialiseoptions(AccessoriesStoreGUI)
        self.pirate = None
        self.camIval = None
        self.buttons = []
        self.buttonIndex = 0
        self.clothingAmount = 0
        self.currentPage = None
        self.buttonsPerPage = 4
        self.displayRegionStates = {}
        self.prevIdx = 0
        self.mode = 0
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.CoinImage = gui.find('**/treasure_w_coin*')
        self.ParchmentIcon = gui.find('**/main_gui_quest_scroll')
        self.TailorIcons = loader.loadModelCopy('models/textureCards/tailorIcons')
        self.ShirtIcon = loader.loadModelOnce('models/gui/char_gui').find('**/chargui_cloth')
        self.LockIcon = gui.find('**/subscribers_lock')
        self.backTabParent = self.attachNewNode('backTabs', sort=0)
        self.panel = GuiPanel.GuiPanel(None, self.width, self.height, parent=self, showClose=False)
        self.setPos(0.0, 0, -0.75)
        self.balance = 0
        self.npc = npc
        self.rootTitle = PLocalizer.TailorStore
        self.shopId = shopId
        if Freebooter.AllAccessHoliday:
            self.paid = Freebooter.FULL
        else:
            self.paid = base.cr.isPaid()
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
        self.purchaseInventory = AccessoriesStoreCartList(self, self.cartWidth, self.cartHeight - 0.95, self.cartWidth, self.cartHeight / 20.0)
        self.purchaseInventory.reparentTo(self.cartFrame)
        self.purchaseInventory.setPos(0.0, 0.0, 0.76)
        self.sellInventory = AccessoriesStoreCartList(self, self.cartWidth, self.cartHeight - 0.95, self.cartWidth, self.cartHeight / 20.0)
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
        self.nextPageButton = DirectButton(parent=self.panel, relief=None, state=DGG.DISABLED, image=triangle, image_scale=0.065, pos=(0.53,
                                                                                                                                       0.0,
                                                                                                                                       0.175), rolloverSound=None, command=self.nextPage)
        self.prevPageButton = DirectButton(parent=self.panel, relief=None, state=DGG.DISABLED, image=triangle, image_scale=-0.065, pos=(0.17,
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
        self.alertDialog = None
        self.accept('mouse1', self._startMouseReadTask)
        self.accept('mouse1-up', self._stopMouseReadTask)
        self.clothWindows = []
        self.clothRenders = []
        self.clothHumans = []
        self.clothCameraNPs = []
        self.clothCameras = []
        self.createDisplayRegions()
        localAvatar.guiMgr.chatPanel.show()
        localAvatar.guiMgr.chatPanel.startFadeTextIval()
        self.accept('aspectRatioChanged', self.aspectRatioChange)
        self.accept('NonPayerPanelShown', self.hideDisplayRegions)
        self.accept('NonPayerPanelHidden', self.showDisplayRegions)
        self.accept('GameOptionsShown', self.hideDisplayRegions)
        self.accept('GameOptionsHidden', self.showDisplayRegions)
        self.accept('GUIShown', self.hideDisplayRegions)
        self.accept('GUIHidden', self.showDisplayRegions)
        self.accept(localAvatar.uniqueName('accessoriesUpdate'), self.reloadPirateDNA)
        self.model = loader.loadModel('models/gui/gui_shop_tailor')
        self.model.reparentTo(self.panel)
        self.model.setBin('gui-fixed', 0)
        self.model.setPos(0.625, 0.0, 1.05)
        self.model.setScale(0.337, 0.0, 0.327)
        self.equipRequests = {ClothingGlobals.HAT: None, ClothingGlobals.SHIRT: None, ClothingGlobals.VEST: None, ClothingGlobals.COAT: None, ClothingGlobals.PANT: None, ClothingGlobals.BELT: None, ClothingGlobals.SHOE: None}
        self.createPirate()
        self.initTabs()
        self.updateBalance()
        self.lastRun = 0
        self.showQuestLabel = False
        if localAvatar.guiMgr.questPage:
            if not localAvatar.guiMgr.questPage.trackedQuestLabel.isHidden():
                localAvatar.guiMgr.questPage.trackedQuestLabel.hide()
                self.showQuestLabel = True
        if config.GetBool('tailor-debug', 0):
            print '######## STORE ID = %s' % self.shopId

            def debugColor(id):
                topColors = localAvatar.style.getClothesTopColor()
                botColors = localAvatar.style.getClothesBotColor()
                hatColor = localAvatar.style.getHatColor()
                if self.currentPage == ClothingGlobals.SHIRT:
                    topColors[0] = id
                elif self.currentPage == ClothingGlobals.VEST:
                    topColors[1] = id
                elif self.currentPage == ClothingGlobals.PANT:
                    botColors[0] = id
                elif self.currentPage == ClothingGlobals.COAT:
                    topColors[2] = id
                elif self.currentPage == ClothingGlobals.SHOE:
                    botColors[2] = id
                elif self.currentPage == ClothingGlobals.HAT:
                    hatColor = id
                elif self.currentPage == ClothingGlobals.BELT:
                    botColors[1] = id
                self.pirate.style.setClothesTopColor(topColors[0], topColors[1], topColors[2])
                self.pirate.style.setClothesBotColor(botColors[0], botColors[1], botColors[2])
                self.pirate.style.setHatColor(hatColor)
                self.pirate.model.handleClothesHiding()
                self.pirate.model.handleHeadHiding()

            self.colorButtons = []
            offsetx = -1.0
            offsety = 0.1
            numcolors = len(HumanDNA.clothesTopColors[0])
            for i in range(0, numcolors):
                colorButton = DirectButton(text=str(i), parent=self, pos=(offsetx, 0.0, offsety), command=debugColor, extraArgs=[i])
                colorButton.setColor(HumanDNA.clothesTopColors[0][i])
                colorButton.setScale(0.05)
                offsetx += 0.075
                if i != 0 and i % 10 == 0:
                    offsetx = -1.0
                    offsety -= 0.075
                self.colorButtons.append(colorButton)

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
        if self.TailorIcons:
            self.TailorIcons.removeNode()
            self.TailorIcons = None
        if self.ShirtIcon:
            self.ShirtIcon.removeNode()
            self.ShirtIcon = None
        if self.LockIcon:
            self.LockIcon.removeNode()
            self.LockIcon = None
        if self.alertDialog:
            self.alertDialog.destroy()
        if localAvatar.guiMgr.questPage and len(localAvatar.guiMgr.questPage.trackedQuestLabel['text']):
            if self.showQuestLabel:
                localAvatar.guiMgr.questPage.trackedQuestLabel.show()
        localAvatar.guiMgr.chatPanel.hide()
        return

    def focusCamera(self, cameraId=BODY_CAMERA):
        if localAvatar.gameFSM.camIval is not None:
            if localAvatar.gameFSM.camIval.isPlaying():
                localAvatar.gameFSM.camIval.finish()
        if self.camIval:
            self.camIval.finish()
            self.camIval = None
        self.pirate.setH(self.initialPirateH)
        self.rotateSlider['value'] = self.rotateSliderOrigin = 0.5
        dummy = self.pirate.attachNewNode('dummy')
        if cameraId == BODY_CAMERA:
            dummy.setPos(dummy, 0, 10, self.pirate.headNode.getZ(self.pirate))
        else:
            dummy.setPos(dummy, 0, 0, 0)
        dummy.wrtReparentTo(render)
        if cameraId == BODY_CAMERA:
            dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 0.9)
        else:
            return
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

    def createPirate(self):
        self.pirate = DynamicHuman.DynamicHuman()
        self.pirate.isPaid = localAvatar.isPaid
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
        self.pirate.show()
        localAvatar.stash()
        self.focusCamera(BODY_CAMERA)

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
            if equip is not None:
                uid = equip[0]
                item = ClothingGlobals.UNIQUE_ID.get(uid)
                typeString = ClothingGlobals.CLOTHING_STRING[type]
                if item is not None:
                    modelId = item[1]
                    texId = item[2]
                    clothColorId = equip[1]
                    equips.append([uid, clothColorId, type])
                    localAvatar.style.setClothesByType(typeString, modelId, texId, clothColorId)
                else:
                    equips.append([0, 0, type])
                    localAvatar.style.setClothesByType(typeString, 0, 0, 0)

        if len(equips) > 0:
            self.npc.sendRequestAccessoryEquip(equips)
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
            type = ClothingGlobals.CLOTHING_NUMBER[item[0]]
            uid = item[5]
            colorId = item[3]
            modelId = item[1]
            texId = item[2]
            purchaseArgList.append([item[5], item[3], type])
            self.equipRequests[type] = [
             uid, colorId, modelId, texId]

        for item in self.sellInventory.purchases:
            type = ClothingGlobals.CLOTHING_NUMBER[item[0]]
            uid = item[5]
            colorId = item[3]
            modelId = item[1]
            texId = item[2]
            sellArgList.append([item[5], item[3], type])
            if self.equipRequests[type] == [uid, colorId, modelId, texId]:
                self.equipRequests[type] = None

        self.purchaseInventory.removeAllPanels()
        self.sellInventory.removeAllPanels()
        self.npc.sendRequestAccessories(purchaseArgList, sellArgList)
        self.changeMode(1, refresh=True)
        return

    def updateBalance(self, extraArgs=None):
        self.myGold['text'] = str(localAvatar.getMoney())
        self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG2
        self.balance = 0
        for item in self.purchaseInventory.panels:
            self.balance += max(item.price, 0)

        for item in self.sellInventory.panels:
            self.balance -= max(item.price, 0)

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
            elif self.balance < 0:
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
        self.tabBar = AccessoriesStoreTabBar(parent=self, backParent=self.backTabParent, frontParent=self.frontTabParent, offset=0)
        self.pageNames = []
        self.createTabs()
        if len(self.pageNames) > 0:
            self.setPage(self.pageNames[0])

    def createTabs(self):
        for item in ClothingGlobals.CLOTHING_NUMBER:
            id = ClothingGlobals.CLOTHING_NUMBER[item]
            if not self.isPageAdded(id):
                self.addTab(id)

    def addTab(self, id):
        newTab = self.tabBar.addTab(id, command=self.setPage, extraArgs=[id, 0, False])
        if id == ClothingGlobals.HAT:
            tabIcon = self.TailorIcons.find('**/icon_shop_tailor_hat')
            tabScale = 0.55
        else:
            if id == ClothingGlobals.BELT:
                tabIcon = self.TailorIcons.find('**/icon_shop_tailor_belt')
                tabScale = 0.55
            else:
                if id == ClothingGlobals.SHOE:
                    tabIcon = self.TailorIcons.find('**/icon_shop_tailor_booths')
                    tabScale = 0.4
                else:
                    if id == ClothingGlobals.COAT:
                        tabIcon = self.TailorIcons.find('**/icon_shop_tailor_coat')
                        tabScale = 0.4
                    else:
                        if id == ClothingGlobals.PANT:
                            tabIcon = self.TailorIcons.find('**/icon_shop_tailor_pants')
                            tabScale = 0.4
                        else:
                            if id == ClothingGlobals.VEST:
                                tabIcon = self.TailorIcons.find('**/icon_shop_tailor_vest')
                                tabScale = 0.5
                            else:
                                if id == ClothingGlobals.SHIRT:
                                    tabIcon = self.ShirtIcon
                                    tabScale = 1.2
                                else:
                                    tabIcon = None
                                    tabScale = 0.0
        newTab.nameTag = DirectLabel(parent=newTab, relief=None, state=DGG.DISABLED, pos=(0.06, 0, -0.035), image=tabIcon, image_scale=tabScale)
        self.pageNames.append(id)
        return

    def isPageAdded(self, pageName):
        return self.pageNames.count(pageName) > 0

    def nextPage(self):
        if self.clothingAmount - (self.buttonIndex + self.buttonsPerPage) > 0:
            startIndex = self.buttonIndex + self.buttonsPerPage
            self.setPage(self.currentPage, startIndex, False)
        else:
            self.setPage(self.currentPage, 0, False)

    def previousPage(self):
        if self.buttonIndex > 0:
            startIndex = self.buttonIndex - self.buttonsPerPage
            self.setPage(self.currentPage, startIndex, False)
        else:
            remainder = self.clothingAmount % self.buttonsPerPage
            if remainder:
                startIndex = self.clothingAmount - remainder
            else:
                startIndex = self.clothingAmount - self.buttonsPerPage
            self.setPage(self.currentPage, startIndex, False)

    def setClothes(self, type, modelId, texId, clothColorId):
        typeString = ClothingGlobals.CLOTHING_STRING[type]
        gender = localAvatar.style.getGender()
        self.pirate.setClothesByType(typeString, modelId, texId, clothColorId)
        self.pirate.model.handleClothesHiding()
        self.pirate.model.handleHeadHiding()
        if self.equipRequests[ClothingGlobals.VEST] is None:
            vestIdx = localAvatar.style.getClothesVest()[0]
        else:
            vestIdx = self.equipRequests[ClothingGlobals.VEST][2]
        if type == ClothingGlobals.SHIRT and gender == 'f' and vestIdx in [3, 4]:
            self.showCutOffVestAlert()
        currTime = globalClock.getFrameTime()
        if currTime - self.lastRun > 10:
            if typeString == 'SHIRT' or typeString == 'COAT':
                if random.randint(0, 1) == 0:
                    self.pirate.play('map_look_arm_left')
                else:
                    self.pirate.play('map_look_arm_right')
            if typeString == 'PANT' or typeString == 'BELT':
                self.pirate.play('map_look_pant_right')
            if typeString == 'SHOE':
                self.pirate.play('map_look_boot_left')
            self.lastRun = currTime
        return

    def addToCart(self, button, type, id, tex, colorId, cost, uid):
        data = [
         type, id, tex, colorId, cost, uid]
        if self.mode == 0:
            if button.addToCart.buyState:
                limit = PiratesGlobals.WARDROBE_LIMIT_TAILOR
                current = 0
                for id, color, equipped in self.currentWardrobe:
                    item = ClothingGlobals.UNIQUE_ID.get(id)
                    if item:
                        itemType = item[0]
                        typeId = ClothingGlobals.CLOTHING_NUMBER.get(type)
                        if itemType == typeId:
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
            if item.clothModelType == data[0] and item.clothModelId == data[1] and item.clothTextureId == data[2] and item.clothColorId == data[3]:
                if self.mode == 0:
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

    def setWardrobe(self, accessories):
        if self.currentWardrobe:
            self.currentWardrobe = []
        self.currentWardrobe = accessories
        self.setPage(self.currentPage, self.buttonIndex, refreshWardrobe=False)

    def reloadPirateDNA(self):
        if self.pirate is None:
            self.createPirate()
        if self.equipRequests[ClothingGlobals.SHIRT] is None:
            self.pirate.style.clothes.shirt = localAvatar.style.clothes.shirt
            self.pirate.style.clothes.shirtTexture = localAvatar.style.clothes.shirtTexture
            self.pirate.style.clothes.shirtColor = localAvatar.style.clothes.shirtColor
        else:
            self.pirate.style.clothes.shirt = self.equipRequests[ClothingGlobals.SHIRT][2]
            self.pirate.style.clothes.shirtTexture = self.equipRequests[ClothingGlobals.SHIRT][3]
            self.pirate.style.clothes.shirtColor = self.equipRequests[ClothingGlobals.SHIRT][1]
        if self.equipRequests[ClothingGlobals.VEST] is None:
            self.pirate.style.clothes.vest = localAvatar.style.clothes.vest
            self.pirate.style.clothes.vestTexture = localAvatar.style.clothes.vestTexture
            self.pirate.style.clothes.vestColor = localAvatar.style.clothes.vestColor
        else:
            self.pirate.style.clothes.vest = self.equipRequests[ClothingGlobals.VEST][2]
            self.pirate.style.clothes.vestTexture = self.equipRequests[ClothingGlobals.VEST][3]
            self.pirate.style.clothes.vestColor = self.equipRequests[ClothingGlobals.VEST][1]
        if self.equipRequests[ClothingGlobals.PANT] is None:
            self.pirate.style.clothes.pant = localAvatar.style.clothes.pant
            self.pirate.style.clothes.pantTexture = localAvatar.style.clothes.pantTexture
            self.pirate.style.clothes.pantColor = localAvatar.style.clothes.pantColor
        else:
            self.pirate.style.clothes.pant = self.equipRequests[ClothingGlobals.PANT][2]
            self.pirate.style.clothes.pantTexture = self.equipRequests[ClothingGlobals.PANT][3]
            self.pirate.style.clothes.pantColor = self.equipRequests[ClothingGlobals.PANT][1]
        if self.equipRequests[ClothingGlobals.COAT] is None:
            self.pirate.style.clothes.coat = localAvatar.style.clothes.coat
            self.pirate.style.clothes.coatTexture = localAvatar.style.clothes.coatTexture
            self.pirate.style.clothes.coatColor = localAvatar.style.clothes.coatColor
        else:
            self.pirate.style.clothes.coat = self.equipRequests[ClothingGlobals.COAT][2]
            self.pirate.style.clothes.coatTexture = self.equipRequests[ClothingGlobals.COAT][3]
            self.pirate.style.clothes.coatColor = self.equipRequests[ClothingGlobals.COAT][1]
        if self.equipRequests[ClothingGlobals.SHOE] is None:
            self.pirate.style.clothes.shoe = localAvatar.style.clothes.shoe
            self.pirate.style.clothes.shoeTexture = localAvatar.style.clothes.shoeTexture
            self.pirate.style.clothes.shoeColor = localAvatar.style.clothes.shoeColor
        else:
            self.pirate.style.clothes.shoe = self.equipRequests[ClothingGlobals.SHOE][2]
            self.pirate.style.clothes.shoeTexture = self.equipRequests[ClothingGlobals.SHOE][3]
            self.pirate.style.clothes.shoeColor = self.equipRequests[ClothingGlobals.SHOE][1]
        if self.equipRequests[ClothingGlobals.BELT] is None:
            self.pirate.style.clothes.belt = localAvatar.style.clothes.belt
            self.pirate.style.clothes.beltTexture = localAvatar.style.clothes.beltTexture
            self.pirate.style.clothes.sashColor = localAvatar.style.clothes.sashColor
        else:
            self.pirate.style.clothes.belt = self.equipRequests[ClothingGlobals.BELT][2]
            self.pirate.style.clothes.beltTexture = self.equipRequests[ClothingGlobals.BELT][3]
            self.pirate.style.clothes.sashColor = self.equipRequests[ClothingGlobals.BELT][1]
        if self.equipRequests[ClothingGlobals.HAT] is None:
            self.pirate.style.clothes.hat = localAvatar.style.clothes.hat
            self.pirate.style.clothes.hatTexture = localAvatar.style.clothes.hatTexture
            self.pirate.style.clothes.hatColor = localAvatar.style.clothes.hatColor
        else:
            self.pirate.style.clothes.hat = self.equipRequests[ClothingGlobals.HAT][2]
            self.pirate.style.clothes.hatTexture = self.equipRequests[ClothingGlobals.HAT][3]
            self.pirate.style.clothes.hatColor = self.equipRequests[ClothingGlobals.HAT][1]
        self.pirate.model.handleClothesHiding()
        self.pirate.model.handleHeadHiding()
        return

    def equipAccessory(self, accessory):
        uid = accessory[5]
        colorId = accessory[4]
        type = accessory[1]
        modelId = accessory[2]
        texId = accessory[3]
        data = [uid, colorId, type]
        self.equipRequests[type] = [
         uid, colorId, modelId, texId]
        self.reloadPirateDNA()
        type = accessory[1]
        gender = localAvatar.style.getGender()
        if self.equipRequests[ClothingGlobals.VEST] is None:
            vestIdx = localAvatar.style.getClothesVest()[0]
        else:
            vestIdx = self.equipRequests[ClothingGlobals.VEST][2]
        if type == ClothingGlobals.SHIRT and gender == 'f' and vestIdx in [3, 4]:
            self.showCutOffVestAlert()
        for button in self.buttons:
            if button != accessory[0]:
                button.equippedText.hide()
                button.equip.show()
                button.addToCart['state'] = DGG.NORMAL
                button.equip['text'] = PLocalizer.TailorEquip
                button.equip['extraArgs'] = [[button, ClothingGlobals.CLOTHING_NUMBER[button.clothModelType], button.clothModelId, button.clothTextureId, button.clothColorId, button.clothUid]]

        if accessory[0].equippedText.isHidden():
            accessory[0].equippedText.show()
            accessory[0].equip['text'] = PLocalizer.TailorTakeOff
            accessory[0].equip['extraArgs'] = [[accessory[0], accessory[1], 0, 0, 0, 0]]
            if accessory[1] == ClothingGlobals.PANT:
                accessory[0].equip.hide()
                accessory[0].addToCart['state'] = DGG.DISABLED
            elif gender == 'f' and accessory[1] == ClothingGlobals.SHIRT:
                accessory[0].equip.hide()
                accessory[0].addToCart['state'] = DGG.DISABLED
            else:
                accessory[0].equip.show()
        else:
            accessory[0].equippedText.hide()
            accessory[0].equip.show()
            accessory[0].equip['text'] = PLocalizer.TailorEquip
            accessory[0].equip['extraArgs'] = [[accessory[0], ClothingGlobals.CLOTHING_NUMBER[accessory[0].clothModelType], accessory[0].clothModelId, accessory[0].clothTextureId, accessory[0].clothColorId, accessory[0].clothUid]]
        return

    def sortItems(self, item1, item2):
        if item1[4] == True:
            return -1
        else:
            if item2[4] == True:
                return 1
            else:
                if self.mode == 0:
                    if item1[7] is not None:
                        return -1
                    elif item2[7] is not None:
                        return 1
                    elif item1[5] > item2[5]:
                        return 1
                    elif item1[5] < item2[5]:
                        return -1
                    elif item1[6] > item2[6]:
                        return 1
                    elif item1[6] < item2[6]:
                        return -1
                    elif item1[1] > item2[1]:
                        return 1
                    elif item1[1] < item2[1]:
                        return -1
                    else:
                        return 0
                else:
                    if self.mode == 1:
                        if item1[3] < item2[3]:
                            return 1
                        elif item1[3] > item2[3]:
                            return -1
                        else:
                            return 0
        return

    def setPage(self, pageName, startIndex=0, refreshWardrobe=True):
        self.tabBar.unstash()
        self.titleLabel['text'] = '\x01smallCaps\x01' + self.rootTitle + ' - ' + self.categoryText[pageName][1] + '\x02'
        if localAvatar.style.getGender() == 'm':
            GENDER = 'MALE'
        else:
            GENDER = 'FEMALE'
        clothingTypeId = pageName
        if self.currentPage != pageName:
            self.prevIdx = 0
        self.currentPage = pageName
        clothingType = ClothingGlobals.CLOTHING_STRING[clothingTypeId]
        gender = localAvatar.style.getGender()
        if refreshWardrobe:
            self.npc.sendRequestAccessoriesList()
        topColor = localAvatar.style.getClothesTopColor()
        botColor = localAvatar.style.getClothesBotColor()
        if self.equipRequests[ClothingGlobals.HAT] is None:
            currentHat = [
             ClothingGlobals.HAT, localAvatar.style.clothes.hat, localAvatar.style.clothes.hatTexture, localAvatar.style.clothes.hatColor]
        else:
            currentHat = [
             ClothingGlobals.HAT, self.equipRequests[ClothingGlobals.HAT][2], self.equipRequests[ClothingGlobals.HAT][3], self.equipRequests[ClothingGlobals.HAT][1]]
        if self.equipRequests[ClothingGlobals.SHIRT] is None:
            currentShirt = [
             ClothingGlobals.SHIRT, localAvatar.style.clothes.shirt, localAvatar.style.clothes.shirtTexture, topColor[0]]
        else:
            currentShirt = [
             ClothingGlobals.SHIRT, self.equipRequests[ClothingGlobals.SHIRT][2], self.equipRequests[ClothingGlobals.SHIRT][3], self.equipRequests[ClothingGlobals.SHIRT][1]]
        if self.equipRequests[ClothingGlobals.VEST] is None:
            currentVest = [
             ClothingGlobals.VEST, localAvatar.style.clothes.vest, localAvatar.style.clothes.vestTexture, topColor[1]]
        else:
            currentVest = [
             ClothingGlobals.VEST, self.equipRequests[ClothingGlobals.VEST][2], self.equipRequests[ClothingGlobals.VEST][3], self.equipRequests[ClothingGlobals.VEST][1]]
        if self.equipRequests[ClothingGlobals.COAT] is None:
            currentCoat = [
             ClothingGlobals.COAT, localAvatar.style.clothes.coat, localAvatar.style.clothes.coatTexture, topColor[2]]
        else:
            currentCoat = [
             ClothingGlobals.COAT, self.equipRequests[ClothingGlobals.COAT][2], self.equipRequests[ClothingGlobals.COAT][3], self.equipRequests[ClothingGlobals.COAT][1]]
        if self.equipRequests[ClothingGlobals.PANT] is None:
            currentPant = [
             ClothingGlobals.PANT, localAvatar.style.clothes.pant, localAvatar.style.clothes.pantTexture, botColor[0]]
        else:
            currentPant = [
             ClothingGlobals.PANT, self.equipRequests[ClothingGlobals.PANT][2], self.equipRequests[ClothingGlobals.PANT][3], self.equipRequests[ClothingGlobals.PANT][1]]
        if self.equipRequests[ClothingGlobals.SHOE] is None:
            currentShoe = [
             ClothingGlobals.SHOE, localAvatar.style.clothes.shoe, localAvatar.style.clothes.shoeTexture, botColor[2]]
        else:
            currentShoe = [
             ClothingGlobals.SHOE, self.equipRequests[ClothingGlobals.SHOE][2], self.equipRequests[ClothingGlobals.SHOE][3], self.equipRequests[ClothingGlobals.SHOE][1]]
        if self.equipRequests[ClothingGlobals.BELT] is None:
            currentBelt = [
             ClothingGlobals.BELT, localAvatar.style.clothes.belt, localAvatar.style.clothes.beltTexture, botColor[1]]
        else:
            currentBelt = [
             ClothingGlobals.BELT, self.equipRequests[ClothingGlobals.BELT][2], self.equipRequests[ClothingGlobals.BELT][3], self.equipRequests[ClothingGlobals.BELT][1]]
        clothes = []
        if self.mode == 0:
            if not self.currentWardrobe:
                return
            startRange = 0
            if GENDER == 'MALE':
                if clothingTypeId == ClothingGlobals.HAT:
                    startRange = ClothingGlobals.HAT_START_RANGE_MALE
                elif clothingTypeId == ClothingGlobals.SHIRT:
                    startRange = ClothingGlobals.SHIRT_START_RANGE_MALE
                elif clothingTypeId == ClothingGlobals.VEST:
                    startRange = ClothingGlobals.VEST_START_RANGE_MALE
                elif clothingTypeId == ClothingGlobals.COAT:
                    startRange = ClothingGlobals.COAT_START_RANGE_MALE
                elif clothingTypeId == ClothingGlobals.PANT:
                    startRange = ClothingGlobals.PANT_START_RANGE_MALE
                elif clothingTypeId == ClothingGlobals.BELT:
                    startRange = ClothingGlobals.BELT_START_RANGE_MALE
                elif clothingTypeId == ClothingGlobals.SHOE:
                    startRange = ClothingGlobals.SHOE_START_RANGE_MALE
            else:
                if GENDER == 'FEMALE':
                    if clothingTypeId == ClothingGlobals.HAT:
                        startRange = ClothingGlobals.HAT_START_RANGE_FEMALE
                    elif clothingTypeId == ClothingGlobals.SHIRT:
                        startRange = ClothingGlobals.SHIRT_START_RANGE_FEMALE
                    elif clothingTypeId == ClothingGlobals.VEST:
                        startRange = ClothingGlobals.VEST_START_RANGE_FEMALE
                    elif clothingTypeId == ClothingGlobals.COAT:
                        startRange = ClothingGlobals.COAT_START_RANGE_FEMALE
                    elif clothingTypeId == ClothingGlobals.PANT:
                        startRange = ClothingGlobals.PANT_START_RANGE_FEMALE
                    elif clothingTypeId == ClothingGlobals.BELT:
                        startRange = ClothingGlobals.BELT_START_RANGE_FEMALE
                    elif clothingTypeId == ClothingGlobals.SHOE:
                        startRange = ClothingGlobals.SHOE_START_RANGE_FEMALE
            store = self.shopId
            set = ClothingGlobals.stores.get(store)
            if set is None:
                return
            for index in range(startRange, startRange + 9999):
                colorSet = set.get(index)
                if colorSet:
                    item = ClothingGlobals.UNIQUE_ID.get(index)
                    if item:
                        cost = item[5]
                        holiday = item[8]
                        id = item[1]
                        tex = item[2]
                        for colorId in colorSet:
                            scaler = ClothingGlobals.colorCostScaler.get(colorId)
                            if scaler:
                                newCost = int(cost * scaler)
                            if holiday is None or holiday in AccessoriesStoreGUI.holidayIdList:
                                clothes.append([index, colorId, 0, newCost, False, id, tex, holiday])

        if self.mode == 1:
            if self.currentWardrobe:
                for item in self.currentWardrobe:
                    cloth = ClothingGlobals.UNIQUE_ID.get(item[0])
                    if cloth[0] == clothingTypeId:
                        uid = item[0]
                        type = cloth[0]
                        id = cloth[1]
                        tex = cloth[2]
                        color = item[1]
                        original = item[2]
                        cost = cloth[5]
                        equipped = False
                        holiday = cloth[8]
                        scaler = ClothingGlobals.colorCostScaler.get(color)
                        if scaler:
                            cost = int(cost * scaler)
                        if [
                         type, id, tex, color] in [currentHat, currentShirt, currentVest, currentCoat, currentPant, currentShoe, currentBelt]:
                            equipped = True
                        clothes.append([uid, color, original, cost, equipped, id, tex, holiday])

            else:
                return
        if not config.GetBool('tailor-debug', 0):
            clothes.sort(self.sortItems)
        clothingAmount = 0
        startPos = Vec3(0.35, 0.0, 1.05)
        buttonScale = Vec3(0.6, 0.6, 0.6)
        for item in self.buttons:
            item.destroy()

        self.buttons = []
        self.clothingAmount = 0
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
        self.reloadPirateDNA()
        regionData = []
        for cloth in clothes:
            if self.clothingAmount - startIndex < self.buttonsPerPage and self.clothingAmount >= startIndex:
                uid = cloth[0]
                clothColorId = cloth[1]
                original = cloth[2]
                item = ClothingGlobals.UNIQUE_ID.get(uid)
                type = item[0]
                id = item[1]
                tex = item[2]
                owned = False
                newItem = False
                equipped = cloth[4]
                clothCost = cloth[3]
                shortDesc = item[6]
                longDesc = item[7]
                if self.mode == 1:
                    clothCost = int(clothCost * 0.25)
                for item in self.currentWardrobe:
                    if [uid, clothColorId] == item[:2]:
                        owned = True

                if self.mode == 1:
                    buttonState = DGG.DISABLED
                else:
                    buttonState = DGG.NORMAL
                helpText = longDesc
                if uid in ClothingGlobals.newClothing:
                    newItem = True
                if newItem:
                    helpText = PLocalizer.StoreNewItem + '\n\n' + helpText
                else:
                    if uid in ClothingGlobals.quest_items:
                        helpText = PLocalizer.ShopQuestItem + '!\n\n' + helpText
                clothButton = GuiButton.GuiButton(command=self.setClothes, parent=self.panel, state=buttonState, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.02), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, pos=startPos, image_scale=buttonScale, image_color=buttonColorA, extraArgs=[clothingTypeId, id, tex, clothColorId], helpText=helpText, helpDelay=0, helpPos=(0.0, 0.0, -0.11), helpLeftAlign=True)
                clothButton.helpWatcher.setPos(clothButton.getPos())
                if config.GetBool('tailor-debug', 0):
                    clothButton['text'] = text = str(uid)
                if self.mode == 0 and not owned:
                    clothButton.previewText = DirectFrame(parent=clothButton, relief=None, text=PLocalizer.TailorPreview, text_fg=PiratesGuiGlobals.TextFG1, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleSmall, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, pos=(-0.02, 0, -0.08))
                else:
                    if self.mode == 1:
                        clothButton.equippedText = DirectFrame(parent=clothButton, relief=None, text=PLocalizer.TattooShopOwned, text_fg=PiratesGuiGlobals.TextFG1, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleSmall, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, pos=(-0.02, 0, -0.08))
                        if equipped:
                            clothButton.equippedText.show()
                        else:
                            clothButton.equippedText.hide()
                clothButton.addToCart = GuiButton.GuiButton(command=self.addToCart, parent=clothButton, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, image_color=buttonColorB, pos=(0.16,
                                                                                                                                                                                                                                                                                                                     0.0,
                                                                                                                                                                                                                                                                                                                     0.055))
                clothButton.addToCart['extraArgs'] = [
                 clothButton, clothingType, id, tex, clothColorId, clothCost, uid]
                clothButton.bind(DGG.ENTER, self.highlightClothStart, extraArgs=[self.clothingAmount])
                clothButton.bind(DGG.EXIT, self.highlightClothStop, extraArgs=[self.clothingAmount])
                if self.mode == 0 and not owned:
                    if clothCost == 0:
                        clothCost = PLocalizer.ShopFree
                    clothButton.cost = DirectFrame(parent=clothButton, relief=None, text=str(clothCost), text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(-0.055, 0.0), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, image=self.CoinImage, image_scale=0.15, image_pos=(-0.025,
                                                                                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                                                                                           0.015), pos=(0.25, 0, -0.05))
                else:
                    if self.mode == 1:
                        if not equipped:
                            clothButton.equip = GuiButton.GuiButton(parent=clothButton, command=self.equipAccessory, text=PLocalizer.TailorEquip, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, image_color=buttonColorB, pos=(0.16, 0.0, -0.05))
                            clothButton.equip['extraArgs'] = [
                             [
                              clothButton, clothingTypeId, id, tex, clothColorId, uid]]
                        else:
                            clothButton.equip = GuiButton.GuiButton(parent=clothButton, command=self.equipAccessory, text=PLocalizer.TailorTakeOff, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, image_color=buttonColorB, pos=(0.16, 0.0, -0.05))
                            clothButton.equip['extraArgs'] = [
                             [
                              clothButton, clothingTypeId, 0, 0, 0, 0]]
                            if clothingTypeId == ClothingGlobals.PANT:
                                clothButton.equip.hide()
                            else:
                                if gender == 'f' and clothingTypeId == ClothingGlobals.SHIRT:
                                    clothButton.equip.hide()
                        if original:
                            clothButton.addToCart['state'] = DGG.DISABLED
                            clothButton.addToCart.hide()
                            clothButton.originalItem = DirectFrame(parent=clothButton, relief=None, text=PLocalizer.TailorStartingItem, text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, pos=(0.16,
                                                                                                                                                                                                                                                                                                                     0.0,
                                                                                                                                                                                                                                                                                                                     0.04))
                if self.paid == OTPGlobals.AccessVelvetRope:
                    if self.mode == 1:
                        clothButton.equip['geom'] = self.LockIcon
                        clothButton.equip['geom_scale'] = 0.2
                        clothButton.equip['geom_pos'] = Vec3(-0.1, 0.0, 0.0)
                        clothButton.equip['command'] = localAvatar.guiMgr.showNonPayer
                        clothButton.equip['extraArgs'] = ['CLOTHING_CANNOT_EQUIP', 10]
                    clothButton.addToCart['geom'] = self.LockIcon
                    clothButton.addToCart['geom_scale'] = 0.2
                    clothButton.addToCart['geom_pos'] = Vec3(-0.1, 0.0, 0.0)
                    clothButton.addToCart['command'] = localAvatar.guiMgr.showNonPayer
                    clothButton.addToCart['extraArgs'] = ['CLOTHING_CANNOT_BUY-SELL', 10]
                data = [
                 clothingType, id, tex, clothColorId, clothCost]
                if self.mode == 0 and owned:
                    clothButton.addToCart.buyState = 0
                    clothButton.addToCart['state'] = DGG.DISABLED
                    clothButton['state'] = DGG.DISABLED
                    clothButton.addToCart['text'] = PLocalizer.TailorPurchased
                else:
                    if self.mode == 0 and self.purchaseInventory.hasPanel(data):
                        clothButton.addToCart.buyState = 0
                        clothButton.addToCart['state'] = DGG.NORMAL
                        clothButton.addToCart['text'] = PLocalizer.TailorRemove
                    else:
                        if self.mode == 1 and self.sellInventory.hasPanel(data):
                            clothButton.addToCart.buyState = 0
                            clothButton.addToCart['state'] = DGG.NORMAL
                            clothButton.addToCart['text'] = PLocalizer.TailorRemove
                            clothButton.equip['state'] = DGG.DISABLED
                        else:
                            clothButton.addToCart.buyState = 1
                            clothButton.addToCart['state'] = DGG.NORMAL
                            if self.mode == 0:
                                clothButton.addToCart['text'] = PLocalizer.TailorAddToCart
                            else:
                                if self.mode == 1:
                                    clothButton.equip['state'] = DGG.NORMAL
                                    clothButton.addToCart['text'] = PLocalizer.TailorSell
                if equipped and type == ClothingGlobals.PANT:
                    clothButton.addToCart['state'] = DGG.DISABLED
                else:
                    if equipped and gender == 'f' and type == ClothingGlobals.SHIRT:
                        clothButton.addToCart['state'] = DGG.DISABLED
                startPos -= Vec3(0.0, 0.0, clothButton.getHeight() - 0.02)
                clothButton.clothModelId = id
                clothButton.clothModelType = ClothingGlobals.CLOTHING_STRING[type]
                clothButton.clothTextureId = tex
                clothButton.clothColorId = clothColorId
                clothButton.clothUid = uid
                clothButton.original = original
                regionData.append([ClothingGlobals.CLOTHING_STRING[type], id, tex, clothColorId])
                self.buttons.append(clothButton)
            self.clothingAmount += 1

        if clothingTypeId == ClothingGlobals.PANT and self.mode == 1:
            pants = 0
            for cloth in self.currentWardrobe:
                uid = cloth[0]
                type = ClothingGlobals.UNIQUE_ID[uid][0]
                if type == ClothingGlobals.PANT:
                    pants += 1

            if pants == 1:
                self.buttons[0].addToCart['state'] = DGG.DISABLED
        if not len(clothes):
            clothButton = GuiButton.GuiButton(command=self.setClothes, parent=self.panel, state=DGG.DISABLED, text=PLocalizer.TailorEmptyWardrobe, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0,
                                                                                                                                                                                                0.0), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, pos=startPos, image_scale=buttonScale, image_color=buttonColorA)
            clothButton.clothModelId = -1
            clothButton.clothModelType = -1
            clothButton.clothTextureId = -1
            clothButton.clothColorId = -1
            clothButton.clothUid = -1
            clothButton.original = -1
            self.buttons.append(clothButton)
        if len(clothes):
            self.setupDisplayRegions(regionData, pageName)
        else:
            for item in self.clothRenders:
                item.hide()

            if self.clothingAmount <= self.buttonsPerPage:
                self.nextPageButton['state'] = DGG.DISABLED
                self.prevPageButton['state'] = DGG.DISABLED
            if startIndex:
                self.prevPageButton['state'] = DGG.NORMAL
            if startIndex + self.buttonsPerPage < self.clothingAmount:
                self.nextPageButton['state'] = DGG.NORMAL
                self.prevPageButton['state'] = DGG.NORMAL
            if self.clothingAmount > self.buttonsPerPage:
                numPages = float(self.clothingAmount) / float(self.buttonsPerPage)
                remainder = numPages - int(numPages)
                if remainder > 0:
                    numPages += 1.0 - remainder
                page = startIndex / self.buttonsPerPage + 1
            numPages = 1
            page = 1
        self.pageNumber['text'] = '%s %s / %s' % (PLocalizer.TailorPage, page, int(numPages))
        return

    def _stopMouseReadTask(self):
        taskMgr.remove('AccessoriesStore-MouseRead')

    def _startMouseReadTask(self):
        self._stopMouseReadTask()
        mouseData = base.win.getPointer(0)
        self.lastMousePos = (mouseData.getX(), mouseData.getY())
        taskMgr.add(self._mouseReadTask, 'AccessoriesStore-MouseRead')

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

    def highlightClothStart(self, item, event=None):
        pass

    def highlightClothStop(self, item, event=None):
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
            item.removeNode()

        self.clothRenders = []
        for item in self.clothHumans:
            item.delete()
            item.removeNode()

        self.clothHumans = []
        for item in self.clothCameraNPs:
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
        startRegion = Vec4(0.526, 0.596, 0.62, 0.69)
        bodyShape = localAvatar.style.getBodyShape()
        if bodyShape == 0:
            bodyOffset = 1
        else:
            if bodyShape == 1:
                bodyOffset = 0
            else:
                if bodyShape == 2:
                    bodyOffset = 0.5
                else:
                    if bodyShape == 3:
                        bodyOffset = 1
                    else:
                        if bodyShape == 4:
                            bodyOffset = 0.5
        x = 0
        m = Mat4(Mat4.identMat())
        headHeight = None
        spine3Height = None
        spine2Height = None
        kneeHeight = None
        hipHeight = None
        ankleHeight = None
        gender = localAvatar.style.getGender()
        source = localAvatar
        source.pose('idle', 1)
        source.update()
        x = 0
        for x in range(len(regionData)):
            if pageName == ClothingGlobals.HAT:
                if headHeight is None:
                    localAvatar.getLOD('2000').getChild(0).node().findJoint('def_head01').getNetTransform(m)
                    headHeight = TransformState.makeMat(m).getPos().getZ()
                offsetZ = -headHeight - 0.4
                offsetY = 2.0 + bodyOffset
                offsetH = 200
            else:
                if pageName == ClothingGlobals.SHIRT:
                    if spine3Height is None:
                        localAvatar.getLOD('2000').getChild(0).node().findJoint('def_spine03').getNetTransform(m)
                        spine3Height = TransformState.makeMat(m).getPos().getZ()
                    offsetZ = -spine3Height
                    offsetY = 3.25 + bodyOffset
                    offsetH = 200
                else:
                    if pageName == ClothingGlobals.VEST:
                        if spine3Height is None:
                            localAvatar.getLOD('2000').getChild(0).node().findJoint('def_spine03').getNetTransform(m)
                            spine3Height = TransformState.makeMat(m).getPos().getZ()
                        offsetZ = -spine3Height
                        offsetY = 3.5 + bodyOffset
                        offsetH = 200
                    else:
                        if pageName == ClothingGlobals.COAT:
                            if spine2Height is None:
                                localAvatar.getLOD('2000').getChild(0).node().findJoint('def_spine02').getNetTransform(m)
                                spine2Height = TransformState.makeMat(m).getPos().getZ()
                            offsetZ = -spine2Height
                            offsetY = 4.5 + bodyOffset
                            offsetH = 200
                        else:
                            if pageName == ClothingGlobals.PANT:
                                if kneeHeight is None:
                                    localAvatar.getLOD('2000').getChild(0).node().findJoint('def_right_knee').getNetTransform(m)
                                    kneeHeight = TransformState.makeMat(m).getPos().getZ()
                                offsetZ = -kneeHeight - 0.5
                                offsetY = 4.5 + bodyOffset
                                offsetH = 200
                            else:
                                if pageName == ClothingGlobals.BELT:
                                    if hipHeight is None:
                                        localAvatar.getLOD('2000').getChild(0).node().findJoint('def_hips').getNetTransform(m)
                                        hipHeight = TransformState.makeMat(m).getPos().getZ()
                                    offsetZ = -hipHeight
                                    offsetY = 1.7 + bodyOffset
                                    offsetH = 180
                                else:
                                    if pageName == ClothingGlobals.SHOE:
                                        if ankleHeight is None:
                                            localAvatar.getLOD('2000').getChild(0).node().findJoint('def_right_ankle').getNetTransform(m)
                                            ankleHeight = TransformState.makeMat(m).getPos().getZ()
                                        offsetZ = -ankleHeight - 0.15
                                        offsetY = 3.25 + bodyOffset
                                        offsetH = 200
                                    else:
                                        offsetZ = 0
                                        offsetY = 0
                                        offsetH = 0
            self.clothHumans[x].setY(offsetY)
            self.clothHumans[x].setZ(offsetZ)
            self.clothHumans[x].setH(offsetH)
            topColor = localAvatar.style.getClothesBotColor()
            botColor = localAvatar.style.getClothesTopColor()
            hatColor = localAvatar.style.getHatColor()
            shirtIdx, shirtTex = localAvatar.style.getClothesShirt()
            hatIdx, hatTex = localAvatar.style.getClothesHat()
            coatIdx, coatTex = localAvatar.style.getClothesCoat()
            beltIdx, beltTex = localAvatar.style.getClothesBelt()
            shoeIdx, shoeTex = localAvatar.style.getClothesShoe()
            vestIdx, vestTex = localAvatar.style.getClothesVest()
            pantIdx, pantTex = localAvatar.style.getClothesPant()
            self.clothHumans[x].style.setClothesBotColor(topColor[0], topColor[1], topColor[2])
            self.clothHumans[x].style.setClothesTopColor(botColor[0], botColor[1], botColor[2])
            self.clothHumans[x].style.setHatColor(hatColor)
            self.clothHumans[x].style.setClothesShirt(shirtIdx, shirtTex)
            self.clothHumans[x].style.setClothesHat(hatIdx, hatTex)
            self.clothHumans[x].style.setClothesBelt(beltIdx, beltTex)
            self.clothHumans[x].style.setClothesPant(pantIdx, pantTex)
            self.clothHumans[x].style.setClothesShoe(shoeIdx, shoeTex)
            if pageName == ClothingGlobals.SHIRT:
                self.clothHumans[x].style.setClothesVest(0)
                self.clothHumans[x].style.setClothesCoat(0)
            else:
                if pageName == ClothingGlobals.VEST:
                    self.clothHumans[x].style.setClothesCoat(0)
                else:
                    if pageName == ClothingGlobals.BELT:
                        self.clothHumans[x].style.setClothesCoat(0)
                        self.clothHumans[x].style.setClothesVest(0)
                    else:
                        self.clothHumans[x].style.setClothesVest(vestIdx, vestTex)
                        self.clothHumans[x].style.setClothesCoat(coatIdx, coatTex)
            self.clothHumans[x].model.handleClothesHiding()
            self.clothHumans[x].model.handleHeadHiding()
            self.clothHumans[x].setClothesByType(regionData[x][0], regionData[x][1], regionData[x][2], regionData[x][3])
            self.clothHumans[x].model.handleClothesHiding()
            self.clothHumans[x].model.handleHeadHiding()
            self.clothRenders[x].show()

        if x < self.buttonsPerPage - 1:
            for y in range(self.buttonsPerPage - 1 - x):
                self.clothRenders[self.buttonsPerPage - 1 - y].hide()

        self.aspectRatioChange()
        return

    def showWardrobeLimitAlert(self, type):
        self.removeAlertDialog()
        limit = str(PiratesGlobals.WARDROBE_LIMIT_TAILOR)
        text = PLocalizer.ShopLimitTailor % limit
        self.alertDialog = PDialog.PDialog(text=text, text_align=TextNode.ACenter, style=OTPDialog.Acknowledge, pos=(-0.65, 0.0, 0.0), command=self.removeAlertDialog)
        self.alertDialog.setBin('gui-fixed', 20, 20)

    def showCutOffVestAlert(self):
        self.removeAlertDialog()
        text = PLocalizer.ShopFemaleVestConflict
        self.alertDialog = PDialog.PDialog(text=text, text_align=TextNode.ACenter, style=OTPDialog.Acknowledge, pos=(-0.65, 0.0, 0.0), command=self.removeAlertDialog)
        self.alertDialog.setBin('gui-fixed', 20, 20)

    def removeAlertDialog(self, value=None):
        if self.alertDialog:
            self.alertDialog.destroy()
            self.alertDialog = None
        return
