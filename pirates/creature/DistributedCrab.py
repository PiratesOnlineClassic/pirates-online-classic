from pirates.creature.Crab import Crab
from pirates.creature.DistributedCreature import DistributedCreature

class DistributedCrab(DistributedCreature):
    

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, Crab())