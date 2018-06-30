import random

from panda3d.core import *
from pirates.battle import CannonGlobals
from direct.actor import Actor
from direct.distributed.ClockDelta import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.interval.ProjectileInterval import *
from direct.showutil import Rope
from otp.otpbase import OTPGlobals
from pirates.battle import WeaponConstants, WeaponGlobals
from pirates.battle.CannonballProjectile import CannonballProjectile
from pirates.battle.WeaponGlobals import *
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.CannonBlastSmoke import CannonBlastSmoke
from pirates.effects.CannonMuzzleFire import CannonMuzzleFire
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.GrapeshotEffect import GrapeshotEffect
from pirates.effects.MuzzleFlame import MuzzleFlame
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesbase.PiratesGlobals import *
from pirates.ship import ShipGlobals
from pirates.shipparts import CannonDNA, ShipPart
from pirates.uberdog.UberDogGlobals import InventoryType

localFireSfxNames = [
    'cball_fire_1.mp3', 'cball_fire_2.mp3', 'cball_fire_3.mp3',
    'cball_fire_4.mp3', 'cball_fire_5.mp3'
]
distFireSfxNames = [
    'dist_cannon_01.mp3', 'dist_cannon_02.mp3', 'dist_cannon_03.mp3',
    'dist_cannon_04.mp3', 'dist_cannon_05.mp3', 'dist_cannon_06.mp3',
    'dist_cannon_07.mp3', 'dist_cannon_08.mp3', 'dist_cannon_09.mp3',
    'dist_cannon_10.mp3'
]


