# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.shipparts.Wheel
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.shipparts import ShipPart
from pirates.ship import ShipGlobals

class Wheel(NodePath, ShipPart.ShipPart):
    __module__ = __name__
    notify = directNotify.newCategory('Wheel')

    def __init__(self):
        NodePath.__init__(self, 'wheel')
        ShipPart.ShipPart.__init__(self)
        self.flash = None
        self.prop = None
        return

    def delete(self):
        del self.dna

    def loadModel(self, shipClass):
        if config.GetBool('disable-ship-geom', 0):
            return
        if self.prop:
            return
        if shipClass == ShipGlobals.BLACK_PEARL:
            self.prop = loader.loadModelCopy('models/shipparts/wheel_bp')
        else:
            self.prop = loader.loadModelCopy('models/shipparts/wheel')
        self.propCollisions = NodePath(ModelNode('Wheel-%d' % self.doId))
        self.geom_High = self.prop.find('**/wheel_high')
        self.geom_Medium = self.prop.find('**/wheel_med')
        self.geom_Low = self.prop.find('**/wheel_low')
        self.propCollisions = self.prop.find('**/collision')
        self.loaded = True

    def unloadModel(self):
        if not self.prop:
            return
        if self.propCollisions:
            self.propCollisions.removeNode()
            self.propCollisions = None
        if self.prop:
            self.prop.removeNode()
            self.prop = None
        self.removeNode()
        return

    def addToShip(self):
        self.propCollisions.reparentTo(self.ship.modelCollisions)
        ShipPart.ShipPart.addToShip(self)
# okay decompiling .\pirates\shipparts\Wheel.pyc
