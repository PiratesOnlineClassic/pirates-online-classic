import semidbm
import base64
import hashlib
import hmac
import json
import time
import urllib.request, urllib.error, urllib.parse

from panda3d.core import *
from panda3d.direct import DCPacker

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import *
from direct.fsm.FSM import FSM

from otp.distributed import OtpDoGlobals
from otp.distributed.MsgTypes import *

from pirates.pirate.HumanDNA import HumanDNA
from pirates.quest.QuestConstants import LocationIds
from pirates.piratesbase import PiratesGlobals

# Import from PyCrypto only if we are using a database that requires it. This
# allows local hosted and developer builds of the game to run without it:
accountDBType = base.config.GetString('accountdb-type', 'developer')
if accountDBType == 'remote':
    from Crypto.Cipher import AES

# Sometimes we'll want to force a specific access level, such as on the
# developer server:
minAccessLevel = base.config.GetInt('min-access-level', 100)
accountServerEndpoint = base.config.GetString('account-server-endpoint', '')  # TODO
accountServerSecret = base.config.GetString('account-server-secret', '6163636f756e7473')

http = HTTPClient()
http.setVerifySsl(0)

# The client creates a brand new pirate with this placeholder name as soon as
# the player starts the tutorial, the pirate is only made and named later on
# in the tutorial's Make-A-Pirate (see PiratesClientRepository.enterCreateAvatar):
DefaultAvatarName = 'dbp'


def isAvatarUnfinished(fields):
    """
    Returns True when the avatar is still the placeholder pirate the client
    created for the tutorial, i.e. its owner never finished Make-A-Pirate and
    never chose a name for it. Such a pirate is of no use to anybody and is
    removed from the account once its owner leaves.
    """

    # Once the avatar has progressed any further into the tutorial than
    # Make-A-Pirate it is a real pirate, no matter what its name is...
    tutorial = fields.get('setTutorial', (PiratesGlobals.TUT_STARTED,))[0]
    if tutorial > PiratesGlobals.TUT_MADE_PIRATE:
        return False

    # A pick-a-name pattern replaces the placeholder name, a typed name is
    # kept as a wish name until it has been approved...
    name = fields.get('setName', ('',))[0]
    if name not in (DefaultAvatarName, ''):
        return False

    wishNameState = fields.get('WishNameState', ('',))[0]
    wishName = fields.get('WishName', ('',))[0]
    if wishNameState != 'OPEN' or wishName:
        return False

    return True


def executeHttpRequest(url, **extras):
    timestamp = str(int(time.time()))
    signature = hmac.new(accountServerSecret, timestamp, hashlib.sha256)
    request = urllib.request.Request(accountServerEndpoint + url)
    request.add_header('User-Agent', 'POC-CSM')
    request.add_header('X-CSM-Timestamp', timestamp)
    request.add_header('X-CSM-Signature', signature.hexdigest())
    for k, v in list(extras.items()):
        request.add_header('X-CSM-' + k, v)
    try:
        return urllib.request.urlopen(request).read()
    except:
        return None

#blacklist = executeHttpRequest('names/blacklist.json')
#if blacklist:
#    blacklist = json.loads(blacklist)


def judgeName(name):
    if not name:
        return False

    """
    if blacklist:
        for namePart in name.split(' '):
            namePart = namePart.lower()
            if len(namePart) < 1:
                return False

            for banned in blacklist.get(namePart[0], []):
                if banned in namePart:
                    return False
    """
    return True

# --- ACCOUNT DATABASES ---
# These classes make up the available account databases for Pirates Online Classic.
# Databases with login tokens use the PyCrypto module for decrypting them.
# DeveloperAccountDB is a special database that accepts a username, and assigns
# each user with 600 access automatically upon login.


class AccountDB:
    notify = directNotify.newCategory('AccountDB')

    def __init__(self, csm):
        self.csm = csm

        filename = base.config.GetString('account-bridge-filename', 'astron/databases/account-bridge')
        self.dbm = semidbm.open(filename, 'c')

    def addNameRequest(self, avId, name):
        return 'Success'

    def getNameStatus(self, avId):
        return 'APPROVED'

    def removeNameRequest(self, avId):
        return 'Success'

    def lookup(self, username, callback):
        pass  # Inheritors should override this.

    def storeAccountID(self, userId, accountId, callback):
        self.dbm[str(userId)] = str(accountId)  # semidbm only allows strings.
        if getattr(self.dbm, 'sync', None):
            self.dbm.sync()
            callback(True)
        else:
            self.notify.warning('Unable to associate user %s with account %d!' % (userId, accountId))
            callback(False)


class DeveloperAccountDB(AccountDB):
    notify = directNotify.newCategory('DeveloperAccountDB')

    def lookup(self, username, callback):
        # Let's check if this user's ID is in your account database bridge:
        if username.encode() not in self.dbm:
            # Nope. Let's associate them with a brand new Account object! We
            # will assign them with 600 access just because they are a
            # developer:
            response = {
                'success': True,
                'userId': username,
                'accountId': 0,
                'accessLevel': max(600, minAccessLevel) if config.GetBool('want-dev-access', False) else max(0, minAccessLevel)
            }

        else:

            # We have an account already, let's return what we've got:
            response = {
                'success': True,
                'userId': username,
                'accountId': int(self.dbm[str(username)]),
            }

        callback(response)


# This is the same as the DeveloperAccountDB, except it doesn't automatically
# give the user an access level of 600. Instead, the first user that is created
# gets 700 access, and every user created afterwards gets 100 access:

class LocalAccountDB(AccountDB):
    notify = directNotify.newCategory('LocalAccountDB')

    def lookup(self, username, callback):
        # Let's check if this user's ID is in your account database bridge:
        if username.encode() not in self.dbm:
            # Nope. Let's associate them with a brand new Account object!
            response = {
                'success': True,
                'userId': username,
                'accountId': 0,
                'accessLevel': max((700 if not self.dbm else 100), minAccessLevel)
            }
            callback(response)
            return response

        else:

            # We have an account already, let's return what we've got:
            response = {
                'success': True,
                'userId': username,
                'accountId': int(self.dbm[str(username)])
            }
            callback(response)
            return response


