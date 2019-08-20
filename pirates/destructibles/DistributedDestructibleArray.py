from pirates.piratesbase.PiratesGlobals import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from pirates.piratesbase import PiratesGlobals
from direct.distributed import DistributedObject
from pirates.piratesbase import PLocalizer
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.destructibles import DistributedDestructibleObject
import copy

class DistributedDestructibleArray(DistributedDestructibleObject.DistributedDestructibleObject):
    notify = directNotify.newCategory('DistributedDestructibleArray')
    
    def __init__(self, cr):
        DistributedDestructibleObject.DistributedDestructibleObject.__init__(self, cr)
        NodePath.__init__(self, 'DistributedDestructibleArray')
        self.maxArrayHp = []
        self.arrayHp = []
        self.breakLevel = {}
        self.arrayObjects = {}
        self.HpDisplay = {}
        self.damageDummy = {}

    def delete(self):
        if base.cr.config.GetBool('want-ship-hpdisplay', 0) is 1:
            self.destroyHpDisplay()
        
        del self.arrayHp
        del self.maxArrayHp
        DistributedDestructibleObject.DistributedDestructibleObject.delete(self)
    
    def setArrayHp(self, hpArray):
        for index in range(len(self.arrayHp)):
            deltaHp = int(hpArray[index] - self.arrayHp[index])
            shouldRepair = self.arrayHp[index] <= 0
            self.arrayHp[index] = int(hpArray[index])
            if base.cr.config.GetBool('want-ship-hpdisplay', 0) is 1:
                self.updateHpDisplay(index)
            
            if deltaHp > 0:
                if shouldRepair:
                    self.respawn(index)
            
            if deltaHp < 0:
                for i in self.breakLevel:
                    if self.arrayHp[index] <= self.breakLevel[i] and deltaHp + self.arrayHp[index] >= self.breakLevel[i]:
                        self.playBreak(index)
                
                if self.prop:
                    if self.arrayHp[index] <= 0 and self.arrayHp[index] - deltaHp > 0:
                        self.playDeath(index)

        self.arrayHp = copy.copy(hpArray)
        for index in range(len(self.arrayHp)):
            self.arrayHp[index] = int(self.arrayHp[index])
    
    def getArrayHp(self, index):
        return self.arrayHp(index)

    def setMaxArrayHp(self, hpArray):
        self.maxArrayHp = copy.copy(hpArray)

    def getMaxArrayHp(self):
        return self.maxArrayHp

    def displayHp(self, index):
        self.hasHpMeter = 1
        self.damageDummy[index] = self.attachNewNode('damageDummy' + str(index))
        self.damageDummy[index].reparentTo(self.arrayObjects[index])
        self.damageDummy[index].setBillboardPointEye()
        self.HpDisplay[index] = DirectLabel(text = 'HP: ' + str(self.arrayHp[index]) + '/' + str(self.maxHp), scale = 3.0, relief = None, text_fg = (1, 1, 1, 1))
        self.HpDisplay[index].reparentTo(self.damageDummy[index])
        self.HpDisplay[index].setBin('fixed', 0)
        self.HpDisplay[index].setDepthTest(0)
    
    def updateHpDisplay(self, index):
        if self.hasHpMeter:
            self.HpDisplay[index]['text'] = 'Hp: ' + str(self.arrayHp[index]) + '/' + str(self.maxHp)

    def destroyHpDisplay(self):
        if self.hasHpMeter:
            for i in range(self.numArray):
                self.HpDisplay[i].removeNode()
            
            del self.HpDisplay
            for i in range(self.numArray):
                self.damageDummy[i].removeNode()
            
            del self.damageDummy

