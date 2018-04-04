
from direct.distributed.DistributedSmoothNode import DistributedSmoothNode
from direct.directnotify import DirectNotifyGlobal

class DistributedAvatarUD(DistributedSmoothNode):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAvatarUD')

    def __init__(self, air):
        DistributedSmoothNode.__init__(self, air)
        self.name = ''


    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name



    # confirmAvOnShard(uint32, int8)

    def confirmAvOnShard(self, confirmAvOnShard, todo_int8_1):
        self.sendUpdate('confirmAvOnShard', [confirmAvOnShard, todo_int8_1])


