import random

import Weapon
import WeaponGlobals
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.effects.RayGlow import RayGlow
from pirates.uberdog.UberDogGlobals import InventoryType

class Wand(Weapon.Weapon):
    
    modelTypes = {InventoryType.WandWeaponL1: ('models/handheld/voodoo_staff_high', Vec4(1, 1, 1, 1)), InventoryType.WandWeaponL2: ('models/handheld/voodoo_staff_a_high', Vec4(1, 1, 1, 1)), InventoryType.WandWeaponL3: ('models/handheld/voodoo_staff_b_high', Vec4(1, 1, 1, 1)), InventoryType.WandWeaponL4: ('models/handheld/voodoo_staff_c_high', Vec4(1, 1, 1, 1)), InventoryType.WandWeaponL5: ('models/handheld/voodoo_staff_d_high', Vec4(1, 1, 1, 1)), InventoryType.WandWeaponL6: ('models/handheld/voodoo_staff_e_high', Vec4(1, 1, 1, 1))}
    colorAndOffset = {InventoryType.WandWeaponL1: (Vec4(0.5, 0.2, 1, 1), Vec3(0, 1.6, 0)), InventoryType.WandWeaponL2: (Vec4(0, 1, 0, 1), Vec3(0, 1.1, 0)), InventoryType.WandWeaponL3: (Vec4(1, 0, 0, 1), Vec3(0, 1.7, 0)), InventoryType.WandWeaponL4: (Vec4(0, 0, 1, 1), Vec3(0, 1.5, 0)), InventoryType.WandWeaponL5: (Vec4(0, 1, 1, 1), Vec3(0, 1.6, 0)), InventoryType.WandWeaponL6: (Vec4(1, 0.6, 0, 1), Vec3(0, 1.7, 0))}
    runAnim = 'run_with_weapon'
    neutralAnim = 'wand_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'wand_hurt'

    def getEffectColor(self, itemId=None):
        if not itemId:
            itemId = self.itemId
        color = self.colorAndOffset.get(itemId)
        if color:
            return color[0]

    def getOffset(self, itemId=None):
        if not itemId:
            itemId = self.itemId
        offset = self.colorAndOffset.get(itemId)
        if offset:
            return offset[1]

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'wand')
        self.effect = None
        self.effect2 = None
        self.glowEffect = None
        self.effectActor = None
        self.chargeSound = None
        self.chargeLoopSound = None
        self.chargeSoundSequence = None
        self.gem = None
        self.fadePulse = None

    def delete(self):
        self.stopChargeEffect()
        Weapon.Weapon.delete(self)

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        def playSfx():
            base.playSfx(self.unsheathSfx, node=self)

        track = Parallel(Func(playSfx), av.actorInterval('voodoo_draw', playRate=1.5, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.56), Func(self.attachTo, av)))
        del playSfx
        return track

    def getReturnIval(self, av, blendInT=0, blendOutT=0.1):
        track = Parallel(av.actorInterval('sword_putaway', playRate=2, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.56), Func(self.detachFrom, av)))
        if base.cr.targetMgr:
            track.append(Func(base.cr.targetMgr.setWantAimAssist, 0))
        return track

    def startChargeEffect(self):
        self.gem = self.prop.find('**/gem')
        self.gem2 = self.getModel(self.itemId).find('**/gem')
        if self.gem and not self.gem.isEmpty():
            self.gem2.reparentTo(self.gem)
            color = self.getEffectColor(self.itemId)
            offset = self.getOffset(self.itemId)
            self.gem.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOne, ColorBlendAttrib.OIncomingAlpha))
            fadeIn = LerpColorScaleInterval(self.gem, 0.5, color / 1.3, startColorScale=color)
            fadeOut = LerpColorScaleInterval(self.gem, 0.5, color, startColorScale=color / 1.3)
            self.fadePulse = Sequence(fadeIn, fadeOut)
            self.fadePulse.loop()
            self.glowEffect = RayGlow.getEffect()
            if self.glowEffect:
                self.glowEffect.reparentTo(self.gem)
                self.glowEffect.setPos(offset)
                self.glowEffect.effectScale = 0.3
                self.glowEffect.setEffectColor(Vec4(color))
                self.glowEffect.startLoop()

    def stopChargeEffect(self):
        if self.fadePulse:
            self.fadePulse.finish()
            self.fadePulse = None
        if self.glowEffect:
            self.glowEffect.stopLoop()
            self.glowEffect = None
        if self.gem and not self.gem.isEmpty():
            self.gem.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MNone))
            self.gem.clearColorScale()

    @classmethod
    def setupSounds(cls):
        Wand.chargeSfx = loader.loadSfx('audio/sfx_wand_charge.mp3')
        Wand.chargeLoopSfx = loader.loadSfx('audio/sfx_wand_charge_loop.wav')
        Wand.blastFireSfx = loader.loadSfx('audio/sfx_wand_blast_fire.mp3')
        Wand.blastHitSfx = loader.loadSfx('audio/sfx_wand_blast_impact.mp3')
        Wand.soulflayChargeSfx = loader.loadSfx('audio/sfx_wand_soul_flay_charge.mp3')
        Wand.soulflayHoldSfx = loader.loadSfx('audio/sfx_wand_soul_flay_hold.wav')
        Wand.soulflayFireSfx = loader.loadSfx('audio/sfx_wand_soul_flay_fire.mp3')
        Wand.soulflayHitSfx = loader.loadSfx('audio/sfx_wand_soul_flay_impact.mp3')
        Wand.pestilenceChargeSfx = loader.loadSfx('audio/sfx_wand_pestilence_charge.mp3')
        Wand.pestilenceHoldSfx = loader.loadSfx('audio/sfx_wand_pestilence_hold.wav')
        Wand.pestilenceFireSfx = loader.loadSfx('audio/sfx_wand_pestilence_fire.mp3')
        Wand.pestilenceHitSfx = loader.loadSfx('audio/sfx_wand_pestilence_impact.mp3')
        Wand.witherChargeSfx = loader.loadSfx('audio/sfx_wand_wither_charge.mp3')
        Wand.witherHoldSfx = loader.loadSfx('audio/sfx_wand_wither_hold.wav')
        Wand.witherFireSfx = loader.loadSfx('audio/sfx_wand_wither_fire.mp3')
        Wand.witherHitSfx = loader.loadSfx('audio/sfx_wand_wither_impact.mp3')
        Wand.hellfireChargeSfx = loader.loadSfx('audio/sfx_wand_hellfire_charge.mp3')
        Wand.hellfireHoldSfx = loader.loadSfx('audio/sfx_wand_hellfire_hold.wav')
        Wand.hellfireFireSfx = loader.loadSfx('audio/sfx_wand_hellfire_fire.mp3')
        Wand.hellfireHitSfx = loader.loadSfx('audio/sfx_wand_hellfire_impact.mp3')
        Wand.banishChargeSfx = loader.loadSfx('audio/sfx_wand_banish_charge.mp3')
        Wand.banishHoldSfx = loader.loadSfx('audio/sfx_wand_banish_hold.wav')
        Wand.banishFireSfx = loader.loadSfx('audio/sfx_wand_banish_fire.mp3')
        Wand.banishHitSfx = loader.loadSfx('audio/sfx_wand_banish_impact.mp3')
        Wand.desolationChargeSfx = loader.loadSfx('audio/sfx_wand_desolation_charge.mp3')
        Wand.desolationHoldSfx = loader.loadSfx('audio/sfx_wand_desolation_hold.wav')
        Wand.desolationFireSfx = loader.loadSfx('audio/sfx_wand_desolation_fire.mp3')
        Wand.desolationHitSfx = loader.loadSfx('audio/sfx_wand_desolation_impact.mp3')
        Wand.unsheathSfx = loader.loadSfx('audio/sword-unsheath.mp3')

