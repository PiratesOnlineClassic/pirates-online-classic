# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.economy.StoreGUI
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.reputation import ReputationGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryItemList
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import GuiButton
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiButton
from pirates.piratesgui import PurchaseList
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import *
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.piratesgui.TabBar import LeftTab, TabBar

class StoreTab(LeftTab):
    __module__ = __name__

    def __init__(self, tabBar, name, **kw):
        optiondefs = (('suffix', '_d', None), ('borderScale', 0.38, None), ('bgBuffer', 0.15, None))
        self.defineoptions(kw, optiondefs)
        LeftTab.__init__(self, tabBar, name, **kw)
        self.initialiseoptions(StoreTab)
        return


class StoreTabBar(TabBar):
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
        return StoreTab(self, name, **kw)


class StoreGUI(DirectFrame):
    __module__ = __name__
    notify = directNotify.newCategory('StoreGUI')
    width = (PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.06) * 2
    height = 1.35
    columnWidth = PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.05
    CoinImage = None
    WeaponIcons = None
    SkillIcons = None

    def __init__(self, inventory, name, **kw):
        optiondefs = (
         ('relief', None, None), ('framSize', (0, self.width, 0, self.height), None), ('sortOrder', 20, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, None, **kw)
        self.initialiseoptions(StoreGUI)
        if not StoreGUI.CoinImage:
            StoreGUI.CoinImage = loader.loadModel('models/gui/toplevel_gui').find('**/treasure_w_coin*')
        if not StoreGUI.WeaponIcons:
            StoreGUI.WeaponIcons = loader.loadModelCopy('models/textureCards/weapon_icons')
        if not StoreGUI.SkillIcons:
            StoreGUI.SkillIcons = loader.loadModelCopy('models/textureCards/skillIcons')
        self.backTabParent = self.attachNewNode('backTabs', sort=0)
        self.panel = GuiPanel.GuiPanel(name, self.width, self.height, parent=self)
        self.panel.closeButton['command'] = self.closePanel
        self.setPos(-1.1, 0, -0.66)
        self.balance = 0
        self.inventory = inventory
        self.storeInventory = InventoryItemList.InventoryItemList(self.inventory, self.height - 0.15, buy=PiratesGuiGlobals.InventoryAdd)
        self.storeInventory.reparentTo(self.panel)
        self.storeInventory.setPos(0.03, 0, 0.04)
        self.cartWidth = self.columnWidth - 0.1
        self.cartHeight = self.height - 0.25
        self.cartFrame = DirectFrame(parent=self.panel, relief=None, frameSize=(0, self.cartWidth, 0, self.cartHeight))
        self.cartFrame.setPos(self.columnWidth + 0.025, 0, 0.08)
        self.purchaseTitle = DirectFrame(parent=self.cartFrame, relief=None, text=PLocalizer.PurchaseCart, text_fg=PiratesGuiGlobals.TextFG1, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0, -0.03), textMayChange=0, pos=(self.cartWidth / 2, 0, self.cartHeight))
        self.purchaseInventory = PurchaseList.PurchaseList([], self.cartHeight - 0.25, buy=PiratesGuiGlobals.InventoryRemove)
        self.purchaseInventory.reparentTo(self.cartFrame)
        self.purchaseInventory.setPos(0, 0, 0.2)
        self.frontTabParent = self.panel.attachNewNode('frontTab', sort=2)
        self.balanceTitle = DirectFrame(parent=self.cartFrame, relief=None, text=PLocalizer.Total, text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                                        0.0), pos=(0.01,
                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                   0.225))
        self.balanceValue = DirectFrame(parent=self.cartFrame, relief=None, text=str(self.balance), text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(-0.055, 0.0), textMayChange=1, image=StoreGUI.CoinImage, image_scale=0.15, image_pos=(-0.025,
                                                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                                                0.025), pos=(self.cartWidth, 0, 0.225))
        self.myGoldTitle = DirectFrame(parent=self.cartFrame, relief=None, text=PLocalizer.YourMoney, text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                                           0.0), pos=(0.01,
                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                      0.155))
        self.myGold = DirectFrame(parent=self.cartFrame, relief=None, text=str(localAvatar.getMoney()), text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(-0.055, 0.0), textMayChange=1, image=StoreGUI.CoinImage, image_scale=0.15, image_pos=(-0.025,
                                                                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                                                                    0.025), pos=(self.cartWidth, 0, 0.155))
        self.commitButton = GuiButton.GuiButton(command=self.handleCommitPurchase, parent=self.cartFrame, text=PLocalizer.PurchaseCommit, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0, -PiratesGuiGlobals.TextScaleLarge * 0.25), text_scale=PiratesGuiGlobals.TextScaleLarge, pos=(self.width - 0.2, 0, 0.075))
        self.commitButton.setPos(self.cartWidth / 2, 0, 0.05)
        self.initTabs()
        self.updateBalance()
        self.accept('inventoryQuantity-%s-%s' % (base.localAvatar.getInventoryId(), InventoryType.GoldInPocket), self.updateBalance)
        self.accept(PiratesGuiGlobals.InventoryBuyEvent, self.handleBuyItem)
        self.acceptOnce('escape', self.closePanel)
        return

    def closePanel(self):
        messenger.send('exitStore')
        self.ignoreAll()

    def handleBuyItem(self, data, useCode):
        itemId = data[0]
        if not itemId:
            return
        data[1] = EconomyGlobals.getItemQuantity(itemId)
        inventory = base.localAvatar.getInventory()
        if not inventory:
            return
        itemQuantity = self.purchaseInventory.getItemQuantity(itemId)
        currStock = inventory.getStackQuantity(itemId)
        currStockLimit = inventory.getStackLimit(itemId)
        if useCode == PiratesGuiGlobals.InventoryAdd:
            itemType = EconomyGlobals.getItemType(itemId)
            itemTypeName = PLocalizer.InventoryItemClassNames.get(itemType)
            trainingReq = EconomyGlobals.getItemTrainingReq(itemId)
            if trainingReq:
                amt = inventory.getStackQuantity(trainingReq)
                if not amt:
                    base.localAvatar.guiMgr.createWarning(PLocalizer.NoTrainingWarning % itemTypeName, PiratesGuiGlobals.TextFG6)
                    return
            minLvl = EconomyGlobals.getItemMinLevel(itemId)
            repId = WeaponGlobals.getRepId(itemId)
            repAmt = inventory.getAccumulator(repId)
            if minLvl > ReputationGlobals.getLevelFromTotalReputation(repId, repAmt)[0]:
                base.localAvatar.guiMgr.createWarning(PLocalizer.LevelReqWarning % (minLvl, itemTypeName), PiratesGuiGlobals.TextFG6)
                return
            itemQuantity = self.purchaseInventory.getItemQuantity(itemId)
            currStock = inventory.getStackQuantity(itemId)
            currStockLimit = inventory.getStackLimit(itemId)
            itemCategory = EconomyGlobals.getItemCategory(itemId)
            if itemCategory == ItemType.WEAPON and itemQuantity >= 1:
                base.localAvatar.guiMgr.createWarning(PLocalizer.TradeItemFullWarning, PiratesGuiGlobals.TextFG6)
                return
            else:
                if itemCategory == ItemType.WEAPON and currStock >= 1:
                    base.localAvatar.guiMgr.createWarning(PLocalizer.AlreadyOwnWeaponWarning, PiratesGuiGlobals.TextFG6)
                    return
                else:
                    if currStock + itemQuantity >= currStockLimit:
                        base.localAvatar.guiMgr.createWarning(PLocalizer.TradeItemFullWarning, PiratesGuiGlobals.TextFG6)
                        return
            self.purchaseInventory.addPanel(data)
            self.purchaseInventory.inventory.append(data)
        else:
            if useCode == PiratesGuiGlobals.InventoryRemove:
                self.purchaseInventory.removePanel(data)
        panel = self.storeInventory.getPanel(data)
        if panel:
            self.checkPanel(panel, inventory, itemId)
        self.updateBalance()

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
        StoreGUI.notify.debug('Make Purchase - Buying: %s' % self.purchaseInventory.inventory)
        messenger.send('makeSale', [self.purchaseInventory.inventory, [], []])

    def updateBalance(self, extraArgs=None):
        self.myGold['text'] = str(localAvatar.getMoney())
        self.balance = 0
        for item in self.purchaseInventory.panels:
            self.balance += max(item.price, 1)

        if self.balance > 0:
            self.balanceTitle['text'] = PLocalizer.Total
            self.balanceValue['text'] = str(abs(self.balance))
        else:
            if self.balance < 0:
                self.balanceTitle['text'] = PLocalizer.Gain
                self.balanceValue['text'] = str(abs(self.balance))
            else:
                self.balanceTitle['text'] = PLocalizer.Total
                self.balanceValue['text'] = str(abs(self.balance))
        if self.balance > localAvatar.getMoney() or self.balance == 0:
            if self.balance > localAvatar.getMoney():
                self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG6
            self.commitButton['state'] = DGG.DISABLED
        else:
            self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG2
            self.commitButton['state'] = DGG.NORMAL
        inventory = base.localAvatar.getInventory()
        if inventory:
            if inventory.getStackQuantity(InventoryType.GoldInPocket) < self.balance or self.purchaseInventory.inventory == []:
                self.commitButton['frameColor'] = PiratesGuiGlobals.ButtonColor3
            else:
                self.commitButton['frameColor'] = PiratesGuiGlobals.ButtonColor4

    def checkPanel(self, panel, inventory, itemId):
        purchaseQty = self.purchaseInventory.getItemQuantity(itemId)
        panel.checkPlayerInventory(itemId, purchaseQty)

    def initTabs(self):
        self.tabBar = StoreTabBar(parent=self, backParent=self.backTabParent, frontParent=self.frontTabParent, offset=0)
        self.pageNames = []
        self.createTabs()
        if len(self.pageNames) > 0:
            self.setPage(self.pageNames[0])

    def createTabs(self):
        for item in self.inventory:
            if item == InventoryType.ShipRepairKit:
                if not base.config.GetBool('want-privateering', 0):
                    continue
            if not self.isPageAdded(getItemGroup(item)):
                self.addTab(getItemGroup(item), item)

    def addTab(self, itemGroup, item):
        newTab = self.tabBar.addTab(itemGroup, command=self.setPage, extraArgs=[itemGroup])
        repId = WeaponGlobals.getRepId(item)
        if repId:
            iconName = ReputationGlobals.RepIcons.get(repId)
            icon = StoreGUI.WeaponIcons.find('**/%s' % iconName)
        else:
            if InventoryType.begin_Consumables <= item < InventoryType.end_Consumables:
                iconName = EconomyGlobals.getItemIcons(item)
                if iconName == 'icon_cannon':
                    icon = StoreGUI.WeaponIcons.find('**/%s' % iconName)
                else:
                    icon = StoreGUI.SkillIcons.find('**/%s' % iconName)
            else:
                if InventoryType.begin_WeaponCannonAmmo <= item < InventoryType.end_WeaponCannonAmmo:
                    iconName = EconomyGlobals.getItemIcons(InventoryType.CannonL1)
                    icon = StoreGUI.WeaponIcons.find('**/%s' % iconName)
                else:
                    if InventoryType.begin_WeaponGrenadeAmmo <= item < InventoryType.end_WeaponGrenadeAmmo:
                        itemId = InventoryType.GrenadeWeaponL1
                        iconName = EconomyGlobals.getItemIcons(itemId)
                        icon = StoreGUI.WeaponIcons.find('**/%s' % iconName)
                    else:
                        icon = None
        newTab.nameTag = DirectLabel(parent=newTab, relief=None, state=DGG.DISABLED, image=icon, image_scale=0.4, image_pos=(0,
                                                                                                                             0,
                                                                                                                             0.04), pos=(0.06, 0, -0.035))
        self.pageNames.append(itemGroup)
        return

    def isPageAdded(self, pageName):
        return self.pageNames.count(pageName) > 0

    def setPage(self, pageName):
        self.tabBar.unstash()
        self.storeInventory.filterByItemGroup(pageName)
# okay decompiling .\pirates\economy\StoreGUI.pyc
