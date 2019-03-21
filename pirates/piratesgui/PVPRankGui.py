import copy
from direct.gui.DirectGui import *
from direct.task.Task import Task
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.ship import ShipGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiTray
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import GuiButton
from pirates.piratesgui import PiratesGuiGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.pvp import PVPGlobals
from pirates.pirate import TitleGlobals
SHIP_RENOWN_DISPLAY = 0
LAND_RENOWN_DISPLAY = 1

class PVPRankGui(DirectFrame):
    
    def __init__(self, parent, displayType, **kw):
        DirectFrame.__init__(self, parent, **kw)
        self.renown = 0
        self.spendableRenown = 0
        self.renownTarget = 0
        self.renownBase = 0
        self.rank = 0
        self.rankIcon = None
        self.xShift = 0
        self.yShift = 0
        self.titleId = 0
        self.rankBox = None
        self.renownBox = None
        self.renownFrame = None
        self.renownMeter = None
        self.renownMeterText = None
        self.iconFrame = None
        self.dummyFrame = None
        self.rankIcons = None
        self.iconsModel = None
        self.titleFrame = None
        self.renownSpendable = None
        self.displayType = displayType
        self.iconImageScale = (0.12, 1, 0.12)
        if self.displayType == SHIP_RENOWN_DISPLAY:
            self.titleMap = PLocalizer.PVPTitleSeaRanks
            self.renownName = PLocalizer.PVPInfamySea
            self.breakPoints = TitleGlobals.getBreakpoints(TitleGlobals.ShipPVPTitle)
            self.maxRank = TitleGlobals.getMaxRank(TitleGlobals.ShipPVPTitle)
            self.rankIcons = TitleGlobals.getIconList(TitleGlobals.ShipPVPTitle)
            self.iconsModel = loader.loadModel(TitleGlobals.getModelPath(TitleGlobals.ShipPVPTitle))
            self.titleId = TitleGlobals.ShipPVPTitle
        elif self.displayType == LAND_RENOWN_DISPLAY:
            self.titleMap = PLocalizer.PVPTitleLandRanks
            self.renownName = PLocalizer.PVPInfamyLand
            self.breakPoints = TitleGlobals.getBreakpoints(TitleGlobals.LandPVPTitle)
            self.maxRank = TitleGlobals.getMaxRank(TitleGlobals.LandPVPTitle)
            self.rankIcons = TitleGlobals.getIconList(TitleGlobals.LandPVPTitle)
            self.iconsModel = loader.loadModel(TitleGlobals.getModelPath(TitleGlobals.LandPVPTitle))
            self.titleId = TitleGlobals.LandPVPTitle
        else:
            self.titleMap = {
                0: 'Unknown'}
            self.renownName = '?'
            self.breakPoints = [
                0]
            self.maxRank = 0
            self.rankIcons = {
                0: 'sail_come_about'}
        if not self.iconsModel:
            self.iconsModel = loader.loadModel('models/textureCards/skillIcons')
        
        self.loadRank()
        self.loadRankIcon()
        self.loadGUI()
        self.setRenown(self.renown)

    def destroy(self):
        self.ignoreAll()
        if self.rankBox:
            self.rankBox.destroy()
            self.rankBox = None
        
        if self.renownBox:
            self.renownBox.destroy()
            self.renownBox = None
        
        if self.renownSpendable:
            self.renownSpendable.destroy()
            self.renownSpendable = None
        
        if self.renownFrame:
            self.renownFrame.destroy()
            self.renownFrame = None
        
        if self.renownMeter:
            self.renownMeter.destroy()
            self.renownMeter = None
        
        if self.renownMeterText:
            self.renownMeterText.destroy()
            self.renownMeterText = None
        
        if self.titleFrame:
            self.titleFrame.destroy()
            self.titleFrame = None
        
        if self.dummyFrame:
            self.dummyFrame.destroy()
            self.dummyFrame = None
        
        DirectFrame.destroy(self)

    def loadRank(self):
        inv = localAvatar.getInventory()
        if not inv:
            return
        
        if self.displayType == SHIP_RENOWN_DISPLAY:
            renown = inv.getStackQuantity(InventoryType.PVPTotalInfamySea)
        elif self.displayType == LAND_RENOWN_DISPLAY:
            renown = inv.getStackQuantity(InventoryType.PVPTotalInfamyLand)
        else:
            renown = 0
        self.spendableRenown = inv.getStackQuantity(InventoryType.PVPCurrentInfamy)
        self.setRenown(renown)
    
    def updateRank(self, extraRenown):
        inv = localAvatar.getInventory()
        if not inv:
            return
        
        limit = self.renown
        if self.displayType == SHIP_RENOWN_DISPLAY:
            limit = inv.getStackLimit(InventoryType.PVPTotalInfamySea)
        elif self.displayType == LAND_RENOWN_DISPLAY:
            limit = inv.getStackLimit(InventoryType.PVPTotalInfamyLand)
        
        self.spendableRenown = max(min(self.spendableRenown + extraRenown, inv.getStackLimit(InventoryType.PVPCurrentInfamy)), 0)
        renown = max(min(self.renown + extraRenown, limit), 0)
        self.setRenown(renown)

    def loadGUI(self):
        sort = 1
        self.dummyFrame = DirectFrame(parent = self, relief = None, pos = (-0.51, 0, 0.48), sortOrder = sort)
        self.rankBox = DirectFrame(parent = self.dummyFrame, relief = None, pos = (0.17, 0, -0.1), text = self.titleMap[self.rank], text_align = TextNode.ALeft, text_scale = 0.045, text_pos = (-0.02, -0.01), text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 15, text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceFont(), sortOrder = sort)
        self.renownBox = DirectFrame(parent = self.dummyFrame, relief = None, pos = (0.0, 0, -0.27), text = PLocalizer.PVPInfamySpendable + ':', text_align = TextNode.ALeft, text_scale = 0.04, text_pos = (0.02, -0.01), text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 15, text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceFont(), sortOrder = sort)
        skullModel = loader.loadModel('models/gui/avatar_chooser_rope')
        renownImage = skullModel.find('**/avatar_c_B_delete')
        self.renownSpendable = DirectFrame(parent = self.dummyFrame, relief = None, pos = (0.38, 0, -0.27), text = str(self.spendableRenown), text_align = TextNode.ARight, text_scale = 0.035, text_pos = (0, -0.01), text_fg = PiratesGuiGlobals.TextFG2, text_wordwrap = 15, text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceFont(), image = renownImage, image_scale = (0.15, 1, 0.15), image_pos = (0.04, 0, 0.01), sortOrder = sort)
        if self.displayType == SHIP_RENOWN_DISPLAY:
            titleStr = PLocalizer.PVPPrivateeringTitle
        elif self.displayType == LAND_RENOWN_DISPLAY:
            titleStr = PLocalizer.PVPLandTitle
        else:
            titleStr = ''
        self.titleFrame = DirectFrame(parent = self.dummyFrame, relief = None, pos = (0.0, 0, -0.02), text = titleStr + ':', text_align = TextNode.ALeft, text_scale = 0.05, text_pos = (0, -0.01), text_fg = PiratesGuiGlobals.TextFG13, text_wordwrap = 15, text_shadow = (0, 0, 0, 1), textMayChange = 0, text_font = PiratesGlobals.getInterfaceFont(), sortOrder = sort)
        shipcard = loader.loadModel('models/gui/ship_battle')
        tex = shipcard.find('**/ship_battle_speed_bar*')
        self.renownFrame = DirectFrame(parent = self.dummyFrame, pos = (0.3, 0, -0.15), relief = None, image = tex, image_scale = (0.23, 1, 0.5), scale = (0.88, 1, 1.2), sortOrder = sort)
        self.renownMeter = DirectWaitBar(parent = self.renownFrame, relief = DGG.RAISED, borderWidth = (0.004, 0.004), range = 100, value = 100, frameColor = (0, 0, 0, 0), barColor = (0.1, 0.7, 0.1, 1), frameSize = (-0.222, 0.084, -0.012, 0.012), pos = (0.069, 0, 0.0))
        self.renownMeterText = DirectFrame(parent = self.dummyFrame, relief = None, pos = (0.44, 0, -0.19), text = '%s / %s' % (self.renownBase, self.renownTarget), text_align = TextNode.ARight, text_scale = 0.028, text_pos = (0, -0.01), text_fg = PiratesGuiGlobals.TextFG1, text_wordwrap = 15, text_shadow = (0, 0, 0, 1), textMayChange = 1, text_font = PiratesGlobals.getInterfaceFont(), sortOrder = sort)
        self.iconFrame = DirectFrame(parent = self.dummyFrame, pos = (0.06, 0, -0.13), relief = None, image = self.rankIcon, image_scale = self.iconImageScale, sortOrder = sort)
    
    def loadRankIcon(self):
        if self.rank <= 0:
            if self.iconFrame:
                self.iconFrame['image'] = None
            
            return None
        
        self.rankIcon = self.iconsModel.find('**/' + self.rankIcons[self.rank])
        if self.iconFrame:
            self.iconFrame['image'] = self.rankIcon
            self.iconFrame['image_scale'] = self.iconImageScale
    
    def setRenown(self, renown):
        self.renown = renown
        if self.displayType == SHIP_RENOWN_DISPLAY:
            self.rank = TitleGlobals.getRank(self.titleId, self.renown)
        elif self.displayType == LAND_RENOWN_DISPLAY:
            self.rank = TitleGlobals.getRank(self.titleId, self.renown)
        else:
            self.rank = 0
        self.renownTarget = self.breakPoints[min(self.rank + 1, self.maxRank)]
        self.renownBase = self.breakPoints[self.rank]
        if self.rankBox:
            self.rankBox['text'] = self.titleMap[self.rank]
            self.rankBox['text_scale'] = 0.045
        
        if self.renownSpendable:
            self.renownSpendable['text'] = str(self.spendableRenown)
        
        if self.renownMeter:
            value = 0
            if self.rank < self.maxRank and self.renownTarget - self.renownBase > 0:
                value = int((self.renown - self.renownBase) * 100 / (self.renownTarget - self.renownBase))
            
            self.renownMeter['value'] = value
        
        if self.renownMeterText:
            if self.rank >= self.maxRank:
                self.renownBase = 0
                self.renownTarget = 0
            
            text = '0 / 0'
            if self.rank < self.maxRank and self.renownTarget - self.renownBase > 0:
                text = '%s / %s' % (self.renown - self.renownBase, self.renownTarget - self.renownBase)
            
            self.renownMeterText['text'] = text
        
        self.loadRankIcon()


