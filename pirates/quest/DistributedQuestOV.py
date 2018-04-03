# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.DistributedQuestOV
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectOV import DistributedObjectOV
from pirates.quest import Quest, QuestBase
QUEST_TYPE_AVATAR = 0
QUEST_TYPE_TM = 1

class DistributedQuestOV(DistributedObjectOV, QuestBase.QuestBase, Quest.Quest):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedQuestOV')

    def __init__(self, cr):
        DistributedObjectOV.__init__(self, cr)
        Quest.Quest.__init__(self)
        self.notify.info('DistributedQuest.__init__')
        self.type = QUEST_TYPE_AVATAR

    def delete(self):
        DistributedObjectOV.delete(self)
        Quest.Quest.destroy(self)

    def setTaskStates(self, taskStates):
        Quest.Quest.setTaskStates(self, taskStates)
        if self.isGenerated():
            if self.isComplete():
                messenger.send('localAvatarQuestComplete', [self])
            else:
                messenger.send('localAvatarQuestUpdate', [self])

    def getCompleteText(self):
        if self.type == QUEST_TYPE_AVATAR:
            return 'QUEST COMPLETE!'
        else:
            return 'OBJECTIVE COMPLETE!'
# okay decompiling .\pirates\quest\DistributedQuestOV.pyc
