# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.CrewPage
from direct.fsm import StateData
from direct.gui.DirectGui import *
from direct.showbase.ShowBaseGlobal import *
from direct.task import Task
from otp.otpbase import OTPGlobals
from panda3d.core import *
from pirates.band import BandConstance, DistributedBandMember
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import (CrewHUD, CrewIconSelector, CrewMatchInviter,
                                PirateButtonChain, PirateMemberList,
                                PiratesGuiGlobals, SocialPage)
from pirates.uberdog.UberDogGlobals import CrewStatus


class CrewPage(SocialPage.SocialPage):
    
    notify = directNotify.newCategory('CrewPage')

    def __init__(self):
        SocialPage.SocialPage.__init__(self, PLocalizer.CrewPageTitle)
        self.initialiseoptions(CrewPage)
        self.gui = loader.loadModel('models/gui/toplevel_gui')
        self.avatarPanel = None
        self.crewHUD = CrewHUD.CrewHUD()
        self.lookingForCrewButton = 0
        self.selectCrewIcon = 0
        self.clearCrewIcon = 0
        self.addCrewLookout = 0
        self.addAvatarToList = 0
        self.startACrewButton = 0
        self.crewButton = 0
        self.addAvatarToListPVP = 0
        self.crewHUDToggleButton = 0
        self.startACrewState = 0
        self.crew = {}
        self.crewIconSelection = 0
        self.icon = loader.loadModel('models/gui/compass_main')
        self.ring = loader.loadModel('models/gui/gui_main')
        self.recruitCrewMatesStatus = 0
        self.joinACrewStatus = 0
        self.joinACrewStatusPVP = 0
        self.accept('destroyCrewMatchInvite', self.deactivateCrewMatchInviteTeleport)
        self.accept(BandConstance.BandMemberHpChange, self.updateCrewMemberHp)
        self.accept(BandConstance.BandMemberShipChange, self.updateCrewMemberShip)
        self.mainFrame = DirectFrame(relief=None, parent=self)
        self.optionsFrame = DirectFrame(relief=None, parent=self)
        self.membersList = PirateMemberList.PirateMemberList(6, self.mainFrame, 'FOOLIO HC', height=0.5475, memberHeight=0.08, memberWidth=0.48, memberOffset=0.04, bottom=0.074)
        self.membersList.setPos(0.001, 0.0, 0.123)
        self.chain = PirateButtonChain.PirateButtonChain(0.49, self.mainFrame, True)
        self.chain.setPos(-0.012, 0.0, 0.045)
        self.optionsChain = PirateButtonChain.PirateButtonChain(0.49, self.optionsFrame, True)
        self.optionsChain.setPos(-0.012, 0.0, 0.045)
        self.optionsChain.hide()
        self.optionsChain.setPos(-0.012, 0.0, 0.045)
        self.optionsChain.hide()
        self.load()
        self.accept(BandConstance.BandMembershipChange, self.DoUpdateCrewData)
        self.headingLabel = DirectLabel(parent=self, relief=None, state=DGG.NORMAL, text=PLocalizer.CrewPageTitle, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                       0.0), text_fg=PiratesGuiGlobals.TextFG1, pos=(0.23,
                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                     0.694))
        return

    def load(self):
        self.leaveButton = self.chain.premakeButton(PLocalizer.CrewPageLeaveCrew, self.leaveCrew)
        self.leaveButton['state'] = DGG.DISABLED
        if not self.crewHUDToggleButton:
            self.crewHUDToggleButton = self.chain.premakeButton(PLocalizer.CrewHUDCrewPanelButton, self.toggleCrewHUD)
        self.optionsButton = self.chain.premakeButton(PLocalizer.CrewOptions, self.crewOptions)
        self.chain.makeButtons()

    def loadOptionsPanel(self):
        self.mainFrame.hide()
        if not self.addAvatarToList:
            self.addAvatarToList = self.optionsChain.premakeButton(PLocalizer.CrewMatchJoinCrewButton, self.toggleAvatarLookout)
        if not self.addAvatarToListPVP:
            self.addAvatarToListPVP = self.optionsChain.premakeButton(PLocalizer.CrewMatchJoinPVPCrewButton, self.toggleAvatarLookoutPVP, textPos=(0.025,
                                                                                                                                                   0,
                                                                                                                                                   0))
        if not self.startACrewButton:
            self.startACrewButton = self.optionsChain.premakeButton(PLocalizer.CrewStartACrewButton, self.toggleStartACrew)
        if not self.addCrewLookout:
            self.addCrewLookout = self.optionsChain.premakeButton(PLocalizer.CrewMatchRecruitButton, self.toggleCrewLookout)
        if not self.selectCrewIcon:
            self.selectCrewIcon = self.optionsChain.premakeButton(PLocalizer.CrewIconButton, self.toggleCrewIcon)
        if not self.lookingForCrewButton:
            self.lookingForCrewButton = self.optionsChain.premakeButton(PLocalizer.CrewLookingForButton, self.toggleLookingForCrew)
        if not self.crewButton:
            self.crewButton = self.optionsChain.premakeButton(PLocalizer.CrewList, self.showCrewPanel)
        self.optionsChain.makeButtons()
        self.onlineIcon = self.icon.find('**/icon_sphere').copyTo(self.lookingForCrewButton)
        self.onlineIconRing = self.ring.find('**/icon_torus').copyTo(self.lookingForCrewButton)
        self.onlineIconRing.reparentTo(self.onlineIcon, -1)
        self.onlineIconRing.setColor(1, 0.9, 0.7, 1)
        self.joinACrewIcon = self.icon.find('**/icon_sphere').copyTo(self.addAvatarToList)
        self.joinACrewIconRing = self.ring.find('**/icon_torus').copyTo(self.addAvatarToList)
        self.joinACrewIconRing.reparentTo(self.joinACrewIcon, -1)
        self.joinACrewIconRing.setColor(1, 0.9, 0.7, 1)
        self.recruitCrewmatesIcon = self.icon.find('**/icon_sphere').copyTo(self.addCrewLookout)
        self.recruitCrewmatesIconRing = self.ring.find('**/icon_torus').copyTo(self.addCrewLookout)
        self.recruitCrewmatesIconRing.reparentTo(self.recruitCrewmatesIcon, -1)
        self.recruitCrewmatesIconRing.setColor(1, 0.9, 0.7, 1)
        self.addAvatarToListPVPIcon = self.icon.find('**/icon_sphere').copyTo(self.addAvatarToListPVP)
        self.addAvatarToListPVPIconRing = self.ring.find('**/icon_torus').copyTo(self.addAvatarToListPVP)
        self.addAvatarToListPVPIconRing.reparentTo(self.addAvatarToListPVPIcon, -1)
        self.addAvatarToListPVPIconRing.setColor(1, 0.9, 0.7, 1)
        self.onlineIcon.setPos(-0.19, 0, 0)
        self.onlineIcon.setScale(0.2)
        currentVal = localAvatar.getLookingForCrew()
        if currentVal == 0:
            self.onlineIcon.setColor(1, 0, 0, 0.6)
        else:
            self.onlineIcon.setColor(0, 1, 0, 0.6)
        self.joinACrewIcon.setPos(-0.19, 0, 0)
        self.joinACrewIcon.setScale(0.2)
        if self.joinACrewStatus == 0:
            self.joinACrewIcon.setColor(1, 0, 0, 0.6)
        else:
            self.joinACrewIcon.setColor(0, 1, 0, 0.6)
        self.recruitCrewmatesIcon.setPos(-0.19, 0, 0)
        self.recruitCrewmatesIcon.setScale(0.2)
        if self.recruitCrewMatesStatus == 0:
            self.recruitCrewmatesIcon.setColor(1, 0, 0, 0.6)
        else:
            self.recruitCrewmatesIcon.setColor(0, 1, 0, 0.6)
        self.addAvatarToListPVPIcon.setPos(-0.19, 0, 0)
        self.addAvatarToListPVPIcon.setScale(0.2)
        if self.joinACrewStatusPVP == 0:
            self.addAvatarToListPVPIcon.setColor(1, 0, 0, 0.6)
        else:
            self.addAvatarToListPVPIcon.setColor(0, 1, 0, 0.6)
        self.determineOptionsButtonsState()
        self.optionsChain.show()

    def showCrewPanel(self):
        self.optionsChain.hide()
        self.mainFrame.show()

    def determineOptionsButtonsState(self):
        if self.clearCrewIcon:
            if not self.crewIconSelection:
                self.clearCrewIcon['state'] = DGG.DISABLED
        if self.selectCrewIcon:
            if self.crew and DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand() == 1:
                self.selectCrewIcon['state'] = DGG.NORMAL
            else:
                self.selectCrewIcon['state'] = DGG.DISABLED
        if self.addCrewLookout:
            if self.crew and DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand() == 1 or self.startACrewState:
                self.addCrewLookout['state'] = DGG.NORMAL
            else:
                self.addCrewLookout['state'] = DGG.DISABLED
        if self.addAvatarToList:
            if self.crew or self.startACrewState or self.joinACrewStatusPVP:
                self.addAvatarToList['state'] = DGG.DISABLED
            else:
                self.addAvatarToList['state'] = DGG.NORMAL
        if self.addAvatarToListPVP:
            if self.crew or self.startACrewState or self.joinACrewStatus:
                self.addAvatarToListPVP['state'] = DGG.DISABLED
            else:
                self.addAvatarToListPVP['state'] = DGG.NORMAL
        if self.joinACrewStatus == 0 or self.crew:
            self.blinkSearchDot(self.joinACrewIcon, 0)
            self.joinACrewIcon.setColor(1, 0, 0, 0.6)
        else:
            self.blinkSearchDot(self.joinACrewIcon, 1)
        if self.joinACrewStatusPVP == 0 or self.crew:
            self.blinkSearchDot(self.addAvatarToListPVPIcon, 0)
            self.addAvatarToListPVPIcon.setColor(1, 0, 0, 0.6)
        else:
            self.blinkSearchDot(self.addAvatarToListPVPIcon, 1)
        if self.recruitCrewMatesStatus == 0:
            self.blinkSearchDot(self.recruitCrewmatesIcon, 0)
            self.recruitCrewmatesIcon.setColor(1, 0, 0, 0.6)
        else:
            self.blinkSearchDot(self.recruitCrewmatesIcon, 1)
        if self.startACrewButton:
            if self.crew or self.startACrewState or self.joinACrewStatus or self.joinACrewStatusPVP:
                self.startACrewButton['state'] = DGG.DISABLED
            else:
                self.startACrewButton['state'] = DGG.NORMAL
        if self.lookingForCrewButton:
            if self.crew:
                self.lookingForCrewButton['state'] = DGG.DISABLED

    def enableClearCrewIconButton(self, selection):
        self.crewIconSelection = selection
        if self.clearCrewIcon:
            self.clearCrewIcon['state'] = DGG.NORMAL

    def toggleLookingForCrew(self):
        currentVal = localAvatar.getLookingForCrew()
        if currentVal == 1:
            localAvatar.setLookingForCrew(0)
            self.blinkSearchDot(self.onlineIcon, 0)
            self.onlineIcon.setColor(1, 0, 0, 0.6)
        else:
            localAvatar.setLookingForCrew(1)
            self.blinkSearchDot(self.onlineIcon, 1)

    def destroy(self):
        self.ignoreAll()
        self.crew = None
        if self.avatarPanel:
            self.avatarPanel.cleanup()
            self.avatarPanel = None
        self.membersList.destroy()
        self.chain.destroy()
        self.optionsChain.destroy()
        self.mainFrame.destroy()
        SocialPage.SocialPage.destroy(self)
        return

    def leaveCrew(self):
        for avId, avButton in self.crew.iteritems():
            av = base.cr.doId2do.get(avId)
            if av:
                av.refreshName()
                crewMembersIconId = av.getCrewIcon()
                if crewMembersIconId:
                    av.setCrewIconIndicator(0)
                    av.setCrewIconIndicator(2)

        base.cr.pirateCrewMatch.deleteCrewFromLookoutList()
        base.cr.PirateBandManager.d_requestRemove(localAvatar.doId)
        self.joinACrewStatus = 0
        self.joinACrewStatusPVP = 0
        self.recruitCrewMatesStatus = 0
        if self.addAvatarToList:
            self.determineOptionsButtonsState()
        self.crewHUD.setHUDOff()

    def crewOptions(self):
        self.mainFrame.hide()
        self.loadOptionsPanel()

    def addCrew(self, member):
        if self.addCrewLookout:
            if self.crew and DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand() == 1:
                self.addCrewLookout['state'] = DGG.NORMAL
            else:
                self.addCrewLookout['state'] = DGG.DISABLED
        if self.addAvatarToList:
            if self.crew:
                self.addAvatarToList['state'] = DGG.DISABLED
                self.blinkSearchDot(self.joinACrewIcon, 0)
                self.joinACrewIcon.setColor(1, 0, 0, 0.6)
        if self.addAvatarToListPVP:
            if self.crew:
                self.addAvatarToListPVP['state'] = DGG.DISABLED
                self.blinkSearchDot(self.addAvatarToListPVPIcon, 0)
                self.addAvatarToListPVPIcon.setColor(1, 0, 0, 0.6)
        changed = 0
        avId = member.avatarId
        if avId == localAvatar.doId:
            self.enableCrewIcon()
            for id in self.crew:
                localAvatar.guiMgr.radarGui.refreshRadarObject(id)

            return
        if avId not in self.crew:
            button = self.membersList.addMember(avId, None, PirateMemberList.MODE_CREW, member)
            self.crewHUD.addCrew(member)
            self.crew[avId] = button
            self.crew[avId].updateShip(member.getShipInfo()[0], member.getShipHasSpace())
            self.repackCrew()
            localAvatar.guiMgr.radarGui.refreshRadarObject(avId)
            return 1
        else:
            return 0
        av = base.cr.doId2do.get(avId)
        if av:
            av.setCrewIconIndicator(0)
            av.setCrewIconIndicator(1)
        return

    def removeCrew(self, member):
        avId = member.avatarId
        self.crew.pop(avId, None)
        self.membersList.removeMember(avId, None, PirateMemberList.MODE_CREW)
        self.crewHUD.removeCrew(member)
        localAvatar.guiMgr.radarGui.refreshRadarObject(avId)
        if avId != localAvatar.getDoId():
            self.repackCrew()
        else:
            self.b_deactivateCrewLookout()
        for avId, avButton in self.crew.iteritems():
            av = base.cr.doId2do.get(avId)
            if av:
                av.refreshName()
                crewMembersIconId = av.getCrewIcon()
                if crewMembersIconId:
                    av.setCrewIconIndicator(0)
                    av.setCrewIconIndicator(2)

        return

    def repackCrew(self):
        if self.crew:
            self.leaveButton['state'] = DGG.NORMAL
            if not self.crewHUD.initialStateSwitch:
                taskMgr.doMethodLater(2, self.delayedHUDOn, 'delayedHUDLoad')
                self.crewHUD.initialStateSwitch = True
            if self.selectCrewIcon:
                if DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand() == 1:
                    self.selectCrewIcon['state'] = DGG.NORMAL
        else:
            self.leaveButton['state'] = DGG.DISABLED
            if self.clearCrewIcon:
                self.clearCrewIcon['state'] = DGG.DISABLED
            if self.selectCrewIcon:
                self.selectCrewIcon['state'] = DGG.DISABLED
            base.localAvatar.setCrewIcon(0)
            if base.cr.pirateCrewMatch:
                base.cr.pirateCrewMatch.deleteCrewFromLookoutList()
            self.crewHUD.initialStateSwitch = False
            self.crewHUD.setHUDOff()
        if self.addCrewLookout:
            if self.crew and DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand() == 1:
                self.addCrewLookout['state'] = DGG.NORMAL
            else:
                self.addCrewLookout['state'] = DGG.DISABLED
                self.blinkSearchDot(self.recruitCrewmatesIcon, 0)
                self.recruitCrewmatesIcon.setColor(1, 0, 0, 0.6)
                self.recruitCrewMatesStatus == 0
        if self.addAvatarToList:
            if self.crew:
                self.addAvatarToList['state'] = DGG.DISABLED
                self.blinkSearchDot(self.joinACrewIcon, 0)
                self.joinACrewIcon.setColor(1, 0, 0, 0.6)
            else:
                self.addAvatarToList['state'] = DGG.NORMAL
                self.blinkSearchDot(self.joinACrewIcon, 0)
                self.joinACrewIcon.setColor(1, 0, 0, 0.6)
                if self.startACrewState == 1:
                    self.addAvatarToList['state'] = DGG.DISABLED
        if self.addAvatarToListPVP:
            if self.crew:
                self.addAvatarToListPVP['state'] = DGG.DISABLED
                self.blinkSearchDot(self.addAvatarToListPVPIcon, 0)
                self.addAvatarToListPVPIcon.setColor(1, 0, 0, 0.6)
            else:
                self.addAvatarToListPVP['state'] = DGG.NORMAL
                self.blinkSearchDot(self.addAvatarToListPVPIcon, 0)
                self.addAvatarToListPVPIcon.setColor(1, 0, 0, 0.6)
                if self.startACrewState == 1:
                    self.addAvatarToListPVP['state'] = DGG.DISABLED
        if self.startACrewButton:
            if self.crew or self.startACrewState:
                self.startACrewButton['state'] = DGG.DISABLED
            else:
                self.startACrewButton['state'] = DGG.NORMAL
        if self.lookingForCrewButton:
            if self.crew and localAvatar.getLookingForCrew() == 1:
                localAvatar.toggleLookingForCrewSign()
                self.lookingForCrewButton['state'] = DGG.DISABLED
            elif not self.crew:
                self.lookingForCrewButton['state'] = DGG.NORMAL
            elif self.crew:
                self.lookingForCrewButton['state'] = DGG.DISABLED
        crewMembersIconId = 0
        for avId, avButton in self.crew.iteritems():
            av = base.cr.doId2do.get(avId)
            if not av:
                return
            av.refreshName()
            crewMembersIconId = av.getCrewIcon()
            if crewMembersIconId:
                av.setCrewIconIndicator(0)
                av.setCrewIconIndicator(1)

        if crewMembersIconId:
            localAvatar.setCrewIcon(0)
            localAvatar.setCrewIcon(1)

    def crewDetails(self, avId):
        avatar = base.cr.doId2do.get(avId)
        if avatar:
            messenger.send(PiratesGlobals.AvatarDetailsEvent, [avatar.getDoId(), False])
            return 1
        crewMember = self.crew.get(avId).getMember()
        if crewMember:
            messenger.send(PiratesGlobals.AvatarDetailsEvent, [avId, False])
            return 1
        return 0

    def hasCrew(self, avId):
        return avId in self.crew

    def updateCrewMemberName(self, member, name):
        crewButton = self.crew.get(member.avatarId)
        if crewButton:
            crewButton.updateName(name)

    def updateCrewMemberHp(self, member, hp, maxHp):
        crewButton = self.crew.get(member.avatarId)
        if crewButton:
            crewButton.updateHp(hp, maxHp)
        self.crewHUD.updateCrewMemberHp(member, hp, maxHp)

    def updateCrewMemberShip(self, member, shipId):
        crewButton = self.crew.get(member.avatarId)
        if crewButton:
            crewButton.updateShip(shipId, member.getShipHasSpace())

    def updateIsManager(self, member, flag):
        crewButton = self.crew.get(member.avatarId)
        if crewButton:
            crewButton.updateIsManager(flag)

    def updateCaptainStatus(self):
        self.repackCrew()

    def DoUpdateCrewData(self, member, remove):
        if remove:
            self.removeCrew(member)
        else:
            self.addCrew(member)
            self.repackCrew()

    def loadSelectCrewIcon(self):
        CrewIconSelector.CrewIconSelector(PLocalizer.CrewIconTitle, self.selectCrewIcon)

    def enableCrewIcon(self):
        base.cr.PirateBandManager.d_requestCrewIconUpdate(1)
        base.localAvatar.setCrewIcon(0)
        base.localAvatar.setCrewIcon(1)
        self.crewIconSelection = 1

    def disableCrewIcon(self):
        base.cr.PirateBandManager.d_requestCrewIconUpdate(0)
        base.localAvatar.setCrewIcon(0)
        self.crewIconSelection = 0

    def toggleCrewIcon(self):
        if self.crewIconSelection:
            self.disableCrewIcon()
        else:
            self.enableCrewIcon()

    def b_clearCrewIcon(self):
        base.localAvatar.setCrewIcon(0)
        if self.clearCrewIcon:
            self.clearCrewIcon['state'] = DGG.DISABLED
        self.crewIconSelection = 0
        base.cr.PirateBandManager.d_requestCrewIconUpdate(0)

    def b_activateAvatarLookout(self):
        base.cr.pirateCrewMatch.addAvatarToLookoutList(1)
        self.joinACrewStatus = 1
        if self.startACrewButton:
            self.startACrewButton['state'] = DGG.DISABLED
        if self.addAvatarToListPVP:
            self.addAvatarToListPVP['state'] = DGG.DISABLED
        try:
            self.joinACrewIcon.setColor(0, 1, 0, 0.6)
            self.blinkSearchDot(self.joinACrewIcon, 1)
        except:
            pass

    def b_activateAvatarLookoutPVP(self):
        base.cr.pirateCrewMatch.addAvatarToLookoutList(2)
        self.joinACrewStatusPVP = 1
        if self.startACrewButton:
            self.startACrewButton['state'] = DGG.DISABLED
        if self.addAvatarToList:
            self.addAvatarToList['state'] = DGG.DISABLED
        try:
            self.addAvatarToListPVPIcon.setColor(0, 1, 0, 0.6)
            self.blinkSearchDot(self.addAvatarToListPVPIcon, 1)
        except:
            pass

    def b_deactivateAvatarLookout(self):
        base.cr.pirateCrewMatch.deleteAvatarFromLookoutList()
        self.joinACrewStatus = 0
        if self.addAvatarToListPVP:
            self.addAvatarToListPVP['state'] = DGG.NORMAL
        if not self.crew:
            if self.startACrewButton:
                self.startACrewButton['state'] = DGG.NORMAL
        try:
            self.blinkSearchDot(self.joinACrewIcon, 0)
            self.joinACrewIcon.setColor(1, 0, 0, 0.6)
        except:
            pass

    def b_deactivateAvatarLookoutPVP(self):
        base.cr.pirateCrewMatch.deleteAvatarFromLookoutList()
        self.joinACrewStatusPVP = 0
        if self.addAvatarToList:
            self.addAvatarToList['state'] = DGG.NORMAL
        if not self.crew:
            if self.startACrewButton:
                self.startACrewButton['state'] = DGG.NORMAL
        try:
            self.blinkSearchDot(self.addAvatarToListPVPIcon, 0)
            self.addAvatarToListPVPIcon.setColor(1, 0, 0, 0.6)
        except:
            pass

    def toggleAvatarLookout(self):
        if self.joinACrewStatus:
            self.b_deactivateAvatarLookout()
        else:
            if not self.joinACrewStatus:
                self.b_activateAvatarLookout()

    def toggleAvatarLookoutPVP(self):
        if self.joinACrewStatusPVP:
            self.b_deactivateAvatarLookoutPVP()
        else:
            if not self.joinACrewStatusPVP:
                self.b_activateAvatarLookoutPVP()

    def b_activateCrewLookout(self, range, sailValue=0, cannonValue=0):
        if self.crew or self.startACrewState:
            base.cr.pirateCrewMatch.addCrewToLookoutList(range, sailValue, cannonValue)
            if self.addCrewLookout:
                self.addCrewLookout['state'] = DGG.NORMAL
            if self.startACrewState:
                self.startACrewButton['state'] = DGG.DISABLED
            if self.addAvatarToList:
                self.addAvatarToList['state'] = DGG.DISABLED
            if self.addAvatarToListPVP:
                self.addAvatarToListPVP['state'] = DGG.DISABLED
            self.recruitCrewMatesStatus = 1
            try:
                self.recruitCrewmatesIcon.setColor(0, 1, 0, 0.6)
                self.blinkSearchDot(self.recruitCrewmatesIcon, 1)
            except:
                pass

    def b_deactivateCrewLookout(self):
        base.cr.pirateCrewMatch.deleteCrewFromLookoutList()
        self.recruitCrewMatesStatus = 0
        if self.startACrewState:
            if not self.crew:
                base.cr.pirateCrewMatch.requestDeleteCrewOfOne()
                if self.startACrewButton:
                    self.startACrewButton['state'] = DGG.NORMAL
                if self.addCrewLookout:
                    self.addCrewLookout['state'] = DGG.DISABLED
                if self.addAvatarToList:
                    self.addAvatarToList['state'] = DGG.NORMAL
                if self.addAvatarToListPVP:
                    self.addAvatarToListPVP['state'] = DGG.NORMAL
        self.startACrewState = 0
        try:
            self.blinkSearchDot(self.recruitCrewmatesIcon, 0)
            self.recruitCrewmatesIcon.setColor(1, 0, 0, 0.6)
        except:
            pass

    def toggleCrewLookout(self):
        if self.recruitCrewMatesStatus:
            self.b_deactivateCrewLookout()
        else:
            if not self.recruitCrewMatesStatus:
                CrewMatchInviter.CrewMatchInviter(localAvatar.getLevel())
                if self.addCrewLookout:
                    self.addCrewLookout['state'] = DGG.DISABLED

    def toggleStartACrew(self):
        self.joinACrewStatus = 0
        if self.startACrewState == 1:
            base.cr.pirateCrewMatch.requestDeleteCrewOfOne()
            self.startACrewButton['state'] = DGG.NORMAL
            self.addCrewLookout['state'] = DGG.DISABLED
            self.startACrewState = 0
            self.recruitCrewMatesStatus = 0
            self.determineOptionsButtonsState()
            return
        base.cr.pirateCrewMatch.requestCrewOfOne()
        self.startACrewState = 1
        self.toggleCrewLookout()
        self.startACrewButton['state'] = DGG.DISABLED
        self.addAvatarToList['state'] = DGG.DISABLED
        self.addAvatarToListPVP['state'] = DGG.DISABLED
        self.determineOptionsButtonsState()

    def blinkSearchDot(self, dotObj, state):
        taskName = str(dotObj) + '_blink'
        if state:
            dotObj.setColor(0, 1, 0, 0.6)
            taskMgr.doMethodLater(1, self.blink, taskName, extraArgs=[dotObj, taskName])
        else:
            taskMgr.remove(taskName)
            dotObj.setColor(1, 0, 0, 0.6)

    def blink(self, dotObj, taskName):
        if dotObj.getColor() == VBase4(0, 0, 0, 0.6):
            dotObj.setColor(0, 1, 0, 0.6)
        else:
            if dotObj.getColor() == VBase4(0, 1, 0, 0.6):
                dotObj.setColor(0, 0, 0, 0.6)
        return Task.again

    def deactivateCrewMatchInviteTeleport(self):
        if self.joinACrewStatus:
            self.b_deactivateAvatarLookout()
        if self.joinACrewStatus:
            self.b_deactivateAvatarLookoutPVP()

    def toggleCrewHUD(self):
        self.crewHUD.toggleHUD()

    def delayedHUDOn(self, task):
        self.crewHUD.setHUDOn()
        return Task.done

    def deactivateCrewHUDButton(self):
        if self.crewHUDToggleButton:
            self.crewHUDToggleButton['state'] = DGG.DISABLED

    def activateCrewHUDButton(self):
        if self.crewHUDToggleButton:
            self.crewHUDToggleButton['state'] = DGG.NORMAL
# okay decompiling .\pirates\piratesgui\CrewPage.pyc
