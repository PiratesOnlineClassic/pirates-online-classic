import semidbm

from panda3d.core import ConfigVariableList

from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

from pirates.economy import AwardGlobals


class ItemTypes:
    STACK = AwardGlobals.STACK
    CLOTHING = AwardGlobals.CLOTHING
    HAIR_BEARD = AwardGlobals.HAIR_BEARD
    HAIR_HAIR = AwardGlobals.HAIR_HAIR
    HAIR_MUSTACHE = AwardGlobals.HAIR_MUSTACHE
    JEWELRY = AwardGlobals.JEWELRY
    GOLD = AwardGlobals.GOLD
    TATTOO = AwardGlobals.TATTOO


class CodeReward:
    # clothing differs between male and female pirates, so a reward
    # may carry a separate item for female avatars...

    def __init__(self, code, awardType, itemId, quantity=1, femaleItemId=None):
        self.code = code
        self.awardType = awardType
        self.itemId = itemId
        self.quantity = quantity
        self.femaleItemId = femaleItemId

    def getItemId(self, gender):
        if gender == 'f' and self.femaleItemId is not None:
            return self.femaleItemId

        return self.itemId

    def needsGender(self):
        return self.femaleItemId is not None

    @staticmethod
    def fromConfig(entry):
        # code;awardType;itemId[;quantity[;femaleItemId]]
        parts = entry.split(';')
        if len(parts) < 3:
            raise ValueError('Invalid code redemption entry: %s' % entry)

        quantity = int(parts[3]) if len(parts) > 3 and parts[3] else 1
        femaleItemId = int(parts[4]) if len(parts) > 4 and parts[4] else None
        return CodeReward(parts[0].lower(), int(parts[1]), int(parts[2]), quantity, femaleItemId)


class CodeRedemptionUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('CodeRedemptionUD')

    STATUS_FAILED = 0
    STATUS_SUCCESS = 1

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.verifyEndpoint = config.GetString('code-redeem-verify-url', '')
        self.codes = {}
        self.pendingAvatars = set()
        self.redeemedDB = None

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        for entry in ConfigVariableList('code-redemption-code'):
            try:
                reward = CodeReward.fromConfig(entry)
            except ValueError as e:
                self.notify.warning(str(e))
                continue

            self.codes[reward.code] = reward

        filename = config.GetString('code-redemption-bridge-filename', 'astron/databases/code-redemption-bridge')
        self.redeemedDB = semidbm.open(filename, 'c')
        self.notify.info('%s going online with %d codes' % (self.__class__.__name__, len(self.codes)))

    def delete(self):
        if self.redeemedDB:
            self.redeemedDB.close()
            self.redeemedDB = None

        DistributedObjectGlobalUD.delete(self)

    def online(self):
        pass

    def getRedeemedKey(self, code, avatarId):
        # semidbm keeps it's keys as bytes, a str key is never found in it:
        return ('%s|%d' % (code, avatarId)).encode('utf-8')

    def hasRedeemed(self, code, avatarId):
        return self.getRedeemedKey(code, avatarId) in self.redeemedDB

    def setRedeemed(self, code, avatarId):
        self.redeemedDB[self.getRedeemedKey(code, avatarId)] = b'1'
        if getattr(self.redeemedDB, 'sync', None):
            self.redeemedDB.sync()

    def sendCodeForRedemption(self, code, username):
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            self.notify.warning('Received code redemption from a client without an avatar!')
            return

        code = code.strip().lower()
        if not code or len(code) > 64:
            self.d_notifyClientCodeRedeemStatus(avatarId, self.STATUS_FAILED)
            return

        if avatarId in self.pendingAvatars:
            self.notify.debug('Avatar %d already has a code redemption pending.' % avatarId)
            return

        if self.hasRedeemed(code, avatarId):
            self.d_notifyClientCodeRedeemStatus(avatarId, self.STATUS_FAILED)
            return

        self.pendingAvatars.add(avatarId)
        reward = self.codes.get(code)
        if reward:
            self.processReward(avatarId, reward)
        elif self.verifyEndpoint:
            self.requestCodeVerification(avatarId, code, username)
        else:
            self.finishRedemption(avatarId, code, False)

    def requestCodeVerification(self, avatarId, code, username):
        headers = {
            'User-Agent': 'UberDOG UserAgent',
        }

        body = {
            'code': code,
            'username': username,
            'avatarId': avatarId
        }

        def handleVerifyCallback(data):
            if not isinstance(data, dict) or not data.get('success'):
                self.finishRedemption(avatarId, code, False)
                return

            try:
                reward = CodeReward(code, int(data['awardType']), int(data['itemId']),
                    int(data.get('quantity', 1)),
                    int(data['femaleItemId']) if data.get('femaleItemId') is not None else None)
            except (KeyError, TypeError, ValueError):
                self.notify.warning('Invalid code verification response for %s: %s' % (code, data))
                self.finishRedemption(avatarId, code, False)
                return

            self.processReward(avatarId, reward)

        self.air.rest.performJsonPostRequest(
            url=self.verifyEndpoint,
            headers=headers,
            post_body=body,
            callback=handleVerifyCallback)

    def processReward(self, avatarId, reward):
        if reward.needsGender():
            self.air.avatarManager.getAvatarGender(avatarId,
                lambda gender: self.giveReward(avatarId, reward, gender))
        else:
            self.giveReward(avatarId, reward, '')

    def giveReward(self, avatarId, reward, gender):
        self.air.awardMaker.giveAward(avatarId, reward.awardType, reward.getItemId(gender),
            reward.quantity, callback=lambda success: self.finishRedemption(avatarId, reward.code, success))

    def finishRedemption(self, avatarId, code, success):
        self.pendingAvatars.discard(avatarId)
        if success:
            self.setRedeemed(code, avatarId)

        self.air.writeServerEvent('codeRedemption', avId=avatarId, code=code, success=success)
        self.d_notifyClientCodeRedeemStatus(avatarId, self.STATUS_SUCCESS if success else self.STATUS_FAILED)

    def recvAvatarGender(self, avatarId, gender, context):
        self.notify.debug('recvAvatarGender %d: %s' % (avatarId, gender))

    def d_notifyClientCodeRedeemStatus(self, avatarId, status):
        self.notify.debug('Sending redeem status (%s) to avatar (%s)' % (status, avatarId))
        self.sendUpdateToAvatarId(avatarId, 'notifyClientCodeRedeemStatus', [status])
