from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.task import Task

from otp.ai.MagicWordGlobal import *

from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase


class InventoryOperationFSM(FSM):
    """
    Base FSM for AI-side inventory operations.
    
    Provides guaranteed cleanup, timeout handling, and safe callback invocation.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('InventoryOperationFSM')
    TIMEOUT_SECONDS = 30.0

    def __init__(self, manager, avatar, callback=None):
        FSM.__init__(self, self.__class__.__name__)

        self.manager = manager
        self.air = manager.air
        self.avatar = avatar
        self.callback = callback
        self._finished = False
        avatarId = avatar.doId if avatar else 0
        self._timeoutTaskName = 'InventoryFSM-AI-timeout-%d-%d' % (id(self), avatarId)

    def getAvatarClassName(self):
        return 'DistributedPlayerPirateAI'

    def getInventoryClassName(self):
        return 'PirateInventoryAI'

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterStart(self):
        # Start timeout timer
        taskMgr.doMethodLater(
            self.TIMEOUT_SECONDS,
            self._onTimeout,
            self._timeoutTaskName
        )

    def exitStart(self):
        pass

    def _onTimeout(self, task):
        """Called when operation times out."""
        if not self._finished:
            avatarId = self.avatar.doId if self.avatar else 0
            self.notify.warning('Operation timed out for avatar %d' % avatarId)
            self._finish(None)
        return Task.done

    def _finish(self, *args, **kwargs):
        """
        Guaranteed cleanup path. Always call this to complete the operation.
        """
        if self._finished:
            return
        self._finished = True

        # Cancel timeout task
        taskMgr.remove(self._timeoutTaskName)

        # Clean up any event listeners
        self.ignoreAll()

        # Unregister from manager safely
        if hasattr(self, 'manager') and self.manager and self.avatar:
            self.manager.avatar2fsm.pop(self.avatar.doId, None)

        # Transition to Off state
        try:
            self.demand('Off')
        except Exception:
            pass

        # Invoke callback safely
        if self.callback:
            try:
                self.callback(*args, **kwargs)
            except Exception:
                avatarId = self.avatar.doId if self.avatar else 0
                self.notify.exception('Callback failed for avatar %d' % avatarId)

    def cleanup(self, *args, **kwargs):
        """Legacy method - redirects to _finish for backwards compatibility."""
        self._finish(*args, **kwargs)


class LoadInventoryFSM(InventoryOperationFSM):
    """Loads an avatar's inventory from the database."""

    def enterStart(self):
        InventoryOperationFSM.enterStart(self)
        
        try:
            self.air.dbInterface.queryObject(self.air.dbId,
                self.avatar.doId,
                callback=self._avatarQueryCallback,
                dclass=self.air.dclassesByName[self.getAvatarClassName()])
        except Exception:
            self.notify.exception('Failed to query avatar %d' % self.avatar.doId)
            self._finish(None)
            return

        # Listen for avatar deletion to abort gracefully
        self.acceptOnce(self.avatar.getDeleteEvent(), self._onAvatarDeleted)

    def _onAvatarDeleted(self):
        """Handle avatar deletion during load."""
        if not self._finished:
            self.notify.debug('Avatar deleted during inventory load')
            self._finish(None)

    def _avatarQueryCallback(self, dclass, fields):
        if self._finished:
            return
            
        if not dclass or not fields:
            self.notify.debug('Failed to query avatar %d!' % self.avatar.doId)
            self._finish(None)
            return

        inventoryId = 0
        try:
            inventoryId, = fields.get('setInventoryId', (0,))
        except (ValueError, TypeError):
            inventoryId = 0
            
        if not inventoryId:
            self.notify.warning('Avatar %d does not have an inventory!' % self.avatar.doId)
            self._finish(None)
            return

        inventory = self.air.doId2do.get(inventoryId)
        if not inventory:
            self.acceptOnce('generate-%d' % inventoryId, self._inventoryArrivedCallback)
        else:
            self._inventoryArrivedCallback(inventory)

    def finalizeInventory(self):
        if not self.inventory or not self.avatar:
            return
        try:
            self.inventory.b_setStackLimit(InventoryType.Hp, self.avatar.getMaxHp())
            self.inventory.b_setStackLimit(InventoryType.Mojo, self.avatar.getMaxMojo())
        except Exception:
            self.notify.exception('Failed to finalize inventory')

    def _inventoryArrivedCallback(self, inventory):
        if self._finished:
            return
            
        self.inventory = inventory
        if not inventory:
            self.notify.warning('Failed to retrieve inventory for avatar %d' % self.avatar.doId)
            self._finish(None)
            return

        try:
            self.finalizeInventory()
            self.inventory.populateInventory()
        except Exception:
            self.notify.exception('Failed to populate inventory for avatar %d' % self.avatar.doId)
            
        self._finish(self.inventory)

    def exitStart(self):
        pass


