from direct.gui.DirectGui import *
from direct.task import Task
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryPage
from pirates.piratesgui import WeaponPanel
from pirates.piratesgui.SkillButton import SkillButton
from pirates.piratesgui import InventoryItemGui
from pirates.piratesgui import InventoryItemList
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.CombatTray import WeaponButton
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.battle import WeaponGlobals
from pirates.reputation import ReputationGlobals

class WeaponPage(InventoryPage.InventoryPage):
    
    def __init__(self):
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(WeaponPage)
        self.weaponPanels = {}
        self.tonicButtons = {}

    def show(self):
        InventoryPage.InventoryPage.show(self)

    def hide(self):
        self.equipStatus = 0
        InventoryPage.InventoryPage.hide(self)

    def tonicCallback(self, skillId):
        localAvatar.guiMgr.combatTray.trySkill(InventoryType.UseItem, skillId, 0)

    def rePanel(self, inventory):
        weapons = [
            (InventoryType.CutlassWeaponL1, InventoryType.CutlassWeaponL2, InventoryType.CutlassWeaponL3, InventoryType.CutlassWeaponL4, InventoryType.CutlassWeaponL5, InventoryType.CutlassWeaponL6),
            (InventoryType.PistolWeaponL1, InventoryType.PistolWeaponL2, InventoryType.PistolWeaponL3, InventoryType.PistolWeaponL4, InventoryType.PistolWeaponL5, InventoryType.PistolWeaponL6),
            (InventoryType.DollWeaponL1, InventoryType.DollWeaponL2, InventoryType.DollWeaponL3, InventoryType.DollWeaponL4, InventoryType.DollWeaponL5, InventoryType.DollWeaponL6),
            (InventoryType.DaggerWeaponL1, InventoryType.DaggerWeaponL2, InventoryType.DaggerWeaponL3, InventoryType.DaggerWeaponL4, InventoryType.DaggerWeaponL5, InventoryType.DaggerWeaponL6),
            (InventoryType.GrenadeWeaponL1, InventoryType.GrenadeWeaponL2, InventoryType.GrenadeWeaponL3, InventoryType.GrenadeWeaponL4, InventoryType.GrenadeWeaponL5, InventoryType.GrenadeWeaponL6),
            (InventoryType.WandWeaponL1, InventoryType.WandWeaponL2, InventoryType.WandWeaponL3, InventoryType.WandWeaponL4, InventoryType.WandWeaponL5, InventoryType.WandWeaponL6)]
        avWeapons = localAvatar.equippedWeapons
        for weaponList in weapons:
            quantity = 0
            weaponId = weaponList[0]
            for wid in weaponList:
                if wid in avWeapons:
                    weaponId = wid
                    quantity = 1
                    break
            
            key = WeaponGlobals.getWeaponKey(weaponId)
            if key:
                panel = WeaponPanel.WeaponPanel((weaponId, quantity), key)
                panel.reparentTo(self)
                panel.setZ(PiratesGuiGlobals.InventoryPanelHeight - 0.18 - key * panel.height)
                repCat = WeaponGlobals.getRepId(weaponId)
                self.weaponPanels[repCat] = panel
        
        items = inventory.getConsumables()
        for i in range(len(InventoryType.Potions) - 1):
            tonicId = InventoryType.Potions[i]
            if items.get(tonicId):
                button = SkillButton(tonicId, self.tonicCallback, items.get(tonicId), showQuantity = True, showHelp = True, showRing = True)
            else:
                button = SkillButton(tonicId, self.tonicCallback, 0, showQuantity = True, showHelp = True, showRing = True)
            button.skillButton['geom_scale'] = 0.1
            button.reparentTo(self)
            button.setPos(0.18 * i + 0.18, 0, 0.13)
            self.tonicButtons[tonicId] = button

    def refreshList(self, newWeaponId = None):
        for panel in self.weaponPanels.values():
            panel.destroy()
        
        for panel in self.tonicButtons.values():
            panel.destroy()
        
        inventory = localAvatar.getInventory()
        if inventory:
            if inventory.isReady():
                self.rePanel(inventory)
            else:
                self.ignore('inventoryReady-%s' % inventory.getDoId())
                self.acceptOnce('inventoryReady-%s' % inventory.getDoId(), self.rePanel)

    def destroy(self):
        InventoryPage.InventoryPage.destroy(self)
    
    def updateTonics(self):
        if not hasattr(base, 'localAvatar'):
            return
        
        inv = localAvatar.getInventory()
        if not inv:
            return
        
        items = inv.getConsumables()
        for i in range(len(InventoryType.Potions) - 1):
            tonicId = InventoryType.Potions[i]
            tonicAmt = inv.getStackQuantity(tonicId)
            if self.tonicButtons.has_key(tonicId):
                self.tonicButtons[tonicId].updateQuantity(tonicAmt)
                self.tonicButtons[tonicId].checkAmount()
        


