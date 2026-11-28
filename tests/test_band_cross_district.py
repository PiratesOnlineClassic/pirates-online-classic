import unittest
from collections import defaultdict
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pirates.band.test_band_ai import FakeAvatar, FakeMember

from pirates.band import BandConstance
from pirates.band import DistributedPirateBandManagerAI as bandModule
from pirates.band.DistributedPirateBandManagerAI import DistributedPirateBandManagerAI
from pirates.band.DistributedCrewMatchAI import DistributedCrewMatchAI


class FakeNetMessenger:
    """
    Delivers net messages to every district, including the sender, like the
    real NetMessenger does.
    """

    def __init__(self):
        self.handlers = defaultdict(list)
        self.sent = []

    def accept(self, message, obj, handler):
        self.handlers[message].append(handler)

    def ignore(self, message, obj):
        pass

    def send(self, message, sentArgs=[]):
        self.sent.append((message, sentArgs))
        for handler in list(self.handlers[message]):
            handler(*sentArgs)


class District:

    def __init__(self, net, doId, online):
        self.channels = iter(range(doId * 100, doId * 100 + 100))
        self.sender = [0]
        self.air = SimpleNamespace(
            doId2do={},
            dclassesByName=defaultdict(Mock),
            netMessenger=net,
            setOwner=Mock(),
            clientAddInterest=Mock(),
            clientRemoveInterest=Mock(),
            logPotentialHacker=Mock(),
            getActivated=lambda avatarId, callback: callback(avatarId, avatarId in online),
            send=Mock(),
            ourChannel=doId * 10,
            allocateChannel=lambda: next(self.channels),
            getAvatarIdFromSender=lambda: self.sender[0],
            getAccountIdFromSender=lambda: 1000 + self.sender[0],
        )

        self.manager = DistributedPirateBandManagerAI(self.air)
        self.manager.doId = doId
        self.manager.sendUpdateToAvatarId = Mock()
        self.air.bandManager = self.manager

        self.crewMatch = DistributedCrewMatchAI(self.air)
        self.crewMatch.doId = doId + 1
        self.crewMatch.sendUpdateToAvatarId = Mock()
        self.air.crewMatch = self.crewMatch

        # announceGenerate without the distributed object machinery:
        for message, handler in (
                ('bandRequest', self.manager.handleBandRequest),
                ('bandRelayToAvatar', self.manager.handleRelayToAvatar),
                ('bandAvatarBandId', self.manager.handleAvatarBandId),
                ('bandInviteRequest', self.manager.handleInviteRequest),
                ('bandInviteCancel', self.manager.handleInviteCancel),
                ('bandInviteAccepted', self.manager.handleInviteAccepted),
                ('bandVerifyMember', self.manager.handleVerifyMember),
                ('bandVerifyMemberResp', self.manager.handleVerifyMemberResp),
                ('crewMatchCrewAdd', self.crewMatch.handleRemoteCrewAdd),
                ('crewMatchCrewRemove', self.crewMatch.handleRemoteCrewRemove),
                ('crewMatchJoinRequest', self.crewMatch.handleJoinRequest),
                ('crewMatchJoinResponse', self.crewMatch.handleJoinResponse)):
            net.accept(message, self, handler)

    def addAvatar(self, doId, name, **kwargs):
        avatar = FakeAvatar(doId, name, **kwargs)
        avatar.d_setBandId = Mock()
        self.air.doId2do[doId] = avatar
        return avatar

    def sentTo(self, obj, avatarId, fieldName):
        return [c[0][2] for c in obj.sendUpdateToAvatarId.call_args_list
                if c[0][0] == avatarId and c[0][1] == fieldName]

    def cleanup(self):
        self.manager.ignoreAll()
        self.crewMatch.ignoreAll()


class CrossDistrictTestBase(unittest.TestCase):

    def setUp(self):
        self.patcher = patch.object(bandModule, 'DistributedBandMemberAI', FakeMember)
        self.patcher.start()

        self.net = FakeNetMessenger()
        self.online = set()
        self.a = District(self.net, 300, self.online)
        self.b = District(self.net, 400, self.online)

    def tearDown(self):
        for district in (self.a, self.b):
            for avatarId in list(district.air.doId2do.keys()):
                taskMgr.remove(district.manager.uniqueName('verify-member-%d' % avatarId))
                taskMgr.remove(district.manager.uniqueName('check-member-%d' % avatarId))
                taskMgr.remove(district.crewMatch.uniqueName('join-crew-%d' % avatarId))

            district.cleanup()

        self.patcher.stop()

    def addAvatar(self, district, doId, name, **kwargs):
        self.online.add(doId)
        return district.addAvatar(doId, name, **kwargs)