class LoadShipInventoryFSM(LoadInventoryFSM):
    """Loads a ship's inventory from the database."""

    def getAvatarClassName(self):
        return 'PlayerShipAI'

    def getInventoryClassName(self):
        return 'DistributedInventoryAI'

    def finalizeInventory(self):
        pass


class DistributedInventoryManagerAI(DistributedObjectGlobalAI):
    """
    AI-side inventory manager.
    
    Manages inventory loading and caching. Responds to netMessenger queries
    from the UberDog and provides inventory lookup for the AI.
    """
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryManagerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)
        self.avatar2fsm = {}
        self.inventories = {}

    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)
        self.air.netMessenger.accept('hasInventory', self, self.sendHasInventory)
        self.air.netMessenger.accept('addInventory', self, self.addInventory)
        self.air.netMessenger.accept('removeInventory', self, self.removeInventory)
        self.air.netMessenger.accept('getInventory', self, self.sendGetInventory)

    def delete(self):
        # Clean up any pending FSMs
        for fsm in list(self.avatar2fsm.values()):
            try:
                fsm._finish(None)
            except Exception:
                pass
        self.avatar2fsm.clear()
        DistributedObjectGlobalAI.delete(self)

    def hasPendingOperation(self, entityId):
        """Check if an operation is already running for this entity."""
        return entityId in self.avatar2fsm

    def hasInventory(self, inventoryId):
        return inventoryId in self.inventories

    def sendHasInventory(self, inventoryId, callback):
        self.air.netMessenger.send('hasInventoryResponse', [callback,
            self.hasInventory(inventoryId)])

    def addInventory(self, inventory):
        if inventory is None:
            return
        if self.hasInventory(inventory.doId):
            self.notify.debug('Tried to add an already existing inventory %d!' % inventory.doId)
            return
        self.inventories[inventory.doId] = inventory

    def removeInventory(self, inventory):
        if inventory is None:
            return
        if not self.hasInventory(inventory.doId):
            self.notify.debug('Tried to remove a non-existant inventory %d!' % inventory.doId)
            return
        try:
            inventory.requestDelete()
        except Exception:
            self.notify.exception('Failed to delete inventory %d' % inventory.doId)
        self.inventories.pop(inventory.doId, None)

    def getInventory(self, avatarId):
        for inventory in list(self.inventories.values()):
            try:
                if inventory.getOwnerId() == avatarId:
                    return inventory
            except Exception:
                continue
        return None

    def sendGetInventory(self, avatarId, callback):
        self.air.netMessenger.send('getInventoryResponse', [callback, self.getInventory(avatarId)])

    def runInventoryFSM(self, fsmtype, avatar, *args, **kwargs):
        if avatar is None:
            self.notify.warning('Cannot run FSM for None avatar')
            callback = kwargs.get('callback')
            if callback:
                try:
                    callback(None)
                except Exception:
                    pass
            return False
            
        if avatar.doId in self.avatar2fsm:
            self.notify.debug('Failed to run inventory FSM for avatar %d, '
                'an FSM already running!' % avatar.doId)
            # Call the callback with failure to avoid leaving caller hanging
            callback = kwargs.get('callback')
            if callback:
                try:
                    callback(None)
                except Exception:
                    pass
            return False

        callback = kwargs.pop('callback', None)
        fsm = fsmtype(self, avatar, callback)
        self.avatar2fsm[avatar.doId] = fsm
        fsm.request('Start', *args, **kwargs)
        return True

    def requestInventory(self):
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return

        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            self.accept('generate-%d' % avatarId, self.initiateInventory)
        else:
            self.initiateInventory(avatar)

    def initiateInventory(self, avatar, callback=None):
        self.runInventoryFSM(LoadInventoryFSM, avatar, callback=callback)

    def initiateShipInventory(self, ship, callback=None):
        self.runInventoryFSM(LoadShipInventoryFSM, ship, callback=callback)

    def processCallbackResponse(self, callback, *args, **kwargs):
        """Safely invoke a callback delivered via netMessenger.

        Wraps the invocation in a try/except and logs any exception
        instead of allowing it to bubble up through the messenger
        task system.
        """
        if callable(callback):
            try:
                callback(*args, **kwargs)
            except Exception:
                try:
                    self.notify.exception('Exception while running callback')
                except Exception:
                    pass
            return

        self.notify.warning('No valid callback for a callback response! What was the purpose of that?')


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def maxSP():
    invoker = spellbook.getInvoker()
    inventory = base.air.inventoryManager.getInventory(invoker.doId)
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


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def weaponrank(rank):
    """
    Sets your weapon rank to the specified rank (1-6)
    """

    invoker = spellbook.getInvoker()
    inventory = base.air.inventoryManager.getInventory(invoker.doId)

    if rank > 6:
        return 'Rank must be within 1-6.'

    # Clear our previous stacks...
    inventory.b_setStackQuantity(InventoryType.CutlassWeaponL1, 0)
    inventory.b_setStackQuantity(InventoryType.PistolWeaponL1, 0)
    inventory.b_setStackQuantity(InventoryType.DollWeaponL1, 0)
    inventory.b_setStackQuantity(InventoryType.DaggerWeaponL1, 0)
    inventory.b_setStackQuantity(InventoryType.WandWeaponL1, 0)

    inventory.b_setStackQuantity(InventoryType.CutlassWeaponL2, 0)
    inventory.b_setStackQuantity(InventoryType.PistolWeaponL2, 0)
    inventory.b_setStackQuantity(InventoryType.DollWeaponL2, 0)
    inventory.b_setStackQuantity(InventoryType.DaggerWeaponL2, 0)
    inventory.b_setStackQuantity(InventoryType.WandWeaponL2, 0)

    inventory.b_setStackQuantity(InventoryType.CutlassWeaponL3, 0)
    inventory.b_setStackQuantity(InventoryType.PistolWeaponL3, 0)
    inventory.b_setStackQuantity(InventoryType.DollWeaponL3, 0)
    inventory.b_setStackQuantity(InventoryType.DaggerWeaponL3, 0)
    inventory.b_setStackQuantity(InventoryType.WandWeaponL3, 0)

    inventory.b_setStackQuantity(InventoryType.CutlassWeaponL4, 0)
    inventory.b_setStackQuantity(InventoryType.PistolWeaponL4, 0)
    inventory.b_setStackQuantity(InventoryType.DollWeaponL4, 0)
    inventory.b_setStackQuantity(InventoryType.DaggerWeaponL4, 0)
    inventory.b_setStackQuantity(InventoryType.WandWeaponL4, 0)

    inventory.b_setStackQuantity(InventoryType.CutlassWeaponL5, 0)
    inventory.b_setStackQuantity(InventoryType.PistolWeaponL5, 0)
    inventory.b_setStackQuantity(InventoryType.DollWeaponL5, 0)
    inventory.b_setStackQuantity(InventoryType.DaggerWeaponL5, 0)
    inventory.b_setStackQuantity(InventoryType.WandWeaponL5, 0)

    inventory.b_setStackQuantity(InventoryType.CutlassWeaponL6, 0)
    inventory.b_setStackQuantity(InventoryType.PistolWeaponL6, 0)
    inventory.b_setStackQuantity(InventoryType.DollWeaponL6, 0)
    inventory.b_setStackQuantity(InventoryType.DaggerWeaponL6, 0)
    inventory.b_setStackQuantity(InventoryType.WandWeaponL6, 0)

    if rank == 1:
        inventory.b_setStackQuantity(InventoryType.CutlassWeaponL1, 1)
        inventory.b_setStackQuantity(InventoryType.PistolWeaponL1, 1)
        inventory.b_setStackQuantity(InventoryType.DollWeaponL1, 1)
        inventory.b_setStackQuantity(InventoryType.DaggerWeaponL1, 1)
        inventory.b_setStackQuantity(InventoryType.WandWeaponL1, 1)
    elif rank == 2:
        inventory.b_setStackQuantity(InventoryType.CutlassWeaponL2, 1)
        inventory.b_setStackQuantity(InventoryType.PistolWeaponL2, 1)
        inventory.b_setStackQuantity(InventoryType.DollWeaponL2, 1)
        inventory.b_setStackQuantity(InventoryType.DaggerWeaponL2, 1)
        inventory.b_setStackQuantity(InventoryType.WandWeaponL2, 1)
    elif rank == 3:
        inventory.b_setStackQuantity(InventoryType.CutlassWeaponL3, 1)
        inventory.b_setStackQuantity(InventoryType.PistolWeaponL3, 1)
        inventory.b_setStackQuantity(InventoryType.DollWeaponL3, 1)
        inventory.b_setStackQuantity(InventoryType.DaggerWeaponL3, 1)
        inventory.b_setStackQuantity(InventoryType.WandWeaponL3, 1)
    elif rank == 4:
        inventory.b_setStackQuantity(InventoryType.CutlassWeaponL4, 1)
        inventory.b_setStackQuantity(InventoryType.PistolWeaponL4, 1)
        inventory.b_setStackQuantity(InventoryType.DollWeaponL4, 1)
        inventory.b_setStackQuantity(InventoryType.DaggerWeaponL4, 1)
        inventory.b_setStackQuantity(InventoryType.WandWeaponL4, 1)
    elif rank == 5:
        inventory.b_setStackQuantity(InventoryType.CutlassWeaponL5, 1)
        inventory.b_setStackQuantity(InventoryType.PistolWeaponL5, 1)
        inventory.b_setStackQuantity(InventoryType.DollWeaponL5, 1)
        inventory.b_setStackQuantity(InventoryType.DaggerWeaponL5, 1)
        inventory.b_setStackQuantity(InventoryType.WandWeaponL5, 1)
    elif rank == 6:
        # Unreleased weapon rank.
        inventory.b_setStackQuantity(InventoryType.CutlassWeaponL6, 1)
        inventory.b_setStackQuantity(InventoryType.PistolWeaponL6, 1)
        inventory.b_setStackQuantity(InventoryType.DollWeaponL6, 1)
        inventory.b_setStackQuantity(InventoryType.DaggerWeaponL6, 1)
        inventory.b_setStackQuantity(InventoryType.WandWeaponL6, 1)

    return 'Set weapon rank to %s!' % rank


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def maxWeapons():
    invoker = spellbook.getInvoker()
    inventory = base.air.inventoryManager.getInventory(invoker.doId)
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

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int, int])
def givePlayerStack(stackId, amount):
    invoker = spellbook.getInvoker()
    inventory = invoker.getInventory()

    if not inventory:
        return

    inventory.b_setStackQuantity(stackId, amount)
    return 'Gave %s stackId %d with a quantity of %d' % (invoker.getName(), stackId, amount)


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def gold(amount):
    invoker = spellbook.getInvoker()
    inventory = base.air.inventoryManager.getInventory(invoker.doId)
    inventory.setGoldInPocket(inventory.getGoldInPocket() + amount)
    return 'Received Gold Amount %s | Current Gold Amount: %s' % (min(amount, 65000), inventory.getGoldInPocket())


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def removeGold(amount):
    invoker = spellbook.getInvoker()
    inventory = base.air.inventoryManager.getInventory(invoker.doId)
    inventory.setGoldInPocket(inventory.getGoldInPocket() - min(amount, 65000))
    return 'Removed Gold Amount: %s' % amount


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def givePork():
    invoker = spellbook.getInvoker()
    inventory = base.air.inventoryManager.getInventory(invoker.doId)
    inventory.b_setStackQuantity(InventoryType.PorkChunk, 10)
    return 'Pork Chunks Given!'
