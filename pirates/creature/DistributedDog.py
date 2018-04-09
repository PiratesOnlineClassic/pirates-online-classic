from pirates.creature.DistributedAnimal import DistributedAnimal
from pirates.creature.Dog import Dog

class DistributedDog(DistributedAnimal):
    __module__ = __name__

    def __init__(self, cr):
        DistributedAnimal.__init__(self, cr, Dog())