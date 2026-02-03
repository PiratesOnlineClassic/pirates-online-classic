from direct.directnotify import DirectNotifyGlobal
from pirates.battle.DistributedIslandCannonAI import DistributedIslandCannonAI


class DistributedFortCannonAI(DistributedIslandCannonAI):
    """
    AI-side implementation of a cannon that belongs to a fort.
    
    Fort cannons are positioned on forts and can be used by NPCs
    to attack player ships during the Black Pearl treasure map quest.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFortCannonAI')

    def __init__(self, air):
        DistributedIslandCannonAI.__init__(self, air)
        
        self.uniqueId = ''
        self.fortId = 0
        self.cannonIndex = 0
        self.islandId = 0
        self.isDestructable = 0
        self.destructState = 0

    # =========================================================================
    # DC Fields
    # =========================================================================

    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def getUniqueId(self):
        return self.uniqueId

    def setFortId(self, fortId):
        self.fortId = fortId

    def d_setFortId(self, fortId):
        self.sendUpdate('setFortId', [fortId])

    def b_setFortId(self, fortId):
        self.setFortId(fortId)
        self.d_setFortId(fortId)

    def getFortId(self):
        return self.fortId

    def setCannonIndex(self, index):
        self.cannonIndex = index

    def d_setCannonIndex(self, index):
        self.sendUpdate('setCannonIndex', [index])

    def b_setCannonIndex(self, index):
        self.setCannonIndex(index)
        self.d_setCannonIndex(index)

    def getCannonIndex(self):
        return self.cannonIndex

    def setIslandId(self, islandId):
        self.islandId = islandId

    def d_setIslandId(self, islandId):
        self.sendUpdate('setIslandId', [islandId])

    def b_setIslandId(self, islandId):
        self.setIslandId(islandId)
        self.d_setIslandId(islandId)

    def getIslandId(self):
        return self.islandId

    def setIsDestructable(self, isDestructable):
        self.isDestructable = isDestructable

    def d_setIsDestructable(self, isDestructable):
        self.sendUpdate('setIsDestructable', [isDestructable])

    def b_setIsDestructable(self, isDestructable):
        self.setIsDestructable(isDestructable)
        self.d_setIsDestructable(isDestructable)

    def getIsDestructable(self):
        return self.isDestructable

    def setDestructState(self, destructState):
        self.destructState = destructState

    def d_setDestructState(self, destructState):
        self.sendUpdate('setDestructState', [destructState])

    def b_setDestructState(self, destructState):
        self.setDestructState(destructState)
        self.d_setDestructState(destructState)

    def getDestructState(self):
        return self.destructState

    # =========================================================================
    # Combat
    # =========================================================================

    def hitByProjectile(self):
        """Called when the cannon is hit by a projectile"""
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return

        # If destructable, take damage
        if self.isDestructable:
            self.b_setDestructState(1)  # Destroyed state