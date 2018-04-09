from direct.directnotify import DirectNotifyGlobal
from pirates.destructibles.DistributedDestructibleObjectAI import DistributedDestructibleObjectAI

class DistributedDestructibleArrayAI(DistributedDestructibleObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDestructibleArrayAI')

    def __init__(self, air):
        DistributedDestructibleObjectAI.__init__(self, air)
        self.maxHp = [100]
        self.hp = [100]
        
    def setArrayHp(self, hp):
        self.hp = hp
    
    def d_setArrayHp(self, hp):
        self.sendUpdate("setArrayHp", [hp])
        
    def b_setArrayHp(self, hp):
        self.setArrayHp(hp)
        self.d_setArrayHp(hp)
        
    def setMaxArrayHp(self, hp):
        self.maxHp = hp
    
    def d_setMaxArrayHp(self, hp):
        self.sendUpdate("setMaxArrayHp", [hp])
        
    def b_setMaxArrayHp(self, hp):
        self.setMaxArrayHp(hp)
        self.d_setMaxArrayHp(hp)