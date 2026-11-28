from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal


class SnapshotRendererUD(DistributedObjectGlobalUD):
    """
    Renders avatar portraits for the website when asked by the snapshot
    dispatcher. Rendering needs a graphics pipe and is not done by this
    server, so requests are ignored.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('SnapshotRendererUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def online(self):
        pass

    def requestRender(self, dispatcherId, avatarId, writeToFile):
        self.notify.debug('Ignoring render request for avatar %d' % avatarId)
