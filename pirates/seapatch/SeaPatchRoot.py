from panda3d.core import Vec2, VBase2, VBase4, Vec4, PerlinNoise3
from direct.directnotify.DirectNotifyGlobal import directNotify
import math


class SeaPatchRoot(object):
    notify = directNotify.newCategory('SeaPatchRoot')

    WTZ = None #TODO
    WTV = None #TODO
    WTU = None #TODO
    WFSin = None #TODO
    WFNoise = PerlinNoise3()

    def __init__(self):
        self.seaLevel = 0.0
        self.waves = []
        self.center = NodePath('center')
        self.anchor = NodePath('anchor')
        self.overallSpeed = 0.0
        self.uvSpeed = Vec2(0, 0)
        self.passiveMove = Vec2(0.0001, 0.0001)
        self.thresfold = 80
        self.radius = 100
        self.uvScale = VBase2(36.0, 36.0)
        self.waveEnabled = 0
        self.normalDamper = 1.0
        self.heightDamper = 0.5
        self.high = VBase4(0.2, 0.40000001, 0.60000002, 1.0)
        self.mid = VBase4(0.2, 0.40000001, 0.60000002, 1.0)
        self.low = VBase4(0.2, 0.40000001, 0.60000002, 1.0)

    def enable(self):
        self.waveEnabled = 1

    def isEnabled(self):
        return self.waveEnabled

    def disable(self):
        self.waveEnabled = 0

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
        self.thresfold = 80
        self.radius = 100
        self.uvScale = VBase2(36.0, 36.0)
        self.waveEnabled = 0
        self.normalDamper = 1.0
        self.heightDamper = 0.5
        self.high = VBase4(0.2, 0.40000001, 0.60000002, 1.0)
        self.mid = VBase4(0.2, 0.40000001, 0.60000002, 1.0)
        self.low = VBase4(0.2, 0.40000001, 0.60000002, 1.0)

    def assignPropertiesFrom(self, wave):
        pass

    def allocateWave(self, todo1):
        pass

    def animateHeight(self, doAnimate):
        pass

    def animateUv(self, doAnimate):
        pass

    def calcHeight(self, x, y, dist):
        return 0

    def calcFilteredHeight(self, apX, apY, minWaveLength, dist2):
        pass

    def calcHeightForMass(self, todo1, todo2, todo3, todo4, todo5):
        pass

    def calcNormal(self, height, ax, ay, dist):
        return 0

    def calcNormalForMass(self, height, ax, ay, dist2, mass, area):
        return 0

    def calcFlatWellScale(self, apX, apY):
        pass

    def calcUv(self, todo1, todo2, todo3, todo4):
        pass

    def calcColor(self, color, height, x, y):
        pass

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
        return self.thresfold

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

    def setNormalDamper(self, todo1):
        pass

    def getNormalDamper(self):
        pass

    def enableWave(self, waveEnabled):
        self.waveEnabled = waveEnabled

    def setWaveTarget(self, layer, waveTarget):
        pass

    def setWaveFunc(self, layer, waveFunc):
        pass

    def setChoppyK(self, layer, choppyK):
        pass

    def setWaveAmplitude(self, layer, waveAmplitude):
        pass

    def setWaveLength(self, layer, waveLength):
        pass

    def getWaveLength(self):
        return

    def setWaveSpeed(self, layer, waveSpeed):
        pass

    def setWaveDirection(self, layer, waveDirection):
        pass
