# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.economy.ShipStoreGUI
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.piratesbase import Freebooter, PiratesGlobals, PLocalizer
from pirates.piratesgui import (BarChart, DialogButton, GuiButton, GuiPanel,
                                NamePanelGui, PiratesGuiGlobals, ShipItemList)
from pirates.ship import ShipGlobals
from pirates.uberdog.UberDogGlobals import *


class ShipStoreGUI(GuiPanel.GuiPanel):
    __module__ = __name__
    notify = directNotify.newCategory('ShipStoreGUI')
    width = (PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.06) * 2
    height = 1.35
    columnWidth = PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.05
    ShipIconTable = {ItemId.INTERCEPTOR_L1: 'Interceptor_Render', ItemId.INTERCEPTOR_L2: 'Interceptor_Render', ItemId.INTERCEPTOR_L3: 'Interceptor_Render', ItemId.MERCHANT_L1: 'Merchant_Render', ItemId.MERCHANT_L2: 'Merchant_Render', ItemId.MERCHANT_L3: 'Merchant_Render', ItemId.WARSHIP_L1: 'Warship_Render', ItemId.WARSHIP_L2: 'Warship_Render', ItemId.WARSHIP_L3: 'Warship_Render'}

    def __init__(self, inventory, name):
        GuiPanel.GuiPanel.__init__(self, name, self.width, self.height, showClose=False)
        self.setPos(-1.25, 0, -0.66)
        self.initialiseoptions(ShipStoreGUI)
        self.balance = 0
        self.purchaseInventory = [[ItemId.INTERCEPTOR_L1, 1]]
        self.sellInventory = []
        self.statData = []
        self.namePanel = None
        self.updateStats()
        self.storeInventory = ShipItemList.ShipItemList(inventory, self.height - 0.1, buy=PiratesGuiGlobals.InventoryAdd)
        self.storeInventory.reparentTo(self)
        self.storeInventory.setPos(0.02, 0, 0.02)
        self.purchaseTitle = DirectFrame(parent=self, relief=None, text=PLocalizer.InventoryTypeNames[self.purchaseInventory[0][0]], text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.03,
                                                                                                                                                                                                                       0.01), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1)
        self.purchaseTitle.setPos(self.storeInventory.width, 0, 0.707 + (self.height - 0.065) / 2.5)
        self.card = loader.loadModel('models/textureCards/shipRenders')
        self.shipImage = DirectFrame(parent=self, relief=DGG.FLAT, image_scale=0.2, frameColor=(0,
                                                                                                0,
                                                                                                0,
                                                                                                1.0), borderWidth=PiratesGuiGlobals.BorderWidthSmall, pad=(0.01,
                                                                                                                                                           0.01), frameSize=(-0.26, 0.26, -0.185, 0.185), textMayChange=1, pos=(self.width * 0.72, 0, 1))
        self.shipImage.setTransparency(1)
        barChartWidth = self.width - (self.storeInventory.width + 0.04)
        self.shipStats = BarChart.BarChart(self.statData, 0.25, barChartWidth, PLocalizer.ShipProfile, PiratesGuiGlobals.TextFG1)
        self.shipStats.reparentTo(self)
        self.shipStats.setPos(self.storeInventory.width + 0.03, 0, 0.12)
        self.descText = DirectFrame(parent=self, relief=None, text=PLocalizer.ShipDescriptions[self.purchaseInventory[0][0]], text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleMed, text_pos=(0.03,
                                                                                                                                                                                                              0.01), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, frameColor=(0,
                                                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                                                              0), frameSize=(0.02, self.width - self.storeInventory.width - 0.02, 0, 0.05), textMayChange=1, text_wordwrap=18, pos=(self.storeInventory.width, 0, 0.75))
        self.balanceTitle = DirectFrame(parent=self, relief=None, text=PLocalizer.Cost, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.31,
                                                                                                                                                                          0.411), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, pos=(self.columnWidth, 0, -0.01))
        self.goldTitle = DirectFrame(parent=self, relief=None, text='%s:' % PLocalizer.MoneyName, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.31,
                                                                                                                                                                                    0.411), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, pos=(self.columnWidth, 0, 0.04))
        coinImage = loader.loadModel('models/gui/toplevel_gui').find('**/treasure_w_coin*')
        self.balanceValue = DirectFrame(parent=self, relief=None, text=str(self.balance), text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.53,
                                                                                                                                                                             0.411), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, image=coinImage, image_scale=0.15, image_pos=(0.56,
                                                                                                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                                                                                                 0.425), pos=(self.columnWidth, 0, -0.01))
        self.goldValue = DirectFrame(parent=self, relief=None, text=str(localAvatar.getMoney()), text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.53,
                                                                                                                                                                                    0.411), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, image=coinImage, image_scale=0.15, image_pos=(0.56,
                                                                                                                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                                                                                                                        0.425), pos=(self.columnWidth, 0, 0.04))
        coinImage.removeNode()
        self.commitButton = DialogButton.DialogButton(command=self.handleCommitPurchase, buttonStyle=DialogButton.DialogButton.YES, parent=self, relief=None, text=PLocalizer.PurchaseCommit, text_fg=PiratesGuiGlobals.TextFG2, text_scale=PiratesGuiGlobals.TextScaleLarge, textMayChange=0, pos=(self.width - 0.39, 0, 0.07), sortOrder=0)
        lockImage = loader.loadModel('models/gui/toplevel_gui').find('**/subscribers_lock')
        self.lock = DirectFrame(parent=self.commitButton, relief=None, image=lockImage, image_scale=0.15, pos=(-0.06, 0, 0))
        self.lock.hide()
        self.closeButton = DialogButton.DialogButton(command=self.closePanel, buttonStyle=DialogButton.DialogButton.NO, parent=self, relief=None, text=PLocalizer.lClose, text_fg=PiratesGuiGlobals.TextFG2, text_scale=PiratesGuiGlobals.TextScaleLarge, textMayChange=0, pos=(self.width - 0.145, 0, 0.07))
        self.updateProfile()
        self.accept('inventoryQuantity-%s-%s' % (base.localAvatar.getInventoryId(), InventoryType.GoldInPocket), self.updateBalance)
        self.accept(PiratesGuiGlobals.InventoryBuyEvent, self.handleBuyItem)
        self.accept(PiratesGuiGlobals.InventorySellEvent, self.handleSellItem)
        self.acceptOnce('escape', self.closePanel)
        base.ssg = self
        return

    def updateProfile(self):
        imageName = self.ShipIconTable.get(self.purchaseInventory[0][0])
        myTexCard = self.card.find('**/' + imageName + '*')
        myTex = myTexCard.findAllTextures()[0]
        self.purchaseTitle['text'] = PLocalizer.InventoryTypeNames[self.purchaseInventory[0][0]]
        self.descText['text'] = (PLocalizer.ShipDescriptions[self.purchaseInventory[0][0]],)
        self.shipImage['image'] = myTex
        self.shipImage['image_scale'] = 0.25
        self.updateStats()
        self.shipStats.refreshBars(self.statData)
        self.updateBalance()
        if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
            if self.purchaseInventory[0][0] != ItemId.INTERCEPTOR_L1 and self.purchaseInventory[0][0] != ItemId.MERCHANT_L1:
                self.lock.show()
            else:
                self.lock.hide()

    def updateStats(self):
        self.statData = []
        stats = ShipGlobals.getHullStats(self.purchaseInventory[0][0])
        maxStats = ShipGlobals.getMaxHullStats()
        self.statData.append([PLocalizer.Hull, stats['maxHp'], maxStats['maxHp']])
        self.statData.append([PLocalizer.Sail, stats['maxSp'], maxStats['maxSp']])
        self.statData.append([PLocalizer.Cannon, stats['maxCannons'], maxStats['maxCannons']])
        self.statData.append([PLocalizer.Broadsides, stats['maxBroadsides'], maxStats['maxBroadsides']])
        self.statData.append([PLocalizer.Cargo, stats['maxCargo'], maxStats['maxCargo']])
        self.statData.append([PLocalizer.Crew, stats['maxCrew'], maxStats['maxCrew']])

    def closePanel(self):
        if self.namePanel:
            self.namePanel.destroy()
            self.namePanel = None
        if self.card:
            self.card.removeNode()
        messenger.send('exitStore')
        self.ignoreAll()
        return

    def handleBuyItem(self, data, useCode):
        if useCode == PiratesGuiGlobals.InventoryAdd:
            self.purchaseInventory = [
             data]
            self.updateProfile()
        else:
            if useCode == PiratesGuiGlobals.InventoryRemove:
                pass

    def handleSellItem(self, data, useCode):
        self.updateBalance()

    def handleCommitPurchase(self):
        if self.purchaseInventory == [] and self.sellInventory == []:
            base.localAvatar.guiMgr.createWarning(PLocalizer.EmptyPurchaseWarning, PiratesGuiGlobals.TextFG6)
            return
        if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
            if self.purchaseInventory[0][0] != ItemId.INTERCEPTOR_L1 and self.purchaseInventory[0][0] != ItemId.MERCHANT_L1:
                base.localAvatar.guiMgr.showNonPayer('Purchase_Restriction', 3)
                return
        inventory = base.localAvatar.getInventory()
        if inventory:
            if inventory.getStackQuantity(InventoryType.GoldInPocket) < self.balance:
                base.localAvatar.guiMgr.createWarning(PLocalizer.NotEnoughMoneyWarning, PiratesGuiGlobals.TextFG6)
                return
            if self.balance < 0 and inventory.getStackQuantity(InventoryType.GoldInPocket) + self.balance > inventory.getStackLimit(InventoryType.GoldInPocket):
                base.localAvatar.guiMgr.createWarning(PLocalizer.CannotHoldGoldWarning, PiratesGuiGlobals.TextFG6)
                return
            if len(inventory.getShipDoIdList()) >= inventory.getCategoryLimit(InventoryCategory.SHIPS):
                base.localAvatar.guiMgr.createWarning(PLocalizer.CannotHoldShipWarning, PiratesGuiGlobals.TextFG6)
                return
        nameData = [
         list(PLocalizer.PirateShipPrefix.keys()), list(PLocalizer.PirateShipSuffix.keys())]
        self.namePanel = NamePanelGui.NamePanelGui(PLocalizer.NamePanelTitle, nameData)
        self.namePanel.setPos(0.2, 0, 0)
        self.lockStore()
        self.acceptOnce('returnStore', self.unlockStore)
        self.acceptOnce('nameChosen', self.handleCommitPurchasePart2)

    def handleCommitPurchasePart2(self, shipNames):
        self.ignore('returnStore')
        self.ignore('nameChosen')
        nameIndices = []
        nameIndices.append(shipNames)
        ShipStoreGUI.notify.debug('Make Purchase - Buying: %s, Selling: %s' % (self.purchaseInventory, self.sellInventory))
        messenger.send('makeSale', [self.purchaseInventory, self.sellInventory, nameIndices])

    def updateBalance(self, extraArgs=None):
        self.balance = 0
        for item in self.purchaseInventory:
            self.balance += EconomyGlobals.getItemCost(item[0])

        if self.balance > 0:
            self.balanceTitle['text'] = PLocalizer.Cost
            self.balanceValue['text'] = str(abs(self.balance))
        else:
            if self.balance < 0:
                self.balanceTitle['text'] = PLocalizer.Gain
                self.balanceValue['text'] = str(abs(self.balance))
            else:
                self.balanceTitle['text'] = PLocalizer.Cost
                self.balanceValue['text'] = str(abs(self.balance))
        inventory = base.localAvatar.getInventory()
        if inventory:
            if inventory.getStackQuantity(InventoryType.GoldInPocket) < self.balance:
                self.commitButton['frameColor'] = PiratesGuiGlobals.ButtonColor3
            elif len(inventory.getShipDoIdList()) >= inventory.getCategoryLimit(InventoryCategory.SHIPS):
                self.commitButton['frameColor'] = PiratesGuiGlobals.ButtonColor3
            else:
                self.commitButton['frameColor'] = PiratesGuiGlobals.ButtonColor4

    def lockStore(self):
        self.commitButton['state'] = DGG.DISABLED
        self.commitButton['frameColor'] = (0.4, 0.4, 0.4, 1)

    def unlockStore(self):
        self.commitButton['state'] = DGG.NORMAL
        self.updateBalance()
# okay decompiling .\pirates\economy\ShipStoreGUI.pyc
