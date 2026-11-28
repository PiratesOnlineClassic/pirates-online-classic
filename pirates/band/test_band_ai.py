import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

import sys
try:
    from pirates.reputation import ReputationGlobals
except (IOError, OSError):
    # game resources (WeaponGlobals.pkl) are not available
    sys.modules['pirates.reputation.ReputationGlobals'] = Mock()

from collections import defaultdict

from otp.ai import AIInterestHandles
from pirates.band import BandConstance
from pirates.band import DistributedPirateBandManagerAI as bandModule
from pirates.band.DistributedPirateBandManagerAI import DistributedPirateBandManagerAI
from pirates.band.DistributedCrewMatchAI import DistributedCrewMatchAI, PVP_ISLAND_ONE
from pirates.band.DistributedBandMemberAI import DistributedBandMemberAI


class FakeMember(DistributedBandMemberAI):
    """DistributedBandMemberAI that records instead of touching the network."""

    def __init__(self, air):
        DistributedBandMemberAI.__init__(self, air)
        self.sent = []
        self.deleted = False

    def generateWithRequiredAndId(self, doId, parentId, zoneId, optionalFields=[]):
        self.doId = doId
        self.parentId = parentId
        self.zoneId = zoneId

    def sendUpdate(self, fieldName, args):
        self.sent.append((fieldName, args))

    def requestDelete(self):
        self.deleted = True


class FakeAvatar:

    def __init__(self, doId, name, hp=100, maxHp=100, level=5, island=''):
        self.doId = doId
        self.name = name
        self.hp = hp
        self.maxHp = maxHp
        self.level = level
        self.island = island
        self.bandId = (0, 0)
        self.activeShipId = 0

    def getName(self):
        return self.name

    def getHp(self):
        return [self.hp, 0]

    def getMaxHp(self):
        return self.maxHp

    def getBandId(self):
        return self.bandId

    def setBandId(self, bandManagerId, bandId):
        self.bandId = (bandManagerId, bandId)

    def b_setBandId(self, bandManagerId, bandId):
        self.setBandId(bandManagerId, bandId)

    def getDISLid(self):
        return 1000 + self.doId

    def getDeleteEvent(self):
        return 'distObjDelete-%d' % self.doId

    def getActiveShipId(self):
        return self.activeShipId

    def getParentObj(self):
        return None

    def getInventory(self):
        return None

    def getLevel(self):
        return self.level

    def getCurrentIsland(self):
        return self.island


class BandTestBase(unittest.TestCase):

    def setUp(self):
        self.channels = iter(range(5000, 6000))
        self.sender = [0]
        self.air = SimpleNamespace(
            doId2do={},
            dclassesByName=defaultdict(Mock),
            netMessenger=Mock(),
            setOwner=Mock(),
            clientAddInterest=Mock(),
            clientRemoveInterest=Mock(),
            logPotentialHacker=Mock(),
            getActivated=Mock(),
            send=Mock(),
            ourChannel=4000,
            allocateChannel=lambda: next(self.channels),
            getAvatarIdFromSender=lambda: self.sender[0],
            getAccountIdFromSender=lambda: 1000 + self.sender[0],
        )

        self.patcher = patch.object(bandModule, 'DistributedBandMemberAI', FakeMember)
        self.patcher.start()

        self.manager = DistributedPirateBandManagerAI(self.air)
        self.manager.doId = 300
        self.manager.sendUpdateToAvatarId = Mock()
        self.air.bandManager = self.manager

        self.crewMatch = DistributedCrewMatchAI(self.air)
        self.crewMatch.doId = 301
        self.crewMatch.sendUpdateToAvatarId = Mock()
        self.air.crewMatch = self.crewMatch

    def tearDown(self):
        self.manager.ignoreAll()
        self.crewMatch.ignoreAll()
        self.patcher.stop()

    def addAvatar(self, doId, name, **kwargs):
        avatar = FakeAvatar(doId, name, **kwargs)
        self.air.doId2do[doId] = avatar
        return avatar

    def sentTo(self, obj, avatarId, fieldName):
        return [c[0][2] for c in obj.sendUpdateToAvatarId.call_args_list
                if c[0][0] == avatarId and c[0][1] == fieldName]

    def makeCrew(self, leaderId, *memberIds):
        for memberId in memberIds:
            self.sender[0] = leaderId
            self.manager.requestInvite(memberId)
            self.sender[0] = memberId
            self.manager.invitationResponce(leaderId, BandConstance.outcome_ok)

        return self.manager.getBandFromAvatar(leaderId)


