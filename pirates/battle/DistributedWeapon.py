# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.DistributedWeapon
from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.distributed import ClockDelta
from direct.directnotify import DirectNotifyGlobal
from pirates.distributed import DistributedInteractive
from pirates.piratesbase import PiratesGlobals
from pirates.effects.CannonSplash import CannonSplash
from pirates.effects.DirtClod import DirtClod
from pirates.effects.CannonExplosion import CannonExplosion
from pirates.effects.DustCloud import DustCloud
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.RockShower import RockShower
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.DustRing import DustRing
from pirates.effects.Fire import Fire
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.ShockwaveRing import ShockwaveRing
from pirates.effects.CameraShaker import CameraShaker
from pirates.ship import ShipGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
import WeaponGlobals
from WeaponBase import WeaponBase

class DistributedWeapon(WeaponBase, DistributedInteractive.DistributedInteractive):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWeapon')

    def __init__(self, cr):
        NodePath.__init__(self, 'weapon')
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        WeaponBase.__init__(self)
        self.ship = None
        self.av = None
        self.weaponSphereNodePath = None
        self.pendingDoMovie = None
        return

    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)
        WeaponBase.generate(self)

    def announceGenerate(self):
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        WeaponBase.announceGenerate(self)
        if __dev__ and base.config.GetBool('show-ai-cannon-targets', 0):
            self.tracker = loader.loadModelCopy('models/effects/explosion_sphere')
            self.tracker.reparentTo(render)
            self.tracker.setScale(30)

    def disable(self):
        if self.pendingDoMovie:
            base.cr.relatedObjectMgr.abortRequest(self.pendingDoMovie)
            self.pendingDoMovie = None
        DistributedInteractive.DistributedInteractive.disable(self)
        WeaponBase.disable(self)
        return

    def delete(self):
        DistributedInteractive.DistributedInteractive.delete(self)
        WeaponBase.delete(self)
        self.removeNode()

    def loadModel(self):
        return

    def getModel(self):
        return

    def startWeapon(self, av):
        pass

    def stopWeapon(self, av):
        pass

    def setMovie(self, mode, avId):

        def doMovie(av):
            if mode == WeaponGlobals.WEAPON_MOVIE_START:
                self.startWeapon(av)
            else:
                if mode == WeaponGlobals.WEAPON_MOVIE_STOP:
                    self.stopWeapon(av)
                else:
                    if mode == WeaponGlobals.WEAPON_MOVIE_CLEAR:
                        pass

        if self.pendingDoMovie:
            base.cr.relatedObjectMgr.abortRequest(self.pendingDoMovie)
            self.pendingDoMovie = None
        self.pendingDoMovie = base.cr.relatedObjectMgr.requestObjects([avId], eachCallback=doMovie, timeout=60)
        return

    def rejectInteraction(self):
        base.localAvatar.motionFSM.on()
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)
# okay decompiling .\pirates\battle\DistributedWeapon.pyc
