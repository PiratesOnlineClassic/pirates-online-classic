
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class SnapshotDispatcherAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('SnapshotDispatcherAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # online()

    def online(self, online):
        self.sendUpdate('online', [online])

    # requestRender(uint32)

    def requestRender(self, requestRender):
        self.sendUpdate('requestRender', [requestRender])

    # avatarDeleted(uint32)

    def avatarDeleted(self, avatarDeleted):
        self.sendUpdate('avatarDeleted', [avatarDeleted])

    # requestNewWork(uint32)

    def requestNewWork(self, requestNewWork):
        self.sendUpdate('requestNewWork', [requestNewWork])

    # errorFetchingAvatar(uint32, uint32)

    def errorFetchingAvatar(self, errorFetchingAvatar, todo_uint32_1):
        self.sendUpdate('errorFetchingAvatar', [errorFetchingAvatar, todo_uint32_1])

    # errorRenderingAvatar(uint32, uint32)

    def errorRenderingAvatar(self, errorRenderingAvatar, todo_uint32_1):
        self.sendUpdate('errorRenderingAvatar', [errorRenderingAvatar, todo_uint32_1])

    # renderSuccessful(uint32, uint32)

    def renderSuccessful(self, renderSuccessful, todo_uint32_1):
        self.sendUpdate('renderSuccessful', [renderSuccessful, todo_uint32_1])