class TestBandManager(BandTestBase):

    def test_invite_and_accept_creates_band(self):
        self.addAvatar(1, 'Jack')
        self.addAvatar(2, 'Will')

        self.sender[0] = 1
        self.manager.requestInvite(2)
        self.assertEqual(self.sentTo(self.manager, 2, 'invitationFrom'), [[1, 'Jack']])

        self.sender[0] = 2
        self.manager.invitationResponce(1, BandConstance.outcome_ok)
        self.assertEqual(self.sentTo(self.manager, 1, 'requestOutCome'), [[2, BandConstance.outcome_ok]])

        band = self.manager.getBandFromAvatar(1)
        self.assertIs(band, self.manager.getBandFromAvatar(2))
        self.assertEqual(band.managerId, 1)
        self.assertEqual(band.getMember(1).getIsManager(), 1)
        self.assertEqual(band.getMember(2).getIsManager(), 0)
        self.assertEqual(band.getMember(2).getBandId(), (300, band.bandId))
        self.assertEqual(band.getMember(2).parentId, 300)
        self.assertEqual(band.getMember(2).zoneId, band.zoneId)
        self.assertEqual(self.air.doId2do[2].getBandId(), (300, band.bandId))

        member = band.getMember(2)
        self.air.setOwner.assert_any_call(member.doId, 1002 << 32 | 2)
        self.air.clientAddInterest.assert_any_call(member.GetPuppetConnectionChannel(2),
            AIInterestHandles.PIRATES_BAND, 300, band.zoneId, False)

    def test_decline(self):
        self.addAvatar(1, 'Jack')
        self.addAvatar(2, 'Will')
        self.sender[0] = 1
        self.manager.requestInvite(2)
        self.sender[0] = 2
        self.manager.invitationResponce(1, BandConstance.outcome_declined)
        self.assertEqual(self.sentTo(self.manager, 1, 'requestOutCome'), [[2, BandConstance.outcome_declined]])
        self.assertFalse(self.manager.hasBand(1))

    def test_invite_rejections(self):
        self.addAvatar(1, 'Jack')
        self.addAvatar(2, 'Will')
        self.addAvatar(3, 'Liz')
        self.sender[0] = 1
        self.manager.requestInvite(99)
        self.manager.requestInvite(2)
        self.sender[0] = 3
        self.manager.requestInvite(2)
        self.assertEqual(self.sentTo(self.manager, 1, 'requestOutCome'), [[99, BandConstance.outcome_not_online]])
        self.assertEqual(self.sentTo(self.manager, 3, 'requestOutCome'), [[2, BandConstance.outcome_already_invited]])

        self.sender[0] = 2
        self.manager.invitationResponce(1, BandConstance.outcome_ok)
        self.sender[0] = 3
        self.manager.requestInvite(2)
        self.assertEqual(self.sentTo(self.manager, 3, 'requestOutCome')[-1], [2, BandConstance.outcome_already_in_Band])

        # a non captain can't invite
        self.sender[0] = 2
        self.manager.requestInvite(3)
        self.assertEqual(self.sentTo(self.manager, 2, 'requestOutCome'), [[3, BandConstance.outcome_declined]])

    def test_band_full(self):
        for avatarId in range(1, BandConstance.MAX_BAND_MEMBERS + 2):
            self.addAvatar(avatarId, 'Pirate%d' % avatarId)

        band = self.makeCrew(1, *range(2, BandConstance.MAX_BAND_MEMBERS + 1))
        self.assertTrue(band.isFull())
        self.sender[0] = 1
        lastId = BandConstance.MAX_BAND_MEMBERS + 1
        self.manager.requestInvite(lastId)
        self.assertEqual(self.sentTo(self.manager, 1, 'requestOutCome')[-1], [lastId, BandConstance.outcome_full])

    def test_cancel_invite(self):
        self.addAvatar(1, 'Jack')
        self.addAvatar(2, 'Will')
        self.sender[0] = 1
        self.manager.requestInvite(2)
        self.manager.requestCancel(2)
        self.assertEqual(self.sentTo(self.manager, 2, 'invitationCancel'), [[1]])
        self.sender[0] = 2
        self.manager.invitationResponce(1, BandConstance.outcome_ok)
        self.assertFalse(self.manager.hasBand(2))

    def test_leave_and_kick_and_promotion(self):
        for avatarId in (1, 2, 3, 4):
            self.addAvatar(avatarId, 'Pirate%d' % avatarId)

        band = self.makeCrew(1, 2, 3, 4)
        kicked = band.getMember(4)

        # crew mates can't kick
        self.sender[0] = 2
        self.manager.requestRemove(3)
        self.assertTrue(self.manager.hasBand(3))
        self.air.logPotentialHacker.assert_called()

        self.sender[0] = 1
        self.manager.requestRemove(4)
        self.assertFalse(self.manager.hasBand(4))
        self.assertTrue(kicked.deleted)
        self.assertEqual(self.air.doId2do[4].getBandId(), (0, 0))
        self.air.clientRemoveInterest.assert_any_call(kicked.GetPuppetConnectionChannel(4),
            AIInterestHandles.PIRATES_BAND, False)

        # captain leaves, next crew mate is promoted
        self.manager.requestRemove(1)
        self.assertFalse(self.manager.hasBand(1))
        self.assertEqual(band.managerId, 2)
        self.assertIn(('setIsManager', [1]), band.getMember(2).sent)

        # crew of one is disbanded
        self.sender[0] = 3
        self.manager.requestRemove(3)
        self.assertFalse(self.manager.hasBand(2))
        self.assertNotIn(band.bandId, self.manager.bands)

    def test_crew_icon(self):
        for avatarId in (1, 2, 3):
            self.addAvatar(avatarId, 'Pirate%d' % avatarId)

        self.makeCrew(1, 2, 3)
        self.sender[0] = 1
        self.manager.requestCrewIconUpdate(4)
        for avatarId in (1, 2, 3):
            self.assertEqual(self.sentTo(self.manager, avatarId, 'receiveUpdatedCrewIcon'), [[4]])

        self.sender[0] = 2
        self.manager.requestCrewIconUpdate(1)
        self.assertEqual(self.sentTo(self.manager, 2, 'receiveUpdatedCrewIcon')[-1], [4])
        self.assertEqual(len(self.sentTo(self.manager, 3, 'receiveUpdatedCrewIcon')), 1)

    def test_hp_update(self):
        jack = self.addAvatar(1, 'Jack')
        self.addAvatar(2, 'Will')
        band = self.makeCrew(1, 2)
        jack.hp = 40
        self.manager.updateAvatarHp(jack)
        self.assertEqual(band.getMember(1).getHp(), 40)
        self.assertIn(('setHp', [40]), band.getMember(1).sent)

    def test_ship_info_update(self):
        jack = self.addAvatar(1, 'Jack')
        self.addAvatar(2, 'Will')
        band = self.makeCrew(1, 2)
        ship = SimpleNamespace(doId=700, getShipClass=lambda: 3, getName=lambda: 'Pearl',
            getCaptainId=lambda: 1, getCrew=lambda: [1], getMaxCrew=lambda: 4)
        self.air.doId2do[700] = ship
        jack.activeShipId = 700
        self.manager.updateAvatarShipInfo(jack)
        member = band.getMember(1)
        self.assertEqual(member.getShipInfo(), (700, 'Pearl', 3, []))
        self.assertTrue(member.getShipHasSpace())
        self.assertIn(('setShipDeployMessage', [1, 'Pearl', 'Unknown']), member.sent)

    def test_member_logout_removed(self):
        self.addAvatar(1, 'Jack')
        self.addAvatar(2, 'Will')
        self.addAvatar(3, 'Liz')
        band = self.makeCrew(1, 2, 3)
        del self.air.doId2do[3]
        self.manager._DistributedPirateBandManagerAI__handleMemberActivated(3, 1)
        self.assertTrue(self.manager.hasBand(3))
        self.manager._DistributedPirateBandManagerAI__handleMemberActivated(3, 0)
        self.assertFalse(self.manager.hasBand(3))
        self.assertEqual(len(band.members), 2)

    def test_remote_band_requests_are_forwarded(self):
        avatar = self.addAvatar(5, 'Remote')
        avatar.bandId = (999, 1)
        self.sender[0] = 5
        self.manager.requestRemove(5)
        self.air.netMessenger.send.assert_called_with('bandRequest', ['requestRemove', 5, [5]])

        # avatars without a crew don't generate network traffic
        self.air.netMessenger.send.reset_mock()
        self.addAvatar(6, 'Lonely')
        self.sender[0] = 6
        self.manager.requestCrewIconUpdate(0)
        self.air.netMessenger.send.assert_not_called()

    def test_forwarded_requests_handled_by_owner(self):
        self.addAvatar(1, 'Jack')
        self.addAvatar(2, 'Will')
        band = self.makeCrew(1, 2)
        # add a member from another district
        self.manager.handleBandRequest('addMember', 1, [[3, 1003, 'Liz', 50, 100]])
        self.assertTrue(self.manager.hasBand(3))
        self.air.netMessenger.send.assert_any_call('bandAvatarBandId', [3, 300, band.bandId])
        self.assertEqual(self.sentTo(self.manager, 1, 'requestOutCome')[-1], [3, BandConstance.outcome_ok])

        # the remote member's district is told about hp changes through the owner
        self.manager.handleBandRequest('updateMemberHp', 3, [25, 100])
        self.assertEqual(band.getMember(3).getHp(), 25)

        self.manager.handleBandRequest('requestRemove', 3, [3])
        self.assertFalse(self.manager.hasBand(3))

    def test_relay_to_avatar(self):
        self.addAvatar(1, 'Jack')
        self.manager.handleRelayToAvatar(1, 'invitationFrom', [2, 'Will'])
        self.manager.handleRelayToAvatar(1, 'setBandId', [0, 0])
        self.manager.handleRelayToAvatar(9, 'invitationFrom', [2, 'Will'])
        self.manager.sendUpdateToAvatarId.assert_called_once_with(1, 'invitationFrom', [2, 'Will'])


