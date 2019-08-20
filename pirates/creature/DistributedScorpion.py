from pirates.creature.DistributedCreature import DistributedCreature
from pirates.creature.Scorpion import Scorpion

class DistributedScorpion(DistributedCreature):
    
    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, Scorpion())


