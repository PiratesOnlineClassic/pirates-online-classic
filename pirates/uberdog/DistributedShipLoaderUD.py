from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.distributed.MsgTypes import *
from direct.distributed.PyDatagram import PyDatagram

from pirates.ship import ShipGlobals
from pirates.shipparts.HullDNA import HullDNA
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryCategory


class ShipLoaderOperationFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipLoaderOperationFSM')

    def __init__(self, air, avatarId, callback=None):
        FSM.__init__(self, self.__class__.__name__)

        self.air = air
        self.avatarId = avatarId
        self.callback = callback

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterStart(self):
        pass

    def exitStart(self):
        pass

    def cleanup(self, *args, **kwargs):
        del self.air.shipLoader.avatar2fsm[self.avatarId]
        self.ignoreAll()
        self.demand('Off')

        if self.callback:
            self.callback(*args, **kwargs)


class CreateShipFSM(ShipLoaderOperationFSM):

    def enterStart(self, shipClass):
        self.modelClass = ShipGlobals.getModelClass(shipClass)
        if not self.modelClass:
            self.notify.warning('Failed to create ship for avatar %d, '
                'with invalid ship class: %r!' % (self.avatarId, shipClass))

            self.cleanup(0)
            return

        self.shipConfig = ShipGlobals.getShipConfig(self.modelClass)
        self.hullConfig = ShipGlobals.getHullConfig(self.modelClass)

        fields = {
            'setBaseTeam': (0,),
            'setShipClass': (self.shipConfig['setShipClass'][0],),
            'setName': ('Unnamed Ship',),
            'setInventoryId': (0,),
            'setIsFlagship': (0,),
            'setMaxHp': (self.shipConfig['setMaxHp'][0],),
            'setHp': (self.shipConfig['setHp'][0],),
            'setMaxSp': (self.hullConfig['setMaxSp'][0],),
            'setSp': (self.hullConfig['setSp'][0],),
            'setHullCondition': (1 << 7,),
            'setMaxCargo': (self.hullConfig['setMaxCargo'][0],),
            'setCargo': ([],),
            'setMaxCrew': (self.shipConfig['setMaxCrew'][0],),
            'setWishName': ('',),
            'setWishNameState': ('',),
        }

        self.air.dbInterface.createObject(self.air.dbId,
            self.air.dclassesByName['PlayerShipUD'],
            fields=fields,
            callback=self.shipCreatedCallback)

    def shipCreatedCallback(self, shipId):
        self.shipId = shipId
        if not self.shipId:
            self.notify.warning('Failed to create ship for avatar %d, '
                'ship database object creation failed!' % self.avatarId)

            self.cleanup(0)
            return

        self.air.inventoryManager.createShipInventory(self.shipId, self.shipInventoryCreatedCallback)

    def shipInventoryCreatedCallback(self, inventoryId):
        self.inventoryId = inventoryId
        if not self.inventoryId:
            self.notify.warning('Failed to create ship %d for avatar %d, '
                'ship inventory database object creation failed!' % (self.shipId, self.avatarId))

            self.cleanup(0)
            return

        fields = {
            # DistributedShippart
            'setOwnerId': (self.avatarId,),
            'setShipId': (self.shipId,),
            'setGeomParentId': (0,),

            # DistributedDestructibleArray:
            'setMaxArrayHp': (self.hullConfig['setMaxArrayHp'][0],),
            'setArrayHp': (self.hullConfig['setArrayHp'][0],),
        }

        hullDNA = HullDNA()
        hullDNA.setShipClass(self.modelClass)
        hullDNA.setBaseTeam(PiratesGlobals.PLAYER_TEAM)
        for key, value in self.hullConfig.items():
            if not hasattr(hullDNA, key):
                continue

            if key == 'setShipClass':
                continue

            getattr(hullDNA, key)(value)

        dclass = self.air.dclassesByName['DistributedHullDNA']
        for fieldIndex in xrange(dclass.getNumFields()):
            field = dclass.getInheritedField(fieldIndex)
            if not field.asAtomicField():
                continue

            fieldValue = getattr(hullDNA, field.getName().replace('set', 'get'))()
            if isinstance(fieldValue, list):
                fields[field.getName()] = fieldValue
            else:
                fields[field.getName()] = (fieldValue,)

        self.air.dbInterface.createObject(self.air.dbId,
            self.air.dclassesByName['DistributedHullUD'],
            fields=fields,
            callback=self.shipHullCreatedCallback)

    def shipHullCreatedCallback(self, shipHullDoId):
        self.shipHullDoId = shipHullDoId
        if not self.shipHullDoId:
            self.notify.warning('Failed to create ship %d for avatar %d, '
                'ship hull database object creation failed!' % (self.shipId, self.avatarId))

            self.cleanup(0)
            return

        self.mastConfig = ShipGlobals.getMastConfig(self.modelClass, 0)

        #fields = {
        #    # DistributedShippart:
        #    'setOwnerId': (self.avatarId,),
        #    'setShipId': (self.shipId,),
        #    'setGeomParentId': (0,),
        #
        #    # DistributedDestructibleArray:
        #    'setMaxArrayHp': (self.mastConfig['setMaxArrayHp'][0],),
        #    'setArrayHp': (self.mastConfig['setArrayHp'][0],),
        #
        #    # DistributedMastDNA:
        #    'setShipClass': (self.modelClass,),
        #    'setBaseTeam': (0,),
        #
        #    'setSailConfig': (self.mastConfig['setSailConfig'],),
        #    'setTextureIndex': (self.mastConfig['setTextureIndex'],),
        #    'setPosIndex': (self.mastConfig['setPosIndex'],)
        #}
        #
        #self.air.dbInterface.createObject(self.air.dbId,
        #    self.air.dclassesByName['DistributedMastUD'],
        #    fields=fields,
        #    callback=self.shipMastCreatedCallback)

    #def shipMastCreatedCallback(self, shipMastDoId):
    #    self.shipMastDoId = shipMastDoId
    #    if not self.shipMastDoId:
    #        self.notify.warning('Failed to create ship %d for avatar %d, '
    #            'ship mast database object creation failed!' % (self.shipId, self.avatarId))
    #
    #        self.cleanup(0)
    #        return

        self.air.dbInterface.queryObject(self.air.dbId,
            self.inventoryId,
            self.shipInventoryQueryCallback,
            dclass=self.air.dclassesByName['DistributedInventoryUD'])

    def shipInventoryQueryCallback(self, dclass, fields):
        if not dclass and not fields:
            self.notify.warning('Failed to query inventory %d for ship %d!' % (
                self.inventory, self.shipId))

            self.cleanup(0)
            return

        # manually update the ship's inventory's doId list containing the shippart doId's...
        doIds, = fields['setDoIds']
        doIds.append([InventoryCategory.SHIP_MAINPARTS, self.shipHullDoId])
        #doIds.append([InventoryCategory.SHIP_MAINPARTS, self.shipMastDoId])

        fields = {
            'setDoIds': (doIds,),
        }

        self.air.dbInterface.updateObject(self.air.dbId,
            self.inventoryId,
            self.air.dclassesByName['DistributedInventoryUD'],
            fields,
            callback=self.shipInventorySetCallback)

    def shipInventorySetCallback(self, fields):
        if fields is not None:
            self.notify.warning('Failed to update inventory %d for ship %d, '
                'invalid database response!' % (self.inventoryId, self.shipId))

            self.cleanup(0)
            return

        self.cleanup(self.shipId)

    def exitStart(self):
        pass


