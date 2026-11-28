from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.piratesbase import PiratesGlobals

class DistributedSurfaceTreasureAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSurfaceTreasureAI')

    # the client's interact options are not exclusive, any number
    # of pirates may loot the same treasure at once...
    MULTIUSE = True
    LootRate = config.GetFloat('pvp-surface-treasure-loot-rate', 1.0)
    LootAmount = config.GetInt('pvp-surface-treasure-loot-amount', 1)

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.withdrawType = 0
        self.opened = False
        self.belongToTeam = PiratesGlobals.INVALID_TEAM
        self.value = 0
        self.gameRules = None
        self.looters = []

    def delete(self):
        for avatarId in list(self.looters):
            self.stopLooting(avatarId)

        self.gameRules = None
        DistributedInteractiveAI.delete(self)

    def setGameRules(self, gameRules):
        # the pvp game rules which hold the loot carried by each pirate,
        # see PVPGameCTLAI.addLoot...
        self.gameRules = gameRules

    def getGameRules(self):
        return self.gameRules

    def setWithdrawType(self, withdrawType):
        self.withdrawType = withdrawType

    def d_setWithdrawType(self, withdrawType):
        self.sendUpdate('setWithdrawType', [withdrawType])

    def b_setWithdrawType(self, withdrawType):
        self.setWithdrawType(withdrawType)
        self.d_setWithdrawType(withdrawType)

    def getWithdrawType(self):
        return self.withdrawType
    def setOpen(self, opened):
        self.opened = opened

    def d_setOpen(self, opened):
        self.sendUpdate('setOpen', [opened])

    def b_setOpen(self, opened):
        self.setOpen(opened)
        self.d_setOpen(opened)

    def getOpen(self):
        return self.opened

    def setBelongsToTeam(self, team):
        self.belongToTeam = team

    def d_setBelongsToTeam(self, team):
        self.sendUpdate('setBelongsToTeam', [team])

    def b_setBelongsToTeam(self, team):
        self.setBelongsToTeam(team)
        self.d_setBelongsToTeam(team)

    def getBelongsToTeam(self):
        return self.belongToTeam

    def setValue(self, value):
        self.value = value

    def d_setValue(self, value):
        self.sendUpdate('setValue', [value])

    def b_setValue(self, value):
        self.setValue(value)
        self.d_setValue(value)

    def getValue(self):
        return self.value

    def d_setEmpty(self, empty):
        self.sendUpdate('setEmpty', [empty])

    def d_startLooting(self, avatarId, lootType):
        self.sendUpdateToAvatarId(avatarId, 'startLooting', [lootType])

    def d_stopLooting(self, avatarId):
        self.sendUpdateToAvatarId(avatarId, 'stopLooting', [])

    def handleRequestInteraction(self, avatar, interactType, instant):
        # the client only offers the interaction when the treasure holds value
        # and does not belong to the avatar's team, see DistributedSurfaceTreasure.enterProximity...
        if self.value <= 0:
            return self.DENY

        if self.withdrawType == PiratesGlobals.WITHDRAW_NONE:
            return self.DENY

        if self.belongToTeam != PiratesGlobals.INVALID_TEAM and \
                hasattr(avatar, 'getTeam') and avatar.getTeam() == self.belongToTeam:
            return self.DENY

        # the loot is carried by the pirates taking part in the game,
        # until they deposit it or have it taken from them...
        if not self.gameRules or avatar.doId not in self.gameRules.getPlayers():
            return self.DENY

        if self.gameRules.getLootCarried(avatar.doId) >= self.gameRules.getMaxCarry():
            return self.DENY

        if avatar.doId in self.looters:
            return self.DENY

        return self.ACCEPT

    def handlePostRequestInteraction(self, avatar):
        self.d_startLooting(avatar.doId, self.withdrawType)
        if self.withdrawType == PiratesGlobals.WITHDRAW_INCREMENTAL:
            # the looter steals from the treasure for as long as they stay with it,
            # the client sits in it's Stealing state until we tell it to stop...
            self.looters.append(avatar.doId)
            taskMgr.doMethodLater(self.LootRate, self.__lootTask,
                self.uniqueName('loot-%d' % avatar.doId), extraArgs=[avatar.doId], appendTask=True)

            return

        # otherwise the looter takes as much of the treasure as they can carry in one go...
        self.withdrawLoot(avatar.doId, self.value)
        self.d_stopLooting(avatar.doId)

    def handleRequestExit(self, avatar):
        self.stopLooting(avatar.doId)
        return self.ACCEPT

    def withdrawLoot(self, avatarId, amount):
        if not self.gameRules:
            return 0

        amount = self.gameRules.addLoot(avatarId, max(0, min(amount, self.value)))
        if amount:
            self.b_setValue(self.value - amount)
            if self.value <= 0:
                self.d_setEmpty(True)

        return amount

    def stopLooting(self, avatarId):
        if avatarId in self.looters:
            self.looters.remove(avatarId)
            taskMgr.remove(self.uniqueName('loot-%d' % avatarId))

        if avatarId in self.air.doId2do:
            self.d_stopLooting(avatarId)

    def __lootTask(self, avatarId, task):
        if avatarId not in self.air.doId2do or avatarId not in self.looters:
            self.stopLooting(avatarId)
            return Task.done

        if not self.withdrawLoot(avatarId, self.LootAmount) or self.value <= 0:
            self.stopLooting(avatarId)
            return Task.done

        return Task.again
