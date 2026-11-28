from direct.directnotify import DirectNotifyGlobal

from pirates.battle.DistributedWeaponAI import DistributedWeaponAI


class DistributedPCCannonAI(DistributedWeaponAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPCCannonAI')

    def __init__(self, air):
        DistributedWeaponAI.__init__(self, air)

    def gainSkill(self, skillId):
        # cannon skills are only ever earned through the avatar's reputation,
        # the client never sends this request so treat it as suspicious...
        avatarId = self.air.getAvatarIdFromSender()
        self.notify.warning('Avatar %d tried to gain cannon skill %d from cannon %d!' % (
            avatarId, skillId, self.doId))

        self.air.writeServerEvent('suspicious', avId=avatarId,
            issue='Tried to gain cannon skill %d from cannon %d!' % (skillId, self.doId))
