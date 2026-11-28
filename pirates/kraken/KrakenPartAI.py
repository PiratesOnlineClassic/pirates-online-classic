from direct.directnotify import DirectNotifyGlobal
from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from pirates.piratesbase import PiratesGlobals
from pirates.battle import EnemyGlobals


class KrakenPartAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('KrakenPartAI')

    # how much tougher this part is than a regular enemy of the same level
    HpScale = 1.0

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)

        self.krakenId = 0

    def createGameFSM(self):
        raise NotImplementedError('%s does not extend createGameFSM!' % \
            self.__class__.__name__)

    def setupPart(self, avatarType, level):
        self.setAvatarType(avatarType)
        self.setLevel(level)
        self.setName(avatarType.getName())
        self.setTeam(PiratesGlobals.UNDEAD_TEAM)
        self.setStartState('LandRoam')

        maxHp, maxMojo = EnemyGlobals.getEnemyStats(avatarType, level)
        self.setMaxHp(int(maxHp * self.HpScale))
        self.setHp(self.getMaxHp(), True)
        self.setMaxMojo(maxMojo)
        self.setMojo(maxMojo)

    def setKrakenId(self, krakenId):
        self.krakenId = krakenId

    def d_setKrakenId(self, krakenId):
        self.sendUpdate('setKrakenId', [krakenId])

    def b_setKrakenId(self, krakenId):
        self.setKrakenId(krakenId)
        self.d_setKrakenId(krakenId)

    def getKrakenId(self):
        return self.krakenId

    def getKraken(self):
        return self.air.doId2do.get(self.krakenId)

    def isDead(self):
        # our hp is updated after the death state has been entered, so
        # also check the game state.
        return self.hp <= 0 or self.gameFSM.getCurrentOrNextState() == 'Death'

    def requestClientAggro(self):
        # the kraken decides who it attacks, not the client.
        pass

    def processDeath(self):
        self.air.battleMgr.rewardAttackers(self)
        self.air.targetMgr.clearTarget(self)

        kraken = self.getKraken()
        if kraken:
            kraken.partDied(self)
