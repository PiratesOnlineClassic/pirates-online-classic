from direct.showbase.PythonUtil import quickProfile, report
from pandac.PandaModules import *
from pirates.distributed import DistributedInteractive
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.ship import ShipGlobals
from pirates.shipparts import DistributedShippart, Wheel


class DistributedSteeringWheel(DistributedInteractive.DistributedInteractive, DistributedShippart.DistributedShippart):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedSteeringWheel')

    def __init__(self, cr):
        NodePath.__init__(self, 'steeringWheel')
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        DistributedShippart.DistributedShippart.__init__(self, cr)
        self.ship = None
        return

    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)
        DistributedShippart.DistributedShippart.generate(self)
        if not self.cr.tutorial:
            self.setInteractOptions(proximityText=PLocalizer.InteractWheel, sphereScale=6)

    def announceGenerate(self):
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        DistributedShippart.DistributedShippart.announceGenerate(self)
        if self.proximityCollisionNodePath:
            self.proximityCollisionNodePath.reparentTo(self.prop.propCollisions)
        locator = self.ship.locators.find('**/location_wheel;+s')
        if not locator.isEmpty():
            if self.ship.shipClass == ShipGlobals.DINGHY:
                self.prop.hide()
        self.setAllowInteract(1)
        self.checkInUse()

    def createProp(self):
        if self.ship.wheel:
            if self.ship.wheel[0]:
                self.prop = self.ship.wheel[0]
                self.ship.wheel[1] = self
                return
        self.prop = Wheel.Wheel()
        self.ship.wheel = [self.prop, self]

    def loadModel(self):
        self.prop.shipId = self.shipId
        self.prop.doId = self.doId
        self.prop.loadModel(self.ship.shipClass)

    def disable(self):
        self.notify.debug('Disable ' + str(self.doId))
        DistributedInteractive.DistributedInteractive.disable(self)
        DistributedShippart.DistributedShippart.disable(self)

    def delete(self):
        self.notify.debug('Delete ' + str(self.doId))
        if self.ship.wheel[1]:
            if self.ship.steeringAvId == base.localAvatar.doId:
                self.ship.clientSteeringEnd()
            self.ship.wheel[1] = None
        del self.ship
        del self.dna
        DistributedInteractive.DistributedInteractive.delete(self)
        DistributedShippart.DistributedShippart.delete(self)
        return

    def setupParent(self, parent):
        if not self.prop:
            return
        if not self.prop.propCollisions:
            return

    def requestInteraction(self, avId, interactType=0):
        av = base.cr.doId2do.get(avId)
        if self.isInteractionAllowed(av):
            base.localAvatar.motionFSM.off()
            self.ship.resetMiniLog('ShipPilot-%s' % (avId,))
            s = MiniLogSentry(self.ship.miniLog, 'SW.requestInteraction', avId, interactType)
            self.ship.miniLog.appendLine("localAvatar's parent: (%s)" % (localAvatar.getParentObj(),))
            DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)

    def isInteractionAllowed(self, av):
        return self.ship.canTakeWheel(self, av)

    def rejectInteraction(self):
        base.localAvatar.motionFSM.on()
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)

    def requestExit(self):
        DistributedInteractive.DistributedInteractive.requestExit(self)
        if base.localAvatar:
            if base.localAvatar.ship:
                base.localAvatar.ship.clientSteeringEnd()

    def enterWaiting(self):
        DistributedInteractive.DistributedInteractive.enterWaiting(self)
        self.accept('shipSinking-' + str(self.shipId), self.shipSinking)

    def exitWaiting(self):
        DistributedInteractive.DistributedInteractive.exitWaiting(self)
        self.ignore('shipSinking-' + str(self.shipId))

    def enterUse(self):
        s = MiniLogSentry(self.ship.miniLog, 'SW.enterUse')
        DistributedInteractive.DistributedInteractive.enterUse(self)
        self.accept('shipSinking-' + str(self.shipId), self.shipSinking)

    def exitUse(self):
        s = MiniLogSentry(self.ship.miniLog, 'SW.exitUse')
        DistributedInteractive.DistributedInteractive.exitUse(self)
        self.ignore('shipSinking-' + str(self.shipId))

    def shipSinking(self):
        self.notify.debug('[DistributedSteeringWheel] shipSinking %s' % self.ship.doId)
        self.requestExit()

    def loadTargetIndicator(self):
        if self.isGenerated():
            if self.ship.shipClass != ShipGlobals.DINGHY:
                self.disk = loader.loadModel('models/effects/selectionCursor')
                self.disk.setScale(self.diskRadius)
                self.disk.setColorScale(0, 1, 0, 1)
                self.disk.setP(-90)
                self.disk.setZ(0.025)
                self.disk.setBillboardAxis(6)
                self.disk.reparentTo(self.ship.highDetail)
                self.disk.setBin('shadow', 0)
                self.disk.setTransparency(TransparencyAttrib.MAlpha)
                self.disk.setDepthWrite(0)
                locator = self.ship.locators.find('**/location_wheel;+s')
                locator.isEmpty() or self.disk.setPos(locator.getPos(self.ship.root))

    def addPropToShip(self):
        self.locator = self.ship.locators.find('**/location_wheel;+s')
        self.prop.propCollisions.reparentTo(self.ship.modelCollisions)
        self.prop.addToShip()
        self.prop.geom_High.setPos(self.locator.getPos(self.ship.root))
        self.prop.geom_Medium.setPos(self.locator.getPos(self.ship.root))
        self.prop.geom_Low.setPos(self.locator.getPos(self.ship.root))
        self.prop.geom_High.setHpr(self.locator.getHpr(self.ship.root))
        self.prop.geom_Medium.setHpr(self.locator.getHpr(self.ship.root))
        self.prop.geom_Low.setHpr(self.locator.getHpr(self.ship.root))
        self.prop.geom_High.setScale(self.locator.getScale(self.ship.root))
        self.prop.geom_Medium.setScale(self.locator.getScale(self.ship.root))
        self.prop.geom_Low.setScale(self.locator.getScale(self.ship.root))
        self.prop.propCollisions.setPos(self.locator.getPos(self.ship.root))
        self.prop.propCollisions.setHpr(self.locator.getHpr(self.ship.root))
        self.prop.propCollisions.setScale(self.locator.getScale(self.ship.root))

    def setUserId(self, avId):
        DistributedInteractive.DistributedInteractive.setUserId(self, avId)
        self.ship.setWheelInUse(self.userId != 0)
        self.checkInUse()

    def checkInUse(self):
        if self.userId and base.localAvatar.getDoId() != self.ship.ownerId and localAvatar.getDoId() != self.userId:
            self.setAllowInteract(0)
        else:
            if self.userId and base.localAvatar.getDoId() == self.ship.ownerId:
                self.proximityText = PLocalizer.InteractWheelCaptain
                self.setAllowInteract(1)
            else:
                self.proximityText = PLocalizer.InteractWheel
                self.setAllowInteract(1)

    def setAllowInteract(self, allow, forceOff=False):
        DistributedInteractive.DistributedInteractive.setAllowInteract(self, allow)
        if not allow and forceOff:
            if self.ship.steeringAvId == base.localAvatar.doId:
                self.requestExit()
