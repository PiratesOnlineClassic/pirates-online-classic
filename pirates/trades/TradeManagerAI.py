from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from otp.distributed.OtpDoGlobals import *

from pirates.trades.TradeAI import LocalTrade, TradeAI


class TradeManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TradeManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.__trades = {}

    def hasTrade(self, tradeId):
        return tradeId in self.__trades

    def createTrade(self, firstAvatarId=0, secondAvatarId=0):
        trade = self.getTradeFromAvatar(firstAvatarId, secondAvatarId)
        if trade is not None:
            self.notify.warning('Cannot create new trade object, firstAvatarId=%d, secondAvatarId=%d; '
                'avatar already has an active trade object!' % (firstAvatarId, secondAvatarId))

            return

        if firstAvatarId and secondAvatarId:
            trade = TradeAI(self.air)
            trade.setFirstAvatarId(firstAvatarId)
            trade.setSecondAvatarId(secondAvatarId)
            trade.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)
            self.__trades[trade.doId] = trade
        else:
            trade = LocalTrade(self.air)
            trade.setAvatarId(firstAvatarId)

        return trade

    def removeTrade(self, tradeId):
        trade = self.__trades.get(tradeId)
        if not trade:
            self.notify.warning('Cannot remove trade: %d, trade object does not exist!' % tradeId)
            return

        del self.__trades[tradeId]
        trade.requestDelete()
        del trade

    def getTrade(self, tradeId):
        return self.__trades.get(tradeId)

    def getTradeFromAvatar(self, firstAvatarId=0, secondAvatarId=0):
        for tradeId, trade in list(self.__trades.items()):
            if trade.getFirstAvatarId() == firstAvatarId or trade.getSecondAvatarId() == secondAvatarId:
                return trade

        return None
