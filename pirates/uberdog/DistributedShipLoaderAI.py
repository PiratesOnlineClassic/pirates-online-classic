from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from pirates.ship import ShipGlobals
from pirates.uberdog import UberDogGlobals


class ShipFSM(FSM):

    def __init__(self, manager, avatar, callback=None):
        FSM.__init__(self, 'ShipFSM')

        self.manager = manager
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

    def enterStop(self):
        del self.manager.avatar2fsm[self.avatar.doId]
        self.demand('Off')

    def exitStop(self):
        pass

class CreateShipFSM(ShipFSM):

    def enterStart(self, shipType):

        def shipCreatedCallback(shipId):
            inventory = self.avatar.getInventory()

            if not inventory:
                self.notify.warning('Failed to create ship %d, avatar %d has no inventory!' % (
                    shipId, self.avatar.doId))

                return

            categoriesAndDoIds = inventory.getDoIds()
            categoriesAndDoIds.append([UberDogGlobals.InventoryCategory.SHIPS, shipId])
            inventory.b_setDoIds(categoriesAndDoIds)

            def shipGeneratedCallback(ship):
                self.manager.air.setOwner(ship.doId, self.avatar.doId)

            self.manager.air.acceptOnce('generate-%d' % shipId,
                shipGeneratedCallback)

            # TODO FIXME: the ship needs to be loaded up on the Uberdog
            # each time the client logs on...
            self.manager.air.sendActivate(shipId,
                self.avatar.parentId,
                self.avatar.zoneId,
                dclass=self.manager.air.dclassesByName['PlayerShipAI'])

            self.request('Stop')

        shipConfig = ShipGlobals.getShipConfig(shipType)

        fields = {
            'setBaseTeam': (0,),
            'setShipClass': (shipConfig['setShipClass'][0],),
            'setName': ('Unnamed Ship',),
            'setInventoryId': (0,),
            'setIsFlagship': (0,),
            'setMaxHp': (shipConfig['setMaxHp'][0],),
            'setHp': (shipConfig['setHp'][0],),
            'setMaxSp': (0,),
            'setSp': (0,),
            'setHullCondition': (0,),
            'setMaxCargo': (0,),
            'setCargo': ([],),
            'setMaxCrew': (shipConfig['setMaxCrew'][0],),
            'setWishName': ('',),
            'setWishNameState': ('',),
        }

        self.manager.air.dbInterface.createObject(self.manager.air.dbId,
            self.manager.air.dclassesByName['PlayerShipAI'],
            fields=fields,
            callback=shipCreatedCallback)

    def exitStart(self):
        pass

class DistributedShipLoaderAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipLoaderAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.avatar2fsm = {}

    def runShipFSM(self, fsmType, avatar, *args):
        if avatar.doId in self.avatar2fsm:
            self.notify.warning('Cannot start shipFSM, an FSM is already running for avatar %d!' % (
                avatar.doId))

            return

        self.avatar2fsm[avatar.doId] = fsmType(self, avatar)
        self.avatar2fsm[avatar.doId].request('Start', *args)

    def requestCreateShip(self, avatar, shipType):
        self.runShipFSM(CreateShipFSM, avatar, shipType)
