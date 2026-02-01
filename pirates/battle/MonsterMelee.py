import types
from direct.interval.IntervalGlobal import *
from pirates.battle import Weapon
from pirates.battle.WeaponGlobals import *
from pirates.effects import PolyTrail
from pirates.pirate import AvatarTypes
_sfxDict = {}

def cacheSfx(name, file):
    sfx = _sfxDict.get(name)
    if not sfx:
        if type(file) == tuple:
            sfx = list(map(loader.loadSfx, file))
        else:
            sfx = loader.loadSfx(file)
        _sfxDict[name] = sfx
    
    return sfx


def getHitSfx():
    return cacheSfx('hit', 'audio/body_blow.mp3')


def getMissSfx():
    return cacheSfx('miss', 'audio/whoosh-10.mp3')


def getEnsnareSfx():
    return cacheSfx('ensnare', 'audio/kraken2.mp3')


def getSmashSfx():
    return cacheSfx('smash', ('audio/wood_impact_1.mp3', 'audio/wood_impact_3.mp3', 'audio/wood_impact_4.mp3'))


def getWaspStingSfx():
    return cacheSfx('waspSting', 'audio/sfx_wasp_sting.mp3')


def getWaspLeapStingSfx():
    return cacheSfx('waspLeapSting', 'audio/sfx_wasp_leap_sting.mp3')


def getBatAttackSfx():
    return cacheSfx('batAttack', 'audio/sfx_bat_attack_left.mp3')


def getAlligatorAttackLeftSfx():
    return cacheSfx('alligatorAttackLeft', 'audio/sfx_alligator_attack_left.mp3')


def getAlligatorAttackStraightSfx():
    return cacheSfx('alligatorAttackStraight', 'audio/sfx_alligator_attack_straight.mp3')


def getScorpionAttackLeftSfx():
    return cacheSfx('scorpionAttackLeft', 'audio/sfx_scorp_attack_left.mp3')


def getScorpionAttackBothSfx():
    return cacheSfx('scorpionAttackBoth', 'audio/sfx_scorpion_attack_both.mp3')


def getScorpionAttackTailStingSfx():
    return cacheSfx('scorpionAttackTailSting', 'audio/sfx_scorp_attack_tail.mp3')


def getScorpionPickUpHumanSfx():
    return cacheSfx('scorpionPickUpHuman', 'audio/sfx_scorp_pickup_human.mp3')


def getScorpionRearUpSfx():
    return cacheSfx('scorpionRearUp', 'audio/sfx_scorpion_rearup.mp3')


def getCrabAttackLeftSfx():
    return cacheSfx('crabAttackLeft', 'audio/sfx_crab_attack_left.mp3')


def getCrabAttackBothSfx():
    return cacheSfx('crabAttackBoth', 'audio/sfx_crab_attack_both.mp3')


def getFlytrapAttackASfx():
    return cacheSfx('flytrapAttackA', 'audio/sfx_flytrap_attack_a.mp3')


def getFlytrapAttackJabSfx():
    return cacheSfx('flytrapAttackJab', 'audio/sfx_flytrap_attack_jab.mp3')


def getFlytrapAttackFakeSfx():
    return cacheSfx('flytrapAttackFake', 'audio/sfx_flytrap_attack_fake.mp3')


def getFlytrapAttackSpitSfx():
    return cacheSfx('flytrapAttackSpit', 'audio/sfx_flytrap_spit.mp3')


def getMossmanAttackKickSfx():
    return cacheSfx('mossmanAttackKick', 'audio/sfx_mossman_kick.mp3')


def getMossmanAttackSlapSfx():
    return cacheSfx('mossmanAttackSlap', 'audio/sfx_mossman_slap_left.mp3')


def getMossmanAttackSwatSfx():
    return cacheSfx('mossmanAttackSwat', 'audio/sfx_mossman_swat_left.mp3')


def getMossmanAttackJumpSfx():
    return cacheSfx('mossmanAttackJump', 'audio/sfx_mossman_jump.mp3')


class MonsterMelee(Weapon.Weapon):
    vertex_list = [
        Vec4(0.0, 0.4, 0.0, 1.0),
        Vec4(0.0, 2.0, 0.0, 1.0),
        Vec4(-0.55, 2.95, 0.0, 1.0)]
    motion_color = [
        Vec4(0.1, 0.2, 0.4, 0.5),
        Vec4(0.25, 0.5, 1.0, 0.5),
        Vec4(0.5, 0.5, 0.6, 0.5)]
    
    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'monsterMelee')
        self.neutralAnim = 'idle'
        self.walkAnim = 'walk'
        self.strafeAnim = 'walk'
        self.painAnim = 'pain'

    def attachTo(self, av):
        pass

    def detachFrom(self, av):
        pass
    
    def delete(self):
        self.endAttack(None)
        self.removeTrail()
        Weapon.Weapon.delete(self)
    
    def changeStance(self, av):
        if av.avatarType.isA(AvatarTypes.Wasp) or av.avatarType.isA(AvatarTypes.AngryWasp):
            self.walkAnim = 'idle_flying'
            self.neutralAnim = 'idle_flying'
        
        av.setWalkForWeapon()

    def getDrawIval(self, av, ammoSkillId = 0, blendInT = 0.1, blendOutT = 0):
        if av.avatarType.isA(AvatarTypes.Bat) or av.avatarType.isA(AvatarTypes.VampireBat):
            av.show()
            track = Parallel(Func(self.attachTo, av), Func(self.changeStance, av), av.actorInterval('spawn', playRate = 1.0))
        else:
            track = Parallel(Func(self.attachTo, av), Func(self.changeStance, av))
        return track

    def getReturnIval(self, av, blendInT = 0, blendOutT = 0.1):
        
        def hideEnemy():
            av.hide()

        if av.avatarType.isA(AvatarTypes.Bat) or av.avatarType.isA(AvatarTypes.VampireBat):
            track = Parallel(Func(self.detachFrom, av), Func(self.changeStance, av), av.actorInterval('spawn', playRate = 1.0, startFrame = 100, endFrame = 20), Func(hideEnemy))
        else:
            track = Parallel(Func(self.detachFrom, av), Func(self.changeStance, av))
        return track
    
    def createTrail(self, target):
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
        


