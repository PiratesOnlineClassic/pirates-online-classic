from otp.otpbase import OTPGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.effects.Bonfire import Bonfire
from . import DistributedPCCannon

class DistributedIslandCannon(DistributedPCCannon.DistributedPCCannon):
    notify = directNotify.newCategory('DistributedIslandCannon')
    
    def __init__(self, cr):
        DistributedPCCannon.DistributedPCCannon.__init__(self, cr)
        self.pendingPlacement = None
        self.bf = None
        self.destructState = None
        self.island = None

    def announceGenerate(self):
        DistributedPCCannon.DistributedPCCannon.announceGenerate(self)
        self.addDestructableCollision()

    def disable(self):
        DistributedPCCannon.DistributedPCCannon.disable(self)
        if self.pendingPlacement:
            base.cr.relatedObjectMgr.abortRequest(self.pendingPlacement)
            self.pendingPlacement = None
        
        del self.island

    def setIslandId(self, islandId):
        self.islandId = islandId
        
        def putCannonOnIsland(island, self = self):
            self.notify.debug('putCannon %s on island %s' % (self.doId, islandId))
            self.island = island
            self.island.attachCannon(self)
            self.accept(island.uniqueName('disable'), self.islandDisable)
            self.cannonExitEvent = island.uniqueName('stopCannon')
            self.pendingPlacement = None

        if islandId > 0:
            self.pendingPlacement = base.cr.relatedObjectMgr.requestObjects([
                self.islandId], eachCallback = putCannonOnIsland)

    def setCannonIndex(self, cannonIndex):
        self.cannonIndex = cannonIndex

    def setIsDestructable(self, isDestructable):
        self.__isDestructable = isDestructable

    def setDestructState(self, state):
        if state != self.destructState:
            self.destructState = state
            if self.destructState == PiratesGlobals.CANNON_STATE_DESTRUCT:
                self.request('Off')
                bf = Bonfire(self)
                bf.reparentTo(self)
                bf.startLoop()
                self.bf = bf
            else:
                self.request('Idle')
                if self.bf:
                    self.bf.removeNode()
                    self.bf = None

    def addDestructableCollision(self):
        if self.__isDestructable:
            self.prop.coll.node().setIntoCollideMask(OTPGlobals.WallBitmask | PiratesGlobals.TargetBitmask)
            self.prop.coll.setTag('objType', str(PiratesGlobals.COLL_CANNON))
            self.prop.coll.setTag('cannonId', str(self.doId))
        
        self.prop.propCollisions.reparentTo(self)

    def islandDisable(self):
        if self.localAvatarUsingWeapon:
            self.stopWeapon(base.localAvatar)

    def sendHitByProjectile(self):
        if self.__isDestructable:
            self.sendUpdate('hitByProjectile')
        