class RemoteAccountDB(AccountDB):
    notify = directNotify.newCategory('RemoteAccountDB')

    def addNameRequest(self, avId, name):
        return executeHttpRequest('names/append', ID=str(avId), Name=name)

    def getNameStatus(self, avId):
        return executeHttpRequest('names/status/?Id=' + str(avId))

    def removeNameRequest(self, avId):
        return executeHttpRequest('names/remove', ID=str(avId))

    def lookup(self, token, callback):
        # First, base64 decode the token:
        try:
            token = base64.b64decode(token)
        except TypeError:
            self.notify.warning('Could not decode the provided token!')
            response = {
                'success': False,
                'reason': "Can't decode this token."
            }
            callback(response)
            return response

        # Ensure this token is a valid size:
        if (not token) or ((len(token) % 16) != 0):
            self.notify.warning('Invalid token length!')
            response = {
                'success': False,
                'reason': 'Invalid token length.'
            }
            callback(response)
            return response

        # Next, decrypt the token using AES-128 in CBC mode:
        accountServerSecret = base.config.GetString(
            'account-server-secret', '6163636f756e7473')

        # Ensure that our secret is the correct size:
        if len(accountServerSecret) > AES.block_size:
            self.notify.warning('account-server-secret is too big!')
            accountServerSecret = accountServerSecret[:AES.block_size]
        elif len(accountServerSecret) < AES.block_size:
            self.notify.warning('account-server-secret is too small!')
            accountServerSecret += '\x80'
            while len(accountServerSecret) < AES.block_size:
                accountServerSecret += '\x00'

        # Take the initialization vector off the front of the token:
        iv = token[:AES.block_size]

        # Truncate the token to get our cipher text:
        cipherText = token[AES.block_size:]

        # Decrypt!
        cipher = AES.new(accountServerSecret, mode=AES.MODE_CBC, IV=iv)
        try:
            token = json.loads(cipher.decrypt(cipherText).replace('\x00', ''))
            if ('timestamp' not in token) or (not isinstance(token['timestamp'], int)):
                raise ValueError
            if ('userid' not in token) or (not isinstance(token['userid'], int)):
                raise ValueError
            if ('accesslevel' not in token) or (not isinstance(token['accesslevel'], int)):
                raise ValueError
        except ValueError as e:
            print(e)
            self.notify.warning('Invalid token.')
            response = {
                'success': False,
                'reason': 'Invalid token.'
            }
            callback(response)
            return response

        # Next, check if this token has expired:
        expiration = base.config.GetInt('account-token-expiration', 1800)
        tokenDelta = int(time.time()) - token['timestamp']
        if tokenDelta > expiration:
            response = {
                'success': False,
                'reason': 'This token has expired.'
            }
            callback(response)
            return response

        # This token is valid. That's all we need to know. Next, let's check if
        # this user's ID is in your account database bridge:
        if str(token['userid']) not in self.dbm:

            # Nope. Let's associate them with a brand new Account object!
            response = {
                'success': True,
                'userId': token['userid'],
                'accountId': 0,
                'accessLevel': max(int(token['accesslevel']), minAccessLevel)
            }
            callback(response)
            return response

        else:

            # Yep. Let's return their account ID and access level!
            response = {
                'success': True,
                'userId': token['userid'],
                'accountId': int(self.dbm[str(token['userid'])]),
                'accessLevel': max(int(token['accesslevel']), minAccessLevel)
            }
            callback(response)
            return response


# --- FSMs ---
class OperationFSM(FSM):
    TARGET_CONNECTION = False

    def __init__(self, csm, target):
        self.csm = csm
        self.target = target

        FSM.__init__(self, self.__class__.__name__)

    def enterKill(self, reason=''):
        if self.TARGET_CONNECTION:
            self.csm.killConnection(self.target, reason)
        else:
            self.csm.killAccount(self.target, reason)
        self.demand('Off')

    def enterOff(self):
        if self.TARGET_CONNECTION:
            del self.csm.connection2fsm[self.target]
        else:
            del self.csm.account2fsm[self.target]


class LoginAccountFSM(OperationFSM):
    notify = directNotify.newCategory('LoginAccountFSM')
    TARGET_CONNECTION = True

    def enterStart(self, token):
        self.token = token
        self.demand('QueryAccountDB')

    def enterQueryAccountDB(self):
        self.csm.accountDB.lookup(self.token, self.__handleLookup)

    def __handleLookup(self, result):
        if not result.get('success'):
            self.csm.air.writeServerEvent('tokenRejected', target=self.target, token=self.token)
            self.demand('Kill', result.get('reason', 'The account server rejected your token.'))
            return

        self.userId = result.get('userId', 0)
        self.accountId = result.get('accountId', 0)
        self.accessLevel = result.get('accessLevel', 0)
        self.paidLevel = 2 #TODO: write this
        if self.accountId:
            self.demand('RetrieveAccount')
        else:
            self.demand('CreateAccount')

    def enterRetrieveAccount(self):
        self.csm.air.dbInterface.queryObject(
            self.csm.air.dbId, self.accountId, self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields
        self.demand('SetAccount')

    def enterCreateAccount(self):
        self.account = {
            'ACCOUNT_AV_SET': [0] * 4,
            'ACCOUNT_AV_SET_DEL': [],
            'CREATED': time.ctime(),
            'LAST_LOGIN': time.ctime(),
            'ACCOUNT_ID': str(self.userId),
            'ACCESS_LEVEL': self.accessLevel,
            'PAID_LEVEL': self.paidLevel
        }
        self.csm.air.dbInterface.createObject(
            self.csm.air.dbId,
            self.csm.air.dclassesByName['AccountUD'],
            self.account,
            self.__handleCreate)

    def __handleCreate(self, accountId):
        if self.state != 'CreateAccount':
            self.notify.warning('Received a create account response outside of the CreateAccount state.')
            return

        if not accountId:
            self.notify.warning('Database failed to construct an account object!')
            self.demand('Kill', 'Your account object could not be created in the game database.')
            return

        self.accountId = accountId
        self.csm.air.writeServerEvent('accountCreated', accountId=accountId)
        self.demand('StoreAccountID')

    def enterStoreAccountID(self):
        self.csm.accountDB.storeAccountID(
            self.userId,
            self.accountId,
            self.__handleStored)

    def __handleStored(self, success=True):
        if not success:
            self.demand('Kill', 'The account server could not save your user ID!')
            return

        self.demand('SetAccount')

    def enterSetAccount(self):
        # If necessary, update their account information:
        if self.accessLevel:
            self.csm.air.dbInterface.updateObject(
                self.csm.air.dbId,
                self.accountId,
                self.csm.air.dclassesByName['AccountUD'],
                {'ACCESS_LEVEL': self.accessLevel})

        if self.paidLevel:
            self.csm.air.dbInterface.updateObject(
                self.csm.air.dbId,
                self.accountId,
                self.csm.air.dclassesByName['AccountUD'],
                {'PAID_LEVEL': self.paidLevel})        

        # If there's anybody on the account, kill them for redundant login:
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.csm.GetAccountConnectionChannel(self.accountId),
            self.csm.air.ourChannel,
            CLIENTAGENT_EJECT)
        datagram.addUint16(100)
        datagram.addString('This account has been logged in from elsewhere.')
        self.csm.air.send(datagram)

        # Next, add this connection to the account channel.
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.target,
            self.csm.air.ourChannel,
            CLIENTAGENT_OPEN_CHANNEL)
        datagram.addChannel(self.csm.GetAccountConnectionChannel(self.accountId))
        self.csm.air.send(datagram)

        # Now set their sender channel to represent their account affiliation:
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.target,
            self.csm.air.ourChannel,
            CLIENTAGENT_SET_CLIENT_ID)

        # Account ID in high 32 bits, 0 in low (no avatar):
        datagram.addChannel(self.accountId << 32)
        self.csm.air.send(datagram)

        # Un-sandbox them!
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.target,
            self.csm.air.ourChannel,
            CLIENTAGENT_SET_STATE)

        datagram.addUint16(2)  # ESTABLISHED
        self.csm.air.send(datagram)

        # Update the last login timestamp:
        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.accountId,
            self.csm.air.dclassesByName['AccountUD'],
            {'LAST_LOGIN': time.ctime(),
             'ACCOUNT_ID': str(self.userId)})

        # We're done.
        self.csm.air.writeServerEvent('accountLogin', target=self.target, accountId=self.accountId, userId=self.userId)
        self.csm.sendUpdateToChannel(self.target, 'acceptLogin', [])
        self.demand('Off')


