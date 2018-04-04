
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedCharterableObjectAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCharterableObjectAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.ownerId = 0
        self.charter = 0
        self.charterTimestamp = 0
        self.timer = [0, 0]


    # setOwnerId(uint32) required broadcast ram db ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def d_setOwnerId(self, ownerId):
        self.sendUpdate('setOwnerId', [ownerId])

    def b_setOwnerId(self, ownerId):
        self.setOwnerId(ownerId)
        self.d_setOwnerId(ownerId)

    def getOwnerId(self):
        return self.ownerId

    # setCharter(uint8) required broadcast ram ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setCharter(self, charter):
        self.charter = charter

    def d_setCharter(self, charter):
        self.sendUpdate('setCharter', [charter])

    def b_setCharter(self, charter):
        self.setCharter(charter)
        self.d_setCharter(charter)

    def getCharter(self):
        return self.charter

    # setCharterTimestamp(int16) required broadcast ram ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setCharterTimestamp(self, charterTimestamp):
        self.charterTimestamp = charterTimestamp

    def d_setCharterTimestamp(self, charterTimestamp):
        self.sendUpdate('setCharterTimestamp', [charterTimestamp])

    def b_setCharterTimestamp(self, charterTimestamp):
        self.setCharterTimestamp(charterTimestamp)
        self.d_setCharterTimestamp(charterTimestamp)

    def getCharterTimestamp(self):
        return self.charterTimestamp

    # setTimer(uint16, int16) required broadcast ram ownrecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setTimer(self, timer, todo_int16_1):
        self.timer = timer

    def d_setTimer(self, timer, todo_int16_1):
        self.sendUpdate('setTimer', [timer, todo_int16_1])

    def b_setTimer(self, timer, todo_int16_1):
        self.setTimer(timer, todo_int16_1)
        self.d_setTimer(timer, todo_int16_1)

    def getTimer(self):
        return self.timer


