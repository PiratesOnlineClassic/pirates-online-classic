from direct.directnotify import DirectNotifyGlobal
from otp.snapshot.SnapshotRendererUD import SnapshotRendererUD


class PSnapshotRendererUD(SnapshotRendererUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PSnapshotRendererUD')
