from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.distributed import DistributedObjectOV
from pirates.economy.EconomyGlobals import *
from pirates.ship import ShipGlobals

class PlayerShipOV(DistributedObjectOV.DistributedObjectOV):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipOV')
    
    def __init__(self, cr):
        DistributedObjectOV.DistributedObjectOV.__init__(self, cr)
        self.shipClass = 0
        self.modelClass = 0
        self.baseTeam = 0
        self.maxHp = 0
        self.Hp = 0
        self.maxSp = 0
        self.Sp = 0
        self.cargo = []
        self.maxCargo = 0
        self.crew = []
        self.name = ''
        self.crewCount = 0
        self.state = None
        self.timerTime = 0
        self.timerTimestamp = 0
    
    def announceGenerate(self):
        DistributedObjectOV.DistributedObjectOV.announceGenerate(self)
        messenger.send('DistributedShipOV-announceGenerate', sentArgs = [self.doId])
        if self.state not in ('Off', 'Sunk'):
            localAvatar.b_setActiveShipId(self.doId)
    
    def delete(self):
        DistributedObjectOV.DistributedObjectOV.delete(self)
        messenger.send('DistributedShipOV-delete', sentArgs = [self.doId])
    
    def loadStats(self):
        self.stats = ShipGlobals.getHullStats(self.shipClass)
        self.maxCrew = self.stats['maxCrew']
        self.acceleration = self.stats['acceleration']
        self.maxSpeed = self.stats['maxSpeed']
        self.reverseAcceleration = self.stats['reverseAcceleration']
        self.maxReverseSpeed = self.stats['maxReverseSpeed']
        self.turnRate = self.stats['turn']
        self.maxTurn = self.stats['maxTurn']
        self.mass = self.stats['mass']
        self.waterIntakeDrag = self.stats['waterIntakeDrag']
        self.sphereRadius = self.stats['sphereRadius']
    
    def setInventoryId(self, inventoryId):
        self.inventoryId = inventoryId

    def setName(self, name):
        self.name = name
        messenger.send('setName-%s' % self.getDoId(), [
            self.name,
            self.baseTeam])

    def setWishName(self, name):
        self.wishName = name
        messenger.send('setWishName-%s' % self.getDoId(), [
            self.wishName])

    def setWishNameState(self, state):
        self.wishNameState = state
        messenger.send('setWishNameState-%s' % self.getDoId(), [
            self.wishNameState])

    def setNPCship(self, val):
        self.npcShip = val

    def setCharterTimestamp(self, timestamp):
        self.charterTimestamp = timestamp
        messenger.send('setCharterTimestamp-%s' % self.getDoId(), [
            self.charterTimestamp])

    def setBaseTeam(self, teamId):
        self.baseTeam = teamId
        messenger.send('setName-%s' % self.getDoId(), [
            self.name,
            self.baseTeam])
    
    def setMaxHp(self, val):
        self.maxHp = val
        messenger.send('setShipHp-%s' % self.getDoId(), [
            self.Hp,
            self.maxHp])

    def setHp(self, Hp):
        self.deltaHp = Hp - self.Hp
        self.Hp = Hp
        messenger.send('setShipHp-%s' % self.getDoId(), [
            self.Hp,
            self.maxHp])

    def setMaxSp(self, val):
        self.maxSp = val
        messenger.send('setShipSp-%s' % self.getDoId(), [
            self.Sp,
            self.maxSp])
    
    def setSp(self, Sp):
        self.deltaSp = Sp - self.Sp
        self.Sp = Sp
        messenger.send('setShipSp-%s' % self.getDoId(), [
            self.Sp,
            self.maxSp])
    
    def setShipClass(self, shipClass):
        self.shipClass = shipClass
        messenger.send('setShipClass-%s' % self.getDoId(), [
            self.shipClass])
        self.loadStats()
        self.modelClass = ShipGlobals.getModelClass(shipClass)

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId
    
    def setCrew(self, crewArray):
        if self.crew != crewArray:
            messenger.send('setShipCrew-%s' % self.getDoId(), [
                crewArray,
                self.maxCrew])
        
        self.crew = crewArray
        self.crewCount = len(self.crew)
    
    def setMaxCargo(self, maxCargo):
        if self.maxCargo != maxCargo:
            self.maxCargo = maxCargo
            messenger.send('setShipCargo-%s' % self.getDoId(), [
                self.cargo,
                self.maxCargo])

    def setCargo(self, cargo):
        self.cargo = cargo
        messenger.send('setShipCargo-%s' % self.getDoId(), [
            self.cargo,
            self.maxCargo])

    def setCrewId(self, crewId):
        self.crewId = crewId
        messenger.send('setCrewId-%s' % self.getDoId(), [
            self.crewId])

    def setHullCondition(self, condition):
        overhaulBit = 1 << 7
        self.isInOverhaul = bool(condition & overhaulBit)
        self.hullCondition = condition & ~overhaulBit
        messenger.send('setShipHullCondition-%s' % self.getDoId(), [
            self.hullCondition])
        messenger.send('setShipIsInOverhaul-%s' % self.getDoId(), [
            self.isInOverhaul])

    def setGameState(self, stateName, avId, timeStamp):
        self.state = stateName
        messenger.send('setState-%s' % self.getDoId(), [
            self.state])
        if self.state in ('Off',) and self.getDoId() == localAvatar.getActiveShipId():
            localAvatar.b_setActiveShipId(0)

    def getShipInfoId(self):
        return self.shipInfoId

    def setShipInfoId(self, shipInfoId):
        self.shipInfoId = shipInfoId

    def getCargoCrate(self):
        return self.cargo.count(ItemId.CARGO_CRATE)

    def getCargoChest(self):
        return self.cargo.count(ItemId.CARGO_CHEST)

    def getCargoSkeletonChest(self):
        return self.cargo.count(ItemId.CARGO_SKCHEST)

    def setTimer(self, time, timestamp):
        elapsedTime = globalClockDelta.localElapsedTime(timestamp)
        localTime = globalClock.getFrameTime()
        self.timerTimestamp = localTime - elapsedTime
        self.timerTime = time
        messenger.send('setShipTimer-%s' % self.getDoId(), [
            self.getTimeLeft()])

    def getTimeLeft(self):
        timePassed = globalClock.getFrameTime() - self.timerTimestamp
        return max(0, self.timerTime - timePassed)
    
    def sendTeleportInfo(self, shardId, instanceDoId):
        self.cr.teleportMgr.requestTeleportToShip(shardId, instanceDoId, self.doId)


