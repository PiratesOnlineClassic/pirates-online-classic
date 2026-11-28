from direct.directnotify import DirectNotifyGlobal

from otp.uberdog.OtpAvatarManagerUD import OtpAvatarManagerUD, AvatarManagerOperationFSM
from otp.uberdog.RejectCode import RejectCode

from pirates.piratesbase import PiratesGlobals


def makePatternName(gender, firstIndex, prefixIndex, suffixIndex):
    """
    Renders a pick-a-name pattern into the avatar's name. The indices match
    the (padded) name lists the client NameGUI scrolls through, which are the
    same lists exposed by PiratesGlobals.maleNames and femaleNames.
    """

    if gender == 'f':
        nameLists = PiratesGlobals.femaleNames
    else:
        nameLists = PiratesGlobals.maleNames

    def getPart(nameList, index):
        if index < 0 or index >= len(nameList):
            return ''
        return nameList[index].strip()

    parts = []
    first = getPart(nameLists[1], firstIndex)
    if first:
        parts.append(first)

    prefix = getPart(nameLists[2], prefixIndex)
    suffix = getPart(nameLists[3], suffixIndex)
    if prefix in PiratesGlobals.lastNamePrefixesCapped:
        suffix = suffix.capitalize()

    lastName = prefix + suffix
    if lastName:
        parts.append(lastName)

    return ' '.join(parts)


class AvatarOperationFSM(AvatarManagerOperationFSM):
    """
    Retrieves the account and then the target avatar, making sure the avatar
    belongs to the account before handing over to the operation's own state.
    """

    POST_ACCOUNT_STATE = 'RetrieveAvatar'
    POST_AVATAR_STATE = 'Off'

    def enterStart(self, avId, *args):
        self.avId = avId
        self.avatarFields = None
        self.setup(*args)
        self.demand('RetrieveAccount')

    def setup(self, *args):
        pass

    def enterRetrieveAvatar(self):
        if not self.avId or self.avId not in self.avList:
            self.reject(RejectCode.NOT_YOUR_AVATAR)
            self.demand('Kill', 'Tried to modify an avatar not in the account!')
            return

        self.mgr.air.dbInterface.queryObject(
            self.mgr.air.dbId, self.avId, self.__handleAvatar)

    def __handleAvatar(self, dclass, fields):
        if dclass != self.mgr.air.dclassesByName['DistributedPlayerPirateUD']:
            self.reject(RejectCode.NO_AVATAR)
            self.demand('Kill', "One of the account's avatars is invalid!")
            return

        self.avatarFields = fields
        self.demand(self.POST_AVATAR_STATE)

    def reject(self, reasonId):
        pass


