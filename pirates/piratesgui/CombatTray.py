from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.reputation import ReputationGlobals
from pirates.piratesbase import PLocalizer
from pirates.battle import WeaponGlobals
from pirates.battle.EnemySkills import *
from direct.task import Task
from pirates.piratesgui import RadialMenu
from pirates.piratesbase import TeamUtils
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.effects.WispSpiral import WispSpiral
from pirates.battle import Wand
from pirates.pvp import DistributedPVPInstance
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.piratesbase import Freebooter
from direct.distributed.ClockDelta import *
import time
import math
import PiratesGuiGlobals
from SkillButton import SkillButton
from GuiTray import GuiTray
from GuiButton import GuiButton
import copy
from TonicsPanel import TonicsPanel
STAFF_INTERVAL = 0.4
AIM_ASSIST_DURATION = 2.0

class WeaponButton(GuiButton):
    notify = DirectNotifyGlobal.directNotify.newCategory('WeaponButton')
    
    def __init__(self, hotkeys = (), hotkeyLabel = None, helpText = None, parent = None, showQuant = 0, **kw):
        gui = loader.loadModel('models/gui/toplevel_gui')
        button_gui = loader.loadModel('models/textureCards/skillIcons')
        buttonImages = (button_gui.find('**/box_base'), button_gui.find('**/box_base_down'), button_gui.find('**/box_base_over'))
        buttonColors = ((1, 1, 1, 1), (0.8, 0.8, 0.8, 1), (1.0, 1.0, 1.0, 1), (0.6, 0.6, 0.6, 1))
        optiondefs = (('relief', None, None), ('state', 'normal', None), ('frameSize', (0, 0.12, 0, 0.12), None), ('image', buttonImages, None), ('image_scale', 0.13, None), ('image_pos', (0.06, 0, 0.06), None), ('extraArgs', [
            0], None))
        self.defineoptions(kw, optiondefs)
        GuiButton.__init__(self, hotkeys = hotkeys, hotkeyLabel = hotkeyLabel, helpText = helpText, parent = parent)
        self.initialiseoptions(WeaponButton)
        self.weaponId = 0
        self.category = 0
        self.card = None
        self.showQuant = showQuant
        self.quantLabel = None
        self.invReq = None
        self.weaponLeveledIval = None
        self.expGainIval = None
        self.lastLevel = None
        self.lastExp = None
        gui.removeNode()

    def refreshStock(self):
        if not self.weaponId:
            return
        
        inventory = localAvatar.getInventory()
        if inventory:
            numItems = inventory.getStackQuantity(self.weaponId)
            if numItems <= 0:
                pass
            elif self.showQuant and self.quantLabel:
                self.quantLabel['text'] = str(numItems)

    def setWeaponId(self, weaponId):
        self.weaponId = weaponId
        if not self.invReq:
            self.invReq = DistributedInventoryBase.getInventory(localAvatar.getInventoryId(), self.initInventory)

    def initInventory(self, inventory):
        self.invReq = None
        if not inventory:
            self.notify.warning('Could not get inventory for setWeaponid: %s' % self.weaponId)
            return None
        
        numItems = inventory.getStackQuantity(self.weaponId)
        if numItems <= 0:
            self.weaponId = 0
        
        if not self.weaponId:
            return None
        
        if self.isEmpty():
            return None
        
        self.category = WeaponGlobals.getRepId(self.weaponId)
        card = loader.loadModel('models/textureCards/weapon_icons')
        gui = None
        if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
            if not Freebooter.allowedFreebooterWeapon(self.category):
                if EconomyGlobals.getItemCategory(self.weaponId) == ItemType.WEAPON:
                    gui = loader.loadModel('models/gui/toplevel_gui')

        if gui:
            self['geom'] = gui.find('**/subscribers_lock')
            self['geom_scale'] = 0.2
            self['geom_pos'] = (0.06, 0, 0.06)
            gui.removeNode()
        else:
            asset = EconomyGlobals.getItemIcons(self.weaponId)
            if asset:
                self['geom'] = card.find('**/%s' % asset)
                self['geom_scale'] = 0.1
                self['geom_pos'] = (0.06, 0, 0.06)
            
        if numItems > 0 and self.showQuant:
            self.quantLabel = DirectLabel(parent = self, relief = None, state = DGG.DISABLED, text = str(numItems), text_font = PiratesGlobals.getPirateBoldOutlineFont(), text_align = TextNode.ACenter, text_scale = PiratesGuiGlobals.TextScaleSmall, text_pos = (0.06, 0.053), text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, textMayChange = 1)
        
        if EconomyGlobals.getItemCategory(self.weaponId) == ItemType.WEAPON:
            repValue = inventory.getReputation(self.category)
            self.updateRep(repValue)
        
        card.removeNode()

    def destroy(self):
        self.linkedCannon = 0
        if self.invReq:
            DistributedInventoryBase.cancelGetInventory(self.invReq)
            self.invReq = None
        
        if self.weaponLeveledIval:
            self.weaponLeveledIval.finish()
            self.weaponLeveledIval = None
        
        if self.expGainIval:
            self.expGainIval.finish()
            self.expGainIval = None
        
        GuiButton.destroy(self)

    def updateRep(self, value):
        (level, leftoverValue) = ReputationGlobals.getLevelFromTotalReputation(self.category, value)
        max = ReputationGlobals.getReputationNeededToLevel(self.category, level)
        if self.lastLevel == None or self.lastExp == None:
            self.lastLevel = level
            self.lastExp = localAvatar.getInventory().getReputation(self.category)
            return None
        
        if self.lastExp:
            expChange = value - self.lastExp
            if expChange:
                localAvatar.guiMgr.gameGui.createExpAlert(expChange, 4.0, Vec3(0.625, 0.0, -0.8), Vec3(0.0, 0.0, 0.25))

        if self.weaponLeveledIval:
            self.weaponLeveledIval.finish()
            self.weaponLeveledIval = None
        
        if self.expGainIval:
            self.expGainIval.finish()
            self.expGainIval = None
        
        if self.lastLevel != level:
            glowColor = Vec4(0.2, 0.2, 0.75, 1.0)
            glowObj = self
            startColor = Vec4(1, 1, 1, 1)
            startPos = self.getPos()
            movePos = startPos + Point3(0, 0, 0.015)
            self.weaponLeveledIval = Sequence(Parallel(LerpPosInterval(self, 0.2, movePos, startPos), LerpColorScaleInterval(glowObj, 0.2, glowColor, startColor, blendType = 'easeInOut')), Wait(0.4), Parallel(LerpColorScaleInterval(glowObj, 3, startColor, blendType = 'easeInOut'), Sequence(LerpPosInterval(self, 0.085, startPos, movePos), LerpPosInterval(self, 0.06, movePos - Point3(0.0, 0.0, 0.005), startPos), LerpPosInterval(self, 0.035, startPos, movePos - Point3(0.0, 0.0, 0.005)))))
            self.weaponLeveledIval.start()
        elif self.lastExp != value:
            glowColor = Vec4(0.15, 0.15, 0.6, 1.0)
            glowObj = self
            startColor = Vec4(1, 1, 1, 1)
            startPos = self.getPos()
            movePos = startPos + Point3(0, 0, 0.01)
            self.expGainIval = Sequence(Parallel(LerpPosInterval(self, 0.1, movePos, startPos), LerpColorScaleInterval(glowObj, 0.1, glowColor, startColor, blendType = 'easeInOut')), Wait(0.1), Parallel(LerpColorScaleInterval(glowObj, 1, startColor, glowColor, blendType = 'easeInOut'), Sequence(LerpPosInterval(self, 0.085, startPos, movePos), LerpPosInterval(self, 0.06, movePos - Point3(0.0, 0.0, 0.005), startPos), LerpPosInterval(self, 0.035, startPos, movePos - Point3(0.0, 0.0, 0.005)))))
            self.expGainIval.start()
        
        self.lastExp = value
        self.lastLevel = level



