# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.ProjectileEffect
import random

from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.CannonExplosion import CannonExplosion
from pirates.effects.CannonSplash import CannonSplash
from pirates.effects.CurseHit import CurseHit
from pirates.effects.DirtClod import DirtClod
from pirates.effects.DrainLife import DrainLife
from pirates.effects.DustCloud import DustCloud
from pirates.effects.DustRing import DustRing
from pirates.effects.Explosion import Explosion
from pirates.effects.ExplosionCloud import ExplosionCloud
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.ExplosionTip import ExplosionTip
from pirates.effects.FadingSigil import FadingSigil
from pirates.effects.Fire import Fire
from pirates.effects.FireballHit import FireballHit
from pirates.effects.FireTrail import FireTrail
from pirates.effects.FlamingDebris import FlamingDebris
from pirates.effects.FlashStar import FlashStar
from pirates.effects.GreenBlood import GreenBlood
from pirates.effects.HitFlashA import HitFlashA
from pirates.effects.LightningStrike import LightningStrike
from pirates.effects.LightSmoke import LightSmoke
from pirates.effects.MuzzleFlame import MuzzleFlame
from pirates.effects.MuzzleFlash import MuzzleFlash
from pirates.effects.PoisonHit import PoisonHit
from pirates.effects.RockDebris import RockDebris
from pirates.effects.RockShower import RockShower
from pirates.effects.ShipDebris import ShipDebris
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.ShockwaveHit import ShockwaveHit
from pirates.effects.ShockwaveRing import ShockwaveRing
from pirates.effects.SmokeBomb import SmokeBomb
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.SmokePillar import SmokePillar
from pirates.effects.Sparks import Sparks
from pirates.effects.SpectralSmoke import SpectralSmoke
from pirates.effects.VoodooSmoke import VoodooSmoke
from pirates.effects.WaspCloud import WaspCloud
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

skillSfxs = None

def getSkillSfx():
    global skillSfxs
    if not skillSfxs:
        skillSfxs = {InventoryType.GrenadeExplosion: loader.loadSfx('audio/sfx_grenade_impact.mp3'), InventoryType.GrenadeShockBomb: loader.loadSfx('audio/sfx_grenade_impact_stink_pot.mp3'), InventoryType.GrenadeFireBomb: loader.loadSfx('audio/sfx_grenade_impact_firebomb_explo.mp3'), InventoryType.GrenadeSmokeCloud: loader.loadSfx('audio/sfx_grenade_impact_smoke.mp3'), InventoryType.GrenadeSiege: loader.loadSfx('audio/sfx_grenade_impact.mp3')}


