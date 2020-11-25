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

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def d_setOwnerId(self, ownerId):
        self.sendUpdate('setOwnerId', [ownerId])

    def b_setOwnerId(self, ownerId):
        self.setOwnerId(ownerId)
        self.d_setOwnerId(ownerId)

    def getOwnerId(self):
        return self.ownerId

    def setCharter(self, charter):
        self.charter = charter

    def d_setCharter(self, charter):
        self.sendUpdate('setCharter', [charter])

    def b_setCharter(self, charter):
        self.setCharter(charter)
        self.d_setCharter(charter)

    def getCharter(self):
        return self.charter

    def setCharterTimestamp(self, charterTimestamp):
        self.charterTimestamp = charterTimestamp

    def d_setCharterTimestamp(self, charterTimestamp):
        self.sendUpdate('setCharterTimestamp', [charterTimestamp])

    def b_setCharterTimestamp(self, charterTimestamp):
        self.setCharterTimestamp(charterTimestamp)
        self.d_setCharterTimestamp(charterTimestamp)

    def getCharterTimestamp(self):
        return self.charterTimestamp

    def setTimer(self, time, timestamp):
        self.timer = [time, timestamp]

    def d_setTimer(self, timer):
        self.sendUpdate('setTimer', [timer])

    def b_setTimer(self, timer):
        self.setTimer(timer)
        self.d_setTimer(timer)

    def getTimer(self):
        return self.timer
