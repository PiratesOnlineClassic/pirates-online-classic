import json

from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryType


class ItemTypes:
    STACK = 1
    CLOTHING = 2
    HAIR_BEARD = 3
    HAIR_HAIR = 4
    HAIR_MUSTACHE = 5
    JEWELRY = 6
    GOLD = 7


class CodeRedemptionUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('CodeRedemptionUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.verifyEndpoint = config.GetString('code-redeem-verify-url', 'https://api.piratesclassic.com/code/redeem')

    def requestCodeVerification(self, code, username, avatar):
        headers = {
            'User-Agent':' UberDOG UserAgent',
        }

        body = {
            'code': code,
            'username': username
        }

        def handleVerifyCallback(self, data):
            data = json.loads(data)
            success = False

            #TODO: write this

            self.d_notifyClientCodeRedeemStatus(avatar.doId, success)

        self.air.rest.performPostRequest(
            url=self.verifyEndpoint,
            headers=headers,
            content_type='application/json',
            post_body=body,
            callback=handleVerifyCallback)

    def sendCodeForRedemption(self, code, username):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        code = code.lower()
        self.requestCodeVerification(code, username)

    def d_notifyClientCodeRedeemStatus(self, avatarId, status):
        self.notify.debug('Sending redeemp notify status (%s) to avatar (%s)' % (status, avatarId))
        self.sendUpdateToAvatarId(avatarId, 'notifyClientCodeRedeemStatus', [status])
