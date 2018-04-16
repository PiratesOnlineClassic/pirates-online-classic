# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.makeapirate.ClothesGUI
import random

from CharGuiBase import CharGuiPicker, CharGuiSlider
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from direct.showbase import DirectObject
from direct.showbase.PythonUtil import Functor
from direct.showbase.ShowBaseGlobal import *
from direct.task import Task
from pandac.PandaModules import *
from pirates.makeapirate import ClothingGlobals
from pirates.pirate import HumanDNA
from pirates.piratesbase import PLocalizer

genderIdx = 0
topNumColor = 21
botNumColor = 21
HAT = 0
SHIRT = 1
VEST = 2
COAT = 3
PANT = 4
BELT = 5
SOCK = 6
SHOE = 7

class ClothesGUI(DirectFrame, StateData.StateData):
    
    notify = DirectNotifyGlobal.directNotify.newCategory('ClothesGUI')

    def __init__(self, main=None):
        self.main = main
        self._parent = main.bookModel
        self.avatar = main.avatar
        self.mode = None
        self.entered = False
        self.once = False
        self.load()
        self.texName = ''
        self.lastRun = 0
        return

    def enter(self):
        self.entered = True
        if self.mode == None:
            self.mode = -1
        self.handleClothingChanged()
        self.show()
        return

    def exit(self):
        self.entered = False
        self.hide()

    def save(self):
        if self.mode == -1:
            pass

    def assignAvatar(self, avatar):
        global genderIdx
        self.avatar = avatar
        genderIdx = 0
        if avatar.dna.getGender() == 'f':
            genderIdx = 1

    def load(self):
        self.loadShirtGUI()
        self.loadPantGUI()
        self.loadShoeGUI()
        self.loadHatGUI()

    def loadShirtGUI(self):
        self.clothesFrame = DirectFrame(parent=self._parent, relief=None, pos=(0, 0,
                                                                              0), scale=1)
        self.clothesFrame.hide()
        self.genPicsButtonsFrame = DirectFrame(parent=self.clothesFrame, relief=None, pos=(0,
                                                                                           0,
                                                                                           0), scale=1)
        if not base.config.GetBool('want-gen-pics-buttons', 0):
            self.genPicsButtonsFrame.hide()
        self.shirtPicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingShirtStyle, nextCommand=Functor(self.handleNextClothing, 'SHIRT'), backCommand=Functor(self.handleLastClothing, 'SHIRT'))
        self.shirtPicker.setPos(-0.3, 0, 0.1)
        self.shirtGenPics = DirectButton(parent=self.genPicsButtonsFrame, relief=DGG.RAISED, frameSize=(-0.17, 0.17, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                                0.008), text=PLocalizer.GeneratePictures, text_pos=(0, -0.015), text_scale=0.08, pos=(-1,
                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                      0.1), command=self.handleShirtGenPics)
        self.vestPicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingVestStyle, nextCommand=Functor(self.handleNextClothing, 'VEST'), backCommand=Functor(self.handleLastClothing, 'VEST'))
        self.vestPicker.setPos(-0.3, 0, -0.3)
        self.vestGenPics = DirectButton(parent=self.genPicsButtonsFrame, relief=DGG.RAISED, frameSize=(-0.17, 0.17, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                               0.008), text=PLocalizer.GeneratePictures, text_pos=(0, -0.015), text_scale=0.08, pos=(-1, 0, -0.3), command=self.handleVestGenPics)
        self.coatPicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingCoatStyle, nextCommand=Functor(self.handleNextClothing, 'COAT'), backCommand=Functor(self.handleLastClothing, 'COAT'))
        self.coatPicker.setPos(-0.3, 0, -0.7)
        self.coatGenPics = DirectButton(parent=self.genPicsButtonsFrame, relief=DGG.RAISED, frameSize=(-0.17, 0.17, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                               0.008), text=PLocalizer.GeneratePictures, text_pos=(0, -0.015), text_scale=0.08, pos=(-1, 0, -0.7), command=self.handleCoatGenPics)
        self.loadTopColorGUI()
        if self.main.wantNPCViewer:
            self.loadTopTextureGUI()
        return

    def loadHatGUI(self):
        self.hatPicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingHatStyle, nextCommand=Functor(self.handleNextClothing, 'HAT'), backCommand=Functor(self.handleLastClothing, 'HAT'))
        self.hatPicker.setPos(-0.3, 0.0, 0.4)
        self.hatGenPics = DirectButton(parent=self.genPicsButtonsFrame, relief=DGG.RAISED, frameSize=(-0.17, 0.17, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                              0.008), text=PLocalizer.GeneratePictures, text_pos=(0, -0.015), text_scale=0.08, pos=(-1,
                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                    -1.1), command=self.handleHatGenPics)

    def loadPantGUI(self):
        self.pantPicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingPantStyle, nextCommand=Functor(self.handleNextClothing, 'PANT'), backCommand=Functor(self.handleLastClothing, 'PANT'))
        self.pantPicker.setPos(-0.3, 0.0, -1.1)
        self.pantGenPics = DirectButton(parent=self.genPicsButtonsFrame, relief=DGG.RAISED, frameSize=(-0.17, 0.17, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                               0.008), text=PLocalizer.GeneratePictures, text_pos=(0, -0.015), text_scale=0.08, pos=(-1,
                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                     -1.1), command=self.handlePantGenPics)
        self.beltPicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingBeltStyle, nextCommand=Functor(self.handleNextClothing, 'BELT'), backCommand=Functor(self.handleLastClothing, 'BELT'))
        self.beltPicker.setPos(-0.3, 0.0, -1.5)
        self.beltGenPics = DirectButton(parent=self.genPicsButtonsFrame, relief=DGG.RAISED, frameSize=(-0.17, 0.17, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                               0.008), text=PLocalizer.GeneratePictures, text_pos=(0, -0.015), text_scale=0.08, pos=(-1,
                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                     -1.46), command=self.handleBeltGenPics)
        self.loadBotColorGUI()

    def loadShoeGUI(self):
        self.shoePicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingShoeStyle, nextCommand=Functor(self.handleNextClothing, 'SHOE'), backCommand=Functor(self.handleLastClothing, 'SHOE'))
        self.shoePicker.setPos(-0.3, 0.0, -1.75)
        self.shoeGenPics = DirectButton(parent=self.genPicsButtonsFrame, relief=DGG.RAISED, frameSize=(-0.17, 0.17, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                               0.008), text=PLocalizer.GeneratePictures, text_pos=(0, -0.015), text_scale=0.08, pos=(-1,
                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                     -1.75), command=self.handleShoeGenPics)
        self.sockPicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingSockStyle, nextCommand=Functor(self.handleNextClothing, 'SHOE'), backCommand=Functor(self.handleLastClothing, 'SHOE'))
        self.sockPicker.setPos(-0.3, 0.0, -2.15)
        wantSocks = base.config.GetBool('want-socks', 0)
        if not wantSocks:
            self.sockPicker.hide()
        self.loadBotColorGUI()
        if self.main.wantNPCViewer:
            self.loadBotTextureGUI()

    def loadTopColorGUI(self):

        def makeColorButtons(frame, colorButtons, colors, xOffset, yOffset, a, b):
            lastTotal = len(colorButtons)
            for i in range(lastTotal, lastTotal + len(colors[a:b])):
                currTotal = i - lastTotal
                if currTotal and currTotal % 7 == 0:
                    xOffset = 0.0
                    yOffset -= 0.1
                clothesColor = colors[currTotal]
                clothesTone = (clothesColor[0], clothesColor[1], clothesColor[2], 1.0)
                colorButtons.append(DirectButton(parent=frame, relief=DGG.RAISED, pos=(xOffset, 0, yOffset), frameSize=(-0.1, 0.1, -0.1, 0.1), borderWidth=(0.008,
                                                                                                                                                            0.008), frameColor=clothesTone, scale=0.5, command=self.handleSetTopColor, extraArgs=[i]))
                xOffset += 0.1

        xOffset = 0.0
        yOffset = 0.0
        self.maleTopColorButtons = []
        self.maleShirtColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame02'), image_scale=(1.1,
                                                                                                                                                            1,
                                                                                                                                                            1.2), image_pos=(0.3, 0, -0.1), scale=0.8, pos=(0.35,
                                                                                                                                                                                                            0,
                                                                                                                                                                                                            0.15))
        makeColorButtons(self.maleShirtColorFrameTitle, self.maleTopColorButtons, HumanDNA.clothesTopColors[0], xOffset, yOffset, 0, topNumColor)
        self.maleShirtColorFrameTitle.hide()
        self.maleVestColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame02'), image_scale=(1.1,
                                                                                                                                                           1,
                                                                                                                                                           1.2), image_pos=(0.3, 0, -0.1), scale=0.8, pos=(0.35, 0, -0.25))
        makeColorButtons(self.maleVestColorFrameTitle, self.maleTopColorButtons, HumanDNA.clothesTopColors[0], xOffset, yOffset, 0, topNumColor)
        self.maleVestColorFrameTitle.hide()
        self.maleCoatColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame02'), image_scale=(1.1,
                                                                                                                                                           1,
                                                                                                                                                           1.2), image_pos=(0.3, 0, -0.1), scale=0.8, pos=(0.35, 0, -0.65))
        makeColorButtons(self.maleCoatColorFrameTitle, self.maleTopColorButtons, HumanDNA.clothesTopColors[0], xOffset, yOffset, 0, topNumColor)
        self.maleCoatColorFrameTitle.hide()
        self.femaleTopColorButtons = []
        self.femaleShirtColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame02'), image_scale=(1.1,
                                                                                                                                                              1,
                                                                                                                                                              1.2), image_pos=(0.3, 0, -0.1), scale=0.8, pos=(0.35,
                                                                                                                                                                                                              0,
                                                                                                                                                                                                              0.15))
        makeColorButtons(self.femaleShirtColorFrameTitle, self.femaleTopColorButtons, HumanDNA.clothesTopColors[1], xOffset, yOffset, 0, topNumColor)
        self.femaleShirtColorFrameTitle.hide()
        self.femaleVestColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame02'), image_scale=(1.1,
                                                                                                                                                             1,
                                                                                                                                                             1.2), image_pos=(0.3, 0, -0.1), scale=0.8, pos=(0.35, 0, -0.25))
        makeColorButtons(self.femaleVestColorFrameTitle, self.femaleTopColorButtons, HumanDNA.clothesTopColors[1], xOffset, yOffset, 0, topNumColor)
        self.femaleVestColorFrameTitle.hide()
        self.femaleCoatColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame02'), image_scale=(1.1,
                                                                                                                                                             1,
                                                                                                                                                             1.2), image_pos=(0.3, 0, -0.1), scale=0.8, pos=(0.35, 0, -0.65))
        makeColorButtons(self.femaleCoatColorFrameTitle, self.femaleTopColorButtons, HumanDNA.clothesTopColors[1], xOffset, yOffset, 0, topNumColor)
        self.femaleCoatColorFrameTitle.hide()
        return

    def loadTopTextureGUI(self):
        self.hatTexturePicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingHatTrend, nextCommand=Functor(self.handleNextTexture, 'HAT'), backCommand=Functor(self.handleLastTexture, 'HAT'))
        self.hatTexturePicker.setPos(-0.3, 0, 0.25)
        self.shirtTexturePicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingShirtTrend, nextCommand=Functor(self.handleNextTexture, 'SHIRT'), backCommand=Functor(self.handleLastTexture, 'SHIRT'))
        self.shirtTexturePicker.setPos(-0.3, 0, -0.05)
        self.vestTexturePicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingVestTrend, nextCommand=Functor(self.handleNextTexture, 'VEST'), backCommand=Functor(self.handleLastTexture, 'VEST'))
        self.vestTexturePicker.setPos(-0.3, 0, -0.45)
        self.coatTexturePicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingCoatTrend, nextCommand=Functor(self.handleNextTexture, 'COAT'), backCommand=Functor(self.handleLastTexture, 'COAT'))
        self.coatTexturePicker.setPos(-0.3, 0, -0.85)

    def loadBotTextureGUI(self):
        self.pantTexturePicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingPantTrend, nextCommand=Functor(self.handleNextTexture, 'PANT'), backCommand=Functor(self.handleLastTexture, 'PANT'))
        self.pantTexturePicker.setPos(-0.3, 0, -1.25)
        self.shoeTexturePicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingShoeTrend, nextCommand=Functor(self.handleNextTexture, 'SHOE'), backCommand=Functor(self.handleLastTexture, 'SHOE'))
        self.shoeTexturePicker.setPos(-0.3, 0, -1.9)

    def loadBotColorGUI(self):
        idx = 0
        self.maleBotColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame02'), image_scale=(1.1,
                                                                                                                                                          1,
                                                                                                                                                          1.2), image_pos=(0.3, 0, -0.1), scale=0.8, pos=(0.35,
                                                                                                                                                                                                          0,
                                                                                                                                                                                                          -1.05))
        self.maleBotColorFrameTitle.hide()
        self.maleBotColorButtons = []
        xOffset = 0.0
        yOffset = 0.0
        for i in range(0, HumanDNA.ClothesMaxMAPColor):
            currTotal = i - 0
            if currTotal and currTotal % 7 == 0:
                xOffset = 0.0
                yOffset -= 0.1
            clothesColor = HumanDNA.clothesBotColors[idx][currTotal]
            clothesTone = (clothesColor[0], clothesColor[1], clothesColor[2], 1.0)
            self.maleBotColorButtons.append(DirectButton(parent=self.maleBotColorFrameTitle, relief=DGG.RAISED, pos=(xOffset, 0, yOffset), frameSize=(-0.1, 0.1, -0.1, 0.1), borderWidth=(0.008,
                                                                                                                                                                                          0.008), frameColor=clothesTone, scale=0.5, command=self.handleSetBotColor, extraArgs=[i]))
            xOffset += 0.1

        idx = 1
        self.femaleBotColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame02'), image_scale=(1.1,
                                                                                                                                                            1,
                                                                                                                                                            1.2), image_pos=(0.3, 0, -0.1), scale=0.8, pos=(0.35,
                                                                                                                                                                                                            0,
                                                                                                                                                                                                            -1.05))
        self.femaleBotColorFrameTitle.hide()
        self.femaleBotColorButtons = []
        xOffset = 0.0
        yOffset = 0.0
        for i in range(0, HumanDNA.ClothesMaxMAPColor):
            currTotal = i - 0
            if currTotal and currTotal % 7 == 0:
                xOffset = 0.0
                yOffset -= 0.1
            clothesColor = HumanDNA.clothesBotColors[idx][currTotal]
            clothesTone = (clothesColor[0], clothesColor[1], clothesColor[2], 1.0)
            self.femaleBotColorButtons.append(DirectButton(parent=self.femaleBotColorFrameTitle, relief=DGG.RAISED, pos=(xOffset, 0, yOffset), frameSize=(-0.1, 0.1, -0.1, 0.1), borderWidth=(0.008,
                                                                                                                                                                                              0.008), frameColor=clothesTone, scale=0.5, command=self.handleSetBotColor, extraArgs=[i]))
            xOffset += 0.1

        return

    def unload(self):
        del self.main
        del self._parent
        del self.avatar

    def showApparelCollections(self):
        if self.entered:
            self.clothesFrame.show()
            self.showTopColorCollections()
            self.showBotColorCollections()

    def showTopColorCollections(self):
        colorButtons = self.maleTopColorButtons
        if self.main.pirate.style.gender == 'f':
            colorButtons = self.femaleTopColorButtons
        clothesTopColor = self.avatar.dna.getClothesTopColor()
        if self.main.pirate.style.gender == 'm':
            self.maleShirtColorFrameTitle.show()
            self.maleVestColorFrameTitle.show()
            self.maleCoatColorFrameTitle.show()
        else:
            self.femaleShirtColorFrameTitle.show()
            self.femaleVestColorFrameTitle.show()
            self.femaleCoatColorFrameTitle.show()
        for i in range(0, topNumColor):
            colorButtons[i]['relief'] = DGG.RAISED

        colorButtons[clothesTopColor[0]]['relief'] = DGG.SUNKEN
        for i in range(topNumColor * 1, topNumColor * 2):
            colorButtons[i]['relief'] = DGG.RAISED

        colorButtons[topNumColor + clothesTopColor[1]]['relief'] = DGG.SUNKEN
        for i in range(topNumColor * 2, topNumColor * 3):
            colorButtons[i]['relief'] = DGG.RAISED

        colorButtons[topNumColor * 2 + clothesTopColor[2]]['relief'] = DGG.SUNKEN

    def showBotColorCollections(self):
        clothesBotColor = self.avatar.dna.getClothesBotColor()
        if self.main.pirate.style.gender == 'f':
            self.femaleBotColorFrameTitle.show()
            for i in range(0, len(self.femaleBotColorButtons)):
                self.femaleBotColorButtons[i]['relief'] = DGG.RAISED

            self.femaleBotColorButtons[clothesBotColor[0]]['relief'] = DGG.SUNKEN
        else:
            self.maleBotColorFrameTitle.show()
            for i in range(0, len(self.maleBotColorButtons)):
                self.maleBotColorButtons[i]['relief'] = DGG.RAISED

            self.maleBotColorButtons[clothesBotColor[0]]['relief'] = DGG.SUNKEN

    def hideApparelCollections(self):
        self.clothesFrame.hide()
        self.maleShirtColorFrameTitle.hide()
        self.maleVestColorFrameTitle.hide()
        self.maleCoatColorFrameTitle.hide()
        self.maleBotColorFrameTitle.hide()
        self.femaleShirtColorFrameTitle.hide()
        self.femaleVestColorFrameTitle.hide()
        self.femaleCoatColorFrameTitle.hide()
        self.femaleBotColorFrameTitle.hide()

    def show(self):
        self.showApparelCollections()
        if self.main.inRandomAll:
            return
        if self.once:
            idx = 0
            if self.main.pirate.gender == 'f':
                idx = 1
            optionsLeft = len(self.main.JSD_CLOTHING_INTRO[idx])
            if optionsLeft:
                choice = random.choice(range(0, optionsLeft))
                if self.main.lastDialog:
                    self.main.lastDialog.stop()
                dialog = self.main.JSD_CLOTHING_INTRO[idx][choice]
                base.playSfx(dialog, node=self.avatar.pirate)
                self.main.lastDialog = dialog
                self.main.JSD_CLOTHING_INTRO[idx].remove(dialog)
        else:
            self.once = True

    def hide(self):
        self.hideApparelCollections()

    def restore(self):
        self.hideApparelCollections()
        self.showApparelCollections()

    def reset(self):
        baseHat = self.avatar.choices['HAT'].keys()[0]
        baseShirt = self.avatar.choices['SHIRT'].keys()[0]
        baseShirtTex = self.avatar.choices['SHIRT'][baseShirt][0]
        baseVest = self.avatar.choices['VEST'].keys()[0]
        baseVestTex = self.avatar.choices['VEST'][baseVest][0]
        baseCoat = self.avatar.choices['COAT'].keys()[0]
        baseCoatTex = self.avatar.choices['COAT'][baseCoat][0]
        basePant = self.avatar.choices['PANT'].keys()[0]
        basePantTex = self.avatar.choices['PANT'][basePant][0]
        baseBelt = self.avatar.choices['BELT'].keys()[0]
        baseBeltTex = self.avatar.choices['BELT'][baseBelt][0]
        baseShoe = self.avatar.choices['SHOE'].keys()[0]
        baseShoeTex = self.avatar.choices['SHOE'][baseShoe][0]
        self.avatar.currentClothing = {'HAT': [baseHat, 0], 'SHIRT': [baseShirt, baseShirtTex, 0], 'VEST': [baseVest, baseVestTex, 0], 'COAT': [baseCoat, baseCoatTex, 0], 'BELT': [baseBelt, baseBeltTex, 0], 'PANT': [basePant, basePantTex, 0], 'SHOE': [baseShoe, baseShoeTex, 0]}
        self.avatar.pirate.setClothesPant(0, 0)
        self.avatar.pirate.setClothesBelt(0, 0)
        self.avatar.pirate.setClothesShirt(0, 0)
        self.avatar.pirate.setClothesVest(0, 0)
        self.avatar.pirate.setClothesCoat(0, 0)
        self.avatar.pirate.setClothesShoe(0, 0)
        self.handleSetTopColor(topNumColor * 0)
        self.handleSetTopColor(topNumColor * 1)
        self.handleSetTopColor(topNumColor * 2)
        self.handleSetBotColor(0)
        self.handleClothingChanged()

    def randomPick(self):
        self.avatar.clothing.stash()
        for type in ['HAT', 'SHIRT', 'VEST', 'COAT', 'PANT', 'BELT', 'SHOE']:
            itemId = random.choice(self.avatar.choices[type].keys())
            texId = random.choice(self.avatar.choices[type][itemId])
            self.avatar.currentClothing[type] = [itemId, texId, 0]
            self.avatar.pirate.setClothesByType(type, itemId, texId, 0)

        if self.avatar.currentClothing['VEST'][0] != 0:
            self.avatar.currentClothing['COAT'] = [
             0, 0, 0]
            self.avatar.pirate.setClothesByType(type, itemId, texId, 0)
        choice = random.choice(range(0, len(HumanDNA.clothesTopColors[genderIdx][:topNumColor])))
        self.avatar.currentClothing['SHIRT'][2] = choice
        self.handleSetTopColor(choice + topNumColor * 0)
        choice = random.choice(range(0, len(HumanDNA.clothesTopColors[genderIdx][:topNumColor])))
        self.avatar.currentClothing['VEST'][2] = choice
        self.handleSetTopColor(choice + topNumColor * 1)
        choice = random.choice(range(0, len(HumanDNA.clothesTopColors[genderIdx][:topNumColor])))
        self.avatar.currentClothing['COAT'][2] = choice
        self.handleSetTopColor(choice + topNumColor * 2)
        choice = random.choice(range(0, len(HumanDNA.clothesBotColors[genderIdx][:botNumColor])))
        self.avatar.currentClothing['PANT'][2] = choice
        self.handleSetBotColor(choice)
        self.handleClothingChanged()

    def handleNextClothing(self, type):
        if not self.main.wantNPCViewer:
            clothing = self.getNextClothingItem(type)
            self.main.playJackDialogOnClothes(type)
        else:
            if self.main.wantPicButtons:
                clothing = self.getNextClothingItem(type)
            else:
                clothing = self.getNextClothingModel(type)
            self.texName = self.avatar.getTextureName(type, clothing[0], clothing[1])[0]
            self.main.guiTextureInfo[type]['text'] = self.texName
            self.main.guiTextureInfo[type]['text_fg'] = (1, 1, 1, 1)
        self.avatar.pirate.setClothesByType(type, clothing[0], clothing[1])
        self.avatar.currentClothing[type][0] = clothing[0]
        self.avatar.currentClothing[type][1] = clothing[1]
        self.handleClothingChanged()
        if base.config.GetBool('want-map-flavor-anims', 0):
            currTime = globalClock.getFrameTime()
            if self.main.pirate.style.gender == 'f':
                if currTime - self.lastRun > 10:
                    if type == 'SHOE':
                        if random.randint(0, 1) == 0:
                            self.avatar.pirate.play('map_look_boot_left')
                        else:
                            self.avatar.pirate.play('map_look_boot_right')
                    self.lastRun = currTime
                currTime = globalClock.getFrameTime()
            elif currTime - self.lastRun > 10:
                if type == 'SHIRT' or type == 'COAT':
                    if random.randint(0, 1) == 0:
                        self.avatar.pirate.play('map_look_arm_left')
                    else:
                        self.avatar.pirate.play('map_look_arm_right')
                if type == 'PANT' or type == 'BELT':
                    self.avatar.pirate.play('map_look_pant_right')
                if type == 'SHOE':
                    self.avatar.pirate.play('map_look_boot_left')
                self.lastRun = currTime

    def handleLastClothing(self, type):
        if not self.main.wantNPCViewer:
            clothing = self.getLastClothingItem(type)
            self.main.playJackDialogOnClothes(type)
        else:
            if self.main.wantPicButtons:
                clothing = self.getLastClothingItem(type)
            else:
                clothing = self.getLastClothingModel(type)
            texName = self.avatar.getTextureName(type, clothing[0], clothing[1])[0]
            self.main.guiTextureInfo[type]['text'] = texName
            self.main.guiTextureInfo[type]['text_fg'] = (1, 1, 1, 1)
        self.avatar.pirate.setClothesByType(type, clothing[0], clothing[1])
        self.avatar.currentClothing[type][0] = clothing[0]
        self.avatar.currentClothing[type][1] = clothing[1]
        if self.main.wantNPCViewer:
            self.texName = self.avatar.getTextureName(SHIRT, self.avatar.clothingShirtIdx, self.avatar.clothingShirtTexture)
            self.main.guiTextureInfo['text'] = self.texName
            self.main.guiTextureInfo['text_fg'] = (1, 1, 1, 1)
        self.handleClothingChanged()
        if base.config.GetBool('want-map-flavor-anims', 0):
            currTime = globalClock.getFrameTime()
            if self.main.pirate.style.gender == 'f':
                if currTime - self.lastRun > 10:
                    if type == 'SHOE':
                        if random.randint(0, 1) == 0:
                            self.avatar.pirate.play('map_look_boot_left')
                        else:
                            self.avatar.pirate.play('map_look_boot_right')
                    self.lastRun = currTime
                currTime = globalClock.getFrameTime()
            else:
                currTime = globalClock.getFrameTime()
                if currTime - self.lastRun > 10:
                    if type == 'SHIRT' or type == 'COAT':
                        if random.randint(0, 1) == 0:
                            self.avatar.pirate.play('map_look_arm_left')
                        else:
                            self.avatar.pirate.play('map_look_arm_right')
                    if type == 'PANT' or type == 'BELT':
                        self.avatar.pirate.play('map_look_pant_right')
                    if type == 'SHOE':
                        self.avatar.pirate.play('map_look_boot_left')
                    self.lastRun = currTime

    def handleNextTexture(self, type):
        clothing = self.getNextClothingTexture(type)
        self.avatar.currentClothing[type][0] = clothing[0]
        self.avatar.currentClothing[type][1] = clothing[1]
        self.avatar.pirate.setClothesByType(type, clothing[0], clothing[1])
        if self.main.wantNPCViewer:
            self.texName = self.avatar.getTextureName(type, clothing[0], clothing[1])[0]
            self.main.guiTextureInfo[type]['text'] = self.texName
            self.main.guiTextureInfo[type]['text_fg'] = (1, 1, 1, 1)
        self.handleClothingChanged()

    def handleLastTexture(self, type):
        clothing = self.getLastClothingTexture(type)
        self.avatar.currentClothing[type][0] = clothing[0]
        self.avatar.currentClothing[type][1] = clothing[1]
        self.avatar.pirate.setClothesByType(type, clothing[0], clothing[1])
        if self.main.wantNPCViewer:
            self.texName = self.avatar.getTextureName(type, clothing[0], clothing[1])[0]
            self.main.guiTextureInfo[type]['text'] = self.texName
            self.main.guiTextureInfo[type]['text_fg'] = (1, 1, 1, 1)
        self.handleClothingChanged()

    def handleSetTopColor(self, color):
        colorButtons = self.maleTopColorButtons
        if self.main.pirate.style.gender == 'f':
            colorButtons = self.femaleTopColorButtons
        clothesTopColor = self.avatar.dna.getClothesTopColor()
        if color >= topNumColor * 0 and color < topNumColor * 1:
            clothesTopColor[0] = color
            for i in range(topNumColor * 0, topNumColor * 1):
                colorButtons[i]['relief'] = DGG.RAISED

            colorButtons[color]['relief'] = DGG.SUNKEN
        else:
            if color >= topNumColor * 1 and color < topNumColor * 2:
                clothesTopColor[1] = color - topNumColor * 1
                for i in range(topNumColor * 1, topNumColor * 2):
                    colorButtons[i]['relief'] = DGG.RAISED

                colorButtons[color]['relief'] = DGG.SUNKEN
            else:
                if color >= topNumColor * 2 and color < topNumColor * 3:
                    clothesTopColor[2] = color - topNumColor * 2
                    for i in range(topNumColor * 2, topNumColor * 3):
                        colorButtons[i]['relief'] = DGG.RAISED

                    colorButtons[color]['relief'] = DGG.SUNKEN
        self.main.pirate.setClothesTopColor(clothesTopColor[0], clothesTopColor[1], clothesTopColor[2])
        self.main.pirate.model.handleClothesHiding()

    def handleSetBotColor(self, color):
        colorButtons = self.maleBotColorButtons
        if self.main.pirate.style.gender == 'f':
            colorButtons = self.femaleBotColorButtons
        for i in range(0, len(colorButtons)):
            colorButtons[i]['relief'] = DGG.RAISED

        colorButtons[color]['relief'] = DGG.SUNKEN
        clothesBotColor = self.avatar.dna.getClothesBotColor()
        if color >= botNumColor * 0 and color < botNumColor * 1:
            clothesBotColor[0] = color
        else:
            if color >= 5 and color < 10:
                clothesBotColor[1] = color
            else:
                if color >= 10 and color < 15:
                    clothesBotColor[2] = color
        self.main.pirate.setClothesBotColor(clothesBotColor[0], clothesBotColor[1], clothesBotColor[2])
        self.main.pirate.model.handleClothesHiding()

    def generatePics(self, type):
        render2d.hide()
        self.avatar.pirate.findAllMatches('**/drop*').getPath(1).hide()
        self.hidePirate()
        self.hideOtherClothes(type)
        clothingSize = self.getClothingSize(type)
        for i in range(0, clothingSize):
            if i == 0:
                self.texName = self.avatar.getTextureName(type, self.avatar.currentClothing[type][0], self.avatar.currentClothing[type][1])[0]
            if i < 10:
                prefix = '0'
            else:
                prefix = ''
            self.avatar.pirate.setHpr(180, 0, 0)
            self.notify.info('SCREENSHOT %d__%s__FRONT' % (i, self.texName))
            uFilename = type + '_' + prefix + str(i) + '__' + self.texName + '__FRONT.' + base.screenshotExtension
            base.graphicsEngine.renderFrame()
            base.screenshot(namePrefix=uFilename, defaultFilename=0)
            self.avatar.pirate.setHpr(0, 0, 0)
            self.notify.info('SCREENSHOT %d__%s__BACK' % (i, self.texName))
            uFilename = type + '_' + prefix + str(i) + '__' + self.texName + '__BACK.' + base.screenshotExtension
            base.graphicsEngine.renderFrame()
            base.screenshot(namePrefix=uFilename, defaultFilename=0)
            self.handleNextClothing(type)

        self.notify.info('done with shirt screencaps')
        render2d.show()
        self.avatar.pirate.findAllMatches('**/drop*').getPath(1).show()
        self.showPirate()
        self.avatar.pirate.setHpr(180, 0, 0)
        self.showOtherClothes(type)

    def handleShirtGenPics(self):
        taskMgr.remove('avCreate-ZoomTask')
        oldPos = base.camera.getPos()
        if self.main.pirate.gender == 'f':
            base.camera.setPos(-0.2, -5, 5.27)
        else:
            base.camera.setPos(-0.2, -5, 5.3)
        self.generatePics('SHIRT')
        base.camera.setPos(oldPos)
        taskMgr.add(self.main.zoomTask, 'avCreate-ZoomTask')

    def handleVestGenPics(self):
        taskMgr.remove('avCreate-ZoomTask')
        oldPos = base.camera.getPos()
        if self.main.pirate.gender == 'f':
            base.camera.setPos(-0.2, -4.1, 4.95)
        else:
            base.camera.setPos(-0.2, -5, 5.3)
        self.generatePics('VEST')
        base.camera.setPos(oldPos)
        taskMgr.add(self.main.zoomTask, 'avCreate-ZoomTask')

    def handleCoatGenPics(self):
        taskMgr.remove('avCreate-ZoomTask')
        oldPos = base.camera.getPos()
        if self.main.pirate.gender == 'f':
            base.camera.setPos(-0.2, -6.6, 5.3)
        else:
            base.camera.setPos(-0.2, -7.5, 5.4)
        self.generatePics('COAT')
        base.camera.setPos(oldPos)
        taskMgr.add(self.main.zoomTask, 'avCreate-ZoomTask')

    def handlePantGenPics(self):
        taskMgr.remove('avCreate-ZoomTask')
        oldPos = base.camera.getPos()
        if self.main.pirate.gender == 'f':
            base.camera.setPos(-0.1, -8, 4)
        else:
            base.camera.setPos(-0.2, -5.5, 3.7)
        self.generatePics('PANT')
        base.camera.setPos(oldPos)
        taskMgr.add(self.main.zoomTask, 'avCreate-ZoomTask')

    def handleBeltGenPics(self):
        taskMgr.remove('avCreate-ZoomTask')
        oldPos = base.camera.getPos()
        if self.main.pirate.gender == 'f':
            base.camera.setPos(-0.1, -4.1, 3.8)
        else:
            base.camera.setPos(-0.1, -3.9, 3.55)
        self.generatePics('BELT')
        base.camera.setPos(oldPos)
        taskMgr.add(self.main.zoomTask, 'avCreate-ZoomTask')

    def handleShoeGenPics(self):
        taskMgr.remove('avCreate-ZoomTask')
        oldPos = base.camera.getPos()
        if self.main.pirate.gender == 'f':
            base.camera.setPos(-0.1, -5, 2.4)
        else:
            base.camera.setPos(-0.1, -4, 1.5)
        self.generatePics('SHOE')
        base.camera.setPos(oldPos)
        taskMgr.add(self.main.zoomTask, 'avCreate-ZoomTask')

    def handleHatGenPics(self):
        taskMgr.remove('avCreate-ZoomTask')
        oldPos = base.camera.getPos()
        if self.main.pirate.gender == 'f':
            base.camera.setPos(-0.1, -3, 6.1)
        else:
            base.camera.setPos(0, -3, 6.5)
        self.generatePics('HAT')
        base.camera.setPos(oldPos)
        taskMgr.add(self.main.zoomTask, 'avCreate-ZoomTask')

    def getNextClothingItem(self, type):
        itemId, textureId, color = self.avatar.currentClothing[type]
        if itemId not in self.avatar.choices[type]:
            self.notify.error('masad: how did it get here? itemId = %s' % itemId)
        itemTextures = self.avatar.choices[type][itemId]
        currentTexIdx = itemTextures.index(textureId)
        texIdx = currentTexIdx + 1
        if texIdx >= len(itemTextures):
            itemIds = self.avatar.choices[type].keys()
            itemIds.sort()
            currIdx = itemIds.index(itemId)
            if currIdx + 1 < len(itemIds):
                newIdx = itemIds[currIdx + 1]
            else:
                newIdx = itemIds[0]
            itemId = newIdx
            textureId = self.avatar.choices[type][newIdx][0]
        else:
            textureId = self.avatar.choices[type][itemId][texIdx]
        return (itemId, textureId)

    def getLastClothingItem(self, type):
        itemId, textureId, color = self.avatar.currentClothing[type]
        if itemId not in self.avatar.choices[type]:
            self.notify.error('masad: how did it get here? itemId = %s' % itemId)
        itemTextures = self.avatar.choices[type][itemId]
        currentTexIdx = itemTextures.index(textureId)
        texIdx = currentTexIdx - 1
        if texIdx < 0:
            itemIds = self.avatar.choices[type].keys()
            itemIds.sort()
            currIdx = itemIds.index(itemId)
            itemId = itemIds[currIdx - 1]
            textureId = self.avatar.choices[type][itemId][-1]
        else:
            textureId = self.avatar.choices[type][itemId][texIdx]
        return (
         itemId, textureId)

    def getNextClothingModel(self, type):
        models = self.avatar.choices[type].keys()
        models.sort()
        currIdx = models.index(self.avatar.currentClothing[type][0])
        currIdx += 1
        if currIdx >= len(models):
            itemId = models[0]
        else:
            itemId = models[currIdx]
        return (itemId, self.avatar.choices[type][itemId][0])

    def getLastClothingModel(self, type):
        models = self.avatar.choices[type].keys()
        models.sort()
        currIdx = models.index(self.avatar.currentClothing[type][0])
        currIdx -= 1
        itemId = models[currIdx]
        return (
         itemId, self.avatar.choices[type][itemId][0])

    def getNextClothingTexture(self, type):
        itemId = self.avatar.currentClothing[type][0]
        itemTextures = self.avatar.choices[type][itemId]
        currTexIdx = itemTextures.index(self.avatar.currentClothing[type][1])
        texIdx = currTexIdx + 1
        if texIdx >= len(itemTextures):
            textureId = itemTextures[0]
        else:
            textureId = itemTextures[texIdx]
        return (
         itemId, textureId)

    def getLastClothingTexture(self, type):
        itemId = self.avatar.currentClothing[type][0]
        itemTextures = self.avatar.choices[type][itemId]
        currTexIdx = itemTextures.index(self.avatar.currentClothing[type][1])
        texIdx = currTexIdx - 1
        textureId = itemTextures[texIdx]
        return (
         itemId, textureId)

    def getClothingSize(self, type):
        size = 0
        for i in self.avatar.choices[type]:
            for j in self.avatar.choices[type][i]:
                size = size + 1

        return size

    def hidePirate(self):
        self.avatar.body.hide()
        self.avatar.hair.hide()
        self.avatar.teeth.hide()
        self.avatar.eyes.hide()

    def showPirate(self):
        self.avatar.body.show()
        self.avatar.hair.show()
        self.avatar.teeth.show()
        self.avatar.eyes.show()

    def hideOtherClothes(self, type):
        clothes = [
         'SHIRT', 'VEST', 'PANT', 'COAT', 'BELT', 'SHOE', 'HAT']
        clothes.remove(type)
        for i in clothes:
            for k in self.avatar.clothesByType[i]:
                k.hide()

    def showOtherClothes(self, type):
        clothes = ['SHIRT', 'VEST', 'PANT', 'COAT', 'BELT', 'SHOE', 'HAT']
        clothes.remove(type)
        for i in clothes:
            for k in self.avatar.clothesByType[i]:
                k.show()

    def handleClothingChanged(self):
        self.avatar.currentClothing['HAT'] = self.main.pirate.style.getClothesHat() + [self.main.pirate.style.getHatColor()]
        self.avatar.currentClothing['SHIRT'] = self.main.pirate.style.getClothesShirt() + [self.main.pirate.style.getClothesTopColor()[0]]
        self.avatar.currentClothing['VEST'] = self.main.pirate.style.getClothesVest() + [self.main.pirate.style.getClothesTopColor()[1]]
        self.avatar.currentClothing['COAT'] = self.main.pirate.style.getClothesCoat() + [self.main.pirate.style.getClothesTopColor()[2]]
        self.avatar.currentClothing['PANT'] = self.main.pirate.style.getClothesPant() + [self.main.pirate.style.getClothesBotColor()[0]]
        self.avatar.currentClothing['BELT'] = self.main.pirate.style.getClothesBelt() + [self.main.pirate.style.getClothesBotColor()[1]]
        self.avatar.currentClothing['SHOE'] = self.main.pirate.style.getClothesShoe() + [self.main.pirate.style.getClothesBotColor()[2]]
        self.avatar.currentClothing['HAIR'] = [self.main.pirate.style.getHairHair(), self.main.pirate.style.getHairColor()]
        self.avatar.handleClothesHiding()
# okay decompiling .\pirates\makeapirate\ClothesGUI.pyc
