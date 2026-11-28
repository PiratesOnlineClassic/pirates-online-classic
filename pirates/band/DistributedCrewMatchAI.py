from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from pirates.reputation import ReputationGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

PVP_ISLAND_ONE = '1196970080.56sdnaik'
PVP_ISLAND_TWO = '1196970035.53sdnaik'
PVP_ISLAND_LIST = [
    PVP_ISLAND_ONE,
    PVP_ISLAND_TWO]


class CrewLookoutEntry:

    def __init__(self, avatarId, crewType, levelRange, sailLevel, cannonLevel):
        self.avatarId = avatarId
        self.crewType = crewType
        self.levelRange = levelRange
        self.sailLevel = sailLevel
        self.cannonLevel = cannonLevel


class DistributedCrewMatchAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCrewMatchAI')

    CREW_TYPE_NORMAL = 1
    CREW_TYPE_PVP = 2

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.crewLookout = {}
        self.avatarLookout = {}
        self.crewsOfOne = set()
        self.initialOffers = {}
        self.offers = {}

    def delete(self):
        self.ignoreAll()
        DistributedObjectAI.delete(self)

    # Helpers

    def getAvatarLevel(self, avatar, repType=InventoryType.OverallRep):
        inventory = avatar.getInventory()
        if not inventory:
            return avatar.getLevel()

        totalRep = inventory.getReputation(repType)
        level, _ = ReputationGlobals.getLevelFromTotalReputation(repType, totalRep)
        return level

    def getAvatarLocation(self, avatar):
        parentObj = avatar.getParentObj()
        if parentObj and hasattr(parentObj, 'getLocalizerName'):
            return parentObj.getLocalizerName()

        return ''

    def getAvatarCrewType(self, avatar):
        if avatar.getCurrentIsland() in PVP_ISLAND_LIST:
            return self.CREW_TYPE_PVP

        return self.CREW_TYPE_NORMAL

    def acceptAvatarDelete(self, avatar):
        self.accept(avatar.getDeleteEvent(), self.__handleAvatarDelete, [avatar.doId])

    def __handleAvatarDelete(self, avatarId):
        self.ignore('distObjDelete-%d' % avatarId)
        self.removeCrewFromLookout(avatarId)
        self.crewsOfOne.discard(avatarId)
        self.avatarLookout.pop(avatarId, None)
        self.initialOffers.pop(avatarId, None)
        self.offers.pop(avatarId, None)

    def canSponsorCrew(self, avatarId):
        """
        Returns True if the avatar is the captain of a crew or has
        started a crew of one, and that crew still has some room.
        """

        if avatarId in self.crewsOfOne:
            return True

        bandManager = self.air.bandManager
        band = bandManager.getBandFromAvatar(avatarId)
        return band is not None and band.managerId == avatarId and not band.isFull()

    def isCrewMatch(self, entry, avatar):
        sponsor = self.air.doId2do.get(entry.avatarId)
        if not sponsor:
            return False

        if not self.canSponsorCrew(entry.avatarId):
            return False

        sponsorLevel = self.getAvatarLevel(sponsor)
        avatarLevel = self.getAvatarLevel(avatar)
        if abs(sponsorLevel - avatarLevel) > entry.levelRange:
            return False

        if entry.sailLevel > 1 and self.getAvatarLevel(avatar, InventoryType.SailingRep) < entry.sailLevel:
            return False

        if entry.cannonLevel > 1 and self.getAvatarLevel(avatar, InventoryType.CannonRep) < entry.cannonLevel:
            return False

        return True

    def findCrewForAvatar(self, avatar, crewType):
        for entry in list(self.crewLookout.values()):
            if entry.crewType != crewType:
                continue

            if self.isCrewMatch(entry, avatar):
                return entry

        return None

    def addAvatarToCrew(self, sponsorId, avatarId):
        avatar = self.air.doId2do.get(avatarId)
        sponsor = self.air.doId2do.get(sponsorId)
        if not avatar or not sponsor:
            return False

        if not self.canSponsorCrew(sponsorId):
            return False

        if not self.air.bandManager.addAvatarToBand(sponsorId, avatar):
            return False

        # the crew of one has now become a real crew
        self.crewsOfOne.discard(sponsorId)
        self.avatarLookout.pop(avatarId, None)
        self.initialOffers.pop(avatarId, None)
        self.offers.pop(avatarId, None)

        self.d_notifySponsorNewMember(sponsorId, avatar.getName())
        return True

    def removeCrewFromLookout(self, avatarId):
        self.crewLookout.pop(avatarId, None)

    def offerCrewToAvatars(self, entry):
        sponsor = self.air.doId2do.get(entry.avatarId)
        if not sponsor:
            return

        location = self.getAvatarLocation(sponsor)
        for avatarId, crewType in list(self.avatarLookout.items()):
            if crewType != entry.crewType:
                continue

            avatar = self.air.doId2do.get(avatarId)
            if not avatar:
                del self.avatarLookout[avatarId]
                continue

            if self.air.bandManager.isAvatarInBand(avatar):
                del self.avatarLookout[avatarId]
                continue

            offers = self.offers.setdefault(avatarId, set())
            if entry.avatarId in offers:
                continue

            if not self.isCrewMatch(entry, avatar):
                continue

            offers.add(entry.avatarId)
            self.d_responseCrewFound(avatarId, sponsor.getName(), entry.avatarId, location)

    # Crew lookout

    def requestCrewAdd(self, levelRange, sailValue, cannonValue):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        if not self.canSponsorCrew(avatarId):
            self.d_responseCrewAdd(avatarId, 0)
            return

        entry = CrewLookoutEntry(avatarId, self.getAvatarCrewType(avatar), levelRange, sailValue, cannonValue)
        self.crewLookout[avatarId] = entry
        self.acceptAvatarDelete(avatar)
        self.d_responseCrewAdd(avatarId, 1)

        self.offerCrewToAvatars(entry)

    def d_responseCrewAdd(self, avatarId, responseCode):
        self.sendUpdateToAvatarId(avatarId, 'responseCrewAdd', [responseCode])

    def requestCrewDelete(self):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.crewLookout:
            self.d_responseCrewDelete(avatarId, 0)
            return

        self.removeCrewFromLookout(avatarId)
        self.d_responseCrewDelete(avatarId, 1)

    def d_responseCrewDelete(self, avatarId, response):
        self.sendUpdateToAvatarId(avatarId, 'responseCrewDelete', [response])

    def requestCrewOfOneCreation(self):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        if self.air.bandManager.isAvatarInBand(avatar):
            return

        self.crewsOfOne.add(avatarId)
        self.acceptAvatarDelete(avatar)

    def requestCrewOfOneDelete(self):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId not in self.crewsOfOne:
            return

        self.crewsOfOne.discard(avatarId)
        self.removeCrewFromLookout(avatarId)

    def d_notifySponsorNewMember(self, sponsorId, avatarName):
        self.sendUpdateToAvatarId(sponsorId, 'notifySponsorNewMember', [avatarName])

    # Avatar lookout

    def requestInitialAvatarAdd(self, crewType):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        if crewType not in (self.CREW_TYPE_NORMAL, self.CREW_TYPE_PVP):
            self.air.logPotentialHacker(
                message='Avatar requested an invalid crew match type!',
                crewType=crewType)

            return

        self.acceptAvatarDelete(avatar)
        entry = None
        if not self.air.bandManager.isAvatarInBand(avatar):
            entry = self.findCrewForAvatar(avatar, crewType)

        if not entry:
            self.d_responseInitialAvatarAdd(avatarId, 0, '', '', crewType)
            return

        sponsor = self.air.doId2do.get(entry.avatarId)
        self.initialOffers[avatarId] = entry.avatarId
        self.d_responseInitialAvatarAdd(avatarId, 1, sponsor.getName(),
            self.getAvatarLocation(sponsor), crewType)

    def d_responseInitialAvatarAdd(self, avatarId, response, submitterName, location, crewType):
        self.sendUpdateToAvatarId(avatarId, 'responseInitialAvatarAdd', [response, submitterName, location, crewType])

    def requestInitialAvatarAddResponse(self, response, crewType):
        avatarId = self.air.getAvatarIdFromSender()
        sponsorId = self.initialOffers.pop(avatarId, None)
        if not sponsorId or not response:
            return

        if not self.addAvatarToCrew(sponsorId, avatarId):
            self.d_responseInitialAvatarAddResponse(avatarId, 0)
            return

        self.d_responseInitialAvatarAddResponse(avatarId, 1)

    def d_responseInitialAvatarAddResponse(self, avatarId, response):
        self.sendUpdateToAvatarId(avatarId, 'responseInitialAvatarAddResponse', [response])

    def requestPutAvatarOnLookoutList(self, crewType):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        if crewType not in (self.CREW_TYPE_NORMAL, self.CREW_TYPE_PVP):
            self.air.logPotentialHacker(
                message='Avatar requested an invalid crew match type!',
                crewType=crewType)

            return

        if self.air.bandManager.isAvatarInBand(avatar):
            return

        # the avatar declined the initial offer, don't offer that crew again
        sponsorId = self.initialOffers.pop(avatarId, None)
        if sponsorId:
            self.offers.setdefault(avatarId, set()).add(sponsorId)

        self.avatarLookout[avatarId] = crewType
        self.acceptAvatarDelete(avatar)

    def requestdeleteAvatarFromLookoutList(self):
        avatarId = self.air.getAvatarIdFromSender()
        self.avatarLookout.pop(avatarId, None)
        self.offers.pop(avatarId, None)

    def d_responseCrewFound(self, avatarId, sponsorName, crewOwnAvId, location):
        self.sendUpdateToAvatarId(avatarId, 'responseCrewFound', [sponsorName, crewOwnAvId, location])

    def requestAcceptInvite(self, crewOwnAvId):
        avatarId = self.air.getAvatarIdFromSender()
        offers = self.offers.get(avatarId, set())
        if crewOwnAvId not in offers:
            self.air.logPotentialHacker(
                message='Avatar tried to accept a crew match invite they were never offered!',
                crewOwnAvId=crewOwnAvId)

            return

        offers.discard(crewOwnAvId)
        if not self.addAvatarToCrew(crewOwnAvId, avatarId):
            self.d_responseInitialAvatarAddResponse(avatarId, 0)
