from pirates.creature.DistributedCreature import DistributedCreature
from pirates.creature.Monkey import Monkey

class DistributedMonkey(DistributedCreature):
    
    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, Monkey())