class CreateAvatarFSM(OperationFSM):
    notify = directNotify.newCategory('CreateAvatarFSM')

    def enterStart(self, dna, index, name):
        # Basic sanity-checking:
        if index >= 4:
            self.demand('Kill', 'Invalid index specified!')
            return

        if not HumanDNA().isValidNetString(dna):
            self.demand('Kill', 'Invalid DNA specified!')
            return

        self.index = index
        self.dna = dna
        self.name = name

        # Okay, we're good to go, let's query their account.
        self.demand('RetrieveAccount')

    def enterRetrieveAccount(self):
        self.csm.air.dbInterface.queryObject(
            self.csm.air.dbId, self.target, self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields

        self.avList = self.account['ACCOUNT_AV_SET']
        # Sanitize:
        self.avList = self.avList[:4]
        self.avList += [0] * (4-len(self.avList))

        # Make sure the index is open:
        if self.avList[self.index]:
            self.demand('Kill', 'This avatar slot is already taken by another avatar!')
            return

        # Okay, there's space. Let's create the avatar!
        self.demand('CreateAvatar')

    def enterCreateAvatar(self):
        pirateFields = {}

        humanDNA = HumanDNA()
        humanDNA.makeFromNetString(self.dna)

        dclass = self.csm.air.dclassesByName['HumanDNA']
        for fieldIndex in range(dclass.getNumFields()):
            field = dclass.getInheritedField(fieldIndex)
            if not field.asAtomicField():
                continue

            fieldValue = getattr(humanDNA, field.getName().replace('set', 'get'))()
            if isinstance(fieldValue, list):
                pirateFields[field.getName()] = fieldValue
            else:
                pirateFields[field.getName()] = (fieldValue,)

        # The client's DNA blob carries a tutorial value too, a new avatar
        # always starts at the beginning of the tutorial...
        pirateFields['setTutorial'] = (PiratesGlobals.TUT_STARTED,)
        pirateFields['setName'] = (self.name,)
        pirateFields['WishNameState'] = ('OPEN',)
        pirateFields['WishName'] = ('',)
        pirateFields['setDISLid'] = (self.target,)

        if base.config.GetBool('skip-tutorial', False):
            pirateFields['setReturnLocation'] = (LocationIds.PORT_ROYAL_ISLAND,)

        self.csm.air.dbInterface.createObject(
            self.csm.air.dbId,
            self.csm.air.dclassesByName['DistributedPlayerPirateUD'],
            pirateFields,
            self.__handleCreate)

    def __handleCreate(self, avId):
        if not avId:
            self.demand('Kill', 'Database failed to create the new avatar object!')
            return

        self.avId = avId
        self.demand('StoreAvatar')

    def enterStoreAvatar(self):
        # Associate the avatar with the account...
        self.avList[self.index] = self.avId
        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.target,
            self.csm.air.dclassesByName['AccountUD'],
            {'ACCOUNT_AV_SET': self.avList},
            {'ACCOUNT_AV_SET': self.account['ACCOUNT_AV_SET']},
            self.__handleStoreAvatar)

    def __handleStoreAvatar(self, fields):
        if fields:
            self.demand('Kill', 'Database failed to associate the new avatar to your account!')
            return

        # Otherwise, we're done!
        self.csm.air.writeServerEvent('avatarCreated', avId=self.avId, target=self.target, dna=self.dna.hex(), avatarSlot=self.index)
        self.csm.sendUpdateToAccountId(self.target, 'createAvatarResp', [self.avId])
        self.demand('Off')