class TonicButton(SkillButton):
    notify = DirectNotifyGlobal.directNotify.newCategory('TonicButton')
    
    def __init__(self):
        SkillButton.__init__(self, InventoryType.Potion1, self.callback, 0, 0, showQuantity = True, showHelp = False, showRing = True, hotkey = 'T')
        self.skillButton['geom_scale'] = 0.1
        self.invReq = None
        self._buttonDisabled = False
        self._hotkeysEnabled = True
        self.enableHotkeys(self.skillId)

    def enableHotkeys(self, skillId = None):
        if skillId:
            skillId = self.skillId
        
        self._hotkeySkillId = skillId
        self._hotkeysEnabled = True
        if not self._buttonDisabled:
            self._enableHotkeys()
    
    def disableHotkeys(self):
        self._hotKeysEnabled = False
        if not self._buttonDisabled:
            self._disableHotkeys()
    
    def disableButton(self):
        self._buttonDisabled = True
        if self._hotkeysEnabled:
            self._disableHotkeys()

    def enableButton(self):
        self._buttonDisabled = False
        if self._hotkeysEnabled:
            self._enableHotkeys()

    def _enableHotkeys(self):
        self.accept('t', self.callback, [
            self._hotkeySkillId])
        self.accept('shift-t', self.callback, [
            self._hotkeySkillId])

    def _disableHotkeys(self):
        self.ignore('t')
        self.ignore('shift-t')

    def callback(self, skillId):
        localAvatar.guiMgr.combatTray.trySkill(InventoryType.UseItem, skillId, 0)

    def updateBestTonic(self):
        if not self.invReq and localAvatar.getInventoryId():
            self.invReq = DistributedInventoryBase.getInventory(localAvatar.getInventoryId(), self.initInventory)
    
    def getBestTonic(self):
        inv = localAvatar.getInventory()
        if inv and inv.isReady():
            tonics = inv.getTonics()
            if tonics.get(InventoryType.PorkChunk) > 0:
                return InventoryType.PorkChunk
            
            idealAmount = max(0, localAvatar.getMaxHp() * 0.8 - localAvatar.getHp())
            bestTonicId = InventoryType.Potion1
            for (tonicId, count) in sorted(tonics.iteritems()):
                if count:
                    bestTonicId = tonicId
                    if WeaponGlobals.getAttackSelfHP(tonicId) > idealAmount:
                        break

            return bestTonicId
        
        return InventoryType.Potion1
    
    def initInventory(self, inventory):
        self.invReq = None
        if not inventory:
            self.notify.warning('Could not get inventory for setTonicid: %s' % self.skillId)
            return None
        
        oldTonic = self.skillId
        newTonic = self.getBestTonic()
        quantity = inventory.getStackQuantity(newTonic)
        self.updateQuantity(quantity)
        if newTonic == oldTonic:
            return None
        
        self.updateSkillId(newTonic)
        if hasattr(self, 'skillRingIval'):
            if self.skillRingIval.isPlaying():
                self.setGeomColor(0.5, 0.5, 0.5, 1.0)

        self.disableHotkeys()
        self.enableHotkeys(newTonic)
        self.skillButton['geom_scale'] = 0.1
    
    def destroy(self):
        self.enableButton()
        self.disableHotkeys()
        if self.invReq:
            DistributedInventoryBase.cancelGetInventory(self.invReq)
            self.invReq = None
        
        SkillButton.destroy(self)



class ShipRepairButton(SkillButton):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipRepairButton')
    
    def __init__(self):
        self._skillIconName = 'sail_come_about'
        self._skillId = InventoryType.ShipRepairKit
        SkillButton.__init__(self, self._skillId, self.callback, 0, 0, showQuantity = True, showHelp = False, showRing = True, hotkey = 'T')
        self.skillButton['geom_scale'] = 0.1
        self.invReq = None
        self._buttonDisabled = False
        self._hotkeysEnabled = True
        self.enableHotkeys()
        self._ignoredAmountUpdates = 0
        self.accept('inventoryQuantity-%s-%s' % (localAvatar.getInventoryId(), self._skillId), self._inventoryQuantityChanged)
        self._updateAmount()
    
    def destroy(self):
        self.enableButton()
        self.disableHotkeys()
        if self.invReq:
            DistributedInventoryBase.cancelGetInventory(self.invReq)
            self.invReq = None
        
        SkillButton.destroy(self)
    
    def enableHotkeys(self):
        self._hotkeysEnabled = True
        if not self._buttonDisabled:
            self._enableHotkeys()

    def disableHotkeys(self):
        self._hotKeysEnabled = False
        if not self._buttonDisabled:
            self._disableHotkeys()

    def disableButton(self):
        self._buttonDisabled = True
        if self._hotkeysEnabled:
            self._disableHotkeys()

    def enableButton(self):
        self._buttonDisabled = False
        if self._hotkeysEnabled:
            self._enableHotkeys()

    def _enableHotkeys(self):
        self.accept('t', self.callback, [
            InventoryType.ShipRepairKit])
        self.accept('shift-t', self.callback, [
            InventoryType.ShipRepairKit])

    def _disableHotkeys(self):
        self.ignore('t')
        self.ignore('shift-t')

    def _updateAmount(self):
        if not self.invReq:
            self.invReq = DistributedInventoryBase.getInventory(localAvatar.getInventoryId(), self._gotInventory)

    def _gotInventory(self, inventory):
        self.invReq = None
        if not inventory:
            self._updateAmount()
            return None
        
        self.updateQuantity(inventory.getStackQuantity(self._skillId))

    def updateQuantity(self, quantity):
        SkillButton.updateQuantity(self, quantity)
        self.updateSkillId(self._skillId)
        if hasattr(self, 'skillRingIval') and self.skillRingIval:
            if self.skillRingIval.isPlaying():
                self.setGeomColor(0.5, 0.5, 0.5, 1.0)

    def _inventoryQuantityChanged(self, amount):
        if self._ignoredAmountUpdates > 0:
            self._ignoredAmountUpdates -= 1
        else:
            self.updateQuantity(amount)

    def callback(self, skillId):
        if localAvatar.guiMgr.combatTray.trySkill(InventoryType.UseItem, skillId, 0):
            self._ignoredAmountUpdates += 1
            self.updateQuantity(self.quantity - 1)
        



