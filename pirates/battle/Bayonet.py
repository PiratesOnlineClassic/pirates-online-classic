# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.Bayonet
import Weapon, WeaponGlobals
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.uberdog.UberDogGlobals import InventoryType
import random

def beginInterrupt(av):
    if av.isLocal():
        messenger.send('skillFinished')


class Bayonet(Weapon.Weapon):
    __module__ = __name__
    modelTypes = {InventoryType.BayonetWeaponL1: ('models/handheld/musket_bayonet', Vec4(1, 1, 1, 1)), InventoryType.BayonetWeaponL2: ('models/handheld/musket_bayonet', Vec4(0.6, 0.6, 1, 1)), InventoryType.BayonetWeaponL3: ('models/handheld/musket_bayonet', Vec4(1, 0.6, 0.6, 1))}
    walkAnim = 'bayonet_attack_walk'
    runAnim = 'bayonet_run'
    neutralAnim = 'bayonet_attack_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'boxing_hit_head_right'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'bayonet')

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)

    def changeStance(self, av):
        if av.gameFSM.state == 'Battle':
            self.walkAnim = 'bayonet_attack_walk'
            self.neutralAnim = 'bayonet_attack_idle'
            self.runAnim = 'bayonet_run'
        else:
            self.walkAnim = 'bayonet_walk'
            self.neutralAnim = 'bayonet_idle'
            self.runAnim = 'bayonet_run'
        av.setWalkForWeapon()

    def getAmmoModel():
        bullet = loader.loadModelCopy('models/props/cannonball-trail-lod')
        bullet.setScale(0.3)
        return bullet

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        track = Parallel(av.actorInterval('bayonet_idle_to_fight_idle', playRate=1.5, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.625), Func(self.attachTo, av)))
        return track

    def getReturnIval(self, av, blendInT=0, blendOutT=0.1):
        track = Parallel(av.actorInterval('bayonet_idle_to_idle', playRate=2, endFrame=37, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.6), Func(self.detachFrom, av)))
        if base.cr.targetMgr:
            track.append(Func(base.cr.targetMgr.setWantAimAssist, 0))
        return track

    def getAnimState(self, animState):
        if animState == 'LandRoam':
            return 'BayonetLandRoam'
        else:
            return animState

    @classmethod
    def setupSounds(cls):
        Bayonet.hitSfxs = (loader.loadSfx('audio/sfx_dagger_impact.mp3'),)
        Bayonet.aimSfxs = (None, )
        Bayonet.gunCockSfxs = (None, )
        Bayonet.reloadSfxs = (None, )
        Bayonet.missSfxs = (
         loader.loadSfx('audio/whoosh-10.mp3'), loader.loadSfx('audio/arm-Whoosh-05.mp3'))
        return


def getShootSfx():
    return Bayonet.hitSfxs


def getHitSfx():
    return Bayonet.hitSfxs


def getMissSfx():
    return Bayonet.missSfxs


def getAimSfx():
    return Bayonet.aimSfxs


def getReloadSfx():
    return Bayonet.reloadSfxs


def getGunCockSfx():
    return Bayonet.gunCockSfxs
# okay decompiling .\pirates\battle\Bayonet.pyc
