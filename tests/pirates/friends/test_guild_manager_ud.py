import builtins
import os
import sys
import types
import unittest

from direct.showbase import DConfig
from tests import REPO_ROOT

from direct.task.TaskManagerGlobal import taskMgr

if not hasattr(builtins, 'config'):
    builtins.config = DConfig

if not hasattr(builtins, 'taskMgr'):
    builtins.taskMgr = taskMgr

# semidbm is only needed on a real UberDOG, the tests use a plain dict:
sys.modules.setdefault('semidbm', types.ModuleType('semidbm'))

from panda3d.direct import DCFile
from panda3d.core import Filename

from otp.chat import ChatFilter
from otp.chat.WhiteList import WhiteList
from otp.distributed.MsgTypes import CLIENTAGENT_ADD_POST_REMOVE
from otp.friends.GuildManagerUD import (GuildDB, GUILDRANK_GM, GUILDRANK_OFFICER, GUILDRANK_MEMBER,
    GUILD_NAME_APPROVED, GUILD_NAME_REJECTED, TOKEN_ERROR_INVALID, TOKEN_PERMANENT)
from otp.uberdog.RejectCode import RejectCode
from pirates.friends.PCGuildManagerUD import PCGuildManagerUD
from pirates.friends.PCGuildManagerAI import PCGuildManagerAI

ROOT = str(REPO_ROOT)

_dcFile = None


def getDCFile():
    global _dcFile
    if _dcFile is None:
        _dcFile = DCFile()
        for name in ('otp.dc', 'pirates.dc'):
            path = os.path.join(ROOT, 'astron', 'dclass', name)
            assert _dcFile.read(Filename.fromOsSpecific(path)), path

    return _dcFile


class FakeAir:
    ourChannel = 4000

    def __init__(self):
        self.sent = []
        self.events = []
        self.sender = 0
        dcFile = getDCFile()
        self.dclassesByName = {
            'DistributedPlayerPirateUD': dcFile.getClassByName('DistributedPlayerPirate'),
            'PCGuildManagerUD': dcFile.getClassByName('PCGuildManager'),
        }

    def getAvatarIdFromSender(self):
        return self.sender

    def send(self, datagram):
        self.sent.append(datagram)

    def writeServerEvent(self, *args, **kwargs):
        self.events.append((args, kwargs))


