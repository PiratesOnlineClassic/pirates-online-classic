
from pirates.pvp.PVPGameBaseAI import PVPGameBaseAI
from direct.directnotify import DirectNotifyGlobal

class PVPGameCTLAI(PVPGameBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameCTLAI')

    def __init__(self, air):
        PVPGameBaseAI.__init__(self, air)


    # treasureDeposited(uint32) airecv clsend

    def treasureDeposited(self, treasureDeposited):
        pass

    # setMaxCarry(uint16) broadcast ram

    def setMaxCarry(self, maxCarry):
        self.sendUpdate('setMaxCarry', [maxCarry])

    # setMaxTeamScore(uint16) broadcast ram

    def setMaxTeamScore(self, maxTeamScore):
        self.sendUpdate('setMaxTeamScore', [maxTeamScore])

    # shipDeposit(uint32) airecv clsend

    def shipDeposit(self, shipDeposit):
        pass

    # shipDeposited(uint32)

    def shipDeposited(self, shipDeposited):
        self.sendUpdate('shipDeposited', [shipDeposited])

    # portEntered(string, uint32) airecv clsend

    def portEntered(self, portEntered, todo_uint32_1):
        pass

    # portExited(string, uint32) airecv clsend

    def portExited(self, portExited, todo_uint32_1):
        pass

    # requestDropTreasure() airecv clsend

    def requestDropTreasure(self, requestDropTreasure):
        pass

    # setShipsNearBase(uint32 [], string []) broadcast ram

    def setShipsNearBase(self, shipsNearBase, todo_string_1):
        self.sendUpdate('setShipsNearBase', [shipsNearBase, todo_string_1])


