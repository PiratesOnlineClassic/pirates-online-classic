from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryItemGui
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.battle import WeaponGlobals
from pirates.quest import QuestLadderDB
from pirates.quest import QuestDB, Quest
from pirates.quest import QuestDNA
from pirates.quest import QuestLadderDNA
from pirates.piratesbase import Freebooter

class QuestTitleNode:
    
    def __init__(self, questDNA):
        self.questDNA = questDNA
        if questDNA:
            self.questId = questDNA.getQuestId()
        else:
            self.questId = None
        self.children = {}

    def getChildren(self):
        return self.children.values()
    
    def hasChild(self, questId):
        return questId in self.children
    
    def addChild(self, node):
        return self.children.setdefault(node.questId, node)



class QuestTitleList(DirectScrolledFrame):
    HeadingFrameColor = ((0, 0, 0, 0), (0.45, 0.35, 0.15, 0.4), (0.55, 0.45, 0.25, 0.4))
    SelectedFrameColor = ((0.9, 0.7, 0.5, 0.4), (0.85, 0.65, 0.45, 0.4), (0.95, 0.75, 0.55, 0.4))
    DeselectedFrameColor = ((0, 0, 0, 0), (0.25, 0.23, 0.15, 0.6), (0.35, 0.33, 0.25, 0.6))
    charGui = None
    compassGui = None
    chapter4Lockout = False
    
    def __init__(self):
        self.width = 0.95
        self.height = 0.63
        if not base.config.GetBool('enable-next-chapter', 0):
            self.chapter4Lockout = True
        
        if not self.charGui:
            self.charGui = loader.loadModel('models/gui/char_gui')
            self.compassGui = loader.loadModel('models/gui/compass_main')
        
        DirectScrolledFrame.__init__(self, relief = None, state = DGG.NORMAL, manageScrollBars = 0, autoHideScrollBars = 1, frameSize = (0, self.width, 0, self.height), canvasSize = (0, self.width - 0.05, 0.025, self.height - 0.025), verticalScroll_relief = None, verticalScroll_image = self.charGui.find('**/chargui_slider_small'), verticalScroll_frameSize = (0, PiratesGuiGlobals.ScrollbarSize, 0, self.height), verticalScroll_image_scale = (self.height + 0.05, 1, 0.75), verticalScroll_image_hpr = (0, 0, 90), verticalScroll_image_pos = (self.width - PiratesGuiGlobals.ScrollbarSize * 0.5 - 0.004, 0, self.height * 0.5), verticalScroll_image_color = (0.61, 0.6, 0.6, 1), verticalScroll_thumb_image = (self.charGui.find('**/chargui_slider_node'), self.charGui.find('**/chargui_slider_node_down'), self.charGui.find('**/chargui_slider_node_over')), verticalScroll_thumb_relief = None, verticalScroll_thumb_image_scale = 0.4, verticalScroll_resizeThumb = 0, horizontalScroll_relief = None, sortOrder = 5)
        self.initialiseoptions(QuestTitleList)
        self.verticalScroll.incButton.destroy()
        self.verticalScroll.decButton.destroy()
        self.horizontalScroll.incButton.destroy()
        self.horizontalScroll.decButton.destroy()
        self.horizontalScroll.hide()
        self.trees = {}
        self.buttons = []
        self.accept('press-wheel_up-%s' % self.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.guiId, self.mouseWheelDown)

    def mouseWheelUp(self, task = None):
        if self.verticalScroll.isHidden():
            return None
        
        amountScroll = 0.05
        if self.verticalScroll['value'] > 0:
            self.verticalScroll['value'] -= amountScroll

    def mouseWheelDown(self, task = None):
        if self.verticalScroll.isHidden():
            return None
        
        amountScroll = 0.05
        if self.verticalScroll['value'] < 1.0:
            self.verticalScroll['value'] += amountScroll
    
    def destroy(self):
        del self.trees
        for button in self.buttons:
            button.destroy()
        
        del self.buttons
        DirectScrolledFrame.destroy(self)

    def repack(self):
        z = 0
        for button in self.buttons:
            if button.indent == 0:
                z -= 0.08
            else:
                z -= 0.042
            button.setPos(0, 0, z)
        
        self['canvasSize'] = (0, self.width - 0.05, z, 0)

    def update(self, questIdList, quest, newQuest):
        if quest and isinstance(quest, Quest.Quest):
            if newQuest:
                localAvatar.questStatus.assignQuest(quest)
                container = localAvatar.questStatus.getContainer(quest.questId)
                if not container:
                    container = localAvatar.getQuestById(quest.questId)
                
                container.viewedInGUI = False

        for button in self.buttons:
            button.destroy()
        
        self.buttons = []
        self.trees = {}
        for questId in questIdList:
            path = QuestLadderDB.getFamePath(questId)
            if path:
                pathName = path[0].getName()
                tree = self.trees.get(pathName)
                self.trees[pathName] = self.__makeTree(path, tree)

            path = QuestLadderDB.getFortunePath(questId)
            if path:
                pathName = path[0].getName()
                tree = self.trees.get(pathName)
                self.trees[pathName] = self.__makeTree(path, tree)

            path = [
                QuestDB.QuestDict.get(questId)]
            self.trees[questId] = self.__makeTree(path, tree = None)
        
        if len(questIdList) == 1:
            localAvatar.b_requestActiveQuest(questIdList[0])
        
        for tree in self.trees.values():
            self.__makeButtons(self.getCanvas(), tree)
        
        self.repack()

    def __makeTree(self, path, tree):
        if not tree:
            tree = QuestTitleNode(None)
        
        parent = tree
        for node in path:
            if self.chapter4Lockout and node.getQuestId() == 'c4.1visitValentina':
                continue
            parent = parent.addChild(QuestTitleNode(node))
        
        return tree

    def __graphWalker(self, node, indent = -1):
        yield (node, indent)
        for child in node.getChildren():
            for result in self.__graphWalker(child, indent + 1):
                yield result

    def __getContainer(self, questId):
        localAvatar.questStatus.forceInit()
        container = localAvatar.questStatus.getContainer(questId)
        if container:
            return container
        
        quest = localAvatar.getQuestById(questId)
        return quest

    def __getText(self, indent, questId, isContainer = False):
        text = '    ' * (indent - 1)
        localizerText = None
        if not isContainer:
            localizerText = PLocalizer.QuestStrings.get(questId)
            if localizerText:
                text += localizerText.get('title', questId)
            else:
                text += questId
        elif indent == 0:
            format = '\x01questTitle\x01%s\x02'
        else:
            format = '%s'
        localizerText = PLocalizer.QuestStrings.get(questId)
        if localizerText:
            text += format % localizerText.get('title', questId)
        else:
            text += format % questId
        localAvatar.questStatus.forceInit()
        container = localAvatar.questStatus.getContainer(questId)
        if not container:
            container = localAvatar.getQuestById(questId)
        
        if not container:
            return text
        
        if container.isComplete(showComplete = True):
            text += '   \x01questComplete\x01' + PLocalizer.QuestTitleComplete + '\x02'
        elif not container.viewedInGUI:
            text += '   \x01questNew\x01' + PLocalizer.QuestTitleNew + '\x02'
        elif not isContainer:
            progressList = container.getTaskProgress()
            for prog in progressList:
                progress = prog[0]
                goal = prog[1]
                if progress < goal:
                    if goal > 1:
                        text += '   \x01questPercent\x01%d of %d\x02' % (progress, goal)

                text += '   \x01questComplete\x01' + PLocalizer.QuestTitleComplete + '\x02'
            
        elif container.isChoice():
            (count, total, length) = container.getProgress(showComplete = True)
            if total == length:
                text += '   \x01questPercent\x01%d of %d\x02' % (count, total)
            else:
                text += '   \x01questPercent\x01%d of %d (of %d)\x02' % (count, total, length)
            format = ' \x01questPercent\x01%s\x02'
            if localizerText:
                text += format % localizerText.get('items', 'Items')
            else:
                text += format % 'Items'
        else:
            (compCont, cont) = container.percentComplete(localAvatar.getQuestLadderHistory())
            compNum = int((float(compCont) / float(cont)) * 100.0)
            if compNum > 0:
                text += '   \x01questPercent\x01(%d%%)\x02' % compNum
            
        return text
    
    def __makeButtons(self, guiParent, tree):
        i = 0
        for (node, indent) in self.__graphWalker(tree):
            if not node.questId:
                continue
            
            isContainer = isinstance(node.questDNA, QuestLadderDNA.QuestContainerDNA)
            text = self.__getText(indent, node.questId, isContainer)
            text_scale = PiratesGuiGlobals.TextScaleLarge
            frameSize = (0, 0.92, 0, 0.042)
            text_pos = (0.06, 0.01)
            if isContainer:
                textFg = PiratesGuiGlobals.TextFG1
                frameColor = self.HeadingFrameColor
                if indent == 0:
                    text_pos = (0.01, 0.01)
                
            else:
                textFg = PiratesGuiGlobals.TextFG2
                frameColor = self.DeselectedFrameColor
            button = DirectButton(parent = guiParent, relief = DGG.RAISED, frameSize = frameSize, borderWidth = (0.005, 0.005), frameColor = frameColor, text = text, text_fg = textFg, text_scale = text_scale, text_align = TextNode.ALeft, text_shadow = PiratesGuiGlobals.TextShadow, text_pos = text_pos, command = self.select, extraArgs = [
                node.questId])
            questDNA = QuestDB.QuestDict.get(node.questId)
            if questDNA:
                if questDNA.getVelvetRoped():
                    if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                        subCard = loader.loadModel('models/gui/toplevel_gui')
                        appendMe = DirectFrame(parent = button, relief = None, pos = (self.width - 0.985, 0, -0.03), state = DGG.DISABLED, geom = subCard.find('**/subscribers_lock'), geom_scale = 0.12, geom_pos = (0.06, 0, 0.06))
                        subCard.removeNode()

            button.accept('press-wheel_up-%s' % button.guiId, self.mouseWheelUp)
            button.accept('press-wheel_down-%s' % button.guiId, self.mouseWheelDown)
            button.indent = indent
            button.questId = node.questId
            self.buttons.append(button)
            i += 1

    def showTracked(self, questId):
        for button in self.buttons:
            if button.questId == questId:
                button['image'] = self.compassGui.find('**/icon_objective_grey')
                button['image_color'] = Vec4(1, 1, 0, 1)
                button['image_scale'] = 0.14
                button['image_pos'] = (0.02, 0, 0.025)
            else:
                button['image'] = None

    def select(self, questId):
        messenger.send('questGuiSelect', [
            questId])
        selectedButton = None
        for button in self.buttons:
            if button.questId == questId:
                button['frameColor'] = self.SelectedFrameColor
                selectedButton = button

            elif button.indent == 0:
                button['frameColor'] = self.HeadingFrameColor
            else:
                button['frameColor'] = self.DeselectedFrameColor
        
        if selectedButton is None:
            return None
        
        container = localAvatar.questStatus.getContainer(questId)
        if not container:
            container = localAvatar.getQuestById(questId)
        
        if container:
            if not container.viewedInGUI:
                container.viewedInGUI = True
                selectedButton['text'] = self.__getText(selectedButton.indent, questId)
            
        


