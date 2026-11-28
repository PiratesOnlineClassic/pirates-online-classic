from direct.directnotify.DirectNotifyGlobal import directNotify

from pirates.pirate.BattleNPCGameFSMAI import BattleNPCGameFSMAI


class BossNPCGameFSMAI(BattleNPCGameFSMAI):
    notify = directNotify.newCategory('BossNPCGameFSMAI')

    def getAttackSkills(self):
        # bosses also get to use their own special skills along
        # with the skills of their non boss avatar type.
        return self.avatar.getAttackSkills()
