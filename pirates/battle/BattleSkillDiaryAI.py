from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

class BattleSkillDiaryAI:
    notify = directNotify.newCategory('BattleSkillDiaryAI')

    def __init__(self, air, av):
        self.air = air
        self.av = av

        self.__skills = {}
        self.__lastSkill = 0
        self.__currentSkill = 0

    def hasSkill(self, skillId):
        return skillId in self.__skills

    def addSkill(self, timestamp, skillId, ammoSkillId):
        if skillId in self.__skills:
            return

        self.__skills[skillId] = [ammoSkillId, timestamp, 0]
        self.__lastSkill = self.__currentSkill
        self.__currentSkill = skillId

    def removeSkill(self, skillId):
        if skillId not in self.__skills:
            return

        del self.__skills[skillId]

    def getSkill(self, skillId):
        if not self.hasSkill(skillId):
            return None

        return self.__skills[skillId]

    def getSkills(self):
        return self.__skills

    def getLastSkill(self):
        return self.__lastSkill

    def getCurrentSkill(self):
        return self.__currentSkill

    def clear(self):
        self.__skills = {}
        self.__lastSkill = 0
        self.__currentSkill = 0
