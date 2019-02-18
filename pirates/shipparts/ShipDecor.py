from pirates.piratesbase.PiratesGlobals import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.shipparts import DecorDNA
from pirates.shipparts import ShipPart

class ShipDecor(NodePath, ShipPart.ShipPart):
    notify = directNotify.newCategory('ShipDecor')
    
    def __init__(self):
        ShipPart.ShipPart.__init__(self)
        NodePath.__init__(self, 'shipDecor')
        self.flash = None
        self.textures = None

    def delete(self):
        del self.dna
        self.clearTargetableCollisions()
    
    def loadModel(self, dna):
        if config.GetBool('disable-ship-geom', 0):
            return
        if self.prop:
            return
        self.dna = dna
        filePrefix = self.getPrefix(self.dna.decorType, self.dna.baseTeam)
        self.prop = loader.loadModelCopy(filePrefix[0])
        self.prop.flattenMedium()
        self.coll = self.prop.findAllMatches('**/collision*').asList()
        for c in self.coll:
            c.setTag('objType', str(PiratesGlobals.COLL_SHIPPART))
            c.setTag('propId', str(self.doId))
            c.setTag('cannonPass', str(1))
            c.setTag('shipId', str(self.shipId))
            c.node().setIntoCollideMask(BitMask32().allOff())
            c.node().setFromCollideMask(BitMask32().allOff())
            self.addTargetableCollision(c)

        self.setTargetBitmask(1)
        self.geom_High = NodePath('geom_High')
        self.geom_Medium = NodePath('geom_Medium')
        self.geom_Low = NodePath('geom_Low')
        geomHigh = self.prop.find('**/geometry_High')
        if not geomHigh.isEmpty():
            geomHigh.reparentTo(self.geom_High)
            geomHigh.flattenStrong()
        geomMed = self.prop.find('**/geometry_Medium')
        if not geomMed.isEmpty():
            geomMed.reparentTo(self.geom_Medium)
            geomMed.flattenStrong()
        self.propCollisions = self.prop.find('**/collisions')
        self.propCollisions.flattenStrong()
        self.loaded = True
    
    def unloadModel(self):
        if not self.prop:
            return
        
        if self.flash:
            self.flash.pause()
            self.flash = None
        
        if self.propCollisions:
            self.propCollisions.removeNode()
            self.propCollisions = None
        
        if self.prop:
            self.prop.removeNode()
            self.prop = None
        
        self.removeNode()

    def getPrefix(self, shipClass, team):
        filePrefix = None
        if team == PiratesGlobals.UNDEAD_TEAM:
            filePrefix = DecorDNA.SkelDecorDict.get(shipClass)
        elif team == PiratesGlobals.FRENCH_UNDEAD_TEAM or team == PiratesGlobals.SPANISH_UNDEAD_TEAM:
            filePrefix = DecorDNA.SkelDecorDict.get(shipClass)
        else:
            filePrefix = DecorDNA.DecorDict.get(shipClass)
        return filePrefix

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        if base.cr.wantSpecialEffects and self.ship:
            shipSplintersAEffect = ShipSplintersA.getEffect()
            if shipSplintersAEffect:
                shipSplintersAEffect.reparentTo(render)
                shipSplintersAEffect.setPos(self.ship, pos)
                shipSplintersAEffect.play()

        self.playFlash()
    
    def death(self):
        if self.prop != None:
            self.prop.hide()
            self.setTargetBitmask(0)

    def showBrokenState(self):
        pass
    
    def respawn(self):
        if self.prop != None:
            self.prop.show()
            if base.localAvatar.ship != self.ship:
                self.setTargetBitmask(1)

    def playFlash(self):
        if self.flash:
            self.flash.finish()
            self.flash = None
        
        self.flash = Sequence(Func(self.hideBaseTexture),
                              Func(self.prop.setColor, Vec4(1, 1, 0, 1)),
                              Wait(0.03),
                              Func(self.prop.setColor, Vec4(1, 0, 0, 1)),
                              Wait(0.03),
                              Func(self.prop.setColorOff),
                              Func(self.showBaseTexture),
                              Wait(0.1),
                              Func(self.hideBaseTexture),
                              Func(self.prop.setColor, Vec4(1, 1, 0, 1)),
                              Wait(0.03),
                              Func(self.prop.setColor, Vec4(1, 0, 0, 1)),
                              Wait(0.03),
                              Func(self.prop.setColorOff),
                              Func(self.showBaseTexture))
        self.flash.start()
    
    def hideBaseTexture(self):
        if not self.textures:
            self.textures = self.prop.findTexture('*')
        
        ts = self.prop.findAllTextureStages()
        if ts.getNumTextureStages():
            self.prop.setTextureOff(ts[0])
    
    def showBaseTexture(self):
        if self.textures:
            self.prop.setTexture(self.textures, 1)

