from pirates.movement.DistributedMovingObjectAI import DistributedMovingObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.battle.Teamable import Teamable
from pirates.ship import ShipGlobals
from pirates.shipparts.DistributedHullAI import DistributedHullAI
from pirates.shipparts.DistributedMastAI import DistributedMastAI
from pirates.shipparts.DistributedCabinAI import DistributedCabinAI

class DistributedShipAI(DistributedMovingObjectAI, Teamable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipAI')

    def __init__(self, air):
        DistributedMovingObjectAI.__init__(self, air)
        Teamable.__init__(self)

        self.ownerId = 0
        self.shipClass = 0
        self.gameState = ['Off', 0, 0]
        self.maxSp = 0
        self.sp = 0
        self.maxCargo = 0

    def loadParts(self):
        # TODO FIXME: find a cleaner way to get the avatar's
        # connection channel id...
        avatar = self.air.doId2do.get(self.ownerId)
        channel = avatar.getDISLid() << 32 | avatar.doId

        cabinType = ShipGlobals.getCabinType(self.shipClass)

        self.hullId = self.air.allocateChannel()
        self.hull = self.createHull()
        self.hull.generateWithRequiredAndId(self.hullId,
            self.parentId, self.zoneId)

        self.air.setOwner(self.hullId, channel)

        mastInfo = ShipGlobals.getMastInfo(self.shipClass)
        self.masts = {}

        for mastType, mastIndex, sailTypes in mastInfo:
            mastId = self.air.allocateChannel()
            self.masts[mastId] = self.createMast(mastType, mastIndex, sailTypes)
            self.masts[mastId].generateWithRequiredAndId(mastId,
                self.parentId, self.zoneId)

            self.air.setOwner(mastId, channel)

        # some ships do not have a cabin object let's check to see
        # if the ship has a cabin and if so then generate the object...
        if cabinType != -1:
            self.cabinId = self.air.allocateChannel()
            self.cabin = self.createCabin()
            self.cabin.generateWithRequiredAndId(self.cabinId,
                self.parentId, self.zoneId)

    def createHull(self):
        hull = DistributedHullAI(self.air)
        hull.setOwnerId(self.ownerId)
        hull.setShipId(self.doId)
        hull.setGeomParentId(0)
        hull.setShipClass(self.getShipClass())
        hull.setMaxSp(self.getMaxSp())
        hull.setSp(self.getMaxSp())
        hull.setMaxCargo(self.getMaxCargo())

        return hull

    def createMast(self, mastType, posIndex, sailTypes):
        mast = DistributedMastAI(self.air)
        mast.setOwnerId(self.ownerId)
        mast.setShipId(self.doId)
        mast.setGeomParentId(0)
        mast.setShipClass(self.getShipClass())
        mast.setMastType(mastType)
        mast.setPosIndex(posIndex)
        mast.setSailConfig(sailTypes)

        return mast

    def createCabin(self):
        cabinConfig = ShipGlobals.getCabinConfig(self.shipClass)

        cabin = DistributedCabinAI(self.air)
        cabin.setOwnerId(self.ownerId)
        cabin.setShipId(self.doId)
        cabin.setGeomParentId(0)
        cabin.setShipClass(self.getShipClass())
        cabin.setMaxHp(cabinConfig['setMaxHp'][0])
        cabin.setHp(cabinConfig['setHp'][0])
        cabin.setMaxCargo(cabinConfig['setMaxCargo'][0])

        return cabin

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def getOwnerId(self):
        return self.ownerId

    def setShipClass(self, shipClass):
        self.shipClass = shipClass

    def d_setShipClass(self, shipClass):
        self.sendUpdate('setShipClass', [shipClass])

    def b_setShipClass(self, shipClass):
        self.setShipClass(shipClass)
        self.d_setShipClass(shipClass)

    def getShipClass(self):
        return self.shipClass

    def setGameState(self, stateName, avId, timeStamp):
        self.gamestate = [stateName, avId, timeStamp]

    def d_setGameState(self, stateName, avId, timeStamp):
        self.sendUpdate('setGameState', [stateName, avId, timeStamp])

    def b_setGameState(self, stateName, avId, timeStamp):
        self.setGameState(stateName, avId, timeStamp)
        self.d_setGameState(stateName, avId, timeStamp)

    def getGameState(self):
        return self.gameState

    def setMaxSp(self, maxSp):
        self.maxSp = maxSp

    def d_setMaxSp(self, maxSp):
        self.sendUpdate('setMaxSp', [maxSp])

    def b_setMaxSp(self, maxSp):
        self.setMaxSp(maxSp)
        self.d_setMaxSp(maxSp)

    def getMaxSp(self):
        return self.maxSp

    def setSp(self, sp):
        self.sp = sp

    def d_setSp(self, sp):
        self.sendUpdate('setSp', [sp])

    def b_setSp(self, sp):
        self.setSp(sp)
        self.d_setSp(sp)

    def getSp(self):
        return self.sp

    def setMaxCargo(self, maxCargo):
        self.maxCargo = maxCargo

    def d_setMaxCargo(self, maxCargo):
        self.sendUpdate('setMaxCargo', [maxCargo])

    def b_setMaxCargo(self, maxCargo):
        self.setMaxCargo(maxCargo)
        self.d_setMaxCargo(maxCargo)

    def getMaxCargo(self):
        return self.maxCargo
