# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.LootPopupPanel
from direct.showbase import DirectObject
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiButton
from pirates.piratesbase import PiratesGlobals
from pirates.makeapirate import ClothingGlobals, JewelryGlobals, TattooGlobals
from direct.interval.IntervalGlobal import *
from pirates.piratesgui import RadialMenu
from pirates.battle import WeaponGlobals
from pirates.piratesbase import CollectionMap
from pirates.piratesgui.MessageStackPanel import StackMessage
from pirates.minigame import PlayingCardGlobals
from pirates.pirate.HumanDNA import hatColors, clothesTopColors, clothesBotColors
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.economy.EconomyGlobals import *

class LootPopupPanel(StackMessage, DirectObject.DirectObject):
    __module__ = __name__
    width = 0.8
    height = 0.2
    lootSfx = None
    BountyTex = None
    CoinTex = None
    CrateTex = None
    ChestTex = None
    RoyalChestTex = None
    TreasureGui = None
    TailorGui = None
    JewelerIconsA = None
    JewelerIconsB = None
    TattooIcons = None
    WeaponIcons = None

    def __init__(self, background=1, extraArgs=[]):
        panelName = PLocalizer.LootPlundered
        StackMessage.__init__(self, text='', text_wordwrap=14, time=PiratesGuiGlobals.LootPopupTime, frameSize=(0, self.width, 0, -self.height, 0))
        self.initialiseoptions(LootPopupPanel)
        self.loot = []
        self.titleLabel = DirectLabel(parent=self, relief=None, text=panelName, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleMed, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceOutlineFont(), textMayChange=1, text_wordwrap=14, sortOrder=21)
        if not LootPopupPanel.lootSfx:
            LootPopupPanel.lootSfx = loader.loadSfx('audio/treasure_hit_1.mp3')
            LootPopupPanel.lootSfx.setVolume(0.75)
            card = loader.loadModel('models/textureCards/icons')
            LootPopupPanel.BountyTex = loader.loadModel('models/gui/avatar_chooser_rope').find('**/avatar_c_B_delete')
            LootPopupPanel.CoinTex = loader.loadModel('models/gui/toplevel_gui').find('**/treasure_w_coin*')
            LootPopupPanel.CrateTex = card.find('**/icon_crate*')
            LootPopupPanel.ChestTex = card.find('**/icon_chest*')
            LootPopupPanel.RoyalChestTex = card.find('**/topgui_icon_ship_chest03*')
            LootPopupPanel.TreasureGui = loader.loadModel('models/gui/treasure_gui')
            LootPopupPanel.TailorGui = loader.loadModel('models/textureCards/tailorIcons')
            LootPopupPanel.JewelerIconsA = loader.loadModel('models/gui/char_gui')
            LootPopupPanel.JewelerIconsB = loader.loadModel('models/textureCards/shopIcons')
            LootPopupPanel.TattooIcons = loader.loadModel('models/textureCards/tattooIcons')
            LootPopupPanel.WeaponIcons = loader.loadModel('models/textureCards/weapon_icons')
        if not background:
            self.frameParent.hide()
            self['relief'] = None
            self.titleLabel['relief'] = None
        self.icons = {ItemId.CARGO_CRATE: (LootPopupPanel.CrateTex, PLocalizer.Crate), ItemId.CARGO_CHEST: (LootPopupPanel.ChestTex, PLocalizer.Chest), ItemId.CARGO_SKCHEST: (LootPopupPanel.RoyalChestTex, PLocalizer.SkChest), ItemId.GOLD: (LootPopupPanel.CoinTex, PLocalizer.MoneyName), ItemId.BOUNTY: (LootPopupPanel.BountyTex, PLocalizer.PVPInfamySpendable)}
        self.titleLabel['text_scale'] = PiratesGuiGlobals.TextScaleLarge
        self.repackPanels()
        return

    def showLoot(self, plunder=[], gold=0, collect=0, card=0, cloth=0, color=0, jewel=None, tattoo=None, weapon=None, bounty=0):
        for loot in self.loot:
            loot.destroy()
            del loot

        self.loot = []
        gender = localAvatar.style.getGender()
        self.show()
        self.setAlphaScale(1.0)
        treasure = []
        for itemId in self.icons.iterkeys():
            count = 0
            for item in plunder:
                if item == itemId:
                    count += 1

            if count > 0:
                treasure.append([itemId, count])

        plunder = treasure
        if gold:
            plunder.append([ItemId.GOLD, gold])
            LootPopupPanel.lootSfx.play()
        if bounty:
            plunder.append([ItemId.BOUNTY, bounty])
            LootPopupPanel.lootSfx.play()
        if collect:
            plunder.append([ItemId.COLLECT, collect])
            LootPopupPanel.lootSfx.play()
        if card:
            plunder.append([ItemId.CARD, card])
            LootPopupPanel.lootSfx.play()
        if cloth:
            plunder.append([ItemId.CLOTHING, (cloth, color)])
            LootPopupPanel.lootSfx.play()
        if jewel is not None:
            plunder.append([ItemId.QUEST_DROP_JEWEL, jewel])
            LootPopupPanel.lootSfx.play()
        if tattoo is not None:
            plunder.append([ItemId.QUEST_DROP_TATTOO, tattoo])
            LootPopupPanel.lootSfx.play()
        if weapon is not None:
            plunder.append([ItemId.QUEST_DROP_WEAPON, weapon])
            LootPopupPanel.lootSfx.play()
        for item in plunder:
            itemType, quantity = item
            if itemType == ItemId.COLLECT:
                itemId = quantity
                howRare = CollectionMap.Collection_Rarity.get(itemId, 0)
                rarityText = PLocalizer.CollectionRarities.get(howRare)
                value = CollectionValues.get(howRare, 0)
                itemName = PLocalizer.Collections[itemId]
                howManyDoIHave = localAvatar.getInventory().getStackQuantity(itemId)
                howManyINeed = CollectionMap.Collection_Needed.get(itemId, 1)
                if howManyDoIHave < howManyINeed:
                    textInfo = PLocalizer.CollectionPopupNewText % (itemName, rarityText, value)
                else:
                    textInfo = PLocalizer.CollectionPopupDuplicateText % (itemName, rarityText, value)
                pic_name = CollectionMap.Assets[itemId]
                lootIcon = LootPopupPanel.TreasureGui.find('**/%s*' % pic_name)
                iconScale = 0.35
            else:
                if itemType == ItemId.CLOTHING:
                    clothingId, colorId = quantity
                    if clothingId in ClothingGlobals.quest_items:
                        textInfo = ClothingGlobals.UNIQUE_ID.get(clothingId)[7]
                    else:
                        textInfo = PLocalizer.TailorColorStrings.get(colorId)
                        textInfo = textInfo + ' ' + ClothingGlobals.getItemTypeName(clothingId)
                    clothingType = ClothingGlobals.getItemType(clothingId)
                    iconScale = 0.13
                    if clothingType == 0:
                        lootIcon = LootPopupPanel.TailorGui.find('**/icon_shop_tailor_hat')
                    elif clothingType == 1:
                        lootIcon = loader.loadModel('models/gui/char_gui').find('**/chargui_cloth')
                        iconScale = 0.3
                    elif clothingType == 2:
                        lootIcon = LootPopupPanel.TailorGui.find('**/icon_shop_tailor_vest')
                    elif clothingType == 3:
                        lootIcon = LootPopupPanel.TailorGui.find('**/icon_shop_tailor_coat')
                    elif clothingType == 4:
                        lootIcon = LootPopupPanel.TailorGui.find('**/icon_shop_tailor_pants')
                    elif clothingType == 5:
                        lootIcon = LootPopupPanel.TailorGui.find('**/icon_shop_tailor_belt')
                    elif clothingType == 6:
                        lootIcon = LootPopupPanel.TailorGui.find('**/icon_shop_tailor_sock')
                    else:
                        lootIcon = LootPopupPanel.TailorGui.find('**/icon_shop_tailor_booths')
                else:
                    if itemType == ItemId.CARD:
                        textInfo = PLocalizer.InventoryTypeNames.get(quantity)
                        pic_name = ''
                        lootIcon = PlayingCardGlobals.getImage('standard', PlayingCardGlobals.getSuit(quantity), PlayingCardGlobals.getRank(quantity))
                        iconScale = 0.2
                    else:
                        if itemType == ItemId.GOLD:
                            textInfo = PLocalizer.LootGold % str(quantity)
                            if base.getHoliday(PiratesGlobals.DOUBLEGOLDHOLIDAYPAID) and Freebooter.getPaidStatus(base.localAvatar.getDoId()) or base.getHoliday(PiratesGlobals.DOUBLEGOLDHOLIDAY):
                                textInfo = PLocalizer.LootGold % str(quantity / 2) + '\n + ' + PLocalizer.LootGoldDouble % str(quantity / 2)
                            lootIcon = self.icons.get(itemType)[0]
                            iconScale = 0.27
                        else:
                            if itemType == ItemId.BOUNTY:
                                textInfo = PLocalizer.LootBounty % str(quantity)
                                lootIcon = self.icons.get(itemType)[0]
                                iconScale = 0.27
                            else:
                                if itemType == ItemId.CARGO_CRATE:
                                    if quantity == 1:
                                        textInfo = PLocalizer.LootCrate % quantity
                                    else:
                                        textInfo = PLocalizer.LootCrateP % quantity
                                    lootIcon = self.icons.get(itemType)[0]
                                    iconScale = 0.09
                                else:
                                    if itemType == ItemId.CARGO_CHEST:
                                        if quantity == 1:
                                            textInfo = PLocalizer.LootChest % quantity
                                        else:
                                            textInfo = PLocalizer.LootChestP % quantity
                                        lootIcon = self.icons.get(itemType)[0]
                                        iconScale = 0.09
                                    else:
                                        if itemType == ItemId.CARGO_SKCHEST:
                                            if quantity == 1:
                                                textInfo = PLocalizer.LootSkChest % quantity
                                            else:
                                                textInfo = PLocalizer.LootSkChestP % quantity
                                            lootIcon = self.icons.get(itemType)[0]
                                            iconScale = 0.09
                                        else:
                                            if itemType == ItemId.QUEST_DROP_JEWEL:
                                                obj = JewelryGlobals.jewelry_id.get(quantity)
                                                textInfo = None
                                                type = None
                                                lootIcon = None
                                                iconScale = 1.0
                                                if obj is not None:
                                                    type = obj[1]
                                                    textInfo = obj[2]
                                                if type == JewelryGlobals.RBROW:
                                                    lootIcon = LootPopupPanel.JewelerIconsB.find('**/icon_shop_tailor_brow')
                                                    iconScale = (-0.14, 0.14, 0.14)
                                                elif type == JewelryGlobals.LBROW:
                                                    lootIcon = LootPopupPanel.JewelerIconsB.find('**/icon_shop_tailor_brow')
                                                    iconScale = (0.14, 0.14, 0.14)
                                                elif type == JewelryGlobals.LEAR:
                                                    lootIcon = LootPopupPanel.JewelerIconsA.find('**/chargui_ears')
                                                    iconScale = (-0.35, 0.35, 0.35)
                                                elif type == JewelryGlobals.REAR:
                                                    lootIcon = LootPopupPanel.JewelerIconsA.find('**/chargui_ears')
                                                    iconScale = (0.35, 0.35, 0.35)
                                                elif type == JewelryGlobals.NOSE:
                                                    lootIcon = LootPopupPanel.JewelerIconsA.find('**/chargui_nose')
                                                    iconScale = (0.35, 0.35, 0.35)
                                                elif type == JewelryGlobals.MOUTH:
                                                    lootIcon = LootPopupPanel.JewelerIconsA.find('**/chargui_mouth')
                                                    iconScale = (0.325, 0.325, 0.325)
                                                elif type == JewelryGlobals.LHAND:
                                                    lootIcon = LootPopupPanel.JewelerIconsB.find('**/icon_shop_tailor_hand')
                                                    iconScale = (0.125, 0.125, 0.125)
                                                elif type == JewelryGlobals.RHAND:
                                                    lootIcon = LootPopupPanel.JewelerIconsB.find('**/icon_shop_tailor_hand')
                                                    iconScale = (-0.125, 0.125, 0.125)
                                                else:
                                                    lootIcon = None
                                            else:
                                                if itemType == ItemId.QUEST_DROP_TATTOO:
                                                    obj = TattooGlobals.tattoos.get(quantity)
                                                    textInfo = None
                                                    type = None
                                                    lootIcon = None
                                                    iconScale = 1.0
                                                    if obj is not None:
                                                        type = obj[0]
                                                        textInfo = obj[3]
                                                    if type == TattooGlobals.ZONE1:
                                                        if gender == 'm':
                                                            lootIcon = LootPopupPanel.TattooIcons.find('**/icon_shop_tailor_chest_male')
                                                        else:
                                                            lootIcon = LootPopupPanel.TattooIcons.find('**/icon_shop_tailor_chest_female')
                                                        iconScale = 0.1
                                                    elif type == TattooGlobals.ZONE2:
                                                        lootIcon = LootPopupPanel.TattooIcons.find('**/icon_shop_tailor_arm')
                                                        iconScale = 0.1
                                                    elif type == TattooGlobals.ZONE3:
                                                        lootIcon = LootPopupPanel.TattooIcons.find('**/icon_shop_tailor_arm')
                                                        iconScale = (-0.1, 0.1, 0.1)
                                                    elif type == TattooGlobals.ZONE4:
                                                        if gender == 'm':
                                                            lootIcon = LootPopupPanel.TattooIcons.find('**/icon_shop_tailor_face_male')
                                                        else:
                                                            lootIcon = LootPopupPanel.TattooIcons.find('**/icon_shop_tailor_face_female')
                                                        iconScale = 0.1
                                                    else:
                                                        lootIcon = None
                                                else:
                                                    if itemType == ItemId.QUEST_DROP_WEAPON:
                                                        weaponId = quantity
                                                        iconScale = 0.1
                                                        textInfo = None
                                                        lootIcon = None
                                                        iconName = getItemIcons(weaponId)
                                                        if iconName is not None:
                                                            lootIcon = LootPopupPanel.WeaponIcons.find('**/' + iconName)
                                                            textInfo = PLocalizer.InventoryTypeNames.get(weaponId)
            entry = DirectFrame(parent=self, relief=None, geom=lootIcon, geom_scale=iconScale, text=textInfo, text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG0, text_pos=(0.07,
                                                                                                                                                                                                                                   0.01), text_font=PiratesGlobals.getInterfaceFont())
            entry.setTransparency(1)
            self.loot.append(entry)

        self.repackPanels()
        return

    def repackPanels(self):
        invHeight = len(self.loot)
        i = 0
        z = 0.1
        iconXOffset = 0.09
        addHeight = (invHeight - 1) * z
        for i in xrange(invHeight):
            iconZOffset = z * (i + 1) - 0.01 - self.height - addHeight
            self.loot[i].setPos(iconXOffset, 0, iconZOffset)

        self.titleLabel.setPos(0.04, 0, -0.06)
        self['frameSize'] = (0, self.width, -self.height - addHeight, 0)
        self.cornerGeom.setPos(0.068, 0, -0.066)
        self.resetFrameSize()

    def destroy(self, autoDestroy=1):
        taskMgr.remove('selfHideTask' + str(self.getParent()))
        self.ignoreAll()
        StackMessage.destroy(self, autoDestroy)
# okay decompiling .\pirates\piratesgui\LootPopupPanel.pyc
