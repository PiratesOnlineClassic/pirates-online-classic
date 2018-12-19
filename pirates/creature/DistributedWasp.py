from pirates.creature.DistributedCreature import DistributedCreature
from pirates.creature.Wasp import Wasp

class DistributedWasp(DistributedCreature):
    
    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, Wasp())


