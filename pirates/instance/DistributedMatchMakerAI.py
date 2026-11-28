import random

from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

from otp.ai.MagicWordGlobal import *
from otp.otpbase import OTPGlobals

from pirates.piratesbase import PiratesGlobals
from pirates.world import GameTypeGlobals


class LookoutMatchSetup:
    # a match the UberDOG has asked this district to host, the game is created
    # once any avatars on other districts have arrived here...

    def __init__(self, matchId, gameCategory, gameType, options, teams):
        self.matchId = matchId
        self.gameCategory = gameCategory
        self.gameType = gameType
        self.options = options
        self.teams = teams
        self.pendingAvatarIds = []

    def getAvatarIds(self):
        avatarIds = []
        for team in self.teams:
            avatarIds.extend(team)

        return avatarIds


class DistributedMatchMakerAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMatchMakerAI')

    # the client's requests (requestJoin, skipJoin, etc.) are handled
    # by the UberDOG, the districts must not listen in on them...
    doNotListenToChannel = True

    ArrivalTimeout = config.GetFloat('lookout-arrival-timeout', 20.0)

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

        self.searchingAvatarIds = []
        self.matchSetups = {}
        self.instance2match = {}

    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)

        self.air.netMessenger.accept('matchMakerCreateMatch', self, self.handleCreateMatch)

    def delete(self):
        self.air.netMessenger.ignore('matchMakerCreateMatch', self)
        for matchId in list(self.matchSetups.keys()):
            taskMgr.remove(self.getArrivalTaskName(matchId))

        self.searchingAvatarIds = []
        self.matchSetups = {}
        self.instance2match = {}
        self.ignoreAll()
        DistributedObjectGlobalAI.delete(self)

    def sendUpdateToAvatar(self, avatarId, fieldName, args):
        # the avatar does not need to be on this district to receive it
        dclass = self.air.dclassesByName['DistributedPlayerPirateAI']
        datagram = dclass.aiFormatUpdate(fieldName, avatarId, self.GetPuppetConnectionChannel(avatarId),
            self.air.ourChannel, args)

        self.air.send(datagram)

    def canRequestActivity(self, avatar, gameCategory):
        if avatar.doId in self.air.teleportMgr.avatar2fsm:
            return False

        if self.air.pvpManager.isAvatarInPVP(avatar):
            return False

        return True

    def requestActivity(self, avatar, gameType, gameCategory, options, shipIds):
        if not self.canRequestActivity(avatar, gameCategory):
            self.notify.debug('Avatar %d cannot request lookout activity %d right now.' % (
                avatar.doId, gameCategory))

            avatar.d_lookoutMatchFailed(False)
            return

        # only the ships the avatar actually owns may be brought along...
        inventory = avatar.getInventory()
        if inventory:
            ownedShipIds = inventory.getShipDoIdList()
            shipIds = [shipId for shipId in shipIds if shipId in ownedShipIds]
        else:
            shipIds = []

        if avatar.doId not in self.searchingAvatarIds:
            self.searchingAvatarIds.append(avatar.doId)
            self.acceptOnce(avatar.getDeleteEvent(), self.__handleAvatarDeleted,
                extraArgs=[avatar.doId])

        self.d_requestActivity(avatar.doId, gameType, gameCategory, options, shipIds,
            self.air.districtId, getattr(avatar, 'gameAccess', OTPGlobals.AccessUnknown))

    def d_requestActivity(self, avatarId, gameType, gameCategory, options, shipIds, shardId, gameAccess):
        self.sendUpdate('requestActivity', [avatarId, gameType, gameCategory, options, shipIds,
            shardId, gameAccess])

    def __handleAvatarDeleted(self, avatarId):
        if avatarId not in self.searchingAvatarIds:
            return

        self.searchingAvatarIds.remove(avatarId)
        self.air.netMessenger.send('matchMakerAvatarLeft', [avatarId, self.air.districtId])

    def getInviteeIds(self, avatar, inviteModes, additionalAvs):
        inviteeIds = []
        if PiratesGlobals.LOOKOUT_INVITE_CREW in inviteModes:
            inviteeIds.extend(self.air.bandManager.getBandMemberIds(avatar.doId))

        if PiratesGlobals.LOOKOUT_INVITE_GUILD in inviteModes and avatar.getGuildId():
            for doId, do in list(self.air.doId2do.items()):
                if hasattr(do, 'getGuildId') and hasattr(do, 'getInventory') and \
                        do.getGuildId() == avatar.getGuildId():
                    inviteeIds.append(doId)

        if PiratesGlobals.LOOKOUT_INVITE_FRIENDS in inviteModes:
            for friendInfo in avatar.getFriendsList():
                inviteeIds.append(friendInfo[0])

        inviteeIds.extend(additionalAvs)

        uniqueIds = []
        for inviteeId in inviteeIds:
            if inviteeId and inviteeId != avatar.doId and inviteeId not in uniqueIds:
                uniqueIds.append(inviteeId)

        return uniqueIds

    def canInvite(self, inviteeId):
        invitee = self.air.doId2do.get(inviteeId)
        if not invitee:
            # the invitee may be on another district, we have no way
            # of telling if they are busy so let them decide...
            return True

        return self.canRequestActivity(invitee, None)

    def requestInvites(self, avatar, inviteModes, gameCategory, gameType, options, additionalAvs):
        inviteeIds = self.getInviteeIds(avatar, inviteModes, additionalAvs)
        invited = []
        numFailed = 0
        for inviteeId in inviteeIds:
            if not self.canInvite(inviteeId):
                numFailed += 1
                continue

            invited.append(inviteeId)

        if invited:
            # the invitees are given the inviter's vip pass, so the lookout
            # is able to keep the party together...
            inviteOptions = []
            for option in options:
                if option[0] in (str(GameTypeGlobals.GAME_OPTION_VIP_PASS),
                                 str(GameTypeGlobals.GAME_OPTION_DESIRED_PLAYERS)):
                    continue

                inviteOptions.append([option[0], option[1]])

            inviteOptions.append([str(GameTypeGlobals.GAME_OPTION_VIP_PASS), str(avatar.doId)])
            inviteOptions.append([str(GameTypeGlobals.GAME_OPTION_DESIRED_PLAYERS),
                ','.join([str(avatarId) for avatarId in [avatar.doId] + invited])])

            for inviteeId in invited:
                self.d_requestLookoutInvite(inviteeId, avatar.doId, avatar.getName(), gameCategory,
                    gameType, inviteOptions)

        self.notify.debug('Avatar %d invited %r to activity %d (%d failed)' % (avatar.doId, invited,
            gameCategory, numFailed))

        avatar.d_requestInvitesResp(invited, numFailed)

    def d_requestLookoutInvite(self, inviteeId, inviterId, inviterName, activityCategory, activityType, options):
        self.sendUpdateToAvatar(inviteeId, 'requestLookoutInvite', [inviterId, inviterName,
            activityCategory, activityType, options])

    def getArrivalTaskName(self, matchId):
        return self.uniqueName('arrival-%d' % matchId)

    def handleCreateMatch(self, shardId, matchId, gameCategory, gameType, options, teams):
        if shardId != self.air.districtId:
            return

        setup = LookoutMatchSetup(matchId, gameCategory, gameType, options, teams)
        self.matchSetups[matchId] = setup
        for avatarId in setup.getAvatarIds():
            if avatarId in self.air.doId2do:
                continue

            # this avatar is on another district, bring them here
            # before the game is created...
            setup.pendingAvatarIds.append(avatarId)
            self.acceptOnce('generate-%d' % avatarId, self.__handleAvatarArrived,
                extraArgs=[matchId, avatarId])

            self.air.setAI(avatarId, self.air.ourChannel)

        if not setup.pendingAvatarIds:
            self.createMatch(setup)
            return

        taskMgr.doMethodLater(self.ArrivalTimeout, self.__arrivalTimedOut,
            self.getArrivalTaskName(matchId), extraArgs=[matchId])

    def __handleAvatarArrived(self, matchId, avatarId, avatar=None):
        setup = self.matchSetups.get(matchId)
        if not setup or avatarId not in setup.pendingAvatarIds:
            return

        setup.pendingAvatarIds.remove(avatarId)
        if not setup.pendingAvatarIds:
            taskMgr.remove(self.getArrivalTaskName(matchId))
            self.createMatch(setup)

    def __arrivalTimedOut(self, matchId):
        setup = self.matchSetups.get(matchId)
        if not setup:
            return Task.done

        for avatarId in setup.pendingAvatarIds:
            self.notify.warning('Avatar %d never arrived for match %d!' % (avatarId, matchId))
            self.ignore('generate-%d' % avatarId)

        setup.pendingAvatarIds = []
        self.createMatch(setup)
        return Task.done

    def createMatch(self, setup):
        self.matchSetups.pop(setup.matchId, None)

        # drop anyone who has since left the district...
        setup.teams = [[avatarId for avatarId in team if avatarId in self.air.doId2do] for team in setup.teams]
        setup.teams = [team for team in setup.teams if team]
        if not setup.teams:
            self.notify.warning('Cannot create match %d, none of the avatars are here!' % setup.matchId)
            self.d_instanceCreated(setup.matchId, self.air.districtId, 0)
            return

        instanceDoId = 0
        if setup.gameCategory == PiratesGlobals.GAME_TYPE_PVP:
            instanceDoId = self.createPVPMatch(setup)
        elif setup.gameCategory == PiratesGlobals.GAME_TYPE_PG:
            instanceDoId = self.createParlorMatch(setup)
        elif setup.gameCategory == PiratesGlobals.GAME_TYPE_TM:
            instanceDoId = self.createTreasureMapMatch(setup)
        else:
            self.notify.warning('Cannot create match %d, unknown game category %d!' % (
                setup.matchId, setup.gameCategory))

        self.d_instanceCreated(setup.matchId, self.air.districtId, instanceDoId)

    def createPVPMatch(self, setup):
        instance = self.air.pvpManager.createPVPInstance(setup.gameType, setup.teams)
        if not instance:
            return 0

        self.watchInstance(setup.matchId, instance)
        return instance.doId

    def getParlorTableClass(self, gameType):
        from pirates.minigame.DistributedBlackjackTableAI import DistributedBlackjackTableAI
        from pirates.minigame.DistributedHoldemTableAI import DistributedHoldemTableAI

        if gameType == PiratesGlobals.GAME_STYLE_BLACKJACK:
            return DistributedBlackjackTableAI
        elif gameType == PiratesGlobals.GAME_STYLE_POKER:
            return DistributedHoldemTableAI

        return None

    def findParlorTable(self, gameType, numPlayers):
        tableClass = self.getParlorTableClass(gameType)
        if not tableClass:
            return None

        tables = []
        for do in list(self.air.doId2do.values()):
            if not isinstance(do, tableClass):
                continue

            if do.getOpenSeatCount() < numPlayers:
                continue

            if not self.air.teleportMgr.getInstanceFromObject(do.getParentObj()):
                continue

            tables.append(do)

        if not tables:
            return None

        return random.choice(tables)

    def createParlorMatch(self, setup):
        avatarIds = setup.getAvatarIds()
        table = self.findParlorTable(setup.gameType, len(avatarIds))
        if not table:
            self.notify.warning('Cannot create match %d, no parlor table available for game type %d!' % (
                setup.matchId, setup.gameType))

            return 0

        area = table.getParentObj()
        for avatarId in avatarIds:
            avatar = self.air.doId2do.get(avatarId)
            if not avatar or avatar.getParentObj() is area:
                continue

            self.air.teleportMgr.teleportToArea(avatar, area)

        return table.doId

    def createTreasureMapMatch(self, setup):
        from pirates.treasuremap.DistributedTreasureMapAI import DistributedTreasureMapAI

        avatarIds = setup.getAvatarIds()
        treasureMapId = 0
        try:
            treasureMapId = int(dict([(option[0], option[1]) for option in setup.options]).get(
                str(GameTypeGlobals.GAME_OPTION_TM_ID), 0))
        except (TypeError, ValueError):
            pass

        treasureMap = self.air.doId2do.get(treasureMapId)
        if not isinstance(treasureMap, DistributedTreasureMapAI) or treasureMap.ownerId not in avatarIds:
            self.notify.warning('Cannot create match %d, invalid treasure map %d!' % (
                setup.matchId, treasureMapId))

            return 0

        owner = self.air.doId2do.get(treasureMap.ownerId)
        participantIds = [avatarId for avatarId in avatarIds if avatarId != treasureMap.ownerId]
        if not owner or not treasureMap.startInstance(owner, participantIds):
            return 0

        if treasureMap.activeInstance:
            self.watchInstance(setup.matchId, treasureMap.activeInstance)
            return treasureMap.activeInstance.doId

        instanceDoId = treasureMap.pendingInstanceDoId
        self.instance2match[instanceDoId] = setup.matchId
        self.acceptOnce('generate-%d' % instanceDoId, lambda instance: self.watchInstance(
            setup.matchId, instance))

        return instanceDoId

    def watchInstance(self, matchId, instance):
        self.instance2match[instance.doId] = matchId
        self.acceptOnce(instance.getDeleteEvent(), self.__handleInstanceDeleted,
            extraArgs=[instance.doId])

    def __handleInstanceDeleted(self, instanceDoId):
        matchId = self.instance2match.pop(instanceDoId, None)
        if matchId is None:
            return

        self.d_instanceRemoved(matchId, self.air.districtId, instanceDoId)

    def d_instanceCreated(self, matchId, shardId, instanceDoId):
        self.sendUpdate('instanceCreated', [matchId, shardId, instanceDoId])

    def d_instanceRemoved(self, matchId, shardId, instanceDoId):
        self.sendUpdate('instanceRemoved', [matchId, shardId, instanceDoId])

    def d_printStatus(self, avatarId):
        self.sendUpdate('printStatus', [avatarId])


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def lookoutStatus():
    """
    Prints the status of the lookout's queue on the UberDOG
    """

    avatar = spellbook.getInvoker()
    spellbook.getManager().air.matchMaker.d_printStatus(avatar.doId)
    return 'Printed lookout status to the UberDOG log.'
