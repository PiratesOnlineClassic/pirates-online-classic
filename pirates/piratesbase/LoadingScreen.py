from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.reputation import ReputationGlobals
from direct.showbase import DirectObject
from direct.distributed.ClockDelta import *
from direct.task import Task
from direct.gui.DirectGui import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import Freebooter
import random
screenShots = [
    'models/gui/loadingScreen_01',
    'models/gui/loadingScreen_02',
    'models/gui/loadingScreen_03',
    'models/gui/loadingScreen_04',
    'models/gui/loadingScreen_05',
    'models/gui/loadingScreen_06',
    'models/gui/loadingScreen_07',
    'models/gui/loadingScreen_08',
    'models/gui/loadingScreen_09',
    'models/gui/loadingScreen_10',
    'models/gui/loadingScreen_11',
    'models/gui/loadingScreen_12',
    'models/gui/loadingScreen_13',
    'models/gui/loadingScreen_14',
    'models/gui/loadingScreen_15',
    'models/gui/loadingScreen_16',
    'models/gui/loadingScreen_17',
    'models/gui/loadingScreen_18',
    'models/gui/loadingScreen_19',
    'models/gui/loadingScreen_20',
    'models/gui/loadingScreen_21',
    'models/gui/loadingScreen_22',
    'models/gui/loadingScreen_23',
    'models/gui/loadingScreen_24',
    'models/gui/loadingScreen_25']
screenShots_Jungles = [
    'models/gui/loadingScreen_13']
screenShots_Swamps = [
    'models/gui/loadingScreen_18']
screenShots_Caves = [
    'models/gui/loadingScreen_03',
    'models/gui/loadingScreen_04',
    'models/gui/loadingScreen_23',
    'models/gui/loadingScreen_22']
areaType_Jungles = {
    '1161798288.34sdnaik': 0,
    '1164141722.61sdnaik': 1,
    '1169592956.59sdnaik': 2,
    '1165004570.58sdnaik': 3,
    '1165009873.53sdnaik': 4,
    '1165009856.72sdnaik': 5,
    '1167857698.16sdnaik': 6,
    '1172209955.25sdnaik': 7}
areaType_Swamps = {
    '1169179552.88sdnaik': 0,
    '1161732578.06sdnaik': 1}
areaType_Caves = {
    '1164952144.06sdnaik': 0,
    '1165001772.05sdnaik': 1,
    '1158121765.09sdnaik': 2,
    '1167862588.52sdnaik': 3,
    '1168057131.73sdnaik': 4,
    '1164929110.98sdnaik': 5,
    '1172208344.92sdnaik': 6}
screenShot_Dinghy = 'models/gui/loadingScreen_08'
screenShot_Jail = 'models/gui/loadingScreen_12'
screenShots_Locations = {
    '1164135492.81dzlu': [
        'models/gui/loadingScreen_01'],
    '1156359855.24bbathen': [
        'models/gui/loadingScreen_02',
        'models/gui/loadingScreen_10'],
    '1160614528.73sdnaik': [
        'models/gui/loadingScreen_05'],
    '1173382404.64sdnaik': [
        'models/gui/loadingScreen_06'],
    '1142018473.22dxschafe': [
        'models/gui/loadingScreen_07'],
    '1164763706.66sdnaik': [
        'models/gui/loadingScreen_09'],
    '1164157132.99dzlu': [
        'models/gui/loadingScreen_11'],
    '1159933206.48sdnaik': [
        'models/gui/loadingScreen_14'],
    '1173381952.2sdnaik': [
        'models/gui/loadingScreen_19'],
    '1150922126.8dzlu': [
        'models/gui/loadingScreen_16'],
    '1161282725.84kmuller': [
        'models/gui/loadingScreen_17'],
    '1164150392.42dzlu': [
        'models/gui/loadingScreen_15'],
    '1156207188.95dzlu': [
        'models/gui/loadingScreen_20'],
    '1172209006.11sdnaik': [
        'models/gui/loadingScreen_22'],
    '1196970035.53sdnaik': [
        'models/gui/loadingScreen_24'],
    '1196970080.56sdnaik': [
        'models/gui/loadingScreen_25']}

def getOceanHint():
    oceans = [
        'Windward_Passage',
        'Brigand_Bay',
        'Bloody_Bayou',
        'Scurvy_Shallows',
        'Blackheart_Strait',
        'Salty_Flats',
        'Mar_de_Plata',
        'Smugglers_Run',
        'The_Hinterseas',
        'Dead_Mans_Trough',
        'Leeward_Passage',
        'Boiling_Bay',
        'Mariners_Reef']
    ocean = random.choice(oceans)
    hints = PLocalizer.HintMap_Locations.get(ocean)
    if hints:
        hint = random.choice(hints)
    else:
        hint = random.choice(PLocalizer.Hints_General)
    return '%s:  %s' % (PLocalizer.LoadingScreen_Hint, hint)


