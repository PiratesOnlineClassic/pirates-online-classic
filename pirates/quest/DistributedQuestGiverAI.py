from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedQuestGiverAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedQuestGiverAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def d_playDialogMovie(self, avatarId, dialogId):
        self.sendUpdateToAvatarId(avatarId, 'playDialogMovie', [dialogId])

    def dialogMovieComplete(self):
        messenger.send('dialog-complete-%d' % self.doId)
