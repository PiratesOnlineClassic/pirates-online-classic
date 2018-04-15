from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal
from otp.ai.MagicWordGlobal import *
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory

class DistributedInventoryManagerAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryManagerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

        self.inventories = {}
        self.inventoryTasks = {}
        
    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)
        
        self.air.netMessenger.accept('hasInventory', self, self.sendHasInventory)
        self.air.netMessenger.accept('addInventory', self, self.addInventory)
        self.air.netMessenger.accept('removeInventory', self, self.removeInventory)
        self.air.netMessenger.accept('getInventory', self, self.sendGetInventory)

    def hasInventory(self, inventoryId):
        return inventoryId in self.inventories
        
    def sendHasInventory(self, inventoryId, callback):
        self.air.netMessenger.send('hasInventoryResponse', [callback, self.hasInventory(inventoryId)])

    def addInventory(self, inventory):
        if self.hasInventory(inventory.doId):
            self.notify.debug('Tried to add an already existing inventory %d!' % inventory.doId)
            return

        self.inventories[inventory.doId] = inventory

    def removeInventory(self, inventory):
        if not self.hasInventory(inventory.doId):
            self.notify.debug('Tried to remove a non-existant inventory %d!' % inventory.doId)
            return

        del self.inventories[inventory.doId]
        inventory.requestDelete()

    def getInventory(self, avatarId):
        for inventory in self.inventories.values():
            if inventory.getOwnerId() == avatarId:
                return inventory

        return None
        
    def sendGetInventory(self, avatarId, callback):
        self.air.netMessenger.send('getInventoryResponse', [callback, self.getInventory(avatarId)])

    def requestInventory(self):
        avatarId = self.air.getAvatarIdFromSender()

        if not avatarId:
            return

        def queryResponse(dclass, fields):
            if not dclass or not fields:
                self.notify.debug('Failed to query avatar %d!' % avatarId)
                return

            inventoryId, = fields.get('setInventoryId', (0,))

            if not inventoryId:
                self.notify.debug('Invalid inventory found for avatar %d!' % avatarId)
                return

            self.__sendInventory(avatarId, inventoryId)

        self.air.dbInterface.queryObject(self.air.dbId, avatarId, callback=queryResponse, dclass=\
            self.air.dclassesByName['DistributedPlayerPirateAI'])

    def __waitForInventory(self, avatarId, inventoryId, task):
        inventory = self.inventories.get(inventoryId)

        if not inventory:
            return task.again

        self.__sendInventory(avatarId, inventory.doId)
        return task.done

    def __cleanupWaitForInventory(self, avatarId):
        if avatarId not in self.inventoryTasks:
            return

        taskMgr.remove(self.inventoryTasks[avatarId])
        del self.inventoryTasks[avatarId]

    def __sendInventory(self, avatarId, inventoryId):
        inventory = self.inventories.get(inventoryId)

        self.acceptOnce('distObjDelete-%d' % (avatarId), lambda: \
            self.__cleanupWaitForInventory(avatarId))

        if not inventory:
            if avatarId in self.inventoryTasks:
                self.notify.debug('Cannot retrieve inventory for avatar %d, already trying to get inventory!' % (
                    avatarId))

                return

            self.inventoryTasks[avatarId] = taskMgr.doMethodLater(1.0, self.__waitForInventory, 'waitForInventory-%d-%s' % (
                avatarId, id(self)), appendTask=True, extraArgs=[avatarId, inventoryId])

            return

        avatar = self.air.doId2do.get(avatarId)

        if not avatar:
            self.notify.debug('Cannot send inventory, unknown avatar!')
            return

        inventory.b_setStackLimit(InventoryType.Hp, avatar.getMaxHp())
        inventory.b_setStackLimit(InventoryType.Mojo, avatar.getMaxMojo())

        def inventoryResponse(dclass, fields):
            if not dclass or not fields:
                self.notify.debug('Failed to query inventory %d!' % avatarId)
                return

            accumulators, = fields.get('setAccumulators', [])
            stackLimits, = fields.get('setStackLimits', [])
            stacks, = fields.get('setStacks', [])

            for accumulator in accumulators:
                inventory.b_setAccumulator(*accumulator)

            inventory.b_setStackLimits(stackLimits)

            for stack in stacks:
                inventory.b_setStack(*stack)

            inventory.d_requestInventoryComplete()

        self.air.dbInterface.queryObject(self.air.dbId, inventoryId, callback=inventoryResponse, dclass=\
            self.air.dclassesByName['DistributedInventoryAI'])
            
    def proccessCallbackResponse(self, callback, *args, **kwargs):
        if callback and callable(callback):
            callback(*args, **kwargs)
            return
        self.notify.warning("No valid callback for a callback response! What was the purpose of that?")

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def maxOutSkillPoints():
    invoker = spellbook.getInvoker()
    inventory = simbase.air.inventoryManager.getInventory(invoker.doId)
    if inventory:
        inventory.b_setStack(InventoryType.UnspentMelee, 255)
        inventory.b_setStack(InventoryType.UnspentCutlass, 255)
        inventory.b_setStack(InventoryType.UnspentPistol, 255)
        inventory.b_setStack(InventoryType.UnspentMusket, 255)
        inventory.b_setStack(InventoryType.UnspentDagger, 255)
        inventory.b_setStack(InventoryType.UnspentGrenade, 255)
        inventory.b_setStack(InventoryType.UnspentWand, 255)
        inventory.b_setStack(InventoryType.UnspentDoll, 255)
        inventory.b_setStack(InventoryType.UnspentKettle, 255)
        inventory.b_setStack(InventoryType.UnspentCannon, 255)
        inventory.b_setStack(InventoryType.UnspentSailing, 255)
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
        inventory.b_setStack(InventoryType.CutlassWeaponL5, 1)
        inventory.b_setStack(InventoryType.PistolWeaponL5, 1)
        inventory.b_setStack(InventoryType.BayonetWeaponL3, 0)
        inventory.b_setStack(InventoryType.MusketWeaponL3, 0)
        inventory.b_setStack(InventoryType.DollWeaponL5, 1)
        inventory.b_setStack(InventoryType.DaggerWeaponL5, 1)
        inventory.b_setStack(InventoryType.GrenadeWeaponL5, 1)
        inventory.b_setStack(InventoryType.WandWeaponL5, 1)
        
        inventory.b_setStack(InventoryType.AmmoAsp, 99)
        inventory.b_setStack(InventoryType.AmmoAdder, 99)
        inventory.b_setStack(InventoryType.AmmoSidewinder, 99)
        inventory.b_setStack(InventoryType.AmmoViperNest, 99)
        
        inventory.b_setStack(InventoryType.AmmoLeadShot, 99)
        inventory.b_setStack(InventoryType.AmmoVenomShot, 99)
        inventory.b_setStack(InventoryType.AmmoBaneShot, 99)
        inventory.b_setStack(InventoryType.AmmoHexEaterShot, 99)
        inventory.b_setStack(InventoryType.AmmoSilverShot, 99)
        inventory.b_setStack(InventoryType.AmmoSteelShot, 99)
        
        inventory.b_setStack(InventoryType.AmmoScatterShot, 99)
        inventory.b_setStack(InventoryType.AmmoCursedShot, 99)
        inventory.b_setStack(InventoryType.AmmoCoalfireShot, 99)
        inventory.b_setStack(InventoryType.AmmoHeavySlug, 99)
        inventory.b_setStack(InventoryType.AmmoExploderShot, 99)
        
        inventory.b_setStack(InventoryType.AmmoGrenadeExplosion, 99)
        inventory.b_setStack(InventoryType.AmmoGrenadeShockBomb, 99)
        inventory.b_setStack(InventoryType.AmmoGrenadeFlame, 99)
        inventory.b_setStack(InventoryType.AmmoGrenadeSmoke, 99)
        inventory.b_setStack(InventoryType.AmmoGrenadeLandMine, 99)
        inventory.b_setStack(InventoryType.AmmoGrenadeSiege, 99)
        return "Maxed weapons to Rank 5!"

    return "Failed to max Weapons"