class TestCrewMatch(BandTestBase):

    def test_initial_avatar_add_joins_crew_of_one(self):
        self.addAvatar(1, 'Jack', level=10)
        self.addAvatar(2, 'Will', level=12)

        self.sender[0] = 1
        self.crewMatch.requestCrewOfOneCreation()
        self.crewMatch.requestCrewAdd(5, 1, 1)
        self.assertEqual(self.sentTo(self.crewMatch, 1, 'responseCrewAdd'), [[1]])

        self.sender[0] = 2
        self.crewMatch.requestInitialAvatarAdd(1)
        self.assertEqual(self.sentTo(self.crewMatch, 2, 'responseInitialAvatarAdd'), [[1, 'Jack', '', 1]])

        self.crewMatch.requestInitialAvatarAddResponse(1, 1)
        self.assertEqual(self.sentTo(self.crewMatch, 2, 'responseInitialAvatarAddResponse'), [[1]])
        self.assertEqual(self.sentTo(self.crewMatch, 1, 'notifySponsorNewMember'), [['Will']])
        band = self.manager.getBandFromAvatar(2)
        self.assertEqual(band.managerId, 1)
        self.assertNotIn(1, self.crewMatch.crewsOfOne)

    def test_no_crew_found_level_range_and_type(self):
        self.addAvatar(1, 'Jack', level=30)
        self.addAvatar(2, 'Will', level=2)
        self.addAvatar(3, 'Liz', level=30, island=PVP_ISLAND_ONE)

        self.sender[0] = 1
        self.crewMatch.requestCrewOfOneCreation()
        self.crewMatch.requestCrewAdd(5, 1, 1)
        self.sender[0] = 2
        self.crewMatch.requestInitialAvatarAdd(1)
        self.assertEqual(self.sentTo(self.crewMatch, 2, 'responseInitialAvatarAdd'), [[0, '', '', 1]])

        self.sender[0] = 3
        self.crewMatch.requestInitialAvatarAdd(2)
        self.assertEqual(self.sentTo(self.crewMatch, 3, 'responseInitialAvatarAdd'), [[0, '', '', 2]])

    def test_lookout_list_offer_and_accept(self):
        self.addAvatar(1, 'Jack', level=10)
        self.addAvatar(2, 'Will', level=10)
        self.addAvatar(3, 'Liz', level=10)
        self.makeCrew(1, 2)

        self.sender[0] = 3
        self.crewMatch.requestPutAvatarOnLookoutList(1)

        self.sender[0] = 1
        self.crewMatch.requestCrewAdd(5, 1, 1)
        self.assertEqual(self.sentTo(self.crewMatch, 3, 'responseCrewFound'), [['Jack', 1, '']])

        self.sender[0] = 3
        self.crewMatch.requestAcceptInvite(1)
        self.assertEqual(self.manager.getBandFromAvatar(3).managerId, 1)
        self.assertNotIn(3, self.crewMatch.avatarLookout)

    def test_accept_uninvited_is_rejected(self):
        self.addAvatar(1, 'Jack')
        self.addAvatar(3, 'Liz')
        self.sender[0] = 3
        self.crewMatch.requestAcceptInvite(1)
        self.air.logPotentialHacker.assert_called()
        self.assertFalse(self.manager.hasBand(3))

    def test_non_captain_cannot_add_crew(self):
        self.addAvatar(1, 'Jack')
        self.addAvatar(2, 'Will')
        self.makeCrew(1, 2)
        self.sender[0] = 2
        self.crewMatch.requestCrewAdd(5, 1, 1)
        self.assertEqual(self.sentTo(self.crewMatch, 2, 'responseCrewAdd'), [[0]])

    def test_band_dissolve_removes_lookout(self):
        self.addAvatar(1, 'Jack')
        self.addAvatar(2, 'Will')
        self.makeCrew(1, 2)
        self.sender[0] = 1
        self.crewMatch.requestCrewAdd(5, 1, 1)
        self.assertIn(1, self.crewMatch.crewLookout)
        self.manager.requestRemove(1)
        self.assertNotIn(1, self.crewMatch.crewLookout)


if __name__ == '__main__':
    unittest.main()