class AvatarOperationFSM(OperationFSM):
    POST_ACCOUNT_STATE = 'Off'  # This needs to be overridden.

    def enterRetrieveAccount(self):
        # Query the account:
        self.csm.air.dbInterface.queryObject(
            self.csm.air.dbId, self.target, self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields

        self.avList = self.account['ACCOUNT_AV_SET']

        # Sanitize:
        self.avList = self.avList[:4]
        self.avList += [0] * (4-len(self.avList))

        self.demand(self.POST_ACCOUNT_STATE)


class GetAvatarsFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('GetAvatarsFSM')
    POST_ACCOUNT_STATE = 'QueryAvatars'

    def enterStart(self):
        self.demand('RetrieveAccount')

    def enterQueryAvatars(self):
        self.pendingAvatars = set()
        self.avatarFields = {}
        for avId in self.avList:
            if avId:
                self.pendingAvatars.add(avId)

                def response(dclass, fields, avId=avId):
                    if self.state != 'QueryAvatars':
                        return
                    if dclass != self.csm.air.dclassesByName['DistributedPlayerPirateUD']:
                        self.demand('Kill', "One of the account's avatars is invalid!")
                        return
                    self.avatarFields[avId] = fields
                    self.pendingAvatars.remove(avId)
                    if not self.pendingAvatars:
                        self.demand('RemoveUnfinishedAvatars')

                self.csm.air.dbInterface.queryObject(
                    self.csm.air.dbId,
                    avId,
                    response)

        if not self.pendingAvatars:
            self.demand('RemoveUnfinishedAvatars')

    def enterRemoveUnfinishedAvatars(self):
        # Any pirate that was never finished in Make-A-Pirate, and is not being
        # played right now, was left behind by a player who quit the tutorial
        # (or by a server going down while they were in it). Get rid of it
        # before showing the player their pirates...
        self.pendingAvatars = set()
        for avId, fields in list(self.avatarFields.items()):
            if self.csm.isAvatarActive(avId):
                continue

            if isAvatarUnfinished(fields):
                self.pendingAvatars.add(avId)

        for avId in list(self.pendingAvatars):
            self.csm.removeUnfinishedAvatar(self.target, avId,
                lambda removed, avId=avId: self.__handleRemoved(avId, removed))

        if not self.pendingAvatars:
            self.demand('SendAvatars')

    def __handleRemoved(self, avId, removed):
        if self.state != 'RemoveUnfinishedAvatars':
            return

        if removed:
            del self.avatarFields[avId]

        self.pendingAvatars.discard(avId)
        if not self.pendingAvatars:
            self.demand('SendAvatars')

    def enterSendAvatars(self):
        potentialAvs = []

        for avId, fields in list(self.avatarFields.items()):
            index = self.avList.index(avId)
            wishNameState = fields.get('WishNameState', [''])[0]
            name = fields['setName'][0]
            nameState = 0

            if wishNameState == 'OPEN':
                nameState = 1
            elif wishNameState == 'PENDING':
                actualNameState = self.csm.accountDB.getNameStatus(avId)
                self.csm.air.dbInterface.updateObject(
                    self.csm.air.dbId,
                    avId,
                    self.csm.air.dclassesByName['DistributedPlayerPirateUD'],
                    {'WishNameState': [actualNameState]}
                )
                if actualNameState == 'PENDING':
                    nameState = 2
                if actualNameState == 'APPROVED':
                    nameState = 3
                    name = fields['WishName'][0]
                elif actualNameState == 'REJECTED':
                    nameState = 4
            elif wishNameState == 'APPROVED':
                nameState = 3
            elif wishNameState == 'REJECTED':
                nameState = 4

            humanDNA = HumanDNA()
            for fieldName, fieldValue in list(fields.items()):
                if hasattr(humanDNA, fieldName):
                    getattr(humanDNA, fieldName)(*fieldValue)

            potentialAvs.append([
                avId, name, humanDNA.makeNetString(), index, nameState])

        self.csm.sendUpdateToAccountId(self.target, 'setAvatars', [potentialAvs])
        self.demand('Off')

class DeleteAvatarFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('DeleteAvatarFSM')
    POST_ACCOUNT_STATE = 'RetrieveAvatar'

    def enterStart(self, avId):
        self.avId = avId
        self.demand('RetrieveAccount')

    def enterRetrieveAvatar(self):
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to delete an avatar not in the account!')
            return

        if self.csm.isAvatarActive(self.avId):
            self.demand('Kill', 'Tried to delete an avatar that is being played!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        self.avatarFields = fields
        self.demand('ProcessDelete')

    def enterProcessDelete(self):
        index = self.avList.index(self.avId)
        self.avList[index] = 0

        avsDeleted = list(self.account.get('ACCOUNT_AV_SET_DEL', []))
        avsDeleted.append([self.avId, int(time.time())])

        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.target,
            self.csm.air.dclassesByName['AccountUD'],
            {'ACCOUNT_AV_SET': self.avList,
             'ACCOUNT_AV_SET_DEL': avsDeleted},
            {'ACCOUNT_AV_SET': self.account['ACCOUNT_AV_SET'],
             'ACCOUNT_AV_SET_DEL': self.account['ACCOUNT_AV_SET_DEL']},
            self.__handleDelete)

    def __handleDelete(self, fields):
        if fields:
            status = False
            self.csm.sendUpdateToAccountId(self.target, 'acknowledgeDeleteAvatarResp', [self.avId, status])
            self.demand('Kill', 'Database failed to mark the avatar as deleted!')
            return

        self.csm.air.writeServerEvent('avatarDeleted', avId=self.avId, target=self.target)
        self.csm.avatarDeleted(self.avId, self.target, self.avatarFields)

        # The client asks for its avatar list again as soon as it hears back
        # from us, so we are done here:
        status = True
        self.csm.sendUpdateToAccountId(self.target, 'acknowledgeDeleteAvatarResp', [self.avId, status])
        self.demand('Off')


class SetNameTypedFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('SetNameTypedFSM')
    POST_ACCOUNT_STATE = 'RetrieveAvatar'

    def enterStart(self, avId, name):
        self.avId = avId
        self.name = name

        if self.avId:
            self.demand('RetrieveAccount')
            return

        # Hmm, self.avId was 0. Okay, let's just cut to the judging:
        self.demand('JudgeName')

    def enterRetrieveAvatar(self):
        if self.avId and self.avId not in self.avList:
            self.demand('Kill', 'Tried to name an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        if fields['WishNameState'][0] != 'OPEN':
            self.demand('Kill', 'Avatar is not in a namable state!')
            return

        self.demand('JudgeName')

    def enterJudgeName(self):
        # Let's see if the name is valid:
        status = judgeName(self.name)

        if self.avId and status:
            resp = self.csm.accountDB.addNameRequest(self.avId, self.name)
            if resp != 'Success':
                status = False
            else:
                self.csm.air.dbInterface.updateObject(
                    self.csm.air.dbId,
                    self.avId,
                    self.csm.air.dclassesByName['DistributedPlayerPirateUD'],
                    {'WishNameState': ('PENDING',),
                     'WishName': (self.name,)})

        if self.avId:
            self.csm.air.writeServerEvent('avatarWishname', avId=self.avId, name=self.name)

        self.csm.sendUpdateToAccountId(self.target, 'setNameTypedResp', [self.avId, status])
        self.demand('Off')

class SetNamePatternFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('SetNamePatternFSM')
    POST_ACCOUNT_STATE = 'RetrieveAvatar'

    def enterStart(self, avId, pattern):
        self.avId = avId
        self.pattern = pattern

        self.demand('RetrieveAccount')

    def enterRetrieveAvatar(self):
        if self.avId and self.avId not in self.avList:
            self.demand('Kill', 'Tried to name an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        if fields['WishNameState'][0] != 'OPEN':
            self.demand('Kill', 'Avatar is not in a namable state!')
            return

        self.demand('SetName')

    def enterSetName(self):
        # Render the pattern into a string:
        parts = []
        for p, f in self.pattern:
            part = self.csm.nameGenerator.nameDictionary.get(p, ('', ''))[1]
            if f:
                part = part[:1].upper() + part[1:]
            else:
                part = part.lower()
            parts.append(part)

        parts[2] += parts.pop(3) # Merge 2&3 (the last name) as there should be no space.
        while '' in parts:
            parts.remove('')
        name = ' '.join(parts)

        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.avId,
            self.csm.air.dclassesByName['DistributedPlayerPirateUD'],
            {'WishNameState': ('',),
             'WishName': ('',),
             'setName': (name,)})

        self.csm.air.writeServerEvent('avatarNamed', avId=self.avId, name=name)
        self.csm.sendUpdateToAccountId(self.target, 'setNamePatternResp', [self.avId, 1])
        self.demand('Off')


class AcknowledgeNameFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('AcknowledgeNameFSM')
    POST_ACCOUNT_STATE = 'GetTargetAvatar'

    def enterStart(self, avId):
        self.avId = avId
        self.demand('RetrieveAccount')

    def enterGetTargetAvatar(self):
        # Make sure the target avatar is part of the account:
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to acknowledge name on an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        # Process the WishNameState change.
        wishNameState = fields['WishNameState'][0]
        wishName = fields['WishName'][0]
        name = fields['setName'][0]

        if wishNameState == 'APPROVED':
            wishNameState = ''
            name = wishName
            wishName = ''
            self.csm.accountDB.removeNameRequest(self.avId)
        elif wishNameState == 'REJECTED':
            wishNameState = 'OPEN'
            wishName = ''
            self.csm.accountDB.removeNameRequest(self.avId)
        else:
            self.demand('Kill', "Tried to acknowledge name on an avatar in %s state!" % wishNameState)
            return

        # Push the change back through:
        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.avId,
            self.csm.air.dclassesByName['DistributedPlayerPirateUD'],
            {'WishNameState': (wishNameState,),
             'WishName': (wishName,),
             'setName': (name,)},
            {'WishNameState': fields['WishNameState'],
             'WishName': fields['WishName'],
             'setName': fields['setName']})

        self.csm.sendUpdateToAccountId(self.target, 'acknowledgeAvatarNameResp', [])
        self.demand('Off')


class LoadAvatarFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('LoadAvatarFSM')
    POST_ACCOUNT_STATE = 'GetTargetAvatar'

    def enterStart(self, avId):
        self.avId = avId
        self.demand('RetrieveAccount')

    def enterGetTargetAvatar(self):
        # Make sure the target avatar is part of the account:
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to play an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        self.avatar = fields
        self.demand('SetAvatar')

    def enterSetAvatarTask(self, channel, inventoryId, task):
        channel = self.csm.GetAccountConnectionChannel(self.target)

        # Finally, grant ownership and shut down.
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.avId,
            self.csm.air.ourChannel,
            STATESERVER_OBJECT_SET_OWNER)
        datagram.addChannel(self.target << 32 | self.avId)
        self.csm.air.send(datagram)

        # add a post remove for removing the avatar as a session object on the ClientAgent
        datagramCleanup = PyDatagram()
        datagramCleanup.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_REMOVE_SESSION_OBJECT)

        datagramCleanup.addUint32(self.avId)

        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_ADD_POST_REMOVE)
        # Must include the blob length prefix; appendData alone truncates.
        datagram.addBlob(datagramCleanup.getMessage())
        self.csm.air.send(datagram)

        self.csm.air.clientAddSessionObject(self.csm.GetPuppetConnectionChannel(self.avId), self.avId)

        def inventoryActivatedCallback(inventoryId):
            self.csm.air.writeServerEvent('avatarChosen', avId=self.avId, target=self.target)

            # Let the friends managers know this avatar is now online:
            self.csm.air.avatarFriendsManager.comingOnline(self.avId, self.target)
            self.csm.air.playerFriendsManager.comingOnline(self.avId, self.target)
            self.demand('Off')

        # activate the avatar's inventory on the DBSS
        self.csm.air.inventoryManager.activateInventory(self.avId, inventoryId,
            inventoryActivatedCallback)

        return task.done

    def enterSetAvatar(self):
        channel = self.csm.GetAccountConnectionChannel(self.target)

        # First, give them a POSTREMOVE to unload the avatar, just in case they
        # disconnect while we're working.
        datagramCleanup = PyDatagram()
        datagramCleanup.addServerHeader(
            self.avId,
            channel,
            STATESERVER_OBJECT_DELETE_RAM)

        datagramCleanup.addUint32(self.avId)

        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_ADD_POST_REMOVE)
        # Must include the blob length prefix; appendData alone truncates.
        datagram.addBlob(datagramCleanup.getMessage())
        self.csm.air.send(datagram)

        # We also want to hear about them disconnecting, so that we can clean
        # up after the avatar ourselves:
        datagramCleanup = self.csm.air.netMessenger.prepare('avatarDisconnected',
            [self.target, self.avId])

        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_ADD_POST_REMOVE)
        datagram.addBlob(datagramCleanup.getMessage())
        self.csm.air.send(datagram)

        self.csm.activeAvatars[self.avId] = self.target

        # get the doId of the avatar's inventory object that it will
        # be activated on by the DBSS...
        self.csm.air.inventoryManager.queryInventory(self.avId, self.inventoryQueryCallback)

    def inventoryQueryCallback(self, inventoryId):
        channel = self.csm.GetAccountConnectionChannel(self.target)

        # Activate the avatar on the DBSS:
        adminAccess = self.account.get('ACCESS_LEVEL', 0)
        adminAccess = adminAccess - adminAccess % 100

        paidLevel = self.account.get('PAID_LEVEL', 0)

        self.csm.air.sendActivate(self.avId, 0, 0, self.csm.air.dclassesByName['DistributedPlayerPirateUD'],
            {'setAdminAccess': (adminAccess,), 'setInventoryId': (inventoryId,), 'setAccess': (paidLevel,)})

        # Next, add them to the avatar channel:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_OPEN_CHANNEL)
        datagram.addChannel(self.csm.GetPuppetConnectionChannel(self.avId))
        self.csm.air.send(datagram)

        # Now set their sender channel to represent their account affiliation:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_SET_CLIENT_ID)
        datagram.addChannel(self.target << 32 | self.avId)
        self.csm.air.send(datagram)

        # Eliminate race conditions.
        taskMgr.doMethodLater(0.2, self.enterSetAvatarTask, 'avatarTask-%s' % self.avId,
            extraArgs=[channel, inventoryId], appendTask=True)

