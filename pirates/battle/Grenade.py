from pirates.battle import Weapon
from direct.interval.IntervalGlobal import *
from panda3d.core import *
from pirates.battle.WeaponGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


class Grenade(Weapon.Weapon):
    modelTypes = {InventoryType.GrenadeWeaponL1: ('models/ammunition/grenade', Vec4(1, 1, 1, 1)), InventoryType.GrenadeWeaponL2: ('models/ammunition/grenade', Vec4(1, 1, 1, 1)), InventoryType.GrenadeWeaponL3: ('models/ammunition/grenade', Vec4(1, 1, 1, 1)), InventoryType.GrenadeWeaponL4: ('models/ammunition/grenade', Vec4(1, 1, 1, 1)), InventoryType.GrenadeWeaponL5: ('models/ammunition/grenade', Vec4(1, 1, 1, 1)), InventoryType.GrenadeWeaponL6: ('models/ammunition/grenade', Vec4(1, 1, 1, 1))}
    walkAnim = 'walk'
    runAnim = 'run_with_weapon'
    neutralAnim = 'bomb_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'bomb_hurt'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'grenade')
        self.ammoSkillId = 0

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)

    def changeStance(self, av):
        if av.gameFSM.state == 'WaterRoam' or av.gameFSM.state == 'WaterTreasureRoam':
            return
        if not self.ammoSkillId:
            self.walkAnim = 'walk'
            self.runAnim = 'run'
            self.walkBackAnim = 'walk'
            self.neutralAnim = 'idle'
            self.strafeLeftAnim = 'strafe_left'
            self.strafeRightAnim = 'strafe_right'
            self.strafeDiagLeftAnim = 'run_diagonal_left'
            self.strafeDiagRightAnim = 'run_diagonal_right'
            self.strafeRevDiagLeftAnim = 'walk_back_diagonal_left'
            self.strafeRevDiagRightAnim = 'walk_back_diagonal_right'
            self.painAnim = 'boxing_hit_head_right'
            self.prop.setPos(-0.05, -0.05, -0.2)
            self.prop.setScale(0.45)
            av.speedIndex = PiratesGlobals.SPEED_BATTLE_INDEX
            if av.isLocal():
                av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[av.speedIndex])
        elif self.ammoSkillId == InventoryType.GrenadeSiege:
            self.walkAnim = 'bigbomb_walk'
            self.runAnim = 'bigbomb_walk'
            self.walkBackAnim = 'bigbomb_walk'
            self.neutralAnim = 'bigbomb_idle'
            self.strafeLeftAnim = 'bigbomb_walk_left'
            self.strafeRightAnim = 'bigbomb_walk_right'
            self.strafeDiagLeftAnim = 'bigbomb_walk_left_diagonal'
            self.strafeDiagRightAnim = 'bigbomb_walk_right_diagonal'
            self.strafeRevDiagLeftAnim = 'bigbomb_walk_back_left'
            self.strafeRevDiagRightAnim = 'bigbomb_walk_back_right'
            self.painAnim = 'boxing_hit_head_right'
            self.prop.setPos(-0.15, -0.25, -0.5)
            self.prop.setScale(1.25)
            av.speedIndex = PiratesGlobals.SPEED_HEAVY_INDEX
            if av.isLocal():
                av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[av.speedIndex])
        else:
            self.walkAnim = 'walk'
            self.runAnim = 'run'
            self.walkBackAnim = 'walk'
            self.neutralAnim = 'bomb_idle'
            self.strafeLeftAnim = 'strafe_left'
            self.strafeRightAnim = 'strafe_right'
            self.strafeDiagLeftAnim = 'run_diagonal_left'
            self.strafeDiagRightAnim = 'run_diagonal_right'
            self.strafeRevDiagLeftAnim = 'walk_back_diagonal_left'
            self.strafeRevDiagRightAnim = 'walk_back_diagonal_right'
            self.painAnim = 'boxing_hit_head_right'
            self.prop.setPos(-0.05, -0.05, -0.2)
            self.prop.setScale(0.45)
            av.speedIndex = PiratesGlobals.SPEED_BATTLE_INDEX
            if av.isLocal():
                av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[av.speedIndex])
        av.setWalkForWeapon()

    def setAmmoSkillId(self, ammoSkillId):
        self.ammoSkillId = ammoSkillId

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        if not ammoSkillId:
            track = Sequence(Func(self.setAmmoSkillId, 0), Func(self.changeStance, av), Func(self.detachFrom, av))
        else:
            if ammoSkillId == InventoryType.GrenadeSiege:
                track = Parallel(av.actorInterval('bigbomb_draw', playRate=1.5, endFrame=40, blendInT=blendInT, blendOutT=blendOutT), Func(base.playSfx, self.drawSfx, node=av), Sequence(Wait(0.343), Func(self.attachTo, av), Func(self.setAmmoSkillId, ammoSkillId), Func(self.changeStance, av)))
            else:
                track = Parallel(av.actorInterval('bomb_draw', playRate=1.5, endFrame=30, blendInT=blendInT, blendOutT=blendOutT), Func(base.playSfx, self.drawSfx, node=av), Sequence(Wait(0.125), Func(self.attachTo, av), Func(self.setAmmoSkillId, ammoSkillId), Func(self.changeStance, av)))
        return track

    def getReturnIval(self, av, ammoSkillId=0, blendInT=0, blendOutT=0.1):
        if not ammoSkillId:
            ammoSkillId = self.ammoSkillId
        if ammoSkillId == InventoryType.GrenadeSiege:
            track = Parallel(av.actorInterval('bigbomb_draw', playRate=1.5, startFrame=28, endFrame=1, blendInT=blendInT, blendOutT=blendOutT), Func(base.playSfx, self.returnSfx, node=av), Sequence(Wait(0.5), Func(self.detachFrom, av), Func(self.setAmmoSkillId, 0), Func(self.changeStance, av)))
        else:
            track = Parallel(av.actorInterval('bomb_draw', playRate=1.5, startFrame=20, endFrame=1, blendInT=blendInT, blendOutT=blendOutT), Func(base.playSfx, self.returnSfx, node=av), Sequence(Wait(0.468), Func(self.detachFrom, av), Func(self.setAmmoSkillId, 0), Func(self.changeStance, av)))
        return track

    def getAmmoChangeIval(self, av, skillId, ammoSkillId, charge, target=None):
        if self.ammoSkillId == InventoryType.GrenadeSiege:
            track = Sequence(Func(self.lockInput, av), av.actorInterval('bigbomb_draw', startFrame=28, endFrame=11, blendInT=0.25, blendOutT=0), Func(self.detachFrom, av))
        else:
            track = Sequence(Func(self.lockInput, av), av.actorInterval('bomb_draw', startFrame=20, endFrame=11, blendInT=0.25, blendOutT=0), Func(self.detachFrom, av))
        if ammoSkillId:
            track.append(Func(self.attachTo, av))
        if ammoSkillId == InventoryType.GrenadeSiege:
            track.append(Func(self.setAmmoSkillId, ammoSkillId))
            track.append(Func(self.changeStance, av))
            track.append(av.actorInterval('bigbomb_draw', startFrame=12, endFrame=40, blendInT=0, blendOutT=0.5))
            track.append(Func(self.unlockInput, av))
        else:
            track.append(Func(self.setAmmoSkillId, ammoSkillId))
            track.append(Func(self.changeStance, av))
            track.append(av.actorInterval('bomb_draw', startFrame=12, endFrame=30, blendInT=0, blendOutT=0.5))
            track.append(Func(self.unlockInput, av))
        return track

    @classmethod
    def setupSounds(cls):
        Grenade.aimSfxs = (loader.loadSfx('audio/sfx_pistol_cock.mp3'),)
        Grenade.reloadSfxs = (loader.loadSfx('audio/sfx_pistol_reload.mp3'),)
        Grenade.skillSfxs = {InventoryType.GrenadeThrow: loader.loadSfx('audio/sfx_grenade_throw.mp3'), InventoryType.GrenadeSiege: loader.loadSfx('audio/sfx_grenade_bigbomb_throw.mp3'), InventoryType.GrenadeLongVolley: loader.loadSfx('audio/sfx_grenade_long_volley_throw.mp3')}
        Grenade.chargingSfx = loader.loadSfx('audio/sfx_grenade_long_volley_charging.mp3')
        Grenade.drawSfx = loader.loadSfx('audio/sfx_grenade_bigbomb_draw.mp3')
        Grenade.returnSfx = loader.loadSfx('audio/sfx_grenade_bigbomb_put_away.mp3')

    def lockInput(self, av):
        if av.isLocal():
            messenger.send('skillStarted')

    def unlockInput(self, av):
        if av.isLocal():
            messenger.send('skillFinished')


def getHitSfx():
    return


def getMissSfx():
    return


def getAimSfx():
    return Grenade.aimSfxs


def getReloadSfx():
    return Grenade.reloadSfxs
