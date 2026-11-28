from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.task import Task

from otp.otpbase import OTPGlobals

from pirates.piratesbase import PiratesGlobals
from pirates.world import GameTypeGlobals


# the activities the lookout is able to match players for, any other
# game category requested by the client is handled locally (crew lookout
# and the treasure map quick start) or is not supported by the server...
MatchStyleInfo = {
    PiratesGlobals.GAME_TYPE_PVP: {
        PiratesGlobals.GAME_STYLE_BATTLE: {
            'minPlayers': 2,
            'maxPlayers': 8},
        PiratesGlobals.GAME_STYLE_TEAM_BATTLE: {
            'minPlayers': 4,
            'maxPlayers': 8,
            'numTeams': 2},
        PiratesGlobals.GAME_STYLE_SHIP_BATTLE: {
            'minPlayers': 2,
            'maxPlayers': 8,
            'numTeams': 2}},
    PiratesGlobals.GAME_TYPE_PG: {
        PiratesGlobals.GAME_STYLE_BLACKJACK: {
            'minPlayers': 1,
            'maxPlayers': 6},
        PiratesGlobals.GAME_STYLE_POKER: {
            'minPlayers': 1,
            'maxPlayers': 6}},
    PiratesGlobals.GAME_TYPE_TM: {
        PiratesGlobals.GAME_STYLE_TM_BLACK_PEARL: {
            'minPlayers': 1,
            'maxPlayers': 12,
            'inviteOnly': True}}}


def getOption(options, optionId, default=None):
    for currOption in options:
        if len(currOption) < 2:
            continue

        if currOption[0] == str(optionId):
            return currOption[1]

    return default


def getIntOption(options, optionId, default=0):
    try:
        return int(getOption(options, optionId, default))
    except (TypeError, ValueError):
        return default


class LookoutRequest:
    """
    A single avatar's request to the lookout, the request stays in the
    queue until the avatar is placed into a game or cancels the request.
    """

    def __init__(self, avatarId, gameType, gameCategory, options, shipIds, shardId, gameAccess):
        self.avatarId = avatarId
        self.gameType = gameType
        self.gameCategory = gameCategory
        self.options = options
        self.shipIds = shipIds
        self.shardId = shardId
        self.gameAccess = gameAccess
        self.timestamp = globalClock.getRealTime()
        self.matchId = 0
        self.skipUntil = 0
        self.lastChance = -1

        self.vipPass = getIntOption(options, GameTypeGlobals.GAME_OPTION_VIP_PASS)
        self.desiredPlayers = []
        desiredPlayers = getOption(options, GameTypeGlobals.GAME_OPTION_DESIRED_PLAYERS, '')
        for avatarIdStr in desiredPlayers.split(','):
            if avatarIdStr.strip().isdigit():
                self.desiredPlayers.append(int(avatarIdStr))

    def isPartyLeader(self):
        return self.vipPass == self.avatarId

    def getPartyId(self):
        return self.vipPass

    def acceptsGameType(self, gameType):
        return self.gameType in (gameType, PiratesGlobals.GAME_STYLE_ANY)

    def getMinPlayers(self, default):
        return getIntOption(self.options, GameTypeGlobals.GAME_OPTION_MIN_PLAYERS, default)

    def getMaxPlayers(self, default):
        return getIntOption(self.options, GameTypeGlobals.GAME_OPTION_MAX_PLAYERS, default)


