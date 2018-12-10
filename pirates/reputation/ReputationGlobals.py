from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType, InventoryId
from pirates.battle import WeaponGlobals
__categories = (InventoryType.GeneralRep, InventoryType.MeleeRep, InventoryType.CutlassRep, InventoryType.PistolRep, InventoryType.MusketRep, InventoryType.DaggerRep, InventoryType.GrenadeRep, InventoryType.DollRep, InventoryType.WandRep, InventoryType.KettleRep, InventoryType.CannonRep, InventoryType.SailingRep, InventoryType.LockpickRep)


def getReputationCategories():
    return __categories


def getUnspentCategories():
    start = InventoryType.begin_Unspent
    total = InventoryType.end_Unspent - start
    listCat = []
    for i in range(total):
        listCat.append(start + i)
    
    return listCat


ReputationNeededToLevel = [
    0,
    50,
    150,
    300,
    500,
    700,
    900,
    1100,
    1300,
    1500,
    1700,
    1900,
    2100,
    2300,
    2500,
    2700,
    2900,
    3200,
    3500,
    3800,
    4100,
    4400,
    4700,
    5000,
    5300,
    0]
GlobalReputationNeeded = [
    0,
    300,
    450,
    600,
    800,
    1000,
    1300,
    1600,
    2000,
    2400,
    2900,
    3400,
    4000,
    4600,
    5300,
    6000,
    6800,
    7600,
    8500,
    9400,
    10400,
    11400,
    12500,
    13600,
    14800,
    16100,
    17400,
    18800,
    20200,
    21700,
    23300,
    24900,
    26600,
    28400,
    30200,
    32100,
    34100,
    36100,
    38200,
    40400,
    42600,
    0]
LevelCap = 25
GlobalLevelCap = 40
TotalReputationAtLevel = []
GlobalReputationAtLevel = []


def __buildTotalReputationList():
    TotalReputationAtLevel.append(0)
    runningTotal = 0
    for rep in ReputationNeededToLevel:
        runningTotal += rep
        TotalReputationAtLevel.append(runningTotal)
    
    GlobalReputationAtLevel.append(0)
    runningTotal = 0
    for rep in GlobalReputationNeeded:
        runningTotal += rep
        GlobalReputationAtLevel.append(runningTotal)
    

__buildTotalReputationList()


def addReputation(category, origLevel, origValue, deltaValue):
    neededToLevel = getReputationNeededToLevel(category, origLevel)
    newLevel = origLevel
    newValue = origValue + deltaValue
    while newValue >= neededToLevel and newLevel + 1 <= LevelCap:
        newLevel += 1
        newValue -= neededToLevel
        neededToLevel = getReputationNeededToLevel(category, newLevel)
    if newLevel == LevelCap and category != InventoryType.GeneralRep:
        return (LevelCap, 0)
    else:
        return (newLevel, newValue)


def getTotalReputation(category, level, value = 0):
    if level >= LevelCap:
        return TotalReputationAtLevel[LevelCap]
    else:
        return TotalReputationAtLevel[level] + value


def getTotalGlobalReputation(category, level, value = 0):
    if level >= LevelCap:
        return GlobalReputationAtLevel[LevelCap]
    else:
        return GlobalReputationAtLevel[level] + value


def getLevelFromTotalReputation(category, totalRep):
    if category == InventoryType.OverallRep:
        data = GlobalReputationAtLevel
        level = -1
        for rep in data:
            if totalRep < rep:
                previousLevelRep = data[level]
                value = totalRep - previousLevelRep
                return (level, value)
            
            level += 1
        
        level = GlobalLevelCap
        value = 0
        return (level, value)
    else:
        data = TotalReputationAtLevel
        level = -1
        for rep in data:
            if totalRep < rep:
                previousLevelRep = data[level]
                value = totalRep - previousLevelRep
                return (level, value)
            
            level += 1
        
        level = LevelCap
        value = 0
        return (level, value)


def getReputationNeededToLevel(category, level):
    if category == InventoryType.OverallRep:
        if level > GlobalLevelCap:
            return None
        else:
            return GlobalReputationNeeded[level]
    elif level > LevelCap:
        return None
    else:
        return ReputationNeededToLevel[level]


MonsterRep = 1
RepIcons = {
    InventoryType.OverallRep: 'main_gui_game_gui_base',
    InventoryType.CutlassRep: 'icon_cutlass_rusty',
    InventoryType.PistolRep: 'icon_pistol_single',
    InventoryType.MusketRep: 'icon_pistol_single',
    InventoryType.DaggerRep: 'icon_dagger_small',
    InventoryType.GrenadeRep: 'icon_grenade',
    InventoryType.DollRep: 'icon_voodoo_doll_straw',
    InventoryType.WandRep: 'icon_staff_wood',
    InventoryType.CannonRep: 'icon_cannon',
    InventoryType.SailingRep: 'sail_full_sail'}
