# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.band.DistributedBandMemberOV
from direct.distributed import DistributedObjectOV
from otp.otpbase import OTPLocalizer
from pirates.piratesbase import PiratesGlobals, PLocalizer


class DistributedBandMemberOV(DistributedObjectOV.DistributedObjectOV):
    
    notify = directNotify.newCategory('PirateBand')

    def __init__(self, cr):
        DistributedObjectOV.DistributedObjectOV.__init__(self, cr)
        base.localAvatar.bandMember = self

    def delete(self):
        if base.localAvatar.bandMember == self:
            base.localAvatar.bandMember = None
        DistributedObjectOV.DistributedObjectOV.delete(self)
        return

    def d_setChat(self, chat, chatFlags):
        self.sendUpdate('setChat', [chat, chatFlags, 0])

    def b_setChat(self, chat, chatFlags):
        localObj = self.cr.doId2do.get(self.doId, None)
        if localObj is not None:
            localObj.setChat(chat, chatFlags, 0)
        self.d_setChat(chat, chatFlags)
        return

    def d_setWLChat(self, chat, chatFlags):
        self.sendUpdate('setWLChat', [chat, chatFlags, 0])

    def b_setWLChat(self, chat, chatFlags):
        localObj = self.cr.doId2do.get(self.doId, None)
        if localObj is not None:
            localObj.setWLChat(chat, chatFlags, 0)
        self.d_setWLChat(chat, chatFlags)
        return

    def d_setSpeedChat(self, msgIndex):
        self.sendUpdate('setSpeedChat', [base.localAvatar.getDoId(), msgIndex])

    def b_setSpeedChat(self, msgIndex):
        localObj = self.cr.doId2do.get(self.doId, None)
        if localObj is not None:
            localObj.setSpeedChat(self.doId, msgIndex)
        self.d_setSpeedChat(msgIndex)
        return

    def d_setSCQuestChat(self, questInt, msgType, taskNum):
        self.sendUpdate('setSCQuestChat', [base.localAvatar.getDoId(), questInt, msgType, taskNum])

    def b_setSCQuestChat(self, questInt, msgType, taskNum):
        localObj = self.cr.doId2do.get(self.doId, None)
        if localObj is not None:
            localObj.setSCQuestChat(self.doId, questInt, msgType, taskNum)
        self.d_setSCQuestChat(questInt, msgType, taskNum)
        return

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def teleportQuery(self, requesterId, requesterShardId):
        self.cr.teleportMgr.handleAvatarTeleportQuery(requesterId, requesterShardId)

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def teleportResponse(self, responderId, available, shardId, instanceDoId, areaDoId):
        self.cr.teleportMgr.handleAvatarTeleportResponse(responderId, available, shardId, instanceDoId, areaDoId)
# okay decompiling .\pirates\band\DistributedBandMemberOV.pyc
