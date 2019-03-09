import Weapon
import WeaponGlobals
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PLocalizer
from pirates.effects import PolyTrail
import random

class DualCutlass(Weapon.Weapon):
    modelTypes = {
        InventoryType.DualCutlassL1: ('models/handheld/cutlass_rusty_high', Vec4(1, 1, 1, 1))}
    models = {}
    icons = {}
    vertex_list = [
        Vec4(0.0, 0.4, 0.0, 1.0),
        Vec4(0.0, 2.0, 0.0, 1.0),
        Vec4(-0.55, 2.95, 0.0, 1.0)]
    motion_color = {
        InventoryType.DualCutlassL1: [
            Vec4(0.3, 0.4, 0.1, 0.5),
            Vec4(0.3, 0.3, 0.3, 0.5),
            Vec4(0.6, 0.6, 0.6, 0.5)]}
    walkAnim = 'dualcutlass_walk'
    runAnim = 'dualcutlass_walk'
    neutralAnim = 'dualcutlass_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'dualcutlass_hurt'
    
    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'dualcutlass')
        self.leftHandWeaponNP = None
    
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
        if self.leftHandWeaponNP:
            self.leftHandWeaponNP.removeNode()
            self.leftHandWeaponNP = None

    def getDrawIval(self, av, ammoSkillId = 0, blendInT = 0.1, blendOutT = 0):
        track = Parallel(Func(base.playSfx, self.drawSfx, node = av), av.actorInterval('dualcutlass_draw', playRate = 1, blendInT = blendInT, blendOutT = blendOutT), Sequence(Wait(0.187), Func(self.attachTo, av)))
        return track

    def getReturnIval(self, av, blendInT = 0, blendOutT = 0.1):
        track = Parallel(Func(base.playSfx, self.returnSfx, node = av), av.actorInterval('sword_putaway', playRate = 2, endFrame = 35, blendInT = blendInT, blendOutT = blendOutT), Sequence(Wait(0.56), Func(self.detachFrom, av)))
        return track
    
    def attachTo(self, av):
        Weapon.Weapon.attachTo(self, av)
        if not self.isEmpty():
            if av.leftHandNode:
                self.leftHandWeaponNP = self.instanceTo(av.leftHandNode)

        self.createTrail(av)

    def detachFrom(self, av):
        Weapon.Weapon.detachFrom(self, av)
        if self.leftHandWeaponNP:
            self.leftHandWeaponNP.detachNode()
            self.leftHandWeaponNP = None
        
        self.removeTrail()

    def createTrail(self, target):
        if self.isEmpty():
            return
        
        if not self.motion_trail:
            self.motion_trail = PolyTrail.PolyTrail(target, self.vertex_list, self.motion_color.get(self.itemId))
            self.motion_trail.reparentTo(self)
            self.motion_trail.setUseNurbs(1)
            card = loader.loadModel('models/effects/swordtrail_effects')
            tex = card.find('**/swordtrail_lines').findTexture('*')
            self.motion_trail.setTexture(tex)
            self.motion_trail.setBlendModeOn()
            card.removeNode()

    def removeTrail(self):
        if self.motion_trail:
            self.motion_trail.destroy()
            self.motion_trail = None

    def hideSpinBlur(self):
        if self.spinBlur:
            if not self.spinBlur.isEmpty():
                self.spinBlur.hide()

    def showSpinBlur(self):
        if self.spinBlur:
            if not self.spinBlur.isEmpty():
                self.spinBlur.setColorScale(self.getBlurColor() / 2.0)
                self.spinBlur.show()

    def getBlurColor(self):
        return self.motion_color.get(self.itemId)[2]

    def beginAttack(self, av):
        self.hideSpinBlur()
        Weapon.Weapon.beginAttack(self, av)

    @classmethod
    def setupSounds(cls):
        DualCutlass.hitSfxs = (loader.loadSfx('audio/sword-clashNclang.mp3'), loader.loadSfx('audio/sword-swipeNclang1.mp3'), loader.loadSfx('audio/sword-swipeNclang2.mp3'), loader.loadSfx('audio/sword-swipeNclang3.mp3'))
        DualCutlass.missSfxs = (loader.loadSfx('audio/sword-swoosh1.mp3'), loader.loadSfx('audio/sword-swoosh2.mp3'))
        DualCutlass.drawSfx = loader.loadSfx('audio/sfx_cutlass_draw.mp3')
        DualCutlass.returnSfx = loader.loadSfx('audio/sfx_cutlass_sheathe.mp3')


def getHitSfx():
    return DualCutlass.hitSfxs


def getMissSfx():
    return DualCutlass.missSfxs

