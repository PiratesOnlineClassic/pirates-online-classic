import time

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta


class TimeManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TimeManagerAI")

    def requestServerTime(self, context):
        self.sendUpdateToAvatarId(self.air.getAvatarIdFromSender(), 'serverTime', [context, globalClockDelta.getRealNetworkTime(bits=32), int(time.time())])

    def setDisconnectReason(self, reason):
        avId = self.air.getAvatarIdFromSender()
        self.air.writeServerEvent('disconnect-reason', avId, reason)
        self.air.disconnectReasons[avId] = reason;

    def setExceptionInfo(self, exception):
        avId = self.air.getAvatarIdFromSender()
        self.air.writeServerEvent('client-exception', avId, exception)
        self.notify.warning("Got exception from %d!\n %s" % (avId, str(exception)))
        del exception

    def setSignature(self, signature, hash, pyc):
        pass

    def setFrameRate(self, fps, deviation, numAvs, locationCode, timeInLocation, timeInGame, gameOptionsCode, vendorId, deviceId,
                     processMemory, pageFileUsage, physicalMemory, pageFaultCount, osInfo, cpuSpeed, numCpuCores, numLogicalCpus, apiName):
        pass

    def setCpuInfo(self, info, cachestatus):
        pass

    def checkForGarbageLeaks(self, todo0):
        pass

    def setNumAIGarbageLeaks(self, todo0):
        pass

    def setClientGarbageLeak(self, num, description):
        pass

    def checkAvOnDistrict(self, todo0, todo1):
        pass
