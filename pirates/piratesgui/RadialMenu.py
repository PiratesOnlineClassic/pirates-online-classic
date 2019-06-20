import math
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.task import Task
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesgui.SkillRing import SkillRing
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter
from direct.interval.IntervalGlobal import *
from pirates.reputation import ReputationGlobals
from pirates.piratesgui.SkillButton import SkillButton
from pirates.piratesgui.ReputationMeter import ReputationMeter
import PiratesGuiGlobals
Tolerance = 20
FrameSize = 0.12
Center = [
    (0, 0),
    (-50, -50),
    (0, -75),
    (50, -50),
    (75, 0),
    (50, 50),
    (0, 75),
    (-50, 50),
    (-75, 0)]

def ImageScale(repId):
    if repId == InventoryType.PistolRep:
        return 0.2
    elif repId == InventoryType.SailingRep:
        return 0.135
    elif repId == InventoryType.CannonRep:
        return 0.14
    elif repId == InventoryType.GrenadeRep:
        return 0.12
    else:
        return 0.14


def getSkillIconName(skillId, frame):
    if skillId == InventoryType.CutlassRep:
        return 'sword'
    elif skillId == InventoryType.SailingRep:
        return 'grenade'
    elif skillId == InventoryType.CannonRep:
        return 'cannon'
    elif skillId == InventoryType.WandRep:
        return 'staff'
    elif skillId == InventoryType.MeleeRep:
        return 'sword'
    elif skillId == InventoryType.DaggerRep:
        return 'dagger'
    elif skillId == InventoryType.GrenadeRep:
        return 'grenade'
    elif skillId == InventoryType.PistolRep:
        return 'pistol'
    elif skillId == InventoryType.DollRep:
        if frame == 0:
            return 'doll'
        else:
            return 'voodoo_attuned'
    else:
        return WeaponGlobals.getSkillIcon(skillId)


def isComboSkill(skillId):
    inv = base.localAvatar.getInventory()
    if inv == None:
        return 0
    
    if skillId == InventoryType.DollAttune or skillId == InventoryType.DollPoke:
        return 0
    
    if WeaponGlobals.getSkillTrack(skillId) == 1:
        if inv.getStackQuantity(skillId):
            return 1

    return 0


def PassiveSkills(repId, minlvl):
    return FindSkills(repId, 3, minlvl)


def ActiveSkills(repId, minlvl):
    return FindSkills(repId, 2, minlvl)


def ComboSkills(repId, minlvl):
    return FindSkills(repId, 1, minlvl)


def AllPassiveSkills(repId, minlvl):
    return FindAllSkills(repId, 3, minlvl)


def AllActiveSkills(repId, minlvl):
    return FindAllSkills(repId, 2, minlvl)


def AllComboSkills(repId, minlvl):
    return FindAllSkills(repId, 1, minlvl)


def FindSkills(repId, skilltrack, minlvl):
    inv = base.localAvatar.getInventory()
    if inv == None:
        print 'WARNING - FindSkills came up with no inventory for ', repId
        return []
    
    choices = []
    if repId == InventoryType.CutlassRep:
        skillId = InventoryType.begin_WeaponSkillCutlass
        while skillId < InventoryType.end_WeaponSkillCutlass:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                if inv.getStackQuantity(skillId) >= minlvl:
                    choices.append(skillId)
            
            skillId += 1
    elif repId == InventoryType.MeleeRep:
        skillId = InventoryType.begin_WeaponSkillMelee
        while skillId < InventoryType.end_WeaponSkillMelee:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                if inv.getStackQuantity(skillId) >= minlvl:
                    choices.append(skillId)

            skillId += 1
    elif repId == InventoryType.DaggerRep:
        skillId = InventoryType.begin_WeaponSkillDagger
        while skillId < InventoryType.end_WeaponSkillDagger:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                if inv.getStackQuantity(skillId) >= minlvl:
                    choices.append(skillId)

            skillId += 1
    elif repId == InventoryType.GrenadeRep:
        skillId = InventoryType.begin_WeaponSkillGrenade
        while skillId < InventoryType.end_WeaponSkillGrenade:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                if inv.getStackQuantity(skillId) >= minlvl:
                    choices.append(skillId)

            skillId += 1
    elif repId == InventoryType.DollRep:
        skillId = InventoryType.begin_WeaponSkillDoll
        while skillId < InventoryType.end_WeaponSkillDoll:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                if inv.getStackQuantity(skillId) >= minlvl:
                    choices.append(skillId)

            skillId += 1
    elif repId == InventoryType.WandRep:
        skillId = InventoryType.begin_WeaponSkillWand
        while skillId < InventoryType.end_WeaponSkillWand:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                if inv.getStackQuantity(skillId) >= minlvl:
                    choices.append(skillId)

            skillId += 1
    elif repId == InventoryType.KettleRep:
        skillId = InventoryType.begin_WeaponSkillKettle
        while skillId < InventoryType.end_WeaponSkillKettle:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                if inv.getStackQuantity(skillId) >= minlvl:
                    choices.append(skillId)

            skillId += 1
    elif repId == InventoryType.PistolRep:
        skillId = InventoryType.begin_WeaponSkillPistol
        while skillId < InventoryType.end_WeaponSkillPistol:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                if inv.getStackQuantity(skillId) >= minlvl:
                    choices.append(skillId)

            skillId += 1
    elif repId == InventoryType.CannonRep:
        skillId = InventoryType.begin_WeaponSkillCannon
        while skillId < InventoryType.end_WeaponSkillCannon:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                if inv.getStackQuantity(skillId) >= minlvl:
                    choices.append(skillId)

            skillId += 1
    elif repId == InventoryType.SailingRep:
        skillId = InventoryType.begin_SkillSailing
        while skillId < InventoryType.end_SkillSailing:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                if inv.getStackQuantity(skillId) >= minlvl:
                    choices.append(skillId)

            skillId += 1
    
    return choices


