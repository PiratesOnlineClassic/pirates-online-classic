class QuestAvatarBase:
    
    def getQuests(self):
        inventory = self.getInventory()
        if inventory is None:
            err = 'could not get inventory'
            if hasattr(self, 'doId'):
                err += ' for %s' % self.doId
            
            print(err)
            return []
        else:
            return inventory.getQuestList()

    def getQuestById(self, questId):
        quests = self.getQuests()
        for currQuest in quests:
            if currQuest.questId == questId:
                return currQuest
        return None
        


