from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.TargetManagerBase import TargetManagerBase

class TargetManagerAI(DistributedObjectAI, TargetManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('TargetManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        TargetManagerBase.__init__(self)

        self.projectiles = {}

    def hasProjectile(self, avatarId, skillId, ammoSkillId):
        projectiles = self.projectiles.get(avatarId)

        if not projectiles:
            return False

        for projectile in projectiles:

            if projectile[0] != skillId or projectile[1] != ammoSkillId:
                continue

            return True

        return False

    def addProjectile(self, avatarId, skillId, ammoSkillId, timestamp):
        if self.hasProjectile(avatarId, skillId, ammoSkillId):
            return

        projectiles = self.projectiles.setdefault(avatarId, [])
        projectiles.append([skillId, ammoSkillId, timestamp])

    def removeProjectile(self, avatarId, skillId, ammoSkillId):
        if not self.hasProjectile(avatarId, skillId, ammoSkillId):
            return

        projectiles = self.projectiles.get(avatarId)

        for index in xrange(len(projectiles)):
            projectile = projectiles[index]

            if projectile[0] != skillId or projectile[1] != ammoSkillId:
                continue

            del projectiles[index]
            break

    def getProjectile(self, avatarId, skillId, ammoSkillId):
        projectiles = self.projectiles.get(avatarId)

        if not projectiles:
            return None

        for projectile in projectiles:

            if projectile[0] != skillId or projectile[1] != ammoSkillId:
                continue

            return projectile

        return None

    def delete(self):
        DistributedObjectAI.delete(self)
        TargetManagerBase.delete(self)
