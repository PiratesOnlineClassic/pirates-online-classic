
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class SnapshotRendererAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('SnapshotRendererAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # online()

    def online(self, online):
        self.sendUpdate('online', [online])

    # requestRender(uint32, uint32, string)

    def requestRender(self, requestRender, todo_uint32_1, todo_string_2):
        self.sendUpdate('requestRender', [requestRender, todo_uint32_1, todo_string_2])


