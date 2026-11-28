from direct.directnotify import DirectNotifyGlobal

from pirates.battle.DistributedWeaponAI import DistributedWeaponAI


class DistributedPCCannonAI(DistributedWeaponAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPCCannonAI')

    def gainSkill(self, skillId):
        # cannon skills are only ever earned through reputation, the client never sends this...
        avatarId = self.air.getAvatarIdFromSender()
        self.air.writeServerEvent('suspicious', avId=avatarId,
            issue='Tried to gain cannon skill %d from cannon %d!' % (skillId, self.doId))
