from pandac.PandaModules import *
from otp.otpbase.OTPGlobals import *
from pirates.uberdog.UberDogGlobals import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.ship import ShipGlobals
OVERHAUL_COST_PERCENTAGE = 0.4
CAPTAIN_LOOT_MULTIPLIER = 0.25

def getAvatarHealHpCost(hp):
    return 5


def getAvatarHealMojoCost(mojo):
    return 5


class ItemType:
    MELEE = 1
    SWORD = 2
    PISTOL = 3
    MUSKET = 4
    DAGGER = 5
    GRENADE = 6
    DOLL = 7
    WAND = 8
    KETTLE = 9
    SHIP = 10
    SHIPPART = 11
    CONSUMABLE = 12
    FURNITURE = 13
    INGREDIENT = 14
    COMBAT_WEAPON = 15
    RANGED_WEAPON = 16
    GRENADE_WEAPON = 17
    VOODOO_WEAPON = 18
    CANNON = 19
    WEAPON = 20
    INTERCEPTOR = 21
    MERCHANT = 22
    WARSHIP = 23
    CANNONAMMO = 24
    AMMO = 25
    PISTOLAMMO = 26
    GRENADEAMMO = 27
    DAGGERAMMO = 28
    POTION = 29
    BOTTLE = 30
    BAYONET = 31
    SHIP_REPAIR_KIT = 32
    POUCH = 32
    PISTOL_POUCH = 33
    DAGGER_POUCH = 34
    GRENADE_POUCH = 35
    CANNON_POUCH = 36
    FOOD = 37


class ItemTypeGroup:
    CUTLASS = 1
    DAGGER = 2
    PISTOL = 3
    CANNON = 4
    DOLL = 5
    POTION = 6
    GRENADE = 7
    WAND = 8

__itemTypeList = {
    ItemType.DAGGER: ItemTypeGroup.DAGGER,
    ItemType.DAGGERAMMO: ItemTypeGroup.DAGGER,
    ItemType.DAGGER_POUCH: ItemTypeGroup.DAGGER,
    ItemType.SWORD: ItemTypeGroup.CUTLASS,
    ItemType.PISTOL: ItemTypeGroup.PISTOL,
    ItemType.PISTOLAMMO: ItemTypeGroup.PISTOL,
    ItemType.PISTOL_POUCH: ItemTypeGroup.PISTOL,
    ItemType.CANNONAMMO: ItemTypeGroup.CANNON,
    ItemType.CANNON_POUCH: ItemTypeGroup.CANNON,
    ItemType.DOLL: ItemTypeGroup.DOLL,
    ItemType.POTION: ItemTypeGroup.POTION,
    ItemType.GRENADE: ItemTypeGroup.GRENADE,
    ItemType.GRENADEAMMO: ItemTypeGroup.GRENADE,
    ItemType.GRENADE_POUCH: ItemTypeGroup.GRENADE,
    ItemType.WAND: ItemTypeGroup.WAND}

