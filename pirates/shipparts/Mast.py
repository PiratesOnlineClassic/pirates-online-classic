import random
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.ship import ShipGlobals
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from pirates.piratesbase.PiratesGlobals import *
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.ShipDebris import ShipDebris
from pirates.effects.CannonSplash import CannonSplash
from pirates.effects.DustRing import DustRing
from pirates.effects.ProjectileArc import ProjectileArc
from pirates.effects.Fire import Fire
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.shipparts import MastDNA
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.shipparts import ShipPart
import copy

mastNetRiggingAnchor = {
    ShipGlobals.MAINMASTL1: 1,
    ShipGlobals.MAINMASTL2: 2,
    ShipGlobals.MAINMASTL3: 3,
    ShipGlobals.MAINMASTL4: 3,
    ShipGlobals.MAINMASTL5: 3,
    ShipGlobals.TRIMASTL1: 3,
    ShipGlobals.TRIMASTL2: 3,
    ShipGlobals.TRIMASTL3: 3,
    ShipGlobals.TRIMASTL4: 3,
    ShipGlobals.TRIMASTL5: 3,
    ShipGlobals.FOREMASTL1: 0,
    ShipGlobals.FOREMASTL2: 0,
    ShipGlobals.FOREMASTL3: 0,
    ShipGlobals.AFTMASTL1: 0,
    ShipGlobals.AFTMASTL2: 0,
    ShipGlobals.AFTMASTL3: 0,
    ShipGlobals.SKEL_MAINMASTL1_A: 0,
    ShipGlobals.SKEL_MAINMASTL2_A: 0,
    ShipGlobals.SKEL_MAINMASTL3_A: 0,
    ShipGlobals.SKEL_MAINMASTL4_A: 0,
    ShipGlobals.SKEL_MAINMASTL5_A: 0,
    ShipGlobals.SKEL_MAINMASTL1_B: 0,
    ShipGlobals.SKEL_MAINMASTL2_B: 0,
    ShipGlobals.SKEL_MAINMASTL3_B: 0,
    ShipGlobals.SKEL_MAINMASTL4_B: 0,
    ShipGlobals.SKEL_MAINMASTL5_B: 0,
    ShipGlobals.SKEL_TRIMASTL1: 0,
    ShipGlobals.SKEL_TRIMASTL2: 0,
    ShipGlobals.SKEL_TRIMASTL3: 0,
    ShipGlobals.SKEL_TRIMASTL4: 0,
    ShipGlobals.SKEL_TRIMASTL5: 0,
    ShipGlobals.SKEL_FOREMASTL1: 0,
    ShipGlobals.SKEL_FOREMASTL2: 0,
    ShipGlobals.SKEL_FOREMASTL3: 0,
    ShipGlobals.SKEL_AFTMASTL1: 0,
    ShipGlobals.SKEL_AFTMASTL2: 0,
    ShipGlobals.SKEL_AFTMASTL3: 0}
maximumMastHeights = [
    3,
    2,
    1,
    1]


