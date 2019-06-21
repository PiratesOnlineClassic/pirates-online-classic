from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm.FSM import FSM

from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.pirate.BattleNPCGameFSMAI import BattleNPCGameFSMAI
from pirates.piratesbase import PLocalizerEnglish
from pirates.battle import EnemyGlobals


class DistributedBattleNPCAI(DistributedBattleAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleNPCAI')

    def __init__(self, air):
        DistributedBattleAvatarAI.__init__(self, air)

        self.gameFSM = BattleNPCGameFSMAI(self.air, self)

        self.name = ''
        self.spawnPos = [0, 0, 0]
        self.animSet = ''
        self.collisionMode = 0
        self.initZ = 0

        self.spawnNode = None

    def generate(self):
        DistributedBattleAvatarAI.generate(self)
        self.air.targetMgr.addTarget(self)

    def getMonsterDmg(self):
        return EnemyGlobals.getMonsterDmg(self.level)

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def setSpawnPos(self, (x, y, z)):
        self.spawnPos = [x, y, z]

    def d_setSpawnPos(self, (x, y, z)):
        self.sendUpdate('setSpawnPos', [x, y, z])

    def b_setSpawnPos(self, (x, y, z)):
        self.setSpawnPos(x, y, z)
        self.d_setSpawnPos(x, y, z)

    def getSpawnPos(self):
        return self.spawnPos

    def d_setSpawnIn(self):
        self.sendUpdate('setSpawnIn', [globalClockDelta.getRealNetworkTime(bits=32)])

    def d_setChat(self, chatString, chatFlags=0):
        self.sendUpdate('setChat', [chatString, chatFlags])

    def setAnimSet(self, animSet):
        self.animSet = animSet

    def d_setAnimSet(self, animSet):
        self.sendUpdate('setAnimSet', [animSet])

    def b_setAnimSet(self, animSet):
        self.setAnimSet(animSet)
        self.d_setAnimSet(animSet)

    def getAnimSet(self):
        return self.animSet

    def setCollisionMode(self, collisionMode):
        self.collisionMode = collisionMode

    def d_setCollisionMode(self, collisionMode):
        self.sendUpdate('setCollisionMode', [collisionMode])

    def b_setCollisionMode(self, collisionMode):
        self.setCollisionMode(collisionMode)
        self.d_setCollisionMode(collisionMode)

    def getCollisionMode(self):
        return self.collisionMode

    def setInitZ(self, initZ):
        self.initZ = initZ

    def d_setInitZ(self, initZ):
        self.sendUpdate('setInitZ', [initZ])

    def b_setInitZ(self, initZ):
        self.setInitZ(initZ)
        self.d_setInitZ(initZ)

    def getInitZ(self):
        return self.initZ

    def setSpawnNode(self, spawnNode):
        self.spawnNode = spawnNode

    def getSpawnNode(self):
        return self.spawnNode

    def requestClientAggro(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        self.handleClientAggro(avatar)

    def handleClientAggro(self, avatar):
        self.d_setChat(PLocalizerEnglish.getNavyAggroPhrase())

    def delete(self):
        self.air.targetMgr.removeTarget(self)
        DistributedBattleAvatarAI.delete(self)
