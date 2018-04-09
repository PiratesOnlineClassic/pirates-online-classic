# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.shipparts.DistributedShipRepairSpot
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.fsm.StatePush import FunctionCall, StateVar
from pandac.PandaModules import NodePath
from pirates.distributed.DistributedInteractive import DistributedInteractive
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.pvp import PVPGlobals


class DistributedShipRepairSpot(DistributedInteractive):
    
    notify = directNotify.newCategory('DistributedShipRepairSpot')

    def __init__(self, cr):
        DistributedInteractive.__init__(self, cr)

    def setShipId(self, shipId):
        self._shipId = shipId

    def setIndex(self, index):
        self._index = index

    def announceGenerate(self):
        DistributedInteractive.announceGenerate(self)
        ship = self.cr.doId2do[self._shipId]
        NodePath.__init__(self, 'ship-%s-repairSpot-%s' % (ship.doId, self._index))
        locName = PVPGlobals.RepairSpotLocatorNames[self._index]
        locator = ship.locators.find('**/%s;+s' % locName)
        self.setPos(locator.getPos(ship.root))
        self.setHpr(locator.getHpr(ship.root))
        self.setScale(locator.getScale(ship.root))
        self.reparentTo(ship.modelGeom)
        self.setInteractOptions(proximityText=PLocalizer.InteractRepairSpot, diskRadius=10.0, sphereScale=6.0)
        self.setAllowInteract(1)
        self.checkInUse()
        self._statePushes = DestructiveScratchPad(evalUsable=FunctionCall(self._evalUsableState, ship._repairSpotMgr._state.fullHealth, ship.getWheelInUseSV()))

    def disable(self):
        self._statePushes.destroy()
        self._statePushes = None
        if self.userId == localAvatar.doId:
            self.stopRepairing()
        DistributedInteractive.disable(self)
        self.detachNode()
        return

    def _evalUsableState(self, fullShipHealth, steeringWheelInUse):
        if not (fullShipHealth or steeringWheelInUse):
            self.setInteractOptions(proximityText=PLocalizer.InteractRepairSpot)
        else:
            if fullShipHealth:
                proximityText = PLocalizer.CannotRepairRepairedShipWarning
            else:
                proximityText = PLocalizer.CannotRepairWhileWheelOccupiedWarning
            self.setInteractOptions(proximityText=proximityText)

    def requestInteraction(self, avId, interactType=0):
        DistributedInteractive.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        if self.userId != localAvatar.doId:
            localAvatar.motionFSM.on()
        DistributedInteractive.rejectInteraction(self)

    def startRepairing(self):
        localAvatar.b_setGameState('ShipRepair')

    def stopRepairing(self):
        if self.userId == localAvatar.doId and localAvatar.getGameState() == 'ShipRepair':
            localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
            base.localAvatar.motionFSM.on()

    def requestExit(self):
        DistributedInteractive.requestExit(self)
        self.stopRepairing()

    def enterWaiting(self):
        DistributedInteractive.enterWaiting(self)
        localAvatar.motionFSM.off()
        self.accept('shipSinking-' + str(self._shipId), self.shipSinking)

    def exitWaiting(self):
        DistributedInteractive.exitWaiting(self)
        self.ignore('shipSinking-' + str(self._shipId))

    def enterUse(self):
        DistributedInteractive.enterUse(self)
        self.accept('shipSinking-' + str(self._shipId), self.shipSinking)
        self.startRepairing()

    def exitUse(self):
        self.stopRepairing()
        DistributedInteractive.exitUse(self)
        self.ignore('shipSinking-' + str(self._shipId))

    def shipSinking(self):
        self.notify.debug('shipSinking %s' % self._shipId)
        self.requestExit()

    def setUserId(self, avId):
        DistributedInteractive.setUserId(self, avId)
        self.checkInUse()

    def checkInUse(self):
        if self.userId and localAvatar.getDoId() != self.userId:
            self.setAllowInteract(0)
        else:
            self.setAllowInteract(1)
# okay decompiling .\pirates\shipparts\DistributedShipRepairSpot.pyc