class UnloadAvatarFSM(OperationFSM):
    notify = directNotify.newCategory('UnloadAvatarFSM')

    def enterStart(self, avId):
        self.avId = avId

        # We don't even need to query the account, we know the avatar is being played!
        self.demand('UnloadAvatar')

    def enterUnloadAvatar(self):
        channel = self.csm.GetAccountConnectionChannel(self.target)

        # Clear off POSTREMOVE:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_CLEAR_POST_REMOVES)
        self.csm.air.send(datagram)

        # Remove avatar channel:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_CLOSE_CHANNEL)
        datagram.addChannel(self.csm.GetPuppetConnectionChannel(self.avId))
        self.csm.air.send(datagram)

        # Reset sender channel:
        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.csm.air.ourChannel,
            CLIENTAGENT_SET_CLIENT_ID)
        datagram.addChannel(self.target<<32)
        self.csm.air.send(datagram)

        # Unload avatar object:
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.avId,
            channel,
            STATESERVER_OBJECT_DELETE_RAM)
        datagram.addUint32(self.avId)
        self.csm.air.send(datagram)

        # Our POSTREMOVEs are gone, so tell the friends and guild managers ourselves:
        self.csm.air.avatarFriendsManager.goingOffline(self.avId)
        self.csm.air.playerFriendsManager.goingOffline(self.avId)
        self.csm.air.guildManager.avatarOffline(self.avId)

        self.csm.activeAvatars.pop(self.avId, None)

        # Done!
        self.csm.air.writeServerEvent('avatarUnload', avId=self.avId)
        self.demand('Off')

        # Leaving the tutorial before the pirate was made in Make-A-Pirate
        # leaves nothing worth keeping behind:
        self.csm.removeUnfinishedAvatar(self.target, self.avId)