def getAllSkills(repId, skilltrack):
    inv = base.localAvatar.getInventory()
    if inv == None:
        print 'WARNING - getAllSkills came up with no inventory for ', repId
        return []
    
    minlvl = 2
    choices = []
    if repId == InventoryType.CutlassRep:
        skillId = InventoryType.begin_WeaponSkillCutlass
        while skillId < InventoryType.end_WeaponSkillCutlass:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                locked = False
                if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                    locked = not WeaponGlobals.canFreeUse(skillId)
                
                if inv.getStackQuantity(skillId) >= minlvl:
                    skill = (skillId, True, locked)
                else:
                    skill = (skillId, False, locked)
                choices.append(skill)
            
            skillId += 1
    elif repId == InventoryType.MeleeRep:
        skillId = InventoryType.begin_WeaponSkillMelee
        while skillId < InventoryType.end_WeaponSkillMelee:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                locked = False
                if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                    locked = not WeaponGlobals.canFreeUse(skillId)
                
                if inv.getStackQuantity(skillId) >= minlvl:
                    skill = (skillId, True, locked)
                else:
                    skill = (skillId, False, locked)
                choices.append(skill)
            
            skillId += 1
    elif repId == InventoryType.DaggerRep:
        skillId = InventoryType.begin_WeaponSkillDagger
        while skillId < InventoryType.end_WeaponSkillDagger:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                locked = False
                if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                    locked = not WeaponGlobals.canFreeUse(skillId)
                
                if inv.getStackQuantity(skillId) >= minlvl:
                    skill = (skillId, True, locked)
                else:
                    skill = (skillId, False, locked)
                choices.append(skill)
            
            skillId += 1
    elif repId == InventoryType.GrenadeRep:
        skillId = InventoryType.begin_WeaponSkillGrenade
        while skillId < InventoryType.end_WeaponSkillGrenade:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                locked = False
                if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                    locked = not WeaponGlobals.canFreeUse(skillId)
                
                if inv.getStackQuantity(skillId) >= minlvl:
                    skill = (skillId, True, locked)
                else:
                    skill = (skillId, False, locked)
                choices.append(skill)
            
            skillId += 1
    elif repId == InventoryType.DollRep:
        skillId = InventoryType.begin_WeaponSkillDoll
        while skillId < InventoryType.end_WeaponSkillDoll:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                locked = False
                if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                    locked = not WeaponGlobals.canFreeUse(skillId)
                
                if inv.getStackQuantity(skillId) >= minlvl:
                    skill = (skillId, True, locked)
                else:
                    skill = (skillId, False, locked)
                choices.append(skill)
            
            skillId += 1
    elif repId == InventoryType.WandRep:
        skillId = InventoryType.begin_WeaponSkillWand
        while skillId < InventoryType.end_WeaponSkillWand:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                locked = False
                if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                    locked = not WeaponGlobals.canFreeUse(skillId)
                
                if inv.getStackQuantity(skillId) >= minlvl:
                    skill = (skillId, True, locked)
                else:
                    skill = (skillId, False, locked)
                choices.append(skill)
            
            skillId += 1
    elif repId == InventoryType.KettleRep:
        skillId = InventoryType.begin_WeaponSkillKettle
        while skillId < InventoryType.end_WeaponSkillKettle:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                locked = False
                if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                    locked = not WeaponGlobals.canFreeUse(skillId)
                
                if inv.getStackQuantity(skillId) >= minlvl:
                    skill = (skillId, True, locked)
                else:
                    skill = (skillId, False, locked)
                choices.append(skill)
            
            skillId += 1
    elif repId == InventoryType.PistolRep:
        skillId = InventoryType.begin_WeaponSkillPistol
        while skillId < InventoryType.end_WeaponSkillPistol:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                locked = False
                if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                    locked = not WeaponGlobals.canFreeUse(skillId)
                
                if inv.getStackQuantity(skillId) >= minlvl:
                    skill = (skillId, True, locked)
                else:
                    skill = (skillId, False, locked)
                choices.append(skill)
            
            skillId += 1
    elif repId == InventoryType.CannonRep:
        skillId = InventoryType.begin_WeaponSkillCannon
        while skillId < InventoryType.end_WeaponSkillCannon:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                locked = False
                if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                    locked = not WeaponGlobals.canFreeUse(skillId)
                
                if inv.getStackQuantity(skillId) >= minlvl:
                    skill = (skillId, True, locked)
                else:
                    skill = (skillId, False, locked)
                choices.append(skill)
            
            skillId += 1
    elif repId == InventoryType.SailingRep:
        skillId = InventoryType.begin_SkillSailing
        while skillId < InventoryType.end_SkillSailing:
            if WeaponGlobals.getSkillTrack(skillId) == skilltrack:
                locked = False
                if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                    locked = not WeaponGlobals.canFreeUse(skillId)
                
                shouldBeVisible = inv.getStackQuantity(skillId) >= minlvl
                skill = (skillId, shouldBeVisible, locked)
                choices.append(skill)
            
            skillId += 1
    
    return choices


