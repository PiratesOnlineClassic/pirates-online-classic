from pirates.creature.DistributedCreature import DistributedCreature
from pirates.creature.Crab import Crab

class DistributedCrab(DistributedCreature):
    
    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, Crab())


