from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal

class DistributedTravelAgent(DistributedObjectGlobal):
    notify = directNotify.newCategory('DistributedTravelAgent')

    def __init__(self, air):
        DistributedObjectGlobal.__init__(self, air)
