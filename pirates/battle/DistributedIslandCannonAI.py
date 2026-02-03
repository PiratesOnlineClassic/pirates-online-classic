from direct.directnotify import DirectNotifyGlobal
from pirates.battle.DistributedPCCannonAI import DistributedPCCannonAI

class DistributedIslandCannonAI(DistributedPCCannonAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedIslandCannonAI')