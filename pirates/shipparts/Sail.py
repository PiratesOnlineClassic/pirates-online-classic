import random
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.actor import Actor
from direct.fsm import FSM
from direct.fsm import State
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.ship import ShipGlobals
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from pirates.effects.Fire import Fire
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.shipparts import MastDNA
from pirates.shipparts import SailDNA
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.shipparts import ShipPart
from pirates.shipparts import SplattableObject
NavySailDict = {
    0: [
        2,
        1,
        1,
        2],
    1: [
        2,
        1,
        2,
        1]}
teamToLetter = [
    '_a_',
    '_b_',
    '_c_']

class Sail(NodePath, ShipPart.ShipPart):
    notify = directNotify.newCategory('Sail')
    card = None
    holeCard = None
    logoCard = None
    sailTearSfx = None

    def __init__(self, ship, cr):
        self.cr = cr
        NodePath.__init__(self, 'sail')
        ShipPart.ShipPart.__init__(self)
        self.navyColors = None
        self.riggingTexture = None
        self.logoOverride = None
        self.stats = None
        self.sailFSM = None
        self.sailActor = None
        self.currAnim = None
        self.currPrefix = None
        self.ship = ship
        self.destructIndex = None
        self.SailAnimDict = {}
        self.alreadyPlayed = 0
        self.sailGeom = None
        self.geom = None
        self.projScreen = None
        self.projNode = None
        self.flash = None
        self.flashState = None
        self.holeLocations = []
        self.sailTexture = None
        self.logoTexture = None
        if not self.sailTearSfx:
            self.sailTearSfx = (loader.loadSfx('audio/x_impact_sail.mp3'),)

        if not self.logoCard:
            Sail.setupTextures()

    @classmethod
    def setupTextures(cls):
        if not cls.logoCard and launcher.getPhaseComplete(3):
            cls.card = loader.loadModel('models/textureCards/sailTextures')
            cls.holeCard = loader.loadModel('models/effects/battleEffects')
            cls.logoCard = loader.loadModel('models/textureCards/sailLogo')

    def delete(self):
        if self.cr:
            base.textureFlattenMgr.clearSail(self)

        for i in self.sailTearSfx:
            i = None

        del self.sailTearSfx
        if hasattr(self, 'sailFSM'):
            if self.sailFSM:
                self.sailFSM.cleanup()

            del self.sailFSM

        if hasattr(self, 'SailAnimDict'):
            del self.SailAnimDict

        self.clearTargetableCollisions()
        self.sailActor.cleanup()
        self.ship = None
        ShipPart.ShipPart.destroy(self)

    def load(self):
        self.createProp()
        self.doReparent()

    def loadModel(self, dna):
        if config.GetBool('disable-ship-geom', 0):
            return

        if self.prop:
            return

        self.dna = dna
        filePrefix = self.getPrefix(self.dna.mastType)
        if self.dna.sailType == ShipGlobals.FLAG:
            fileSuffix = 'flag'
        else:
            fileSuffix = 'sail_' + str(self.dna.posIndex)
        self.currPrefix = filePrefix
        self.prop = self.attachNewNode('prop')
        self.propCollisions = self.ship.modelCollisions.attachNewNode(ModelNode('sail-%d-%d' % (self.dna.mastPosIndex, self.dna.posIndex)))
        textureType = SailDNA.SailTextureDict.get(self.dna.textureIndex)
        if textureType and self.card:
            self.sailTexture = self.card.find('**/%s' % textureType).findTexture('*')

        fileName = SailDNA.LogoDict.get(self.dna.logoIndex)
        if fileName:
            self.logoTexture = self.logoCard.find('**/%s' % fileName).findTexture('*')
            self.logoTexture.setMinfilter(Texture.FTLinearMipmapLinear)
            self.logoTexture.setMagfilter(Texture.FTLinear)
            if self.dna.logoIndex != 201:
                self.logoTexture.setWrapU(Texture.WMClamp)
                self.logoTexture.setWrapV(Texture.WMClamp)

        self.baseLayer = TextureStage('baseLayer')
        self.baseLayer.setSort(5)
        self.baseLayer.setCombineRgb(TextureStage.CMModulate, TextureStage.CSConstant, TextureStage.COSrcColor, TextureStage.CSTexture, TextureStage.COSrcColor)
        self.baseLayer.setCombineAlpha(TextureStage.CMModulate, TextureStage.CSConstant, TextureStage.COSrcAlpha, TextureStage.CSTexture, TextureStage.COSrcAlpha)
        self.baseLayer.setColor(VBase4(1.0, 1.0, 1.0, 1.0))
        self.logoLayer = TextureStage('logoLayer')
        self.logoLayer.setCombineRgb(TextureStage.CMModulate, TextureStage.CSPrevious, TextureStage.COSrcColor, TextureStage.CSTexture, TextureStage.COSrcColor)
        self.logoLayer.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSPrevious, TextureStage.COSrcAlpha)
        self.logoLayer.setSort(12)
        self.logoLayer.setTexcoordName('uvLogo')
        self.blendTs = TextureStage('blendTs')
        self.blendTs.setCombineRgb(TextureStage.CMModulate, TextureStage.CSPrimaryColor, TextureStage.COSrcColor, TextureStage.CSPrevious, TextureStage.COSrcColor)
        self.blendTs.setCombineAlpha(TextureStage.CMModulate, TextureStage.CSPrimaryColor, TextureStage.COSrcAlpha, TextureStage.CSPrevious, TextureStage.COSrcAlpha)
        self.blendTs.setSort(30)
        self.holeLayer = TextureStage('holeLayer')
        self.holeLayer.setMode(TextureStage.MModulate)
        self.holeLayer.setSort(25)
        self.holeLayer.setTexcoordName('uvSplat')
        self.holeTex = self.holeCard.find('**/effectSailHoleA').findTexture('*')
        self.holeTex.setWrapU(Texture.WMClamp)
        self.holeTex.setWrapV(Texture.WMClamp)
        self.holeTex2 = self.holeCard.find('**/effectSailHoleB').findTexture('*')
        self.holeTex2.setWrapU(Texture.WMClamp)
        self.holeTex2.setWrapV(Texture.WMClamp)
        self.breakTex = self.holeCard.find('**/effectHullBreach').findTexture('*')
        self.breakTex.setWrapU(Texture.WMClamp)
        self.breakTex.setWrapV(Texture.WMClamp)
        self.blankTex = self.holeCard.find('**/hullBlank').findTexture('*')
        self.blankTex.setMinfilter(Texture.FTLinearMipmapLinear)
        self.blankTex.setMagfilter(Texture.FTLinear)
        if self.dna.sailType == ShipGlobals.FLAG:
            fileSuffix = 'flag'
        else:
            fileSuffix = 'sail_' + str(self.dna.posIndex)
        filePrefix = self.currPrefix
        self.sailActor = Actor.Actor()
        for anim in SailDNA.DefaultAnimDict:
            self.SailAnimDict[anim[0]] = filePrefix + anim[1] + '_new'

        for i in range(self.dna.posIndex + 2):
            animName = 'break' + str(i) + 'A'
            self.SailAnimDict[animName] = filePrefix + animName + '_new'

        self.sailActor.loadModel(filePrefix + fileSuffix + '_h')
        self.sailActor.loadAnims(self.SailAnimDict)
        sailNodePrefix = 'sail_%d' % self.dna.posIndex
        self.sailActor.makeSubpart('mast', [
            'def_mast_base',
            'def_mast_0',
            'def_mast_1'], [])
        self.sailActor.setSubpartsComplete(True)
        self.sailActor.findAllMatches('**/+ModelNode').detach()
        if self.dna.baseTeam == PiratesGlobals.PLAYER_TEAM:
            self.sailActor.findAllMatches('**/%s_b_high' % sailNodePrefix).detach()
            self.sailActor.findAllMatches('**/%s_c_high' % sailNodePrefix).detach()
        elif self.dna.baseTeam == PiratesGlobals.NAVY_TEAM:
            self.sailActor.findAllMatches('**/%s_a_high' % sailNodePrefix).detach()
            self.sailActor.findAllMatches('**/%s_c_high' % sailNodePrefix).detach()
        elif self.dna.baseTeam == PiratesGlobals.TRADING_CO_TEAM:
            self.sailActor.findAllMatches('**/%s_a_high' % sailNodePrefix).detach()
            self.sailActor.findAllMatches('**/%s_b_high' % sailNodePrefix).detach()

        self.sailActor.flattenStrong()
        self.character = self.sailActor.find('**/+Character')
        self.sailGeom = self.sailActor.find('**/+GeomNode')
        self.sailGeom.setTransparency(1)
        self.sailGeom.flattenStrong()
        self.sailGeom.node().setPreserved(True)
        if self.dna.baseTeam == PiratesGlobals.NAVY_TEAM:
            self.addNavyColors(random.choice(NavySailDict))

        self.initDestruction()
        self.sailFSM = SailFSM(self)
        self.sailFSM.parentDoId = self.doId
        if self.currAnim:
            self.setAnimState(self.currAnim)

        if config.GetBool('enable-sail-colls-in-port', 0):
            self.enableCollisions()

        self.loaded = True
        self.sailGeom.setTexture(self.holeLayer, self.blankTex)

    def setLogo(self, logoIndex):
        if logoIndex != self.logoOverride:
            self.logoOverride = logoIndex
            if logoIndex == None:
                fileName = SailDNA.LogoDict.get(self.dna.logoIndex)
            else:
                fileName = SailDNA.LogoDict.get(logoIndex)
            if fileName:
                self.logoTexture = self.logoCard.find('**/%s' % fileName).findTexture('*')
                if logoIndex not in [210, 211]:
                    self.logoTexture.setMinfilter(Texture.FTLinearMipmapLinear)
                    self.logoTexture.setMagfilter(Texture.FTLinear)
                else:
                    self.logoTexture.setMinfilter(Texture.FTNearest)
                    self.logoTexture.setMagfilter(Texture.FTNearest)
                if logoIndex != 201:
                    self.logoTexture.setWrapU(Texture.WMClamp)
                    self.logoTexture.setWrapV(Texture.WMClamp)

            else:
                self.logoTexture = None
            self.initDestruction()

    def unloadModel(self):
        if not self.prop:
            return

        if self.dna.sailType == ShipGlobals.FLAG:
            fileSuffix = 'flag'
        else:
            fileSuffix = 'sail_' + str(self.dna.posIndex)
        filePrefix = self.currPrefix
        if self.flash:
            self.flash.pause()
            self.flash = None

        if self.prop:
            self.prop.removeNode()
            self.prop = None

        self.removeNode()

    def loadLow(self):
        pass

    def unloadLow(self):
        if not self.sailActor:
            return

        if self.dna.sailType == ShipGlobals.FLAG:
            fileSuffix = 'flag'
        else:
            fileSuffix = 'sail_' + str(self.dna.posIndex)
        filePrefix = self.currPrefix
        if self.sailFSM.ival:
            self.sailFSM.ival.pause()
            self.sailFSM.ival = None

        for anim in SailDNA.DefaultAnimDict:
            loader.unloadModel(filePrefix + anim[1])

        if self.sailActor:
            self.sailActor.cleanup()
            self.sailActor.removeNode()
            self.sailActor = None

    def loadCollisions(self):
        if config.GetBool('disable-ship-geom', 0):
            return
        if self.collisions:
            return
        if self.isEmpty() or not self.prop:
            return
        if self.dna.sailType == ShipGlobals.FLAG:
            fileSuffix = 'flag'
        else:
            fileSuffix = 'sail_' + str(self.dna.posIndex)
        filePrefix = self.currPrefix
        self.collisions = loader.loadModel(filePrefix + 'zero_coll_' + fileSuffix)
        self.collisions.reparentTo(self.propCollisions)
        self.coll = self.collisions.findAllMatches('**/collision*')
        for c in self.coll:
            c.setTag('objType', str(PiratesGlobals.COLL_SHIPPART))
            c.setTag('propId', str(self.doId))
            c.setTag('shipId', str(self.shipId))
            c.setTag('cannonPass', str(1))
            c.setTag('sailCode', str(1))
            self.addTargetableCollision(c)

        self.setTargetBitmask(1)
        if not config.GetBool('enable-sail-colls-in-port', 0):
            if self.sailFSM:
                if self.sailFSM.state == 'TiedUp' or self.sailFSM.state == 'Falling' or self.sailFSM.state == 'Dead' or self.sailFSM.state == 'Rolldown' or self.sailFSM.state == 'Rollup':
                    self.disableCollisions()

    def unloadCollisions(self):
        if self.collisions:
            self.collisions.removeNode()
            self.collisions = None

    def getPrefix(self, mastType):
        filePrefix = MastDNA.MastDict.get(mastType)
        return filePrefix

    def cutGeomTextureStates(self, geomNode, excludedStages = []):
        numGeoms = geomNode.getNumGeoms()
        finalPacket = []
        for i in xrange(numGeoms):
            geomState = geomNode.getGeomState(i)
            attrib = geomState.getAttrib(TextureAttrib.getClassType())
            finalPacket.append(attrib)
            geomNode.setGeomState(i, geomState.setAttrib(TextureAttrib.make()))

        return finalPacket

    def pasteGeomTextureStates(self, geomNode, attribList):
        for i in xrange(geomNode.getNumGeoms()):
            gs = geomNode.getGeomState(i).setAttrib(attribList[i])
            geomNode.setGeomState(i, gs)

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker):
        if self.cr and self.cr.wantSpecialEffects:
            pass
        self.alreadyPlayed = 0
        if self.dna.baseTeam not in [
            PiratesGlobals.UNDEAD_TEAM,
            PiratesGlobals.FRENCH_UNDEAD_TEAM,
            PiratesGlobals.SPANISH_UNDEAD_TEAM]:
            self.playHoleSplat(pos, normal, ammoSkillId)

    def resetFlashing(self):
        if self.flashState:
            self.showBaseTexture()
            self.flashState = 0

    def playFlash(self):
        if self.flash:
            self.flash.finish()

        self.resetFlashing()
        self.flash = Sequence(Func(self.hideBaseTexture), Func(self.sailActor.setColor, Vec4(1, 1, 0, 1)), Wait(0.03), Func(self.sailActor.setColor, Vec4(1, 0, 0, 1)), Wait(0.03), Func(self.sailActor.setColorOff), Func(self.showBaseTexture), Wait(0.1), Func(self.hideBaseTexture), Func(self.sailActor.setColor, Vec4(1, 1, 0, 1)), Wait(0.03), Func(self.sailActor.setColor, Vec4(1, 0, 0, 1)), Wait(0.03), Func(self.sailActor.setColorOff), Func(self.showBaseTexture))
        self.flash.start()

    def setProjScreen(self, projScreen):
        self.projScreen = projScreen
        self.projNode = projScreen.node()

    def initDestruction(self):
        if not self.sailActor:
            return

        if self.sailTexture:
            sailNode = self.sailGeom.node()
            foundState = False
            geomIndex = 0
            geomState = None
            texAttrib = None
            if self.destructIndex is None:
                for i in xrange(sailNode.getNumGeoms()):
                    geomState = sailNode.getGeomState(i)
                    geomIndex = i
                    texAttrib = geomState.getAttrib(TextureAttrib.getClassType())
                    defaultTex = texAttrib.getOnTexture(TextureStage.getDefault())
                    if defaultTex:
                        if defaultTex.getName() != 'ab_ship_rigging_alpha':
                            foundState = True
                            break

                if not foundState:
                    self.notify.warning("destruction wasn't setup for sail!")

                self.destructIndex = geomIndex
            else:
                geomState = sailNode.getGeomState(self.destructIndex)
                texAttrib = geomState.getAttrib(TextureAttrib.getClassType())
            texAttrib = texAttrib.removeOnStage(TextureStage.getDefault())
            texAttrib = texAttrib.removeOnStage(self.logoLayer)
            texAttrib = texAttrib.addOnStage(self.baseLayer, self.sailTexture)
            texAttrib = texAttrib.addOnStage(self.blendTs, self.blankTex)
            if self.logoTexture:
                texAttrib = texAttrib.addOnStage(self.logoLayer, self.logoTexture)
                if self.dna.logoIndex == 201:
                    val = random.uniform(0, 360)
                    r = Mat4.rotateMat(val, Vec3(0, 0, 1))
                    s = Mat4.scaleMat(Vec3(1.7, 1, 1.7))
                    tma = TexMatrixAttrib.make()
                    tma = tma.addStage(self.logoLayer, TransformState.makeMat(r * s))
                    geomState = geomState.addAttrib(tma)

            geomState = geomState.addAttrib(texAttrib)
            sailNode.setGeomState(self.destructIndex, geomState)

    def playHoleSplat(self, pos, normal, ammoSkillId):
        self.notify.debug('START POKE HOLE')
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
            if self.cr and self.cr.wantSpecialEffects and self.destructIndex is not None:
                holeCount = base.textureFlattenMgr.addSail(self)
                t = TextureStage('sailHoleStage-%s-%s' % (self.dna.posIndex, holeCount))
                t.setMode(TextureStage.MModulate)
                t.setSort(27)
                t.setTexcoordName('sailHole-%s-%s' % (self.dna.posIndex, holeCount))
                n = render.attachNewNode('dummy')
                n.lookAt(Point3(normal))
                hpr = n.getHpr()
                n.removeNode()
                del n
                hole = self.ship.attachNewNode('hole')
                hole.setPos(pos)
                hole.setHpr(render, hpr[0], hpr[1], 0)
                self.holeLocations.append(('3d', [
                    pos[0],
                    pos[1],
                    pos[2],
                    hpr[0],
                    hpr[1]]))
                holeSize = ShipGlobals.getHoleSizes(self.dna.mastType)[0]
                l = OrthographicLens()
                if ammoSkillId == InventoryType.CannonChainShot:
                    l.setFilmSize(3 * holeSize, 5 * holeSize)
                else:
                    l.setFilmSize(holeSize, holeSize)
                lens = LensNode('lens')
                lens.setLens(l)
                holeLocation = hole.attachNewNode(lens)
                if ammoSkillId == InventoryType.CannonChainShot:
                    self.sailGeom.setTexture(t, self.holeTex2)
                else:
                    self.sailGeom.setTexture(t, self.holeTex)
                self.projNode.setProjector(holeLocation)
                self.projNode.setTexcoordName('sailHole-%s-%s' % (self.dna.posIndex, holeCount))
                self.projNode.recompute()
                sfx = random.choice(self.sailTearSfx)
                base.playSfx(sfx, node = self.sailGeom, cutoff = 2000)
                del t
                hole.removeNode()
                del hole
                del l
                del lens
                holeLocation.removeNode()
                del holeLocation
                self.notify.debug('FINISHED POKE HOLE')

    def playBreak(self):
        self.notify.debug('START PLAY BREAK')
        if self.cr and self.cr.wantSpecialEffects:
            t = TextureStage('t')
            t.setMode(TextureStage.MModulate)
            t.setSort(200)
            self.sailActor.setTexture(t, self.breakTex)
            self.sailActor.setTexScale(t, 0.8, 0.8)
            if self.flash:
                self.flash.pause()

            cutStates = SplattableObject.cutGeomTextureStates(self.sailGeom.node(), ['holeLayer'])
            self.sailGeom.flattenMultitex(useGeom = 0, target = self.holeLayer)
            holeTex = self.sailGeom.findTexture(self.holeLayer)
            SplattableObject.pasteGeomTextureStates(self.sailGeom.node(), cutStates)
            self.sailGeom.setTexture(self.holeLayer, holeTex)
            if self.flash:
                self.flash.resume()

            del t

    def add2dHole(self, u, v):
        pass

    def death(self):
        self.propCollisions.stash()
        self.hideSail()

    def respawn(self):
        self.sailGeom.setTexture(self.holeLayer, self.blankTex)
        self.propCollisions.unstash()
        self.showSail()
        if self.sailFSM.state not in ('Idle', 'Rolldown', 'Billow'):
            self.sailFSM.demand('TiedUp')

    def hideSail(self):
        self.sailGeom.hide()
        self.disableCollisions()

    def showSail(self):
        self.sailGeom.show()
        self.enableCollisions()

    def disableCollisions(self):
        self.unloadCollisions()

    def enableCollisions(self):
        self.loadCollisions()

    def hideBaseTexture(self):
        pass

    def showBaseTexture(self):
        self.notify.debug('SHOW TEX STAGE')
        if self.cr and self.cr.config.GetBool('want-hires-destruction', 1) is 0:
            self.sailActor.flattenMultitex(useGeom = 0, target = self.holeLayer)

    def copyMultitexLayer(self, sourcePanel, targetPanel):
        if not sourcePanel or not targetPanel:
            return 0

        ts = sourcePanel.findTextureStage('holeLayer')
        if ts:
            tex = sourcePanel.findTexture(ts)
            if tex:
                targetPanel.setTexture(self.holeLayer, tex, 1)
                return 1

        return 0

    def addNavyColors(self, config):
        self.navyColors = config
        for i in range(4):
            sailquad = self.sailActor.find('**/sail_' + str(self.dna.posIndex) + '_quad_' + str(i) + '_high')
            if not sailquad.isEmpty():
                self.colorateQuad(sailquad, config, i)

            sailquad = self.sailActor.find('**/sail_' + str(self.dna.posIndex) + '_quad_' + str(i) + '_med')
            if not sailquad.isEmpty():
                self.colorateQuad(sailquad, config, i)

            sailquad = self.sailActor.find('**/sail_' + str(self.dna.posIndex) + '_quad_' + str(i) + '_low')
            if not sailquad.isEmpty():
                self.colorateQuad(sailquad, config, i)

    def colorateQuad(self, sailquad, config, index):
        if config[index] == 1:
            sailquad.setColorScale(Vec4(0.466, 0.15, 0.08, 1))
        elif config[index] == 2:
            sailquad.setColorScale(Vec4(0.92, 0.67, 0.23, 1))

    def setAnimState(self, animName):
        if animName == 'Falling':
            animName = 'break0A'

        self.currAnim = animName
        if not self.sailFSM:
            return

        if animName in MastDNA.AllMastAnims and self.sailFSM.state == 'Falling':
            return

        if animName not in MastDNA.AllMastAnims:
            if animName == 'Hit':
                if self.sailFSM.state != 'Hit':
                    self.sailFSM.request(animName)

            else:
                self.sailFSM.request(animName)
        elif self.sailFSM.state != 'Falling' and self.sailFSM.state != 'Dead':
            if self.sailFSM.ival != None:
                self.sailFSM.ival.pause()
                self.sailFSM.ival = None
                self.sailFSM.sail.sailActor.stop()

            self.sailFSM.demand('Falling', animName)

    def addToShip(self):
        id = ShipGlobals.getMastClassification(self.dna.mastType)[0]
        if id == ShipGlobals.FOREMAST:
            locator = self.ship.locators.find('**/location_foremast;+s')
        elif id == ShipGlobals.MAINMAST:
            locator = self.ship.locators.find('**/location_mainmast_' + str(self.dna.mastPosIndex) + ';+s')
        elif id == ShipGlobals.AFTMAST:
            locator = self.ship.locators.find('**/location_aftmast;+s')

        lpos = locator.getPos(self.ship.root)
        lhpr = locator.getHpr(self.ship.root)
        lscl = locator.getScale(self.ship.root)
        self.character.setPos(lpos)
        self.character.setHpr(lhpr)
        self.character.setScale(lscl)
        self.character.reparentTo(self.projScreen)
        self.propCollisions.setPos(lpos)
        self.propCollisions.setHpr(lhpr)
        self.propCollisions.setScale(lscl)

    def cutState(self):
        self.sailState = self.sailGeom.getState()
        self.sailGeom.setState(RenderState.makeEmpty())

    def pasteState(self):
        self.sailGeom.setState(self.sailState)
        self.sailState = None


