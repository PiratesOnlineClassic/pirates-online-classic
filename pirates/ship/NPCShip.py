from pirates.ship.DistributedShip import DistributedShip
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPGlobals
from . import ShipBalance

class NPCShip(DistributedShip):
    
    def __init__(self, cr):
        DistributedShip.__init__(self, cr)
        self.isNpc = 1
    
    def announceGenerate(self):
        self.setupAggroCollisions()
        DistributedShip.announceGenerate(self)

    def disable(self):
        self.cleanupAggroCollisions()
        DistributedShip.disable(self)

    def getNPCship(self):
        return True

    def updatePickable(self):
        self.setPickable(0)
    
    def canBoard(self, avId):
        return True

    def getDamageInputModifier(self):
        return ShipBalance.NPCDamageIn.getValue()
    
    def getDamageOutputModifier(self):
        return ShipBalance.NPCDamageOut.getValue()

    def setupSmoothing(self):
        self.activateSmoothing(1, 0)
        self.smoother.setDelay(OTPGlobals.NetworkLatency * 1.5)
        broadcastPeriod = PiratesGlobals.AI_BROADCAST_PERIOD
        self.smoother.setMaxPositionAge(broadcastPeriod * 1.25 * 10)
        self.smoother.setExpectedBroadcastPeriod(broadcastPeriod)
        self.smoother.setDefaultToStandingStill(False)
        self.setSmoothWrtReparents(True)
        self.startSmooth()


