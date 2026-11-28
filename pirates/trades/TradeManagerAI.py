from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from otp.distributed.OtpDoGlobals import *
from otp.uberdog.RejectCode import RejectCode

from pirates.trades.TradeAI import LocalTrade, TradeAI


class TradeManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TradeManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.__trades = {}
        self.__tradeZones = {}

    def hasTrade(self, tradeId):
        return tradeId in self.__trades

    def createTrade(self, firstAvatarId=0, secondAvatarId=0):
        if not secondAvatarId:
            # local trades are used by the AI to reward an avatar (quests, treasure etc.)
            # they are never distributed and do not block or get blocked by player trades...
            trade = LocalTrade(self.air)
            trade.setAvatarId(firstAvatarId)
            return trade

        if not firstAvatarId:
            return None

        if self.getTradeFromAvatar(firstAvatarId, secondAvatarId) is not None:
            self.notify.warning('Cannot create new trade object, firstAvatarId=%d, secondAvatarId=%d; '
                'avatar already has an active trade object!' % (firstAvatarId, secondAvatarId))

            return None

        # the client opens interest on the trade's zone underneath the trade manager,
        # see TradeManager.createTradeResponse...
        zoneId = self.air.allocateZone()
        trade = TradeAI(self.air)
        trade.setFirstAvatarId(firstAvatarId)
        trade.setSecondAvatarId(secondAvatarId)
        trade.generateWithRequiredAndId(self.air.allocateChannel(), self.doId, zoneId)
        self.__trades[trade.doId] = trade
        self.__tradeZones[trade.doId] = zoneId
        return trade

    def removeTrade(self, tradeId):
        trade = self.__trades.get(tradeId)
        if not trade:
            self.notify.warning('Cannot remove trade: %d, trade object does not exist!' % tradeId)
            return

        del self.__trades[tradeId]
        zoneId = self.__tradeZones.pop(tradeId, None)
        trade.requestDelete()
        if zoneId is not None:
            self.air.deallocateZone(zoneId)

        del trade

    def getTrade(self, tradeId):
        return self.__trades.get(tradeId)

    def getTradeFromAvatar(self, firstAvatarId=0, secondAvatarId=0):
        for tradeId, trade in list(self.__trades.items()):
            for avatarId in (firstAvatarId, secondAvatarId):
                if avatarId and trade.hasAvatar(avatarId):
                    return trade

        return None

    def requestCreateTrade(self, otherAvatarId):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.notify.warning('Received requestCreateTrade from non-existant avatar %d!' % avatarId)
            return

        if avatarId == otherAvatarId:
            self.d_rejectCreateTrade(avatarId, otherAvatarId, RejectCode.NO_SELF_TRADE)
            return

        otherAvatar = self.air.doId2do.get(otherAvatarId)
        if not otherAvatar or not hasattr(otherAvatar, 'getInventory'):
            self.d_rejectCreateTrade(avatarId, otherAvatarId, RejectCode.OTHER_AVATAR_NOT_HERE)
            return

        if self.getTradeFromAvatar(avatarId) is not None:
            self.d_rejectCreateTrade(avatarId, otherAvatarId, RejectCode.MAY_NOT_TRADE)
            return

        if self.getTradeFromAvatar(otherAvatarId) is not None:
            self.d_rejectCreateTrade(avatarId, otherAvatarId, RejectCode.OTHER_AVATAR_MAY_NOT_TRADE)
            return

        trade = self.createTrade(avatarId, otherAvatarId)
        if not trade:
            self.d_rejectCreateTrade(avatarId, otherAvatarId, RejectCode.BUSY)
            return

        zoneId = self.__tradeZones[trade.doId]
        self.d_createTradeResponse(avatarId, otherAvatarId, zoneId)
        self.d_createTradeResponse(otherAvatarId, avatarId, zoneId)

    def d_rejectCreateTrade(self, avatarId, otherAvatarId, reasonCode):
        self.sendUpdateToAvatarId(avatarId, 'rejectCreateTrade', [otherAvatarId, reasonCode])

    def d_createTradeResponse(self, avatarId, otherAvatarId, tradeZoneId):
        self.sendUpdateToAvatarId(avatarId, 'createTradeResponse', [otherAvatarId, tradeZoneId])