class GuildManagerUDTests(unittest.TestCase):

    def setUp(self):
        self.air = FakeAir()
        self.manager = PCGuildManagerUD(self.air)
        self.manager.doId = 4701
        self.dbm = {}
        self.manager.db = GuildDB(self.dbm)
        self.updates = []

        def sendUpdateToAvatarId(avatarId, fieldName, args):
            # Pack the update with the real dclass so bad argument types fail:
            self.manager.dclass.aiFormatUpdate(fieldName, self.manager.doId,
                self.manager.GetPuppetConnectionChannel(avatarId), self.air.ourChannel, args)
            self.updates.append((avatarId, fieldName, args))

        self.manager.sendUpdateToAvatarId = sendUpdateToAvatarId

        # Whitelist chat goes through the server chat filter; use a known
        # whitelist rather than whatever pwhitelist.txt is on the model path:
        ChatFilter.setWhiteList(WhiteList(['ahoy', 'matey']))

    def tearDown(self):
        ChatFilter.setWhiteList(None)

    def online(self, avatarId, name=None):
        self.manager.recvAvatarOnline(avatarId, name or 'Pirate%d' % avatarId, 0, 0)

    def send(self, avatarId, fieldName, *args):
        self.air.sender = avatarId
        getattr(self.manager, fieldName)(*args)

    def updatesFor(self, avatarId, fieldName):
        return [args for (avId, name, args) in self.updates if avId == avatarId and name == fieldName]

    def makeGuild(self, leaderId=1):
        self.online(leaderId)
        self.send(leaderId, 'createGuild')
        return self.manager.db.getAvatarGuildId(leaderId)

    def addMember(self, guildId, avatarId):
        self.online(avatarId)
        self.send(1, 'requestInvite', avatarId)
        self.send(avatarId, 'acceptInvite')
        self.assertEqual(self.manager.db.getAvatarGuildId(avatarId), guildId)

    def test_create_guild(self):
        guildId = self.makeGuild()
        self.assertEqual(guildId, 1)
        self.assertEqual(self.updatesFor(1, 'guildStatusUpdate'), [[1, '', GUILDRANK_GM]])
        guild = self.manager.db.getGuild(guildId)
        self.assertEqual(guild['members'], [[1, 'Pirate1', GUILDRANK_GM]])

        # Can't create a second guild while in one:
        self.send(1, 'createGuild')
        self.assertEqual(self.manager.db.allocateGuildId(), 2)

    def test_online_pushes_guild_and_post_remove(self):
        self.air.sent = []
        self.online(5)
        # Not in a guild: clear the stale guild fields and add the post remove.
        self.assertEqual(len(self.air.sent), 3)
        self.assertEqual(self.updatesFor(5, 'guildStatusUpdate'), [])

        guildId = self.makeGuild(1)
        self.manager.avatarOffline(1)
        self.online(1)
        self.assertEqual(self.updatesFor(1, 'guildStatusUpdate')[-1], [guildId, '', GUILDRANK_GM])

    def test_post_remove_datagram(self):
        self.air.sent = []
        self.manager.addAvatarOfflinePostRemove(77)
        datagram = self.air.sent[0]
        from direct.distributed.PyDatagramIterator import PyDatagramIterator
        di = PyDatagramIterator(datagram)
        self.assertEqual(di.getUint8(), 1)
        self.assertEqual(di.getUint64(), self.manager.GetPuppetConnectionChannel(77))
        self.assertEqual(di.getUint64(), self.air.ourChannel)
        self.assertEqual(di.getUint16(), CLIENTAGENT_ADD_POST_REMOVE)
        self.assertTrue(len(di.getBlob()) > 0)

    def test_invite_accept(self):
        guildId = self.makeGuild()
        self.online(2)
        self.send(1, 'requestInvite', 2)
        self.assertEqual(self.updatesFor(2, 'invitationFrom'), [[1, 'Pirate1', guildId, '']])
        self.send(2, 'acceptInvite')
        self.assertEqual(self.updatesFor(1, 'guildAcceptInvite'), [[2]])
        self.assertEqual(self.updatesFor(2, 'guildStatusUpdate'), [[guildId, '', GUILDRANK_MEMBER]])
        self.assertEqual(self.updatesFor(1, 'recvMemberAdded'), [[[2, 'Pirate2', GUILDRANK_MEMBER, 1, 0, 0]]])

        self.send(2, 'memberList')
        self.assertEqual(self.updatesFor(2, 'receiveMembers')[-1],
            [[[1, 'Pirate1', GUILDRANK_GM, 1, 0, 0], [2, 'Pirate2', GUILDRANK_MEMBER, 1, 0, 0]]])

    def test_invite_rejections(self):
        guildId = self.makeGuild()
        self.send(1, 'requestInvite', 3)
        self.assertEqual(self.updatesFor(1, 'guildRejectInvite')[-1], [3, RejectCode.INVITEE_NOT_ONLINE])

        self.online(2)
        self.send(1, 'requestInvite', 2)
        self.send(1, 'requestInvite', 2)
        self.assertEqual(self.updatesFor(1, 'guildRejectInvite')[-1], [2, RejectCode.BUSY])

        self.send(2, 'declineInvite')
        self.assertEqual(self.updatesFor(1, 'guildRejectInvite')[-1], [2, RejectCode.NO_GUILD])
        self.assertEqual(self.manager.db.getAvatarGuildId(2), 0)

        self.addMember(guildId, 2)
        # Regular members may not invite:
        self.online(4)
        self.send(2, 'requestInvite', 4)
        self.assertEqual(self.updatesFor(2, 'guildRejectInvite')[-1], [4, RejectCode.NO_GUILD])

        # Already in a guild:
        self.online(10)
        self.send(10, 'createGuild')
        self.send(1, 'requestInvite', 10)
        self.assertEqual(self.updatesFor(1, 'guildRejectInvite')[-1], [10, RejectCode.ALREADY_IN_GUILD])

        # Full guild:
        self.manager.maxMembers = 2
        self.send(1, 'requestInvite', 4)
        self.assertEqual(self.updatesFor(1, 'guildRejectInvite')[-1], [4, RejectCode.GUILD_FULL])

    def test_invitee_going_offline_rejects(self):
        self.makeGuild()
        self.online(2)
        self.send(1, 'requestInvite', 2)
        self.manager.avatarOffline(2)
        self.assertEqual(self.updatesFor(1, 'guildRejectInvite')[-1], [2, RejectCode.INVITEE_NOT_ONLINE])
        self.assertNotIn(2, self.manager.pendingInvites)

    def test_name_approval(self):
        guildId = self.makeGuild()
        self.send(1, 'setWantName', '  Black Pearl  ')
        self.assertEqual(self.updatesFor(1, 'guildNameChange'), [['Black Pearl', GUILD_NAME_APPROVED]])
        self.assertEqual(self.manager.db.getGuild(guildId)['name'], 'Black Pearl')
        self.assertEqual(self.updatesFor(1, 'guildStatusUpdate')[-1], [guildId, 'Black Pearl', GUILDRANK_GM])

        # Can't rename once named:
        self.send(1, 'setWantName', 'Other')
        self.assertEqual(self.manager.db.getGuild(guildId)['name'], 'Black Pearl')

        # Duplicate names are rejected regardless of case:
        self.online(20)
        self.send(20, 'createGuild')
        otherId = self.manager.db.getAvatarGuildId(20)
        self.send(20, 'setWantName', 'black pearl')
        self.assertEqual(self.updatesFor(20, 'guildNameReject'), [[otherId]])

        # Bad characters are rejected:
        self.send(20, 'setWantName', '<b>Bad</b>')
        self.assertEqual(self.updatesFor(20, 'guildNameChange'), [['<b>Bad</b>', GUILD_NAME_REJECTED]])

    def test_members_cannot_name(self):
        guildId = self.makeGuild()
        self.addMember(guildId, 2)
        self.send(2, 'setWantName', 'Nope')
        self.assertEqual(self.manager.db.getGuild(guildId)['name'], '')

    def test_ranks(self):
        guildId = self.makeGuild()
        self.addMember(guildId, 2)
        self.send(1, 'changeRank', 2, GUILDRANK_OFFICER)
        self.assertEqual(self.manager.getAvatarRank(self.manager.db.getGuild(guildId), 2), GUILDRANK_OFFICER)
        self.assertEqual(self.updatesFor(1, 'recvMemberUpdateRank'), [[2, GUILDRANK_OFFICER]])
        self.assertEqual(self.updatesFor(2, 'guildStatusUpdate')[-1], [guildId, '', GUILDRANK_OFFICER])

        # Only the guild master may change ranks, and never to guild master:
        self.addMember(guildId, 3)
        self.send(2, 'changeRank', 3, GUILDRANK_OFFICER)
        self.send(1, 'changeRank', 3, GUILDRANK_GM)
        self.assertEqual(self.manager.getAvatarRank(self.manager.db.getGuild(guildId), 3), GUILDRANK_MEMBER)

        self.send(1, 'changeRank', 2, GUILDRANK_MEMBER)
        self.assertEqual(self.manager.getAvatarRank(self.manager.db.getGuild(guildId), 2), GUILDRANK_MEMBER)

    def test_kick_and_leave(self):
        guildId = self.makeGuild()
        self.addMember(guildId, 2)
        self.addMember(guildId, 3)

        # Members can't kick:
        self.send(2, 'removeMember', 3)
        self.assertEqual(self.manager.db.getAvatarGuildId(3), guildId)

        self.send(1, 'removeMember', 3)
        self.assertEqual(self.manager.db.getAvatarGuildId(3), 0)
        self.assertEqual(self.updatesFor(3, 'guildStatusUpdate')[-1], [0, 'Null', 0])
        self.assertEqual(self.updatesFor(3, 'recvMemberRemoved'), [[3]])
        self.assertEqual(self.updatesFor(2, 'recvMemberRemoved'), [[3]])

        # Leaving:
        self.send(2, 'removeMember', 2)
        self.assertEqual(self.manager.db.getAvatarGuildId(2), 0)
        self.assertEqual(self.manager.db.getGuild(guildId)['members'], [[1, 'Pirate1', GUILDRANK_GM]])

    def test_guild_master_leaving_passes_leadership(self):
        guildId = self.makeGuild()
        self.addMember(guildId, 2)
        self.addMember(guildId, 3)
        self.send(1, 'changeRank', 3, GUILDRANK_OFFICER)
        self.send(1, 'removeMember', 1)
        guild = self.manager.db.getGuild(guildId)
        self.assertEqual(self.manager.getAvatarRank(guild, 3), GUILDRANK_GM)
        self.assertEqual(self.updatesFor(3, 'guildStatusUpdate')[-1], [guildId, '', GUILDRANK_GM])

    def test_last_member_leaving_deletes_guild(self):
        guildId = self.makeGuild()
        self.send(1, 'setWantName', 'Lonely')
        self.send(1, 'removeMember', 1)
        self.assertIsNone(self.manager.db.getGuild(guildId))
        self.assertEqual(self.manager.db.getGuildIdByName('Lonely'), 0)
        self.assertNotIn('guild-%d' % guildId, self.dbm)

    def test_chat_goes_to_online_members(self):
        guildId = self.makeGuild()
        self.addMember(guildId, 2)
        self.addMember(guildId, 3)
        self.manager.avatarOffline(3)
        self.assertEqual(self.updatesFor(1, 'recvAvatarOffline'), [[3, 'Pirate3']])

        self.send(2, 'sendChat', 'Yo ho', 0, 0)
        self.send(2, 'sendWLChat', 'Ahoy matey', 0, 0)
        self.send(2, 'sendWLChat', 'Ahoy scallywag', 0, 0)
        self.send(2, 'sendSC', 100)
        # Not a SpeedChat phrase, the chat filter drops it:
        self.send(2, 'sendSC', 5)
        self.send(2, 'sendSCQuest', 1, 2, 3)
        for avatarId in (1, 2):
            self.assertEqual(self.updatesFor(avatarId, 'recvChat'), [[2, 'Yo ho', 0, 0]])
            self.assertEqual(self.updatesFor(avatarId, 'recvWLChat'),
                             [[2, 'Ahoy matey', 0, 0], [2, 'Ahoy arrr', 0, 0]])
            self.assertEqual(self.updatesFor(avatarId, 'recvSC'), [[2, 100]])
            self.assertEqual(self.updatesFor(avatarId, 'recvSCQuest'), [[2, 1, 2, 3]])

        self.assertEqual(self.updatesFor(3, 'recvChat'), [])

        # Non-members can't chat:
        self.online(9)
        self.send(9, 'sendChat', 'Hi', 0, 0)
        self.assertEqual(len(self.updatesFor(1, 'recvChat')), 1)

    def test_online_notifications(self):
        guildId = self.makeGuild()
        self.addMember(guildId, 2)
        self.manager.avatarOffline(2)
        self.online(2, 'Renamed')
        self.assertEqual(self.updatesFor(1, 'recvAvatarOnline'), [[2, 'Renamed', 0, 0]])
        self.assertEqual(self.manager.getMember(self.manager.db.getGuild(guildId), 2)[1], 'Renamed')

        # Changing districts is not a new login:
        self.online(2, 'Renamed')
        self.assertEqual(len(self.updatesFor(1, 'recvAvatarOnline')), 1)

    def test_avatar_deleted_leaves_guild(self):
        guildId = self.makeGuild()
        self.addMember(guildId, 2)
        self.manager.avatarDeleted(2)
        self.assertEqual(self.manager.db.getAvatarGuildId(2), 0)
        self.assertIsNone(self.manager.getMember(self.manager.db.getGuild(guildId), 2))

    def test_teleport_reflect(self):
        guildId = self.makeGuild()
        self.addMember(guildId, 2)
        self.online(9)
        self.send(1, 'reflectTeleportQuery', 2, 0, 0, guildId, 401000000)
        self.assertEqual(self.updatesFor(2, 'teleportQuery'), [[1, 0, 0, guildId, 401000000]])
        self.send(2, 'reflectTeleportResponse', 1, 1, 401000000, 5, 6)
        self.assertEqual(self.updatesFor(1, 'teleportResponse'), [[2, 1, 401000000, 5, 6]])

        # Not a guild mate:
        self.send(1, 'reflectTeleportQuery', 9, 0, 0, guildId, 401000000)
        self.assertEqual(self.updatesFor(9, 'teleportQuery'), [])

    def test_invite_tokens(self):
        guildId = self.makeGuild()
        self.send(1, 'sendTokenRequest')
        token, preExistPerm = self.updatesFor(1, 'recvTokenInviteValue')[-1]
        self.assertEqual(preExistPerm, 0)
        self.send(1, 'sendNonPermTokenCount')
        self.assertEqual(self.updatesFor(1, 'recvNonPermTokenCount')[-1], [1])

        # Single use:
        self.online(2)
        self.send(2, 'sendTokenForJoinRequest', token.lower(), 'Pirate2')
        self.assertEqual(self.updatesFor(2, 'recvTokenRedeemMessage'), [['Pirate Guild %d' % guildId]])
        self.assertEqual(self.updatesFor(1, 'recvTokenRedeemedByPlayerMessage'), [['Pirate2']])
        self.assertEqual(self.manager.db.getAvatarGuildId(2), guildId)

        self.online(3)
        self.send(3, 'sendTokenForJoinRequest', token, 'Pirate3')
        self.assertEqual(self.updatesFor(3, 'recvTokenRedeemMessage'), [[TOKEN_ERROR_INVALID]])

        # Permanent:
        self.send(1, 'sendTokenRequest')
        token = self.updatesFor(1, 'recvTokenInviteValue')[-1][0]
        self.send(1, 'sendTokenRValue', token, TOKEN_PERMANENT)
        self.send(1, 'sendPermToken')
        self.assertEqual(self.updatesFor(1, 'recvPermToken')[-1], [token])
        self.send(3, 'sendTokenForJoinRequest', token, 'Pirate3')
        self.online(4)
        self.send(4, 'sendTokenForJoinRequest', token, 'Pirate4')
        self.assertEqual(self.manager.db.getAvatarGuildId(4), guildId)

        self.send(1, 'sendClearTokens', 1)
        self.send(1, 'sendPermToken')
        self.assertEqual(self.updatesFor(1, 'recvPermToken')[-1], ['0'])

    def test_limited_tokens(self):
        guildId = self.makeGuild()
        self.send(1, 'sendTokenRequest')
        token = self.updatesFor(1, 'recvTokenInviteValue')[-1][0]
        self.send(1, 'sendTokenRValue', token, 2)
        for avatarId in (2, 3, 4):
            self.online(avatarId)
            self.send(avatarId, 'sendTokenForJoinRequest', token, '')

        self.assertEqual(self.manager.db.getAvatarGuildId(3), guildId)
        self.assertEqual(self.manager.db.getAvatarGuildId(4), 0)

        self.send(1, 'sendTokenRequest')
        self.send(1, 'sendClearTokens', 0)
        self.send(1, 'sendNonPermTokenCount')
        self.assertEqual(self.updatesFor(1, 'recvNonPermTokenCount')[-1], [0])

    def test_status_request(self):
        self.online(1)
        self.send(1, 'statusRequest')
        self.assertEqual(self.updatesFor(1, 'guildStatusUpdate'), [[0, 'Null', 0]])

    def test_guild_db_round_trip(self):
        guildId = self.makeGuild()
        reloaded = GuildDB(self.dbm)
        self.assertEqual(reloaded.getAvatarGuildId(1), guildId)
        self.assertEqual(reloaded.getGuild(guildId)['members'], [[1, 'Pirate1', GUILDRANK_GM]])


class GuildManagerAITests(unittest.TestCase):

    def test_avatar_online_is_sent_to_uberdog(self):
        manager = object.__new__(PCGuildManagerAI)
        sent = []
        manager.sendUpdate = lambda fieldName, args: sent.append((fieldName, args))
        av = types.SimpleNamespace(doId=42, getName=lambda: 'Jack', getBandId=lambda: (300, 7))
        manager.avatarOnline(av)
        self.assertEqual(sent, [('recvAvatarOnline', [42, 'Jack', 300, 7])])


if __name__ == '__main__':
    unittest.main()
