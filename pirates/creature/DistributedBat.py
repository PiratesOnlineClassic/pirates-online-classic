from pirates.creature.Bat import Bat
from pirates.creature.DistributedCreature import DistributedCreature


class DistributedBat(DistributedCreature):
    

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, Bat())