def getGeneralHint():
    type = random.choice([
        0,
        1])
    if not Freebooter.getPaidStatus(base.localAvatar.getDoId()) and type == 1:
        hint = random.choice(PLocalizer.Hints_VelvetRope)
    else:
        hint = random.choice(PLocalizer.Hints_General)
    return hint


def getPrivateeringHint():
    hint = random.choice(PLocalizer.Hints_Privateering)
    return '%s:  %s' % (PLocalizer.LoadingScreen_Hint, hint)


def getHint(destId = None, level = None):
    if destId and level:
        type = random.choice([
            0,
            1,
            2])
        if type == 0:
            hints = PLocalizer.HintMap_Locations.get(destId)
            if hints is None:
                hint = getGeneralHint()
            elif len(hints):
                hint = random.choice(hints)
            else:
                hint = getGeneralHint()
        elif type == 1:
            hints = PLocalizer.HintMap_Levels.get(level)
            if hints is None:
                hint = getGeneralHint()
            elif len(hints):
                hint = random.choice(hints)
            else:
                hint = getGeneralHint()
        else:
            hint = getGeneralHint()
    elif destId and not level:
        type = random.choice([
            0,
            1])
        if type == 0:
            hints = PLocalizer.HintMap_Locations.get(destId)
            if hints is None:
                hint = getGeneralHint()
            elif len(hints):
                hint = random.choice(hints)
            else:
                hint = getGeneralHint()
        else:
            hint = getGeneralHint()
    elif level and not destId:
        type = random.choice([
            0,
            1])
        if type == 0:
            hints = PLocalizer.HintMap_Levels.get(level)
            if hints is None:
                hint = getGeneralHint()
            elif len(hints):
                hint = random.choice(hints)
            else:
                hint = getGeneralHint()
        else:
            hint = getGeneralHint()
    else:
        hint = getGeneralHint()
    return '%s:  %s' % (PLocalizer.LoadingScreen_Hint, hint)


