import builtins
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

# WeaponGlobals needs game resources which are not available to the tests...
sys.modules.setdefault('pirates.battle.WeaponGlobals', MagicMock())

from pirates.piratesbase import PiratesGlobals
from pirates.world import GameTypeGlobals
from pirates.instance import DistributedMatchMakerUD as udModule
from pirates.instance.DistributedMatchMakerUD import DistributedMatchMakerUD
from pirates.instance.DistributedMatchMakerAI import DistributedMatchMakerAI

PVP = PiratesGlobals.GAME_TYPE_PVP
PG = PiratesGlobals.GAME_TYPE_PG
TM = PiratesGlobals.GAME_TYPE_TM
BATTLE = PiratesGlobals.GAME_STYLE_BATTLE
TEAM_BATTLE = PiratesGlobals.GAME_STYLE_TEAM_BATTLE
BLACKJACK = PiratesGlobals.GAME_STYLE_BLACKJACK

SHARD_A = 1000
SHARD_B = 2000


def option(optionId, value):
    return [str(optionId), str(value)]


class MatchMakerUDTests(unittest.TestCase):

    def setUp(self):
        self.air = SimpleNamespace(netMessenger=Mock(), getAvatarIdFromSender=Mock(return_value=0),
            dclassesByName=MagicMock())
        self.mm = DistributedMatchMakerUD(self.air)
        self.mm.MinPlayersOverride = 0
        self.mm.WantCrossDistrict = True
        self.sent = []
        self.mm.sendUpdateToAvatar = lambda avatarId, fieldName, args: self.sent.append(
            (avatarId, fieldName, args))

    def tearDown(self):
        for match in list(self.mm.matches.values()):
            match.cleanup()

    def sentTo(self, avatarId, fieldName):
        return [args for (doId, name, args) in self.sent if doId == avatarId and name == fieldName]

    def request(self, avatarId, gameType=BATTLE, gameCategory=PVP, options=[], shardId=SHARD_A):
        self.mm.requestActivity(avatarId, gameType, gameCategory, options, [], shardId, 2)

    def fromAvatar(self, avatarId):
        self.air.getAvatarIdFromSender.return_value = avatarId

    def getOnlyMatch(self):
        self.assertEqual(len(self.mm.matches), 1)
        return list(self.mm.matches.values())[0]

    def test_request_is_queued_and_accepted(self):
        self.request(1)
        self.assertIn(1, self.mm.requests)
        self.assertEqual(self.sentTo(1, 'requestActivityAccepted'), [[]])
        self.assertEqual(self.mm.matches, {})

    def test_unsupported_activity_fails(self):
        self.request(1, gameCategory=PiratesGlobals.GAME_TYPE_HSA)
        self.assertNotIn(1, self.mm.requests)
        self.assertEqual(self.sentTo(1, 'lookoutMatchFailed'), [[False]])

    def test_free_player_cannot_request_paid_game(self):
        self.mm.requestActivity(1, TEAM_BATTLE, PVP, [], [], SHARD_A, 1)
        self.assertNotIn(1, self.mm.requests)
        self.assertEqual(self.sentTo(1, 'lookoutMatchFailed'), [[False]])

    def test_battle_match_found_joined_and_created(self):
        self.request(1)
        self.request(2, shardId=SHARD_B)
        match = self.getOnlyMatch()
        self.assertEqual(match.state, 'Joining')
        self.assertEqual(self.sentTo(1, 'lookoutMatchFound'), [[PiratesGlobals.LOOKOUT_JOIN_TIMEOUT, match.matchId]])
        self.assertEqual(self.sentTo(2, 'lookoutMatchFound'), [[PiratesGlobals.LOOKOUT_JOIN_TIMEOUT, match.matchId]])

        self.fromAvatar(1)
        self.mm.requestJoin(match.matchId)
        self.air.netMessenger.send.assert_not_called()
        self.fromAvatar(2)
        self.mm.requestJoin(match.matchId)
        self.assertEqual(match.state, 'Creating')
        self.air.netMessenger.send.assert_called_once_with('matchMakerCreateMatch',
            [SHARD_A, match.matchId, PVP, BATTLE, [], [[1], [2]]])

        self.mm.instanceCreated(match.matchId, SHARD_A, 5000)
        self.assertEqual(match.state, 'Playing')
        self.assertEqual(self.mm.requests, {})

        self.mm.instanceRemoved(match.matchId, SHARD_A, 5000)
        self.assertEqual(self.mm.matches, {})

    def test_stale_match_id_is_ignored(self):
        self.request(1)
        self.request(2)
        match = self.getOnlyMatch()
        self.fromAvatar(1)
        self.mm.requestJoin(match.matchId + 100)
        self.assertEqual(match.joined, [])

    def test_min_players_option_is_respected(self):
        self.request(1, options=[option(GameTypeGlobals.GAME_OPTION_MIN_PLAYERS, 3)])
        self.request(2)
        self.assertEqual(self.mm.matches, {})
        self.request(3)
        self.assertEqual(sorted(self.getOnlyMatch().getAvatarIds()), [1, 2, 3])

    def test_skip_with_restart_requeues_everyone(self):
        self.request(1)
        self.request(2)
        match = self.getOnlyMatch()
        self.fromAvatar(1)
        self.mm.skipJoin(match.matchId, False)

        # the match is no longer viable, the other avatar is sent back to searching
        self.assertEqual(self.sentTo(2, 'lookoutMatchFailed'), [[True]])
        self.assertEqual(self.mm.matches, {})
        self.assertIn(1, self.mm.requests)
        self.assertIn(2, self.mm.requests)
        self.assertEqual(self.mm.requests[1].matchId, 0)
        self.assertGreater(self.mm.requests[1].skipUntil, 0)

    def test_skip_with_clear_removes_request(self):
        self.request(1)
        self.request(2)
        match = self.getOnlyMatch()
        self.fromAvatar(2)
        self.mm.skipJoin(match.matchId, True)
        self.assertNotIn(2, self.mm.requests)
        self.assertEqual(self.sentTo(1, 'lookoutMatchFailed'), [[True]])

    def test_join_timeout_drops_idle_avatars(self):
        self.request(1)
        self.request(2, options=[option(GameTypeGlobals.GAME_OPTION_MIN_PLAYERS, 3)])
        self.assertEqual(self.mm.matches, {})
        self.request(3)
        match = self.getOnlyMatch()
        self.fromAvatar(1)
        self.mm.requestJoin(match.matchId)
        self.fromAvatar(2)
        self.mm.requestJoin(match.matchId)

        match._LookoutMatch__joinTimedOut(None)
        self.assertEqual(self.sentTo(3, 'lookoutMatchFailed'), [[False]])
        self.assertNotIn(3, self.mm.requests)

        # avatar 2 wanted at least 3 players, the others go back to searching...
        self.assertEqual(match.state, 'Off')
        self.assertEqual(self.sentTo(1, 'lookoutMatchFailed'), [[True]])
        self.assertEqual(self.mm.requests[1].matchId, 0)

    def test_join_timeout_continues_viable_match(self):
        self.request(1)
        self.request(2, options=[option(GameTypeGlobals.GAME_OPTION_MIN_PLAYERS, 3)])
        self.request(3)
        match = self.getOnlyMatch()
        match.requests[1].options = []
        for avatarId in (1, 2):
            self.fromAvatar(avatarId)
            self.mm.requestJoin(match.matchId)

        match._LookoutMatch__joinTimedOut(None)
        self.assertEqual(match.state, 'Creating')
        self.assertEqual(self.sentTo(3, 'lookoutMatchFailed'), [[False]])

    def test_failed_creation_requeues(self):
        self.request(1)
        self.request(2)
        match = self.getOnlyMatch()
        for avatarId in (1, 2):
            self.fromAvatar(avatarId)
            self.mm.requestJoin(match.matchId)

        self.mm.instanceCreated(match.matchId, SHARD_A, 0)
        self.assertEqual(self.sentTo(1, 'lookoutMatchFailed'), [[True]])
        self.assertEqual(self.mm.requests[1].matchId, 0)

    def test_cancel_request(self):
        self.request(1)
        self.fromAvatar(1)
        self.mm.cancelRequest(0)
        self.assertNotIn(1, self.mm.requests)

    def test_avatar_left_district(self):
        self.request(1)
        self.mm.handleAvatarLeft(1, SHARD_B)
        self.assertIn(1, self.mm.requests)
        self.mm.handleAvatarLeft(1, SHARD_A)
        self.assertNotIn(1, self.mm.requests)

    def test_parlor_game_matches_immediately(self):
        self.request(1, gameType=BLACKJACK, gameCategory=PG)
        match = self.getOnlyMatch()
        self.fromAvatar(1)
        self.mm.requestJoin(match.matchId)
        self.mm.instanceCreated(match.matchId, SHARD_A, 7000)
        self.assertEqual(self.mm.matches, {})
        self.assertEqual(self.mm.requests, {})

    def test_party_waits_for_invitees_and_stays_together(self):
        vip = option(GameTypeGlobals.GAME_OPTION_VIP_PASS, 1)
        desired = option(GameTypeGlobals.GAME_OPTION_DESIRED_PLAYERS, '1,2')
        self.request(1, gameType=TEAM_BATTLE, options=[vip, desired])
        self.request(3, gameType=TEAM_BATTLE)
        self.request(4, gameType=TEAM_BATTLE)
        self.assertEqual(self.mm.matches, {})

        self.request(2, gameType=TEAM_BATTLE, options=[vip, desired])
        match = self.getOnlyMatch()
        teams = match.getTeams()
        self.assertEqual(len(teams), 2)
        self.assertIn(sorted([1, 2]), [sorted(team) for team in teams])

    def test_treasure_map_requires_party(self):
        self.request(1, gameType=PiratesGlobals.GAME_STYLE_TM_BLACK_PEARL, gameCategory=TM)
        self.assertNotIn(1, self.mm.requests)
        self.assertEqual(self.sentTo(1, 'lookoutMatchFailed'), [[False]])

    def test_treasure_map_party_hosted_by_leader(self):
        vip = option(GameTypeGlobals.GAME_OPTION_VIP_PASS, 1)
        desired = option(GameTypeGlobals.GAME_OPTION_DESIRED_PLAYERS, '1,2')
        tm = option(GameTypeGlobals.GAME_OPTION_TM_ID, 99)
        self.request(2, gameType=0, gameCategory=TM, options=[vip, desired], shardId=SHARD_B)
        self.request(1, gameType=0, gameCategory=TM, options=[vip, desired, tm], shardId=SHARD_A)
        match = self.getOnlyMatch()
        for avatarId in (1, 2):
            self.fromAvatar(avatarId)
            self.mm.requestJoin(match.matchId)

        self.air.netMessenger.send.assert_called_once_with('matchMakerCreateMatch',
            [SHARD_A, match.matchId, TM, 0, [vip, desired, tm], [[2, 1]]])

    def test_match_chance_feedback(self):
        self.request(1, gameType=TEAM_BATTLE)
        self.request(2, gameType=TEAM_BATTLE)
        self.mm.sendFeedback()
        self.assertEqual(self.sentTo(1, 'lookoutFeedback'), [[33]])

        # unchanged chances are not sent again
        self.mm.sendFeedback()
        self.assertEqual(len(self.sentTo(1, 'lookoutFeedback')), 1)


