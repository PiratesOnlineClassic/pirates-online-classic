from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from pirates.ship import ShipGlobals


class ShipLoaderOperationFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipLoaderOperationFSM')

    def __init__(self, air, avatar, callback=None):
        FSM.__init__(self, self.__class__.__name__)

        self.air = air
        self.avatar = avatar
        self.callback = callback

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterStart(self):
        pass

    def exitStart(self):
        pass

    def enterFinish(self):
        pass

    def exitFinish(self):
        pass

    def cleanup(self, *args, **kwargs):
        del self.air.shipLoader.avatar2fsm[self.avatar.doId]
        self.ignoreAll()
        self.demand('Off')

        if self.callback:
            self.callback(*args, **kwargs)


class CreateShipFSM(ShipLoaderOperationFSM):

    def enterStart(self, shipClass):
        self.modelClass = ShipGlobals.getModelClass(shipClass)
        if not self.modelClass:
            self.notify.warning('Failed to create ship for avatar %d, '
                'with invalid ship class: %r!' % (self.avatar.doId, shipClass))

            self.cleanup(0)
            return

        self.inventory = self.avatar.getInventory()
        if not self.inventory:
            self.notify.warning('Failed to create ship for avatar %d, '
                'avatar has no inventory!' % self.avatar.doId)

            self.cleanup(0)
            return

        self.air.shipLoader.sendCreateShip(self.avatar.doId, shipClass)

    def exitStart(self):
        pass

    def enterFinish(self, shipId):
        self.shipId = shipId
        if not self.shipId:
            self.notify.warning('Failed to create ship for avatar %d, '
                'ship database object creation failed!' % self.avatar.doId)

            self.cleanup(0)
            return

        shipDoIdList = self.inventory.getShipDoIdList()
        shipDoIdList.append(self.shipId)
        self.inventory.setShipDoIdList(shipDoIdList)

        self.cleanup(self.shipId)

    def exitFinish(self):
        pass


class ActivateShipFSM(ShipLoaderOperationFSM):

    def enterStart(self, shipId):
        self.shipId = shipId
        if not self.shipId:
            self.notify.warning('Failed to activate unknown ship for avatar %d!' % self.avatar.doId)
            self.cleanup(False)
            return

        self.inventory = self.avatar.getInventory()
        if not self.inventory:
            self.notify.warning('Failed to create ship for avatar %d, '
                'avatar has no inventory!' % self.avatar.doId)

            self.cleanup(False)
            return

        self.air.shipLoader.sendActivateShip(self.avatar.doId, self.shipId)

    def exitStart(self):
        pass

    def enterFinish(self):
        # we're done.
        self.cleanup(True)

    def exitFinish(self):
        pass


class DistributedShipLoaderAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipLoaderAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

        self.avatar2fsm = {}

    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)

        self.air.netMessenger.accept('createShipResponse', self, self.createShipResponse)
        self.air.netMessenger.accept('activateShipResponse', self, self.activateShipResponse)

    def runShipLoaderFSM(self, fsmtype, avatar, *args, **kwargs):
        fsm = self.avatar2fsm.get(avatar.doId)
        if fsm is not None:
            self.notify.warning('Failed to run ship loader fsm, '
                'an FSM: %s is already running for avatar %d!' % (fsm.__class__.__name__, avatar.doId))

            return

        callback = kwargs.pop('callback', None)

        self.avatar2fsm[avatar.doId] = fsmtype(self.air, avatar, callback)
        self.avatar2fsm[avatar.doId].request('Start', *args, **kwargs)

    def createShip(self, avatar, shipClass):

        def _shipCreatedCallback(shipId):
            if not shipId:
                return

            # we've just created this ship object, the avatar will have expected
            # that we automatically activate their ship. This is only done after creation of
            # a new ship object, the Uberdog will activate the avatar's ships object on login...
            self.sendActivateShip(avatar.doId, shipId)

        self.runShipLoaderFSM(CreateShipFSM, avatar, shipClass, callback=_shipCreatedCallback)

    def sendCreateShip(self, avatarId, shipClass):
        self.air.netMessenger.send('createShip', [avatarId, shipClass])

    def createShipResponse(self, avatarId, shipId):
        fsm = self.avatar2fsm.get(avatarId)
        if not fsm:
            return

        if not shipId:
            self.notify.warning('Failed to create ship for avatar %d!' % avatarId)
            fsm.cleanup(0)
            return

        if avatarId not in self.avatar2fsm:
            self.notify.warning('Failed to handle ship response for avatar %d, '
                'no ship creation FSM found!' % avatarId)

            fsm.cleanup(0)
            return

        fsm.demand('Finish', shipId)

    def activateShip(self, avatar, shipId):

        def _shipActivatedCallback(success):
            pass

        self.runShipLoaderFSM(ActivateShipFSM, avatar, shipId, callback=_shipActivatedCallback)

    def sendActivateShip(self, avatarId, shipId):
        self.air.netMessenger.send('activateShip', [avatarId, shipId])

    def activateShipResponse(self, avatarId, shipId, success):
        fsm = self.avatar2fsm.get(avatarId)
        if not fsm:
            self.notify.warning('Failed to activate ship %d for avatar %d, '
                'avatar has no running FSM!' % (shipId, avatarId))

            return

        if not success:
            self.notify.warning('Failed to activate ship %d for avatar %d, '
                'result was unsuccessful!' % (shipId, avatarId))

            fsm.cleanup(False)
            return

        fsm.demand('Finish')
