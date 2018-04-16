# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.Dagger
import random

import Weapon
import WeaponGlobals
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.effects import PolyTrail
from pirates.uberdog.UberDogGlobals import InventoryType


class Dagger(Weapon.Weapon):
    
    modelTypes = {InventoryType.DaggerWeaponL1: ('models/handheld/dagger_high', Vec4(1, 1, 1, 1)), InventoryType.DaggerWeaponL2: ('models/handheld/dagger_dirk_high', Vec4(1, 1, 1, 1)), InventoryType.DaggerWeaponL3: ('models/handheld/dagger_gauche_high', Vec4(1, 1, 1, 1)), InventoryType.DaggerWeaponL4: ('models/handheld/dagger_coltello_high', Vec4(1, 1, 1, 1)), InventoryType.DaggerWeaponL5: ('models/handheld/dagger_bloodletter_high', Vec4(1, 1, 1, 1)), InventoryType.DaggerWeaponL6: ('models/handheld/dagger_slicer_high', Vec4(1, 1, 1, 1))}
    models = {}
    icons = {}
    vertex_list = [
     Vec4(0.0, 0.4, 0.0, 1.0), Vec4(0.0, 2.0, 0.0, 1.0)]
    motion_color = [
     Vec4(0.3, 0.4, 0.6, 1.0), Vec4(0.7, 0.7, 0.8, 1.0)]
    runAnim = 'run_with_weapon'
    neutralAnim = 'sword_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'dagger_hurt'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'daggers')

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)
        self.spinBlur = self.prop.find('**/motion_blur')
        self.spinBlur.setAlphaScale(0.5)
        self.hideSpinBlur()

    def delete(self):
        self.endAttack(None)
        self.removeTrail()
        Weapon.Weapon.delete(self)
        return

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):

        def playSfx():
            base.playSfx(self.unsheathSfx, node=self)

        track = Parallel(Func(playSfx), av.actorInterval('sword_draw', playRate=1.5, endFrame=15, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.187), Func(self.attachTo, av)))
        del playSfx
        return track

    def getReturnIval(self, av, blendInT=0, blendOutT=0.1):
        track = Parallel(av.actorInterval('sword_putaway', playRate=2, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.56), Func(self.detachFrom, av)))
        return track

    def throwDagger(self, av, time, targetPos, motion_color=None, startOffset=Vec3(0, 0, 0), roll=0):
        if av:
            roll += random.uniform(-15.0, 15.0)
            effect = DaggerProjectile.getEffect()
            if effect:
                effect.reparentTo(render)
                effect.setPos(av.rightHandNode, startOffset)
                effect.setHpr(av.getH(render) + roll, 90 + roll, roll)
                effect.play(time, targetPos, motion_color)

    def attachTo(self, av):
        Weapon.Weapon.attachTo(self, av)
        self.createTrail(av)

    def detachFrom(self, av):
        Weapon.Weapon.detachFrom(self, av)
        self.removeTrail()

    def createTrail(self, target):
        if self.isEmpty():
            return
        if not self.motion_trail:
            self.motion_trail = PolyTrail.PolyTrail(target, self.vertex_list, self.motion_color)
            self.motion_trail.reparentTo(self)
            self.motion_trail.setUseNurbs(1)
            card = loader.loadModelCopy('models/effects/swordtrail_effects')
            tex = card.find('**/swordtrail_lines').findTexture('*')
            self.motion_trail.setTexture(tex)
            card.removeNode()

    def removeTrail(self):
        if self.motion_trail:
            self.motion_trail.destroy()
            self.motion_trail = None
        return

    def beginAttack(self, av):
        self.hideSpinBlur()
        if self.motion_trail:
            self.motion_trail.beginTrail()

    def getCut(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Func(self.playSkillSfx, skillId, av), Sequence(Func(self.lockInput, av), Func(self.endAttack, av), Func(self.setTrailLength, 0.25), Func(self.beginAttack, av), av.actorInterval('dagger_combo', playRate=1.0, startFrame=1, endFrame=28, blendInT=0.2, blendOutT=0.5)), Sequence(Wait(0.75), Func(self.unlockInput, av)))
        return ival

    def getSwipe(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Func(self.playSkillSfx, skillId, av), Sequence(Func(self.lockInput, av), Func(self.endAttack, av), Func(self.setTrailLength, 0.3), Func(self.beginAttack, av), av.actorInterval('dagger_combo', playRate=1.0, startFrame=29, endFrame=53, blendInT=0.5, blendOutT=0.5), Func(self.hideSpinBlur)), Sequence(Wait(0.583), Func(self.unlockInput, av)), Sequence(Wait(0.1), Func(self.showSpinBlur)))
        return ival

    def getGouge(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Func(self.playSkillSfx, skillId, av), Sequence(Func(self.lockInput, av), Func(self.endAttack, av), Func(self.setTrailLength, 0.5), Func(self.beginAttack, av), av.actorInterval('dagger_combo', playRate=1.0, startFrame=54, endFrame=87, blendInT=0.5, blendOutT=0.5)), Sequence(Wait(0.958), Func(self.unlockInput, av)))
        return ival

    def getEviscerate(self, av, skillId, ammoSkillId, charge, target):
        ival = Parallel(Func(self.playSkillSfx, skillId, av), Sequence(Func(self.lockInput, av), Func(self.endAttack, av), Func(self.setTrailLength, 0.6), Func(self.beginAttack, av), av.actorInterval('dagger_combo', playRate=1.0, startFrame=88, endFrame=142, blendInT=0.5, blendOutT=0.5)), Sequence(Wait(1.5), Func(self.unlockInput, av)))
        return ival

    def getDaggerThrowDirtInterval(self, av, skillId, ammoSkillId, charge, target):

        def startVFX():
            effect = ThrowDirt.getEffect()
            if effect:
                effect.reparentTo(render)
                effect.setPos(av.getPos(render))
                effect.setHpr(av.getHpr(render))
                effect.particleDummy.setPos(av.getPos(render))
                effect.particleDummy.setHpr(av.getHpr(render))
                effect.play()

        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(self.hideMouse, av), Func(base.disableMouse), Func(self.endAttack, av), Func(self.setTrailLength, 0.25), Func(self.hideWeapon), Func(self.beginAttack, av), av.actorInterval('dagger_throw_sand', playRate=1.0, startFrame=1, endFrame=10, blendInT=0.2, blendOutT=0), Func(self.playSkillSfx, skillId, av), Func(startVFX), av.actorInterval('dagger_throw_sand', playRate=1.0, startFrame=11, endFrame=38, blendInT=0, blendOutT=0.3), Func(self.showWeapon), Func(av.motionFSM.on), Func(self.unlockInput, av))
        return ival

    def getDaggerAspInterval(self, av, skillId, ammoSkillId, charge, target):
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        track = Sequence(Func(self.lockInput, av), Func(self.setTrailLength, 0.25), Func(self.playSkillSfx, skillId, av), av.actorInterval('knife_throw', endFrame=17, blendInT=0.2, blendOutT=0), Parallel(av.actorInterval('knife_throw', startFrame=18, blendInT=0, blendOutT=0.4), Func(self.throwDagger, av, speed, targetPos), Func(self.hideWeapon)), Func(self.showWeapon), Func(self.unlockInput, av))
        return track

    def getDaggerAdderInterval(self, av, skillId, ammoSkillId, charge, target):
        motion_color = [
         Vec4(0.1, 1.0, 0.4, 1.0), Vec4(0.5, 1.0, 0.4, 1.0)]
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        track = Sequence(Func(self.lockInput, av), Func(self.setTrailLength, 0.25), Func(self.playSkillSfx, skillId, av), av.actorInterval('knife_throw', endFrame=17, blendInT=0.2, blendOutT=0), Parallel(av.actorInterval('knife_throw', startFrame=18, blendInT=0, blendOutT=0.4), Func(self.throwDagger, av, speed, targetPos, motion_color), Func(self.hideWeapon)), Func(self.showWeapon), Func(self.unlockInput, av))
        return track

    def getDaggerSidewinderInterval(self, av, skillId, ammoSkillId, charge, target):
        motion_color = [
         Vec4(1.0, 0.0, 0.0, 1.0), Vec4(1.0, 0.2, 0.0, 1.0)]
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        track = Sequence(Func(self.lockInput, av), Func(self.setTrailLength, 0.25), Func(self.playSkillSfx, skillId, av), av.actorInterval('dagger_asp', endFrame=7, blendInT=0.1, blendOutT=0), Parallel(av.actorInterval('dagger_asp', startFrame=8, blendInT=0, blendOutT=0.4), Func(self.throwDagger, av, speed, targetPos, motion_color, roll=90), Func(self.hideWeapon)), Func(self.showWeapon), Func(self.unlockInput, av))
        return track

    def getDaggerViperNestInterval(self, av, skillId, ammoSkillId, charge, target):
        numDaggers = 12.0
        time = 0.7
        placeHolder = av.attachNewNode('daggerPlaceHolder')
        daggerTossIval = Parallel(Sequence(Func(self.lockInput, av), Func(self.setTrailLength, 0.25), av.actorInterval('dagger_vipers_nest', startFrame=21, endFrame=35, blendInT=0, blendOutT=0.4), Func(self.showWeapon), Func(av.motionFSM.on), Func(self.unlockInput, av)))
        for i in range(numDaggers):
            if av.isLocal():
                placeHolder.setPos(camera, random.uniform(-12, 12), random.uniform(100, 120), random.uniform(8, 18))
            else:
                placeHolder.setPos(av, random.uniform(-12, 12), random.uniform(100, 120), random.uniform(2, 12))
            targetPos = placeHolder.getPos(render)
            daggerTossIval.append(Func(self.throwDagger, av, time + random.uniform(-0.5, 1.0), targetPos, startOffset=Vec3(-3, 0, 0), roll=90))

        placeHolder.removeNode()
        track = Sequence(Func(av.motionFSM.off), Func(self.hideMouse, av), Func(self.hideWeapon), Func(self.playSkillSfx, skillId, av), av.actorInterval('dagger_vipers_nest', endFrame=20, blendOutT=0), daggerTossIval)
        return track

    @classmethod
    def setupSounds(cls):
        Dagger.missSfxs = (loader.loadSfx('audio/swordSwipeSingle-01.mp3'), loader.loadSfx('audio/swordSwipeSingle-02.mp3'))
        Dagger.hitSfxs = (
         loader.loadSfx('audio/sfx_dagger_impact.mp3'),)
        Dagger.skillSfxs = {InventoryType.DaggerCut: loader.loadSfx('audio/sfx_dagger_cut.mp3'), InventoryType.DaggerSwipe: loader.loadSfx('audio/sfx_dagger_swipe.mp3'), InventoryType.DaggerGouge: loader.loadSfx('audio/sfx_dagger_gouge.mp3'), InventoryType.DaggerEviscerate: loader.loadSfx('audio/sfx_dagger_eviscerate.mp3'), InventoryType.DaggerAsp: loader.loadSfx('audio/sfx_dagger_thrown.mp3'), InventoryType.DaggerAdder: loader.loadSfx('audio/sfx_dagger_poison.mp3'), InventoryType.DaggerThrowDirt: loader.loadSfx('audio/sfx_dagger_throw_dirt.mp3'), InventoryType.DaggerSidewinder: loader.loadSfx('audio/sfx_dagger_sidewinder.mp3'), InventoryType.DaggerViperNest: loader.loadSfx('audio/sfx_dagger_vipersnest.mp3')}
        Dagger.unsheathSfx = loader.loadSfx('audio/sword-unsheath.mp3')


def getHitSfx():
    return Dagger.hitSfxs


def getMissSfx():
    return Dagger.missSfxs
# okay decompiling .\pirates\battle\Dagger.pyc
