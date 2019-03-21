from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryPage
from pirates.pirate import TitleGlobals
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.ship import ShipGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiTray
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import GuiButton
from pirates.uberdog.UberDogGlobals import InventoryType

class TitlePanel(DirectFrame):
    
    def __init__(self, parent, titleId, position, panelIndex, titlesPage):
        DirectFrame.__init__(self, parent, pos = position)
        self.iconModel = loader.loadModelOnce(TitleGlobals.getModelPath(titleId))
        tempModel = loader.loadModelOnce('models/textureCards/skillIcons')
        self.iconVisible = tempModel.find('**/grenade_determination2')
        self.iconInvisible = tempModel.find('**/grenade_determination')
        self.titleId = titleId
        self.rank = 1
        self.maxRank = 1
        self.expPoints = 241
        self.expBase = 150
        self.expTarget = 400
        self.landActive = 0
        self.seaActive = 0
        self.panelIndex = panelIndex
        self.titlesPage = titlesPage
        self.titleNameFrame = DirectFrame(parent = self, relief = None, pos = (0.38, 0, 0.01), text = TitleGlobals.getTitleName(self.titleId, self.expPoints), text_align = TextNode.ALeft, text_scale = 0.032, text_pos = (0, -0.01), text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 15, text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceFont())
        self.titleDescFrame = DirectFrame(parent = self, relief = None, pos = (0.385, 0, -0.095), text = TitleGlobals.getTitleDesc(self.titleId), text_align = TextNode.ALeft, text_scale = 0.03, text_pos = (0, -0.01), text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 15, text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceFont())
        shipcard = loader.loadModelOnce('models/gui/ship_battle')
        tex = shipcard.find('**/ship_battle_speed_bar*')
        self.expFrame = DirectFrame(parent = self, pos = (0.62, 0, -0.04), relief = None, image = tex, image_scale = (0.23, 1, 0.5), scale = (1.48, 1, 1.2))
        self.expMeter = DirectWaitBar(parent = self.expFrame, relief = DGG.RAISED, borderWidth = (0.004, 0.004), range = 100, value = 50, frameColor = (0, 0, 0, 0), barColor = (0.1, 0.7, 0.1, 1), frameSize = (-0.222, 0.084, -0.012, 0.012), pos = (0.069, 0, 0.0))
        self.expMeterText = DirectFrame(parent = self, relief = None, pos = (0.86, 0, 0.01), text = '%s / %s' % (self.expBase, self.expTarget), text_align = TextNode.ARight, text_scale = 0.035, text_pos = (0, -0.01), text_fg = PiratesGuiGlobals.TextFG1, text_wordwrap = 15, text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceFont())
        self.iconFrame = DirectFrame(parent = self, pos = (0.27, 0, -0.03), relief = None, image = self.iconModel.find('**/' + TitleGlobals.getIconName(self.titleId, self.rank)), image_scale = (0.15, 1, 0.15))
        self.landButton = DirectButton(parent = self, pos = (0.01, 0, -0.03), relief = None, image = self.iconInvisible, image_scale = (0.07, 1, 0.07), command = self.landToggle)
        self.seaButton = DirectButton(parent = self, pos = (0.12, 0, -0.03), relief = None, image = self.iconInvisible, image_scale = (0.07, 1, 0.07), command = self.seaToggle)
    
    def refresh(self):
        inv = localAvatar.getInventory()
        if inv:
            self.expPoints = inv.getStackQuantity(TitleGlobals.getInventoryType(self.titleId))
            self.rank = TitleGlobals.getRank(self.titleId, self.expPoints)
            self.maxRank = TitleGlobals.getMaxRank(self.titleId)
            self.expTarget = TitleGlobals.getBreakpoints(self.titleId)[min(self.rank + 1, self.maxRank)]
            self.expBase = TitleGlobals.getBreakpoints(self.titleId)[self.rank]
        else:
            print 'No Inventory'
        print 'TitleID ', self.titleId, ' has ', self.expPoints, ' exp'
        if self.titleNameFrame:
            self.titleNameFrame['text'] = TitleGlobals.getTitleName(self.titleId, self.expPoints)
        
        if self.expMeter:
            value = 0
            if self.rank < self.maxRank and self.expTarget - self.expBase > 0:
                value = int((self.expPoints - self.expBase) * 100 / (self.expTarget - self.expBase))
            
            self.expMeter['value'] = value
        
        if self.expMeterText:
            if self.rank >= self.maxRank:
                self.expBase = 0
                self.expTarget = 0
            
            text = '0 / 0'
            if self.rank < self.maxRank and self.expTarget - self.expBase > 0:
                text = '%s / %s' % (self.expPoints - self.expBase, self.expTarget - self.expBase)
            
            self.expMeterText['text'] = text
        
        if self.iconFrame:
            self.iconFrame['image'] = self.iconModel.find('**/' + TitleGlobals.getIconName(self.titleId, self.rank))
        
        if self.landButton:
            self.landButton['image'] = [
                self.iconInvisible,
                self.iconVisible][self.landActive]
        
        if self.seaButton:
            self.seaButton['image'] = [
                self.iconInvisible,
                self.iconVisible][self.seaActive]
    
    def destroy(self):
        if self.titleNameFrame:
            self.titleNameFrame.destroy()
            self.titleNameFrame = None
        
        if self.expFrame:
            self.expFrame.destroy()
            self.expFrame = None
        
        if self.expMeterText:
            self.expMeterText.destroy()
            self.expMeterText = None
        
        if self.iconFrame:
            self.iconFrame.destroy()
            self.iconFrame = None
        
        if self.titleDescFrame:
            self.titleDescFrame.destroy()
            self.titleDescFrame = None
        
        DirectFrame.destroy(self)
    
    def landToggle(self, notifyParent = 1):
        print 'Toggling land'
        self.landActive = 1 - self.landActive
        print 'Land', self.panelIndex, ' is ', self.landActive
        self.landButton['image'] = [
            self.iconInvisible,
            self.iconVisible][self.landActive]
        if notifyParent:
            self.titlesPage.setLandActive(self.panelIndex, self.landActive)

    def seaToggle(self, notifyParent = 1):
        print 'Toggling sea'
        self.seaActive = 1 - self.seaActive
        print 'Sea ', self.seaActive
        self.seaButton['image'] = [
            self.iconInvisible,
            self.iconVisible][self.seaActive]
        if notifyParent:
            self.titlesPage.setSeaActive(self.panelIndex, self.seaActive)
        



