from pirates.creature.DistributedCreature import DistributedCreature
from pirates.creature.FlyTrap import FlyTrap

class DistributedFlyTrap(DistributedCreature):
    
    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, FlyTrap())


