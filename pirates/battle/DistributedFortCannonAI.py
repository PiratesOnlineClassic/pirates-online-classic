from direct.directnotify import DirectNotifyGlobal

from pirates.battle.DistributedIslandCannonAI import DistributedIslandCannonAI


class DistributedFortCannonAI(DistributedIslandCannonAI):
    """
    AI-side implementation of a cannon that belongs to a fort.

    Fort cannons are positioned on forts and can be used by NPCs
    to attack player ships during the Black Pearl treasure map quest.
    A fort cannon stays out of action for as long as its fort is destroyed.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFortCannonAI')

    def __init__(self, air):
        DistributedIslandCannonAI.__init__(self, air)

        self.fortId = 0

    def announceGenerate(self):
        DistributedIslandCannonAI.announceGenerate(self)

        fort = self.getFort()
        if fort:
            fort.addCannon(self)

    def delete(self):
        fort = self.getFort()
        if fort:
            fort.removeCannon(self)

        DistributedIslandCannonAI.delete(self)

    # =========================================================================
    # DC Fields
    # =========================================================================

    def setFortId(self, fortId):
        self.fortId = fortId

    def d_setFortId(self, fortId):
        self.sendUpdate('setFortId', [fortId])

    def b_setFortId(self, fortId):
        self.setFortId(fortId)
        self.d_setFortId(fortId)

    def getFortId(self):
        return self.fortId

    def getFort(self):
        return self.air.doId2do.get(self.fortId)

    # =========================================================================
    # Destruction
    # =========================================================================

    def repairCannon(self):
        fort = self.getFort()
        if fort and fort.isDestroyed():
            return

        DistributedIslandCannonAI.repairCannon(self)
