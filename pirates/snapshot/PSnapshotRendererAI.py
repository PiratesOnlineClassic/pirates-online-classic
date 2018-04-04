
from otp.snapshot.SnapshotRendererAI import SnapshotRendererAI
from direct.directnotify import DirectNotifyGlobal

class PSnapshotRendererAI(SnapshotRendererAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PSnapshotRendererAI')

    def __init__(self, air):
        SnapshotRendererAI.__init__(self, air)



