from pirates.pirate.BattleAvatarGameFSMAI import BattleAvatarGameFSMAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesbase import PiratesGlobals

class PlayerPirateGameFSMAI(BattleAvatarGameFSMAI):
    notify = directNotify.newCategory('PlayerPirateGameFSMAI')

    def __init__(self, air, avatar):
        BattleAvatarGameFSMAI.__init__(self, air, avatar)

        self.jailTeleportingTask = None
        self.jailTeleportingFinishTask = None

    def enterDeath(self):

        def teleportToJail(task):
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

            self.avatar.setJailCellIndex(cellDoor.getCellIndex())

            # tell the instance to send the avatar to the jail, and set it's interest
            # properly before we update their game state...
            instance.d_sendLocalAvatarToJail(self.avatar.doId, interior.doId,
                interior.parentId, interior.zoneId)

            return task.done

        # eliminate race conditions...
        self.jailTeleportingTask = taskMgr.doMethodLater(5.0, teleportToJail,
            self.avatar.uniqueName('teleport-to-jail'))

    def exitDeath(self):
        if self.jailTeleportingTask:
            taskMgr.remove(self.jailTeleportingTask)
            self.jailTeleportingTask = None

    def enterThrownInJail(self):

        def teleportToJailFinish(task):
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

            # retrieve the spawn position of the avatar's current cell index,
            # this is where the avatar will spawn in the jail cell...
            (x, y, z, h) = instance.getSpawnPt(area.getUniqueId(), self.avatar.getJailCellIndex())
            instance.d_setSpawnInfo(self.avatar.doId, x, y, z, h, 0, [area.doId,
                area.parentId, area.zoneId])

            # broadcast the avatar's current cell index to enable interaction with
            # the appropriate cell door...
            self.avatar.d_setJailCellIndex(self.avatar.getJailCellIndex())

            # finally set the new location of the avatar to be located
            # in the same interests as all other objects in the jail...
            self.avatar.b_setLocation(area.doId, PiratesGlobals.InteriorDoorZone)

            return task.done

        # eliminate race conditions...
        self.jailTeleportingFinishTask = taskMgr.doMethodLater(2.0, teleportToJailFinish,
            self.avatar.uniqueName('teleport-to-jail-finish'))

    def exitThrownInJail(self):
        if self.jailTeleportingFinishTask:
            taskMgr.remove(self.jailTeleportingFinishTask)
            self.jailTeleportingFinishTask = None
