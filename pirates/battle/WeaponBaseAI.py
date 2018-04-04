# NO BASE CLASSES WERE FOUND! 
 #THIS CLASS LIKELY HAD NO DEFINITION IN THE DCLASS FILES WHEN stub_generator.py WAS RUN!

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class WeaponBaseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('WeaponBaseAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # requestTargetedSkill(SkillId, SkillId, uint8, DoId, DoIdList, uint32, Pos, uint8) clsend airecv

    def requestTargetedSkill(self, requestTargetedSkill, todo_SkillId_1, todo_uint8_2, todo_DoId_3, todo_DoIdList_4, todo_uint32_5, todo_Pos_6, todo_uint8_7):
        pass

    # useTargetedSkill(SkillId, SkillId, uint8, DoId, DoIdList, SkillEffects, SkillEffects, SkillEffectsList, uint32, Pos, uint8) broadcast

    def useTargetedSkill(self, useTargetedSkill, todo_SkillId_1, todo_uint8_2, todo_DoId_3, todo_DoIdList_4, todo_SkillEffects_5, todo_SkillEffects_6, todo_SkillEffectsList_7, todo_uint32_8, todo_Pos_9, todo_uint8_10):
        self.sendUpdate('useTargetedSkill', [useTargetedSkill, todo_SkillId_1, todo_uint8_2, todo_DoId_3, todo_DoIdList_4, todo_SkillEffects_5, todo_SkillEffects_6, todo_SkillEffectsList_7, todo_uint32_8, todo_Pos_9, todo_uint8_10])

    # requestShipSkill(SkillId, SkillId, uint8, DoId, uint32) clsend airecv

    def requestShipSkill(self, requestShipSkill, todo_SkillId_1, todo_uint8_2, todo_DoId_3, todo_uint32_4):
        pass

    # useShipSkill(SkillId, SkillId, uint8, DoId, SkillEffects, ShipEffects, uint32) broadcast

    def useShipSkill(self, useShipSkill, todo_SkillId_1, todo_uint8_2, todo_DoId_3, todo_SkillEffects_4, todo_ShipEffects_5, todo_uint32_6):
        self.sendUpdate('useShipSkill', [useShipSkill, todo_SkillId_1, todo_uint8_2, todo_DoId_3, todo_SkillEffects_4, todo_ShipEffects_5, todo_uint32_6])

    # requestProjectileSkill(SkillId, SkillId, PosHpr, uint32, uint8) clsend airecv

    def requestProjectileSkill(self, requestProjectileSkill, todo_SkillId_1, todo_PosHpr_2, todo_uint32_3, todo_uint8_4):
        pass

    # useProjectileSkill(SkillId, SkillId, PosHpr, uint32, uint8) broadcast

    def useProjectileSkill(self, useProjectileSkill, todo_SkillId_1, todo_PosHpr_2, todo_uint32_3, todo_uint8_4):
        self.sendUpdate('useProjectileSkill', [useProjectileSkill, todo_SkillId_1, todo_PosHpr_2, todo_uint32_3, todo_uint8_4])

    # suggestProjectileSkillResult(SkillId, SkillId, uint8, DoId, DoIdList, Pos, Normal, uint8array, uint32) clsend airecv

    def suggestProjectileSkillResult(self, suggestProjectileSkillResult, todo_SkillId_1, todo_uint8_2, todo_DoId_3, todo_DoIdList_4, todo_Pos_5, todo_Normal_6, todo_uint8array_7, todo_uint32_8):
        pass

    # setProjectileSkillResult(SkillId, SkillId, uint8, DoId, DoIdList, SkillEffects, SkillEffects, SkillEffectsList, Pos, Normal, uint8array, DoId, uint32) broadcast

    def setProjectileSkillResult(self, projectileSkillResult, todo_SkillId_1, todo_uint8_2, todo_DoId_3, todo_DoIdList_4, todo_SkillEffects_5, todo_SkillEffects_6, todo_SkillEffectsList_7, todo_Pos_8, todo_Normal_9, todo_uint8array_10, todo_DoId_11, todo_uint32_12):
        self.sendUpdate('setProjectileSkillResult', [projectileSkillResult, todo_SkillId_1, todo_uint8_2, todo_DoId_3, todo_DoIdList_4, todo_SkillEffects_5, todo_SkillEffects_6, todo_SkillEffectsList_7, todo_Pos_8, todo_Normal_9, todo_uint8array_10, todo_DoId_11, todo_uint32_12])