class PopulateAvatarFSM(AvatarOperationFSM):
    notify = directNotify.newCategory('PopulateAvatarFSM')
    POST_ACCOUNT_STATE = 'RetrieveAvatar'

    def enterStart(self, avId, dna, usePattern, p1, p2, p3, p4):
        self.avId = avId
        self.dna = dna
        self.usePattern = usePattern
        # p1=nick, p2=first, p3=prefix, p4=suffix (indices into name lists)
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

        # Validate the DNA
        if not HumanDNA().isValidNetString(dna):
            self.demand('Kill', 'Invalid DNA specified!')
            return

        self.demand('RetrieveAccount')

    def enterRetrieveAvatar(self):
        if self.avId not in self.avList:
            self.demand('Kill', 'Tried to populate an avatar not in the account!')
            return

        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.csm.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        # Make-A-Pirate is only ever shown at the very start of the tutorial...
        if fields.get('setTutorial', (PiratesGlobals.TUT_STARTED,))[0] > PiratesGlobals.TUT_STARTED:
            self.demand('Kill', 'Tried to populate an avatar that has already been made!')
            return

        self.avatarFields = fields
        self.demand('UpdateAvatar')

    def enterUpdateAvatar(self):
        # Build the update fields from the DNA
        updateFields = {}

        humanDNA = HumanDNA()
        humanDNA.makeFromNetString(self.dna)

        dclass = self.csm.air.dclassesByName['HumanDNA']
        for fieldIndex in range(dclass.getNumFields()):
            field = dclass.getInheritedField(fieldIndex)
            if not field.asAtomicField():
                continue

            fieldValue = getattr(humanDNA, field.getName().replace('set', 'get'))()
            if isinstance(fieldValue, list):
                updateFields[field.getName()] = fieldValue
            else:
                updateFields[field.getName()] = (fieldValue,)

        # Handle name pattern if requested
        if self.usePattern:
            # Get the name lists based on gender
            gender = humanDNA.getGender()
            if gender == 'f':
                nameLists = PiratesGlobals.femaleNames
            else:
                nameLists = PiratesGlobals.maleNames

            # Pattern is (nick, first, prefix, suffix) indices
            # nameLists[0] = nicknames (not used)
            # nameLists[1] = first names
            # nameLists[2] = prefixes
            # nameLists[3] = suffixes
            parts = []

            # First name (self.p2 = first name index)
            if self.p2 > 0 and self.p2 < len(nameLists[1]):
                parts.append(nameLists[1][self.p2].strip())

            # Last name = prefix + suffix
            lastName = ''
            if self.p3 > 0 and self.p3 < len(nameLists[2]):
                prefix = nameLists[2][self.p3].strip()
                lastName = prefix
                # Check if prefix needs suffix to be capitalized
                if prefix in PiratesGlobals.lastNamePrefixesCapped:
                    if self.p4 > 0 and self.p4 < len(nameLists[3]):
                        lastName += nameLists[3][self.p4].strip().capitalize()
                else:
                    if self.p4 > 0 and self.p4 < len(nameLists[3]):
                        lastName += nameLists[3][self.p4].strip()

            if lastName:
                parts.append(lastName)

            name = ' '.join(parts)

            if name:
                updateFields['WishNameState'] = ('',)
                updateFields['WishName'] = ('',)
                updateFields['setName'] = (name,)

        # The avatar's tutorial progress is owned by the AI, the client's
        # Make-A-Pirate DNA must never roll it back...
        updateFields.pop('setTutorial', None)

        # Update the avatar in the database
        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.avId,
            self.csm.air.dclassesByName['DistributedPlayerPirateUD'],
            updateFields)

        # The avatar is populated from inside of the tutorial while it is already
        # active on the state server, update the live object as well so the AI
        # and other clients see the new pirate without having to log out first...
        self.sendLiveAvatarFields(updateFields)

        self.csm.air.writeServerEvent('avatarPopulated', avId=self.avId, target=self.target)
        self.csm.sendUpdateToAccountId(self.target, 'populateAvatarResp', [True])
        self.demand('Off')

    def sendLiveAvatarFields(self, fields):
        dclass = self.csm.air.dclassesByName['DistributedPlayerPirateUD']
        fieldPacker = DCPacker()
        fieldCount = 0
        for fieldName, value in list(fields.items()):
            field = dclass.getFieldByName(fieldName)
            if field is None:
                continue

            fieldPacker.rawPackUint16(field.getNumber())
            fieldPacker.beginPack(field)
            field.packArgs(fieldPacker, value)
            fieldPacker.endPack()
            fieldCount += 1

        if not fieldCount:
            return

        dg = PyDatagram()
        dg.addServerHeader(self.avId, self.csm.air.ourChannel, STATESERVER_OBJECT_SET_FIELDS)
        dg.addUint32(self.avId)
        dg.addUint16(fieldCount)
        dg.appendData(fieldPacker.getBytes())
        self.csm.air.send(dg)