class SailFSM(FSM.FSM):
    notify = directNotify.newCategory('SailFSM')
    sailUnfoldSfx = None
    sailFoldSfx = None

    def __init__(self, sail):
        FSM.FSM.__init__(self, 'SailFSM')
        self.parentDoId = 0
        self.sail = sail
        self.ival = None
        self.sailIval = None
        self.oldBound = None
        self.billowAmount = 0
        if not self.sailUnfoldSfx:
            self.sailUnfoldSfx = loader.loadSfx('audio/sfx_ship_sails-unfurl.mp3')

        if not self.sailFoldSfx:
            self.sailFoldSfx = loader.loadSfx('audio/sfx_ship_sails-furl.mp3')

    def cleanup(self):
        FSM.FSM.cleanup(self)
        self.sail = None
        self.sailUnfoldSfx = None
        self.sailFoldSfx = None
        if self.ival:
            self.ival.pause()
            self.ival = None

    def filterOff(self, request, args = []):
        if request == 'Rollup':
            return 'TiedUp'
        elif request == 'Rolldown':
            return 'Idle'

        return self.defaultFilter(request, args)

    def enterIdle(self, args = []):
        self.notify.debug('enterIdle %s' % self.parentDoId)
        self.sail.sailActor.loop('Idle')
        self.sail.sailActor.update()
        self.sail.enableCollisions()

    def exitIdle(self):
        self.notify.debug('exitIdle %s' % self.parentDoId)
        if self.sail and not self.sail.isEmpty():
            self.sail.sailActor.stop()

    def enterBillow(self, args = []):
        self.notify.debug('enterIdle %s' % self.parentDoId)
        self.ival = ActorInterval(self.sail.sailActor, 'Idle')
        self.ival.loop()
        self.sail.enableCollisions()

    def exitBillow(self):
        self.notify.debug('exitIdle %s' % self.parentDoId)
        if self.ival:
            self.ival.finish()

    def enterTiedUp(self, args = []):
        self.notify.debug('enterTiedUp %s' % self.parentDoId)
        self.sail.sailActor.pose('Rolldown', 1)
        self.sail.sailActor.update()
        if not config.GetBool('enable-sail-colls-in-port', 0):
            self.sail.disableCollisions()

    def exitTiedUp(self):
        self.notify.debug('exitTiedUp %s' % self.parentDoId)
        if not config.GetBool('enable-sail-colls-in-port', 0):
            self.sail.enableCollisions()

    def enterRollup(self, args = []):
        self.notify.debug('enterRollup %s' % self.parentDoId)
        if self.ival:
            self.ival.pause()

        if self.sailIval:
            self.sailIval.pause()
            self.sailIval = None

        self.sailIval = ActorInterval(self.sail.sailActor, 'Rolldown', playRate = 2.0, startFrame = 80, endFrame = 0)
        self.ival = Sequence(Func(base.playSfx, self.sailFoldSfx, node = self.sail.sailGeom, cutoff = 1000), self.sailIval, Func(self.demand, 'TiedUp'))
        self.ival.start()
        self.sail.sailActor.update()
        if not config.GetBool('enable-sail-colls-in-port', 0):
            self.sail.disableCollisions()

    def filterRollup(self, request, args = []):
        if request == 'advance':
            return 'TiedUp'

        if request == 'Hit' or request == 'Idle':
            return

        return self.defaultFilter(request, args)

    def exitRollup(self):
        self.notify.debug('exitRollup %s' % self.parentDoId)
        if self.ival:
            self.ival.pause()

        if not config.GetBool('enable-sail-colls-in-port', 0):
            self.sail.enableCollisions()

    def enterRolldown(self, args = []):
        self.notify.debug('enterRolldown %s' % self.parentDoId)
        if self.ival:
            self.ival.pause()

        if self.sailIval:
            self.sailIval.pause()
            self.sailIval = None

        self.sailIval = ActorInterval(self.sail.sailActor, 'Rolldown', playRate = 1.5, startFrame = 0, endFrame = 80)
        self.ival = Sequence(Func(base.playSfx, self.sailUnfoldSfx, node = self.sail.sailGeom, cutoff = 1000), self.sailIval, Func(self.demand, 'Idle'))
        self.ival.start()
        self.sail.sailActor.update()

    def filterRolldown(self, request, args = []):
        if request == 'advance':
            return 'Idle'

        if request == 'Hit' or request == 'TiedUp':
            return

        return self.defaultFilter(request, args)

    def exitRolldown(self):
        self.notify.debug('exitRolldown %s' % self.parentDoId)
        if self.ival:
            self.ival.pause()

    def enterHit(self, args = []):
        self.notify.debug('enterHit %s' % self.parentDoId)
        if self.ival:
            self.ival.pause()

        self.ival = Parallel(Sequence(ActorInterval(self.sail.sailActor, 'Hit'), Func(self.demand, 'Idle')))
        self.ival.start()
        self.sail.sailActor.update()

    def exitHit(self):
        self.notify.debug('exitHit %s' % self.parentDoId)
        if self.ival:
            self.ival.pause()
            self.ival = None

    def enterFalling(self, args = []):
        self.notify.debug('enterFalling %s' % self.parentDoId)
        if not args:
            return

        self.sail.setTargetBitmask(0)
        self.oldBound = self.sail.sailActor.node().getBounds()
        self.sail.sailActor.node().setBound(OmniBoundingVolume())
        self.sail.sailActor.node().setFinal(1)
        if self.ival:
            self.ival.pause()

        self.ival = Sequence(Func(self.sail.sailActor.play, args, partName = 'mast'), Wait(10.0), Func(self.demand, 'Dead'))
        self.ival.start()
        self.sail.disableCollisions()

    def filterFalling(self, request, args = []):
        if request == 'advance':
            return 'Dead'

        if request == 'Idle' or request == 'Hit' or request == 'Rolldown' or request == 'Rollup' or request == 'Billow':
            return

        return self.defaultFilter(request, args)

    def exitFalling(self):
        self.notify.debug('exitFalling %s' % self.parentDoId)
        if self.ival:
            self.ival.pause()
            self.ival = None

        if self.sail.sailActor:
            self.sail.sailActor.node().setBounds(self.oldBound)
            self.sail.sailActor.node().setFinal(0)

    def enterDead(self, args = []):
        self.notify.debug('enterDead %s' % self.parentDoId)
        self.sail.death()

    def filterDead(self, request, args = []):
        if request == 'advance':
            return 'Idle'

        if request == 'Idle' or request == 'Hit' or request == 'Falling' or request == 'Rolldown' or request == 'Rollup' or request == 'Billow':
            return

        return self.defaultFilter(request, args)

    def exitDead(self):
        self.notify.debug('exitDead %s' % self.parentDoId)
        if hasattr(base, 'localAvatar') and base.localAvatar and base.localAvatar.ship != self.sail.ship:
            self.sail.setTargetBitmask(1)

        self.sail.respawn()

    def destroy(self):
        self.cleanup()
        if self.ival:
            self.ival.pause()
            del self.ival

        del self.sail

    def unload(self):
        if not self.prop.isEmpty():
            self.unloadModel()
            self.prop.removeNode()
            self.prop = None
