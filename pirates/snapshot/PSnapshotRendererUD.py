
from otp.snapshot.SnapshotRendererUD import SnapshotRendererUD
from direct.directnotify import DirectNotifyGlobal

class PSnapshotRendererUD(SnapshotRendererUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PSnapshotRendererUD')

    def __init__(self, air):
        SnapshotRendererUD.__init__(self, air)



