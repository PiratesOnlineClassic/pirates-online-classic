from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

from otp.ai import AIInterestHandles

from pirates.band import BandConstance
from pirates.band.DistributedBandMemberAI import DistributedBandMemberAI
from pirates.piratesbase import PLocalizer


class PirateBand:
    """
    Book keeping for a single crew owned by this band manager.
    The crew's members are DistributedBandMemberAI objects generated
    under the band manager in the band's own zone.
    """

    def __init__(self, bandId):
        self.bandId = bandId
        self.zoneId = bandId
        self.managerId = 0
        self.crewIcon = 1
        self.members = {}

    def getMember(self, avatarId):
        return self.members.get(avatarId)

    def getMemberIds(self):
        return list(self.members.keys())

    def isFull(self):
        return len(self.members) >= BandConstance.MAX_BAND_MEMBERS


class DistributedPirateBandManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPirateBandManagerAI')

    # The amount of time to wait before checking if a band member,
    # whom's avatar has left this district, is still online
    MEMBER_OFFLINE_CHECK_DELAY = 5.0

    # The interval at which we check that the band members currently
    # on another district are still online
    MEMBER_ONLINE_CHECK_INTERVAL = 60.0

    # Client bound fields which may be relayed to an avatar on another district
    RELAY_FIELDS = (
        'requestOutCome',
        'invitationFrom',
        'invitationCancel',
        'receiveUpdatedCrewIcon')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.bands = {}
        self.avatar2band = {}
        self.invites = {}
        self.accountIds = {}
        self.nextBandId = 1

        self.bandRequestHandlers = {
            'requestRemove': self.handleRequestRemove,
            'requestCrewIconUpdate': self.handleRequestCrewIconUpdate,
            'addMember': self.handleAddMember,
            'updateMemberHp': self.handleUpdateMemberHp,
            'updateMemberShip': self.handleUpdateMemberShip
        }

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        self.air.netMessenger.accept('bandRequest', self, self.handleBandRequest)
        self.air.netMessenger.accept('bandRelayToAvatar', self, self.handleRelayToAvatar)
        self.air.netMessenger.accept('bandAvatarBandId', self, self.handleAvatarBandId)

        taskMgr.doMethodLater(self.MEMBER_ONLINE_CHECK_INTERVAL, self.__checkMembersOnline,
            self.uniqueName('check-members-online'))

    def delete(self):
        taskMgr.remove(self.uniqueName('check-members-online'))
        self.air.netMessenger.ignore('bandRequest', self)
        self.air.netMessenger.ignore('bandRelayToAvatar', self)
        self.air.netMessenger.ignore('bandAvatarBandId', self)

        for bandId in list(self.bands.keys()):
            self.removeBand(bandId)

        self.ignoreAll()
        DistributedObjectAI.delete(self)

    # Band helpers

    def getBand(self, bandId):
        return self.bands.get(bandId)

    def getBandFromAvatar(self, avatarId):
        bandId = self.avatar2band.get(avatarId)
        if not bandId:
            return None

        return self.bands.get(bandId)

    def hasBand(self, avatarId):
        return avatarId in self.avatar2band

    def isBandLeader(self, avatarId):
        band = self.getBandFromAvatar(avatarId)
        return band is not None and band.managerId == avatarId

    def getBandMemberIds(self, avatarId):
        band = self.getBandFromAvatar(avatarId)
        if not band:
            return []

        return band.getMemberIds()

    def isAvatarInBand(self, avatar):
        """
        Returns True if the avatar is in a band owned by any band manager.
        """

        if self.hasBand(avatar.doId):
            return True

        bandManagerId, bandId = avatar.getBandId()
        return bandManagerId != 0 and bandId != 0

    def getAvatarAccountId(self, avatar):
        accountId = self.accountIds.get(avatar.doId)
        if accountId:
            return accountId

        return avatar.getDISLid()

    def getMemberInfo(self, avatar):
        hp, maxHp = self.getAvatarHp(avatar)
        return [avatar.doId, self.getAvatarAccountId(avatar), avatar.getName(), hp, maxHp]

    def getAvatarHp(self, avatar):
        hp = avatar.getHp()
        if isinstance(hp, (list, tuple)):
            hp = hp[0]

        return (max(0, hp), max(0, avatar.getMaxHp()))

    def createBand(self):
        bandId = self.nextBandId
        self.nextBandId += 1

        band = PirateBand(bandId)
        self.bands[bandId] = band
        return band

    def removeBand(self, bandId):
        band = self.bands.get(bandId)
        if not band:
            return

        for avatarId in band.getMemberIds():
            self.removeBandMember(band, avatarId, dissolve=False)

        self.air.crewMatch.removeCrewFromLookout(band.managerId)
        del self.bands[bandId]

    def addBandMember(self, band, memberInfo, isManager=False):
        avatarId, accountId, name, hp, maxHp = memberInfo
        if band.getMember(avatarId):
            return band.getMember(avatarId)

        member = DistributedBandMemberAI(self.air)
        member.setAvatarId(avatarId)
        member.setName(name)
        member.setHp(hp)
        member.setMaxHp(maxHp)
        member.setBandId(self.doId, band.bandId)
        member.setIsManager(int(isManager))
        member.generateWithRequiredAndId(self.air.allocateChannel(), self.doId, band.zoneId)

        band.members[avatarId] = member
        self.avatar2band[avatarId] = band.bandId
        if isManager:
            band.managerId = avatarId

        # give the avatar it's owner view of the band member, this is
        # how the avatar sends it's crew chat and receives teleport queries...
        if accountId:
            self.accountIds[avatarId] = accountId
            self.air.setOwner(member.doId, accountId << 32 | avatarId)
        else:
            self.notify.warning('Cannot set owner of band member for avatar %d, '
                'avatar has no account id!' % avatarId)

        # open the band zone on behalf of the client, so they can
        # see all of their crew mates regardless of what district they are on
        self.air.clientAddInterest(member.GetPuppetConnectionChannel(avatarId),
            AIInterestHandles.PIRATES_BAND, self.doId, band.zoneId, False)

        self.d_setAvatarBandId(avatarId, self.doId, band.bandId)
        self.updateMemberShipInfo(avatarId)

        avatar = self.air.doId2do.get(avatarId)
        if avatar:
            self.acceptAvatarDelete(avatar)

        return member

    def removeBandMember(self, band, avatarId, dissolve=True):
        member = band.members.pop(avatarId, None)
        if not member:
            return

        self.avatar2band.pop(avatarId, None)
        self.accountIds.pop(avatarId, None)
        taskMgr.remove(self.uniqueName('check-member-%d' % avatarId))

        self.air.clientRemoveInterest(member.GetPuppetConnectionChannel(avatarId),
            AIInterestHandles.PIRATES_BAND, False)

        member.requestDelete()
        self.d_setAvatarBandId(avatarId, 0, 0)

        if not dissolve:
            return

        if len(band.members) <= 1:
            # a crew of one isn't a crew at all...
            self.removeBand(band.bandId)
            return

        if band.managerId == avatarId:
            self.air.crewMatch.removeCrewFromLookout(avatarId)
            newManagerId = band.getMemberIds()[0]
            band.managerId = newManagerId
            band.members[newManagerId].b_setIsManager(1)

    def addAvatarToBand(self, managerId, avatar):
        """
        Adds the avatar to the band managed by the managerId, if the manager isn't
        in a band yet then a new band is created. Returns True on success.
        """

        if self.isAvatarInBand(avatar):
            return False

        manager = self.air.doId2do.get(managerId)
        band = self.getBandFromAvatar(managerId)
        if band:
            if band.managerId != managerId or band.isFull():
                return False

        elif manager and not self.isAvatarInBand(manager):
            band = self.createBand()
            self.addBandMember(band, self.getMemberInfo(manager), isManager=True)
        else:
            return False

        self.addBandMember(band, self.getMemberInfo(avatar))
        return True

    def d_setAvatarBandId(self, avatarId, bandManagerId, bandId):
        avatar = self.air.doId2do.get(avatarId)
        if avatar:
            avatar.b_setBandId(bandManagerId, bandId)
            return

        # the avatar is on another district, send the update directly to the avatar
        # object and let the district it's on know about the change too.
        dclass = self.air.dclassesByName['DistributedPlayerPirateAI']
        field = dclass.getFieldByName('setBandId')
        datagram = field.aiFormatUpdate(avatarId, avatarId, self.air.ourChannel, [bandManagerId, bandId])
        self.air.send(datagram)

        self.air.netMessenger.send('bandAvatarBandId', [avatarId, bandManagerId, bandId])

    def handleAvatarBandId(self, avatarId, bandManagerId, bandId):
        avatar = self.air.doId2do.get(avatarId)
        if not avatar or not hasattr(avatar, 'setBandId'):
            return

        avatar.setBandId(bandManagerId, bandId)

    def sendUpdateToAvatar(self, avatarId, fieldName, args):
        if avatarId in self.air.doId2do:
            self.sendUpdateToAvatarId(avatarId, fieldName, args)
            return

        self.air.netMessenger.send('bandRelayToAvatar', [avatarId, fieldName, args])

    def handleRelayToAvatar(self, avatarId, fieldName, args):
        if fieldName not in self.RELAY_FIELDS:
            return

        if avatarId not in self.air.doId2do:
            return

        self.sendUpdateToAvatarId(avatarId, fieldName, args)

    def sendBandRequest(self, request, avatarId, args):
        """
        Sends a band request to the band manager which owns the avatar's band.
        """

        handler = self.bandRequestHandlers[request]
        if self.hasBand(avatarId):
            handler(avatarId, *args)
            return

        # don't bother the other districts when the avatar isn't in a band
        avatar = self.air.doId2do.get(avatarId)
        if avatar and hasattr(avatar, 'getBandId') and not self.isAvatarInBand(avatar):
            return

        self.air.netMessenger.send('bandRequest', [request, avatarId, args])

    def handleBandRequest(self, request, avatarId, args):
        if not self.hasBand(avatarId):
            return

        handler = self.bandRequestHandlers.get(request)
        if not handler:
            self.notify.warning('Received unknown band request: %s!' % request)
            return

        handler(avatarId, *args)

    def acceptAvatarDelete(self, avatar):
        self.accept(avatar.getDeleteEvent(), self.__handleAvatarDelete, [avatar.doId])

    def __handleAvatarDelete(self, avatarId):
        self.ignore('distObjDelete-%d' % avatarId)

        # cancel any pending invitations
        inviterId = self.invites.pop(avatarId, None)
        if inviterId:
            self.sendUpdateToAvatar(inviterId, 'requestOutCome', [avatarId, BandConstance.outcome_not_online])

        for inviteeId, inviterId in list(self.invites.items()):
            if inviterId == avatarId:
                del self.invites[inviteeId]
                self.d_invitationCancel(inviteeId, avatarId)

        if not self.hasBand(avatarId):
            return

        # the avatar may have only changed district, crews are cross district
        # so wait a moment and check if the avatar is still logged in.
        taskMgr.doMethodLater(self.MEMBER_OFFLINE_CHECK_DELAY, self.__checkMemberOnline,
            self.uniqueName('check-member-%d' % avatarId), extraArgs=[avatarId])

    def __checkMemberOnline(self, avatarId):
        if not self.hasBand(avatarId):
            return

        self.air.getActivated(avatarId, self.__handleMemberActivated)

    def __checkMembersOnline(self, task):
        for avatarId in list(self.avatar2band.keys()):
            if avatarId not in self.air.doId2do:
                self.air.getActivated(avatarId, self.__handleMemberActivated)

        return Task.again

    def __handleMemberActivated(self, avatarId, activated):
        if activated or avatarId in self.air.doId2do:
            return

        band = self.getBandFromAvatar(avatarId)
        if not band:
            return

        self.notify.debug('Removing avatar %d from band %d, avatar is no longer online.' % (
            avatarId, band.bandId))

        self.removeBandMember(band, avatarId)

    # Invitations

    def requestInvite(self, avatarId):
        inviterId = self.air.getAvatarIdFromSender()
        inviter = self.air.doId2do.get(inviterId)
        if not inviter:
            return

        self.accountIds[inviterId] = self.air.getAccountIdFromSender()
        if avatarId == inviterId:
            self.air.logPotentialHacker(
                message='Avatar tried to invite themselves to their own crew!',
                avatarId=avatarId)

            return

        invitee = self.air.doId2do.get(avatarId)
        if not invitee or not hasattr(invitee, 'getBandId'):
            self.d_requestOutCome(inviterId, avatarId, BandConstance.outcome_not_online)
            return

        if avatarId in self.invites:
            self.d_requestOutCome(inviterId, avatarId, BandConstance.outcome_already_invited)
            return

        if self.isAvatarInBand(invitee):
            self.d_requestOutCome(inviterId, avatarId, BandConstance.outcome_already_in_Band)
            return

        band = self.getBandFromAvatar(inviterId)
        if band:
            if band.managerId != inviterId:
                self.d_requestOutCome(inviterId, avatarId, BandConstance.outcome_declined)
                return

            if band.isFull():
                self.d_requestOutCome(inviterId, avatarId, BandConstance.outcome_full)
                return

        self.invites[avatarId] = inviterId
        self.acceptAvatarDelete(inviter)
        self.acceptAvatarDelete(invitee)
        self.d_invitationFrom(avatarId, inviterId, inviter.getName())

    def requestCancel(self, avatarId):
        inviterId = self.air.getAvatarIdFromSender()
        if self.invites.get(avatarId) != inviterId:
            return

        del self.invites[avatarId]
        self.d_invitationCancel(avatarId, inviterId)

    def invitationResponce(self, avatarId, responce):
        inviteeId = self.air.getAvatarIdFromSender()
        invitee = self.air.doId2do.get(inviteeId)
        if not invitee:
            return

        if self.invites.get(inviteeId) != avatarId:
            self.notify.debug('Avatar %d responded to a non existent invitation from %d!' % (
                inviteeId, avatarId))

            return

        del self.invites[inviteeId]
        self.accountIds[inviteeId] = self.air.getAccountIdFromSender()
        if responce != BandConstance.outcome_ok:
            self.d_requestOutCome(avatarId, inviteeId, BandConstance.outcome_declined)
            return

        if self.isAvatarInBand(invitee):
            self.d_requestOutCome(avatarId, inviteeId, BandConstance.outcome_already_in_Band)
            return

        inviter = self.air.doId2do.get(avatarId)
        if not self.hasBand(avatarId) and (not inviter or self.isAvatarInBand(inviter)):
            # the inviter's crew is owned by another district's band manager
            self.sendBandRequest('addMember', avatarId, [self.getMemberInfo(invitee)])
            return

        self.handleAddMember(avatarId, self.getMemberInfo(invitee))

    def handleAddMember(self, managerId, memberInfo):
        avatarId = memberInfo[0]
        band = self.getBandFromAvatar(managerId)
        if band:
            if band.managerId != managerId:
                self.d_requestOutCome(managerId, avatarId, BandConstance.outcome_declined)
                return

            if band.isFull():
                self.d_requestOutCome(managerId, avatarId, BandConstance.outcome_full)
                return

            if self.hasBand(avatarId):
                self.d_requestOutCome(managerId, avatarId, BandConstance.outcome_already_in_Band)
                return

        else:
            manager = self.air.doId2do.get(managerId)
            if not manager:
                self.d_requestOutCome(managerId, avatarId, BandConstance.outcome_not_online)
                return

            band = self.createBand()
            self.addBandMember(band, self.getMemberInfo(manager), isManager=True)

        self.addBandMember(band, memberInfo)
        self.d_requestOutCome(managerId, avatarId, BandConstance.outcome_ok)

    def d_requestOutCome(self, inviterId, avatarId, responce):
        self.sendUpdateToAvatar(inviterId, 'requestOutCome', [avatarId, responce])

    def d_invitationFrom(self, inviteeId, avatarId, avatarName):
        self.sendUpdateToAvatar(inviteeId, 'invitationFrom', [avatarId, avatarName])

    def d_invitationCancel(self, inviteeId, avatarId):
        self.sendUpdateToAvatar(inviteeId, 'invitationCancel', [avatarId])

    # Leaving and kicking

    def requestRemove(self, avatarId):
        requesterId = self.air.getAvatarIdFromSender()
        if not requesterId:
            return

        self.sendBandRequest('requestRemove', requesterId, [avatarId])

    def handleRequestRemove(self, requesterId, avatarId):
        band = self.getBandFromAvatar(requesterId)
        if not band:
            return

        if avatarId != requesterId:
            if band.managerId != requesterId:
                self.air.logPotentialHacker(
                    message='Avatar tried to remove a crew member without being the captain!',
                    requesterId=requesterId,
                    targetAvId=avatarId)

                return

            if not band.getMember(avatarId):
                return

        self.removeBandMember(band, avatarId)

    # Crew icon

    def requestCrewIconUpdate(self, iconKey):
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return

        self.sendBandRequest('requestCrewIconUpdate', avatarId, [iconKey])

    def handleRequestCrewIconUpdate(self, avatarId, iconKey):
        band = self.getBandFromAvatar(avatarId)
        if not band:
            return

        if band.managerId != avatarId:
            # only the captain can choose the crew's icon, crew mates
            # turning on their icon get the icon the captain has chosen
            if iconKey:
                self.d_receiveUpdatedCrewIcon(avatarId, band.crewIcon)

            return

        band.crewIcon = iconKey
        for memberId in band.getMemberIds():
            self.d_receiveUpdatedCrewIcon(memberId, iconKey)

    def d_receiveUpdatedCrewIcon(self, avatarId, iconKey):
        self.sendUpdateToAvatar(avatarId, 'receiveUpdatedCrewIcon', [iconKey])

    # Member status

    def updateAvatarHp(self, avatar):
        """
        Called by the avatar when it's hp or max hp has changed.
        """

        if not self.isAvatarInBand(avatar):
            return

        hp, maxHp = self.getAvatarHp(avatar)
        self.sendBandRequest('updateMemberHp', avatar.doId, [hp, maxHp])

    def handleUpdateMemberHp(self, avatarId, hp, maxHp):
        band = self.getBandFromAvatar(avatarId)
        if not band:
            return

        member = band.getMember(avatarId)
        if member.getMaxHp() != maxHp:
            member.b_setMaxHp(maxHp)

        if member.getHp() != hp:
            member.b_setHp(hp)

    def getShipInfo(self, avatar):
        ship = self.air.doId2do.get(avatar.getActiveShipId())
        if not ship or not hasattr(ship, 'getShipClass'):
            return [0, '', 0, [], False]

        # only the captain's ship is shown as the crew member's ship
        captainId = ship.getCaptainId() if hasattr(ship, 'getCaptainId') else 0
        if captainId and captainId != avatar.doId:
            return [0, '', 0, [], False]

        hasSpace = len(ship.getCrew()) < ship.getMaxCrew()
        return [ship.doId, ship.getName(), ship.getShipClass(), [], hasSpace]

    def updateMemberShipInfo(self, avatarId):
        avatar = self.air.doId2do.get(avatarId)
        if not avatar or not hasattr(avatar, 'getActiveShipId'):
            return

        self.updateAvatarShipInfo(avatar)

    def updateAvatarShipInfo(self, avatar):
        """
        Called by the avatar when it's active ship has changed.
        """

        if not self.isAvatarInBand(avatar):
            return

        locationName = ''
        parentObj = avatar.getParentObj()
        if parentObj and hasattr(parentObj, 'getLocalizerName'):
            locationName = parentObj.getLocalizerName()

        self.sendBandRequest('updateMemberShip', avatar.doId, [self.getShipInfo(avatar), locationName])

    def handleUpdateMemberShip(self, avatarId, shipInfo, locationName):
        band = self.getBandFromAvatar(avatarId)
        if not band:
            return

        member = band.getMember(avatarId)
        shipId, shipName, shipClass, mastInfo, hasSpace = shipInfo
        previousShipId = member.getShipInfo()[0]
        if member.getShipHasSpace() != hasSpace:
            member.b_setShipHasSpace(hasSpace)

        if previousShipId == shipId:
            return

        member.b_setShipInfo(shipId, shipName, shipClass, mastInfo)
        if shipId:
            member.d_setShipDeployMessage(avatarId, shipName, locationName or PLocalizer.Unknown)