class ActivateShipFSM(ShipLoaderOperationFSM):

    def enterStart(self, shipId):
        self.shipId = shipId
        if not self.shipId:
            self.notify.warning('Failed to load invalid ship for avatar %d, '
                'invalid shipId specified!' % self.avatarId)

            self.cleanup(False)
            return

        self.air.dbInterface.queryObject(self.air.dbId,
            self.avatarId,
            self.avatarQueryCallback,
            dclass=self.air.dclassesByName['DistributedPlayerPirateUD'])

    def avatarQueryCallback(self, dclass, fields):
        if not dclass and not fields:
            self.notify.warning('Failed to activate ship %d for avatar %d, '
                'could not query avatar database object!' % (self.shipId, self.avatarId))

            self.cleanup(False)
            return

        self.accountId, = fields['setDISLid']
        if not self.accountId:
            self.notify.warning('Failed to activate ship %d for avatar %d, '
                'could not retrieve the avatar\'s account id!' % (self.shipId, self.avatarId))

            self.cleanup(False)
            return

        self.air.dbInterface.queryObject(self.air.dbId,
            self.shipId,
            self.shipQueryCallback,
            dclass=self.air.dclassesByName['PlayerShipUD'])

    def shipQueryCallback(self, dclass, fields):
        if not dclass and not fields:
            self.notify.warning('Failed to query ship %d for avatar %d!' % (
                self.shipId, self.avatarId))

            self.cleanup(False)
            return

        self.inventoryId, = fields['setInventoryId']
        self.air.inventoryManager.activateShipInventory(self.avatarId, self.shipId, self.inventoryId,
            self.shipInventoryActivatedCallback)

    def shipInventoryActivatedCallback(self, inventoryId):
        self.air.sendActivate(self.shipId, 0, 0,
            self.air.dclassesByName['PlayerShipUD'],
            {'setInventoryId': (inventoryId,)})

        channel = self.accountId << 32 | self.avatarId
        self.air.setOwner(self.shipId, channel)

        datagramCleanup = PyDatagram()
        datagramCleanup.addServerHeader(
            self.shipId,
            channel,
            STATESERVER_OBJECT_DELETE_RAM)
        datagramCleanup.addUint32(self.shipId)

        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.air.ourChannel,
            CLIENTAGENT_ADD_POST_REMOVE)
        datagram.addString(datagramCleanup.getMessage())
        self.air.send(datagram)

        self.air.dbInterface.queryObject(self.air.dbId,
            self.inventoryId,
            self.shipInventoryQueryCallback,
            dclass=self.air.dclassesByName['DistributedInventoryUD'])

    def shipInventoryQueryCallback(self, dclass, fields):
        if not dclass and not fields:
            self.notify.warning('Failed to activate ship %d for avatar %d!' % (
                self.shipId, self.avatarId))

            self.cleanup(False)
            return

        self.pendingShipparts = []
        doIdsInCategory, = fields['setDoIds']
        for category, doId in doIdsInCategory:
            if category == InventoryCategory.SHIP_MAINPARTS:
                self.pendingShipparts.append(doId)
                self.air.dbInterface.queryObject(self.air.dbId,
                    doId,
                    lambda dclass, fields: self.shippartQueryCallback(doId, dclass, fields))

    def shippartQueryCallback(self, shippartDoId, dclass, fields):
        if not dclass and fields:
            self.notify.warning('Failed to activate ship %d for avatar %d, '
                'failed to query shippart %d!' % (self.shipId, self.avatarId, shippartDoId))

            self.cleanup(False)
            return

        self.air.sendActivate(shippartDoId, 0, 0,
            dclass,
            {'setOwnerId': (self.avatarId,), 'setShipId': (self.shipId,)})

        channel = self.accountId << 32 | self.avatarId
        self.air.setOwner(shippartDoId, channel)

        datagramCleanup = PyDatagram()
        datagramCleanup.addServerHeader(
            shippartDoId,
            channel,
            STATESERVER_OBJECT_DELETE_RAM)
        datagramCleanup.addUint32(shippartDoId)

        datagram = PyDatagram()
        datagram.addServerHeader(
            channel,
            self.air.ourChannel,
            CLIENTAGENT_ADD_POST_REMOVE)
        datagram.addString(datagramCleanup.getMessage())
        self.air.send(datagram)

        self.pendingShipparts.remove(shippartDoId)
        if not self.pendingShipparts:
            self.cleanup(True)

    def exitStart(self):
        pass


class DistributedShipLoaderUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipLoaderUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

        self.avatar2fsm = {}

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)

        self.air.netMessenger.accept('createShip', self, self.createShip)
        self.air.netMessenger.accept('activateShip', self, self.activateShip)

    def runShipLoaderFSM(self, fsmtype, avatarId, *args, **kwargs):
        if avatarId in self.avatar2fsm:
            self.notify.warning('Failed to run ship loader fsm, '
                'an FSM is already running for avatar %d!' % avatarId)

            return

        callback = kwargs.pop('callback', None)

        self.avatar2fsm[avatarId] = fsmtype(self.air, avatarId, callback)
        self.avatar2fsm[avatarId].request('Start', *args, **kwargs)

    def createShip(self, avatarId, shipClass):

        def shipCreatedCallback(shipId):
            self.air.netMessenger.send('createShipResponse', [avatarId, shipId])

        self.runShipLoaderFSM(CreateShipFSM, avatarId, shipClass, callback=shipCreatedCallback)

    def activateShip(self, avatarId, shipId):

        def shipActivatedCallback(success):
            self.air.netMessenger.send('activateShipResponse', [avatarId, shipId, success])

        self.runShipLoaderFSM(ActivateShipFSM, avatarId, shipId, callback=shipActivatedCallback)
