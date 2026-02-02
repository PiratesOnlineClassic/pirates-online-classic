import math
import random
from direct.showbase.DirectObject import *
from direct.distributed.ClockDelta import *
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.showbase.PythonUtil import quickProfile
from direct.interval.ProjectileInterval import *
from direct.interval.IntervalGlobal import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.task import Task
from pirates.piratesbase import PiratesGlobals
from pirates.shipparts import CannonPort
from pirates.effects.CannonMuzzleFire import CannonMuzzleFire
from pirates.effects.CannonBlastSmoke import CannonBlastSmoke
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.GrapeshotEffect import GrapeshotEffect
from pirates.effects.MuzzleFlame import MuzzleFlame
from pirates.effects.MuzzleFlash import MuzzleFlash
from pirates.ship import ShipGlobals
from pirates.ship import ShipBalance
from pirates.ship.DistributedShip import DistributedShip
from pirates.shipparts.DistributedShippart import DistributedShippart
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.shipparts import ShipPart
from pirates.battle.WeaponGlobals import *
from pirates.battle.EnemySkills import EnemySkills
from .DistributedWeapon import DistributedWeapon
from . import WeaponGlobals
from . import CannonGlobals
from .CannonballProjectile import CannonballProjectile
localFireSfxNames = [
    'cball_fire_1.mp3',
    'cball_fire_2.mp3',
    'cball_fire_3.mp3',
    'cball_fire_4.mp3',
    'cball_fire_5.mp3']
distFireSfxNames = [
    'dist_cannon_01.mp3',
    'dist_cannon_02.mp3',
    'dist_cannon_03.mp3',
    'dist_cannon_04.mp3',
    'dist_cannon_05.mp3',
    'dist_cannon_06.mp3',
    'dist_cannon_07.mp3',
    'dist_cannon_08.mp3',
    'dist_cannon_09.mp3',
    'dist_cannon_10.mp3']

