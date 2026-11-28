from direct.directnotify import DirectNotifyGlobal

from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.piratesbase import PiratesGlobals

class DistributedSurfaceTreasureAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSurfaceTreasureAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.withdrawType = 0
        self.opened = False
        self.belongToTeam = PiratesGlobals.INVALID_TEAM
        self.value = 0

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

        if self.belongToTeam != PiratesGlobals.INVALID_TEAM and \
                hasattr(avatar, 'getTeam') and avatar.getTeam() == self.belongToTeam:
            return self.DENY

        return self.ACCEPT

    def handlePostRequestInteraction(self, avatar):
        self.d_startLooting(avatar.doId, self.withdrawType)

    def handleRequestExit(self, avatar):
        self.d_stopLooting(avatar.doId)
        return self.ACCEPT
