# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.ScoreboardItemGui
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.economy.EconomyGlobals import ItemId
from pirates.economy import EconomyGlobals
from direct.interval.IntervalGlobal import *

class ScoreboardItemGui(DirectFrame):
    __module__ = __name__

    def __init__(self, item, width, height, parent=None, **kw):
        self.width = width
        self.height = height
        optiondefs = (('state', DGG.NORMAL, None), ('frameColor', (0.1, 0.1, 1, 0.08), None), ('borderWidth', PiratesGuiGlobals.BorderWidth, None), ('frameSize', (0.0, self.width, 0.0, self.height), None), ('relief', None, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(ScoreboardItemGui)
        self.icons = {ItemId.CARGO_CRATE: ('icon_crate', PLocalizer.Crate), ItemId.CARGO_CHEST: ('icon_chest', PLocalizer.Chest), ItemId.CARGO_SKCHEST: ('topgui_icon_ship_chest03', PLocalizer.SkChest), ItemId.WHEAT: ('icon_wheat', PLocalizer.InventoryTypeNames.get(ItemId.WHEAT)), ItemId.COTTON: ('icon_cotton', PLocalizer.InventoryTypeNames.get(ItemId.COTTON)), ItemId.RUM: ('icon_rum', PLocalizer.InventoryTypeNames.get(ItemId.RUM)), ItemId.IRON_ORE: ('icon_ironore', PLocalizer.InventoryTypeNames.get(ItemId.IRON_ORE)), ItemId.IVORY: ('icon_ivory', PLocalizer.InventoryTypeNames.get(ItemId.IVORY)), ItemId.SILK: ('icon_silk', PLocalizer.InventoryTypeNames.get(ItemId.SILK)), ItemId.SPICES: ('icon_spices', PLocalizer.InventoryTypeNames.get(ItemId.SPICES)), ItemId.COPPER_BARS: ('icon_copperbars', PLocalizer.InventoryTypeNames.get(ItemId.COPPER_BARS)), ItemId.SILVER_BARS: ('icon_silverbars', PLocalizer.InventoryTypeNames.get(ItemId.SILVER_BARS)), ItemId.GOLD_BARS: ('icon_goldbars', PLocalizer.InventoryTypeNames.get(ItemId.GOLD_BARS)), ItemId.EMERALDS: ('icon_emeralds', PLocalizer.InventoryTypeNames.get(ItemId.EMERALDS)), ItemId.RUBIES: ('icon_rubies', PLocalizer.InventoryTypeNames.get(ItemId.RUBIES)), ItemId.DIAMONDS: ('icon_diamonds', PLocalizer.InventoryTypeNames.get(ItemId.DIAMONDS)), ItemId.CURSED_COIN: ('icon_cursedcoin', PLocalizer.InventoryTypeNames.get(ItemId.CURSED_COIN)), ItemId.ARTIFACT: ('icon_artifact', PLocalizer.InventoryTypeNames.get(ItemId.ARTIFACT)), ItemId.RELIC: ('icon_relic', PLocalizer.InventoryTypeNames.get(ItemId.RELIC)), ItemId.RARE_DIAMOND: ('icon_rarediamond', PLocalizer.InventoryTypeNames.get(ItemId.RARE_DIAMOND)), ItemId.CROWN_JEWELS: ('icon_crownjewels', PLocalizer.InventoryTypeNames.get(ItemId.CROWN_JEWELS)), ItemId.RAREITEM6: ('icon_rareitem6', PLocalizer.InventoryTypeNames.get(ItemId.RAREITEM6))}
        self.item = item
        self.revealTime = 0
        self.counter = None
        self.valueText = None
        self.valueText2 = None
        self._createIface()
        return

    def getIcon(self, name):
        card = loader.loadModelCopy('models/textureCards/icons')
        icon = card.find('**/' + name + '*')
        card.removeNode()
        del card
        return icon

    def destroy(self):
        if self.revealTime:
            taskMgr.remove('scoreboardItemGuiWait-' + str(self.revealTime))
        if self.counter:
            self.counter.finish()
            self.counter = None
        self._destroyIface()
        DirectFrame.destroy(self)
        self.ignoreAll()
        return

    def _createIface(self):
        self.descText = DirectLabel(parent=self, relief=None, text=self.item.get('Text'), text_align=TextNode.ALeft, text_scale=0.05, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.02, 0, self.height / 2), text_font=PiratesGlobals.getInterfaceOutlineFont())
        self.valueText = DirectLabel(parent=self, relief=None, text=str(self.item.get('Value1')), text_align=TextNode.ALeft, text_scale=0.05, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(self.width * 0.65, 0, self.height / 2), text_font=PiratesGlobals.getInterfaceOutlineFont())
        if self.item.get('Type') == 'Title':
            self.descText['text_scale'] = 0.055
            self.descText['text_fg'] = PiratesGuiGlobals.TextFG1
            self.descText['text_font'] = PiratesGlobals.getInterfaceOutlineFont()
            self.valueText['text_scale'] = 0.045
            self.valueText['text_font'] = PiratesGlobals.getInterfaceOutlineFont()
            if self.item.has_key('Value2'):
                self.valueText2 = DirectLabel(parent=self, relief=None, text=str(self.item.get('Value2')), text_align=TextNode.ALeft, text_scale=0.05, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(self.width * 0.8, 0, self.height / 2), text_font=PiratesGlobals.getInterfaceOutlineFont())
            if self.valueText2:
                self.valueText2['text_scale'] = 0.045
                self.valueText2['text_font'] = PiratesGlobals.getInterfaceOutlineFont()
        else:
            if self.item.get('Type') == 'Entry':
                self.descText['text_pos'] = (
                 self.width * 0.06, 0, 0)
                if self.item.has_key('Value2'):
                    self.valueText2 = DirectLabel(parent=self, relief=None, text=str(self.item.get('Value2')), text_align=TextNode.ALeft, text_scale=0.05, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(self.width * 0.8, 0, self.height / 2), text_font=PiratesGlobals.getInterfaceOutlineFont())
            else:
                if self.item.get('Type') == 'Space':
                    self.descText['text_scale'] = 0.02
                    self.descText['text'] = ' '
                    self.valueText['text_scale'] = 0.02
                    self.valueText['text'] = ' '
                else:
                    if self.item.get('Type') == 'Button':
                        self.descText['text_pos'] = (
                         self.width * 0.06, 0, 0)
                        self.valueText['text'] = ' '
                        self.button = DirectButton(parent=self, relief=DGG.RIDGE, text=self.item.get('Text'), text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, frameColor=PiratesGuiGlobals.ButtonColor1, command=self.item.get('Value2'), pos=(self.width * 0.65, 0, self.height / 2), borderWidth=(0.01,
                                                                                                                                                                                                                                                                                                                                                                                                         0.01), pad=(0.005,
                                                                                                                                                                                                                                                                                                                                                                                                                     0.005), textMayChange=1)
                        if self.item.get('State') == 'off':
                            self.button['state'] = DGG.DISABLED
                            self.button['text_fg'] = PiratesGuiGlobals.TextFG3
                        elif self.item.get('State') == 'oneShot':
                            self.button.bind(DGG.B1RELEASE, self.disableButton)
                    else:
                        if self.item.get('Type') == 'Cargo':
                            itemId = self.item.get('Value1')
                            iconId = EconomyGlobals.getCargoCategory(itemId)
                            icon = self.icons.get(iconId)
                            self.descText['geom'] = self.getIcon(icon[0])
                            self.descText['geom_scale'] = 0.09 * self.height * 10
                            self.descText['geom_pos'] = (0.05, 0, 0.01)
                            self.descText['text_pos'] = (0.24, 0, 0)
                            self.descText['text'] = icon[1]
                            self.descText['text_fg'] = PiratesGuiGlobals.TextFG2
                            self.descText['text_font'] = PiratesGlobals.getInterfaceOutlineFont()
                            self.descText['text_scale'] = 0.05 * self.height * 10
                            self.descText.setTransparency(1)
                            self.valueText['text'] = PLocalizer.UnknownGoldValue
                            self.valueText['text_font'] = PiratesGlobals.getInterfaceOutlineFont()
                            self.valueText['text_scale'] = 0.05 * self.height * 10
                            icon = self.icons.get(ItemId.CARGO_CRATE)
                            self.descText2 = DirectLabel(parent=self, relief=None, text='?', text_align=TextNode.ACenter, text_scale=0.05 * self.height * 10, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.08, 0, self.height / 2), geom=self.getIcon(icon[0]), geom_scale=0.09 * self.height * 10, geom_pos=(0.1,
                                                                                                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                                                                                                      0.01), text_pos=(0.1,
                                                                                                                                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                                                                                                                                       0), geom_color=Vec4(0, 0, 0, 1), text_font=PiratesGlobals.getInterfaceOutlineFont())
        return

    def reveal(self, args=None):
        if self.item.get('Type') == 'Cargo':
            itemId = self.item.get('Value1')
            icon = self.icons.get(itemId)
            self.descText2['geom'] = self.getIcon(icon[0])
            self.descText2['geom_color'] = Vec4(1, 1, 1, 1)
            value = EconomyGlobals.getCargoValue(itemId)
            self.descText['text'] = icon[1]
            self.descText2['text'] = ''
            self.valueText['text'] = str(value) + ' ' + PLocalizer.MoneyName

    def showSelf(self, args=None):
        self.show()
        if self.item.get('Type') == 'Entry' and isinstance(self.item.get('Value1'), int):

            def refreshValue(val):
                self.valueText['text'] = str(int(val))

            self.counter = LerpFunctionInterval(refreshValue, fromData=0, toData=self.item.get('Value1'), duration=self.revealTime)
            self.counter.start()

    def setRevealTimer(self, time, unwrapMode=0):
        self.revealTime = time
        if unwrapMode:
            taskMgr.doMethodLater(time, self.reveal, 'scoreboardItemGuiWait-' + str(self.revealTime))
        else:
            self.hide()
            taskMgr.doMethodLater(time, self.showSelf, 'scoreboardItemGuiWait-' + str(self.revealTime))

    def _destroyIface(self):
        self.descText.destroy()
        del self.descText
        self.valueText.destroy()
        del self.valueText

    def _handleItemChange(self):
        self._destroyIface()
        self._createIface()

    def disableButton(self, args):
        self.button['state'] = DGG.DISABLED
        self.button['text_fg'] = PiratesGuiGlobals.TextFG3
# okay decompiling .\pirates\piratesgui\ScoreboardItemGui.pyc
