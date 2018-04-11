from direct.directnotify import DirectNotifyGlobal
from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI

class DistributedBattleNPCAI(DistributedBattleAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleNPCAI')

    def __init__(self, air):
        DistributedBattleAvatarAI.__init__(self, air)

        self.name = ''
        self.spawnPos = [0, 0, 0, 0, 0, 0]
        self.actorAnims = ['', '', '', '']
        self.animSet = ''
        self.collisionMode = 0
        self.initZ = 0

        self.spawnerNode = None

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def setSpawnPosHpr(self, (x, y, z), (h, p, r)):
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

    def setSpawner(self, spawner):
        self.spawnerNode = spawner

    def setHp(self, hp, quietly=False):
        DistributedBattleAvatarAI.setHp(self, hp, quietly)

        # Tell the spawner we have perished!
        if hp <= 0:
            if self.spawnerNode:
                self.spawnerNode.processDeath()
            else:
                self.notify.warning('%s died without a spawner node to respawn!' % self.__class__.__name__)