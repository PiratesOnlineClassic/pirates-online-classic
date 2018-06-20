from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal
from otp.ai.MagicWordGlobal import *
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory


class DistributedInventoryManagerAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryManagerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

        self.inventories = {}
        self.pendingInventories = {}

    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)

        self.air.netMessenger.accept('hasInventory', self, self.sendHasInventory)
        self.air.netMessenger.accept('addInventory', self, self.addInventory)
        self.air.netMessenger.accept('removeInventory', self, self.removeInventory)
        self.air.netMessenger.accept('getInventory', self, self.sendGetInventory)

    def hasInventory(self, inventoryId):
        return inventoryId in self.inventories

    def sendHasInventory(self, inventoryId, callback):
        self.air.netMessenger.send('hasInventoryResponse', [callback,
            self.hasInventory(inventoryId)])

    def addInventory(self, inventory):
        if self.hasInventory(inventory.doId):
            self.notify.debug('Tried to add an already existing inventory %d!' % (
                inventory.doId))

            return

        self.inventories[inventory.doId] = inventory

    def removeInventory(self, inventory):
        if not self.hasInventory(inventory.doId):
            self.notify.debug('Tried to remove a non-existant inventory %d!' % (
                inventory.doId))

            return

        inventory.requestDelete()
        del self.inventories[inventory.doId]

    def getInventory(self, avatarId):
        for inventory in self.inventories.values():
            if inventory.getOwnerId() == avatarId:
                return inventory

        return None

    def sendGetInventory(self, avatarId, callback):
        self.air.netMessenger.send('getInventoryResponse', [callback,
            self.getInventory(avatarId)])

    def requestInventory(self):
        avatarId = self.air.getAvatarIdFromSender()

        if not avatarId:
            return

        self.initiateInventory(avatarId)

    def initiateInventory(self, avatarId):

        def queryResponse(dclass, fields):
            if not dclass or not fields:
                self.notify.debug('Failed to query avatar %d!' % (
                    avatarId))

                return

            inventoryId, = fields.get('setInventoryId', (0,))

            if not inventoryId:
                self.notify.warning('Avatar %d does not have an inventory!' % (
                    avatarId))

                return

            self.__sendInventory(avatarId, inventoryId)

        self.air.dbInterface.queryObject(self.air.dbId,
            avatarId,
            callback=queryResponse,
            dclass=self.air.dclassesByName['DistributedPlayerPirateAI'])

    def __waitForInventory(self, avatarId, inventoryId, task):
        inventory = self.inventories.get(inventoryId)

        if not inventory:
            self.notify.debug('Failed to retrieve inventory %d for avatar %d!' % (
                inventoryId, avatarId))

            return task.done

        self.__sendInventory(avatarId, inventory.doId)
        return task.done

    def __cleanupWaitForInventory(self, avatarId):
        if avatarId not in self.pendingInventories:
            return

        self.ignore('distObjDelete-%d' % avatarId)
        taskMgr.remove(self.pendingInventories[avatarId])
        del self.pendingInventories[avatarId]

    def __sendInventory(self, avatarId, inventoryId):
        inventory = self.inventories.get(inventoryId)

        self.acceptOnce('distObjDelete-%d' % avatarId, lambda: \
            self.__cleanupWaitForInventory(avatarId))

        if not inventory:
            if avatarId in self.pendingInventories:
                self.notify.debug('Cannot retrieve inventory for avatar %d, already trying to get inventory!' % (
                    avatarId))

                return

            self.pendingInventories[avatarId] = taskMgr.doMethodLater(5.0,
                self.__waitForInventory,
                self.uniqueName('waitForInventory-%d' % avatarId),
                appendTask=True,
                extraArgs=[avatarId, inventoryId])

            return

        avatar = self.air.doId2do.get(avatarId)

        if not avatar:
            return

        def inventoryResponseCalback(dclass, fields):
            if not dclass or not fields:
                self.notify.debug('Failed to query inventory %d for avatar %d!' % (
                    inventoryId, avatarId))

                return

            categoriesAndLimits, = fields.get('setCategoryLimits', [])
            categoriesAndDoIds, = fields.get('setDoIds', [])
            accumulatorTypesAndQuantities, = fields.get('setAccumulators', [])
            stackTypesAndLimits, = fields.get('setStackLimits', [])
            stackTypesAndQuantities, = fields.get('setStacks', [])

            for categoryAndLimit in categoriesAndLimits:
                inventory.b_setCategoryLimit(*categoryAndLimit)

            inventory.b_setDoIds(categoriesAndDoIds)

            for accumulatorTypeAndQuantity in accumulatorTypesAndQuantities:
                inventory.b_setAccumulator(*accumulatorTypeAndQuantity)

            for stackTypeAndLimit in stackTypesAndLimits:
                inventory.b_setStackLimit(*stackTypeAndLimit)

            for stackTypeAndQuantity in stackTypesAndQuantities:
                inventory.b_setStackQuantity(*stackTypeAndQuantity)

            inventory.b_setStackLimit(InventoryType.Hp, avatar.getMaxHp())
            inventory.b_setStackLimit(InventoryType.Mojo, avatar.getMaxMojo())

            inventory.d_requestInventoryComplete()

        self.air.dbInterface.queryObject(self.air.dbId,
            inventoryId,
            callback=inventoryResponseCalback,
            dclass=self.air.dclassesByName['DistributedInventoryAI'])

    def proccessCallbackResponse(self, callback, *args, **kwargs):
        if callback and callable(callback):
            callback(*args, **kwargs)
            return

        self.notify.warning('No valid callback for a callback response!'
            'What was the purpose of that?')


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def maxSP():
    invoker = spellbook.getInvoker()
    inventory = simbase.air.inventoryManager.getInventory(invoker.doId)
    if inventory:
        inventory.b_setStackQuantity(InventoryType.UnspentMelee, 255)
        inventory.b_setStackQuantity(InventoryType.UnspentCutlass, 255)
        inventory.b_setStackQuantity(InventoryType.UnspentPistol, 255)
        inventory.b_setStackQuantity(InventoryType.UnspentMusket, 255)
        inventory.b_setStackQuantity(InventoryType.UnspentDagger, 255)
        inventory.b_setStackQuantity(InventoryType.UnspentGrenade, 255)
        inventory.b_setStackQuantity(InventoryType.UnspentWand, 255)
        inventory.b_setStackQuantity(InventoryType.UnspentDoll, 255)
        inventory.b_setStackQuantity(InventoryType.UnspentKettle, 255)
        inventory.b_setStackQuantity(InventoryType.UnspentCannon, 255)
        inventory.b_setStackQuantity(InventoryType.UnspentSailing, 255)
        return "Maxed out Skill Points!"

    return "Failed to max out Skill Points!"


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def maxWeapons():
    invoker = spellbook.getInvoker()
    inventory = simbase.air.inventoryManager.getInventory(invoker.doId)
    if inventory:
        # There is a rank higher, but i don't think it was even a thing in-game back then,
        # Because i've heard alot about pirate blade being the best. Which is L5.
        # So i think L5 was the highest available to the player at the time.
        ## Some nice ol grammar better put together while this comment has bad grammar fix ~ Dan.

        # Remove the original items from your inventory stacks...
        inventory.b_setStackQuantity(InventoryType.CutlassWeaponL1, 0)
        inventory.b_setStackQuantity(InventoryType.PistolWeaponL1, 0)
        inventory.b_setStackQuantity(InventoryType.DollWeaponL1, 0)
        inventory.b_setStackQuantity(InventoryType.DaggerWeaponL1, 0)
        inventory.b_setStackQuantity(InventoryType.WandWeaponL1, 0)

        # Set new weapon stacks
        inventory.b_setStackQuantity(InventoryType.CutlassWeaponL5, 1)
        inventory.b_setStackQuantity(InventoryType.PistolWeaponL5, 1)
        inventory.b_setStackQuantity(InventoryType.BayonetWeaponL3, 0)
        inventory.b_setStackQuantity(InventoryType.MusketWeaponL3, 0)
        inventory.b_setStackQuantity(InventoryType.DollWeaponL5, 1)
        inventory.b_setStackQuantity(InventoryType.DaggerWeaponL5, 1)
        inventory.b_setStackQuantity(InventoryType.WandWeaponL5, 1)

        # There is only one true rank for grenade weapons. Not sure why disney added more
        inventory.b_setStackQuantity(InventoryType.GrenadeWeaponL1, 1)

        # Set Ammo
        inventory.b_setStackQuantity(InventoryType.AmmoAsp, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoAdder, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoSidewinder, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoViperNest, 99)

        inventory.b_setStackQuantity(InventoryType.AmmoLeadShot, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoVenomShot, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoBaneShot, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoHexEaterShot, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoSilverShot, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoSteelShot, 99)

        inventory.b_setStackQuantity(InventoryType.AmmoScatterShot, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoCursedShot, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoCoalfireShot, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoHeavySlug, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoExploderShot, 99)

        inventory.b_setStackQuantity(InventoryType.AmmoGrenadeExplosion, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoGrenadeShockBomb, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoGrenadeFlame, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoGrenadeSmoke, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoGrenadeLandMine, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoGrenadeSiege, 99)

        inventory.b_setStackQuantity(InventoryType.AmmoChainShot, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoGrapeShot, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoFirebrand, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoThunderbolt, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoExplosive, 99)
        inventory.b_setStackQuantity(InventoryType.AmmoFury, 99)
        return "Maxed weapons to Rank 5!"

    return "Failed to max Weapons"


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def gold(amount):
    invoker = spellbook.getInvoker()
    inventory = simbase.air.inventoryManager.getInventory(invoker.doId)
    inventory.setGoldInPocket(inventory.getGoldInPocket() + amount)
    return 'Received Gold Amount %s | Current Gold Amount: %s' % (min(amount, 65000), inventory.getGoldInPocket())


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def removeGold(amount):
    invoker = spellbook.getInvoker()
    inventory = simbase.air.inventoryManager.getInventory(invoker.doId)
    inventory.setGoldInPocket(inventory.getGoldInPocket() - min(amount, 65000))
    return 'Removed Gold Amount: %s' % amount
