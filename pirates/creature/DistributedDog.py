from pirates.creature.DistributedAnimal import DistributedAnimal
from pirates.creature.Dog import Dog

class DistributedDog(DistributedAnimal):
    
    def __init__(self, cr):
        DistributedAnimal.__init__(self, cr, Dog())


