# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestBase
from pirates.quest import QuestReward


class QuestBase:
    __module__ = __name__

    def delete(self):
        messenger.send(self.getDeletedEventString(), [self.getDeletedEventString()])

    def getCompleteEventString(self):
        return 'quest-complete-%d' % self.doId

    def getDroppedEventString(self):
        return 'quest-dropped-%d' % self.doId

    def getDeletedEventString(self):
        return 'quest-deleted-%d' % self.doId
# okay decompiling .\pirates\quest\QuestBase.pyc
