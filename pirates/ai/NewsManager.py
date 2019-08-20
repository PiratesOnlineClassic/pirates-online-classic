from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.task import Task
from pirates.ai import HolidayGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.economy import StoreGUI, AccessoriesStoreGUI, TattooStoreGUI, JewelryStoreGUI, BarberStoreGUI
from pirates.chat.PChatInputSpeedChat import PChatInputSpeedChat
from pirates.piratesgui import PiratesGuiGlobals
from pirates.makeapirate import TattooGlobals
from pirates.makeapirate import ClothingGlobals
from pirates.makeapirate import JewelryGlobals
from pirates.makeapirate import BarberGlobals
from pirates.piratesbase import Freebooter
import time
messages = {
    0: PLocalizer.FullMoonWarning1,
    1: PLocalizer.FullMoonWarning2,
    2: PLocalizer.JollyRogerCurseComing,
    3: PLocalizer.JollyRogerCurseActive,
    4: PLocalizer.JollyRogerCurseIndoors,
    5: PLocalizer.JollyRogerCurseOutdoors,
    6: PLocalizer.JollyRogerCurseJail,
    7: PLocalizer.JollyRogerCurseEnd}

class NewsManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('NewsManager')
    neverDisable = 1
    
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.holidayIdList = []
        self.holidayEndTimes = {}
        base.cr.newsManager = self
    
    def delete(self):
        for holidayId in HolidayGlobals.holidays.keys():
            taskMgr.remove('showHolidayMessage-holidayId:' + str(holidayId))
        
        self.cr.newsManager = None
        DistributedObject.DistributedObject.delete(self)
    
    def displayMessage(self, messageId):
        message = messages.get(messageId)
        if self.inNewsWorld() and not self.inTutorial(level = PiratesGlobals.TUT_GOT_COMPASS):
            base.localAvatar.guiMgr.messageStack.addModalTextMessage(message, seconds = 45, priority = 0, color = PiratesGuiGlobals.TextFG14, icon = ('admin', ''), suffix = '_f')
            base.chatAssistant.receiveGameMessage(message)

    def showHolidayMessage(self, holidayId, msgType):
        self.notify.debug('showHolidayMessage-holidayId:' + str(holidayId))
        taskMgr.remove('showHolidayMessage-holidayId:' + str(holidayId))
        if not hasattr(base, 'localAvatar'):
            return
        
        if base.localAvatar.getTutorialState() == 0 or self.inNewsWorld() == None:
            taskMgr.doMethodLater(15, self.showHolidayMessage, 'showHolidayMessage-holidayId:' + str(holidayId), extraArgs = [holidayId, msgType])
            return
        
        if msgType == 1:
            (hours, minutes) = self.getTimeRemaining(holidayId)
            message = HolidayGlobals.getHolidayStartMsg(holidayId, base.cr.isPaid())
            chatMessage = HolidayGlobals.getHolidayStartChatMsg(holidayId, base.cr.isPaid())
        elif msgType == 0:
            message = HolidayGlobals.getHolidayEndMsg(holidayId, base.cr.isPaid())
            chatMessage = HolidayGlobals.getHolidayEndChatMsg(holidayId, base.cr.isPaid())

        timeRemaining = self.getTimeRemaining(holidayId)
        formatting = {
            'hours': max(timeRemaining[0], 0),
            'minutes': max(timeRemaining[1], 0)
        }
        
        if message:
            message = message % formatting
        
        if chatMessage:
            chatMessage = chatMessage % formatting
        
        if self.inNewsWorld() and not self.inTutorial(level = PiratesGlobals.TUT_GOT_COMPASS):
            if message:
                base.localAvatar.guiMgr.messageStack.addModalTextMessage(message, seconds = 45, priority = 0, color = PiratesGuiGlobals.TextFG14, icon = (HolidayGlobals.getHolidayIcon(holidayId), ''), suffix = '_f')
            
            if chatMessage:
                base.chatAssistant.receiveGameMessage(chatMessage)

    def startHoliday(self, holidayId):
        if holidayId not in self.holidayIdList:
            self.notify.debug('setHolidayId: Starting Holiday %s' % holidayId)
            self.holidayIdList.append(holidayId)
            base.setHoliday(holidayId, 1)
            AccessoriesStoreGUI.AccessoriesStoreGUI.holidayIdList.append(holidayId)
            JewelryStoreGUI.JewelryStoreGUI.holidayIdList.append(holidayId)
            BarberStoreGUI.BarberStoreGUI.holidayIdList.append(holidayId)
            TattooStoreGUI.TattooStoreGUI.holidayIdList.append(holidayId)
            if holidayId == PiratesGlobals.FLIRTEMOTE:
                emoteId = PLocalizer.EMOTE_VALENTINES
                localAvatar.chatMgr.speedEntry.addEmote(emoteId)
            
            PChatInputSpeedChat.holidayIdList.append(holidayId)
            self.showHolidayMessage(holidayId, 1)
            if holidayId == PiratesGlobals.HALFOFFCUSTOMIZATION:
                if base.cr.isPaid() == 2:
                    self.divideAllAccessories(2)

            if holidayId == PiratesGlobals.ALLACCESSWEEKEND:
                Freebooter.AllAccessHoliday = True
                if localAvatar.guiMgr.prevTag:
                    localAvatar.guiMgr.prevTag.hide()

            if holidayId == PiratesGlobals.FOURTHOFJULY:
                base.fourthOfJuly = True

            if holidayId == PiratesGlobals.SAINTPATRICKSDAY:
                base.saintPatricksDay = True

            messenger.send('HolidayStarted', [HolidayGlobals.getHolidayName(holidayId)])

    def endHoliday(self, holidayId):
        if holidayId in self.holidayIdList:
            self.notify.debug('setHolidayId: Ending Holiday %s' % holidayId)
            self.holidayIdList.remove(holidayId)
            base.setHoliday(holidayId, 0)
            AccessoriesStoreGUI.AccessoriesStoreGUI.holidayIdList.remove(holidayId)
            JewelryStoreGUI.JewelryStoreGUI.holidayIdList.remove(holidayId)
            BarberStoreGUI.BarberStoreGUI.holidayIdList.remove(holidayId)
            TattooStoreGUI.TattooStoreGUI.holidayIdList.remove(holidayId)
            PChatInputSpeedChat.holidayIdList.remove(holidayId)
            self.showHolidayMessage(holidayId, 0)
            if holidayId == PiratesGlobals.HALFOFFCUSTOMIZATION:
                self.endHalfOffCustomizationHoliday()
                if base.cr.isPaid() == 2:
                    self.multiplyAllAccessories(2)

            if holidayId == PiratesGlobals.ALLACCESSWEEKEND:
                Freebooter.AllAccessHoliday = False
            
            if holidayId == PiratesGlobals.FOURTHOFJULY:
                base.fourthOfJuly = False

            if holidayId == PiratesGlobals.SAINTPATRICKSDAY:
                base.saintPatricksDay = False

            messenger.send('HolidayEnded', [HolidayGlobals.getHolidayName(holidayId)])

    def setHolidayIdList(self, holidayIdArray):
        holidayIdList = []
        for hid in holidayIdArray:
            if hid[0] != None:
                holidayIdList.append(hid[0])
            
            self.holidayEndTimes[hid[0]] = hid[1]

        def isEnding(id):
            return id not in holidayIdList

        def isStarting(id):
            return id not in self.holidayIdList

        toEnd = filter(isEnding, self.holidayIdList)
        for endingHolidayId in toEnd:
            self.endHoliday(endingHolidayId)
        
        toStart = filter(isStarting, holidayIdList)
        for startingHolidayId in toStart:
            self.startHoliday(startingHolidayId)
        
        messenger.send('setHolidayIdList', [holidayIdList])
    
    def getHolidayIdList(self):
        return self.holidayIdList

    def holidayNotify(self):
        pass

    def inTutorial(self, level = PiratesGlobals.TUT_CHAPTER3_STARTED):
        if base.localAvatar.getTutorialState() <= level:
            return True
        else:
            return False

    def inNewsWorld(self):
        w = base.localAvatar.getWorld()
        if not w:
            return None
        
        ourInstance = w.type
        if ourInstance == None:
            return None
        
        for iType in PiratesGlobals.INSTANCE_NO_NEWS_MESSAGES:
            if ourInstance == iType:
                return False
        
        return True

    def getTimeRemaining(self, holidayId):
        t = self.holidayEndTimes.get(holidayId, -1)
        if t == -1:
            return [0, 0]
        
        t = int(t)
        epochNow = int(time.time())
        epochRemain = t - epochNow
        (minutes, seconds) = divmod(epochRemain, 60)
        (hours, minutes) = divmod(minutes, 60)
        return [
            hours,
            minutes]

    def displayHolidayStatus(self):
        if not self.holidayIdList:
            base.chatAssistant.receiveGameMessage(PLocalizer.NO_CURRENT_HOLIDAYS)
            return
        
        for holidayId in self.holidayIdList:
            (h, m) = self.getTimeRemaining(holidayId)
            message = HolidayGlobals.getHolidayStatusMsg(holidayId)
            if message:
                base.chatAssistant.receiveGameMessage(message % (h, m))

    def divideTattooPrices(self, divisor):
        for (k, v) in TattooGlobals.tattoos.iteritems():
            currentPrice = v[4]
            newPrice = int(currentPrice / divisor)
            TattooGlobals.tattoos[k][4] = newPrice

    def divideClothingPrices(self, divisor):
        for (k, v) in ClothingGlobals.UNIQUE_ID.iteritems():
            currentPrice = v[5]
            newPrice = int(currentPrice / divisor)
            ClothingGlobals.UNIQUE_ID[k][5] = newPrice

    def divideJewelryPrices(self, divisor):
        for (k, v) in JewelryGlobals.jewelry_id.iteritems():
            currentPrice = v[3]
            newPrice = int(currentPrice / divisor)
            JewelryGlobals.jewelry_id[k][3] = newPrice

    def divideBarberPrices(self, divisor):
        for (k, v) in BarberGlobals.barber_id.iteritems():
            currentPrice = v[4]
            newPrice = int(currentPrice / divisor)
            BarberGlobals.barber_id[k][4] = newPrice

    def multiplyTattooPrices(self, factor):
        for (k, v) in TattooGlobals.tattoos.iteritems():
            currentPrice = v[4]
            newPrice = int(currentPrice * factor)
            TattooGlobals.tattoos[k][4] = newPrice

    def multiplyClothingPrices(self, factor):
        for (k, v) in ClothingGlobals.UNIQUE_ID.iteritems():
            currentPrice = v[5]
            newPrice = int(currentPrice * factor)
            ClothingGlobals.UNIQUE_ID[k][5] = newPrice

    def multiplyJewelryPrices(self, factor):
        for (k, v) in JewelryGlobals.jewelry_id.iteritems():
            currentPrice = v[3]
            newPrice = int(currentPrice * factor)
            JewelryGlobals.jewelry_id[k][3] = newPrice

    def multiplyBarberPrices(self, factor):
        for (k, v) in BarberGlobals.barber_id.iteritems():
            currentPrice = v[4]
            newPrice = int(currentPrice * factor)
            BarberGlobals.barber_id[k][4] = newPrice

    def divideAllAccessories(self, divisor):
        self.divideTattooPrices(divisor)
        self.divideClothingPrices(divisor)
        self.divideJewelryPrices(divisor)
        self.divideBarberPrices(divisor)

    def multiplyAllAccessories(self, factor):
        self.multiplyTattooPrices(factor)
        self.multiplyClothingPrices(factor)
        self.multiplyJewelryPrices(factor)
        self.multiplyBarberPrices(factor)


