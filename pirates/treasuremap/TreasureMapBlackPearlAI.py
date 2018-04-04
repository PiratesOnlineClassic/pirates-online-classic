
from pirates.treasuremap.DistributedTreasureMapInstanceAI import DistributedTreasureMapInstanceAI
from direct.directnotify import DirectNotifyGlobal

class TreasureMapBlackPearlAI(DistributedTreasureMapInstanceAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TreasureMapBlackPearlAI')

    def __init__(self, air):
        DistributedTreasureMapInstanceAI.__init__(self, air)


    # requestShipCapture() airecv clsend

    def requestShipCapture(self, requestShipCapture):
        pass

    # requestShipAmbush() airecv clsend

    def requestShipAmbush(self, requestShipAmbush):
        pass

    # requestEndCutscene() airecv clsend

    def requestEndCutscene(self, requestEndCutscene):
        pass

    # endCutscene() broadcast

    def endCutscene(self, endCutscene):
        self.sendUpdate('endCutscene', [endCutscene])

    # displayCutsceneMessage(uint32, uint8) broadcast

    def displayCutsceneMessage(self, displayCutsceneMessage, todo_uint8_1):
        self.sendUpdate('displayCutsceneMessage', [displayCutsceneMessage, todo_uint8_1])

    # setBlackPearlId(uint32) broadcast ram

    def setBlackPearlId(self, blackPearlId):
        self.sendUpdate('setBlackPearlId', [blackPearlId])

    # setGoliathId(uint32) broadcast ram

    def setGoliathId(self, goliathId):
        self.sendUpdate('setGoliathId', [goliathId])

    # setAllPlayersReady(uint8) broadcast ram

    def setAllPlayersReady(self, allPlayersReady):
        self.sendUpdate('setAllPlayersReady', [allPlayersReady])

    # setAttackShipIds(uint32 []) broadcast ram

    def setAttackShipIds(self, attackShipIds):
        self.sendUpdate('setAttackShipIds', [attackShipIds])

    # fireShipCannonsAtTarget(uint32, uint32) broadcast

    def fireShipCannonsAtTarget(self, fireShipCannonsAtTarget, todo_uint32_1):
        self.sendUpdate('fireShipCannonsAtTarget', [fireShipCannonsAtTarget, todo_uint32_1])

    # destroyBarricade(uint8) broadcast

    def destroyBarricade(self, destroyBarricade):
        self.sendUpdate('destroyBarricade', [destroyBarricade])

    # barricadeWarning(uint8) broadcast

    def barricadeWarning(self, barricadeWarning):
        self.sendUpdate('barricadeWarning', [barricadeWarning])

    # disableBarricadeCollisions(uint8) broadcast

    def disableBarricadeCollisions(self, disableBarricadeCollisions):
        self.sendUpdate('disableBarricadeCollisions', [disableBarricadeCollisions])

    # enableBarricadeCollisions(uint8) broadcast

    def enableBarricadeCollisions(self, enableBarricadeCollisions):
        self.sendUpdate('enableBarricadeCollisions', [enableBarricadeCollisions])

    # startStageFourCutscene() broadcast

    def startStageFourCutscene(self, startStageFourCutscene):
        self.sendUpdate('startStageFourCutscene', [startStageFourCutscene])

    # stopStageFourCutscene() broadcast

    def stopStageFourCutscene(self, stopStageFourCutscene):
        self.sendUpdate('stopStageFourCutscene', [stopStageFourCutscene])

    # handleAttackShipSunk() broadcast

    def handleAttackShipSunk(self, handleAttackShipSunk):
        self.sendUpdate('handleAttackShipSunk', [handleAttackShipSunk])

    # handleNPCsKilled() broadcast

    def handleNPCsKilled(self, handleNPCsKilled):
        self.sendUpdate('handleNPCsKilled', [handleNPCsKilled])


