from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.piratesbase import PiratesGlobals


class DistributedBankAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBankAI')

    MULTIUSE = True
    LootRate = config.GetFloat('pvp-bank-loot-rate', 1.0)
    LootAmount = config.GetInt('pvp-bank-loot-amount', 1)

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)

        self.modelPath = ''
        self.belongsToTeam = PiratesGlobals.INVALID_TEAM
        self.value = 0
        self.maxValue = 100
        self.parentObjId = 0
        self.gameRules = None
        self.looters = []

    def delete(self):
        for avatarId in list(self.looters):
            self.stopLooting(avatarId)

        if self.gameRules:
            self.gameRules.removeBank(self)
            self.gameRules = None

        DistributedInteractiveAI.delete(self)

    def setGameRules(self, gameRules):
        self.gameRules = gameRules

    def getGameRules(self):
        return self.gameRules

    # -------------------------------------------------------------------
    # Interaction
    # -------------------------------------------------------------------

    def handleRequestInteraction(self, avatar, interactType, instant):
        if not self.gameRules or avatar.doId not in self.gameRules.getPlayers():
            return self.DENY

        if self.belongsToTeam == avatar.getPVPTeam():
            return self.DENY

        if self.value <= 0:
            return self.DENY

        if self.gameRules.getLootCarried(avatar.doId) >= self.gameRules.getMaxCarry():
            return self.DENY

        return self.ACCEPT

    def handlePostRequestInteraction(self, avatar):
        self.startLooting(avatar.doId)

    def handleRequestExit(self, avatar):
        if avatar.doId not in self.looters:
            return self.DENY

        return self.ACCEPT

    def handlePostRequestExit(self, avatar):
        self.stopLooting(avatar.doId)

    def startLooting(self, avatarId):
        if avatarId in self.looters:
            return

        self.looters.append(avatarId)
        self.d_startLooting(avatarId, PiratesGlobals.TREASURE_BANK)
        taskMgr.doMethodLater(self.LootRate, self.__lootTask,
            self.uniqueName('loot-%d' % avatarId), extraArgs=[avatarId], appendTask=True)

    def stopLooting(self, avatarId):
        if avatarId not in self.looters:
            return

        self.looters.remove(avatarId)
        taskMgr.remove(self.uniqueName('loot-%d' % avatarId))
        if avatarId in self.air.doId2do:
            self.d_stopLooting(avatarId)

    def __lootTask(self, avatarId, task):
        if avatarId not in self.air.doId2do or not self.gameRules:
            self.stopLooting(avatarId)
            return Task.done

        amount = self.gameRules.addLoot(avatarId, min(self.LootAmount, self.value))
        if not amount:
            self.stopLooting(avatarId)
            return Task.done

        self.b_setValue(self.value - amount)
        if self.value <= 0:
            self.stopLooting(avatarId)
            return Task.done

        return Task.again

    def d_startLooting(self, avatarId, lootType):
        self.sendUpdateToAvatarId(avatarId, 'startLooting', [lootType])

    def d_stopLooting(self, avatarId):
        self.sendUpdateToAvatarId(avatarId, 'stopLooting', [])

    # -------------------------------------------------------------------
    # DC fields
    # -------------------------------------------------------------------

    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def getModelPath(self):
        return self.modelPath

    def setBelongsToTeam(self, team):
        self.belongsToTeam = team

    def d_setBelongsToTeam(self, team):
        self.sendUpdate('setBelongsToTeam', [team])

    def b_setBelongsToTeam(self, team):
        self.setBelongsToTeam(team)
        self.d_setBelongsToTeam(team)

    def getBelongsToTeam(self):
        return self.belongsToTeam

    def setValue(self, value):
        self.value = max(0, value)

    def d_setValue(self, value):
        self.sendUpdate('setValue', [value])

    def b_setValue(self, value):
        self.setValue(value)
        self.d_setValue(self.value)

    def getValue(self):
        return self.value

    def addValue(self, amount):
        self.b_setValue(self.value + amount)

    def setMaxValue(self, maxValue):
        self.maxValue = maxValue

    def d_setMaxValue(self, maxValue):
        self.sendUpdate('setMaxValue', [maxValue])

    def b_setMaxValue(self, maxValue):
        self.setMaxValue(maxValue)
        self.d_setMaxValue(maxValue)

    def getMaxValue(self):
        return self.maxValue

    def setParentObjId(self, parentObjId):
        self.parentObjId = parentObjId

    def getParentObjId(self):
        return self.parentObjId
