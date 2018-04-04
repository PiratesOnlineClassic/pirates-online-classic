
from pirates.movement.DistributedMovingObjectAI import DistributedMovingObjectAI
from pirates.distributed.DistributedCharterableObjectAI import DistributedCharterableObjectAI
from pirates.battle.Teamable import Teamable
from direct.directnotify import DirectNotifyGlobal

class DistributedShipAI(DistributedMovingObjectAI, DistributedCharterableObjectAI, Teamable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipAI')

    def __init__(self, air):
        DistributedMovingObjectAI.__init__(self, air)
        DistributedCharterableObjectAI.__init__(self, air)
        Teamable.__init__(self, air)
        self.uniqueId = ''
        self.baseTeam = 0
        self.level = 0
        self.shipClass = 0
        self.name = ''
        self.inventoryId = 0
        self.nPCship = 0
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
        self.cargo = 0
        self.maxCrew = 0
        self.worldKey = 0
        self.crew = 0
        self.gameState = ['', 0, 0]
        self.badge = [0, 0]
        self.isInBoardingPosition = 0
        self.landedGrapples = None
        self.wishName = ''
        self.wishNameState = ''


    # setUniqueId(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def d_setUniqueId(self, uniqueId):
        self.sendUpdate('setUniqueId', [uniqueId])

    def b_setUniqueId(self, uniqueId):
        self.setUniqueId(uniqueId)
        self.d_setUniqueId(uniqueId)

    def getUniqueId(self):
        return self.uniqueId

    # setBaseTeam(int8) required broadcast ram db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setBaseTeam(self, baseTeam):
        self.baseTeam = baseTeam

    def d_setBaseTeam(self, baseTeam):
        self.sendUpdate('setBaseTeam', [baseTeam])

    def b_setBaseTeam(self, baseTeam):
        self.setBaseTeam(baseTeam)
        self.d_setBaseTeam(baseTeam)

    def getBaseTeam(self):
        return self.baseTeam

    # setLevel(uint16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setLevel(self, level):
        self.level = level

    def d_setLevel(self, level):
        self.sendUpdate('setLevel', [level])

    def b_setLevel(self, level):
        self.setLevel(level)
        self.d_setLevel(level)

    def getLevel(self):
        return self.level

    # setShipClass(uint8) required broadcast ram db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setShipClass(self, shipClass):
        self.shipClass = shipClass

    def d_setShipClass(self, shipClass):
        self.sendUpdate('setShipClass', [shipClass])

    def b_setShipClass(self, shipClass):
        self.setShipClass(shipClass)
        self.d_setShipClass(shipClass)

    def getShipClass(self):
        return self.shipClass

    # setName(string) required broadcast ram db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    # setInventoryId(uint32) required broadcast db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setInventoryId(self, inventoryId):
        self.inventoryId = inventoryId

    def d_setInventoryId(self, inventoryId):
        self.sendUpdate('setInventoryId', [inventoryId])

    def b_setInventoryId(self, inventoryId):
        self.setInventoryId(inventoryId)
        self.d_setInventoryId(inventoryId)

    def getInventoryId(self):
        return self.inventoryId

    # setNPCship(uint8) required broadcast ram ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setNPCship(self, nPCship):
        self.nPCship = nPCship

    def d_setNPCship(self, nPCship):
        self.sendUpdate('setNPCship', [nPCship])

    def b_setNPCship(self, nPCship):
        self.setNPCship(nPCship)
        self.d_setNPCship(nPCship)

    def getNPCship(self):
        return self.nPCship

    # setIsBoardable(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setIsBoardable(self, isBoardable):
        self.isBoardable = isBoardable

    def d_setIsBoardable(self, isBoardable):
        self.sendUpdate('setIsBoardable', [isBoardable])

    def b_setIsBoardable(self, isBoardable):
        self.setIsBoardable(isBoardable)
        self.d_setIsBoardable(isBoardable)

    def getIsBoardable(self):
        return self.isBoardable

    # setIsExitable(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setIsExitable(self, isExitable):
        self.isExitable = isExitable

    def d_setIsExitable(self, isExitable):
        self.sendUpdate('setIsExitable', [isExitable])

    def b_setIsExitable(self, isExitable):
        self.setIsExitable(isExitable)
        self.d_setIsExitable(isExitable)

    def getIsExitable(self):
        return self.isExitable

    # setShipInfoId(uint32) required ram airecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setShipInfoId(self, shipInfoId):
        self.shipInfoId = shipInfoId

    def d_setShipInfoId(self, shipInfoId):
        self.sendUpdate('setShipInfoId', [shipInfoId])

    def b_setShipInfoId(self, shipInfoId):
        self.setShipInfoId(shipInfoId)
        self.d_setShipInfoId(shipInfoId)

    def getShipInfoId(self):
        return self.shipInfoId

    # setIsFlagship(int8) required broadcast ram db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setIsFlagship(self, isFlagship):
        self.isFlagship = isFlagship

    def d_setIsFlagship(self, isFlagship):
        self.sendUpdate('setIsFlagship', [isFlagship])

    def b_setIsFlagship(self, isFlagship):
        self.setIsFlagship(isFlagship)
        self.d_setIsFlagship(isFlagship)

    def getIsFlagship(self):
        return self.isFlagship

    # setMaxHp(int16) required broadcast ram db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def d_setMaxHp(self, maxHp):
        self.sendUpdate('setMaxHp', [maxHp])

    def b_setMaxHp(self, maxHp):
        self.setMaxHp(maxHp)
        self.d_setMaxHp(maxHp)

    def getMaxHp(self):
        return self.maxHp

    # setHp(int16) required broadcast ram db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setHp(self, hp):
        self.hp = hp

    def d_setHp(self, hp):
        self.sendUpdate('setHp', [hp])

    def b_setHp(self, hp):
        self.setHp(hp)
        self.d_setHp(hp)

    def getHp(self):
        return self.hp

    # setMaxSp(int16) required broadcast ram db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setMaxSp(self, maxSp):
        self.maxSp = maxSp

    def d_setMaxSp(self, maxSp):
        self.sendUpdate('setMaxSp', [maxSp])

    def b_setMaxSp(self, maxSp):
        self.setMaxSp(maxSp)
        self.d_setMaxSp(maxSp)

    def getMaxSp(self):
        return self.maxSp

    # setSp(int16) required broadcast ram db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setSp(self, sp):
        self.sp = sp

    def d_setSp(self, sp):
        self.sendUpdate('setSp', [sp])

    def b_setSp(self, sp):
        self.setSp(sp)
        self.d_setSp(sp)

    def getSp(self):
        return self.sp

    # setHullCondition(uint8) required broadcast ram db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setHullCondition(self, hullCondition):
        self.hullCondition = hullCondition

    def d_setHullCondition(self, hullCondition):
        self.sendUpdate('setHullCondition', [hullCondition])

    def b_setHullCondition(self, hullCondition):
        self.setHullCondition(hullCondition)
        self.d_setHullCondition(hullCondition)

    def getHullCondition(self):
        return self.hullCondition

    # setMaxCargo(uint8) required broadcast ram db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setMaxCargo(self, maxCargo):
        self.maxCargo = maxCargo

    def d_setMaxCargo(self, maxCargo):
        self.sendUpdate('setMaxCargo', [maxCargo])

    def b_setMaxCargo(self, maxCargo):
        self.setMaxCargo(maxCargo)
        self.d_setMaxCargo(maxCargo)

    def getMaxCargo(self):
        return self.maxCargo

    # setCargo(uint8array) required broadcast ram db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setCargo(self, cargo):
        self.cargo = cargo

    def d_setCargo(self, cargo):
        self.sendUpdate('setCargo', [cargo])

    def b_setCargo(self, cargo):
        self.setCargo(cargo)
        self.d_setCargo(cargo)

    def getCargo(self):
        return self.cargo

    # setMaxCrew(uint8) required broadcast ram db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setMaxCrew(self, maxCrew):
        self.maxCrew = maxCrew

    def d_setMaxCrew(self, maxCrew):
        self.sendUpdate('setMaxCrew', [maxCrew])

    def b_setMaxCrew(self, maxCrew):
        self.setMaxCrew(maxCrew)
        self.d_setMaxCrew(maxCrew)

    def getMaxCrew(self):
        return self.maxCrew

    # setWorldKey(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setWorldKey(self, worldKey):
        self.worldKey = worldKey

    def d_setWorldKey(self, worldKey):
        self.sendUpdate('setWorldKey', [worldKey])

    def b_setWorldKey(self, worldKey):
        self.setWorldKey(worldKey)
        self.d_setWorldKey(worldKey)

    def getWorldKey(self):
        return self.worldKey

    # setCrew(uint32array) required broadcast ram ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setCrew(self, crew):
        self.crew = crew

    def d_setCrew(self, crew):
        self.sendUpdate('setCrew', [crew])

    def b_setCrew(self, crew):
        self.setCrew(crew)
        self.d_setCrew(crew)

    def getCrew(self):
        return self.crew

    # setBandId(uint32, uint32) broadcast ram

    def setBandId(self, bandId, todo_uint32_1):
        self.sendUpdate('setBandId', [bandId, todo_uint32_1])

    # setGuildId(uint32) broadcast ram

    def setGuildId(self, guildId):
        self.sendUpdate('setGuildId', [guildId])

    # setGameState(string, uint32, int16) required broadcast ram ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setGameState(self, gameState, todo_uint32_1, todo_int16_2):
        self.gameState = gameState

    def d_setGameState(self, gameState, todo_uint32_1, todo_int16_2):
        self.sendUpdate('setGameState', [gameState, todo_uint32_1, todo_int16_2])

    def b_setGameState(self, gameState, todo_uint32_1, todo_int16_2):
        self.setGameState(gameState, todo_uint32_1, todo_int16_2)
        self.d_setGameState(gameState, todo_uint32_1, todo_int16_2)

    def getGameState(self):
        return self.gameState

    # fixSail() airecv clsend

    def fixSail(self, fixSail):
        pass

    # dropAnchor(uint32) airecv clsend

    def dropAnchor(self, dropAnchor):
        pass

    # purchaseRepairAll() airecv clsend

    def purchaseRepairAll(self, purchaseRepairAll):
        pass

    # clearDockTimer() airecv clsend

    def clearDockTimer(self, clearDockTimer):
        pass

    # leave(uint32) airecv clsend

    def leave(self, leave):
        pass

    # requestBoard(uint32) airecv clsend

    def requestBoard(self, requestBoard):
        pass

    # requestSkillEvent(uint32, uint32) airecv clsend

    def requestSkillEvent(self, requestSkillEvent, todo_uint32_1):
        pass

    # recordSkillEvent(uint32, uint32) broadcast

    def recordSkillEvent(self, recordSkillEvent, todo_uint32_1):
        self.sendUpdate('recordSkillEvent', [recordSkillEvent, todo_uint32_1])

    # setClientController(uint32) broadcast ram

    def setClientController(self, clientController):
        self.sendUpdate('setClientController', [clientController])

    # forceSteerShip(uint32)

    def forceSteerShip(self, forceSteerShip):
        self.sendUpdate('forceSteerShip', [forceSteerShip])

    # forceBoardShip()

    def forceBoardShip(self, forceBoardShip):
        self.sendUpdate('forceBoardShip', [forceBoardShip])

    # forceExitShip()

    def forceExitShip(self, forceExitShip):
        self.sendUpdate('forceExitShip', [forceExitShip])

    # sendCrewToIsland(uint32, PosH)

    def sendCrewToIsland(self, sendCrewToIsland, todo_PosH_1):
        self.sendUpdate('sendCrewToIsland', [sendCrewToIsland, todo_PosH_1])

    # notifyReceivedLoot(uint8array) broadcast

    def notifyReceivedLoot(self, notifyReceivedLoot):
        self.sendUpdate('notifyReceivedLoot', [notifyReceivedLoot])

    # damage(int16, Pos, DoId) broadcast

    def damage(self, damage, todo_Pos_1, todo_DoId_2):
        self.sendUpdate('damage', [damage, todo_Pos_1, todo_DoId_2])

    # setBadge(int8, int8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setBadge(self, badge, todo_int8_1):
        self.badge = badge

    def d_setBadge(self, badge, todo_int8_1):
        self.sendUpdate('setBadge', [badge, todo_int8_1])

    def b_setBadge(self, badge, todo_int8_1):
        self.setBadge(badge, todo_int8_1)
        self.d_setBadge(badge, todo_int8_1)

    def getBadge(self):
        return self.badge

    # setDeploy(uint8, int16) broadcast ram

    def setDeploy(self, deploy, todo_int16_1):
        self.sendUpdate('setDeploy', [deploy, todo_int16_1])

    # setMovie(uint8, uint32, uint32, bool, int16) broadcast

    def setMovie(self, movie, todo_uint32_1, todo_uint32_2, todo_bool_3, todo_int16_4):
        self.sendUpdate('setMovie', [movie, todo_uint32_1, todo_uint32_2, todo_bool_3, todo_int16_4])

    # setBoardableShipId(uint32) broadcast ram

    def setBoardableShipId(self, boardableShipId):
        self.sendUpdate('setBoardableShipId', [boardableShipId])

    # setIsInBoardingPosition(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setIsInBoardingPosition(self, isInBoardingPosition):
        self.isInBoardingPosition = isInBoardingPosition

    def d_setIsInBoardingPosition(self, isInBoardingPosition):
        self.sendUpdate('setIsInBoardingPosition', [isInBoardingPosition])

    def b_setIsInBoardingPosition(self, isInBoardingPosition):
        self.setIsInBoardingPosition(isInBoardingPosition)
        self.d_setIsInBoardingPosition(isInBoardingPosition)

    def getIsInBoardingPosition(self):
        return self.isInBoardingPosition

    # setLandedGrapples(LandedGrappleList) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setLandedGrapples(self, landedGrapples):
        self.landedGrapples = landedGrapples

    def d_setLandedGrapples(self, landedGrapples):
        self.sendUpdate('setLandedGrapples', [landedGrapples])

    def b_setLandedGrapples(self, landedGrapples):
        self.setLandedGrapples(landedGrapples)
        self.d_setLandedGrapples(landedGrapples)

    def getLandedGrapples(self):
        return self.landedGrapples

    # setBoardingSuccess(uint32, int16) broadcast ram

    def setBoardingSuccess(self, boardingSuccess, todo_int16_1):
        self.sendUpdate('setBoardingSuccess', [boardingSuccess, todo_int16_1])

    # setRespectDeployBarriers(bool, uint32) broadcast ram

    def setRespectDeployBarriers(self, respectDeployBarriers, todo_uint32_1):
        self.sendUpdate('setRespectDeployBarriers', [respectDeployBarriers, todo_uint32_1])

    # swingLocalAvatarToGrappledShip(uint32)

    def swingLocalAvatarToGrappledShip(self, swingLocalAvatarToGrappledShip):
        self.sendUpdate('swingLocalAvatarToGrappledShip', [swingLocalAvatarToGrappledShip])

    # setSinkTimer(int16, int16) broadcast ram

    def setSinkTimer(self, sinkTimer, todo_int16_1):
        self.sendUpdate('setSinkTimer', [sinkTimer, todo_int16_1])

    # requestBoardFlagship(uint32) clsend airecv

    def requestBoardFlagship(self, requestBoardFlagship):
        pass

    # shipBoarded() clsend airecv

    def shipBoarded(self, shipBoarded):
        pass

    # setWishName(string) required db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setWishName(self, wishName):
        self.wishName = wishName

    def d_setWishName(self, wishName):
        self.sendUpdate('setWishName', [wishName])

    def b_setWishName(self, wishName):
        self.setWishName(wishName)
        self.d_setWishName(wishName)

    def getWishName(self):
        return self.wishName

    # setWishNameState(string) required db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setWishNameState(self, wishNameState):
        self.wishNameState = wishNameState

    def d_setWishNameState(self, wishNameState):
        self.sendUpdate('setWishNameState', [wishNameState])

    def b_setWishNameState(self, wishNameState):
        self.setWishNameState(wishNameState)
        self.d_setWishNameState(wishNameState)

    def getWishNameState(self):
        return self.wishNameState

    # setFlagDNAString(string) broadcast ram

    def setFlagDNAString(self, flagDNAString):
        self.sendUpdate('setFlagDNAString', [flagDNAString])

    # requestShipRam(DoId, Pos, uint32) clsend airecv

    def requestShipRam(self, requestShipRam, todo_Pos_1, todo_uint32_2):
        pass

    # useShipRam(Pos) broadcast

    def useShipRam(self, useShipRam):
        self.sendUpdate('useShipRam', [useShipRam])

    # setSkillEffects(BuffList) broadcast ram

    def setSkillEffects(self, skillEffects):
        self.sendUpdate('setSkillEffects', [skillEffects])

    # setRepairCount(uint8) broadcast ram

    def setRepairCount(self, repairCount):
        self.sendUpdate('setRepairCount', [repairCount])

    # setCaptainId(DoId) broadcast ram

    def setCaptainId(self, captainId):
        self.sendUpdate('setCaptainId', [captainId])

    # requestClientAggro() airecv clsend

    def requestClientAggro(self, requestClientAggro):
        pass

    # relayTeleportInfo() airecv

    def relayTeleportInfo(self, relayTeleportInfo):
        pass

    # sendTeleportInfo(uint32, uint32) ownrecv

    # setRespawnLocation(uint32, uint32)

    def setRespawnLocation(self, respawnLocation, todo_uint32_1):
        self.sendUpdate('setRespawnLocation', [respawnLocation, todo_uint32_1])

    # clientReachedRespawnLocation() airecv clsend

    def clientReachedRespawnLocation(self, clientReachedRespawnLocation):
        pass


