class CrewStatus:
    ADMIRAL = 1
    CAPTAIN = 2
    MEMBER = 3


class GuildStatus:
    INVITED = -2
    APPLICANT = -1
    NOT_IN_GUILD = 0
    LEADER = 1
    MEMBER = 2


class GiftOrigin:
    _BEGIN_VALUE = 0
    MAGIC_WORD = 0
    COMBAT = 1
    LOCKPICK = 2
    NAVY_CREW = 3
    TREASURE_CHEST = 4
    BOSS = 5
    MERCHANT_SHIP = 6
    SKELETON_SHIP = 7
    NAVY_SHIP = 8
    PLAYER_SHIP = 9
    SEA_MONSTER = 10
    LEVEL_UP = 11
    HIGHSEAS_ADVENTURE = 12
    CARD_GAME = 13
    DICE_GAME = 14
    CANNON = 15
    FLAG_SHOP = 16
    SEARCHABLE_CONTAINER = 17
    HOLIDAY_OBJECT = 18
    _END_VALUE = HOLIDAY_OBJECT + 1


class TradeStatus:
    ACTIVE = 1
    APPROVED = 2
    DISAPPROVED = 3
    REMOVED = 3


class InventoryCategory:
    _BEGIN_CATEGORY = 0
    BAD_CATEGORY = 0
    MONEY = 1000
    WEAPONS = 1001
    INGREDIENTS = 1002
    CONSUMABLES = 1003
    SHIP_CANNONS = 1004
    QUEST_SLOTS = 1006
    MAX_PLAYER_ATTRIBUTES = 2000
    TELEPORT_ACCESS = 2002
    WEAPON_SKILL_MELEE = 3000
    WEAPON_SKILL_CUTLASS = 3001
    WEAPON_SKILL_PISTOL = 3002
    WEAPON_SKILL_MUSKET = 3003
    WEAPON_SKILL_DAGGER = 3004
    WEAPON_SKILL_GRENADE = 3005
    WEAPON_SKILL_DOLL = 3006
    WEAPON_SKILL_WAND = 3007
    WEAPON_SKILL_KETTLE = 3008
    WEAPON_SKILL_CANNON = 3009
    UNSPENT_SKILL_POINTS = 3010
    WEAPON_SKILL_ITEM = 3011
    SKILL_SAILING = 3012
    VITAE_PENALTY = 3013
    WEAPON_SKILL_BAYONET = 3014
    PLAYER_RANKING = 3015
    NUM_RESPEC = 4000
    KEY_ITEMS = 5010
    GAME_OUTCOMES = 5011
    TELEPORT_TOKENS = 5012
    PVP_RENOWN = 6000
    ACCUMULATORS = 7000
    REPAIR_TOKENS = 7001
    WEAPON_PISTOL_AMMO = 7002
    WEAPON_MUSKET_AMMO = 7003
    WEAPON_GRENADE_AMMO = 7004
    WEAPON_CANNON_AMMO = 7005
    WEAPON_DAGGER_AMMO = 7006
    PISTOL_POUCHES = 7100
    DAGGER_POUCHES = 7101
    GRENADE_POUCHES = 7102
    CANNON_POUCHES = 7103
    CLOTHING = 8000
    FURNITURE = 8001
    TREASURE_MAPS = 8002
    SHIP_MAINPARTS = 8003
    FISH_CAUGHT = 8004
    QUESTS = 8005
    SHIP_ACCESSORIES = 8006
    FLAGS = 8007
    COLLECTIONS = 8008
    SHIPS = 9000
    PETS = 9001
    WAGERS = 9002
    CARDS = 9500
    CLOTHING = 9501
    SONGS = 9502
    TRASH = 9999
    _END_CATEGORY = TRASH + 1


