from direct.directnotify.DirectNotifyGlobal import directNotify

from pirates.pirate.BattleAvatarGameFSMAI import BattleAvatarGameFSMAI
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PiratesGlobals
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI


class PlayerPirateGameFSMAI(BattleAvatarGameFSMAI):
    notify = directNotify.newCategory('PlayerPirateGameFSMAI')

    def __init__(self, air, avatar):
        BattleAvatarGameFSMAI.__init__(self, air, avatar)

    def enterLandRoam(self):
        self.avatar.startToonUp()

    def exitLandRoam(self):
        self.avatar.stopToonUp()

    def enterDeath(self):
        inventory = self.avatar.getInventory()
        assert(inventory is not None)

        parentObj = self.avatar.getParentObj()
        interior = parentObj.getJailInterior()
        if not interior:
            island = self.air.uidMgr.justGetMeMeObject(self.avatar.getReturnLocation())
            assert(island is not None)
            interior = island.getJailInterior()

        if not inventory:
            self.notify.warning('Cannot teleport avatar %d, no inventory was found!' %
                self.avatar.doId)

            return

        if self.avatar.testTeleportFlag(PiratesGlobals.TFInJail):
            self.notify.debug('Cannot teleport avatar %d to jail, '
                'avatar already in jail!' % self.avatar.doId)

            return

        if not isinstance(parentObj, DistributedGameAreaAI):
            self.notify.warning('Cannot teleport avatar %d to jail, '
                'parent object has invalid type: %r!' % (self.avatar.doId, parentObj))

            return

        if not interior:
            self.notify.warning('Cannot teleport avatar %d to jail, '
                'parent object %d has unknown interior object!' % (self.avatar.doId, parentObj.doId))

            return

        cellDoor = interior.getCellDoor()
        if not cellDoor:
            self.notify.warning('Cannot teleport avatar %d to jail, '
                'no cell were doors found for interior %d!' % (self.avatar.doId, interior.doId))

            return

        # prepare this jail cell to be occupied by the avatar
        # that has just died and we are now sending to the jail...
        cellDoor.setAvatarId(0)
        cellDoor.b_setHealth(cellDoor.getMaxHealth())
        self.avatar.b_setJailCellIndex(cellDoor.getCellIndex())

        # update the avatar's inventory values
        vitaeCost = (10 * 60) * 60
        inventory.b_setStackQuantity(InventoryType.Vitae_Level, 1)
        inventory.b_setStackQuantity(InventoryType.Vitae_Cost, vitaeCost)
        inventory.b_setStackQuantity(InventoryType.Vitae_Left, vitaeCost)
        self.avatar.b_setHp(1)

        # tell the instance to send the avatar to the jail, and set it's interest
        # properly before we update their game state...
        parentWorld = parentObj.getParentObj()
        parentWorld.d_sendLocalAvatarToJail(self.avatar.doId, interior.doId,
            interior.parentId, interior.zoneId)

    def exitDeath(self):
        pass

    def enterThrownInJail(self):
        if not self.avatar.testTeleportFlag(PiratesGlobals.TFInJail):
            self.notify.debug('Cannot finish teleporting avatar %d to jail, '
                'avatar was never teleporting to jail!' % self.avatar.doId)

            return

        parentObj = self.avatar.getParentObj()
        if not parentObj:
            self.notify.warning('Cannot finish teleporting avatar %d to jail, '
                'no parent object found!' % self.avatar.doId)

            return

        if not isinstance(parentObj, DistributedGameAreaAI):
            self.notify.warning('Cannot finish teleporting avatar %d to jail, '
                'parent object has invalid type: %r!' % (self.avatar.doId, parentObj))

            return

        # broadcast the avatar's current cell index to enable interaction with
        # the appropriate cell door...
        self.avatar.d_setJailCellIndex(self.avatar.getJailCellIndex())

        # retrieve the spawn position of the avatar's current cell index,
        # this is where the avatar will spawn in the jail cell...
        parentWorld = parentObj.getParentObj()
        (x, y, z, h) = parentWorld.getSpawnPt(parentObj.getUniqueId(), self.avatar.getJailCellIndex())
        parentWorld.d_setSpawnInfo(self.avatar.doId, x, y, z, h, 0, [parentObj.doId,
            parentObj.parentId, parentObj.zoneId])

    def exitThrownInJail(self):
        pass
