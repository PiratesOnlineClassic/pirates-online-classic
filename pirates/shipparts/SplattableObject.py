import random
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase.PythonUtil import report
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.Fire import Fire
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.WoodShards import WoodShards
from pirates.effects.ShipDebris import ShipDebris
from pirates.effects.CameraShaker import CameraShaker
from pirates.battle import WeaponGlobals
from pirates.ship import ShipGlobals
from pirates.shipparts import HullDNA

def cutGeomTextureStates(geomNode, excludedStages = []):
    numGeoms = geomNode.getNumGeoms()
    finalPacket = []
    for i in xrange(numGeoms):
        geomState = geomNode.getGeomState(i)
        attrib = geomState.getAttrib(TextureAttrib.getClassType())
        finalPacket.append(attrib)
        geomNode.setGeomState(i, geomState.addAttrib(TextureAttrib.make()))

    return finalPacket


def pasteGeomTextureStates(geomNode, attribList):
    for i in xrange(geomNode.getNumGeoms()):
        gs = geomNode.getGeomState(i).addAttrib(attribList[i])
        geomNode.setGeomState(i, gs)


class SplattableObject(NodePath):
    holeCard = None
    holeTex = None
    breakTex1 = None
    blankTex = None
    shipTextures = None

    def __init__(self):
        self.card = None
        self.ship = None
        self.frameHoleCount = 0
        self.panelsHigh = []
        self.panelsMed = []
        self.panelsLow = []
        self.collPanels = []
        self.cutHighStates = {}
        self.cutMedStates = {}
        self.projScreens = {}
        self.projScreensNodePaths = {}
        self.colorConfigDict = {}
        self.fireEffects = {}
        self.smokeEffects = {}
        self.holeLocations = {}
        if not self.holeCard:
            SplattableObject.holeCard = loader.loadModelCopy('models/effects/battleEffects')
            SplattableObject.holeTexArray = [
                [
                    self.holeCard.find('**/effectHoleC').findTexture('*'),
                    1],
                [
                    self.holeCard.find('**/effectHoleD').findTexture('*'),
                    1],
                [
                    self.holeCard.find('**/effectHoleE').findTexture('*'),
                    1]]
            SplattableObject.breakTex1 = self.holeCard.find('**/effectHullBreach').findTexture('*')
            if base.supportAlphaFb:
                blankTex = Texture()
                image = PNMImage(512, 512, 4)
                blankTex.load(image)
                SplattableObject.blankTex = blankTex
            else:
                SplattableObject.blankTex = self.holeCard.find('**/hullBlank').findTexture('*')
            SplattableObject.shipTextures = loader.loadModelCopy('models/textureCards/shipTextures')
            for texInfo in SplattableObject.holeTexArray:
                tex = texInfo[0]
                tex.setWrapU(Texture.WMBorderColor)
                tex.setWrapV(Texture.WMBorderColor)
                tex.setMinfilter(Texture.FTNearest)
                tex.setMagfilter(Texture.FTNearest)
                tex.setBorderColor(Vec4(1, 1, 1, 0))

            self.blankTex.setMinfilter(Texture.FTLinearMipmapLinear)
            self.blankTex.setMagfilter(Texture.FTLinear)

    def disable(self):
        self.cleanupEffects()
        self.panelsHigh = []
        self.panelsMed = []
        self.panelsLow = []
        self.collPanels = []
        self.projScreens = {}

    def delete(self):
        if self.cr:
            base.textureFlattenMgr.clearSplattables(self)

        del self.fireEffects
        del self.smokeEffects

    def load(self):
        self.mainLayer = TextureStage('mainLayer')
        self.mainLayer.setSort(1)
        self.holeLayer = TextureStage('holeLayer')
        if base.supportAlphaFb:
            self.holeLayer.setMode(TextureStage.MDecal)
        else:
            self.holeLayer.setMode(TextureStage.MModulate)
        self.holeLayer.setSort(60)
        self.holeLayer.setTexcoordName('uvSplat')

    def initDestruction(self):
        for panel in self.panelsMed:
            panel.setTexture(self.holeLayer, self.blankTex)

    def resetDestruction(self, index):
        panelHigh = None
        panelMed = None
        t = TextureStage('t')
        t.setSort(250)
        if len(self.panelsHigh) - 1 >= index:
            self.panelsHigh[index].setTexture(self.holeLayer, self.blankTex)

        if len(self.panelsMed) - 1 >= index:
            self.panelsMed[index].setTexture(self.holeLayer, self.blankTex)

        if self.fireEffects.has_key(index):
            self.fireEffects[index].stopLoop()
            del self.fireEffects[index]

        if self.smokeEffects.has_key(index):
            self.smokeEffects[index].stopLoop()
            del self.smokeEffects[index]

    def playHoleSplat(self, pos, normal, index):
        if base.options.getSpecialEffectsSetting() <= base.options.SpecialEffectsLow:
            return

        panel = None
        if index > 0:
            index = (index - 1) % 2 + 1

        if base.config.GetBool('force-highLOD-destruction', 0) is 1:
            if len(self.panelsHigh) - 1 >= index:
                panel = self.panelsHigh[index]

        elif len(self.panelsMed) - 1 >= index:
            panel = self.panelsMed[index]

        if not panel:
            return

        if not self.projScreens:
            return

        if base.cr.wantSpecialEffects and panel:
            holeCount = base.textureFlattenMgr.addSplattable(self, index)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                t = TextureStage('hole stage %s' % holeCount)
                t.setMode(TextureStage.MDecal)
                t.setSort(200)
                t.setTexcoordName('uvHole-%s' % holeCount)
                self.t = t

            n = render.attachNewNode('dummy')
            n.lookAt(Point3(normal))
            hpr = n.getHpr()
            n.removeNode()
            del n
            hole = self.ship.attachNewNode('hole')
            hole.setPos(pos)
            hole.setHpr(render, hpr[0], hpr[1], 0)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                pass

            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                holeSize = ShipGlobals.getHoleSizes(self.dna.modelClass)[0]
                texInfo = random.choice(self.holeTexArray)
                tex = texInfo[0]
                holeSize *= texInfo[1]
                l = OrthographicLens()
                l.setFilmSize(holeSize, holeSize)
                lens = LensNode('lens')
                lens.setLens(l)
                holeLocation = hole.attachNewNode(lens)
                panel.setTexture(t, tex)
                self.projScreens[index].setProjector(holeLocation)
                self.projScreens[index].setTexcoordName('uvHole-%s' % holeCount)
                self.projScreens[index].recompute()
                del t
                del l
                del lens
                holeLocation.removeNode()
                del holeLocation

            hole.removeNode()
            del hole

    def playBreak(self, index, collIndex):
        if not self.ship:
            return

        panel = None
        if len(self.panelsMed) - 1 >= index:
            panel = self.panelsMed[index]

        if not panel:
            return

        if not self.projScreens:
            return

        projNode = self.ship.locators.find('**/location_fire_' + str(collIndex) + ';+s')
        hole = render.attachNewNode('hole')
        hole.reparentTo(self.ship)
        hole.setPos(render, projNode.getPos(render))
        hole.setHpr(render, projNode.getHpr(render))
        if base.cr.wantSpecialEffects and panel:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                for i in range(random.randint(2, 4)):
                    shipDebrisEffect = ShipDebris.getEffect()
                    if shipDebrisEffect:
                        shipDebrisEffect.reparentTo(render)
                        shipDebrisEffect.setPosHpr(hole, 0, 0, 0, 0, 0, 0)
                        shipDebrisEffect.endPlaneZ -= hole.getZ()
                        shipDebrisEffect.play()

            pos = projNode.getPos()
            sfx = random.choice(self.woodBreakSfx)
            base.playSfx(sfx, node = self, cutoff = 2500)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.reparentTo(self.ship.root)
                cameraShakerEffect.setPos(pos)
                cameraShakerEffect.shakeSpeed = 0.06
                cameraShakerEffect.shakePower = 5.0
                cameraShakerEffect.numShakes = 3
                cameraShakerEffect.play(100.0)
                blackSmokeEffect = BlackSmoke.getEffect()
                if blackSmokeEffect:
                    blackSmokeEffect.reparentTo(self.ship.root)
                    blackSmokeEffect.setPos(pos)
                    blackSmokeEffect.duration = 10.0
                    blackSmokeEffect.startLoop()
                    if self.smokeEffects.get(collIndex):
                        self.smokeEffects[collIndex].stopLoop()
                        del self.smokeEffects[collIndex]

                    self.smokeEffects[collIndex] = blackSmokeEffect

            fireEffect = Fire.getEffect()
            if fireEffect:
                fireEffect.reparentTo(self.ship.root)
                fireEffect.setPos(pos)
                fireEffect.effectScale = 1.0
                fireEffect.duration = 10.0
                fireEffect.startLoop()
                if self.fireEffects.get(collIndex):
                    self.fireEffects[collIndex].stopLoop()
                    del self.fireEffects[collIndex]

                self.fireEffects[collIndex] = fireEffect

    def add2dHole(self, index, u, v):
        panel = None
        if len(self.panelsMed) - 1 >= index:
            panel = self.panelsMed[index]

        if base.cr.wantSpecialEffects and panel:
            t = TextureStage('final')
            t.setMode(TextureStage.MModulate)
            t.setSort(200)
            t.setTexcoordName('uvHole')
            panel.setTexture(t, self.holeTex)
            panel.setTexScale(t, 2, 2)
            panel.setTexOffset(t, u, v)
            attribList = self.cutGeomTextureStates(panel.node(), ['holeLayer'])
            panel.flattenMultitex(useGeom = 0, target = self.holeLayer)
            self.copyMultitexLayer(panel, self.panelsHigh[index])
            self.pasteGeomTextureStates(panel.node(), attribList)
            del t

    def changeColor(self, geom):
        suffix = [
            'A',
            'B',
            'C',
            'D',
            'E']

        for i in xrange(len(self.dna.hullTextureIndex)):
            self.configColor(geom, 'hull%s' % suffix[i], self.dna.hullTextureIndex[i], self.dna.hullColorIndex[i], self.dna.hullHilightColorIndex[i])

        for i in xrange(len(self.dna.stripeTextureIndex)):
            self.configColor(geom, 'stripe%s' % suffix[i], self.dna.stripeTextureIndex[i], self.dna.stripeColorIndex[i], self.dna.stripeHilightColorIndex[i])

        for i in xrange(len(self.dna.patternTextureIndex)):
            self.configColor(geom, 'pattern%s' % suffix[i], self.dna.patternTextureIndex[i], self.dna.patternColorIndex[i], self.dna.patternHilightColorIndex[i])

        self.configColor(geom, 'bottom_hull', 255)
        if self.dna.hullTextureIndex or self.dna.stripeTextureIndex or self.dna.patternTextureIndex:
            panels = geom.findAllMatches('**/panel_*/*')
            self.reloadPanelTex(panels)

    def configColor(self, geom, prefix, texIndex = 0, color = 0, hilightColor = 0):
        if texIndex:
            self.setMultitexColorFromRoot(geom, prefix, texIndex, color, hilightColor)

    def reloadPanelTex(self, panels):
        for panel in panels:
            if panel:
                texStage = panel.findTextureStage('default')
                if texStage:
                    panel.setTextureOff(texStage, 1)

    def setMultitexColorFromRoot(self, root, prefix, texIndex, color, hilightColor):
        if prefix[0:4] == 'hull' or prefix[0:11] == 'bottom_hull':
            filePrefix = HullDNA.HullTexDict.get(texIndex)
        elif prefix[0:6] == 'stripe':
            filePrefix = HullDNA.StripeTexDict.get(texIndex)
        elif prefix[0:7] == 'pattern':
            filePrefix = HullDNA.PatternTexDict.get(texIndex)

        if not filePrefix:
            return

        colorTs = TextureStage(prefix + 'Color')
        colorTs.setCombineRgb(TextureStage.CMModulate, TextureStage.CSConstant, TextureStage.COSrcColor, TextureStage.CSTexture, TextureStage.COSrcColor)
        colorTs.setColor(HullDNA.HullColors[color])
        colorTs.setSort(5)
        blendTs = TextureStage(prefix + 'blendTs')
        blendTs.setCombineRgb(TextureStage.CMModulate, TextureStage.CSPrimaryColor, TextureStage.COSrcColor, TextureStage.CSPrevious, TextureStage.COSrcColor)
        blendTs.setSort(30)
        colorTex = self.shipTextures.find('**/%s' % filePrefix[0]).findTexture('*')
        if filePrefix[1]:
            hilightTex = self.shipTextures.find('**/%s' % filePrefix[1]).findTexture('*')
        else:
            hilightTex = None
        targets = root.findAllMatches('**/%s*' % prefix)
        for i in range(targets.getNumPaths()):
            target = targets[i]
            target.setTexture(colorTs, colorTex)
            if hilightTex:
                if prefix[0:4] == 'hull' or prefix[0:11] == 'bottom_hull':
                    if target.hasTexcoord('uvGrunge'):
                        hilightTs = TextureStage(prefix + 'Hilight')
                        hilightTs.setTexcoordName('uvGrunge')
                        hilightTs.setMode(TextureStage.MModulate)
                        hilightTs.setSort(12)
                        target.setTexture(hilightTs, hilightTex)

                else:
                    hilightTs = TextureStage(prefix + 'Hilight')
                    hilightTs.setMode(TextureStage.MBlend)
                    hilightTs.setColor(HullDNA.HullColors[hilightColor])
                    hilightTs.setSort(12)
                    target.setTexture(hilightTs, hilightTex)

            target.setTexture(blendTs, colorTex)

    def hideBaseTexture(self, panel):
        pass

    def showBaseTexture(self, panel):
        pass

    def copyMultitexLayer(self, sourcePanel, targetPanel):
        if not sourcePanel or not targetPanel:
            return 0

        ts = sourcePanel.findTextureStage('holeLayer')
        if ts:
            tex = sourcePanel.findTexture(ts)
            if tex:
                targetPanel.setTexture(self.holeLayer, tex)
                return 1

        return 0

    def cutState(self):
        for i in range(len(self.panelsHigh)):
            self.cutHighStates[i] = self.panelsHigh[i].getState()
            self.cutMedStates[i] = self.panelsMed[i].getState()
            self.panelsHigh[i].setState(RenderState.makeEmpty())
            self.panelsMed[i].setState(RenderState.makeEmpty())

    def pasteState(self):
        for i in range(len(self.panelsHigh)):
            self.panelsHigh[i].setState(self.cutHighStates[i])
            self.panelsMed[i].setState(self.cutMedStates[i])

        self.cutHighStates = {}
        self.cutMedStates = {}

    def hideAllPanels(self):
        for panel in self.panelsHigh:
            panel.hide()

        for panel in self.panelsMed:
            panel.hide()

        for panel in self.panelsLow:
            panel.hide()

    def showAllPanels(self):
        for panel in self.panelsHigh:
            panel.show()

        for panel in self.panelsMed:
            panel.show()

        for panel in self.panelsLow:
            panel.show()

    def cleanupEffects(self):
        for i in self.fireEffects:
            self.fireEffects[i].stopLoop()

        self.fireEffects = {}
        for i in self.smokeEffects:
            self.smokeEffects[i].stopLoop()

        self.smokeEffects = {}

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

    def stopAllSmoke(self):
        for i in self.smokeEffects:
            if self.smokeEffects.get(i):
                self.smokeEffects[i].stopLoop()

        self.smokeEffects = {}

    def hideSmoke(self):
        for effect in self.smokeEffects.values():
            effect.p0.renderer.getRenderNodePath().hide()

    def showSmoke(self):
        for effect in self.smokeEffects.values():
            effect.p0.renderer.getRenderNodePath().show()

    def startSmoke(self, collIndex):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
            projNode = self.ship.locators.find('**/location_fire_' + str(collIndex) + ';+s')
            pos = projNode.getPos()
            blackSmokeEffect = BlackSmoke.getEffect()
            if blackSmokeEffect:
                blackSmokeEffect.reparentTo(self.ship.root)
                blackSmokeEffect.setPos(pos)
                blackSmokeEffect.startLoop()
                if self.smokeEffects.get(collIndex):
                    self.smokeEffects[collIndex].stopLoop()
                    del self.smokeEffects[collIndex]

                self.smokeEffects[collIndex] = blackSmokeEffect
