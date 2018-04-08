from direct.directnotify import DirectNotifyGlobal
from otp.avatar.DistributedAvatarAI import DistributedAvatarAI
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.movement.DistributedMovingObjectAI import DistributedMovingObjectAI
from pirates.quest.DistributedQuestGiverAI import DistributedQuestGiverAI

class DistributedReputationAvatarAI(DistributedAvatarAI, DistributedInteractiveAI, DistributedMovingObjectAI, DistributedQuestGiverAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedReputationAvatarAI')

    def __init__(self, air):
        DistributedAvatarAI.__init__(self, air)
        DistributedInteractiveAI.__init__(self, air)
        DistributedMovingObjectAI.__init__(self, air)
        DistributedQuestGiverAI.__init__(self, air)