class LookoutMatch(FSM):
    """
    A group of lookout requests which have been matched together, the
    match waits for each avatar to join before the game is created on
    the district hosting the match.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('LookoutMatch')

    def __init__(self, mgr, matchId, gameCategory, gameType, requests):
        FSM.__init__(self, 'LookoutMatch-%d' % matchId)
        self.mgr = mgr
        self.matchId = matchId
        self.gameCategory = gameCategory
        self.gameType = gameType
        self.requests = requests
        self.joined = []
        self.hostShardId = 0
        self.instanceDoId = 0

    def getTaskName(self, name):
        return 'lookoutMatch-%d-%s' % (self.matchId, name)

    def getAvatarIds(self):
        return [request.avatarId for request in self.requests]

    def getRequest(self, avatarId):
        for request in self.requests:
            if request.avatarId == avatarId:
                return request

        return None

    def removeRequest(self, avatarId):
        request = self.getRequest(avatarId)
        if request:
            self.requests.remove(request)

        if avatarId in self.joined:
            self.joined.remove(avatarId)

        return request

    def isViable(self):
        return len(self.requests) >= self.mgr.getMinPlayers(self.gameCategory, self.gameType, self.requests)

    def isInviteOnly(self):
        return self.mgr.getStyleInfo(self.gameCategory, self.gameType).get('inviteOnly', False)

    def getOptions(self):
        # the party leader's options take priority, they own the treasure map, etc...
        for request in self.requests:
            if request.isPartyLeader():
                return request.options

        if self.requests:
            return self.requests[0].options

        return []

    def getTeams(self):
        styleInfo = self.mgr.getStyleInfo(self.gameCategory, self.gameType)
        parties = {}
        for request in self.requests:
            partyId = request.getPartyId() or request.avatarId
            parties.setdefault(partyId, []).append(request.avatarId)

        parties = sorted(list(parties.values()), key=len, reverse=True)
        numTeams = styleInfo.get('numTeams', 0)
        if not numTeams:
            # every party is a team of it's own...
            return parties

        # keep each party together, placing them on the smallest team...
        teams = [[] for x in range(numTeams)]
        for party in parties:
            smallestTeam = min(teams, key=len)
            smallestTeam.extend(party)

        return [team for team in teams if team]

    def chooseHostShard(self):
        shardCounts = {}
        for request in self.requests:
            if request.isPartyLeader() and self.isInviteOnly():
                # the leader owns the activity (their treasure map), so
                # the game must be hosted on the leader's district...
                return request.shardId

            shardCounts[request.shardId] = shardCounts.get(request.shardId, 0) + 1

        if not shardCounts:
            return 0

        return max(list(shardCounts.keys()), key=lambda shardId: shardCounts[shardId])

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterJoining(self):
        for request in self.requests:
            request.matchId = self.matchId
            self.mgr.d_lookoutMatchFound(request.avatarId, PiratesGlobals.LOOKOUT_JOIN_TIMEOUT, self.matchId)

        taskMgr.doMethodLater(PiratesGlobals.LOOKOUT_JOIN_TIMEOUT + self.mgr.JoinTimeoutGrace,
            self.__joinTimedOut, self.getTaskName('joinTimeout'))

    def exitJoining(self):
        taskMgr.remove(self.getTaskName('joinTimeout'))

    def __joinTimedOut(self, task):
        for request in list(self.requests):
            if request.avatarId in self.joined:
                continue

            self.notify.debug('Avatar %d did not join match %d in time.' % (request.avatarId, self.matchId))
            self.requests.remove(request)
            self.mgr.removeRequest(request.avatarId, removeFromMatch=False)
            self.mgr.d_lookoutMatchFailed(request.avatarId, False)

        self.checkJoined()
        return Task.done

    def avatarJoined(self, avatarId):
        if avatarId not in self.joined:
            self.joined.append(avatarId)

        self.checkJoined()

    def avatarSkipped(self, avatarId):
        self.removeRequest(avatarId)
        self.checkJoined()

    def checkJoined(self):
        if self.state != 'Joining':
            return

        if not self.isViable():
            self.mgr.matchFailed(self, restartRequest=True)
            return

        if len(self.joined) == len(self.requests):
            self.request('Creating')

    def enterCreating(self):
        self.hostShardId = self.chooseHostShard()
        self.notify.info('Creating match %d (category=%d, type=%d) on district %d for avatars: %r' % (
            self.matchId, self.gameCategory, self.gameType, self.hostShardId, self.getAvatarIds()))

        self.mgr.d_createMatch(self.hostShardId, self.matchId, self.gameCategory, self.gameType,
            self.getOptions(), self.getTeams())

        taskMgr.doMethodLater(self.mgr.CreateTimeout, self.__createTimedOut,
            self.getTaskName('createTimeout'))

    def exitCreating(self):
        taskMgr.remove(self.getTaskName('createTimeout'))

    def __createTimedOut(self, task):
        self.notify.warning('District %d never created match %d!' % (self.hostShardId, self.matchId))
        self.mgr.matchFailed(self, restartRequest=True)
        return Task.done

    def enterPlaying(self):
        # the players have been handed over to the district, they
        # are no longer waiting on the lookout...
        for request in self.requests:
            self.mgr.removeRequest(request.avatarId, removeFromMatch=False)

    def exitPlaying(self):
        pass

    def cleanup(self):
        if self.state != 'Off':
            self.demand('Off')

        self.requests = []
        self.joined = []
        self.mgr = None


class DistributedMatchMakerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMatchMakerUD')

    MatchInterval = config.GetFloat('lookout-match-interval', 5.0)
    FeedbackInterval = config.GetFloat('lookout-feedback-interval', 10.0)
    SkipDelay = config.GetFloat('lookout-skip-delay', 15.0)
    JoinTimeoutGrace = config.GetFloat('lookout-join-timeout-grace', 5.0)
    CreateTimeout = config.GetFloat('lookout-create-timeout', 60.0)
    PartyTimeout = config.GetFloat('lookout-party-timeout', PiratesGlobals.LOOKOUT_JOIN_TIMEOUT_INVITE)
    MinPlayersOverride = config.GetInt('lookout-min-players', 0)
    WantCrossDistrict = config.GetBool('lookout-cross-district', True)

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        self.requests = {}
        self.matches = {}
        self.nextMatchId = 1

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        self.air.netMessenger.accept('matchMakerAvatarLeft', self, self.handleAvatarLeft)

        taskMgr.doMethodLater(self.MatchInterval, self.__matchTask, self.uniqueName('match'))
        taskMgr.doMethodLater(self.FeedbackInterval, self.__feedbackTask, self.uniqueName('feedback'))

    def delete(self):
        taskMgr.remove(self.uniqueName('match'))
        taskMgr.remove(self.uniqueName('feedback'))
        self.air.netMessenger.ignore('matchMakerAvatarLeft', self)

        for match in list(self.matches.values()):
            match.cleanup()

        self.matches = {}
        self.requests = {}
        DistributedObjectGlobalUD.delete(self)

    # -------------------------------------------------------------------
    # Game styles
    # -------------------------------------------------------------------

    def getStyleInfo(self, gameCategory, gameType):
        return MatchStyleInfo.get(gameCategory, {}).get(gameType, {})

    def getGameTypes(self, gameCategory):
        gameTypes = list(MatchStyleInfo.get(gameCategory, {}).keys())
        if gameCategory == PiratesGlobals.GAME_TYPE_PVP:
            # respect the pvp game styles the cluster has enabled...
            enabledStyles = GameTypeGlobals.GameTypes.get(gameCategory, {}).get('style', {})
            gameTypes = [gameType for gameType in gameTypes if gameType in enabledStyles]

        return sorted(gameTypes)

    def getMinPlayers(self, gameCategory, gameType, requests):
        styleInfo = self.getStyleInfo(gameCategory, gameType)
        minPlayers = styleInfo.get('minPlayers', 1)
        for request in requests:
            minPlayers = max(minPlayers, request.getMinPlayers(minPlayers))

        if self.MinPlayersOverride:
            minPlayers = min(minPlayers, self.MinPlayersOverride)

        return max(1, minPlayers)

    def getMaxPlayers(self, gameCategory, gameType, requests):
        styleInfo = self.getStyleInfo(gameCategory, gameType)
        maxPlayers = styleInfo.get('maxPlayers', 1)
        for request in requests:
            maxPlayers = min(maxPlayers, request.getMaxPlayers(maxPlayers))

        return max(1, maxPlayers)

    def isGameTypeAccessible(self, gameCategory, gameType, gameAccess):
        if gameAccess in (OTPGlobals.AccessFull, OTPGlobals.AccessUnknown):
            return True

        return GameTypeGlobals.gameTypeAccessable(gameCategory, gameType, gameAccess)

    # -------------------------------------------------------------------
    # Requests
    # -------------------------------------------------------------------

    def requestActivity(self, avatarId, gameType, gameCategory, options, shipIds, shardId, gameAccess):
        if not avatarId:
            return

        if gameCategory not in MatchStyleInfo:
            self.notify.warning('Avatar %d requested unsupported lookout activity %d!' % (
                avatarId, gameCategory))

            self.d_lookoutMatchFailed(avatarId, False)
            return

        if gameType != PiratesGlobals.GAME_STYLE_ANY and gameType not in self.getGameTypes(gameCategory):
            self.notify.warning('Avatar %d requested unsupported game type %d for activity %d!' % (
                avatarId, gameType, gameCategory))

            self.d_lookoutMatchFailed(avatarId, False)
            return

        if not self.isGameTypeAccessible(gameCategory, gameType, gameAccess):
            self.notify.debug('Avatar %d does not have access to game type %d.' % (avatarId, gameType))
            self.d_lookoutMatchFailed(avatarId, False)
            return

        # a new request replaces whatever the avatar was looking for before...
        self.removeRequest(avatarId)

        request = LookoutRequest(avatarId, gameType, gameCategory, options, shipIds, shardId, gameAccess)
        self.requests[avatarId] = request
        self.notify.debug('Avatar %d is now on the lookout for category=%d type=%d on district %d' % (
            avatarId, gameCategory, gameType, shardId))

        self.d_requestActivityAccepted(avatarId)
        self.findMatches()

    def removeRequest(self, avatarId, removeFromMatch=True):
        request = self.requests.pop(avatarId, None)
        if not request:
            return None

        if removeFromMatch and request.matchId:
            match = self.matches.get(request.matchId)
            if match:
                match.avatarSkipped(avatarId)

        return request

    def getRequestFromSender(self, matchId):
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return None

        request = self.requests.get(avatarId)
        if not request:
            return None

        if matchId and request.matchId != matchId:
            self.notify.debug('Avatar %d sent stale match id %d (expected %d).' % (
                avatarId, matchId, request.matchId))

            return None

        return request

    def requestJoin(self, matchId):
        request = self.getRequestFromSender(matchId)
        if not request:
            return

        match = self.matches.get(request.matchId)
        if not match or match.state != 'Joining':
            return

        match.avatarJoined(request.avatarId)

    def skipJoin(self, matchId, clearSearch):
        request = self.getRequestFromSender(matchId)
        if not request:
            return

        match = self.matches.get(request.matchId)
        if not match or match.state != 'Joining':
            return

        if clearSearch:
            self.removeRequest(request.avatarId)
            return

        # the avatar would like to continue looking, but not for this game...
        match.avatarSkipped(request.avatarId)
        request.matchId = 0
        request.skipUntil = globalClock.getRealTime() + self.SkipDelay

    def cancelRequest(self, matchId):
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return

        request = self.requests.get(avatarId)
        if not request:
            return

        match = self.matches.get(request.matchId)
        if match and match.state not in ('Off', 'Joining'):
            # too late, the game is already being created...
            return

        self.removeRequest(avatarId)

    def handleAvatarLeft(self, avatarId, shardId):
        request = self.requests.get(avatarId)
        if not request or request.shardId != shardId:
            return

        match = self.matches.get(request.matchId)
        if match and match.state == 'Creating':
            # the avatar is being moved to the district hosting the match...
            return

        self.notify.debug('Avatar %d left district %d, removing lookout request.' % (avatarId, shardId))
        self.removeRequest(avatarId)

    # -------------------------------------------------------------------
    # Matching
    # -------------------------------------------------------------------

    def __matchTask(self, task):
        self.findMatches()
        return Task.again

    def __feedbackTask(self, task):
        self.sendFeedback()
        return Task.again

    def getSearchingRequests(self, gameCategory=None):
        now = globalClock.getRealTime()
        requests = []
        for request in list(self.requests.values()):
            if request.matchId:
                continue

            if request.skipUntil > now:
                continue

            if gameCategory is not None and request.gameCategory != gameCategory:
                continue

            requests.append(request)

        return sorted(requests, key=lambda request: request.timestamp)

    def getRequestBlocks(self, requests):
        """
        Groups the requests into blocks which must be placed in a match together,
        an avatar on their own is a block of one, invited parties are kept together.
        """

        now = globalClock.getRealTime()
        blocks = []
        parties = {}
        for request in requests:
            partyId = request.getPartyId()
            if not partyId:
                blocks.append([request])
                continue

            parties.setdefault(partyId, []).append(request)

        for partyId, partyRequests in list(parties.items()):
            leader = None
            for request in partyRequests:
                if request.avatarId == partyId:
                    leader = request
                    break

            oldest = min([request.timestamp for request in partyRequests])
            timedOut = now - oldest >= self.PartyTimeout
            if not leader:
                if timedOut:
                    # the party leader never made it onto the lookout...
                    for request in partyRequests:
                        self.removeRequest(request.avatarId)
                        self.d_lookoutMatchFailed(request.avatarId, False)

                continue

            partyIds = [request.avatarId for request in partyRequests]
            waitingFor = [avatarId for avatarId in leader.desiredPlayers if avatarId not in partyIds]
            if waitingFor and not timedOut:
                continue

            blocks.append(partyRequests)

        return sorted(blocks, key=lambda block: min([request.timestamp for request in block]))

    def findMatches(self):
        for gameCategory in list(MatchStyleInfo.keys()):
            self.findMatchesForCategory(gameCategory)

    def findMatchesForCategory(self, gameCategory):
        blocks = self.getRequestBlocks(self.getSearchingRequests(gameCategory))
        for gameType in self.getGameTypes(gameCategory):
            styleInfo = self.getStyleInfo(gameCategory, gameType)
            candidates = [block for block in blocks if self.blockAcceptsGameType(block, gameType)]
            if styleInfo.get('inviteOnly'):
                # invite only games are played by the party alone...
                for block in candidates:
                    if block[0].getPartyId():
                        self.createMatch(gameCategory, gameType, block)
                        continue

                    for request in block:
                        self.removeRequest(request.avatarId)
                        self.d_lookoutMatchFailed(request.avatarId, False)
            else:
                while candidates:
                    matchRequests = self.gatherMatch(gameCategory, gameType, candidates)
                    if not matchRequests:
                        break

                    self.createMatch(gameCategory, gameType, matchRequests)
                    candidates = [block for block in candidates if not block[0].matchId]

            blocks = [block for block in blocks if not block[0].matchId and block[0].avatarId in self.requests]

    def blockAcceptsGameType(self, block, gameType):
        for request in block:
            if not request.acceptsGameType(gameType):
                return False

        return True

    def gatherMatch(self, gameCategory, gameType, candidates):
        matchRequests = []
        for block in candidates:
            if not self.WantCrossDistrict and matchRequests and block[0].shardId != matchRequests[0].shardId:
                continue

            newRequests = matchRequests + block
            if len(newRequests) > self.getMaxPlayers(gameCategory, gameType, newRequests):
                continue

            matchRequests = newRequests

        if not matchRequests:
            return None

        if len(matchRequests) < self.getMinPlayers(gameCategory, gameType, matchRequests):
            return None

        return matchRequests

    def createMatch(self, gameCategory, gameType, requests):
        matchId = self.nextMatchId
        self.nextMatchId = (self.nextMatchId % 0xFFFFFFFF) + 1

        match = LookoutMatch(self, matchId, gameCategory, gameType, list(requests))
        self.matches[matchId] = match
        self.notify.debug('Found match %d for avatars: %r' % (matchId, match.getAvatarIds()))

        match.request('Joining')
        return match

    def matchFailed(self, match, restartRequest=True):
        self.notify.debug('Match %d failed (restart=%s).' % (match.matchId, restartRequest))
        for request in list(match.requests):
            request.matchId = 0
            if restartRequest and request.avatarId in self.requests:
                # put the avatar back on the lookout...
                request.timestamp = globalClock.getRealTime()
            else:
                self.requests.pop(request.avatarId, None)

            self.d_lookoutMatchFailed(request.avatarId, restartRequest)

        self.removeMatch(match)

    def removeMatch(self, match):
        self.matches.pop(match.matchId, None)
        match.cleanup()

    def getMatchChance(self, request):
        gameTypes = self.getGameTypes(request.gameCategory)
        if request.gameType != PiratesGlobals.GAME_STYLE_ANY:
            gameTypes = [request.gameType]

        bestChance = 0
        searching = self.getSearchingRequests(request.gameCategory)
        for gameType in gameTypes:
            others = [other for other in searching if other is not request and other.acceptsGameType(gameType)]
            needed = self.getMinPlayers(request.gameCategory, gameType, [request]) - 1
            if needed <= 0:
                return GameTypeGlobals.MATCH_CHANCE_HIGH

            chance = int(100 * len(others) / float(needed))
            bestChance = max(bestChance, min(chance, 100))

        return max(bestChance, GameTypeGlobals.MATCH_CHANCE_LOW)

    def sendFeedback(self):
        for request in self.getSearchingRequests():
            chance = self.getMatchChance(request)
            if chance == request.lastChance:
                continue

            request.lastChance = chance
            self.d_lookoutFeedback(request.avatarId, chance)

    # -------------------------------------------------------------------
    # Districts
    # -------------------------------------------------------------------

    def d_createMatch(self, shardId, matchId, gameCategory, gameType, options, teams):
        self.air.netMessenger.send('matchMakerCreateMatch', [shardId, matchId, gameCategory,
            gameType, options, teams])

    def instanceCreated(self, matchId, shardId, instanceDoId):
        match = self.matches.get(matchId)
        if not match or match.state != 'Creating':
            return

        if shardId != match.hostShardId:
            self.notify.warning('Received instanceCreated for match %d from district %d, '
                'expected district %d!' % (matchId, shardId, match.hostShardId))

            return

        if not instanceDoId:
            self.notify.warning('District %d failed to create match %d!' % (shardId, matchId))
            self.matchFailed(match, restartRequest=True)
            return

        match.instanceDoId = instanceDoId
        match.request('Playing')
        if match.gameCategory == PiratesGlobals.GAME_TYPE_PG:
            # parlor games are played at the district's own tables, there
            # is no instance for us to keep track of...
            self.removeMatch(match)

    def instanceRemoved(self, matchId, shardId, instanceDoId):
        match = self.matches.get(matchId)
        if not match or match.instanceDoId != instanceDoId:
            return

        self.notify.debug('Match %d instance %d was removed from district %d.' % (
            matchId, instanceDoId, shardId))

        self.removeMatch(match)

    def printStatus(self, avatarId):
        self.notify.info('Lookout status: %d requests, %d matches' % (len(self.requests), len(self.matches)))
        for request in list(self.requests.values()):
            self.notify.info('  request: avatar=%d category=%d type=%d district=%d match=%d' % (
                request.avatarId, request.gameCategory, request.gameType, request.shardId,
                request.matchId))

        for match in list(self.matches.values()):
            self.notify.info('  match %d: state=%s category=%d type=%d district=%d avatars=%r' % (
                match.matchId, match.state, match.gameCategory, match.gameType,
                match.hostShardId, match.getAvatarIds()))

    # -------------------------------------------------------------------
    # Avatar messages
    # -------------------------------------------------------------------

    def sendUpdateToAvatar(self, avatarId, fieldName, args):
        dclass = self.air.dclassesByName['DistributedPlayerPirateUD']
        datagram = dclass.aiFormatUpdate(fieldName, avatarId, self.GetPuppetConnectionChannel(avatarId),
            self.air.ourChannel, args)

        self.air.send(datagram)

    def d_requestActivityAccepted(self, avatarId):
        self.sendUpdateToAvatar(avatarId, 'requestActivityAccepted', [])

    def d_lookoutMatchFound(self, avatarId, timeToJoin, matchId):
        self.sendUpdateToAvatar(avatarId, 'lookoutMatchFound', [timeToJoin, matchId])

    def d_lookoutMatchFailed(self, avatarId, restartRequest):
        self.sendUpdateToAvatar(avatarId, 'lookoutMatchFailed', [restartRequest])

    def d_lookoutFeedback(self, avatarId, matchChance):
        self.sendUpdateToAvatar(avatarId, 'lookoutFeedback', [matchChance])
