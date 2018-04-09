from pirates.creature.Chicken import Chicken
from pirates.creature.DistributedAnimal import DistributedAnimal


class DistributedChicken(DistributedAnimal):
    

    def __init__(self, cr):
        DistributedAnimal.__init__(self, cr, Chicken())