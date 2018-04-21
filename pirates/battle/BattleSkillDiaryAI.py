from direct.distributed.ClockDelta import globalClockDelta
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

class BattleSkillDiaryAI:

    def __init__(self, air, av):
        self.air = air
        self.av = av

        self.__skills = {}
        self.__lastSkill = 0
        self.__currentSkill = 0

    def hasSkill(self, skillId):
        return skillId in self.__skills

    def addSkill(self, skillId, ammoSkillId):
        if skillId in self.__skills:
            return

        self.__skills[skillId] = [ammoSkillId, globalClockDelta.getRealNetworkTime(bits=32), 0]

        # store the last and current skill id's so that we can use them
        # later to determin the battle results in the battle mgr...
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

    def reset(self):
        self.__skills = {}
        self.__lastSkill = 0
        self.__currentSkill = 0