def InnerRingOffset(num):
    if num == 1:
        return (-0.175, 0.175)
    elif num == 2:
        return (0.0, 0.25)
    elif num == 3:
        return (0.175, 0.175)
    elif num == 4:
        return (0.25, 0.0)
    elif num == 5:
        return (0.175, -0.175)
    elif num == 6:
        return (0.0, -0.25)
    elif num == 7:
        return (-0.175, -0.175)
    elif num == 8:
        return (-0.25, 0.0)
    


def RingMatch(maxSlot, xc, yc):
    if xc * xc + yc * yc < 2 * Tolerance * Tolerance:
        return 0
    
    degOff = rad2Deg(math.atan2(xc, yc))
    degOff += 180
    degOff = 360 - degOff
    degOff += 67.5
    if degOff > 360:
        degOff -= 360
    
    slot = degOff / 45
    if slot > maxSlot:
        return -1
    else:
        return 1 + int(slot)


def ExactRingMatch(maxSlot, xc, yc):
    loopItr = 0
    Xscale = base.win.getXSize() / 800
    Yscale = base.win.getYSize() / 600
    XTol = Tolerance * Xscale
    YTol = Tolerance * Yscale
    while loopItr < maxSlot + 1:
        targetXc = Center[loopItr][0] * Xscale
        targetYc = Center[loopItr][1] * Yscale
        if xc - targetXc < XTol and xc - targetXc > XTol * -1 and yc - targetYc < YTol and yc - targetYc > YTol * -1:
            return loopItr
        loopItr += 1

    return -1


