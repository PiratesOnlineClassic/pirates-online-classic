
from pirates.battle.DistributedIslandCannonAI import DistributedIslandCannonAI
from direct.directnotify import DirectNotifyGlobal

class DistributedFortCannonAI(DistributedIslandCannonAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFortCannonAI')

    def __init__(self, air):
        DistributedIslandCannonAI.__init__(self, air)
        self.fortId = 0


    # setFortId(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setFortId(self, fortId):
        self.fortId = fortId

    def d_setFortId(self, fortId):
        self.sendUpdate('setFortId', [fortId])

    def b_setFortId(self, fortId):
        self.setFortId(fortId)
        self.d_setFortId(fortId)

    def getFortId(self):
        return self.fortId

    # hitByProjectile() airecv clsend

    def hitByProjectile(self, hitByProjectile):
        pass


