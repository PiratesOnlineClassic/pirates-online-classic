from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal
from otp.distributed import OtpDoGlobals

class DistributedTravelAgentAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTravelAgentAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

    def requestInitLocUDtoAI(self, avatarId):
        if not avatarId:
            self.notify.warning('Cannot init AI loc, unknown avatar %d!' % avatarId)
            return

        if avatarId in self.air.doId2do:
            self.notify.warning('Cannot init AI loc, avatar %d, already exists!' % avatarId)
            return

        def avatarArrived(avatar):
            if not avatar:
                self.notify.warning('Cannot init AI loc, avatar %d, did not arrive!' % avatarId)
                return

            avatar.d_relayTeleportLoc(self.air.districtId, self.air.distributedDistrict.zoneId,
                self.air.teleportMgr.doId)

        self.acceptOnce('generate-%d' % avatarId, avatarArrived)
        self.air.setAI(avatarId, self.air.ourChannel)
