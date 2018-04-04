
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTimeOfDayManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTimeOfDayManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.sync = [0, 0, 0, 0]


    # sync(uint8, uint8, uint32, uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def sync(self, sync, todo_uint8_1, todo_uint32_2, todo_uint32_3):
        self.sync = sync

    def d_sync(self, sync, todo_uint8_1, todo_uint32_2, todo_uint32_3):
        self.sendUpdate('sync', [sync, todo_uint8_1, todo_uint32_2, todo_uint32_3])

    def b_sync(self, sync, todo_uint8_1, todo_uint32_2, todo_uint32_3):
        self.sync(sync, todo_uint8_1, todo_uint32_2, todo_uint32_3)
        self.d_sync(sync, todo_uint8_1, todo_uint32_2, todo_uint32_3)

    def gync(self):
        return self.sync


