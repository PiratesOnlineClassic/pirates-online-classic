
from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from direct.directnotify import DirectNotifyGlobal

class DistributedAvatarAI(DistributedSmoothNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAvatarAI')

    def __init__(self, air):
        DistributedSmoothNodeAI.__init__(self, air)
        self.name = ''


    # setName(string) required broadcast db airecv
    
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

    # friendsNotify(int32, int8) ownrecv airecv clsend

    def friendsNotify(self, friendsNotify, todo_int8_1):
        pass

    # checkAvOnShard(uint32) clsend airecv

    def checkAvOnShard(self, checkAvOnShard):
        pass

    # confirmAvOnShard(uint32, int8)

    def confirmAvOnShard(self, confirmAvOnShard, todo_int8_1):
        self.sendUpdate('confirmAvOnShard', [confirmAvOnShard, todo_int8_1])


