# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestStepIndicator
from pirates.quest.QuestIndicatorNodeArea import QuestIndicatorNodeArea
from pirates.quest.QuestIndicatorNodeExtDoor import QuestIndicatorNodeExtDoor
from pirates.quest.QuestIndicatorNodeIntDoor import QuestIndicatorNodeIntDoor
from pirates.quest.QuestIndicatorNodeItem import QuestIndicatorNodeItem
from pirates.quest.QuestIndicatorNodeNPC import QuestIndicatorNodeNPC
from pirates.quest.QuestIndicatorNodeQuestNode import \
    QuestIndicatorNodeQuestNode
from pirates.quest.QuestIndicatorNodeShip import QuestIndicatorNodeShip
from pirates.quest.QuestIndicatorNodeTunnel import QuestIndicatorNodeTunnel
from pirates.quest.QuestPath import QuestStep


class QuestStepIndicator:

    TypeMap = {
        QuestStep.STNPC: QuestIndicatorNodeNPC,
        QuestStep.STItem: QuestIndicatorNodeItem,
        QuestStep.STArea: QuestIndicatorNodeArea,
        QuestStep.STTunnel: QuestIndicatorNodeTunnel,
        QuestStep.STExteriorDoor: QuestIndicatorNodeExtDoor,
        QuestStep.STInteriorDoor: QuestIndicatorNodeIntDoor,
        QuestStep.STQuestNode: QuestIndicatorNodeQuestNode,
        QuestStep.STShip: QuestIndicatorNodeShip
    }

    def __init__(self):
        self.questStep = None
        self.indicatorNode = None
        self.muted = False
        return

    def delete(self):
        self.hideQuestStep()
        self.indicatorNone = None
        self.questStep = None
        return

    @report(
        types=['frameCount', 'args'],
        dConfigParam='want-quest-indicator-report')
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

    @report(
        types=['frameCount', 'args'],
        dConfigParam='want-quest-indicator-report')
    def hideQuestStep(self):
        if self.indicatorNode:
            self.indicatorNode.delete()
            self.indicatorNode = None
        self.questStep = None
        return

    def showEffect(self):
        self.muted = False
        if self.indicatorNode:
            self.indicatorNode.showEffect()

    def hideEffect(self):
        self.muted = True
        if self.indicatorNode:
            self.indicatorNode.hideEffect()


# okay decompiling .\pirates\quest\QuestStepIndicator.pyc
