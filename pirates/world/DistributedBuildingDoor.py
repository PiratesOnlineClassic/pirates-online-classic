from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import report
from panda3d.core import *
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.world import DistributedDoorBase


class DistributedBuildingDoor(DistributedDoorBase.DistributedDoorBase):
    notify = directNotify.newCategory('DistributedBuildingDoor')

    def __init__(self, cr):
        DistributedDoorBase.DistributedDoorBase.__init__(self, cr, 'DistributedBuildingDoor')
        self.areaRequest = None
        self.privateInteriorId = 0

    def disable(self):
        self.notify.debug('%s DistributedBuildingDoor.disable' % self.doId)
        if self.areaRequest:
            base.cr.relatedObjectMgr.abortRequest(self.areaRequest)
            self.areaRequest = None

        self.privateInteriorId = 0
        DistributedDoorBase.DistributedDoorBase.disable(self)

    def delete(self):
        self.notify.debug('%s DistributedBuildingDoor.delete' % self.doId)
        DistributedDoorBase.DistributedDoorBase.delete(self)

    def setInteriorId(self, interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId):
        self.interiorDoId = interiorDoId
        self.interiorUid = interiorUid
        self.interiorWorldParentId = interiorWorldParentId
        self.interiorWorldZoneId = interiorWorldZoneId

    def getBuilding(self):
        island = self.getParentObj()
        building = island.find('**/=uid=%s' % self.buildingUid)
        return building

    def getBuildingName(self):
        return PLocalizer.LocationNames.get(self.interiorUid)

    def getPrompt(self):
        buildingName = self.getBuildingName()
        if buildingName:
            return PLocalizer.InteractEnterNamedBuilding % buildingName

        return PLocalizer.InteractOpenDoor

    def getParentModel(self):
        return self.getBuilding()

    def getOtherSideParentModel(self):
        if not self.privateInteriorId:
            return base.cr.doId2do[self.interiorDoId]
        else:
            return base.cr.doId2do[self.privateInteriorId]

    def loadOtherSide(self):
        self.requestPrivateInteriorInstance()

    def requestPrivateInteriorInstance(self):
        self.sendUpdate('requestPrivateInteriorInstance')

    def setPrivateInteriorInstance(self, worldId, worldZoneId, interiorId, autoFadeIn=True):
        if worldId == 0 and worldZoneId == 0:
            worldId = self.interiorWorldParentId
            worldZoneId = self.interiorWorldZoneId
            interiorId = self.interiorDoId
            self.privateInteriorId = 0
        else:
            self.privateInteriorId = interiorId

        self.loadInstanceWorld(worldId, worldZoneId, interiorId, autoFadeIn)

    def loadInstanceWorld(self, worldId, worldZoneId, interiorId, autoFadeIn):

        def areaFinishedCallback(interior):
            self.areaRequest = None
            self.loadInteriorAreaFinished(interior, autoFadeIn)
            return

        self.areaRequest = base.cr.relatedObjectMgr.requestObjects([interiorId],
            eachCallback=areaFinishedCallback)

        base.cr.addTaggedInterest(worldId, worldZoneId, ['instanceInterest-Door'])

    def loadInteriorAreaFinished(self, interior, autoFadeIn):
        oldParent = self.getParentObj()
        oldWorld = oldParent.getParentObj()
        oldWorld.removeWorldInterest(oldParent)
        base.cr.clearTaggedInterestNamed(None, ['instanceInterest'])
        base.cr.replaceTaggedInterestTag('instanceInterest-Door', 'instanceInterest')
        world = interior.getParentObj()
        world.addWorldInterest(interior)
        self.setupOtherSideDoors()
        interior.reparentTo(render)
        interior.setAutoFadeInOnEnter(autoFadeIn)
        interior.enterInteriorFromDoor(self.doorIndex)

    def requestInteraction(self, avId, interactType=0):
        if avId == localAvatar.doId and localAvatar.zombie and self.buildingUid != '1189479168.0sdnaik':
            localAvatar.guiMgr.createWarning(PLocalizer.ZombieNoDoors, PiratesGuiGlobals.TextFG6)
            return

        base.richPresence.setLocation(self.interiorUid, interior=True)
        DistributedDoorBase.DistributedDoorBase.requestInteraction(self, avId, interactType)