class InventoryType:
    begin_Money = 10000
    GoldInPocket = 10000
    GoldWagered = 10001
    end_Money = GoldWagered + 1
    begin_Weapon = 10100
    MeleeWeaponL1 = 10100
    MeleeWeaponL2 = 10101
    MeleeWeaponL3 = 10102
    CutlassWeaponL1 = 10103
    CutlassWeaponL2 = 10104
    CutlassWeaponL3 = 10105
    PistolWeaponL1 = 10106
    PistolWeaponL2 = 10107
    PistolWeaponL3 = 10108
    MusketWeaponL1 = 10109
    MusketWeaponL2 = 10110
    MusketWeaponL3 = 10111
    DaggerWeaponL1 = 10112
    DaggerWeaponL2 = 10113
    DaggerWeaponL3 = 10114
    GrenadeWeaponL1 = 10115
    GrenadeWeaponL2 = 10116
    GrenadeWeaponL3 = 10117
    DollWeaponL1 = 10118
    DollWeaponL2 = 10119
    DollWeaponL3 = 10120
    WandWeaponL1 = 10121
    WandWeaponL2 = 10122
    WandWeaponL3 = 10123
    KettleWeaponL1 = 10124
    KettleWeaponL2 = 10125
    KettleWeaponL3 = 10126
    MonsterWeaponL1 = 10127
    MonsterWeaponL2 = 10128
    MonsterWeaponL3 = 10129
    MonsterWeaponL4 = 10130
    MonsterWeaponL5 = 10131
    BayonetWeaponL1 = 10132
    BayonetWeaponL2 = 10133
    BayonetWeaponL3 = 10134
    MeleeWeaponL4 = 10135
    MeleeWeaponL5 = 10136
    MeleeWeaponL6 = 10137
    CutlassWeaponL4 = 10138
    CutlassWeaponL5 = 10139
    CutlassWeaponL6 = 10140
    PistolWeaponL4 = 10141
    PistolWeaponL5 = 10142
    PistolWeaponL6 = 10143
    DaggerWeaponL4 = 10144
    DaggerWeaponL5 = 10145
    DaggerWeaponL6 = 10146
    GrenadeWeaponL4 = 10147
    GrenadeWeaponL5 = 10148
    GrenadeWeaponL6 = 10149
    DollWeaponL4 = 10150
    DollWeaponL5 = 10151
    DollWeaponL6 = 10152
    WandWeaponL4 = 10153
    WandWeaponL5 = 10154
    WandWeaponL6 = 10155
    DualCutlassL1 = 10156
    FoilL1 = 10157
    end_Weapon = FoilL1 + 1
    begin_Ingredient = 11000
    AppleIngredient = 11000
    end_Ingredient = AppleIngredient + 1
    begin_ShipCannon = 11100
    CannonL1 = 11100
    CannonL2 = 11101
    CannonL3 = 11102
    CannonL4 = 11103
    end_ShipCannon = CannonL4 + 1
    begin_Consumables = 11200
    Potion1 = 11200
    Potion2 = 11201
    Potion3 = 11202
    Potion4 = 11203
    Potion5 = 11204
    ShipRepairKit = 11205
    PorkChunk = 11206
    end_Consumables = PorkChunk + 1
    Potions = (Potion1, Potion2, Potion3, Potion4, Potion5, PorkChunk)
    begin_MaxPlayerAttribute = 11400
    Hp = 11400
    Mojo = 11401
    end_MaxPlayerAttribute = Mojo + 1
    begin_TeleportAccess = 11600
    TeleportHome = 11600
    TeleportGuildIsland = 11601
    end_TeleportAccess = TeleportGuildIsland + 1
    begin_WeaponSkillMelee = 12000
    MeleePunch = 12000
    MeleeJab = 12001
    MeleeKick = 12002
    MeleeRoundhouse = 12003
    MeleeHeadbutt = 12004
    MeleeHaymaker = 12005
    MeleeThrowDirt = 12006
    MeleeToughness = 12007
    MeleeIronSkin = 12008
    MeleeDetermination = 12009
    end_WeaponSkillMelee = MeleeDetermination + 1
    begin_WeaponSkillCutlass = 12100
    CutlassHack = 12100
    CutlassSlash = 12101
    CutlassCleave = 12102
    CutlassFlourish = 12103
    CutlassStab = 12104
    CutlassParry = 12105
    CutlassEndurance = 12106
    CutlassSweep = 12107
    CutlassBrawl = 12108
    CutlassTaunt = 12109
    CutlassBladestorm = 12110
    end_WeaponSkillCutlass = CutlassBladestorm + 1
    begin_WeaponSkillPistol = 12200
    PistolShoot = 12200
    PistolLeadShot = 12201
    PistolVenomShot = 12202
    PistolBaneShot = 12203
    PistolHexEaterShot = 12204
    PistolSilverShot = 12205
    PistolSteelShot = 12206
    PistolSharpShooter = 12207
    PistolDodge = 12208
    PistolEagleEye = 12209
    PistolTakeAim = 12210
    end_WeaponSkillPistol = PistolTakeAim + 1
    begin_WeaponSkillMusket = 12300
    MusketShoot = 12300
    MusketTakeAim = 12301
    MusketDeadeye = 12302
    MusketEagleEye = 12303
    MusketCrackShot = 12304
    MusketMarksman = 12305
    MusketLeadShot = 12306
    MusketScatterShot = 12307
    MusketCursedShot = 12308
    MusketCoalfireShot = 12309
    MusketHeavySlug = 12310
    MusketExploderShot = 12311
    end_WeaponSkillMusket = MusketExploderShot + 1
    begin_WeaponSkillDagger = 12400
    DaggerCut = 12400
    DaggerSwipe = 12401
    DaggerGouge = 12402
    DaggerEviscerate = 12403
    DaggerFinesse = 12404
    DaggerBladeInstinct = 12405
    DaggerAsp = 12406
    DaggerAdder = 12407
    DaggerThrowDirt = 12408
    DaggerSidewinder = 12409
    DaggerViperNest = 12410
    end_WeaponSkillDagger = DaggerViperNest + 1
    begin_WeaponSkillGrenade = 12500
    GrenadeThrow = 12500
    GrenadeExplosion = 12501
    GrenadeShockBomb = 12502
    GrenadeFireBomb = 12503
    GrenadeSmokeCloud = 12504
    GrenadeSiege = 12505
    GrenadeLongVolley = 12506
    GrenadeDetermination = 12507
    GrenadeDemolitions = 12508
    GrenadeToughness = 12509
    GrenadeIgnorePain = 12510
    end_WeaponSkillGrenade = GrenadeIgnorePain + 1
    begin_WeaponSkillDoll = 12600
    DollAttune = 12600
    DollPoke = 12601
    DollSwarm = 12602
    DollHeal = 12603
    DollCurse = 12604
    DollBurn = 12605
    DollCure = 12606
    DollShackles = 12607
    DollLifeDrain = 12608
    DollFocus = 12609
    DollSpiritWard = 12610
    end_WeaponSkillDoll = DollSpiritWard + 1
    begin_SkillSailing = 12650
    SailBroadsideLeft = 12650
    SailBroadsideRight = 12651
    SailFullSail = 12652
    SailComeAbout = 12653
    SailOpenFire = 12654
    SailRammingSpeed = 12655
    SailTakeCover = 12656
    SailWindcatcher = 12657
    SailTacking = 12658
    SailTreasureSense = 12659
    SailTaskmaster = 12660
    SailPowerRecharge = 12661
    end_SkillSailing = SailPowerRecharge + 1
    begin_WeaponSkillWand = 12700
    StaffBlast = 12700
    StaffSoulFlay = 12701
    StaffPestilence = 12702
    StaffWither = 12703
    StaffHellfire = 12704
    StaffBanish = 12705
    StaffDesolation = 12706
    StaffConcentration = 12707
    StaffSpiritLore = 12708
    StaffConservation = 12709
    StaffSpiritMastery = 12710
    end_WeaponSkillWand = StaffSpiritMastery + 1
    begin_WeaponSkillKettle = 12800
    end_WeaponSkillKettle = 12800
    begin_WeaponSkillCannon = 12900
    CannonShoot = 12900
    CannonRoundShot = 12901
    CannonChainShot = 12902
    CannonGrapeShot = 12903
    CannonFirebrand = 12904
    CannonThunderbolt = 12905
    CannonExplosive = 12906
    CannonFury = 12907
    CannonGrappleHook = 12908
    CannonRapidReload = 12909
    CannonBarrage = 12910
    CannonShrapnel = 12911
    end_WeaponSkillCannon = CannonShrapnel + 1
    CannonBullet = 12913
    CannonGasCloud = 12914
    CannonSkull = 12915
    CannonFlamingSkull = 12916
    CannonFlameCloud = 12917
    CannonBarShot = 12918
    CannonKnives = 12919
    CannonMine = 12920
    CannonBarnacles = 12921
    CannonComet = 12922
    end_ExtendedWeaponSkillCannon = CannonComet + 1
    begin_WeaponSkillItem = 13000
    UseItem = 13000
    end_WeaponSkillItem = UseItem + 1
    begin_WeaponSkillBayonet = 13100
    BayonetShoot = 13100
    BayonetStab = 13101
    BayonetRush = 13102
    BayonetBash = 13103
    end_WeaponSkillBayonet = BayonetBash + 1
    BackstabSkills = (DaggerCut, DaggerSwipe, DaggerGouge, DaggerEviscerate)
    StartingSkills = [
        CutlassHack,
        CutlassSlash,
        SailBroadsideLeft,
        SailBroadsideRight,
        DaggerCut,
        DaggerSwipe,
        StaffBlast,
        StaffSoulFlay,
        GrenadeThrow,
        GrenadeExplosion,
        PistolShoot,
        PistolLeadShot,
        DollAttune,
        DollPoke,
        CannonShoot,
        CannonRoundShot]
    DontResetSkills = [
        SailPowerRecharge,
        CannonGrappleHook]
    begin_NumRespec = 13200
    NumRespecCutlass = 13200
    NumRespecPistol = 13201
    NumRespecDoll = 13202
    NumRespecDagger = 13203
    NumRespecGrenade = 13204
    NumRespecStaff = 13205
    NumRespecCannon = 13206
    NumRespecSailing = 13207
    end_NumRespec = NumRespecSailing + 1
    begin_KeyItem = 13400
    Dinghy = 13400
    NewPlayerToken = 13401
    NewShipToken = 13402
    NewWeaponToken = 13403
    SmallBottle = 13404
    MediumBottle = 13405
    LargeBottle = 13406
    CutlassToken = 13407
    PistolToken = 13408
    MusketToken = 13409
    DaggerToken = 13410
    GrenadeToken = 13411
    WandToken = 13412
    DollToken = 13413
    KettleToken = 13414
    FirstDeathToken = 13420
    end_KeyItem = FirstDeathToken + 1
    begin_TeleportToken = 13500
    TortugaTeleportToken = 13500
    PortRoyalTeleportToken = 13501
    KingsheadTeleportToken = 13502
    PadresDelFuegoTeleportToken = 13503
    CubaTeleportToken = 13504
    end_TeleportToken = CubaTeleportToken + 1
    __islandToTeleportTokenMap = {
        '1156207188.95dzlu': TortugaTeleportToken,
        '1150922126.8dzlu': PortRoyalTeleportToken,
        '1159933206.48sdnaik': KingsheadTeleportToken,
        '1142018473.22dxschafe': PadresDelFuegoTeleportToken,
        '1160614528.73sdnaik': CubaTeleportToken}

    @classmethod
    def getIslandTeleportToken(cls, islandUid):
        return cls.__islandToTeleportTokenMap.get(islandUid)

    @classmethod
    def getIslandUidFromTeleportToken(cls, token):
        for key in list(cls.__islandToTeleportTokenMap.keys()):
            if cls.__islandToTeleportTokenMap[key] == token:
                return key
        
        return ''

    begin_QuestSlot = 13600
    OpenQuestSlot = 13600
    end_QuestSlot = OpenQuestSlot + 1
    begin_Accumulator = 13700
    OverallRep = 13700
    GeneralRep = 13701
    MeleeRep = 13702
    CutlassRep = 13703
    PistolRep = 13704
    MusketRep = 13705
    DaggerRep = 13706
    GrenadeRep = 13707
    WandRep = 13708
    DollRep = 13709
    KettleRep = 13710
    CannonRep = 13711
    SailingRep = 13712
    MonsterRep = 13713
    LockpickRep = 13714
    GamblingRep = 13715
    end_Accumulator = GamblingRep + 1
    begin_Unspent = 13750
    UnspentMelee = 13750
    UnspentCutlass = 13751
    UnspentPistol = 13752
    UnspentMusket = 13753
    UnspentDagger = 13754
    UnspentGrenade = 13755
    UnspentWand = 13756
    UnspentDoll = 13757
    UnspentKettle = 13758
    UnspentCannon = 13759
    UnspentSailing = 13760
    end_Unspent = UnspentSailing + 1
    begin_Vitae = 13790
    Vitae_Level = 13790
    Vitae_Cost = 13791
    Vitae_Left = 13792
    Vitae_Update = 13793
    end_Vitae = Vitae_Update + 1
    begin_RepairTokens = 13800
    ShipRepairToken = 13800
    PlayerHealToken = 13801
    PlayerMojoHealToken = 13802
    end_RepairTokens = PlayerMojoHealToken + 1
    begin_PvPRenown = 13850
    PvPRenownLand = 13850
    PvPPointsLand = 13851
    PvPRenownSea = 13852
    PvPPointsSea = 13853
    end_PvPRenown = PvPPointsSea + 1
    begin_WeaponPistolAmmo = 13900
    AmmoLeadShot = 13900
    AmmoVenomShot = 13901
    AmmoBaneShot = 13902
    AmmoHexEaterShot = 13903
    AmmoSilverShot = 13904
    AmmoSteelShot = 13905
    end_WeaponPistolAmmo = AmmoSteelShot + 1
    begin_WeaponMusketAmmo = 14000
    AmmoScatterShot = 14000
    AmmoCursedShot = 14001
    AmmoCoalfireShot = 14002
    AmmoHeavySlug = 14003
    AmmoExploderShot = 14004
    end_WeaponMusketAmmo = AmmoExploderShot + 1
    begin_WeaponGrenadeAmmo = 14100
    AmmoGrenadeExplosion = 14100
    AmmoGrenadeShockBomb = 14101
    AmmoGrenadeFlame = 14102
    AmmoGrenadeSmoke = 14103
    AmmoGrenadeLandMine = 14104
    AmmoGrenadeSiege = 14105
    end_WeaponGrenadeAmmo = AmmoGrenadeSiege + 1
    begin_WeaponCannonAmmo = 14200
    AmmoRoundShot = 14200
    AmmoChainShot = 14201
    AmmoGrapeShot = 14202
    AmmoFirebrand = 14203
    AmmoThunderbolt = 14204
    AmmoExplosive = 14205
    AmmoFury = 14206
    AmmoGrappleHook = 14207
    AmmoBullet = 14208
    AmmoGasCloud = 14209
    AmmoSkull = 14210
    AmmoFlameCloud = 14211
    AmmoFlamingSkull = 14212
    AmmoBarShot = 14213
    AmmoKnives = 14214
    AmmoMine = 14215
    AmmoBarnacles = 14216
    AmmoComet = 14217
    end_WeaponCannonAmmo = AmmoComet + 1
    begin_WeaponDaggerAmmo = 14300
    AmmoAsp = 14300
    AmmoAdder = 14301
    AmmoSidewinder = 14302
    AmmoViperNest = 14303
    end_WeaponDaggerAmmo = AmmoViperNest + 1
    begin_PistolPouches = 14400
    PistolPouchL1 = 14400
    PistolPouchL2 = 14401
    PistolPouchL3 = 14402
    end_PistolPouches = PistolPouchL3 + 1
    begin_DaggerPouches = 14500
    DaggerPouchL1 = 14500
    DaggerPouchL2 = 14501
    DaggerPouchL3 = 14502
    end_DaggerPouches = DaggerPouchL3 + 1
    begin_GrenadePouches = 14600
    GrenadePouchL1 = 14600
    GrenadePouchL2 = 14601
    GrenadePouchL3 = 14602
    end_GrenadePouches = GrenadePouchL3 + 1
    begin_CannonPouches = 14700
    CannonPouchL1 = 14700
    CannonPouchL2 = 14701
    CannonPouchL3 = 14702
    end_CannonPouches = CannonPouchL3 + 1
    Clothing = 14999
    begin_Collections = 15000
    Collection_Set1 = 15000
    Collection_Set1_Part1 = 15001
    Collection_Set1_Part2 = 15002
    Collection_Set1_Part3 = 15003
    Collection_Set1_Part4 = 15004
    Collection_Set1_Part5 = 15005
    Collection_Set1_Part6 = 15006
    Collection_Set1_Part7 = 15007
    Collection_Set1_Part8 = 15008
    Collection_Set1_Part9 = 15009
    Collection_Set1_Part10 = 15010
    Collection_Set1_Part11 = 15011
    Collection_Set1_Part12 = 15012
    Collection_Set1_Part13 = 15013
    Collection_Set1_Part14 = 15014
    Collection_Set1_Part15 = 15015
    Collection_Set1_Part16 = 15016
    Collection_Set1_Part17 = 15017
    Collection_Set1_Part18 = 15018
    Collection_Set1_Part19 = 15019
    Collection_Set1_Part20 = 15020
    Collection_Set2 = 15030
    Collection_Set2_Part1 = 15031
    Collection_Set2_Part2 = 15032
    Collection_Set2_Part3 = 15033
    Collection_Set2_Part4 = 15034
    Collection_Set2_Part5 = 15035
    Collection_Set2_Part6 = 15036
    Collection_Set2_Part7 = 15037
    Collection_Set2_Part8 = 15038
    Collection_Set2_Part9 = 15039
    Collection_Set2_Part10 = 15040
    Collection_Set2_Part11 = 15041
    Collection_Set2_Part12 = 15042
    Collection_Set2_Part13 = 15043
    Collection_Set2_Part14 = 15044
    Collection_Set2_Part15 = 15045
    Collection_Set2_Part16 = 15046
    Collection_Set2_Part17 = 15047
    Collection_Set2_Part18 = 15048
    Collection_Set2_Part19 = 15049
    Collection_Set2_Part20 = 15050
    Collection_Set3 = 15060
    Collection_Set3_Part1 = 15061
    Collection_Set3_Part2 = 15062
    Collection_Set3_Part3 = 15063
    Collection_Set3_Part4 = 15064
    Collection_Set3_Part5 = 15065
    Collection_Set3_Part6 = 15066
    Collection_Set3_Part7 = 15067
    Collection_Set3_Part8 = 15068
    Collection_Set3_Part9 = 15069
    Collection_Set4 = 15090
    Collection_Set4_Part1 = 15091
    Collection_Set4_Part2 = 15092
    Collection_Set4_Part3 = 15093
    Collection_Set4_Part4 = 15094
    Collection_Set4_Part5 = 15095
    Collection_Set4_Part6 = 15096
    Collection_Set4_Part7 = 15097
    Collection_Set4_Part8 = 15098
    Collection_Set4_Part9 = 15099
    Collection_Set4_Part10 = 15100
    Collection_Set4_Part11 = 15101
    Collection_Set4_Part12 = 15102
    Collection_Set4_Part13 = 15103
    Collection_Set4_Part14 = 15104
    Collection_Set4_Part15 = 15105
    Collection_Set4_Part16 = 15106
    Collection_Set4_Part17 = 15107
    Collection_Set4_Part18 = 15108
    Collection_Set4_Part19 = 15109
    Collection_Set4_Part20 = 15110
    Collection_Set5 = 15120
    Collection_Set5_Part1 = 15121
    Collection_Set5_Part2 = 15122
    Collection_Set5_Part3 = 15123
    Collection_Set5_Part4 = 15124
    Collection_Set5_Part5 = 15125
    Collection_Set5_Part6 = 15126
    Collection_Set5_Part7 = 15127
    Collection_Set6 = 15150
    Collection_Set6_Part1 = 15151
    Collection_Set6_Part2 = 15152
    Collection_Set6_Part3 = 15153
    Collection_Set6_Part4 = 15154
    Collection_Set6_Part5 = 15155
    Collection_Set6_Part6 = 15156
    Collection_Set6_Part7 = 15157
    Collection_Set6_Part8 = 15158
    Collection_Set6_Part9 = 15159
    Collection_Set6_Part10 = 15160
    Collection_Set6_Part11 = 15161
    Collection_Set7 = 15180
    Collection_Set7_Part1 = 15181
    Collection_Set7_Part2 = 15182
    Collection_Set7_Part3 = 15183
    Collection_Set7_Part4 = 15184
    Collection_Set7_Part5 = 15185
    Collection_Set7_Part6 = 15186
    Collection_Set7_Part7 = 15187
    Collection_Set7_Part8 = 15188
    Collection_Set7_Part9 = 15189
    Collection_Set7_Part10 = 15190
    Collection_Set7_Part11 = 15191
    Collection_Set7_Part12 = 15192
    Collection_Set8 = 15210
    Collection_Set8_Part1 = 15211
    Collection_Set8_Part2 = 15212
    Collection_Set8_Part3 = 15213
    Collection_Set8_Part4 = 15214
    Collection_Set8_Part5 = 15215
    Collection_Set8_Part6 = 15216
    Collection_Set8_Part7 = 15217
    Collection_Set8_Part8 = 15218
    Collection_Set8_Part9 = 15219
    Collection_Set8_Part10 = 15220
    Collection_Set8_Part11 = 15221
    Collection_Set8_Part12 = 15222
    Collection_Set8_Part13 = 15223
    Collection_Set8_Part14 = 15224
    Collection_Set8_Part15 = 15225
    Collection_Set9 = 15230
    Collection_Set9_Part1 = 15231
    Collection_Set9_Part2 = 15232
    Collection_Set9_Part3 = 15233
    Collection_Set9_Part4 = 15234
    Collection_Set9_Part5 = 15235
    Collection_Set9_Part6 = 15236
    Collection_Set9_Part7 = 15237
    Collection_Set9_Part8 = 15238
    Collection_Set9_Part9 = 15239
    Collection_Set9_Part10 = 15240
    Collection_Set9_Part11 = 15241
    Collection_Set9_Part12 = 15242
    Collection_Set10 = 15243
    end_Collections = Collection_Set10 + 1
    Collection_Sets = (Collection_Set1, Collection_Set2, Collection_Set3, Collection_Set4, Collection_Set5, Collection_Set6, Collection_Set7, Collection_Set8, Collection_Set9)
    UberDogRev = 15999
    begin_RankingCategories = 16000
    begin_PVPCategories = 16000
    CTFGame = 16001
    CTLGame = 16002
    PTRGame = 16003
    BTLGame = 16004
    TBTGame = 16005
    SBTGame = 16006
    ARMGame = 16007
    end_PVPCategories = 16008
    TKPGame = 16009
    BTBGame = 16010
    PokerGame = 16011
    BlackjackGame = 16012
    ShipPVPRank = 16013
    PVPTotalInfamyLand = 16014
    PVPCurrentInfamy = 16015
    PVPTotalInfamySea = 16016
    end_RankingCategories = PVPTotalInfamySea + 1
    begin_Cards = 17000
    TwoOfHearts = begin_Cards
    ThreeOfHearts = begin_Cards + 1
    FourOfHearts = begin_Cards + 2
    FiveOfHearts = begin_Cards + 3
    SixOfHearts = begin_Cards + 4
    SevenOfHearts = begin_Cards + 5
    EightOfHearts = begin_Cards + 6
    NineOfHearts = begin_Cards + 7
    TenOfHearts = begin_Cards + 8
    JackOfHearts = begin_Cards + 9
    QueenOfHearts = begin_Cards + 10
    KingOfHearts = begin_Cards + 11
    AceOfHearts = begin_Cards + 12
    TwoOfDiamonds = begin_Cards + 13
    ThreeOfDiamonds = begin_Cards + 14
    FourOfDiamonds = begin_Cards + 15
    FiveOfDiamonds = begin_Cards + 16
    SixOfDiamonds = begin_Cards + 17
    SevenOfDiamonds = begin_Cards + 18
    EightOfDiamonds = begin_Cards + 19
    NineOfDiamonds = begin_Cards + 20
    TenOfDiamonds = begin_Cards + 21
    JackOfDiamonds = begin_Cards + 22
    QueenOfDiamonds = begin_Cards + 23
    KingOfDiamonds = begin_Cards + 24
    AceOfDiamonds = begin_Cards + 25
    TwoOfClubs = begin_Cards + 26
    ThreeOfClubs = begin_Cards + 27
    FourOfClubs = begin_Cards + 28
    FiveOfClubs = begin_Cards + 29
    SixOfClubs = begin_Cards + 30
    SevenOfClubs = begin_Cards + 31
    EightOfClubs = begin_Cards + 32
    NineOfClubs = begin_Cards + 33
    TenOfClubs = begin_Cards + 34
    JackOfClubs = begin_Cards + 35
    QueenOfClubs = begin_Cards + 36
    KingOfClubs = begin_Cards + 37
    AceOfClubs = begin_Cards + 38
    TwoOfSpades = begin_Cards + 39
    ThreeOfSpades = begin_Cards + 40
    FourOfSpades = begin_Cards + 41
    FiveOfSpades = begin_Cards + 42
    SixOfSpades = begin_Cards + 43
    SevenOfSpades = begin_Cards + 44
    EightOfSpades = begin_Cards + 45
    NineOfSpades = begin_Cards + 46
    TenOfSpades = begin_Cards + 47
    JackOfSpades = begin_Cards + 48
    QueenOfSpades = begin_Cards + 49
    KingOfSpades = begin_Cards + 50
    AceOfSpades = begin_Cards + 51
    end_Cards = AceOfSpades + 1
    begin_Songs = 18001
    Song_1 = begin_Songs
    Song_2 = begin_Songs + 1
    Song_3 = begin_Songs + 2
    Song_4 = begin_Songs + 3
    Song_5 = begin_Songs + 4
    Song_6 = begin_Songs + 5
    Song_7 = begin_Songs + 6
    Song_8 = begin_Songs + 7
    Song_9 = begin_Songs + 8
    Song_10 = begin_Songs + 9
    Song_11 = begin_Songs + 10
    Song_12 = begin_Songs + 11
    Song_13 = begin_Songs + 12
    Song_14 = begin_Songs + 13
    Song_15 = begin_Songs + 14
    Song_16 = begin_Songs + 15
    Song_17 = begin_Songs + 16
    Song_18 = begin_Songs + 17
    Song_19 = begin_Songs + 18
    Song_20 = begin_Songs + 19
    end_Songs = Song_20 + 1
    end_InventoryTypeOrCategory = 32768