class TestCrossDistrictInvites(CrossDistrictTestBase):

    def test_invite_avatar_on_another_district(self):
        self.addAvatar(self.a, 1, 'Jack')
        will = self.addAvatar(self.b, 2, 'Will')

        self.a.sender[0] = 1
        self.a.manager.requestInvite(2)
        self.assertEqual(self.b.sentTo(self.b.manager, 2, 'invitationFrom'), [[1, 'Jack']])
        self.assertEqual(self.b.manager.invites, {2: 1})

        self.b.sender[0] = 2
        self.b.manager.invitationResponce(1, BandConstance.outcome_ok)

        # the inviter's district starts the crew
        band = self.a.manager.getBandFromAvatar(1)
        self.assertIsNotNone(band)
        self.assertEqual(band.managerId, 1)
        self.assertEqual(sorted(band.getMemberIds()), [1, 2])
        self.assertFalse(self.b.manager.hasBand(2))
        self.assertEqual(will.getBandId(), (300, band.bandId))
        self.assertEqual(self.a.sentTo(self.a.manager, 1, 'requestOutCome'), [[2, BandConstance.outcome_ok]])
        self.assertEqual(self.a.manager.remoteInvites, {})

    def test_invite_offline_avatar(self):
        self.addAvatar(self.a, 1, 'Jack')
        self.a.sender[0] = 1
        self.a.manager.requestInvite(2)
        self.assertEqual(self.a.sentTo(self.a.manager, 1, 'requestOutCome'), [[2, BandConstance.outcome_not_online]])
        self.assertEqual(self.a.manager.remoteInvites, {})

    def test_decline_and_already_in_band_across_districts(self):
        self.addAvatar(self.a, 1, 'Jack')
        self.addAvatar(self.b, 2, 'Will')
        self.a.sender[0] = 1
        self.a.manager.requestInvite(2)
        self.b.sender[0] = 2
        self.b.manager.invitationResponce(1, BandConstance.outcome_declined)

        # the outcome is relayed back to the inviter's district
        relays = [args for message, args in self.net.sent if message == 'bandRelayToAvatar']
        self.assertIn([1, 'requestOutCome', [2, BandConstance.outcome_declined]], relays)
        self.assertEqual(self.a.sentTo(self.a.manager, 1, 'requestOutCome'), [[2, BandConstance.outcome_declined]])
        self.assertEqual(self.a.manager.remoteInvites, {})

    def test_cancel_invite_across_districts(self):
        self.addAvatar(self.a, 1, 'Jack')
        self.addAvatar(self.b, 2, 'Will')
        self.a.sender[0] = 1
        self.a.manager.requestInvite(2)
        self.a.manager.requestCancel(2)
        self.assertEqual(self.b.sentTo(self.b.manager, 2, 'invitationCancel'), [[1]])
        self.assertEqual(self.b.manager.invites, {})

    def test_invite_into_crew_owned_by_another_district(self):
        # Jack's crew is owned by district a, but Jack is now on district b
        self.addAvatar(self.a, 1, 'Jack')
        self.addAvatar(self.a, 3, 'Liz')
        self.a.sender[0] = 1
        self.a.manager.requestInvite(3)
        self.a.sender[0] = 3
        self.a.manager.invitationResponce(1, BandConstance.outcome_ok)
        band = self.a.manager.getBandFromAvatar(1)

        jack = self.a.air.doId2do.pop(1)
        self.b.air.doId2do[1] = jack
        will = self.addAvatar(self.b, 2, 'Will')

        self.b.sender[0] = 1
        self.b.manager.requestInvite(2)
        self.b.sender[0] = 2
        self.b.manager.invitationResponce(1, BandConstance.outcome_ok)
        self.assertEqual(sorted(band.getMemberIds()), [1, 2, 3])
        self.assertFalse(self.b.manager.hasBand(1))
        self.assertEqual(will.getBandId(), (300, band.bandId))


