
from pirates.destructibles.DistributedDestructibleObjectAI import DistributedDestructibleObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedDestructibleArrayAI(DistributedDestructibleObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDestructibleArrayAI')

    def __init__(self, air):
        DistributedDestructibleObjectAI.__init__(self, air)
        self.maxArrayHp = 0
        self.arrayHp = 0


    # setMaxArrayHp(int16array) required broadcast ram db
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setMaxArrayHp(self, maxArrayHp):
        self.maxArrayHp = maxArrayHp

    def d_setMaxArrayHp(self, maxArrayHp):
        self.sendUpdate('setMaxArrayHp', [maxArrayHp])

    def b_setMaxArrayHp(self, maxArrayHp):
        self.setMaxArrayHp(maxArrayHp)
        self.d_setMaxArrayHp(maxArrayHp)

    def getMaxArrayHp(self):
        return self.maxArrayHp

    # setArrayHp(int16array) required broadcast ram db
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setArrayHp(self, arrayHp):
        self.arrayHp = arrayHp

    def d_setArrayHp(self, arrayHp):
        self.sendUpdate('setArrayHp', [arrayHp])

    def b_setArrayHp(self, arrayHp):
        self.setArrayHp(arrayHp)
        self.d_setArrayHp(arrayHp)

    def getArrayHp(self):
        return self.arrayHp


