
from pirates.pvp.PVPGameBaseAI import PVPGameBaseAI
from direct.directnotify import DirectNotifyGlobal

class PVPGamePirateerAI(PVPGameBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGamePirateerAI')

    def __init__(self, air):
        PVPGameBaseAI.__init__(self, air)


    # coinCaptured(uint32) broadcast ram

    def coinCaptured(self, coinCaptured):
        self.sendUpdate('coinCaptured', [coinCaptured])

    # displayCoins(uint32 []) broadcast ram

    def displayCoins(self, displayCoins):
        self.sendUpdate('displayCoins', [displayCoins])

    # unDisplayCoin(uint32) broadcast

    def unDisplayCoin(self, unDisplayCoin):
        self.sendUpdate('unDisplayCoin', [unDisplayCoin])

    # lootWreck(uint32, uint32) clsend airecv

    def lootWreck(self, lootWreck, todo_uint32_1):
        pass

    # unLootWreck(uint32, uint32) clsend airecv

    def unLootWreck(self, unLootWreck, todo_uint32_1):
        pass

    # setMaxCarry(uint16) broadcast ram

    def setMaxCarry(self, maxCarry):
        self.sendUpdate('setMaxCarry', [maxCarry])

    # setMaxTeamScore(uint16) broadcast ram

    def setMaxTeamScore(self, maxTeamScore):
        self.sendUpdate('setMaxTeamScore', [maxTeamScore])

    # portEntered(string, uint32) airecv clsend

    def portEntered(self, portEntered, todo_uint32_1):
        pass

    # portExited(string, uint32) airecv clsend

    def portExited(self, portExited, todo_uint32_1):
        pass

    # setShipsNearBase(uint32 [], string []) broadcast ram

    def setShipsNearBase(self, shipsNearBase, todo_string_1):
        self.sendUpdate('setShipsNearBase', [shipsNearBase, todo_string_1])


