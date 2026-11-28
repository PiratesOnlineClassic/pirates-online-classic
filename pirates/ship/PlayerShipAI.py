import random

from direct.directnotify import DirectNotifyGlobal

from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship import ShipGlobals
from pirates.economy import EconomyGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.shipparts.DistributedShipRepairSpotAI import DistributedShipRepairSpotAI
from pirates.quest.QuestConstants import LocationIds


class PlayerShipAI(DistributedShipAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayerShipAI')

    # matches the length of the client's sinking movie:
    SinkDuration = 20.0
    DockTimerDuration = 30.0

    # the dock timer is counted down by the client too, allow for some latency:
    DockTimerTolerance = 2.0

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
        self.missionStartTime = 0
        self.shipKills = 0

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

    def canDock(self):
        # a ship that is under attack cannot dock until it's dock timer runs out,
        # see DistributedPlayerPirate.startTimer (SHIP_DOCK_TIMER)...
        if not self.lastAttacked:
            return True

        elapsed = globalClock.getFrameTime() - self.lastAttacked
        return elapsed >= self.DockTimerDuration - self.DockTimerTolerance

    def setDeploy(self, deployState, timestamp=0):
        DistributedShipAI.setDeploy(self, deployState, timestamp)
        if deployState:
            # a new voyage begins each time the ship is deployed:
            self.missionStartTime = globalClock.getRealTime()
            self.shipKills = 0

    def addShipKill(self):
        self.shipKills += 1

    @staticmethod
    def unpackCargo(cargo):
        # each cargo container holds one of the trade goods of it's type, the rarer
        # goods are found less often (see EconomyGlobals.__cargoList)...
        unpackedCargo = []
        for containerType in cargo:
            itemIds = EconomyGlobals.getAllCargoType(containerType)
            if not itemIds:
                continue

            weights = [EconomyGlobals.getCargoRarity(itemId) for itemId in itemIds]
            unpackedCargo.append(random.choices(itemIds, weights=weights)[0])

        return unpackedCargo

    def getMissionData(self, cargo, gold=0):
        # see the client's MissionData struct and HighSeasScoreboard.getMissionResults...
        missionTime = 0
        if self.missionStartTime:
            missionTime = int(globalClock.getRealTime() - self.missionStartTime)

        shipDamage = 0
        if self.maxHp:
            shipDamage = int(100 * (self.maxHp - self.hp) / float(self.maxHp))

        return [max(0, missionTime), max(0, min(shipDamage, 255)), 0, 0, 0, 0, 0, 0,
            min(self.shipKills, 65535), 0, 0, min(gold, 65535), list(cargo), min(len(self.crew), 255)]

    def getPlunderShare(self, avatar, cargo):
        # each pirate's share of the plunder, the owner receives a captain's bonus
        # when sailing with a crew (see HighSeasScoreboard.getCargoResults)...
        gold = EconomyGlobals.getCargoTotalValue(cargo)
        if avatar.doId == self.ownerId and len(self.crew) > 1:
            gold += int(gold * EconomyGlobals.CAPTAIN_LOOT_MULTIPLIER)

        return gold

    def handleDockedAtPort(self, island):
        # the cargo crates plundered at sea are opened and sold once the ship
        # makes it back into port, the goods are divided up amongst the crew...
        if self.getSiegeTeam():
            return

        crew = [self.air.doId2do.get(avatarId) for avatarId in self.crew]
        crew = [avatar for avatar in crew if avatar is not None]
        if not crew:
            return

        # the captain is dealt their share first:
        crew.sort(key=lambda avatar: avatar.doId != self.ownerId)

        unpackedCargo = self.unpackCargo(self.cargo)
        shares = dict((avatar.doId, []) for avatar in crew)
        for index, itemId in enumerate(unpackedCargo):
            shares[crew[index % len(crew)].doId].append(itemId)

        missionData = self.getMissionData(unpackedCargo)
        for avatar in crew:
            share = shares[avatar.doId]
            gold = self.getPlunderShare(avatar, share)
            inventory = avatar.getInventory() if hasattr(avatar, 'getInventory') else None
            if gold and inventory:
                inventory.addGoldInPocket(gold)

            self.d_endMissionPanel(avatar.doId, missionData, self.getMissionData(share))

        if self.cargo:
            self.air.writeServerEvent('ship-cargo-sold', shipId=self.doId, cargo=list(self.cargo),
                goods=unpackedCargo)

            self.b_setCargo([])

        self.missionStartTime = globalClock.getRealTime()
        self.shipKills = 0

    def d_endMissionPanel(self, avatarId, missionData, playerData):
        avatar = self.air.doId2do.get(avatarId)
        if avatar is not None:
            avatar.sendUpdateToAvatarId(avatarId, 'endMissionPanel', [missionData, playerData])

    def setGameState(self, stateName, avId, timeStamp=0):
        DistributedShipAI.setGameState(self, stateName, avId, timeStamp)

        # a ship that is no longer at sea should not be listed as deployed:
        if stateName in ('Sunk', 'PutAway'):
            self.air.shipManager.removePlayerShip(self)

    def handleShipSinking(self):
        DistributedShipAI.handleShipSinking(self)

        # if a ship sinks at sea, all of it's cargo is lost (see PLocalizer.ShipTip20):
        if self.cargo:
            self.b_setCargo([])

    def handleShipSunk(self):
        # player ships are never deleted when they sink, the ship stays in the avatar's
        # inventory with zero hp until it has been repaired by a shipwright...
        self.b_setGameState('Sunk', 0)
        self.sendCrewToReturnLocation()

    def sendCrewToReturnLocation(self, excludeIds=()):
        parentObj = self.getParentObj()
        world = parentObj.getParentObj() if parentObj is not None else None
        for avatarId in list(self.crew):
            avatar = self.air.doId2do.get(avatarId)
            if not avatar or avatarId in excludeIds:
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
        # the ship is removed from the world when it's owner logs out, the rest
        # of the crew would be left stranded at sea so send them home...
        if self.crew and self.getCurrentGameState() not in ('Sunk', 'PutAway'):
            owner = self.air.doId2do.get(self.ownerId)
            self.sendCrewToReturnLocation(excludeIds=(self.ownerId,))
            for avatarId in list(self.crew):
                avatar = self.air.doId2do.get(avatarId)
                if avatar is None or avatar is owner:
                    continue

                if avatar.getCrewShipId() == self.doId:
                    avatar.b_setShipId(0)
                    avatar.b_setActiveShipId(0)
                    avatar.b_setCrewShipId(0)

        self.ignoreAll()
        self.deleteRepairSpots()
        self.air.shipManager.removePlayerShip(self)
        DistributedShipAI.delete(self)
