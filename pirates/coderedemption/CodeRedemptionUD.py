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


class AwardTypes:
    GOLD = 1

    AWARD_ID = {
        GOLD: [
            ItemTypes.STACK,
            InventoryType.GoldInPocket,  # Item type
            None,
            200,  # Amount
            # TODO: Pull from the localizer??
            'Gold'  # Code Name
        ],
    }


class CodeRedemptionUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('CodeRedemptionUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

    def getAwardFromCode(self, code):
        for award in AwardTypes.AWARD_ID:
            award = AwardTypes.AWARD_ID.get(award)
            codeword = award[4].lower()
            if codeword == code.lower():
                return award

    def tryRedeemCode(self, code):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        reward = self.getAwardFromCode(code)

        if reward is not None:
            amount = reward[3]

            # TODO: Rewards

        else:
            self.notify.warning('Could not redeem code; No reward found for: %s' % code)

    def sendCodeForRedemption(self, code):
        code = code.lower()

        avatarId = self.air.getAvatarIdFromSender()
        response = self.tryRedeemCode(code)

        reward = self.getAwardFromCode(code)
        if reward is not None:
            reward = reward[4].lower()
            if code in reward:
                self.d_notifyClientCodeRedeemStatus(avatarId, 1)
        else:
            self.d_notifyClientCodeRedeemStatus(avatarId, 0)
        return response

    def d_notifyClientCodeRedeemStatus(self, avatarId, status):
        self.sendUpdateToAvatarId(avatarId, 'notifyClientCodeRedeemStatus', [status])
