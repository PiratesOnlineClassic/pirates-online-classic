# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.SongListItem
from direct.gui.DirectGui import *
from direct.task.Task import Task
from panda3d.core import *
from pirates.battle import CannonGlobals, WeaponGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.reputation import ReputationGlobals
from pirates.uberdog import UberDogGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


class SongListItem(DirectButton):
    
    width = 0
    height = 0
    guiLoaded = False
    topGui = None
    genericButton = None
    parchmentImage = None
    coinImage = None
    weaponIcons = None
    skillIcons = None

    def __init__(self, data, trade=0, buy=0, sell=0, use=0, weapon=0, isDisabled=0, width=0, height=0):
        self.width = width
        self.height = height
        self.data = data
        self.trade = trade
        self.buy = buy
        self.sell = sell
        self.use = use
        self.weapon = weapon
        self.isDisabled = isDisabled
        DirectButton.__init__(self)
        self.loadGui()
        self.loadData()

    def destroyGui(self):
        pass

    def loadGui(self):
        if SongListItem.guiLoaded:
            return
        SongListItem.topGui = loader.loadModel('models/gui/toplevel_gui')
        SongListItem.coinImage = SongListItem.topGui.find('**/treasure_w_coin*')
        SongListItem.weaponIcons = loader.loadModel('models/textureCards/weapon_icons')
        SongListItem.skillIcons = loader.loadModel('models/textureCards/skillIcons')
        SongListItem.guiLoaded = True

    def loadData(self):
        itemId = self.data[0]
        if UberDogGlobals.InventoryId.isStackable(itemId):
            item, quantity = self.data
            name = PLocalizer.InventoryTypeNames.get(item)
            self.quantity = 1
            itemType = None
            itemTypeName = None
            self.price = 5
        else:
            category, doId = self.data
            name = PLocalizer.InventoryCategoryNames.get(category)
            self.quantity = 1
            itemTypeName = 'Object'
            self.price = 5
        if self.buy:
            self.price *= self.quantity
            self.price = int(self.price)
        self.name = PLocalizer.makeHeadingString(name, 2)
        self.itemType = itemTypeName
        self.minLvl = EconomyGlobals.getItemMinLevel(self.data[0])
        return

    def destroy(self):
        del self.data
        del self.weapon
        DirectButton.destroy(self)

    def getData(self):
        return self.data

    def sendEvents(self):
        if self.buy:
            messenger.send(PiratesGuiGlobals.InventoryBuyEvent, [
             self.data, self.buy])

    def bringToFront(self):
        self.reparentTo(self.getParent())

    def equipWeapon(self, event):
        if base.localAvatar.guiMgr.weaponPage.equipStatus > 0:
            base.localAvatar.guiMgr.weaponPage.equipWeapon(self.data[0])
# okay decompiling .\pirates\piratesgui\SongListItem.pyc
