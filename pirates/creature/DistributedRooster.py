from pirates.creature.DistributedAnimal import DistributedAnimal
from pirates.creature.Rooster import Rooster

class DistributedRooster(DistributedAnimal):
    __module__ = __name__

    def __init__(self, cr):
        DistributedAnimal.__init__(self, cr, Rooster())