class TitlesPage(InventoryPage.InventoryPage):
    
    def __init__(self):
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(TitlesPage)
        self.titles = []
        self.dividerLines = []
        self.selectedLandIndex = -1
        self.selectedSeaIndex = -1
        ornament = loader.loadModelCopy('models/gui/gui_treasure_window_b')
        ornament.setPos(0.53, 0, 0.72)
        ornament.setScale(0.315)
        ornament.reparentTo(self)
        ornament.flattenStrong()
        self.dummyFrame = DirectFrame(parent = self, relief = None, pos = (0.1, 0, 0.89))
        self.displayTitleFrame = DirectFrame(parent = self, relief = None, pos = (0.34, 0, 1.075), text = PLocalizer.DisplayTitle, text_align = TextNode.ALeft, text_scale = 0.06, text_pos = (0, -0.01), text_fg = PiratesGuiGlobals.TextFG14, text_wordwrap = 15, text_shadow = (0, 0, 0, 1), textMayChange = 0, text_font = PiratesGlobals.getInterfaceFont())
        self.displayTitleLandFrame = DirectFrame(parent = self, relief = None, pos = (0.07, 0, 1.0), text = PLocalizer.DisplayTitleLand, text_align = TextNode.ALeft, text_scale = 0.032, text_pos = (0, -0.01), text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 15, text_shadow = (0, 0, 0, 1), textMayChange = 0, text_font = PiratesGlobals.getInterfaceFont())
        self.displayTitleSeaFrame = DirectFrame(parent = self, relief = None, pos = (0.19, 0, 1.0), text = PLocalizer.DisplayTitleSea, text_align = TextNode.ALeft, text_scale = 0.032, text_pos = (0, -0.01), text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 15, text_shadow = (0, 0, 0, 1), textMayChange = 0, text_font = PiratesGlobals.getInterfaceFont())
        self.underlineFrame = DirectWaitBar(parent = self, relief = DGG.RAISED, borderWidth = (0.004, 0.004), range = 100, value = 100, frameColor = (0, 0, 0, 0), barColor = (0.8, 0.7, 0.5, 1), frameSize = (0.0, 0.95, 0.0, 0.015), pos = (0.06, 0, 0.95))
        self.loadGui()

    def destroy(self):
        if self.displayTitleFrame:
            self.displayTitleFrame.destroy()
            self.displayTitleFrame = None
        
        if self.displayTitleLandFrame:
            self.displayTitleLandFrame.destroy()
            self.displayTitleLandFrame = None
        
        if self.displayTitleSeaFrame:
            self.displayTitleSeaFrame.destroy()
            self.displayTitleSeaFrame = None
        
        if self.underlineFrame:
            self.underlineFrame.destroy()
            self.underlineFrame = None
        
        if self.titles:
            for panel in self.titles:
                panel.destroy()

        if self.dividerLines:
            for panel in self.dividerLines:
                panel.destroy()

        self.titles = None
        InventoryPage.InventoryPage.destroy(self)

    def show(self):
        for panel in self.titles:
            panel.refresh()
        
        InventoryPage.InventoryPage.show(self)

    def hide(self):
        InventoryPage.InventoryPage.hide(self)

    def loadGui(self):
        count = 0
        for key in TitleGlobals.TitlesDict.keys():
            yPos = 0.01 - count * 0.2
            panel = TitlePanel(self.dummyFrame, key, (0, 0, yPos), count, self)
            self.titles.append(panel)
            divider = self.createDivider(yPos - 0.15)
            self.dividerLines.append(divider)
            count += 1

    def createDivider(self, yPos):
        divider = DirectWaitBar(parent = self.dummyFrame, relief = DGG.RAISED, borderWidth = (0.004, 0.004), range = 100, value = 100, frameColor = (0, 0, 0, 0), barColor = (0.8, 0.7, 0.5, 1), frameSize = (0.0, 0.93, 0.0, 0.015), pos = (-0.03, 0, yPos))
        return divider

    def setLandActive(self, panelIndex, value):
        if panelIndex >= len(self.titles) or panelIndex < 0:
            return
        
        if panelIndex == self.selectedLandIndex and value == 0:
            self.selectedLandIndex = -1
        elif panelIndex != self.selectedLandIndex:
            if self.selectedLandIndex >= 0:
                self.titles[self.selectedLandIndex].landToggle(0)
            
            self.selectedLandIndex = panelIndex
        
        if self.selectedLandIndex < 0:
            localAvatar.sendRequestSetBadgeIcon(-1, -1)
        else:
            titlePanel = self.titles[self.selectedLandIndex]
            localAvatar.sendRequestSetBadgeIcon(titlePanel.titleId, titlePanel.rank)

    def setSeaActive(self, panelIndex, value):
        if panelIndex >= len(self.titles) or panelIndex < 0:
            return
        
        if panelIndex == self.selectedSeaIndex and value == 0:
            self.selectedSeaIndex = -1
        elif panelIndex != self.selectedSeaIndex:
            if self.selectedSeaIndex >= 0:
                self.titles[self.selectedSeaIndex].seaToggle(0)
            
            self.selectedSeaIndex = panelIndex

    def initLandTitleActive(self, titleId):
        if titleId < 0:
            return
        
        if self.selectedLandIndex >= 0:
            return
        
        for panel in self.titles:
            if panel.titleId == titleId:
                if not panel.landActive:
                    panel.landToggle()
        


