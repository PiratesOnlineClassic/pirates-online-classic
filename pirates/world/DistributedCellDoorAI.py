import random

from direct.directnotify import DirectNotifyGlobal

from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI


class DistributedCellDoorAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCellDoorAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)

        self.cellIndex = 0
        self.maxHealth = 100
        self.health = 100
        self.avatarId = 0

    def handleRequestInteraction(self, avatar, interactType, instant):
        return self.ACCEPT

    def handleRequestExit(self, avatar):
        return self.ACCEPT

    def setCellIndex(self, cellIndex):
        self.cellIndex = cellIndex

    def d_setCellIndex(self, cellIndex):
        self.sendUpdate('setCellIndex', [cellIndex])

    def b_setCellIndex(self, cellIndex):
        self.setCellIndex(cellIndex)
        self.d_setCellIndex(cellIndex)

    def getCellIndex(self):
        return self.cellIndex

    def setMaxHealth(self, maxHealth):
        self.maxHealth = maxHealth

    def getMaxHealth(self):
        return self.maxHealth

    def setHealth(self, health):
        self.health = health

    def d_setHealth(self, health):
        self.sendUpdate('setHealth', [health])

    def b_setHealth(self, health):
        self.setHealth(health)
        self.d_setHealth(health)

    def getHealth(self):
        return self.health

    def setAvatarId(self, avatarId):
        self.avatarId = avatarId

    def getAvatarId(self):
        return self.avatarId

    def doorKicked(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        if self.avatarId:
            return

        self.b_setHealth(max(0, min(self.getHealth() - (random.random() * \
            self.getMaxHealth()), 100)))

        if self.health <= 0:
            self.setAvatarId(avatar.doId)
            self.d_rejectInteraction(avatar.doId)
            return