class RadialMenu:
    SkillIcons = None
    
    def __init__(self, rep, weaponMode):
        self.rep = rep
        self.weaponMode = weaponMode
        localAvatar.cr.targetMgr.reticle.hide()
        if self.weaponMode in (WeaponGlobals.MELEE, WeaponGlobals.COMBAT, WeaponGlobals.THROWING):
            target = base.cr.targetMgr.takeAim(localAvatar)
            if target:
                localAvatar.guiMgr.combatTray.beginAimAssist(target)

        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        localAvatar.guiMgr.setSeaChestAllowed(False)
        self.radial = {}
        self.rframe = {}
        self.ammoAmt = {}
        self.rstatus = {}
        self.rstatus[0] = 0
        self.rframe[0] = SkillRing(Vec4(1, 0.8, 0.5, 1), Vec4(0, 0, 0, 1.0))
        skillRing = SkillRing(Vec4(1, 0.8, 0.5, 1), Vec4(0, 0, 0, 1.0))
        skillRing.reparentTo(aspect2d)
        skillRing.setPos(0.01, 0, 0.01)
        if not self.SkillIcons:
            self.SkillIcons = loader.loadModel('models/textureCards/skillIcons')
        
        if self.rep == InventoryType.DollRep and localAvatar.hasStickyTargets():
            asset = getSkillIconName(self.rep, 1)
        else:
            asset = getSkillIconName(self.rep, 0)
        self.radial[0] = DirectFrame(parent = aspect2d, relief = None, image = self.SkillIcons.find('**/%s' % asset), image_scale = ImageScale(self.rep), image_pos = (0.06, 0, 0.06), pos = (-0.05, 0, -0.05), sortOrder = 10)
        self.radial[0].setTransparency(1)
        origMap = ActiveSkills(self.rep, 2)
        self.radialSkillMap = Freebooter.pruneFreebooterSkills(origMap)
        self.numberOfItems = len(self.radialSkillMap)
        for i in range(self.numberOfItems):
            (x, y) = InnerRingOffset(i + 1)
            self.rstatus[i + 1] = 0
            self.rframe[i + 1] = SkillRing(Vec4(1, 0.8, 0.5, 1), Vec4(0, 0, 0, 1.0))
            skillRing = SkillRing(Vec4(1, 0.8, 0.5, 1), Vec4(0, 0, 0, 1.0))
            skillRing.reparentTo(aspect2d)
            skillRing.setPos(0.01 + x, 0, 0.01 + y)
            asset = getSkillIconName(self.radialSkillMap[i], 0)
            self.radial[i + 1] = DirectFrame(parent = aspect2d, relief = None, image = self.SkillIcons.find('**/%s' % asset), image_pos = (0.06, 0, 0.06), image_scale = ImageScale(self.rep), sortOrder = 100, pos = (-0.05 + x, 0, -0.05 + y))
            self.radial[i + 1].setTransparency(1)
            if self.weaponMode in (WeaponGlobals.FIREARM, WeaponGlobals.THROWING, WeaponGlobals.CANNON, WeaponGlobals.GRENADE):
                inv = localAvatar.getInventory()
                skillId = self.radialSkillMap[i]
                maxQuant = WeaponGlobals.getSkillMaxQuantity(skillId)
                if maxQuant == WeaponGlobals.INF_QUANT:
                    amtstr = '++'
                else:
                    ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(skillId)
                    ammoAmt = inv.getStackQuantity(ammoInvId)
                    ammoMax = inv.getStackLimit(ammoInvId)
                    amtstr = '%d' % ammoAmt
                self.ammoAmt[i + 1] = DirectLabel(parent = aspect2d, relief = None, text = amtstr, text_align = TextNode.ACenter, text_scale = 0.03, text_fg = (0.7, 1.0, 1.0, 1), text_font = PiratesGlobals.getPirateBoldOutlineFont(), pos = (x + 0.06, 0, y + 0.04), textMayChange = 1)
        
        self.mouseBasePosX = base.win.getXSize() / 2
        self.mouseBasePosY = base.win.getYSize() / 2
        self.radialHelp = DirectLabel(parent = aspect2d, relief = None, text = '', text_align = TextNode.ACenter, text_scale = 0.04, text_fg = (0.95, 1.0, 1.0, 1), text_shadow = PiratesGuiGlobals.TextShadow, pos = (0, 0, 0), textMayChange = 1)
        self.radialHelp.hide()
        self.radial[0].show()
        self.rframe[0].show()
        self.hiLiteItem = 0
        taskMgr.add(self.radialMenuHeartBeat, 'radialMenuHeartBeat', priority = 40)
        messenger.send('openedSpecialMenu')

    def radialMenuHeartBeat(self, task):
        if base.mouseWatcherNode.hasMouse():
            mouseData = base.win.getPointer(0)
            curX = mouseData.getX()
            curY = mouseData.getY()
        else:
            curX = 0
            curY = 0
        hLItem = RingMatch(self.numberOfItems, curX - self.mouseBasePosX, curY - self.mouseBasePosY)
        if hLItem != self.hiLiteItem:
            if hLItem < 1:
                self.radialHelp.hide()
            else:
                self.radialHelp['text'] = PLocalizer.InventoryTypeNames[self.radialSkillMap[hLItem - 1]]
                basePos = self.radial[hLItem].getPos()
                self.radialHelp.setPos(basePos[0] + 0.06, basePos[1], basePos[2] - 0.04)
                self.radialHelp.show()
            if self.hiLiteItem != -1:
                self.rframe[self.hiLiteItem].rollover(False)
            
            self.hiLiteItem = hLItem
            if self.hiLiteItem > 0:
                self.rframe[self.hiLiteItem].rollover(True)

        count = 0
        for skillId in self.radialSkillMap:
            greyOut = 0
            count += 1
            if self.weaponMode in (WeaponGlobals.FIREARM, WeaponGlobals.THROWING, WeaponGlobals.CANNON, WeaponGlobals.GRENADE):
                inv = localAvatar.getInventory()
                maxQuant = WeaponGlobals.getSkillMaxQuantity(skillId)
                if maxQuant == WeaponGlobals.INF_QUANT:
                    greyOut = 0
                else:
                    ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(skillId)
                    ammoAmt = inv.getStackQuantity(ammoInvId)
                    if ammoAmt <= 0:
                        greyOut = 1

            if localAvatar.mojo < -1 * WeaponGlobals.getMojoCost(skillId):
                greyOut = 1
            
            if skillId == InventoryType.SailBroadsideLeft or skillId == InventoryType.SailBroadsideRight:
                if not localAvatar.ship.broadside:
                    greyOut = 1

            range = localAvatar.cr.battleMgr.getModifiedRechargeTime(localAvatar, skillId)
            value = localAvatar.skillDiary.getTimeSpentRecharging(skillId)
            if not value:
                value = range
            elif value >= range:
                if self.rstatus[count] == 3:
                    startScale = self.rframe[count].getScale()
                    startColor = Vec4(1, 1, 1, 1)
                    glowColor = Vec4(0.0, 0.75, 0.0, 1.0)
                    buttomFrame = self.rframe[count]

            self.rframe[count].update(value, range)
            if value < range:
                greyOut = 3
            
            if self.rep == InventoryType.DollRep:
                haveFriendly = localAvatar.getFriendlyStickyTargets()
                haveHostile = localAvatar.getHostileStickyTargets()
                if haveFriendly and not haveHostile:
                    if not WeaponGlobals.isFriendlyFire(self.radialSkillMap[count - 1]):
                        greyOut = 1
                    
                elif not haveFriendly and haveHostile:
                    if WeaponGlobals.isFriendlyFire(self.radialSkillMap[count - 1]):
                        greyOut = 1

            if self.rstatus[count] != greyOut:
                self.rstatus[count] = greyOut
                if greyOut == 2:
                    self.radial[count].setColorScale(0.7, 0.7, 0.7, 1.0)
                elif greyOut == 1:
                    self.radial[count].setColorScale(0.4, 0.4, 0.4, 1.0)
                    self.rframe[count].meterFaceHalf1.setColorScale(0.4, 0.4, 0.4, 1.0)
                    self.rframe[count].meterFaceHalf2.setColorScale(0.4, 0.4, 0.4, 1.0)
                elif greyOut == 3:
                    self.radial[count].setColorScale(0.4, 0.4, 0.4, 1.0)
                else:
                    self.radial[count].setColorScale(1, 1, 1, 1)
                    self.radial[count].setAlphaScale(1)
                    self.rframe[count].meterFaceHalf1.setColorScale(1, 1, 1, 1.0)
                    self.rframe[count].meterFaceHalf2.setColorScale(1, 1, 1, 1.0)

        return Task.cont

    def destroy(self):
        if self.numberOfItems < 0:
            return
        
        taskMgr.remove('radialMenuHeartBeat')
        for i in range(self.numberOfItems + 1):
            if i != 0 and len(self.ammoAmt):
                self.ammoAmt[i].destroy()
            
            self.radial[i].destroy()
            self.rframe[i].destroy()
        
        del self.radial
        del self.rframe
        del self.ammoAmt
        del self.rstatus
        self.radialHelp.destroy()
        del self.radialHelp
        self.numberOfItems = -1
        localAvatar.endTrackTarget()
        localAvatar.guiMgr.setSeaChestAllowed(True)
    
    def radialMenuRelease(self):
        localAvatar.cr.targetMgr.reticle.show()
        if base.mouseWatcherNode.hasMouse():
            mouseData = base.win.getPointer(0)
            self.mouseFinalPosX = mouseData.getX()
            self.mouseFinalPosY = mouseData.getY()
        else:
            self.mouseFinalPosX = 0
            self.mouseFinalPosY = 0
        difX = self.mouseFinalPosX - self.mouseBasePosX
        difY = self.mouseFinalPosY - self.mouseBasePosY
        hLItem = RingMatch(self.numberOfItems, difX, difY)
        return hLItem



