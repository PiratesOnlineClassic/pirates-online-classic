from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

class BattleSkillDiaryAI:
    notify = directNotify.newCategory('BattleSkillDiaryAI')

    def __init__(self, air, av):
        self.air = air
        self.av = av

        # the skills are recorded per target, an avatar may fight many enemies
        # at once and is rewarded for each of them seperately once defeated...
        self.__targets = {}
        self.__targetSkills = {}
        self.__lastSkill = 0
        self.__currentSkill = 0

    def hasSkill(self, skillId, targetId=0):
        return skillId in self.__targets.get(targetId, {})

    def addSkill(self, timestamp, skillId, ammoSkillId, targetId=0):
        # the last skill used is always remembered, the reputation earned
        # with a skill is only reset once the target leaves the battle...
        if skillId != self.__currentSkill:
            self.__lastSkill = self.__currentSkill
            self.__currentSkill = skillId

        self.__targetSkills[targetId] = skillId
        skills = self.__targets.setdefault(targetId, {})
        if skillId in skills:
            return

        skills[skillId] = [ammoSkillId, timestamp, 0]

    def removeSkill(self, skillId, targetId=0):
        skills = self.__targets.get(targetId)
        if not skills or skillId not in skills:
            return

        del skills[skillId]

    def getSkill(self, skillId, targetId=0):
        if not self.hasSkill(skillId, targetId):
            return None

        return self.__targets[targetId][skillId]

    def getSkills(self, targetId=0):
        return self.__targets.get(targetId, {})

    def getLastSkill(self):
        return self.__lastSkill

    def getCurrentSkill(self, targetId=None):
        if targetId is not None:
            return self.__targetSkills.get(targetId, 0)

        return self.__currentSkill

    def clear(self, targetId=None):
        if targetId is not None:
            self.__targets.pop(targetId, None)
            self.__targetSkills.pop(targetId, None)
            return

        self.__targets = {}
        self.__targetSkills = {}
        self.__lastSkill = 0
        self.__currentSkill = 0
