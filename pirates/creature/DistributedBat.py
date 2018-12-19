from pirates.creature.DistributedCreature import DistributedCreature
from pirates.creature.Bat import Bat

class DistributedBat(DistributedCreature):
    
    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, Bat())


