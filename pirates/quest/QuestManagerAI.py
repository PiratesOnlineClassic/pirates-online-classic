from direct.directnotify import DirectNotifyGlobal

from pirates.quest.DistributedQuestAI import DistributedQuestAI


class QuestManagerAI(object):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestManagerAI')

    def __init__(self, air):
        self.air = air
        self.__quests = {}

    def hasQuest(self, av, questId):
        if av.doId not in self.__quests:
            return False

        return questId in self.__quests[av.doId]

    def addQuest(self, av, questId):
        currQuests = self.__quests.setdefault(av.doId, {})
        if questId in currQuests:
            self.notify.warning('Cannot add a new quest %s for avatar %d, '
                'quest already added!' % (questId, av.doId))

            return

        gameAreaObj = av.getParentObj()
        if not gameAreaObj:
            self.notify.warning('Cannot generate a new quest %s for avatar %d '
                'avatar has no parentObj!' % (questId, av.doId))

            return

        instanceObj = gameAreaObj.getParentObj()
        if not instanceObj:
            self.notify.warning('Cannot generate a new quest %s for avatar %d '
                'gameAreaObj %d has no instanceObj!' % (questId, av.doId, gameAreaObj.doId))

            return

        quest = DistributedQuestAI(self.air)
        quest.setQuestId(questId)
        quest.generateWithRequiredAndId(self.air.allocateChannel(),
            instanceObj.doId, gameAreaObj.zoneId)

        # set the owner of the quest object, this will then send an
        # OwnerView object generate to the client...
        channel = av.getDISLid() << 32 | av.doId
        self.air.setOwner(quest.doId, channel)

        # store the new quest object to the dictionary of quest objects
        # so we can keep track of it for later use...
        currQuests[questId] = quest
        return quest

    def dropQuest(self, av, quest):
        if not self.hasQuest(av, quest.questId):
            self.notify.warning('Cannot drop quest %s for avatar %d, '
                'quest never added!' % (quest.questId, av.doId))

            return

        del self.__quests[av.doId][quest.questId]
        quest.requestDelete()

    def getQuest(self, av, questId):
        if av.doId not in self.__quests:
            return None

        return self.__quests[av.doId].get(questId)
