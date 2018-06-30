from direct.directnotify import DirectNotifyGlobal
from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from direct.distributed.ClockDelta import globalClockDelta
from pirates.pirate.BattleNPCGameFSMAI import BattleNPCGameFSMAI


class DistributedBattleNPCAI(DistributedBattleAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedBattleNPCAI')

    def __init__(self, air):
        DistributedBattleAvatarAI.__init__(self, air)

        self.gameFSM = BattleNPCGameFSMAI(self.air, self)

        self.name = ''
        self.spawnPos = [0, 0, 0, 0, 0, 0]
        self.animSet = 'default'
        self.collisionMode = 0
        self.initZ = 0

        self.spawnerNode = None

    def generate(self):
        DistributedBattleAvatarAI.generate(self)

        self.air.battleMgr.addTarget(self)

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def setSpawnPosHpr(self, xxx_todo_changeme, xxx_todo_changeme1):
        (x, y, z) = xxx_todo_changeme
        (h, p, r) = xxx_todo_changeme1
        self.spawnPos = [x, y, z, h, p, r]

    def d_setSpawnPosHpr(self, x, y, z, h, p, r):
        self.sendUpdate('setSpawnPosHpr', [x, y, z, h, p, r])

    def b_setSpawnPosHpr(self, x, y, z, h, p, r):
        self.setSpawnPosHpr(x, y, z, h, p, r)
        self.d_setSpawnPosHpr(x, y, z, h, p, r)

    def getSpawnPosHpr(self):
        return self.spawnPos

    def setAnimSet(self, animSet):
        self.animSet = animSet

    def d_setAnimSet(self, animSet):
        self.sendUpdate('setAnimSet', [animSet])

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

    def setSpawner(self, spawnerNode):
        self.spawnerNode = spawnerNode

    def getSpawner(self):
        return self.spawnerNode

    def requestClientAggro(self):
        pass

    def d_setSpawnIn(self):
        self.sendUpdate(
            'setSpawnIn', [globalClockDelta.getRealNetworkTime(bits=32)])

    def delete(self):
        self.air.battleMgr.removeTarget(self)

        DistributedBattleAvatarAI.delete(self)
