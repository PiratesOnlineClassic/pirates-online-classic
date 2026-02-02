from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *

from pirates.battle.DistributedWeaponAI import DistributedWeaponAI


class DistributedShipBroadsideAI(DistributedWeaponAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipBroadsideAI')

    def __init__(self, air):
        DistributedWeaponAI.__init__(self, air)

        self.shipId = 0
        self.geomParentId = 0

        self.leftBroadside = []
        self.rightBroadside = []

        self.leftBroadsideEnabledState = []
        self.rightBroadsideEnabledState = []

        self.baseTeam = 0
        self.ammoType = 0

    def requestBroadside(self, side, delays, hitPosList, zoneId, flightTime):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        ship = self.air.doId2do.get(self.shipId)
        if not ship:
            self.notify.warning('Cannot request broadside for unknown ship with doId: %d' % self.shipId)
            return

        if avatar.doId != ship.clientControllerDoId:
            return

        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        self.sendUpdate('doBroadside', [side, delays, hitPosList, zoneId, flightTime, timestamp])

    def setShipId(self, shipId):
        self.shipId = shipId

    def d_setShipId(self, shipId):
        self.sendUpdate('setShipId', [shipId])

    def b_setShipId(self, shipId):
        self.setShipId(shipId)
        self.d_setShipId(shipId)

    def getShipId(self):
        return self.shipId

    def getShip(self):
        return self.air.doId2do.get(self.shipId)

    def setGeomParentId(self, geomParentId):
        self.geomParentId = geomParentId

    def d_setGeomParentId(self, geomParentId):
        self.sendUpdate('setGeomParentId', [geomParentId])

    def b_setGeomParentId(self, geomParentId):
        self.setGeomParentId(geomParentId)
        self.d_setGeomParentId(geomParentId)

    def getGeomParentId(self):
        return self.geomParentId

    def setLeftBroadside(self, leftBroadside):
        self.leftBroadside = leftBroadside

    def getLeftBroadside(self):
        return self.leftBroadside

    def setRightBroadside(self, rightBroadside):
        self.rightBroadside = rightBroadside

    def getRightBroadside(self):
        return self.rightBroadside

    def setLeftBroadsideEnabledState(self, leftBroadsideEnabledState):
        self.leftBroadsideEnabledState = leftBroadsideEnabledState

    def d_setLeftBroadsideEnabledState(self, leftBroadsideEnabledState):
        self.sendUpdate('setLeftBroadsideEnabledState', [leftBroadsideEnabledState])

    def b_setLeftBroadsideEnabledState(self, leftBroadsideEnabledState):
        self.setLeftBroadsideEnabledState(leftBroadsideEnabledState)
        self.d_setLeftBroadsideEnabledState(leftBroadsideEnabledState)

    def getLeftBroadsideEnabledState(self):
        return self.leftBroadsideEnabledState

    def setRightBroadsideEnabledState(self, rightBroadsideEnabledState):
        self.rightBroadsideEnabledState = rightBroadsideEnabledState

    def d_setRightBroadsideEnabledState(self, rightBroadsideEnabledState):
        self.sendUpdate('setRightBroadsideEnabledState', [rightBroadsideEnabledState])

    def b_setRightBroadsideEnabledState(self, rightBroadsideEnabledState):
        self.setRightBroadsideEnabledState(rightBroadsideEnabledState)
        self.d_setRightBroadsideEnabledState(rightBroadsideEnabledState)

    def getRightBroadsideEnabledState(self):
        return self.rightBroadsideEnabledState

    def setBaseTeam(self, baseTeam):
        self.baseTeam = baseTeam

    def getBaseTeam(self):
        return self.baseTeam

    def setAmmoType(self, ammoType):
        self.ammoType = ammoType

    def getAmmoType(self):
        return self.ammoType

    def doBroadside(self, side, delays, hitPosList, zoneId, flightTime):
        """
        Fire a broadside from the AI.
        This is used by NPC ships to attack targets.
        """
        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        self.sendUpdate('doBroadside', [side, delays, hitPosList, zoneId, flightTime, timestamp])

    def fireAtTarget(self, targetShip, side):
        """
        Fire a broadside at a target ship.
        
        Args:
            targetShip: The target ship to fire at
            side: 0 for left, 1 for right
        """
        import random
        
        if not targetShip:
            return False
        
        ship = self.getShip()
        if not ship:
            return False
        
        try:
            # Get target position
            targetPos = targetShip.getPos()
            
            # Get zone for network transmission
            oceanGrid = ship.getParentObj()
            if not oceanGrid:
                return False
            
            zoneId = oceanGrid.getZoneFromXYZ(targetPos)
            zonePos = oceanGrid.getZoneCellOrigin(zoneId)
            
            # Calculate relative position
            relX = targetPos.getX() - zonePos[0]
            relY = targetPos.getY() - zonePos[1]
            relZ = targetPos.getZ() - zonePos[2] if hasattr(targetPos, 'getZ') else 0
            
            # Get distance for flight time calculation
            dist = ship.getDistance(targetShip)
            flightTime = max(1.0, dist / 500.0)  # Approximate flight time
            
            # Get actual number of cannons on this side
            if side == 0:
                numCannons = len(self.leftBroadside) if self.leftBroadside else 0
            else:
                numCannons = len(self.rightBroadside) if self.rightBroadside else 0
            
            if numCannons == 0:
                self.notify.warning('No broadside cannons on side %d' % side)
                return False
            
            # Generate cannon delays and hit positions with spread
            delays = []
            hitPosList = []
            
            for i in range(numCannons):
                delays.append(random.uniform(0, 0.5))
                # Add spread for realism
                spreadX = random.gauss(0, 25)
                spreadY = random.gauss(0, 25)
                spreadZ = random.gauss(0, 10)
                hitPosList.append((relX + spreadX, relY + spreadY, relZ + spreadZ))
            
            # Fire the broadside (visual)
            self.doBroadside(side, delays, hitPosList, zoneId, flightTime)
            
            # Apply damage directly on server
            # AI broadsides apply damage after a delay matching flight time
            self._applyBroadsideDamage(targetShip, numCannons, dist, flightTime)
            
            return True
            
        except Exception as e:
            self.notify.warning('Failed to fire broadside at target: %s' % str(e))
            import traceback
            traceback.print_exc()
            return False

    def _applyBroadsideDamage(self, targetShip, numCannons, distance, flightTime):
        """
        Apply broadside damage to target ship after a delay.
        This handles server-side damage for AI ship attacks.
        """
        from pirates.ship import ShipBalance
        
        def _doDamage(task):
            try:
                # Check if target still exists and is valid
                if not targetShip or targetShip.isEmpty():
                    return task.done
                
                # Get attacker ship for damage calculation
                ship = self.getShip()
                if not ship:
                    return task.done
                
                # Base damage per cannon (based on ship's level and broadside config)
                baseDamagePerCannon = 50  # Base damage
                
                # Apply NPC damage output modifier
                npcDamageOut = ShipBalance.NPCDamageOut.getValue()
                
                # Apply distance falloff (less damage at max range)
                maxRange = 2000.0
                distanceMod = max(0.3, 1.0 - (distance / maxRange) * 0.5)
                
                # Calculate hit chance per cannon (accuracy decreases with distance)
                baseAccuracy = 0.7  # 70% base accuracy
                accuracyFalloff = max(0.3, 1.0 - (distance / maxRange) * 0.4)
                hitChance = baseAccuracy * accuracyFalloff
                
                # Calculate total damage from cannons that hit
                import random
                totalDamage = 0
                hitsLanded = 0
                for i in range(numCannons):
                    if random.random() < hitChance:
                        cannonDamage = baseDamagePerCannon * npcDamageOut * distanceMod
                        totalDamage += cannonDamage
                        hitsLanded += 1
                
                if hitsLanded == 0:
                    return task.done  # All shots missed
                
                totalDamage = int(totalDamage)
                
                # Apply damage to target ship
                # Use takeDamage if available (NPCShipAI), otherwise set HP directly
                if hasattr(targetShip, 'takeDamage'):
                    targetShip.takeDamage(totalDamage, ship.doId, applyModifiers=False)
                else:
                    # Direct HP reduction for player ships
                    newHp = max(0, targetShip.getHp() - totalDamage)
                    targetShip.b_setHp(newHp)
                    
                    # Notify player ship's FSM if it has one
                    if hasattr(targetShip, 'gameFSM') and targetShip.gameFSM:
                        if hasattr(targetShip.gameFSM, 'onDamageReceived'):
                            targetShip.gameFSM.onDamageReceived(ship.doId, totalDamage)
                    
                    # Check for sinking
                    if newHp <= 0:
                        targetShip.b_setGameState('Sinking', 0)
                
            except Exception as e:
                self.notify.warning('Error applying broadside damage: %s' % str(e))
            
            return task.done
        
        # Schedule damage after flight time
        taskMgr.doMethodLater(flightTime, _doDamage, 
                              self.uniqueName('broadside-damage-%d' % targetShip.doId))
