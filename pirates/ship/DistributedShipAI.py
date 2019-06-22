from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *

from pirates.battle.Teamable import Teamable
from pirates.ship import ShipGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.movement.DistributedMovingObjectAI import DistributedMovingObjectAI
from pirates.distributed.DistributedCharterableObjectAI import DistributedCharterableObjectAI
from pirates.shipparts.DistributedShippartAI import DistributedShippartAI
from pirates.shipparts.DistributedSteeringWheelAI import DistributedSteeringWheelAI
from pirates.shipparts.DistributedBowSpritAI import DistributedBowSpritAI
from pirates.shipparts.DistributedSailAI import DistributedSailAI


class DistributedShipAI(DistributedMovingObjectAI, DistributedCharterableObjectAI, Teamable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipAI')

    def __init__(self, air):
        DistributedMovingObjectAI.__init__(self, air)
        DistributedCharterableObjectAI.__init__(self, air)
        Teamable.__init__(self)

        self.uniqueId = ''
        self.baseTeam = 0
        self.shipClass = 0
        self.name = ''
        self.inventoryId = 0
        self.npcShip = 0
        self.isBoardable = 0
        self.isExitable = 0
        self.shipInfoId = 0
        self.isFlagship = 0
        self.maxHp = 0
        self.hp = 0
        self.maxSp = 0
        self.sp = 0
        self.hullCondition = 0
        self.maxCargo = 0
        self.cargo = []
        self.maxCrew = 0
        self.crew = []
        self.gameState = ['Off', 0, 0]
        self.badge = [0, 0]
        self.isInBoardingPosition = 0
        self.landedGrapples = []
        self.wishName = ''
        self.wishNameState = ''
        self.clientControllerDoId = 0

    def sendCurrentPosition(self):
        x, y, z = self.getPos()
        h, p, r = self.getHpr()
        print (x, y, z, h, p, r)
        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        self.sendUpdate('setSmPosHpr', [x, y, z, h, p, r, timestamp])

    def startPosHprBroadcast(self):

        def _broadcast(task):
            try:
                self.sendCurrentPosition()
            except:
                pass

            return task.again

        taskMgr.doMethodLater(0.2, _broadcast, self.uniqueName('broadcast-pos'))

    def announceGenerate(self):
        DistributedMovingObjectAI.announceGenerate(self)
        DistributedCharterableObjectAI.announceGenerate(self)

        self.steeringWheel = DistributedSteeringWheelAI(self.air)
        self.steeringWheel.setShipId(self.doId)
        self.generateChildWithRequired(self.steeringWheel, PiratesGlobals.ShipZoneOnDeck)

        #self.bowSprit = DistributedBowSpritAI(self.air)
        #self.bowSprit.setShipId(self.doId)
        #
        #prowConfig = ShipGlobals.getProwConfig(self.shipClass)
        #for key, value in prowConfig.items():
        #    if not hasattr(self.bowSprit, key):
        #        continue
        #
        #    if isinstance(value, list):
        #        value = value[0]
        #
        #    getattr(self.bowSprit, key)(value)
        #
        #self.generateChildWithRequired(self.bowSprit, PiratesGlobals.ShipZoneOnDeck)

        mastInfo = ShipGlobals.getMastInfo(self.shipClass)
        for mastType, x, sailTypes in mastInfo:
            sailIndex = 0
            for sailType in sailTypes:
                sailConfig = ShipGlobals.getSailConfig(self.shipClass, x, sailIndex)
                sail = DistributedSailAI(self.air)
                sail.setShipId(self.doId)
                sail.setAnimState('TiedUp')

                for key, value in sailConfig.items():
                    if not hasattr(sail, key):
                        continue

                    if isinstance(value, list):
                        value = value[0]

                    getattr(sail, key)(value)

                self.generateChildWithRequired(sail, PiratesGlobals.ShipZoneOnDeck)
                sailIndex += 1

    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def d_setUniqueId(self, uniqueId):
        self.sendUpdate('setUniqueId', [uniqueId])

    def b_setUniqueId(self, uniqueId):
        self.setUniqueId(uniqueId)
        self.d_setUniqueId(uniqueId)

    def getUniqueId(self):
        return self.uniqueId

    def setLevel(self, level):
        self.level = level

    def d_setLevel(self, level):
        self.sendUpdate('setLevel', [level])

    def b_setLevel(self, level):
        self.setLevel(level)
        self.d_setLevel(level)

    def getLevel(self):
        return self.level

    def setShipClass(self, shipClass):
        self.shipClass = shipClass

    def d_setShipClass(self, shipClass):
        self.sendUpdate('setShipClass', [shipClass])

    def b_setShipClass(self, shipClass):
        self.setShipClass(shipClass)
        self.d_setShipClass(shipClass)

    def getShipClass(self):
        return self.shipClass

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def getInventory(self):
        return self.air.inventoryManager.getInventory(self.inventoryId)

    def setInventoryId(self, inventoryId):
        self.inventoryId = inventoryId

    def d_setInventoryId(self, inventoryId):
        self.sendUpdate('setInventoryId', [inventoryId])

    def b_setInventoryId(self, inventoryId):
        self.setInventoryId(inventoryId)
        self.d_setInventoryId(inventoryId)

    def getInventoryId(self):
        return self.inventoryId

    def setNPCship(self, npcShip):
        self.npcShip = npcShip

    def d_setNPCship(self, npcShip):
        self.sendUpdate('setNPCship', [npcShip])

    def b_setNPCship(self, npcShip):
        self.setNPCship(npcShip)
        self.d_setNPCship(npcShip)

    def getNPCship(self):
        return self.npcShip

    def setIsBoardable(self, isBoardable):
        self.isBoardable = isBoardable

    def d_setIsBoardable(self, isBoardable):
        self.sendUpdate('setIsBoardable', [isBoardable])

    def b_setIsBoardable(self, isBoardable):
        self.setIsBoardable(isBoardable)
        self.d_setIsBoardable(isBoardable)

    def getIsBoardable(self):
        return self.isBoardable

    def setIsExitable(self, isExitable):
        self.isExitable = isExitable

    def d_setIsExitable(self, isExitable):
        self.sendUpdate('setIsExitable', [isExitable])

    def b_setIsExitable(self, isExitable):
        self.setIsExitable(isExitable)
        self.d_setIsExitable(isExitable)

    def getIsExitable(self):
        return self.isExitable

    def setShipInfoId(self, shipInfoId):
        self.shipInfoId = shipInfoId

    def d_setShipInfoId(self, shipInfoId):
        self.sendUpdate('setShipInfoId', [shipInfoId])

    def b_setShipInfoId(self, shipInfoId):
        self.setShipInfoId(shipInfoId)
        self.d_setShipInfoId(shipInfoId)

    def getShipInfoId(self):
        return self.shipInfoId

    def setIsFlagship(self, isFlagship):
        self.isFlagship = isFlagship

    def d_setIsFlagship(self, isFlagship):
        self.sendUpdate('setIsFlagship', [isFlagship])

    def b_setIsFlagship(self, isFlagship):
        self.setIsFlagship(isFlagship)
        self.d_setIsFlagship(isFlagship)

    def getIsFlagship(self):
        return self.isFlagship

    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def d_setMaxHp(self, maxHp):
        self.sendUpdate('setMaxHp', [maxHp])

    def b_setMaxHp(self, maxHp):
        self.setMaxHp(maxHp)
        self.d_setMaxHp(maxHp)

    def getMaxHp(self):
        return self.maxHp

    def setHp(self, hp):
        self.hp = hp

    def d_setHp(self, hp):
        self.sendUpdate('setHp', [hp])

    def b_setHp(self, hp):
        self.setHp(hp)
        self.d_setHp(hp)

    def getHp(self):
        return self.hp

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

    def setHullCondition(self, hullCondition):
        self.hullCondition = hullCondition

    def d_setHullCondition(self, hullCondition):
        self.sendUpdate('setHullCondition', [hullCondition])

    def b_setHullCondition(self, hullCondition):
        self.setHullCondition(hullCondition)
        self.d_setHullCondition(hullCondition)

    def getHullCondition(self):
        return self.hullCondition

    def setMaxCargo(self, maxCargo):
        self.maxCargo = maxCargo

    def d_setMaxCargo(self, maxCargo):
        self.sendUpdate('setMaxCargo', [maxCargo])

    def b_setMaxCargo(self, maxCargo):
        self.setMaxCargo(maxCargo)
        self.d_setMaxCargo(maxCargo)

    def getMaxCargo(self):
        return self.maxCargo

    def setCargo(self, cargo):
        self.cargo = cargo

    def d_setCargo(self, cargo):
        self.sendUpdate('setCargo', [cargo])

    def b_setCargo(self, cargo):
        self.setCargo(cargo)
        self.d_setCargo(cargo)

    def getCargo(self):
        return self.cargo

    def setMaxCrew(self, maxCrew):
        self.maxCrew = maxCrew

    def d_setMaxCrew(self, maxCrew):
        self.sendUpdate('setMaxCrew', [maxCrew])

    def b_setMaxCrew(self, maxCrew):
        self.setMaxCrew(maxCrew)
        self.d_setMaxCrew(maxCrew)

    def getMaxCrew(self):
        return self.maxCrew

    def setCrew(self, crew):
        self.crew = crew

    def d_setCrew(self, crew):
        self.sendUpdate('setCrew', [crew])

    def b_setCrew(self, crew):
        self.setCrew(crew)
        self.d_setCrew(crew)

    def getCrew(self):
        return self.crew

    def setGameState(self, stateName, avId, timeStamp=0):
        self.gameState = [stateName, avId, timeStamp]

    def d_setGameState(self, stateName, avId, timeStamp=0):
        self.sendUpdate('setGameState', [stateName, avId, timeStamp])

    def b_setGameState(self, stateName, avId, timeStamp=0):
        if not timeStamp:
            timeStamp = globalClockDelta.getRealNetworkTime(bits=16)

        self.setGameState(stateName, avId, timeStamp)
        self.d_setGameState(stateName, avId, timeStamp)

    def getGameState(self):
        return self.gameState

    def setClientController(self, clientControllerDoId):
        self.clientControllerDoId = clientControllerDoId

    def d_setClientController(self, clientControllerDoId):
        self.sendUpdate('setClientController', [clientControllerDoId])

    def b_setClientController(self, clientControllerDoId):
        self.setClientController(clientControllerDoId)
        self.d_setClientController(clientControllerDoId)

    def getClientController(self):
        return self.clientControllerDoId

    def setBadge(self, titleId, rank):
        self.badge = [titleId, rank]

    def d_setBadge(self, titleId, rank):
        self.sendUpdate('setBadge', [titleId, rank])

    def b_setBadge(self, titleId, rank):
        self.setBadge(titleId, rank)
        self.d_setBadge(titleId, rank)

    def getBadge(self):
        return self.badge

    def setIsInBoardingPosition(self, isInBoardingPosition):
        self.isInBoardingPosition = isInBoardingPosition

    def d_setIsInBoardingPosition(self, isInBoardingPosition):
        self.sendUpdate('setIsInBoardingPosition', [isInBoardingPosition])

    def b_setIsInBoardingPosition(self, isInBoardingPosition):
        self.setIsInBoardingPosition(isInBoardingPosition)
        self.d_setIsInBoardingPosition(isInBoardingPosition)

    def getIsInBoardingPosition(self):
        return self.isInBoardingPosition

    def setLandedGrapples(self, landedGrapples):
        self.landedGrapples = landedGrapples

    def d_setLandedGrapples(self, landedGrapples):
        self.sendUpdate('setLandedGrapples', [landedGrapples])

    def b_setLandedGrapples(self, landedGrapples):
        self.setLandedGrapples(landedGrapples)
        self.d_setLandedGrapples(landedGrapples)

    def getLandedGrapples(self):
        return self.landedGrapples

    def setWishName(self, wishName):
        self.wishName = wishName

    def d_setWishName(self, wishName):
        self.sendUpdate('setWishName', [wishName])

    def b_setWishName(self, wishName):
        self.setWishName(wishName)
        self.d_setWishName(wishName)

    def getWishName(slef):
        return self.wishName

    def setWishNameState(self, wishNameState):
        self.wishNameState = wishNameState

    def d_setWishNameState(self, wishNameState):
        self.sendUpdate('setWishNameState', [wishNameState])

    def b_setWishNameState(self, wishNameState):
        self.setWishNameState(wishNameState)
        self.d_setWishNameState(wishNameState)

    def getWishNameState(self):
        return self.wishNameState

    def shipBoarded(self):
        pass

    def generateChildWithRequired(self, do, zoneId, optionalFields=[]):
        self.generateChildWithRequiredAndId(do, self.air.allocateChannel(), self.doId, zoneId, optionalFields)

    def generateChildWithRequiredAndId(self, do, doId, parentId, zoneId, optionalFields=[]):
        do.generateWithRequiredAndId(doId, parentId, zoneId, optionalFields)
