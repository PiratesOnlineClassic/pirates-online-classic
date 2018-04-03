# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.shipparts.Window
import random
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from pirates.effects.WoodShards import WoodShards
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.Fire import Fire
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.shipparts import DecorDNA
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.shipparts import ShipPart

class Window(NodePath, ShipPart.ShipPart):
    __module__ = __name__
    notify = directNotify.newCategory('Window')
    glassBreakSfx = None

    def __init__(self):
        NodePath.__init__(self, 'window')
        ShipPart.ShipPart.__init__(self)
        self.flash = None
        self.textures = None
        if not self.glassBreakSfx:
            self.glassBreakSfx = (
             loader.loadSfx('audio/glass_break1.mp3'), loader.loadSfx('audio/glass_break2.mp3'), loader.loadSfx('audio/glass_break3.mp3'), loader.loadSfx('audio/explode-w-glass.mp3'))
        return

    def delete(self):
        del self.dna
        for i in self.glassBreakSfx:
            i = None

        del self.glassBreakSfx
        self.clearTargetableCollisions()
        return

    def loadModel(self, dna):
        if config.GetBool('disable-ship-geom', 0):
            return
        if self.prop:
            return
        self.dna = dna
        LOD = LODNode('windowLOD')
        LOD.addSwitch(100, 0)
        LOD.addSwitch(600, 100)
        lodnp = NodePath(LOD)
        lodnp.reparentTo(self)
        filePrefix = self.getPrefix(self.dna.decorType, self.dna.baseTeam)
        self.prop = loader.loadModelCopy(filePrefix[0])
        self.coll = self.prop.findAllMatches('**/collision*').asList()
        for c in self.coll:
            c.setTag('objType', str(PiratesGlobals.COLL_SHIPPART))
            c.setTag('propId', str(self.doId))
            c.setTag('shipId', str(self.shipId))
            c.node().setIntoCollideMask(BitMask32().allOff())
            c.node().setFromCollideMask(BitMask32().allOff())
            self.addTargetableCollision(c)

        self.setTargetBitmask(1)
        self.propCollisions = self.prop.find('**/collisions')
        if not self.propCollisions.isEmpty():
            self.propCollisions.flattenStrong()
            self.propCollisions.setName('window-%d' % self.dna.posIndex)
        self.prop.flattenStrong()
        self.geom_High = self.prop.find('**/geometry_High/+GeomNode')
        if self.geom_High.isEmpty():
            self.geom_High = None
        self.geom_Medium = self.prop.find('**/geometry_Medium/+GeomNode')
        if self.geom_Medium.isEmpty():
            self.geom_Medium = None
        self.geom_Low = self.prop.find('**/geometry_Medium/+GeomNode')
        if self.geom_Low.isEmpty():
            self.geom_Low = None
        self.holeCard = loader.loadModelCopy('models/effects/battleEffects')
        self.holeTex = self.holeCard.find('**/effectSailHoleA').findTexture('*')
        self.holeTex.setWrapU(Texture.WMClamp)
        self.holeTex.setWrapV(Texture.WMClamp)
        self.holeLayer = TextureStage('holeLayer')
        self.holeLayer.setMode(TextureStage.MModulate)
        self.holeLayer.setSort(20)
        self.holeLayer.setTexcoordName('holeUV')
        self.loaded = True
        return

    def unloadModel(self):
        if not self.prop:
            return
        if self.flash:
            self.flash.pause()
            self.flash = None
        if self.prop:
            self.prop.removeNode()
            self.prop = None
        if not self.propCollisions.isEmpty():
            self.propCollisions.removeNode()
            self.propCollisions = None
        if self.holeCard:
            self.holeCard.removeNode()
            self.holeCard = None
        self.holeTex = None
        self.removeNode()
        return

    def getPrefix(self, shipClass, team):
        filePrefix = None
        if team == PiratesGlobals.UNDEAD_TEAM:
            filePrefix = DecorDNA.SkelDecorDict.get(shipClass)
        else:
            if team == PiratesGlobals.FRENCH_UNDEAD_TEAM or team == PiratesGlobals.SPANISH_UNDEAD_TEAM:
                filePrefix = DecorDNA.SkelDecorDict.get(shipClass)
            else:
                filePrefix = DecorDNA.DecorDict.get(shipClass)
        return filePrefix

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        print 'Window Sound'
        sfx = random.choice(self.glassBreakSfx)
        base.playSfx(sfx, node=self, cutoff=2000)
        if base.cr.wantSpecialEffects and self.ship:
            shipSplintersAEffect = ShipSplintersA.getEffect()
            if shipSplintersAEffect:
                shipSplintersAEffect.reparentTo(render)
                shipSplintersAEffect.setPos(self.ship.transNode, pos)
                shipSplintersAEffect.play()
            woodShardsEffect = WoodShards.getEffect()
            if woodShardsEffect:
                woodShardsEffect.reparentTo(render)
                woodShardsEffect.setPos(self.ship, self.getPos(self.ship))
                woodShardsEffect.setHpr(self.ship, self.getHpr(self.ship))
                woodShardsEffect.play()
        self.playBreak()
        self.playFlash()

    def playBreak(self):
        pass

    def death(self):
        if self.prop != None:
            self.setTargetBitmask(0)
        return

    def showBrokenState(self):
        pass

    def respawn(self):
        if self.prop != None:
            self.prop.show()
            if base.localAvatar.ship != self.ship:
                self.setTargetBitmask(1)
        return

    def playFlash(self):
        if self.flash:
            self.flash.finish()
            self.flash = None
        self.flash = Sequence(Func(self.hideBaseTexture), Func(self.prop.setColor, Vec4(1, 1, 0, 1)), Wait(0.03), Func(self.prop.setColor, Vec4(1, 0, 0, 1)), Wait(0.03), Func(self.prop.setColorOff), Func(self.showBaseTexture), Wait(0.1), Func(self.hideBaseTexture), Func(self.prop.setColor, Vec4(1, 1, 0, 1)), Wait(0.03), Func(self.prop.setColor, Vec4(1, 0, 0, 1)), Wait(0.03), Func(self.prop.setColorOff), Func(self.showBaseTexture))
        self.flash.start()
        return

    def hideBaseTexture(self):
        if not self.textures:
            self.textures = self.prop.findTexture('*')
        ts = self.prop.findAllTextureStages()
        if ts.getNumTextureStages():
            self.prop.setTextureOff(ts[0])

    def showBaseTexture(self):
        if self.textures:
            self.prop.setTexture(self.textures, 1)
# okay decompiling .\pirates\shipparts\Window.pyc
