# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.world.DistributedGADoor
import DistributedGAConnector


class DistributedGADoor(DistributedGAConnector.DistributedGAConnector):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedGADoor')

    def __init__(self, cr):
        DistributedGAConnector.DistributedGAConnector.__init__(self, cr)
        self.connectorNodes = [
         'portal_A', 'portal_B']

    def generate(self):
        DistributedGAConnector.DistributedGAConnector.generate(self)
        self.loadArea(0)
        self.loadArea(1)
        self.setupPortal()

    def loadArea(self, areaIndex, entry=None):
        parentId, zoneId = self.areaParentZone[areaIndex]
        visContext = self.cr.addInterest(parentId, zoneId, 'gaConnector', areaEvent)

    def setupConnectorNodes(self):
        pass

    def setupPortal(self):
        area0 = self.areaId[0]
        area1 = self.areaId[1]
        areaNode0 = self.areaNode[0]
        areaNode1 = self.areaNode[1]
        portalNode0 = area0.find('**/' + areaNode0).node()
        portalNode1 = area1.find('**/' + areaNode1).node()
        portalNode0.setCellIn(area0)
        portalNode0.setCellOut(area1)
        portalNode1.setCellIn(area1)
        portalNode1.setCellOut(area0)
        base.cam.node().setCullCenter(base.camera)
        base.graphicsEngine.setPortalCull(1)
# okay decompiling .\pirates\world\DistributedGADoor.pyc
