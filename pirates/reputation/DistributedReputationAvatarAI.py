from direct.directnotify import DirectNotifyGlobal

from otp.avatar.DistributedAvatarAI import DistributedAvatarAI

from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.movement.DistributedMovingObjectAI import DistributedMovingObjectAI
from pirates.quest.DistributedQuestGiverAI import DistributedQuestGiverAI


class DistributedReputationAvatarAI(DistributedAvatarAI, DistributedMovingObjectAI, DistributedInteractiveAI, DistributedQuestGiverAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedReputationAvatarAI')

    def __init__(self, air):
        DistributedAvatarAI.__init__(self, air)
        DistributedMovingObjectAI.__init__(self, air)
        DistributedInteractiveAI.__init__(self, air)
        DistributedQuestGiverAI.__init__(self, air)

    def announceGenerate(self):
        DistributedAvatarAI.announceGenerate(self)
        DistributedMovingObjectAI.announceGenerate(self)
        DistributedInteractiveAI.announceGenerate(self)
        DistributedQuestGiverAI.announceGenerate(self)

    def generate(self):
        DistributedAvatarAI.generate(self)
        DistributedMovingObjectAI.generate(self)
        DistributedInteractiveAI.generate(self)
        DistributedQuestGiverAI.generate(self)

    def disable(self):
        DistributedAvatarAI.disable(self)
        DistributedMovingObjectAI.disable(self)
        DistributedInteractiveAI.disable(self)
        DistributedQuestGiverAI.disable(self)

    def delete(self):
        DistributedAvatarAI.delete(self)
        DistributedMovingObjectAI.delete(self)
        DistributedInteractiveAI.delete(self)
        DistributedQuestGiverAI.delete(self)

    def setLocation(self, parentId, zoneId, teleport=0):
        DistributedAvatarAI.setLocation(self, parentId, zoneId, teleport)
        DistributedMovingObjectAI.setLocation(self, parentId, zoneId, teleport)
        DistributedInteractiveAI.setLocation(self, parentId, zoneId, teleport)
