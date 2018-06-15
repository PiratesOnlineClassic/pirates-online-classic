from pirates.shipparts.DistributedShippartAI import DistributedShippartAI
from direct.directnotify import DirectNotifyGlobal
from pirates.shipparts.SailDNA import SailDNA
from pirates.destructibles.DistributedDestructibleArrayAI import DistributedDestructibleArrayAI


class DistributedSailDNA(SailDNA):

    def __init__(self):
        SailDNA.__init__(self)

class DistributedSailAI(DistributedShippartAI, DistributedDestructibleArrayAI, DistributedSailDNA):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSailAI')

    def __init__(self, air):
        DistributedShippartAI.__init__(self, air)
        DistributedDestructibleArrayAI.__init__(self, air)
        DistributedSailDNA.__init__(self)

        self.maxHp = 0
        self.hp = 0
        self.maxSp = 0
        self.sp = 0
        self.animState = ''

    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def d_setMaxHp(self, maxHp):
        self.sendUpdate('setMaxHp', [maxHp])

    def b_setMaxHp(self, maxHp):
        self.setMaxHp(maxHp)
        self.d_setMaxHp(maxHp)

    def getMaxHp(self):
        return self.maxHp

    def setHp(self, hp):
        self.hp = hp

    def d_setHp(self, hp):
        self.sendUpdate('setHp', [hp])

    def b_setHp(self, hp):
        self.setHp(hp)
        self.d_setHp(hp)

    def getHp(self):
        return self.hp

    def setMaxSp(self, maxSp):
        self.maxSp = maxSp

    def d_setMaxSp(self, maxSp):
        self.sendUpdate('setMaxSp', [maxSp])

    def b_setMaxSp(self, maxSp):
        self.setMaxSp(maxSp)
        self.d_setMaxSp(maxSp)

    def getMaxSp(self):
        return self.maxSp

    def setSp(self, sp):
        self.sp = sp

    def d_setSp(self, sp):
        self.sendUpdate('setSp', [sp])

    def b_setSp(self, sp):
        self.setSp(sp)
        self.d_setSp(sp)

    def getSp(self):
        return self.sp

    def requestSetAnimState(self, animState):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        self.b_setAnimState(animState)

    def setAnimState(self, animState):
        self.animState = animState

    def d_setAnimState(self, animState):
        self.sendUpdate('setAnimState', [animState])

    def b_setAnimState(self, animState):
        self.setAnimState(animState)
        self.d_setAnimState(animState)

    def getAnimState(self):
        return self.animState
