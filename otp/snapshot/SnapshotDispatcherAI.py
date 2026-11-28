from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class SnapshotDispatcherAI(DistributedObjectAI):
    """
    The snapshot dispatcher handed avatar portrait render jobs (used by the
    website) out to the snapshot renderers. No renderers run on this server,
    so render requests are acknowledged and dropped.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('SnapshotDispatcherAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def online(self):
        pass

    def requestRender(self, avatarId):
        self.notify.debug('Ignoring render request for avatar %d, no snapshot renderers.' % avatarId)

    def avatarDeleted(self, avatarId):
        pass

    def requestNewWork(self, rendererId):
        pass

    def errorFetchingAvatar(self, rendererId, avatarId):
        self.notify.warning('Renderer %d failed to fetch avatar %d' % (rendererId, avatarId))

    def errorRenderingAvatar(self, rendererId, avatarId):
        self.notify.warning('Renderer %d failed to render avatar %d' % (rendererId, avatarId))

    def renderSuccessful(self, rendererId, avatarId):
        pass
