from direct.directnotify import DirectNotifyGlobal
from pirates.destructibles.DistributedDestructibleObjectAI import DistributedDestructibleObjectAI

class DistributedDestructibleArrayAI(DistributedDestructibleObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDestructibleArrayAI')

    def __init__(self, air):
        DistributedDestructibleObjectAI.__init__(self, air)
        self.maxArrayHp = [100]
        self.arrayHp = [100]

    def setMaxArrayHp(self, maxArrayHp):
        self.maxArrayHp = maxArrayHp

    def d_setMaxArrayHp(self, maxArrayHp):
        self.sendUpdate("setMaxArrayHp", [maxArrayHp])

    def b_setMaxArrayHp(self, maxArrayHp):
        self.setMaxArrayHp(maxArrayHp)
        self.d_setMaxArrayHp(maxArrayHp)

    def getMaxArrayHp(self):
        return self.maxArrayHp

    def setArrayHp(self, arrayHp):
        self.arrayHp = arrayHp

    def d_setArrayHp(self, arrayHp):
        self.sendUpdate("setArrayHp", [arrayHp])

    def b_setArrayHp(self, arrayHp):
        self.setArrayHp(arrayHp)
        self.d_setArrayHp(arrayHp)

    def getArrayHp(self):
        return self.arrayHp

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        pass
