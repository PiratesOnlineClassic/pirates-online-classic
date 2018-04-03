# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.world.DistributedJailInterior
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.world import DistributedGAInterior


class DistributedJailInterior(DistributedGAInterior.DistributedGAInterior):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedJailInterior')

    @report(types=['frameCount', 'args'], dConfigParam='want-jail-report')
    def handleChildArrive(self, childObj, zoneId):
        DistributedGAInterior.DistributedGAInterior.handleChildArrive(self, childObj, zoneId)
        if childObj.isLocal() and childObj.getJailCellIndex() < 100:
            localAvatar.b_setGameState('ThrownInJail')

    @report(types=['frameCount', 'args'], dConfigParam='want-jail-report')
    def handleAvatarSetLocation(self, parentId, zoneId):
        if parentId != self.doId:
            logBlock(4, 'jailed avatar is leaving before ThrownInJail is complete.\nGoing to %s (%s,%s)' % (self.cr.doId2do.get(parentId), parentId, zoneId))
# okay decompiling .\pirates\world\DistributedJailInterior.pyc
