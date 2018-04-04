
from pirates.battle.DistributedWeaponAI import DistributedWeaponAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPCCannonAI(DistributedWeaponAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPCCannonAI')

    def __init__(self, air):
        DistributedWeaponAI.__init__(self, air)


    # gainSkill(uint32) airecv clsend

    def gainSkill(self, gainSkill):
        pass


