from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import report
from otp.otpgui import OTPDialog
from panda3d.core import *
from pirates.piratesbase import PiratesGlobals, PLocalizer, TimeOfDayManager
from pirates.piratesgui import PDialog
from pirates.quest.QuestConstants import LocationIds
from pirates.world import DistributedDoorBase


class DistributedInteriorDoor(DistributedDoorBase.DistributedDoorBase):
    notify = directNotify.newCategory('DistributedInteriorDoor')

    def __init__(self, cr):
        DistributedDoorBase.DistributedDoorBase.__init__(self, cr, 'DistributedInteriorDoor')
        self.islandRequest = None
        self.doorDisableDialog = None

    def generate(self):
        DistributedDoorBase.DistributedDoorBase.generate(self)

    def delete(self):
        if self.islandRequest:
            base.cr.relatedObjectMgr.abortRequest(self.islandRequest)
            self.islandRequest = None

        DistributedDoorBase.DistributedDoorBase.delete(self)

    def disable(self):
        self.cleanupDoorDisableDialog()
        del self.interior
        DistributedDoorBase.DistributedDoorBase.disable(self)

    def setInteriorId(self, interiorDoId, interiorParentId, interiorZoneId):
        self.interiorDoId = interiorDoId
        self.interiorParentId = interiorParentId
        self.interiorZoneId = interiorZoneId
        self.interior = base.cr.doId2do[self.interiorDoId]

    def setExteriorId(self, exteriorDoId, exteriorWorldParentId, exteriorWorldZoneId):
        self.exteriorDoId = exteriorDoId
        self.exteriorWorldParentId = exteriorWorldParentId
        self.exteriorWorldZoneId = exteriorWorldZoneId

    def setBuildingDoorId(self, buildingDoorId):
        self.buildingDoorId = buildingDoorId

    def getParentModel(self):
        return self.interior

    def getOtherSideParentModel(self):
        island = base.cr.doId2do.get(self.exteriorDoId)
        building = island.find('**/=uid=%s' % self.buildingUid)
        return building

    def loadOtherSide(self):
        localAvatar.setInterest(self.exteriorWorldParentId, self.exteriorWorldZoneId, [
            'instanceInterest-Door'])

        def extFinishedCallback(ext):
            self.islandRequest = None
            self.loadExteriorFinished()

        self.islandRequest = base.cr.relatedObjectMgr.requestObjects([self.exteriorDoId],
            eachCallback=extFinishedCallback)

    def cleanupDoorDisableDialog(self, extraArgs=None):
        if self.doorDisableDialog:
            self.doorDisableDialog.destroy()
            self.doorDisableDialog = None

    def requestInteraction(self, avId, interactType=0):
        if not base.launcher.getPhaseComplete(3):
            if not self.doorDisableDialog:
                self.doorDisableDialog = PDialog.PDialog(text=PLocalizer.NoRambleshack, style=OTPDialog.Acknowledge,
                    command=self.cleanupDoorDisableDialog)

            return

        if self.buildingUid == LocationIds.PARLOR_BUILDING:
            if avId == base.localAvatar.doId:
                base.transitions.fadeOut(self.tOpen)
                self.openDoorIval.start()
                base.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 'mainWorld')
                return

        #buildingUid = None
        #exterior = base.cr.doId2do.get(self.exteriorDoId)
        #if exterior:
        #    buildingUid = exterior.getUniqueId()
        #base.richPresence.setLocation(buildingUid)
        DistributedDoorBase.DistributedDoorBase.requestInteraction(self, avId, interactType)

    def loadExteriorFinished(self):
        self.interior.handleExitGameArea(None)
        self.interior.disableFloors()
        world = self.interior.getParentObj()
        world.removeWorldInterest()
        localAvatar.clearInterestNamed(None, ['instanceInterest'])
        localAvatar.replaceInterestTag('instanceInterest-Door', 'instanceInterest')
        island = base.cr.doId2do.get(self.exteriorDoId)
        areaParentWorld = island.getParentObj()
        areaParentWorld.addWorldInterest(island)
        building = self.getOtherSideParentModel()
        doorLocator = building.find(self.doorLocatorStr)
        if doorLocator.isEmpty():
            doorLocator = building.find(self.doorLeftStr)
            if doorLocator.isEmpty():
                doorLocator = building.find(self.doorRightStr)

        localAvatar.reparentTo(doorLocator)
        localAvatar.setPos(0, 10, 0)
        localAvatar.setHpr(0, 0, 0)
        localAvatar.wrtReparentTo(island)
        localAvatar.setScale(1)
        self.setupOtherSideDoors()
        messenger.send('doorToExteriorFadeIn')
        self.fadeIn()
        locationUid = island.getUniqueId()
        localAvatar.guiMgr.radarGui.showLocation(locationUid)

    def handleEnterProximity(self, collEntry):
        DistributedDoorBase.DistributedDoorBase.handleEnterProximity(self, collEntry)
