from direct.interval.IntervalGlobal import *
from pirates.creature.DistributedCreature import DistributedCreature
from pirates.creature.Stump import Stump

class DistributedStump(DistributedCreature):
    
    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, Stump())


