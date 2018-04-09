import random

import Weapon
import WeaponGlobals
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.uberdog.UberDogGlobals import InventoryType


class Doll(Weapon.Weapon):
    modelTypes = {InventoryType.DollWeaponL1: ('models/handheld/voodoo_doll_high', Vec4(1, 1, 1, 1), 'None'), InventoryType.DollWeaponL2: ('models/handheld/voodoo_doll_cloth_high', Vec4(0.5, 0.3, 1, 1), 'effectCloth'), InventoryType.DollWeaponL3: ('models/handheld/voodoo_doll_witch_high', Vec4(1, 0.7, 0.7, 1), 'effectWitch'), InventoryType.DollWeaponL4: ('models/handheld/voodoo_doll_pirate_high', Vec4(1, 1, 1, 1), 'effectPirate'), InventoryType.DollWeaponL5: ('models/handheld/voodoo_doll_taboo_high', Vec4(1, 1, 1, 1), 'effectTaboo'), InventoryType.DollWeaponL6: ('models/handheld/voodoo_doll_mojo_high', Vec4(0.7, 0.5, 1, 1), 'effectMojo')}
    painAnim = 'voodoo_doll_hurt'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'doll')
        self.effect = None
        self.effectCard = None
        self.effectColor = self.modelTypes.get(itemId)[1]
        card = loader.loadModel('models/effects/effectCards').find('**/' + self.modelTypes.get(itemId)[2])
        if not card.isEmpty():
            self.effectCard = card
        return

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)
        self.prop.setScale(1.4)

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        track = Parallel(av.actorInterval('voodoo_draw', playRate=1.5, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.56), Func(self.attachTo, av)))
        return track

    def getReturnIval(self, av, blendInT=0, blendOutT=0.1):
        track = Parallel(av.actorInterval('sword_putaway', playRate=2, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.56), Func(self.detachFrom, av)))
        return track

    def playUnattuneSfx(self, node):
        base.playSfx(self.unattuneSfx, node=node)

    @classmethod
    def setupSounds(cls):
        Doll.hitSfxs = loader.loadSfx('audio/sword-clashNclang.mp3')
        Doll.missSfxs = (
         loader.loadSfx('audio/sword-swoosh1.mp3'), loader.loadSfx('audio/sword-swoosh2.mp3'))
        Doll.attuneSfx = loader.loadSfx('audio/sfx_doll_attune.mp3')
        Doll.unattuneSfx = loader.loadSfx('audio/sfx_doll_unattune.mp3')
        Doll.attuneLoopSfx = loader.loadSfx('audio/sfx_doll_attune_loop.wav')
        Doll.pokeSfx = loader.loadSfx('audio/sfx_doll_poke.mp3')
        Doll.swarmSfx = loader.loadSfx('audio/sfx_doll_swarm.mp3')
        Doll.healSfx = loader.loadSfx('audio/sfx_doll_heal.mp3')
        Doll.curseSfx = loader.loadSfx('audio/sfx_doll_curse.mp3')
        Doll.scorchSfx = loader.loadSfx('audio/sfx_doll_burn.mp3')
        Doll.cureSfx = loader.loadSfx('audio/sfx_doll_cure.mp3')
        Doll.shacklesSfx = loader.loadSfx('audio/sfx_doll_poke.mp3')
        Doll.lifedrainSfx = loader.loadSfx('audio/sfx_doll_poke.mp3')
        Doll.unsheathSfx = loader.loadSfx('audio/sword-unsheath.mp3')


def getHitSfx():
    return Doll.hitSfxs


def getMissSfx():
    return Doll.missSfxs


def getAttuneSfx():
    return Doll.attuneSfx


def getUnattuneSfx():
    return Doll.unattuneSfx


def getPokeSfx():
    return Doll.pokeSfx


def getSwarmSfx():
    return Doll.swarmSfx


def getHealSfx():
    return Doll.healSfx


def getCurseSfx():
    return Doll.curseSfx


def getScorchSfx():
    return Doll.scorchSfx


def getCureSfx():
    return Doll.cureSfx


def getShacklesSfx():
    return Doll.shacklesSfx


def getLifedrainSfx():
    return Doll.lifedrainSfx