class RemoveUnfinishedAvatarFSM(FSM):
    """
    Removes a pirate that was never finished in Make-A-Pirate from its
    account. This is not an account operation; it runs once the pirate's owner
    has left the game (they may not even be connected anymore).
    """
    notify = directNotify.newCategory('RemoveUnfinishedAvatarFSM')
    MAX_ACCOUNT_ATTEMPTS = 3

    def __init__(self, csm, accountId, avId):
        FSM.__init__(self, self.__class__.__name__)
        self.csm = csm
        self.accountId = accountId
        self.avId = avId
        self.avatarFields = None
        self.account = None
        self.attempts = 0
        self.removed = False
        self.callbacks = []

    def enterStart(self):
        self.demand('RetrieveAvatar')

    def enterRetrieveAvatar(self):
        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.avId,
                                             self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if self.state != 'RetrieveAvatar':
            return

        if dclass != self.csm.air.dclassesByName['DistributedPlayerPirateUD']:
            self.demand('Off')
            return

        # Never touch a pirate that is finished, being played or that was not
        # created for this account:
        if not isAvatarUnfinished(fields) or self.csm.isAvatarActive(self.avId):
            self.demand('Off')
            return

        if fields.get('setDISLid', (0,))[0] != self.accountId:
            self.notify.warning('Unfinished avatar %d does not belong to account %d!' % (
                self.avId, self.accountId))
            self.demand('Off')
            return

        self.avatarFields = fields
        self.demand('RetrieveAccount')

    def enterRetrieveAccount(self):
        self.csm.air.dbInterface.queryObject(self.csm.air.dbId, self.accountId,
                                             self.__handleAccount)

    def __handleAccount(self, dclass, fields):
        if self.state != 'RetrieveAccount':
            return

        if dclass != self.csm.air.dclassesByName['AccountUD']:
            self.notify.warning('Account %d of unfinished avatar %d was not found!' % (
                self.accountId, self.avId))
            self.demand('Off')
            return

        self.account = fields
        if self.avId not in self.account.get('ACCOUNT_AV_SET', []):
            # It never made it into the account, there is only the avatar
            # object itself to get rid of:
            self.demand('DeleteAvatar')
            return

        self.demand('UpdateAccount')

    def enterUpdateAccount(self):
        avList = list(self.account['ACCOUNT_AV_SET'])
        avList[avList.index(self.avId)] = 0

        self.csm.air.dbInterface.updateObject(
            self.csm.air.dbId,
            self.accountId,
            self.csm.air.dclassesByName['AccountUD'],
            {'ACCOUNT_AV_SET': avList},
            {'ACCOUNT_AV_SET': self.account['ACCOUNT_AV_SET']},
            self.__handleUpdate)

    def __handleUpdate(self, fields):
        if self.state != 'UpdateAccount':
            return

        if fields is not None:
            # Somebody else changed the account in the meantime, try again:
            self.attempts += 1
            if self.attempts >= self.MAX_ACCOUNT_ATTEMPTS:
                self.notify.warning('Failed to remove unfinished avatar %d from account %d!' % (
                    self.avId, self.accountId))
                self.demand('Off')
                return

            self.demand('RetrieveAccount')
            return

        self.demand('DeleteAvatar')

    def enterDeleteAvatar(self):
        self.removed = True
        self.csm.air.writeServerEvent('unfinishedAvatarDeleted', avId=self.avId, accountId=self.accountId)
        self.csm.avatarDeleted(self.avId, self.accountId, self.avatarFields)
        self.demand('Off')

    def enterOff(self):
        if self.csm.avatar2removeFsm.get(self.avId) is self:
            del self.csm.avatar2removeFsm[self.avId]

        callbacks, self.callbacks = self.callbacks, []
        for callback in callbacks:
            callback(self.removed)


class DeleteAvatarObjectsFSM(FSM):
    """
    Permanently removes a deleted avatar from the database, along with the
    avatar's inventory and everything the inventory holds: ships (with their
    own inventories and parts), quests, treasure maps and so on.
    """
    notify = directNotify.newCategory('DeleteAvatarObjectsFSM')

    # Only ever remove objects that can belong to a single avatar:
    OWNED_CLASS_NAMES = (
        'DistributedInventory',
        'PirateInventory',
        'DistributedTreasureMap',
        'DistributedGoldReceipt',
        'DistributedQuest',
        'PlayerShip',
        'DistributedHull',
        'DistributedMast')

    def __init__(self, csm, avId):
        FSM.__init__(self, self.__class__.__name__)
        self.csm = csm
        self.avId = avId
        self.pendingObjects = set()
        self.visitedObjects = set()
        self.deletedObjects = []

    def enterStart(self, fields):
        self.visitedObjects.add(self.avId)
        self.deletedObjects.append(self.avId)
        self.demand('QueryObjects', fields)

    def enterQueryObjects(self, fields):
        self.queryOwnedObjects(fields)
        if not self.pendingObjects:
            self.demand('DeleteObjects')

    def queryOwnedObjects(self, fields):
        doIds = []

        inventoryId = fields.get('setInventoryId', (0,))[0]
        if inventoryId:
            doIds.append(inventoryId)

        for category, doId in fields.get('setDoIds', ([],))[0]:
            doIds.append(doId)

        for doId in doIds:
            if not doId or doId in self.visitedObjects:
                continue

            self.visitedObjects.add(doId)
            self.pendingObjects.add(doId)
            self.csm.air.dbInterface.queryObject(self.csm.air.dbId, doId,
                lambda dclass, fields, doId=doId: self.__handleObject(doId, dclass, fields))

    def __handleObject(self, doId, dclass, fields):
        if self.state != 'QueryObjects':
            return

        self.pendingObjects.discard(doId)
        if dclass is None:
            self.notify.warning('Object %d of avatar %d is already gone.' % (doId, self.avId))
        elif dclass.getName() not in self.OWNED_CLASS_NAMES:
            self.notify.warning('Not deleting %s object %d held by avatar %d!' % (
                dclass.getName(), doId, self.avId))
        else:
            self.deletedObjects.append(doId)
            self.queryOwnedObjects(fields)

        if not self.pendingObjects:
            self.demand('DeleteObjects')

    def enterDeleteObjects(self):
        for doId in self.deletedObjects:
            self.csm.air.dbInterface.deleteObject(self.csm.air.dbId, doId)

        self.csm.air.writeServerEvent('avatarObjectsDeleted', avId=self.avId,
            objects=len(self.deletedObjects))
        self.demand('Off')


