from direct.gui.DirectGui import *
from panda3d.core import *
from direct.task.Task import Task
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.battle import WeaponGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.battle import CannonGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.uberdog import UberDogGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.reputation import ReputationGlobals
from pirates.piratesgui.InventoryListItem import InventoryListItem
from pirates.piratesbase import Freebooter

class InventoryItemGui(InventoryListItem):
    width = PiratesGuiGlobals.InventoryItemGuiWidth
    height = PiratesGuiGlobals.InventoryItemGuiHeight
    available = True
    
    def __init__(self, data, trade = 0, buy = 0, sell = 0, use = 0, weapon = 0, isDisabled = 0, **kw):
        if (trade or buy or sell or use or weapon) and not isDisabled:
            buttonRelief = DGG.RAISED
            buttonState = DGG.NORMAL
        else:
            buttonRelief = DGG.RIDGE
            buttonState = DGG.DISABLED
        self.loadGui()
        optiondefs = (('relief', None, None),
                      ('state', buttonState, None),
                      ('frameSize', (0, self.width, 0, self.height), None),
                      ('image', InventoryItemGui.genericButton, None),
                      ('image_scale', (0.54, 1, 0.42), None),
                      ('image_pos', (0.26, 0, 0.08), None),
                      ('pressEffect', 0, None),
                      ('command', self.sendEvents, None)
                      )
        self.defineoptions(kw, optiondefs)
        InventoryListItem.__init__(self, data, trade = trade, buy = buy, sell = sell, use = use, weapon = weapon, isDisabled = isDisabled, width = self.width, height = self.height)
        self.initialiseoptions(InventoryItemGui)
        self.createGui()
        self.draggable = abs(self.buy) + abs(self.sell) + abs(self.use) + abs(self.trade) - 1
        if self.draggable > 0:
            self.bind(DGG.B1PRESS, self.dragStart)
            self.bind(DGG.B1RELEASE, self.dragStop)
            self.bind(DGG.B2PRESS, self.dragStart)
            self.bind(DGG.B2RELEASE, self.dragStop)
            self.bind(DGG.B3PRESS, self.dragStart)
            self.bind(DGG.B3RELEASE, self.dragStop)
        
        if self.weapon:
            self.bind(DGG.B1PRESS, self.equipWeapon)
            self.bind(DGG.B2PRESS, self.equipWeapon)
            self.bind(DGG.B3PRESS, self.equipWeapon)
        
        self.helpBox = None
        self.bind(DGG.ENTER, self.showDetails)
        self.bind(DGG.EXIT, self.hideDetails)

    def loadGui(self):
        if InventoryItemGui.guiLoaded:
            return
        
        InventoryListItem.loadGui(self)
        InventoryItemGui.parchmentImage = loader.loadModel('models/gui/panel_parchment')
        InventoryItemGui.genericButton = (InventoryListItem.topGui.find('**/generic_button'), InventoryListItem.topGui.find('**/generic_button_down'), InventoryListItem.topGui.find('**/generic_button_over'), InventoryListItem.topGui.find('**/generic_button_disabled'))

    def createGui(self):
        itemId = self.data[0]
        self.picture = DirectFrame(parent = self, relief = None, state = DGG.DISABLED, pos = (0.01, 0, 0.01))
        self.nameTag = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = self.name, text_scale = PiratesGuiGlobals.TextScaleSmall * PLocalizer.getHeadingScale(2), text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, pos = (0.16, 0, 0.105), text_font = PiratesGlobals.getInterfaceFont())
        if itemId in range(InventoryType.begin_PistolPouches, InventoryType.end_PistolPouches):
            self.itemTypeFormatted = PLocalizer.makeHeadingString(PLocalizer.InventoryItemClassNames.get(ItemType.PISTOL), 1)
        elif itemId in range(InventoryType.begin_DaggerPouches, InventoryType.end_DaggerPouches):
            self.itemTypeFormatted = PLocalizer.makeHeadingString(PLocalizer.InventoryItemClassNames.get(ItemType.DAGGER), 1)
        elif itemId in range(InventoryType.begin_GrenadePouches, InventoryType.end_GrenadePouches):
            self.itemTypeFormatted = PLocalizer.makeHeadingString(PLocalizer.GrenadeShort, 1)
        elif itemId in range(InventoryType.begin_CannonPouches, InventoryType.end_CannonPouches):
            self.itemTypeFormatted = PLocalizer.makeHeadingString(PLocalizer.ShipCannonShort, 1)
        else:
            self.itemTypeFormatted = PLocalizer.makeHeadingString(self.itemType, 1)
        self.itemTypeName = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = self.itemTypeFormatted, text_scale = PiratesGuiGlobals.TextScaleSmall, text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getInterfaceFont(), pos = (0.16, 0, 0.065))
        self.miscText = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = '', text_scale = PiratesGuiGlobals.TextScaleSmall, text_align = TextNode.ALeft, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.16, 0, 0.025))
        if self.minLvl > 0:
            repId = WeaponGlobals.getRepId(itemId)
            if repId:
                self.checkLevel(repId, self.minLvl)

        self.checkFreebooter(itemId, base.localAvatar.getDoId())
        trainingReq = EconomyGlobals.getItemTrainingReq(itemId)
        if trainingReq:
            self.checkTrainingReq(trainingReq)
        
        if EconomyGlobals.getItemCategory(itemId) == ItemType.AMMO:
            skillId = WeaponGlobals.getSkillIdForAmmoSkillId(itemId)
            self.checkSkillReq(skillId)
        
        if self.buy:
            self.checkPlayerInventory(itemId)
        
        self.costText = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, image = InventoryListItem.coinImage, image_scale = 0.12, image_pos = Vec3(-0.01, 0, 0.01), text = str(self.price), text_scale = PiratesGuiGlobals.TextScaleSmall, text_align = TextNode.ARight, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, text_pos = (-0.03, 0, 0), pos = (self.width - 0.035, 0, 0.105), text_font = PiratesGlobals.getInterfaceFont())
        if self.quantity and self.quantity > 1:
            self.quantityLabel = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = str(self.quantity), frameColor = (0, 0, 0, 1), frameSize = (-0.01, 0.02, -0.01, 0.025), text_scale = 0.0275, text_align = TextNode.ACenter, text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_wordwrap = 11, pos = (0.02, 0, 0.025), text_font = PiratesGlobals.getPirateBoldOutlineFont())
        
        itemClass = EconomyGlobals.getItemCategory(itemId)
        if itemClass == ItemType.WEAPON or itemClass == ItemType.POUCH:
            asset = EconomyGlobals.getItemIcons(itemId)
            if asset:
                self.picture['geom'] = InventoryItemGui.weaponIcons.find('**/%s*' % asset)
                self.picture['geom_scale'] = 0.11
                self.picture['geom_pos'] = (0.08, 0, 0.068)
            
        elif itemClass == ItemType.CONSUMABLE:
            asset = EconomyGlobals.getItemIcons(itemId)
            if asset:
                self.picture['geom'] = InventoryItemGui.skillIcons.find('**/%s*' % asset)
                self.picture['geom_scale'] = 0.11
                self.picture['geom_pos'] = (0.08, 0, 0.068)

        if InventoryType.begin_WeaponCannonAmmo <= itemId and itemId <= InventoryType.end_WeaponCannonAmmo or InventoryType.begin_WeaponPistolAmmo <= itemId and itemId <= InventoryType.end_WeaponGrenadeAmmo or InventoryType.begin_WeaponDaggerAmmo <= itemId and itemId <= InventoryType.end_WeaponDaggerAmmo:
            skillId = WeaponGlobals.getSkillIdForAmmoSkillId(itemId)
            if skillId:
                asset = WeaponGlobals.getSkillIcon(skillId)
                if asset:
                    self.picture['geom'] = InventoryListItem.skillIcons.find('**/%s' % asset)
                    self.picture['geom_scale'] = 0.15
                    self.picture['geom_pos'] = (0.069, 0, 0.069)

        elif InventoryType.SmallBottle <= itemId and itemId <= InventoryType.LargeBottle:
            self.picture['geom'] = InventoryListItem.topGui.find('**/main_gui_ship_bottle')
            self.picture['geom_scale'] = 0.1
            self.picture['geom_pos'] = (0.069, 0, 0.069)
            
        self.flattenStrong()
    
    def checkFreebooter(self, itemId, avId):
        itemClass = EconomyGlobals.getItemCategory(itemId)
        if itemClass == ItemType.CONSUMABLE:
            return
        
        if InventoryType.begin_WeaponCannonAmmo <= itemId and itemId <= InventoryType.end_WeaponCannonAmmo or InventoryType.begin_WeaponPistolAmmo <= itemId and itemId <= InventoryType.end_WeaponGrenadeAmmo or InventoryType.begin_WeaponDaggerAmmo <= itemId and itemId <= InventoryType.end_WeaponDaggerAmmo:
            return
            
        if not Freebooter.getPaidStatus(avId):
            self.highlightRed(PLocalizer.FreebooterDisallow)

    def checkLevel(self, repId, minLvl):
        inv = localAvatar.getInventory()
        if inv:
            repAmt = inv.getAccumulator(repId)
            if minLvl > ReputationGlobals.getLevelFromTotalReputation(repId, repAmt)[0]:
                self.highlightRed(PLocalizer.LevelRequirement % self.minLvl + ' ' + str(self.itemTypeFormatted))

    def checkTrainingReq(self, trainingReq):
        inv = localAvatar.getInventory()
        if inv:
            amt = inv.getStackQuantity(trainingReq)
            if not amt:
                self.highlightRed(PLocalizer.TrainingRequirement)

    def checkSkillReq(self, skillId):
        if skillId:
            if base.localAvatar.getSkillQuantity(skillId) < 2:
                skillName = PLocalizer.getInventoryTypeName(skillId)
                self.highlightRed(PLocalizer.SkillRequirement % skillName)

    def checkPlayerInventory(self, itemId, extraQty = 0):
        if self.available:
            itemCategory = EconomyGlobals.getItemCategory(itemId)
            inventory = base.localAvatar.getInventory()
            currStock = inventory.getStackQuantity(itemId)
            currStockLimit = inventory.getStackLimit(itemId)
            if itemCategory == ItemType.AMMO or itemCategory == ItemType.CONSUMABLE:
                if currStock + extraQty >= currStockLimit and currStockLimit > 0:
                    self.highlightGreen(PLocalizer.InventoryFull % currStockLimit)
                else:
                    self.highlightBox(PLocalizer.InventoryCurrent % (currStock + extraQty, currStockLimit), Vec4(1, 1, 1, 1), PiratesGuiGlobals.TextFG2)
            elif itemCategory == ItemType.WEAPON:
                if currStock >= 1:
                    self.highlightGreen(PLocalizer.InventoryOwned)
                else:
                    inv = base.localAvatar.getInventory()
                    if inv is None:
                        return
                    
                    itemRep = WeaponGlobals.getRepId(itemId)
                    if itemRep == InventoryType.CutlassRep:
                        options = [
                            InventoryType.CutlassWeaponL1,
                            InventoryType.CutlassWeaponL2,
                            InventoryType.CutlassWeaponL3,
                            InventoryType.CutlassWeaponL4,
                            InventoryType.CutlassWeaponL5,
                            InventoryType.CutlassWeaponL6]
                    elif itemRep == InventoryType.PistolRep:
                        options = [
                            InventoryType.PistolWeaponL1,
                            InventoryType.PistolWeaponL2,
                            InventoryType.PistolWeaponL3,
                            InventoryType.PistolWeaponL4,
                            InventoryType.PistolWeaponL5,
                            InventoryType.PistolWeaponL6]
                    elif itemRep == InventoryType.DaggerRep:
                        options = [
                            InventoryType.DaggerWeaponL1,
                            InventoryType.DaggerWeaponL2,
                            InventoryType.DaggerWeaponL3,
                            InventoryType.DaggerWeaponL4,
                            InventoryType.DaggerWeaponL5,
                            InventoryType.DaggerWeaponL6]
                    elif itemRep == InventoryType.GrenadeRep:
                        options = [
                            InventoryType.GrenadeWeaponL1,
                            InventoryType.GrenadeWeaponL2,
                            InventoryType.GrenadeWeaponL3,
                            InventoryType.GrenadeWeaponL4,
                            InventoryType.GrenadeWeaponL5,
                            InventoryType.GrenadeWeaponL6]
                    elif itemRep == InventoryType.DollRep:
                        options = [
                            InventoryType.DollWeaponL1,
                            InventoryType.DollWeaponL2,
                            InventoryType.DollWeaponL3,
                            InventoryType.DollWeaponL4,
                            InventoryType.DollWeaponL5,
                            InventoryType.DollWeaponL6]
                    elif itemRep == InventoryType.WandRep:
                        options = [
                            InventoryType.WandWeaponL1,
                            InventoryType.WandWeaponL2,
                            InventoryType.WandWeaponL3,
                            InventoryType.WandWeaponL4,
                            InventoryType.WandWeaponL5,
                            InventoryType.WandWeaponL6]
                    else:
                        return
                    for idx in range(len(options)):
                        optionId = options[idx]
                        if optionId == itemId:
                            currIdx = idx
                            for weaponId in options[currIdx:]:
                                if weaponId == itemId:
                                    continue
                                
                                stackAmt = inv.getStackQuantity(weaponId)
                                if stackAmt >= 1:
                                    self.highlightRed(PLocalizer.InventoryLowLevel)
                                    return
                    
            elif itemCategory == ItemType.POUCH:
                inv = base.localAvatar.getInventory()
                if currStock >= 1:
                    self.highlightGreen(PLocalizer.InventoryOwned)
                else:
                    pistolPouches = [
                        InventoryType.PistolPouchL1,
                        InventoryType.PistolPouchL2,
                        InventoryType.PistolPouchL3]
                    daggerPouches = [
                        InventoryType.DaggerPouchL1,
                        InventoryType.DaggerPouchL2,
                        InventoryType.DaggerPouchL3]
                    grenadePouches = [
                        InventoryType.GrenadePouchL1,
                        InventoryType.GrenadePouchL2,
                        InventoryType.GrenadePouchL3]
                    cannonPouches = [
                        InventoryType.CannonPouchL1,
                        InventoryType.CannonPouchL2,
                        InventoryType.CannonPouchL3]
                    if itemId in pistolPouches:
                        pouchSet = pistolPouches
                    elif itemId in daggerPouches:
                        pouchSet = daggerPouches
                    elif itemId in grenadePouches:
                        pouchSet = grenadePouches
                    elif itemId in cannonPouches:
                        pouchSet = cannonPouches
                    else:
                        pouchSet = []
                    for pouchIdx in range(len(pouchSet)):
                        if pouchSet[pouchIdx] == itemId and pouchIdx + 1 < len(pouchSet):
                            for higherPouchIdx in range(pouchIdx + 1, len(pouchSet)):
                                stackAmt = inv.getStackQuantity(pouchSet[higherPouchIdx])
                                if stackAmt >= 1:
                                    self.highlightRed(PLocalizer.InventoryLowLevel)
                                    return

    def highlightRed(self, text = ''):
        self['state'] = DGG.DISABLED
        self['image_color'] = Vec4(0.55, 0.55, 0.5, 1)
        self.available = False
        self.highlightBox(text, Vec4(0.75, 0.5, 0.5, 1), PiratesGuiGlobals.TextFG6)

    def highlightGreen(self, text = ''):
        self.highlightBox(text, Vec4(0.5, 0.75, 0.5, 1), PiratesGuiGlobals.TextFG4)

    def highlightBox(self, text, image_color, text_fg):
        self.miscText['text_fg'] = text_fg
        if text != '':
            self.miscText['text'] = text

    def enable(self):
        if self.available:
            self['state'] = DGG.NORMAL

    def disable(self):
        if self.available:
            self['state'] = DGG.DISABLED

    def createHelpbox(self, args = None):
        if self.helpBox:
            return
        
        weaponInfo = PLocalizer.WeaponDescriptions.get(self.data[0])
        weaponDesc = weaponInfo
        self.helpText = DirectFrame(parent = self, relief = None, text = weaponDesc, state = DGG.DISABLED, text_align = TextNode.ALeft, text_scale = PiratesGuiGlobals.TextScaleSmall, text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 13, textMayChange = 0, sortOrder = 91)
        height = -self.helpText.getHeight()
        self.helpBox = BorderFrame(parent = aspect2d, state = DGG.DISABLED, frameSize = (-0.03, 0.43, height, 0.05), sortOrder = 90, borderScale = 0.2)
        self.helpText.reparentTo(self.helpBox)
        self.helpBox.setBin('gui-popup', 0)
        self.helpBox.setPos(self, 0.25, 0, -0.035)

    def destroy(self):
        taskMgr.remove('helpInfoTask')
        taskMgr.remove(self.taskName('dragTask'))
        if self.helpBox:
            self.helpBox.destroy()
            self.helpBox = None
        
        del self.picture
        if self.weapon:
            taskMgr.remove(DGG.B1PRESS)
            taskMgr.remove(DGG.B2PRESS)
            taskMgr.remove(DGG.B3PRESS)
        
        InventoryListItem.destroy(self)
    
    def setDraggable(self, d):
        self.draggable = d
    
    def dragStart(self, event):
        self.origionalPos = self.getPos(render2d)
        self.origionalParent = self.getParent()
        self.bringToFront()
        self.setColorScale(1, 1, 1, 0.5)
        if self.draggable:
            self.wrtReparentTo(aspect2d)
            taskMgr.remove(self.taskName('dragTask'))
            vWidget2render2d = self.getPos(render2d)
            vMouse2render2d = Point3(event.getMouse()[0], 0, event.getMouse()[1])
            editVec = Vec3(vWidget2render2d - vMouse2render2d)
            task = taskMgr.add(self.dragTask, self.taskName('dragTask'))
            task.editVec = editVec

    def dragTask(self, task):
        if task.time < PiratesGuiGlobals.DragStartDelayTime:
            return Task.cont
        else:
            mwn = base.mouseWatcherNode
            if mwn.hasMouse():
                vMouse2render2d = Point3(mwn.getMouse()[0], 0, mwn.getMouse()[1])
                newPos = vMouse2render2d + task.editVec
                self.setPos(render2d, newPos)
                newPos = self.getPos(aspect2d)
                x = newPos[0]
                z = newPos[2]
                x = x - x % 0.05
                z = z - z % 0.05
                x = min(1.3 - self.width, max(-1.3, x))
                z = min(1 - self.height, max(-1, z))
                self.setPos(aspect2d, x, 0.0, z)
            
            return Task.cont

    def dragStop(self, event):
        self.clearColorScale()
        self.wrtReparentTo(self.origionalParent)
        self.setPos(render2d, self.origionalPos)
        if self.draggable:
            taskMgr.remove(self.taskName('dragTask'))

    def showDetails(self, event):
        taskMgr.doMethodLater(PiratesGuiGlobals.HelpPopupTime, self.createHelpbox, 'helpInfoTask')
        self.createHelpbox()

    def hideDetails(self, event):
        taskMgr.remove('helpInfoTask')
        if self.helpBox:
            self.helpBox.destroy()
            self.helpBox = None
        


