from panda3d.core import *
from direct.interval.IntervalGlobal import *
from otp.otpbase import OTPRender
from pirates.piratesbase import PiratesGlobals

class SkyGroup(NodePath):

    def __init__(self):
        NodePath.__init__(self, 'SkyGroup')
        self.showThrough(OTPRender.SkyReflectionCameraBitmask)
        self.setEffect(CompassEffect.make(NodePath(), CompassEffect.PRot))
        self.setAttrib(ColorWriteAttrib.make(ColorWriteAttrib.CRed | ColorWriteAttrib.CGreen | ColorWriteAttrib.CBlue))
        self.setTransparency(1)
        self.setColorScaleOff()
        self.setDepthWrite(0)
        self.setDepthTest(0)
        self.clearFog()
        self.setFogOff()
        self.setLightOff()
        self.setHpr(0.0, 0.0, 0.0)
        self.setScale(10)
        self.setZ(-10)
        skydome = loader.loadModel('models/sky/PiratesSkyDome')
        geoms = skydome.findAllMatches('**/+GeomNode')
        for geom in geoms:
            self._clearTexAttrib(geom)

        self.sides = skydome.find('**/Sides')
        self.sides.setBin('background', 102)
        self.sides.reparentTo(self)
        self.top = skydome.find('**/Top')
        self.top.setBin('background', 104)
        self.top.reparentTo(self)
        self.horizon = skydome.find('**/Horizon')
        self.horizon.setBin('background', 125)
        self.horizon.reparentTo(self)
        self.clouds = skydome.find('**/CloudsTop')
        self.clouds.setBin('background', 125)
        self.clouds.reparentTo(self)
        self.stars = skydome.find('**/stars')
        self.stars.setBin('background', 100)
        self.stars.reparentTo(self)
        textures = loader.loadModel('models/sky/PiratesSkyDomeCards')
        self.texCloudsLight = textures.find('**/clouds_light').findAllTextures()[0]
        self.texCloudsMedium = textures.find('**/clouds_medium').findAllTextures()[0]
        self.texCloudsHeavy = textures.find('**/clouds_heavy').findAllTextures()[0]
        self.texOpaque = textures.find('**/opaque').findAllTextures()[0]
        self.texTransparent = textures.find('**/transparent').findAllTextures()[0]
        self.texGradient = textures.find('**/gradient').findAllTextures()[0]
        self.texStars = textures.find('**/stars').findAllTextures()[0]
        textures = loader.loadModel('models/effects/particleCards')
        self.texStar = textures.find('**/particleSparkle').findAllTextures()[0]
        self.cloudSettings = {
            0: (self.texTransparent, ''),
            1: (self.texCloudsLight, ''),
            2: (self.texCloudsMedium, ''),
            3: (self.texCloudsHeavy, '')
        }
        self.skySettings = {PiratesGlobals.TOD_DAWN: [(self.texTransparent, '', VBase4(0, 0, 0, 0), VBase4(0.8, 0.5, 0.2, 1)), (self.texOpaque, '', VBase4(0, 0, 0, 0), VBase4(0.4, 0.58, 0.6, 1)), VBase4(0.8, 0.8, 0.6, 1), VBase4(0.3, 0.2, 0.15, 1)],
                            PiratesGlobals.TOD_DAY: [(self.texTransparent, '', VBase4(0, 0, 0, 0), VBase4(1, 1, 1, 0.7)), (self.texOpaque, '', VBase4(0, 0, 0, 0), VBase4(0.45, 0.55, 0.7, 0)), VBase4(1, 1, 1, 1), VBase4(0.6, 0.7, 0.9, 1)],
                            PiratesGlobals.TOD_DUSK: [(self.texTransparent, '', VBase4(0, 0, 0, 0), VBase4(0.7, 0.4, 0.2, 1)), (self.texOpaque, '', VBase4(0, 0, 0, 0), VBase4(0.45, 0.4, 0.52, 1)), VBase4(0.75, 0.35, 0.22, 1), VBase4(0.3, 0.18, 0.15, 1)],
                            PiratesGlobals.TOD_NIGHT: [(self.texStars, 'map2', VBase4(0.1, 0.1, 0.1, 0.1), VBase4(0.36, 0.48, 0.74, 0.8)), (self.texStars, 'map2', VBase4(0, 0, 0, 0), VBase4(0.36, 0.48, 0.74, 0.2)), VBase4(0.34, 0.45, 0.7, 0.8), VBase4(0.15, 0.2, 0.35, 1)],
                            PiratesGlobals.TOD_STARS: [(self.texStars, 'map2', VBase4(0.85, 0.8, 0.5, 0.5), VBase4(1, 1, 1, 1)), (self.texStars, 'map2', VBase4(0, 0, 0, 0), VBase4(1, 1, 1, 1)), VBase4(0.45, 0.45, 0.7, 0.6), VBase4(0.05, 0.06, 0.17, 1)],
                            PiratesGlobals.TOD_HALLOWEEN: [(self.texStars, 'map2', VBase4(0, 0, 0, 0.2), VBase4(0.5, 0.6, 0.15, 1)), (self.texStars, 'map2', VBase4(0, 0, 0, 0), VBase4(1, 1, 1, 0.4)), VBase4(0.5, 0.6, 0.15, 1), VBase4(0.1, 0.12, 0.03, 1)],
                            PiratesGlobals.TOD_SWAMP: [(self.texTransparent, '', VBase4(0, 0, 0, 0), VBase4(0.35, 0.5, 0.6, 1)), (self.texOpaque, '', VBase4(0, 0, 0, 0), VBase4(0.35, 0.5, 0.6, 0)), VBase4(0.35, 0.5, 0.6, 1), VBase4(0.15, 0.2, 0.35, 1)]}
        self.tsSides = []
        self.tsSides.append(self._setupTexStageA('tsSidesA'))
        self.tsSides.append(self._setupTexStageB('tsSidesB'))
        self.tsSides.append(self._setupTexStageC('tsSidesC'))
        self.tsSides.append(self._setupTexStageD('tsSidesD'))
        self.sides.setTexture(self.tsSides[3], self.texTransparent)
        self.tsTop = []
        self.tsTop.append(self._setupTexStageA('tsTopA'))
        self.tsTop.append(self._setupTexStageB('tsTopB'))
        self.tsTop.append(self._setupTexStageD('tsTopD'))
        self.top.setTexture(self.tsSides[3], self.texTransparent)
        self.clouds.setTexture(self.tsSides[3], self.texTransparent)
        self.cloudIval = None
        self.setCloudLevel(2)
        self.stars.setTexture(TextureStage.getDefault(), self.texStar)
        self.stars.setColorScale(1, 1, 1, 0.25)
        self.sunTrack = self.attachNewNode('sunTrack')
        self.sunTrack.setHpr(-90, 0, 90)
        self.sunWheel = self.sunTrack.attachNewNode('sunWheel')
        self.sunLight = self.sunWheel.attachNewNode('sunLight')
        self.sunLight.setPosHpr(0, 2300, 0, 180, 0, 0)
        dl = DirectionalLight('directionalLightSun')
        self.dirLightSun = self.sunLight.attachNewNode(dl)
        al = AmbientLight('grassLight')
        al.setColor(VBase4(1, 1, 1, 1))
        self.grassLight = self.sunLight.attachNewNode(al)
        al = AmbientLight('ambientLight')
        al.setColor(VBase4(1, 1, 1, 1))
        self.ambLight = self.sunLight.attachNewNode(al)
        self.sunModel = loader.loadModel('models/sky/sun')
        if base.config.GetBool('prepare-scene', 1):
            if base.win.getGsg():
                self.sunModel.prepareScene(base.win.getGsg())
        self.sunModel.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.sunModel.setBillboardPointEye()
        self.sunModel.setBin('background', 120)
        self.sunModel.setScale(2700)
        self.sunModel.reparentTo(self.sunLight)
        self.moonTrack = self.attachNewNode('moonTrack')
        self.moonTrack.setHpr(-90, 30, 0)
        self.moonWheel = self.moonTrack.attachNewNode('moonWheel')
        self.moonLight = self.moonWheel.attachNewNode('moonLight')
        self.moonLight.setPosHpr(0, 4000, 0, 180, 0, 0)
        dl = DirectionalLight('directionalLightMoon')
        self.dirLightMoon = self.moonLight.attachNewNode(dl)
        self.moonModel = loader.loadModel('models/sky/moon')
        self.moonModel.setBillboardPointEye()
        self.moonModel.setBin('background', 110)
        self.moonModel.setHpr(0, 0, -60)
        self.moonModel.setScale(500)
        self.moonModel.reparentTo(self.moonLight)
        self.moonGlow = loader.loadModel('models/sky/sun')
        self.moonGlow.reparentTo(self.moonModel)
        self.moonGlow.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.moonGlow.setBin('background', 109, 1)
        self.moonGlow.setPos(0, 0, -.2)
        self.moonGlow.setColorScale(0.7, 0.8, 1, 1)
        self.moonGlow.setScale(5)
        self.tsMoon = self._setupTexStageAlpha('tsMoon')
        self.texGradient.setWrapU(Texture.WMClamp)
        self.texGradient.setWrapV(Texture.WMClamp)
        self.moonModel.setTexture(self.tsMoon, self.texGradient)
        self.moonAlphaNode = NodePath('MoonAlphaNode')
        self.moonModel.setTexProjector(self.tsMoon, self.moonAlphaNode, NodePath())
        self.setMoonState(1.0)
        self.moonOverlay = loader.loadModel('models/effects/effectCards').find('**/effectJolly')
        self.moonOverlay.setBin('background', 111)
        self.moonOverlay.reparentTo(self.moonModel)
        self.moonOverlay.setHpr(0, 0, 60)
        self.moonOverlay.setScale(0.9)
        self.moonOverlay.setColorScale(1, 1, 1, 0.25)
        self.moonOverlay.stash()
        self.moonOverlayIval = None
        self.lightSettings = {
            PiratesGlobals.TOD_DAWN: self.dirLightSun,
            PiratesGlobals.TOD_DAY: self.dirLightSun,
            PiratesGlobals.TOD_DUSK: self.dirLightSun,
            PiratesGlobals.TOD_NIGHT: self.dirLightMoon,
            PiratesGlobals.TOD_STARS: self.dirLightMoon,
            PiratesGlobals.TOD_HALLOWEEN: self.dirLightMoon
        }
        render.setLight(self.ambLight)
        render.setLight(self.dirLightSun)
        render.setLight(self.dirLightMoon)
        try:
            areg = AttribNodeRegistry.getGlobalPtr()
        except:
            areg = None

        if areg:
            areg.addNode(self.ambLight)
            areg.addNode(self.dirLightSun)
            areg.addNode(self.dirLightMoon)

        messenger.send('nametagAmbientLightChanged', [self.ambLight])
        self.shadowCaster = None

    def getLight(self, tod):
        return self.lightSettings.get(tod)

    def _clearTexAttrib(self, geomNode):
        attrib = geomNode.node().getGeomState(0).removeAttrib(TextureAttrib.getClassType())
        geomNode.node().setGeomState(0, attrib)

    def _setupTexStageAlpha(self, name):
        ts = TextureStage(name)
        ts.setCombineRgb(TextureStage.CMReplace, TextureStage.CSPrevious, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMModulate, TextureStage.CSPrevious, TextureStage.COSrcAlpha, TextureStage.CSTexture, TextureStage.COSrcAlpha)
        ts.setSort(2)
        return ts

    def _setupTexStageA(self, name):
        ts = TextureStage(name)
        ts.setCombineRgb(TextureStage.CMReplace, TextureStage.CSTexture, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSTexture, TextureStage.COSrcAlpha)
        ts.setSort(1)
        return ts

    def _setupTexStageB(self, name):
        ts = TextureStage(name)
        ts.setColor(Vec4(0, 0, 0, 0))
        ts.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcColor, TextureStage.CSPrevious, TextureStage.COSrcColor, TextureStage.CSConstant, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcAlpha, TextureStage.CSPrevious, TextureStage.COSrcAlpha, TextureStage.CSConstant, TextureStage.COSrcAlpha)
        ts.setSort(2)
        return ts

    def _setupTexStageC(self, name):
        ts = TextureStage(name)
        ts.setColor(Vec4(0, 0, 0, 0))
        ts.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcColor, TextureStage.CSPrevious, TextureStage.COSrcColor, TextureStage.CSConstant, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcAlpha, TextureStage.CSPrevious, TextureStage.COSrcAlpha, TextureStage.CSConstant, TextureStage.COSrcAlpha)
        ts.setSort(3)
        return ts

    def _setupTexStageD(self, name):
        ts = TextureStage(name)
        ts.setCombineRgb(TextureStage.CMModulate, TextureStage.CSPrimaryColor, TextureStage.COSrcColor, TextureStage.CSPrevious, TextureStage.COSrcColor)
        ts.setCombineAlpha(TextureStage.CMModulate, TextureStage.CSPrimaryColor, TextureStage.COSrcAlpha, TextureStage.CSPrevious, TextureStage.COSrcAlpha)
        ts.setSort(4)
        return ts

    def setStageColor(self, t, ts, startColor, endColor):
        ts.setColor(startColor * (1.0 - t) + endColor * t)

    def stashMoon(self):
        self.moonWheel.stash()
        self.stars.stash()

    def unstashMoon(self):
        self.moonWheel.unstash()
        self.moonOverlay.stash()
        self.stars.unstash()
        self.moonModel.setColorScale(1, 1, 1, 1)
        self.moonModel.setScale(500)

    def unstashMoonBig(self):
        self.moonWheel.unstash()
        self.stars.unstash()
        self.moonModel.setColorScale(1, 1, 1, 1)
        self.moonModel.setScale(1000)

    def fadeInMoon(self, duration):
        return LerpColorScaleInterval(self.moonModel, duration, Vec4(1, 1, 1, 1), startColorScale = Vec4(1, 1, 1, 0))

    def fadeOutMoon(self, duration):
        return LerpColorScaleInterval(self.moonModel, duration, Vec4(1, 1, 1, 0), startColorScale = Vec4(1, 1, 1, 1))
    
    def fadeInMoonOverlay(self, duration = 1.0):
        self.moonOverlay.unstash()
        return LerpColorScaleInterval(self.moonOverlay, duration, Vec4(1, 1, 1, 0.35), startColorScale = Vec4(1, 1, 1, 0))

    def fadeOutMoonOverlay(self, duration = 1.0):
        self.moonOverlay.unstash()
        return LerpColorScaleInterval(self.moonOverlay, duration, Vec4(1, 1, 1, 0), startColorScale = Vec4(1, 1, 1, 0.35))

    def setMoonState(self, state):
        pos = 0.1 - state * 0.8
        self.moonAlphaNode.setPos(0, pos, 0)
    
    def transitionMoon(self, fromState, toState, duration = 10.0):
        return LerpFunctionInterval(self.setMoonState, duration, fromData = fromState, toData = toState)

    def stashSun(self):
        self.sunWheel.stash()

    def unstashSun(self):
        self.sunWheel.unstash()
        self.sunTrack.setColorScale(1, 1, 1, 1)
    
    def fadeInSun(self, duration):
        return LerpColorScaleInterval(self.sunTrack, duration, Vec4(1, 1, 1, 1), startColorScale = Vec4(0, 0, 0, 0))
    
    def fadeOutSun(self, duration):
        return LerpColorScaleInterval(self.sunTrack, duration, Vec4(0, 0, 0, 0), startColorScale = Vec4(1, 1, 1, 1))

    def setSunAngle(self, t):
        h = t * 360.0 % 360.0
        self.sunWheel.setH(h)
        if self.shadowCaster and self.shadowCaster.shadowsEnabled:
            self.shadowCaster.updateShadows(h)
        
        return h

    def transitionSun(self, beginTime, endTime, duration = 10.0):
        return LerpFunctionInterval(self.setSunAngle, duration, fromData = beginTime, toData = endTime)
    
    def stashStars(self):
        self.sunWheel.stash()
    
    def unstashStars(self):
        self.sunWheel.unstash()
        self.sunModel.setColorScale(1, 1, 1, 1)

    def fadeInStars(self, duration):
        return LerpColorScaleInterval(self.stars, duration, Vec4(1, 1, 1, 0.25), startColorScale = Vec4(1, 1, 1, 0))

    def fadeInStarsMore(self, duration):
        return LerpColorScaleInterval(self.stars, duration, Vec4(1, 1, 1, 1), startColorScale = Vec4(1, 1, 1, 0.25))
    
    def fadeOutStars(self, duration):
        return LerpColorScaleInterval(self.stars, duration, Vec4(1, 1, 1, 0), startColorScale = Vec4(1, 1, 1, 1))

    def setupCloudIval(self):
        ival = Parallel(name = 'CloudIval')
        cloudNodeA = NodePath('CloudNodeA')
        anim = LerpPosInterval(cloudNodeA, startPos = VBase3(0.0, 0.0, 0.0), pos = VBase3(2.0, 1.0, 0.0), duration = 400.0)
        ival.append(anim)
        cloudNodeB = NodePath('CloudNodeB')
        anim = LerpPosInterval(cloudNodeB, startPos = VBase3(0.0, 0.0, 0.0), pos = VBase3(-2.0, 0.0, 0.0), duration = 400.0)
        ival.append(anim)
        self.clouds.setTexProjector(self.tsSides[0], cloudNodeA, NodePath())
        self.sides.setTexProjector(self.tsSides[0], cloudNodeB, NodePath())
        return ival

    def startCloudIval(self):
        if not self.cloudIval:
            self.cloudIval = self.setupCloudIval()
        
        self.cloudIval.loop()

    def stopCloudIval(self):
        if self.cloudIval:
            self.cloudIval.pause()
            self.cloudIval = None

    def setCloudLevel(self, level):
        self.startCloudIval()
        cloudTex = self.cloudSettings.get(level)[0]
        uvSetName = self.cloudSettings.get(level)[1]
        self.sides.setTexture(self.tsSides[0], cloudTex)
        self.clouds.setTexture(self.tsSides[0], cloudTex)
        self.tsSides[0].setTexcoordName(uvSetName)
        self.tsSides[1].setColor(Vec4(0, 0, 0, 0))

    def transitionClouds(self, level, duration = 5.0):
        self.stopCloudIval()
        cloudTex = self.cloudSettings.get(level)[0]
        uvSetName = self.cloudSettings.get(level)[1]
        self.sides.setTexture(self.tsSides[1], cloudTex)
        self.clouds.setTexture(self.tsSides[1], cloudTex)
        self.tsSides[1].setTexcoordName(uvSetName)
        ival = Sequence(LerpFunctionInterval(self.setStageColor, duration, fromData = 0.0, toData = 1.0, extraArgs = [
            self.tsSides[1],
            Vec4(0, 0, 0, 0),
            Vec4(1, 1, 1, 1)]), Func(self.setCloudLevel, level))
        return ival

    def setSky(self, tod):
        settings = self.skySettings.get(tod)
        self.sides.setTexture(self.tsSides[2], settings[0][0])
        self.tsSides[2].setTexcoordName(settings[0][1])
        self.tsSides[1].setColor(Vec4(0, 0, 0, 0))
        self.tsSides[2].setColor(settings[0][2])
        self.sides.setColorScale(settings[0][3])
        self.top.setTexture(self.tsTop[0], settings[1][0])
        self.tsTop[0].setTexcoordName(settings[1][1])
        self.tsTop[1].setColor(Vec4(0, 0, 0, 0))
        self.top.setColorScale(settings[1][3])
        self.clouds.setColorScale(settings[2])
        self.horizon.setColorScale(settings[3])
    
    def transitionSky(self, todA, todB, duration = 10.0):
        self.setSky(todA)
        settingsA = self.skySettings.get(todA)
        settingsB = self.skySettings.get(todB)
        self.sides.setTexture(self.tsSides[1], settingsB[0][0])
        self.tsSides[1].setTexcoordName(settingsB[0][1])
        self.top.setTexture(self.tsTop[1], settingsB[1][0])
        self.tsTop[1].setTexcoordName(settingsB[1][1])
        ival = Parallel(LerpFunctionInterval(self.setStageColor, duration, fromData = 0.0, toData = 1.0, extraArgs = [
            self.tsSides[2],
            settingsA[0][2],
            Vec4(0, 0, 0, 0)]), LerpFunctionInterval(self.setStageColor, duration, fromData = 0.0, toData = 1.0, extraArgs = [
            self.tsSides[1],
            Vec4(0, 0, 0, 0),
            settingsB[0][2]]), LerpFunctionInterval(self.setStageColor, duration, fromData = 0.0, toData = 1.0, extraArgs = [
            self.tsTop[1],
            Vec4(0, 0, 0, 0),
            Vec4(1, 1, 1, 1)]), LerpColorScaleInterval(self.sides, duration, settingsB[0][3]),
                                LerpColorScaleInterval(self.top, duration, settingsB[1][3]),
                                LerpColorScaleInterval(self.clouds, duration, settingsB[2]),
                                LerpColorScaleInterval(self.horizon, duration, settingsB[3]))
        return ival


