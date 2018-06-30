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