class ItemId:
    GOLD = InventoryType.GoldInPocket
    COLLECT = InventoryType.Collection_Set1
    CARD = InventoryType.begin_Cards
    CLOTHING = InventoryType.Clothing
    BOUNTY = InventoryType.PVPCurrentInfamy
    MELEE_L1 = InventoryType.MeleeWeaponL1
    MELEE_L2 = InventoryType.MeleeWeaponL2
    MELEE_L3 = InventoryType.MeleeWeaponL3
    MELEE_L4 = InventoryType.MeleeWeaponL4
    MELEE_L5 = InventoryType.MeleeWeaponL5
    MELEE_L6 = InventoryType.MeleeWeaponL6
    CUTLASS_L1 = InventoryType.CutlassWeaponL1
    CUTLASS_L2 = InventoryType.CutlassWeaponL2
    CUTLASS_L3 = InventoryType.CutlassWeaponL3
    CUTLASS_L4 = InventoryType.CutlassWeaponL4
    CUTLASS_L5 = InventoryType.CutlassWeaponL5
    CUTLASS_L6 = InventoryType.CutlassWeaponL6
    PISTOL_L1 = InventoryType.PistolWeaponL1
    PISTOL_L2 = InventoryType.PistolWeaponL2
    PISTOL_L3 = InventoryType.PistolWeaponL3
    PISTOL_L4 = InventoryType.PistolWeaponL4
    PISTOL_L5 = InventoryType.PistolWeaponL5
    PISTOL_L6 = InventoryType.PistolWeaponL6
    MUSKET_L1 = InventoryType.MusketWeaponL1
    MUSKET_L2 = InventoryType.MusketWeaponL2
    MUSKET_L3 = InventoryType.MusketWeaponL3
    DAGGER_L1 = InventoryType.DaggerWeaponL1
    DAGGER_L2 = InventoryType.DaggerWeaponL2
    DAGGER_L3 = InventoryType.DaggerWeaponL3
    DAGGER_L4 = InventoryType.DaggerWeaponL4
    DAGGER_L5 = InventoryType.DaggerWeaponL5
    DAGGER_L6 = InventoryType.DaggerWeaponL6
    GRENADE_L1 = InventoryType.GrenadeWeaponL1
    GRENADE_L2 = InventoryType.GrenadeWeaponL2
    GRENADE_L3 = InventoryType.GrenadeWeaponL3
    GRENADE_L4 = InventoryType.GrenadeWeaponL4
    GRENADE_L5 = InventoryType.GrenadeWeaponL5
    GRENADE_L6 = InventoryType.GrenadeWeaponL6
    WAND_L1 = InventoryType.WandWeaponL1
    WAND_L2 = InventoryType.WandWeaponL2
    WAND_L3 = InventoryType.WandWeaponL3
    WAND_L4 = InventoryType.WandWeaponL4
    WAND_L5 = InventoryType.WandWeaponL5
    WAND_L6 = InventoryType.WandWeaponL6
    DOLL_L1 = InventoryType.DollWeaponL1
    DOLL_L2 = InventoryType.DollWeaponL2
    DOLL_L3 = InventoryType.DollWeaponL3
    DOLL_L4 = InventoryType.DollWeaponL4
    DOLL_L5 = InventoryType.DollWeaponL5
    DOLL_L6 = InventoryType.DollWeaponL6
    KETTLE_L1 = InventoryType.KettleWeaponL1
    KETTLE_L2 = InventoryType.KettleWeaponL2
    KETTLE_L3 = InventoryType.KettleWeaponL3
    CANNON_L1 = InventoryType.CannonL1
    CANNON_L2 = InventoryType.CannonL2
    CANNON_L3 = InventoryType.CannonL3
    BAYONET_L1 = InventoryType.BayonetWeaponL1
    BAYONET_L2 = InventoryType.BayonetWeaponL2
    BAYONET_L3 = InventoryType.BayonetWeaponL3
    ROUNDSHOT = InventoryType.AmmoRoundShot
    CHAIN_SHOT = InventoryType.AmmoChainShot
    GRAPE_SHOT = InventoryType.AmmoGrapeShot
    FIREBRAND = InventoryType.AmmoFirebrand
    THUNDERBOLT = InventoryType.AmmoThunderbolt
    EXPLOSIVE = InventoryType.AmmoExplosive
    FURY = InventoryType.AmmoFury
    GRAPPLE_HOOK = InventoryType.AmmoGrappleHook
    BULLET = InventoryType.AmmoBullet
    GAS_CLOUD = InventoryType.AmmoGasCloud
    SKULL_AMMO = InventoryType.AmmoSkull
    FLAME_CLOUD = InventoryType.AmmoFlameCloud
    FLAMING_SKULL = InventoryType.AmmoFlamingSkull
    BAR_SHOT = InventoryType.AmmoBarShot
    KNIVES = InventoryType.AmmoKnives
    MINE = InventoryType.AmmoMine
    BARNACLES = InventoryType.AmmoBarnacles
    COMET = InventoryType.AmmoComet
    VENOMSHOT = InventoryType.AmmoVenomShot
    IRONSHOT = InventoryType.AmmoBaneShot
    GOLDENSHOT = InventoryType.AmmoHexEaterShot
    SILVERSHOT = InventoryType.AmmoSilverShot
    STEELSHOT = InventoryType.AmmoSteelShot
    ASP_DAGGER = InventoryType.AmmoAsp
    ADDER_DAGGER = InventoryType.AmmoAdder
    SIDEWINDER_DAGGER = InventoryType.AmmoSidewinder
    VIPERNEST_DAGGER = InventoryType.AmmoViperNest
    EXPLOSION_G = InventoryType.AmmoGrenadeExplosion
    SHOCKBOMB_G = InventoryType.AmmoGrenadeShockBomb
    FLAME_G = InventoryType.AmmoGrenadeFlame
    SMOKE_G = InventoryType.AmmoGrenadeSmoke
    SIEGE_G = InventoryType.AmmoGrenadeSiege
    LANDMINE_G = InventoryType.AmmoGrenadeLandMine
    PISTOL_POUCH_L1 = InventoryType.PistolPouchL1
    PISTOL_POUCH_L2 = InventoryType.PistolPouchL2
    PISTOL_POUCH_L3 = InventoryType.PistolPouchL3
    DAGGER_POUCH_L1 = InventoryType.DaggerPouchL1
    DAGGER_POUCH_L2 = InventoryType.DaggerPouchL2
    DAGGER_POUCH_L3 = InventoryType.DaggerPouchL3
    GRENADE_POUCH_L1 = InventoryType.GrenadePouchL1
    GRENADE_POUCH_L2 = InventoryType.GrenadePouchL2
    GRENADE_POUCH_L3 = InventoryType.GrenadePouchL3
    CANNON_POUCH_L1 = InventoryType.CannonPouchL1
    CANNON_POUCH_L2 = InventoryType.CannonPouchL2
    CANNON_POUCH_L3 = InventoryType.CannonPouchL3
    POTION_1 = InventoryType.Potion1
    POTION_2 = InventoryType.Potion2
    POTION_3 = InventoryType.Potion3
    POTION_4 = InventoryType.Potion4
    POTION_5 = InventoryType.Potion5
    PORK_CHUNK = InventoryType.PorkChunk
    SHIP_REPAIR_KIT = InventoryType.ShipRepairKit
    INTERCEPTOR_L1 = ShipGlobals.INTERCEPTORL1
    INTERCEPTOR_L2 = ShipGlobals.INTERCEPTORL2
    INTERCEPTOR_L3 = ShipGlobals.INTERCEPTORL3
    INTERCEPTOR_L4 = ShipGlobals.INTERCEPTORL4
    MERCHANT_L1 = ShipGlobals.MERCHANTL1
    MERCHANT_L2 = ShipGlobals.MERCHANTL2
    MERCHANT_L3 = ShipGlobals.MERCHANTL3
    MERCHANT_L4 = ShipGlobals.MERCHANTL4
    WARSHIP_L1 = ShipGlobals.WARSHIPL1
    WARSHIP_L2 = ShipGlobals.WARSHIPL2
    WARSHIP_L3 = ShipGlobals.WARSHIPL3
    WARSHIP_L4 = ShipGlobals.WARSHIPL4
    BLACK_PEARL = ShipGlobals.BLACK_PEARL
    GOLIATH = ShipGlobals.GOLIATH
    DAUNTLESS = ShipGlobals.DAUNTLESS
    FLYING_DUTCHMAN = ShipGlobals.FLYING_DUTCHMAN
    JOLLY_ROGER = ShipGlobals.JOLLY_ROGER
    SKEL_WARSHIPL3 = ShipGlobals.SKEL_WARSHIPL3
    SKEL_INTERCEPTORL3 = ShipGlobals.SKEL_INTERCEPTORL3
    SMALL_BOTTLE = InventoryType.SmallBottle
    MEDIUM_BOTTLE = InventoryType.MediumBottle
    LARGE_BOTTLE = InventoryType.LargeBottle
    CARGO_CRATE = 1
    CARGO_CHEST = 2
    CARGO_SKCHEST = 3
    WHEAT = 101
    COTTON = 102
    RUM = 103
    SILK = 104
    IVORY = 105
    SPICES = 106
    IRON_ORE = 107
    COPPER_BARS = 151
    SILVER_BARS = 152
    GOLD_BARS = 153
    EMERALDS = 154
    RUBIES = 155
    DIAMONDS = 156
    CURSED_COIN = 201
    ARTIFACT = 202
    RELIC = 203
    RARE_DIAMOND = 204
    CROWN_JEWELS = 205
    RAREITEM6 = 206
    QUEST_DROP_JEWEL = 250
    QUEST_DROP_TATTOO = 251
    QUEST_DROP_WEAPON = 252