class CombatTray(GuiTray):
    notify = DirectNotifyGlobal.directNotify.newCategory('CombatTray')
    InstantCast = base.config.GetBool('instant-cast', 0)
    WeaponButtonPositions = ((-0.55, 0, 0.02),)
    SkillButtonEvents = ('attack', 'mouse2', 'attack-up')
    COMBO_WINDOW_START = 0.3
    COMBO_WINDOW_END = 1.0
    RECOVERY_TIME = 0.75
    WINDOW_LENGTH = 0.4
    BUTTON_MASH_WINDOW = 1.3
    BASIC_ATTACKS = (InventoryType.CutlassHack, InventoryType.PistolShoot, InventoryType.MusketShoot, InventoryType.MeleePunch, InventoryType.DaggerCut, InventoryType.GrenadeThrow, InventoryType.StaffBlast, InventoryType.DollAttune, InventoryType.DollPoke)
    IGNORES_INPUT_LOCK = (InventoryType.UseItem, EnemySkills.PISTOL_RELOAD, EnemySkills.GRENADE_RELOAD)
    NO_PRINT_RANGE = (InventoryType.UseItem, EnemySkills.PISTOL_RELOAD, EnemySkills.PISTOL_CHARGE, EnemySkills.GRENADE_RELOAD, EnemySkills.GRENADE_CHARGE, EnemySkills.STAFF_FIZZLE, EnemySkills.STAFF_WITHER_CHARGE, EnemySkills.STAFF_SOULFLAY_CHARGE, EnemySkills.STAFF_PESTILENCE_CHARGE, EnemySkills.STAFF_HELLFIRE_CHARGE, EnemySkills.STAFF_BANISH_CHARGE, EnemySkills.STAFF_DESOLATION_CHARGE, EnemySkills.LEFT_BROADSIDE, EnemySkills.RIGHT_BROADSIDE, EnemySkills.DOLL_UNATTUNE, InventoryType.CutlassHack, InventoryType.CutlassSlash, InventoryType.CutlassCleave, InventoryType.CutlassFlourish, InventoryType.CutlassStab, InventoryType.DaggerCut, InventoryType.DaggerSwipe, InventoryType.DaggerGouge, InventoryType.DaggerEviscerate)
    L1_COMBO_ATTACKS = (InventoryType.CutlassHack, InventoryType.DaggerCut)
    NO_VOLLEY_PROJECTILES = (EnemySkills.STAFF_WITHER_CHARGE, EnemySkills.STAFF_SOULFLAY_CHARGE, EnemySkills.STAFF_HELLFIRE_CHARGE, EnemySkills.STAFF_PESTILENCE_CHARGE, EnemySkills.STAFF_BANISH_CHARGE, EnemySkills.STAFF_DESOLATION_CHARGE, EnemySkills.PISTOL_CHARGE, EnemySkills.PISTOL_RELOAD, EnemySkills.GRENADE_CHARGE, EnemySkills.GRENADE_RELOAD, InventoryType.UseItem)
    
    def __init__(self, parent, **kw):
        optiondefs = (('relief', None, None),)
        self.defineoptions(kw, optiondefs)
        GuiTray.__init__(self, parent, 0.36, 0.12)
        self.initialiseoptions(CombatTray)
        self.CHARGE_MODE_TIME_THRESHOLD = 0.3
        self.thresholdHit = 0
        self.aimAssistTarget = None
        self.skillTray = RadialMenu.SkillTray()
        self.skillsHidden = 1
        self.weaponId = 0
        self.rep = 0
        self.numberOfItems = -1
        self.ammoSkillId = 0
        self.lastAmmoSkillId = {}
        self.lastAttack = ()
        self.chargeTime = 0
        self.maxCharge = 0
        self.tryShoot = 0
        self.volley = 0
        self.linkedCannon = 0
        self.weaponMode = 0
        self.weaponIds = []
        self.weaponButtons = {}
        self.tonicButton = None
        self.shipRepairButton = None
        self.skillIds = []
        self.skillFrame = None
        self.comboReady = 0
        self.comboLevel = 0
        self.combatChainLvl = 0
        self.missedTime = 0
        self.skillQueue = None
        self.weaponQueue = None
        self.isUsingSkill = 0
        self.isDrawingWeapon = 0
        self.isCharging = 0
        self.isAcceptingInput = 0
        self.isMouseMode = 0
        self.isEnabled = 0
        self.activeReload = 0
        self.invReq = None
        self.taskTime = 0
        self.card = loader.loadModel('models/textureCards/skillIcons')
        self.chargeCard = loader.loadModel('models/textureCards/chargeMeter')
        self.reloadFrame = DirectFrame(parent = base.a2dBottomCenter, relief = None, state = DGG.DISABLED, image = self.card.find('**/base'), image_scale = 0.12, image_pos = (0, 0, 0.02), pos = (-0.07, 0, 0.3))
        self.reloadFrame.hide()
        self.chargeMeter = DirectLabel(parent = base.a2dBottomCenter, relief = None, state = DGG.DISABLED, frameColor = (1, 1, 1, 1), pos = (0.45, 0, 0.2), image = self.chargeCard.find('**/distance_meter'), image_scale = (0.06, 0, 0.6), image_pos = (-0.012, 0, 0.3))
        self.chargeMeter.setTransparency(1)
        self.chargeMeterBar = DirectWaitBar(parent = self.chargeMeter, relief = DGG.FLAT, state = DGG.DISABLED, range = 100, value = 0, frameColor = (0, 0, 0, 1), barColor = (1, 0.2, 0.1, 1), pos = (-0.005, 0, 0.01), hpr = (0, 0, -90), frameSize = (0, 0.583, 0, 0.014))
        self.chargeMeter.hide()
        self.activeName = DirectLabel(parent = self.reloadFrame, relief = None, state = DGG.DISABLED, text = PLocalizer.UsingSkill, text_align = TextNode.ALeft, text_scale = 0.06, pos = (0.09, 0, 0.01), text_fg = PiratesGuiGlobals.TextFG2, text_shadow = PiratesGuiGlobals.TextShadow, text_font = PiratesGlobals.getPirateOutlineFont())
        self.skillFrame = DirectFrame(parent = self.reloadFrame, relief = None, state = DGG.DISABLED, image = self.card.find('**/cutlass_sweep'), image_scale = 0.12, sortOrder = 20, image_pos = (0, 0, 0.02))
        self.skillFrame.setTransparency(1)
        self.skillMapping = {}
        self.chargeCard.removeNode()
        self.chargeCard = None
        self.accept('drawStarted', self.setDrawWeapon, [1])
        self.accept('drawFinished', self.setDrawWeapon, [0])
        self.actionPressed = False
        self.accept('control', self.actionDown)
        self.accept('control-up', self.actionUp)
        self.accept('mouse1', self.actionDown)
        self.accept('mouse1-up', self.actionUp)

    def destroy(self):
        self.ignoreAll()
        if self.invReq:
            DistributedInventoryBase.cancelGetInventory(self.invReq)
            self.invReq = None
        
        if self.reloadFrame:
            self.reloadFrame.destroy()
            self.reloadFrame = None
        
        self._destroyShipRepairButton()
        taskMgr.remove(self.getResetComboName())
        taskMgr.remove(self.getComboRecoveryName())
        self.skillTray.destroy()
        taskMgr.remove('buttonCharging')
        taskMgr.remove('comboReadyTimer')
        taskMgr.remove('skillFinishedTimer')
        self.weaponIds = None
        if self.weaponButtons:
            for button in self.weaponButtons.values():
                button.destroy()

        self.weaponButtons = None
        self.skillIds = None
        GuiTray.destroy(self)
    
    def setAmmoSkillId(self, ammoSkillId):
        self.endButtonCharge()
        self.ammoSkillId = ammoSkillId
        if localAvatar.currentWeaponId:
            self.lastAmmoSkillId[localAvatar.currentWeaponId] = ammoSkillId

    def refreshList(self):
        for button in self.weaponButtons.values():
            button.refreshStock()

    def toggleWeapon(self, weaponId, args = None, fromWheel = 0):
        if localAvatar.guiMgr.ignoreAllKeys:
            return
        
        if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
            category = WeaponGlobals.getRepId(weaponId)
            if not Freebooter.allowedFreebooterWeapon(category):
                base.localAvatar.guiMgr.showNonPayer(quest = 'Restricted_Weapon_Selection', focus = 5)
                return
        
        state = localAvatar.getGameState()
        if state in ('Spawn', 'Stunned', 'Death', 'WaterRoam', 'WaterTreasureRoam', 'Cutscene', 'MakeAPirate', 'TeleportOut', 'TeleportIn', 'ParlorGame', 'NPCInteract', 'ShipBoarding', 'Ensnared', 'Thrown', 'Knockdown', 'Unconcious', 'ThrownInJail', 'DoorKicking', 'EnterTunnel', 'LeaveTunnel', 'PVPWait'):
            return
        
        if self.isMouseMode:
            return
        
        if not weaponId:
            localAvatar.guiMgr.createWarning(PLocalizer.NothingEquippedWarning, PiratesGuiGlobals.TextFG6)
            return
        
        if self.isDrawingWeapon or self.isUsingSkill or self.isCharging:
            if localAvatar.currentWeaponId != weaponId:
                self.weaponQueue = weaponId
                self.skillQueue = 0
            
            return
        
        if fromWheel and weaponId == localAvatar.currentWeaponId:
            self.skillTray.showSkillTray()
            return
        
        if EconomyGlobals.getItemCategory(weaponId) == ItemType.CONSUMABLE:
            self.trySkill(InventoryType.UseItem, weaponId, 0)
        else:
            self.weaponId = weaponId
            self.rep = WeaponGlobals.getRepId(self.weaponId)
            localAvatar.toggleWeapon(weaponId, fromWheel)

    def toggleNextWeapon(self):
        rep = WeaponGlobals.getRepId(self.weaponId)
        if rep != InventoryType.SailingRep and rep != InventoryType.CannonRep:
            localAvatar.guiMgr.barSelection.selectNext()
            self.skillTray.hideSkillTray()

    def togglePrevWeapon(self):
        rep = WeaponGlobals.getRepId(self.weaponId)
        if rep != InventoryType.SailingRep and rep != InventoryType.CannonRep:
            localAvatar.guiMgr.barSelection.selectPrev()
            self.skillTray.hideSkillTray()

    def cleanupEquippedWeapons(self):
        for weaponId in self.weaponIds:
            key = WeaponGlobals.getWeaponKey(weaponId)
            if key:
                hotkey = 'f%s' % key
                self.ignore(hotkey)

    def setEquippedWeapons(self, weaponIds):
        if weaponIds == [0, 0, 0, 0, 0, 0]:
            weaponIds = [
                InventoryType.MeleeWeaponL1]
        
        self.weaponIds = weaponIds
        for weaponId in weaponIds:
            key = WeaponGlobals.getWeaponKey(weaponId)
            if key:
                hotkey = 'f%s' % key
                self.ignore(hotkey)
                self.accept(hotkey, self.toggleWeapon, [weaponId])
        
        if not self.skillsHidden:
            self.acceptInput()

    def setCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        for weaponButton in self.weaponButtons.values():
            weaponButton.destroy()
        
        self.weaponButtons = {}
        self.weaponMode = WeaponGlobals.getWeaponCategory(currentWeaponId)
        self.resetComboLevel()
        self.combatChainLvl = 0
        showQuant = 0
        weaponButton = WeaponButton(parent = self, scale = 1.1, command = self.toggleWeapon, showQuant = showQuant)
        weaponButton.setWeaponId(currentWeaponId)
        weaponButton['extraArgs'] = [
            currentWeaponId]
        weaponButton.setPos(*self.WeaponButtonPositions[0])
        self.weaponButtons[0] = weaponButton
        if currentWeaponId and not self.skillsHidden:
            self.acceptInput()
        
        repId = WeaponGlobals.getRepId(currentWeaponId)
        if currentWeaponId and isWeaponDrawn:
            if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                if Freebooter.allowedFreebooterWeapon(self.rep):
                    if EconomyGlobals.getItemCategory(currentWeaponId) == ItemType.WEAPON:
                        self.skillTray.updateSkillTray(repId, self.weaponMode, self.__skillTrayCallback)

            else:
                self.skillTray.updateSkillTray(repId, self.weaponMode, self.__skillTrayCallback)
        
        messenger.send('weaponChange')
    
    def updateBestTonic(self, tonicId = None):
        self._createTonicButton()
        self.tonicButton.updateBestTonic()
        self.tonicButton.checkAmount()

    def _createTonicButton(self):
        if not self.tonicButton:
            self.tonicButton = TonicButton()
            self.tonicButton.reparentTo(self)
            self.tonicButton.setPos(-0.64, 0, 0.08)

    def _destroyTonicButton(self):
        if self.tonicButton:
            self.tonicButton.destroy()
            self.tonicButton = None
    
    def enableShipRepair(self):
        self._createShipRepairButton()
        self._showRepairButton()
        self.shipRepairButton.checkAmount()
    
    def disableShipRepair(self):
        self._hideRepairButton()
        self._destroyShipRepairButton()

    def updateShipRepairKits(self):
        if self.shipRepairButton:
            self.shipRepairButton.checkAmount()
    
    def _createShipRepairButton(self):
        if not self.shipRepairButton:
            self.shipRepairButton = ShipRepairButton()
            self.shipRepairButton.detachNode()
            self.shipRepairButton.setPos(-0.64, 0, 0.08)

    def _destroyShipRepairButton(self):
        if self.shipRepairButton:
            self.shipRepairButton.destroy()
            self.shipRepairButton = None

    def _showRepairButton(self):
        self.tonicButton.disableButton()
        self.tonicButton.detachNode()
        self.shipRepairButton.reparentTo(self)
        self.shipRepairButton.enableButton()

    def _hideRepairButton(self):
        self.shipRepairButton.disableButton()
        self.shipRepairButton.detachNode()
        self.tonicButton.reparentTo(self)
        self.tonicButton.enableButton()
    
    def triggerInputLock(self):
        self.isUsingSkill = 1
    
    def setDrawWeapon(self, value):
        self.isDrawingWeapon = value
        self.triggerWeaponQueue()
    
    def initCombatTray(self, rep = None):
        self.isEnabled = 1
        self.aimAssistTarget = None
        self.accept('skillStarted', self.triggerInputLock)
        self.accept('skillFinished', self.triggerSkillQueue)
        self.accept('reloadFinished', self.finishReload)
        self.skillMapping.clear()
        self.reloadFrame.hide()
        self.endButtonCharge()
        leftSkills = []
        rightSkills = []
        localAvatar.skillDiary.continueRecharging(InventoryType.UseItem)
        self.accept('inventoryChanged-%s' % localAvatar.getInventoryId(), self.refreshList)
        self.weaponMode = WeaponGlobals.getWeaponCategory(localAvatar.currentWeaponId)
        if (rep == None or rep == 0) and self.rep == 0:
            self.rep = InventoryType.MeleeRep
            leftSkills = [
                InventoryType.MeleePunch]
            self.weaponMode = WeaponGlobals.COMBAT
        elif rep:
            self.rep = rep
            leftSkills = RadialMenu.ComboSkills(self.rep, 2)
            rightSkills = RadialMenu.ActiveSkills(self.rep, 2)
        else:
            leftSkills = RadialMenu.ComboSkills(self.rep, 2)
            rightSkills = RadialMenu.ActiveSkills(self.rep, 2)
        if self.rep == InventoryType.SailingRep:
            self.weaponMode = WeaponGlobals.SAILING
        elif self.rep == InventoryType.CannonRep:
            self.weaponMode = WeaponGlobals.CANNON
        
        if len(leftSkills):
            self.skillMapping['action'] = leftSkills
            for skillId in leftSkills:
                localAvatar.skillDiary.continueRecharging(skillId)

        if len(rightSkills):
            self.skillMapping['mouse2'] = rightSkills
            for skillId in rightSkills:
                localAvatar.skillDiary.continueRecharging(skillId)
            
            lastAmmo = self.lastAmmoSkillId.get(localAvatar.currentWeaponId, rightSkills[0])
            self.ammoSkillId = lastAmmo
        
        allSkills = RadialMenu.getAllSkills(self.rep, 2)
        for i in range(len(allSkills)):
            (skillId, avail) = allSkills[i][:2]
            if avail:
                self.accept('%d' % (i + 1), self.triggerSkillTraySkill, [skillId])
        
        self.acceptInput()

    def equipWeapon(self, newWeaponId):
        pass

    def trySkill(self, skillId, ammoSkillId, combo = 0, charge = 0):
        if localAvatar.hp <= 0:
            return 0
        
        if not skillId:
            return 0
        
        if ammoSkillId in (InventoryType.Potion1, InventoryType.Potion2, InventoryType.Potion3, InventoryType.Potion4, InventoryType.Potion5):
            if localAvatar.getHp() == localAvatar.getMaxHp() and localAvatar.getMojo() == localAvatar.getMaxMojo():
                localAvatar.guiMgr.createWarning(PLocalizer.FullHealthWarning, PiratesGuiGlobals.TextFG6)
                return 0
        
        if ammoSkillId in (InventoryType.ShipRepairKit,) and hasattr(localAvatar, 'ship') and localAvatar.ship:
            if localAvatar.ship.getHp() == localAvatar.ship.getMaxHp() and localAvatar.ship.getSp() == localAvatar.ship.getMaxSp():
                localAvatar.guiMgr.createWarning(PLocalizer.FullShipHealthWarning, PiratesGuiGlobals.TextFG6)
                return 0
        
        if WeaponGlobals.getIsShipSkill(skillId) and not WeaponGlobals.getIsShout(skillId) and not (skillId == InventoryType.SailBroadsideLeft) and not (skillId == InventoryType.SailBroadsideRight):
            if localAvatar.ship:
                if not localAvatar.ship.sailsReady:
                    localAvatar.guiMgr.createWarning(PLocalizer.SailsNotReadyWarning, PiratesGuiGlobals.TextFG6)
                    return 0
                
            else:
                return 0
        
        if WeaponGlobals.getIsShipSkill(skillId):
            if localAvatar.ship:
                if skillId == InventoryType.SailRammingSpeed and localAvatar.ship.queryGameState() in 'InBoardingPosition':
                    localAvatar.guiMgr.createWarning(PLocalizer.RamWhileBoardingWarning, PiratesGuiGlobals.TextFG6)
                    return 0
                
                if localAvatar.ship.isRamming() and skillId != InventoryType.SailBroadsideLeft and skillId != InventoryType.SailBroadsideRight:
                    return 0
        
        if skillId not in self.IGNORES_INPUT_LOCK and not WeaponGlobals.getIsShipSkill(skillId):
            if not self.isAcceptingInput:
                return 0
            
            if not localAvatar.currentWeapon or not self.weaponId:
                return 0
            
            if localAvatar.getGameState() != 'Battle':
                return 0
            
            weaponVolley = WeaponGlobals.getWeaponVolley(localAvatar.currentWeaponId)
            if weaponVolley > 0 and self.volley >= weaponVolley:
                return 0
            
            skillRepCategory = WeaponGlobals.getSkillReputationCategoryId(skillId)
            if self.rep != skillRepCategory and skillRepCategory > 0:
                return 0
            
            if ammoSkillId:
                ammoRepCategory = WeaponGlobals.getSkillReputationCategoryId(ammoSkillId)
                if self.rep != ammoRepCategory and ammoRepCategory > 0:
                    return 0

        skillEffects = localAvatar.getSkillEffects()
        if WeaponGlobals.C_STUN in skillEffects:
            localAvatar.guiMgr.createWarning(PLocalizer.StunWarning, PiratesGuiGlobals.TextFG6)
            return 0
        
        if not WeaponGlobals.getIsInstantSkill(skillId, ammoSkillId):
            if self.isUsingSkill:
                if (self.weaponMode == WeaponGlobals.COMBAT or self.weaponMode == WeaponGlobals.THROWING) and skillId != EnemySkills.DOLL_UNATTUNE:
                    if not self.skillQueue and not self.weaponQueue:
                        self.skillQueue = (skillId, ammoSkillId, combo)

                return 0

        if WeaponGlobals.getNeedSight(skillId, ammoSkillId):
            inView = 0
            target = 0
            if self.aimAssistTarget:
                inView = localAvatar.checkViewingArc(self.aimAssistTarget)
            else:
                target = base.cr.targetMgr.takeAim(localAvatar, skillId, ammoSkillId)
                if target:
                    inView = localAvatar.checkViewingArc(target)

            if not inView and (target or self.aimAssistTarget):
                localAvatar.guiMgr.createWarning(PLocalizer.OutOfSightWarning, PiratesGuiGlobals.TextFG6)
                return 0

        rechargingTime = localAvatar.skillDiary.getTimeRemaining(skillId)
        if rechargingTime > 0:
            if skillId == InventoryType.UseItem:
                if ammoSkillId in InventoryType.Potions:
                    localAvatar.guiMgr.createWarning(PLocalizer.TonicRechargingWarning, PiratesGuiGlobals.TextFG6)
                elif ammoSkillId == InventoryType.ShipRepairKit:
                    localAvatar.guiMgr.createWarning(PLocalizer.RepairKitRechargingWarning, PiratesGuiGlobals.TextFG6)
                
            elif skillId not in self.BASIC_ATTACKS:
                localAvatar.guiMgr.createWarning(PLocalizer.SkillRechargingWarning, PiratesGuiGlobals.TextFG6)
            
            return 0
        
        if ammoSkillId:
            if not WeaponGlobals.isInfiniteAmmo(ammoSkillId):
                ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(ammoSkillId)
                inv = localAvatar.getInventory()
                if inv is None:
                    return 0
                
                amt = inv.getStackQuantity(ammoInvId)
                if amt < 1:
                    if EconomyGlobals.getItemCategory(ammoSkillId) == ItemType.AMMO:
                        localAvatar.guiMgr.createWarning(PLocalizer.OutOfAmmoWarning, PiratesGuiGlobals.TextFG6)
                    else:
                        localAvatar.guiMgr.createWarning(PLocalizer.OutOfItemWarning, PiratesGuiGlobals.TextFG6)
                    return 0

        if skillId:
            if not WeaponGlobals.isInfiniteAmmo(skillId):
                ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(skillId)
                inv = localAvatar.getInventory()
                if inv is None:
                    return 0
                
                amt = inv.getStackQuantity(ammoInvId)
                if amt < 1:
                    if EconomyGlobals.getItemCategory(skillId) == ItemType.AMMO:
                        localAvatar.guiMgr.createWarning(PLocalizer.OutOfAmmoWarning, PiratesGuiGlobals.TextFG6)
                    else:
                        localAvatar.guiMgr.createWarning(PLocalizer.OutOfItemWarning, PiratesGuiGlobals.TextFG6)
                    return 0

        cost = -1 * WeaponGlobals.getMojoCost(skillId)
        if localAvatar.mojo < cost and cost:
            localAvatar.guiMgr.createWarning(PLocalizer.NoManaWarning, PiratesGuiGlobals.TextFG6)
            return 0
        
        if localAvatar.isAirborne():
            if not WeaponGlobals.getUsableInAir(skillId, ammoSkillId):
                localAvatar.guiMgr.createWarning(PLocalizer.NotUsableInAirWarning, PiratesGuiGlobals.TextFG6)
                return 0

        if self.weaponMode == WeaponGlobals.STAFF and WeaponGlobals.getAttackMaxCharge(skillId):
            if self.chargeTime < self.maxCharge:
                localAvatar.guiMgr.createWarning(PLocalizer.SpellFailedWarning, PiratesGuiGlobals.TextFG6)
                return 0

        if skillId == InventoryType.SailBroadsideLeft or skillId == InventoryType.SailBroadsideRight:
            if localAvatar.ship and not (localAvatar.ship.broadside):
                localAvatar.guiMgr.createWarning(PLocalizer.NoBroadsidesWarning, PiratesGuiGlobals.TextFG6)
                return 0

        self.currentSkill = skillId
        if ammoSkillId and skillId != EnemySkills.PISTOL_RELOAD and skillId != EnemySkills.GRENADE_RELOAD:
            visSkillId = ammoSkillId
        else:
            visSkillId = skillId
        prevSkillId = 0
        time = 0
        if self.lastAttack:
            prevSkillId = self.lastAttack[0]
            time = globalClockDelta.localElapsedTime(self.lastAttack[1])
        
        if combo == -1:
            self.activeName['text'] = PLocalizer.Mistimed
        elif prevSkillId in self.L1_COMBO_ATTACKS and skillId == prevSkillId and time <= self.BUTTON_MASH_WINDOW:
            self.activeName['text'] = PLocalizer.Mistimed
        else:
            self.activeName['text'] = PLocalizer.InventoryTypeNames[visSkillId]
        if self.skillFrame:
            asset = RadialMenu.getSkillIconName(visSkillId, 0)
            tex = self.card.find('**/%s' % asset)
            self.skillFrame['image'] = tex
        
        allTargets = []
        if WeaponGlobals.getIsShipSkill(skillId):
            allTargets.append(localAvatar.ship)
        else:
            if localAvatar.currentTarget:
                allTargets.append(localAvatar.currentTarget)

            if WeaponGlobals.isAttackAreaSelfDamaging(skillId, ammoSkillId):
                allTargets.append(localAvatar)
        
        effectId = WeaponGlobals.getSkillEffectFlag(skillId)
        newPriority = WeaponGlobals.getBuffPriority(effectId)
        newCategory = WeaponGlobals.getBuffCategory(effectId)
        if newPriority:
            for target in allTargets:
                if isinstance(target, int):
                    continue
                
                for buffId in target.skillEffects:
                    priority = WeaponGlobals.getBuffPriority(buffId)
                    category = WeaponGlobals.getBuffCategory(buffId)
                    if newPriority < priority and category == newCategory:
                        localAvatar.guiMgr.createWarning(PLocalizer.BuffPriorityWarning, PiratesGuiGlobals.TextFG6)
                        return 0

        if not hasattr(base.cr, 'targetMgr'):
            return 0
        
        if localAvatar.hasStickyTargets() and skillId != InventoryType.DollAttune:
            target = localAvatar.currentTarget
        elif self.aimAssistTarget:
            target = self.aimAssistTarget
        else:
            target = base.cr.targetMgr.takeAim(localAvatar, skillId, ammoSkillId)
        if target:
            distance = target.getDistance(localAvatar)
            attackRange = base.cr.battleMgr.getModifiedAttackRange(localAvatar, skillId, ammoSkillId)
            if skillId not in self.NO_PRINT_RANGE:
                if distance > attackRange * 1.333:
                    localAvatar.guiMgr.createWarning(PLocalizer.OutOfRangeWarning, PiratesGuiGlobals.TextFG6)

            if target != localAvatar.currentTarget:
                if distance <= attackRange * 1.333:
                    target.requestInteraction(localAvatar.doId, interactType = PiratesGlobals.INTERACT_TYPE_HOSTILE)

            if skillId == InventoryType.DollAttune:
                if distance <= attackRange:
                    pass
                else:
                    localAvatar.guiMgr.createWarning(PLocalizer.TooFarAttuneWarning, PiratesGuiGlobals.TextFG6)
                    return 0
            
            backstab = 0
            if skillId in InventoryType.BackstabSkills:
                angle1 = localAvatar.getH()
                angle2 = target.getH()
                diff = abs(angle2 - angle1)
                if diff > 180:
                    diff = abs(diff - 360)
                
                if diff < WeaponGlobals.BACKSTAB_ANGLE:
                    self.chargeTime = 1
                    backstab = 1
                else:
                    self.chargeTime = 0
            
            self.comboLevel += 1
            if combo == -1:
                self.ignoreInput()
            else:
                self.acceptInput()
        elif localAvatar.currentTarget:
            localAvatar.setCurrentTarget(0)
        
        if self.weaponMode == WeaponGlobals.FIREARM or self.weaponMode == WeaponGlobals.GRENADE:
            if skillId not in self.NO_VOLLEY_PROJECTILES:
                self.volley += 1

        if self.skillTray.traySkillMap:
            if skillId in self.skillTray.traySkillMap:
                for i in range(len(self.skillTray.traySkillMap)):
                    if self.skillTray.traySkillMap[i] == skillId:
                        if self.skillTray.tray[i + 1].skillStatus:
                            self.skillTray.tray[i + 1].startRecharge()

        if ammoSkillId in InventoryType.Potions:
            self.tonicButton.startRecharge()
            inv = localAvatar.getInventory()
            if inv is None:
                return 0
            
            amt = inv.getStackQuantity(ammoSkillId)
            if localAvatar.guiMgr.weaponPage.tonicButtons.has_key(ammoSkillId):
                localAvatar.guiMgr.weaponPage.tonicButtons[ammoSkillId].updateQuantity(amt - 1)
            
            for skillButton in localAvatar.guiMgr.weaponPage.tonicButtons:
                if localAvatar.guiMgr.weaponPage.tonicButtons[skillButton].quantity > 0:
                    localAvatar.guiMgr.weaponPage.tonicButtons[skillButton].startRecharge()
                else:
                    localAvatar.guiMgr.weaponPage.tonicButtons[skillButton].checkAmount()

        if ammoSkillId in (InventoryType.ShipRepairKit,):
            self.shipRepairButton.startRecharge()
        
        if ammoSkillId:
            self.skillTray.decrementSkillTrayAmount(ammoSkillId)
        else:
            self.skillTray.decrementSkillTrayAmount(skillId)
        if skillId == InventoryType.UseItem:
            messenger.send(WeaponGlobals.LocalAvatarUseItem, [
                skillId,
                ammoSkillId,
                combo,
                charge])
        elif WeaponGlobals.isProjectileSkill(skillId, ammoSkillId):
            posHpr = [
                0,
                0,
                0,
                0,
                0,
                0]
            messenger.send(WeaponGlobals.LocalAvatarUseProjectileSkill, [
                skillId,
                ammoSkillId,
                posHpr,
                charge])
        elif WeaponGlobals.getIsShipSkill(skillId) and not WeaponGlobals.getIsShout(skillId):
            messenger.send(WeaponGlobals.LocalAvatarUseShipSkill, [
                skillId,
                ammoSkillId])
        elif skillId in InventoryType.BackstabSkills:
            messenger.send(WeaponGlobals.LocalAvatarUseTargetedSkill, [
                skillId,
                ammoSkillId,
                combo,
                self.chargeTime])
        else:
            messenger.send(WeaponGlobals.LocalAvatarUseTargetedSkill, [
                skillId,
                ammoSkillId,
                combo,
                charge])
        if WeaponGlobals.getIsShipSkill(skillId):
            if localAvatar.ship:
                localAvatar.ship.requestShipSkill(skillId, ammoSkillId)

        if skillId:
            if self.weaponMode in (WeaponGlobals.COMBAT, WeaponGlobals.MELEE, WeaponGlobals.VOODOO, WeaponGlobals.THROWING, WeaponGlobals.SAILING):
                skillTrack = WeaponGlobals.getSkillTrack(skillId)
                if skillTrack == WeaponGlobals.RADIAL_SKILL_INDEX:
                    rechargeT = base.cr.battleMgr.getModifiedRechargeTime(localAvatar, skillId)
                    taskMgr.doMethodLater(rechargeT, self.skillRechargeAlert, 'skillRechargePopup-' + str(skillId), extraArgs = [
                        skillId])

        self.__startSkillTimers()
        if combo == -1:
            self.missedTime = 1
            self.resetComboLevel()
            self.ignoreInput()
            self.combatChainLvl = 0
            messenger.send('tooFast')
        
        timestamp = globalClockDelta.getFrameNetworkTime(bits = 32)
        self.lastAttack = (skillId, timestamp)
        if skillId not in (EnemySkills.PISTOL_CHARGE, EnemySkills.STAFF_WITHER_CHARGE, EnemySkills.STAFF_SOULFLAY_CHARGE, EnemySkills.STAFF_PESTILENCE_CHARGE, EnemySkills.STAFF_HELLFIRE_CHARGE, EnemySkills.STAFF_BANISH_CHARGE, EnemySkills.STAFF_DESOLATION_CHARGE, EnemySkills.GRENADE_CHARGE) and skillId not in InventoryType.BackstabSkills:
            self.chargeTime = 0
            if skillId not in self.IGNORES_INPUT_LOCK:
                self.triggerInputLock()

        return 1

    def __startSkillTimers(self):
        if localAvatar.curAttackAnim:
            duration = localAvatar.curAttackAnim.getDuration()
        else:
            duration = 1.0
        self.comboReady = -1
        self.reloadFrame.show()
        taskMgr.remove('comboReadyTimer')
        taskMgr.remove('skillFinishedTimer')
        taskMgr.doMethodLater(self.WINDOW_LENGTH * duration, self.__comboReadyTimer, 'comboReadyTimer')
        taskMgr.doMethodLater(duration, self.__skillFinishedTimer, 'skillFinishedTimer', priority = 40)

    def __comboReadyTimer(self, task):
        self.comboReady = 1
    
    def __skillFinishedTimer(self, task):
        if self.combatChainLvl == 1 and self.missedTime == 0:
            messenger.send('tooSlow')
        
        self.reloadFrame.hide()
        self.comboReady = 0
        self.combatChainLvl = 0
        self.missedTime = 0
        
        def invArrived(inv):
            self.invReq = None
            if inv:
                self.resetComboLevel()

        if not self.invReq:
            DistributedInventoryBase.getInventory(localAvatar.getInventoryId(), invArrived)

    def triggerSkillTraySkill(self, skillId):
        if skillId > 0:
            combo = self.comboLevel
            attackSelected = 'usedSpecialAttack'
            if self.weaponMode == WeaponGlobals.STAFF:
                if self.chargeTime >= self.CHARGE_MODE_TIME_THRESHOLD:
                    localAvatar.guiMgr.createWarning(PLocalizer.AmmoChargingWarning, PiratesGuiGlobals.TextFG6)
                    return
                
                if self.skillTray.traySkillMap:
                    if skillId in self.skillTray.traySkillMap:
                        for i in range(len(self.skillTray.traySkillMap)):
                            if self.skillTray.traySkillMap[i] == skillId:
                                if self.skillTray.origMap[i][1]:
                                    self.skillTray.tray[i + 1].toggleButton(True)
                            else:
                                if self.skillTray.origMap[i][1]:
                                    self.skillTray.tray[i + 1].toggleButton(False)

            if self.weaponMode in (WeaponGlobals.FIREARM, WeaponGlobals.STAFF, WeaponGlobals.CANNON, WeaponGlobals.GRENADE):
                if self.weaponMode == WeaponGlobals.CANNON:
                    self.setAmmoSkillId(skillId)
                    if self.linkedCannon:
                        self.linkedCannon.selectAmmo(self.ammoSkillId)
                    
                elif self.weaponMode == WeaponGlobals.FIREARM or self.weaponMode == WeaponGlobals.GRENADE:
                    ammoChoice = skillId
                    inv = localAvatar.getInventory()
                    if inv is None:
                        return
                    
                    maxQuant = WeaponGlobals.getSkillMaxQuantity(ammoChoice)
                    if not maxQuant == WeaponGlobals.INF_QUANT:
                        ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(ammoChoice)
                        ammoAmt = inv.getStackQuantity(ammoInvId)
                        if ammoAmt > 0:
                            self.setAmmoSkillId(ammoChoice)
                            if self.weaponMode == WeaponGlobals.FIREARM:
                                self.reloadWeapon()
                            elif self.weaponMode == WeaponGlobals.GRENADE:
                                self.changeHandheld(self.ammoSkillId)
                            
                            if self.skillTray.traySkillMap:
                                if skillId in self.skillTray.traySkillMap:
                                    for i in range(len(self.skillTray.traySkillMap)):
                                        if self.skillTray.traySkillMap[i] == skillId:
                                            if self.skillTray.origMap[i][1]:
                                                self.skillTray.tray[i + 1].toggleButton(True)
                                        else:
                                            if self.skillTray.origMap[i][1]:
                                                self.skillTray.tray[i + 1].toggleButton(False)

                        else:
                            localAvatar.guiMgr.createWarning(PLocalizer.OutOfAmmoWarning, PiratesGuiGlobals.TextFG6)
                    else:
                        self.setAmmoSkillId(ammoChoice)
                        if self.weaponMode == WeaponGlobals.FIREARM:
                            self.reloadWeapon()
                        elif self.weaponMode == WeaponGlobals.GRENADE:
                            self.changeHandheld(self.ammoSkillId)
                        
                        if self.skillTray.traySkillMap:
                            if skillId in self.skillTray.traySkillMap:
                                for i in range(len(self.skillTray.traySkillMap)):
                                    if self.skillTray.traySkillMap[i] == skillId:
                                        if self.skillTray.origMap[i][1]:
                                            self.skillTray.tray[i + 1].toggleButton(True)
                                    else:
                                        if self.skillTray.origMap[i][1]:
                                            self.skillTray.tray[i + 1].toggleButton(False)

                else:
                    ammoChoice = skillId
                    self.setAmmoSkillId(ammoChoice)
            elif self.weaponMode in (WeaponGlobals.COMBAT, WeaponGlobals.SAILING, WeaponGlobals.THROWING):
                self.trySkill(skillId, 0, combo)
            elif self.weaponMode == WeaponGlobals.VOODOO:
                if localAvatar.hasStickyTargets():
                    haveFriendly = localAvatar.getFriendlyStickyTargets()
                    haveHostile = localAvatar.getHostileStickyTargets()
                    if haveFriendly and not haveHostile:
                        if not WeaponGlobals.isFriendlyFire(skillId):
                            localAvatar.guiMgr.createWarning(PLocalizer.NeedHostileTarget, PiratesGuiGlobals.TextFG6)
                        else:
                            self.trySkill(skillId, 0, combo)
                    elif not haveFriendly and haveHostile:
                        if WeaponGlobals.isFriendlyFire(skillId):
                            localAvatar.guiMgr.createWarning(PLocalizer.NeedFriendlyTarget, PiratesGuiGlobals.TextFG6)
                        else:
                            self.trySkill(skillId, 0, combo)
                    else:
                        self.trySkill(skillId, 0, combo)
                else:
                    localAvatar.guiMgr.createWarning(PLocalizer.NotAttunedWarning, PiratesGuiGlobals.TextFG6)
            else:
                attackSelected = None
            if attackSelected:
                messenger.send(attackSelected)
            
            self.acceptInput()
        
        self.combatChainLvl = 0

    def isPVP(self):
        if isinstance(base.cr.activeWorld, DistributedPVPInstance.DistributedPVPInstance):
            return 1
        else:
            return 0

    def beginButtonCharge(self):
        if not self.ammoSkillId:
            return
        
        self.chargeTime = 0
        self.maxCharge = 0
        self.thresholdHit = 0
        self.offsetTime = 0
        self.chargeWeapon = self.weaponMode
        if self.weaponMode == WeaponGlobals.FIREARM:
            self.maxCharge = WeaponGlobals.getAttackMaxCharge(InventoryType.PistolTakeAim, self.ammoSkillId)
        elif self.weaponMode == WeaponGlobals.GRENADE:
            self.maxCharge = WeaponGlobals.getAttackMaxCharge(InventoryType.GrenadeLongVolley, self.ammoSkillId)
        elif self.weaponMode == WeaponGlobals.STAFF:
            self.maxCharge = WeaponGlobals.getAttackMaxCharge(self.ammoSkillId)
            inv = localAvatar.getInventory()
            amt = max(0, inv.getStackQuantity(InventoryType.StaffSpiritLore) - 1) * WeaponGlobals.getAttackMaxCharge(InventoryType.StaffSpiritLore)
            amt = 1.0 - amt
            self.maxCharge = self.maxCharge * amt
        
        if self.maxCharge == 0:
            return
        
        self.maxCharge += self.CHARGE_MODE_TIME_THRESHOLD
        if self.weaponMode == WeaponGlobals.STAFF:
            self.chargeMeterBar['barColor'] = Vec4(0.6, 0.3, 1.0, 1.0)
        else:
            self.chargeMeterBar['barColor'] = Vec4(1.0, 0.2, 0.1, 1.0)
        taskMgr.add(self.buttonCharging, 'buttonCharging', priority = 40)

    def endButtonCharge(self):
        self.chargeMeter.hide()
        self.isCharging = 0
        self.thresholdHit = 0
        taskMgr.remove('buttonCharging')

    def buttonCharging(self, task):
        self.taskTime = task.time
        if self.chargeWeapon != self.weaponMode:
            self.endButtonCharge()
        if self.chargeTime > 0:
            if self.weaponMode == WeaponGlobals.FIREARM or self.weaponMode == WeaponGlobals.GRENADE:
                weaponVolley = WeaponGlobals.getWeaponVolley(localAvatar.currentWeaponId)
                if weaponVolley > 0 and self.volley >= weaponVolley:
                    self.chargeTime = 0
                    self.offsetTime = task.time
                    return Task.cont
            if localAvatar.isAirborne():
                if self.weaponMode == WeaponGlobals.STAFF or self.weaponMode == WeaponGlobals.GRENADE:
                    self.chargeTime = 0
                    self.offsetTime = task.time
                    return Task.cont
            skillEffects = localAvatar.getSkillEffects()
            if WeaponGlobals.C_STUN in skillEffects:
                self.chargeTime = 0
                self.offsetTime = task.time
            if self.isUsingSkill and self.weaponMode != WeaponGlobals.VOODOO:
                self.chargeTime = 0
                self.offsetTime = task.time
            else:
                if self.weaponMode == WeaponGlobals.STAFF:
                    cost = -1 * WeaponGlobals.getMojoCost(self.ammoSkillId)
                    if localAvatar.mojo < cost:
                        self.endButtonCharge()
                        localAvatar.guiMgr.createWarning(PLocalizer.NoManaWarning, PiratesGuiGlobals.TextFG6)
                        return Task.done
                if not self.thresholdHit:
                    if self.weaponMode == WeaponGlobals.FIREARM:
                        self.trySkill(EnemySkills.PISTOL_CHARGE, 0)
                    elif self.weaponMode == WeaponGlobals.GRENADE:
                        self.trySkill(EnemySkills.GRENADE_CHARGE, 0)
                    elif self.weaponMode == WeaponGlobals.STAFF:
                        skillId = WeaponGlobals.getChargeSkill(self.ammoSkillId)
                        self.trySkill(skillId, 0)
                    self.thresholdHit = 1
                    self.isCharging = 1
                    if self.ammoSkillId:
                        if not WeaponGlobals.isInfiniteAmmo(self.ammoSkillId):
                            ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(self.ammoSkillId)
                            inv = localAvatar.getInventory()
                            amt = inv.getStackQuantity(ammoInvId)
                            if amt < 1:
                                self.endButtonCharge()
                                return Task.done
            if self.weaponMode != WeaponGlobals.VOODOO:
                self.chargeMeter.show()
        if self.chargeTime > 0:
            self.chargeMeterBar['value'] = self.chargeTime
            if self.chargeTime >= self.maxCharge:
                if self.weaponMode == WeaponGlobals.STAFF:
                    self.chargeMeterBar['barColor'] = Vec4(0.7, 0.7, 1.0, 1.0)
                else:
                    self.chargeMeterBar['barColor'] = Vec4(1.0, 0.6, 0.3, 1.0)
        else:
            self.chargeMeterBar['value'] = 0
        self.chargeMeterBar['range'] = self.maxCharge
        if self.InstantCast:
            self.chargeTime = self.maxCharge
        else:
            self.chargeTime = max(0, min(1 + self.maxCharge + self.CHARGE_MODE_TIME_THRESHOLD, task.time - self.offsetTime)) - self.CHARGE_MODE_TIME_THRESHOLD
        return Task.cont

    def processInput(self, button):
        if not self.skillMapping:
            return
        
        inventory = localAvatar.getInventory()
        if not inventory:
            return
        elif button == 'action-up':
            self.endButtonCharge()
            if self.chargeTime >= 0:
                skillIndex = 1
            else:
                skillIndex = 0
            skillId = 0
            skillMap = self.skillMapping.get(button[:-3])
            if skillMap:
                if skillIndex > len(skillMap) - 1:
                    skillIndex = len(skillMap) - 1
                
                skillId = skillMap[skillIndex]
            
            if self.weaponMode == WeaponGlobals.VOODOO:
                self.trySkill(InventoryType.DollAttune, 0)
                return
            elif self.weaponMode == WeaponGlobals.STAFF:
                maxCharge = WeaponGlobals.getAttackMaxCharge(skillId, self.ammoSkillId)
                inv = localAvatar.getInventory()
                amt = max(0, inv.getStackQuantity(InventoryType.StaffSpiritLore) - 1) * WeaponGlobals.getAttackMaxCharge(InventoryType.StaffSpiritLore)
                amt = 1.0 - amt
                maxCharge = maxCharge * amt
                chargeAmt = int(self.chargeTime / STAFF_INTERVAL)
                chargeAmt = max(0, min(chargeAmt, maxCharge))
                if self.chargeTime > 0:
                    if self.chargeTime >= self.maxCharge:
                        self.trySkill(self.ammoSkillId, 0, charge = chargeAmt)
                    else:
                        self.trySkill(EnemySkills.STAFF_FIZZLE, 0)
                else:
                    self.trySkill(InventoryType.StaffBlast, 0)
                return
            elif self.weaponMode == WeaponGlobals.FIREARM:
                if localAvatar.currentTarget:
                    if not base.cr.battleMgr.obeysPirateCode(localAvatar, localAvatar.currentTarget):
                        if localAvatar.guiMgr.codeShown:
                            self.tryShoot += 1
                            if self.tryShoot > 5:
                                self.tryShoot = 0
                                localAvatar.guiMgr.codeShown = 0
                                localAvatar.guiMgr.showPirateCode()

                self.trySkill(skillId, self.ammoSkillId, charge = self.chargeTime)
                return
            elif self.weaponMode == WeaponGlobals.GRENADE:
                self.trySkill(skillId, self.ammoSkillId, charge = self.chargeTime)
                return
            
        elif button == 'action':
            if self.weaponMode == WeaponGlobals.VOODOO or self.weaponMode == WeaponGlobals.STAFF:
                self.beginButtonCharge()
                return
            elif self.weaponMode == WeaponGlobals.FIREARM:
                if inventory.getStackQuantity(InventoryType.PistolTakeAim) > 1:
                    self.beginButtonCharge()
                else:
                    if localAvatar.currentTarget:
                        if not base.cr.battleMgr.obeysPirateCode(localAvatar, localAvatar.currentTarget):
                            if localAvatar.guiMgr.codeShown:
                                self.tryShoot += 1
                                if self.tryShoot > 5:
                                    self.tryShoot = 0
                                    localAvatar.guiMgr.codeShown = 0
                                    localAvatar.guiMgr.showPirateCode()

                    skillId = self.skillMapping[button][0]
                    self.trySkill(skillId, self.ammoSkillId)
                return
            elif self.weaponMode == WeaponGlobals.GRENADE:
                if inventory.getStackQuantity(InventoryType.GrenadeLongVolley) > 1:
                    self.beginButtonCharge()
                else:
                    skillId = self.skillMapping[button][0]
                    self.trySkill(skillId, self.ammoSkillId)
                return
            elif self.weaponMode == WeaponGlobals.MELEE:
                self.trySkill(InventoryType.MeleePunch, 0, 0)
                return
            
            if self.weaponMode == WeaponGlobals.COMBAT or self.weaponMode == WeaponGlobals.VOODOO or self.weaponMode == WeaponGlobals.THROWING:
                origTrack = self.skillMapping.get(button)
                skillTrack = Freebooter.pruneFreebooterSkills(origTrack)
                if not skillTrack:
                    return
                
                combo = self.checkCombo()
                if self.combatChainLvl > len(skillTrack) - 1:
                    self.ignoreInput()
                    return
                elif self.combatChainLvl == 0 and not (combo == -1):
                    self.resetComboLevel()
                
                if self.isUsingSkill:
                    if localAvatar.currentTarget:
                        if self.combatChainLvl <= 1 and combo <= 0:
                            self.resetComboLevel()
                            messenger.send('tooFast')
                            self.combatChainLvl = 0
                            combo = 0
                            return

                skillId = skillTrack[self.combatChainLvl]
                isSkillUsed = self.trySkill(skillId, 0, combo)
                if isSkillUsed:
                    self.combatChainLvl += 1

    def triggerSkillQueue(self):
        if self.skillQueue and not self.weaponQueue:
            self.isUsingSkill = 0
            (skillId, ammoSkillId, combo) = self.skillQueue
            self.skillQueue = None
            isSkillUsed = self.trySkill(skillId, ammoSkillId, combo)
            if isSkillUsed:
                self.combatChainLvl += 1
            
        else:
            self.isUsingSkill = 0

    def triggerWeaponQueue(self):
        if self.weaponQueue:
            weapon = self.weaponQueue
            self.weaponQueue = None
            self.skillQueue = 0
            self.toggleWeapon(weapon)

    def acceptInput(self, args = None):
        if self.isAcceptingInput:
            return
        
        if not self.isEnabled:
            return
        
        if self.rep != InventoryType.CannonRep:
            self.accept('action', self.processInput, [
                'action'])
            self.accept('action-up', self.processInput, [
                'action-up'])
        
        self.accept('mouse2', self.processInput, [
            'mouse2'])
        self.accept('shift-mouse1', self.processInput, [
            'shift-mouse1'])
        self.isAcceptingInput = 1
    
    def disableTray(self):
        self.isEnabled = 0
        self.endAimAssist()
        self.reloadFrame.hide()
        for buttonName in self.SkillButtonEvents:
            self.ignore(buttonName)
        
        self.ignore('skillStarted')
        self.ignore('skillFinished')
        self.ignore('reloadFinished')
        for i in xrange(1, 9):
            self.ignore('%d' % i)
        
        self.ignoreInput()
        self.isUsingSkill = 0
        self.linkedCannon = 0
        self.endButtonCharge()
        self.weaponMode = 0
    
    def ignoreInput(self):
        if not self.isAcceptingInput:
            return
        
        self.isAcceptingInput = 0

    def hideSkills(self):
        self.ignoreInput()
        if self.skillTray:
            self.skillTray.hideSkillTray()

    def showSkills(self):
        self.acceptInput()
        for skillId in self.skillIds:
            localAvatar.skillDiary.continueRecharging(skillId)

    def hide(self):
        GuiTray.hide(self)
        self.hideSkills()
    
    def show(self):
        GuiTray.show(self)
        self.showSkills()
    
    def getResetComboName(self):
        return 'resetComboName'

    def getComboRecoveryName(self):
        return 'comboRecoveryName'
    
    def resetComboLevel(self, args = None):
        self.comboLevel = 0
        if self.weaponMode == WeaponGlobals.FIREARM or self.weaponMode == WeaponGlobals.GRENADE:
            weaponVolley = WeaponGlobals.getWeaponVolley(localAvatar.currentWeaponId)
            if weaponVolley > 0 and self.volley >= weaponVolley:
                self.reloadWeapon()
            else:
                self.acceptInput()
        else:
            self.acceptInput()
        if localAvatar.currentTarget:
            localAvatar.currentTarget.resetComboLevel()
        
        self.triggerWeaponQueue()

    def checkCombo(self):
        if self.comboReady == 1:
            combo = self.comboLevel
        elif self.comboReady == -1:
            combo = -1
        else:
            combo = 0
        return combo

    def setLinkedCannon(self, cannon):
        self.linkedCannon = cannon

    def interruptCharge(self):
        self.chargeTime = 0
        self.offsetTime = self.taskTime
        self.taskTime = 0
    
    def reloadWeapon(self):
        if self.ammoSkillId:
            inv = localAvatar.getInventory()
            maxQuant = WeaponGlobals.getSkillMaxQuantity(self.ammoSkillId)
            if not maxQuant == WeaponGlobals.INF_QUANT:
                ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(self.ammoSkillId)
                if not inv:
                    self.outOfAmmo()
                    return
                else:
                    ammoAmt = inv.getStackQuantity(ammoInvId)
                    if ammoAmt <= 0:
                        self.outOfAmmo()
                        return

        if self.weaponMode == WeaponGlobals.FIREARM:
            self.trySkill(EnemySkills.PISTOL_RELOAD, 0)
        elif self.weaponMode == WeaponGlobals.GRENADE:
            self.trySkill(EnemySkills.GRENADE_RELOAD, 0)
        
        self.ignoreInput()

    def finishReload(self):
        self.volley = 0

    def changeHandheld(self, ammoSkillId):
        localAvatar.setCurrentAmmo(ammoSkillId)
        localAvatar.d_requestCurrentAmmo(ammoSkillId)
        self.volley = 0
        self.ignoreInput()

    def outOfAmmo(self):
        if self.weaponMode == WeaponGlobals.GRENADE:
            localAvatar.setCurrentAmmo(0)
            localAvatar.d_requestCurrentAmmo(0)
        
        localAvatar.guiMgr.createWarning(PLocalizer.OutOfAmmoWarning, PiratesGuiGlobals.TextFG6)
    
    def beginAimAssist(self, target):
        self.aimAssistTarget = target
        taskMgr.remove('aimAssistTask')
        taskMgr.doMethodLater(AIM_ASSIST_DURATION, self.endAimAssist, 'aimAssistTask')
    
    def endAimAssist(self, args = None):
        taskMgr.remove('aimAssistTask')
        self.aimAssistTarget = None
    
    def skillRechargeAlert(self, skillId):
        pass
    
    def enableMouseDrawsWeapon(self):
        self.isMouseMode = 0
    
    def disableMouseDrawsWeapon(self):
        self.isMouseMode = 1

    def updateWeaponRep(self, category, rep):
        for button in self.weaponButtons.values():
            if button.category == category:
                button.updateRep(rep)
        
        self.skillTray.updateSkillTrayMeter()

    def __skillTrayCallback(self, skillId):
        self.triggerSkillTraySkill(skillId)
    
    def actionDown(self):
        if not self.actionPressed:
            self.actionPressed = True
            messenger.send('action')

    def actionUp(self):
        if self.actionPressed:
            self.actionPressed = False
            messenger.send('action-up')

    def clearQueues(self):
        self.weaponQueue = None
        self.skillQueue = None


