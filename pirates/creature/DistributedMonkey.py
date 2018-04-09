from pirates.creature.DistributedCreature import DistributedCreature
from pirates.creature.Monkey import Monkey

class DistributedMonkey(DistributedCreature):
    __module__ = __name__

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, Monkey())