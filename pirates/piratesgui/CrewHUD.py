# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.CrewHUD
from direct.gui.DirectGui import *
from direct.showbase.ShowBaseGlobal import *
from pandac.PandaModules import *
from pirates.band import BandConstance, DistributedBandMember
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import (PirateButtonChain, PirateMemberList,
                                PiratesGuiGlobals, SocialPage)
from pirates.uberdog.UberDogGlobals import CrewStatus

HUD_ICONS = {0: None, 1: 'icon_cutlass_black', 2: 'icon_pistol_single', 3: 'icon_voodoo_doll_straw', 4: 'icon_dagger_dagger', 5: 'icon_grenade', 6: 'icon_voodoo_staff_L1', 7: 'icon_cannon', 8: 'sail_come_about', 9: 'topgui_icon_ship', 10: 'treasure_w_card'}

class CrewHUD(SocialPage.SocialPage):
    __module__ = __name__
    notify = directNotify.newCategory('CrewHUD')

    def __init__(self):
        SocialPage.SocialPage.__init__(self, 'Crew HUD')
        self.crew = {}
        self.mainFrame = DirectFrame(relief=None, parent=base.a2dTopLeft, frameSize=(0,
                                                                                     0.5,
                                                                                     0,
                                                                                     1.5), state=DGG.DISABLED, sortOrder=0)
        self.mainFrameSea = DirectFrame(relief=None, parent=base.a2dTopLeft, frameSize=(0,
                                                                                        0.5,
                                                                                        0,
                                                                                        1), state=DGG.DISABLED, sortOrder=0)
        self.mainFrame.setPos(-0.0566664, 0, -1.93)
        self.mainFrameSea.setPos(-0.0566664, 0, -1.62667)
        self.hudLabel = DirectLabel(relief=None, parent=self.mainFrame, text=PLocalizer.CrewHUDNoCrew, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.29,
                                                                                                                                                                                                                                   1.56,
                                                                                                                                                                                                                                   0), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, state=DGG.DISABLED)
        self.hudLabelSea = DirectLabel(relief=None, parent=self.mainFrameSea, text=PLocalizer.CrewHUDNoCrew, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.29,
                                                                                                                                                                                                                                         1.055,
                                                                                                                                                                                                                                         0), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, state=DGG.DISABLED)
        self.membersList = PirateMemberList.PirateMemberList(12, self.mainFrame, 'FOOLIO HC', height=1.5475, memberHeight=0.08, memberWidth=0.48, memberOffset=0.2, bottom=0.074, width=0.6, hud=True)
        self.membersListSea = PirateMemberList.PirateMemberList(12, self.mainFrameSea, 'FOOLIO HC', height=1.0475, memberHeight=0.065, memberWidth=0.48, memberOffset=0.2, bottom=0.074, width=0.6, hud=True)
        self.weaponCard = loader.loadModel('models/textureCards/weapon_icons')
        self.card = loader.loadModel('models/textureCards/skillIcons')
        self.topGui = loader.loadModel('models/gui/toplevel_gui')
        self.mainFrame.hide()
        self.mainFrameSea.hide()
        self.hudOn = False
        self.initialStateSwitch = False
        self.debugAvId = False
        self.debugCount = 0
        self.accept('chatPanelMax', self.respondChatPanelMax)
        self.accept('chatPanelMin', self.respondChatPanelMin)
        self.toggledByChat = False
        self.accept('localAvatarToSea', self.adjustHUDToSea)
        self.accept('localAvatarToLand', self.adjustHUDToLand)
        self.atSea = False
        self.accept('chatPanelOpen', self.chatPanelOpen)
        self.accept('chatPanelClose', self.chatPanelClose)
        self.chatPanelOpen = False
        return

    def addCrew(self, member):
        avId = member.avatarId
        if avId not in self.crew or self.debugAvId:
            button = self.membersList.addMember(avId + self.debugCount, None, PirateMemberList.MODE_CREW_HUD, member)
            buttonSea = self.membersListSea.addMember(avId + self.debugCount, None, PirateMemberList.MODE_CREW_HUD_SEA, member)
            reloadFrame = DirectFrame(parent=button, relief=None, state=DGG.DISABLED, image=self.card.find('**/base'), image_scale=0.08, image_pos=(0,
                                                                                                                                                    0,
                                                                                                                                                    0.02), pos=(0.09,
                                                                                                                                                                0,
                                                                                                                                                                0.01))
            reloadFrameSea = DirectFrame(parent=buttonSea, relief=None, state=DGG.DISABLED, image=self.card.find('**/base'), image_scale=0.055, image_pos=(0,
                                                                                                                                                           0,
                                                                                                                                                           0.02), pos=(0.11,
                                                                                                                                                                       0,
                                                                                                                                                                       0.01))
            skillFrame = DirectFrame(parent=reloadFrame, relief=None, state=DGG.DISABLED, image=self.weaponCard.find('**/icon_cutlass_iron'), image_scale=0.07, image_pos=(0,
                                                                                                                                                                           0,
                                                                                                                                                                           0.02))
            skillFrameSea = DirectFrame(parent=reloadFrameSea, relief=None, state=DGG.DISABLED, image=self.weaponCard.find('**/icon_cutlass_iron'), image_scale=0.035, image_pos=(0,
                                                                                                                                                                                  0,
                                                                                                                                                                                  0.02))
            skillFrame.setTransparency(1)
            skillFrameSea.setTransparency(1)
            self.crew[avId + self.debugCount] = [
             button, reloadFrame, skillFrame, buttonSea, reloadFrameSea, skillFrameSea]
        if self.debugAvId and self.debugCount < 11:
            print 'In CrewHUD Debug mode, generating debug button %s' % self.debugCount
            self.debugCount += 1
            self.addCrew(member)
        return

    def removeCrew(self, member):
        avId = member.avatarId
        self.crew.pop(avId, None)
        self.membersList.removeMember(avId, None, PirateMemberList.MODE_CREW_HUD)
        self.membersListSea.removeMember(avId, None, PirateMemberList.MODE_CREW_HUD_SEA)
        return

    def updateActionIcon(self, avId, action):
        skillFrameObj = self.crew.get(avId)
        if skillFrameObj:
            skillFrame = skillFrameObj[2]
        else:
            return
        skillFrameSeaObj = self.crew.get(avId)
        if skillFrameSeaObj:
            skillFrameSea = skillFrameSeaObj[5]
        else:
            return
        newIcon = HUD_ICONS[action]
        if newIcon == None:
            skillFrame['image'] = None
            skillFrameSea['image'] = None
        else:
            if action in [8]:
                skillFrame['image'] = self.card.find('**/%s' % newIcon)
                skillFrame['image_scale'] = 0.07
            else:
                if action in [9, 10]:
                    skillFrame['image'] = self.topGui.find('**/%s' % newIcon)
                    if action == 9:
                        skillFrame['image_scale'] = 0.125
                    elif action == 10:
                        skillFrame['image_scale'] = 0.2
                else:
                    skillFrame['image'] = self.weaponCard.find('**/%s' % newIcon)
                    skillFrame['image_scale'] = 0.06
            skillFrame['image_pos'] = (0, 0, 0.02)
            if action in [8]:
                skillFrameSea['image'] = self.card.find('**/%s' % newIcon)
                skillFrameSea['image_scale'] = 0.045
            else:
                if action in [9, 10]:
                    skillFrameSea['image'] = self.topGui.find('**/%s' % newIcon)
                    if action == 9:
                        skillFrameSea['image_scale'] = 0.065
                    elif action == 10:
                        skillFrameSea['image_scale'] = 0.1
                else:
                    skillFrameSea['image'] = self.weaponCard.find('**/%s' % newIcon)
                    skillFrameSea['image_scale'] = 0.035
            skillFrameSea['image_pos'] = (0, 0, 0.02)
        return

    def updateAll(self, crewNearBy, actionList):
        for element in actionList:
            if element[0] != localAvatar.getDoId():
                self.updateActionIcon(element[0], element[1])

        if crewNearBy > 0:
            self.hudLabel['text'] = PLocalizer.CrewHUDCrewNearBy % crewNearBy
            self.hudLabelSea['text'] = PLocalizer.CrewHUDCrewNearBy % crewNearBy
        else:
            self.hudLabel['text'] = PLocalizer.CrewHUDNoCrew
            self.hudLabelSea['text'] = PLocalizer.CrewHUDNoCrew

    def toggleHUD(self):
        if self.hudOn:
            self.mainFrameSea.hide()
            self.mainFrame.hide()
            self.hudOn = False
        else:
            if self.atSea:
                self.mainFrameSea.show()
            else:
                self.mainFrame.show()
            self.hudOn = True

    def setHUDOff(self):
        self.hudOn = False
        self.mainFrame.hide()
        self.mainFrameSea.hide()

    def setHUDOn(self):
        self.hudOn = True
        if self.atSea:
            self.mainFrameSea.show()
        else:
            self.mainFrame.show()

    def debugFullCrewList(self):
        self.debugAvId = True
        print 'DEBUG: Activating crew HUD display debug mode'

    def destroyFullCrewList(self):
        self.debugAvId = False
        print 'DEBUG: Deactivating crew HUD display debug mode'

    def respondChatPanelMax(self):
        if self.hudOn and self.chatPanelOpen and self.atSea or self.hudOn and len(self.crew) > 2:
            self.toggledByChat = True
            self.setHUDOff()

    def respondChatPanelMin(self):
        if self.toggledByChat:
            self.toggledByChat = False
            self.setHUDOn()

    def adjustHUDToSea(self):
        if self.hudOn:
            self.mainFrame.hide()
            self.mainFrameSea.show()
        self.atSea = True

    def adjustHUDToLand(self):
        if self.hudOn:
            self.mainFrameSea.hide()
            self.mainFrame.show()
        self.atSea = False

    def chatPanelOpen(self):
        if self.hudOn and self.atSea:
            self.chatPanelOpen = True

    def chatPanelClose(self):
        if hasattr(base, 'localAvatar'):
            if base.localAvatar.guiMgr.crewHUDTurnedOff:
                pass
            elif self.chatPanelOpen:
                self.setHUDOn()
                self.chatPanelOpen = False

    def updateCrewMemberHp(self, member, hp, maxHp):
        hudButton = self.crew.get(member.avatarId)
        if hudButton:
            hudButton[0].updateHp(hp, maxHp)
# okay decompiling .\pirates\piratesgui\CrewHUD.pyc
