# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.distributed.DistributedDistrict
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObject import DistributedObject

class DistributedDistrict(DistributedObject):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedDistrict')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.name = 'NotGiven'
        self.available = 0
        self.avatarCount = 0
        self.newAvatarCount = 0

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.cr.activeDistrictMap[self.doId] = self
        messenger.send('shardInfoUpdated')

    def delete(self):
        if base.cr.distributedDistrict is self:
            base.cr.distributedDistrict = None
        if self.cr.activeDistrictMap.has_key(self.doId):
            del self.cr.activeDistrictMap[self.doId]
        DistributedObject.delete(self)
        messenger.send('shardInfoUpdated')
        return

    def setAvailable(self, available):
        self.available = available
        messenger.send('shardInfoUpdated')

    def setName(self, name):
        self.name = name
        messenger.send('shardInfoUpdated')
# okay decompiling .\otp\distributed\DistributedDistrict.pyc
