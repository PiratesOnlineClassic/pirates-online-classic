# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesbase.Freebooter
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

NONE = 0
VELVET_ROPE = 1
FULL = 2
FreeLevelCap = 7
FreeOverallLevelCap = 25
FreeSkillCap = 3
FreeMaxSkillSpend = 6
FreeGuildRestrict = True
FreeExpNerf = 0.7
FreeNametagChange = True
AllAccessHoliday = False

def getPaidStatus(avId):
    av = base.cr.getDo(avId)
    if av:
        if AllAccessHoliday:
            return FULL
        else:
            return av.getGameAccess() == FULL
    return False


def getFounderStatus(avId):
    av = base.cr.getDo(avId)
    if av:
        return av.getFounder()
    return False


def getPaidStatusAI(playerID):
    playerOb = simbase.air.getDo(playerID)
    if playerOb:
        if AllAccessHoliday:
            return FULL
        return hasattr(playerOb, 'getGameAccess') and playerOb.getGameAccess() == FULL
    else:
        return NONE


def pruneFreebooterSkills(skillTrack):
    if getPaidStatus(base.localAvatar.getDoId()):
        return skillTrack
    else:
        return filter(lambda skillId: WeaponGlobals.canFreeUse(skillId), skillTrack)


def allowedFreebooterWeapon(repId):
    if repId == InventoryType.DaggerRep:
        return False
    else:
        if repId == InventoryType.GrenadeRep:
            return False
        else:
            if repId == InventoryType.WandRep:
                return False
            else:
                if repId == InventoryType.DollRep:
                    return True
                else:
                    return True
# okay decompiling .\pirates\piratesbase\Freebooter.pyc
