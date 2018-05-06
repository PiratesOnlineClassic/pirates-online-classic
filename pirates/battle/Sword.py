import random

from pirates.battle import Weapon
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from pirates.effects import PolyTrail
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType

class Sword(Weapon.Weapon):
    modelTypes = {InventoryType.CutlassWeaponL1: ('models/handheld/cutlass_rusty_high', Vec4(1, 1, 1, 1)), InventoryType.CutlassWeaponL2: ('models/handheld/cutlass_iron_high', Vec4(1, 1, 1, 1)), InventoryType.CutlassWeaponL3: ('models/handheld/cutlass_steel_high', Vec4(1, 1, 1, 1)), InventoryType.CutlassWeaponL4: ('models/handheld/cutlass_fine_high', Vec4(1, 1, 1, 1)), InventoryType.CutlassWeaponL5: ('models/handheld/cutlass_pirateblade_high', Vec4(1, 1, 1, 1)), InventoryType.CutlassWeaponL6: ('models/handheld/cutlass_dark_high', Vec4(1, 1, 1, 1))}
    models = {}
    icons = {}
    vertex_list = [Vec4(0.0, 0.4, 0.0, 1.0), Vec4(0.0, 2.0, 0.0, 1.0), Vec4(-0.55, 2.95, 0.0, 1.0)]
    motion_color = {InventoryType.CutlassWeaponL1: [Vec4(0.3, 0.4, 0.1, 0.5), Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.6, 0.6, 0.6, 0.5)], InventoryType.CutlassWeaponL2: [Vec4(0.1, 0.2, 0.4, 0.5), Vec4(0.4, 0.5, 0.7, 0.5), Vec4(0.5, 0.5, 0.9, 0.75)], InventoryType.CutlassWeaponL3: [Vec4(1, 1, 0.4, 0.5), Vec4(0.4, 0.5, 0.6, 0.5), Vec4(0.7, 0.7, 0.8, 0.75)], InventoryType.CutlassWeaponL4: [Vec4(0.6, 0.6, 0.75, 1), Vec4(0.6, 0.5, 0.2, 1), Vec4(0.6, 0.6, 0.4, 1)], InventoryType.CutlassWeaponL5: [Vec4(1, 0.2, 0.2, 0.5), Vec4(0.5, 0.5, 0.5, 0.75), Vec4(0.7, 0.7, 0.9, 1)], InventoryType.CutlassWeaponL6: [Vec4(1, 1, 0, 0.5), Vec4(0.3, 0.3, 0.3, 1), Vec4(0.1, 0.1, 0.1, 1)]}
    walkAnim = 'walk'
    runAnim = 'run_with_weapon'
    neutralAnim = 'sword_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'boxing_hit_head_right'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'sword')

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)
        self.spinBlur = self.prop.find('**/motion_blur')
        self.spinBlur.setAlphaScale(0.25)
        self.hideSpinBlur()

    def delete(self):
        self.endAttack(None)
        self.removeTrail()
        Weapon.Weapon.delete(self)

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        track = Parallel(Func(base.playSfx, self.drawSfx, node=av), av.actorInterval('sword_draw', playRate=1.5, endFrame=15, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.187), Func(self.attachTo, av)))
        return track

    def getReturnIval(self, av, blendInT=0, blendOutT=0.1):
        track = Parallel(Func(base.playSfx, self.returnSfx, node=av), av.actorInterval('sword_putaway', playRate=2, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.56), Func(self.detachFrom, av)))
        return track

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
            self.motion_trail = PolyTrail.PolyTrail(target, self.vertex_list, self.motion_color.get(self.itemId))
            self.motion_trail.reparentTo(self)
            self.motion_trail.setUseNurbs(1)
            card = loader.loadModelCopy('models/effects/swordtrail_effects')
            tex = card.find('**/swordtrail_lines').findTexture('*')
            self.motion_trail.setTexture(tex)
            self.motion_trail.setBlendModeOn()
            if self.itemId == InventoryType.CutlassWeaponL6:
                self.motion_trail.setBlendModeOff()
            card.removeNode()

    def removeTrail(self):
        if self.motion_trail:
            self.motion_trail.destroy()
            self.motion_trail = None

    def getBlurColor(self):
        return self.motion_color.get(self.itemId)[2]

    def beginAttack(self, av):
        self.hideSpinBlur()
        Weapon.Weapon.beginAttack(self, av)

    @classmethod
    def setupSounds(cls):
        Sword.hitSfxs = (loader.loadSfx('audio/sword-clashNclang.mp3'), loader.loadSfx('audio/sword-swipeNclang1.mp3'), loader.loadSfx('audio/sword-swipeNclang2.mp3'), loader.loadSfx('audio/sword-swipeNclang3.mp3'))
        Sword.missSfxs = (
         loader.loadSfx('audio/sword-swoosh1.mp3'), loader.loadSfx('audio/sword-swoosh2.mp3'))
        Sword.skillSfxs = {InventoryType.CutlassHack: loader.loadSfx('audio/sfx_cutlass_hack.mp3'), InventoryType.CutlassSlash: loader.loadSfx('audio/sfx_cutlass_slash.mp3'), InventoryType.CutlassStab: loader.loadSfx('audio/sfx_cutlass_stab.mp3'), InventoryType.CutlassFlourish: loader.loadSfx('audio/sfx_cutlass_flourish.mp3'), InventoryType.CutlassCleave: loader.loadSfx('audio/sfx_cutlass_cleave.mp3'), InventoryType.CutlassTaunt: loader.loadSfx('audio/sfx_cutlass_taunt.mp3'), InventoryType.CutlassBrawl: loader.loadSfx('audio/sfx_cutlass_brawl_headbutt.mp3'), InventoryType.CutlassSweep: loader.loadSfx('audio/sfx_cutlass_sweep.mp3'), InventoryType.CutlassBladestorm: loader.loadSfx('audio/sfx_cutlass_bladestorm.mp3')}
        Sword.drawSfx = loader.loadSfx('audio/sfx_cutlass_draw.mp3')
        Sword.returnSfx = loader.loadSfx('audio/sfx_cutlass_sheathe.mp3')

def getHitSfx():
    return Sword.hitSfxs

def getMissSfx():
    return Sword.missSfxs