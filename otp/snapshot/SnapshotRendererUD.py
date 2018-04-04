
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class SnapshotRendererUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('SnapshotRendererUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)


    # online()

    def online(self, online):
        self.sendUpdate('online', [online])

    # requestRender(uint32, uint32, string)

    def requestRender(self, requestRender, todo_uint32_1, todo_string_2):
        self.sendUpdate('requestRender', [requestRender, todo_uint32_1, todo_string_2])


