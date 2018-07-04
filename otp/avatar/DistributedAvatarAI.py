from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals


class DistributedAvatarAI(DistributedSmoothNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAvatarAI')

    def __init__(self, air):
        DistributedSmoothNodeAI.__init__(self, air)
        self.name = ''

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def setLocationName(self, locationName):
        self.locationName = locationName

    def b_setLocationName(self, locationName):
        self.d_setLocationName(locationName)
        self.setLocationName(locationName)

    def d_setLocationName(self, locationName):
        pass

    def getLocationName(self):
        return self.locationName

    def setActivity(self, activity):
        self.activity = activity

    def d_setActivity(self, activity):
        pass

    def b_setActivity(self, activity):
        self.d_setActivity(activity)
        self.setActivity(activity)

    def getActivity(self):
        return self.activity

    def getRadius(self):
        return OTPGlobals.AvatarDefaultRadius

    def checkAvOnShard(self, avId):
        self.sendUpdateToAvatarId(self.air.getAvatarIdFromSender(), 'confirmAvOnShard', [
            avId, avId in self.air.doId2do])
