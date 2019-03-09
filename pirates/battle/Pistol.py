import Weapon
import WeaponGlobals
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.uberdog.UberDogGlobals import InventoryType
import random

class Pistol(Weapon.Weapon):
    modelTypes = {
        InventoryType.PistolWeaponL1: ('models/handheld/pistol_high', Vec4(1, 1, 1, 1)),
        InventoryType.PistolWeaponL2: ('models/handheld/double_barrel_pistol_high', Vec4(1, 1, 1, 1)),
        InventoryType.PistolWeaponL3: ('models/handheld/triple_barrel_pistol_high', Vec4(1, 1, 1, 1)),
        InventoryType.PistolWeaponL4: ('models/handheld/triple_barrel_pistol_b_high', Vec4(1, 1, 1, 1)),
        InventoryType.PistolWeaponL5: ('models/handheld/triple_barrel_pistol_c_high', Vec4(1, 1, 1, 1)),
        InventoryType.PistolWeaponL6: ('models/handheld/quad_barrel_pistol_high', Vec4(1, 1, 1, 1))}
    walkAnim = 'walk'
    runAnim = 'run_with_weapon'
    neutralAnim = 'gun_pointedup_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'gun_hurt'
    
    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'pistol')
    
    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)
    
    def getAmmoModel():
        bullet = loader.loadModelCopy('models/props/cannonball-trail-lod')
        bullet.setScale(0.3)
        return bullet
    
    def getDrawIval(self, av, ammoSkillId = 0, blendInT = 0.1, blendOutT = 0):
        track = Parallel(av.actorInterval('gun_draw', playRate = 1.5, endFrame = 35, blendInT = blendInT, blendOutT = blendOutT), Func(base.playSfx, self.drawSfx, node = av), Sequence(Wait(0.625), Func(self.attachTo, av)))
        return track
    
    def getReturnIval(self, av, blendInT = 0, blendOutT = 0.1):
        track = Parallel(av.actorInterval('gun_putaway', playRate = 2, endFrame = 37, blendInT = blendInT, blendOutT = blendOutT), Func(base.playSfx, self.returnSfx, node = av), Sequence(Wait(0.6), Func(self.detachFrom, av)))
        if base.cr.targetMgr:
            track.append(Func(base.cr.targetMgr.setWantAimAssist, 0))
        
        return track

    @classmethod
    def setupSounds(cls):
        hpHit = loader.loadSfx('audio/sfx_pistol_effective.mp3')
        manaHit = loader.loadSfx('audio/sfx_pistol_mana_drain.mp3')
        Pistol.hitSfxs = {
            InventoryType.PistolLeadShot: hpHit,
            InventoryType.PistolBaneShot: manaHit,
            InventoryType.PistolSilverShot: hpHit,
            InventoryType.PistolHexEaterShot: manaHit,
            InventoryType.PistolSteelShot: hpHit,
            InventoryType.PistolVenomShot: manaHit}
        Pistol.missSfxs = (loader.loadSfx('audio/gunshot1.mp3'),)
        Pistol.aimSfxs = (loader.loadSfx('audio/musketCock.mp3'),)
        Pistol.skillSfxs = {
            InventoryType.PistolShoot: loader.loadSfx('audio/sfx_pistol_shoot.mp3'),
            InventoryType.PistolTakeAim: loader.loadSfx('audio/sfx_pistol_shoot.mp3')}
        Pistol.drawSfx = loader.loadSfx('audio/sfx_pistol_draw.mp3')
        Pistol.gunCockSfx = loader.loadSfx('audio/sfx_pistol_cock.mp3')
        Pistol.reloadSfx = loader.loadSfx('audio/sfx_pistol_reload.mp3')
        Pistol.returnSfx = loader.loadSfx('audio/sfx_pistol_put_away.mp3')


def getHitSfx():
    return Pistol.hitSfxs


def getMissSfx():
    return Pistol.missSfxs


def getAimSfx():
    return Pistol.aimSfxs

