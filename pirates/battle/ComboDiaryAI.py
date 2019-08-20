from pirates.battle.ComboDiary import ComboDiary
from direct.directnotify.DirectNotifyGlobal import directNotify

class ComboDiaryAI(ComboDiary):
    notify = directNotify.newCategory('ComboDiaryAI')

    def __init__(self, air, av):
        self.air = air

        ComboDiary.__init__(self, av)

    def hasCombo(self, avId, skillId):
        if avId not in self.timers:
            return False

        for combo in self.timers[avId]:
            if combo[self.SKILLID_INDEX] == skillId:
                return True

        return False

    def addCombo(self, avId, timestamp, skillId, damage):
        if avId in self.timers:
            return

        self.timers[avId] = [[timestamp, skillId, damage]]

    def removeCombo(self, avId, skillId):
        if avId not in self.timers:
            return

        for combo in self.timers[avId]:
            if combo[self.SKILLID_INDEX] == skillId:
                self.timers[avId].remove(combo)

    def removeCombos(self, avId):
        if avId not in self.timers:
            return

        del self.timers[avId]

    def getCombos(self, avId):
        return self.timers.get(avId, [])
