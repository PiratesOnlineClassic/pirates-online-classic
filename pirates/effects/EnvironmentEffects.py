import random

from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from pirates.effects import Grass
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.Bonfire import Bonfire
from pirates.effects.CandleFlame import CandleFlame
from pirates.effects.CraterSmoke import CraterSmoke
from pirates.effects.DarkSteamEffect import DarkSteamEffect
from pirates.effects.Fire import Fire
from pirates.effects.GypsyBallGlow import GypsyBallGlow
from pirates.effects.LanternGlow import LanternGlow
from pirates.effects.LavaBurst import LavaBurst
from pirates.effects.LightSmoke import LightSmoke
from pirates.effects.MysticFire import MysticFire
from pirates.effects.MysticSmoke import MysticSmoke
from pirates.effects.SteamCloud import SteamCloud
from pirates.effects.SteamEffect import SteamEffect
from pirates.effects.TorchFire import TorchFire
from pirates.effects.WaterSplash import WaterSplash
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.GameOptions import Options
from PooledEffect import PooledEffect

class EnvironmentEffects(DirectObject):
    effectDict = {'effect_gypsyball': [(GypsyBallGlow, Options.SpecialEffectsLow)], 'candle_effect': [(CandleFlame, Options.SpecialEffectsLow)], 'torch_effect': [(TorchFire, Options.SpecialEffectsLow)], 'no_glow_effect': [(TorchFire, Options.SpecialEffectsLow)], 'lantern_effect': [(LanternGlow, Options.SpecialEffectsLow)], 'bonfire_effect': [(Bonfire, Options.SpecialEffectsMedium)], 'fireplace_effect': [(Fire, Options.SpecialEffectsLow)], 'watersplash_effect': [(WaterSplash, Options.SpecialEffectsMedium)], 'steam_effect': [(SteamEffect, Options.SpecialEffectsHigh)], 'darksteam_effect': [(DarkSteamEffect, Options.SpecialEffectsMedium)], 'steamcloud_effect': [(SteamCloud, Options.SpecialEffectsMedium)], 'cratersmoke_effect': [(CraterSmoke, Options.SpecialEffectsHigh)], 'lavaburst_effect': [(LavaBurst, Options.SpecialEffectsHigh)], 'blacksmoke_effect': [(BlackSmoke, Options.SpecialEffectsMedium)], 'lightsmoke_effect': [(LightSmoke, Options.SpecialEffectsMedium)], 'mysticsmoke_effect': [(MysticSmoke, Options.SpecialEffectsHigh)], 'mysticfire_effect': [(MysticFire, Options.SpecialEffectsHigh)]}
    soundDict = {'waterfall_sound': 'audio/sfx_waterfall_small.wav', 'waterfall_cave_sound': 'audio/sfx_cave_waterfall.wav'}
    particleDict = {}
    EffectNodeNames = effectDict.keys()
    EffectNodeNames.extend(particleDict.keys())
    animPartsDict = {'chandelier': [('Hpr', 2, Point3(2, 2, 0), Point3(-2, -2, 0))], 'hanging_pot': [('Hpr', 2, Point3(20, 20, 0), Point3(-20, -20, 0))], 'lightstream': [('UVOverlayScroll', 40, 0.15, 0.3, 'models/effects/cloudOverlay'), ('UVScroll', 1200, 1, 0), ('DelayColorFade', 2, Vec4(0.3, 0.3, 0.4, 1), Vec4(0.6, 0.6, 0.7, 1), 10), 'Unlit']}

    def __init__(self, parent, modelPath):
        self.parent = parent
        self.modelPath = modelPath
        self.locators = []
        self.effects = []
        self.particles = []
        self.sounds = []
        self.intervals = []
        self.lights = []
        self.colorScale = None
        self.grass = None
        self.holidayLocators = {}
        self.holidayEffects = {}
        self.loadAnimParts()
        self.loadEffects()
        self.loadSounds()
        self.loadGrass()
        self.accept('HolidayStarted', self.loadHolidayEffects)
        self.accept('HolidayEnded', self.stopHolidayEffects)

    def delete(self):
        for effect in self.effects:
            if effect:
                effect.destroy()
                effect = None

        self.effects = []
        for effect in self.particles:
            if effect:
                effect.finish()
                effect = None

        self.particles = []
        for sound in self.sounds:
            if sound:
                sound.finish()
                sound = None

        self.sounds = []
        for anim in self.intervals:
            if anim:
                anim.pause()
                del anim

        self.intervals = []
        for light in self.lights:
            del light

        self.lights = []
        if self.grass:
            self.grass.stop()
            self.grass.destroy()
            self.grass = None

    def loadSingleEffect(self, nodePath):
        for effect in self.effectDict:
            locators = nodePath.findAllMatches('**/' + effect + '*;+s')
            for locator in locators:
                if not locator.isEmpty():
                    effectParent = locator.getParent()
                    effects = self.effectDict.get(effect)
                    for effectName in effects:
                        glow = effectName[0](effectParent)
                        return glow

    def loadEffects(self):
        if not self.parent:
            return
        effectSetting = None
        if not hasattr(base, 'pe'):
            effectSetting = base.options.getSpecialEffectsSetting()
        else:
            effectSetting = 2
        for effectEntry in self.effectDict:
            locators = self.parent.findAllMatches('**/' + effectEntry + '*;+s')
            for locator in locators:
                if not locator.isEmpty():
                    if effectEntry in self.holidayLocators:
                        list = self.holidayLocators.get(effectEntry)
                        list.append(locator)
                        self.holidayLocators[effectEntry] = list
                        continue
                    else:
                        if locator.getTag('Holiday') != '':
                            self.holidayLocators[effectEntry] = [locator]
                            continue
                    effectParent = locator.getParent()
                    locatorPos = locator.getPos()
                    locatorHpr = locator.getHpr()
                    locatorScale = locator.getScale()
                    effects = self.effectDict.get(effectEntry)
                    for effectName, effectLevel in effects:
                        if effectLevel <= effectSetting:
                            if isinstance(effectName, PooledEffect):
                                effect.reparentTo(effectParent)
                                effect = effectName.getEffect()
                            else:
                                effect = effectName(effectParent)
                            effect.setPos(locatorPos)
                            if effectEntry != 'candle_effect':
                                effect.setScale(locatorScale)
                            effect.startLoop(effectSetting)
                            self.effects.append(effect)

                    locator.stash()

    def loadHolidayEffects(self, holidayName):
        effectSetting = None
        if not hasattr(base, 'pe'):
            effectSetting = base.options.getSpecialEffectsSetting()
        else:
            effectSetting = 2
        for effectEntry in self.holidayLocators.keys():
            locators = self.holidayLocators.get(effectEntry)
            for locator in locators:
                if locator.getTag('Holiday') == holidayName:
                    effectParent = locator.getParent()
                    locatorPos = locator.getPos()
                    locatorHpr = locator.getHpr()
                    locatorScale = locator.getScale()
                    effects = self.effectDict.get(effectEntry)
                    for effectName, effectLevel in effects:
                        if effectLevel <= effectSetting:
                            if isinstance(effectName, PooledEffect):
                                effect.reparentTo(effectParent)
                                effect = effectName.getEffect()
                            else:
                                effect = effectName(effectParent)
                            effect.setPos(locatorPos)
                            if effectEntry != 'candle_effect':
                                effect.setScale(locatorScale)
                            effect.startLoop(effectSetting)
                            if not self.holidayEffects.has_key(holidayName):
                                self.holidayEffects[holidayName] = [
                                 effect]
                            else:
                                list = self.holidayEffects.get(holidayName)
                                list.append(effect)
                                self.holidayEffects[holidayName] = list


    def stopHolidayEffects(self, holidayName):
        if not self.holidayEffects.has_key(holidayName):
            return
        for effect in self.holidayEffects.get(holidayName):
            effect.stop()
            effect = None

        self.holidayEffects[holidayName] = []

    def unloadEffects(self):
        for effect in self.effects:
            effect.stop()
            effect = None

        self.effects = []
        return

    def loadParticles(self):
        if self.parent:
            for effect in self.particleDict:
                locators = self.parent.findAllMatches('**/' + effect + '*;+s')
                for locator in locators:
                    if not locator.isEmpty():
                        effectParent = locator.getParent()
                        effects = self.particleDict.get(effect)
                        locatorPos = locator.getPos()
                        locatorHpr = locator.getHpr()
                        for effectName in effects:
                            particleFX = effectName.getEffect()
                            if particleFX:
                                particleFX.wrtReparentTo(effectParent)
                                particleFX.setPos(locatorPos)
                                particleFX.setHpr(locatorHpr)
                                particleFX.startLoop()
                                self.particles.append(particleFX)

                        locator.stash()

    def loadSounds(self):
        if self.parent:
            for effect in self.soundDict:
                locators = self.parent.findAllMatches('**/' + effect + '*;+s')
                sfx = loader.loadSfx(self.soundDict.get(effect))
                for locator in locators:
                    if not locator.isEmpty():
                        soundFX = SoundInterval(sfx, node=locator, volume=0.5)
                        soundFX.loop()
                        self.sounds.append(soundFX)
                        locator.stash()

    def soundVolumeDown(self):
        for effect in self.sounds:
            effect.volume = 0.25

    def soundVolumeUp(self):
        for effect in self.sounds:
            effect.volume = 0.5

    def loadAnimParts(self):
        if self.parent:
            for part in self.animPartsDict:
                foundParts = self.parent.findAllMatches('**/' + part + '*;+s')
                for myPart in foundParts:
                    if not myPart.isEmpty():
                        effects = self.animPartsDict.get(part)
                        for effect in effects:
                            if effect[0] == 'Hpr':
                                randomness = random.random() / 10
                                rotate1 = myPart.hprInterval(effect[1] + randomness, effect[3], startHpr=effect[2], blendType='easeInOut')
                                rotate2 = myPart.hprInterval(effect[1] + randomness, effect[2], startHpr=effect[3], blendType='easeInOut')
                                anim = Sequence(rotate1, rotate2)
                                anim.loop()
                                self.intervals.append(anim)
                            elif effect[0] == 'ColorFade':
                                randomness = random.random() / 10
                                fadeIn = myPart.colorInterval(effect[1] + randomness, effect[3], startColor=effect[2])
                                fadeOut = myPart.colorInterval(effect[1] + randomness, effect[2], startColor=effect[3])
                                anim = Sequence(fadeIn, fadeOut)
                                anim.loop()
                                self.intervals.append(anim)
                            elif effect[0] == 'DelayColorFade':
                                randomness = random.random() / 10
                                fadeIn = myPart.colorInterval(effect[1] + randomness, effect[3], startColor=effect[2])
                                fadeOut = myPart.colorInterval(effect[1] + randomness, effect[2], startColor=effect[3])
                                anim = Sequence(fadeIn, Wait(effect[4]), fadeOut, Wait(effect[4]))
                                anim.loop()
                                self.intervals.append(anim)
                            elif effect[0] == 'UVScroll':
                                t = myPart.findAllTextureStages()[0]
                                randomness = random.random() / 10
                                anim = LerpFunctionInterval(self.setNewUVs, fromData=0.0, toData=10.0, duration=effect[1] + randomness, extraArgs=[myPart, t, effect])
                                anim.loop()
                                self.intervals.append(anim)
                            elif effect[0] == 'UVOverlayScroll':
                                t = TextureStage('t')
                                t.setMode(TextureStage.MBlend)
                                t.setSort(60)
                                card = loader.loadModel(effect[4])
                                tex = card.findTexture('*')
                                myPart.setTexture(t, tex)
                                myPart.setTexScale(t, 2, 2)
                                randomness = random.random() / 10
                                anim = LerpFunctionInterval(self.setNewUVs, fromData=0.0, toData=10.0, duration=effect[1] + randomness, extraArgs=[myPart, t, effect])
                                anim.loop()
                                self.intervals.append(anim)
                            elif effect[0] == 'Unlit':
                                myPart.setDepthWrite(0)
                                myPart.setColorScaleOff()
                                myPart.setFogOff()

    def loadPolylights(self):
        if self.parent:
            polyLights = self.parent.findAllMatches('**/polylight*')
            for i in range(len(polyLights)):
                light = polyLights[i]
                plNode = light.node()
                print 'light node radius = %s' % plNode.getRadius()
                plNode.setFlickerType(PolylightNode.FSIN)
                plNode.setAttenuation(PolylightNode.AQUADRATIC)
                plNode.setRadius(20)
                effect = base.localAvatar.node().getEffect(PolylightEffect.getClassType()).addLight(light)
                base.localAvatar.node().setEffect(effect)
                self.lights.append(light)

    def loadGrass(self):
        if base.config.GetBool('want-grass', 0) and Grass.HasGrass(self.modelPath):
            self.grass = Grass.Grass(self.parent)
            self.grass.reparentTo(self.parent)

    def setNewUVs(self, time, part, ts, effect):
        part.setTexOffset(ts, time * effect[2], time * effect[3])

    def setupAnimActor(self):
        if not hasattr(self.parent, 'geom'):
            return
        pt = Actor.Actor()
        self.parent.geom.detachNode()
        pt.loadModel(self.parent.geom, copy=0)
        pt.loadModel(self.modelPrefix + 'none')
        pt.loadAnims({'idle': self.modelPrefix + 'idle'})
        pt.reparentTo(self.parent)
        pt.loop('idle')
        mesh = pt.findAllMatches('**/RockMeshGroup')
        if not mesh.isEmpty():
            mesh = mesh[0]
            mesh.flattenStrong()
            tc = mesh.findAllTextureStages()
            for k in range(0, tc.getNumTextureStages()):
                if tc[k].getTexcoordName().getName().find('Top') != -1:
                    joint = pt.findAllMatches('**/uvj_WaterTexture')[0]
                    ts = tc[k]
                    mesh.setTexProjector(ts, joint, self.parent)

        mesh = pt.findAllMatches('**/WaterfallMeshGroup')
        if not mesh.isEmpty():
            mesh = mesh[0]
            mesh.flattenStrong()
            tc = mesh.findTextureStage('default')
            joints = pt.findAllMatches('**/uvj_WaterfallTexture')
            if tc:
                if not joints.isEmpty():
                    joint = joints[0]
                    ts = tc
                    mesh.setTexProjector(ts, joint, self.parent)
            mesh = pt.findAllMatches('**/LightMeshGroup')
            if not mesh.isEmpty():
                mesh = mesh[0]
                mesh.flattenStrong()
                tc = mesh.findTextureStage('default')
                joints = pt.findAllMatches('**/uvj_LightTexture')
                if tc and not joints.isEmpty():
                    joint = joints[0]
                    ts = tc
                    mesh.setTexProjector(ts, joint, self.parent)
            mesh = pt.findAllMatches('**/WaterMeshGroup')
            if not mesh.isEmpty():
                mesh = mesh[0]
                mesh.flattenStrong()
                tc = mesh.findAllTextureStages()
                for k in range(0, tc.getNumTextureStages()):
                    if tc[k].getName().find('dummy') != -1:
                        continue
                    if tc[k].getTexcoordName().getName().find('Top') != -1:
                        joint = pt.findAllMatches('**/uvj_WaterTopTexture')[0]
                        ts = tc[k]
                        mesh.setTexProjector(ts, joint, render)
                    if tc[k].getTexcoordName().getName().find('Bottom') != -1:
                        joint = pt.findAllMatches('**/uvj_WaterBottomTexture')[0]
                        ts = tc[k]
                        mesh.setTexProjector(ts, joint, self.parent)

        return pt
