
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedQuestAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedQuestAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.questId = None
        self.giverId = None
        self.combineOp = 0
        self.taskStates = []
        self.rewardStructs = []


    # setQuestId(QuestId) required broadcast db
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setQuestId(self, questId):
        self.questId = questId

    def d_setQuestId(self, questId):
        self.sendUpdate('setQuestId', [questId])

    def b_setQuestId(self, questId):
        self.setQuestId(questId)
        self.d_setQuestId(questId)

    def getQuestId(self):
        return self.questId

    # setGiverId(QuestGiverId) required broadcast db
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setGiverId(self, giverId):
        self.giverId = giverId

    def d_setGiverId(self, giverId):
        self.sendUpdate('setGiverId', [giverId])

    def b_setGiverId(self, giverId):
        self.setGiverId(giverId)
        self.d_setGiverId(giverId)

    def getGiverId(self):
        return self.giverId

    # announceNewQuest() broadcast ram

    def announceNewQuest(self, announceNewQuest):
        self.sendUpdate('announceNewQuest', [announceNewQuest])

    # setCombineOp(uint8) required broadcast db
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setCombineOp(self, combineOp):
        self.combineOp = combineOp

    def d_setCombineOp(self, combineOp):
        self.sendUpdate('setCombineOp', [combineOp])

    def b_setCombineOp(self, combineOp):
        self.setCombineOp(combineOp)
        self.d_setCombineOp(combineOp)

    def getCombineOp(self):
        return self.combineOp

    # setTaskStates(QuestTaskState []) required broadcast db
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setTaskStates(self, taskStates):
        self.taskStates = taskStates

    def d_setTaskStates(self, taskStates):
        self.sendUpdate('setTaskStates', [taskStates])

    def b_setTaskStates(self, taskStates):
        self.setTaskStates(taskStates)
        self.d_setTaskStates(taskStates)

    def getTaskStates(self):
        return self.taskStates

    # startFinalizeScene(uint8, uint32, string) broadcast ram

    def startFinalizeScene(self, startFinalizeScene, todo_uint32_1, todo_string_2):
        self.sendUpdate('startFinalizeScene', [startFinalizeScene, todo_uint32_1, todo_string_2])

    # doneFinalizeScene() airecv clsend

    def doneFinalizeScene(self, doneFinalizeScene):
        pass

    # amFinalized() broadcast ram

    def amFinalized(self, amFinalized):
        self.sendUpdate('amFinalized', [amFinalized])

    # setRewardStructs(QuestRewardStruct []) required broadcast db
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setRewardStructs(self, rewardStructs):
        self.rewardStructs = rewardStructs

    def d_setRewardStructs(self, rewardStructs):
        self.sendUpdate('setRewardStructs', [rewardStructs])

    def b_setRewardStructs(self, rewardStructs):
        self.setRewardStructs(rewardStructs)
        self.d_setRewardStructs(rewardStructs)

    def getRewardStructs(self):
        return self.rewardStructs

    # setActive() airecv clsend

    def setActive(self, active):
        pass

    # updateTargetLoc(Pos, uint32, uint32) broadcast

    def updateTargetLoc(self, updateTargetLoc, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('updateTargetLoc', [updateTargetLoc, todo_uint32_1, todo_uint32_2])


