from direct.directnotify import DirectNotifyGlobal
from otp.snapshot.SnapshotRendererAI import SnapshotRendererAI


class PSnapshotRendererAI(SnapshotRendererAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PSnapshotRendererAI')
