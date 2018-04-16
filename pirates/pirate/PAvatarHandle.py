from otp.avatar.AvatarHandle import AvatarHandle


class PAvatarHandle(AvatarHandle):

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