class Mast(DirectObject.DirectObject, NodePath, ShipPart.ShipPart):
    notify = directNotify.newCategory('Mast')
    breakSfx1 = None
    breakSfx2 = None
    card = None

    def __init__(self, ship, cr):
        self.cr = cr
        ShipPart.ShipPart.__init__(self)
        NodePath.__init__(self, 'Mast')
        self.mastAnimDict = {}
        self.mastIval = None
        self.collMasts = {}
        self.actor = None
        self.mastsState = []
        self.flashIvals = {}
        self.mastTexture = None
        self.ship = ship
        self.sailLoc = []
        self.sails = {}
        self.flash = None
        self.rigging = None
        if self.breakSfx1 is None:
            Mast.breakSfx1 = loader.loadSfx('audio/mastBreak1.mp3')
            Mast.breakSfx2 = loader.loadSfx('audio/mastBreak2.mp3')
            Mast.card = loader.loadModel('models/textureCards/mastTextures')

    def delete(self):
        if self.mastIval:
            self.mastIval.pause()
            self.mastIval = None

        del self.prop
        for i in self.collMasts:
            del i

        del self.collMasts
        del self.mastAnimDict
        self.breakSfx1 = None
        del self.breakSfx1
        self.breakSfx2 = None
        del self.breakSfx2
        self.clearTargetableCollisions()

    def loadModel(self, dna):
        if config.GetBool('disable-ship-geom', 0):
            return

        if self.prop:
            return

        self.dna = dna
        id = ShipGlobals.getMastClassification(self.dna.mastType)[0]
        if id == ShipGlobals.MAINMAST:
            mastCategory = 0
        elif id == ShipGlobals.FOREMAST:
            mastCategory = 2
        elif id == ShipGlobals.AFTMAST:
            mastCategory = 3
        else:
            mastCategory = 1
        mastHeight = len(ShipGlobals.getMastStats(self.dna.mastType)['maxArrayHp'])
        self.mastsState = [
                              0] * mastHeight
        filePrefix = self.getPrefix(self.dna.mastType)
        (self.prop, self.locators) = ShipGlobals.getMast('%s%s_%s' % (filePrefix, mastHeight, self.dna.posIndex))
        textureType = MastDNA.TextureDict.get(self.dna.textureIndex)
        if textureType:
            self.mastTexture = self.card.find('**/' + textureType).findTexture('*')
        else:
            self.mastTexture = None
        self.propCollisions = NodePath(ModelNode('mast-%d' % self.dna.posIndex))

        try:
            for i in xrange(mastHeight):
                self.prop.play('Idle', partName='mast_%d_%d' % (i, self.dna.posIndex))
        except:
            self.notify.warning('failed call: self.prop.play("Idle")')

        if self.locators:
            self.locators.reparentTo(self.ship.root)
            self.locators.stash()

        self.geom_Low = self.prop.getLOD('low')
        self.geom_Medium = self.prop.getLOD('medium')
        self.geom_High = self.prop.getLOD('high')
        bounds = self.prop.getBounds()
        self.prop.setCenter(bounds.getApproxCenter())
        if self.mastTexture:
            self.replaceMastTexture(self.mastTexture, self.geom_High)
            self.replaceMastTexture(self.mastTexture, self.geom_Medium)
            self.replaceMastTexture(self.mastTexture, self.geom_Low)

        if self.dna.baseTeam not in [
            PiratesGlobals.UNDEAD_TEAM,
            PiratesGlobals.FRENCH_UNDEAD_TEAM,
            PiratesGlobals.SPANISH_UNDEAD_TEAM]:
            if self.dna.mastType >= ShipGlobals.MAINMASTL1 and self.dna.mastType <= ShipGlobals.TRIMASTL5:
                riggingPrefix = MastDNA.RiggingDict.get(self.dna.modelClass)
                self.rigging = ShipGlobals.getRigging(riggingPrefix + str(self.dna.posIndex))

        self.prop.reparentTo(self)
        self.loaded = True

    def unloadModel(self):
        if not self.prop:
            return

        if self.card:
            self.card.removeNode()
            self.card = None

        filePrefix = MastDNA.MastDict.get(self.dna.mastType)
        for i in self.flashIvals:
            if self.flashIvals[i]:
                self.flashIvals[i].pause()
                self.flashIvals[i] = None

        if self.prop:
            self.prop.cleanup()
            self.prop.removeNode()
            self.prop = None

        for anim in self.mastAnimDict:
            loader.unloadModel(filePrefix + 'mast_' + str(i) + anim[1])

        self.removeNode()

    def loadCollisions(self):
        if config.GetBool('disable-ship-geom', 0):
            return

        if self.collisions or self.isEmpty():
            return

        filePrefix = self.getPrefix(self.dna.mastType)
        self.collisions = loader.loadModel(filePrefix + 'zero_collisions')
        self.collisions.reparentTo(self.propCollisions)
        coll = self.collisions.findAllMatches('**/collision_*')
        for c in coll:
            c.setTag('objType', str(PiratesGlobals.COLL_SHIPPART))
            c.setTag('propId', str(self.doId))
            c.setTag('sailCode', str(1))
            c.setTag('shipId', str(self.shipId))
            self.addTargetableCollision(c)

        self.setTargetBitmask(1)
        mastHeight = len(ShipGlobals.getMastStats(self.dna.mastType)['maxArrayHp'])
        for i in range(mastHeight):
            currPrefix = filePrefix + 'mast_' + str(i) + '_'
            self.collMasts[i] = self.collisions.find('**/collision_mast_' + str(i))
            if self.collMasts[i] != self.collMasts[i].notFound():
                self.collMasts[i].setTag('cannonCode', str(i + 1))
                self.collMasts[i].setTag('sailCode', str(1))
            else:
                self.collMasts[i] = hidden

    def unloadCollisions(self):
        if not self.collisions:
            return

        if self.collisions.isEmpty():
            return

        if self.collisions:
            self.collisions.removeNode()
            self.collisions = None

    def setupMast(self):
        for i in range(len(self.mastsState)):
            state = self.mastsState[i]
            if state == 1:
                for j in range(i, len(self.mastsState)):
                    self.hideMast(j)
                break
            elif state == 0:
                self.restoreMast(i)

    def getPrefix(self, mastType):
        filePrefix = MastDNA.MastDict.get(mastType)
        return filePrefix

    def getFlatPrefix(self, mastType):
        filePrefix = MastDNA.MastFlatDict.get(mastType)
        return filePrefix

    def radians2degrees(self, radians):
        return radians / 0.0174532925

    def replaceMastTexture(self, texture, object):
        geom = object.find('**/+GeomNode').node()
        renderState = geom.getGeomState(0)
        texAttrib = renderState.getAttrib(TextureAttrib.getClassType())
        texAttrib = texAttrib.addOnStage(TextureStage.getDefault(), texture)
        renderState = renderState.addAttrib(texAttrib)
        geom.setGeomState(0, renderState)

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        if localAvatar.ship == self.ship:
            sfx = random.choice(self.woodBreakSfx)
            base.playSfx(sfx, node=self.ship, cutoff=2500)
        else:
            sfx = random.choice(self.distantBreakSfx)
            base.playSfx(sfx, node=self.ship, cutoff=2500)
        (cannonCode, hullCode, sailCode) = codes
        if self.cr and self.cr.wantSpecialEffects:
            if hullCode >= 1:
                index = hullCode - 1

            if WeaponGlobals.getSkillEffectFlag(skillId) & WeaponGlobals.EFFECT_FLAME:
                if hullCode >= 1:
                    index = hullCode - 1
                    fxParent = self.collMasts[index]
                else:
                    fxParent = render

    def death(self, index=None):
        if index != None:
            for i in range(random.randint(2, 4)):
                spawnPoint = self.locators.find('**/break_' + str(index) + ';+s')
                if self.cr and self.cr.wantSpecialEffects != 0:
                    shipDebrisEffect = ShipDebris.getEffect()
                    if shipDebrisEffect and not spawnPoint.isEmpty():
                        shipDebrisEffect.reparentTo(render)
                        shipDebrisEffect.setPosHpr(spawnPoint, 0, 0, 0, 0, 0, 0)
                        shipDebrisEffect.endPlaneZ = 0
                        shipDebrisEffect.play()

    def hideMast(self, index):
        mastHeight = len(ShipGlobals.getMastStats(self.dna.mastType)['maxArrayHp'])
        for i in range(index, mastHeight):
            self.prop.pose('Hidden', 1, partName='mast_%d_%d' % (i, self.dna.posIndex))
            self.disableCollisions(i)

        if index == 0:
            if self.rigging:
                self.rigging.hide()

    def showMast(self, index):
        self.prop.pose('Idle', 0, partName='mast_%d_%d' % (index, self.dna.posIndex))
        self.prop.update()
        if self.ship.sails.has_key(self.dna.posIndex):
            if self.ship.sails[self.dna.posIndex].has_key(index):
                self.ship.sails[self.dna.posIndex][index][0].respawn()

        if index == 0:
            if self.rigging:
                self.rigging.show()

        self.enableCollisions(index)

    def respawn(self, index):
        if self.mastIval:
            self.mastIval.finish()
            self.mastIval = None

        self.restoreMast(index)

    def setBreakAnim(self, index, animMultiplier=1.0):
        for i in range(index, 5):
            anim = 'break' + str(index) + 'A'
            if len(self.mastsState) - 1 >= i:
                if self.mastsState[i] == 0:
                    projDummy = ProjectileArc(wantColl=1)
                    projDummy.reparentTo(self.collMasts[i])
                    projDummy.bigSplash = 1
                    projDummy.startCollisions()
                    if self.mastIval:
                        self.mastIval.finish()

                    ival = Parallel(Func(base.playSfx, self.breakSfx1, node=self.ship, cutoff=3000),
                                    Sequence(Func(self.prop.play, anim, partName='mast_%d_%d' % (i, self.dna.posIndex)),
                                             Wait(10.0),
                                             Func(self.hideMast, index),
                                             Func(projDummy.destroy)))
                    ival.start()
                    self.mastIval = ival
                    self.mastsState[i] = 1

        if index == 0 or self.ship.modelClass < 4 and self.dna.posIndex == 0 and index < 2:
            self.breakRigging()

    def restoreMast(self, index):
        self.mastsState[index] = 0
        self.showMast(index)

    def disableCollisions(self, index):
        self.collMasts[index].setCollideMask(PiratesGlobals.TargetBitmask.allOff())

    def enableCollisions(self, index):
        self.collMasts[index].setCollideMask(PiratesGlobals.TargetBitmask | PiratesGlobals.WallBitmask)

    def breakRigging(self):
        if not self.rigging:
            return

        fadeOut = self.rigging.colorScaleInterval(1.0, Vec4(1.0, 1.0, 1.0, 0.0))
        self.riggingIval = Sequence(fadeOut, Func(self.rigging.hide))
        self.riggingIval.start()

    def addToShip(self):
        self.propCollisions.reparentTo(self.ship.modelCollisions)
        id = ShipGlobals.getMastClassification(self.dna.mastType)[0]
        if id == ShipGlobals.FOREMAST:
            locator = self.ship.locators.find('**/location_foremast;+s')
        elif id == ShipGlobals.MAINMAST:
            locator = self.ship.locators.find('**/location_mainmast_%s;+s' % self.dna.posIndex)
        elif id == ShipGlobals.AFTMAST:
            locator = self.ship.locators.find('**/location_aftmast;+s')

        lpos = locator.getPos(self.ship.root)
        lhpr = locator.getHpr(self.ship.root)
        lscl = locator.getScale(self.ship.root)
        self.geom_Low.setPos(lpos)
        self.geom_Low.setHpr(lhpr)
        self.geom_Low.setScale(lscl)
        self.geom_Medium.setPos(lpos)
        self.geom_Medium.setHpr(lhpr)
        self.geom_Medium.setScale(lscl)
        self.geom_High.setPos(lpos)
        self.geom_High.setHpr(lhpr)
        self.geom_High.setScale(lscl)
        self.propCollisions.setPos(lpos)
        self.propCollisions.setHpr(lhpr)
        self.propCollisions.setScale(lscl)
        self.propCollisions.reparentTo(self.ship.modelCollisions)
        self.propCollisions.flattenLight()
        if self.rigging:
            self.rigging.reparentTo(self.ship.modelGeom)

        self.prop.setLODNode(self.ship.lodRoot)
        ShipPart.ShipPart.addToShip(self)