__weaponId2SkillCategory = {
    InventoryType.MeleeWeaponL1: InventoryCategory.WEAPON_SKILL_MELEE,
    InventoryType.MeleeWeaponL2: InventoryCategory.WEAPON_SKILL_MELEE,
    InventoryType.MeleeWeaponL3: InventoryCategory.WEAPON_SKILL_MELEE,
    InventoryType.MeleeWeaponL4: InventoryCategory.WEAPON_SKILL_MELEE,
    InventoryType.MeleeWeaponL5: InventoryCategory.WEAPON_SKILL_MELEE,
    InventoryType.MeleeWeaponL6: InventoryCategory.WEAPON_SKILL_MELEE,
    InventoryType.CutlassWeaponL1: InventoryCategory.WEAPON_SKILL_CUTLASS,
    InventoryType.CutlassWeaponL2: InventoryCategory.WEAPON_SKILL_CUTLASS,
    InventoryType.CutlassWeaponL3: InventoryCategory.WEAPON_SKILL_CUTLASS,
    InventoryType.CutlassWeaponL4: InventoryCategory.WEAPON_SKILL_CUTLASS,
    InventoryType.CutlassWeaponL5: InventoryCategory.WEAPON_SKILL_CUTLASS,
    InventoryType.CutlassWeaponL6: InventoryCategory.WEAPON_SKILL_CUTLASS,
    InventoryType.PistolWeaponL1: InventoryCategory.WEAPON_SKILL_PISTOL,
    InventoryType.PistolWeaponL2: InventoryCategory.WEAPON_SKILL_PISTOL,
    InventoryType.PistolWeaponL3: InventoryCategory.WEAPON_SKILL_PISTOL,
    InventoryType.PistolWeaponL4: InventoryCategory.WEAPON_SKILL_PISTOL,
    InventoryType.PistolWeaponL5: InventoryCategory.WEAPON_SKILL_PISTOL,
    InventoryType.PistolWeaponL6: InventoryCategory.WEAPON_SKILL_PISTOL,
    InventoryType.MusketWeaponL1: InventoryCategory.WEAPON_SKILL_MUSKET,
    InventoryType.MusketWeaponL2: InventoryCategory.WEAPON_SKILL_MUSKET,
    InventoryType.MusketWeaponL3: InventoryCategory.WEAPON_SKILL_MUSKET,
    InventoryType.BayonetWeaponL1: InventoryCategory.WEAPON_SKILL_MUSKET,
    InventoryType.BayonetWeaponL2: InventoryCategory.WEAPON_SKILL_MUSKET,
    InventoryType.BayonetWeaponL3: InventoryCategory.WEAPON_SKILL_MUSKET,
    InventoryType.DaggerWeaponL1: InventoryCategory.WEAPON_SKILL_DAGGER,
    InventoryType.DaggerWeaponL2: InventoryCategory.WEAPON_SKILL_DAGGER,
    InventoryType.DaggerWeaponL3: InventoryCategory.WEAPON_SKILL_DAGGER,
    InventoryType.DaggerWeaponL4: InventoryCategory.WEAPON_SKILL_DAGGER,
    InventoryType.DaggerWeaponL5: InventoryCategory.WEAPON_SKILL_DAGGER,
    InventoryType.DaggerWeaponL6: InventoryCategory.WEAPON_SKILL_DAGGER,
    InventoryType.GrenadeWeaponL1: InventoryCategory.WEAPON_SKILL_GRENADE,
    InventoryType.GrenadeWeaponL2: InventoryCategory.WEAPON_SKILL_GRENADE,
    InventoryType.GrenadeWeaponL3: InventoryCategory.WEAPON_SKILL_GRENADE,
    InventoryType.GrenadeWeaponL4: InventoryCategory.WEAPON_SKILL_GRENADE,
    InventoryType.GrenadeWeaponL5: InventoryCategory.WEAPON_SKILL_GRENADE,
    InventoryType.GrenadeWeaponL6: InventoryCategory.WEAPON_SKILL_GRENADE,
    InventoryType.WandWeaponL1: InventoryCategory.WEAPON_SKILL_WAND,
    InventoryType.WandWeaponL2: InventoryCategory.WEAPON_SKILL_WAND,
    InventoryType.WandWeaponL3: InventoryCategory.WEAPON_SKILL_WAND,
    InventoryType.WandWeaponL4: InventoryCategory.WEAPON_SKILL_WAND,
    InventoryType.WandWeaponL5: InventoryCategory.WEAPON_SKILL_WAND,
    InventoryType.WandWeaponL6: InventoryCategory.WEAPON_SKILL_WAND,
    InventoryType.DollWeaponL1: InventoryCategory.WEAPON_SKILL_DOLL,
    InventoryType.DollWeaponL2: InventoryCategory.WEAPON_SKILL_DOLL,
    InventoryType.DollWeaponL3: InventoryCategory.WEAPON_SKILL_DOLL,
    InventoryType.DollWeaponL4: InventoryCategory.WEAPON_SKILL_DOLL,
    InventoryType.DollWeaponL5: InventoryCategory.WEAPON_SKILL_DOLL,
    InventoryType.DollWeaponL6: InventoryCategory.WEAPON_SKILL_DOLL,
    InventoryType.KettleWeaponL1: InventoryCategory.WEAPON_SKILL_KETTLE,
    InventoryType.KettleWeaponL2: InventoryCategory.WEAPON_SKILL_KETTLE,
    InventoryType.KettleWeaponL3: InventoryCategory.WEAPON_SKILL_KETTLE}


