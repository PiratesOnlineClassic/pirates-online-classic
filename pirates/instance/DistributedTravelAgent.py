from direct.distributed import DistributedObject

class DistributedTravelAgent(DistributedObject.DistributedObject):
    notify = directNotify.newCategory('DistributedTravelAgent')
    
    def __init__(self, air):
        DistributedObject.DistributedObject.__init__(self, air)