class TestStaleBandIds(CrossDistrictTestBase):

    def test_stale_clear_from_previous_band_is_ignored(self):
        will = self.addAvatar(self.b, 2, 'Will')
        will.bandId = (500, 7)

        # band manager 300 removed will from it's crew, but will has since
        # joined crew 7 on band manager 500
        self.b.manager.handleAvatarBandId(2, 0, 0, 300)
        self.assertEqual(will.getBandId(), (500, 7))
        will.d_setBandId.assert_called_once_with(500, 7)

        self.b.manager.handleAvatarBandId(2, 0, 0, 500)
        self.assertEqual(will.getBandId(), (0, 0))

    def test_verify_clears_dissolved_band(self):
        will = self.addAvatar(self.b, 2, 'Will')
        will.bandId = (300, 7)
        self.b.manager.verifyAvatarBandId(will)
        self.assertEqual(will.getBandId(), (0, 0))

    def test_verify_keeps_existing_band(self):
        self.addAvatar(self.a, 1, 'Jack')
        self.addAvatar(self.a, 2, 'Will')
        self.a.sender[0] = 1
        self.a.manager.requestInvite(2)
        self.a.sender[0] = 2
        self.a.manager.invitationResponce(1, BandConstance.outcome_ok)
        band = self.a.manager.getBandFromAvatar(1)

        will = self.a.air.doId2do.pop(2)
        self.b.air.doId2do[2] = will
        self.b.manager.verifyAvatarBandId(will)
        self.assertEqual(will.getBandId(), (300, band.bandId))
        self.assertFalse(taskMgr.hasTaskNamed(self.b.manager.uniqueName('verify-member-2')))

    def test_verify_on_owning_district(self):
        will = self.addAvatar(self.a, 2, 'Will')
        will.bandId = (300, 7)
        self.a.manager.verifyAvatarBandId(will)
        self.assertEqual(will.getBandId(), (0, 0))


class TestCrossDistrictCrewMatch(CrossDistrictTestBase):

    def test_crew_on_another_district_is_matched(self):
        self.addAvatar(self.a, 1, 'Jack', level=10)
        will = self.addAvatar(self.b, 2, 'Will', level=11)

        self.a.sender[0] = 1
        self.a.crewMatch.requestCrewOfOneCreation()
        self.a.crewMatch.requestCrewAdd(5, 1, 1)
        self.assertTrue(self.b.crewMatch.crewLookout[1].remote)

        self.b.sender[0] = 2
        self.b.crewMatch.requestInitialAvatarAdd(1)
        self.assertEqual(self.b.sentTo(self.b.crewMatch, 2, 'responseInitialAvatarAdd'), [[1, 'Jack', '', 1]])
        self.b.crewMatch.requestInitialAvatarAddResponse(1, 1)

        band = self.a.manager.getBandFromAvatar(1)
        self.assertEqual(sorted(band.getMemberIds()), [1, 2])
        self.assertEqual(will.getBandId(), (300, band.bandId))
        self.assertEqual(self.b.sentTo(self.b.crewMatch, 2, 'responseInitialAvatarAddResponse'), [[1]])
        self.assertEqual(self.a.sentTo(self.a.crewMatch, 1, 'notifySponsorNewMember'), [['Will']])
        self.assertEqual(self.b.crewMatch.pendingJoins, {})

    def test_lookout_avatar_offered_remote_crew(self):
        self.addAvatar(self.a, 1, 'Jack', level=10)
        self.addAvatar(self.b, 2, 'Will', level=11)
        self.b.sender[0] = 2
        self.b.crewMatch.requestPutAvatarOnLookoutList(1)

        self.a.sender[0] = 1
        self.a.crewMatch.requestCrewOfOneCreation()
        self.a.crewMatch.requestCrewAdd(5, 1, 1)
        self.assertEqual(self.b.sentTo(self.b.crewMatch, 2, 'responseCrewFound'), [['Jack', 1, '']])

        self.b.crewMatch.requestAcceptInvite(1)
        self.assertTrue(self.a.manager.hasBand(2))
        self.assertNotIn(2, self.b.crewMatch.avatarLookout)

    def test_removed_crew_leaves_every_district(self):
        self.addAvatar(self.a, 1, 'Jack', level=10)
        self.a.sender[0] = 1
        self.a.crewMatch.requestCrewOfOneCreation()
        self.a.crewMatch.requestCrewAdd(5, 1, 1)
        self.a.crewMatch.requestCrewDelete()
        self.assertNotIn(1, self.b.crewMatch.crewLookout)

    def test_full_remote_crew_rejects_join(self):
        self.addAvatar(self.a, 1, 'Jack', level=10)
        self.addAvatar(self.b, 2, 'Will', level=11)
        self.a.sender[0] = 1
        self.a.crewMatch.requestCrewOfOneCreation()
        self.a.crewMatch.requestCrewAdd(5, 1, 1)

        # the crew of one is cancelled, the other district hasn't heard yet
        self.a.crewMatch.crewsOfOne.discard(1)
        self.b.sender[0] = 2
        self.b.crewMatch.requestInitialAvatarAdd(1)
        self.b.crewMatch.requestInitialAvatarAddResponse(1, 1)
        self.assertEqual(self.b.sentTo(self.b.crewMatch, 2, 'responseInitialAvatarAddResponse'), [[0]])
        self.assertFalse(self.a.manager.hasBand(2))


if __name__ == '__main__':
    unittest.main()