def getSoulflayChargeSfx():
    return Wand.soulflayChargeSfx

def getPestilenceChargeSfx():
    return Wand.pestilenceChargeSfx

def getWitherChargeSfx():
    return Wand.witherChargeSfx

def getHellfireChargeSfx():
    return Wand.hellfireChargeSfx

def getBanishChargeSfx():
    return Wand.banishChargeSfx

def getDesolationChargeSfx():
    return Wand.desolationChargeSfx

def getSoulflayHoldSfx():
    return Wand.soulflayHoldSfx

def getPestilenceHoldSfx():
    return Wand.pestilenceHoldSfx

def getWitherHoldSfx():
    return Wand.witherHoldSfx

def getHellfireHoldSfx():
    return Wand.hellfireHoldSfx

def getBanishHoldSfx():
    return Wand.banishHoldSfx

def getDesolationHoldSfx():
    return Wand.desolationHoldSfx

def getBlastFireSfx():
    return Wand.blastFireSfx

def getSoulflayFireSfx():
    return Wand.soulflayFireSfx

def getPestilenceFireSfx():
    return Wand.pestilenceFireSfx

def getWitherFireSfx():
    return Wand.witherFireSfx

def getHellfireFireSfx():
    return Wand.hellfireFireSfx

def getBanishFireSfx():
    return Wand.banishFireSfx

def getDesolationFireSfx():
    return Wand.desolationFireSfx

def getBlastHitSfx():
    return Wand.blastHitSfx

def getSoulflayHitSfx():
    return Wand.soulflayHitSfx

def getPestilenceHitSfx():
    return Wand.pestilenceHitSfx

def getWitherHitSfx():
    return Wand.witherHitSfx

def getHellfireHitSfx():
    return Wand.hellfireHitSfx

def getBanishHitSfx():
    return Wand.banishHitSfx

def getDesolationHitSfx():
    return Wand.desolationHitSfx

def getChargeSfx():
    return Wand.chargeSfx

def getChargeLoopSfx():
    return Wand.chargeLoopSfx