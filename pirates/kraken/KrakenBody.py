# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.kraken.KrakenBody
from pirates.creature.DistributedCreature import DistributedCreature
from pirates.kraken.Body import Body
from pirates.kraken.BodyGameFSM import BodyGameFSM


class KrakenBody(Body, DistributedCreature):
    

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr)
        Body.__init__(self)
        Body.generateCreature(self)

    def delete(self):
        Body.delete(self)
        DistributedCreature.delete(self)

    def setKrakenId(self, krackenId):
        self.krakenId = krackenId

    def getKrakenId(self):
        return self.krakenId

    def getKraken(self):
        return self.cr.getDo(self.krakenId)

    def createGameFSM(self):
        self.gameFSM = BodyGameFSM(self)

    def reparentTo(self, *args, **kw):
        Body.reparentTo(self, *args, **kw)
        import pdb
        pdb.set_trace()
# okay decompiling .\pirates\kraken\KrakenBody.pyc
