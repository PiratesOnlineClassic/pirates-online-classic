from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship import ShipGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.shipparts.DistributedShipRepairSpotAI import DistributedShipRepairSpotAI
from pirates.quest.QuestConstants import LocationIds


class PlayerShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayerShipAI')

    # matches the length of the client's sinking movie:
    SinkDuration = 20.0
    DockTimerDuration = 30.0

    def __init__(self, air):
        DistributedShipAI.__init__(self, air)

        self.allowCrewState = True
        self.allowFriendState = True
        self.allowGuildState = False
        self.allowPublicState = False
        self.siegeBounty = 0
        self.lastAttacked = 0
        self.pendingRespawnCrew = set()
        self.repairSpots = []

    def setAllowCrewState(self, allowCrewState):
        self.allowCrewState = allowCrewState

    def d_setAllowCrewState(self, allowCrewState):
        self.sendUpdate('setAllowCrewState', [allowCrewState])

    def b_setAllowCrewState(self, allowCrewState):
        self.setAllowCrewState(allowCrewState)
        self.d_setAllowCrewState(allowCrewState)

    def getAllowCrewState(self):
        return self.allowCrewState

    def setAllowFriendState(self, allowFriendState):
        self.allowFriendState = allowFriendState

    def d_setAllowFriendState(self, allowFriendState):
        self.sendUpdate('setAllowFriendState', [allowFriendState])

    def b_setAllowFriendState(self, allowFriendState):
        self.setAllowFriendState(allowFriendState)
        self.d_setAllowFriendState(allowFriendState)

    def getAllowFriendState(self):
        return self.allowFriendState

    def setAllowGuildState(self, allowGuildState):
        self.allowGuildState = allowGuildState

    def d_setAllowGuildState(self, allowGuildState):
        self.sendUpdate('setAllowGuildState', [allowGuildState])

    def b_setAllowGuildState(self, allowGuildState):
        self.setAllowGuildState(allowGuildState)
        self.d_setAllowGuildState(allowGuildState)

    def getAllowGuildState(self):
        return self.allowGuildState

    def setAllowPublicState(self, allowPublicState):
        self.allowPublicState = allowPublicState

    def d_setAllowPublicState(self, allowPublicState):
        self.sendUpdate('setAllowPublicState', [allowPublicState])

    def b_setAllowPublicState(self, allowPublicState):
        self.setAllowPublicState(allowPublicState)
        self.d_setAllowPublicState(allowPublicState)

    def getAllowPublicState(self):
        return self.allowPublicState

    def setCaptainId(self, captainId):
        oldCaptainId = self.captainId
        DistributedShipAI.setCaptainId(self, captainId)
        if oldCaptainId and oldCaptainId != captainId:
            self.ignore('bandIdChanged-%d' % oldCaptainId)

        if captainId:
            # the ship belongs to the captain's crew, keep it updated
            # whenever the captain joins or leaves a crew...
            self.accept('bandIdChanged-%d' % captainId, self._captainBandIdChanged)

        self.updateBandId()

    def _captainBandIdChanged(self, bandManagerId, bandId):
        self.updateBandId()

    def updateBandId(self):
        if not self.isGenerated():
            return

        bandManagerId, bandId = 0, 0
        captain = self.air.doId2do.get(self.captainId)
        if captain is not None and hasattr(captain, 'getBandId'):
            bandManagerId, bandId = captain.getBandId()

        if [bandManagerId, bandId] != list(self.bandId):
            self.b_setBandId(bandManagerId, bandId)

    def setSiegeBounty(self, siegeBounty):
        self.siegeBounty = siegeBounty

    def d_setSiegeBounty(self, siegeBounty):
        self.sendUpdate('setSiegeBounty', [siegeBounty])

    def b_setSiegeBounty(self, siegeBounty):
        self.setSiegeBounty(siegeBounty)
        self.d_setSiegeBounty(siegeBounty)

    def getSiegeBounty(self):
        return self.siegeBounty

    def d_attacked(self):
        self.sendUpdate('attacked', [])

    def shipAttacked(self, attackerShipId, damage):
        DistributedShipAI.shipAttacked(self, attackerShipId, damage)

        # let the crew know the ship was attacked, this prevents
        # the ship from docking for a short period of time...
        self.lastAttacked = globalClock.getFrameTime()
        self.d_attacked()

    def getAttackTimerRemaining(self):
        if not self.lastAttacked:
            return 0

        return max(0, int(self.DockTimerDuration - (globalClock.getFrameTime() - self.lastAttacked)))

    def _clearDockTimer(self):
        self.lastAttacked = 0

    def setGameState(self, stateName, avId, timeStamp=0):
        DistributedShipAI.setGameState(self, stateName, avId, timeStamp)

        # a ship that is no longer at sea should not be listed as deployed:
        if stateName in ('Sunk', 'PutAway'):
            self.air.shipManager.removePlayerShip(self)

    def handleShipSunk(self):
        # player ships are never deleted when they sink, the ship stays in the avatar's
        # inventory with zero hp until it has been repaired by a shipwright...
        self.b_setGameState('Sunk', 0)
        self.sendCrewToReturnLocation()

    def sendCrewToReturnLocation(self):
        parentObj = self.getParentObj()
        world = parentObj.getParentObj() if parentObj is not None else None
        for avatarId in list(self.crew):
            avatar = self.air.doId2do.get(avatarId)
            if not avatar:
                continue

            locationUid = self.getCrewReturnLocation(avatar, world)
            if not locationUid:
                self.notify.warning('Cannot send avatar %d home from sunk ship %d, '
                    'no return location available!' % (avatar.doId, self.doId))

                continue

            self.air.teleportMgr.d_initiateTeleport(avatar, locationUid=locationUid,
                targetWorld=world)

    def getCrewReturnLocation(self, avatar, world):
        if world is None or not hasattr(world, 'builder'):
            return None

        locationUid = avatar.getReturnLocation() or LocationIds.PORT_ROYAL_ISLAND
        if world.builder.getObject(uniqueId=locationUid):
            return locationUid

        # the avatar's return location is not within this ocean,
        # fall back to the first island they're able to dock at...
        for island in world.builder.getIslands():
            if not island.getUndockable():
                return island.getUniqueId()

        return None

    def respawnShip(self, parentId, zoneId):
        # used by game modes which respawn a sunk ship back out at sea,
        # once all of the crew have arrived the ship recovers from being sunk...
        self.pendingRespawnCrew = set(self.crew)
        for avatarId in self.crew:
            self.d_setRespawnLocation(avatarId, parentId, zoneId)

        self.b_setLocation(parentId, zoneId)
        if not self.pendingRespawnCrew:
            self._respawnComplete()

    def clientReachedRespawnLocation(self):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.pendingRespawnCrew:
            return

        self.pendingRespawnCrew.discard(avatarId)
        if not self.pendingRespawnCrew:
            self._respawnComplete()

    def _respawnComplete(self):
        self.repairShip()
        self.b_setGameState('RecoverFromSunk', 0)
        self.b_setGameState('Adrift', 0)

    def createRepairSpots(self):
        # repair spots are only used by ships which belong to a PvP or siege team,
        # this is called by the game mode once the ship's team has been assigned...
        from pirates.pvp import PVPGlobals

        self.deleteRepairSpots()
        locators = PVPGlobals.ShipClass2repairLocators.get(self.shipClass)
        if not locators:
            return

        for index in locators.getValue():
            repairSpot = DistributedShipRepairSpotAI(self.air)
            repairSpot.setShipId(self.doId)
            repairSpot.setIndex(index)
            self.generateChildWithRequired(repairSpot, PiratesGlobals.ShipZoneOnDeck)
            self.repairSpots.append(repairSpot)

    def deleteRepairSpots(self):
        for repairSpot in self.repairSpots:
            repairSpot.requestDelete()

        self.repairSpots = []

    def delete(self):
        self.ignoreAll()
        self.deleteRepairSpots()
        self.air.shipManager.removePlayerShip(self)
        DistributedShipAI.delete(self)
