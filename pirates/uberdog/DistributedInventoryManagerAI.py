from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, InventoryCategory

class DistributedInventoryManagerAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryManagerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

        self.inventories = {}
        self.inventoryTasks = {}

    def hasInventory(self, inventoryId):
        return inventoryId in self.inventories

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

        # Weapons
        inventory.b_setStack(InventoryType.CutlassWeaponL1, 1)
        inventory.b_setStack(InventoryType.PistolWeaponL1, 1)
        inventory.b_setStack(InventoryType.MusketWeaponL1, 1)
        inventory.b_setStack(InventoryType.DaggerWeaponL1, 1)
        inventory.b_setStack(InventoryType.GrenadeWeaponL1, 1)
        inventory.b_setStack(InventoryType.DollWeaponL1, 1)
        inventory.b_setStack(InventoryType.WandWeaponL1, 1)

        # Cutlass Skills
        inventory.b_setStack(InventoryType.CutlassHack, 1)
        inventory.b_setStack(InventoryType.CutlassSlash, 1)

        # Gun Skills
        inventory.b_setStack(InventoryType.PistolShoot, 1)
        inventory.b_setStack(InventoryType.PistolLeadShot, 1)
        inventory.b_setStack(InventoryType.PistolVenomShot, 0)
        inventory.b_setStack(InventoryType.PistolBaneShot, 0)
        inventory.b_setStack(InventoryType.PistolHexEaterShot, 0)
        inventory.b_setStack(InventoryType.PistolSilverShot, 0)
        inventory.b_setStack(InventoryType.PistolSteelShot, 0)
        inventory.b_setStack(InventoryType.PistolSharpShooter, 0)
        inventory.b_setStack(InventoryType.PistolDodge, 0)
        inventory.b_setStack(InventoryType.PistolEagleEye, 0)
        inventory.b_setStack(InventoryType.PistolTakeAim, 0)
        
        # Musket Skills
        inventory.b_setStack(InventoryType.MusketShoot, 1)
        inventory.b_setStack(InventoryType.MusketTakeAim, 1)
        inventory.b_setStack(InventoryType.MusketDeadeye, 0)
        inventory.b_setStack(InventoryType.MusketEagleEye, 0)
        inventory.b_setStack(InventoryType.MusketCrackShot, 0)
        inventory.b_setStack(InventoryType.MusketMarksman, 0)
        inventory.b_setStack(InventoryType.MusketLeadShot, 0)
        inventory.b_setStack(InventoryType.MusketScatterShot, 0)
        inventory.b_setStack(InventoryType.MusketCursedShot, 0)
        inventory.b_setStack(InventoryType.MusketCoalfireShot, 0)
        inventory.b_setStack(InventoryType.MusketHeavySlug, 0)
        inventory.b_setStack(InventoryType.MusketExploderShot, 0)

        # Doll Skills
        inventory.b_setStack(InventoryType.DollAttune, 1)
        inventory.b_setStack(InventoryType.DollPoke, 1)

        # Dagger Skills
        inventory.b_setStack(InventoryType.DaggerCut, 1)
        inventory.b_setStack(InventoryType.DaggerSwipe, 1)
        inventory.b_setStack(InventoryType.DaggerGouge, 0)
        inventory.b_setStack(InventoryType.DaggerEviscerate, 0)
        inventory.b_setStack(InventoryType.DaggerFinesse, 0)
        inventory.b_setStack(InventoryType.DaggerBladeInstinct, 0)
        inventory.b_setStack(InventoryType.DaggerAsp, 0)
        inventory.b_setStack(InventoryType.DaggerAdder, 0)
        inventory.b_setStack(InventoryType.DaggerThrowDirt, 0)
        inventory.b_setStack(InventoryType.DaggerSidewinder, 0)
        inventory.b_setStack(InventoryType.DaggerViperNest, 0)

        # Staff Skills
        inventory.b_setStack(InventoryType.StaffBlast, 1)
        inventory.b_setStack(InventoryType.StaffSoulFlay, 1)

        # Grenade Skills
        inventory.b_setStack(InventoryType.GrenadeThrow, 1)
        
        # Skill Points
        inventory.b_setStack(InventoryType.UnspentMelee, 0)
        inventory.b_setStack(InventoryType.UnspentCutlass, 0)
        inventory.b_setStack(InventoryType.UnspentPistol, 0)
        inventory.b_setStack(InventoryType.UnspentMusket, 0)
        inventory.b_setStack(InventoryType.UnspentDagger, 0)
        inventory.b_setStack(InventoryType.UnspentGrenade, 0)
        inventory.b_setStack(InventoryType.UnspentWand, 0)
        inventory.b_setStack(InventoryType.UnspentDoll, 0)
        inventory.b_setStack(InventoryType.UnspentKettle, 0)
        inventory.b_setStack(InventoryType.UnspentCannon, 0)
        inventory.b_setStack(InventoryType.UnspentSailing, 0)

        # Request inventory completion
        inventory.d_requestInventoryComplete()