__crateCargoList = {
    ItemId.CARGO_CRATE: 50,
    ItemId.CARGO_CHEST: 45,
    ItemId.CARGO_SKCHEST: 5}

def getCargoValue(itemId):
    entry = __crateCargoList.get(itemId)
    if entry:
        return entry[0]
    return None
    

__cargoList = {
    ItemId.WHEAT: (5, ItemId.CARGO_CRATE, 35),
    ItemId.COTTON: (7, ItemId.CARGO_CRATE, 25),
    ItemId.RUM: (9, ItemId.CARGO_CRATE, 20),
    ItemId.IRON_ORE: (15, ItemId.CARGO_CRATE, 10),
    ItemId.IVORY: (25, ItemId.CARGO_CRATE, 5),
    ItemId.SILK: (40, ItemId.CARGO_CRATE, 3),
    ItemId.SPICES: (90, ItemId.CARGO_CRATE, 2),
    ItemId.COPPER_BARS: (25, ItemId.CARGO_CHEST, 75),
    ItemId.SILVER_BARS: (50, ItemId.CARGO_CHEST, 20),
    ItemId.GOLD_BARS: (120, ItemId.CARGO_CHEST, 5),
    ItemId.EMERALDS: (90, ItemId.CARGO_SKCHEST, 80),
    ItemId.RUBIES: (140, ItemId.CARGO_SKCHEST, 15),
    ItemId.DIAMONDS: (250, ItemId.CARGO_SKCHEST, 5)}

def getCargoValue(itemId):
    entry = __cargoList.get(itemId)
    if entry:
        return entry[0]
    
    return 0


def getCargoCategory(itemId):
    entry = __cargoList.get(itemId)
    if entry:
        return entry[1]
    return None
    

def getCargoRarity(itemId):
    entry = __cargoList.get(itemId)
    if entry:
        return entry[2]
    return None
    

def getAllCargoType(cargoType):
    cargo = []
    for itemId in __cargoList:
        if __cargoList.get(itemId)[1] == cargoType:
            cargo.append(itemId)
    
    return cargo


def getCargoTotalValue(unpackedCargoList):
    total = 0
    for itemId in unpackedCargoList:
        total += getCargoValue(itemId)
    
    return total


def getRespecCost(numRespecs):
    if numRespecs <= 0:
        return 250
    elif numRespecs <= 1:
        return 2500
    else:
        return 10000

