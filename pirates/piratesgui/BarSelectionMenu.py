# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.BarSelectionMenu
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from otp.otpbase import OTPGlobals
from pandac.PandaModules import *
from pirates.battle import WeaponGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.piratesbase import Freebooter, PiratesGlobals, PLocalizer
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.reputation import ReputationGlobals


class BarSelectionMenu(GuiPanel.GuiPanel):
    
    notify = DirectNotifyGlobal.directNotify.newCategory('BarSelectionMenu')
    ICON_WIDTH = 0.13
    HEIGHT = 0.15
    SelectionDelay = 0.6

    def __init__(self, items, command=None):
        GuiPanel.GuiPanel.__init__(self, None, 1.0, self.HEIGHT, showClose=0)
        self.items = items
        self.icons = []
        self.hotkeys = []
        self.repMeters = []
        self.choice = 0
        self.command = command
        self.hideTask = None
        card = loader.loadModel('models/textureCards/selectionGui')
        texCard = card.find('**/main_gui_general_box_over')
        self.cursor = DirectFrame(parent=self, state=DGG.DISABLED, relief=None, frameSize=(0,
                                                                                           0.08,
                                                                                           0,
                                                                                           0.08), pos=(0.08,
                                                                                                       0,
                                                                                                       0.07), geom=texCard, geom_scale=0.12)
        self.cursor.setTransparency(1)
        self.cursor.resetFrameSize()
        card.removeNode()
        self.initialiseoptions(BarSelectionMenu)
        self.card = loader.loadModel('models/textureCards/weapon_icons')
        self.accept('escape', self.__handleCancel)
        self.loadWeaponButtons()
        self.hide()
        return

    def loadWeaponButtons(self):
        for hotkey in self.hotkeys:
            hotkey.destroy()

        self.hotkeys = []
        for icon in self.icons:
            icon.destroy()

        self.icons = []
        for repMeter in self.repMeters:
            repMeter.destroy()

        self.repMeters = []
        self['frameSize'] = (
         0, self.ICON_WIDTH * len(self.items) + 0.04, 0, self.HEIGHT)
        self.setX(-((self.ICON_WIDTH * len(self.items) + 0.04) / 2.0))
        topGui = loader.loadModel('models/gui/toplevel_gui')
        kbButton = topGui.find('**/keyboard_button')
        for i in range(len(self.items)):
            if self.items[i]:
                category = WeaponGlobals.getRepId(self.items[i])
                icon = DirectFrame(parent=self, state=DGG.DISABLED, relief=None, frameSize=(0,
                                                                                            0.08,
                                                                                            0,
                                                                                            0.08), pos=(self.ICON_WIDTH * i + 0.08, 0, 0.082))
                icon.setTransparency(1)
                key = WeaponGlobals.getWeaponKey(self.items[i])
                hotkeyText = 'F%s' % key
                hotkey = DirectFrame(parent=icon, state=DGG.DISABLED, relief=None, text=hotkeyText, text_align=TextNode.ACenter, text_scale=0.045, text_pos=(0,
                                                                                                                                                             0), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, image=kbButton, image_scale=0.06, image_pos=(0,
                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                           0.01), image_color=(0.5,
                                                                                                                                                                                                                                                                                                               0.5,
                                                                                                                                                                                                                                                                                                               0.35,
                                                                                                                                                                                                                                                                                                               1), pos=(0,
                                                                                                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                                                                                                        0.08))
                self.hotkeys.append(hotkey)
                category = WeaponGlobals.getRepId(self.items[i])
                if Freebooter.getPaidStatus(base.localAvatar.getDoId()) or Freebooter.allowedFreebooterWeapon(category):
                    asset = EconomyGlobals.getItemIcons(self.items[i])
                    if asset:
                        texCard = self.card.find('**/%s' % asset)
                        icon['geom'] = texCard
                        icon['geom_scale'] = 0.08
                    icon.resetFrameSize()
                    self.icons.append(icon)
                else:
                    texCard = topGui.find('**/subscribers_lock*')
                    icon['geom'] = texCard
                    icon['geom_scale'] = 0.2
                    icon.resetFrameSize()
                    self.icons.append(icon)
                repMeter = DirectWaitBar(parent=icon, relief=DGG.SUNKEN, state=DGG.DISABLED, borderWidth=(0.002,
                                                                                                          0.002), range=0, value=0, frameColor=(0.24,
                                                                                                                                                0.24,
                                                                                                                                                0.21,
                                                                                                                                                1), barColor=(0.8,
                                                                                                                                                              0.8,
                                                                                                                                                              0.7,
                                                                                                                                                              1), pos=(-0.05, 0, -0.0525), hpr=(0,
                                                                                                                                                                                                0,
                                                                                                                                                                                                0), frameSize=(0.005,
                                                                                                                                                                                                               0.095,
                                                                                                                                                                                                               0,
                                                                                                                                                                                                               0.0125))
                self.repMeters.append(repMeter)
                inv = base.localAvatar.getInventory()
                if inv:
                    repValue = inv.getReputation(category)
                    level, leftoverValue = ReputationGlobals.getLevelFromTotalReputation(category, repValue)
                    max = ReputationGlobals.getReputationNeededToLevel(category, level)
                    repMeter['range'] = max
                    repMeter['value'] = leftoverValue

        return

    def selectPrev(self):
        if len(self.items) < 1:
            return
        self.show()
        if len(self.items) > 1:
            keepTrying = True
        else:
            keepTrying = False
        while keepTrying:
            keepTrying = False
            self.choice = self.choice - 1
            if self.choice < 0:
                self.choice = len(self.items) - 1
            if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                category = WeaponGlobals.getRepId(self.items[self.choice])
                if not Freebooter.allowedFreebooterWeapon(category):
                    keepTrying = True

        self.cursor.setPos(self.ICON_WIDTH * self.choice + 0.08, 0, 0.072)
        taskMgr.remove('BarSelectHideTask' + str(self.getParent()))
        self.hideTask = taskMgr.doMethodLater(self.SelectionDelay, self.confirmSelection, 'BarSelectHideTask' + str(self.getParent()), extraArgs=[])

    def selectNext(self):
        if len(self.items) < 1:
            return
        self.show()
        if len(self.items) > 1:
            keepTrying = True
        else:
            keepTrying = False
        while keepTrying:
            keepTrying = False
            self.choice = self.choice + 1
            if self.choice > len(self.items) - 1:
                self.choice = 0
            if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                category = WeaponGlobals.getRepId(self.items[self.choice])
                if not Freebooter.allowedFreebooterWeapon(category):
                    keepTrying = True

        self.cursor.setPos(self.ICON_WIDTH * self.choice + 0.08, 0, 0.072)
        taskMgr.remove('BarSelectHideTask' + str(self.getParent()))
        self.hideTask = taskMgr.doMethodLater(self.SelectionDelay, self.confirmSelection, 'BarSelectHideTask' + str(self.getParent()), extraArgs=[])

    def selectChoice(self, weaponId):
        if len(self.items) < 1:
            return
        if weaponId not in self.items:
            return
        self.show()
        self.choice = self.items.index(weaponId)
        self.cursor.setPos(self.ICON_WIDTH * self.choice + 0.08, 0, 0.072)
        taskMgr.remove('BarSelectHideTask' + str(self.getParent()))
        self.hideTask = taskMgr.doMethodLater(self.SelectionDelay * 2, self.hide, 'BarSelectHideTask' + str(self.getParent()), extraArgs=[])

    def confirmSelection(self):
        self.hide()
        if self.command:
            self.command(self.items[self.choice], fromWheel=1)

    def update(self, items):
        if self.items != items:
            self.items = items
            self.loadWeaponButtons()

    def updateRep(self, category, value):
        for i in range(len(self.items)):
            repId = WeaponGlobals.getRepId(self.items[i])
            if repId == category:
                level, leftoverValue = ReputationGlobals.getLevelFromTotalReputation(category, value)
                max = ReputationGlobals.getReputationNeededToLevel(category, level)
                if len(self.repMeters) - 1 >= i:
                    self.repMeters[i]['range'] = max
                    self.repMeters[i]['value'] = leftoverValue

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        taskMgr.remove('BarSelectHideTask' + str(self.getParent()))
        self.ignore('escape')
        for icon in self.icons:
            icon.destroy()
            icon = None

        self.icons = []
        if self.card:
            self.card.removeNode()
            self.card = None
        GuiPanel.GuiPanel.destroy(self)
        return

    def __handleCancel(self):
        taskMgr.remove('BarSelectHideTask' + str(self.getParent()))
        self.hide()
        if localAvatar.currentWeaponId in self.items:
            index = self.items.index(localAvatar.currentWeaponId)
            self.choice = index

    def hide(self):
        if hasattr(base, 'localAvatar'):
            if hasattr(localAvatar.guiMgr.combatTray, 'skillTray'):
                localAvatar.guiMgr.combatTray.skillTray.show()
        GuiPanel.GuiPanel.hide(self)
# okay decompiling .\pirates\piratesgui\BarSelectionMenu.pyc
