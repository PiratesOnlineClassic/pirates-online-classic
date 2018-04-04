
from pirates.battle.DistributedPCCannonAI import DistributedPCCannonAI
from direct.directnotify import DirectNotifyGlobal

class DistributedIslandCannonAI(DistributedPCCannonAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedIslandCannonAI')

    def __init__(self, air):
        DistributedPCCannonAI.__init__(self, air)
        self.cannonIndex = 0
        self.islandId = 0
        self.isDestructable = 0
        self.destructState = 0


    # setCannonIndex(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setCannonIndex(self, cannonIndex):
        self.cannonIndex = cannonIndex

    def d_setCannonIndex(self, cannonIndex):
        self.sendUpdate('setCannonIndex', [cannonIndex])

    def b_setCannonIndex(self, cannonIndex):
        self.setCannonIndex(cannonIndex)
        self.d_setCannonIndex(cannonIndex)

    def getCannonIndex(self):
        return self.cannonIndex

    # setIslandId(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setIslandId(self, islandId):
        self.islandId = islandId

    def d_setIslandId(self, islandId):
        self.sendUpdate('setIslandId', [islandId])

    def b_setIslandId(self, islandId):
        self.setIslandId(islandId)
        self.d_setIslandId(islandId)

    def getIslandId(self):
        return self.islandId

    # setIsDestructable(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setIsDestructable(self, isDestructable):
        self.isDestructable = isDestructable

    def d_setIsDestructable(self, isDestructable):
        self.sendUpdate('setIsDestructable', [isDestructable])

    def b_setIsDestructable(self, isDestructable):
        self.setIsDestructable(isDestructable)
        self.d_setIsDestructable(isDestructable)

    def getIsDestructable(self):
        return self.isDestructable

    # setDestructState(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setDestructState(self, destructState):
        self.destructState = destructState

    def d_setDestructState(self, destructState):
        self.sendUpdate('setDestructState', [destructState])

    def b_setDestructState(self, destructState):
        self.setDestructState(destructState)
        self.d_setDestructState(destructState)

    def getDestructState(self):
        return self.destructState

    # hitByProjectile() airecv clsend

    def hitByProjectile(self, hitByProjectile):
        pass


