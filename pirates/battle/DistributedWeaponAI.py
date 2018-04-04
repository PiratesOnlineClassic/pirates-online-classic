
from pirates.battle.WeaponBaseAI import WeaponBaseAI
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedWeaponAI(WeaponBaseAI, DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWeaponAI')

    def __init__(self, air):
        WeaponBaseAI.__init__(self, air)
        DistributedInteractiveAI.__init__(self, air)


    # setMovie(uint8, uint32) broadcast ram

    def setMovie(self, movie, todo_uint32_1):
        self.sendUpdate('setMovie', [movie, todo_uint32_1])

    # doAIAttack(int32/10, int32/10, int32/10, uint32, SkillId, SkillId, int16) broadcast

    def doAIAttack(self, doAIAttack, todo_int32_10_1, todo_int32_10_2, todo_uint32_3, todo_SkillId_4, todo_SkillId_5, todo_int16_6):
        self.sendUpdate('doAIAttack', [doAIAttack, todo_int32_10_1, todo_int32_10_2, todo_uint32_3, todo_SkillId_4, todo_SkillId_5, todo_int16_6])


