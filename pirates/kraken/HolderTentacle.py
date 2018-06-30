from pirates.creature.DistributedCreature import DistributedCreature
from pirates.kraken.Holder import Holder
from pirates.kraken.HolderGameFSM import HolderGameFSM


class HolderTentacle(DistributedCreature):

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, Holder())
        Holder.__init__(self)
        Holder.generateCreature(self)
        self.emergeIval = None

    def delete(self):
        Holder.delete(self)
        DistributedCreature.delete(self)

    def setKrakenId(self, krackenId):
        self.krakenId = krackenId

    def getKrakenId(self):
        return self.krakenId

    def getKraken(self):
        return self.cr.getDo(self.krakenId)

    def createGameFSM(self):
        self.gameFSM = HolderGameFSM(self)

    def emerge(self, emerge):
        if self.emergeIval:
            self.emergeIval.finish()
            self.emergeIval = None
        if emerge:
            self.setPlayRate(0.75, 'emerge')
            self.emergeIval = Sequence(
                Wait(random.random()), Func(self.creature.show),
                Func(self.play, 'emerge', blendInT=0))
        else:
            self.setPlayRate(-1, 'emerge')
            self.emergeIval = Sequence(
                Wait(random.random()), Func(self.play, 'emerge', blendOutT=0),
                Wait(
                    self.creature.getDuration('emerge') /
                    abs(self.creature.getPlayRate('emerge')) - 0.1),
                Func(self.creature.hide))
        self.emergeIval.start()
