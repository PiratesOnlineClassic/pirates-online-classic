from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesgui import PiratesConfirm
from pirates.piratesgui import PiratesInfo
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import CrewMatchInvitee
from pirates.piratesgui import PiratesGuiGlobals
PVP_ISLAND_ONE = '1196970080.56sdnaik'
PVP_ISLAND_TWO = '1196970035.53sdnaik'
PVP_ISLAND_LIST = [
    PVP_ISLAND_ONE,
    PVP_ISLAND_TWO]

class DistributedCrewMatch(DistributedObject):
    notify = directNotify.newCategory('DistributedCrewMatch')
    
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.offerRequestCache = []
        self.offerCurrentlyOnScreen = False
        self.crewType = 1
    
    def generate(self):
        DistributedObject.generate(self)
        base.cr.pirateCrewMatch = self

    def disable(self):
        DistributedObject.disable(self)
        base.cr.pirateCrewMatch = None
    
    def addCrewToLookoutList(self, range, sailValue, cannonValue):
        self.sendUpdate('requestCrewAdd', [
            range,
            sailValue,
            cannonValue])
        if localAvatar.getCurrentIsland() in PVP_ISLAND_LIST:
            self.stackMessage(PLocalizer.CrewMatchEnabledForCrewPVP)
        else:
            self.stackMessage(PLocalizer.CrewMatchEnabledForCrew)
    
    def deleteCrewFromLookoutList(self):
        self.sendUpdate('requestCrewDelete', [])

    def responseCrewAdd(self, responseCode):
        self.notify.debug('responseCrewAdd(%s)' % responseCode)

    def responseCrewDelete(self, response):
        self.notify.debug('responseCrewDelete(%s)' % response)
    
    def addAvatarToLookoutList(self, crewType):
        self.crewType = crewType
        self.sendUpdate('requestInitialAvatarAdd', [crewType])
    
    def responseInitialAvatarAdd(self, response, submitterName, location, crewType):
        self.notify.debug('responseInitialAvatarAdd(%s, %s, %s)' % (response, submitterName, location))
        self.availableCrewSubmitterName = submitterName
        if response:
            confirmBox = CrewMatchInvitee.CrewMatchInvitee(localAvatar.getDoId(), submitterName, location, True, crewType)
        else:
            if crewType == 1:
                self.stackMessage(PLocalizer.CrewMatchNoCrewFound)
            elif crewType == 2:
                self.stackMessage(PLocalizer.CrewMatchNoCrewFoundPVP)
        
            self.putAvatarOnLookoutList(crewType)
    
    def acceptInitialInviteGUI(self):
        self.sendUpdate('requestInitialAvatarAddResponse', [1, self.crewType])

    def putAvatarOnLookoutList(self, crewType):
        self.sendUpdate('requestPutAvatarOnLookoutList', [crewType])

    def deleteAvatarFromLookoutList(self):
        if self.crewType == 1:
            self.stackMessage(PLocalizer.CrewMatchRemoveAvatarFromLookout)
        elif self.crewType == 2:
            self.stackMessage(PLocalizer.CrewMatchRemoveAvatarFromLookoutPVP)
        
        self.sendUpdate('requestdeleteAvatarFromLookoutList', [])

    def responseCrewFound(self, sponsorName, crewOwnAvId, location):
        if not self.offerCurrentlyOnScreen:
            self.offerCurrentlyOnScreen = True
            self.availableCrew = crewOwnAvId
            self.notify.debug('responseCrewFound(%s, %s, %s)' % (sponsorName, crewOwnAvId, location))
            confirmBox = CrewMatchInvitee.CrewMatchInvitee(localAvatar.getDoId(), sponsorName, location, False)
        else:
            self.offerRequestCache.append([
                sponsorName,
                crewOwnAvId,
                location])

    def acceptInvite(self):
        self.sendUpdate('requestAcceptInvite', [self.availableCrew])

    def initialAvatarAddResponse(self, response):
        self.sendUpdate('requestInitialAvatarAddResponse', [response, self.crewType])
    
    def responseInitialAvatarAddResponse(self, response):
        self.notify.debug('responseInitialAvatarAddResponse(%s)' % response)
        if response == 0:
            self.stackMessage(PLocalizer.CrewMatchCrewNowUnavailable)
            self.offerCurrentlyOnScreen = False
            self.checkOfferCache()

    def checkOfferCache(self):
        if self.offerRequestCache:
            (sponsorName, crewOwnAvId, location) = self.offerRequestCache.pop()
            self.responseCrewFound(sponsorName, crewOwnAvId, location)
    
    def stackMessage(self, msg):
        base.localAvatar.guiMgr.messageStack.addTextMessage(msg, seconds = 15, priority = 0, color = PiratesGuiGlobals.TextFG14, suffix = '_f', icon = ('friends', ''))

    def requestCrewOfOne(self):
        self.sendUpdate('requestCrewOfOneCreation', [])
    
    def requestDeleteCrewOfOne(self):
        self.sendUpdate('requestCrewOfOneDelete', [])
    
    def notifySponsorNewMember(self, avName):
        self.stackMessage(PLocalizer.CrewMatchAvatarAddedToYourCrew % avName)

