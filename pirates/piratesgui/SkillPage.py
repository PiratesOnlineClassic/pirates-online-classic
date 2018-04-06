# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.SkillPage
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from otp.otpgui import OTPDialog
from pandac.PandaModules import *
from pirates.battle import WeaponGlobals
from pirates.piratesbase import Freebooter, PiratesGlobals, PLocalizer
from pirates.piratesgui import (InventoryPage, PDialog, PiratesGuiGlobals,
                                RadialMenu, SkillpageGuiButton)
from pirates.piratesgui.ReputationMeter import ReputationMeter
from pirates.piratesgui.SkillButton import SkillButton
from pirates.reputation import ReputationGlobals
from pirates.uberdog.UberDogGlobals import (InventoryCategory, InventoryId,
                                            InventoryType)

MAX_REP = 6

class SkillPage(InventoryPage.InventoryPage):
    __module__ = __name__
    MAX_UPGRADE_DOTS = 5
    EXCLUDED_SKILLS = [
     InventoryType.CannonGrappleHook]
    notify = DirectNotifyGlobal.directNotify.newCategory('SkillPage')
    SkillIcons = None
    WeaponIcons = None
    TopGui = None
    DotTex = None
    FrameTex = None

    def __init__(self):
        if not SkillPage.SkillIcons:
            SkillPage.SkillIcons = loader.loadModel('models/textureCards/skillIcons')
            SkillPage.WeaponIcons = loader.loadModel('models/textureCards/weapon_icons')
            SkillPage.DotTex = SkillPage.SkillIcons.find('**/skill_tree_level_dot')
            SkillPage.FrameTex = SkillPage.SkillIcons.find('**/skill_tree_level_ring')
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(SkillPage)
        self.tabBar = None
        self.currentRep = InventoryType.CannonRep
        self.skillFrames = {}
        self.dots = {}
        self.lastUserSelectedTab = None
        self.dataChanged = True
        self.spentDialog = None
        self.localMods = {}
        ornament = loader.loadModel('models/gui/gui_skill_window')
        ornament.find('**/pPlane81').detachNode()
        ornament.find('**/pPlane83').detachNode()
        ornament.find('**/pPlane84').detachNode()
        ornament.find('**/pPlane93').detachNode()
        ornament.setScale(0.325, 0, 0.32)
        ornament.setPos(0.54, 0, 0.72)
        ornament.flattenStrong()
        ornament.reparentTo(self)
        self.box = box = loader.loadModel('models/gui/gui_title_box').find('**/gui_title_box_top')
        box.setPos(0.55, 0, 1.26)
        box.setScale(0.325, 0.0, 0.25)
        box.reparentTo(ornament)
        ornament.flattenStrong()
        self.repMeter = ReputationMeter(self.getRep(), width=0.7)
        self.repMeter.reparentTo(self)
        self.repMeter.setPos(0.55, 0, 1.24)
        self.unspent = DirectLabel(parent=self, relief=None, text=PLocalizer.SkillPageUnspentPoints % 0, text_scale=0.04, text_align=TextNode.ACenter, text_pos=(0, -0.01), text_fg=(1,
                                                                                                                                                                                     1,
                                                                                                                                                                                     1,
                                                                                                                                                                                     1), pos=(0.8,
                                                                                                                                                                                              0,
                                                                                                                                                                                              0.02))
        return

    def destroy(self):
        for spot in list(self.skillFrames.keys()):
            self.skillFrames[spot].destroy()

        if self.tabBar:
            self.tabBar.destroy()
            self.tabBar = None
        self.__handleFreeDialog()
        InventoryPage.InventoryPage.destroy(self)
        return

    def __handleFreeDialog(self, value=None):
        if self.spentDialog:
            self.spentDialog.destroy()
            self.spentDialog = None
        return

    def createTabs(self):
        repIds = [
         InventoryType.CannonRep, InventoryType.SailingRep]
        for weaponId in localAvatar.equippedWeapons:
            if weaponId:
                repIds.append(WeaponGlobals.getRepId(weaponId))

        for repId in repIds:
            if not self.tabBar.getTab(str(repId)):
                self.createTab(repId)

    def createTab(self, repId):
        newTab = self.tabBar.addTab(str(repId), frameSize=(-0.12, 0.12, -0.11, 0.11), focusSize=(-0.12, 0.12, -0.12, 0.12), heightFactor=0.55, command=self.update, extraArgs=[repId, 1])
        if repId == InventoryType.SailingRep:
            model = SkillPage.SkillIcons
        else:
            model = SkillPage.WeaponIcons
        asset = ReputationGlobals.RepIcons.get(repId)
        image = model.find('**/%s' % asset)
        name = PLocalizer.InventoryTypeNames[repId]
        newTab.nameTag = DirectLabel(parent=newTab, relief=None, state=DGG.DISABLED, image=image, image_scale=0.1, image_color=Vec4(0.8, 0.8, 0.8, 1), pos=(0,
                                                                                                                                                            0,
                                                                                                                                                            0))

        def mouseOver(tab=newTab):
            tab.nameTag.setScale(1.1)
            tab.nameTag['image_color'] = Vec4(1, 1, 1, 1)
            base.playSfx(PiratesGuiGlobals.getDefaultRolloverSound())

        def mouseOff(tab=newTab):
            if not tab['selected']:
                tab.nameTag.setScale(1.0)
                tab.nameTag['image_color'] = Vec4(0.8, 0.8, 0.8, 1)
            else:
                mouseOver(tab)

        newTab['mouseEntered'] = mouseOver
        newTab['mouseLeft'] = mouseOff
        return

    def show(self):
        if self.tabBar == None:
            self.tabBar = localAvatar.guiMgr.chestPanel.makeTabBar()
        else:
            self.tabBar.unstash()
        self.createTabs()
        InventoryPage.InventoryPage.show(self)
        self.update()
        return

    def update(self, repId=None, fromUser=0):
        inv = localAvatar.getInventory()
        if not inv:
            self.notify.warning('SkillPage unable to find inventory')
            return
        if self.tabBar == None:
            return
        if fromUser:
            self.lastUserSelectedTab = repId
        if repId == None:
            if localAvatar.cannon:
                repId = InventoryType.CannonRep
            elif localAvatar.gameFSM.state == 'ShipPilot':
                repId = InventoryType.SailingRep
            elif localAvatar.currentWeaponId and localAvatar.isWeaponDrawn:
                repId = WeaponGlobals.getRepId(localAvatar.currentWeaponId)
            elif localAvatar.currentWeaponId and not localAvatar.isWeaponDrawn and self.lastUserSelectedTab:
                repId = self.lastUserSelectedTab
            else:
                repId = InventoryType.CannonRep
        self.setRep(repId)
        self.tabBar.selectTab(str(repId))
        self.repMeter.setCategory(repId)
        self.repMeter.update(inv.getReputation(repId))
        unSpentId = self.getUnspent()
        amt = inv.getStackQuantity(unSpentId)
        if unSpentId in self.localMods:
            amt = self.localMods[unSpentId]
        self.unspent['text'] = PLocalizer.SkillPageUnspentPoints % amt
        if amt > 0:
            self.unspent['text_fg'] = (0.8, 1, 0.8, 1)
        else:
            self.unspent['text_fg'] = (1, 1, 1, 1)
        comboSkills = RadialMenu.ComboSkills(repId, 1)
        totalComboSkills = RadialMenu.ComboSkills(repId, 0)
        activeSkills = RadialMenu.ActiveSkills(repId, 1)
        totalActiveSkills = RadialMenu.ActiveSkills(repId, 0)
        passiveSkills = RadialMenu.PassiveSkills(repId, 1)
        totalPassiveSkills = RadialMenu.PassiveSkills(repId, 0)
        for excludedSkillId in self.EXCLUDED_SKILLS:
            for skillId in activeSkills:
                if excludedSkillId == skillId:
                    activeSkills.remove(skillId)
                    totalActiveSkills.remove(skillId)

        for spot in list(self.skillFrames.keys()):
            if spot not in totalComboSkills:
                self.skillFrames[spot].hide()

        count = 0
        for skill in totalComboSkills:
            skillPts = inv.getStackQuantity(skill)
            if skill in self.localMods:
                skillPts = self.localMods[skill]
            showIcon = skill in comboSkills or skillPts > 0
            freeLock = False
            if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                if not WeaponGlobals.canFreeUse(skill):
                    freeLock = True
            self.createFrame(skill, skillPts, amt, freeLock, showIcon)
            x = 0.2 + 0.175 * count
            y = 1.11
            self.skillFrames[skill].setPos(x, 0, y)
            if showIcon and skillPts > 1:
                self.makeDots(skill, skillPts - 1)
            if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                if not WeaponGlobals.canFreeUse(skill):
                    self.skillFrames[skill].skillButton['command'] = base.localAvatar.guiMgr.showNonPayer
                    self.skillFrames[skill].skillButton['extraArgs'] = ['Restricted_Skill_' + WeaponGlobals.getSkillName(skill), 5]
            count += 1

        count = 0
        for skill in totalActiveSkills:
            skillPts = inv.getStackQuantity(skill)
            if skill in self.localMods:
                skillPts = self.localMods[skill]
            xMod, yMod = self.ringOffset(count)
            xMod *= 0.9
            yMod *= 0.9
            showIcon = skill in activeSkills or skillPts > 0
            freeLock = False
            if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                if not WeaponGlobals.canFreeUse(skill):
                    freeLock = True
            self.createFrame(skill, skillPts, amt, freeLock, showIcon)
            x = xMod + 0.53
            y = yMod + 0.615
            self.skillFrames[skill].setPos(x, 0, y)
            if showIcon and skillPts > 1:
                self.makeDots(skill, skillPts - 1)
            if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                if not WeaponGlobals.canFreeUse(skill):
                    self.skillFrames[skill].skillButton['command'] = base.localAvatar.guiMgr.showNonPayer
                    self.skillFrames[skill].skillButton['extraArgs'] = ['Restricted_Skill_' + WeaponGlobals.getSkillName(skill), 5]
            ammo = self.getAmmo(skill)
            if ammo != None and showIcon:
                self.skillFrames[skill].showQuantity = True
                self.skillFrames[skill].updateQuantity(ammo)
            count += 1

        count = 0
        for skill in totalPassiveSkills:
            skillPts = inv.getStackQuantity(skill)
            if skill in self.localMods:
                skillPts = self.localMods[skill]
            showIcon = skill in passiveSkills or skillPts > 0
            freeLock = False
            if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                if not WeaponGlobals.canFreeUse(skill):
                    freeLock = True
            self.createFrame(skill, skillPts, amt, freeLock, showIcon)
            x = 0.2 + 0.175 * count
            y = 0.15
            self.skillFrames[skill].setPos(x, 0, y)
            if showIcon and skillPts > 1:
                self.makeDots(skill, skillPts - 1)
            if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                if not WeaponGlobals.canFreeUse(skill):
                    self.skillFrames[skill].skillButton['command'] = base.localAvatar.guiMgr.showNonPayer
                    self.skillFrames[skill].skillButton['extraArgs'] = ['Restricted_Skill_' + WeaponGlobals.getSkillName(skill), 5]
            count += 1

        self.dataChanged = False
        return

    def hide(self):
        if self.tabBar:
            self.tabBar.stash()
        InventoryPage.InventoryPage.hide(self)

    def makeDots(self, skillId, points):
        if skillId == InventoryType.SailPowerRecharge:
            return
        if skillId not in self.dots:
            self.dots[skillId] = {}
            buildNew = True
        else:
            buildNew = False
        for i in range(self.MAX_UPGRADE_DOTS):
            if i in self.dots[skillId]:
                if points > 0:
                    self.dots[skillId][i].show()
            else:
                if skillId in self.skillFrames:
                    self.dots[skillId][i] = DirectFrame(parent=self.skillFrames[skillId], relief=None, image=SkillPage.FrameTex, image_scale=0.029)
                    if i == 0:
                        self.dots[skillId][i].setPos(-0.0736, 0, 0.0)
                    else:
                        if i == 1:
                            self.dots[skillId][i].setPos(-0.0637, 0, -0.0368)
                        else:
                            if i == 2:
                                self.dots[skillId][i].setPos(-0.0368, 0, -0.0637)
                            else:
                                if i == 3:
                                    self.dots[skillId][i].setPos(0.0, 0, -0.0736)
                                else:
                                    if i == 4:
                                        self.dots[skillId][i].setPos(0.0368, 0, -0.0637)
                    self.dots[skillId][i].setColorScale(1, 1, 1, 0.7)
            dotNum = i + self.MAX_UPGRADE_DOTS
            if i < points:
                if dotNum in self.dots[skillId]:
                    self.dots[skillId][dotNum].show()
                else:
                    self.dots[skillId][dotNum] = DirectFrame(parent=self.dots[skillId][i], relief=None, image=SkillPage.DotTex, image_scale=0.02)
                    self.dots[skillId][dotNum].setColorScaleOff()
            elif dotNum in self.dots[skillId]:
                self.dots[skillId][dotNum].hide()

        return

    def addPoint(self, skillId):
        if skillId == InventoryType.SailPowerRecharge:
            return
        inv = localAvatar.getInventory()
        if self.currentRep == InventoryType.CutlassRep and localAvatar.style.tutorial < PiratesGlobals.TUT_GOT_CUTLASS:
            if inv.getStackQuantity(InventoryType.CutlassSweep) < 2:
                if skillId != InventoryType.CutlassSweep:
                    return
            elif skillId == InventoryType.CutlassSweep:
                messenger.send('skillImprovementAttempted')
        unSpentId = self.getUnspent()
        unSp = inv.getStackQuantity(unSpentId)
        if unSpentId in self.localMods:
            unSp = self.localMods[unSpentId]
        if unSp < 1:
            return
        if inv.getStackLimit(skillId):
            curAmt = inv.getStackQuantity(skillId)
            if skillId in self.localMods:
                curAmt = self.localMods[skillId]
            if curAmt > 5:
                return
            else:
                curAmt += 1
        else:
            return
        self.__handleFreeDialog()
        if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
            if curAmt > Freebooter.FreeSkillCap:
                self.spentDialog = PDialog.PDialog(text=PLocalizer.FreebooterSkillMax, style=OTPDialog.CancelOnly, command=self.__handleFreeDialog)
                return
            playerExp = inv.getAccumulator(self.currentRep)
            categoryLevel, extra = ReputationGlobals.getLevelFromTotalReputation(self.currentRep, playerExp)
            alreadySpent = categoryLevel - 1 - unSp
            if alreadySpent > 5:
                self.spentDialog = PDialog.PDialog(text=PLocalizer.FreebooterSkillLock, style=OTPDialog.CancelOnly, command=self.__handleFreeDialog)
                return
        if not base.config.GetBool('want-combo-skips', 0):
            comboSkills = [
             InventoryType.CutlassSlash, InventoryType.CutlassCleave, InventoryType.CutlassFlourish, InventoryType.CutlassStab, InventoryType.DaggerSwipe, InventoryType.DaggerGouge, InventoryType.DaggerEviscerate]
            if skillId in comboSkills and inv.getStackQuantity(skillId - 1) <= 1:
                base.localAvatar.guiMgr.createWarning(PLocalizer.ComboOrderWarn, PiratesGuiGlobals.TextFG6)
                return
        messenger.send('skillImprovementAttempted')
        localAvatar.spendSkillPoint(skillId)
        self.localMods[skillId] = curAmt
        self.localMods[unSpentId] = unSp - 1
        self.skillFrames[skillId].skillRank = curAmt - 1

    def createFrame(self, skillId, skillPts, upgradeMode=0, freeLock=False, showIcon=True):
        skillRank = max(0, skillPts - 1)
        if skillId in self.skillFrames:
            button = self.skillFrames[skillId]
            showUpgrade = upgradeMode and showIcon
            button.setShowUpgrade(showUpgrade)
            button.setShowIcon(showIcon)
            button.setShowLock(freeLock)
            button.show()
        else:
            button = SkillButton(skillId, self.addPoint, 0, skillRank, showHelp=True, showIcon=showIcon, showLock=freeLock)
            showUpgrade = upgradeMode and showIcon
            button.setShowUpgrade(showUpgrade)
            button.reparentTo(self)
            self.skillFrames[skillId] = button
        button.skillButton['image_scale'] = 0.12
        if skillPts == 1:
            self.skillFrames[skillId]['text_fg'] = (0.5, 0.5, 0.5, 1)
            self.skillFrames[skillId].skillButton.setColorScale(1, 1, 1, 0.5)
        else:
            self.skillFrames[skillId]['text_fg'] = (1, 1, 1, 1)
            self.skillFrames[skillId].skillButton.clearColorScale()

    def getAmmo(self, skillId):
        ammoId = WeaponGlobals.getSkillAmmoInventoryId(skillId)
        if ammoId == None:
            return
        else:
            amount = localAvatar.getInventory().getStackQuantity(ammoId)
            return amount
        return

    def setRep(self, repId):
        self.currentRep = repId

    def getRep(self):
        return self.currentRep

    def updateUnspent(self, category, value):
        if category in self.localMods:
            del self.localMods[category]
        self.dataChanged = True
        self.update(self.currentRep)

    def updateSkillUnlock(self, skillId):
        self.dataChanged = True
        self.update(self.currentRep)

    def getUnspent(self):
        if self.currentRep == InventoryType.CutlassRep:
            return InventoryType.UnspentCutlass
        else:
            if self.currentRep == InventoryType.DaggerRep:
                return InventoryType.UnspentDagger
            else:
                if self.currentRep == InventoryType.PistolRep:
                    return InventoryType.UnspentPistol
                else:
                    if self.currentRep == InventoryType.GrenadeRep:
                        return InventoryType.UnspentGrenade
                    else:
                        if self.currentRep == InventoryType.DollRep:
                            return InventoryType.UnspentDoll
                        else:
                            if self.currentRep == InventoryType.WandRep:
                                return InventoryType.UnspentWand
                            else:
                                if self.currentRep == InventoryType.SailingRep:
                                    return InventoryType.UnspentSailing
                                else:
                                    return InventoryType.UnspentCannon

    def ringOffset(self, num):
        if num == 0:
            return (-0.175, 0.175)
        else:
            if num == 1:
                return (0.0, 0.25)
            else:
                if num == 2:
                    return (0.175, 0.175)
                else:
                    if num == 3:
                        return (0.25, 0.0)
                    else:
                        if num == 4:
                            return (0.175, -0.175)
                        else:
                            if num == 5:
                                return (0.0, -0.25)
                            else:
                                if num == 6:
                                    return (-0.175, -0.175)
                                else:
                                    if num == 7:
                                        return (-0.25, 0.0)

    def slideOpenPrecall(self):
        self.dataChanged = True
        self.update()

    def respec(self, weaponRep):
        listReset1 = InventoryType.StartingSkills
        begin = -1
        end = -1
        unSpentId = -1
        if weaponRep == InventoryType.CutlassRep:
            begin = InventoryType.begin_WeaponSkillCutlass
            end = InventoryType.end_WeaponSkillCutlass
            unSpentId = InventoryType.UnspentCutlass
        else:
            if weaponRep == InventoryType.PistolRep:
                begin = InventoryType.begin_WeaponSkillPistol
                end = InventoryType.end_WeaponSkillPistol
                unSpentId = InventoryType.UnspentPistol
            else:
                if weaponRep == InventoryType.DaggerRep:
                    begin = InventoryType.begin_WeaponSkillDagger
                    end = InventoryType.end_WeaponSkillDagger
                    unSpentId = InventoryType.UnspentDagger
                else:
                    if weaponRep == InventoryType.GrenadeRep:
                        begin = InventoryType.begin_WeaponSkillGrenade
                        end = InventoryType.end_WeaponSkillGrenade
                        unSpentId = InventoryType.UnspentGrenade
                    else:
                        if weaponRep == InventoryType.DollRep:
                            begin = InventoryType.begin_WeaponSkillDoll
                            end = InventoryType.end_WeaponSkillDoll
                            unSpentId = InventoryType.UnspentDoll
                        else:
                            if weaponRep == InventoryType.WandRep:
                                begin = InventoryType.begin_WeaponSkillWand
                                end = InventoryType.end_WeaponSkillWand
                                unSpentId = InventoryType.UnspentWand
                            else:
                                if weaponRep == InventoryType.SailingRep:
                                    begin = InventoryType.begin_SkillSailing
                                    end = InventoryType.end_SkillSailing
                                    unSpentId = InventoryType.UnspentSailing
                                else:
                                    if weaponRep == InventoryType.CannonRep:
                                        begin = InventoryType.begin_WeaponSkillCannon
                                        end = InventoryType.end_WeaponSkillCannon
                                        unSpentId = InventoryType.UnspentCannon
                                    else:
                                        return
        localAvatar.resetSkillPoints(weaponRep)
        inv = localAvatar.getInventory()
        extra = 0
        for skillId in range(begin, end):
            if skillId in InventoryType.DontResetSkills:
                continue
            curAmt = inv.getStackQuantity(skillId)
            if skillId in self.localMods:
                curAmt = self.localMods[skillId]
            resetAmt = 1
            if skillId in listReset1:
                resetAmt = 2
            if curAmt > resetAmt:
                extra += curAmt - resetAmt
                self.localMods[skillId] = resetAmt
                if self.tabBar and skillId in self.skillFrames:
                    self.skillFrames[skillId].skillRank = resetAmt - 1
                if self.tabBar:
                    try:
                        self.makeDots(skillId, resetAmt - 1)
                    except:
                        pass

                if resetAmt == 1 and self.tabBar:
                    try:
                        self.dots[skillId][0].hide()
                        self.dots[skillId][1].hide()
                        self.dots[skillId][2].hide()
                        self.dots[skillId][3].hide()
                        self.dots[skillId][4].hide()
                    except:
                        pass

        if unSpentId in self.localMods:
            self.localMods[unSpentId] += extra
# okay decompiling .\pirates\piratesgui\SkillPage.pyc
