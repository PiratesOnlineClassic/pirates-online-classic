import sys
import types
import unittest
from unittest.mock import patch

from pirates.friends.test_guild_manager_ud import FakeAir

from otp.friends.GuildManagerUD import GuildDB, GUILDRANK_GM, GUILD_NAME_REJECTED
from otp.otpbase import OTPGlobals
from otp.uberdog.RejectCode import RejectCode
from pirates.friends.PCGuildManagerUD import PCGuildManagerUD


class GuildTestBase(unittest.TestCase):

    def setUp(self):
        self.air = FakeAir()
        self.manager = PCGuildManagerUD(self.air)
        self.manager.doId = 4701
        self.manager.db = GuildDB({})
        self.updates = []

        def sendUpdateToAvatarId(avatarId, fieldName, args):
            # Pack the update with the real dclass so bad argument types fail:
            self.manager.dclass.aiFormatUpdate(fieldName, self.manager.doId,
                self.manager.GetPuppetConnectionChannel(avatarId), self.air.ourChannel, args)
            self.updates.append((avatarId, fieldName, args))

        self.manager.sendUpdateToAvatarId = sendUpdateToAvatarId

    def tearDown(self):
        for inviteeId in list(self.manager.pendingInvites.keys()):
            self.manager.clearInvite(inviteeId)

    def online(self, avatarId, name=None):
        self.manager.recvAvatarOnline(avatarId, name or 'Pirate%d' % avatarId, 0, 0)

    def send(self, avatarId, fieldName, *args):
        self.air.sender = avatarId
        getattr(self.manager, fieldName)(*args)

    def updatesFor(self, avatarId, fieldName):
        return [args for (avId, name, args) in self.updates if avId == avatarId and name == fieldName]

    def makeGuild(self, leaderId, *memberIds):
        self.online(leaderId)
        self.send(leaderId, 'createGuild')
        guildId = self.manager.db.getAvatarGuildId(leaderId)
        for memberId in memberIds:
            self.online(memberId)
            self.send(leaderId, 'requestInvite', memberId)
            self.send(memberId, 'acceptInvite')

        return guildId


class TestGuildLeaderboard(GuildTestBase):

    def test_top_ten_ranks_guilds_by_size(self):
        small = self.makeGuild(1)
        big = self.makeGuild(2, 3, 4)
        self.send(2, 'setWantName', 'Black Pearl')
        for leaderId in range(10, 22):
            self.makeGuild(leaderId)

        self.send(1, 'requestLeaderboardTopTen')
        topTen = self.updatesFor(1, 'leaderboardTopTen')[0][0]
        self.assertEqual(len(topTen), 10)
        self.assertEqual(topTen[0], [big, 'Black Pearl', 3])
        smallName = self.manager.getGuildDisplayName(small, self.manager.db.getGuild(small))
        self.assertEqual(topTen[1], [small, smallName, 1])

    def test_top_ten_is_throttled(self):
        self.makeGuild(1)
        self.send(1, 'requestLeaderboardTopTen')
        self.send(1, 'requestLeaderboardTopTen')
        self.assertEqual(len(self.updatesFor(1, 'leaderboardTopTen')), 1)

        self.manager.leaderboardRequests[1] -= self.manager.leaderboardCooldown
        self.send(1, 'requestLeaderboardTopTen')
        self.assertEqual(len(self.updatesFor(1, 'leaderboardTopTen')), 2)


class TestGuildInviteTimeout(GuildTestBase):

    def test_invite_expires(self):
        guildId = self.makeGuild(1)
        self.online(2)
        self.send(1, 'requestInvite', 2)
        self.assertIn(2, self.manager.pendingInvites)
        taskName = self.manager.uniqueName('invite-timeout-2')
        self.assertTrue(taskMgr.hasTaskNamed(taskName))

        self.manager._GuildManagerUD__inviteTimeout(2, 1)
        self.assertNotIn(2, self.manager.pendingInvites)
        self.assertFalse(taskMgr.hasTaskNamed(taskName))
        self.assertEqual(self.updatesFor(1, 'guildRejectInvite'), [[2, RejectCode.INVITEE_NOT_ONLINE]])

        # accepting the expired invitation does nothing
        self.send(2, 'acceptInvite')
        self.assertEqual(self.manager.db.getAvatarGuildId(2), 0)
        self.assertEqual(self.manager.db.getGuild(guildId)['members'][0][0], 1)

    def test_answered_invite_cancels_timeout(self):
        self.makeGuild(1)
        self.online(2)
        self.send(1, 'requestInvite', 2)
        self.send(2, 'declineInvite')
        self.assertFalse(taskMgr.hasTaskNamed(self.manager.uniqueName('invite-timeout-2')))


class TestGuildFreePlayers(GuildTestBase):

    def setUp(self):
        GuildTestBase.setUp(self)
        self.access = {}
        self.air.getObject = lambda doId, callback: callback(doId, 0, 0, None,
            {'setAccess': (self.access.get(doId, OTPGlobals.AccessVelvetRope),)})

        # Freebooter needs the game resources, give it what the guild manager reads:
        freebooter = types.ModuleType('pirates.piratesbase.Freebooter')
        freebooter.FreeGuildRestrict = True
        freebooter.AllAccessHoliday = False
        self.modules = patch.dict(sys.modules, {'pirates.piratesbase.Freebooter': freebooter})
        self.modules.start()
        self.config = patch.object(config, 'GetBool',
            lambda name, default=False: True if name == 'want-membership' else default)
        self.config.start()

    def tearDown(self):
        self.config.stop()
        self.modules.stop()
        GuildTestBase.tearDown(self)

    def test_free_player_can_not_create_guild(self):
        self.online(1)
        self.send(1, 'createGuild')
        self.assertEqual(self.manager.db.getAvatarGuildId(1), 0)

        self.access[1] = OTPGlobals.AccessFull
        self.send(1, 'createGuild')
        self.assertNotEqual(self.manager.db.getAvatarGuildId(1), 0)

    def test_free_player_can_not_name_guild(self):
        self.access[1] = OTPGlobals.AccessFull
        guildId = self.makeGuild(1)
        self.access[1] = OTPGlobals.AccessVelvetRope
        self.send(1, 'setWantName', 'Black Pearl')
        self.assertEqual(self.manager.db.getGuild(guildId)['name'], '')
        self.assertEqual(self.updatesFor(1, 'guildNameChange'), [['Black Pearl', GUILD_NAME_REJECTED]])
        self.assertEqual(self.manager.db.getGuildIdByName('Black Pearl'), 0)

    def test_free_player_can_join_guild(self):
        self.access[1] = OTPGlobals.AccessFull
        guildId = self.makeGuild(1, 2)
        self.assertEqual(self.manager.db.getAvatarGuildId(2), guildId)


class TestGuildRenames(GuildTestBase):

    def test_member_name_follows_rename(self):
        guildId = self.makeGuild(1, 2)
        self.manager.avatarNameChanged(2, 1002, 'Captain Will')
        members = self.manager.db.getGuild(guildId)['members']
        self.assertEqual(members[1][1], 'Captain Will')
        self.assertEqual(self.updatesFor(1, 'recvMemberUpdateName'), [[2, 'Captain Will']])


if __name__ == '__main__':
    unittest.main()