class PatternNameFSM(AvatarOperationFSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('PatternNameFSM')
    POST_AVATAR_STATE = 'SetName'

    def setup(self, nicknameIndex, firstIndex, prefixIndex, suffixIndex):
        self.nicknameIndex = nicknameIndex
        self.firstIndex = firstIndex
        self.prefixIndex = prefixIndex
        self.suffixIndex = suffixIndex

    def reject(self, reasonId):
        self.mgr.d_patternNameResponse(self.target, False)

    def enterSetName(self):
        wishNameState = self.avatarFields.get('WishNameState', ('',))[0]
        if wishNameState != 'OPEN':
            self.notify.warning('Avatar %d is not in a nameable state (%s)!' % (self.avId, wishNameState))
            self.reject(RejectCode.NOT_YOUR_AVATAR)
            self.demand('Off')
            return

        gender = self.avatarFields.get('setGender', ('m',))[0]
        name = makePatternName(gender, self.firstIndex, self.prefixIndex, self.suffixIndex)
        if not name:
            self.notify.warning('Avatar %d sent an empty name pattern!' % self.avId)
            self.reject(RejectCode.NOT_YOUR_AVATAR)
            self.demand('Off')
            return

        self.mgr.air.dbInterface.updateObject(
            self.mgr.air.dbId,
            self.avId,
            self.mgr.air.dclassesByName['DistributedPlayerPirateUD'],
            {'WishNameState': ('',),
             'WishName': ('',),
             'setName': (name,)})

        self.mgr.air.writeServerEvent('avatarNamed', avId=self.avId, name=name, pattern=True)
        self.mgr.d_patternNameResponse(self.target, True)
        self.demand('Off')


class FinalizeNameFSM(AvatarOperationFSM):
    """
    The client acknowledges the result of a typed name request from the
    avatar chooser. An approved name replaces the avatar's name and a
    rejected one opens the avatar back up for naming.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('FinalizeNameFSM')
    POST_AVATAR_STATE = 'Finalize'

    def enterFinalize(self):
        wishNameState = self.avatarFields['WishNameState'][0]
        wishName = self.avatarFields['WishName'][0]
        name = self.avatarFields['setName'][0]

        if wishNameState == 'APPROVED':
            wishNameState = ''
            name = wishName
            wishName = ''
        elif wishNameState == 'REJECTED':
            wishNameState = 'OPEN'
            wishName = ''
        else:
            self.notify.warning('Tried to finalize name on avatar %d in %s state!' % (self.avId, wishNameState))
            self.demand('Off')
            return

        csm = getattr(self.mgr.air, 'csm', None)
        if csm and hasattr(csm, 'accountDB'):
            csm.accountDB.removeNameRequest(self.avId)

        self.mgr.air.dbInterface.updateObject(
            self.mgr.air.dbId,
            self.avId,
            self.mgr.air.dclassesByName['DistributedPlayerPirateUD'],
            {'WishNameState': (wishNameState,),
             'WishName': (wishName,),
             'setName': (name,)},
            {'WishNameState': self.avatarFields['WishNameState'],
             'WishName': self.avatarFields['WishName'],
             'setName': self.avatarFields['setName']})

        self.mgr.air.writeServerEvent('avatarNameFinalized', avId=self.avId, name=name)
        self.demand('Off')


class ShareAvatarFSM(AvatarOperationFSM):
    """
    Avatar sharing between the sub accounts of a family account. Accounts on
    this server only ever carry a single sub account, so once the avatar has
    been validated the request is rejected.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('ShareAvatarFSM')
    POST_AVATAR_STATE = 'Share'

    def setup(self, subId, shared):
        self.subId = subId
        self.shared = shared

    def reject(self, reasonId):
        self.mgr.d_rejectShareAvatar(self.target, reasonId)

    def enterShare(self):
        self.reject(RejectCode.INVALID_ACCOUNT)
        self.demand('Off')


class DistributedAvatarManagerUD(OtpAvatarManagerUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAvatarManagerUD')

    # Client requests:

    def requestCreateAvatar(self, todo0, subId):
        # Avatars are created through the ClientServicesManager.
        sender = self.air.getAccountIdFromSender()
        self.d_rejectCreateAvatar(sender, RejectCode.MAY_NOT_CREATE_AVATAR)

    def requestPopulateAvatar(self, todo0, avId, avatarData, usePattern, nicknameIndex, firstIndex, prefixIndex, suffixIndex):
        # Avatars are populated through the ClientServicesManager.
        sender = self.air.getAccountIdFromSender()
        self.d_populateAvatarResponse(sender, False)

    def requestPatternName(self, todo0, avId, nicknameIndex, firstIndex, prefixIndex, suffixIndex):
        self.runAccountFSM(PatternNameFSM, avId, nicknameIndex, firstIndex, prefixIndex, suffixIndex)

    def requestFinalize(self, todo0, avId):
        self.runAccountFSM(FinalizeNameFSM, avId)

    def requestShareAvatar(self, todo0, avatarId, subId, shared):
        self.runAccountFSM(ShareAvatarFSM, avatarId, subId, shared)

    # Server requests:

    def requestAwardableAvatars(self, accountId, context):
        """
        Asks for every avatar of an account. The AwardMaker uses this to let an
        award be given to a specific pirate on the account.
        """

        replyTo = self.air.getMsgSender()

        def callback(avIds, names):
            self.sendUpdateToChannel(replyTo, 'recvAwardableAvatars', [context, avIds, names])

        self.getAwardableAvatars(accountId, callback)

    def getAwardableAvatars(self, accountId, callback):
        def handleAccount(dclass, fields):
            if dclass != self.air.dclassesByName['AccountUD']:
                self.notify.warning('Account %d was not found for awardable avatars!' % accountId)
                callback([], [])
                return

            avIds = [avId for avId in fields.get('ACCOUNT_AV_SET', []) if avId]
            if not avIds:
                callback([], [])
                return

            names = {}

            def handleAvatar(avId, dclass, fields):
                if dclass == self.air.dclassesByName['DistributedPlayerPirateUD']:
                    names[avId] = fields.get('setName', ('',))[0]
                else:
                    names[avId] = None

                if len(names) == len(avIds):
                    validIds = [avId for avId in avIds if names[avId] is not None]
                    callback(validIds, [names[avId] for avId in validIds])

            for avId in avIds:
                self.air.dbInterface.queryObject(self.air.dbId, avId,
                    lambda dclass, fields, avId=avId: handleAvatar(avId, dclass, fields))

        self.air.dbInterface.queryObject(self.air.dbId, accountId, handleAccount)

    def requestAvatarGender(self, avatarId, context):
        """
        Asks for the gender of an avatar. CodeRedemption uses this to decide
        which version of a clothing reward the avatar should receive.
        """

        replyTo = self.air.getMsgSender()

        def callback(gender):
            self.sendUpdateToChannel(replyTo, 'recvAvatarGender', [avatarId, gender, context])

        self.getAvatarGender(avatarId, callback)

    def getAvatarGender(self, avatarId, callback):
        def handleAvatar(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedPlayerPirateUD']:
                self.notify.warning('Avatar %d was not found for gender request!' % avatarId)
                callback('')
                return

            callback(fields.get('setGender', ('',))[0])

        self.air.dbInterface.queryObject(self.air.dbId, avatarId, handleAvatar)

    # Responses:

    def d_populateAvatarResponse(self, accountId, success):
        self.sendUpdateToAccountId(accountId, 'populateAvatarResponse', [success])

    def d_patternNameResponse(self, accountId, success):
        self.sendUpdateToAccountId(accountId, 'patternNameResponse', [success])

    def d_sendAvIdList(self, accountId, avIds):
        self.sendUpdateToAccountId(accountId, 'sendAvIdList', [avIds])
