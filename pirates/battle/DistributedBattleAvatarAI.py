from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.task import Task

from pirates.reputation. DistributedReputationAvatarAI import  DistributedReputationAvatarAI
from pirates.battle.WeaponBaseAI import WeaponBaseAI
from pirates.battle.Teamable import Teamable
from pirates.pirate import AvatarTypes
from pirates.pirate.BattleAvatarGameFSMAI import BattleAvatarGameFSMAI
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.battle.DistributedWeaponAI import DistributedWeaponAI
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from pirates.battle.BattleRandom import BattleRandom
from pirates.battle.BattleSkillDiaryAI import BattleSkillDiaryAI


class DistributedBattleAvatarAI(DistributedReputationAvatarAI, WeaponBaseAI, Teamable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleAvatarAI')

    def __init__(self, air):
        DistributedReputationAvatarAI.__init__(self, air)
        WeaponBaseAI.__init__(self, air)
        Teamable.__init__(self)

        self.gameFSM = BattleAvatarGameFSMAI(self.air, self)
        self.isNpc = True
        self.battleRandom = None

        self.avatarType = AvatarTypes.AnyAvatar
        self.shipId = 0
        self.currentWeaponId = 0
        self.isWeaponDrawn = False
        self.currentAmmo = 0
        self.shipId = 0
        self.maxHp = 0
        self.hp = 0
        self.immortal = False
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
        self.swiftnessMod = 0
        self.hasteMod = 0
        self.stunMod = 0
        self.powerMod = 0
        self.attackerId = 0
        self.combo = 0
        self.teamCombo = 0
        self.comboDamage = 0
        self.skillEffects = []
        self.ensaredTargetId = 0
        self.level = 0

        self.currentTarget = None
        self.weapon = None

    def announceGenerate(self):
        DistributedReputationAvatarAI.announceGenerate(self)

    def generate(self):
        DistributedReputationAvatarAI.generate(self)

        self.battleRandom = BattleRandom(self.doId)
        self.battleSkillDiary = BattleSkillDiaryAI(self.air, self)

    def setLocation(self, parentId, zoneId):
        DistributedReputationAvatarAI.setLocation(self, parentId, zoneId)

        parentObj = self.getParentObj()
        if parentObj:
            if isinstance(parentObj, DistributedGameAreaAI):
                if not self.weapon:
                    self.weapon = DistributedWeaponAI(self.air)
                    self.weapon.generateWithRequiredAndId(self.air.allocateChannel(),
                        self.parentId, self.zoneId)

                if self.weapon:
                    self.weapon.b_setLocation(parentId, zoneId)

    def getWorld(self):
        parentObj = self.getParentObj()
        if parentObj:
            if isinstance(parentObj, DistributedGameAreaAI):
                parentObj = parentObj.getParentObj()

        if not parentObj:
            return None

        if isinstance(parentObj, DistributedInstanceBaseAI):
            return parentObj

        return None

    def setAvatarType(self, avatarType):
        self.avatarType = avatarType

    def d_setAvatarType(self, avatarType):
        self.sendUpdate('setAvatarType', [avatarType])

    def b_setAvatarType(self, avatarType):
        self.setAvatarType(avatarType)
        self.d_setAvatarType(avatarType)

    def getAvatarType(self):
        return self.avatarType

    def setGameState(self, gameState, timestamp=0):
        self.gameFSM.request(gameState)

    def d_setGameState(self, gameState):
        self.sendUpdate('setGameState', [gameState, globalClockDelta.getRealNetworkTime(bits=16)])

    def b_setGameState(self, gameState):
        self.setGameState(gameState)
        self.d_setGameState(gameState)

    def getGameState(self):
        return self.gameFsm.getCurrentOrNextState()

    def setShipId(self, shipId):
        self.shipId = shipId

    def d_setShipId(self, shipId):
        self.sendUpdate('setShipId', [shipId])

    def b_setShipId(self, shipId):
        self.setShipId(shipId)
        self.d_setShipId(shipId)

    def getShipId(self):
        return self.shipId

    def setCurrentTarget(self, currentTargetDoId):
        if self.currentTarget is not None:
            if not currentTargetDoId:
                self.currentTarget.resetComboLevel()

        self.currentTarget = self.air.doId2do.get(currentTargetDoId)

    def d_setCurrentTarget(self, currentTargetDoId):
        self.sendUpdate('setCurrentTarget', [currentTargetDoId])

    def b_setCurrentTarget(self, currentTargetDoId):
        self.setCurrentTarget(currentTargetDoId)
        self.d_setCurrentTarget(currentTargetDoId)

    def getCurrentTarget(self):
        if not self.currentTarget:
            return 0

        return self.currentTarget.doId

    def setCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        self.currentWeaponId = currentWeaponId
        self.isWeaponDrawn = isWeaponDrawn

    def d_setCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        self.sendUpdate('setCurrentWeapon', [currentWeaponId, isWeaponDrawn])

    def b_setCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        self.setCurrentWeapon(currentWeaponId, isWeaponDrawn)
        self.d_setCurrentWeapon(currentWeaponId, isWeaponDrawn)

    def getCurrentWeapon(self):
        return [self.currentWeaponId, self.isWeaponDrawn]

    def setCurrentAmmo(self, currentAmmo):
        self.currentAmmo = currentAmmo

    def d_setCurrentAmmo(self, currentAmmo):
        self.sendUpdate('setCurrentAmmo', [currentAmmo])

    def b_setCurrentAmmo(self, currentAmmo):
        self.setCurrentAmmo(currentAmmo)
        self.d_setCurrentAmmo(currentAmmo)

    def getCurrentAmmo(self):
        return self.currentAmmo

    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def d_setMaxHp(self, maxHp):
        self.sendUpdate('setMaxHp', [maxHp])

    def b_setMaxHp(self, maxHp):
        self.setMaxHp(maxHp)
        self.d_setMaxHp(maxHp)

    def getMaxHp(self):
        return self.maxHp

    def setHp(self, hp, quietly=False):
        if self.getImmortal():
            return

        if hp <= 0 and self.hp > 0:
            self.b_setGameState('Death')

        self.hp = max(0, hp)
        self.quietly = quietly

    def d_setHp(self, hp, quietly=False):
        if self.getImmortal():
            return

        self.sendUpdate('setHp', [hp, quietly])

    def b_setHp(self, hp, quietly=False):
        self.setHp(hp, quietly)
        self.d_setHp(hp, quietly)

    def getHp(self):
        return [self.hp, self.quietly]

    def setImmortal(self, immortal):
        self.immortal = immortal

    def getImmortal(self):
        return self.immortal

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

    def getSwiftnessMod(self):
        return self.swiftnessMod

    def getHasteMod(self):
        return self.hasteMod

    def getStunMod(self):
        return self.stunMod

    def getPowerMod(self):
        return self.powerMod

    def setCombo(self, combo, teamCombo, comboDamage, attackerId):
        self.combo = combo
        self.teamCombo = teamCombo
        self.comboDamage = comboDamage
        self.attackerId = attackerId

    def d_setCombo(self, combo, teamCombo, comboDamage, attackerId):
        self.sendUpdate('setCombo', [combo, teamCombo, comboDamage, attackerId])

    def b_setCombo(self, combo, teamCombo, comboDamage, attackerId):
        self.setCombo(combo, teamCombo, comboDamage, attackerId)
        self.d_setCombo(combo, teamCombo, comboDamage, attackerId)

    def getCombo(self):
        return [self.combo, self.teamCombo, self.comboDamage, self.attackerId]

    def resetComboLevel(self):
        self.combo = 0
        self.teamCombo = 0
        self.comboDamage = 0
        self.attackerId = 0

    def setSkillEffects(self, skillEffects):
        self.skillEffects = skillEffects

    def d_setSkillEffects(self, skillEffects):
        self.sendUpdate('setSkillEffects', [skillEffects])

    def b_setSkillEffects(self, skillEffects):
        self.setSkillEffects(skillEffects)
        self.d_setSkillEffects(skillEffects)

    def hasSkillEffect(self, effectId):
        for skillEffect in list(self.skillEffects):
            if skillEffect[0] == effectId:
                return True

        return False

    def addSkillEffect(self, effectId, duration, attackerId):
        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        skillEffect = [
            effectId,
            duration,
            timestamp,
            attackerId]

        self.skillEffects.append(skillEffect)
        self.d_setSkillEffects(self.skillEffects)

    def removeSkillEffect(self, effectId):
        if not self.hasSkillEffect(effectId):
            return

        for skillEffect in list(self.skillEffects):
            if skillEffect[0] == effectId:
                self.skillEffects.remove(skillEffect)

                # attempt to remove the skill effect from the battle manager's
                # deque of pending skill effects:
                self.air.battleMgr.removePendingSkillEffect(effectId)
                break

        self.d_setSkillEffects(self.skillEffects)

    def getSkillEffectCount(self, effectId):
        numSkillEffects = 0
        for skillEffect in list(self.skillEffects):
            if skillEffect[0] == effectId:
                numSkillEffects += 1

        return numSkillEffects

    def clearSkillEffects(self):
        for skillEffect in list(self.skillEffects):
            self.air.battleMgr.removePendingSkillEffect(skillEffect[0])

        self.skillEffects = []
        self.d_setSkillEffects(self.skillEffects)

    def getSkillEffects(self):
        return self.skillEffects

    def setEnsaredTargetId(self, ensaredTargetId):
        self.ensaredTargetId = ensaredTargetId

    def d_setEnsaredTargetId(self, ensaredTargetId):
        self.sendUpdate('setEnsaredTargetId', [ensaredTargetId])

    def b_setEnsaredTargetId(self, ensaredTargetId):
        self.setEnsaredTargetId(ensaredTargetId)
        self.d_setEnsaredTargetId(ensaredTargetId)

    def getEnsnaredTargetId(self):
        return self.ensaredTargetId

    def interupted(self, todo):
        pass

    def setLevel(self, level):
        self.level = level

    def d_setLevel(self, level):
        self.sendUpdate('setLevel', [level])

    def b_setLevel(self, level):
        self.setLevel(level)
        self.d_setLevel(level)

    def getLevel(self):
        return self.level

    def isBoss(self):
        return self.avatarType.isA(AvatarTypes.BossType)

    def delete(self):
        self.clearSkillEffects()
        if self.battleRandom:
            self.battleRandom.delete()
            self.battleRandom = None

        if self.weapon:
            self.weapon.requestDelete()
            self.weapon = None

        self.gameFSM.destroy()
        self.gameFSM = None
        DistributedReputationAvatarAI.delete(self)
