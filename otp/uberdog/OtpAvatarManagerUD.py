from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import PyDatagram
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from otp.distributed.MsgTypes import CLIENTAGENT_EJECT
from otp.uberdog.RejectCode import RejectCode


class AvatarManagerOperationFSM(FSM):
    """
    Base operation for all account based avatar manager requests. The account
    is always retrieved first so that the requested avatar can be verified as
    belonging to the sender before anything is touched in the database.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('AvatarManagerOperationFSM')
    POST_ACCOUNT_STATE = 'Off'

    def __init__(self, mgr, target):
        self.mgr = mgr
        self.target = target
        self.account = None
        self.avList = []

        FSM.__init__(self, self.__class__.__name__)

    def enterKill(self, reason=''):
        self.mgr.killAccount(self.target, reason)
        self.demand('Off')

    def enterOff(self):
        if self.mgr.account2fsm.get(self.target) is self:
            del self.mgr.account2fsm[self.target]

    def enterRetrieveAccount(self):
        self.mgr.air.dbInterface.queryObject(
            self.mgr.air.dbId, self.target, self.__handleRetrieve)

    def __handleRetrieve(self, dclass, fields):
        if dclass != self.mgr.air.dclassesByName['AccountUD']:
            self.demand('Kill', 'Your account object was not found in the database!')
            return

        self.account = fields
        self.avList = list(self.account.get('ACCOUNT_AV_SET', []))
        self.demand(self.POST_ACCOUNT_STATE)


class OtpAvatarManagerUD(DistributedObjectGlobalUD):
    """
    The OTP avatar manager. Avatar listing, creation, deletion and selection have
    been moved to the ClientServicesManager on this server, so the OTP level
    requests are answered with a rejection pointing the client at the CSM.
    Game specific managers extend this to add their own operations.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('OtpAvatarManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.account2fsm = {}

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.notify.info('%s going online' % self.__class__.__name__)

    def delete(self):
        for fsm in list(self.account2fsm.values()):
            fsm.demand('Off')

        self.account2fsm = {}
        DistributedObjectGlobalUD.delete(self)

    def killAccount(self, accountId, reason, code=122):
        datagram = PyDatagram()
        datagram.addServerHeader(
            self.GetAccountConnectionChannel(accountId),
            self.air.ourChannel,
            CLIENTAGENT_EJECT)
        datagram.addUint16(code)
        datagram.addString(reason)
        self.air.send(datagram)

    def runAccountFSM(self, fsmtype, *args):
        sender = self.air.getAccountIdFromSender()
        if not sender:
            self.notify.warning('Received %s from a client that is not logged in!' % fsmtype.__name__)
            return None

        if sender in self.account2fsm:
            self.killAccount(sender, 'An operation is already underway: %s' % self.account2fsm[sender].__class__.__name__)
            return None

        fsm = fsmtype(self, sender)
        self.account2fsm[sender] = fsm
        fsm.request('Start', *args)
        return fsm

    # Client requests:

    def requestAvatarList(self, todo0):
        sender = self.air.getAccountIdFromSender()
        self.notify.debug('requestAvatarList from account %d, list is served by the CSM' % sender)
        self.d_rejectAvatarList(sender, RejectCode.MAY_NOT_LIST_AVATARS)

    def requestAvatarSlot(self, todo0, subId, slot):
        sender = self.air.getAccountIdFromSender()
        self.d_rejectAvatarSlot(sender, RejectCode.NO_LOCK_ON_SLOT, subId, slot)

    def requestPlayAvatar(self, todo0, avatarId, subId):
        sender = self.air.getAccountIdFromSender()
        self.d_rejectPlayAvatar(sender, RejectCode.NOT_YOUR_AVATAR, avatarId)

    def requestRemoveAvatar(self, todo0, avatarId, subId, confirmPassword):
        sender = self.air.getAccountIdFromSender()
        self.d_rejectRemoveAvatar(sender, RejectCode.MAY_NOT_REMOVE_AVATAR)

    def requestShareAvatar(self, todo0, avatarId, subId, shared):
        sender = self.air.getAccountIdFromSender()
        self.d_rejectShareAvatar(sender, RejectCode.INVALID_ACCOUNT)

    # Responses:

    def d_rejectAvatarList(self, accountId, result):
        self.sendUpdateToAccountId(accountId, 'rejectAvatarList', [result])

    def d_rejectAvatarSlot(self, accountId, reasonId, subId, slot):
        self.sendUpdateToAccountId(accountId, 'rejectAvatarSlot', [reasonId, subId, slot])

    def d_avatarSlotResponse(self, accountId, subId, slot):
        self.sendUpdateToAccountId(accountId, 'avatarSlotResponse', [subId, slot])

    def d_rejectPlayAvatar(self, accountId, reasonId, avatarId):
        self.sendUpdateToAccountId(accountId, 'rejectPlayAvatar', [reasonId, avatarId])

    def d_playAvatarResponse(self, accountId, avatarId, subId, access, founder):
        self.sendUpdateToAccountId(accountId, 'playAvatarResponse', [avatarId, subId, access, founder])

    def d_rejectCreateAvatar(self, accountId, result):
        self.sendUpdateToAccountId(accountId, 'rejectCreateAvatar', [result])

    def d_createAvatarResponse(self, accountId, avatarId, subId, access, founder):
        self.sendUpdateToAccountId(accountId, 'createAvatarResponse', [avatarId, subId, access, founder])

    def d_rejectRemoveAvatar(self, accountId, reasonId):
        self.sendUpdateToAccountId(accountId, 'rejectRemoveAvatar', [reasonId])

    def d_removeAvatarResponse(self, accountId, avatarId, subId):
        self.sendUpdateToAccountId(accountId, 'removeAvatarResponse', [avatarId, subId])

    def d_rejectShareAvatar(self, accountId, reasonId):
        self.sendUpdateToAccountId(accountId, 'rejectShareAvatar', [reasonId])

    def d_shareAvatarResponse(self, accountId, avatarId, subId, shared):
        self.sendUpdateToAccountId(accountId, 'shareAvatarResponse', [avatarId, subId, shared])
