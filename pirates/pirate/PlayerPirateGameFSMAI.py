from pirates.pirate.BattleAvatarGameFSMAI import BattleAvatarGameFSMAI
from pirates.uberdog.UberDogGlobals import InventoryType
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesbase import PiratesGlobals

class PlayerPirateGameFSMAI(BattleAvatarGameFSMAI):
    notify = directNotify.newCategory('PlayerPirateGameFSMAI')

    def __init__(self, air, avatar):
        BattleAvatarGameFSMAI.__init__(self, air, avatar)

        self.jailTeleportingTask = None
        self.jailTeleportingFinishTask = None

    def enterLandRoam(self):
        self.avatar.startToonUp()

    def exitLandRoam(self):
        self.avatar.stopToonUp()

    def enterDeath(self):
        area = self.avatar.getParentObj()

        if not area:
            self.notify.warning('Cannot teleport avatar %d to jail, no parent object found!' % (
                self.avatar.doId))

            return

        instance = area.getParentObj()

        if not instance:
            self.notify.warning('Cannot teleport avatar %d to jail, parent object has no instance!' % (
                self.avatar.doId))

            return

        interior = area.getJailInterior()

        if not interior:
            self.notify.warning('Cannot teleport avatar %d to jail, unknown interior object!' % (
                self.avatar.doId))

            return

        # get a random cell door from the jails list of available cells,
        # ensure a cell doors was available...
        cellDoor = interior.getCellDoor()

        if not cellDoor:
            self.notify.warning('Cannot teleport avatar %d to jail, no cell doors found!' % (
                self.avatar.doId))

            return

        # reset the jail's health and current avatarId incase
        # an avatar is still in the interior...
        cellDoor.setAvatarId(0)
        cellDoor.b_setHealth(cellDoor.getMaxHealth())

        # set the avatar's cell index so they will
        # teleport to the jail interior
        self.avatar.setJailCellIndex(cellDoor.getCellIndex())

        def teleportToJail(task):
            # tell the instance to send the avatar to the jail, and set it's interest
            # properly before we update their game state...
            instance.d_sendLocalAvatarToJail(self.avatar.doId, interior.doId,
                interior.parentId, interior.zoneId)

            # set the avatars groggy state
            inventory = self.avatar.getInventory()
            if not inventory:
                self.notify.warning('Cannot set groggy state for avatar %d, no inventory was found!' %
                    self.avatar.doId)

                return task.done

            vitaeCost = (10 * 60) * 60
            inventory.b_setStackQuantity(InventoryType.Vitae_Level, 1)
            inventory.b_setStackQuantity(InventoryType.Vitae_Cost, vitaeCost)
            inventory.b_setStackQuantity(InventoryType.Vitae_Left, vitaeCost)

            # Set the avatars health to the minimal amounts
            self.avatar.b_setHp(1)

            return task.done

        # eliminate race conditions...
        self.jailTeleportingTask = taskMgr.doMethodLater(5.0, teleportToJail,
            self.avatar.uniqueName('teleport-to-jail'))

    def exitDeath(self):
        if self.jailTeleportingTask:
            taskMgr.remove(self.jailTeleportingTask)
            self.jailTeleportingTask = None

    def enterThrownInJail(self):
        area = self.avatar.getParentObj()

        if not area:
            self.notify.warning('Cannot finish teleporting to jail, Avatar %d has no parent object!' % (
                self.avatar.doId))

            return

        instance = area.getParentObj()

        if not instance:
            self.notify.warning('Cannot finish teleporting to jail, avatar %d parent object has no instance!' % (
                self.avatar.doId))

            return

        def teleportToJailFinish(task):
            # retrieve the spawn position of the avatar's current cell index,
            # this is where the avatar will spawn in the jail cell...
            (x, y, z, h) = instance.getSpawnPt(area.getUniqueId(), self.avatar.getJailCellIndex())
            instance.d_setSpawnInfo(self.avatar.doId, x, y, z, h, 0, [area.doId,
                area.parentId, area.zoneId])

            # broadcast the avatar's current cell index to enable interaction with
            # the appropriate cell door...
            self.avatar.d_setJailCellIndex(self.avatar.getJailCellIndex())

            return task.done

        # eliminate race conditions...
        self.jailTeleportingFinishTask = taskMgr.doMethodLater(2.0, teleportToJailFinish,
            self.avatar.uniqueName('teleport-to-jail-finish'))

    def exitThrownInJail(self):
        if self.jailTeleportingFinishTask:
            taskMgr.remove(self.jailTeleportingFinishTask)
            self.jailTeleportingFinishTask = None