class SkillTray:
    SkillIcons = None
    MeterFrame = None
    
    def __init__(self):
        if not self.SkillIcons:
            self.SkillIcons = loader.loadModel('models/textureCards/skillIcons')
            self.MeterFrame = loader.loadModel('models/gui/ship_battle')
        
        self.tray = {}
        self.origMap = {}
        self.traySkillMap = None
        self.skillTrayState = False
        self.rep = None
        self.weaponMode = None
        self.callback = None
        self.numberOfItems = 0
        self.repMeter = None
        self.skillRechargedSound = base.loader.loadSfx('audio/sword-swoosh2.mp3')
        self.skillTray = DirectFrame(parent = base.a2dBottomCenter, pos = (0, 0, -0.12), scale = 0.9, sortOrder = 2)
        self.hide()
        moveUp = 0.25
        skillTrayZ = self.skillTray.getZ()
        self.showSkillTrayIval = Sequence(Func(self.show), LerpFunc(self.skillTray.setZ, 0.25, skillTrayZ, moveUp + skillTrayZ))
        self.hideSkillTrayIval = Sequence(LerpFunc(self.skillTray.setZ, 0.25, moveUp + skillTrayZ, skillTrayZ), Func(self.hide))
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.lockArt = gui.find('**/subscribers_lock')

    def show(self):
        self.skillTray.show()
    
    def hide(self):
        self.skillTray.hide()

    def showSkillTray(self, task = None):
        if localAvatar.isWeaponDrawn == False:
            if localAvatar.gameFSM.state != 'ShipPilot' and not localAvatar.cannon:
                return

        if self.skillTrayState:
            return
        else:
            self.skillTrayState = True
        if self.showSkillTrayIval.isPlaying():
            self.showSkillTrayIval.pause()
        
        if self.hideSkillTrayIval.isPlaying():
            self.hideSkillTrayIval.pause()
        
        self.showSkillTrayIval.start()

    def hideSkillTray(self):
        if not self.skillTrayState:
            return
        else:
            self.skillTrayState = False
        if self.showSkillTrayIval.isPlaying():
            self.showSkillTrayIval.pause()
        
        if self.hideSkillTrayIval.isPlaying():
            self.hideSkillTrayIval.pause()
        
        self.hideSkillTrayIval.start()

    def updateSkillTrayMeter(self):
        if not self.traySkillMap:
            return
        
        inv = base.localAvatar.getInventory()
        reputation = inv.getReputation(self.rep)
        self.repMeter.setCategory(self.rep)
        self.repMeter.update(reputation, playFX = True)

    def rebuildSkillTray(self, rep = None, weaponMode = None, callback = None):
        if not rep:
            rep = self.rep
        
        if not weaponMode:
            weaponMode = self.weaponMode
        
        if not callback:
            callback = self.callback
        
        if rep is None:
            return
        
        self.updateSkillTray(rep, weaponMode, callback, hideFirst = False)
    
    def updateSkillTray(self, rep, weaponMode, callback = None, hideFirst = True):
        if rep == InventoryType.MeleeRep:
            return
        
        if not callback:
            callback = localAvatar.guiMgr.combatTray.triggerSkillTraySkill
        
        if taskMgr.hasTaskNamed('updateSkillTray'):
            taskMgr.remove('updateSkillTray')
        
        if self.skillTrayState and hideFirst:
            self.hideSkillTray()
            taskMgr.doMethodLater(0.75, self.updateSkillTray, 'updateSkillTray', extraArgs = [
                rep,
                weaponMode,
                callback])
            return
        
        text = PLocalizer.InventoryTypeNames.get(rep, 'Unknown')
        for i in range(self.numberOfItems):
            self.tray[i + 1].destroy()
            self.repMeter.destroy()
        
        self.rep = rep
        self.weaponMode = weaponMode
        self.callback = callback
        skillMap = []
        self.origMap = getAllSkills(self.rep, 2)
        for i in range(len(self.origMap)):
            skillMap.append(self.origMap[i][0])
        
        self.traySkillMap = skillMap
        self.numberOfItems = len(self.traySkillMap)
        self.skillTray.setX(0)
        self.repMeter = ReputationMeter(self.rep, width = 0.7)
        self.repMeter.setScale(1.15, 1.15, 1.15)
        self.repMeter.reparentTo(self.skillTray)
        self.repMeter.setCategory(self.rep)
        inv = base.localAvatar.getInventory()
        if inv is None:
            return
        
        self.repMeter.update(inv.getReputation(self.rep))
        x = 0.0
        offset = 0.0
        for i in range(self.numberOfItems):
            if self.origMap[i][1] == False:
                locked = self.origMap[i][2]
                if locked:
                    image = (self.SkillIcons.find('**/base'), self.SkillIcons.find('**/base_down'), self.SkillIcons.find('**/base_over'))
                else:
                    image = self.SkillIcons.find('**/base')
                button = DirectButton(parent = self.skillTray, relief = None, state = DGG.DISABLED, image = image, image_pos = (0.0, 0.0, 0.06), image_scale = 0.12, image_color = (0.2, 0.2, 0.2, 0.55), sortOrder = 100, pos = (x, 0, -0.04))
                button.setTransparency(1)
                button.showQuantity = False
                button.greyOut = -1
                button.showRing = False
                button.skillStatus = False
                if locked:
                    lock = DirectFrame(parent = button, relief = None, image = self.lockArt, image_scale = 0.14, image_pos = (0.05, 0, 0.035))
                    button['state'] = DGG.NORMAL
                    button['command'] = base.localAvatar.guiMgr.showNonPayer
                    button['extraArgs'] = [
                        'Restricted_Radial_Menu',
                        5]
                
                self.tray[i + 1] = button
                x = x + 0.16
                if i < self.numberOfItems - 1:
                    offset = offset + 0.01
                    self.skillTray.setX(self.skillTray.getX() - 0.08)

            if self.origMap[i][1] == True:
                skillId = self.traySkillMap[i]
                name = PLocalizer.InventoryTypeNames[skillId]
                hotkey = str(i + 1)
                totalRechargeTime = base.cr.battleMgr.getModifiedRechargeTime(localAvatar, skillId)
                timeSpentRecharging = localAvatar.skillDiary.getTimeSpentRecharging(skillId)
                if not timeSpentRecharging:
                    timeSpentRecharging = 0
                
                if weaponMode not in (WeaponGlobals.CANNON, WeaponGlobals.FIREARM, WeaponGlobals.GRENADE, WeaponGlobals.STAFF):
                    showRing = True
                else:
                    showRing = False
                locked = self.origMap[i][2]
                button = SkillButton(skillId, self.callback, 0, 0, showQuantity = False, showHelp = False, showRing = showRing, hotkey = hotkey, name = name, showLock = locked)
                button.skillStatus = True
                if locked:
                    button.skillButton['command'] = base.localAvatar.guiMgr.showNonPayer
                    button.skillButton['extraArgs'] = [
                        'Restricted_Radial_Menu',
                        5]
                
                if showRing:
                    button.skillRing.meterFaceHalf1.setScale(0.96)
                    button.skillRing.meterFaceHalf2.setScale(0.96)
                
                button.reparentTo(self.skillTray)
                button.setPos(x, 0, 0.035)
                self.tray[i + 1] = button
                if weaponMode in (WeaponGlobals.FIREARM, WeaponGlobals.GRENADE, WeaponGlobals.STAFF):
                    lastAmmo = localAvatar.guiMgr.combatTray.lastAmmoSkillId.get(localAvatar.currentWeaponId)
                    if lastAmmo is not None:
                        if lastAmmo == skillId:
                            button.toggleButton(True)
                        
                    elif self.tray[1].skillStatus is True:
                        self.tray[1].toggleButton(True)

                if self.weaponMode in (WeaponGlobals.FIREARM, WeaponGlobals.THROWING, WeaponGlobals.CANNON, WeaponGlobals.GRENADE):
                    inv = localAvatar.getInventory()
                    maxQuant = WeaponGlobals.getSkillMaxQuantity(skillId)
                    if maxQuant == WeaponGlobals.INF_QUANT:
                        ammoAmt = WeaponGlobals.INF_QUANT
                    else:
                        ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(skillId)
                        ammoAmt = inv.getStackQuantity(ammoInvId)
                        ammoMax = inv.getStackLimit(ammoInvId)
                        button.showQuantity = True
                        button.updateQuantity(ammoAmt)
                
                x = x + 0.18
                if i < self.numberOfItems - 1:
                    self.skillTray.setX(self.skillTray.getX() - 0.09)

        currentX = self.skillTray.getX()
        self.skillTray.setX(currentX + float(offset))
        self.repMeter.setPos(-currentX, 0.0, -0.11)
        self.updateSkillTrayStates()
        self.showSkillTray()

    def updateSkillTrayStates(self):
        if not self.traySkillMap:
            return
        
        if not hasattr(base, 'localAvatar'):
            return
        
        inv = localAvatar.getInventory()
        if not inv:
            return
        
        self.numberOfItems = len(self.traySkillMap)
        for i in range(self.numberOfItems):
            skillId = self.traySkillMap[i]
            greyOut = 0
            if self.tray[i + 1].greyOut == -1:
                continue
            
            if self.tray[i + 1].showQuantity:
                maxQuant = WeaponGlobals.getSkillMaxQuantity(skillId)
                if maxQuant == WeaponGlobals.INF_QUANT:
                    quantity = WeaponGlobals.INF_QUANT
                else:
                    ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(skillId)
                    quantity = inv.getStackQuantity(ammoInvId)
                if quantity == 0:
                    greyOut = 1

            if localAvatar.mojo < -1 * WeaponGlobals.getMojoCost(skillId):
                greyOut = 1
            
            if localAvatar.ship:
                pass
            else:
                if skillId == InventoryType.SailBroadsideLeft or skillId == InventoryType.SailBroadsideRight:
                    if not localAvatar.ship.broadside:
                        greyOut = 1

            rep = WeaponGlobals.getSkillReputationCategoryId(skillId)
            if rep == InventoryType.DollRep:
                haveFriendly = localAvatar.getFriendlyStickyTargets()
                haveHostile = localAvatar.getHostileStickyTargets()
                if haveFriendly and not haveHostile:
                    if not WeaponGlobals.isFriendlyFire(skillId):
                        greyOut = 1
                    
                elif not haveFriendly and haveHostile:
                    if WeaponGlobals.isFriendlyFire(skillId):
                        greyOut = 1

            if self.tray[i + 1].greyOut != greyOut:
                if hasattr(self.tray[i + 1], 'skillButton'):
                    self.tray[i + 1].greyOut = greyOut
                    if greyOut == 1:
                        self.tray[i + 1].setGeomColor(0.5, 0.5, 0.5, 1.0)
                        if self.tray[i + 1].showRing:
                            self.tray[i + 1].skillRing.meterFaceHalf1.setColorScale(0.4, 0.4, 0.4, 1.0)
                            self.tray[i + 1].skillRing.meterFaceHalf2.setColorScale(0.4, 0.4, 0.4, 1.0)
                        
                    elif greyOut == 2:
                        self.tray[i + 1].setGeomColor(0.5, 0.5, 0.5, 1.0)
                    elif greyOut == 3:
                        self.tray[i + 1].setGeomColor(0.5, 0.5, 0.5, 1.0)
                    else:
                        self.tray[i + 1].setGeomColor(1, 1, 1, 1)
                        if self.tray[i + 1].showRing:
                            self.tray[i + 1].skillRing.meterFaceHalf1.clearColorScale()
                            self.tray[i + 1].skillRing.meterFaceHalf2.clearColorScale()

    def callback(self, skillId):
        localAvatar.guiMgr.combatTray.trySkill(InventoryType.UseItem, skillId, 0)

    def decrementSkillTrayAmount(self, skillId, amt = 1):
        if not self.traySkillMap:
            return
        
        if self.weaponMode not in (WeaponGlobals.FIREARM, WeaponGlobals.THROWING, WeaponGlobals.CANNON, WeaponGlobals.GRENADE):
            return
        
        if not hasattr(base, 'localAvatar'):
            return
        
        self.numberOfItems = len(self.traySkillMap)
        for i in range(self.numberOfItems):
            if self.tray[i + 1].greyOut == -1:
                continue
            
            if self.tray[i + 1].showQuantity:
                if skillId == self.traySkillMap[i]:
                    currentAmt = self.tray[i + 1].quantity
                    newAmt = currentAmt - amt
                    if newAmt >= 0:
                        self.tray[i + 1].updateQuantity(newAmt)
                        if newAmt == 0:
                            self.tray[i + 1].setGeomColor(0.5, 0.5, 0.5, 1.0)
                            if self.tray[i + 1].showRing:
                                self.tray[i + 1].skillRing.meterFaceHalf1.setColorScale(0.4, 0.4, 0.4, 1.0)
                                self.tray[i + 1].skillRing.meterFaceHalf2.setColorScale(0.4, 0.4, 0.4, 1.0)

                        return

    def updateSkillTrayAmounts(self):
        if not self.traySkillMap:
            return
        
        if self.weaponMode not in (WeaponGlobals.FIREARM, WeaponGlobals.THROWING, WeaponGlobals.CANNON, WeaponGlobals.GRENADE):
            return
        
        if not hasattr(base, 'localAvatar'):
            return
        
        inv = localAvatar.getInventory()
        if not inv:
            return
        
        self.numberOfItems = len(self.traySkillMap)
        for i in range(self.numberOfItems):
            if self.tray[i + 1].greyOut == -1:
                continue
            
            skillId = self.traySkillMap[i]
            maxQuant = WeaponGlobals.getSkillMaxQuantity(skillId)
            if maxQuant == WeaponGlobals.INF_QUANT:
                ammoAmt = WeaponGlobals.INF_QUANT
            else:
                ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(skillId)
                ammoAmt = inv.getStackQuantity(ammoInvId)
                ammoMax = inv.getStackLimit(ammoInvId)
            self.tray[i + 1].updateQuantity(ammoAmt)

    def updateSkillIval(self, skillId):
        for button in self.tray:
            if isinstance(self.tray[button], SkillButton):
                if not self.tray[button].isEmpty() and self.tray[button].skillId == skillId:
                    self.tray[button].skillRingIval.isPlaying() or self.tray[button].skillRingIval.start()

    def addPowerRechargeEffect(self):
        for button in self.tray:
            if isinstance(self.tray[button], SkillButton):
                if not self.tray[button].isEmpty() and (WeaponGlobals.getIsShipSkill(self.tray[button].skillId) or WeaponGlobals.getIsCannonSkill(self.tray[button].skillId)) and self.tray[button].skillId != InventoryType.SailPowerRecharge:
                    self.tray[button].quickGlowImpulse()
                    self.tray[button].startPowerImpulse()
                    self.tray[button].updateSkillRingIval()

    def continuePowerRechargeEffect(self):
        for button in self.tray:
            if isinstance(self.tray[button], SkillButton):
                if not self.tray[button].isEmpty() and (WeaponGlobals.getIsShipSkill(self.tray[button].skillId) or WeaponGlobals.getIsCannonSkill(self.tray[button].skillId)) and self.tray[button].skillId != InventoryType.SailPowerRecharge:
                    self.tray[button].startPowerImpulse()

    def removePowerRechargeEffect(self):
        for button in self.tray:
            if isinstance(self.tray[button], SkillButton):
                if not self.tray[button].isEmpty() and (WeaponGlobals.getIsShipSkill(self.tray[button].skillId) or WeaponGlobals.getIsCannonSkill(self.tray[button].skillId)) and self.tray[button].skillId != InventoryType.SailPowerRecharge:
                    self.tray[button].stopPowerImpulse()
                    self.tray[button].updateSkillRingIval()
    
    def destroy(self):
        self.hideSkillTray()
        self.skillTray.destroy()
        if self.repMeter:
            self.repMeter.destroy()
        
        for i in range(self.numberOfItems):
            self.tray[i + 1].destroy()
        
        del self.tray
        del self.callback
        if self.showSkillTrayIval:
            self.showSkillTrayIval.pause()
            self.showSkillTrayIval = None
        
        if self.hideSkillTrayIval:
            self.hideSkillTrayIval.pause()
            self.hideSkillTrayIval = None
        