class Cannon(ShipPart.ShipPart, NodePath):

    notify = directNotify.newCategory('Cannon')
    localFireSfx = None
    distFireSfx = None

    def __init__(self, cr, shipCannon=False):
        ShipPart.ShipPart.__init__(self)
        NodePath.__init__(self, 'cannon')
        self.cr = cr
        self.flash = None
        self.collisionRadius = 4.0
        self.localAvatarUsingWeapon = 0
        self.ammoSequence = 0
        self.shotNum = 0
        self.baseVel = Vec3(0)
        self.shipH = 0
        self.oldShipH = 0
        self.currentHpr = (0, 0, 0)
        self.recoilIval = None
        self.ship = None
        self.av = None
        self.cannonPost = self
        self.propCollisions = NodePath(ModelNode('Cannon-collisions'))
        if not self.localFireSfx:
            Cannon.localFireSfx = []
            for filename in localFireSfxNames:
                audioPath = 'audio/'
                Cannon.localFireSfx.append(
                    base.loader.loadSfx('audio/' + filename))

            Cannon.distFireSfx = []
            for filename in distFireSfxNames:
                Cannon.distFireSfx.append(
                    base.loader.loadSfx('audio/' + filename))

        self.isShipCannon = shipCannon
        return

    def delete(self):
        del self.dna
        self.cannonPost = None
        if self.recoilIval:
            self.recoilIval.pause()
            self.recoilIval = None
        self.prop = None
        return

    def loadModel(self, dna):
        if config.GetBool('disable-ship-geom', 0):
            return
        self.dna = dna
        if self.dna:
            if self.dna.cannonType:
                filePrefix = CannonDNA.CannonDict.get(self.dna.cannonType)
            else:
                filePrefix = CannonDNA.CannonDict.get(InventoryType.CannonL1)
        else:
            filePrefix = CannonDNA.CannonDict.get(InventoryType.CannonL1)
        result, self.prop = ShipGlobals.getActor(filePrefix)
        self.geom_Low = self.prop.getLOD('low')
        self.geom_Medium = self.prop.getLOD('med')
        self.geom_High = self.prop.getLOD('hi')
        self.controls = {}
        self.setPivots()
        self.cannonExitPoint = self.pivot.attachNewNode('cannonExitPoint')
        self.cannonExitPoint.setY(4)
        self.island = None
        self.prop.setColorScale(1, 1, 1, 1, 1)
        self.loaded = True
        return

    def setPivots(self):
        cj1 = 0
        cj2 = 0
        for lodName in self.prop.getLODNames():
            if lodName == 'hi':
                cj1 = self.prop.controlJoint(None, 'modelRoot',
                                             'def_cannon_updown', lodName)
                cj2 = self.prop.controlJoint(None, 'modelRoot',
                                             'def_cannon_turn', lodName)
            else:
                self.prop.controlJoint(cj1, 'modelRoot', 'def_cannon_updown',
                                       lodName)
                self.prop.controlJoint(cj2, 'modelRoot', 'def_cannon_turn',
                                       lodName)

        self.pivot = cj1
        self.hNode = cj2
        self.pivot.reparentTo(self.hNode)
        self.prop.reparentTo(self)
        self.prop.loop('zero')
        self.recoilIval = self.pivot.scaleInterval(
            0.4, Vec3(1, 1, 1), startScale=Vec3(1, 0.7, 1), blendType='easeOut')
        return

    def unloadModel(self):
        if self.recoilIval:
            self.recoilIval.pause()
            self.recoilIval = None
        if self.prop:
            self.prop.removeNode()
            self.prop = None
        self.deleteCollisions()
        return

    def initializeCollisions(self):
        if config.GetBool('disable-ship-geom', 0):
            return
        self.coll = loader.loadModelCopy(
            'models/shipparts/cannon_zero_collisions')
        self.coll.reparentTo(self.propCollisions)

    def deleteCollisions(self):
        self.propCollisions.removeNode()

    def setupShaders(self):
        pass

    def enableShaders(self):
        pass

    def disableShaders(self):
        pass

    def playFireEffect(self, ammoSkillId=0, buffs=[]):
        if self.localAvatarUsingWeapon:
            boomSfx = random.choice(self.localFireSfx)
        else:
            boomSfx = random.choice(self.distFireSfx)
        base.playSfx(boomSfx, node=self.pivot, cutoff=3500)
        if self.ship:
            effectParent = self.ship.root
            relativeNode = self.cannonExitPoint
        else:
            effectParent = self.prop
            relativeNode = self.cannonExitPoint
        effectH = self.hNode.getH(effectParent)
        effectP = self.pivot.getP(effectParent)
        if self.localAvatarUsingWeapon:
            if base.options.getSpecialEffectsSetting(
            ) >= base.options.SpecialEffectsLow:
                muzzleFlameEffect = MuzzleFlame.getEffect()
                if muzzleFlameEffect:
                    muzzleFlameEffect.reparentTo(effectParent)
                    muzzleFlameEffect.particleDummy.reparentTo(effectParent)
                    muzzleFlameEffect.flash.setScale(18)
                    muzzleFlameEffect.setHpr(effectParent, effectH, effectP, 0)
                    muzzleFlameEffect.particleDummy.setHpr(
                        effectParent, effectH, effectP, 0)
                    muzzleFlameEffect.setPos(relativeNode.getPos(effectParent))
                    muzzleFlameEffect.play()
            if self.recoilIval:
                self.recoilIval.pause()
                self.recoilIval.start()
        else:
            if base.options.getSpecialEffectsSetting(
            ) >= base.options.SpecialEffectsMedium:
                cannonSmokeEffect = CannonBlastSmoke.getEffect()
                if cannonSmokeEffect:
                    cannonSmokeEffect.reparentTo(effectParent)
                    cannonSmokeEffect.particleDummy.reparentTo(effectParent)
                    cannonSmokeEffect.setHpr(effectParent, effectH, effectP, 0)
                    cannonSmokeEffect.particleDummy.setHpr(
                        effectParent, effectH, effectP, 0)
                    cannonSmokeEffect.setPos(relativeNode.getPos(effectParent))
                    cannonSmokeEffect.play()
            if base.options.getSpecialEffectsSetting(
            ) >= base.options.SpecialEffectsHigh:
                explosionEffect = ExplosionFlip.getEffect()
                if explosionEffect:
                    explosionEffect.reparentTo(effectParent)
                    explosionEffect.setScale(0.35)
                    explosionEffect.setHpr(effectParent, effectH, effectP, 0)
                    explosionEffect.setPos(relativeNode.getPos(effectParent))
                    explosionEffect.play()
            if base.options.getSpecialEffectsSetting(
            ) >= base.options.SpecialEffectsLow:
                muzzleFlameEffect = MuzzleFlame.getEffect()
                if muzzleFlameEffect:
                    muzzleFlameEffect.reparentTo(effectParent)
                    muzzleFlameEffect.particleDummy.reparentTo(effectParent)
                    muzzleFlameEffect.flash.setScale(45)
                    muzzleFlameEffect.setHpr(effectParent, effectH, effectP, 0)
                    muzzleFlameEffect.particleDummy.setHpr(
                        effectParent, effectH, effectP, 0)
                    muzzleFlameEffect.particleDummy.setPos(
                        relativeNode.getPos(effectParent))
                    muzzleFlameEffect.setPos(relativeNode.getPos(effectParent))
                    muzzleFlameEffect.play()
        if base.options.getSpecialEffectsSetting(
        ) >= base.options.SpecialEffectsHigh:
            if WeaponConstants.C_OPENFIRE in buffs:
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.reparentTo(effectParent)
                cameraShakerEffect.shakeSpeed = 0.03
                cameraShakerEffect.shakePower = 0.7
                cameraShakerEffect.numShakes = 1
                cameraShakerEffect.play(10.0)
        if ammoSkillId == InventoryType.CannonGrapeShot:
            if base.options.getSpecialEffectsSetting(
            ) >= base.options.SpecialEffectsLow:
                effect = GrapeshotEffect.getEffect()
                if effect:
                    effect.reparentTo(effectParent)
                    effect.setHpr(effectParent, effectH, effectP, 0)
                    effect.setPos(relativeNode.getPos(effectParent))
                    effect.play()

    def getProjectile(self, ammoSkillId, projectileHitEvent, buffs=[]):
        cannonball = CannonballProjectile(self.cr, ammoSkillId,
                                          projectileHitEvent, buffs)
        cannonball.reparentTo(render)
        cannonball.setHpr(self.hNode.getH(render), self.hNode.getP(render), 0)
        return cannonball

    def getRope(self, thickness=0.15):
        rope = Rope.Rope()
        rope.ropeNode.setRenderMode(RopeNode.RMTube)
        rope.ropeNode.setNumSlices(10)
        rope.ropeNode.setUvMode(RopeNode.UVDistance)
        rope.ropeNode.setUvDirection(1)
        rope.ropeNode.setUvScale(0.25)
        rope.ropeNode.setThickness(thickness)
        ropePile = loader.loadModel('models/char/rope_high')
        ropeTex = ropePile.findTexture('rope_single_omit')
        ropePile.removeNode()
        rope.setTexture(ropeTex)
        return rope

    def playAttack(self,
                   skillId,
                   ammoSkillId,
                   projectileHitEvent,
                   targetPos=None,
                   wantCollisions=0,
                   flightTime=None,
                   preciseHit=False,
                   buffs=[],
                   timestamp=None):
        if base.cr.wantSpecialEffects != 0:
            self.playFireEffect(ammoSkillId, buffs)
        if not WeaponGlobals.isProjectileSkill(skillId, ammoSkillId):
            if self.localAvatarUsingWeapon:
                localAvatar.composeRequestTargetedSkill(skillId, ammoSkillId)
            return
        wantCollisions = 1
        self.ammoSequence = self.ammoSequence + 1 & 255
        ammo = self.getProjectile(ammoSkillId, projectileHitEvent, buffs)
        collNode = None
        if self.localAvatarUsingWeapon or wantCollisions:
            collNode = ammo.getCollNode()
            collNode.reparentTo(render)
        self.shotNum += 1
        if self.shotNum > 100000:
            self.shotNum = 0
        ammo.setTag('shotNum', str(self.shotNum))
        ammo.setTag('ammoSequence', str(self.ammoSequence))
        ammo.setTag('skillId', str(int(skillId)))
        ammo.setTag('ammoSkillId', str(int(ammoSkillId)))
        if self.av:
            ammo.setTag('attackerId', str(self.av.doId))
        if hasattr(self, 'fortId'):
            ammo.setTag('fortId', str(self.fortId))
        if hasattr(self, 'ship') and self.ship and hasattr(self.ship, 'doId'):
            setShipTag = True
            if setShipTag:
                ammo.setTag('shipId', str(self.ship.doId))
        startPos = self.cannonExitPoint.getPos(render)
        ammo.setPos(startPos)
        ammo.setH(self.hNode.getH(render))
        ammo.setP(self.pivot.getP(render))
        endPlaneZ = -100
        if startPos[2] < endPlaneZ:
            self.notify.warning('bad startPos Z: %s' % startPos[2])
            return
        m = ammo.getMat(render)
        curPower = WeaponGlobals.getAttackProjectilePower(skillId,
                                                          ammoSkillId) * 0.6
        if targetPos is None:
            startVel = m.xformVec(Vec3(0, curPower, 0))
            if self.ship:
                fvel = self.ship.smoother.getSmoothForwardVelocity() * 0.5
                faxis = self.ship.smoother.getForwardAxis()
                self.baseVel = faxis * fvel
                startVel += self.baseVel
        else:
            startVel = m.xformVec(Vec3(0, 20, 2))

        def attachRope():
            if ammoSkillId == InventoryType.CannonGrappleHook and self.cannonPost:
                rope = self.getRope()
                rope.reparentTo(ammo)
                rope.setup(3, ((None, Point3(0, 0, 0)),
                               (self.cannonPost, Point3(2, 5, 10)),
                               (self.cannonPost, Point3(2, 0, 0))))
            return

        if preciseHit:
            if flightTime is None:
                flightTime = CannonGlobals.AI_FIRE_TIME
            pi = ProjectileInterval(
                ammo,
                startPos=startPos,
                endPos=targetPos,
                duration=flightTime,
                collNode=collNode)
        else:
            if targetPos:
                if flightTime is None:
                    flightTime = CannonGlobals.getCannonballFlightTime(
                        startPos, targetPos, curPower)
                pi = ProjectileInterval(
                    ammo,
                    endZ=endPlaneZ,
                    startPos=startPos,
                    wayPoint=targetPos,
                    timeToWayPoint=flightTime,
                    gravityMult=2.5,
                    collNode=collNode)
            else:
                pi = ProjectileInterval(
                    ammo,
                    startPos=startPos,
                    startVel=startVel,
                    endZ=endPlaneZ,
                    gravityMult=4.0,
                    collNode=collNode)
        if self.localAvatarUsingWeapon or wantCollisions:
            s = Sequence(
                Func(base.cTrav.addCollider, collNode, ammo.collHandler),
                Func(attachRope), pi, Func(ammo.destroy),
                Func(base.cTrav.removeCollider, collNode))
        else:
            s = Sequence(Func(attachRope), pi, Func(ammo.destroy))
        ts = 0
        if timestamp:
            ts = globalClockDelta.localElapsedTime(timestamp)
        ammo.setIval(s, start=True, offset=ts)
        return

    def setLocalAvatarUsingWeapon(self, val):
        self.localAvatarUsingWeapon = val
