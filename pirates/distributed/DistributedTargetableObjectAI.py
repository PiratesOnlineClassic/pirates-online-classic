from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.battle.ComboDiaryAI import ComboDiaryAI

class DistributedTargetableObjectAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTargetableObjectAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def generate(self):
        DistributedObjectAI.generate(self)

        self.comboDiary = ComboDiaryAI(self.air, self)
