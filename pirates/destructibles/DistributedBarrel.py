from direct.distributed import DistributedObject
from direct.distributed.ClockDelta import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.destructibles import DistributedDestructibleObject
from pirates.effects import ShipSplintersA
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesbase.PiratesGlobals import *


class DistributedBarrel(DistributedDestructibleObject.DistributedDestructibleObject):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedBarrel')

    def __init__(self, cr):
        DistributedDestructibleObject.DistributedDestructibleObject.__init__(self, cr)
        NodePath.__init__(self)
        self.assign(hidden.attachNewNode('barrel'))
        self.Hp = 0
        self.maxHp = 0
        self.parentId = None
        self.HpDisplay = None
        self.prop = None
        self.modelType = 0

    def load(self):
        self.loadModel()
        self.displayHp()

    def loadModel(self):
        self.prop = loader.loadModel('models/props/barrel')
        self.coll = self.prop.findAllMatches('**/collision*') 
        for c in self.coll:
            self.curMask = c.node().getIntoCollideMask()
            c.setCollideMask(PiratesGlobals.AmmoBitmask | self.curMask)
            c.setTag('objType', str(PiratesGlobals.COLL_DESTRUCTIBLE))
            c.setTag('propId', str(self.doId))

        self.prop.reparentTo(self)

    def playDamage(self, pos):
        if base.cr.wantSpecialEffects:
            shipSplintersAEffect = ShipSplintersA.getEffect()
            if shipSplintersAEffect:
                shipSplintersAEffect.reparentTo(render)
                shipSplintersAEffect.setPos(pos)
                shipSplintersAEffect.play()

    def playDeath(self):
        if self.prop != None:
            self.prop.hide()
            for c in self.coll:
                c.setCollideMask(PiratesGlobals.AmmoBitmask.allOff())

    def respawn(self):
        if self.prop != None:
            self.prop.show()
            for c in self.coll:
                c.setCollideMask(PiratesGlobals.AmmoBitmask | self.curMask)