class FakeAvatar:

    def __init__(self, doId, name='Pirate', guildId=0):
        self.doId = doId
        self.name = name
        self.guildId = guildId
        self.gameAccess = 2
        self.parent = None
        self.d_lookoutMatchFailed = Mock()
        self.d_requestInvitesResp = Mock()

    def getName(self):
        return self.name

    def getGuildId(self):
        return self.guildId

    def getFriendsList(self):
        return []

    def getInventory(self):
        return SimpleNamespace(getShipDoIdList=lambda: [55])

    def getDeleteEvent(self):
        return 'distObjDelete-%d' % self.doId

    def getParentObj(self):
        return self.parent


class MatchMakerAITests(unittest.TestCase):

    def setUp(self):
        self.air = SimpleNamespace(
            netMessenger=Mock(),
            districtId=SHARD_A,
            ourChannel=12345,
            doId2do={},
            teleportMgr=Mock(avatar2fsm={}),
            pvpManager=Mock(),
            bandManager=Mock(),
            setAI=Mock(),
            dclassesByName=MagicMock())
        self.air.pvpManager.isAvatarInPVP.return_value = False
        self.mm = DistributedMatchMakerAI(self.air)
        self.mm.doId = 4700
        self.mm.sendUpdate = Mock()
        self.mm.sendUpdateToAvatar = Mock()

    def tearDown(self):
        self.mm.ignoreAll()
        for matchId in list(self.mm.matchSetups.keys()):
            taskMgr.remove(self.mm.getArrivalTaskName(matchId))

    def addAvatar(self, doId, **kwargs):
        avatar = FakeAvatar(doId, **kwargs)
        self.air.doId2do[doId] = avatar
        return avatar

    def test_request_activity_forwards_to_uberdog(self):
        avatar = self.addAvatar(1)
        self.mm.requestActivity(avatar, BATTLE, PVP, [], [55, 66])
        self.mm.sendUpdate.assert_called_once_with('requestActivity', [1, BATTLE, PVP, [], [55],
            SHARD_A, 2])

        messenger.send(avatar.getDeleteEvent())
        self.air.netMessenger.send.assert_called_once_with('matchMakerAvatarLeft', [1, SHARD_A])

    def test_request_activity_refused_while_in_pvp(self):
        avatar = self.addAvatar(1)
        self.air.pvpManager.isAvatarInPVP.return_value = True
        self.mm.requestActivity(avatar, BATTLE, PVP, [], [])
        self.mm.sendUpdate.assert_not_called()
        avatar.d_lookoutMatchFailed.assert_called_once_with(False)

    def test_request_invites_crew(self):
        avatar = self.addAvatar(1, name='Jack')
        self.air.bandManager.getBandMemberIds.return_value = [1, 2, 3]
        options = [option(GameTypeGlobals.GAME_OPTION_VIP_PASS, 1)]
        self.mm.requestInvites(avatar, [PiratesGlobals.LOOKOUT_INVITE_CREW], PVP, TEAM_BATTLE, options, [])

        inviteOptions = [option(GameTypeGlobals.GAME_OPTION_VIP_PASS, 1),
            option(GameTypeGlobals.GAME_OPTION_DESIRED_PLAYERS, '1,2,3')]
        self.mm.sendUpdateToAvatar.assert_any_call(2, 'requestLookoutInvite', [1, 'Jack', PVP,
            TEAM_BATTLE, inviteOptions])
        self.mm.sendUpdateToAvatar.assert_any_call(3, 'requestLookoutInvite', [1, 'Jack', PVP,
            TEAM_BATTLE, inviteOptions])
        avatar.d_requestInvitesResp.assert_called_once_with([2, 3], 0)

    def test_request_invites_skips_busy_avatars(self):
        avatar = self.addAvatar(1)
        self.addAvatar(2)
        self.air.teleportMgr.avatar2fsm[2] = object()
        self.mm.requestInvites(avatar, [PiratesGlobals.LOOKOUT_INVITE_NONE], PVP, BATTLE, [], [2])
        self.mm.sendUpdateToAvatar.assert_not_called()
        avatar.d_requestInvitesResp.assert_called_once_with([], 1)

    def test_create_match_for_other_district_is_ignored(self):
        self.mm.handleCreateMatch(SHARD_B, 1, PVP, BATTLE, [], [[1], [2]])
        self.air.pvpManager.createPVPInstance.assert_not_called()
        self.mm.sendUpdate.assert_not_called()

    def test_create_pvp_match(self):
        self.addAvatar(1)
        self.addAvatar(2)
        instance = SimpleNamespace(doId=5000, getDeleteEvent=lambda: 'distObjDelete-5000')
        self.air.pvpManager.createPVPInstance.return_value = instance
        self.mm.handleCreateMatch(SHARD_A, 7, PVP, BATTLE, [], [[1], [2]])

        self.air.pvpManager.createPVPInstance.assert_called_once_with(BATTLE, [[1], [2]])
        self.mm.sendUpdate.assert_called_once_with('instanceCreated', [7, SHARD_A, 5000])

        messenger.send('distObjDelete-5000')
        self.mm.sendUpdate.assert_called_with('instanceRemoved', [7, SHARD_A, 5000])

    def test_create_pvp_match_failure(self):
        self.addAvatar(1)
        self.air.pvpManager.createPVPInstance.return_value = None
        self.mm.handleCreateMatch(SHARD_A, 7, PVP, BATTLE, [], [[1]])
        self.mm.sendUpdate.assert_called_once_with('instanceCreated', [7, SHARD_A, 0])

    def test_create_match_waits_for_remote_avatars(self):
        self.addAvatar(1)
        instance = SimpleNamespace(doId=5000, getDeleteEvent=lambda: 'distObjDelete-5000')
        self.air.pvpManager.createPVPInstance.return_value = instance
        self.mm.handleCreateMatch(SHARD_A, 7, PVP, BATTLE, [], [[1], [2]])

        self.air.setAI.assert_called_once_with(2, self.air.ourChannel)
        self.air.pvpManager.createPVPInstance.assert_not_called()

        avatar = self.addAvatar(2)
        messenger.send('generate-2', [avatar])
        self.air.pvpManager.createPVPInstance.assert_called_once_with(BATTLE, [[1], [2]])

    def test_create_match_arrival_timeout(self):
        self.addAvatar(1)
        self.air.pvpManager.createPVPInstance.return_value = None
        self.mm.handleCreateMatch(SHARD_A, 7, PVP, BATTLE, [], [[1], [2]])
        self.mm._DistributedMatchMakerAI__arrivalTimedOut(7)
        self.air.pvpManager.createPVPInstance.assert_called_once_with(BATTLE, [[1]])

    def test_create_parlor_match(self):
        avatar = self.addAvatar(1)
        area = object()
        table = SimpleNamespace(doId=8000, getOpenSeatCount=lambda: 3, getParentObj=lambda: area)
        self.mm.findParlorTable = Mock(return_value=table)
        self.mm.handleCreateMatch(SHARD_A, 7, PG, BLACKJACK, [], [[1]])

        self.mm.findParlorTable.assert_called_once_with(BLACKJACK, 1)
        self.air.teleportMgr.teleportToArea.assert_called_once_with(avatar, area)
        self.mm.sendUpdate.assert_called_once_with('instanceCreated', [7, SHARD_A, 8000])


if __name__ == '__main__':
    unittest.main()
