from direct.directnotify import DirectNotifyGlobal
from pirates.battle.DistributedBattleNPCAI import *
from pirates.pirate import AvatarTypes
from pirates.creature.CreatureGameFSMAI import CreatureGameFSMAI

class DistributedCreatureAI(DistributedBattleNPCAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCreatureAI')

    # creatures that are rooted to the ground and cannot walk
    StationaryCreatures = [
        AvatarTypes.FlyTrap]

    # creatures that never start a fight on their own
    PassiveCreatures = [
        AvatarTypes.Monkey]

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)

        # creatures have their own rules for which game states they
        # can enter, replace the generic battle npc game fsm...
        self.gameFSM.destroy()
        self.gameFSM = self.createGameFSM()

    def createGameFSM(self):
        return CreatureGameFSMAI(self.air, self)

    def isStationary(self):
        return self.avatarType.getNonBossType() in self.StationaryCreatures

    def isPassive(self):
        return self.avatarType.getNonBossType() in self.PassiveCreatures

    def setStartState(self, startState):
        if self.isStationary() and startState in ['Patrol', 'Walk']:
            startState = 'Idle'

        DistributedBattleNPCAI.setStartState(self, startState)

    def requestClientAggro(self):
        if self.isPassive():
            return

        DistributedBattleNPCAI.requestClientAggro(self)

    def d_setChat(self, chatString, chatFlags=0):
        # creatures do not have anything to say...
        if not chatString:
            return

        DistributedBattleNPCAI.d_setChat(self, chatString, chatFlags)
