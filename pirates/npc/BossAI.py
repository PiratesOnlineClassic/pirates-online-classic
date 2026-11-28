from direct.directnotify import DirectNotifyGlobal
from pirates.npc.BossBase import BossBase
from pirates.npc.BossNPCList import BOSS_NPC_LIST
from pirates.battle import EnemyGlobals

class BossAI(BossBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('BossAI')

    def __init__(self, air):
        BossBase.__init__(self, air)
        self.air = air

    def loadBossData(self, uniqueId, avatarType):
        # only named bosses listed in the boss npc list have their own data,
        # every other boss is generated from it's avatar type.
        if uniqueId and uniqueId in BOSS_NPC_LIST:
            self.loadBossDataUid(uniqueId)
            if self.bossData['AvatarType'] is None:
                self.bossData['AvatarType'] = avatarType
        elif avatarType:
            self.loadBossDataAvatarType(avatarType)
        else:
            raise KeyError('Unknown boss: %s' % uniqueId)

    def getBossData(self, key):
        bossData = getattr(self, 'bossData', None) or BOSS_NPC_LIST['']
        return bossData.get(key, BOSS_NPC_LIST[''].get(key))

    def getBossName(self):
        return self.bossData['Name']

    def getBossLevel(self):
        return self.bossData['Level']

    def getHpScale(self):
        return self.getBossData('HpScale')

    def getMpScale(self):
        return self.getBossData('MpScale')

    def getGoldScale(self):
        return self.getBossData('GoldScale')

    def getDamageScale(self):
        return self.getBossData('DamageScale')

    def getModelScale(self):
        return self.getBossData('ModelScale')

    def getBossSkills(self):
        return list(self.getBossData('Skills') or [])

    def getBossWeapons(self):
        weapon = self.getBossData('Weapon')
        if not weapon:
            return []

        weapons = EnemyGlobals.getEnemyWeapons(self.getAvatarType(), self.getLevel(),
            [weapon], self.getBossData('WeaponLevel'))

        return list(weapons.keys())

    def getMonsterDmg(self):
        return EnemyGlobals.getMonsterDmg(self.getLevel(), self.getDamageScale())

    def getAttackSkills(self):
        skills = list(EnemyGlobals.getBaseSkills(self.getAvatarType())[1])
        for skillId in self.getBossSkills():
            if skillId not in skills:
                skills.append(skillId)

        return skills
