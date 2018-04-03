# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestAvatarBase


class QuestAvatarBase:
    __module__ = __name__

    def getQuests(self):
        inventory = self.getInventory()
        if inventory is None:
            err = 'could not get inventory'
            if hasattr(self, 'doId'):
                err += ' for %s' % self.doId
            print err
            return []
        else:
            return inventory.getQuestList()
        return

    def getQuestById(self, questId):
        quests = self.getQuests()
        for currQuest in quests:
            if currQuest.questId == questId:
                return currQuest

        return
# okay decompiling .\pirates\quest\QuestAvatarBase.pyc
