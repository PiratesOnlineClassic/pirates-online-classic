from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *

from pirates.battle.DistributedPCCannonAI import DistributedPCCannonAI
from pirates.shipparts.DistributedShippartAI import DistributedShippartAI
from pirates.shipparts.CannonDNA import CannonDNA
from pirates.uberdog.UberDogGlobals import InventoryType


class DistributedCannonDNA(CannonDNA):
    pass


class DistributedShipCannonAI(DistributedPCCannonAI, DistributedShippartAI, DistributedCannonDNA):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipCannonAI')

    def __init__(self, air):
        DistributedPCCannonAI.__init__(self, air)
        DistributedShippartAI.__init__(self, air)
        DistributedCannonDNA.__init__(self)
        self.cannonIndex = 0

    def setCannonIndex(self, cannonIndex):
        self.cannonIndex = cannonIndex

    def d_setCannonIndex(self, cannonIndex):
        self.sendUpdate('setCannonIndex', [cannonIndex])

    def b_setCannonIndex(self, cannonIndex):
        self.setCannonIndex(cannonIndex)
        self.d_setCannonIndex(cannonIndex)

    def getCannonIndex(self):
        return self.cannonIndex

    def handleRequestInteraction(self, avatar, interactType, instant):
        self.startWeapon(avatar.doId)
        return self.ACCEPT

    def handleRequestExit(self, avatar):
        self.stopWeapon(avatar.doId)
        return self.ACCEPT

    def fireAtPosition(self, targetPos, skillId=None, ammoSkillId=None):
        """
        Fire this cannon at a target position.
        Used by AI to simulate crew firing deck cannons.
        
        Args:
            targetPos: Point3 target position
            skillId: Skill ID for the cannon shot (default: CannonShoot)
            ammoSkillId: Ammo type (default: CannonRoundShot)
        """
        if skillId is None:
            skillId = InventoryType.CannonShoot
        if ammoSkillId is None:
            ammoSkillId = InventoryType.CannonRoundShot
        
        try:
            # Get the ship this cannon belongs to
            ship = self.air.doId2do.get(self.shipId)
            if not ship:
                return False
            
            # Get zone for network transmission
            oceanGrid = ship.getParentObj()
            if not oceanGrid:
                return False
            
            zoneId = oceanGrid.getZoneFromXYZ(targetPos)
            zonePos = oceanGrid.getZoneCellOrigin(zoneId)
            
            # Calculate relative position for zone
            relX = targetPos.getX() - zonePos[0]
            relY = targetPos.getY() - zonePos[1]
            relZ = targetPos.getZ() - zonePos[2] if hasattr(targetPos, 'getZ') else 0
            
            # Get timestamp
            timestamp = globalClockDelta.getRealNetworkTime(bits=32)
            
            # Calculate position/heading for the shot
            # We'll use a simple approach - the cannon's position and direction to target
            shipPos = ship.getPos()
            
            # Calculate heading to target
            import math
            dx = targetPos.getX() - shipPos.getX()
            dy = targetPos.getY() - shipPos.getY()
            dz = targetPos.getZ() - shipPos.getZ() if hasattr(targetPos, 'getZ') else 0
            
            h = -math.degrees(math.atan2(dx, dy))
            dist = math.sqrt(dx*dx + dy*dy)
            p = math.degrees(math.atan2(dz, dist)) if dist > 0 else 0
            
            # PosHpr for the projectile
            posHpr = [shipPos.getX(), shipPos.getY(), shipPos.getZ() + 5, h, p, 0]
            
            # Send the projectile skill to clients (visual effect)
            charge = 0
            self.sendUpdate('useProjectileSkill', [skillId, ammoSkillId, posHpr, timestamp, charge])
            
            return True
            
        except Exception as e:
            self.notify.warning('Failed to fire cannon at position: %s' % str(e))
            return False
