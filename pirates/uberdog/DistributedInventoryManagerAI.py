from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from otp.ai.MagicWordGlobal import *

from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase


class InventoryOperationFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('InventoryOperationFSM')

    def __init__(self, air, avatar, callback=None):
        FSM.__init__(self, self.__class__.__name__)

        self.air = air
        self.avatar = avatar
        self.callback = callback

    def getAvatarClassName(self):
        return 'DistributedPlayerPirateAI'

    def getInventoryClassName(self):
        return 'PirateInventoryAI'

    def enterOff(self):
        pass

    def exitOff(Self):
        pass

    def cleanup(self, *args, **kwargs):
        del self.air.inventoryManager.avatar2fsm[self.avatar.doId]
        self.ignoreAll()
        self.demand('Off')

        if self.callback:
            self.callback(*args, **kwargs)


class LoadInventoryFSM(InventoryOperationFSM):

    def enterStart(self):
        self.air.dbInterface.queryObject(self.air.dbId,
            self.avatar.doId,
            callback=self._avatarQueryCallback,
            dclass=self.air.dclassesByName[self.getAvatarClassName()])

        self.acceptOnce(self.avatar.getDeleteEvent(), lambda: self.cleanup(None))

    def _avatarQueryCallback(self, dclass, fields):
        if not dclass or not fields:
            self.notify.debug('Failed to query avatar %d!' % self.avatar.doId)
            self.cleanup(None)
            return

        inventoryId, = fields.get('setInventoryId', (0,))
        if not inventoryId:
            self.notify.warning('Avatar %d does not have an inventory!' % self.avatar.doId)
            self.cleanup(None)
            return

        inventory = self.air.doId2do.get(inventoryId)
        if not inventory:
            self.acceptOnce('generate-%d' % inventoryId, self._inventoryArrivedCallback)
        else:
            self._inventoryArrivedCallback(inventory)

    def finalizeInventory(self):
        self.inventory.b_setStackLimit(InventoryType.Hp, self.avatar.getMaxHp())
        self.inventory.b_setStackLimit(InventoryType.Mojo, self.avatar.getMaxMojo())

    def _inventoryArrivedCallback(self, inventory):
        self.inventory = inventory
        if not inventory:
            self.notify.warning('Failed to retrieve inventory for avatar %d' % self.avatar.doId)
            self.cleanup(None)
            return

        self.finalizeInventory()
        self.inventory.populateInventory()
        self.cleanup(self.inventory)

    def exitStart(self):
        pass


class LoadShipInventoryFSM(LoadInventoryFSM):

    def getAvatarClassName(self):
        return 'PlayerShipAI'

    def getInventoryClassName(self):
        return 'DistributedInventoryAI'

    def finalizeInventory(self):
        pass


class DistributedInventoryManagerAI(DistributedObjectGlobalAI):
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

    def hasInventory(self, inventoryId):
        return inventoryId in list(self.inventories)

    def sendHasInventory(self, inventoryId, callback):
        self.air.netMessenger.send('hasInventoryResponse', [callback,
            self.hasInventory(inventoryId)])

    def addInventory(self, inventory):
        if self.hasInventory(inventory.doId):
            self.notify.debug('Tried to add an already existing inventory %d!' % inventory.doId)
            return

        self.inventories[inventory.doId] = inventory

    def removeInventory(self, inventory):
        if not self.hasInventory(inventory.doId):
            self.notify.debug('Tried to remove a non-existant inventory %d!' % inventory.doId)
            return

        inventory.requestDelete()
        del self.inventories[inventory.doId]

    def getInventory(self, avatarId):
        for inventory in list(self.inventories.values()):
            if inventory.getOwnerId() == avatarId:
                return inventory

        return None

    def sendGetInventory(self, avatarId, callback):
        self.air.netMessenger.send('getInventoryResponse', [callback, self.getInventory(avatarId)])

    def runInventoryFSM(self, fsmtype, avatar, *args, **kwargs):
        if avatar.doId in self.avatar2fsm:
            self.notify.debug('Failed to run inventory FSM for avatar %d, '
                'an FSM already running!' % avatar.doId)

            return

        callback = kwargs.pop('callback', None)

        self.avatar2fsm[avatar.doId] = fsmtype(self.air, avatar, callback)
        self.avatar2fsm[avatar.doId].request('Start', *args, **kwargs)

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


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def weaponrank(rank):
    """
    Sets your weapon rank to the specified rank (1-6)
    """

    invoker = spellbook.getInvoker()
    inventory = simbase.air.inventoryManager.getInventory(invoker.doId)

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
    inventory = simbase.air.inventoryManager.getInventory(invoker.doId)
    inventory.setGoldInPocket(inventory.getGoldInPocket() + amount)
    return 'Received Gold Amount %s | Current Gold Amount: %s' % (min(amount, 65000), inventory.getGoldInPocket())


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def removeGold(amount):
    invoker = spellbook.getInvoker()
    inventory = simbase.air.inventoryManager.getInventory(invoker.doId)
    inventory.setGoldInPocket(inventory.getGoldInPocket() - min(amount, 65000))
    return 'Removed Gold Amount: %s' % amount


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def givePork():
    invoker = spellbook.getInvoker()
    inventory = simbase.air.inventoryManager.getInventory(invoker.doId)
    inventory.b_setStackQuantity(InventoryType.PorkChunk, 10)
    return 'Pork Chunks Given!'
