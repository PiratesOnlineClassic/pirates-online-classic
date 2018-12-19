from pirates.creature.DistributedAnimal import DistributedAnimal
from pirates.creature.Chicken import Chicken

class DistributedChicken(DistributedAnimal):
    
    def __init__(self, cr):
        DistributedAnimal.__init__(self, cr, Chicken())