class DistributedShipBroadside(DistributedWeapon, DistributedShippart):
    notify = directNotify.newCategory('DistributedShipBroadside')
    localFireSfx = []
    distFireSfx = []

    def __init__(self, cr):
        DistributedWeapon.__init__(self, cr)
        DistributedShippart.__init__(self, cr)
        self.baseVel = Vec3(0)
        self.setPos(0, 0, 0)
        self.ball = None
        self.baseTeam = 0
        self.prop = None
        self.av = None
        self.ammoType = 0
        self.shotNum = 0
        self.leftBroadside = []
        self.rightBroadside = []
        self.leftBroadsideConfig = []
        self.rightBroadsideConfig = []
        self.rightPlayShots = []
        self.leftPlayShots = []
        self.collisionLists = {}
        self.listening = False
        if not self.localFireSfx:
            for filename in localFireSfxNames:
                audioPath = 'audio/'
                self.localFireSfx.append(base.loader.loadSfx('audio/' + filename))

        if not self.distFireSfx:
            for filename in distFireSfxNames:
                self.distFireSfx.append(base.loader.loadSfx('audio/' + filename))

        self.aimAITrack = None
        if __dev__ and config.GetBool('want-broadside-assist', 0):
            self.tracker = loader.loadModelCopy('models/effects/explosion_sphere')
            self.tracker.reparentTo(render)
            self.tracker.setScale(30)

    def disable(self):
        self.ignoreAll()
        self.av = None
        self.effectNode.removeNode()
        self.effectNode = None
        taskMgr.remove(self.getTrailTaskName())
        if self.aimAITrack:
            self.aimAITrack.pause()
            self.aimAITrack = None

        DistributedWeapon.disable(self)
        DistributedShippart.disable(self)

    def generate(self):
        DistributedWeapon.generate(self)
        DistributedShippart.generate(self)

    def announceGenerate(self):
        self.effectNode = NodePath(ModelNode('broadside-%d-effects' % self.doId))
        self.effectNode.reparentTo(self)
        DistributedWeapon.announceGenerate(self)
        DistributedShippart.announceGenerate(self)

    def delete(self):
        for i in self.leftPlayShots:
            i.pause()

        del self.leftPlayShots
        for i in self.rightPlayShots:
            i.pause()

        del self.rightPlayShots
        del self.rightBroadside
        del self.leftBroadside
        del self.rightBroadsideConfig
        del self.leftBroadsideConfig
        self.ignoreAll()
        self.removeNode()
        if self.ship.broadside:
            self.ship.broadside[1] = None

        DistributedWeapon.delete(self)
        DistributedShippart.delete(self)

    def load(self):
        bs = self.ship.broadside
        if bs:
            if bs[0]:
                self.leftBroadside = bs[0][0]
                self.rightBroadside = bs[0][1]
                self.ship.broadside[1] = self
                return

        self.loadModel()
        self.addPropToShip()
        self.ship.broadside = [[self.leftBroadside, self.rightBroadside], self]

    def loadModel(self):
        for i in range(len(self.leftBroadsideConfig)):
            if self.leftBroadsideConfig[i] > 0:
                locator = self.ship.locators.find('**/broadsides_left').find('broadside_left_%s;+s' % i)
                cannon = CannonPort.CannonPort(self.leftBroadsideConfig[i], self, locator, 0, len(self.leftBroadside))
                cannon.setEnabled(self.leftBroadsideEnabledState[i])
                lpos = locator.getPos()
                lhpr = locator.getHpr()
                lscale = locator.getScale()
                cannon.geom_Medium.reparentTo(self.ship.mediumDetail)
                cannon.geom_Medium.setPos(lpos)
                cannon.geom_Medium.setHpr(lhpr)
                cannon.geom_Medium.setScale(lscale)
                cannon.geom_High.reparentTo(self.ship.highDetail)
                cannon.geom_High.setPos(lpos)
                cannon.geom_High.setHpr(lhpr)
                cannon.geom_High.setScale(lscale)
                self.leftBroadside.append(cannon)
            else:
                self.leftBroadside.append(None)

        for i in range(len(self.rightBroadsideConfig)):
            if self.rightBroadsideConfig[i] > 0:
                locator = self.ship.locators.find('**/broadsides_right').find('broadside_right_%s;+s' % i)
                cannon = CannonPort.CannonPort(self.rightBroadsideConfig[i], self, locator, 1, len(self.rightBroadside))
                cannon.setEnabled(self.rightBroadsideEnabledState[i])
                lpos = locator.getPos()
                lhpr = locator.getHpr()
                lscale = locator.getScale()
                cannon.geom_Medium.reparentTo(self.ship.mediumDetail)
                cannon.geom_Medium.setPos(lpos)
                cannon.geom_Medium.setHpr(lhpr)
                cannon.geom_Medium.setScale(lscale)
                cannon.geom_High.reparentTo(self.ship.highDetail)
                cannon.geom_High.setPos(lpos)
                cannon.geom_High.setHpr(lhpr)
                cannon.geom_High.setScale(lscale)
                cannon.locator = locator
                self.rightBroadside.append(cannon)
            else:
                self.rightBroadside.append(None)

    def fireBroadside(self, side, targetId = 0):
        zoneId = 0
        target = self.cr.doId2do.get(targetId)
        if target:
            if isinstance(target, DistributedShip):
                targetPos = target.transNode.getPos(render)
            else:
                targetPos = target.getPos(render)
            zoneId = self.cr.activeWorld.worldGrid.getZoneFromXYZ(targetPos)
            zonePos = self.cr.activeWorld.worldGrid.getZoneCellOrigin(zoneId)

        shipPos = self.ship.getPos(render)
        cannonList = []
        if side == 0:
            if self.leftBroadside and self.leftBroadsideConfig:
                cannonList = self.leftBroadside

        elif side == 1:
            if self.rightBroadside and self.rightBroadsideConfig:
                cannonList = self.rightBroadside

        spread = 1
        flightTime = 0
        if target and self.ship:
            dist = self.ship.getDistance(target)
            spread = max(0.5, dist / 1000.0)
            flightTime = dist / CannonGlobals.CLIENT_BROADSIDE_FIRE_VELOCITY

        broadsideMaxDelay = ShipGlobals.getBroadsideMaxDelay(self.ship.modelClass)
        targetShipVel = 0
        if target:
            fvel = target.smoother.getSmoothForwardVelocity()
            faxis = target.smoother.getForwardAxis()
            targetShipVel = faxis * fvel * (flightTime + broadsideMaxDelay / 2.0)

        if targetShipVel:
            targetPos = Vec3(targetPos[0] + targetShipVel[0], targetPos[1] + targetShipVel[1], targetPos[2] + targetShipVel[2])
            if __dev__ and config.GetBool('want-broadside-assist', 0):
                self.tracker.setPos(render, targetPos)

        delays = []
        hitPosList = []
        if side == 0:
            for i in range(len(self.leftBroadsideConfig)):
                if cannonList[i]:
                    delays.append(random.uniform(0, broadsideMaxDelay))
                    if target:
                        randX = random.gauss(0.0, 5.0 * spread)
                        randY = random.gauss(0.0, 5.0 * spread)
                        randZ = random.gauss(0.0, 3.0 * spread)
                        cannonPos = cannonList[i].locator.getPos(render)
                        diffX = shipPos[0] - cannonPos[0]
                        diffY = shipPos[1] - cannonPos[1]
                        hitPosList.append(((targetPos[0] - zonePos[0]) + randX - diffX, (targetPos[1] - zonePos[1]) + randY - diffY, (targetPos[2] - zonePos[2]) + randZ))
                    else:
                        hitPosList.append((100, 100, 100))
                else:
                    delays.append(0)
                    hitPosList.append((100, 100, 100))

        elif side == 1:
            for i in range(len(self.rightBroadsideConfig)):
                if cannonList[i]:
                    delays.append(random.uniform(0, broadsideMaxDelay))
                    if target:
                        randX = random.gauss(0.0, 5.0 * spread)
                        randY = random.gauss(0.0, 5.0 * spread)
                        randZ = random.gauss(0.0, 3.0 * spread)
                        cannonPos = cannonList[i].locator.getPos(render)
                        diffX = shipPos[0] - cannonPos[0]
                        diffY = shipPos[1] - cannonPos[1]
                        hitPosList.append(((targetPos[0] - zonePos[0]) + randX - diffX, (targetPos[1] - zonePos[1]) + randY - diffY, (targetPos[2] - zonePos[2]) + randZ))
                    else:
                        hitPosList.append((100, 100, 100))
                else:
                    delays.append(0)
                    hitPosList.append((100, 100, 100))

        delays[0] = 0.0
        if len(delays) > 4:
            delays[1] = 0.0

        random.shuffle(delays)
        self.doBroadside(side, delays, hitPosList, zoneId, flightTime, clientFire = 1)
        self.sendUpdate('requestBroadside', [
            side,
            delays,
            hitPosList,
            zoneId,
            flightTime])

    def doBroadside(self, side, delays, hitPosList, zoneId, flightTime, timestamp = None, clientFire = 0):
        if not clientFire:
            if self.localAvatarUsingWeapon:
                return

        if not (self.cr.activeWorld and self.cr.activeWorld.worldGrid):
            return

        if timestamp == None:
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)
        zonePos = self.cr.activeWorld.worldGrid.getZoneCellOrigin(zoneId)
        if side == 0:
            for i in self.leftPlayShots:
                i.pause()

            self.leftPlayShots = []
            for index in range(len(self.leftBroadside)):
                if self.leftBroadside[index]:
                    if not self.leftBroadside[index].isEnabled():
                        return

                    targetPos = 0
                    if index < len(hitPosList) and hitPosList[index] != (100, 100, 100):
                        tPos = hitPosList[index]
                        targetPos = Vec3(tPos[0] + zonePos[0], tPos[1] + zonePos[1], tPos[2] + zonePos[2])

                    delay = delays[index] if index < len(delays) else 0.0
                    playShot = Sequence(Wait(delay), Func(self.setCannonAnim, index, 0, 0), Wait(0.5), Func(self.__requestAttack, index, side, targetPos, flightTime), Wait(3.0), Func(self.setCannonAnim, index, 0, 1))
                    playShot.start(ts)
                    self.leftPlayShots.append(playShot)

        elif side == 1:
            for i in self.rightPlayShots:
                i.pause()

            self.rightPlayShots = []
            for index in range(len(self.rightBroadside)):
                if self.rightBroadside[index]:
                    if not self.rightBroadside[index].isEnabled():
                        return

                    targetPos = 0
                    if index < len(hitPosList) and hitPosList[index] != (100, 100, 100):
                        tPos = hitPosList[index]
                        targetPos = Vec3(tPos[0] + zonePos[0], tPos[1] + zonePos[1], tPos[2] + zonePos[2])

                    delay = delays[index] if index < len(delays) else 0.0
                    playShot = Sequence(Wait(delay), Func(self.setCannonAnim, index, 1, 0), Wait(0.5), Func(self.__requestAttack, index, side, targetPos, flightTime), Wait(3.0), Func(self.setCannonAnim, index, 1, 1))
                    playShot.start(ts)
                    self.rightPlayShots.append(playShot)

    def __requestAttack(self, index, side, targetPos, flightTime):
        if side == 0:
            if self.leftBroadside and self.leftBroadsideConfig:
                cannonList = self.leftBroadside
                cannonConfig = self.leftBroadsideConfig

            skillId = EnemySkills.LEFT_BROADSIDE
        elif side == 1:
            if self.rightBroadside and self.rightBroadsideConfig:
                cannonList = self.rightBroadside
                cannonConfig = self.rightBroadsideConfig

            skillId = EnemySkills.RIGHT_BROADSIDE

        ammoSkillId = self.ammoType
        if cannonList and cannonConfig:
            cannonList[index].playFire()
            cballSpawnPoint = cannonList[index].locator
            cballSpawnPoint.setP(render, 0)
            self.playFireEffect(cballSpawnPoint, ammoSkillId)
            if not WeaponGlobals.isProjectileSkill(skillId, ammoSkillId):
                return

            pos = cballSpawnPoint.getPos(render) + Vec3(0, -25, 0)
            if targetPos:
                self.playAttack(skillId, ammoSkillId, pos, targetPos = targetPos, flightTime = flightTime)
            else:
                m = cballSpawnPoint.getMat(self)
                power = WeaponGlobals.getAttackProjectilePower(ammoSkillId) * CannonGlobals.BROADSIDE_POWERMOD
                if side == 1:
                    startVel = m.xformVec(Vec3(0, -power, 90))
                else:
                    startVel = m.xformVec(Vec3(0, -power, 90))
                self.playAttack(skillId, ammoSkillId, pos, startVel)

    def getProjectile(self, skillId, projectileHitEvent, buffs):
        cannonball = CannonballProjectile(self.cr, skillId, projectileHitEvent, buffs)
        cannonball.reparentTo(render)
        return cannonball

    def playAttack(self, skillId, ammoSkillId, pos = 0, startVel = 0, targetPos = None, flightTime = 0):
        if not WeaponGlobals.isProjectileSkill(skillId, ammoSkillId):
            if self.localAvatarUsingWeapon:
                localAvatar.composeRequestTargetedSkill(skillId, ammoSkillId)

            return

        self.ammoSequence = self.ammoSequence + 1 & 255
        buffs = []
        if self.av:
            buffs = self.av.getSkillEffects()

        ammo = self.getProjectile(ammoSkillId, self.projectileHitEvent, buffs)
        ammo.setPos(pos)
        if skillId == EnemySkills.LEFT_BROADSIDE:
            ammo.setH(render, self.ship.getH(render) + 90)
        elif skillId == EnemySkills.RIGHT_BROADSIDE:
            ammo.setH(render, self.ship.getH(render) - 90)

        collNode = ammo.getCollNode()
        collNode.reparentTo(render)
        ammo.setTag('ammoSequence', str(self.ammoSequence))
        ammo.setTag('skillId', str(int(skillId)))
        ammo.setTag('ammoSkillId', str(int(ammoSkillId)))
        if self.av:
            ammo.setTag('attackerId', str(self.av.doId))

        startPos = pos
        endPlaneZ = -10
        if self.ship:
            ammo.setTag('shipId', str(self.ship.doId))
            self.shotNum += 1
            if self.shotNum > 100000:
                self.shotNum = 0

            ammo.setTag('shotNum', str(self.shotNum))
            self.baseVel = self.ship.worldVelocity

        if startPos[2] < endPlaneZ:
            self.notify.warning('bad startPos Z: %s' % startPos[2])
            return

        if targetPos is None:
            startVel += self.baseVel
            pi = ProjectileInterval(ammo, startPos = startPos, startVel = startVel, endZ = endPlaneZ, gravityMult = 2.0, collNode = collNode)
        elif self.ship.getNPCship():
            pi = ProjectileInterval(ammo, endZ = endPlaneZ, startPos = startPos, wayPoint = targetPos, timeToWayPoint = flightTime, gravityMult = 0.5, collNode = collNode)
        else:
            pi = ProjectileInterval(ammo, endZ = endPlaneZ, startPos = startPos, wayPoint = targetPos, timeToWayPoint = flightTime, gravityMult = 1.2, collNode = collNode)
        s = Parallel(Sequence(Wait(0.1), Func(base.cTrav.addCollider, collNode, ammo.collHandler)), Sequence(pi, Func(ammo.destroy), Func(base.cTrav.removeCollider, collNode)))
        ammo.setIval(s, start = True)

    def playFireEffect(self, spawnNode, ammoSkillId):
        if self.localAvatarUsingWeapon:
            boomSfx = random.choice(self.localFireSfx)
        else:
            boomSfx = random.choice(self.distFireSfx)
        base.playSfx(boomSfx, node = spawnNode, cutoff = 3000)
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
            cannonSmokeEffect = CannonBlastSmoke.getEffect()
            if cannonSmokeEffect:
                cannonSmokeEffect.reparentTo(self.effectNode)
                cannonSmokeEffect.particleDummy.reparentTo(self.effectNode)
                cannonSmokeEffect.setPosHpr(spawnNode, 0, -8, 0, 180, 0, 0)
                cannonSmokeEffect.particleDummy.setHpr(spawnNode, 180, 0, 0)
                cannonSmokeEffect.play()

        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
            flashEffect = MuzzleFlash.getEffect()
            if flashEffect:
                flashEffect.reparentTo(self.effectNode)
                flashEffect.flash.setScale(30)
                flashEffect.setPos(spawnNode, 0, 0, 0)
                flashEffect.startCol = Vec4(1, 1, 1, 1)
                flashEffect.fadeTime = 0.2
                flashEffect.play()

        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
            explosionEffect = ExplosionFlip.getEffect()
            if explosionEffect:
                explosionEffect.reparentTo(self.effectNode)
                pos = Vec3(0, -6, 0)
                explosionEffect.setPos(spawnNode, pos)
                explosionEffect.setScale(0.6)
                explosionEffect.play()

        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            muzzleFlameEffect = MuzzleFlame.getEffect()
            if muzzleFlameEffect:
                muzzleFlameEffect.reparentTo(self.effectNode)
                muzzleFlameEffect.particleDummy.reparentTo(self.effectNode)
                muzzleFlameEffect.flash.setScale(100)
                muzzleFlameEffect.startCol = Vec4(1, 1, 1, 1)
                muzzleFlameEffect.setPosHpr(spawnNode, 0, -8, 0, 180, 0, 0)
                muzzleFlameEffect.particleDummy.setHpr(spawnNode, 180, 0, 0)
                muzzleFlameEffect.play()

        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            if ammoSkillId == InventoryType.CannonGrapeShot:
                effect = GrapeshotEffect.getEffect()
                if effect:
                    effect.reparentTo(self.effectNode)
                    effect.setPosHpr(spawnNode, 0, 0, 0, -90, 0, 0)
                    effect.play()

    def getTrailTaskName(self):
        return self.uniqueName('cannonTrail')

    def b_setCannonAnim(self, index, side, anim, callback = None, extraArgs = []):
        self.setCannonAnim(index, side, anim, None, callback, extraArgs)
        self.d_setCannonAnim(index, side, anim)

    def d_setCannonAnim(self, index, side, anim):
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.sendUpdate('setCannonAnim', [
            index,
            side,
            anim,
            timestamp])

    def setCannonAnim(self, index, side, anim, timestamp = None, callback = None, extraArgs = []):
        if timestamp == None:
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)
        if side == 0:
            if anim == 0:
                self.leftBroadside[index].playOpen(ts)
            elif anim == 1:
                self.leftBroadside[index].playClosed(ts)

        elif side == 1:
            if anim == 0:
                self.rightBroadside[index].playOpen(ts)
            elif anim == 1:
                self.rightBroadside[index].playClosed(ts)

    def setCannonPortHitByProjectile(self, sideIndex, portIndex):
        if sideIndex == 0:
            self.leftBroadside[portIndex].setEnabled(0)
        elif sideIndex == 1:
            self.rightBroadside[portIndex].setEnabled(0)

        self.sendUpdate('requestCannonEnabledState', [
            sideIndex,
            portIndex,
            0])

    def setLeftBroadside(self, val):
        self.leftBroadsideConfig = val

    def setRightBroadside(self, val):
        self.rightBroadsideConfig = val

    def setLeftBroadsideEnabledState(self, state):
        self.leftBroadsideEnabledState = state
        for i in range(len(self.leftBroadside)):
            self.leftBroadside[i].setEnabled(state[i])

    def setRightBroadsideEnabledState(self, state):
        self.rightBroadsideEnabledState = state
        for i in range(len(self.rightBroadside)):
            self.rightBroadside[i].setEnabled(state[i])

    def setBaseTeam(self, val):
        self.baseTeam = val

    def setAmmoType(self, val):
        self.ammoType = val

    def setZoneLevel(self, level):
        pass

    def loadZoneLevel(self, level):
        pass

    def unloadZoneLevel(self, level):
        pass

    def addPropToShip(self):
        self.effectNode.reparentTo(self.ship.modelGeom)

    def completeCannonCheck(self):
        for colList in list(self.collisionLists.values()):
            colList.sort()
            ammo = colList[0][1].getFromNodePath().getPythonTag('ammo')
            if not ammo or ammo.destroyed:
                continue

            for entryData in colList:
                DistributedWeapon.projectileHitObject(self, entryData[1])
                if ammo.destroyed:
                    break

        self.collisionLists = {}
        self.listening = False

    def projectileHitObject(self, entry):
        shot = int(entry.getFromNodePath().getNetTag('shotNum'))
        if not self.collisionLists.get(shot):
            self.collisionLists[shot] = []

        y = entry.getSurfacePoint(entry.getIntoNodePath())[1]
        self.collisionLists[shot].append((y, entry))
        if not self.listening:
            self.listening = True
            self.acceptOnce('event-loop-done', self.completeCannonCheck)
