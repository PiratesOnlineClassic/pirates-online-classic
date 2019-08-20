from pirates.creature.DistributedAnimal import DistributedAnimal
from pirates.creature.Rooster import Rooster

class DistributedRooster(DistributedAnimal):
    
    def __init__(self, cr):
        DistributedAnimal.__init__(self, cr, Rooster())


