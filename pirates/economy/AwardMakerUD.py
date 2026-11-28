from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

from otp.distributed.OtpDoGlobals import OTP_DO_ID_PIRATES_AVATAR_ACCESSORIES_MANAGER
from pirates.economy import AwardGlobals


class AwardMakerUD(DistributedObjectGlobalUD):
    """
    Hands out awards (gold, stackable items and accessories) to avatars. The
    award is sent to every district through the AvatarAccessoriesManager; the
    district hosting the avatar gives it out and reports back. If nobody
    answers in time the avatar is assumed to be offline and the award fails.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('AwardMakerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.context = 0
        self.pendingAwards = {}

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.notify.info('%s going online' % self.__class__.__name__)

    def delete(self):
        for context in list(self.pendingAwards.keys()):
            taskMgr.remove(self.uniqueName('awardTimeout-%d' % context))

        self.pendingAwards = {}
        DistributedObjectGlobalUD.delete(self)

    def getAwardableAvatars(self, accountId, callback):
        """
        Calls back with (avIds, names) for the account, so a tool can choose
        which pirate receives an award.
        """

        self.air.avatarManager.getAwardableAvatars(accountId, callback)

    def giveAward(self, avatarId, awardType, itemId, quantity=1, callback=None):
        if awardType not in AwardGlobals.AwardTypes:
            self.notify.warning('Tried to give unknown award type %s!' % awardType)
            if callback:
                callback(False)
            return 0

        self.context = (self.context + 1) & 0xFFFFFFFF
        context = self.context
        self.pendingAwards[context] = (avatarId, awardType, itemId, quantity, callback)

        taskMgr.doMethodLater(AwardGlobals.AwardTimeout, self.__awardTimeout,
            self.uniqueName('awardTimeout-%d' % context), extraArgs=[context])

        dclass = self.air.dclassesByName['AvatarAccessoriesManager']
        datagram = dclass.aiFormatUpdate('requestAward', OTP_DO_ID_PIRATES_AVATAR_ACCESSORIES_MANAGER,
            OTP_DO_ID_PIRATES_AVATAR_ACCESSORIES_MANAGER, self.air.ourChannel,
            [context, awardType, avatarId, itemId, quantity])
        self.air.send(datagram)
        return context

    def __awardTimeout(self, context):
        if context not in self.pendingAwards:
            return

        avatarId = self.pendingAwards[context][0]
        self.notify.info('Award %d for avatar %d timed out, avatar is not online.' % (context, avatarId))
        self.awardFailure(context)

    def __finishAward(self, context, success):
        award = self.pendingAwards.pop(context, None)
        if award is None:
            return

        taskMgr.remove(self.uniqueName('awardTimeout-%d' % context))
        avatarId, awardType, itemId, quantity, callback = award
        self.air.writeServerEvent('awardMaker', avId=avatarId, awardType=awardType,
            itemId=itemId, quantity=quantity, success=success)

        if callback:
            callback(success)

    # Responses:

    def recvAwardableAvatars(self, context, avIds, names):
        # Remote avatar manager response; local callers use getAwardableAvatars.
        self.notify.debug('recvAwardableAvatars %d: %s' % (context, avIds))

    def awardSuccess(self, context):
        self.__finishAward(context, True)

    def awardFailure(self, context):
        self.__finishAward(context, False)