class LoadingScreen(DirectObject.DirectObject):
    
    def __init__(self, parent):
        DirectObject.DirectObject.__init__(self)
        self.parent = parent
        self.state = False
        self.model = None
        self.wheel = None
        self.snapshot = None
        self.snapshotFrame = None
        self.currentTime = 0
        self.locationLabel = None
        self.locationText = None
        self.hintLabel = None
        self.hintText = None
        self.title_art = []

    def destroy(self):
        for part in (self.model, self.snapshot):
            if part is not None:
                tex = part.findTexture('*')
                if tex:
                    tex.releaseAll()
                
                part.removeNode()
        
        self.model = None
        self.snapshot = None
        if self.snapshotFrame:
            self.snapshotFrame.destroy()
        
        if self.locationLabel:
            self.locationLabel.destroy()
        
        if self.hintLabel:
            self.hintLabel.destroy()
        
        taskMgr.remove('updateLoadingScreen')
        self.ignoreAll()

    def showTitleFrame(self):
        if base.config.GetBool('no-loading-screen', 0):
            return
        
        for part in self.title_art:
            part.show()

    def hideTitleFrame(self):
        for part in self.title_art:
            part.hide()
    
    def show(self, waitForLocation = False):
        if self.state or base.config.GetBool('no-loading-screen', 0):
            return
        
        self.state = True
        self.model = loader.loadModelOnce('models/gui/loading_screen')
        self.locationLabel = DirectLabel(parent = aspect2dp, relief = None, text = '', text_font = PiratesGlobals.getPirateOutlineFont(), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_scale = PiratesGuiGlobals.TextScaleTitleJumbo * 0.7, text_align = TextNode.ACenter, text_pos = (0.0, -0.52), textMayChange = 1)
        self.hintLabel = DirectLabel(parent = aspect2dp, relief = None, text = '', text_font = PiratesGlobals.getPirateOutlineFont(), text_fg = PiratesGuiGlobals.TextFG1, text_shadow = PiratesGuiGlobals.TextShadow, text_scale = PiratesGuiGlobals.TextScaleTitleJumbo * 0.5, text_align = TextNode.ACenter, text_pos = (0.0, -0.8), text_wordwrap = 30, textMayChange = 1)
        self.wheel = self.model.find('**/red_wheel')
        self.title_art.append(self.model.find('**/title_bg'))
        self.title_art.append(self.model.find('**/title_frame'))
        self.hideTitleFrame()
        if not waitForLocation:
            if self.snapshot is None:
                screenshot = random.choice(screenShots)
                self.__setLoadingArt(screenshot)
            
            if self.snapshot:
                self.snapshot.show()
            
        elif self.snapshot:
            self.snapshot.show()
        
        self.snapshotFrame = DirectFrame(parent = aspect2dp, relief = DGG.FLAT, frameColor = (0.0, 0.0, 0.0, 1.0), frameSize = (-2.0, 2.0, 2.0, -2.0))
        self.snapshotFrame.setBin('fixed', 0)
        self.model.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
        self.locationLabel.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
        self.hintLabel.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
        self.model.setScale(0.25, 0.25, 0.25)
        self.model.setPos(0.0, 0.0, -0.15)
        if self.locationText is not None:
            if len(self.locationText):
                self.__setLocationText(self.locationText)
        
        if self.hintText is not None:
            if len(self.hintText):
                self.__setHintText(self.hintText)

        base.graphicsEngine.renderFrame()
        base.refreshAds()
        taskMgr.add(self.update, 'updateLoadingScreen', priority = -100)

    def showHint(self, destId = None, ocean = False):
        if base.config.GetBool('no-loading-screen', 0):
            return
        
        if ocean:
            hint = getOceanHint()
        elif hasattr(base, 'localAvatar'):
            totalReputation = 0
            inv = base.localAvatar.getInventory()
            if inv:
                for repCat in ReputationGlobals.getReputationCategories():
                    totalReputation += inv.getReputation(repCat)

            (level, leftoverValue) = ReputationGlobals.getLevelFromTotalReputation(InventoryType.OverallRep, totalReputation)
            if totalReputation:
                hint = getHint(destId, level)
            else:
                hint = getHint(destId)
        else:
            hint = getHint()
        shipPVPIslands = [
            '1196970035.53sdnaik',
            '1196970080.56sdnaik']
        if destId in shipPVPIslands or ocean and base.localAvatar.getCurrentIsland() in shipPVPIslands:
            hint = getPrivateeringHint()
        
        self.__setHintText(hint)
    
    def update(self, task = None):
        self.currentTime += 10
        self.wheel.setR(-(self.currentTime))
        base.graphicsEngine.renderFrame()
        return Task.cont

    def hide(self):
        if not self.state:
            return
        
        self.state = False
        self.currentTime = 0
        self.locationText = None
        self.hintText = None
        for part in (self.model, self.snapshot):
            if part:
                tex = part.findTexture('*')
                if tex:
                    tex.releaseAll()
                
                part.removeNode()
        
        self.model = None
        self.snapshot = None
        if self.snapshotFrame:
            self.snapshotFrame.destroy()
        
        if self.locationLabel:
            self.locationLabel.destroy()
        
        if self.hintLabel:
            self.hintLabel.destroy()
        
        taskMgr.remove('updateLoadingScreen')

    def showTarget(self, targetId = None, ocean = False, jail = False):
        if base.config.GetBool('no-loading-screen', 0):
            return
        
        if ocean:
            screenshot = screenShot_Dinghy
        elif jail:
            screenshot = screenShot_Jail
        else:
            screenshot = screenShots_Locations.get(targetId)
            if not screenshot:
                if areaType_Jungles.has_key(targetId):
                    screenshot = random.choice(screenShots_Jungles)
                elif areaType_Swamps.has_key(targetId):
                    screenshot = random.choice(screenShots_Swamps)
                elif areaType_Caves.has_key(targetId):
                    screenshot = random.choice(screenShots_Caves)
                else:
                    screenshot = random.choice(screenShots)
            elif len(screenshot) > 1:
                screenshot = random.choice(screenshot)
            else:
                screenshot = screenshot[0]
        self.__setLoadingArt(screenshot)
        if ocean:
            targetName = PLocalizer.LoadingScreen_Ocean
        elif jail:
            targetName = PLocalizer.LoadingScreen_Jail
        else:
            targetName = PLocalizer.LocationNames.get(targetId)
        base.setLocationCode('Loading: %s' % targetName)
        if targetName is None:
            return
        
        if len(targetName):
            self.__setLocationText(targetName)
    
    def __setLoadingArt(self, screenshot):
        if self.snapshot:
            return
        
        self.snapshot = loader.loadModel(screenshot)
        if self.snapshot:
            self.snapshot.reparentTo(aspect2dp, NO_FADE_SORT_INDEX)
            self.snapshot.setScale(2.15, 1, 1.2)
            self.snapshot.setPos(0.0, 0.0, 0.09)
            self.snapshot.setBin('fixed', 1)
            if not self.__isVisible():
                self.snapshot.hide()
    
    def __setLocationText(self, locationText):
        self.locationText = locationText
        if self.__isVisible():
            self.locationLabel['text'] = locationText
            self.locationLabel.show()
            self.showTitleFrame()

    def __setHintText(self, hintText):
        self.hintText = hintText
        if self.__isVisible():
            self.hintLabel['text'] = hintText
            self.hintLabel.show()

    def __isVisible(self):
        return self.state

    def scheduleHide(self, function):
        base.cr.queueAllInterestsCompleteEvent()
        self.acceptOnce(function, self.hide)


