import math

from panda3d.core import *
from direct.directnotify.DirectNotifyGlobal import directNotify

class SeaPatchLayer(object):

    def __init__(self, id):
        self.id = id
        self.waveTarget = SeaPatchRoot.WTZ
        self.waveFunc = SeaPatchRoot.WFSin
        self.waveDirection = Vec2(0, 0)
        self.choppyK = 1
        self.waveAmplitude = 0.0
        self.waveLength = 0.0
        self.waveSpeed = 1
    
class SeaPatchRoot(object):
    notify = directNotify.newCategory('SeaPatchRoot')
    
    noiseTableSize = 64
    WTZ = None #TODO
    WTV = None #TODO
    WTU = None #TODO
    WFSin = 2
    WFNoise = 1

    def __init__(self):
        self.seaLevel = 0.0
        self.waves = []
        self.center = NodePath('center')
        self.anchor = NodePath('anchor')
        self.overallSpeed = 0.0
        self.uvSpeed = Vec2(0, 0)
        self.passiveMove = Vec2(0.0001, 0.0001)
        self.threshold = 80
        self.radius = 100
        self.uvScale = VBase2(36.0, 36.0)
        self.waveEnabled = False
        self.normalDamper = 1.0
        self.heightDamper = 0.5
        self.high = VBase4(0.2, 0.40000001, 0.60000002, 1.0)
        self.mid = VBase4(0.2, 0.40000001, 0.60000002, 1.0)
        self.low = VBase4(0.2, 0.40000001, 0.60000002, 1.0)
        self.perlin = PerlinNoise2(512, 512, self.noiseTableSize)

    def enable(self):
        self.waveEnabled = True

    def isEnabled(self):
        return self.waveEnabled

    def disable(self):
        self.waveEnabled = False

    def addFlatWell(self, todo1, todo2, todo3, todo4, todo5, todo6):
        pass

    def removeFlatWell(self, uniqueName):
        pass

    def resetEnvironment(self):
        pass

    def assignEnviormentFrom(self, todo1):
        pass

    def resetProperties(self):
        self.seaLevel = 0.0
        self.center = NodePath('center')
        self.anchor = NodePath('anchor')
        self.overallSpeed = 0.0
        self.uvSpeed = Vec2(0, 0)
        self.passiveMove = Vec2(0.0001, 0.0001)
        self.threshold = 80
        self.radius = 100
        self.uvScale = VBase2(36.0, 36.0)
        self.normalDamper = 1.0
        self.heightDamper = 0.5
        self.high = VBase4(0.2, 0.40000001, 0.60000002, 1.0)
        self.mid = VBase4(0.2, 0.40000001, 0.60000002, 1.0)
        self.low = VBase4(0.2, 0.40000001, 0.60000002, 1.0)

    def assignPropertiesFrom(self, wave):
        self.seaLevel = wave.seaLevel
        self.center = wave.center
        self.anchor = wave.anchor
        self.overallSpeed = wave.overallSpeed
        self.uvSpeed = wave.uvSpeed
        self.passiveMove = wave.passiveMove
        self.threshold = wave.threshold
        self.radius = wave.radius
        self.uvScale = wave.uvScale
        self.normalDamper = wave.normalDamper
        self.heightDamper = wave.heightDamper
        self.high = wave.high
        self.mid = wave.mid
        self.low = wave.low

    def allocateWave(self, index):
        pass

    def animateHeight(self, doAnimate):
        pass

    def animateUv(self, doAnimate):
        pass
    
    def __waveSin(self, x, y, layer):
        frameTime = globalClock.getFrameTime()
        waveSpeed = self.overallSpeed + layer.waveSpeed
        slider = frameTime * waveSpeed

        h = math.sin(slider + (x/layer.waveLength))
        h += math.sin(slider + (y/layer.waveLength)) * layer.waveAmplitude
        return h

    def __wavePerlin(self, x, y, layer):
        frameTime = globalClock.getFrameTime()
        waveSpeed = self.overallSpeed + layer.waveSpeed
        slider = frameTime * waveSpeed

        x = (x/layer.waveLength) + slider
        y = (y/layer.waveLength) + slider

        return self.perlin.noise(x, y) * layer.waveAmplitude

    def calcHeight(self, x, y, dist):

        newCenter = self.center.getPos()
        cx = newCenter.getX()
        cy = newCenter.getY()

        # Calculate the wave
        heightChange = 0
        for layer in self.waves:
            if layer.waveFunc == self.WFSin:
                heightChange += self.__waveSin(x, y, layer)
            elif layer.waveFunc == self.WFNoise:
                heightChange += self.__wavePerlin(x, y, layer)

        # Calculate distance for fading out waves
        dist = float(math.sqrt(math.pow(x - cx, 2) + math.pow(y - cy,2)))

        finalHeight = heightChange
        if (dist > self.threshold):
            if (dist >= self.radius):
                finalHeight = 0.0 # Complete faded out
            else:
                finalHeight = heightChange * ((self.radius - dist)/self.radius) # Linear fade

        return finalHeight

    def calcFilteredHeight(self, apX, apY, minWaveLength, dist2):
        pass

    def calcHeightForMass(self, todo1, todo2, todo3, todo4, todo5):
        pass

    def calcNormal(self, height, ax, ay, dist):
        h = self.getHeight(ax, ay, dist)
        h1 = self.getHeight(ax - 0.3, ay + 0.2, dist)
        h2 = self.getHeight(ax - 0.4, ay - 0.1, dist)

        a = LVecBase3f(ax - 0.3, ay + 0.2, h1)
        b = LVecBase3f(ax - 0.4, ay - 0.1, h2)
        s = LVecBase3f(ax, ay, h)

        a1 = a - s
        b1 = b - s

        n = LVecBase3f.cross(a1, b1)
        length = float(math.sqrt(n.getX() * n.getX() + n.getY() * n.getY() + n.getZ() * n.getZ()))

        if length == 0:
            length = 1.0

        n.setX(n.getX()/length)
        n.setY(n.getY()/length)
        n.setZ(n.getZ()/length)

        return n

    def calcNormalForMass(self, height, ax, ay, dist2, mass, area):
        return 0

    def calcFlatWellScale(self, apX, apY):
        pass

    def calcUv(self, todo1, todo2, todo3, todo4):
        pass

    def calcColor(self, color, height, x, y):
        
        colorChoice = self.high #TODO

        cx = (color + colorChoice.getX() + (height / (2 * self.amplitude)))/3.0
        cy = (color + colorChoice.getY() + (height / (2 * self.amplitude)))/3.0
        cz = (color + colorChoice.getZ() + (height / (2 * self.amplitude)))/3.0
        ca = (self.alphaScale + colorChoice.getW() + (1.0 - (height / (2 * self.amplitude))))/3.0

        return LVecBase4f(cx, cy, cz, ca)

    def calcReflection(self, todo1, todo2):
        pass

    def setSeaLevel(self, seaLevel):
        self.seaLevel = seaLevel

    def getSeaLevel(self):
        return self.seaLevel

    def setCenter(self, center):
        self.center = center

    def getCenter(self):
        return self.center

    def setAnchor(self, anchor):
        self.anchor = anchor

    def getAnchor(self):
        return self.anchor

    def setOverallSpeed(self, overallSpeed):
        self.overallSpeed = overallSpeed

    def getOverallSpeed(self):
        return self.overallSpeed

    def setUvSpeed(self, uvSpeed):
        self.uvSpeed = uvSpeed

    def getUvSpeed(self):
        return self.uvSpeed

    def setThreshold(self, threshold):
        self.threshold = threshold

    def getThreshold(self):
        return self.threshold

    def setRadius(self, radius):
        self.radius = radius

    def getRadius(self):
        return self.radius

    def setUvScale(self, scale):
        self.uvScale = scale

    def setHighColor(self, high):
        self.high = high
        self.mid = (self.low + self.high) * 0.5

    def getHighColor(self):
        return self.high

    def getMidColor(self):
        return self.mid

    def setLowColor(self, low):
        self.low = low
        self.mid = (self.low + self.high) * 0.5

    def getLowColor(self):
        return self.low

    def clampColor(self, color):
        pass

    def setNormalDamper(self, normalDamper):
        self.normalDamper = normalDamper

    def getNormalDamper(self):
        return self.normalDamper

    def enableWave(self, layer):
        self.waves.append(SeaPatchLayer(layer))

    def getWaveFromId(self, id):
        for layer in self.waves:
            if layer.id == id:
                return layer

        return None

    def setWaveTarget(self, index, waveTarget):
        layer = self.getWaveFromId(index)
        if layer:
            layer.waveTarget = waveTarget

    def setWaveFunc(self, index, waveFunc):
        layer = self.getWaveFromId(index)
        if layer:
            layer.waveFunc = waveFunc

    def setChoppyK(self, index, choppyK):
        layer = self.getWaveFromId(index)
        if layer:
            layer.choppyK = choppyK

    def setWaveAmplitude(self, index, waveAmplitude):
        layer = self.getWaveFromId(index)
        if layer:
            layer.waveAmplitude = waveAmplitude
    
    def setWaveLength(self, index, waveLength):
        layer = self.getWaveFromId(index)
        if layer:
            layer.waveLength = waveLength

    def getWaveLength(self, index):
        layer = self.getWaveFromId(index)
        if layer:
            return layer.waveLength
        return 0.0

    def setWaveSpeed(self, index, waveSpeed):
        layer = self.getWaveFromId(index)
        if layer:
            layer.waveSpeed = waveSpeed

    def setWaveDirection(self, index, waveDirection):
        layer = self.getWaveFromId(index)
        if layer:
            layer.waveDirection = waveDirection