def getSkillCategory(weaponId):
    return __weaponId2SkillCategory.get(weaponId)


__skillRepToNumRespec = {
    InventoryType.CutlassRep: InventoryType.NumRespecCutlass,
    InventoryType.PistolRep: InventoryType.NumRespecPistol,
    InventoryType.DollRep: InventoryType.NumRespecDoll,
    InventoryType.DaggerRep: InventoryType.NumRespecDagger,
    InventoryType.GrenadeRep: InventoryType.NumRespecGrenade,
    InventoryType.WandRep: InventoryType.NumRespecStaff,
    InventoryType.CannonRep: InventoryType.NumRespecCannon,
    InventoryType.SailingRep: InventoryType.NumRespecSailing}


def getNumRespecType(weaponRep):
    return __skillRepToNumRespec.get(weaponRep)


class InventoryId:
    CATEGORY = 1
    BOOLEAN = 2
    STACK = 4
    ACCUMULATOR = 8
    DO_ID = 16
    PERCENT_CHANGE = 32
    MIN_CHANGE = 64
    TWO_WAY_TRADE = 256
    FREE_GIVE = 512
    FREE_TAKE = 1024
    AUTO_LOCATION = 4096
    AUTO_OWNER = 8192
    SPECIAL = 16384
    IS_LIMIT_CHANGE = 32768
    TWO_WAY_TRADE_STACK = TWO_WAY_TRADE | STACK
    FREE_GIVE_STACK = FREE_GIVE | STACK
    FREE_TAKE_STACK = FREE_TAKE | STACK
    ACCUMULATOR_CATEGORY = ACCUMULATOR | CATEGORY
    TWO_WAY_TRADE_CATEGORY = TWO_WAY_TRADE_STACK | CATEGORY
    FREE_GIVE_CATEGORY = TWO_WAY_TRADE_STACK | CATEGORY
    FREE_TAKE_CATEGORY = TWO_WAY_TRADE_STACK | CATEGORY
    STACKABLE_CATEGORY = STACK | CATEGORY
    AUTO_LOCATION_DO_ID = AUTO_LOCATION | DO_ID | CATEGORY
    AUTO_OWNER_DO_ID = AUTO_OWNER | DO_ID | CATEGORY
    DO_ID_CATEGORY = DO_ID | CATEGORY
    idFlags = {}
    idFlags[InventoryCategory.BAD_CATEGORY] = (0, 0)
    idFlags[InventoryCategory.MONEY] = (0, TWO_WAY_TRADE_CATEGORY)
    MoneyStack = (InventoryCategory.MONEY, TWO_WAY_TRADE_STACK)
    idFlags[InventoryType.GoldInPocket] = MoneyStack
    idFlags[InventoryType.GoldWagered] = MoneyStack
    idFlags[InventoryCategory.WEAPONS] = (0, TWO_WAY_TRADE_CATEGORY)
    WeaponStack = (InventoryCategory.WEAPONS, TWO_WAY_TRADE_STACK)
    for i in range(InventoryType.begin_Weapon, InventoryType.end_Weapon):
        idFlags[i] = WeaponStack
    
    idFlags[InventoryCategory.INGREDIENTS] = (0, TWO_WAY_TRADE_CATEGORY)
    IngredientStack = (InventoryCategory.INGREDIENTS, TWO_WAY_TRADE_STACK)
    for i in range(InventoryType.begin_Ingredient, InventoryType.end_Ingredient):
        idFlags[i] = IngredientStack
    
    idFlags[InventoryCategory.SHIP_CANNONS] = (0, TWO_WAY_TRADE_CATEGORY)
    ShipCannonStack = (InventoryCategory.SHIP_CANNONS, TWO_WAY_TRADE_STACK)
    for i in range(InventoryType.begin_ShipCannon, InventoryType.end_ShipCannon):
        idFlags[i] = ShipCannonStack
    
    idFlags[InventoryCategory.CONSUMABLES] = (0, FREE_TAKE_CATEGORY)
    ConsumablesStack = (InventoryCategory.CONSUMABLES, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_Consumables, InventoryType.end_Consumables):
        idFlags[i] = ConsumablesStack
    
    idFlags[InventoryCategory.QUEST_SLOTS] = (0, TWO_WAY_TRADE_CATEGORY)
    QuestSlotStack = (InventoryCategory.QUEST_SLOTS, TWO_WAY_TRADE_STACK)
    for i in range(InventoryType.begin_QuestSlot, InventoryType.end_QuestSlot):
        idFlags[i] = QuestSlotStack
    
    idFlags[InventoryCategory.MAX_PLAYER_ATTRIBUTES] = (0, FREE_GIVE_CATEGORY)
    MaxPlayerAttributeStack = (InventoryCategory.MAX_PLAYER_ATTRIBUTES, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_MaxPlayerAttribute, InventoryType.end_MaxPlayerAttribute):
        idFlags[i] = MaxPlayerAttributeStack
    
    idFlags[InventoryCategory.NUM_RESPEC] = (0, TWO_WAY_TRADE_CATEGORY)
    RespecStack = (InventoryCategory.NUM_RESPEC, TWO_WAY_TRADE_STACK)
    for i in range(InventoryType.begin_NumRespec, InventoryType.end_NumRespec):
        idFlags[i] = RespecStack
    
    idFlags[InventoryCategory.PVP_RENOWN] = (0, FREE_GIVE_CATEGORY)
    PvPStack = (InventoryCategory.PVP_RENOWN, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_PvPRenown, InventoryType.end_PvPRenown):
        idFlags[i] = PvPStack
    
    idFlags[InventoryCategory.TELEPORT_ACCESS] = (0, FREE_GIVE_CATEGORY)
    TeleportAccessStack = (InventoryCategory.TELEPORT_ACCESS, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_TeleportAccess, InventoryType.end_TeleportAccess):
        idFlags[i] = TeleportAccessStack
    
    idFlags[InventoryCategory.WEAPON_SKILL_MELEE] = (0, FREE_GIVE_CATEGORY)
    WeaponSkillMeleeStack = (InventoryCategory.WEAPON_SKILL_MELEE, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_WeaponSkillMelee, InventoryType.end_WeaponSkillMelee):
        idFlags[i] = WeaponSkillMeleeStack
    
    idFlags[InventoryCategory.WEAPON_SKILL_CUTLASS] = (0, FREE_GIVE_CATEGORY)
    WeaponSkillCutlassStack = (InventoryCategory.WEAPON_SKILL_CUTLASS, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_WeaponSkillCutlass, InventoryType.end_WeaponSkillCutlass):
        idFlags[i] = WeaponSkillCutlassStack
    
    idFlags[InventoryCategory.WEAPON_SKILL_PISTOL] = (0, FREE_GIVE_CATEGORY)
    WeaponSkillPistolStack = (InventoryCategory.WEAPON_SKILL_PISTOL, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_WeaponSkillPistol, InventoryType.end_WeaponSkillPistol):
        idFlags[i] = WeaponSkillPistolStack
    
    idFlags[InventoryCategory.WEAPON_SKILL_MUSKET] = (0, FREE_GIVE_CATEGORY)
    WeaponSkillMusketStack = (InventoryCategory.WEAPON_SKILL_MUSKET, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_WeaponSkillMusket, InventoryType.end_WeaponSkillMusket):
        idFlags[i] = WeaponSkillMusketStack
    
    idFlags[InventoryCategory.WEAPON_SKILL_BAYONET] = (0, FREE_GIVE_CATEGORY)
    WeaponSkillBayonetStack = (InventoryCategory.WEAPON_SKILL_BAYONET, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_WeaponSkillBayonet, InventoryType.end_WeaponSkillBayonet):
        idFlags[i] = WeaponSkillBayonetStack
    
    idFlags[InventoryCategory.WEAPON_SKILL_DAGGER] = (0, FREE_GIVE_CATEGORY)
    WeaponSkillDaggerStack = (InventoryCategory.WEAPON_SKILL_DAGGER, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_WeaponSkillDagger, InventoryType.end_WeaponSkillDagger):
        idFlags[i] = WeaponSkillDaggerStack
    
    idFlags[InventoryCategory.SKILL_SAILING] = (0, FREE_GIVE_CATEGORY)
    SkillSailingStack = (InventoryCategory.SKILL_SAILING, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_SkillSailing, InventoryType.end_SkillSailing):
        idFlags[i] = SkillSailingStack
    
    idFlags[InventoryCategory.VITAE_PENALTY] = (0, FREE_GIVE_CATEGORY)
    VitaeStack = (InventoryCategory.VITAE_PENALTY, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_Vitae, InventoryType.end_Vitae):
        idFlags[i] = VitaeStack
    
    idFlags[InventoryCategory.UNSPENT_SKILL_POINTS] = (0, FREE_GIVE_CATEGORY)
    UnspentSkillStack = (InventoryCategory.UNSPENT_SKILL_POINTS, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_Unspent, InventoryType.end_Unspent):
        idFlags[i] = UnspentSkillStack
    
    idFlags[InventoryCategory.WEAPON_SKILL_GRENADE] = (0, FREE_GIVE_CATEGORY)
    WeaponSkillGrenadeStack = (InventoryCategory.WEAPON_SKILL_GRENADE, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_WeaponSkillGrenade, InventoryType.end_WeaponSkillGrenade):
        idFlags[i] = WeaponSkillGrenadeStack
    
    idFlags[InventoryCategory.WEAPON_SKILL_DOLL] = (0, FREE_GIVE_CATEGORY)
    WeaponSkillDollStack = (InventoryCategory.WEAPON_SKILL_DOLL, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_WeaponSkillDoll, InventoryType.end_WeaponSkillDoll):
        idFlags[i] = WeaponSkillDollStack
    
    idFlags[InventoryCategory.WEAPON_SKILL_WAND] = (0, FREE_GIVE_CATEGORY)
    WeaponSkillWandStack = (InventoryCategory.WEAPON_SKILL_WAND, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_WeaponSkillWand, InventoryType.end_WeaponSkillWand):
        idFlags[i] = WeaponSkillWandStack
    
    idFlags[InventoryCategory.WEAPON_SKILL_KETTLE] = (0, FREE_GIVE_CATEGORY)
    WeaponSkillKettleStack = (InventoryCategory.WEAPON_SKILL_KETTLE, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_WeaponSkillKettle, InventoryType.end_WeaponSkillKettle):
        idFlags[i] = WeaponSkillKettleStack
    
    idFlags[InventoryCategory.WEAPON_SKILL_CANNON] = (0, FREE_GIVE_CATEGORY)
    WeaponSkillCannonStack = (InventoryCategory.WEAPON_SKILL_CANNON, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_WeaponSkillCannon, InventoryType.end_ExtendedWeaponSkillCannon):
        idFlags[i] = WeaponSkillCannonStack
    
    idFlags[InventoryCategory.WEAPON_SKILL_ITEM] = (0, FREE_GIVE_CATEGORY)
    WeaponSkillItemStack = (InventoryCategory.WEAPON_SKILL_ITEM, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_WeaponSkillItem, InventoryType.end_WeaponSkillItem):
        idFlags[i] = WeaponSkillItemStack
    
    idFlags[InventoryCategory.KEY_ITEMS] = (0, FREE_GIVE_CATEGORY)
    KeyItemStack = (InventoryCategory.KEY_ITEMS, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_KeyItem, InventoryType.end_KeyItem):
        idFlags[i] = KeyItemStack
    
    idFlags[InventoryCategory.TELEPORT_TOKENS] = (0, FREE_GIVE_CATEGORY)
    TeleportTokenStack = (InventoryCategory.TELEPORT_TOKENS, FREE_GIVE_STACK)
    for i in range(InventoryType.begin_TeleportToken, InventoryType.end_TeleportToken):
        idFlags[i] = TeleportTokenStack
    
    idFlags[InventoryCategory.GAME_OUTCOMES] = (0, FREE_GIVE_CATEGORY)
    idFlags[InventoryCategory.ACCUMULATORS] = (0, ACCUMULATOR_CATEGORY)
    AccumulatorStack = (InventoryCategory.ACCUMULATORS, ACCUMULATOR)
    for i in range(InventoryType.begin_Accumulator, InventoryType.end_Accumulator):
        idFlags[i] = AccumulatorStack
    
    idFlags[InventoryCategory.REPAIR_TOKENS] = (0, FREE_TAKE_CATEGORY)
    RepairTokensStack = (InventoryCategory.REPAIR_TOKENS, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_RepairTokens, InventoryType.end_RepairTokens):
        idFlags[i] = RepairTokensStack
    
    idFlags[InventoryCategory.WEAPON_PISTOL_AMMO] = (0, FREE_TAKE_CATEGORY)
    WeaponPistolAmmoStack = (InventoryCategory.WEAPON_PISTOL_AMMO, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_WeaponPistolAmmo, InventoryType.end_WeaponPistolAmmo):
        idFlags[i] = WeaponPistolAmmoStack
    
    idFlags[InventoryCategory.WEAPON_MUSKET_AMMO] = (0, FREE_TAKE_CATEGORY)
    WeaponMusketAmmoStack = (InventoryCategory.WEAPON_MUSKET_AMMO, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_WeaponMusketAmmo, InventoryType.end_WeaponMusketAmmo):
        idFlags[i] = WeaponMusketAmmoStack
    
    idFlags[InventoryCategory.WEAPON_GRENADE_AMMO] = (0, FREE_TAKE_CATEGORY)
    WeaponGrenadeAmmoStack = (InventoryCategory.WEAPON_GRENADE_AMMO, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_WeaponGrenadeAmmo, InventoryType.end_WeaponGrenadeAmmo):
        idFlags[i] = WeaponGrenadeAmmoStack
    
    idFlags[InventoryCategory.WEAPON_CANNON_AMMO] = (0, FREE_TAKE_CATEGORY)
    WeaponCannonAmmoStack = (InventoryCategory.WEAPON_CANNON_AMMO, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_WeaponCannonAmmo, InventoryType.end_WeaponCannonAmmo):
        idFlags[i] = WeaponCannonAmmoStack
    
    idFlags[InventoryCategory.COLLECTIONS] = (0, FREE_TAKE_CATEGORY)
    CollectionsStack = (InventoryCategory.COLLECTIONS, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_Collections, InventoryType.end_Collections):
        idFlags[i] = CollectionsStack
    
    idFlags[InventoryCategory.PLAYER_RANKING] = (0, FREE_TAKE_CATEGORY)
    RankingStack = (InventoryCategory.PLAYER_RANKING, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_RankingCategories, InventoryType.end_RankingCategories):
        idFlags[i] = RankingStack
    
    idFlags[InventoryCategory.WEAPON_DAGGER_AMMO] = (0, FREE_TAKE_CATEGORY)
    WeaponDaggerAmmoStack = (InventoryCategory.WEAPON_DAGGER_AMMO, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_WeaponDaggerAmmo, InventoryType.end_WeaponDaggerAmmo):
        idFlags[i] = WeaponDaggerAmmoStack
    
    idFlags[InventoryCategory.PISTOL_POUCHES] = (0, FREE_TAKE_CATEGORY)
    PouchesPistolAmmoStack = (InventoryCategory.PISTOL_POUCHES, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_PistolPouches, InventoryType.end_PistolPouches):
        idFlags[i] = PouchesPistolAmmoStack
    
    idFlags[InventoryCategory.DAGGER_POUCHES] = (0, FREE_TAKE_CATEGORY)
    PouchesDaggerAmmoStack = (InventoryCategory.DAGGER_POUCHES, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_DaggerPouches, InventoryType.end_DaggerPouches):
        idFlags[i] = PouchesDaggerAmmoStack
    
    idFlags[InventoryCategory.GRENADE_POUCHES] = (0, FREE_TAKE_CATEGORY)
    PouchesGrenadeAmmoStack = (InventoryCategory.GRENADE_POUCHES, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_GrenadePouches, InventoryType.end_GrenadePouches):
        idFlags[i] = PouchesGrenadeAmmoStack
    
    idFlags[InventoryCategory.CANNON_POUCHES] = (0, FREE_TAKE_CATEGORY)
    PouchesCannonAmmoStack = (InventoryCategory.CANNON_POUCHES, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_CannonPouches, InventoryType.end_CannonPouches):
        idFlags[i] = PouchesCannonAmmoStack
    
    idFlags[InventoryCategory.CLOTHING] = (0, FREE_TAKE_CATEGORY)
    idFlags[InventoryType.Clothing] = (0, FREE_TAKE_CATEGORY)
    idFlags[InventoryCategory.CARDS] = (0, FREE_TAKE_CATEGORY)
    CardsStack = (InventoryCategory.CARDS, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_Cards, InventoryType.end_Cards):
        idFlags[i] = CardsStack
    
    idFlags[InventoryCategory.SONGS] = (0, FREE_TAKE_CATEGORY)
    SongsStack = (InventoryCategory.SONGS, FREE_TAKE_STACK)
    for i in range(InventoryType.begin_Songs, InventoryType.end_Songs):
        idFlags[i] = SongsStack
    
    idFlags[InventoryCategory.CLOTHING] = (0, AUTO_LOCATION_DO_ID)
    idFlags[InventoryCategory.FURNITURE] = (0, AUTO_LOCATION_DO_ID)
    idFlags[InventoryCategory.TREASURE_MAPS] = (0, AUTO_LOCATION_DO_ID)
    idFlags[InventoryCategory.SHIP_MAINPARTS] = (0, AUTO_LOCATION_DO_ID)
    idFlags[InventoryCategory.FISH_CAUGHT] = (0, AUTO_LOCATION_DO_ID)
    idFlags[InventoryCategory.QUESTS] = (0, AUTO_LOCATION_DO_ID)
    idFlags[InventoryCategory.SHIP_ACCESSORIES] = (0, AUTO_LOCATION_DO_ID)
    idFlags[InventoryCategory.FLAGS] = (0, AUTO_LOCATION_DO_ID)
    idFlags[InventoryCategory.SHIPS] = (0, AUTO_OWNER_DO_ID)
    idFlags[InventoryCategory.PETS] = (0, AUTO_OWNER_DO_ID)
    idFlags[InventoryCategory.WAGERS] = (0, AUTO_OWNER_DO_ID)
    idFlags[InventoryCategory.TRASH] = (0, SPECIAL)
    idFlags[InventoryType.UberDogRev] = (InventoryCategory.PLAYER_RANKING, FREE_TAKE_STACK)
    
    @staticmethod
    def isLimitChange(a):
        return a & InventoryId.IS_LIMIT_CHANGE

    @staticmethod
    def isPercentChange(a):
        return a & InventoryId.PERCENT_CHANGE

    @staticmethod
    def isMinChange(a):
        return a & InventoryId.MIN_CHANGE

    @staticmethod
    def isFreeGiveStackType(id):
        return InventoryId.idFlags.get(id, (0, 0))[1] & InventoryId.FREE_GIVE_STACK != 0

    @staticmethod
    def isFreeTakeStackType(id):
        return InventoryId.idFlags.get(id, (0, 0))[1] & InventoryId.FREE_TAKE_STACK != 0

    @staticmethod
    def isStackable(id):
        return InventoryId.idFlags.get(id, (0, 0))[1] & InventoryId.STACK != 0

    @staticmethod
    def isAccumulator(id):
        return InventoryId.idFlags.get(id, (0, 0))[1] & InventoryId.ACCUMULATOR != 0

    @staticmethod
    def isDoId(id):
        return InventoryId.idFlags.get(id, (0, 0))[1] & InventoryId.DO_ID != 0

    @staticmethod
    def isAutoLocation(id):
        return InventoryId.idFlags.get(id, (0, 0))[1] & InventoryId.AUTO_LOCATION != 0

    @staticmethod
    def isAutoOwner(id):
        return InventoryId.idFlags.get(id, (0, 0))[1] & InventoryId.AUTO_OWNER != 0

    @staticmethod
    def isCategory(id):
        return InventoryId.idFlags.get(id, (0, 0))[1] & InventoryId.CATEGORY != 0

    @staticmethod
    def getCategory(id):
        return InventoryId.idFlags.get(id, (0, 0))[0]

    @staticmethod
    def getLimitChange(id):
        return id | InventoryId.IS_LIMIT_CHANGE

    @staticmethod
    def getLimitMinChange(id):
        return id | InventoryId.IS_LIMIT_CHANGE | InventoryId.MIN_CHANGE

    @staticmethod
    def getStackPercentChange(id):
        return id | InventoryId.PERCENT_CHANGE

    @staticmethod
    def getChangeCategoryOrType(id):
        return id & ~InventoryId.IS_LIMIT_CHANGE

