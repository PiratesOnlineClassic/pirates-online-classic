from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.creature.DistributedCreatureAI import *
from pirates.creature.AnimalGameFSMAI import AnimalGameFSMAI

class DistributedAnimalAI(DistributedCreatureAI):
    notify = directNotify.newCategory('DistributedAnimalAI')
    avatarType = AvatarTypes.Animal

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)

    def createGameFSM(self):
        return AnimalGameFSMAI(self.air, self)

    def generate(self):
        DistributedCreatureAI.generate(self)

        # animals are ambient and cannot be battled, so they should never
        # be tracked as a target by the target manager...
        self.air.targetMgr.removeTarget(self)

    def isPassive(self):
        return True

    def isBattleable(self):
        return False

    def getDamagable(self):
        return False

    def setStartState(self, startState):
        if startState not in ['Idle', 'Patrol', 'Walk']:
            startState = 'Idle'

        DistributedCreatureAI.setStartState(self, startState)

    def requestClientAggro(self):
        pass
