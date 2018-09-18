from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory


class TradeBase(object):

    def giveStack(self, avatar, stackType, quantity):
        inventory = avatar.getInventory()
        if not inventory:
            self.notify.warning('Failed to give stackType: %d for avatar %d, '
                'avatar has no inventory!' % (stackType, avatar.doId))

            return

        currentQuantity = inventory.getStackQuantity(stackType)
        inventory.b_setStackQuantity(stackType, currentQuantity + quantity)


class LocalTrade(TradeBase):

    def __init__(self, air):
        self.air = air

        self.avatarId = 0
        self.avatar = None

    def setAvatarId(self, avatarId):
        self.avatarId = avatarId
        self.avatar = self.air.doId2do.get(self.avatarId)

    def getAvatarId(self):
        return self.avatarId

    def giveStack(self, stackType, quantity):
        TradeBase.giveStack(self, self.avatar, stackType, quantity)

    def giveReputation(self, reputationType, reputation):
        inventory = self.avatar.getInventory()
        if not inventory:
            self.notify.warning('Failed to give reputationType: %d for avatar %d, '
                'avatar has no inventory!' % (reputationType, self.avatar.doId))

            return

        currentReputation = inventory.getReputation(reputationType)
        inventory.setReputation(reputationType, currentReputation + reputation)

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

    def giveWeaponMessage(self, weapon):
        self.avatar.d_sendWeaponMessage(weapon)

    def giveJewelryMessage(self, jewelryUID):
        self.avatar.d_sendJewelryMessage(jewelryUID)

    def giveTattooMessage(self, tattooUID):
        self.avatar.d_sendTattooMessage(tattooUID)

    def giveClothingMessage(self, dropId, colorId):
        self.avatar.d_sendClothingMessage(dropId, colorId)


class TradeAI(DistributedObjectAI, TradeBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('TradeAI')

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

    def setFirstAvatarId(self, avatarId):
        self.firstAvatarId = avatarId
        self.firstAvatar = self.air.doId2do.get(self.firstAvatarId)

    def getFirstAvatarId(self):
        return self.firstAvatarId

    def setFirstAvatarStatus(self, avatarStatus):
        self.firstAvatarStatus = avatarStatus

    def getFirstAvatarStatus(self):
        return self.firstAvatarStatus

    def setFirstAvatarGiving(self, giving):
        self.firstAvatarGiving = giving

    def getFirstAvatarGiving(self):
        return self.firstAvatarGiving

    def setSecondAvatarId(self, avatarId):
        self.secondAvatarId = avatarId
        self.secondAvatar = self.air.doId2do.get(self.secondAvatarId)

    def getSecondAvatarId(self):
        return self.secondAvatarId

    def setSecondAvatarStatus(self, avatarStatus):
        self.secondAvatarStatus = avatarStatus

    def getSecondAvatarStatus(self):
        return self.secondAvatarStatus

    def setSecondAvatarGiving(self, giving):
        self.secondAvatarGiving = giving

    def getSecondAvatarGiving(self):
        return self.secondAvatarGiving