__itemList = {
    ItemId.MELEE_L1: (0, ItemType.WEAPON, ItemType.MELEE, ItemType.COMBAT_WEAPON, 1, 0, None),
    ItemId.MELEE_L2: (50, ItemType.WEAPON, ItemType.MELEE, ItemType.COMBAT_WEAPON, 1, 5, None),
    ItemId.MELEE_L3: (500, ItemType.WEAPON, ItemType.MELEE, ItemType.COMBAT_WEAPON, 1, 10, None),
    ItemId.MELEE_L4: (2500, ItemType.WEAPON, ItemType.MELEE, ItemType.COMBAT_WEAPON, 1, 15, None),
    ItemId.MELEE_L5: (10000, ItemType.WEAPON, ItemType.MELEE, ItemType.COMBAT_WEAPON, 1, 20, None),
    ItemId.MELEE_L6: (50000, ItemType.WEAPON, ItemType.MELEE, ItemType.COMBAT_WEAPON, 1, 25, None),
    ItemId.CUTLASS_L1: (40, ItemType.WEAPON, ItemType.SWORD, ItemType.COMBAT_WEAPON, 1, 0, InventoryType.CutlassToken),
    ItemId.CUTLASS_L2: (200, ItemType.WEAPON, ItemType.SWORD, ItemType.COMBAT_WEAPON, 1, 5, InventoryType.CutlassToken),
    ItemId.CUTLASS_L3: (1000, ItemType.WEAPON, ItemType.SWORD, ItemType.COMBAT_WEAPON, 1, 10, InventoryType.CutlassToken),
    ItemId.CUTLASS_L4: (5000, ItemType.WEAPON, ItemType.SWORD, ItemType.COMBAT_WEAPON, 1, 15, InventoryType.CutlassToken),
    ItemId.CUTLASS_L5: (10000, ItemType.WEAPON, ItemType.SWORD, ItemType.COMBAT_WEAPON, 1, 20, InventoryType.CutlassToken),
    ItemId.CUTLASS_L6: (25000, ItemType.WEAPON, ItemType.SWORD, ItemType.COMBAT_WEAPON, 1, 25, InventoryType.CutlassToken),
    ItemId.PISTOL_L1: (60, ItemType.WEAPON, ItemType.PISTOL, ItemType.RANGED_WEAPON, 1, 0, InventoryType.PistolToken),
    ItemId.PISTOL_L2: (300, ItemType.WEAPON, ItemType.PISTOL, ItemType.RANGED_WEAPON, 1, 5, InventoryType.PistolToken),
    ItemId.PISTOL_L3: (2000, ItemType.WEAPON, ItemType.PISTOL, ItemType.RANGED_WEAPON, 1, 10, InventoryType.PistolToken),
    ItemId.PISTOL_L4: (7500, ItemType.WEAPON, ItemType.PISTOL, ItemType.RANGED_WEAPON, 1, 15, InventoryType.PistolToken),
    ItemId.PISTOL_L5: (15000, ItemType.WEAPON, ItemType.PISTOL, ItemType.RANGED_WEAPON, 1, 20, InventoryType.PistolToken),
    ItemId.PISTOL_L6: (30000, ItemType.WEAPON, ItemType.PISTOL, ItemType.RANGED_WEAPON, 1, 25, InventoryType.PistolToken),
    ItemId.MUSKET_L1: (60, ItemType.WEAPON, ItemType.MUSKET, ItemType.RANGED_WEAPON, 1, 0, None),
    ItemId.MUSKET_L2: (600, ItemType.WEAPON, ItemType.MUSKET, ItemType.RANGED_WEAPON, 1, 5, None),
    ItemId.MUSKET_L3: (6000, ItemType.WEAPON, ItemType.MUSKET, ItemType.RANGED_WEAPON, 1, 15, None),
    ItemId.DAGGER_L1: (100, ItemType.WEAPON, ItemType.DAGGER, ItemType.COMBAT_WEAPON, 1, 0, InventoryType.DaggerToken),
    ItemId.DAGGER_L2: (250, ItemType.WEAPON, ItemType.DAGGER, ItemType.COMBAT_WEAPON, 1, 5, InventoryType.DaggerToken),
    ItemId.DAGGER_L3: (1250, ItemType.WEAPON, ItemType.DAGGER, ItemType.COMBAT_WEAPON, 1, 10, InventoryType.DaggerToken),
    ItemId.DAGGER_L4: (7000, ItemType.WEAPON, ItemType.DAGGER, ItemType.COMBAT_WEAPON, 1, 15, InventoryType.DaggerToken),
    ItemId.DAGGER_L5: (14000, ItemType.WEAPON, ItemType.DAGGER, ItemType.COMBAT_WEAPON, 1, 20, InventoryType.DaggerToken),
    ItemId.DAGGER_L6: (28000, ItemType.WEAPON, ItemType.DAGGER, ItemType.COMBAT_WEAPON, 1, 25, InventoryType.DaggerToken),
    ItemId.GRENADE_L1: (200, ItemType.WEAPON, ItemType.GRENADE, ItemType.GRENADE_WEAPON, 1, 0, InventoryType.GrenadeToken),
    ItemId.WAND_L1: (100, ItemType.WEAPON, ItemType.WAND, ItemType.VOODOO_WEAPON, 1, 0, InventoryType.WandToken),
    ItemId.WAND_L2: (300, ItemType.WEAPON, ItemType.WAND, ItemType.VOODOO_WEAPON, 1, 5, InventoryType.WandToken),
    ItemId.WAND_L3: (1800, ItemType.WEAPON, ItemType.WAND, ItemType.VOODOO_WEAPON, 1, 10, InventoryType.WandToken),
    ItemId.WAND_L4: (6000, ItemType.WEAPON, ItemType.WAND, ItemType.VOODOO_WEAPON, 1, 15, InventoryType.WandToken),
    ItemId.WAND_L5: (12000, ItemType.WEAPON, ItemType.WAND, ItemType.VOODOO_WEAPON, 1, 20, InventoryType.WandToken),
    ItemId.WAND_L6: (24000, ItemType.WEAPON, ItemType.WAND, ItemType.VOODOO_WEAPON, 1, 25, InventoryType.WandToken),
    ItemId.DOLL_L1: (80, ItemType.WEAPON, ItemType.DOLL, ItemType.VOODOO_WEAPON, 1, 0, InventoryType.DollToken),
    ItemId.DOLL_L2: (200, ItemType.WEAPON, ItemType.DOLL, ItemType.VOODOO_WEAPON, 1, 5, InventoryType.DollToken),
    ItemId.DOLL_L3: (1200, ItemType.WEAPON, ItemType.DOLL, ItemType.VOODOO_WEAPON, 1, 10, InventoryType.DollToken),
    ItemId.DOLL_L4: (2400, ItemType.WEAPON, ItemType.DOLL, ItemType.VOODOO_WEAPON, 1, 15, InventoryType.DollToken),
    ItemId.DOLL_L5: (4800, ItemType.WEAPON, ItemType.DOLL, ItemType.VOODOO_WEAPON, 1, 20, InventoryType.DollToken),
    ItemId.DOLL_L6: (20000, ItemType.WEAPON, ItemType.DOLL, ItemType.VOODOO_WEAPON, 1, 25, InventoryType.DollToken),
    ItemId.KETTLE_L1: (300, ItemType.WEAPON, ItemType.KETTLE, ItemType.VOODOO_WEAPON, 1, 0, None),
    ItemId.KETTLE_L2: (3000, ItemType.WEAPON, ItemType.KETTLE, ItemType.VOODOO_WEAPON, 1, 5, None),
    ItemId.KETTLE_L3: (30000, ItemType.WEAPON, ItemType.KETTLE, ItemType.VOODOO_WEAPON, 1, 15, None),
    ItemId.BAYONET_L1: (60, ItemType.WEAPON, ItemType.BAYONET, ItemType.RANGED_WEAPON, 1, 0, None),
    ItemId.BAYONET_L2: (600, ItemType.WEAPON, ItemType.BAYONET, ItemType.RANGED_WEAPON, 1, 5, None),
    ItemId.BAYONET_L3: (6000, ItemType.WEAPON, ItemType.BAYONET, ItemType.RANGED_WEAPON, 1, 15, None),
    ItemId.VENOMSHOT: (0.15, ItemType.AMMO, ItemType.PISTOLAMMO, None, 25, 0, None),
    ItemId.IRONSHOT: (0.2, ItemType.AMMO, ItemType.PISTOLAMMO, None, 25, 0, None),
    ItemId.GOLDENSHOT: (0.25, ItemType.AMMO, ItemType.PISTOLAMMO, None, 25, 0, None),
    ItemId.SILVERSHOT: (0.3, ItemType.AMMO, ItemType.PISTOLAMMO, None, 25, 0, None),
    ItemId.STEELSHOT: (0.35, ItemType.AMMO, ItemType.PISTOLAMMO, None, 25, 0, None),
    ItemId.ASP_DAGGER: (0.15, ItemType.AMMO, ItemType.DAGGERAMMO, None, 25, 0, None),
    ItemId.ADDER_DAGGER: (0.3, ItemType.AMMO, ItemType.DAGGERAMMO, None, 25, 0, None),
    ItemId.SIDEWINDER_DAGGER: (0.45, ItemType.AMMO, ItemType.DAGGERAMMO, None, 25, 0, None),
    ItemId.VIPERNEST_DAGGER: (1.5, ItemType.AMMO, ItemType.DAGGERAMMO, None, 5, 0, None),
    ItemId.EXPLOSION_G: (0.4, ItemType.AMMO, ItemType.GRENADEAMMO, None, 25, 0, None),
    ItemId.SHOCKBOMB_G: (0.5, ItemType.AMMO, ItemType.GRENADEAMMO, None, 10, 0, None),
    ItemId.FLAME_G: (0.6, ItemType.AMMO, ItemType.GRENADEAMMO, None, 10, 0, None),
    ItemId.SMOKE_G: (1.5, ItemType.AMMO, ItemType.GRENADEAMMO, None, 5, 0, None),
    ItemId.LANDMINE_G: (1.2, ItemType.AMMO, ItemType.GRENADEAMMO, None, 5, 0, None),
    ItemId.SIEGE_G: (2.0, ItemType.AMMO, ItemType.GRENADEAMMO, None, 5, 0, None),
    ItemId.POTION_1: (3, ItemType.CONSUMABLE, ItemType.POTION, None, 1, 0, None),
    ItemId.POTION_2: (6, ItemType.CONSUMABLE, ItemType.POTION, None, 1, 0, None),
    ItemId.POTION_3: (9, ItemType.CONSUMABLE, ItemType.POTION, None, 1, 0, None),
    ItemId.POTION_4: (15, ItemType.CONSUMABLE, ItemType.POTION, None, 1, 0, None),
    ItemId.POTION_5: (30, ItemType.CONSUMABLE, ItemType.POTION, None, 1, 0, None),
    ItemId.PORK_CHUNK: (0, ItemType.CONSUMABLE, ItemType.FOOD, None, 1, 0, None),
    ItemId.SHIP_REPAIR_KIT: (50, ItemType.CONSUMABLE, ItemType.SHIP_REPAIR_KIT, None, 1, 0, None),
    ItemId.INTERCEPTOR_L1: (100, ItemType.SHIP, ItemType.INTERCEPTOR, None, 1, 0, InventoryType.NewShipToken),
    ItemId.MERCHANT_L1: (300, ItemType.SHIP, ItemType.MERCHANT, None, 1, 0, InventoryType.NewShipToken),
    ItemId.WARSHIP_L1: (800, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),
    ItemId.INTERCEPTOR_L2: (1000, ItemType.SHIP, ItemType.INTERCEPTOR, None, 1, 5, InventoryType.NewShipToken),
    ItemId.MERCHANT_L2: (3500, ItemType.SHIP, ItemType.MERCHANT, None, 1, 5, InventoryType.NewShipToken),
    ItemId.WARSHIP_L2: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 5, InventoryType.NewShipToken),
    ItemId.INTERCEPTOR_L3: (20000, ItemType.SHIP, ItemType.INTERCEPTOR, None, 1, 15, InventoryType.NewShipToken),
    ItemId.MERCHANT_L3: (40000, ItemType.SHIP, ItemType.MERCHANT, None, 1, 15, InventoryType.NewShipToken),
    ItemId.WARSHIP_L3: (60000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 15, InventoryType.NewShipToken),
    ItemId.BLACK_PEARL: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),
    ItemId.GOLIATH: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),
    ItemId.DAUNTLESS: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),
    ItemId.FLYING_DUTCHMAN: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),
    ItemId.JOLLY_ROGER: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),
    ItemId.SKEL_WARSHIPL3: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),
    ItemId.SKEL_INTERCEPTORL3: (0, ItemType.SHIP, ItemType.INTERCEPTOR, None, 1, 0, InventoryType.NewShipToken),
    ItemId.CANNON_L1: (300, ItemType.SHIPPART, ItemType.CANNON, None, 1, 0, None),
    ItemId.CANNON_L2: (3000, ItemType.SHIPPART, ItemType.CANNON, None, 1, 0, None),
    ItemId.CANNON_L3: (30000, ItemType.SHIPPART, ItemType.CANNON, None, 1, 0, None),
    ItemId.ROUNDSHOT: (0, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.CHAIN_SHOT: (0.15, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.GRAPE_SHOT: (0.2, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.FIREBRAND: (0.5, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.THUNDERBOLT: (0.6, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.EXPLOSIVE: (15, ItemType.AMMO, ItemType.CANNONAMMO, None, 1, 0, None),
    ItemId.FURY: (0.8, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.GRAPPLE_HOOK: (0.2, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.BULLET: (0.2, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.GAS_CLOUD: (0.2, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.SKULL_AMMO: (0.3, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.FLAME_CLOUD: (0.3, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.FLAMING_SKULL: (0.3, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.BAR_SHOT: (0.4, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.KNIVES: (0.4, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.MINE: (0.5, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.BARNACLES: (0.5, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.COMET: (0.5, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),
    ItemId.SMALL_BOTTLE: (50, ItemType.BOTTLE, ItemType.BOTTLE, None, 1, 0, None),
    ItemId.MEDIUM_BOTTLE: (500, ItemType.BOTTLE, ItemType.BOTTLE, None, 1, 0, None),
    ItemId.LARGE_BOTTLE: (5000, ItemType.BOTTLE, ItemType.BOTTLE, None, 1, 0, None),
    ItemId.PISTOL_POUCH_L1: (300, ItemType.POUCH, ItemType.PISTOL_POUCH, None, 1, 7, InventoryType.PistolToken),
    ItemId.PISTOL_POUCH_L2: (1200, ItemType.POUCH, ItemType.PISTOL_POUCH, None, 1, 12, InventoryType.PistolToken),
    ItemId.PISTOL_POUCH_L3: (3600, ItemType.POUCH, ItemType.PISTOL_POUCH, None, 1, 17, InventoryType.PistolToken),
    ItemId.DAGGER_POUCH_L1: (200, ItemType.POUCH, ItemType.DAGGER_POUCH, None, 1, 7, InventoryType.DaggerToken),
    ItemId.DAGGER_POUCH_L2: (800, ItemType.POUCH, ItemType.DAGGER_POUCH, None, 1, 12, InventoryType.DaggerToken),
    ItemId.DAGGER_POUCH_L3: (2400, ItemType.POUCH, ItemType.DAGGER_POUCH, None, 1, 17, InventoryType.DaggerToken),
    ItemId.GRENADE_POUCH_L1: (1000, ItemType.POUCH, ItemType.GRENADE_POUCH, None, 1, 7, InventoryType.GrenadeToken),
    ItemId.GRENADE_POUCH_L2: (4000, ItemType.POUCH, ItemType.GRENADE_POUCH, None, 1, 12, InventoryType.GrenadeToken),
    ItemId.GRENADE_POUCH_L3: (12000, ItemType.POUCH, ItemType.GRENADE_POUCH, None, 1, 17, InventoryType.GrenadeToken),
    ItemId.CANNON_POUCH_L1: (500, ItemType.POUCH, ItemType.CANNON_POUCH, None, 1, 7, None),
    ItemId.CANNON_POUCH_L2: (2000, ItemType.POUCH, ItemType.CANNON_POUCH, None, 1, 12, None),
    ItemId.CANNON_POUCH_L3: (8000, ItemType.POUCH, ItemType.CANNON_POUCH, None, 1, 17, None)}

def getItemCost(itemId):
    item = __itemList.get(itemId)
    if item:
        return item[0]
    else:
        return None


def getItemCategory(itemId):
    item = __itemList.get(itemId)
    if item:
        return item[1]
    else:
        return None


def getItemType(itemId):
    item = __itemList.get(itemId)
    if item:
        return item[2]
    else:
        return None


def getItemGroup(itemId):
    return __itemTypeList.get(getItemType(itemId))


def getWeaponClass(itemId):
    item = __itemList.get(itemId)
    if item:
        return item[3]
    else:
        return None


def getItemQuantity(itemId):
    item = __itemList.get(itemId)
    if item:
        return item[4]
    else:
        return None


def getItemMinLevel(itemId):
    item = __itemList.get(itemId)
    if item:
        return item[5]
    else:
        return 0


def getItemTrainingReq(itemId):
    item = __itemList.get(itemId)
    if item:
        return item[6]
    else:
        return 0


__itemIcons = {
    ItemId.CUTLASS_L1: 'icon_cutlass_rusty',
    ItemId.CUTLASS_L2: 'icon_cutlass_iron',
    ItemId.CUTLASS_L3: 'icon_cutlass_steel',
    ItemId.CUTLASS_L4: 'icon_cutlass_fine',
    ItemId.CUTLASS_L5: 'icon_cutlass_pirate',
    ItemId.CUTLASS_L6: 'icon_cutlass_black',
    ItemId.PISTOL_L1: 'icon_pistol_single',
    ItemId.PISTOL_L2: 'icon_pistol_double',
    ItemId.PISTOL_L3: 'icon_pistol_triple',
    ItemId.PISTOL_L4: 'icon_pistol_4',
    ItemId.PISTOL_L5: 'icon_pistol_5',
    ItemId.PISTOL_L6: 'icon_pistol_6',
    ItemId.BAYONET_L1: 'icon_pistol_single',
    ItemId.BAYONET_L2: 'icon_pistol_double',
    ItemId.BAYONET_L3: 'icon_pistol_triple',
    ItemId.DAGGER_L1: 'icon_dagger_small',
    ItemId.DAGGER_L2: 'icon_dagger_battle',
    ItemId.DAGGER_L3: 'icon_dagger_gauche',
    ItemId.DAGGER_L4: 'icon_dagger_coltello',
    ItemId.DAGGER_L5: 'icon_dagger_bloodletter',
    ItemId.DAGGER_L6: 'icon_dagger_slicer',
    ItemId.GRENADE_L1: 'icon_grenade',
    ItemId.GRENADE_L2: 'icon_grenade',
    ItemId.GRENADE_L3: 'icon_grenade',
    ItemId.GRENADE_L4: 'icon_grenade',
    ItemId.GRENADE_L5: 'icon_grenade',
    ItemId.GRENADE_L6: 'icon_grenade',
    ItemId.WAND_L1: 'icon_voodoo_staff_L1',
    ItemId.WAND_L2: 'icon_voodoo_staff_L2',
    ItemId.WAND_L3: 'icon_voodoo_staff_L3',
    ItemId.WAND_L4: 'icon_voodoo_staff_L4',
    ItemId.WAND_L5: 'icon_voodoo_staff_L5',
    ItemId.WAND_L6: 'icon_voodoo_staff_L6',
    ItemId.DOLL_L1: 'icon_voodoo_doll',
    ItemId.DOLL_L2: 'icon_voodoo_doll_cloth',
    ItemId.DOLL_L3: 'icon_voodoo_doll_witch',
    ItemId.DOLL_L4: 'icon_voodoo_doll_pirate',
    ItemId.DOLL_L5: 'icon_voodoo_doll_taboo',
    ItemId.DOLL_L6: 'icon_voodoo_doll_mojo',
    ItemId.CANNON_L1: 'icon_cannon',
    ItemId.CANNON_L2: 'icon_cannon',
    ItemId.CANNON_L3: 'icon_cannon',
    ItemId.POTION_1: 'icon_potion_tonic',
    ItemId.POTION_2: 'icon_potion_tonic',
    ItemId.POTION_3: 'icon_potion_holy_water',
    ItemId.POTION_4: 'icon_potion_elixer',
    ItemId.POTION_5: 'icon_potion_miracle_water',
    ItemId.PORK_CHUNK: 'pir_t_gui_pot_porkTonic',
    ItemId.SHIP_REPAIR_KIT: 'sail_come_about',
    ItemId.PISTOL_POUCH_L1: 'icon_pistol_shotpouch',
    ItemId.PISTOL_POUCH_L2: 'icon_pistol_shotpouch',
    ItemId.PISTOL_POUCH_L3: 'icon_pistol_shotpouch',
    ItemId.DAGGER_POUCH_L1: 'icon_dagger_belt',
    ItemId.DAGGER_POUCH_L2: 'icon_dagger_belt',
    ItemId.DAGGER_POUCH_L3: 'icon_dagger_belt',
    ItemId.GRENADE_POUCH_L1: 'icon_grenade_pouch',
    ItemId.GRENADE_POUCH_L2: 'icon_grenade_pouch',
    ItemId.GRENADE_POUCH_L3: 'icon_grenade_pouch',
    ItemId.CANNON_POUCH_L1: 'icon_cannonball_barrel',
    ItemId.CANNON_POUCH_L2: 'icon_cannonball_barrel',
    ItemId.CANNON_POUCH_L3: 'icon_cannonball_barrel'}

def getItemIcons(itemId):
    item = __itemIcons.get(itemId)
    if item:
        return item
    else:
        return None


MELEE_SHELF_L1 = []
MELEE_SHELF_L2 = [
    ItemId.CUTLASS_L2,
    ItemId.CUTLASS_L3,
    ItemId.DAGGER_L2,
    ItemId.DAGGER_L3]
MELEE_SHELF_L3 = [
    ItemId.CUTLASS_L5,
    ItemId.CUTLASS_L6,
    ItemId.DAGGER_L5,
    ItemId.DAGGER_L6]
MISSILE_SHELF_L1 = []
MISSILE_SHELF_L2 = [
    ItemId.PISTOL_L2,
    ItemId.PISTOL_L3]
MISSILE_SHELF_L3 = [
    ItemId.PISTOL_L5,
    ItemId.PISTOL_L6]
DAGGER_AMMO_SHELF_L1 = [
    ItemId.ASP_DAGGER,
    ItemId.ADDER_DAGGER]
DAGGER_AMMO_SHELF_L2 = [
    ItemId.SIDEWINDER_DAGGER,
    ItemId.VIPERNEST_DAGGER]
CANNON_AMMO_SHELF_L1 = [
    ItemId.CHAIN_SHOT,
    ItemId.GRAPE_SHOT]
CANNON_AMMO_SHELF_L2 = [
    ItemId.FIREBRAND,
    ItemId.THUNDERBOLT,
    ItemId.EXPLOSIVE,
    ItemId.FURY]
SIEGE_SHELF = [
    ItemId.SHIP_REPAIR_KIT]
PISTOL_AMMO_SHELF_L1 = [
    ItemId.VENOMSHOT,
    ItemId.IRONSHOT]
PISTOL_AMMO_SHELF_L2 = [
    ItemId.GOLDENSHOT,
    ItemId.SILVERSHOT,
    ItemId.STEELSHOT]
PISTOL_POUCH_SHELF = [
    ItemId.PISTOL_POUCH_L1,
    ItemId.PISTOL_POUCH_L2,
    ItemId.PISTOL_POUCH_L3]
DAGGER_POUCH_SHELF = [
    ItemId.DAGGER_POUCH_L1,
    ItemId.DAGGER_POUCH_L2,
    ItemId.DAGGER_POUCH_L3]
GRENADE_POUCH_SHELF = [
    ItemId.GRENADE_POUCH_L1,
    ItemId.GRENADE_POUCH_L2,
    ItemId.GRENADE_POUCH_L3]
CANNON_POUCH_SHELF = [
    ItemId.CANNON_POUCH_L1,
    ItemId.CANNON_POUCH_L2,
    ItemId.CANNON_POUCH_L3]
BOMB_AMMO_SHELF_L1 = [
    ItemId.EXPLOSION_G,
    ItemId.SHOCKBOMB_G,
    ItemId.FLAME_G]
BOMB_AMMO_SHELF_L2 = [
    ItemId.SMOKE_G,
    ItemId.SIEGE_G]
TONIC_SHELF_L1 = [
    ItemId.POTION_1,
    ItemId.POTION_2,
    ItemId.POTION_3]
TONIC_SHELF_L2 = [
    ItemId.POTION_4,
    ItemId.POTION_5]
BOMB_SHELF_L1 = []
BOMB_SHELF_L2 = []
BOMB_SHELF_L3 = []
WEAPON_SHELF_ALL = CANNON_AMMO_SHELF_L1
SHIP_ITEM_SHELF = [
    ItemId.SMALL_BOTTLE,
    ItemId.MEDIUM_BOTTLE,
    ItemId.LARGE_BOTTLE]
MUSIC_SHELF = [
    InventoryType.Song_1,
    InventoryType.Song_2,
    InventoryType.Song_3,
    InventoryType.Song_4,
    InventoryType.Song_5,
    InventoryType.Song_6,
    InventoryType.Song_7,
    InventoryType.Song_8,
    InventoryType.Song_9,
    InventoryType.Song_10,
    InventoryType.Song_11,
    InventoryType.Song_12,
    InventoryType.Song_13,
    InventoryType.Song_14,
    InventoryType.Song_15,
    InventoryType.Song_16,
    InventoryType.Song_17,
    InventoryType.Song_18,
    InventoryType.Song_19,
    InventoryType.Song_20]
MOJO_SHELF_L1 = []
MOJO_SHELF_L2 = [
    ItemId.WAND_L2,
    ItemId.WAND_L3,
    ItemId.DOLL_L2,
    ItemId.DOLL_L3]
MOJO_SHELF_L3 = [
    ItemId.WAND_L5,
    ItemId.WAND_L6,
    ItemId.DOLL_L5,
    ItemId.DOLL_L6]
MOJO_SHELF_ALL = MOJO_SHELF_L1 + MOJO_SHELF_L2 + MOJO_SHELF_L3
SHIP_SHELF = [
    ItemId.INTERCEPTOR_L1,
    ItemId.MERCHANT_L1,
    ItemId.WARSHIP_L1,
    ItemId.INTERCEPTOR_L2,
    ItemId.MERCHANT_L2,
    ItemId.WARSHIP_L2,
    ItemId.INTERCEPTOR_L3,
    ItemId.MERCHANT_L3,
    ItemId.WARSHIP_L3]
CollectionValues = {
    0: 10,
    1: 25,
    2: 100}
__pouchTypeToAmmo = {
    ItemType.PISTOL_POUCH: [
        ItemId.VENOMSHOT,
        ItemId.IRONSHOT,
        ItemId.GOLDENSHOT,
        ItemId.SILVERSHOT,
        ItemId.STEELSHOT],
    ItemType.DAGGER_POUCH: [
        ItemId.ASP_DAGGER,
        ItemId.ADDER_DAGGER,
        ItemId.SIDEWINDER_DAGGER,
        ItemId.VIPERNEST_DAGGER],
    ItemType.GRENADE_POUCH: [
        ItemId.EXPLOSION_G,
        ItemId.SHOCKBOMB_G,
        ItemId.FLAME_G,
        ItemId.SMOKE_G,
        ItemId.SIEGE_G],
    ItemType.CANNON_POUCH: [
        ItemId.CHAIN_SHOT,
        ItemId.GRAPE_SHOT,
        ItemId.FIREBRAND,
        ItemId.THUNDERBOLT,
        ItemId.EXPLOSIVE,
        ItemId.FURY]}

def getPouchAmmoList(pouchType):
    ammoList = __pouchTypeToAmmo.get(pouchType)
    if ammoList:
        return ammoList
    else:
        return None


__pouchInventoryBonus = {
    ItemId.PISTOL_POUCH_L1: [
        125,
        125,
        125,
        125,
        125],
    ItemId.PISTOL_POUCH_L2: [
        150,
        150,
        150,
        150,
        150],
    ItemId.PISTOL_POUCH_L3: [
        175,
        175,
        175,
        175,
        175],
    ItemId.DAGGER_POUCH_L1: [
        125,
        75,
        75,
        35],
    ItemId.DAGGER_POUCH_L2: [
        150,
        100,
        100,
        45],
    ItemId.DAGGER_POUCH_L3: [
        175,
        125,
        125,
        60],
    ItemId.GRENADE_POUCH_L1: [
        100,
        60,
        60,
        30,
        30],
    ItemId.GRENADE_POUCH_L2: [
        125,
        70,
        70,
        35,
        35],
    ItemId.GRENADE_POUCH_L3: [
        150,
        80,
        80,
        40,
        40],
    ItemId.CANNON_POUCH_L1: [
        125,
        125,
        75,
        75,
        6,
        75],
    ItemId.CANNON_POUCH_L2: [
        150,
        150,
        100,
        100,
        9,
        100],
    ItemId.CANNON_POUCH_L3: [
        175,
        175,
        125,
        125,
        12,
        125]}

def getInventoryBonus(itemId, index = -1):
    amount = __pouchInventoryBonus.get(itemId)
    if amount:
        if index >= 0:
            return amount[index]
        
        return amount
    
    return 0

