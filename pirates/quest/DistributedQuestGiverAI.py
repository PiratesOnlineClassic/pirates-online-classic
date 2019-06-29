from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class DistributedQuestGiverAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedQuestGiverAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def d_setQuestOffer(self, avatarId, offers):
        self.sendUpdateToAvatarId(avatarId, 'setQuestOffer', [offers])

    def d_setQuestLadderOffer(self, avatarId, offers, quitButton):
        self.sendUpdateToAvatarId(avatarId, 'setQuestLadderOffer', [offers, quitButton])

    def d_playDialogMovie(self, avatarId, dialogId):
        self.sendUpdateToAvatarId(avatarId, 'playDialogMovie', [dialogId])

    def d_setQuestsCompleted(self, avatarId, menuFlag=1, completedContainerIds=[], completedChainedQuestIds=[], completedQuestIds=[], completedQuestDoIds=[]):
        self.sendUpdateToAvatarId(avatarId, 'setQuestsCompleted', [menuFlag, completedContainerIds, completedChainedQuestIds, completedQuestIds, completedQuestDoIds])

    def dialogMovieComplete(self):
        messenger.send('dialog-complete-%d' % self.doId)
