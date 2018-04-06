# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.Weapon
import WeaponGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from pandac.PandaModules import *
from pirates.effects.SmokeCloud import SmokeCloud


class Weapon(NodePath):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('Weapon')
    models = {}
    icons = {}
    walkAnim = 'walk'
    runAnim = 'run'
    walkBackAnim = 'walk'
    neutralAnim = 'idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    strafeDiagLeftAnim = 'run_diagonal_left'
    strafeDiagRightAnim = 'run_diagonal_right'
    strafeRevDiagLeftAnim = 'walk_back_diagonal_left'
    strafeRevDiagRightAnim = 'walk_back_diagonal_right'
    fallGroundAnim = 'fall_ground'
    fallWaterAnim = 'fall_ground'
    spinLeftAnim = 'spin_left'
    spinRightAnim = 'spin_right'
    painAnim = 'boxing_hit_head_right'

    def __init__(self, itemId=None, name='weapon'):
        NodePath.__init__(self, name)
        self.itemId = itemId
        self.effect = None
        self.effect2 = None
        self.effectActor = None
        self.chargeSound = None
        self.chargeLoopSound = None
        self.chargeSoundSequence = None
        self.loadModel()
        self.motion_trail = None
        self.spinBlur = None
        self.ammoSkillId = 0
        return

    def delete(self):
        self.removeNode()

    def loadModel(self):
        pass

    def getWalkForWeapon(self, av):
        return [
         self.walkAnim, self.runAnim, self.walkBackAnim, self.neutralAnim, self.strafeLeftAnim, self.strafeRightAnim, self.strafeDiagLeftAnim, self.strafeDiagRightAnim, self.strafeRevDiagLeftAnim, self.strafeRevDiagRightAnim, self.fallGroundAnim, self.fallWaterAnim, self.spinLeftAnim, self.spinRightAnim]

    def getAutoAttackIval(self, av, blendInT, blendOutT):
        return

    def getAttackIval(self, av, blendInT, blendOutT):
        return

    def getDrawIval(self, av, ammoSkillId, blendInT, blendOutT):
        return

    def getReturnIval(self, av, blendInT, blendOutT):
        return

    def getNeutralIval(self, av, blendInT, blendOutT):
        return

    def getAmmoChangeIval(self, av, skillId, ammoSkillId, charge, target=None):
        return

    def updateItemId(self, itemId):
        self.itemId = itemId
        if hasattr(self, 'prop'):
            self.prop.removeNode()
            self.loadModel()

    def attachTo(self, av):
        if not self.isEmpty():
            if av.rightHandNode:
                self.reparentTo(av.rightHandNode)
            else:
                self.notify.warning('av.rightHandNode is None, just reparenting to av')
                self.reparentTo(av)

    def detachFrom(self, av):
        if not self.isEmpty():
            self.detachNode()

    def hideWeapon(self):
        if not self.isEmpty():
            self.hide()

    def showWeapon(self):
        if not self.isEmpty():
            self.show()

    def beginAttack(self, av):
        if self.motion_trail:
            self.motion_trail.beginTrail()

    def endAttack(self, av):
        if self.motion_trail:
            self.motion_trail.endTrail()

    def setTrailLength(self, time):
        if self.motion_trail:
            self.motion_trail.setTimeWindow(time)

    def showSpinBlur(self):
        if self.spinBlur:
            if not self.spinBlur.isEmpty():
                self.spinBlur.setColorScale(self.getBlurColor() / 2.0)
                self.spinBlur.show()

    def hideSpinBlur(self):
        if self.spinBlur:
            if not self.spinBlur.isEmpty():
                self.spinBlur.hide()

    def hideMouse(self, av):
        pass

    def playSkillSfx(self, skillId, node, startTime=0):
        if self.getName() not in ['sword', 'pistol', 'daggers', 'grenade']:
            return
        sfx = self.skillSfxs.get(skillId)
        if sfx:
            base.playSfx(sfx, node=node, cutoff=100, time=startTime)

    def getModel(self, itemId):
        model = self.models.get(itemId)
        if not model:
            base.buildAssets()
            model = self.models.get(itemId)
        model = model.copyTo(hidden)
        model.detachNode()
        return model

    def getIcon(self, itemId):
        model = self.icons[itemId]
        model = model.copyTo(hidden)
        model.detachNode()
        return model

    @classmethod
    def setupAssets(cls):
        for item in cls.modelTypes.keys():
            data = cls.modelTypes[item]
            model = loader.loadModel(data[0])
            try:
                model.flattenLight()
            except AttributeError:
                cls.notify.error('Could not load %s model: %s' % (cls.__name__, data[0]))
            else:
                cls.models[item] = model

        cls.setupSounds()

    @classmethod
    def setupSounds(cls):
        pass

    def getAnimState(self, animState):
        return animState

    def getEffectColor(self, itemId=None):
        return Vec4(1, 1, 1, 1)

    def getBlurColor(self):
        return Vec4(1, 1, 1, 1)
# okay decompiling .\pirates\battle\Weapon.pyc
