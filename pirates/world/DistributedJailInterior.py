from panda3d.core import *
from pirates.piratesbase import PiratesGlobals
from pirates.world import DistributedGAInterior

class DistributedJailInterior(DistributedGAInterior.DistributedGAInterior):
    notify = directNotify.newCategory('DistributedJailInterior')

    @report(types=['frameCount', 'args'], dConfigParam='want-jail-report')
    def handleChildArrive(self, childObj, zoneId):
        DistributedGAInterior.DistributedGAInterior.handleChildArrive(self, childObj, zoneId)
        if childObj.isLocal() and childObj.getJailCellIndex() < 100:
            localAvatar.b_setGameState('ThrownInJail')

    @report(types=['frameCount', 'args'], dConfigParam='want-jail-report')
    def handleAvatarSetLocation(self, parentId, zoneId):
        if parentId != self.doId:
            logBlock(4, 'jailed avatar is leaving before ThrownInJail is complete.\nGoing to %s (%s,%s)' % (self.cr.doId2do.get(
                parentId), parentId, zoneId))
