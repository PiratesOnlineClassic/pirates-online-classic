from pandac.PandaModules import Vec3
from direct.task import Task
from pirates.effects.WaterRipple2 import WaterRipple2
from pirates.effects.TentacleWaterDrips import TentacleWaterDrips
from pirates.effects.TentacleFire import TentacleFire

class TentacleUtils:
    
    def __init__(self):
        self.statusTable = []
        self.effectsScale = 1.0
    
    def initStatusTable(self):
        self.statusTable = []
        joints = self.findAllMatches('**/def_ten*').asList()
        for i in range(len(joints) - 1):
            self.statusTable.append([
                joints[i],
                joints[i + 1],
                0,
                Vec3(0, 0, 0),
                [None, None, None]])

    def setEffectsScale(self, scale):
        self.effectsScale = scale

    def updateStatusTable(self):
        for i in range(len(self.statusTable)):
            tempWaterPos = self.getWaterPos(self.statusTable[i][0], self.statusTable[i][1])
            self.statusTable[i][3] = tempWaterPos
            joint1Z = self.statusTable[i][0].getZ(render)
            joint2Z = self.statusTable[i][1].getZ(render)
            if joint1Z > tempWaterPos[2] and joint2Z > tempWaterPos[2]:
                if self.statusTable[i][2] != 2:
                    self.stopRippleEffect(i)
                    self.statusTable[i][2] = 2

            elif joint1Z > tempWaterPos[2] and joint2Z <= tempWaterPos[2] or joint1Z <= tempWaterPos[2] and joint2Z > tempWaterPos[2]:
                if self.statusTable[i][2] != 1:
                    self.startRippleEffect(i)
                    self.startWaterDripEffect(i)
                    self.statusTable[i][2] = 1

            elif self.statusTable[i][2] != 0:
                self.stopAllEffects(i)
                self.statusTable[i][2] = 0

    def getWaterPos(self, aboveJoint, belowJoint):
        avgPos = (aboveJoint.getPos(render) + belowJoint.getPos(render)) / 2.0
        waterHeight = base.cr.activeWorld.getWater().calcHeight(avgPos[0], avgPos[1], 0, render)
        return Vec3(avgPos[0], avgPos[1], waterHeight)
    
    def startRippleEffect(self, section):
        if not self.statusTable[section][4][0]:
            self.statusTable[section][4][0] = WaterRipple2.getEffect()
            if self.statusTable[section][4][0]:
                self.statusTable[section][4][0].reparentTo(self)
                self.statusTable[section][4][0].setEffectScale(self.effectsScale)
                self.statusTable[section][4][0].startLoop()

    def stopRippleEffect(self, section):
        if self.statusTable[section][4][0]:
            self.statusTable[section][4][0].stopLoop()
            self.statusTable[section][4][0] = None
    
    def startWaterDripEffect(self, section):
        if not self.statusTable[section][4][1]:
            self.statusTable[section][4][1] = TentacleWaterDrips.getEffect()
            if self.statusTable[section][4][1]:
                length = self.statusTable[section][0].getDistance(self.statusTable[section][1])
                self.statusTable[section][4][1].reparentTo(self.statusTable[section][1])
                self.statusTable[section][4][1].setEffectScale(self.effectsScale)
                self.statusTable[section][4][1].setEffectLength(length)
                self.statusTable[section][4][1].play()

    def stopWaterDripEffect(self, section):
        if self.statusTable[section][4][1]:
            self.statusTable[section][4][1].stop()
            self.statusTable[section][4][1] = None

    def startFireEffect(self, section):
        if not self.statusTable[section][4][2]:
            self.statusTable[section][4][2] = TentacleFire.getEffect()
            if self.statusTable[section][4][2]:
                length = self.statusTable[section][0].getDistance(self.statusTable[section][1])
                self.statusTable[section][4][2].reparentTo(self.statusTable[section][1])
                self.statusTable[section][4][2].setEffectScale(self.effectsScale)
                self.statusTable[section][4][2].setEffectLength(length)
                self.statusTable[section][4][2].startLoop()

    def stopFireEffect(self, section):
        if self.statusTable[section][4][2]:
            self.statusTable[section][4][2].stopLoop()
            self.statusTable[section][4][2] = None

    def stopAllEffects(self, section):
        self.stopRippleEffect(section)
        self.stopWaterDripEffect(section)
        self.stopFireEffect(section)

    def removeEffects(self):
        for i in range(len(self.statusTable)):
            self.stopAllEffects(i)
    
    def updateEffects(self):
        for i in range(len(self.statusTable)):
            if self.statusTable[i][4][0]:
                self.statusTable[i][4][0].setPos(render, self.statusTable[i][3])
                self.statusTable[i][4][0].particleDummy.setZ(render, self.statusTable[i][3][2] + 2.0)
    
    def startUpdateTask(self):
        taskMgr.add(self.updateTask, self.uniqueName('updateTask'))
    
    def stopUpdateTask(self):
        taskMgr.remove(self.uniqueName('updateTask'))
    
    def updateTask(self, task):
        self.updateStatusTable()
        self.updateEffects()
        return task.cont

    def uniqueName(self, str):
        pass