class ProjectileEffect:
    
    notify = DirectNotifyGlobal.directNotify.newCategory('ProjectileEffect')

    def __init__(self, cr, attackerId, hitObject, objType, pos, skillId, ammoSkillId, normal=None):
        self.cr = cr
        self.attackerId = attackerId
        self.normal = normal
        getSkillSfx()
        from pirates.ship.DistributedShip import DistributedShip
        from pirates.shipparts.DistributedShippart import DistributedShippart
        from pirates.battle.DistributedBattleAvatar import DistributedBattleAvatar
        from pirates.world.DistributedIsland import DistributedIsland
        self.projVelocity = (
         (25, 0), (0, 25), (-25, 0), (0, -25))
        if not objType:
            if isinstance(hitObject, DistributedShip):
                objType = PiratesGlobals.COLL_SHIPPART
            elif isinstance(hitObject, DistributedShippart):
                objType = PiratesGlobals.COLL_SHIPPART
            elif isinstance(hitObject, DistributedBattleAvatar):
                objType = PiratesGlobals.COLL_AV
            elif isinstance(hitObject, DistributedIsland):
                objType = PiratesGlobals.COLL_LAND
            else:
                self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)
                return
        if objType == PiratesGlobals.COLL_AV:
            self.avatarHitEffect(hitObject, pos, skillId, ammoSkillId)
        else:
            if objType == PiratesGlobals.COLL_MONSTER:
                self.monsterHitEffect(hitObject, pos, skillId, ammoSkillId)
            else:
                if objType == PiratesGlobals.COLL_DESTRUCTIBLE:
                    self.propHitEffect(hitObject, pos, skillId, ammoSkillId)
                else:
                    if objType == PiratesGlobals.COLL_SHIPPART:
                        self.propHitEffect(hitObject, pos, skillId, ammoSkillId)
                    else:
                        if objType == PiratesGlobals.COLL_SEA:
                            self.waterHitEffect(hitObject, pos, skillId, ammoSkillId)
                        else:
                            if objType == PiratesGlobals.COLL_LAND:
                                self.groundHitEffect(hitObject, pos, skillId, ammoSkillId)
                            else:
                                if objType == PiratesGlobals.COLL_BLOCKER:
                                    self.blockerHitEffect(hitObject, pos, skillId, ammoSkillId)
                                else:
                                    if objType == PiratesGlobals.COLL_BLDG:
                                        self.buildingHitEffect(hitObject, pos, skillId, ammoSkillId)
                                    else:
                                        if objType == PiratesGlobals.COLL_GRAPPLE_TARGET:
                                            self.grappleHitEffect(hitObject, pos, skillId, ammoSkillId)
                                        else:
                                            if objType == PiratesGlobals.COLL_CANNON:
                                                self.cannonHitEffect(hitObject, pos, skillId, ammoSkillId)
                                            else:
                                                if objType == PiratesGlobals.COLL_FORT:
                                                    self.fortHitEffect(hitObject, pos, skillId, ammoSkillId)
                                                else:
                                                    self.notify.warning('playEffect: unknown objType: %s' % objType)

    def playSfx(self, ammoSkillId, node, startTime=0):
        sfx = skillSfxs.get(ammoSkillId)
        if sfx:
            base.playSfx(sfx, node=node, time=startTime, cutoff=400)

    def basicHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        from pirates.battle import WeaponGlobals
        attacker = self.cr.doId2do.get(self.attackerId)
        aoeRadius = self.cr.battleMgr.getModifiedAttackAreaRadius(attacker, skillId, ammoSkillId)
        if config.GetBool('show-aoe-radius', 0):
            s = loader.loadModelCopy('models/misc/smiley')
            s.reparentTo(render)
            s.setPos(hitObject, pos)
            s.setScale(aoeRadius)
            s.setTransparency(1)
            s.setColorScale(1.0, 0.5, 0.5, 0.4)
        if ammoSkillId == InventoryType.CannonRoundShot or ammoSkillId == InventoryType.CannonChainShot or ammoSkillId == InventoryType.CannonBullet or ammoSkillId == InventoryType.CannonSkull or ammoSkillId == InventoryType.CannonBarShot or ammoSkillId == InventoryType.CannonFury:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                explosionEffect = ExplosionFlip.getEffect()
                if explosionEffect:
                    explosionEffect.reparentTo(base.effectsRoot)
                    explosionEffect.setPos(hitObject, pos)
                    explosionEffect.setScale(0.8)
                    explosionEffect.play()
                shipSplintersAEffect = ShipSplintersA.getEffect()
                if shipSplintersAEffect:
                    shipSplintersAEffect.reparentTo(hitObject)
                    shipSplintersAEffect.setPos(hitObject, pos)
                    shipSplintersAEffect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                smokeCloudEffect = SmokeCloud.getEffect()
                if smokeCloudEffect:
                    smokeCloudEffect.reparentTo(hitObject)
                    smokeCloudEffect.setPos(hitObject, pos)
                    smokeCloudEffect.setScale(1.0)
                    smokeCloudEffect.spriteScale = 1.0
                    smokeCloudEffect.radius = 7.0
                    smokeCloudEffect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                shockwaveRingEffect = ShockwaveRing.getEffect()
                if shockwaveRingEffect:
                    shockwaveRingEffect.wrtReparentTo(base.effectsRoot)
                    if self.normal:
                        shockwaveRingEffect.lookAt(shockwaveRingEffect.getPos() + self.normal)
                    shockwaveRingEffect.setPos(hitObject, pos)
                    shockwaveRingEffect.size = aoeRadius * 4
                    shockwaveRingEffect.play()
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.wrtReparentTo(hitObject)
                cameraShakerEffect.setPos(hitObject, pos)
                cameraShakerEffect.shakeSpeed = 0.04
                cameraShakerEffect.shakePower = 6.0
                cameraShakerEffect.numShakes = 2
                cameraShakerEffect.scalePower = 1
                cameraShakerEffect.play(120.0)
        else:
            if ammoSkillId == InventoryType.CannonFirebrand or ammoSkillId == InventoryType.CannonFlamingSkull:
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    explosionEffect = ExplosionFlip.getEffect()
                    if explosionEffect:
                        explosionEffect.wrtReparentTo(base.effectsRoot)
                        explosionEffect.setPos(hitObject, pos)
                        explosionEffect.setScale(0.8)
                        explosionEffect.play()
                    shipSplintersAEffect = ShipSplintersA.getEffect()
                    if shipSplintersAEffect:
                        shipSplintersAEffect.wrtReparentTo(hitObject)
                        shipSplintersAEffect.setPos(hitObject, pos)
                        shipSplintersAEffect.play()
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                    smokeCloudEffect = SmokeCloud.getEffect()
                    if smokeCloudEffect:
                        smokeCloudEffect.wrtReparentTo(hitObject)
                        smokeCloudEffect.setPos(hitObject, pos)
                        smokeCloudEffect.setScale(1.0)
                        smokeCloudEffect.spriteScale = 1.0
                        smokeCloudEffect.radius = 7.0
                        smokeCloudEffect.play()
                    cameraShakerEffect = CameraShaker()
                    cameraShakerEffect.wrtReparentTo(hitObject)
                    cameraShakerEffect.setPos(hitObject, pos)
                    cameraShakerEffect.shakeSpeed = 0.04
                    cameraShakerEffect.shakePower = 6.0
                    cameraShakerEffect.numShakes = 2
                    cameraShakerEffect.scalePower = 1
                    cameraShakerEffect.play(100.0)
            else:
                if ammoSkillId == InventoryType.CannonExplosive:
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                        effect = Explosion.getEffect()
                        if effect:
                            effect.wrtReparentTo(hitObject)
                            effect.setPos(hitObject, pos)
                            effect.effectScale = 1.0
                            effect.radius = aoeRadius / 1.5
                            effect.play()
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                        dustRingEffect = DustRing.getEffect()
                        if dustRingEffect:
                            dustRingEffect.wrtReparentTo(hitObject)
                            dustRingEffect.setPos(hitObject, pos)
                            dustRingEffect.play()
                        for i in range(2):
                            effect = FlamingDebris.getEffect()
                            if effect:
                                effect.wrtReparentTo(base.effectsRoot)
                                effect.setPos(hitObject, pos)
                                effect.duration = 4
                                effect.velocityX = self.projVelocity[i][0]
                                effect.velocityY = self.projVelocity[i][1]
                                effect.play()

                        shipSplintersAEffect = ShipSplintersA.getEffect()
                        if shipSplintersAEffect:
                            shipSplintersAEffect.wrtReparentTo(hitObject)
                            shipSplintersAEffect.setPos(hitObject, pos)
                            shipSplintersAEffect.play()
                        smokeCloudEffect = SmokeCloud.getEffect()
                        if smokeCloudEffect:
                            smokeCloudEffect.wrtReparentTo(hitObject)
                            smokeCloudEffect.setPos(hitObject, pos)
                            smokeCloudEffect.setScale(3.0)
                            smokeCloudEffect.spriteScale = 4.0
                            smokeCloudEffect.radius = aoeRadius / 1.5
                            smokeCloudEffect.play()
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                        for i in range(2):
                            effect = FlamingDebris.getEffect()
                            if effect:
                                effect.wrtReparentTo(base.effectsRoot)
                                effect.setPos(hitObject, pos)
                                effect.duration = 4
                                effect.velocityX = self.projVelocity[i][0]
                                effect.velocityY = self.projVelocity[i][1]
                                effect.play()

                        shockwaveRingEffect = ShockwaveRing.getEffect()
                        if shockwaveRingEffect:
                            shockwaveRingEffect.wrtReparentTo(base.effectsRoot)
                            shockwaveRingEffect.setPos(hitObject, pos)
                            shockwaveRingEffect.size = aoeRadius * 4
                            shockwaveRingEffect.play()
                        cameraShakerEffect = CameraShaker()
                        cameraShakerEffect.wrtReparentTo(hitObject)
                        cameraShakerEffect.setPos(hitObject, pos)
                        cameraShakerEffect.shakeSpeed = 0.04
                        cameraShakerEffect.shakePower = 6.0
                        cameraShakerEffect.numShakes = 2
                        cameraShakerEffect.scalePower = 1
                        cameraShakerEffect.play(300.0)
                else:
                    if ammoSkillId == InventoryType.CannonThunderbolt:
                        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                            shockwaveRingEffect = ShockwaveRing.getEffect()
                            if shockwaveRingEffect:
                                shockwaveRingEffect.wrtReparentTo(base.effectsRoot)
                                shockwaveRingEffect.setPos(hitObject, pos)
                                shockwaveRingEffect.size = aoeRadius * 4
                                shockwaveRingEffect.play()
                            shipSplintersAEffect = ShipSplintersA.getEffect()
                            if shipSplintersAEffect:
                                shipSplintersAEffect.wrtReparentTo(hitObject)
                                shipSplintersAEffect.setPos(hitObject, pos)
                                shipSplintersAEffect.play()
                        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                            flashEffect = MuzzleFlash.getEffect()
                            if flashEffect:
                                flashEffect.wrtReparentTo(base.effectsRoot)
                                flashEffect.flash.setScale(3000)
                                flashEffect.setPos(hitObject, pos)
                                flashEffect.setZ(hitObject, 100)
                                flashEffect.startCol = Vec4(0.5, 0.8, 1, 1)
                                flashEffect.fadeTime = 0.2
                                flashEffect.play()
                            cameraShakerEffect = CameraShaker()
                            cameraShakerEffect.wrtReparentTo(hitObject)
                            cameraShakerEffect.setPos(hitObject, pos)
                            cameraShakerEffect.shakeSpeed = 0.06
                            cameraShakerEffect.shakePower = 4.0
                            cameraShakerEffect.numShakes = 2
                            cameraShakerEffect.scalePower = 1
                            cameraShakerEffect.play(300.0)
                        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                            smokeCloudEffect = SmokeCloud.getEffect()
                            if smokeCloudEffect:
                                smokeCloudEffect.wrtReparentTo(hitObject)
                                smokeCloudEffect.setPos(hitObject, pos)
                                smokeCloudEffect.setScale(1.0)
                                smokeCloudEffect.spriteScale = 1.0
                                smokeCloudEffect.radius = 7.0
                                smokeCloudEffect.play()
                            effect = LightningStrike.getEffect()
                            if effect:
                                effect.wrtReparentTo(base.effectsRoot)
                                effect.setPos(hitObject, pos)
                                effect.play()
                    else:
                        if ammoSkillId == InventoryType.GrenadeExplosion:
                            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                                explosionEffect = ExplosionFlip.getEffect()
                                if explosionEffect:
                                    explosionEffect.reparentTo(base.effectsRoot)
                                    explosionEffect.setPos(hitObject, pos)
                                    explosionEffect.setScale(1.0)
                                    explosionEffect.play()
                                    self.playSfx(ammoSkillId, explosionEffect)
                                if base.launcher.getPhaseComplete(3):
                                    for i in range(random.randint(2, 4)):
                                        debrisEffect = RockDebris.getEffect()
                                        if debrisEffect:
                                            debrisEffect.reparentTo(base.effectsRoot)
                                            debrisEffect.setPos(hitObject, pos)
                                            debrisEffect.offsetEndPlaneZFrom(hitObject.getZ())
                                            debrisEffect.debris.setScale(0.4)
                                            debrisEffect.radiusDist = 20
                                            debrisEffect.minHeight = 30
                                            debrisEffect.maxHeight = 100
                                            if debrisEffect.testTrajectory():
                                                debrisEffect.play()
                                            else:
                                                debrisEffect.cleanUpEffect()

                                flashEffect = MuzzleFlash.getEffect()
                                if flashEffect:
                                    flashEffect.reparentTo(base.effectsRoot)
                                    flashEffect.flash.setScale(100)
                                    flashEffect.setPos(hitObject, pos)
                                    flashEffect.startCol = Vec4(0.7, 0.7, 0.7, 1)
                                    flashEffect.fadeTime = 0.2
                                    flashEffect.play()
                            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                                shipSplintersAEffect = ShipSplintersA.getEffect()
                                if shipSplintersAEffect:
                                    shipSplintersAEffect.reparentTo(hitObject)
                                    shipSplintersAEffect.setPos(hitObject, pos)
                                    shipSplintersAEffect.play()
                                shockwaveRingEffect = ShockwaveRing.getEffect()
                                if shockwaveRingEffect:
                                    shockwaveRingEffect.reparentTo(base.effectsRoot)
                                    shockwaveRingEffect.setPos(hitObject, pos)
                                    shockwaveRingEffect.size = aoeRadius * 4
                                    shockwaveRingEffect.play()
                                cameraShakerEffect = CameraShaker()
                                cameraShakerEffect.reparentTo(hitObject)
                                cameraShakerEffect.setPos(hitObject, pos)
                                cameraShakerEffect.shakeSpeed = 0.04
                                cameraShakerEffect.shakePower = 6.0
                                cameraShakerEffect.numShakes = 2
                                cameraShakerEffect.scalePower = 1
                                cameraShakerEffect.play(80.0)
                            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                                smokeCloudEffect = SmokeCloud.getEffect()
                                if smokeCloudEffect:
                                    smokeCloudEffect.reparentTo(hitObject)
                                    smokeCloudEffect.setPos(hitObject, pos)
                                    smokeCloudEffect.setScale(1.0)
                                    smokeCloudEffect.spriteScale = 1.0
                                    smokeCloudEffect.radius = 7.0
                                    smokeCloudEffect.play()
                        else:
                            if ammoSkillId == InventoryType.GrenadeShockBomb:
                                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                                    explosionEffect = ExplosionFlip.getEffect()
                                    if explosionEffect:
                                        explosionEffect.reparentTo(base.effectsRoot)
                                        explosionEffect.setPos(hitObject, pos)
                                        explosionEffect.setScale(1.0)
                                        explosionEffect.play()
                                        self.playSfx(ammoSkillId, explosionEffect)
                                    flashEffect = MuzzleFlash.getEffect()
                                    if flashEffect:
                                        flashEffect.reparentTo(base.effectsRoot)
                                        flashEffect.flash.setScale(100)
                                        flashEffect.setPos(hitObject, pos)
                                        flashEffect.startCol = Vec4(0.7, 0.7, 0.7, 1)
                                        flashEffect.fadeTime = 0.2
                                        flashEffect.play()
                                    cameraShakerEffect = CameraShaker()
                                    cameraShakerEffect.reparentTo(hitObject)
                                    cameraShakerEffect.setPos(hitObject, pos)
                                    cameraShakerEffect.shakeSpeed = 0.04
                                    cameraShakerEffect.shakePower = 3.0
                                    cameraShakerEffect.numShakes = 2
                                    cameraShakerEffect.scalePower = 1
                                    cameraShakerEffect.play(80.0)
                                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                                    smokeCloudEffect = SmokeCloud.getEffect()
                                    if smokeCloudEffect:
                                        smokeCloudEffect.reparentTo(hitObject)
                                        smokeCloudEffect.setPos(hitObject, pos)
                                        smokeCloudEffect.setScale(1.0)
                                        smokeCloudEffect.spriteScale = 1.0
                                        smokeCloudEffect.radius = 7.0
                                        smokeCloudEffect.play()
                                    shockwaveRingEffect = ShockwaveRing.getEffect()
                                    if shockwaveRingEffect:
                                        shockwaveRingEffect.reparentTo(base.effectsRoot)
                                        shockwaveRingEffect.setPos(hitObject, pos)
                                        shockwaveRingEffect.size = aoeRadius * 4
                                        shockwaveRingEffect.play()
                                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                                    dustRingEffect = DustRing.getEffect()
                                    if dustRingEffect:
                                        dustRingEffect.reparentTo(hitObject)
                                        dustRingEffect.setPos(hitObject, pos)
                                        dustRingEffect.play()
                            else:
                                if ammoSkillId == InventoryType.GrenadeSiege:
                                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                                        smokePillarEffect = SmokePillar.getEffect()
                                        if smokePillarEffect:
                                            smokePillarEffect.reparentTo(hitObject)
                                            smokePillarEffect.setPos(hitObject, pos)
                                            smokePillarEffect.setScale(1.0)
                                            smokePillarEffect.spriteScale = 1.0
                                            smokePillarEffect.radius = 7.0
                                            smokePillarEffect.play()
                                        shockwaveRingEffect = ShockwaveRing.getEffect()
                                        if shockwaveRingEffect:
                                            shockwaveRingEffect.reparentTo(base.effectsRoot)
                                            shockwaveRingEffect.setPos(hitObject, pos)
                                            shockwaveRingEffect.size = aoeRadius * 4
                                            shockwaveRingEffect.play()
                                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                                        shipSplintersAEffect = ShipSplintersA.getEffect()
                                        if shipSplintersAEffect:
                                            shipSplintersAEffect.reparentTo(hitObject)
                                            shipSplintersAEffect.setPos(hitObject, pos)
                                            shipSplintersAEffect.play()
                                        explosionEffect = ExplosionFlip.getEffect()
                                        if explosionEffect:
                                            explosionEffect.reparentTo(base.effectsRoot)
                                            explosionEffect.setPos(hitObject, pos)
                                            explosionEffect.setScale(2.0)
                                            explosionEffect.play()
                                            self.playSfx(ammoSkillId, explosionEffect)
                                        for i in range(random.randint(3, 6)):
                                            debrisEffect = RockDebris.getEffect()
                                            if debrisEffect:
                                                debrisEffect.reparentTo(base.effectsRoot)
                                                debrisEffect.setPos(hitObject, pos)
                                                debrisEffect.offsetEndPlaneZFrom(hitObject.getZ())
                                                debrisEffect.debris.setScale(0.8)
                                                debrisEffect.radiusDist = 30
                                                debrisEffect.minHeight = 30
                                                debrisEffect.maxHeight = 120
                                                if debrisEffect.testTrajectory():
                                                    debrisEffect.play()
                                                else:
                                                    debrisEffect.cleanUpEffect()

                                        flashEffect = MuzzleFlash.getEffect()
                                        if flashEffect:
                                            flashEffect.reparentTo(base.effectsRoot)
                                            flashEffect.flash.setScale(200)
                                            flashEffect.setPos(hitObject, pos)
                                            flashEffect.startCol = Vec4(0.7, 0.7, 0.7, 1)
                                            flashEffect.fadeTime = 0.2
                                            flashEffect.play()
                                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                                        dustRingEffect = DustRing.getEffect()
                                        if dustRingEffect:
                                            dustRingEffect.reparentTo(hitObject)
                                            dustRingEffect.setPos(hitObject, pos)
                                            dustRingEffect.play()
                                        cameraShakerEffect = CameraShaker()
                                        cameraShakerEffect.wrtReparentTo(hitObject)
                                        cameraShakerEffect.setPos(hitObject, pos)
                                        cameraShakerEffect.shakeSpeed = 0.06
                                        cameraShakerEffect.shakePower = 4.0
                                        cameraShakerEffect.numShakes = 2
                                        cameraShakerEffect.scalePower = 1
                                        cameraShakerEffect.play(80.0)
                                else:
                                    if ammoSkillId == InventoryType.GrenadeFireBomb:
                                        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                                            flashEffect = MuzzleFlash.getEffect()
                                            if flashEffect:
                                                flashEffect.wrtReparentTo(base.effectsRoot)
                                                flashEffect.flash.setScale(100)
                                                flashEffect.setPos(hitObject, pos)
                                                flashEffect.startCol = Vec4(0.7, 0.7, 0.7, 1)
                                                flashEffect.fadeTime = 0.2
                                                flashEffect.play()
                                                self.playSfx(ammoSkillId, flashEffect)
                                            shockwaveRingEffect = ShockwaveRing.getEffect()
                                            if shockwaveRingEffect:
                                                shockwaveRingEffect.wrtReparentTo(base.effectsRoot)
                                                shockwaveRingEffect.setPos(hitObject, pos)
                                                shockwaveRingEffect.size = aoeRadius * 4
                                                shockwaveRingEffect.play()
                                        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                                            fireEffect = Fire.getEffect()
                                            if fireEffect:
                                                fireEffect.wrtReparentTo(base.effectsRoot)
                                                fireEffect.setPos(hitObject, pos + Vec3(0, 0, -0.5))
                                                fireEffect.effectScale = 0.5
                                                fireEffect.duration = 2.5
                                                fireEffect.play()
                                        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                                            blackSmokeEffect = LightSmoke.getEffect()
                                            if blackSmokeEffect:
                                                blackSmokeEffect.wrtReparentTo(base.effectsRoot)
                                                blackSmokeEffect.setPos(hitObject, pos)
                                                blackSmokeEffect.duration = 4.0
                                                blackSmokeEffect.play()
                                            cameraShakerEffect = CameraShaker()
                                            cameraShakerEffect.wrtReparentTo(hitObject)
                                            cameraShakerEffect.setPos(hitObject, pos)
                                            cameraShakerEffect.shakeSpeed = 0.04
                                            cameraShakerEffect.shakePower = 2.0
                                            cameraShakerEffect.numShakes = 2
                                            cameraShakerEffect.scalePower = 1
                                            cameraShakerEffect.play(80.0)
                                    else:
                                        if ammoSkillId == InventoryType.GrenadeSmokeCloud:
                                            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                                                smokeCloudEffect = SmokeBomb.getEffect()
                                                if smokeCloudEffect:
                                                    smokeCloudEffect.reparentTo(hitObject)
                                                    smokeCloudEffect.setPos(hitObject, pos)
                                                    smokeCloudEffect.radius = aoeRadius / 1.5
                                                    smokeCloudEffect.play()
                                                    self.playSfx(ammoSkillId, smokeCloudEffect)
                                            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                                                flashEffect = MuzzleFlash.getEffect()
                                                if flashEffect:
                                                    flashEffect.wrtReparentTo(base.effectsRoot)
                                                    flashEffect.flash.setScale(100)
                                                    flashEffect.setPos(hitObject, pos)
                                                    flashEffect.startCol = Vec4(0.7, 0.7, 0.7, 1)
                                                    flashEffect.fadeTime = 0.2
                                                    flashEffect.play()
                                            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                                                shockwaveRingEffect = ShockwaveRing.getEffect()
                                                if shockwaveRingEffect:
                                                    shockwaveRingEffect.wrtReparentTo(base.effectsRoot)
                                                    shockwaveRingEffect.setPos(hitObject, pos)
                                                    shockwaveRingEffect.size = aoeRadius * 4
                                                    shockwaveRingEffect.play()
                                                cameraShakerEffect = CameraShaker()
                                                cameraShakerEffect.wrtReparentTo(hitObject)
                                                cameraShakerEffect.setPos(hitObject, pos)
                                                cameraShakerEffect.shakeSpeed = 0.04
                                                cameraShakerEffect.shakePower = 2.0
                                                cameraShakerEffect.numShakes = 2
                                                cameraShakerEffect.scalePower = 1
                                                cameraShakerEffect.play(80.0)

    def propHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def shipHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def avatarHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def blockerHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        for i in range(random.randint(2, 4)):
            debrisEffect = RockDebris.getEffect()
            if debrisEffect:
                debrisEffect.reparentTo(base.effectsRoot)
                debrisEffect.setPos(hitObject, pos)
                debrisEffect.offsetEndPlaneZFrom(hitObject.getZ())
                debrisEffect.debris.setScale(random.random() * 3)
                debrisEffect.radiusDist = 40
                debrisEffect.minHeight = 50
                debrisEffect.maxHeight = 100
                if debrisEffect.testTrajectory():
                    debrisEffect.play()
                else:
                    debrisEffect.cleanUpEffect()

    def groundHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        if ammoSkillId == InventoryType.CannonRoundShot or ammoSkillId == InventoryType.CannonChainShot or ammoSkillId == InventoryType.CannonBullet or ammoSkillId == InventoryType.CannonSkull or ammoSkillId == InventoryType.CannonBarShot:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                cannonExplosion = CannonExplosion.getEffect()
                if cannonExplosion:
                    cannonExplosion.wrtReparentTo(base.effectsRoot)
                    cannonExplosion.setScale(1.0)
                    cannonExplosion.setPos(hitObject, pos)
                    cannonExplosion.play()
                rockShowerEffect = RockShower.getEffect()
                if rockShowerEffect:
                    rockShowerEffect.wrtReparentTo(hitObject)
                    rockShowerEffect.setPos(hitObject, pos)
                    rockShowerEffect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                dustCloudEffect = DustCloud.getEffect()
                if dustCloudEffect:
                    dustCloudEffect.wrtReparentTo(hitObject)
                    dustCloudEffect.setPos(hitObject, pos)
                    dustCloudEffect.play()
                shockwaveRingEffect = ShockwaveRing.getEffect()
                if shockwaveRingEffect:
                    shockwaveRingEffect.wrtReparentTo(base.effectsRoot)
                    shockwaveRingEffect.size = 40
                    shockwaveRingEffect.setPos(hitObject, pos)
                    shockwaveRingEffect.play()
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.wrtReparentTo(hitObject)
                cameraShakerEffect.setPos(hitObject, pos)
                cameraShakerEffect.shakeSpeed = 0.06
                cameraShakerEffect.shakePower = 6.0
                cameraShakerEffect.numShakes = 3
                cameraShakerEffect.scalePower = 1
                cameraShakerEffect.play(80.0)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                dirtClodEffect = DirtClod.getEffect()
                if dirtClodEffect:
                    dirtClodEffect.wrtReparentTo(hitObject)
                    dirtClodEffect.setPos(hitObject, pos)
                    dirtClodEffect.play()
        else:
            self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def buildingHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def waterHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        np = render.attachNewNode('temp')
        np.setPos(hitObject, pos)
        pos = np.getPos(render)
        np.removeNode()
        if base.cr.activeWorld.getWater():
            entryWaterHeight = base.cr.activeWorld.getWater().calcHeight(pos[0], pos[1])
        else:
            entryWaterHeight = pos[2]
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            splashEffect = CannonSplash.getEffect()
            if splashEffect:
                splashEffect.wrtReparentTo(render)
                splashEffect.setPos(pos[0], pos[1], entryWaterHeight)
                splashEffect.play()

    def monsterHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        if ammoSkillId == InventoryType.CannonRoundShot or ammoSkillId == InventoryType.CannonChainShot or ammoSkillId == InventoryType.CannonBullet or ammoSkillId == InventoryType.CannonSkull or ammoSkillId == InventoryType.CannonBarShot:
            pass
        else:
            self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def grappleHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        if ammoSkillId == InventoryType.CannonGrappleHook:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                hitFlashA = HitFlashA.getEffect()
                if hitFlashA:
                    hitFlashA.wrtReparentTo(base.effectsRoot)
                    hitFlashA.setPos(hitObject, pos)
                    hitFlashA.play()
        else:
            self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def cannonHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def fortHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)
