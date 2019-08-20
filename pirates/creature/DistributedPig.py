from pirates.creature.DistributedAnimal import DistributedAnimal
from pirates.creature.Pig import Pig

class DistributedPig(DistributedAnimal):
    
    def __init__(self, cr):
        DistributedAnimal.__init__(self, cr, Pig())


