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
from pirates.battle import WeaponConstants


class DistributedBattleAvatarAI(DistributedReputationAvatarAI, WeaponBaseAI, Teamable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleAvatarAI')

    # how often the avatar's skill effects recur and expire
    SkillEffectsUpdateInterval = 0.5

    # slowed avatars move at half their speed and hastened avatars move at one and
    # a half their speed (see PLocalizer.HastenDesc), see LocalPirate.updatePlayerSpeed...
    SlowStunMod = -0.5
    HastenHasteMod = 0.5

    def __init__(self, air):
        DistributedReputationAvatarAI.__init__(self, air)
        WeaponBaseAI.__init__(self, air)
        Teamable.__init__(self)

        self.gameFSM = self.createGameFSM()
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
        self._skillEffectTimers = {}
        self._skillEffectsTask = None
        self._skillEffectImmobilized = False
        self.ensnaredTargetId = 0
        self.level = 0

        self.currentTarget = None
        self.weapon = None

    def createGameFSM(self):
        return BattleAvatarGameFSMAI(self.air, self)

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
        try:
            self.gameFSM.request(gameState)
        except AssertionError:
            self.notify.warning("Invalid game state request: %s" % gameState)

    def d_setGameState(self, gameState):
        self.sendUpdate('setGameState', [gameState, globalClockDelta.getRealNetworkTime(bits=16)])

    def b_setGameState(self, gameState):
        self.setGameState(gameState)

        # only broadcast the state when our FSM actually accepted it
        if self.gameFSM.getCurrentOrNextState() == gameState:
            self.d_setGameState(gameState)

    def getGameState(self):
        return self.gameFSM.getCurrentOrNextState()

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

        justRanOutOfHp = hp <= 0 and self.hp > 0
        self.hp = max(0, hp)
        self.quietly = quietly

        # update our hp before entering the death state, so that the death
        # state sees the avatar as defeated and may restore it's hp...
        if justRanOutOfHp:
            self.b_setGameState('Death')

    def d_setHp(self, hp, quietly=False):
        if self.getImmortal():
            return

        self.sendUpdate('setHp', [hp, quietly])

    def b_setHp(self, hp, quietly=False):
        self.setHp(hp, quietly)
        self.d_setHp(hp, quietly)

    def getHp(self):
        return [self.hp, self.quietly]

    def getAdjMaxHp(self):
        return self.maxHp

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

    def getAdjMaxMojo(self):
        return self.maxMojo

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
        self.sendUpdate('setMaxSwiftness', [maxSwiftness])

    def b_setMaxSwiftness(self, maxSwiftness):
        self.setMaxSwiftness(maxSwiftness)
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

    def setHasteMod(self, hasteMod):
        self.hasteMod = hasteMod

    def d_setHasteMod(self, hasteMod):
        self.sendUpdate('setHasteMod', [hasteMod])

    def b_setHasteMod(self, hasteMod):
        self.setHasteMod(hasteMod)
        self.d_setHasteMod(hasteMod)

    def getHasteMod(self):
        return self.hasteMod

    def setStunMod(self, stunMod):
        self.stunMod = stunMod

    def d_setStunMod(self, stunMod):
        self.sendUpdate('setStunMod', [stunMod])

    def b_setStunMod(self, stunMod):
        self.setStunMod(stunMod)
        self.d_setStunMod(stunMod)

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

    def getSkillEffectTime(self):
        return globalClock.getFrameTime()

    def addSkillEffect(self, effectId, duration, attackerId, recur=0):
        # the client keys it's buffs by their effect and attacker, it only reads
        # a buff's duration and timestamp when the buff first appears. renewing
        # an effect removes the old buff first so the buff tray restarts it...
        if self.__removeSkillEffectEntries(effectId, attackerId):
            self.d_setSkillEffects(self.skillEffects)

        # buff durations are sent in whole seconds (int16), their timestamps
        # are 16 bit network times, see BuffIcon.updateIconInfo...
        self.skillEffects.append([
            effectId,
            max(-32768, min(32767, int(duration))),
            globalClockDelta.getRealNetworkTime(bits=16),
            attackerId])

        now = self.getSkillEffectTime()
        expireTime = now + duration if duration > 0 else None
        nextTickTime = now + recur if recur > 0 else None
        self._skillEffectTimers[(effectId, attackerId)] = [expireTime, nextTickTime, recur]

        self.d_setSkillEffects(self.skillEffects)
        self.updateSkillEffectMods()
        self.__startSkillEffectsTask()

    def __removeSkillEffectEntries(self, effectId, attackerId=None):
        removed = False
        for skillEffect in list(self.skillEffects):
            if skillEffect[0] != effectId:
                continue

            if attackerId is not None and skillEffect[3] != attackerId:
                continue

            self.skillEffects.remove(skillEffect)
            self._skillEffectTimers.pop((skillEffect[0], skillEffect[3]), None)
            removed = True

        return removed

    def removeSkillEffect(self, effectId, attackerId=None):
        if not self.__removeSkillEffectEntries(effectId, attackerId):
            return

        self.d_setSkillEffects(self.skillEffects)
        self.updateSkillEffectMods()

    def getSkillEffectCount(self, effectId):
        numSkillEffects = 0
        for skillEffect in list(self.skillEffects):
            if skillEffect[0] == effectId:
                numSkillEffects += 1

        return numSkillEffects

    def getSkillEffectAttackers(self, effectId):
        return [skillEffect[3] for skillEffect in self.skillEffects if skillEffect[0] == effectId]

    def clearSkillEffects(self):
        self.__stopSkillEffectsTask()
        self._skillEffectTimers = {}
        if not self.skillEffects:
            return

        self.skillEffects = []
        self.d_setSkillEffects(self.skillEffects)
        self.updateSkillEffectMods()

    def getSkillEffects(self):
        return self.skillEffects

    def getSkillEffectIds(self):
        # getSkillEffects is the getter of the required BuffList field, the battle
        # formulas need the ids of the active effects (see BattleManagerBase)...
        effectIds = []
        for skillEffect in self.skillEffects:
            if skillEffect[0] not in effectIds:
                effectIds.append(skillEffect[0])

        return effectIds

    def __startSkillEffectsTask(self):
        if self._skillEffectsTask or not self._skillEffectTimers:
            return

        self._skillEffectsTask = taskMgr.doMethodLater(self.SkillEffectsUpdateInterval,
            self.__updateSkillEffectsTask, self.taskName('updateSkillEffects'))

    def __stopSkillEffectsTask(self):
        if self._skillEffectsTask:
            taskMgr.remove(self._skillEffectsTask)
            self._skillEffectsTask = None

    def __updateSkillEffectsTask(self, task):
        self.updateSkillEffects(self.getSkillEffectTime())
        if not self._skillEffectTimers:
            self._skillEffectsTask = None
            return task.done

        return task.again

    def updateSkillEffects(self, now):
        # defeated avatars lose all of their effects...
        if self.hp <= 0:
            self.clearSkillEffects()
            return

        expired = []
        for key, timer in list(self._skillEffectTimers.items()):
            expireTime, nextTickTime, recur = timer

            # damage over time effects deal their effects every time they recur
            # until they expire, see BattleManagerAI.applySkillEffectTick...
            while nextTickTime is not None and nextTickTime <= now and (expireTime is None or nextTickTime <= expireTime):
                self.air.battleMgr.applySkillEffectTick(self, key[0], key[1])
                if self._skillEffectTimers.get(key) is not timer:
                    break

                nextTickTime += recur
                timer[1] = nextTickTime

            if self._skillEffectTimers.get(key) is not timer:
                continue

            if expireTime is not None and now >= expireTime:
                expired.append(key)

        removed = False
        for effectId, attackerId in expired:
            removed = self.__removeSkillEffectEntries(effectId, attackerId) or removed

        if removed:
            self.d_setSkillEffects(self.skillEffects)
            self.updateSkillEffectMods()

    def updateSkillEffectMods(self):
        # the client moves it's avatar at the speed these mods give, see
        # LocalPirate.updatePlayerSpeed. stuns and holds take all of the avatar's
        # swiftness away (see WeaponGlobals.getEffects), until they expire...
        effectIds = self.getSkillEffectIds()
        immobilized = WeaponConstants.C_STUN in effectIds or WeaponConstants.C_HOLD in effectIds
        if immobilized and not self._skillEffectImmobilized:
            self._skillEffectImmobilized = True
            if self.swiftness > 0:
                self.b_setSwiftness(0)
        elif not immobilized and self._skillEffectImmobilized:
            self._skillEffectImmobilized = False
            if self.swiftness < self.maxSwiftness:
                self.b_setSwiftness(self.maxSwiftness)

        stunMod = self.SlowStunMod if WeaponConstants.C_SLOW in effectIds else 0
        if stunMod != self.stunMod:
            self.b_setStunMod(stunMod)

        hasteMod = self.HastenHasteMod if WeaponConstants.C_HASTEN in effectIds else 0
        if hasteMod != self.hasteMod:
            self.b_setHasteMod(hasteMod)

    def setEnsnaredTargetId(self, ensnaredTargetId):
        self.ensnaredTargetId = ensnaredTargetId

    def d_setEnsnaredTargetId(self, ensnaredTargetId):
        self.sendUpdate('setEnsnaredTargetId', [ensnaredTargetId])

    def b_setEnsnaredTargetId(self, ensnaredTargetId):
        self.setEnsnaredTargetId(ensnaredTargetId)
        self.d_setEnsnaredTargetId(ensnaredTargetId)

    def getEnsnaredTargetId(self):
        return self.ensnaredTargetId

    def interrupted(self, todo):
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
        self.__stopSkillEffectsTask()
        self._skillEffectTimers = {}
        self.skillEffects = []
        if self.battleRandom:
            self.battleRandom.delete()
            self.battleRandom = None

        if self.weapon:
            self.weapon.requestDelete()
            self.weapon = None

        self.gameFSM.destroy()
        self.gameFSM = None
        DistributedReputationAvatarAI.delete(self)
