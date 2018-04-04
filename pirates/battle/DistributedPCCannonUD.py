
from pirates.battle.DistributedWeaponUD import DistributedWeaponUD
from direct.directnotify import DirectNotifyGlobal

class DistributedPCCannonUD(DistributedWeaponUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPCCannonUD')

    def __init__(self, air):
        DistributedWeaponUD.__init__(self, air)




