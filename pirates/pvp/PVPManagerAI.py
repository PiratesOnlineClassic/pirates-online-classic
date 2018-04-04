
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PVPManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # requestChallenge(uint32) airecv clsend

    def requestChallenge(self, requestChallenge):
        pass

    # acceptChallenge(uint32) airecv clsend

    def acceptChallenge(self, acceptChallenge):
        pass

    # challengeAccepted(uint32)

    def challengeAccepted(self, challengeAccepted):
        self.sendUpdate('challengeAccepted', [challengeAccepted])

    # challengeFrom(uint32)

    def challengeFrom(self, challengeFrom):
        self.sendUpdate('challengeFrom', [challengeFrom])


