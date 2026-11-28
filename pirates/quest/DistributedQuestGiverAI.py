from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from pirates.quest import QuestConstants


class DistributedQuestGiverAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedQuestGiverAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.avatar2offers = {}

    def d_setQuestOffer(self, avatarId, offers):
        self.avatar2offers[avatarId] = list(offers)
        self.sendUpdateToAvatarId(avatarId, 'setQuestOffer', [offers])

    def d_setQuestLadderOffer(self, avatarId, offers, quitButton):
        self.avatar2offers[avatarId] = list(offers)
        self.sendUpdateToAvatarId(avatarId, 'setQuestLadderOffer', [offers, quitButton])

    def getOffers(self, avatarId):
        return self.avatar2offers.get(avatarId)

    def setOfferResponse(self, index, ladder):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        offers = self.avatar2offers.pop(avatar.doId, None)
        if offers is None:
            self.notify.warning('Received offer response from avatar %d, '
                'but no quests were offered to them by %d!' % (avatar.doId, self.doId))

            return

        if index == QuestConstants.CANCEL_QUEST:
            return

        if index < 0 or index >= len(offers):
            self.air.logPotentialHacker(message='Received invalid quest offer response!',
                index=index, numOffers=len(offers), giverId=self.doId)

            return

        questId = offers[index].getQuestId()
        if self.air.questMgr.hasQuest(avatar, questId=questId):
            self.notify.debug('Avatar %d already has offered quest %s!' % (avatar.doId, questId))
            return

        self.air.questMgr.createQuest(avatar, questId)

    def d_playDialogMovie(self, avatarId, dialogId):
        self.sendUpdateToAvatarId(avatarId, 'playDialogMovie', [dialogId])

    def d_setQuestsCompleted(self, avatarId, menuFlag=1, completedContainerIds=[], completedChainedQuestIds=[], completedQuestIds=[], completedQuestDoIds=[]):
        self.sendUpdateToAvatarId(avatarId, 'setQuestsCompleted', [menuFlag, completedContainerIds, completedChainedQuestIds, completedQuestIds, completedQuestDoIds])

    def dialogMovieComplete(self):
        messenger.send('dialog-complete-%d' % self.doId)
