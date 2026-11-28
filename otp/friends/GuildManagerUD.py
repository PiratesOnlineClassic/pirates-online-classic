import json
import random
import time
import semidbm

from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import PyDatagram
from direct.directnotify import DirectNotifyGlobal

from otp.distributed.MsgTypes import *
from otp.chat import ChatFilter
from otp.uberdog.RejectCode import RejectCode

GUILDRANK_GM = 3
GUILDRANK_OFFICER = 2
GUILDRANK_MEMBER = 1

GUILD_NAME_APPROVED = 1
GUILD_NAME_REJECTED = 2

TOKEN_ERROR_INVALID = '***ERROR - GUILD CODE INVALID***'
TOKEN_ERROR_FULL = '***ERROR - GUILD FULL***'
TOKEN_TOO_MANY = 'TOO_MANY_TOKENS'
TOKEN_GUILD_FULL = 'GUILD FULL'
TOKEN_CHARACTERS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
TOKEN_PERMANENT = -1

GuildNameAllowedPunctuation = " '-."


class GuildDB:
    """
    The original OTP server kept guilds in a SQL database next to the
    UberDOGs. Nothing in the dclass describes a guild object for the Astron
    database, so the guilds are kept in a small key/value store alongside
    the account bridge instead. Guild records are cached in memory and
    written straight through on every change.

    Keys:
        nextGuildId       -> next guild id to hand out
        guild-<guildId>   -> guild record
        avatar-<avId>     -> guild id the avatar belongs to
        name-<name>       -> guild id that owns the (lowercase) name
        token-<token>     -> invite token record
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('GuildDB')

    def __init__(self, dbm):
        self.dbm = dbm
        self.guildCache = {}

    def __get(self, key):
        # semidbm keeps it's keys as bytes, a str key is never found in it:
        key = key.encode('utf-8')
        if key not in self.dbm:
            return None

        value = self.dbm[key]
        if isinstance(value, bytes):
            value = value.decode('utf-8')

        return json.loads(value)

    def __set(self, key, value):
        self.dbm[key.encode('utf-8')] = json.dumps(value).encode('utf-8')
        self.__sync()

    def __delete(self, key):
        key = key.encode('utf-8')
        if key in self.dbm:
            del self.dbm[key]
            self.__sync()

    def __sync(self):
        if getattr(self.dbm, 'sync', None):
            self.dbm.sync()

    def allocateGuildId(self):
        guildId = self.__get('nextGuildId') or 1
        self.__set('nextGuildId', guildId + 1)
        return guildId

    def getGuild(self, guildId):
        if not guildId:
            return None

        if guildId not in self.guildCache:
            guild = self.__get('guild-%d' % guildId)
            if guild is None:
                return None

            self.guildCache[guildId] = guild

        return self.guildCache[guildId]

    def storeGuild(self, guildId, guild):
        self.guildCache[guildId] = guild
        self.__set('guild-%d' % guildId, guild)

    def deleteGuild(self, guildId):
        self.guildCache.pop(guildId, None)
        self.__delete('guild-%d' % guildId)

    def getGuildIds(self):
        guildIds = []
        for key in list(self.dbm.keys()):
            if isinstance(key, bytes):
                key = key.decode('utf-8')

            if key.startswith('guild-'):
                guildIds.append(int(key[len('guild-'):]))

        return guildIds

    def getAvatarGuildId(self, avatarId):
        return self.__get('avatar-%d' % avatarId) or 0

    def setAvatarGuildId(self, avatarId, guildId):
        if guildId:
            self.__set('avatar-%d' % avatarId, guildId)
        else:
            self.__delete('avatar-%d' % avatarId)

    def getGuildIdByName(self, name):
        return self.__get('name-%s' % name.lower()) or 0

    def setGuildIdByName(self, name, guildId):
        if guildId:
            self.__set('name-%s' % name.lower(), guildId)
        else:
            self.__delete('name-%s' % name.lower())

    def getToken(self, token):
        return self.__get('token-%s' % token)

    def storeToken(self, token, tokenInfo):
        self.__set('token-%s' % token, tokenInfo)

    def deleteToken(self, token):
        self.__delete('token-%s' % token)


class GuildManagerUD(DistributedObjectGlobalUD):
    """
    UberDOG side of the guild system. Handles everything the client's
    GuildManager asks for: guild creation and naming, invitations (both the
    avatar to avatar kind and invite codes), the member list, ranks,
    leaving and kicking, guild chat and the online/offline notifications.

    A guild record is a dict:
        name      : the approved guild name, '' while the guild is unnamed
        members   : [[avatarId, avatarName, rank], ...] in join order
        permToken : the guild's permanent invite code, '' when there is none
        tokens    : the guild's limited use invite codes
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('GuildManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        # avatarId -> [avatarName, bandManagerId, bandId] for every avatar
        # the districts have told us is playing right now.
        self.onlineAvatars = {}

        # inviteeId -> (inviterId, guildId)
        self.pendingInvites = {}

        # avatarId -> when the avatar last asked for the leaderboard
        self.leaderboardRequests = {}

        self.db = None
        self.maxMembers = config.GetInt('guild-max-members', 500)
        self.maxNameLength = config.GetInt('guild-name-max-length', 30)
        self.maxTokens = config.GetInt('guild-max-invite-tokens', 25)
        self.maxTokenUses = config.GetInt('guild-max-invite-token-uses', 100)
        self.tokenLength = config.GetInt('guild-invite-token-length', 8)
        self.inviteTimeout = config.GetFloat('guild-invite-timeout', 60.0)

        # The client shows the leaderboard for 15 seconds, and can not cope
        # with a second leaderboard arriving while the first one is shown.
        self.leaderboardCooldown = config.GetFloat('guild-leaderboard-cooldown', 20.0)

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        filename = config.GetString('guild-db-filename', 'astron/databases/guilds')
        self.db = GuildDB(semidbm.open(filename, 'c'))

    def getAvatarDClass(self):
        return self.air.dclassesByName['DistributedPlayerUD']

    def getGuildDisplayName(self, guildId, guild):
        return guild['name'] or str(guildId)

    # --- Helpers ---

    def getAvatarName(self, avatarId):
        info = self.onlineAvatars.get(avatarId)
        if info:
            return info[0]

        return ''

    def isOnline(self, avatarId):
        return avatarId in self.onlineAvatars

    def getMember(self, guild, avatarId):
        for member in guild['members']:
            if member[0] == avatarId:
                return member

        return None

    def getAvatarGuild(self, avatarId):
        guildId = self.db.getAvatarGuildId(avatarId)
        guild = self.db.getGuild(guildId)
        if not guild:
            return (0, None)

        if not self.getMember(guild, avatarId):
            self.notify.warning('Avatar %d thinks it is in guild %d, but is not a member!' % (avatarId, guildId))
            self.db.setAvatarGuildId(avatarId, 0)
            return (0, None)

        return (guildId, guild)

    def getAvatarRank(self, guild, avatarId):
        member = self.getMember(guild, avatarId)
        if not member:
            return 0

        return member[2]

    def isGuildFull(self, guild):
        return len(guild['members']) >= self.maxMembers

    def getMemberInfo(self, member):
        avatarId, avatarName, rank = member
        info = self.onlineAvatars.get(avatarId)
        if info:
            return [avatarId, avatarName, rank, 1, info[1], info[2]]

        return [avatarId, avatarName, rank, 0, 0, 0]

    def sendToOnlineMembers(self, guild, fieldName, args, excludeId=None):
        for member in guild['members']:
            avatarId = member[0]
            if avatarId == excludeId or not self.isOnline(avatarId):
                continue

            self.sendUpdateToAvatarId(avatarId, fieldName, args)

    def isValidGuildName(self, name):
        if not name or len(name) > self.maxNameLength:
            return False

        if '  ' in name or not name[0].isalnum():
            return False

        for character in name:
            if not character.isalnum() and character not in GuildNameAllowedPunctuation:
                return False

        return True

    def checkGuildAccess(self, avatarId, callback):
        """
        Calls back with whether or not the avatar may start and name a guild.
        """

        callback(True)

    def generateToken(self):
        while True:
            token = ''.join(random.choice(TOKEN_CHARACTERS) for x in range(self.tokenLength))
            if not self.db.getToken(token):
                return token

    def setAvatarGuildFields(self, avatarId, guildId, guildName):
        # setGuildId is a ram field, so the guild has to be pushed onto the
        # avatar every time it comes online. setGuildName is a db field and
        # persists on the avatar through the database state server.
        if not guildId:
            guildName = 'Null'

        dclass = self.getAvatarDClass()
        for fieldName, args in (('setGuildId', [guildId]), ('setGuildName', [guildName])):
            datagram = dclass.aiFormatUpdate(fieldName, avatarId, avatarId, self.air.ourChannel, args)
            self.air.send(datagram)

    def addAvatarOfflinePostRemove(self, avatarId):
        # If the client disconnects, have the Client Agent tell us that the
        # avatar went offline.
        datagramCleanup = self.dclass.aiFormatUpdate('avatarOffline', self.doId, self.doId,
            self.air.ourChannel, [avatarId])

        datagram = PyDatagram()
        datagram.addServerHeader(
            self.GetPuppetConnectionChannel(avatarId),
            self.air.ourChannel,
            CLIENTAGENT_ADD_POST_REMOVE)
        # Must include the blob length prefix; appendData alone truncates.
        datagram.addBlob(datagramCleanup.getMessage())
        self.air.send(datagram)

    def addMember(self, guildId, guild, avatarId, rank, avatarName=''):
        avatarName = self.getAvatarName(avatarId) or avatarName
        member = [avatarId, avatarName, rank]
        guild['members'].append(member)
        self.db.storeGuild(guildId, guild)
        self.db.setAvatarGuildId(avatarId, guildId)
        self.clearInvite(avatarId)

        self.setAvatarGuildFields(avatarId, guildId, guild['name'])
        self.d_guildStatusUpdate(avatarId, guildId, guild['name'], rank)
        self.sendToOnlineMembers(guild, 'recvMemberAdded', [self.getMemberInfo(member)], excludeId=avatarId)
        self.air.writeServerEvent('guildJoin', avId=avatarId, guildId=guildId, rank=rank)

    def removeMemberFromGuild(self, guildId, guild, avatarId):
        member = self.getMember(guild, avatarId)
        if not member:
            return

        guild['members'].remove(member)
        self.db.setAvatarGuildId(avatarId, 0)

        successor = None
        if not guild['members']:
            self.deleteGuild(guildId, guild)
        else:
            if member[2] == GUILDRANK_GM:
                # The guild master left, hand the guild to the highest ranking
                # member that has been in the guild the longest:
                successor = guild['members'][0]
                for other in guild['members']:
                    if other[2] > successor[2]:
                        successor = other

                successor[2] = GUILDRANK_GM

            self.db.storeGuild(guildId, guild)

        if self.isOnline(avatarId):
            self.setAvatarGuildFields(avatarId, 0, 'Null')
            self.d_guildStatusUpdate(avatarId, 0, 'Null', 0)
            self.sendUpdateToAvatarId(avatarId, 'recvMemberRemoved', [avatarId])

        self.sendToOnlineMembers(guild, 'recvMemberRemoved', [avatarId])
        if successor:
            self.sendToOnlineMembers(guild, 'recvMemberUpdateRank', [successor[0], GUILDRANK_GM])
            if self.isOnline(successor[0]):
                self.d_guildStatusUpdate(successor[0], guildId, guild['name'], GUILDRANK_GM)

        self.air.writeServerEvent('guildLeave', avId=avatarId, guildId=guildId)

    def deleteGuild(self, guildId, guild):
        if guild['name']:
            self.db.setGuildIdByName(guild['name'], 0)

        if guild['permToken']:
            self.db.deleteToken(guild['permToken'])

        for token in guild['tokens']:
            self.db.deleteToken(token)

        self.db.deleteGuild(guildId)
        self.air.writeServerEvent('guildDeleted', guildId=guildId)

    def clearInvite(self, inviteeId):
        taskMgr.remove(self.uniqueName('invite-timeout-%d' % inviteeId))
        return self.pendingInvites.pop(inviteeId, None)

    def __inviteTimeout(self, inviteeId, inviterId):
        invite = self.pendingInvites.get(inviteeId)
        if not invite or invite[0] != inviterId:
            return

        # The client has no way of taking the invitation off the invitee's
        # screen, accepting it from here on is ignored. The inviter is told
        # the invitee is busy and to try again later.
        self.clearInvite(inviteeId)
        self.d_guildRejectInvite(inviterId, inviteeId, RejectCode.INVITEE_NOT_ONLINE)

    def clearInvitesFor(self, avatarId):
        invite = self.clearInvite(avatarId)
        if invite:
            inviterId, guildId = invite
            self.d_guildRejectInvite(inviterId, avatarId, RejectCode.INVITEE_NOT_ONLINE)

        for inviteeId, (inviterId, guildId) in list(self.pendingInvites.items()):
            if inviterId == avatarId:
                self.clearInvite(inviteeId)

    # --- District/UberDOG messages ---

    def online(self):
        pass

    def recvAvatarOnline(self, avatarId, avatarName, bandManagerId, bandId):
        # Sent to us by a district whenever one of our avatars arrives on it.
        newlyOnline = not self.isOnline(avatarId)
        self.onlineAvatars[avatarId] = [avatarName, bandManagerId, bandId]
        if newlyOnline:
            self.addAvatarOfflinePostRemove(avatarId)

        guildId, guild = self.getAvatarGuild(avatarId)
        if not guild:
            if newlyOnline:
                # Clear any stale guild name, e.g. we were kicked while away.
                self.setAvatarGuildFields(avatarId, 0, 'Null')

            return

        member = self.getMember(guild, avatarId)
        if member[1] != avatarName:
            member[1] = avatarName
            self.db.storeGuild(guildId, guild)

        if not newlyOnline:
            # The avatar is only changing districts.
            return

        self.setAvatarGuildFields(avatarId, guildId, guild['name'])
        self.d_guildStatusUpdate(avatarId, guildId, guild['name'], member[2])
        self.sendToOnlineMembers(guild, 'recvAvatarOnline', [avatarId, avatarName, bandManagerId, bandId],
            excludeId=avatarId)

    def avatarOffline(self, avatarId):
        info = self.onlineAvatars.pop(avatarId, None)
        self.leaderboardRequests.pop(avatarId, None)
        if not info:
            return

        self.clearInvitesFor(avatarId)
        guildId, guild = self.getAvatarGuild(avatarId)
        if guild:
            self.sendToOnlineMembers(guild, 'recvAvatarOffline', [avatarId, info[0]])

    def avatarDeleted(self, avatarId):
        self.avatarOffline(avatarId)
        guildId, guild = self.getAvatarGuild(avatarId)
        if guild:
            self.removeMemberFromGuild(guildId, guild, avatarId)

    def avatarNameChanged(self, avatarId, accountId, avatarName):
        # Called once an avatar's new name has been written to the database.
        guildId, guild = self.getAvatarGuild(avatarId)
        if not guild:
            return

        member = self.getMember(guild, avatarId)
        if member[1] == avatarName:
            return

        member[1] = avatarName
        self.db.storeGuild(guildId, guild)
        self.sendToOnlineMembers(guild, 'recvMemberUpdateName', [avatarId, avatarName])

    def sendAvatarBandId(self, avatarId, bandManagerId, bandId):
        info = self.onlineAvatars.get(avatarId)
        if not info:
            return

        info[1] = bandManagerId
        info[2] = bandId
        guildId, guild = self.getAvatarGuild(avatarId)
        if guild:
            self.sendToOnlineMembers(guild, 'recvMemberUpdateBandId', [avatarId, bandManagerId, bandId])

    # --- Client requests ---

    def statusRequest(self):
        avatarId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(avatarId)
        if not guild:
            self.d_guildStatusUpdate(avatarId, 0, 'Null', 0)
            return

        self.d_guildStatusUpdate(avatarId, guildId, guild['name'], self.getAvatarRank(guild, avatarId))

    def memberList(self):
        avatarId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(avatarId)
        members = []
        if guild:
            for member in guild['members']:
                members.append(self.getMemberInfo(member))

        self.sendUpdateToAvatarId(avatarId, 'receiveMembers', [members])

    def createGuild(self):
        avatarId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(avatarId)
        if guild:
            self.notify.warning('Avatar %d tried to create a guild while in guild %d!' % (avatarId, guildId))
            return

        self.checkGuildAccess(avatarId, lambda allowed: self.__handleCreateGuildAccess(avatarId, allowed))

    def __handleCreateGuildAccess(self, avatarId, allowed):
        if not allowed:
            self.notify.warning('Avatar %d tried to create a guild without access!' % avatarId)
            return

        if self.getAvatarGuild(avatarId)[1]:
            return

        guildId = self.db.allocateGuildId()
        guild = {
            'name': '',
            'members': [],
            'permToken': '',
            'tokens': []
        }

        self.air.writeServerEvent('guildCreated', avId=avatarId, guildId=guildId)
        self.addMember(guildId, guild, avatarId, GUILDRANK_GM)

    def setWantName(self, newName):
        avatarId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(avatarId)
        if not guild or self.getAvatarRank(guild, avatarId) != GUILDRANK_GM:
            self.notify.warning('Avatar %d tried to name a guild they do not lead!' % avatarId)
            return

        if guild['name']:
            self.notify.warning('Avatar %d tried to rename guild %d!' % (avatarId, guildId))
            return

        newName = newName.strip()
        if not self.isValidGuildName(newName):
            self.d_guildNameChange(avatarId, newName, GUILD_NAME_REJECTED)
            return

        if self.db.getGuildIdByName(newName):
            self.d_guildNameReject(avatarId, guildId)
            return

        self.checkGuildAccess(avatarId, lambda allowed: self.__handleNameGuildAccess(avatarId, guildId, newName, allowed))

    def __handleNameGuildAccess(self, avatarId, guildId, newName, allowed):
        if not allowed:
            self.notify.warning('Avatar %d tried to name guild %d without access!' % (avatarId, guildId))
            self.d_guildNameChange(avatarId, newName, GUILD_NAME_REJECTED)
            return

        # Make sure nothing changed while we were waiting:
        guild = self.db.getGuild(guildId)
        if not guild or guild['name'] or self.getAvatarRank(guild, avatarId) != GUILDRANK_GM:
            return

        if self.db.getGuildIdByName(newName):
            self.d_guildNameReject(avatarId, guildId)
            return

        self.db.setGuildIdByName(newName, guildId)
        guild['name'] = newName
        self.db.storeGuild(guildId, guild)

        for member in guild['members']:
            if self.isOnline(member[0]):
                self.setAvatarGuildFields(member[0], guildId, newName)

        self.d_guildNameChange(avatarId, newName, GUILD_NAME_APPROVED)
        self.d_guildStatusUpdate(avatarId, guildId, newName, GUILDRANK_GM)
        self.air.writeServerEvent('guildNamed', avId=avatarId, guildId=guildId, name=newName)

    def requestInvite(self, inviteeId):
        inviterId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(inviterId)
        if not guild or self.getAvatarRank(guild, inviterId) < GUILDRANK_OFFICER or inviteeId == inviterId:
            self.d_guildRejectInvite(inviterId, inviteeId, RejectCode.NO_GUILD)
            return

        if not self.isOnline(inviteeId):
            self.d_guildRejectInvite(inviterId, inviteeId, RejectCode.INVITEE_NOT_ONLINE)
            return

        if self.getAvatarGuild(inviteeId)[1]:
            self.d_guildRejectInvite(inviterId, inviteeId, RejectCode.ALREADY_IN_GUILD)
            return

        if self.isGuildFull(guild):
            self.d_guildRejectInvite(inviterId, inviteeId, RejectCode.GUILD_FULL)
            return

        if inviteeId in self.pendingInvites:
            self.d_guildRejectInvite(inviterId, inviteeId, RejectCode.BUSY)
            return

        self.pendingInvites[inviteeId] = (inviterId, guildId)
        taskMgr.doMethodLater(self.inviteTimeout, self.__inviteTimeout,
            self.uniqueName('invite-timeout-%d' % inviteeId), extraArgs=[inviteeId, inviterId])

        self.d_invitationFrom(inviteeId, inviterId, self.getAvatarName(inviterId), guildId, guild['name'])

    def acceptInvite(self):
        inviteeId = self.air.getAvatarIdFromSender()
        invite = self.clearInvite(inviteeId)
        if not invite:
            # The invitation may have timed out while it was on the screen.
            self.notify.debug('Avatar %d accepted a guild invite they do not have.' % inviteeId)
            return

        inviterId, guildId = invite
        guild = self.db.getGuild(guildId)
        if not guild or self.getAvatarRank(guild, inviterId) < GUILDRANK_OFFICER:
            self.d_guildRejectInvite(inviterId, inviteeId, RejectCode.NO_GUILD)
            return

        if self.getAvatarGuild(inviteeId)[1]:
            self.d_guildRejectInvite(inviterId, inviteeId, RejectCode.ALREADY_IN_GUILD)
            return

        if self.isGuildFull(guild):
            self.d_guildRejectInvite(inviterId, inviteeId, RejectCode.GUILD_FULL)
            return

        self.addMember(guildId, guild, inviteeId, GUILDRANK_MEMBER)
        self.d_guildAcceptInvite(inviterId, inviteeId)

    def declineInvite(self):
        inviteeId = self.air.getAvatarIdFromSender()
        invite = self.clearInvite(inviteeId)
        if not invite:
            return

        inviterId, guildId = invite
        # The client's GuildInviter shows "said no" for NO_GUILD.
        self.d_guildRejectInvite(inviterId, inviteeId, RejectCode.NO_GUILD)

    def removeMember(self, avatarId):
        senderId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(senderId)
        if not guild:
            return

        member = self.getMember(guild, avatarId)
        if not member:
            self.notify.warning('Avatar %d tried to remove non-member %d from guild %d!' % (senderId, avatarId, guildId))
            return

        if avatarId != senderId:
            # Officers and the guild master may only kick regular members.
            if self.getAvatarRank(guild, senderId) <= GUILDRANK_MEMBER or member[2] > GUILDRANK_MEMBER:
                self.notify.warning('Avatar %d tried to kick %d from guild %d without permission!' % (senderId, avatarId, guildId))
                return

        self.removeMemberFromGuild(guildId, guild, avatarId)

    def changeRank(self, avatarId, rank):
        senderId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(senderId)
        if not guild or self.getAvatarRank(guild, senderId) != GUILDRANK_GM:
            self.notify.warning('Avatar %d tried to change a rank without being a guild master!' % senderId)
            return

        if avatarId == senderId or rank not in (GUILDRANK_MEMBER, GUILDRANK_OFFICER):
            return

        member = self.getMember(guild, avatarId)
        if not member or member[2] == rank:
            return

        member[2] = rank
        self.db.storeGuild(guildId, guild)
        self.sendToOnlineMembers(guild, 'recvMemberUpdateRank', [avatarId, rank])
        if self.isOnline(avatarId):
            self.d_guildStatusUpdate(avatarId, guildId, guild['name'], rank)

    def getLeaderboardTopTen(self):
        """
        Nothing in the guild records keeps a reputation for the guild, so the
        guilds are ranked by the size of their crew.
        """

        records = []
        for guildId in self.db.getGuildIds():
            guild = self.db.getGuild(guildId)
            if guild:
                records.append([guildId, self.getGuildDisplayName(guildId, guild), len(guild['members'])])

        records.sort(key=lambda record: (-record[2], record[0]))
        return records[:10]

    def requestLeaderboardTopTen(self):
        avatarId = self.air.getAvatarIdFromSender()
        now = time.time()
        if now - self.leaderboardRequests.get(avatarId, 0) < self.leaderboardCooldown:
            return

        self.leaderboardRequests[avatarId] = now
        self.sendUpdateToAvatarId(avatarId, 'leaderboardTopTen', [self.getLeaderboardTopTen()])

    # --- Chat ---

    def sendChat(self, msgText, chatFlags, senderDISLid):
        avatarId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(avatarId)
        msgText = ChatFilter.cleanMessage(msgText)
        if guild and msgText:
            self.sendToOnlineMembers(guild, 'recvChat', [avatarId, msgText, ChatFilter.cleanChatFlags(chatFlags), 0])

    def sendWLChat(self, msgText, chatFlags, senderDISLid):
        avatarId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(avatarId)
        msgText = ChatFilter.cleanMessage(msgText)
        if guild and msgText:
            msgText = ChatFilter.filterWhiteList(msgText)
            self.sendToOnlineMembers(guild, 'recvWLChat', [avatarId, msgText, ChatFilter.cleanChatFlags(chatFlags), 0])

    def sendSC(self, msgIndex):
        avatarId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(avatarId)
        # The client looks the phrase up without checking it exists.
        if guild and ChatFilter.isValidSpeedChat(msgIndex):
            self.sendToOnlineMembers(guild, 'recvSC', [avatarId, msgIndex])

    # --- Teleport ---

    def getGuildMateOnline(self, senderId, avatarId):
        guildId, guild = self.getAvatarGuild(senderId)
        if not guild or not self.getMember(guild, avatarId) or not self.isOnline(avatarId):
            return 0

        return guildId

    def reflectTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        avatarId = self.air.getAvatarIdFromSender()
        guildId = self.getGuildMateOnline(avatarId, sendToId)
        if guildId:
            self.sendUpdateToAvatarId(sendToId, 'teleportQuery',
                [avatarId, localBandMgrId, localBandId, guildId, localShardId])

    def reflectTeleportResponse(self, sendToId, available, shardId, instanceDoId, areaDoId):
        avatarId = self.air.getAvatarIdFromSender()
        if self.getGuildMateOnline(avatarId, sendToId):
            self.sendUpdateToAvatarId(sendToId, 'teleportResponse',
                [avatarId, available, shardId, instanceDoId, areaDoId])

    # --- Invite codes ---

    def sendTokenRequest(self):
        avatarId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(avatarId)
        if not guild or self.getAvatarRank(guild, avatarId) < GUILDRANK_OFFICER:
            return

        preExistPerm = int(bool(guild['permToken']))
        if self.isGuildFull(guild):
            self.d_recvTokenInviteValue(avatarId, TOKEN_GUILD_FULL, preExistPerm)
            return

        if len(guild['tokens']) >= self.maxTokens:
            self.d_recvTokenInviteValue(avatarId, TOKEN_TOO_MANY, preExistPerm)
            return

        # New codes are single use until the client says otherwise:
        token = self.generateToken()
        self.db.storeToken(token, {'guildId': guildId, 'creatorId': avatarId, 'uses': 1})
        guild['tokens'].append(token)
        self.db.storeGuild(guildId, guild)
        self.d_recvTokenInviteValue(avatarId, token, preExistPerm)

    def sendTokenRValue(self, tokenString, rValue):
        avatarId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(avatarId)
        if not guild or self.getAvatarRank(guild, avatarId) < GUILDRANK_OFFICER:
            return

        tokenInfo = self.db.getToken(tokenString)
        if not tokenInfo or tokenInfo['guildId'] != guildId:
            return

        if rValue == TOKEN_PERMANENT:
            if guild['permToken'] and guild['permToken'] != tokenString:
                self.db.deleteToken(guild['permToken'])

            if tokenString in guild['tokens']:
                guild['tokens'].remove(tokenString)

            guild['permToken'] = tokenString
            tokenInfo['uses'] = TOKEN_PERMANENT
        else:
            tokenInfo['uses'] = max(1, min(rValue, self.maxTokenUses))

        self.db.storeToken(tokenString, tokenInfo)
        self.db.storeGuild(guildId, guild)

    def sendPermToken(self):
        avatarId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(avatarId)
        if not guild or not guild['permToken'] or self.getAvatarRank(guild, avatarId) < GUILDRANK_OFFICER:
            self.sendUpdateToAvatarId(avatarId, 'recvPermToken', ['0'])
            return

        self.sendUpdateToAvatarId(avatarId, 'recvPermToken', [guild['permToken']])

    def sendNonPermTokenCount(self):
        avatarId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(avatarId)
        count = 0
        if guild and self.getAvatarRank(guild, avatarId) >= GUILDRANK_OFFICER:
            count = min(len(guild['tokens']), 255)

        self.sendUpdateToAvatarId(avatarId, 'recvNonPermTokenCount', [count])

    def sendClearTokens(self, type):
        avatarId = self.air.getAvatarIdFromSender()
        guildId, guild = self.getAvatarGuild(avatarId)
        if not guild or self.getAvatarRank(guild, avatarId) < GUILDRANK_OFFICER:
            return

        if type:
            if guild['permToken']:
                self.db.deleteToken(guild['permToken'])
                guild['permToken'] = ''
        else:
            for token in guild['tokens']:
                self.db.deleteToken(token)

            guild['tokens'] = []

        self.db.storeGuild(guildId, guild)

    def sendTokenForJoinRequest(self, tokenString, name):
        avatarId = self.air.getAvatarIdFromSender()
        if self.getAvatarGuild(avatarId)[1]:
            self.d_recvTokenRedeemMessage(avatarId, TOKEN_ERROR_INVALID)
            return

        tokenString = tokenString.replace(' ', '').upper()
        tokenInfo = self.db.getToken(tokenString)
        if not tokenInfo:
            self.d_recvTokenRedeemMessage(avatarId, TOKEN_ERROR_INVALID)
            return

        guildId = tokenInfo['guildId']
        guild = self.db.getGuild(guildId)
        if not guild:
            self.db.deleteToken(tokenString)
            self.d_recvTokenRedeemMessage(avatarId, TOKEN_ERROR_INVALID)
            return

        if self.isGuildFull(guild):
            self.d_recvTokenRedeemMessage(avatarId, TOKEN_ERROR_FULL)
            return

        if tokenInfo['uses'] != TOKEN_PERMANENT:
            tokenInfo['uses'] -= 1
            if tokenInfo['uses'] <= 0:
                self.db.deleteToken(tokenString)
                if tokenString in guild['tokens']:
                    guild['tokens'].remove(tokenString)
            else:
                self.db.storeToken(tokenString, tokenInfo)

        self.addMember(guildId, guild, avatarId, GUILDRANK_MEMBER, name)
        self.d_recvTokenRedeemMessage(avatarId, self.getGuildDisplayName(guildId, guild))

        creatorId = tokenInfo['creatorId']
        if self.isOnline(creatorId) and self.getMember(guild, creatorId):
            self.sendUpdateToAvatarId(creatorId, 'recvTokenRedeemedByPlayerMessage',
                [self.getAvatarName(avatarId) or name])

    # --- Senders ---

    def d_guildStatusUpdate(self, avatarId, guildId, guildName, guildRank):
        self.sendUpdateToAvatarId(avatarId, 'guildStatusUpdate', [guildId, guildName, guildRank])

    def d_guildNameReject(self, avatarId, guildId):
        self.sendUpdateToAvatarId(avatarId, 'guildNameReject', [guildId])

    def d_guildNameChange(self, avatarId, guildName, changeStatus):
        self.sendUpdateToAvatarId(avatarId, 'guildNameChange', [guildName, changeStatus])

    def d_invitationFrom(self, inviteeId, inviterId, inviterName, guildId, guildName):
        self.sendUpdateToAvatarId(inviteeId, 'invitationFrom', [inviterId, inviterName, guildId, guildName])

    def d_guildAcceptInvite(self, inviterId, inviteeId):
        self.sendUpdateToAvatarId(inviterId, 'guildAcceptInvite', [inviteeId])

    def d_guildRejectInvite(self, inviterId, inviteeId, reason):
        self.sendUpdateToAvatarId(inviterId, 'guildRejectInvite', [inviteeId, reason])

    def d_recvTokenInviteValue(self, avatarId, tokenValue, preExistPerm):
        self.sendUpdateToAvatarId(avatarId, 'recvTokenInviteValue', [tokenValue, preExistPerm])

    def d_recvTokenRedeemMessage(self, avatarId, guildName):
        self.sendUpdateToAvatarId(avatarId, 'recvTokenRedeemMessage', [guildName])
