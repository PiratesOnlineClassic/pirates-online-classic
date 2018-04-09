# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.PAvatarHandle
from otp.avatar.AvatarHandle import AvatarHandle


class PAvatarHandle(AvatarHandle):
    __module__ = __name__

    def getBandId(self):
        if __dev__:
            pass
        return (0, 0)

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def sendTeleportQuery(self, sendToId, localShardId):
        if __dev__:
            pass

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def sendTeleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId=None):
        if __dev__:
            pass
# okay decompiling .\pirates\pirate\PAvatarHandle.pyc
