from pirates.quest import QuestReward


class QuestBase:

    def getCompleteEventString(self):
        return 'quest-complete-%d' % self.doId

    def getDroppedEventString(self):
        return 'quest-dropped-%d' % self.doId

    def getDeletedEventString(self):
        return 'quest-deleted-%d' % self.doId

    def delete(self):
        messenger.send(self.getDeletedEventString(), [self.getDeletedEventString()])
