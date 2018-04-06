from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.battle.WeaponBase import WeaponBase
from pirates.battle.Teamable import Teamable

class DistributedBattleAvatarAI(WeaponBase, Teamable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleAvatarAI')

    def __init__(self, air):
        WeaponBase.__init__(self)
        Teamable.__init__(self)
        self.maxHp = 0
        self.hp = 0
        self.quietly = False
        self.luck = 0
        self.maxLuck = 0
        self.mojo = 0
        self.maxMojo = 0
        self.swiftness = 0
        self.maxSwiftness = 0
        self.power = 0
        self.maxPower = 0
        self.luckMod = 0
        self.mojoMod = 0

    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def d_setMaxHp(self, maxHp):
        self.sendUpdate('setMaxHp', [maxHp])

    def b_setMaxHp(self, maxHp):
        self.setMaxHp(maxHp)
        self.d_setMaxHp(maxHp)

    def getMaxHp(self):
        return self.maxHp

    def setHp(self, hp, quietly):
        self.hp = hp
        self.quietly = quietly

    def d_setHp(self, hp, quietly):
        self.sendUpdate('setHp', [hp, quietly])

    def b_setHp(self, hp, quietly=False):
        self.setHp(hp, quietly)
        self.d_setHp(hp, quietly)

    def getHp(self):
        return (self.hp, self.quietly)

    def setLuck(self, luck):
        self.luck = luck

    def d_setLuck(self, luck):
        self.sendUpdate('setLuck', [luck])

    def b_setLuck(self, luck):
        self.setLuck(luck)
        self.d_setLuck(luck)

    def getLuck(self):
        return self.luck

    def setMaxLuck(self, maxLuck):
        self.maxLuck = maxLuck

    def d_setMaxLuck(self, maxLuck):
        self.sendUpdate('setMaxLuck', [maxLuck])

    def b_setMaxLuck(self, maxLuck):
        self.setMaxLuck(maxLuck)
        self.d_setMaxLuck(maxLuck)

    def getMaxLuck(self):
        return self.maxLuck

    def setMaxMojo(self, maxMojo):
        self.maxMojo = maxMojo

    def d_setMaxMojo(self, maxMojo):
        self.sendUpdate('setMaxMojo', [maxMojo])

    def b_setMaxMojo(self, maxMojo):
        self.setMaxMojo(maxMojo)
        self.d_setMaxMojo(maxMojo)

    def getMaxMojo(self):
        return self.maxMojo

    def setMojo(self, mojo):
        self.mojo = mojo

    def d_setMojo(self, mojo):
        self.sendUpdate('setMojo', [mojo])

    def b_setMojo(self, mojo):
        self.setMojo(mojo)
        self.d_setMojo(self.mojo)

    def getMojo(self):
        return self.mojo

    def setSwiftness(self, swiftness):
        self.swiftness = swiftness

    def d_setSwiftness(self, swiftness):
        self.sendUpdate('setSwiftness', [swiftness])

    def b_setSwiftness(self, swiftness):
        self.setSwiftness(swiftness)
        self.d_setSwiftness(swiftness)

    def getSwiftness(self):
        return self.swiftness

    def setMaxSwiftness(self, maxSwiftness):
        self.maxSwiftness = maxSwiftness

    def d_setMaxSwiftness(self, maxSwiftness):
        self.sendUpdate('setMaxSwiftnes', [maxSwiftness])

    def b_setMaxSwiftness(self, maxSwiftness):
        self.setMaxSwiftnes(maxSwiftness)
        self.d_setMaxSwiftness(maxSwiftness)

    def getMaxSwiftness(self):
        return self.maxSwiftness

    def setPower(self, power):
        self.power = power

    def d_setPower(self, power):
        self.sendUpdate('setPower', [power])

    def b_setPower(self, power):
        self.setPower(power)
        self.d_setPower(power)

    def getPower(self):
        return self.power

    def setMaxPower(self, maxPower):
        self.maxPower = maxPower

    def d_setMaxPower(self, maxPower):
        self.sendUpdate('setMaxPower', [maxPower])

    def b_setMaxPower(self, maxPower):
        self.setMaxPower(maxPower)
        self.d_setMaxPower(maxPower)

    def getMaxPower(self):
        return self.maxPower

    def setLuckMod(self, luckMod):
        self.luckMod = luckMod

    def d_setLuckMod(self, luckMod):
        self.sendUpdate('setLuckMod', [luckMod])

    def b_setLuckMod(self, luckMod):
        self.setLuckMod(luckMod)
        self.d_setLuckMod(luckMod)

    def getLuckMod(self):
        return self.luckMod

    def setMojoMod(self, mojoMod):
        self.mojoMod = mojoMod

    def d_setMojoMod(self, mojoMod):
        self.sendUpdate('setMojoMod', [mojoMod])

    def b_setMojoMod(self, mojoMod):
        self.setMojoMod(mojoMod)
        self.d_setMojoMod(mojoMod)

    def getMojoMod(self):
        return self.mojoMod
