from pirates.quest.QuestPath import QuestStep
from pirates.quest.QuestIndicatorNodeNPC import QuestIndicatorNodeNPC
from pirates.quest.QuestIndicatorNodeItem import QuestIndicatorNodeItem
from pirates.quest.QuestIndicatorNodeArea import QuestIndicatorNodeArea
from pirates.quest.QuestIndicatorNodeTunnel import QuestIndicatorNodeTunnel
from pirates.quest.QuestIndicatorNodeExtDoor import QuestIndicatorNodeExtDoor
from pirates.quest.QuestIndicatorNodeIntDoor import QuestIndicatorNodeIntDoor
from pirates.quest.QuestIndicatorNodeQuestNode import QuestIndicatorNodeQuestNode
from pirates.quest.QuestIndicatorNodeShip import QuestIndicatorNodeShip

class QuestStepIndicator:
    TypeMap = {
        QuestStep.STNPC: QuestIndicatorNodeNPC,
        QuestStep.STItem: QuestIndicatorNodeItem,
        QuestStep.STArea: QuestIndicatorNodeArea,
        QuestStep.STTunnel: QuestIndicatorNodeTunnel,
        QuestStep.STExteriorDoor: QuestIndicatorNodeExtDoor,
        QuestStep.STInteriorDoor: QuestIndicatorNodeIntDoor,
        QuestStep.STQuestNode: QuestIndicatorNodeQuestNode,
        QuestStep.STShip: QuestIndicatorNodeShip}
    
    def __init__(self):
        self.questStep = None
        self.indicatorNode = None
        self.muted = False
    
    def delete(self):
        self.hideQuestStep()
        self.indicatorNone = None
        self.questStep = None

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def showQuestStep(self, questStep):
        if self.questStep != questStep:
            self.hideQuestStep()
            self.questStep = questStep
            if self.questStep:
                questType = questStep.getStepType()
                IndicatorClass = QuestStepIndicator.TypeMap.get(questType)
                if IndicatorClass:
                    self.indicatorNode = IndicatorClass(questStep)
                    if self.muted:
                        self.hideEffect()

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def hideQuestStep(self):
        if self.indicatorNode:
            self.indicatorNode.delete()
            self.indicatorNode = None
        
        self.questStep = None
    
    def showEffect(self):
        self.muted = False
        if self.indicatorNode:
            self.indicatorNode.showEffect()

    def hideEffect(self):
        self.muted = True
        if self.indicatorNode:
            self.indicatorNode.hideEffect()
        


