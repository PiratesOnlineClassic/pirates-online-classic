from direct.gui.DirectGui import *
from panda3d.core import *
from direct.interval.IntervalGlobal import *
from pirates.distributed import InteractGlobals
from pirates.quest import QuestDB, QuestLadderDB, QuestReward
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals

class QuestDetailBase(DirectFrame):

    def __init__(self, parent = aspect2d, pos = (0, 0, 0), *args, **kw):
        topGui = loader.loadModel('models/gui/toplevel_gui')
        questScroll = topGui.find('**/main_gui_quest_scroll')
        topGui.removeNode()
        optiondefs = (('relief', None, None), ('pos', pos, None), ('image', questScroll, None), ('image_scale', 0.47, None), ('text', '', None), ('text_align', TextNode.ALeft, None), ('text_fg', PiratesGuiGlobals.TextFG2, None), ('text_scale', PiratesGuiGlobals.TextScaleLarge, None), ('text_pos', (-0.42, 0.21), None), ('text_shadow', (0, 0, 0, 1), None), ('text_wordwrap', 22, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent = parent, *args, **kw)
        self.initialiseoptions(QuestDetailBase)



class QuestDetailGUI(QuestDetailBase):

    def __init__(self, offer, callback, quest = None):
        self.width = 1
        QuestDetailBase.__init__(self, parent = base.a2dBottomRight, pos = (0.6, 0, 0.52))
        self.callback = callback
        self.initialiseoptions(QuestDetailGUI)
        if offer:
            self.setQuestInfoFromOffer(offer)
        else:
            self.setQuestInfoFromQuest(quest)
        self.buildIvals()
        self.showPanel()

    def destroy(self):
        self.showIval.pause()
        self.showIval = None
        self.hideIval.pause()
        self.hideIval = None
        QuestDetailBase.destroy(self)

    def buildIvals(self):
        self.showIval = LerpPosInterval(self, 0.3, pos = Point3(-.47, 0, 0.52), blendType = 'easeOut')
        self.hideIval = LerpPosInterval(self, 0.3, pos = Point3(0.6, 0, 0.52), blendType = 'easeIn')

    def showPanel(self):
        self.showIval.start()

    def hidePanel(self):
        self.hideIval.start()

    def hidePanelAndDestroy(self):
        Sequence(self.hideIval, Wait(0.25), Func(self.destroy)).start()

    @exceptionLogged()
    def setQuestInfoFromOffer(self, offer):
        questId = offer.getQuestId()
        if offer.isLadder():
            containerDNA = QuestLadderDB.getContainer(questId)
            if containerDNA:
                status = containerDNA.getDescriptionText()

        else:
            status = QuestDB.QuestDict[questId].getDescriptionText(offer.initialTaskStates)
        questStrings = PLocalizer.QuestStrings.get(questId)
        if questStrings:
            title = questStrings.get('title', '\n')
            desc = questStrings.get('description', '\n')
        else:
            title = desc = '\n'
        reward = QuestReward.QuestReward.getDescriptionText(offer.getRewards())
        if len(reward) > 1:
            text = PLocalizer.QuestItemGuiIncompleteFormat % {
                'title': title,
                'status': status,
                'desc': desc,
                'reward': reward}
        else:
            text = PLocalizer.QuestItemGuiIncompleteFormatNoReward % {
                'title': title,
                'status': status,
                'desc': desc}
        self['text'] = text

    def setQuestInfoFromQuest(self, quest):
        questId = quest.getQuestId()
        taskStates = getattr(quest, 'taskStates', None)
        if not taskStates:
            taskStates = QuestDB.QuestDict[questId].getInitialTaskStates(localAvatar)

        status = QuestDB.QuestDict[questId].getDescriptionText(taskStates)
        questStrings = PLocalizer.QuestStrings.get(questId)
        if questStrings:
            title = questStrings.get('title', '\n')
            desc = questStrings.get('description', '\n')
        else:
            title = desc = '\n'
        hasRewards = hasattr(quest, 'rewards')
        reward = ''
        if hasRewards:
            reward = QuestReward.QuestReward.getDescriptionText(quest.getRewards())
        else:
            base.cr.centralLogger.writeClientEvent('Debug_QuestDetailGUI_GetRewardCrash: Error would have occured for localAvatar=%s; with questId=%s' % (localAvatar.getDoId(), questId))
            if hasattr(quest, 'doId'):
                base.cr.centralLogger.writeClientEvent('Debug_QuestDetailGUI_GetRewardCrash: Error would have occured for localAvatar=%s; with questDoId=%s' % (localAvatar.getDoId(), quest.getDoId()))

        text = PLocalizer.QuestItemGuiIncompleteFormat % {
            'title': title,
            'status': status,
            'desc': desc,
            'reward': reward}
        self['text'] = text
