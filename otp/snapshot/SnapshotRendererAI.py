from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class SnapshotRendererAI(DistributedObjectAI):
    """
    Renders avatar portraits for the website when asked by the snapshot
    dispatcher. Rendering needs a graphics pipe and is not done by this
    server, so requests are ignored.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('SnapshotRendererAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def online(self):
        pass

    def requestRender(self, dispatcherId, avatarId, writeToFile):
        self.notify.debug('Ignoring render request for avatar %d' % avatarId)
