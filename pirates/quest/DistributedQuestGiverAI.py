# NO BASE CLASSES WERE FOUND! 
 #THIS CLASS LIKELY HAD NO DEFINITION IN THE DCLASS FILES WHEN stub_generator.py WAS RUN!

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedQuestGiverAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedQuestGiverAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # setQuestOffer(QuestOffer [])

    def setQuestOffer(self, questOffer):
        self.sendUpdate('setQuestOffer', [questOffer])

    # setQuestLadderOffer(QuestLadderOffer [], int8)

    def setQuestLadderOffer(self, questLadderOffer, todo_int8_1):
        self.sendUpdate('setQuestLadderOffer', [questLadderOffer, todo_int8_1])

    # setOfferResponse(int8, int8) airecv clsend

    def setOfferResponse(self, offerResponse, todo_int8_1):
        pass

    # setQuestsCompleted(int8, QuestId [], QuestId [], QuestId [], uint32 [])

    def setQuestsCompleted(self, questsCompleted, todo_QuestId_1, todo_QuestId_2, todo_QuestId_3, todo_uint32_4):
        self.sendUpdate('setQuestsCompleted', [questsCompleted, todo_QuestId_1, todo_QuestId_2, todo_QuestId_3, todo_uint32_4])

    # playDialogMovie(string)

    def playDialogMovie(self, playDialogMovie):
        self.sendUpdate('playDialogMovie', [playDialogMovie])

    # dialogMovieComplete() airecv clsend

    def dialogMovieComplete(self, dialogMovieComplete):
        pass