# --- CLIENT SERVICES MANAGER UBERDOG ---
class ClientServicesManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('ClientServicesManagerUD')

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        # These keep track of the connection/account IDs currently undergoing an
        # operation on the CSM. This is to prevent (hacked) clients from firing up more
        # than one operation at a time, which could potentially lead to exploitation
        # of race conditions.
        self.connection2fsm = {}
        self.account2fsm = {}

        # These keep track of the avatars currently being played and the
        # unfinished avatars waiting to be removed from their accounts:
        self.activeAvatars = {}
        self.avatar2removeFsm = {}

        self.air.netMessenger.accept('avatarDisconnected', self, self.avatarDisconnected)

        # Temporary HMAC key:
        self.key = 'cd09ed406383f3d3ebb62b9ce23d41dd'

        # Instantiate our account DB interface:
        if accountDBType == 'developer':
            self.accountDB = DeveloperAccountDB(self)
        elif accountDBType == 'local':
            self.accountDB = LocalAccountDB(self)
        elif accountDBType == 'remote':
            self.accountDB = RemoteAccountDB(self)
        else:
            self.notify.error('Invalid accountdb-type: ' + accountDBType)

    def killConnection(self, connId, reason, code=122):
        datagram = PyDatagram()
        datagram.addServerHeader(
            connId,
            self.air.ourChannel,
            CLIENTAGENT_EJECT)
        datagram.addUint16(code)
        datagram.addString(reason)
        self.air.send(datagram)

    def killConnectionFSM(self, connId):
        fsm = self.connection2fsm.get(connId)

        if not fsm:
            self.notify.warning('Tried to kill connection %d for duplicate FSM, but none exists!' % connId)
            return

        self.killConnection(connId, 'An operation is already underway: ' + fsm.__class__.__name__)

    def killAccount(self, accountId, reason, code=122):
        self.killConnection(self.GetAccountConnectionChannel(accountId), reason, code)

    def killAccountFSM(self, accountId):
        fsm = self.account2fsm.get(accountId)
        if not fsm:
            self.notify.warning('Tried to kill account %d for duplicate FSM, but none exists!' % accountId)
            return

        self.killAccount(accountId, 'An operation is already underway: ' + fsm.__class__.__name__)

    def runAccountFSM(self, fsmtype, *args):
        sender = self.air.getAccountIdFromSender()

        if not sender:
            self.killAccount(sender, 'Client is not logged in.')

        if sender in self.account2fsm:
            self.killAccountFSM(sender)
            return

        self.account2fsm[sender] = fsmtype(self, sender)
        self.account2fsm[sender].request('Start', *args)

    def isAvatarActive(self, avId):
        return avId in self.activeAvatars

    def avatarDisconnected(self, accountId, avId):
        # Sent to us by the Client Agent as a post remove; the avatar's owner
        # disconnected while they were playing it.
        if self.activeAvatars.get(avId) == accountId:
            del self.activeAvatars[avId]

        self.air.writeServerEvent('avatarDisconnected', avId=avId, accountId=accountId)
        self.removeUnfinishedAvatar(accountId, avId)

    def removeUnfinishedAvatar(self, accountId, avId, callback=None):
        fsm = self.avatar2removeFsm.get(avId)
        if fsm:
            if callback:
                fsm.callbacks.append(callback)

            return

        fsm = RemoveUnfinishedAvatarFSM(self, accountId, avId)
        if callback:
            fsm.callbacks.append(callback)

        self.avatar2removeFsm[avId] = fsm
        fsm.request('Start')

    def avatarDeleted(self, avId, accountId, fields):
        # Nobody should be left knowing a pirate that no longer exists:
        friendsList = fields.get('setFriendsList', ([],))[0]
        self.air.avatarFriendsManager.avatarDeleted(avId, friendsList)
        self.air.playerFriendsManager.avatarDeleted(avId, accountId)
        self.air.guildManager.avatarDeleted(avId)
        self.accountDB.removeNameRequest(avId)

        DeleteAvatarObjectsFSM(self, avId).request('Start', fields)

    def login(self, cookie, address, authKey):
        self.notify.debug('Received login cookie %r from %d' % (cookie, self.air.getMsgSender()))

        sender = self.air.getMsgSender()

        banned_addresses = []

        # Time to check this login to see if its authentic
        digest_maker = hmac.new(self.key.encode('utf-8'), digestmod=hashlib.md5)
        digest_maker.update(cookie.encode('utf-8') if isinstance(cookie, str) else cookie)
        serverKey = digest_maker.hexdigest()

        # This login is not authentic...
        if not hmac.compare_digest(serverKey, authKey):
            self.killConnection(sender, ' ')
            return

        if sender >> 32:
            self.killConnection(sender, 'Client is already logged in.', 100)
            return

        # This user is banned.
        if address in banned_addresses:
            self.killConnection(sender, ' ')
            return

        if sender in self.connection2fsm:
            self.killConnectionFSM(sender)
            return

        self.connection2fsm[sender] = LoginAccountFSM(self, sender)
        self.connection2fsm[sender].request('Start', cookie)

    def requestAvatars(self):
        self.notify.debug('Received avatar list request from %d' % (self.air.getMsgSender()))
        self.runAccountFSM(GetAvatarsFSM)

    def createAvatar(self, dna, index, name):
        self.runAccountFSM(CreateAvatarFSM, dna, index, name)

    def deleteAvatar(self, avId):
        self.runAccountFSM(DeleteAvatarFSM, avId)

    def setNameTyped(self, avId, name):
        self.runAccountFSM(SetNameTypedFSM, avId, name)

    def setNamePattern(self, avId, p1, f1, p2, f2, p3, f3, p4, f4):
        self.runAccountFSM(SetNamePatternFSM, avId, [(p1, f1), (p2, f2), (p3, f3), (p4, f4)])

    def acknowledgeAvatarName(self, avId):
        self.runAccountFSM(AcknowledgeNameFSM, avId)

    def populateAvatar(self, avId, dna, usePattern, p1, p2, p3, p4):
        self.runAccountFSM(PopulateAvatarFSM, avId, dna, usePattern, p1, p2, p3, p4)

    def chooseAvatar(self, avId):
        currentAvId = self.air.getAvatarIdFromSender()
        accountId = self.air.getAccountIdFromSender()
        if currentAvId and avId:
            self.killAccount(accountId, 'A Pirate is already chosen!')
            return
        elif not currentAvId and not avId:
            return

        if avId:
            self.runAccountFSM(LoadAvatarFSM, avId)
        else:
            self.runAccountFSM(UnloadAvatarFSM, currentAvId)
