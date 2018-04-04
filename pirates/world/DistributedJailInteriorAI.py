
from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
from direct.directnotify import DirectNotifyGlobal

class DistributedJailInteriorAI(DistributedGAInteriorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedJailInteriorAI')

    def __init__(self, air):
        DistributedGAInteriorAI.__init__(self, air)


    # avatarAlreadyInJail() airecv clsend

    def avatarAlreadyInJail(self, avatarAlreadyInJail):
        pass


