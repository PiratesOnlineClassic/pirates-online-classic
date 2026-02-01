from direct.directnotify import DirectNotifyGlobal

from pirates.shipparts.DistributedShippartAI import DistributedShippartAI
from pirates.shipparts.HullDNA import HullDNA
from pirates.destructibles.DistributedDestructibleArrayAI import DistributedDestructibleArrayAI
from pirates.ship import ShipBalance


class DistributedHullDNA(HullDNA):
    pass

class DistributedHullAI(DistributedShippartAI, DistributedDestructibleArrayAI, DistributedHullDNA):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHullAI')

    def __init__(self, air):
        DistributedShippartAI.__init__(self, air)
        DistributedDestructibleArrayAI.__init__(self, air)
        DistributedHullDNA.__init__(self)

        self.maxSp = 0
        self.sp = 0
        self.maxCargo = 0

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

    def setMaxCargo(self, maxCargo):
        self.maxCargo = maxCargo

    def d_setMaxCargo(self, maxCargo):
        self.sendUpdate('setMaxCargo', [maxCargo])

    def b_setMaxCargo(self, maxCargo):
        self.setMaxCargo(maxCargo)
        self.d_setMaxCargo(maxCargo)

    def getMaxCargo(self):
        return self.maxCargo

    def getArmorStatus(self):
        if len(self.arrayHp) % 2 == 1:
            left = 1.0 - (self.arrayHp[1] + self.arrayHp[3] + self.arrayHp[5]) / float(self.maxArrayHp[1] + self.maxArrayHp[3] + self.maxArrayHp[5])
            rear = 1.0 - self.arrayHp[0] / float(self.maxArrayHp[0])
            right = 1.0 - (self.arrayHp[2] + self.arrayHp[4] + self.arrayHp[6]) / float(self.maxArrayHp[2] + self.maxArrayHp[4] + self.maxArrayHp[6])
        else:
            left = 1.0 - (self.arrayHp[1] + self.arrayHp[3] + self.arrayHp[5]) / float(self.maxArrayHp[1] + self.maxArrayHp[3] + self.maxArrayHp[5])
            rear = 1.0 - self.arrayHp[0] / float(self.maxArrayHp[0])
            right = 1.0 - (self.arrayHp[2] + self.arrayHp[4]) / float(self.maxArrayHp[2] + self.maxArrayHp[4])

        return (left, rear, right)

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        cannonCode, hullCode, sailCode = codes
        hullDamage = self.air.battleMgr.getModifiedHullDamage(attacker, self.ship, skillId, ammoSkillId)

        index = -1
        if hullCode == 255:
            for x in range(len(self.arrayHp)):
                if self.arrayHp[x] > 0:
                    index = x
                    break
        else:
            index = hullCode - 1
            if index > 0:
                index = (index - 1) % 2 + 1

        if index == -1:
            return

        arrayHp = list(self.arrayHp)
        if index >= len(arrayHp):
            return

        arrayHp[index] = max(arrayHp[index] + hullDamage, 0)
        self.b_setArrayHp(arrayHp)

        # now damage the ship, but absorbing some of the damage until our
        # hull armor is completely gone:
        left, rear, right = self.getArmorStatus()
        armorAsorb = (left + rear + right) / 3
        armorAsorb = min(armorAsorb, ShipBalance.ArmorAbsorb.getValue())
        self.ship.b_setHp(self.ship.getHp() + (hullDamage - (armorAsorb * hullDamage)))
