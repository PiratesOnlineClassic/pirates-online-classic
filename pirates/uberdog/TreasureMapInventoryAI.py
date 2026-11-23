from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import DirectObject
from direct.task import Task

from otp.distributed.OtpDoGlobals import OTP_ZONE_ID_MANAGEMENT
from pirates.uberdog import InventoryInit
from pirates.uberdog.UberDogGlobals import InventoryCategory


class TreasureMapInventoryAI(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('TreasureMapInventoryAI')
    timeout = 30

    def __init__(self, inventory):
        self.inventory = inventory
        self.air = inventory.air
        self.activations = {}
        self.award = None
        self.closed = False

    def _live(self):
        return (not self.closed and
                self.air.doId2do.get(self.inventory.doId) is self.inventory and
                self.air.doId2do.get(self.inventory.ownerId) is not None)

    def activateAll(self):
        for doId in list(self.inventory.getDoIdListCategory(InventoryCategory.TREASURE_MAPS)):
            self.activate(doId, lambda result: None)

    def activate(self, doId, callback):
        obj = self.air.doId2do.get(doId)
        if obj:
            callback(obj if (callable(getattr(obj, 'getMapId', None)) and
                             callable(getattr(obj, 'getOwnerId', None)) and
                             obj.getOwnerId() == self.inventory.ownerId) else None)
            return
        if not self._live():
            callback(None)
            return
        if doId in self.activations:
            self.activations[doId].append(callback)
            return
        self.activations[doId] = [callback]
        name = self._activationTask(doId)
        self.acceptOnce('generate-%d' % doId, self._activated, [doId])
        taskMgr.doMethodLater(self.timeout, self._activationTimedOut, name,
                              extraArgs=[doId])
        try:
            self.air.sendActivate(doId, self.inventory.doId, OTP_ZONE_ID_MANAGEMENT,
                                  self.air.dclassesByName['DistributedTreasureMapAI'],
                                  {'setIsEnabled': (1,)})
        except Exception as error:
            self.notify.warning('Cannot activate treasure map %d: %s' % (doId, error))
            self._finishActivation(doId, None)

    def _activationTask(self, doId):
        return 'treasure-map-activation-%s-%s' % (id(self), doId)

    def _activationTimedOut(self, doId):
        self._finishActivation(doId, None)
        return Task.done

    def _activated(self, doId, obj):
        if (not self._live() or not callable(getattr(obj, 'getMapId', None)) or
                not callable(getattr(obj, 'getOwnerId', None)) or
                obj.getOwnerId() != self.inventory.ownerId):
            self._finishActivation(doId, None)
            return
        self._finishActivation(doId, obj)

    def _finishActivation(self, doId, obj):
        callbacks = self.activations.pop(doId, [])
        self.ignore('generate-%d' % doId)
        taskMgr.remove(self._activationTask(doId))
        for callback in callbacks:
            callback(obj)

    def give(self, mapId, callback):
        if self.award or not self._live():
            callback(False)
            return
        self.award = {'mapId': mapId, 'callback': callback}
        award = self.award
        taskMgr.doMethodLater(self.timeout, self._awardTimedOut,
                              'treasure-map-award-%s' % id(self))
        try:
            self.air.dbInterface.queryObject(
                self.air.dbId, self.inventory.doId,
                lambda dclass, fields: self._inventoryQueried(award, dclass, fields),
                dclass=self.air.dclassesByName['PirateInventoryAI'])
        except Exception as error:
            self.notify.warning('Cannot query inventory for treasure map: %s' % error)
            self._finishAward(False)

    def _awardTimedOut(self, task):
        self._finishAward(False)
        return Task.done

    def _finishAward(self, success):
        award, self.award = self.award, None
        taskMgr.remove('treasure-map-award-%s' % id(self))
        if award:
            award['callback'](success)

    def _inventoryQueried(self, award, dclass, fields):
        if self.award is not award:
            return
        if not self._live() or not dclass or not fields or 'setDoIds' not in fields:
            self._finishAward(False)
            return
        try:
            persisted = list(fields['setDoIds'][0])
            current = self.inventory.getDoIds()
            nonMaps = lambda slots: {(category, doId) for category, doId in slots
                                     if category != InventoryCategory.TREASURE_MAPS}
            if nonMaps(persisted) != nonMaps(current):
                self._finishAward(False)
                return
            persistedMaps = [doId for category, doId in persisted
                             if category == InventoryCategory.TREASURE_MAPS]
            localMaps = self.inventory.getDoIdListCategory(InventoryCategory.TREASURE_MAPS)
            if set(localMaps) - set(persistedMaps):
                self._finishAward(False)
                return
            if set(persistedMaps) != set(localMaps):
                self.inventory.b_setDoIdListCategory(InventoryCategory.TREASURE_MAPS,
                                                      persistedMaps)
            self.award['pending'] = list(persistedMaps)
            self._checkExisting()
        except (TypeError, ValueError, KeyError) as error:
            self.notify.warning('Invalid inventory database response: %s' % error)
            self._finishAward(False)

    def _checkExisting(self):
        if not self.award:
            return
        if not self.award['pending']:
            self._create()
            return
        award = self.award
        self.activate(award['pending'].pop(0),
                      lambda obj: self._existingActivated(award, obj))

    def _existingActivated(self, award, obj):
        if self.award is not award:
            return
        if not obj:
            self._finishAward(False)
        elif obj.getMapId() == self.award['mapId']:
            self._finishAward(True)
        else:
            self._checkExisting()

    def _create(self):
        award = self.award
        fields = {
            'setMapId': (self.award['mapId'],),
            'setOwnerId': (self.inventory.ownerId,),
            'setInventoryVersion': (InventoryInit.UberDogRevision,),
            'setCategoryLimits': ([],),
            'setDoIds': ([],),
            'setAccumulators': ([],),
            'setStackLimits': ([],),
            'setStacks': ([],),
        }
        try:
            self.air.dbInterface.createObject(
                self.air.dbId, self.air.dclassesByName['DistributedTreasureMapAI'],
                fields, lambda doId: self._created(award, doId))
        except Exception as error:
            self.notify.warning('Cannot create treasure map: %s' % error)
            self._finishAward(False)

    def _created(self, award, doId):
        if self.award is not award:
            return
        if not doId or not self._live():
            self._finishAward(False)
            return
        self.award['doId'] = doId
        old = self.inventory.getDoIds()
        new = old + [[InventoryCategory.TREASURE_MAPS, doId]]
        try:
            self.air.dbInterface.updateObject(
                self.air.dbId, self.inventory.doId,
                self.air.dclassesByName['PirateInventoryAI'],
                {'setDoIds': (new,)}, oldFields={'setDoIds': (old,)},
                callback=lambda response: self._linked(award, response))
        except Exception as error:
            self.notify.warning('Cannot link treasure map %d: %s' % (doId, error))
            self._finishAward(False)

    def _linked(self, award, response):
        if self.award is not award:
            return
        if response is not None or not self._live():
            self._finishAward(False)
            return
        doId = self.award['doId']
        maps = list(self.inventory.getDoIdListCategory(InventoryCategory.TREASURE_MAPS))
        if doId not in maps:
            maps.append(doId)
            self.inventory.b_setDoIdListCategory(InventoryCategory.TREASURE_MAPS, maps)
        self.activate(doId, lambda obj: self._mapAwardActivated(award, obj))

    def _mapAwardActivated(self, award, obj):
        if self.award is award:
            self._finishAward(bool(obj))

    def close(self):
        self.closed = True
        self._finishAward(False)
        for doId in list(self.activations):
            self._finishActivation(doId, None)
        for doId in list(self.inventory.getDoIdListCategory(InventoryCategory.TREASURE_MAPS)):
            obj = self.air.doId2do.get(doId)
            if obj:
                obj.requestDelete()
