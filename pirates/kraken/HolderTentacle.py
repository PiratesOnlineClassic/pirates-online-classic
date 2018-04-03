# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.kraken.HolderTentacle
from pirates.creature.DistributedCreature import DistributedCreature
from pirates.kraken.HolderGameFSM import HolderGameFSM
from pirates.kraken.Holder import Holder

class HolderTentacle(DistributedCreature):
    __module__ = __name__

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, Holder())
        Holder.__init__(self)
        Holder.generateCreature(self)
        self.emergeIval = None
        return

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
            self.emergeIval = Sequence(Wait(random.random()), Func(self.creature.show), Func(self.play, 'emerge', blendInT=0))
        else:
            self.setPlayRate(-1, 'emerge')
            self.emergeIval = Sequence(Wait(random.random()), Func(self.play, 'emerge', blendOutT=0), Wait(self.creature.getDuration('emerge') / abs(self.creature.getPlayRate('emerge')) - 0.1), Func(self.creature.hide))
        self.emergeIval.start()
        return
# okay decompiling .\pirates\kraken\HolderTentacle.pyc
