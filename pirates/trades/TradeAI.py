from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from otp.uberdog.RejectCode import RejectCode
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import ItemType
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory, InventoryId


class TradeBase(object):

    def giveStack(self, avatar, stackType, quantity):
        inventory = avatar.getInventory()
        if not inventory:
            self.notify.warning('Failed to give stackType: %d for avatar %d, '
                'avatar has no inventory!' % (stackType, avatar.doId))

            return

        currentQuantity = inventory.getStackQuantity(stackType)
        inventory.b_setStackQuantity(stackType, currentQuantity + quantity)

    def giveStackableTypeLimit(self, avatar, stackType, limit):
        inventory = avatar.getInventory()
        if not inventory:
            self.notify.warning('Failed to give stackType: %d limit for avatar %d, '
                'avatar has no inventory!' % (stackType, avatar.doId))

            return

        inventory.b_setStackLimit(stackType, limit)


class LocalTrade(TradeBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('LocalTrade')

    def __init__(self, air):
        self.air = air

        self.avatarId = 0
        self.avatar = None

    def setAvatarId(self, avatarId):
        self.avatarId = avatarId
        self.avatar = self.air.doId2do.get(self.avatarId)

    def getAvatarId(self):
        return self.avatarId

    def giveNewTreasureMap(self, mapId, callback):
        inventory = self.avatar.getInventory() if self.avatar else None
        if not inventory:
            callback(False)
            return
        inventory.giveTreasureMap(mapId, callback)

    def giveStack(self, stackType, quantity):
        TradeBase.giveStack(self, self.avatar, stackType, quantity)

    def giveStackableTypeLimit(self, stackType, limit):
        TradeBase.giveStackableTypeLimit(self, self.avatar, stackType, limit)

    def giveReputation(self, reputationType, reputation):
        inventory = self.avatar.getInventory()
        if not inventory:
            self.notify.warning('Failed to give reputationType: %d for avatar %d, '
                'avatar has no inventory!' % (reputationType, self.avatar.doId))

            return

        currentReputation = inventory.getReputation(reputationType)
        inventory.setReputation(reputationType, currentReputation + reputation)

        # all reputation earned also counts towards the avatar's overall
        # reputation (notoriety), just as it does in BattleManagerAI.rewardAttacker...
        if reputationType != InventoryType.OverallRep:
            inventory.setOverallRep(inventory.getOverallRep() + reputation)

    def giveGoldInPocket(self, amount):
        inventory = self.avatar.getInventory()
        if not inventory:
            self.notify.warning('Failed to give %d gold to avatar %d, '
                'avatar has no inventory!' % (amount, self.avatar.doId))

            return

        inventory.setGoldInPocket(inventory.getGoldInPocket() + amount)

    def givePlayingCard(self, cardId):
        self.giveStack(InventoryType.begin_Cards + cardId, 1)

    def giveShip(self, shipDoId):
        inventory = self.avatar.getInventory()
        if not inventory:
            self.notify.warning('Failed to give ship %d to avatar %d, '
                'avatar has no inventory!' % (shipDoId, self.avatar.doId))

            return

        shipList = inventory.getShipDoIdList()
        if shipDoId not in shipList:
            inventory.setShipDoIdList(shipList + [shipDoId])

    def giveNewShipToken(self):
        self.giveStack(InventoryType.NewShipToken, 1)

    def giveTeleportToken(self, tokenType):
        inventory = self.avatar.getInventory()
        if not inventory:
            self.notify.warning('Failed to give teleport tokenType: %d for avatar %d, '
                'avatar has no inventory!' % (tokenType, self.avatar.doId))

            return

        inventory.b_setStackQuantity(tokenType, 1)

    def giveTortugaTeleportToken(self):
        self.giveTeleportToken(InventoryType.TortugaTeleportToken)

    def giveCubaTeleportToken(self):
        self.giveTeleportToken(InventoryType.CubaTeleportToken)

    def givePortRoyalTeleportToken(self):
        self.giveTeleportToken(InventoryType.PortRoyalTeleportToken)

    def givePadresDelFuegoTeleportToken(self):
        self.giveTeleportToken(InventoryType.PadresDelFuegoTeleportToken)

    def giveKingsheadTeleportToken(self):
        self.giveTeleportToken(InventoryType.KingsheadTeleportToken)

    def giveSkill(self, skillType, value):
        inventory = self.avatar.getInventory()
        if not inventory:
            self.notify.warning('Failed to give skill type: %d for avatar %d, '
                'avatar has no inventory!' % (skillType, self.avatar.doId))

            return

        inventory.b_setStackQuantity(skillType, value)

    def giveCutlassTraining(self):
        self.giveStack(InventoryType.CutlassToken, 1)

    def givePistolTraining(self):
        self.giveStack(InventoryType.PistolToken, 1)

    def giveDollTraining(self):
        self.giveStack(InventoryType.DollToken, 1)

    def giveDaggersTraining(self):
        self.giveStack(InventoryType.DaggerToken, 1)

    def giveGrenadeTraining(self):
        self.giveStack(InventoryType.GrenadeToken, 1)

    def giveWandTraining(self):
        self.giveStack(InventoryType.WandToken, 1)


class TradeAI(DistributedObjectAI, TradeBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('TradeAI')

    STATUS_NOT_READY = 0
    STATUS_READY = 1

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.firstAvatarId = 0
        self.firstAvatarStatus = 0
        self.firstAvatarGiving = []
        self.secondAvatarId = 0
        self.secondAvatarStatus = 0
        self.secondAvatarGiving = []

        self.firstAvatar = None
        self.secondAvatar = None
        self.finished = False

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        # cancel the trade if either avatar leaves the shard mid trade...
        for avatarId in (self.firstAvatarId, self.secondAvatarId):
            self.accept(self.air.getAvatarExitEvent(avatarId), self.handleAvatarExit, extraArgs=[avatarId])

    def delete(self):
        self.ignoreAll()
        self.firstAvatar = None
        self.secondAvatar = None
        DistributedObjectAI.delete(self)

    def setFirstAvatarId(self, avatarId):
        self.firstAvatarId = avatarId
        self.firstAvatar = self.air.doId2do.get(self.firstAvatarId)

    def getFirstAvatarId(self):
        return self.firstAvatarId

    def setFirstAvatarStatus(self, avatarStatus):
        self.firstAvatarStatus = avatarStatus

    def d_setFirstAvatarStatus(self, avatarStatus):
        self.sendUpdate('setFirstAvatarStatus', [avatarStatus])

    def b_setFirstAvatarStatus(self, avatarStatus):
        self.setFirstAvatarStatus(avatarStatus)
        self.d_setFirstAvatarStatus(avatarStatus)

    def getFirstAvatarStatus(self):
        return self.firstAvatarStatus

    def setFirstAvatarGiving(self, giving):
        self.firstAvatarGiving = giving

    def d_setFirstAvatarGiving(self, giving):
        self.sendUpdate('setFirstAvatarGiving', [giving])

    def b_setFirstAvatarGiving(self, giving):
        self.setFirstAvatarGiving(giving)
        self.d_setFirstAvatarGiving(giving)

    def getFirstAvatarGiving(self):
        return self.firstAvatarGiving

    def setSecondAvatarId(self, avatarId):
        self.secondAvatarId = avatarId
        self.secondAvatar = self.air.doId2do.get(self.secondAvatarId)

    def getSecondAvatarId(self):
        return self.secondAvatarId

    def setSecondAvatarStatus(self, avatarStatus):
        self.secondAvatarStatus = avatarStatus

    def d_setSecondAvatarStatus(self, avatarStatus):
        self.sendUpdate('setSecondAvatarStatus', [avatarStatus])

    def b_setSecondAvatarStatus(self, avatarStatus):
        self.setSecondAvatarStatus(avatarStatus)
        self.d_setSecondAvatarStatus(avatarStatus)

    def getSecondAvatarStatus(self):
        return self.secondAvatarStatus

    def setSecondAvatarGiving(self, giving):
        self.secondAvatarGiving = giving

    def d_setSecondAvatarGiving(self, giving):
        self.sendUpdate('setSecondAvatarGiving', [giving])

    def b_setSecondAvatarGiving(self, giving):
        self.setSecondAvatarGiving(giving)
        self.d_setSecondAvatarGiving(giving)

    def getSecondAvatarGiving(self):
        return self.secondAvatarGiving

    def hasAvatar(self, avatarId):
        return bool(avatarId) and avatarId in (self.firstAvatarId, self.secondAvatarId)

    def isTradableType(self, stackType):
        if stackType == InventoryType.GoldInPocket:
            return True

        if not InventoryId.isStackable(stackType):
            return False

        # only items that exist within the economy may change hands, this
        # excludes reputation, skills, skill points and training tokens. The
        # ammo capacity a pouch gave stays with it's buyer, so a pouch could
        # be traded away and bought again for more capacity...
        itemCategory = EconomyGlobals.getItemCategory(stackType)
        return itemCategory is not None and itemCategory not in (ItemType.SHIP, ItemType.POUCH)

    def collapseGiving(self, giving):
        # the client appends a new slot every time an item is offered,
        # e.g. TradePanel.addGold adds a single gold piece at a time...
        totals = {}
        order = []
        for stackType, quantity in giving:
            if stackType not in totals:
                order.append(stackType)
                totals[stackType] = 0

            totals[stackType] += quantity

        return [[stackType, totals[stackType]] for stackType in order]

    def validateGiving(self, avatar, giving):
        inventory = avatar.getInventory() if avatar else None
        if not inventory:
            return RejectCode.NO_INVENTORY

        for stackType, quantity in giving:
            if quantity <= 0 or not self.isTradableType(stackType):
                return RejectCode.CONTENT_TYPE_NOT_ALLOWED

            if inventory.getStackQuantity(stackType) < quantity:
                return RejectCode.HAS_NONE_OF_THAT_TYPE

        return 0

    def validateReceiving(self, avatar, receiving, giving):
        inventory = avatar.getInventory() if avatar else None
        if not inventory:
            return RejectCode.NO_INVENTORY

        given = dict((stackType, quantity) for stackType, quantity in giving)
        for stackType, quantity in receiving:
            remaining = inventory.getStackQuantity(stackType) - given.get(stackType, 0)
            if remaining + quantity > inventory.getStackLimit(stackType):
                return RejectCode.OVERFLOW

        return 0

    def requestChangeGiving(self, giving):
        avatarId = self.air.getAvatarIdFromSender()
        if not self.hasAvatar(avatarId):
            self.air.logPotentialHacker(
                message='Received requestChangeGiving from an avatar not in the trade!',
                avatarId=avatarId,
                tradeId=self.doId)

            return

        if self.finished:
            self.d_rejectChangeGiving(avatarId, RejectCode.TRADE_NOT_ACTIVE)
            return

        giving = self.collapseGiving(giving)
        reason = self.validateGiving(self.air.doId2do.get(avatarId), giving)
        if reason:
            self.d_rejectChangeGiving(avatarId, reason)
            return

        if avatarId == self.firstAvatarId:
            self.b_setFirstAvatarGiving(giving)
        else:
            self.b_setSecondAvatarGiving(giving)

        # the offer has changed, both avatars must approve the trade again...
        self.b_setFirstAvatarStatus(self.STATUS_NOT_READY)
        self.b_setSecondAvatarStatus(self.STATUS_NOT_READY)

    def d_rejectChangeGiving(self, avatarId, reason):
        self.sendUpdateToAvatarId(avatarId, 'rejectChangeGiving', [reason])

    def requestChangeStatus(self, status):
        avatarId = self.air.getAvatarIdFromSender()
        if not self.hasAvatar(avatarId):
            self.air.logPotentialHacker(
                message='Received requestChangeStatus from an avatar not in the trade!',
                avatarId=avatarId,
                tradeId=self.doId)

            return

        if self.finished:
            self.d_rejectChangeStatus(avatarId, RejectCode.TRADE_NOT_ACTIVE)
            return

        status = self.STATUS_READY if status else self.STATUS_NOT_READY
        if avatarId == self.firstAvatarId:
            self.b_setFirstAvatarStatus(status)
        else:
            self.b_setSecondAvatarStatus(status)

        if self.firstAvatarStatus and self.secondAvatarStatus:
            self.completeTrade()

    def d_rejectChangeStatus(self, avatarId, reason):
        self.sendUpdateToAvatarId(avatarId, 'rejectChangeStatus', [reason])

    def requestRemoveTrade(self):
        avatarId = self.air.getAvatarIdFromSender()
        if not self.hasAvatar(avatarId):
            self.d_rejectRemoveTrade(avatarId, RejectCode.NOT_YOUR_TRADE)
            return

        self.cancelTrade()

    def d_rejectRemoveTrade(self, avatarId, reason):
        self.sendUpdateToAvatarId(avatarId, 'rejectRemoveTrade', [reason])

    def handleAvatarExit(self, avatarId):
        self.notify.debug('Avatar %d left during trade %d, canceling trade.' % (avatarId, self.doId))
        self.cancelTrade()

    def sendToAvatars(self, fieldName):
        for avatarId in (self.firstAvatarId, self.secondAvatarId):
            if avatarId in self.air.doId2do:
                self.sendUpdateToAvatarId(avatarId, fieldName, [])

    def d_tradeCanceled(self):
        self.sendToAvatars('tradeCanceled')

    def d_tradeFailed(self):
        self.sendToAvatars('tradeFailed')

    def d_tradeCompleted(self):
        self.sendToAvatars('tradeCompleted')

    def cancelTrade(self):
        if self.finished:
            return

        self.finished = True
        self.d_tradeCanceled()
        self.air.tradeMgr.removeTrade(self.doId)

    def failTrade(self):
        if self.finished:
            return

        self.finished = True
        self.d_tradeFailed()
        self.air.tradeMgr.removeTrade(self.doId)

    def completeTrade(self):
        firstAvatar = self.air.doId2do.get(self.firstAvatarId)
        secondAvatar = self.air.doId2do.get(self.secondAvatarId)
        if not firstAvatar or not secondAvatar:
            self.failTrade()
            return

        # validate both offers once more, the inventories may have changed
        # since the items were offered...
        if (self.validateGiving(firstAvatar, self.firstAvatarGiving) or
                self.validateGiving(secondAvatar, self.secondAvatarGiving) or
                self.validateReceiving(firstAvatar, self.secondAvatarGiving, self.firstAvatarGiving) or
                self.validateReceiving(secondAvatar, self.firstAvatarGiving, self.secondAvatarGiving)):
            self.notify.debug('Trade %d failed validation upon completion!' % self.doId)
            self.failTrade()
            return

        firstInventory = firstAvatar.getInventory()
        secondInventory = secondAvatar.getInventory()
        for stackType, quantity in self.firstAvatarGiving:
            firstInventory.b_setStackQuantity(stackType, firstInventory.getStackQuantity(stackType) - quantity)

        for stackType, quantity in self.secondAvatarGiving:
            secondInventory.b_setStackQuantity(stackType, secondInventory.getStackQuantity(stackType) - quantity)

        for stackType, quantity in self.secondAvatarGiving:
            self.giveStack(firstAvatar, stackType, quantity)

        for stackType, quantity in self.firstAvatarGiving:
            self.giveStack(secondAvatar, stackType, quantity)

        self.air.writeServerEvent('trade-completed',
            firstAvatarId=self.firstAvatarId,
            firstAvatarGiving=self.firstAvatarGiving,
            secondAvatarId=self.secondAvatarId,
            secondAvatarGiving=self.secondAvatarGiving)

        self.finished = True
        self.d_tradeCompleted()
        self.air.tradeMgr.removeTrade(self.doId)
