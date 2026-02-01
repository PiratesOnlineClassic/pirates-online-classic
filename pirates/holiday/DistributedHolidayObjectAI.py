from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.ai import HolidayGlobals

class DistributedHolidayObjectAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractiveAI')

    INTERACT_NONE = 0
    INTERACT_ALL = 1
    INTERACT_GM = 2

    INTERACT_MODES = {
        'None': INTERACT_NONE,
        'All': INTERACT_ALL,
        'GM': INTERACT_GM,
    }

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.holiday = None
        self.interactRadius = 0
        self.interactMode = self.INTERACT_NONE
        self.activeInteractMode = self.INTERACT_NONE

    def announceGenerate(self):
        DistributedInteractiveAI.announceGenerate(self)

        self.accept('HolidayStarted', self.serverHolidayStart)
        self.accept('HolidayEnd', self.serverHolidayEnd)

    def delete(self):
        DistributedInteractiveAI.delete(self)

        self.ignore('HolidayStarted')
        self.ignore('HolidayEnded')

    def setHoliday(self, holiday):
        self.holiday = holiday

    def getHoliday(self, holiday):
        return self.holiday

    def isObjectActive(self):
        return self.interactMode != self.INTERACT_NONE

    def isHolidayActive(self):
        if not self.holiday:
            return False

        for holidayId, name in list(HolidayGlobals.holidayNames.items()):
            if name == self.holiday:
                return self.air.newsManager.isHolidayActive(holidayId)

        return False

    def serverHolidayStart(self, holidayId):
        if self.isObjectActive():
            return

        if self.isHolidayActive():
            interactMode = self.INTERACT_MODES.get(self.activeInteractMode, 'None')  
            self.b_setInteractMode(interactMode)
            self.holidayStart()
            
    def holidayStart(self):
        # Overriden by child objects to process holiday start events
        pass

    def serverHolidayEnd(self, holidayId):
        if not self.isObjectActive():
            return

        if self.isHolidayActive():
            self.b_setInteractMode(self.DENY_INTERACT)
            self.holidayEnd()

    def holidayEnd(self):
        # Overriden by child objects to process holiday end events
        pass

    def setInteractRadius(self, radius):
        self.interactRadius = radius

    def d_setInteractRadius(self, radius):
        self.sendUpdate('setInteractRadius', [radius])
    
    def b_setInteractRadius(self, radius):
        self.setInteractRadius(radius)
        self.d_setInteractRadius(radius)

    def getInteractRadius(self):
        return self.interactRadius

    def setInteractMode(self, mode):
        self.interactMode = mode 

    def d_setInteractMode(self, mode):
        self.sendUpdate('setInteractMode', [mode])

    def b_setInteractMode(self, mode):
        self.setInteractMode(mode)
        self.d_setInteractMode(mode)

    def getInteractMode(self):
        return self.interactMode

    def setActiveInteractMode(self, mode):
        self.activeInteractMode = mode

    def getActiveInteractMode(self, mode):
        return self.activeInteractMode

    def handleHolidayInteract(self, avatar, interactType, instant):
        self.notify.warning('%s does not implement handleHolidayInteract' % self.__class__.__name__)
        return self.DENY

    def handleRequestInteraction(self, avatar, interactType, instant):
        
        # Verify we are in an interactable state
        if self.interactMode == self.INTERACT_NONE:
            self.notify.warning('Attempted to interact with an uninteractable holiday object')
            return self.DENY

        canInteract = False
        if self.interactMode == self.INTERACT_ALL:
            canInteract = True
        elif self.interactMode == self.INTERACT_GM and avatar.getAllowGMNameTag():
            canInteract = True

        if canInteract:
            return self.handleHolidayInteract(avatar, interactType, instant)