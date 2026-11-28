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

        # crews which are looking for crew mates on another district
        # are described by the district the sponsor is on
        self.remote = False
        self.sponsorName = ''
        self.sponsorLevel = 0
        self.location = ''

    def getRemoteInfo(self):
        return [self.avatarId, self.crewType, self.levelRange, self.sailLevel, self.cannonLevel,
            self.sponsorName, self.sponsorLevel, self.location]

    @classmethod
    def makeFromRemoteInfo(cls, remoteInfo):
        avatarId, crewType, levelRange, sailLevel, cannonLevel, sponsorName, sponsorLevel, location = remoteInfo
        entry = cls(avatarId, crewType, levelRange, sailLevel, cannonLevel)
        entry.remote = True
        entry.sponsorName = sponsorName
        entry.sponsorLevel = sponsorLevel
        entry.location = location
        return entry


class DistributedCrewMatchAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCrewMatchAI')

    CREW_TYPE_NORMAL = 1
    CREW_TYPE_PVP = 2

    # The amount of time to wait for another district to add an
    # avatar to a crew on that district before giving up
    JOIN_TIMEOUT = 10.0

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.crewLookout = {}
        self.avatarLookout = {}
        self.crewsOfOne = set()
        self.initialOffers = {}
        self.offers = {}
        self.pendingJoins = {}

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        # the crew lookout is cross district, crews looking for crew mates are
        # shared with every district so avatars can be matched with them
        self.air.netMessenger.accept('crewMatchCrewAdd', self, self.handleRemoteCrewAdd)
        self.air.netMessenger.accept('crewMatchCrewRemove', self, self.handleRemoteCrewRemove)
        self.air.netMessenger.accept('crewMatchJoinRequest', self, self.handleJoinRequest)
        self.air.netMessenger.accept('crewMatchJoinResponse', self, self.handleJoinResponse)

    def delete(self):
        for avatarId, entry in list(self.crewLookout.items()):
            if not entry.remote:
                self.removeCrewFromLookout(avatarId)

        self.air.netMessenger.ignore('crewMatchCrewAdd', self)
        self.air.netMessenger.ignore('crewMatchCrewRemove', self)
        self.air.netMessenger.ignore('crewMatchJoinRequest', self)
        self.air.netMessenger.ignore('crewMatchJoinResponse', self)
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
        self.pendingJoins.pop(avatarId, None)
        taskMgr.remove(self.uniqueName('join-crew-%d' % avatarId))

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

    def getSponsorName(self, entry):
        if entry.remote:
            return entry.sponsorName

        sponsor = self.air.doId2do.get(entry.avatarId)
        if not sponsor:
            return ''

        return sponsor.getName()

    def getSponsorLocation(self, entry):
        if entry.remote:
            return entry.location

        sponsor = self.air.doId2do.get(entry.avatarId)
        if not sponsor:
            return ''

        return self.getAvatarLocation(sponsor)

    def isCrewMatch(self, entry, avatar):
        if entry.avatarId == avatar.doId:
            return False

        if entry.remote:
            # the sponsor's district checks the crew still has room when the avatar joins
            sponsorLevel = entry.sponsorLevel
        else:
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
        if not avatar:
            return False

        if self.air.bandManager.isAvatarInBand(avatar):
            return False

        if not self.addMemberToCrew(sponsorId, self.air.bandManager.getMemberInfo(avatar)):
            return False

        self.handleJoinedCrew(avatarId)
        return True

    def addMemberToCrew(self, sponsorId, memberInfo):
        """
        Adds the new member to the sponsor's crew, the sponsor must be on this
        district. The new member may be on any district.
        """

        if sponsorId not in self.air.doId2do:
            return False

        if not self.canSponsorCrew(sponsorId):
            return False

        if not self.air.bandManager.addMemberToBand(sponsorId, memberInfo):
            return False

        # the crew of one has now become a real crew
        self.crewsOfOne.discard(sponsorId)
        self.d_notifySponsorNewMember(sponsorId, memberInfo[2])
        return True

    def handleJoinedCrew(self, avatarId):
        self.avatarLookout.pop(avatarId, None)
        self.initialOffers.pop(avatarId, None)
        self.offers.pop(avatarId, None)
        self.pendingJoins.pop(avatarId, None)

    def joinCrew(self, sponsorId, avatarId, notifySuccess):
        """
        Adds the avatar to the sponsor's crew and lets the avatar know how it went,
        when the sponsor is on another district the sponsor's district is asked to
        add the avatar.
        """

        if sponsorId in self.air.doId2do:
            success = self.addAvatarToCrew(sponsorId, avatarId)
            if notifySuccess or not success:
                self.d_responseInitialAvatarAddResponse(avatarId, int(success))

            return

        entry = self.crewLookout.get(sponsorId)
        avatar = self.air.doId2do.get(avatarId)
        if not entry or not entry.remote or not avatar or self.air.bandManager.isAvatarInBand(avatar):
            self.d_responseInitialAvatarAddResponse(avatarId, 0)
            return

        self.pendingJoins[avatarId] = (sponsorId, notifySuccess)
        taskMgr.doMethodLater(self.JOIN_TIMEOUT, self.__joinTimeout, self.uniqueName('join-crew-%d' % avatarId),
            extraArgs=[avatarId, sponsorId])

        self.air.netMessenger.send('crewMatchJoinRequest', [sponsorId, self.air.bandManager.getMemberInfo(avatar)])

    def handleJoinRequest(self, sponsorId, memberInfo):
        if sponsorId not in self.air.doId2do:
            return

        success = self.addMemberToCrew(sponsorId, memberInfo)
        self.air.netMessenger.send('crewMatchJoinResponse', [memberInfo[0], sponsorId, success])

    def __joinTimeout(self, avatarId, sponsorId):
        self.notify.warning('Timed out adding avatar %d to crew %d on another district!' % (avatarId, sponsorId))
        self.handleRemoteCrewRemove(sponsorId)
        self.handleJoinResponse(avatarId, sponsorId, False)

    def handleJoinResponse(self, avatarId, sponsorId, success):
        pendingJoin = self.pendingJoins.get(avatarId)
        if not pendingJoin or pendingJoin[0] != sponsorId:
            return

        taskMgr.remove(self.uniqueName('join-crew-%d' % avatarId))

        notifySuccess = pendingJoin[1]
        if success:
            self.handleJoinedCrew(avatarId)
        else:
            del self.pendingJoins[avatarId]

        if notifySuccess or not success:
            self.d_responseInitialAvatarAddResponse(avatarId, int(success))

    def removeCrewFromLookout(self, avatarId):
        entry = self.crewLookout.pop(avatarId, None)
        if entry and not entry.remote:
            self.air.netMessenger.send('crewMatchCrewRemove', [avatarId])

    def addCrewToLookout(self, entry):
        sponsor = self.air.doId2do.get(entry.avatarId)
        entry.sponsorName = sponsor.getName()
        entry.sponsorLevel = self.getAvatarLevel(sponsor)
        entry.location = self.getAvatarLocation(sponsor)

        self.crewLookout[entry.avatarId] = entry
        self.air.netMessenger.send('crewMatchCrewAdd', [entry.getRemoteInfo()])

    def handleRemoteCrewAdd(self, remoteInfo):
        entry = CrewLookoutEntry.makeFromRemoteInfo(remoteInfo)
        if entry.avatarId in self.air.doId2do:
            # we're the sponsor's district
            return

        self.crewLookout[entry.avatarId] = entry
        self.offerCrewToAvatars(entry)

    def handleRemoteCrewRemove(self, avatarId):
        entry = self.crewLookout.get(avatarId)
        if entry and entry.remote:
            del self.crewLookout[avatarId]

    def offerCrewToAvatars(self, entry):
        if not entry.remote and entry.avatarId not in self.air.doId2do:
            return

        sponsorName = self.getSponsorName(entry)
        location = self.getSponsorLocation(entry)
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
            self.d_responseCrewFound(avatarId, sponsorName, entry.avatarId, location)

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
        self.addCrewToLookout(entry)
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

        self.initialOffers[avatarId] = entry.avatarId
        self.d_responseInitialAvatarAdd(avatarId, 1, self.getSponsorName(entry),
            self.getSponsorLocation(entry), crewType)

    def d_responseInitialAvatarAdd(self, avatarId, response, submitterName, location, crewType):
        self.sendUpdateToAvatarId(avatarId, 'responseInitialAvatarAdd', [response, submitterName, location, crewType])

    def requestInitialAvatarAddResponse(self, response, crewType):
        avatarId = self.air.getAvatarIdFromSender()
        sponsorId = self.initialOffers.pop(avatarId, None)
        if not sponsorId or not response:
            return

        self.joinCrew(sponsorId, avatarId, notifySuccess=True)

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
        self.joinCrew(crewOwnAvId, avatarId, notifySuccess=False)
