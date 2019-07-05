import string
import os
from otp.otpbase import OTPGlobals
from pirates.uberdog.UberDogGlobals import *
from pirates.economy.EconomyGlobals import *
from pirates.battle.EnemySkills import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.world import OceanZone
from otp.otpbase import OTPLocalizer as OL
InterfaceFont = 'models/fonts/BardiT.bam'
InterfaceOutlineFont = 'models/fonts/BardiT_outline.bam'
PirateChippedFont = 'models/fonts/BriosoPro_chipped.bam'
PirateChippedOutlineFont = 'models/fonts/BriosoPro_chipped_outline.bam'
PirateBoldOutlineFont = 'models/fonts/BriosoPro_bold_outline.bam'
SignFont = PirateChippedOutlineFont
NoRambleshack = 'You cannot go outside yet. Rambleshack is still loading'
NoMainWorld = 'You cannot use ships yet. The main world is still loading'
DialogOK = 'OK'
DialogYes = 'Yes'
DialogNo = 'No'
DialogCancel = 'Cancel'
PortNames = {
    'PortRoyalPort': 'Port Royal',
    'Bilgewater': 'Bilgewater',
    'Art Prototype': 'Art Prototype',
    'TheRock': 'The Rock',
    'Tortuga': 'Tortuga',
    'MadreDelFuego': 'Padres Del Fuego',
    'ArtPrototypePort': 'Bilgewater',
    'VegasPort': 'Vegas',
    'HiddenIslandPort': 'Hidden Island',
    'CutthroatPort': 'Cutthroat Isle',
    'TormentaPort': 'Isla Tormenta'}
lCancel = 'Cancel'
lSubmit = 'Submit'
lConfirm = 'Confirm'
lClose = 'Close'
lOk = 'OK'
lNext = 'Next'
lBack = 'Back'
lQuit = 'Quit'
lYes = 'Yes'
lNo = 'No'
lExit = 'Exit'
PirateShip = 'Pirate Ship'
MoneyName = 'Gold'
CheatCardName = 'Cards'
LevelUp = 'LEVEL UP!'
Level = 'Level'
Rank = 'Rank'
Lv = 'lv'
EXP = 'Rep.'
EXP_Nerf = 'basic access'
CrewBonus = 'crew bonus'
DoubleRepBonus = 'double rep bonus'
HolidayBonus = 'event bonus'
LevelRequirement = 'Requires level %s'
TrainingRequirement = 'Requires training'
SkillRequirement = 'Needs %s'
Unknown = 'Unknown'
NotYet = 'This skill is not yet available.'
InventoryCurrent = '%d/%d'
InventoryFull = 'Inventory Full (%d)'
InventoryOwned = 'Already Owned'
InventoryLowLevel = 'Higher Level Owned'
Sticky = 'Attuned'
Hull = 'Hull'
Sail = 'Sail'
Cannon = 'Cannons'
Broadside = 'Broadside'
Broadsides = 'Broadsides'
Armor = 'Armor'
Cargo = 'Cargo'
Timer = 'Timer'
Crew = 'Shipmates'
HP = 'HP'
SP = 'SP'
Speed = 'Speed'
Sails = 'Sails'
Plunder = 'Plunder'
Limits = 'Limits'
Hull = 'Hull'
Wear = 'Wear'
Skills = 'Skills'
Weapons = 'Weapons'
Treasure = 'Treasure'
ShipProfile = 'Ship Profile'
ExcessGoldLost = 'Are you sure you want to sell this? You can only carry 65,000 Gold, so the extra gold will be lost!'
NotEnoughMoneyWarning = 'Not enough ' + MoneyName + ' !'
EmptyPurchaseWarning = 'Nothing to purchase!'
CannotHoldGoldWarning = 'Cannot hold anymore ' + MoneyName + '!'
CannotHoldShipWarning = 'Cannot hold anymore Ships!'
NothingEquippedWarning = 'No item equipped!'
NoTrainingWarning = 'Requires %s training to use this weapon!'
LevelReqWarning = 'Must be at least Level %s in %s to use this weapon!'
WaitYourTurnWarning = 'Already playing a request!'
Apostrophe = "'s"
ShipRepair = 'Ship Repair'
SellShip = 'Sell Ship'
ShipOverhaul = 'Ship Overhaul'
RepairSails = 'Repair\nSails'
HitCombo = 'Hit Combo!'
TeamCombo = 'Team Attack!'
Damage = 'Total Damage!'
PassiveSkill = 'Passive Skill'
ComboSkill = 'Combo Skill'
CombatSkill = 'Combat Attack'
Consumable = 'Consumable'
ShipRepairSkill = 'Ship Repair Skill'
AmmoSkill = 'Ammo Skill'
AttackSkill = 'Combat Skill'
ShipSkill = 'Ship Maneuver'
ThrowSkill = 'Throwing Skill'
ManaName = 'Voodoo'
HexSkill = 'Hex - %d ' + ManaName
OrderSkill = 'Battle Order'
DealsDamage = 'Deals %d to %d damage!'
HealsDamageRange = 'Heals %d to %d health!'
HealsDamage = 'Heals %s voodoo and %d health!'
DealsMpDamage = 'Removes %d to %d ' + ManaName + ' from the victim!'
LevelUpHeading = 'Level Up!\nPress K to spend skill point.'
LevelUpHPIncrease = '    %s point HP increase.\n'
LevelUpVoodooIncrease = '    %s point Voodoo increase.\n'
LevelUpSkillPoint = '    %s earned.\n'
LevelUpSkillUnlock = '    %s skill unlocked.\n'
TradeCannotHoldWarning = 'Cannot hold those Items!'
TradeItemFullWarning = 'Cannot carry more of that Item!'
TradeTimeoutWarning = 'Trade timeout!'
TradeFailedWarning = 'Trade failed'
WeaponSlotWarning = 'Can only equip a weapon on this slot!'
ItemSlotWarning = 'Can only equip an item on this slot!'
AlreadyOwnWeaponWarning = 'Weapon already owned.'
PurchaseCart = 'Purchase'
SellCart = 'Sell'
PurchaseCommit = 'Buy'
PurchaseCommitHelp = 'Finalize the Sale'
Cost = 'Cost: '
Gain = 'Gain: '
Total = 'Total: '
YourMoney = 'Your Gold: '
YourPVPMoney = 'Your Infamy: '
Vests = 'Vests'
Vest = 'Vest'
Shirts = 'Shirts'
Shirt = 'Shirt'
Pants = 'Pants'
Coats = 'Coats'
Coat = 'Coat'
Shoes = 'Shoes'
Shoe = 'Shoe'
Hats = 'Hats'
Hat = 'Hat'
Belts = 'Belts'
Belt = 'Belt'
MerchantStore = 'Merchant Store'
TailorStore = 'Accessories Store'
TailorPurchase = 'Purchases'
TailorPurchased = 'Purchased'
TailorSelling = 'Selling'
TailorWardrobe = 'My Items'
TailorRemove = 'Remove'
TailorSell = 'Sell'
TailorAddToCart = 'Add'
TailorPreview = 'Click to preview'
TailorEmptyWardrobe = 'No items in category.'
TailorEquip = 'Wear'
TailorPage = 'Page'
TailorTakeOff = 'Take Off'
TattooShopOwned = 'Currently worn'
TattooConfirm = 'Do you wish to\npurchase a %s\n%s for\n%s gold?'
TattooPurchase = 'Purchase Tattoo'
TattooChest = 'Chest'
TattooLeftArm = 'Left Arm'
TattooRightArm = 'Right Arm'
TattooFace = 'Face'
TattooGeneral = 'General'
TattooShop = 'Tattoo Shop'
TailorStartingItem = 'Starting Item'
BarberConfirm = 'Would you like to buy \n%s for %s gold?'
BarberNoMustache = 'Your current beard does not allow for mustaches.'
BarberPurchase = 'Purchase Style'
StoreNewItem = 'New Item!'
TailorColorStrings = {
    0: 'Plain',
    1: 'Light Blue',
    2: 'Light Yellow',
    3: 'Light Green',
    4: 'Brown',
    5: 'Pink',
    6: 'Light Purple',
    7: 'Light Grey',
    8: 'Blue',
    9: 'Yellow',
    10: 'Light Green',
    11: 'Light Brown',
    12: 'Light Red',
    13: 'Light Purple',
    14: 'Grey',
    15: 'Dark Blue',
    16: 'Dark Yellow',
    17: 'Dark Green',
    18: 'Dark Brown',
    19: 'Red',
    20: 'Purple',
    21: 'Bright Orange',
    22: 'Bright Yellow',
    23: 'Bright Blue',
    24: 'Lavender',
    25: 'Forest Green',
    26: 'Magenta',
    27: 'Bright Green',
    28: 'Navy Blue',
    29: 'Bright Red',
    30: 'Dark Black'}
HAIR = 0
BEARD = 1
MUSTACHE = 2
barberNames = {
    HAIR: 'Hair',
    BEARD: 'Beards',
    MUSTACHE: 'Mustaches'}
BarberShortStrings = {
    0: 'Shaved',
    1: 'Haircut',
    2: 'Ponytail',
    3: 'Balding',
    4: 'Mohawk',
    5: 'Beard',
    6: 'Mustache',
    7: 'Bun',
    8: 'Barrette'}
BarberLongStrings = {
    0: 'Completely shaved',
    1: "Men's short haircut",
    2: "Men's haircut with short ponytail",
    3: "Men's haircut with short top ponytail",
    4: "Men's balding haircut",
    5: "Men's shaved head with top ponytail",
    6: "Men's long mullet",
    7: "Men's short Mohawk",
    8: 'Short beard with mustache',
    9: 'Long beard with mustache',
    10: 'Long sideburns with mustache',
    11: 'Medium goatee',
    12: 'Thin goatee',
    13: 'Long hanging goatee',
    14: 'Side chops',
    15: 'Short goatee with soul patch',
    16: 'Thin side burns',
    17: 'Long braided beard',
    18: 'Thick bushy mustache',
    19: 'Thin short mustache',
    20: 'Regular short mustache',
    21: 'Long hanging mustache',
    22: 'Waxed long mustache',
    23: 'Curly waxed long mustache',
    24: 'Small bun',
    25: 'Small bun with bangs',
    26: 'Small bun with long bangs',
    27: 'Long top ponytail',
    28: 'Long top ponytail with bangs',
    29: 'Long top ponytail with long bangs',
    30: 'Short barrette haircut',
    31: 'Short barrette haircut with bangs',
    32: 'Medium haircut with bun',
    33: 'Medium haircut with long top ponytail',
    34: 'Medium haircut with barrette',
    35: 'Barrette with long braided ponytail',
    36: 'Barrette with long braided ponytail and bangs',
    37: 'Barrette with long braided ponytail and long bangs',
    38: 'Short barrette haircut',
    39: 'Short barrette with bangs',
    40: 'Short barrette with long bangs',
    41: 'Long layered haircut',
    42: 'Short layered haircut'}
JewelryStrings = {
    0: 'Golden eye brow spike',
    1: 'Silver eye brow spike',
    2: 'Golden eye brow ring',
    3: 'Silver eye brow ring',
    4: 'Golden ear stud',
    5: 'Silver ear stud',
    6: 'Golden small ear loop',
    7: 'Silver small ear loop',
    8: 'Golden ear spike',
    9: 'Silver ear spike',
    10: 'Golden ear double loop',
    11: 'Silver ear double loop',
    12: 'Gold and silver ear double loop',
    13: 'Golden small ear spike',
    14: 'Silver small ear spike',
    15: 'Golden large ear loop',
    16: 'Silver large ear loop',
    17: 'Golden small ear loop',
    18: 'Silver small ear loop',
    19: 'Golden large ear loop with double top ring',
    20: 'Silver large ear loop with double top ring',
    21: 'Golden double top ear ring',
    22: 'Silver double top ear ring',
    23: 'Golden spike and ring',
    24: 'Silver spike and ring',
    25: 'Golden large ear stud with double top ring',
    26: 'Silver large ear stud with double top ring',
    27: 'Golden nose loop',
    28: 'Silver nose loop',
    29: 'Golden nose spike',
    30: 'Silver nose spike',
    31: 'Golden nose double spike.',
    32: 'Silver nose double spike.',
    33: 'Golden nose spike with loop.',
    34: 'Silver nose spike with loop.',
    35: 'Golden lip ring',
    36: 'Silver lip ring',
    37: 'Golden mouth spike',
    38: 'Silver mouth spike',
    39: 'Golden double lip ring',
    40: 'Silver double lip ring',
    41: 'Golden band',
    42: 'Silver band',
    43: 'Golden ring with ruby',
    44: 'Silver ring with ruby',
    45: 'Golden ring with amethyst',
    46: 'Silver ring with amethyst',
    47: 'Golden ring with sapphire',
    48: 'Silver ring with sapphire',
    49: 'Golden ring with turquoise',
    50: 'Silver ring with turquoise',
    51: 'Golden ring with emerald',
    52: 'Silver ring with emerald',
    53: 'Golden ring with onyx',
    54: 'Silver ring with onyx',
    55: 'Golden double band',
    56: 'Silver double band',
    57: 'Ruby lip ring',
    58: 'Onyx large ear loop',
    59: 'Sapphire eye brow ring',
    60: 'Ruby and amethyst ear stud and rings',
    61: 'Emerald double nose spike',
    62: 'Torquoise eye brow spike'}
ClothingStrings = {
    0: 'Small hat',
    1: "Large sailor's hat",
    2: 'Tied hat',
    3: 'Hat',
    4: 'Exclusive! Free skull bandana. Available only until 03/02/08!',
    5: 'Sleeveless shirt',
    6: 'Striped sleeveless shirt',
    7: 'Sleeveless shirt with suspenders',
    8: 'Fancy sleeveless shirt',
    9: 'Fancy short sleeve shirt',
    10: 'Short sleeve shirt',
    11: 'Striped short sleeve shirt',
    12: 'Long sleeve shirt',
    13: 'Fancy long sleeve shirt',
    14: 'Long sleeve button down shirt',
    15: 'Long sleeve open button down shirt',
    16: 'Plain vest',
    17: 'Large vest',
    18: 'Large long coat',
    19: 'Short coat',
    20: 'Long pants',
    21: 'Striped long pants',
    22: 'Cloth belt',
    23: 'Fancy belt',
    24: 'Plain shoes',
    25: 'Large hat with feather',
    26: 'Puffy short sleeve shirt',
    27: 'Long sleeve fancy shirt',
    28: 'Low vest',
    29: 'Cut off vest',
    30: 'Long coat',
    31: 'Shorts',
    32: 'Long skirt',
    33: 'Striped belt',
    34: 'Boots',
    35: 'Tall boots',
    36: 'Tall knee high boots',
    37: 'Large hat with feather',
    38: 'Large leather hat',
    39: "Fancy Captain's hat",
    40: 'Fancy short sleeve open shirt',
    41: 'Fancy long sleeve open shirt',
    42: 'Fancy long sleeve shirt with bowtie',
    43: 'Fancy vest with buttons',
    44: 'Large closed leather vest',
    45: 'Large closed vest with pockets',
    46: 'Fancy long vest',
    47: 'Long vest',
    48: 'Long fancy coat',
    49: 'Short fancy coat',
    50: 'Fancy striped pants',
    51: 'Fancy long pants',
    52: 'Fancy long sleeve belly shirt',
    53: 'Fancy vest',
    54: 'Fancy low cut vest',
    55: 'Fancy cut off vest',
    56: 'Tall fancy boots',
    57: 'Truehound Bandana',
    58: 'Fine Callecutter Hat',
    59: "Barbossa's Feathered Hat",
    60: 'Truehound Shirt',
    61: 'Puffy Callecutter Shirt',
    62: "Barbossa's Sleeveless Shirt",
    63: 'Callecutter Vest',
    64: "Barbossa's Closed Vest",
    65: "Barbossa's Long Coat",
    66: 'Truehound Pants',
    67: 'Long Callecutter Slacks',
    68: "Barbossa's Long Pants",
    69: 'Truehound Belt',
    70: 'Leather Callecutter Belt',
    71: "Barbossa's Belt",
    72: 'Truehound Boots',
    73: 'Tall Callecutter Boots',
    74: "Barbossa's Tall Boots",
    75: 'Truehound Bandana',
    76: 'Fine Callecutter Hat',
    77: "Barbosssa's Feathered Hat",
    78: 'Truehound Shirt',
    79: 'Puffy Callecutter Shirt',
    80: "Barbossa's Long Sleeve Shirt",
    81: 'Callecutter Vest',
    82: "Barbossa's Closed Vest",
    83: "Barbossa's Long Coat",
    84: 'Truehound Pants',
    85: 'Long Callecutter Slacks',
    86: "Barbossa's Short Pants",
    87: 'Truehound Belt',
    88: 'Leather Callecutter Belt',
    89: "Barbossa's Belt",
    90: 'Truehound Boots',
    91: 'Tall Callecutter Boots',
    92: "Barbossa's Short Boots",
    93: 'Exclusive! Free golden skull bandana. Available only until 12/07/08!'}
TattooStrings = {
    0: 'Tattoo Removal',
    1: 'Shark tattoo',
    2: 'Skull pirate tattoo',
    3: 'Skull shield tattoo',
    4: 'Skull stab tattoo',
    5: 'Snake and daggers tattoo',
    6: 'Fancy dagger tattoo',
    7: 'Skull flag tattoo',
    8: 'Fancy key tattoo',
    9: 'Skull iron cross tattoo',
    10: 'Sword and scroll tattoo',
    11: 'Dagger tattoo',
    12: 'Heart torch tattoo',
    13: 'Lock and key tattoo',
    14: 'Skull and dagger',
    15: 'Skull and crossbones tattoo',
    16: 'Anchor tattoo',
    17: 'Compass tattoo',
    18: 'Dagger and scroll tattoo',
    19: 'Ship and anchor tattoo',
    20: 'Skull and crossbones tattoo',
    21: 'Skull tattoo',
    22: 'Nautical star',
    23: 'Mayan face tattoo',
    24: 'Octopus tattoo',
    25: 'Tribal skull tattoo',
    26: 'Squid and ship tattoo',
    27: "Saint Patrick's Day tattoo",
    28: 'Native lizards tattoo',
    29: 'Tribal swirl tattoo',
    30: 'Tribal bird tattoo',
    31: 'Tribal jellyfish tattoo',
    32: 'Tribal jellyfish tattoo',
    33: 'African face tattoo',
    34: 'Maori face tattoo',
    35: 'Asian leaf tattoo',
    36: 'Ethnic tattoo',
    37: 'Maori man tattoo',
    38: 'Native leaf tattoo',
    39: 'Thai tattoo',
    40: 'Two clovers face tattoo',
    41: 'Horseshoe face tattoo',
    42: 'Celtic leaf tattoo',
    43: 'Ethnic eagle tattoo',
    44: 'Crossed flintlocks tattoo',
    45: 'Shamrock tattoo',
    46: 'Thai monkey face tattoo',
    47: 'Tribal face tattoo',
    48: 'Tribal face tattoo',
    49: 'Asian face tattoo',
    50: 'Maori face tattoo',
    51: 'Tribal design tattoo',
    52: 'Celtic knot tattoo',
    53: 'Chinese knot tattoo',
    54: 'Hawaiian tiki tattoo',
    55: 'Twin sharks tattoo',
    56: 'Tribal waves tattoo',
    57: 'Celtic deer tattoo',
    58: 'Hawaiian design tattoo',
    59: 'Petroglyph tattoo',
    60: 'Ravens tattoo',
    61: 'Wave fan tattoo',
    62: 'Hawaiian pectoral tattoo',
    63: 'Tribal yakuza tattoo',
    64: 'Jack Sparrow eye tattoo',
    65: 'Tribal cheek tattoo',
    66: 'Tribal chin tattoo',
    67: 'Tribal forehead tattoo',
    68: 'Maori chin tattoo',
    69: 'Maori nose tattoo',
    70: 'Native eye tattoo',
    71: 'Tribal goatee tattoo',
    92: "Mother's Day flower tattoo",
    95: "Mother's Day sparrow tattoo",
    96: "Classic Mother's Day tattoo",
    100: "Mother's Day face flower tattoo",
    102: "Mother's Day face hearts tattoo",
    104: 'Spanish Ship PVP Tattoo',
    105: 'French Ship PVP Tattoo',
    111: 'Octopus Tattoo',
    112: 'Healed Bullet Holes Tattoo',
    113: 'Pirate Brand Tattoo',
    114: 'Large Stitched Scar',
    115: 'Stitched Bullet Holes Tattoo',
    116: 'Large X Stitch Tattoo',
    117: 'Large Y Stitch Tattoo',
    106: 'Healed Bullet Holes Tattoo',
    107: 'Pirate Brand Tattoo',
    108: 'Large Stitched Scar',
    129: 'Stitched Bullet Holes Tattoo',
    130: 'Large X Stitch Tattoo',
    131: 'Large Y Stitch Tattoo'}
JewelryStore = 'Jewelry Store'
Jewelry = 'Jewelry'
CannonAmmoStore = 'Cannon Ammo'
Shipyard = 'Shipyard'
Submit = lSubmit
SubmitNameHelp = 'Commit the Ship Name'
Random = 'Random'
Shuffle = 'Shuffle'
RandomNameHelp = 'Make a random name'
NamePanelTitle = 'Name Your Ship'
TypeAName = 'Type'
PickAName = 'Pick'
TypeANameHelp = 'Type a Custom Name'
PickANameHelp = 'Generate a Ship Name'
TypeANameInstructions = 'Type in a custom name and submit it to the Pirate Ship Council for approval.'
AdventureTimerCancelHelp = 'Cancel the Adventure'
Timer = 'Timer'
AtSea = 'Out at Sea'
InPort = 'Docked'
InBottle = 'In Bottle'
Chartered = 'Chartered'
ShoveOff = 'Leaving Port'
LootPlundered = 'Plunder!'
SkillReady = 'Skill Ready'
ShipDisabled = 'Disabled'
Sunk = 'Sunk!'
Captain = 'Captain'
Commodore = 'Commodore'
ShipPinnedWarning = 'Ship is pinned in place!'
NotCaptainWarning = 'Must be the Captain to start Adventure!'
NotShipTeamWarning = "Not part of the Ship's Crew!"
AlreadyInUseWarning = 'Already in use!'
NoBoardingPermissionWarning = 'Must be part of Crew to board Ship!'
NoHelmPermissionWarning = 'Must be the Captain to Shove Off!'
NoBoardingCaptainReserved = 'Cannot board! Remaining space is reserved for the Captain!'
CannotRepairRepairedShipWarning = 'Ship does not need repairs!'
CannotRepairWhileWheelOccupiedWarning = 'Cannot repair while steering wheel is in use!'
IslandPlayerBarrierWarning = 'Need a Ship to enter High Seas!'
NoManaWarning = 'Not enough ' + ManaName + '!'
NotAttunedWarning = 'Must Attune Doll to a Target first!'
NeedFriendlyTarget = 'This skill must be used on an Ally!'
NeedHostileTarget = 'This skill must be used on an Enemy!'
TooFarAttuneWarning = 'Must be closer to Attune Doll!'
OutOfRangeWarning = 'Out of range!'
UnattuneAll = 'Unattune All'
OutOfAmmoWarning = 'Out of Ammo!'
AmmoChargingWarning = 'Cannot change skills while charging!'
OutOfItemWarning = 'Item is used up!'
SkillRechargingWarning = 'Skill is not finished recharging!'
TonicRechargingWarning = 'Tonic is not finished recharging!'
RepairKitRechargingWarning = 'Repair kit is not finished recharging!'
BuffPriorityWarning = 'Cannot use that skill right now!'
SpellFailedWarning = 'Spirit summoning interrupted!'
NotUsableInAirWarning = 'Skill not usable in air!'
OutOfSightWarning = 'Target is out of sight!'
NoBroadsidesWarning = 'No broadside cannons to fire!'
FullHealthWarning = 'You already have full Health!'
FullShipHealthWarning = 'Your ship does not need repairs!'
TonicHelp = 'Drink a Tonic to heal.'
UsingSkill = 'Using Skill'
FriendlyFireWarning = "Cannot damage other Player's Ships!"
CannotDockYet = 'Cannon dock under fire, try again in %s seconds!'
TeamFireWarning = 'Cannot damage your own team...'
StunWarning = 'You cannot attack while Stunned!'
SailsNotReadyWarning = 'Sails not ready yet!'
RamWhileBoardingWarning = 'Cannot ram while boarding!'
ScoreboardTitle = 'High Seas Adventure:'
AdventureResults = 'Voyage Results:'
DividingPlunder = 'Plunder & Loot:'
ShipStatus = 'Ship Status:'
PlunderShare = 'Your Plunder Share:'
RatingsTitle = 'Pirate Rating:'
UnknownGoldValue = '??? %s' % MoneyName
You = 'You'
Team = 'Team'
TotalTime = 'Total Time'
CrewRemaining = 'Shipmates Remaining'
ShipsSunk = 'Ships Sunk'
UndeadDefeated = 'Undead Defeated'
PiratesDefeated = 'Pirates Defeated'
NavyDefeated = 'Navy Defeated'
CreaturesDefeated = 'Creatures Defeated'
SeamonstersDefeated = 'Sea Monsters Defeated'
TownfolkDefeated = 'Townfolk Killed'
GoldLooted = 'Gold Looted'
CargoLooted = 'Cargo Looted'
NoCargoLooted = 'No Cargo Looted'
CaptainsBonus = "Captain's Bonus"
ShipDamage = 'Ship Damage'
ShipRepairCost = 'Repair Cost'
PayForRepairs = 'Pay for Repairs'
TotalGold = 'Total Gold Earned'
CrewRating = 'Shipmates Rating:'
Rating = 'Your Rating:'
__highSeasAdventureRating = {
    0: 'Stowaway',
    1: 'Cabinboy',
    3: 'Swabbie',
    6: 'Deckhand',
    10: 'Seaman',
    15: 'Mariner',
    20: 'Swashbuckler',
    30: 'First Mate',
    50: 'Robber Baron!'}

def getHighSeasRating(value):
    probabilityTable = __highSeasAdventureRating.keys()
    probabilityTable.sort()
    for rating in probabilityTable:
        if value <= rating:
            return __highSeasAdventureRating[rating]
    
    return __highSeasAdventureRating[rating]

__crewAdventureRating = {
    -1: 'Landlubbers',
    0: 'Sailors',
    5: 'Sea Dogs',
    10: 'Adventurers!',
    20: 'Plunderers!',
    30: 'Raiders!',
    40: 'Buccaneers!',
    50: 'Warmongers!',
    75: 'Robber Villains!',
    100: 'HighSea Terrors!'}

def getCrewRating(value):
    probabilityTable = __crewAdventureRating.keys()
    probabilityTable.sort()
    for rating in probabilityTable:
        if value <= rating:
            return __crewAdventureRating[rating]
    
    return __crewAdventureRating[rating]

CRConnecting = 'Connecting...'
CRNoConnectTryAgain = 'Could not connect to %s:%s. Try again?'
CRNoConnectProxyNoPort = 'Could not connect to %s:%s.\n\nYou are communicating to the internet via a proxy, but your proxy does not permit connections on port %s.\n\nYou must open up this port, or disable your proxy, in order to play.  If your proxy has been provided by your ISP, you must contact your ISP to request them to open up this port.'
CRLostConnection = 'Your internet connection has been unexpectedly broken.'
CRBootedReasons = {
    1: 'An unexpected problem has occurred.  Your connection has been lost, but you should be able to connect again and go right back into the game.',
    100: 'You have been disconnected because someone else just logged in using your account on another computer.',
    120: 'You have been disconnected because of a problem with your authorization to use keyboard chat.',
    122: 'There has been an unexpected problem logging you in.  Please contact customer support.',
    125: 'Your installed files appear to be invalid.  Please use the Play button on the official website to run.',
    126: 'You are not authorized to use administrator privileges.',
    151: 'You have been logged out by an administrator working on the servers.',
    153: 'The world you were playing on has been reset.  Everyone who was playing on that world has been disconnected.  However, you should be able to connect again and go right back into the game.',
    288: 'Sorry, you have used up all of your available minutes this month.',
    349: 'Sorry, you have used up all of your available minutes this month.'}
CRBootedReasonUnknownCode = 'An unexpected problem has occurred (error code %s).  Your connection has been lost, but you should be able to connect again and go right back into the game.'
CRTryConnectAgain = '\n\nTry to connect again?'
CRToontownUnavailable = 'Pirates appears to be temporarily unavailable, still trying...'
CRToontownUnavailableCancel = lCancel
CRNameCongratulations = 'CONGRATULATIONS!!'
CRNameAccepted = 'Your name has been\napproved by the Pirate Bretheren.\n\nFrom this day forth\nyou will be named\n"%s"'
CRServerConstantsProxyNoPort = 'Unable to contact %s.\n\nYou are communicating to the internet via a proxy, but your proxy does not permit connections on port %s.\n\nYou must open up this port, or disable your proxy, in order to play.  If your proxy has been provided by your ISP, you must contact your ISP to request them to open up this port.'
CRServerConstantsProxyNoCONNECT = 'Unable to contact %s.\n\nYou are communicating to the internet via a proxy, but your proxy does not support the CONNECT method.\n\nYou must enable this capability, or disable your proxy, in order to play.  If your proxy has been provided by your ISP, you must contact your ISP to request them to enable this capability.'
CRServerConstantsTryAgain = 'Unable to contact %s.\n\nThe account server might be temporarily down, or there might be some problem with your internet connection.\n\nTry again?'
CRServerDateTryAgain = 'Could not get server date from %s. Try again?'
AfkForceAcknowledgeMessage = 'Your pirate got groggy and passed out.'
PeriodTimerWarning = 'Your time limit this month is almost over!'
PeriodForceAcknowledgeMessage = 'You have used up all of your available minutes this month.  Come back and play some more next month!'
CREnteringToontown = 'Entering Pirates...'
CRAvatarListFailed = 'Failed to login and retrieve your pirates. Please restart and try again.'
FriendsListLabel = 'Friends'
FriendsPageNewFriend = 'New Friend'
FriendsPageSecrets = 'Secrets'
FriendsPageOnlineFriends = 'ONLINE\nFRIENDS'
FriendsPageAllFriends = 'ALL\nFRIENDS'
FriendsPageIgnoredFriends = 'IGNORED\nPIRATES'
FriendsPagePets = 'NEARBY\nPETS'
FriendsPageOffline = '\x01slant\x01Offline\x02'
FriendsPageOnline = '\x01slant\x01Online\x02'
FriendsPageNameText = '%(avName)s [%(playerName)s]'
FriendsPageFriendText = '%(nameText)s\n%(presenceText)s'
FriendsPagePlayerName = '[%(playerName)s]'
AvatarChooserTitle = 'Choose Yer Pirate'
AvatarChooserCreate = 'Create A Pirate'
AvatarChooserUnderConstruction = 'Under Construction'
AvatarChooserSlotUnavailable = 'Unlimited Access Only'
AvatarChooserQuit = 'Quit'
AvatarChooserOptions = 'Options'
AvatarChooserPlay = 'Play'
AvatarChooserDelete = 'Delete'
AvatarChooserShared = 'Share'
AvatarChooserLocked = 'Lock'
AvatarChooserLockedByOwner = 'Locked by Owner'
AvatarChooserAlreadyOnline = 'Already Online'
AvatarChooserConfirmDelete = 'Are you sure you want to delete %s?'
AvatarChooserConfirmShare = 'Share %s with all family member accounts?'
AvatarChooserConfirmLock = 'Lock out %s from all other family member accounts?'
AvatarChooserRejectPlayAvatar = 'Your request to play this pirate failed. Please reconnect and try again.'
OptionsPageLogout = 'Log Out'
AvatarChooserNameAccepted = 'Congratulations! Your pirate name was accepted.'
AvatarChooserPleaseRename = "We're sorry, your pirate name was not approved. Please enter a new name."
AvatarChooserNotDownload = 'Download is not yet complete.  Please wait until download is finished.'
FirstAddTitle = 'Your 7 Day Full-Screen Preview Has Ended'
PreviewTitle1 = '7 Day'
PreviewTitle2 = 'Full Screen Preview'
FirstAddDisplay = 'You can continue to play in the current framed mode with free Basic Access or you can upgrade to Unlimited Access for expanded features, including full-screen game play.'
FirstAddBasic = 'Continue In Basic Access'
FirstAddUpgrade = 'Upgrade To Unlimited Access'
VR_FirstAddBasic = 'Continue Playing'
VR_FirstAddUpgrade = 'Become A Member'
MakeAPirateDone = 'Done'
MakeAPirateCancel = lCancel
MakeAPirateNext = lNext
MakeAPirateNextAnim = '>>'
MakeAPirateLastAnim = '<<'
MakeAPirateAllAnims = 'All Anims'
MakeAPirateWait = 'Please wait...'
AnimateFrame = 'Motion'
LODFrame = 'LOD'
LODLow = 'Low'
LODMed = 'Med'
LODHi = 'Hi'
RandomButton = 'Random'
ShuffleButton = 'Shuffle'
ShuffleNextButton = 'Next'
ShufflePrevButton = 'Last'
ResetButton = 'Reset'
DoneButton = 'Finished'
BodyShapeTab = 'Shape'
BodyHeightTab = 'Height'
BodyColorTab = 'Color'
BodyShapeTabTitle = 'Pick Body Shapes'
BodyHeightTabTitle = 'Adjust Body Height'
BodyColorTabTitle = 'Pick Skin Color'
GeneratePictures = 'Take Pics'
ClothingShirtTab = 'Shirt'
ClothingPantTab = 'Pants'
ClothingShoeTab = 'Shoe'
ClothingShirtTabTitle = 'Pick Shirts'
ClothingPantTabTitle = 'Pick Pants'
ClothingSockTabTitle = 'Pick Socks'
ClothingShoeTabTitle = 'Pick Shoes'
ShapeTab = 'Shape'
MouthTab = 'Mouth'
EyesTab = 'Eyes'
NoseTab = 'Nose'
EarTab = 'Ear'
ShapeTabTitle = 'Pick Shape'
MouthTabTitle = 'Pick Mouth'
EyesTabTitle = 'Pick Eyes'
NoseTabTitle = 'Pick Nose'
EarTabTitle = 'Pick Ear'
HairTabTitle = 'Pick Hair'
ClothesFrameTitle = 'Apparel'
ShirtFrameTitle = 'Top'
PantFrameTitle = 'Bottom'
ShoeFrameTitle = 'Shoe'
BodyShortFat = '1'
BodyMediumSkinny = '2'
BodyMediumIdeal = '3'
BodyTallPear = '4'
BodyTallMuscular = '5'
CastButton = 'CastButton'
SkeletonDJ1 = 'Crash'
SkeletonDJ2 = 'Jimmyleg'
SkeletonDJ3 = 'Koleniko'
SkeletonDJ4 = 'Palifico'
SkeletonDJ5 = 'Twins'
SkeletonGP1 = 'gp1'
SkeletonGP2 = 'gp2'
SkeletonGP4 = 'gp4'
SkeletonGP8 = 'gp8'
SkeletonSP1 = 'sp1'
SkeletonSP2 = 'sp2'
SkeletonSP3 = 'sp3'
SkeletonSP4 = 'sp4'
SkeletonFR1 = 'fr1'
SkeletonFR2 = 'fr2'
SkeletonFR3 = 'fr3'
SkeletonFR4 = 'fr4'
NPCShapeTab = 'Shape'
NPCHeadTab = 'Head'
NPCColorTab = 'Color'
NPCClothesTab = 'Clothes'
NPCShapeTabTitle = 'Pick NPC Shapes'
NPCHeadTabTitle = 'Adjust NPC Height'
NPCColorTabTitle = 'Pick Skin Color'
NPCClothesTabTitle = 'Pick Clothes'
NPCShapeFrameTitle = 'NPC Shape'
NPCHeadFrameTitle = 'Pick A Head'
NPCHeadFrame = 'Head'
NPCHead = 'Head'
NPCHeadScale = 'Size'
NPCColorFrameTitle = 'Skin Color'
NPCColorFrame = 'Skin Color'
NPCClothesFrameTitle = 'Clothes'
NPCShirtFrame = 'Shirt'
NPCVestFrame = 'Vest'
NPCCoatFrame = 'Coat'
NPCPantFrame = 'Pants'
NPCShoeFrame = 'Shoe'
NPCAccFrame = 'Acc'
NPCNext = '>>'
NPCLast = '<<'
MakeAPirateClothingHatStyle = 'Hat'
MakeAPirateClothingHatTrend = 'Pattern'
MakeAPirateClothingShirtStyle = 'Shirt'
MakeAPirateClothingShirtTrend = 'Pattern'
MakeAPirateClothingVestStyle = 'Vest'
MakeAPirateClothingVestTrend = 'Pattern'
MakeAPirateClothingCoatStyle = 'Coat'
MakeAPirateClothingCoatTrend = 'Pattern'
ClothingTopColorFrameTitle = 'Shirt Color'
ClothingTopColorTitle = 'Color'
MakeAPirateClothingPantStyle = 'Pants'
MakeAPirateClothingPantTrend = 'Pattern'
MakeAPirateClothingBeltStyle = 'Belt'
MakeAPirateClothingBeltTrend = 'Pattern'
ClothingBotColorFrameTitle = 'Pants Color'
ClothingBotColorFrame = 'Color'
MakeAPirateClothingSockStyle = 'Sock'
MakeAPirateClothingSockTrend = 'Pattern'
MakeAPirateClothingShoeStyle = 'Shoe'
MakeAPirateClothingShoeTrend = 'Pattern'
MakeAPirateCoatOff = 'Coat Off'
MakeAPirateCoatOn = 'Coat On'
TempNameIssued = 'Until your name is approved, you will be given a temporary name.'
RotateSlider = 'Rotate'
ZoomSlider = 'Zoom'
AnimSpeedSlider = 'Speed'
AvHPosSlider = 'H-Pos'
AvVPosSlider = 'V-Pos'
HatFrameTitle = 'Hat'
HatColorFrameTitle = 'Hat Color'
HatColorFrame = 'Color'
HairFrameTitle = 'Hair'
HairColorFrameTitle = 'Hair Color'
HairHighLightColorFrameTitle = 'Highlight Color'
MakeAPirateHairHair = 'Hair'
MakeAPirateHairBeard = 'Beard'
MakeAPirateHairMustache = 'Mustache'
MakeAPirateHairEyeBrow = 'Eyebrow'
MakeAPirateHairColor = 'Color'
MakeAPirateMale = 'Male'
MakeAPirateFemale = 'Female'
NameFrameTitle = 'Choose Your Name'
GenderFrameTitle = 'Gender'
BodyShapeFrameTitle = 'Shape'
BodyHeightFrameTitle = 'Height'
BodyHeight = 'Height'
BodyHeadScale = 'Shape'
BodyColorFrameTitle = 'Skin Tone'
BodyColorFrame = 'Skin Color'
NoseFrameTitle = 'Nose'
NoseBridgeWidth = 'Bridge Width'
NoseNostrilWidth = 'Nostril Width'
NoseLength = 'Length'
NoseBump = 'Bump'
NoseNostrilHeight = 'Nostril Height'
NoseNostrilAngle = 'Nostril Angle'
NoseBridgeBroke = 'Bridge Deform'
NoseNostrilBroke = 'Nostril Deform'
EarFrameTitle = 'Ears'
EarScale = 'Size'
EarFlapAngle = 'Angle'
EarPosition = 'Position'
EarLobe = 'Lobe'
BodyHairFrameTitle = 'Skin'
ShapeScaleFrameTitle = 'Size'
ShapeHeadFrameTitle = 'Head Shape'
ShapeTextureFrameTitle = 'Face'
ShapeTextureFrame = 'Style'
ShapeHeadWidth = 'Width'
ShapeHeadHeight = 'Height'
ShapeHeadRoundness = 'Roundness'
ShapeJewelryLEarFrameTitle = 'Ear Left'
ShapeJewelryREarFrameTitle = 'Ear Right'
ShapeJewelryLBrowFrameTitle = 'Brow Left'
ShapeJewelryRBrowFrameTitle = 'Brow Right'
ShapeJewelryNoseFrameTitle = 'Nose'
ShapeJewelryMouthFrameTitle = 'Mouth'
ShapeJewelryLHandFrameTitle = 'Hand Left'
ShapeJewelryRHandFrameTitle = 'Hand Right'
MouthJawFrameTitle = 'Jaw'
MouthFrameTitle = 'Lips'
MouthCheekFrameTitle = 'Cheeks'
MouthTeethFrameTitle = 'Teeth'
MouthTeethFrame = 'Teeth'
MouthJawWidth = 'Width'
MouthJawRoundness = 'Roundness'
MouthJawChinAngle = 'Chin Angle'
MouthJawChinSize = 'Chin Size'
MouthJawLength = 'Length'
MouthWidth = 'Width'
MouthThickness = 'Thickness'
MouthFrown = 'Frown'
CheekBoneWidth = 'Width'
CheekBoneHeight = 'Height'
CheekFat = 'Fat'
Teeth = 'Teeth'
EyeFrameTitle = 'Eyes'
EyeBrowFrameTitle = 'Brow'
EyeBrowWidth = 'Width'
EyeBrowProtruding = 'Protruding'
EyeBrowAngle = 'Angle'
EyeBrowHeight = 'Height'
EyeCorner = 'Corner'
EyeOpeningSize = 'Opening'
EyeBulge = 'Bulge'
EyeSpacing = 'Spacing'
EyeIrisColor = 'Eye Iris Color'
EyeBloodShot = 'Eye Blood Shot'
EyesColorFrameTitle = 'Eye Color'
EyesColorFrame = 'Color'
CreateYourPirateTitle = 'Create Your Pirate'
CreateYourPirateHead = "Click the 'head' arrows to pick different animals."
PirateButton = 'Pirate'
NPCButton = 'NPC'
NavyButton = 'Navy'
CastButton = 'Cast'
PickGender = 'Click the arrows to pick gender!'
PickBody = 'Click the arrows to pick body!'
PickHead = 'Click the arrows to pick head!'
PickClothes = 'Click the arrows to pick clothes!'
PickName = 'Choose a name for your pirate!'
MakeAPiratePageNames = [
    'Body',
    'Head',
    'Mouth',
    'Eyes',
    'Nose',
    'Ear',
    'Hair',
    'Clothes',
    'Name',
    'Tattoos',
    'Jewelry']
PaintYourPirate = 'Click the arrows to paint your pirate!'
PaintYourPirateTitle = 'Paint Your Pirate'
MakeAPirateYouCanGoBack = 'You can go back to change your body too!'
InventoryCategoryNames = {
    InventoryCategory.BAD_CATEGORY: 'bad',
    InventoryCategory.MONEY: 'Money',
    InventoryCategory.WEAPONS: 'Weapons',
    InventoryCategory.INGREDIENTS: 'Voodoo Ingredients',
    InventoryCategory.CONSUMABLES: 'Consumables',
    InventoryCategory.SHIP_CANNONS: 'Ship Cannons',
    InventoryCategory.MAX_PLAYER_ATTRIBUTES: 'Max Player Attributes',
    InventoryCategory.TELEPORT_ACCESS: 'Teleport Access',
    InventoryCategory.WEAPON_SKILL_MELEE: 'Brawl Skill',
    InventoryCategory.WEAPON_SKILL_CUTLASS: 'Cutlass Skill',
    InventoryCategory.WEAPON_SKILL_PISTOL: 'Pistol Skill',
    InventoryCategory.WEAPON_SKILL_MUSKET: 'Musket Skill',
    InventoryCategory.WEAPON_SKILL_DAGGER: 'Dagger Skill',
    InventoryCategory.WEAPON_SKILL_GRENADE: 'Grenade Skill',
    InventoryCategory.WEAPON_SKILL_DOLL: 'Doll Skill',
    InventoryCategory.WEAPON_SKILL_WAND: 'Staff Skill',
    InventoryCategory.WEAPON_SKILL_KETTLE: 'Kettle Skill',
    InventoryCategory.WEAPON_SKILL_CANNON: 'Cannon Skill',
    InventoryCategory.UNSPENT_SKILL_POINTS: 'Unspent Skill Points',
    InventoryCategory.WEAPON_SKILL_ITEM: 'Weapon Skill',
    InventoryCategory.SKILL_SAILING: 'Sailing Skill',
    InventoryCategory.VITAE_PENALTY: 'Vitae Penalty',
    InventoryCategory.PLAYER_RANKING: 'Player Ranking',
    InventoryCategory.KEY_ITEMS: 'Key Items',
    InventoryCategory.QUEST_SLOTS: 'Quest Slots',
    InventoryCategory.ACCUMULATORS: 'Accumulators',
    InventoryCategory.REPAIR_TOKENS: 'Repair Tokens',
    InventoryCategory.WEAPON_PISTOL_AMMO: 'Pistol Ammo',
    InventoryCategory.WEAPON_MUSKET_AMMO: 'Musket Ammo',
    InventoryCategory.WEAPON_GRENADE_AMMO: 'Grenade Ammo',
    InventoryCategory.WEAPON_CANNON_AMMO: 'Cannon Ammo',
    InventoryCategory.WEAPON_DAGGER_AMMO: 'Dagger Ammo',
    InventoryCategory.CARDS: 'Cards',
    InventoryCategory.CLOTHING: 'Clothing',
    InventoryCategory.PETS: 'Pets',
    InventoryCategory.FURNITURE: 'Furniture',
    InventoryCategory.SHIPS: 'Ships',
    InventoryCategory.SHIP_ACCESSORIES: 'Ship Accessories',
    InventoryCategory.FLAGS: 'Flags',
    InventoryCategory.COLLECTIONS: 'Collections',
    InventoryCategory.TELEPORT_TOKENS: 'Teleport Tokens',
    InventoryCategory.FISH_CAUGHT: 'Fish Caught',
    InventoryCategory.QUESTS: 'Quests',
    InventoryCategory.WAGERS: 'Wagers',
    InventoryCategory.TREASURE_MAPS: 'Treasure Maps',
    InventoryCategory.TRASH: 'trash'}
BuffPoison = 'ACID \n Acid damage over time \n'
BuffAcid = 'VENOM \n Poison damage over time \n'
BuffWound = 'WOUNDED \n Health decay over time \n'
BuffHold = 'SNARE \n Locks victim movement \n'
BuffOnFire = 'BURN \n Fire damage over time \n'
BuffStun = 'STUN \n Cannot move or attack \n'
BuffUnstun = 'STUN IMMUNE \n Immune to Stun \n'
BuffVoodooStunLock = 'ATTUNEMENT LOCK \n Attunements cannot be broken \n'
BuffSlow = 'SLOW \n Slowed movement \n'
BuffBlind = 'BLIND \n Hindered sight \n'
BuffCurse = 'CURSED \n Increases damage taken \n'
BuffHasten = 'HASTEN \n Speed increase \n'
BuffTaunt = 'PROVOKED \n Accuracy lowered \n'
BuffWeaken = 'WEAKEN \n Decreased attack power! \n'
BuffSpawn = 'SPAWNING \n Temporary spawning invulnerability! \n'
BuffRegen = 'REGENERATION \n Regain lost health over time \n'
BuffAttune = 'ATTUNED \n A Voodoo Doll is attuned to you! \n'
BuffFullSail = 'FULL SAIL \n Full Speed Ahead! \n'
BuffComeAbout = 'COME ABOUT \n Ship Tacking Maneuver \n'
BuffOpenFire = 'OPEN FIRE \n Increases Cannon Damage \n'
BuffRam = 'RAMMING SPEED \n Ramming Maneuver \n'
BuffTakeCover = 'TAKE COVER \n Decreases Damage Take by Shipmates \n'
BuffPowerRecharge = 'LEADERSHIP \n Increases the rate of recharge for sailing skills and cannons \n'
BuffDuration = ' Duration: %s seconds'
CrewBuffCaptainOrder = "Captain's Orders:"
CrewBuffTakeCover = 'Shipmates immune\nto damage! Ship takes \n%s%% less damage!'
CrewBuffOpenFire = '+%s%% Damage Bonus for\nCannons & Broadsides!'
CrewBuffTakeCoverString = 'Take Cover!'
CrewBuffOpenFireString = 'Open Fire!'
DiceText_Wait = 'Waiting for Players'
DiceText_isTurn = "'s Turn"
DiceText_Wins = ' Wins'
DiceText_Roll = ' is Rolling'
DiceText_LowBet = 'You Must Exceed Prior Claim'
DiceText_Caught = '%s Caught Cheating'
DiceText_FirstClaim = 'You Must Make the First Claim'
DiceText_Call = '%s Calls Bluff'
DiceText_Ante = 'ANTE: '
DiceText_DiceUp_Chat = [
    'Higher than that',
    'Up ye vermin!',
    'Perhaps some more',
    'Up we go']
DiceText_DiceUp_Size = len(DiceText_DiceUp_Chat) - 1
DiceText_DiceDown_Chat = [
    'Whoa, too high',
    'Maybe a wee bit less',
    'Not so much then']
DiceText_DiceDown_Size = len(DiceText_DiceDown_Chat) - 1
DiceText_Roll_Chat = [
    'Gimme a winner!',
    'No tricks now you scamps!',
    'Something good',
    "C'mon, show me the gold.",
    "Don't you be making me mad now"]
DiceText_Roll_Size = len(DiceText_Roll_Chat) - 1
ShipClassNames = {
    ShipGlobals.DINGHY: 'Dinghy',
    ShipGlobals.WARSHIPL1: 'Light Frigate',
    ShipGlobals.WARSHIPL2: 'Frigate',
    ShipGlobals.WARSHIPL3: 'War Frigate',
    ShipGlobals.WARSHIPL4: 'Command Frigate',
    ShipGlobals.MERCHANTL1: 'Light Galleon',
    ShipGlobals.MERCHANTL2: 'Galleon',
    ShipGlobals.MERCHANTL3: 'War Galleon',
    ShipGlobals.MERCHANTL4: 'Command Galleon',
    ShipGlobals.INTERCEPTORL1: 'Light Sloop',
    ShipGlobals.INTERCEPTORL2: 'Sloop',
    ShipGlobals.INTERCEPTORL3: 'War Sloop',
    ShipGlobals.INTERCEPTORL4: 'Command Sloop',
    'AnyLargeShip': 'Galleon or Frigate',
    'AnyWarShip': 'Frigate',
    'AnyL7PlusShip': 'Level 7+ ship',
    'AnyL7PlusNavyShip': 'Level 7+ Navy ship',
    'AnyL9PlusShip': 'Level 9+ ship',
    'AnyL9PlusNavyShip': 'Level 9+ Navy ship',
    'AnyL13PlusShip': 'Level 13+ ship',
    'AnyL13PlusNavyShip': 'Level 13+ Navy ship',
    'AnyEITCSeaViper': 'Sea Viper',
    'AnyEITCMarauder': 'Marauder',
    'AnyEITCBarracuda': 'Barracuda',
    'AnyEITCCorvette': 'Corvette',
    'AnyFrenchShadowCrow': 'French Shadow Crow',
    'AnyFrenchHellhound': 'French Cerberus',
    'AnyFrenchBloodScourge': 'French Blood Scourge',
    'AnySpanishShadowCrow': 'Spanish Shadow Crow',
    'AnySpanishHellhound': 'Spanish Cerberus',
    'AnySpanishBloodScourge': 'Spanish Blood Scourge',
    ShipGlobals.SKEL_WARSHIPL3: 'War Frigate',
    ShipGlobals.SKEL_INTERCEPTORL3: 'War Sloop',
    ShipGlobals.BLACK_PEARL: 'Legendary Ship',
    ShipGlobals.FLYING_DUTCHMAN: 'Legendary Ship',
    ShipGlobals.STUMPY_SHIP: 'Light Sloop',
    ShipGlobals.GOLIATH: 'The Goliath',
    ShipGlobals.NAVY_FERRET: 'Navy Ferret',
    ShipGlobals.NAVY_GREYHOUND: 'Navy Greyhound',
    ShipGlobals.NAVY_KINGFISHER: 'Navy Kingfisher',
    ShipGlobals.NAVY_PREDATOR: 'Navy Predator',
    ShipGlobals.NAVY_BULWARK: 'Navy Bulwark',
    ShipGlobals.NAVY_VANGUARD: 'Navy Vanguard',
    ShipGlobals.NAVY_MONARCH: 'Navy Monarch',
    ShipGlobals.NAVY_COLOSSUS: 'Navy Colossus',
    ShipGlobals.NAVY_PANTHER: 'Navy Panther',
    ShipGlobals.NAVY_CENTURION: 'Navy Centurion',
    ShipGlobals.NAVY_MAN_O_WAR: 'Navy Man-O-War',
    ShipGlobals.NAVY_DREADNOUGHT: 'Navy Dreadnought',
    ShipGlobals.EITC_SEA_VIPER: 'EITC Sea Viper',
    ShipGlobals.EITC_BLOODHOUND: 'EITC Bloodhound',
    ShipGlobals.EITC_BARRACUDA: 'EITC Barracuda',
    ShipGlobals.EITC_CORSAIR: 'EITC Corsair',
    ShipGlobals.EITC_SENTINEL: 'EITC Sentinel',
    ShipGlobals.EITC_IRONWALL: 'EITC Ironwall',
    ShipGlobals.EITC_OGRE: 'EITC Ogre',
    ShipGlobals.EITC_BEHEMOTH: 'EITC Behemoth',
    ShipGlobals.EITC_CORVETTE: 'EITC Corvette',
    ShipGlobals.EITC_MARAUDER: 'EITC Marauder',
    ShipGlobals.EITC_WARLORD: 'EITC Warlord',
    ShipGlobals.EITC_JUGGERNAUT: 'EITC Juggernaut',
    ShipGlobals.SKEL_PHANTOM: 'Phantom',
    ShipGlobals.SKEL_REVENANT: 'Revenant',
    ShipGlobals.SKEL_STORM_REAPER: 'Storm Reaper',
    ShipGlobals.SKEL_BLACK_HARBINGER: 'Black Harbinger',
    ShipGlobals.SKEL_DEATH_OMEN: 'Death Omen',
    ShipGlobals.SKEL_SHADOW_CROW_FR: 'French Shadow Crow',
    ShipGlobals.SKEL_HELLHOUND_FR: 'French Cerberus',
    ShipGlobals.SKEL_BLOOD_SCOURGE_FR: 'French Blood Scourge',
    ShipGlobals.SKEL_SHADOW_CROW_SP: 'Spanish Shadow Crow',
    ShipGlobals.SKEL_HELLHOUND_SP: 'Spanish Cerberus',
    ShipGlobals.SKEL_BLOOD_SCOURGE_SP: 'Spanish Blood Scourge'}
InventoryTypeNames = {
    InventoryType.GoldInPocket: 'Gold in Pocket',
    InventoryType.GoldWagered: 'Gold Wagered',
    InventoryType.NewPlayerToken: 'New Player Token',
    InventoryType.MeleeWeaponL1: 'Fists',
    InventoryType.MeleeWeaponL2: 'Brass Knuckle',
    InventoryType.MeleeWeaponL3: 'Spiked Knuckle',
    InventoryType.MeleeWeaponL4: 'Fists',
    InventoryType.MeleeWeaponL5: 'Brass Knuckle',
    InventoryType.MeleeWeaponL6: 'Spiked Knuckle',
    InventoryType.CutlassWeaponL1: 'Rusty Cutlass',
    InventoryType.CutlassWeaponL2: 'Iron Cutlass',
    InventoryType.CutlassWeaponL3: 'Steel Cutlass',
    InventoryType.CutlassWeaponL4: 'Fine Cutlass',
    InventoryType.CutlassWeaponL5: 'Pirate Blade',
    InventoryType.CutlassWeaponL6: 'Dark Cutlass',
    InventoryType.PistolWeaponL1: 'Flintlock Pistol',
    InventoryType.PistolWeaponL2: 'Double-Barrel',
    InventoryType.PistolWeaponL3: 'Tri-Barrel',
    InventoryType.PistolWeaponL4: 'Heavy Tri-Barrel',
    InventoryType.PistolWeaponL5: 'Grand Pistol',
    InventoryType.PistolWeaponL6: 'Quad-Barrel',
    InventoryType.BayonetWeaponL1: 'Rusty Bayonet',
    InventoryType.BayonetWeaponL2: 'Navy Bayonet',
    InventoryType.BayonetWeaponL3: 'War Bayonet',
    InventoryType.MusketWeaponL1: 'Rusty Musket',
    InventoryType.MusketWeaponL2: 'Brass Musket',
    InventoryType.MusketWeaponL3: 'Iron Musket',
    InventoryType.DaggerWeaponL1: 'Dagger',
    InventoryType.DaggerWeaponL2: 'Battle Dirk',
    InventoryType.DaggerWeaponL3: 'Main Gauche',
    InventoryType.DaggerWeaponL4: 'Coltello',
    InventoryType.DaggerWeaponL5: 'Bloodletter',
    InventoryType.DaggerWeaponL6: 'Slicer',
    InventoryType.GrenadeWeaponL1: 'Grenades',
    InventoryType.GrenadeWeaponL2: 'Grenades Lvl2',
    InventoryType.GrenadeWeaponL3: 'Grenades Lvl3',
    InventoryType.GrenadeWeaponL4: 'Grenades Lvl4',
    InventoryType.GrenadeWeaponL5: 'Grenades Lvl5',
    InventoryType.GrenadeWeaponL6: 'Grenades Lvl6',
    InventoryType.DollWeaponL1: 'Voodoo Doll',
    InventoryType.DollWeaponL2: 'Cloth Doll',
    InventoryType.DollWeaponL3: 'Witch Doll',
    InventoryType.DollWeaponL4: 'Pirate Doll',
    InventoryType.DollWeaponL5: 'Taboo Doll',
    InventoryType.DollWeaponL6: 'Mojo Doll',
    InventoryType.WandWeaponL1: 'Cursed Staff',
    InventoryType.WandWeaponL2: 'Warped Staff',
    InventoryType.WandWeaponL3: 'Rend Staff',
    InventoryType.WandWeaponL4: 'Harrow Staff',
    InventoryType.WandWeaponL5: 'Vile Staff',
    InventoryType.WandWeaponL6: 'Dire Staff',
    InventoryType.KettleWeaponL1: 'Kettle',
    InventoryType.KettleWeaponL2: 'Cauldron',
    InventoryType.KettleWeaponL3: 'Black Kettle',
    InventoryType.AppleIngredient: 'Apples',
    InventoryType.Potion1: 'Tonic',
    InventoryType.Potion2: 'Remedy',
    InventoryType.Potion3: 'Holy Water',
    InventoryType.Potion4: 'Elixir',
    InventoryType.Potion5: 'Miracle Water',
    InventoryType.ShipRepairKit: 'Ship Repair Kit',
    InventoryType.PorkChunk: 'Roast Pork',
    InventoryType.CannonL1: 'Rusty Cannon',
    InventoryType.CannonL2: 'Iron Cannon',
    InventoryType.CannonL3: 'Gatling Cannon',
    InventoryType.Hp: 'Max HP',
    InventoryType.Mojo: 'Max Voodoo',
    InventoryType.TeleportHome: 'TeleportHome',
    InventoryType.TeleportGuildIsland: 'TeleportGuildIsland',
    InventoryType.MeleeJab: 'Jab',
    InventoryType.MeleePunch: 'Punch',
    InventoryType.MeleeKick: 'Kick',
    InventoryType.MeleeRoundhouse: 'Roundhouse',
    InventoryType.MeleeHeadbutt: 'Headbutt',
    InventoryType.MeleeHaymaker: 'Haymaker',
    InventoryType.MeleeThrowDirt: 'Throw Dirt',
    InventoryType.MeleeToughness: 'Toughness',
    InventoryType.MeleeIronSkin: 'Iron Skin',
    InventoryType.MeleeDetermination: 'Determination',
    InventoryType.CutlassHack: 'Hack',
    InventoryType.CutlassSlash: 'Slash',
    InventoryType.CutlassStab: 'Thrust',
    InventoryType.CutlassFlourish: 'Flourish',
    InventoryType.CutlassCleave: 'Cleave',
    InventoryType.CutlassParry: 'Parry',
    InventoryType.CutlassEndurance: 'Endurance',
    InventoryType.CutlassTaunt: 'Taunt',
    InventoryType.CutlassBrawl: 'Brawl',
    InventoryType.CutlassSweep: 'Sweep',
    InventoryType.CutlassBladestorm: 'Blade Storm',
    InventoryType.PistolShoot: 'Shoot',
    InventoryType.PistolTakeAim: 'Take Aim',
    EnemySkills.PISTOL_CHARGE: 'Take Aim',
    EnemySkills.PISTOL_RELOAD: 'Reload',
    EnemySkills.SERPENT_VENOM: 'Venom Spit',
    InventoryType.PistolEagleEye: 'Eagle Eye',
    InventoryType.PistolDodge: 'Dodge',
    InventoryType.PistolSharpShooter: 'Sharp Shooter',
    InventoryType.PistolLeadShot: 'Lead Shot',
    InventoryType.PistolBaneShot: 'Bane Shot',
    InventoryType.PistolSilverShot: 'Silver Shot',
    InventoryType.PistolHexEaterShot: 'Hex Eater Shot',
    InventoryType.PistolSteelShot: 'Steel Shot',
    InventoryType.PistolVenomShot: 'Venom Shot',
    InventoryType.BayonetShoot: 'Shoot',
    InventoryType.BayonetStab: 'Bayonet Stab',
    InventoryType.BayonetRush: 'Bayonet Rush',
    InventoryType.BayonetBash: 'Bayonet Bash',
    InventoryType.MusketShoot: 'Shoot',
    InventoryType.MusketTakeAim: 'Take Aim',
    InventoryType.MusketDeadeye: 'Deadeye',
    InventoryType.MusketEagleEye: 'Eagle Eye',
    InventoryType.MusketCrackShot: 'Crack Shot',
    InventoryType.MusketMarksman: 'Marksman',
    InventoryType.MusketLeadShot: 'Lead Shot',
    InventoryType.MusketScatterShot: 'Scatter Shot',
    InventoryType.MusketCursedShot: 'Cursed Shot',
    InventoryType.MusketCoalfireShot: 'Coalfire Shot',
    InventoryType.MusketHeavySlug: 'Heavy Slug',
    InventoryType.MusketExploderShot: 'Exploder Shot',
    InventoryType.DaggerCut: 'Cut',
    InventoryType.DaggerGouge: 'Gouge',
    InventoryType.DaggerSwipe: 'Swipe',
    InventoryType.DaggerEviscerate: 'Eviscerate',
    InventoryType.DaggerFinesse: 'Finesse',
    InventoryType.DaggerBladeInstinct: 'Blade Instinct',
    InventoryType.DaggerAsp: 'Asp',
    InventoryType.DaggerAdder: 'Adder',
    InventoryType.DaggerThrowDirt: 'Throw Dirt',
    InventoryType.DaggerSidewinder: 'Sidewinder',
    InventoryType.DaggerViperNest: "Viper's Nest",
    InventoryType.SailBroadsideLeft: 'Left Broadside',
    InventoryType.SailBroadsideRight: 'Right Broadside',
    InventoryType.SailFullSail: 'Full Sail',
    InventoryType.SailComeAbout: 'Come About',
    InventoryType.SailOpenFire: 'Open Fire!',
    InventoryType.SailRammingSpeed: 'Ramming Speed',
    InventoryType.SailTakeCover: 'Take Cover!',
    InventoryType.SailPowerRecharge: 'Leadership',
    InventoryType.SailWindcatcher: 'Windcatcher',
    InventoryType.SailTacking: 'Tacking',
    InventoryType.SailTreasureSense: 'Treasure Sense',
    InventoryType.SailTaskmaster: 'Taskmaster',
    InventoryType.GrenadeThrow: 'Throw',
    InventoryType.GrenadeExplosion: 'Explosive',
    InventoryType.GrenadeShockBomb: 'Stink Pot',
    InventoryType.GrenadeFireBomb: 'Fire Bomb',
    InventoryType.GrenadeSmokeCloud: 'Smoke Bomb',
    InventoryType.GrenadeSiege: 'Siege Charge',
    InventoryType.GrenadeDetermination: 'Determination',
    InventoryType.GrenadeLongVolley: 'Long Volley',
    InventoryType.GrenadeDemolitions: 'Demolitions',
    InventoryType.GrenadeToughness: 'Toughness',
    InventoryType.GrenadeIgnorePain: 'Ignore Pain',
    EnemySkills.GRENADE_RELOAD: 'Reload',
    EnemySkills.GRENADE_CHARGE: 'Long Volley',
    InventoryType.DollAttune: 'Attune Doll',
    EnemySkills.DOLL_UNATTUNE: 'Unattune Doll',
    EnemySkills.DOLL_POKE2: 'Poke',
    InventoryType.DollPoke: 'Poke',
    InventoryType.DollSwarm: 'Swarm',
    InventoryType.DollHeal: 'Heal',
    InventoryType.DollBurn: 'Scorch',
    InventoryType.DollShackles: 'Grave Shackles',
    InventoryType.DollCure: 'Cure',
    InventoryType.DollCurse: 'Curse',
    InventoryType.DollLifeDrain: 'Life Drain',
    InventoryType.DollFocus: 'Focus',
    InventoryType.DollSpiritWard: 'Spirit Ward',
    EnemySkills.STAFF_WITHER_CHARGE: 'Casting',
    EnemySkills.STAFF_SOULFLAY_CHARGE: 'Casting',
    EnemySkills.STAFF_PESTILENCE_CHARGE: 'Casting',
    EnemySkills.STAFF_HELLFIRE_CHARGE: 'Casting',
    EnemySkills.STAFF_BANISH_CHARGE: 'Casting',
    EnemySkills.STAFF_DESOLATION_CHARGE: 'Casting',
    EnemySkills.STAFF_FIZZLE: 'Fizzled',
    InventoryType.StaffBlast: 'Blast',
    InventoryType.StaffWither: 'Wither',
    InventoryType.StaffSoulFlay: 'Soul Flay',
    InventoryType.StaffPestilence: 'Pestilence',
    InventoryType.StaffHellfire: 'Flaming Skull',
    InventoryType.StaffBanish: 'Banish',
    InventoryType.StaffDesolation: 'Desolation',
    InventoryType.StaffConcentration: 'Concentration',
    InventoryType.StaffSpiritLore: 'Spirit Lore',
    InventoryType.StaffConservation: 'Conservation',
    InventoryType.StaffSpiritMastery: 'Spirit Mastery',
    InventoryType.CannonShoot: 'Shoot',
    InventoryType.CannonRoundShot: 'Round Shot',
    InventoryType.CannonChainShot: 'Chain Shot',
    InventoryType.CannonExplosive: 'Explosive',
    InventoryType.CannonBullet: 'Bullet',
    InventoryType.CannonGasCloud: 'Gas Cloud',
    InventoryType.CannonGrapeShot: 'Grape Shot',
    InventoryType.CannonSkull: 'Skull Ammo',
    InventoryType.CannonFirebrand: 'Firebrand',
    InventoryType.CannonFlameCloud: 'Flame Cloud',
    InventoryType.CannonFlamingSkull: 'Firebrand',
    InventoryType.CannonBarShot: 'Bar Shot',
    InventoryType.CannonKnives: 'Knives',
    InventoryType.CannonMine: 'Mine',
    InventoryType.CannonBarnacles: 'Barnacles',
    InventoryType.CannonThunderbolt: 'Thunderbolt',
    InventoryType.CannonFury: 'Fury',
    InventoryType.CannonComet: 'Comet',
    InventoryType.CannonGrappleHook: 'Grapple Hook',
    InventoryType.CannonRapidReload: 'Rapid Reload',
    InventoryType.CannonBarrage: 'Barrage',
    InventoryType.CannonShrapnel: 'Shrapnel',
    InventoryType.UseItem: 'Use Item',
    EnemySkills.CLAW_RAKE: 'Claw Rake',
    EnemySkills.CLAW_STRIKE: 'Claw Strike',
    EnemySkills.DUAL_CLAW: 'Dual Claw',
    EnemySkills.POISON_VOMIT: 'Poison Vomit',
    EnemySkills.GROUND_SLAP: 'Ground Slap',
    EnemySkills.ENSNARE: 'Ensnare',
    EnemySkills.CONSTRICT: 'Constrict',
    EnemySkills.PILEDRIVER: 'Piledriver',
    EnemySkills.POUND: 'Pound',
    EnemySkills.SQUASH: 'Squash',
    EnemySkills.STUMP_KICK: 'Lunge Kick',
    EnemySkills.STUMP_KICK_RIGHT: 'Kick',
    EnemySkills.STUMP_SLAP_LEFT: 'Smash Left',
    EnemySkills.STUMP_SLAP_RIGHT: 'Smash Right',
    EnemySkills.STUMP_SWAT_LEFT: 'Swat Left',
    EnemySkills.STUMP_SWAT_RIGHT: 'Swat Right',
    EnemySkills.STUMP_STOMP: 'Earthquake',
    EnemySkills.FLYTRAP_ATTACK_A: 'Bite',
    EnemySkills.FLYTRAP_ATTACK_JAB: 'Jab',
    EnemySkills.FLYTRAP_LEFT_FAKE: 'Left Fake',
    EnemySkills.FLYTRAP_RIGHT_FAKE: 'Right Fake',
    EnemySkills.FLYTRAP_SPIT: 'Venom Spit',
    EnemySkills.SCORPION_ATTACK_LEFT: 'Left Pincer',
    EnemySkills.SCORPION_ATTACK_RIGHT: 'Right Pincer',
    EnemySkills.SCORPION_ATTACK_BOTH: 'Dual Pincer',
    EnemySkills.SCORPION_ATTACK_TAIL_STING: 'Tail Sting',
    EnemySkills.SCORPION_PICK_UP_HUMAN: 'Pickup',
    EnemySkills.SCORPION_REAR_UP: 'Rearup',
    EnemySkills.ALLIGATOR_ATTACK_LEFT: 'Bite',
    EnemySkills.ALLIGATOR_ATTACK_RIGHT: 'Bite',
    EnemySkills.ALLIGATOR_ATTACK_STRAIGHT: 'Bite',
    EnemySkills.ALLIGATOR_CRUSH: 'Crushing Bite',
    EnemySkills.ALLIGATOR_MAIM: 'Maim',
    EnemySkills.BAT_ATTACK_LEFT: 'Bite',
    EnemySkills.BAT_ATTACK_RIGHT: 'Talon Rake',
    EnemySkills.BAT_SHRIEK: 'Shriek',
    EnemySkills.BAT_FLURRY: 'Bat Flurry',
    EnemySkills.WASP_ATTACK: 'Sting',
    EnemySkills.WASP_ATTACK_LEAP: 'Sting',
    EnemySkills.WASP_POISON_STING: 'Poison Sting',
    EnemySkills.WASP_PAIN_BITE: 'Paralyzing Sting',
    EnemySkills.LEFT_BROADSIDE: 'Left Broadside',
    EnemySkills.RIGHT_BROADSIDE: 'Right Broadside',
    EnemySkills.CUTLASS_CHOP: 'Savage Blow',
    EnemySkills.CUTLASS_DOUBLESLASH: 'Double Cut',
    EnemySkills.CUTLASS_LUNGE: 'Lunge',
    EnemySkills.CUTLASS_STAB: 'Stab',
    EnemySkills.CUTLASS_ROLLTHRUST: 'Rolling Thrust',
    EnemySkills.CUTLASS_COMBOA: 'Coupe de Grace',
    EnemySkills.CUTLASS_WILDSLASH: 'Wild Swing',
    EnemySkills.CUTLASS_FLURRY: 'Flurry',
    EnemySkills.CUTLASS_RIPOSTE: 'Riposte',
    EnemySkills.DAGGER_THROW_KNIFE: 'Throwing Blade',
    EnemySkills.DAGGER_THROW_VENOMBLADE: 'Venom Blade',
    EnemySkills.DAGGER_THROW_BARBED: 'Crippling Blade',
    EnemySkills.DAGGER_THROW_INTERRUPT: 'Stinging Blade',
    EnemySkills.FOIL_FLECHE: 'Foil Fleche',
    EnemySkills.FOIL_REPRISE: 'Foil Reprise',
    EnemySkills.FOIL_SWIPE: 'Foil Swipe',
    EnemySkills.FOIL_IMPALE: 'Foil Impale',
    EnemySkills.FOIL_REMISE: 'Foil Remise',
    EnemySkills.FOIL_BALESTRAKICK: 'Foil Balestra Kick',
    EnemySkills.FOIL_CADENCE: 'Foil Cadence',
    EnemySkills.DUALCUTLASS_COMBINATION: 'Dual Cutlass Combintation',
    EnemySkills.DUALCUTLASS_SPIN: 'Dual Cutlass Spin',
    EnemySkills.DUALCUTLASS_BARRAGE: 'Dual Cutlass Barrage',
    EnemySkills.DUALCUTLASS_XSLASH: 'Dual Cutlass X-Slash',
    EnemySkills.DUALCUTLASS_GORE: 'Dual Cutlass Gore',
    InventoryType.Dinghy: 'Dinghy',
    InventoryType.NewShipToken: 'New Ship Token',
    InventoryType.NewWeaponToken: 'New Weapon Token',
    InventoryType.SmallBottle: 'Small Ship Bottle',
    InventoryType.MediumBottle: 'Medium Ship Bottle',
    InventoryType.LargeBottle: 'Large Ship Bottle',
    InventoryType.CutlassToken: 'Cutlass Token',
    InventoryType.PistolToken: 'Pistol Token',
    InventoryType.MusketToken: 'Musket Token',
    InventoryType.DaggerToken: 'Dagger Token',
    InventoryType.GrenadeToken: 'Grenade Token',
    InventoryType.WandToken: 'Wand Token',
    InventoryType.DollToken: 'Doll Token',
    InventoryType.KettleToken: 'Kettle Token',
    InventoryType.OpenQuestSlot: 'Open Quest Slot',
    InventoryType.OverallRep: 'Notoriety',
    InventoryType.GeneralRep: 'General',
    InventoryType.MeleeRep: 'Brawl',
    InventoryType.CutlassRep: 'Cutlass',
    InventoryType.PistolRep: 'Pistol',
    InventoryType.MusketRep: 'Musket',
    InventoryType.DaggerRep: 'Dagger',
    InventoryType.GrenadeRep: 'Grenade',
    InventoryType.DollRep: 'Doll',
    InventoryType.WandRep: 'Staff',
    InventoryType.KettleRep: 'Kettle',
    InventoryType.CannonRep: 'Cannon',
    InventoryType.LockpickRep: 'Lockpick',
    InventoryType.MonsterRep: 'Monster',
    InventoryType.SailingRep: 'Sailing',
    InventoryType.GamblingRep: 'Gambling',
    InventoryType.UnspentMelee: 'Melee Skill Point',
    InventoryType.UnspentCutlass: 'Cutlass Skill Point',
    InventoryType.UnspentPistol: 'Pistol Skill Point',
    InventoryType.UnspentMusket: 'Musket Skill Point',
    InventoryType.UnspentDagger: 'Dagger Skill Point',
    InventoryType.UnspentGrenade: 'Grenade Skill Point',
    InventoryType.UnspentWand: 'Wand Skill Point',
    InventoryType.UnspentDoll: 'Doll Skill Point',
    InventoryType.UnspentKettle: 'Kettle Skill Point',
    InventoryType.UnspentCannon: 'Cannon Skill Point',
    InventoryType.UnspentSailing: 'Sailing Skill Point',
    InventoryType.Vitae_Level: 'Vitae Level',
    InventoryType.Vitae_Cost: 'Vitae Cost',
    InventoryType.Vitae_Left: 'Vitae Left',
    InventoryType.ShipRepairToken: 'Ship Repair Token',
    InventoryType.PlayerHealToken: 'Player Heal Token',
    InventoryType.PlayerMojoHealToken: 'Player Mojo Heal Token',
    InventoryType.AmmoLeadShot: 'Lead Shot',
    InventoryType.AmmoBaneShot: 'Bane Shot',
    InventoryType.AmmoSilverShot: 'Silver Shot',
    InventoryType.AmmoHexEaterShot: 'Hex Eater Shot',
    InventoryType.AmmoSteelShot: 'Steel Shot',
    InventoryType.AmmoVenomShot: 'Venom Shot',
    InventoryType.AmmoAsp: 'Throwing Knife',
    InventoryType.AmmoAdder: 'Venom Dagger',
    InventoryType.AmmoSidewinder: 'Sidewinder',
    InventoryType.AmmoViperNest: 'Viper Brace',
    InventoryType.AmmoScatterShot: 'Scatter Shot',
    InventoryType.AmmoCursedShot: 'Cursed Shot',
    InventoryType.AmmoCoalfireShot: 'Coalfire Shot',
    InventoryType.AmmoHeavySlug: 'Heavy Slug',
    InventoryType.AmmoExploderShot: 'Exploder Shot',
    InventoryType.AmmoGrenadeExplosion: 'Explosive',
    InventoryType.AmmoGrenadeFlame: 'Flame Burst',
    InventoryType.AmmoGrenadeShockBomb: 'Stink Pot',
    InventoryType.AmmoGrenadeSmoke: 'Smoke Cloud',
    InventoryType.AmmoGrenadeLandMine: 'Land Mine',
    InventoryType.AmmoGrenadeSiege: 'Siege Charge',
    InventoryType.AmmoRoundShot: 'Round Shot',
    InventoryType.AmmoChainShot: 'Chain Shot',
    InventoryType.AmmoExplosive: 'Explosive',
    InventoryType.AmmoBullet: 'Bullet',
    InventoryType.AmmoGasCloud: 'Gas Cloud',
    InventoryType.AmmoGrapeShot: 'Grape Shot',
    InventoryType.AmmoSkull: 'Skull',
    InventoryType.AmmoFirebrand: 'Firebrand',
    InventoryType.AmmoFlameCloud: 'Flame Cloud',
    InventoryType.AmmoFlamingSkull: 'Flaming Skull',
    InventoryType.AmmoBarShot: 'Bar Shot',
    InventoryType.AmmoKnives: 'Knives',
    InventoryType.AmmoMine: 'Mines',
    InventoryType.AmmoBarnacles: 'Barnacles',
    InventoryType.AmmoThunderbolt: 'Thunderbolt',
    InventoryType.AmmoFury: 'Fury',
    InventoryType.AmmoComet: 'Comet',
    InventoryType.AmmoGrappleHook: 'Grappling Hook',
    InventoryType.PistolPouchL1: 'Small Pouch',
    InventoryType.PistolPouchL2: 'Medium Pouch',
    InventoryType.PistolPouchL3: 'Large Pouch',
    InventoryType.DaggerPouchL1: 'Small Belt',
    InventoryType.DaggerPouchL2: 'Medium Belt',
    InventoryType.DaggerPouchL3: 'Large Belt',
    InventoryType.GrenadePouchL1: 'Small Sack',
    InventoryType.GrenadePouchL2: 'Medium Sack',
    InventoryType.GrenadePouchL3: 'Large Sack',
    InventoryType.CannonPouchL1: 'Small Barrel',
    InventoryType.CannonPouchL2: 'Medium Barrel',
    InventoryType.CannonPouchL3: 'Large Barrel',
    InventoryType.CTFGame: 'CTFGame',
    InventoryType.CTLGame: 'CTLGame',
    InventoryType.PTRGame: 'PTRGame',
    InventoryType.BTLGame: 'BTLGame',
    InventoryType.TBTGame: 'TBTGame',
    InventoryType.SBTGame: 'SBTGame',
    InventoryType.ARMGame: 'ARMGame',
    InventoryType.TKPGame: 'TKPGame',
    InventoryType.BTBGame: 'BTBGame',
    InventoryType.PokerGame: 'PokerGame',
    InventoryType.BlackjackGame: 'BlackjackGame',
    InventoryType.ShipPVPRank: 'Ship PVP',
    ItemId.INTERCEPTOR_L1: ShipClassNames.get(ShipGlobals.INTERCEPTORL1),
    ItemId.INTERCEPTOR_L2: ShipClassNames.get(ShipGlobals.INTERCEPTORL2),
    ItemId.INTERCEPTOR_L3: ShipClassNames.get(ShipGlobals.INTERCEPTORL3),
    ItemId.INTERCEPTOR_L4: ShipClassNames.get(ShipGlobals.INTERCEPTORL4),
    ItemId.MERCHANT_L1: ShipClassNames.get(ShipGlobals.MERCHANTL1),
    ItemId.MERCHANT_L2: ShipClassNames.get(ShipGlobals.MERCHANTL2),
    ItemId.MERCHANT_L3: ShipClassNames.get(ShipGlobals.MERCHANTL3),
    ItemId.MERCHANT_L4: ShipClassNames.get(ShipGlobals.MERCHANTL4),
    ItemId.WARSHIP_L1: ShipClassNames.get(ShipGlobals.WARSHIPL1),
    ItemId.WARSHIP_L2: ShipClassNames.get(ShipGlobals.WARSHIPL2),
    ItemId.WARSHIP_L3: ShipClassNames.get(ShipGlobals.WARSHIPL3),
    ItemId.WARSHIP_L4: ShipClassNames.get(ShipGlobals.WARSHIPL4),
    ItemId.WHEAT: 'Wheat',
    ItemId.COTTON: 'Cotton',
    ItemId.RUM: 'Grog',
    ItemId.IRON_ORE: 'Iron Ore',
    ItemId.IVORY: 'Ivory',
    ItemId.SILK: 'Silk',
    ItemId.SPICES: 'Spices',
    ItemId.COPPER_BARS: 'Copper Bars',
    ItemId.SILVER_BARS: 'Silver Bars',
    ItemId.GOLD_BARS: 'Gold Bars',
    ItemId.EMERALDS: 'Emeralds',
    ItemId.RUBIES: 'Rubies',
    ItemId.DIAMONDS: 'Diamonds',
    ItemId.CURSED_COIN: 'Cursed Coin',
    ItemId.ARTIFACT: 'Artifact',
    ItemId.RELIC: 'Relic',
    ItemId.RARE_DIAMOND: 'Rare Diamond',
    ItemId.CROWN_JEWELS: 'Crown Jewels',
    ItemId.RAREITEM6: 'Rare Item 6',
    InventoryType.PVPTotalInfamySea: 'Privateering Infamy Rank',
    InventoryType.PVPTotalInfamyLand: 'PvP Infamy Rank',
    InventoryType.Song_1: '1. Driftwood Island',
    InventoryType.Song_2: '2. Isla Cangrejos',
    InventoryType.Song_3: '3. Outcast Isle',
    InventoryType.Song_4: '4. Scatter the Gulls',
    InventoryType.Song_5: '5. Married to the Sea',
    InventoryType.Song_6: '6. Song 6',
    InventoryType.Song_7: '7. Song 7',
    InventoryType.Song_8: '8. Song 8',
    InventoryType.Song_9: '9. Song 9',
    InventoryType.Song_10: '10. Song 10',
    InventoryType.Song_11: "11. Merchant's Folly",
    InventoryType.Song_12: '12. Prepare to Cast Off!',
    InventoryType.Song_13: '13. Cutthroat Isle',
    InventoryType.Song_14: '14. Kingshead',
    InventoryType.Song_15: "15. Rumrunner's Isle",
    InventoryType.Song_16: '16. Song 16',
    InventoryType.Song_17: '17. Song 17',
    InventoryType.Song_18: '18. Song 18',
    InventoryType.Song_19: '19. Song 19',
    InventoryType.Song_20: '20. Song 20'}

def getInventoryTypeName(itemId):
    name = InventoryTypeNames.get(itemId)
    if name:
        return name
    
    return ''

ClickToLearn = 'Click to learn Skill!'
ClickToLearnCombo = 'Click to learn a new Combo Skill and lengthen your Combo Chain!'
ClickToLearnAmmo = 'Click to learn how to use a new Ammunition Type!'
ClickToLearnManeuver = 'Click to learn a new Ship Maneuver!'
UpgradesDamage = 'Upgrade to improve damage'
UpgradesHealing = 'Upgrade to improve healing power'
UpgradesMpDamage = 'for Health and ' + ManaName
UpgradesDuration = 'Upgrade to increase the'
UnlocksAtLevel = 'Skill unlocks at Level %s'
And = 'and'
SkillDescriptions = {
    InventoryType.MeleeJab: ('', '', ''),
    InventoryType.MeleePunch: ('', '', ''),
    InventoryType.MeleeKick: ('', '', ''),
    InventoryType.MeleeRoundhouse: ('', '', ''),
    InventoryType.MeleeHeadbutt: ('', '', ''),
    InventoryType.MeleeHaymaker: ('', '', ''),
    InventoryType.MeleeThrowDirt: ('', '', ''),
    InventoryType.MeleeToughness: ('', '', ''),
    InventoryType.MeleeIronSkin: ('', '', ''),
    InventoryType.MeleeDetermination: ('', '', ''),
    InventoryType.CutlassHack: (ComboSkill, 'A quick opening attack!', '', ClickToLearnCombo),
    InventoryType.CutlassSlash: (ComboSkill, 'A broad slash!', '', ClickToLearnCombo),
    InventoryType.CutlassCleave: (ComboSkill, 'A mighty overhead cleave!', '', ClickToLearnCombo),
    InventoryType.CutlassFlourish: (ComboSkill, 'A series of fast slashes!', '', ClickToLearnCombo),
    InventoryType.CutlassStab: (ComboSkill, 'A fancy finishing thrust!', '', ClickToLearnCombo),
    InventoryType.CutlassParry: (PassiveSkill, 'Parry enemy attacks! %d%% chance to block incoming Combat Attacks!', 'Upgrade to increase your chance to Parry!'),
    InventoryType.CutlassEndurance: (PassiveSkill, 'Increases maximum Health by %d!', 'Upgrade to increase your maximum Health!'),
    InventoryType.CutlassTaunt: (CombatSkill, 'Pulls enemy Aggression!', ''),
    InventoryType.CutlassBrawl: (CombatSkill, 'Fight dirty!', ''),
    InventoryType.CutlassSweep: (CombatSkill, 'A wide circular slash! Hits all nearby enemies!', ''),
    InventoryType.CutlassBladestorm: (CombatSkill, 'Delivers a barrage of sword slashes!', ''),
    InventoryType.PistolShoot: (AttackSkill, 'Basic shooting skill.', ''),
    InventoryType.PistolTakeAim: (AttackSkill, 'Hold down the attack button for an Aimed Shot! Increases the accuracy, range, and damage of the shot!', ''),
    InventoryType.PistolEagleEye: (PassiveSkill, 'Increases the maximum range for Firearms and ranged Dagger attacks by %d feet!', 'Upgrade to increase Range bonus of this Skill!'),
    InventoryType.PistolDodge: (PassiveSkill, '%d%% chance to Dodge incoming Ranged Attacks.', 'Upgrade to increase your chance to Dodge!'),
    InventoryType.PistolSharpShooter: (PassiveSkill, 'Increases accuracy for Firearms and ranged Dagger attacks by %d%%!', 'Upgrade Accuracy boost for Firearms and ranged Dagger attacks!'),
    InventoryType.PistolLeadShot: (AmmoSkill, 'Standard Ammunition.', '', ClickToLearnAmmo),
    InventoryType.PistolBaneShot: (AmmoSkill, 'A cursed bullet.', '', ClickToLearnAmmo),
    InventoryType.PistolSilverShot: (AmmoSkill, 'Made from solid silver.', '', ClickToLearnAmmo),
    InventoryType.PistolHexEaterShot: (AmmoSkill, 'Damages ' + ManaName + ' as well as Health.', '', ClickToLearnAmmo),
    InventoryType.PistolSteelShot: (AmmoSkill, 'The strongest metal shot.', '', ClickToLearnAmmo),
    InventoryType.PistolVenomShot: (AmmoSkill, 'Coated with deadly venom.', '', ClickToLearnAmmo),
    InventoryType.MusketShoot: ('', '', ''),
    InventoryType.MusketTakeAim: ('', '', ''),
    InventoryType.MusketDeadeye: ('', '', ''),
    InventoryType.MusketEagleEye: ('', '', ''),
    InventoryType.MusketCrackShot: ('', '', ''),
    InventoryType.MusketMarksman: ('', '', ''),
    InventoryType.MusketLeadShot: ('', '', '', ClickToLearnAmmo),
    InventoryType.MusketScatterShot: ('', '', '', ClickToLearnAmmo),
    InventoryType.MusketCursedShot: ('', '', '', ClickToLearnAmmo),
    InventoryType.MusketCoalfireShot: ('', '', '', ClickToLearnAmmo),
    InventoryType.MusketHeavySlug: ('', '', '', ClickToLearnAmmo),
    InventoryType.MusketExploderShot: ('', '', '', ClickToLearnAmmo),
    InventoryType.SailBroadsideLeft: (ShipSkill, 'Fire left broadside.', 'Upgrade to increase Left Broadside Cannonball damage!', ClickToLearnManeuver),
    InventoryType.SailBroadsideRight: (ShipSkill, 'Fire right broadside.', 'Upgrade to increase Right Broadside Cannonball damage!', ClickToLearnManeuver),
    InventoryType.SailFullSail: (ShipSkill, "Coaxes a short burst of speed out of the ship. Interrupts the 'Come About' Maneuver.", 'Upgrade to increase Maneuver duration!', ClickToLearnManeuver),
    InventoryType.SailComeAbout: (ShipSkill, "Allows your ship to make a hard sudden turn. Interrupts the 'Full Sail' Maneuver.", 'Upgrade to increase Maneuver duration!', ClickToLearnManeuver),
    InventoryType.SailOpenFire: (OrderSkill, 'Call upon your shipmates to fire cannons for great effect!', 'Upgrade to increase Open Fire duration!'),
    InventoryType.SailRammingSpeed: (ShipSkill, 'Bear down upon an enemy vessel and ram it into splinters! Interrupts all other Sailing Maneuvers.', 'Upgrade to improve ship ramming damage!', ClickToLearnManeuver),
    InventoryType.SailTakeCover: (OrderSkill, 'Protect your ship and shipmates from incoming fire.', 'Upgrade to increase Take Cover duration!'),
    InventoryType.SailPowerRecharge: (ShipSkill, 'Temporarily increases the rate of recharging sailing and cannon skills for the ship.', 'Unlocked after you recover the Black Pearl!'),
    InventoryType.SailWindcatcher: (PassiveSkill, 'A master of the sail, you know how to catch the wind in your sails for maximum speed. Increases ship speed by %d%%!', 'Upgrade to increase Speed bonus!'),
    InventoryType.SailTacking: (PassiveSkill, 'Superior knowledge of the rigging allows you to turn more rapidly. Improves ship turning radius by %d%%!', 'Upgrade to increase Maneuverability bonus!'),
    InventoryType.SailTreasureSense: (PassiveSkill, 'Your endeavours always seem to uncover more gold. Increases the quality of cargo drops by %d%%!', 'Upgrade to increase Cargo Drop bonus!'),
    InventoryType.SailTaskmaster: (PassiveSkill, 'A harsh taskmaster can get his shipmates to reload his cannons faster. Decreases cooldown time for Broadsides by %d%%!', 'Upgrade to decrease Broadside cooldown time!'),
    InventoryType.DaggerCut: (ComboSkill, 'An opening cut! Deals extra damage when striking a foe in the back!', '', ClickToLearnCombo),
    InventoryType.DaggerSwipe: (ComboSkill, 'A whirling dagger attack! Deals extra damage when striking a foe in the back!', '', ClickToLearnCombo),
    InventoryType.DaggerGouge: (ComboSkill, 'A powerful downward slice! Deals extra damage when striking a foe in the back!', '', ClickToLearnCombo),
    InventoryType.DaggerEviscerate: (ComboSkill, 'Delivers three quick cuts! Deals extra damage when striking a foe in the back!', '', ClickToLearnCombo),
    InventoryType.DaggerFinesse: (PassiveSkill, 'Decreases cooldown time for Dagger and Cutlass Skills by %d%%!', 'Upgrade to decrease Dagger and Cutlass Skill cooldown times!'),
    InventoryType.DaggerBladeInstinct: (PassiveSkill, 'Increases Cutlass and Dagger Combat damage by %d%%!', 'Upgrade to increase Cutlass and Dagger damage!'),
    InventoryType.DaggerAsp: (ThrowSkill, 'Basic dagger throw!', ''),
    InventoryType.DaggerAdder: (ThrowSkill, 'Poisoned dagger throw!', ''),
    InventoryType.DaggerThrowDirt: (CombatSkill, 'Fight dirty!', ''),
    InventoryType.DaggerSidewinder: (ThrowSkill, 'Sidearm dagger throw!', ''),
    InventoryType.DaggerViperNest: (ThrowSkill, 'Throw a brace of daggers!', ''),
    InventoryType.GrenadeThrow: (AttackSkill, 'Fire in the hole! Basic grenade throwing skill.', ''),
    InventoryType.GrenadeExplosion: (AmmoSkill, 'A hefty grenade!', '', ClickToLearnAmmo),
    InventoryType.GrenadeShockBomb: (AmmoSkill, 'A weak but stunning grenade!', '', ClickToLearnAmmo),
    InventoryType.GrenadeFireBomb: (AmmoSkill, 'A flammable concoction!', '', ClickToLearnAmmo),
    InventoryType.GrenadeSmokeCloud: (AmmoSkill, 'A smoke grenade that can used to obscure vision.', '', ClickToLearnAmmo),
    InventoryType.GrenadeSiege: (AmmoSkill, 'A powerful siege bomb! Watch out, it is heavy!', '', ClickToLearnAmmo),
    InventoryType.GrenadeLongVolley: (CombatSkill, 'Hold down the attack button to throw the grenade farther!  The longer you hold down the button, the further it will go!', ''),
    InventoryType.GrenadeDemolitions: (PassiveSkill, 'Increases the area of effect for your Grenade and Cannonball explosions!', 'Upgrade to increase Area of Effect bonus!'),
    InventoryType.GrenadeDetermination: (PassiveSkill, 'Increases your Health Recovery rate by %d%%!', 'Upgrade to increase your Health Recovery rate!'),
    InventoryType.GrenadeToughness: (PassiveSkill, 'Decreases damage suffered by incoming Grenades and Cannonballs by %d%%', 'Upgrade to increase your damage resistance to Grenades and Cannonballs!'),
    InventoryType.GrenadeIgnorePain: (PassiveSkill, 'Stun and Slow effect durations are reduced by %d%%!', 'Upgrade to increase Slow recovery speed!'),
    InventoryType.DollAttune: (AttackSkill, 'Attune the doll to a target in order to cast Hexes!', 'Upgrade to gain the ability to Attune the doll to 1 additional friend or enemy!'),
    InventoryType.DollPoke: (HexSkill, 'Poke attack!', ''),
    InventoryType.DollSwarm: (HexSkill, 'Summon insects to attack the enemy!', ''),
    InventoryType.DollHeal: (HexSkill, 'Heals a friendly pirate!', ''),
    InventoryType.DollBurn: (HexSkill, 'Sets enemies on fire!', ''),
    InventoryType.DollShackles: (HexSkill, 'Chains from the grave wrap around the enemy!', ''),
    InventoryType.DollCure: (HexSkill, 'Heals a friendly pirate and removes hostile effect Buffs from a friendly pirate!', ''),
    InventoryType.DollCurse: (HexSkill, 'Curses your opponent!', ''),
    InventoryType.DollLifeDrain: (HexSkill, 'Drain vitality from the victim.', ''),
    InventoryType.DollFocus: (PassiveSkill, 'Increases your maximum ' + ManaName + ' amount by %d ' + ManaName + '!', 'Upgrade to increase your maximum ' + ManaName + '!'),
    InventoryType.DollSpiritWard: (PassiveSkill, '%d%% chance to Resist enemy Voodoo!', 'Upgrade to increase your chance to Resist enemy Voodoo!'),
    InventoryType.StaffBlast: (AttackSkill, '', ''),
    InventoryType.StaffWither: (HexSkill, '', ''),
    InventoryType.StaffSoulFlay: (HexSkill, '', ''),
    InventoryType.StaffPestilence: (HexSkill, '', ''),
    InventoryType.StaffHellfire: (HexSkill, '', ''),
    InventoryType.StaffBanish: (HexSkill, '', ''),
    InventoryType.StaffDesolation: (HexSkill, '', ''),
    InventoryType.StaffConcentration: (PassiveSkill, 'Increases your ' + ManaName + ' Recovery rate by %d%%!', 'Upgrade to increase your ' + ManaName + ' Recovery rate!'),
    InventoryType.StaffSpiritLore: (PassiveSkill, 'Increases Casting Speed for the Voodoo Staff by %d%%!', 'Upgrade to increase Casting Speed for the Voodoo Staff!'),
    InventoryType.StaffConservation: (PassiveSkill, 'Decreases ' + ManaName + ' used by Voodoo Staff and Voodoo Doll by %d%%!', 'Upgrade to decrease ' + ManaName + ' usage for Voodoo Staff and Voodoo Doll!'),
    InventoryType.StaffSpiritMastery: (PassiveSkill, 'Increases damage of Voodoo Doll and Staff Voodoo Hexes by %d%%!', 'Upgrade to increase Staff and Doll Voodoo Hex damage!'),
    InventoryType.CannonShoot: (AttackSkill, 'Basic Cannoneering Skill!', 'Upgrade to increase Cannon firing rate!'),
    InventoryType.CannonRoundShot: (AmmoSkill, 'Medium ranged shot! Effective against ship hulls!', '', ClickToLearnAmmo),
    InventoryType.CannonChainShot: (AmmoSkill, 'Short ranged shot! Effective against masts & sails!', '', ClickToLearnAmmo),
    InventoryType.CannonExplosive: (AmmoSkill, 'Explodes and damages a large area!', '', ClickToLearnAmmo),
    InventoryType.CannonBullet: (AmmoSkill, '', '', ClickToLearnAmmo),
    InventoryType.CannonGasCloud: (AmmoSkill, '', '', ClickToLearnAmmo),
    InventoryType.CannonGrapeShot: (AmmoSkill, 'Short ranged shot! Effective only against Crew in PVP and Sea Monsters!', '', ClickToLearnAmmo),
    InventoryType.CannonSkull: (AmmoSkill, '', '', ClickToLearnAmmo),
    InventoryType.CannonFirebrand: (AmmoSkill, 'Flaming cannonballs set fire to enemy ships.', '', ClickToLearnAmmo),
    InventoryType.CannonFlameCloud: (AmmoSkill, '', '', ClickToLearnAmmo),
    InventoryType.CannonFlamingSkull: (AmmoSkill, 'Flaming cannonballs set fire to enemy ships.', '', ClickToLearnAmmo),
    InventoryType.CannonBarShot: (AmmoSkill, '', '', ClickToLearnAmmo),
    InventoryType.CannonKnives: (AmmoSkill, '', '', ClickToLearnAmmo),
    InventoryType.CannonMine: (AmmoSkill, '', '', ClickToLearnAmmo),
    InventoryType.CannonBarnacles: (AmmoSkill, '', '', ClickToLearnAmmo),
    InventoryType.CannonThunderbolt: (AmmoSkill, 'Summons a thunderbolt to strike the enemy ship!', '', ClickToLearnAmmo),
    InventoryType.CannonFury: (AmmoSkill, 'A spectral cannonball!', '', ClickToLearnAmmo),
    InventoryType.CannonComet: (AmmoSkill, '', '', ClickToLearnAmmo),
    InventoryType.CannonGrappleHook: (AmmoSkill, 'Used for grappling enemy ships for boarding actions!', '', ClickToLearnAmmo),
    InventoryType.CannonRapidReload: (PassiveSkill, 'Increases Cannon reloading speed by %d%%!', 'Upgrade to increase Cannon reloading speed!'),
    InventoryType.CannonBarrage: (PassiveSkill, 'Increases damage for Cannon and Grenade attacks by %d%%!', 'Upgrade to increase Cannon and Grenade damage!'),
    InventoryType.CannonShrapnel: (PassiveSkill, 'Upgrade your Cannonballs and Grenades to explode in a cloud of shrapnel!', 'Upgrade to increase Shrapnel Wounding duration!'),
    InventoryType.Potion1: (Consumable, '', ''),
    InventoryType.Potion2: (Consumable, '', ''),
    InventoryType.Potion3: (Consumable, '', ''),
    InventoryType.Potion4: (Consumable, '', ''),
    InventoryType.Potion5: (Consumable, '', ''),
    InventoryType.ShipRepairKit: (ShipRepairSkill, '', ''),
    InventoryType.PorkChunk: (Consumable, '', '')}
PoisonDesc = 'Poisons an enemy for %d seconds!'
PoisonUpgrade = 'Poison duration'
AcidDesc = 'Causes acid burns on an enemy for %d seconds!'
AcidUpgrade = 'Acid duration'
HoldDesc = 'Prevents enemy from moving for %d seconds!'
HoldUpgrade = 'movement lock duration'
WoundDesc = 'Wounds an enemy for %d seconds!'
WoundUpgrade = 'Wound duration'
OnFireDesc = 'Burns an enemy for %d seconds!'
OnFireUpgrade = 'Burning duration'
StunDesc = 'Disables an enemy for %d seconds!'
StunUpgrade = 'Stun duration'
UnstunDesc = 'Immune to Stun for %d seconds!'
UnstunUpgrade = 'Stun Immunity duration'
SlowDesc = 'Slows an enemy for %d seconds!'
SlowUpgrade = 'Slow duration'
BlindDesc = 'Blinds an enemy for %d seconds!'
BlindUpgrade = 'Blindness duration'
CurseDesc = 'Curses an enemy so that they suffer an additional %d%% damage from attacks! Lasts %d seconds!'
CurseUpgrade = 'Curse duration'
HastenDesc = 'Increases movement speed of a pirate by 50%%! Lasts %d seconds!'
HastenUpgrade = 'Hasten duration'
TauntDesc = 'Decreases enemy attack accuracy! Lasts %d seconds!'
TauntUpgrade = 'Taunt duration'
WeakenDesc = 'Decreases enemy attack power by %d%% for %d seconds!'
WeakenUpgrade = 'Weakness duration'
RegenDesc = 'Regain lost health for %d seconds!'
RegenUpgrade = 'Regeneration duration'
SoulTapDesc = "Injures the caster and expends most of the pirate's remaining Health!"
LifeDrainDesc = 'Drains Health from the victim!'
ManaDrainDesc = 'Drains ' + ManaName + ' from the victim!'
InterruptDesc = 'Interrupts weapon charging!'
UnattuneDesc = 'Breaks voodoo attunements!'
FullSailDesc = 'Lasts %d seconds!'
ComeAboutDesc = 'Lasts %d seconds!'
OpenFireDesc = 'Lasts %d seconds!'
OpenFireUpgrade = 'Ram Maneuver duration!'
RamDesc = 'Lasts %d seconds!'
TakeCoverDesc = 'Lasts %d seconds!'
PowerRechargeDesc = 'Lasts %d seconds!'
AttuneDesc = 'Can attune up to %d friends or enemies!'
MonsterKillerDesc = 'Powerful against the Living, but weak against the Undead.'
UndeadKillerDesc = 'Powerful against the Undead, but weak against the Living.'
BuffBreakDesc = 'Has a chance to destroy a Voodoo Hex on the target!'
BuffBreakUpgrade = 'increase the chance to remove a Voodoo Hex from the target'
BroadsideDesc = 'Cannonball damage increased by %d%%!'
CannonShootDesc = 'Cannon firing rate increased by %d%%!'
MultiAttuneDesc = 'The more targets attuned, the weaker your Hexes will be!'
AttackBackstab = 'Backstrike!'
AttackUnattune = 'Attunements Shattered!'
AttackInterrupt = 'Interrupted!'
ComboReqSwipe = 'Requires Swipe.'
ComboReqGouge = 'Requires Gouge'
ComboReqSlash = 'Requires Slash'
ComboReqCleave = 'Requires Cleave'
ComboReqFlourish = 'Requires Flourish'
SloopDescription = 'The fastest and most maneuverable ship class, the Sloop is ideal for scouting and hit-and-run attacks.  However, Sloops tend to have weak armor and little cargo room. \n \n The strongest armor of the hull is located near the middle of the ship.'
MerchantDescription = 'The Galleons have the toughest armor amongst the ship classes.  They also can carry the most cargo.  \n \n Their strongest armor is near the rear of the ship, with a weakness in the front.'
WarshipDescription = "The Frigate Class vessels pack the most firepower, sporting many cannons and strong below deck broadside capability.  \n \n The warship's strongest armor is near the front, with a weakness in the rear."
WeaponDescriptions = {
    InventoryType.CutlassWeaponL1: "It's a bit crude, but it still has an edge.",
    InventoryType.CutlassWeaponL2: 'A well crafted iron blade. A good weapon! \n +2 damage per hit.',
    InventoryType.CutlassWeaponL3: 'An ornate steel cutlass. Well balanced and sharp! \n +4 damage per hit.',
    InventoryType.CutlassWeaponL4: "A Fine Cutlass. It is crafted with pride by the Caribbean's best blacksmiths.\n +6 damage per hit.",
    InventoryType.CutlassWeaponL5: 'A Pirate Blade, a clear warning sign to any EITC or Navy blokes.\n +8 damage per hit.',
    InventoryType.CutlassWeaponL6: 'A Dark Cutlass. \n +10 damage per hit.',
    InventoryType.PistolWeaponL1: 'A standard flintlock pistol. Fires one shot before it needs to be reloaded.',
    InventoryType.PistolWeaponL2: 'A flintlock pistol with two barrels. Each barrel can be fired separately before reloading.',
    InventoryType.PistolWeaponL3: 'A multi-barreled pistol! This rare device can fire three times before reloading.',
    InventoryType.PistolWeaponL4: 'A Heavy Tri-Barrel Pistol, a fine piece of weaponry. \n +1 damage per hit.',
    InventoryType.PistolWeaponL5: 'A Grand Pistol, equipped with three deadly barrels. \n +2 damage per hit.',
    InventoryType.PistolWeaponL6: 'A Quad-Barrel Pistol, four shiny barrels that will scare even the deadliest of pirates away. \n +3 damage per hit.',
    InventoryType.MusketWeaponL1: '',
    InventoryType.MusketWeaponL2: '',
    InventoryType.MusketWeaponL3: '',
    InventoryType.BayonetWeaponL1: '',
    InventoryType.BayonetWeaponL2: '',
    InventoryType.BayonetWeaponL3: '',
    InventoryType.DaggerWeaponL1: 'A sharp dagger. Small but deadly.',
    InventoryType.DaggerWeaponL2: 'A long knife. Well balanced for fighting. \n +2 damage per hit.',
    InventoryType.DaggerWeaponL3: 'A fancy blade that is useful for keeping your opponent off guard. \n +4 damage per hit.',
    InventoryType.DaggerWeaponL4: "A Coltello dagger, it is a pirate's best friend in the right fight. \n +6 damage per hit.",
    InventoryType.DaggerWeaponL5: 'A Bloodletter dagger. It is meticulously designed to fend off even the largest of foes. \n +8 damage per hit.',
    InventoryType.DaggerWeaponL6: 'A Slicer dagger. Tear through your enemies with ease with this deadly weapon. \n +10 damage per hit.',
    InventoryType.GrenadeWeaponL1: 'Grenades are highly lethal explosives. They are effective against large crowds of enemies!',
    InventoryType.GrenadeWeaponL2: '',
    InventoryType.GrenadeWeaponL3: '',
    InventoryType.GrenadeWeaponL4: '',
    InventoryType.GrenadeWeaponL5: '',
    InventoryType.GrenadeWeaponL6: '',
    InventoryType.DollWeaponL1: 'A mystical doll said to be able to bind to the spirit of anything it touches.',
    InventoryType.DollWeaponL2: 'A powerful doll able to bind to the spirits of the living and the dead. \n +2 damage per hit.',
    InventoryType.DollWeaponL3: 'An elaborate oriental doll able to strongly bind to the spirits of others. \n +4 damage per hit.',
    InventoryType.DollWeaponL4: 'A Pirate Doll. Bind to the spirits of the Caribbean with this rare doll. \n +6 damage per hit.',
    InventoryType.DollWeaponL5: 'A Taboo Doll. Many pirates fear the power and unknowns of this legendary doll. \n +8 damage per hit.',
    InventoryType.DollWeaponL6: 'A Mojo Doll. Out perform almost any pirate with deadly and unmatched precision. \n +10 damage per hit.',
    InventoryType.WandWeaponL1: 'A tribal fetish used for summoning evil spirits.',
    InventoryType.WandWeaponL2: 'A powerful fetish used for summoning and controlling spirits. \n +2 damage per hit.',
    InventoryType.WandWeaponL3: 'Sought after by many, this fetish allows the bearer to speak to the spirits of the dead. \n +4 damage per hit.',
    InventoryType.WandWeaponL4: 'Harrow Staff. Inflict the secrets of the dead upon your enemies with this rare staff. \n +6 damage per hit.',
    InventoryType.WandWeaponL5: 'Vile Staff. Summon the plagues of the dead and unknown against your foes. \n +8 damage per hit.',
    InventoryType.WandWeaponL6: 'Dire Staff. A myth to some pirates, this staff holds the power to demolish your enemies. \n +10 damage per hit.',
    InventoryType.KettleWeaponL1: '',
    InventoryType.KettleWeaponL2: '',
    InventoryType.KettleWeaponL3: '',
    InventoryType.Potion1: 'Eases pain. Smells kinda strong too.',
    InventoryType.Potion2: 'An exotic remedy. Said to cure all maladies.',
    InventoryType.Potion3: 'Water blessed by the angels and gods.',
    InventoryType.Potion4: 'The one and only, legendary Elixir of Life!',
    InventoryType.Potion5: 'A miracle potion said to cure all sicknesses and regrow hair!',
    InventoryType.PorkChunk: "A tasty chunk of pork cooked for the Founder's Feast!",
    InventoryType.ShipRepairKit: 'Tools and supplies for repairing your ship in PvP.',
    InventoryType.AmmoLeadShot: 'A solid ball of lead. Crude but effective.',
    InventoryType.AmmoVenomShot: "Coated with snake venom. If the shot don't kill you, the venom will.",
    InventoryType.AmmoBaneShot: 'Cursed by Davy Jones himself! Weakens your opponents.',
    InventoryType.AmmoSilverShot: 'Useful against spooks and ghouls.',
    InventoryType.AmmoHexEaterShot: 'Disrupts Voodoo of witch doctors and the like.',
    InventoryType.AmmoSteelShot: 'The strongest shot. Great for hunting beasts and monsters.',
    InventoryType.AmmoAsp: 'A small set of throwing knives. \n Throwing ammunition for the Asp Skill.',
    InventoryType.AmmoAdder: 'A throwing knife coated with snake venom. \n Throwing ammunition for the Adder Skill.',
    InventoryType.AmmoSidewinder: 'A large curved throwing knife. \n Throwing ammunition for the Sidewinder Skill.',
    InventoryType.AmmoViperNest: 'A brace of special throwing knives meant to be thrown in a set. \n Throwing ammunition for the Viper Nest Skill.',
    InventoryType.AmmoGrenadeExplosion: 'A crude ceramic grenade.',
    InventoryType.AmmoGrenadeFlame: 'A flammable bomb that sets fire to its surroundings.',
    InventoryType.AmmoGrenadeShockBomb: 'A ceramic pot filled with noxious gas and foul smelling gunk.',
    InventoryType.AmmoGrenadeSmoke: 'A bomb filled with quick burning tar and rags. Creates a blinding cloud of smoke.',
    InventoryType.AmmoGrenadeSiege: 'A heavy iron grenade that packs a wallop!',
    InventoryType.AmmoRoundShot: 'Standard large round cannonball.',
    InventoryType.AmmoChainShot: 'Two iron balls connected by a chain. Useful for tearing down sails and masts.',
    InventoryType.AmmoExplosive: 'A mighty exploding cannonball. Highly volatile and extremely heavy.',
    InventoryType.AmmoGrapeShot: 'A canister of small metal balls that fires in a huge spread. It is deadly against enemy crewmen, but has a short range.',
    InventoryType.AmmoFirebrand: 'A flaming cannonball capable of setting fire to enemy ships.',
    InventoryType.AmmoFlamingSkull: 'A flaming skull capable of setting fire to enemy ships.',
    InventoryType.AmmoThunderbolt: 'A highly charged cannonball that causes a lightning bolt to strike where it lands.',
    InventoryType.AmmoFury: 'An ethereal ghostly fireball.',
    InventoryType.AmmoGrappleHook: 'Useful for boarding enemy ships. First, disable the ship. Then fire grapples and pull it in.',
    InventoryType.PistolPouchL1: 'A small ammo pouch for pistol bullets. Lets you hold more bullets of each type.',
    InventoryType.PistolPouchL2: 'A medium ammo pouch for pistol bullets. Lets you hold more bullets of each type.',
    InventoryType.PistolPouchL3: 'A large ammo pouch for pistol bullets. Lets you hold more bullets of each type.',
    InventoryType.DaggerPouchL1: 'A small belt for throwing daggers. Lets you hold more throwing daggers of each type.',
    InventoryType.DaggerPouchL2: 'A medium belt for throwing daggers. Lets you hold more throwing daggers of each type.',
    InventoryType.DaggerPouchL3: 'A large belt for throwing daggers. Lets you hold more throwing daggers of each type.',
    InventoryType.GrenadePouchL1: 'A small sack for grenades. Lets you hold more grenades of each type.',
    InventoryType.GrenadePouchL2: 'A medium sack for grenades. Lets you hold more grenades of each type.',
    InventoryType.GrenadePouchL3: 'A large sack for grenades. Lets you hold more grenades of each type.',
    InventoryType.CannonPouchL1: 'A small barrel for holding cannon ammo. Lets you hold more cannonballs of each type.',
    InventoryType.CannonPouchL2: 'A medium barrel for holding cannon ammo. Lets you hold more cannonballs of each type.',
    InventoryType.CannonPouchL3: 'A large barrel for holding cannon ammo. Lets you hold more cannonballs of each type.'}
ShipDescriptions = {
    ItemId.INTERCEPTOR_L1: SloopDescription,
    ItemId.INTERCEPTOR_L2: SloopDescription,
    ItemId.INTERCEPTOR_L3: SloopDescription,
    ItemId.MERCHANT_L1: MerchantDescription,
    ItemId.MERCHANT_L2: MerchantDescription,
    ItemId.MERCHANT_L3: MerchantDescription,
    ItemId.WARSHIP_L1: WarshipDescription,
    ItemId.WARSHIP_L2: WarshipDescription,
    ItemId.WARSHIP_L3: WarshipDescription}
GrenadeShort = 'Grenade'
ShipCannonShort = 'Cannon'
InventoryItemClassNames = {
    ItemType.MELEE: 'Brawl',
    ItemType.SWORD: 'Cutlass',
    ItemType.PISTOL: 'Pistol',
    ItemType.MUSKET: 'Musket',
    ItemType.DAGGER: 'Dagger',
    ItemType.GRENADE: 'Grenade Weapon',
    ItemType.DOLL: 'Voodoo Doll',
    ItemType.WAND: 'Voodoo Staff',
    ItemType.KETTLE: 'Voodoo Kettle',
    ItemType.SHIP: 'Ship',
    ItemType.SHIPPART: 'Ship Part',
    ItemType.CONSUMABLE: 'Consumable',
    ItemType.POTION: 'Drink',
    ItemType.FOOD: 'Food',
    ItemType.FURNITURE: 'Furniture',
    ItemType.INGREDIENT: 'Voodoo Ingredient',
    ItemType.CANNON: 'Ship Cannon',
    ItemType.BOTTLE: 'Holds a Ship',
    ItemType.CANNONAMMO: 'Cannon Ammo',
    ItemType.DAGGERAMMO: 'Dagger Ammo',
    ItemType.PISTOLAMMO: 'Pistol Ammo',
    ItemType.GRENADEAMMO: 'Grenade Ammo',
    ItemType.POUCH: 'Ammo Pouch',
    ItemType.PISTOL_POUCH: 'Pistol Ammo Pouch',
    ItemType.DAGGER_POUCH: 'Throwing Dagger Belt',
    ItemType.GRENADE_POUCH: 'Grenade Sack',
    ItemType.CANNON_POUCH: 'Cannonball Barrel',
    ItemType.SHIP_REPAIR_KIT: 'Repairs Ship in PvP'}
ItemGroupNames = {
    ItemTypeGroup.CUTLASS: 'Cutlasses',
    ItemTypeGroup.DAGGER: 'Daggers',
    ItemTypeGroup.PISTOL: 'Pistols',
    ItemTypeGroup.CANNON: 'Cannons',
    ItemTypeGroup.DOLL: 'Dolls',
    ItemTypeGroup.POTION: 'Tonics',
    ItemTypeGroup.GRENADE: 'Grenades',
    ItemTypeGroup.WAND: 'Staff'}
VoodooNames = {
    0: 'Heartiness',
    1: 'Strength',
    2: 'Swiftness',
    3: 'Luck',
    4: 'Voodoo'}
SkillResultNames = {
    0: 'Miss',
    1: 'Hit',
    2: 'Delayed',
    3: 'Out of Range',
    4: 'Not Available',
    5: 'Not Recharged',
    6: 'Against Pirate Code',
    7: 'Parry',
    8: 'Dodge',
    9: 'Resist'}
Mistimed = 'Mistimed'
Disengage = 'Disengage'
InteractCancel = lExit
InteractTalk = 'Talk'
InteractTrade = 'Trade'
InteractDuel = 'Duel'
InteractQuest = 'Quest'
InteractBribe = 'Bribe'
InteractBribeAlt = 'Pay Gold'
InteractShips = 'Purchase'
InteractSellShips = 'Sell'
InteractStore = 'Store'
InteractRepair = 'Repair'
InteractOverhaul = 'Overhaul'
InteractUpgrade = 'Upgrade'
InteractHealHp = 'Healing'
InteractHealMojo = 'Recharge'
InteractTrain = 'Training'
InteractSail = 'Sail'
InteractSailTM = 'Treasure Map'
InteractRespec = 'Retrain Skills'
InteractRespecCutlass = 'Retrain Cutlass'
InteractRespecPistol = 'Retrain Pistol'
InteractRespecGrenade = 'Retrain Grenade'
InteractRespecDoll = 'Retrain Voodoo Doll'
InteractRespecDagger = 'Retrain Dagger'
InteractRespecStaff = 'Retrain Voodoo Staff'
InteractRespecSailing = 'Retrain Sailing'
InteractRespecCannon = 'Retrain Cannon'
InteractBack = 'Back'
InteractMusician = 'Request a Song'
InteractPvPTattoo = 'PvP Tattoos'
InteractPvPEyePatch = 'PvP Eye Patches'
InteractPvPHat = 'PvP Hats'
InteractCancelHelp = 'Finish talking with this person'
InteractTalkHelp = 'Chat with this person'
InteractTradeHelp = 'Trade with this person'
InteractDuelHelp = 'Fight this person'
InteractQuestHelp = 'Ask for a new Quest'
InteractBribeHelp = 'Bribe this person'
InteractShipsHelp = 'Purchase new ships'
InteractSellShipsHelp = 'Sell your ships'
InteractStoreHelp = 'Purchase or sell equipment and items'
InteractRepairHelp = 'Repair damage to your ship'
InteractOverhaulHelp = 'Reconstruct severely wrecked ships'
InteractUpgradeHelp = 'Upgrade your ship'
InteractHealHpHelp = 'Heal your character'
InteractHealMojoHelp = 'Refills lost Voodoo'
InteractTrainHelp = 'Learn new skills and techniques'
InteractAmmoHelp = 'Purchase cannon ammo'
InteractSailHelp = 'Sail the high seas'
InteractSailTMHelp = 'Sail using a Treasure Map'
InteractRespecHelp = 'Redistribute skill points'
InteractBackHelp = 'Go back to previous menu'
InteractMusicianHelp = 'Request some music...for a fee'
InteractPvPTattooHelp = 'Spend PvP Infamy on unique tattoos'
InteractPvPEyePatchHelp = 'Only the infamous can wear eye patches'
InteractPvPHatHelp = 'Spend PvP Infamy on unique hats'
RespecConfirmDialog = 'Pay %(gold)s gold to retrain your %(weapon)s? Retraining will refund all of your spent skill points so that you can redistribute them.'
RespecPriceIncreaseDialog = ' \n\nChoose carefully! The next time you Retrain, it will cost more Gold!'
BribeConfirmDialog = 'Bribe %(name)s for %(gold)s gold?'
HealHpConfirmDialog = 'Pay %(gold)s gold for full healing?'
HealMojoConfirmDialog = 'Pay %(gold)s gold for full voodoo recharge?'
RepairConfirmDialog = 'Pay %(gold)s gold for full ship repairs?'
OverhaulConfirmDialog = 'Pay %(gold)s gold to reconstruct your wrecked ship?'
SellShipConfirmDialog = 'Sell this ship for %(gold)s gold?'
SellShipAreYouSureDialog = 'Are you sure you want to sell your ship? It will be permanently lost.'
BribeConfirmYourGold = 'Your Gold: %s'
BribeNotEnoughGold = 'You cannot afford %(gold)s gold for the bribe.'
InteractKey = 'Shift'
TabKey = 'Tab'
CtrlKey = 'Ctrl'
ShiftKey = 'Shift'
EscapeKey = 'Esc'
OneKey = '1'
QuestPageKey = 'J'
WeaponPageKey = 'I'
SkillPageKey = 'K'
LookoutPageKey = 'L'
WeaponSlot1 = 'F1'
WeaponSlot2 = 'F2'
ForwardMoveKey = 'W'
LeftMoveKey = 'A'
RightMoveKey = 'D'
BackwardMoveKey = 'S'
InteractGeneral = 'Press %s to interact' % InteractKey
InteractCannon = 'Press %s to use cannon' % InteractKey
InteractWheel = 'Press %s to steer ship' % InteractKey
InteractWheelCaptain = 'Press %s to take over steering the ship' % InteractKey
InteractRepairSpot = 'Press %s to repair ship' % InteractKey
InteractBuriedTreasure = 'Press %s to dig' % InteractKey
InteractDigging = 'Digging...'
InteractSearchableContainer = 'Press %s to search' % InteractKey
InteractSearching = 'Searching...'
InteractHolidayBonfire = 'Press %s to initiate the Founders Feast Bonfire' % InteractKey
InteractHolidayPig = 'Press %s to get some Founders Feast meat' % InteractKey
AlreadySearched = 'Nothing interesting here.'
DidNotFindQuestItem = 'Did not find any quest items.'
FoundQuestItem = 'Found quest item!'
InteractTownfolk = 'Press %s to talk to townsperson' % InteractKey
InteractNamedTownfolk = 'Press %s to talk to ' % InteractKey + '%s'
InteractNavySailor = 'Press %s to battle the Navy Soldier' % InteractKey
BoardShipInstructions = 'Press %s to board ship' % InteractKey
DeployShipInstructions = 'Press %s to row out to a ship' % InteractKey
ShipDepositInstructions = 'Press %s to load treasure onto ship' % InteractKey
ShipTransferInstructions = 'Press %s to transfer treasure to base' % InteractKey
UnableBoardShipInstructions = 'Not able to board ship'
DinghyNeedFirstShip = 'Use the map in your sea chest to return to %s to see about acquiring a ship of your own.'
DinghyNeedShip = 'You must have a ship before you can go sailing.'
DinghyNoFriendShip = "None of your friends' ships are available for sailing at the moment."
DinghyNoCrewShip = "None of your crew members' ships are available for sailing at the moment."
DinghyNoGuildShip = "None of your guild members' ships are available for sailing at the moment."
DinghyNoPublicShip = 'There are no public ships available for sailing at the moment.'
DinghyMyShip = 'Own'
DinghyFriendShip = 'Friend'
DinghyCrewShip = 'Crew'
DinghyGuildShip = 'Guild'
DinghyPublicShip = 'Public'
ExitShipInstructions = 'Press %s to exit ship' % InteractKey
ExitShipLockedInstructions = 'Must be Docked to exit ship'
ExitShipToEnemyShipInstructions = 'Press %s to board enemy ship' % InteractKey
ExitShipToOriginalShipInstructions = 'Press %s to return to your ship' % InteractKey
FlagshipWaitingForGrappleInstructions = 'Shoot grappling hooks at the flashing green targets to tow the flagship into boarding position.'
FlagshipGrappleLerpingInstructions = 'Grappling hook landed!  Land more grappling hooks to tow the flagship faster!'
FlagshipInPositionInstructionsCaptain = 'Flagship is in position, click button to board it with your shipmates!'
FlagshipInPositionInstructionsCrew = 'Flagship is in position, waiting for captain to initiate boarding...'
FlagshipStatusWaitingForGrapple = 'Crippled'
FlagshipStatusInPosition = 'Ready to be boarded'
FlagshipStatusBoarded = 'Boarded'
FlagshipClickToBoard = 'Click button to board'
NoPigRoasting = 'No pig roasting. Try again later!'
BonfireAlreadyStarted = 'Founders Feast Bonfire already started!'
PorkChunkReceived = "You took some Roast Pork from the Founder's Feast Roast"
ClickToBattleGeneral = 'Click on enemy to battle'
ClickToBattleSkeleton = 'Click on skeleton to battle'
KeyToBattleGeneral = 'Press %s to battle enemy' % InteractKey
InteractOpenDoor = 'Press %s to open door' % InteractKey
InteractEnterNamedBuilding = 'Press %s to enter ' % InteractKey + '%s'
InteractKickDoor = 'Press %s to kick door' % InteractKey
InteractKicking = 'Kicking...'
InteractLock = 'Press %s to pick lock' % InteractKey
LockMechanism = 'Mechanism'
LockpickFailed = 'Lockpick Failed'
UnlockedBy = 'Unlocked by'
InteractTable = 'Press %s to sit down' % InteractKey
InteractTableBlackjack = 'Press %s to sit down and play Blackjack' % InteractKey
InteractTablePoker = 'Press %s to sit down and play Poker' % InteractKey
InteractTableHoldemPoker = "Press %s to sit down and play Tortuga Hold'em Poker" % InteractKey
InteractTable7StudPoker = 'Press %s to sit down and play 7 Stud Poker' % InteractKey
ShipAlreadyDeployedWarning = 'Already have a ship launched!'
ShipAlreadyDeployingWarning = 'Already deploying a ship!'
ShipReturnAdventureWarning = 'Cannot return ships during an Adventure!'
PlayerNotInWaterWarning = 'Player must be in water'
PlayerInHighSeaWarning = 'Cannot launch ships in High Seas!'
CannotBoardShipWarning = 'Cannot board ship at this time!'
ShipNotInBottleWarning = 'Ship must be put away in bottle first!'
OtherShipIsBeingDeployed = "%s's ship, the %s, is now being launched at %s!"
CoralReefWarning = 'You are sailing too close to shore!'
AnchorButtonInfo = 'Drop Anchor'
AnchorButtonHelp = 'Drop anchor and enter port'
FlagshipButtonInfo = 'Swing Over'
FlagshipButtonHelp = 'Board the enemy flagship'
JournalButtonInfo = 'New Quest!'
JournalButtonHelp = 'You have a New Quest! Open your Quest Journal and view it!'
SocialButtonHelp = 'Friends'
QuestButtonHelp = 'Quest Journal'
WeaponButtonHelp = 'Weapons'
SkillButtonHelp = 'Skills'
ClothingButtonHelp = 'Clothing'
TitlesButtonHelp = 'Titles'
TreasuresButtonHelp = 'Treasure'
ShipsButtonHelp = 'Ships'
RadarButtonHelp = 'Compass'
OptionsButtonHelp = 'Options'
MapButtonHelp = 'Map'
ShardActiveWorlds = 'Active Oceans'
ShardCurrentWorld = 'Current Server'
ShardPreferredWorld = 'Preferred Server'
ShardNone = 'Random (Click here to choose)'
Ocean = 'Ocean'
ShardPageLow = 'Quiet'
ShardPageMed = 'Ideal'
ShardPageHigh = 'Full'
PortOfCall = 'Port of Call'
LookoutButtonHelp = 'Lookout'
SeaChestButtonHelp = 'Sea Chest'
InventoryHelp = 'Sea Chest'
SkillHelp = 'Skills'
QuestHelp = 'Quests'
WeaponHelp = 'Click to Equip Weapon'
WeaponSwitchHelp = 'Click to Change Selected Weapon'
GameHelp = 'Display Game Menu'
SocialButtonHelp = 'Hearties'
FriendButtonHelp = 'Toggle Friend List'
CrewButtonHelp = 'Toggle Crew List'
GuildButtonHelp = 'Toggle Guild List'
PirateCodeWarning1 = 'Keep to the Code'
PirateCodeWarning2 = 'Choose Another Weapon'
UnattuneGui = 'Unattune a Target?'
EmptyBottle = 'Empty Bottle'
EmptyBottleDesc = 'Will hold one ship'
ScreenshotLocation = 'Screenshots located'
HighSeasAdventureStartTitle = 'High Seas Adventure'
HighSeasAdventureStartInfo = 'Return to your Ship before it leaves Port!'
HighSeasAdventureStartWaitInfo = 'Waiting for Shipmates to board Ship!'
HighSeasAdventureLimitTitle = 'Supplies'
HighSeasShipSelectionTitle = 'Ship Selection'
Accept = 'Accept'
Decline = 'Decline'
Cancel = lCancel
Back = lBack
Decline = 'Decline'
Bribe = 'Bribe'
DropQuest = 'Drop'
DropQuestHelp = 'Abandon this quest and remove it from your journal.'
ShareQuest = 'Share'
TrackQuest = 'Track'
TrackQuestHelp = 'Show visual indicator to help find your next step in this quest.'
QuestDescription = 'Quest Description'
BPCrew = 'Crew'
BPCrewTitle = 'The Black Pearl Crew'
QuestPageStoryQuests = 'Fame'
QuestPageWorkQuests = 'Fortune'
QuestFull = 'You must complete one of your Fortune Quests before accepting another task.'
QuestMultiHeadingOr = 'Do ONE of the following:'
QuestMultiHeadingAnd = 'Do ALL of the following:'
QuestStrOneTask = '%(task)s'
QuestStrMultiTask = '%(heading)s%(tasks)s'
QuestDescTaskSingle = '%(task)s.'
QuestDescTaskSingleNoPeriod = '%(task)s'
QuestDescTaskMulti = '\n- %(task)s'
QuestStatusTaskSingle = '%(task)s. %(prog)s'
QuestStatusTaskMulti = '\n- %(task)s %(prog)s'
QuestTaskProgress = '(%(prog)s/%(goal)s)'
QuestProgressComplete = '(COMPLETE)'
QuestTitleNew = 'NEW!'
QuestTitleComplete = 'COMPLETE!'
DefeatProgress = '%d/%d %s Defeated'
DefeatProgressWeapon = '%d/%d %s Defeated Using A %s'
DefeatNPCProgress = '%s Defeated'
RecoverItemProgress = '%d/%d %s Found'
DeliverItemProgress = '%d/%d %s Delivered'
SmuggleItemProgress = '%d/%d %s Smuggled'
PokerProgress = '%d/%d Gold Won'
BlackjackProgress = '%d/%d Gold Won'
TreasureItemProgress = '%d/%d %s Found'
DefeatShipProgress = '%d/%d Ships Sunk'
DefeatShipTypeProgress = '%d/%d %s Sunk'
DefeatShipFactionProgress = '%d/%d %s Sunk'
DefeatShipFactionTypeProgress = '%d/%d %s %ss Sunk'
CaptureShipNPCProgress = '%d/%d %s Found'
QuestRewardDescS = '%s'
QuestRewardDescM = '%s'
QuestRewardDescItem = '%s\n'
QuestButtonNext = 'Next'
QuestButtonLast = 'Okay'
QuestCompleteFrameWorkText = '\n\nReward:'
VisitTaskTitle = 'Visit %s'
BribeTaskTitle = 'Bribe %s'
MaroonTaskTitle = 'Maroon %s'
DefeatNPCTaskTitle = 'Defeat %s'
ViewCutsceneTaskTitle = 'Visit %s'
RecoverAvatarItemTaskTitle = 'Recover Enemy Item'
RecoverShipItemTaskTitle = 'Recover Ship Item'
CaptureShipNPCTaskTitle = 'Capture %s on Ship'
RecoverContainerItemTaskTitle = 'Recover Container Item'
DeliverItemTaskTitle = 'Deliver Item'
SmuggleItemTaskTitle = 'Smuggle Item'
PokerTaskTitle = 'Win at Poker'
BlackjackTaskTitle = 'Win at Blackjack'
RecoverTreasureItemTaskTitle = 'Recover Treasure Item'
DefeatTaskTitle = 'Defeat %s'
DefeatWithWeaponTaskTitle = 'Defeat %s using a %s'
DefeatShipTaskTitle = 'Sink Ship'
CaptureNPCTaskTitle = 'Capture %s'
BossBattleName = 'Boss Battle'
BossBattleTaskTitle = BossBattleName + ': %s'
DeployShipTaskTitle = 'Launch Ship'
VisitTaskDesc = 'Visit \x01questObj\x01%(toNpcName)s\x02'
BribeTaskDesc = 'Bribe \x01questObj\x01%(toNpcName)s\x02 with \x01questObj\x01%(gold)s\x02 gold'
BribeTaskAltDesc = 'Pay \x01questObj\x01%(toNpcName)s\x02 with \x01questObj\x01%(gold)s\x02 gold'
DefeatNPCTaskDesc = 'Defeat \x01questObj\x01%(npcName)s\x02'
ViewCutsceneTaskDesc = 'Visit \x01questObj\x01%(toNpcName)s\x02'
RecoverAvatarItemTaskDescS = 'Recover \x01questObj\x01%(itemName)s\x02 from \x01questObj\x01%(enemyName)s\x02'
RecoverAvatarItemTaskDescP = 'Recover \x01questObj\x01%(num)s %(itemName)s\x02 from \x01questObj\x01%(enemyName)s\x02'
RecoverAvatarItemTaskDescSL = 'Recover \x01questObj\x01%(itemName)s\x02 from \x01questObj\x01%(enemyName)s L%(level)d+\x02'
RecoverAvatarItemTaskDescPL = 'Recover \x01questObj\x01%(num)s %(itemName)s\x02 from \x01questObj\x01L%(level)d+ %(enemyName)s\x02'
RecoverShipItemTaskDescS = 'Recover \x01questObj\x01%(itemName)s\x02 from any ship'
RecoverShipItemLevelTaskDescS = 'Recover \x01questObj\x01%(itemName)s\x02 from any ship \x01questObj\x01L%(level)d+\x02'
RecoverShipItemTaskDescSN = 'Recover \x01questObj\x01%(itemName)s\x02 from any \x01questObj\x01%(shipType)s\x02'
RecoverShipItemLevelTaskDescSN = 'Recover \x01questObj\x01%(itemName)s\x02 from \x01questObj\x01%(shipType)s L%(level)d+\x02'
RecoverShipItemTaskDescP = 'Recover \x01questObj\x01%(num)s %(itemName)s\x02 from any ships'
RecoverShipItemLevelTaskDescP = 'Recover \x01questObj\x01%(num)s %(itemName)s\x02 from any ships \x01questObj\x01L%(level)d+\x02'
RecoverShipItemTaskDescPN = 'Recover \x01questObj\x01%(num)s %(itemName)s\x02 from any \x01questObj\x01%(shipType)ss\x02'
RecoverShipItemLevelTaskDescPN = 'Recover \x01questObj\x01%(num)s %(itemName)s\x02 from any \x01questObj\x01%(shipType)ss\x02 \x01questObj\x01L%(level)d+\x02'
RecoverShipFactionItemTaskDescS = 'Recover \x01questObj\x01%(itemName)s\x02 from \x01questObj\x01%(faction)s ship\x02'
RecoverShipFactionItemLevelTaskDescS = 'Recover \x01questObj\x01%(itemName)s\x02 from \x01questObj\x01%(faction)s\x02 ship \x01questObj\x01L%(level)d+\x02'
RecoverShipFactionItemTaskDescSN = 'Recover \x01questObj\x01%(itemName)s\x02 from \x01questObj\x01%(faction)s %(shipType)s\x02'
RecoverShipFactionItemLevelTaskDescSN = 'Recover \x01questObj\x01%(itemName)s\x02 from \x01questObj\x01%(faction)s %(shipType)s L%(level)d+\x02'
RecoverShipFactionItemTaskDescP = 'Recover \x01questObj\x01%(num)s %(itemName)s\x02 from \x01questObj\x01%(faction)s\x02 ships'
RecoverShipFactionItemLevelTaskDescP = 'Recover \x01questObj\x01%(num)s %(itemName)s\x02 from \x01questObj\x01%(faction)s\x02 ships \x01questObj\x01L%(level)d+\x02'
RecoverShipFactionItemTaskDescPN = 'Recover \x01questObj\x01%(num)s %(itemName)s\x02 from \x01questObj\x01%(faction)s %(shipType)ss\x02'
RecoverShipFactionItemLevelTaskDescPN = 'Recover \x01questObj\x01%(num)s %(itemName)s\x02 from \x01questObj\x01%(faction)s %(shipType)ss\x02 \x01questObj\x01L%(level)d+\x02'
CaptureShipNPCTaskDescS = 'Capture \x01questObj\x01%(npcName)s\x02 from any ship'
CaptureShipNPCTaskDescSN = 'Capture \x01questObj\x01%(npcName)s\x02 from any \x01questObj\x01%(shipType)s\x02'
CaptureShipFactionNPCTaskDescS = 'Capture \x01questObj\x01%(npcName)s\x02 from \x01questObj\x01%(faction)s\x02 ship'
CaptureShipFactionNPCTaskDescSN = 'Capture \x01questObj\x01%(npcName)s\x02 from \x01questObj\x01%(faction)s %(shipType)s\x02'
DeliverItemTaskDescS = 'Deliver \x01questObj\x01%(itemName)s\x02 to \x01questObj\x01%(location)s\x02'
DeliverItemTaskDescP = 'Deliver \x01questObj\x01%(num)s %(itemName)s\x02 to \x01questObj\x01%(location)s\x02'
SmuggleItemTaskDescS = 'Smuggle \x01questObj\x01%(itemName)s\x02 to \x01questObj\x01%(location)s\x02'
SmuggleItemTaskDescP = 'Smuggle \x01questObj\x01%(num)s %(itemName)s\x02 to \x01questObj\x01%(location)s\x02'
PokerTaskDescS = 'Win \x01questObj\x01%(gold)s gold\x02 playing poker'
PokerTaskDescP = 'Win \x01questObj\x01%(gold)s gold\x02 playing poker'
BlackjackTaskDescS = 'Win \x01questObj\x01%(gold)s gold\x02 playing blackjack'
BlackjackTaskDescP = 'Win \x01questObj\x01%(gold)s gold\x02 playing blackjack'
RecoverTreasureItemTaskDescS = 'Recover \x01questObj\x01%(itemName)s\x02 from a buried treasure chest'
RecoverTreasureItemTaskDescP = 'Recover \x01questObj\x01%(num)s %(itemName)s\x02 from a buried treasure chest'
RecoverContainerItemTaskDescS = 'Recover \x01questObj\x01%(itemName)s\x02 from a storage container'
RecoverContainerItemTaskDescP = 'Recover \x01questObj\x01%(num)s %(itemName)s\x02 from a storage container'
DefeatTaskDescS = 'Defeat \x01questObj\x01%(enemyName)s\x02'
DefeatTaskDescSWeapon = 'Defeat \x01questObj\x01%(enemyName)s\x02 using a \x01questObj\x01%(weaponType)s\x02'
DefeatTaskDescP = 'Defeat \x01questObj\x01%(num)s %(enemyName)s\x02'
DefeatTaskDescPWeapon = 'Defeat \x01questObj\x01%(num)s %(enemyName)s\x02 using a \x01questObj\x01%(weaponType)s\x02'
DefeatTaskDescSL = 'Defeat \x01questObj\x01%(enemyName)s L%(level)d+\x02'
DefeatTaskDescSLWeapon = 'Defeat \x01questObj\x01%(enemyName)s L%(level)d+\x02 using a \x01questObj\x01%(weaponType)s\x02'
DefeatTaskDescPL = 'Defeat \x01questObj\x01%(num)s L%(level)d+ %(enemyName)s\x02'
DefeatTaskDescPLWeapon = 'Defeat \x01questObj\x01%(num)s L%(level)d+ %(enemyName)s\x02 using a \x01questObj\x01%(weaponType)s\x02'
DefeatShipTaskDescS = 'Sink a ship'
DefeatShipTaskDescSN = 'Sink a \x01questObj\x01%(shipType)s\x02'
DefeatShipTaskDescP = 'Sink \x01questObj\x01%(num)s\x02 ships'
DefeatShipTaskDescPN = 'Sink \x01questObj\x01%(num)s\x02 %(shipType)ss'
DefeatShipFactionTaskDescS = 'Sink \x01questObj\x01%(faction)s\x02 ship'
DefeatShipFactionTaskDescSN = 'Sink \x01questObj\x01%(faction)s %(shipType)s\x02'
DefeatShipFactionTaskDescP = 'Sink \x01questObj\x01%(num)s %(faction)s\x02 ships'
DefeatShipFactionTaskDescPN = 'Sink \x01questObj\x01%(num)s %(faction)s %(shipType)ss\x02'
CaptureNPCTaskDesc = 'Capture \x01questObj\x01%(npcName)s\x02'
MaroonNPCTaskDesc = 'Maroon \x01questObj\x01%(npcName)s\x02 at \x01questObj\x01%(location)s\x02'
BossBattleTaskDesc = 'Complete ' + BossBattleName + ' : \x01questObj\x01%(treasureMapId)s\x02'
DeployShipTaskDesc = 'Launch Your Ship'
MultipleQuestReturnIds = 'Return to one of the following: \x01questObj\x01%(npcNames)s\x02'
MultipleChoiceQuestReturnIds = 'Return to one of the following after all parts completed: \x01questObj\x01%(npcNames)s\x02'
SingleQuestReturnId = 'Return to \x01questObj\x01%(npcName)s\x02.'
SingleChoiceQuestReturnId = 'Return to \x01questObj\x01%(npcName)s\x02 after all parts completed.'
DefaultTownfolkName = 'Unknown Townfolk'
ReturnVisitQuestTitle = 'Visit %s'
ReturnVisitQuestDesc = 'Return to \x01questObj\x01%s\x02.'
ReturnVisitQuestDialog = "Good, you're back. Let's start again."
QuestItemGuiCompleteFormat = '\x01questTitle\x01%(title)s\x02    \x01CPGreen\x01COMPLETE\x02\n\n\x01questTitle\x01Task\x02\n%(status)s\n\n%(returnTo)s\n\n\x01questTitle\x01Reward\x02\n%(reward)s\n\n'
QuestItemGuiIncompleteFormat = '\x01questTitle\x01%(title)s\x02\n\n\x01questTitle\x01Task\x02\n%(status)s\n\n\x01questTitle\x01Description\x02\n%(desc)s\n\n\x01questTitle\x01Reward\x02\n%(reward)s\n\n'
QuestItemGuiCompleteFormatNoReward = '\x01questTitle\x01%(title)s\x02    \x01CPGreen\x01COMPLETE\x02\n\n\x01questTitle\x01Task\x02\n%(status)s\n\n%(returnTo)s\n\n'
QuestItemGuiIncompleteFormatNoReward = '\x01questTitle\x01%(title)s\x02\n\n\x01questTitle\x01Task\x02\n%(status)s\n\n\x01questTitle\x01Description\x02\n%(desc)s\n\n'
QuestItemGuiHeadingFormat = '\x01questTitle\x01%(title)s\x02\n\n\x01questTitle\x01Description\x02\n%(desc)s'
QuestItemGuiHeadingFormatWithReward = '\x01questTitle\x01%(title)s\x02\n\n\x01questTitle\x01Description\x02\n%(desc)s\n\n\x01questTitle\x01Reward\x02\n%(reward)s\n\n'
Ship = ('a ship', 'ships')
QuestSCBribe = 'I need to  bribe %(npcName)s.'
QuestSCMaroonNPC = 'Maroon %(npcName)s at %(location)s.'
QuestSCFindNPC = 'I need to find %(npcName)s.'
QuestSCDefeatEnemy = 'I need to kill %(enemyName)s.'
QuestSCDefeatEnemyWeapon = 'I need to kill %(enemyName)s using a %(weaponType)s.'
QuestSCDefeatEnemyLvl = 'I need to kill %(enemyName)s L%(level)d+.'
QuestSCDefeatEnemyLvlWeapon = 'I need to kill %(enemyName)s L%(level)d+ using a %(weaponType)s.'
QuestSCDefeatEnemies = 'I need to kill %(num)s %(enemyName)s.'
QuestSCDefeatEnemiesWeapon = 'I need to kill %(num)s %(enemyName)s using a %(weaponType)s.'
QuestSCDefeatEnemiesLvl = 'I need to kill %(num)s L%(level)d+ %(enemyName)s.'
QuestSCDefeatEnemiesLvlWeapon = 'I need to kill %(num)s L%(level)d+ %(enemyName)s using a %(weaponType)s.'
QuestSCCapture = 'I need to capture a ship.'
QuestSCCaptureShip = 'I need to capture a %(shipType)s.'
QuestSCCaptureFaction = 'I need to capture a %(faction)s ship.'
QuestSCCaptureFactionShip = 'I need to capture a %(faction)s  %(shipType)s.'
QuestSCSink = 'I need to sink a ship.'
QuestSCSinkShip = 'I need to sink a %(shipType)s.'
QuestSCSinkNum = 'I need to sink %(num)s ships.'
QuestSCSinkShipNum = 'I need to sink %(num)s %(shipType)s.'
QuestSCSinkFaction = 'I need to sink %(faction)s ship.'
QuestSCSinkFactionShip = 'I need to sink %(faction)s %(shipType)s.'
QuestSCSinkFactionNum = 'I need to sink %(num)s %(faction)s ship.'
QuestSCSinkFactionNumShip = 'I need to sink %(num)s %(faction)s %(shipType)s.'
QuestSCCaptureNPC = 'I need to capture %(npcName)s.'
QuestSCCaptureNPCShip = 'I need to capture %(npcName)s from any %(shipType)s.'
QuestSCCaptureNPCFaction = 'I need to capture %(npcName)s from %(faction)s ship.'
QuestSCCaptureNPCFactionShip = 'I need to capture %(npcName)s from %(faction)s %(shipType)s.'
QuestSCRecoverItem = 'I need to recover %(itemName)s from %(enemyName)s.'
QuestSCRecoverItemNum = 'I need to recover %(num)s %(itemName)s from %(enemyName)s.'
QuestSCRecoverItemLvl = 'I need to recover %(itemName)s from %(enemyName)s L%(level)d+.'
QuestSCRecoverItemNumLvl = 'I need to recover %(num)s %(itemName)s from L%(level)d+ %(enemyName)s.'
QuestSCRecoverShipItem = 'I need to recover %(itemName)s from any ship.'
QuestSCRecoverShipItemShip = 'I need to recover %(itemName)s from any %(shipType)s.'
QuestSCRecoverShipItemNum = 'I need to recover %(num)s %(itemName)s from any ships.'
QuestSCRecoverShipItemNumShip = 'I need to recover %(num)s %(itemName)s from any %(shipType)s.'
QuestSCRecoverFactionShipItem = 'I need to recover %(itemName)s from %(faction)s ship.'
QuestSCRecoverFactionShipItemShip = 'I need to recover %(itemName)s from %(faction)s %(shipType)s.'
QuestSCRecoverFactionShipItemNum = 'I need to recover %(num)s %(itemName)s from %(faction)s ships.'
QuestSCRecoverFactionShipItemNumShip = 'I need to recover %(num)s %(itemName)s from %(faction)s %(shipType)s.'
QuestSCBossBattle = 'I need to complete the ' + BossBattleName + ': %s.'
QuestSCBossBattleMap = 'I need to complete the ' + BossBattleName + ': %(treasureMapId)s.'
QuestSCDeliverItem = 'I need to deliver %(itemName)s to %(location)s.'
QuestSCDeliverItemNum = 'I need to deliver %(num)s %(itemName)s to %(location)s.'
QuestSCSmuggleItem = 'I need to smuggle %(itemName)s to %(location)s.'
QuestSCSmuggleItemNum = 'I need to smuggle %(num)s %(itemName)s to %(location)s.'
QuestSCPokerWinGold = 'I need to win %(gold)s gold playing poker.'
QuestSCBlackjackWinGold = 'I need to win %(gold)s gold playing blackjack.'
QuestSCTreasureItem = 'I need to recover %(itemName)s from a buried treasure chest.'
QuestSCTreasureItemNum = 'I need to recover %(num)s %(itemName)s from a buried treasure chest.'
QuestSCContainerItem = 'I need to recover %(itemName)s from a storage container.'
QuestSCContainerItemNum = 'I need to recover %(num)s %(itemName)s from a storage container.'
QuestSCDeployShip = 'I need to launch my ship.'
QuestSCWhereIsNPC = 'Where do I find %(npcName)s?'
QuestSCWhereIsEnemy = 'Where do I find %(enemyName)s?'
QuestSCWhereIsShip = 'Where do I find %(shipType)s?'
QuestSCWhereIsFaction = 'Where do I find  %(faction)s ships?'
QuestSCWhereIsFactionShip = 'Where do I find  %(faction)s %(shipType)s?'
QuestSCWhereIsLocation = 'Where is %(location)s?'
QuestSCWhereIsContainers = 'Where can I find containers to search?'
QuestSCFindTreasure = 'How do I find buried treasure?'
QuestSCFindHiddenContainer = 'How do I find hidden items?'
QuestSCHowToBribe = 'How do I bribe somebody?'
QuestSCWinPoker = 'How do I find a poker game?'
QuestSCWinBlackjack = 'How do I find a blackjack game?'
QuestSCHowToCaptureShip = 'How do I capture a ship?'
QuestSCHowToCaptureNPC = 'How do I capture an NPC?'
QuestSCHowDoIMaroon = 'How do I maroon someone?'
QuestSCHowDoIRecover = 'How do I recover %(itemName)s from %(enemyName)s?'
QuestSCHowDoIRecoverShipItem = 'How do I recover an %(itemName)s from a ship?'
QuestSCWhereDoIDeployShip = 'Where do I launch my ship?'
QuestSCHowDoIDeployShip = 'How do I launch my ship?'
QuestItemNotifications = {
    1: 'Enough %s have already been acquired.',
    2: '%s acquired. Quest Complete!',
    3: '%s acquired. Quest Updated.',
    4: 'Checking for %s... not found.',
    5: '%s are not found here. Look elsewhere.'}
QuestNPCNotifications = {
    1: '%s has already been captured.',
    2: '%s captured. Quest Complete!',
    3: '%s captured. Quest Updated.',
    4: 'Checking for %s... not found.',
    5: '%s will not be found here. Look elsewhere.'}
QuestItemNames = {
    0: ('a key', 'keys', 'Keys'),
    1: ('a sea chart', 'sea charts', 'Sea Charts'),
    2: ('an earring', 'earrings', 'Earrings'),
    3: ('a barrel of rum', 'barrels of rum', 'Barrels of Rum'),
    4: ('a crab claw', 'crab claws', 'Crab Claws'),
    5: ('a bag of coins', 'bags of coins', 'Bags of Coins'),
    6: ('a tattoo pattern', 'tattoo patterns', 'Tattoo Patterns'),
    7: ('a copper rod', 'copper rods', 'Copper Rods'),
    8: ('blood', 'blood', 'Blood'),
    9: ('a flag', 'flags', 'Flags'),
    10: ('a list', 'lists', 'Lists'),
    11: ('an arrest warrant', 'arrest warrants', 'Arrest Warrants'),
    12: ('a handkerchief', 'handkerchiefs', 'Handkerchiefs'),
    13: ('bat guano', 'bat guano', 'Bat Guano'),
    14: ('a remedy', 'remedies', 'Remedies'),
    15: ('personal effects', 'personal effects', 'Personal Effects'),
    16: ('an engraved pearl', 'engraved pearls', 'Engraved Pearls'),
    17: ('a severed arm', 'severed arms', 'Severed Arms'),
    18: ('alligator saliva', 'alligator saliva', 'Alligator Saliva'),
    19: ('venom', 'venom', 'Venom'),
    20: ('cursed wood', 'cursed wood', 'Cursed Wood'),
    21: ('a map', 'maps', 'Maps'),
    22: ('a necklace', 'necklaces', 'Necklaces'),
    23: ('a shipment of tin', 'shipments of tin', 'Shipments of Tin'),
    24: ('a shipment of sand', 'shipments of sand', 'Shipments of Sand'),
    25: ('a glass ring', 'glass rings', 'Glass Rings'),
    26: ('a wooden plate', 'wooden plates', 'Wooden Plates'),
    27: ('a chicken', 'chickens', 'Chickens'),
    28: ('a pig', 'pigs', 'Pigs'),
    29: ('an egg', 'eggs', 'Eggs'),
    30: ('a tooth', 'teeth', 'Teeth'),
    31: ('a wasp wing', 'wasp wings', 'Wasp Wings'),
    32: ('an alligator scale', 'alligator scales', 'Alligator Scales'),
    33: ('poison', 'poison', 'Poison'),
    34: ('a lump of mud', 'lumps of mud', 'Lumps of Mud'),
    35: ('a pint of grog', 'pints of grog', 'Pints of Grog'),
    36: ('a doll', 'dolls', 'Dolls'),
    37: ('a dinghy', 'dinghies', 'Dinghies'),
    38: ('release orders', 'release orders', 'Release Orders'),
    39: ('a barrel of honey', 'barrels of honey', 'Barrels of Honey'),
    40: ('a dress', 'dresses', 'Dresses'),
    41: ('a die', 'dice', 'Dice'),
    42: ('a wasp egg', 'wasp eggs', 'Wasp Eggs'),
    43: ('a container of bile', 'containers of bile', 'Containers of Bile'),
    44: ('a bottle of rum', 'bottles of rum', 'Bottles of Rum'),
    45: ('a bracelet', 'bracelets', 'Bracelets'),
    46: ('a needle', 'needles', 'Needles'),
    47: ('a kraken eye', 'kraken eyes', 'Kraken Eyes'),
    48: ('powder', 'powder', 'Powder'),
    49: ('croc water', 'croc water', 'Croc Water'),
    50: ('entrails', 'entrails', 'Entrails'),
    51: ('a splinter', 'splinters', 'Splinters'),
    52: ('dust', 'dust', 'Dust'),
    53: ('earth', 'earth', 'Earth'),
    54: ('a lichen', 'lichens', 'Lichens'),
    55: ('water', 'water', 'Water'),
    56: ('a scorpion egg', 'scorpion eggs', 'Scorpion Eggs'),
    57: ('bloody treasure', 'bloody treasure', 'Bloody Treasure'),
    58: ('nightshade', 'nightshade', 'Nightshade'),
    59: ('a whisker', 'whiskers', 'Whiskers'),
    60: ('a jar', 'jars', 'Jars'),
    61: ('a piece of paper', 'papers', 'Papers'),
    62: ('a bone', 'bones', 'Bones'),
    63: ('bone shavings', 'bone shavings', 'Bone Shavings'),
    64: ('a chest', 'chests', 'Chests'),
    65: ('a hook arm', 'hook arms', 'Hook Arms'),
    66: ('a diamond', 'diamonds', 'Diamonds'),
    67: ('a box of cigars', 'boxes of cigars', 'Boxes of Cigars'),
    68: ('a gold chain', 'gold chains', 'Gold Chains'),
    69: ('cargo', 'cargo', 'Cargo'),
    70: ('a ladle', 'ladles', 'Ladles'),
    71: ('sugar', 'sugar', 'Sugar'),
    72: ('a bottle', 'bottles', 'Bottles'),
    73: ('a barrel of molasses', 'barrels of molasses', 'Barrels of Molasses'),
    74: ('vanilla', 'vanilla', 'Vanilla'),
    75: ('bone dust', 'pinches of bone dust', 'Pinches Bone Dust'),
    76: ('swamp gas', 'swamp gas', 'Swamp Gas'),
    77: ('a stinger', 'stingers', 'Stingers'),
    78: ('a bladder', 'bladders', 'Bladders'),
    79: ('a pint', 'pints', 'Pints'),
    80: ('a pinch of cinnamon', 'pinches of cinnamon', 'Pinches of Cinnamon'),
    81: ('a coconut', 'coconuts', 'Coconuts'),
    82: ('a feather', 'feathers', 'Feathers'),
    83: ('a barrel of honey', 'barrels of honey', 'Barrels of Honey'),
    84: ('barnacles', 'barnacles', 'Barnacles'),
    85: ('a hairball', 'hairballs', 'Hairballs'),
    86: ('a flea', 'fleas', 'Fleas'),
    87: ('a drink', 'drinks', 'Drinks'),
    88: ('a schedule', 'schedules', 'Schedules'),
    89: ('a hair', 'hairs', 'Hairs'),
    90: ('honeysuckle', 'honeysuckle', 'Honeysuckle'),
    91: ('sap', 'sap', 'Sap'),
    92: ('a tear', 'tears', 'Tears'),
    93: ('a bottle of perfume', 'bottles of perfume', 'Bottles of Perfume'),
    94: ('oil', 'oils', 'Oils'),
    95: ('rum', 'rum', 'Rum'),
    96: ('orders', 'orders', 'Orders'),
    97: ('salve', 'salve', 'Salve'),
    98: ('wax', 'wax', 'Wax'),
    99: ('a chunk of meat', 'chunks of meat', 'Chunks of Meat'),
    100: ('a plank of wood', 'planks of wood', 'Planks of Wood'),
    101: ('a nail', 'nails', 'Nails'),
    102: ('a bucket of pitch', 'buckets of pitch', 'Buckets of Pitch'),
    103: ('a saw', 'saws', 'Saws'),
    104: ('a ship in a bottle', 'ships in bottles', 'Ships in Bottles'),
    105: ('a wood beam', 'wood beams', 'Wood Beams'),
    106: ('a bolt', 'bolts', 'Bolts'),
    107: ('a yard of sailcloth', 'yards of sailcloth', 'Yards of Sailcloth'),
    108: ('a rope', 'ropes', 'Ropes'),
    109: ('a cannon', 'cannons', 'Cannons'),
    110: ('a figurehead', 'figureheads', 'Figureheads'),
    111: ('a parrot', 'parrots', 'Parrots'),
    112: ('a document', 'documents', 'Documents'),
    113: ('an eye', 'eyes', 'Eyes'),
    114: ('a portrait', 'portraits', 'Portraits'),
    115: ('a treasure', 'treasures', 'Treasures'),
    116: ('a bundle of straw', 'bundles of straw', 'Bundles of Straw'),
    117: ('a bolt of silk', 'bolts of silk', 'Bolts of Silk'),
    118: ('a spool of wire', 'spools of wire', 'Spools of Wire'),
    119: ('a bag', 'bags', 'Bags'),
    120: ('dirt', 'dirt', 'Dirt'),
    121: ('a ring', 'rings', 'Rings'),
    122: ('a medal', 'medals', 'Medals'),
    123: ('a reagent', 'reagents', 'Reagents'),
    124: ('a chess piece', 'chess pieces', 'Chess Pieces'),
    125: ('a figurine', 'figurines', 'Figurines'),
    126: ('a steel rod', 'steel rods', 'Steel Rods'),
    127: ('a silver ingot', 'silver ingots', 'Silver Ingots'),
    128: ('tongs', 'tongs', 'Tongs'),
    129: ('a bucket of coal', 'buckets of coal', 'Buckets of Coal'),
    130: ('a message', 'messages', 'Messages'),
    131: ('knives', 'knives', 'Knives'),
    132: ('a grenade', 'grenades', 'Grenades'),
    133: ('a branch', 'branches', 'Branches'),
    134: ('a shrunken head', 'shrunken heads', 'Shrunken Heads'),
    135: ('a bucket of saltpeter', 'buckets of saltpeter', 'Buckets of Saltpeter'),
    136: ('a sack of charcoal', 'sacks of charcoal', 'Sacks of Charcoal'),
    137: ('a cup of sulfur', 'cups of sulfur', 'Cups of Sulfur'),
    138: ('a fuse', 'fuses', 'Fuses'),
    139: ('a flint', 'flints', 'Flints'),
    140: ('a casing', 'casings', 'Casings'),
    141: ('a bucket of tar', 'buckets of tar', 'Buckets of Tar'),
    142: ('a teleport totem', 'teleport totems', 'Teleport Totems'),
    143: ('a pair of bat wings', 'pairs of bat wings', 'Pairs of Bat Wings'),
    144: ('an alligator tooth', 'alligator teeth', 'Alligator Teeth'),
    145: ('a wasp essence', 'wasp essences', 'Wasp Essences'),
    146: ('a tortugan artifact', 'tortugan artifacts', 'Tortugan Artifacts'),
    147: ('a yard of cotton', 'yards of cotton', 'Yards of Cotton'),
    148: ('an iron bar', 'iron bars', 'Iron Bars'),
    149: ('an alligator tail', 'alligator tails', 'Alligator Tails'),
    150: ('a crab shell', 'crab shells', 'Crab Shells'),
    151: ('bat hair', 'bat hair', 'Bat Hair'),
    152: ('scorpion blood', 'scorpion blood', 'Scorpion Blood'),
    153: ('scorpion venom', 'scorpion venom', 'Scorpion Venom'),
    154: ('a barrel of whiskey', 'barrels of whiskey', 'Barrels of Whiskey'),
    155: ('a set of bar glasses', 'sets of bar glasses', 'Sets of Bar Glasses'),
    156: ('a bag of coal', 'bags of coal', 'Bags of Coal'),
    157: ('smithing tools', 'smithing tools', 'Smithing Tools'),
    158: ('the name of the attacker', 'the name of the attacker', 'the Name of the Attacker'),
    159: ('a fly trap leaf', 'fly trap leaves', 'Fly Trap Leaves'),
    160: ('a fly trap root', 'fly trap roots', 'Fly Trap Roots'),
    161: ('a Navy coat', 'Navy coats', 'Navy Coats'),
    162: ('The First Medal of Port Royal', '', 'The First Medal of Port Royal'),
    163: ('The Eye of Nabai', '', 'The Eye of Nabai'),
    164: ('a well-fashioned voodoo doll head', '', 'Well-Fashioned Voodoo Doll Heads'),
    165: ('a well-fashioned voodoo doll torso', '', 'Well-Fashioned Voodoo Doll Torsos'),
    166: ('a well-fashioned voodoo doll left arm', '', 'Well-Fashioned Voodoo Doll Left Arms'),
    167: ('a well-fashioned voodoo doll right arm', '', 'Well-Fashioned Voodoo Doll Right Arms'),
    168: ('a well-fashioned voodoo doll left leg', '', 'Well-Fashioned Voodoo Doll Left Legs'),
    169: ('a well-fashioned voodoo doll right leg', '', 'Well-Fashioned Voodoo Doll Right Legs'),
    170: ('a navy musket', 'navy muskets', 'Navy Muskets'),
    171: ('a pair of Navy pants', 'pairs of Navy pants', 'Pairs of Navy Pants'),
    172: ('a sergeant badge', 'sergeant badges', 'Sergeant Badges'),
    173: ('a prison key', 'prison keys', 'Prison Keys'),
    174: ('the hidden coins map for Fort Charles', '', ''),
    175: ('a sewing needle', 'sewing needles', 'Sewing Needles'),
    176: ('a guard schedule', 'guard schedules', 'Guard Schedules'),
    177: ('a navy ship schedule', 'navy ship schedules', 'Navy Ship Schedules'),
    178: ('a canteen of latrine water', 'canteens of latrine water', 'Canteens of Latrine Water'),
    179: ('a cup of moonlit water', 'cups of moonlit water', 'Cups of Moonlit Water'),
    180: ('a bottle of battle-touched water', 'bottles of battle-touched water', 'Bottles of Battle-Touched Water'),
    181: ('a pair of dice', 'pairs of dice', 'Pairs of Dice'),
    182: ('a water canteen', 'water canteens', 'Water Canteens'),
    183: ('a stash of rubies', 'a stash of rubies', 'Stash of Rubies'),
    184: ('a stash of amethysts', 'a stash of amethysts', 'Stash of Amethysts'),
    185: ('a stash of sapphires', 'a stash of sapphires', 'Stash of Sapphires'),
    186: ('a bottle of fine ink', 'fine inks', 'Fine Inks'),
    187: ('a deed', 'deeds', 'Deeds'),
    188: ('a EITC coat', 'EITC coats', 'EITC Coats'),
    189: ('a pair of EITC pants', 'pairs of EITC pants', 'Pairs of EITC Pants'),
    190: ('a shop application', 'shop applications', 'Shop Applications'),
    191: ('a hide', 'hides', 'Hides'),
    192: ('a contract', 'contracts', 'Contracts'),
    193: ('a blood sample', 'blood samples', 'Blood Samples'),
    194: ('a bandage', 'bandages', 'Bandages'),
    195: ('a medical tool', 'medical tools', 'Medical Tools'),
    196: ('a diary', 'diaries', 'Diary'),
    197: ('a ship log', 'ship logs', 'Ship Logs'),
    198: ('a family heirloom', 'family heirlooms', 'Family Heirlooms'),
    199: ('a gun', 'guns', 'Guns'),
    200: ('a gun order', 'gun orders', 'Gun Orders'),
    201: ('an antique pistol', 'antique pistols', 'Antique Pistols'),
    202: ('a ship plan', 'ship plans', 'Ship Plans'),
    203: ('a background check', 'background checks', 'Background Checks'),
    204: ('a bar of fine steel', 'bars of fine steel', 'Bars Of Fine Steel'),
    205: ('a strap of leather', 'leather straps', 'Leather Straps'),
    206: ('a blade sharpener', 'blade sharpeners', 'Blade Sharpeners'),
    207: ('a page from Pirate Lore', 'pages from Pirate Lore', 'Pages from Pirate Lore'),
    208: ('a chest of Pirate Lore', 'chests of Pirate Lore', 'Chests of Pirate Lore'),
    209: ('a book of Pirate Lore', 'books of Pirate Lore', 'Books of Pirate Lore'),
    210: ('an EITC manual', 'EITC manuals', 'EITC Manuals'),
    211: ('an unfinished book of Pirate Lore', 'unfinished books of Pirate Lore', 'Unfinished Books of Pirate Lore'),
    212: ('an alligator eye', 'alligator eyes', 'Alligator Eyes'),
    213: ('a wasp', 'wasps', 'Wasps'),
    214: ('a scorpion eye', 'scorpion eyes', 'Scorpion Eyes'),
    215: ('a bat eye', 'bat eyes', 'Bat Eyes'),
    216: ('a cloudy blue orb', 'cloudy blue orbs', 'Cloudy Blue Orbs'),
    217: ('a skeleton rib', 'skeleton ribs', 'Skeleton Ribs'),
    218: ('a badge', 'badges', 'Badges'),
    219: ('a writ of authority', 'writs of authority', 'Writs of Authority'),
    220: ('an alligator tooth', 'alligator teeth', 'Alligator Teeth'),
    221: ('a bat claw', 'bat claws', 'Bat Claws'),
    222: ('a skeleton bone', 'skeleton bones', 'Skeleton Bones'),
    223: ('a sunken ship mast', 'sunken ship masts', 'Sunken Ship Masts'),
    224: ('a bottle of battle-touched earth', 'bottles of battle-touched earth', 'Bottles of Battle-Touched Earth'),
    225: ('a relic piece', 'relic pieces', 'Relic Pieces'),
    226: ('Capt. Teague', 'Capt. Teague', 'Capt. Teague'),
    227: ('a spool of thread', 'spools of thread', 'Spools of Thread'),
    228: ('a rare feather', 'rare feathers', 'Rare Feathers'),
    229: ('a manifest', 'manifests', 'Manifests'),
    230: ("Bingham's diary", "Bingham's diary", "Bingham's Diary"),
    231: ('a bolt of cloth', 'bolts of cloth', 'Bolts of Cloth'),
    232: ('a pair of fine scissors', 'pairs of fine scissors', 'Pairs of Fine Scissors'),
    233: ('a spool of silk thread', 'spools of silk thread', 'Spools of Silk Thread'),
    234: ("Scarlet's pearl", "Scarlet's pearls", "Scarlet's Pearls"),
    235: ('a letter from Scarlet', 'letters from Scarlet', 'Letters From Scarlet'),
    236: ('a belt buckle', 'belt buckles', 'Belt Buckles'),
    237: ('a fine shoe design', 'fine shoe designs', 'Fine Shoe Designs'),
    238: ('a scorpion shell', 'scorpion shells', 'Scorpion Shells'),
    239: ('a piece of kraken cloth', 'kraken cloths', 'Kraken Cloths'),
    240: ('a cursed button', 'cursed buttons', 'Cursed Buttons'),
    241: ('a piece of cursed bark', 'cursed bark', 'Cursed Bark'),
    242: ('a piece of cursed cloth', 'cursed cloth', 'Cursed Cloth'),
    243: ('a piece of cursed thread', 'cursed threads', 'Cursed Thread'),
    244: ('a cursed needle', 'cursed needles', 'Cursed Needles'),
    245: ('a voodoo artifact', 'voodoo artifacts', 'Voodoo Artifacts'),
    246: ('a chunk of rotten meat', 'chunks of rotten meat', 'Chunks of Rotten Meat'),
    247: ('a compass', 'compasses', 'Compasses'),
    248: ("Lockgrim's letter", "Lockgrim's letters", "Lockgrim's Letters"),
    249: ('a tentacle', 'tentacles', 'Tentacles'),
    250: ('an Urchinfist eye', 'Urchinfist eyes', 'Urchinfist Eyes'),
    251: ('a cursed chest', 'cursed chests', 'Cursed Chests'),
    252: ('a bottle of fine rum', 'bottles of fine rum', 'Bottles of Fine Rum'),
    253: ("Turk's lucky deck", "Turk's lucky deck", "Turk's Lucky Deck"),
    254: ('a Navy shoestring', 'Navy shoestrings', 'Navy Shoestrings'),
    255: ('a Navy anchor', 'Navy anchors', 'Navy Anchors'),
    256: ('a EITC parchment', 'EITC parchments', 'EITC Parchments'),
    257: ('an empty flask', 'empty flasks', 'Empty Flasks'),
    258: ('a sail', 'sails', 'Sails'),
    259: ('a ship wheel', 'ship wheels', 'Ship Wheels'),
    260: ('a piece of Navy fabric', 'pieces of Navy fabric', 'Pieces of Navy Fabric'),
    261: ('a scrap of cursed sail cloth', 'scraps of cursed sail cloth', 'Scraps of Cursed Sail Cloth'),
    262: ('a suit of spanish armor', 'suits of spanish armor', 'Suits of Spanish Armor'),
    263: ('a spanish pistol component', 'spanish pistol components', 'Spanish Pistol Components'),
    264: ('a gun stock', 'gun stocks', 'Gun Stocks'),
    265: ('a bone handle', 'bone handles', 'Bone Handles'),
    266: ('a lock of hair', 'locks of hair', 'Locks of Hair'),
    267: ('a wooden statuette', 'wooden statuettes', 'Wooden Statuettes'),
    268: ('a barrel of gun powder', 'barrels of gun powder', 'Barrels of Gun Powder'),
    269: ('a spar', 'spars', 'Spars'),
    270: ('a stolen dagger', 'stolen daggers', 'Stolen Daggers'),
    271: ('a gem', 'gems', 'Gems'),
    272: ('a bar of navy steel', 'bars of navy steel', 'Bars of Navy Steel'),
    273: ('a gold-handle rapier', 'gold-handle rapiers', 'Gold Handle Rapiers')}
AnyAvType = ('Anyone', ('an enemy', 'enemies'))
FactionAvTypeNames = {
    0: ('Undead', ('a Skeleton', 'Skeletons')),
    1: ('Navy', ('a Navy Soldier', 'Navy Soldiers')),
    2: ('Creature', ('a Creature', 'Creatures')),
    3: ('Townsfolk', ('a Townsperson', 'Townsfolk')),
    4: ('Pirate', ('a Pirate', 'Pirates')),
    5: ('East India Trading Co', ('an EITC Soldier', 'EITC Soldiers'))}
FactionShipTypeNames = {
    0: ('Undead', ('a Skeleton', 'Skeleton')),
    1: ('Navy', ('a Navy', 'Navy')),
    2: ('Creature', ('a Creature', 'Creature')),
    3: ('Townsfolk', ('a Townsperson', 'Townsfolk')),
    4: ('Pirate', ('a Pirate', 'Pirate')),
    5: ('East India Trading Co', ('an East India Trading Co', 'East India Trading Co')),
    6: ('French Skeleton', ('a French Skeleton', 'French Skeleton')),
    7: ('Spanish Skeleton', ('a Spanish Skeleton', 'Spanish Skeleton'))}
TrackAvTypeNames = {
    0: {
        0: ('Earth Undead', ('an Earth Skeleton', 'Earth Skeletons')),
        1: ('Air Undead', ('an Air Skeleton', 'Air Skeletons')),
        2: ('Fire Undead', ('a Fire Skeleton', 'Fire Skeletons')),
        3: ('Water Undead', ('a Water Skeleton', 'Water Skeletons')),
        4: ('Classic Undead', ('a Classic Skeleton', 'Classic Skeletons')),
        5: ('Boss Undead', ('a Boss Skeleton', 'Boss Skeletons')),
        6: ('French Undead', ('a French Skeleton', 'French Skeletons')),
        7: ('Spanish Undead', ('a Spanish Skeleton', 'Spanish Skeletons'))},
    1: {
        0: ('Navy Soldiers', ('a Navy Soldier', 'Navy Soldiers')),
        1: ('Navy Marksmen', ('a Navy Marksman', 'Navy Marksmen')),
        2: ('Navy Officer', ('a Navy Officer', 'Navy Officers'))},
    2: {
        0: ('Land Creatures', ('a Land Creature', 'Land Creatures')),
        1: ('Sea Creatures', ('a Sea Creature', 'Sea Creatures')),
        2: ('Air Creatures', ('an Air Creature', 'Air Creatures')),
        3: ('Sea Monsters', ('a Sea Monster', 'Sea Monsters')),
        4: ('Animals', ('an Animal', 'Animals'))},
    3: {
        0: ('Commoners', ('a Commoner', 'Commoners')),
        1: ('Merchants', ('a Merchant', 'Merchants')),
        2: ('Cast', ('a Character', 'Characters'))},
    4: {
        0: ('Players', ('a Player', 'Players')),
        1: ('Pirate Brawler', ('a Pirate Brawler', 'Pirate Brawlers')),
        2: ('Pirate Gunner', ('a Pirate Gunner', 'Pirate Gunners'))},
    5: {
        0: ('Trading Co Mercenaries', ('a Trading Co Mercenary', 'Trading Co Mercenaries')),
        1: ('Trading Co Assassins', ('a Trading Co Assassin', 'Trading Co Assassins')),
        2: ('Trading Co Officials', ('a Trading Co Official', 'Trading Co Officials'))}}
BossNames = {
    0: {
        0: {
            0: {
                0: 'Will Burybones',
                1: 'Foul Crenshaw',
                2: 'Evan the Digger',
                3: 'Thad Ill-Fortune'},
            1: {
                0: 'Simon Butcher'},
            2: {
                0: 'Thaddeus Woodworm'},
            3: {
                0: 'Bonebreaker'},
            4: {
                0: 'Gideon Grog'},
            5: {
                0: 'Whit Widowmaker'},
            6: {
                0: 'Blackheart'},
            7: {
                0: 'Francis Faust'},
            8: {
                0: 'Jeremy Coldhand'},
            9: {
                0: 'Stench'}}},
    1: {
        0: {
            1: 'Swordsman'},
        1: {
            0: {
                0: 'Geoffrey Pain'},
            1: {
                0: 'Hugh Brandish'},
            2: {
                0: 'Nathaniel Grimm'},
            3: {
                0: 'Sid Shiver'},
            4: {
                0: 'Ian Ramjaw'}}},
    2: {
        0: {
            0: {
                0: 'Sand Stalker'},
            1: {
                0: 'Man Ripper'},
            2: {
                0: 'Claw Chief'},
            6: {
                0: 'Bowbreaker'},
            7: {
                0: 'Snap Dragon'},
            8: {
                0: 'Rip Tail'},
            9: {
                0: 'Silent Stinger'},
            10: {
                0: 'Bonecracker'},
            11: {
                0: 'Trapjaw'},
            12: {
                0: 'Swamp Terror'}},
        2: {
            1: {
                0: 'Frightfang'},
            2: {
                0: 'Bloodleach'},
            3: {
                0: 'Firesting'},
            4: {
                0: 'Devilwing'}}},
    5: {
        0: {
            0: {
                0: 'Carlos Cudgel'},
            1: {
                0: 'Zachariah Sharp'},
            2: {
                0: 'Henry Flint'},
            3: {
                0: 'Phineas Fowl'},
            4: {
                0: 'Edward Lohand'}}}}
BossNPCNames = {
    'dynamicBoss_1': 'Blood Blade',
    '1154059362.19Shochet': 'Crabby',
    '1154059366.69Shochet': 'Spike',
    '1169616489.03Shochet': 'Woody',
    '1218238592.59mtucker': 'Test Skeleton Boss',
    '1218760328.71mtucker': 'Venom Lash',
    '1219277508.79mtucker': 'Dreadtooth',
    '1219352693.09mtucker': 'Neban the Silent',
    '1219339266.79mtucker': 'Samuel',
    '1219367627.94mtucker': 'Remington the Vicious',
    '1219428571.98mtucker': 'General Bloodless',
    '1220906480.53mtucker': 'General Hex',
    '1219434293.16mtucker': 'General Sandspine',
    '1219424341.05mtucker': 'General Darkhart',
    '1219426331.38mtucker': 'Bonerattler',
    '1219425030.24mtucker': 'Undead Timothy Dartan'}
AvatarNames = {
    0: {
        0: {
            0: ('Undead Gravedigger', ('an Undead Gravedigger', 'Undead Gravediggers')),
            1: ('Undead Bandit', ('an Undead Bandit', 'Undead Bandits')),
            2: ('Undead Pirate', ('an Undead Pirate', 'Undead Pirates')),
            3: ('Undead Witchdoctor', ('an Undead Witchdoctor', 'Undead Witchdoctors')),
            4: ('Undead Brigand', ('an Undead Brigand', 'Undead Brigands')),
            5: ('Undead Grenadier', ('an Undead Grenadier', 'Undead Grenadiers')),
            6: ('Undead Gypsy', ('an Undead Gypsy', 'Undead Gypsies')),
            7: ('Undead Raider', ('an Undead Raider', 'Undead Raiders')),
            8: ('Undead Captain', ('an Undead Captain', 'Undead Captains')),
            9: ('Mossman', ('a Mossman', 'Mossmen'))},
        1: {
            0: ('Whiff', ('a Whiff', 'Whiffs')),
            1: ('Reek', ('a Reek', 'Reeks')),
            2: ('Billow', ('a Billow', 'Billows')),
            3: ('Stench', ('a Stench', 'Stenches')),
            4: ('Shade', ('a Shade', 'Shades')),
            5: ('Specter', ('a Specter', 'Specters')),
            6: ('Phantom', ('a Phantom', 'Phantoms')),
            7: ('Wraith', ('a Wraith', 'Wraiths')),
            8: ('Captain Zephyr Windshadow', ('Captain Zephyr Windshadow', 'Captain Zephyr Windshadow')),
            9: ('Squall', ('a Squall', 'Squalls'))},
        2: {
            0: ('Glint', ('a Glint', 'Glints')),
            1: ('Flicker', ('a Flicker', 'Flickers')),
            2: ('Smolder', ('a Smolder', 'Smolders')),
            3: ('Spark', ('a Spark', 'Sparks')),
            4: ('Imp', ('an Imp', 'Imps')),
            5: ('Brand', ('a Brand', 'Brands')),
            6: ('Lumen', ('a Lumen', 'Lumens')),
            7: ('Fiend', ('a Fiend', 'Fiends')),
            8: ('Captain Cinderbones', ('Captain Cinderbones', 'Captain Cinderbones')),
            9: ('Torch', ('a Torch', 'Torches'))},
        3: {
            0: ('Dregs', ('a Dregs', 'Dregs')),
            1: ('Flotsam', ('a Flotsam', 'Flotsams')),
            2: ('Spineskull', ('a Spineskull', 'Spineskull')),
            3: ('Kelpbrain', ('a Kelpbrain', 'Kelpbrains')),
            4: ('Brinescum', ('a Brinescum', 'Brinescums')),
            5: ('Seabeard', ('a Seabeard', 'Seabeards')),
            6: ('Molusk', ('a Molusk', 'Molusks')),
            7: ('Urchinfist', ('an Urchinfist', 'Urchinfists')),
            8: ('Thrall Captain', ('Thrall Captain', 'Thrall Captains')),
            9: ('Spout', ('a Spout', 'Spouts'))},
        4: {},
        5: {
            0: ('Jolly Roger', ('a Jolly Roger', 'Jolly Rogers'))},
        6: {
            0: ('French Undead Quarter Master', ('a French Undead Quarter Master', 'French Undead Quarter Masters'), 'Fr.Undead Qtr.Master'),
            1: ('French Undead Maitre', ('a French Undead Maitre', 'French Undead Maitres'), 'Fr.Undead Maitres'),
            2: ('French Undead Lieutenant', ('a French Undead Lieutenant', 'French Undead Lieutenants'), 'Fr.Undead Lieutenant'),
            3: ('French Undead Capitaine', ('a French Undead Captaine', 'French Undead Captaines'), 'Fr.Undead Capitaine')},
        7: {
            0: ('Spanish Undead Conquistador', ('a Spanish Undead Conquistador', 'Spanish Undead Conquistadors'), 'Sp.Undead Conquistador'),
            1: ('Spanish Undead Bandido', ('a Spanish Undead Bandido', 'Spanish Undead Bandidos'), 'Sp.Undead Bandido'),
            2: ('Spanish Undead Pirata', ('a Spanish Undead Pirata', 'Spanish Undead Piratas'), 'Sp.Undead Pirata'),
            3: ('Spanish Undead Capitan', ('a Spanish Undead Capitan', 'Spanish Undead Capitans'), 'Sp.Undead Capitan')}},
    1: {
        0: {
            0: ('Axeman', ('an Axeman', 'Axemen')),
            1: ('Swordsman', ('a Swordsman', 'Swordsmen')),
            2: ('Royal Guard', ('a Royal Guard', 'Royal Guards')),
            3: ('Master Swordsman', ('a Master Swordsman', 'Master Swordsmen')),
            4: ('Weapons Master', ('a Weapons Master', 'Weapons Masters'))},
        1: {
            0: ('Cadet', ('a Cadet', 'Cadets')),
            1: ('Guard', ('a Guard', 'Guards')),
            2: ('Sergeant', ('a Sergeant', 'Sergeants')),
            3: ('Veteran', ('a Veteran', 'Veterans')),
            4: ('Officer', ('an Officer', 'Officers'))},
        2: {
            0: ('First Mate', ('a First Mate', 'First Mates')),
            1: ('Captain', ('a Captain', 'Captains')),
            2: ('Lieutenant', ('a Lieutenant', 'Lieutenants')),
            3: ('Admiral', ('an Admiral', 'Admirals')),
            4: ('Commodore', ('a Commodore', 'Commodores'))}},
    2: {
        0: {
            0: ('Sand Crab', ('a Sand Crab', 'Sand Crabs')),
            1: ('Rock Crab', ('a Rock Crab', 'Rock Crabs')),
            2: ('Giant Crab', ('a Giant Crab', 'Giant Crabs')),
            3: ('Chicken', ('a Chicken', 'Chickens')),
            4: ('Rooster', ('a Rooster', 'Roosters')),
            5: ('Pig', ('a Pig', 'Pigs')),
            6: ('Stump', ('a Stump', 'Stumps')),
            7: ('Fly Trap', ('a Fly Trap', 'Fly Traps')),
            8: ('Giant Scorpion', ('a Giant Scorpion', 'Giant Scorpions')),
            9: ('Dread Scorpion', ('a Dread Scorpion', 'Dread Scorpions')),
            10: ('Swamp Alligator', ('a Swamp Alligator', 'Swamp Alligators')),
            11: ('Big Alligator', ('a Big Alligator', 'Big Alligators')),
            12: ('Huge Alligator', ('a Huge Alligator', 'Huge Alligators')),
            13: ('Dog', ('a Dog', 'Dogs')),
            14: ('Seagull', ('a Seagull', 'Seagulls')),
            15: ('Monkey', ('a Monkey', 'Monkies'))},
        1: {
            0: ('Fish', ('a Fish', 'Fish'))},
        2: {
            0: ('Seagull', ('a Seagull', 'Seagulls')),
            1: ('Cave Bat', ('a Cave Bat', 'Cave Bats')),
            2: ('Vampire Bat', ('a Vampire Bat', 'Vampire Bats')),
            3: ('Dire Wasp', ('a Dire Wasp', 'Dire Wasps')),
            4: ('Terror Wasp', ('a Terror Wasp', 'Terror Wasps'))},
        3: {
            0: ('The Kraken', ('a Kraken', 'Krakens')),
            1: ('Head', ('a head', 'heads')),
            2: ('Tentacle', ('a tentacle', 'tentacles')),
            3: ('Back Tentacle', ('a tentacle', 'tentacles')),
            4: ('Wrapper Tentacle', ('a tentacle', 'tentacles')),
            5: ('Sea Serpent', ('a sea serpent', 'sea serpents'))},
        4: {
            0: ('Chicken', ('a Chicken', 'Chickens')),
            1: ('Rooster', ('a Rooster', 'Roosters')),
            2: ('Pig', ('a Pig', 'Pigs')),
            3: ('Dog', ('a Dog', 'Dogs')),
            4: ('Seagull', ('a Seagull', 'Seagulls'))}},
    3: {
        0: {
            0: ('Peasant', ('a Peasant', 'Peasants'))},
        1: {
            0: ('Gypsy', ('a Gypsy', 'Gypsy')),
            1: ('Blacksmith', ('a Blacksmith', 'Blacksmith')),
            2: ('Shipwright', ('a Shipwright', 'Shipwright')),
            3: ('Cannoneer', ('a Cannoneer', 'Cannoneer')),
            4: ('Merchant', ('a Merchant', 'Merchant')),
            5: ('Bartender', ('a Bartender', 'Bartender')),
            6: ('Gunsmith', ('a Gunsmith', 'Gunsmith')),
            7: ('Grenadier', ('a Grenadier', 'Grenadier')),
            8: ('Medicine Man', ('a Medicine Man', 'Medicine Man')),
            9: ('Tailor', ('a Tailor', 'Tailor')),
            10: ('Tattoo', ('a Tattooist', 'Tattooist')),
            11: ('Jeweler', ('a Jeweler', 'Jeweler')),
            12: ('Barber', ('a Barber', 'Barber')),
            13: ('Musician', ('a Musician', 'Musician')),
            14: ('Trainer', ('a Trainer', 'Trainer')),
            15: ('PvP Master', ('a PvP Master', 'PvP Master'))},
        2: {
            0: ('Cast', ('a Character', 'Characters'))}},
    4: {
        0: {
            0: ('You', ('you', 'you')),
            1: ('Another Player', ('another player', 'other players'))},
        1: {
            0: ('Landlubber', ('a Landlubber', 'Landlubbers')),
            1: ('Scallywag', ('a Scallywag', 'Scallywags')),
            2: ('Buccaneer', ('a Buccaneer', 'Buccaneers')),
            3: ('Swashbuckler', ('a Swashbuckler', 'Swashbucklers')),
            4: ('Warmonger', ('a Warmonger', 'Warmongers'))},
        2: {
            0: ('Cadet', ('a Gypsy', 'Gypsy')),
            1: ('Blacksmith', ('a Blacksmith', 'Blacksmith')),
            2: ('Shipwright', ('a Shipwright', 'Shipwright')),
            3: ('Merchant', ('a Merchant', 'Merchant')),
            4: ('Bartender', ('a Bartender', 'Bartender'))}},
    5: {
        0: {
            0: ('Thug', ('a Thug', 'Thugs')),
            1: ('Grunt', ('a Grunt', 'Grunts')),
            2: ('Hired-gun', ('a Hired-Gun', 'Hired-Guns')),
            3: ('Mercenary', ('a Mercenary', 'Mercenaries')),
            4: ('Assassin', ('an Assassin', 'Assassins'))},
        1: {
            0: ('Cadet', ('a Cadet', 'Cadets')),
            1: ('Musketeer', ('a Musketeer', 'Musketeers')),
            2: ('Cannoneer', ('a Cannoneer', 'Cannoneers')),
            3: ('Grenadier', ('a Grenadier', 'Grenadiers')),
            4: ('Master Gunner', ('a Master Gunner', 'Master Gunners'))},
        2: {
            0: ('First Mate', ('a First Mate', 'First Mates')),
            1: ('Captain', ('a Captain', 'Captains')),
            2: ('Lieutenant', ('a Lieutenant', 'Lieutenants')),
            3: ('Admiral', ('an Admiral', 'Admirals')),
            4: ('Commodore', ('a Commodore', 'Commodores'))}}}
PracticeDummy = 'Practice Dummy'
LandCrabStrings = ('land crab', ('a land crab', 'land crabs'))
Boss = 'Boss'
TownfolkMenuTitle = 'Townfolk'
CommonerMenuTitle = 'Commoner'
CastMenuTitle = 'Character'
PeasantMenuTitle = 'Peasant'
StoreOwnerMenuTitle = 'General Store'
GypsyMenuTitle = 'Gypsy Mystic'
BlacksmithMenuTitle = 'Blacksmith'
GunsmithMenuTitle = 'Gunsmith'
GrenadierMenuTitle = 'Grenadier'
ShipwrightMenuTitle = 'Shipwright'
MerchantMenuTitle = 'Merchant Trader'
BartenderMenuTitle = 'Bartender'
CannoneerMenuTitle = 'Cannoneer'
MedicineManMenuTitle = 'Medicine Man'
TrainerMenuTitle = 'Trainer'
GoldRewardDesc = '%s gold pieces'
MaxHpRewardDesc = '%s point HP boost'
MaxMojoRewardDesc = '%s point Voodoo boost'
LuckRewardDesc = '%s point luck boost'
SwiftnessRewardDesc = '%s point swiftness boost'
TreasureMapDesc = 'a treasure map'
ShipRewardDesc = 'a ship'
PistolRewardDesc = 'a pistol'
DollRewardDesc = 'a voodoo doll'
DaggerRewardDesc = 'a dagger'
CutlassRewardDesc = 'a cutlass'
GrenadeRewardDesc = 'a grenade'
StaffRewardDesc = 'a voodoo staff'
TeleportTotemRewardDesc = 'a teleportation totem'
CubaTeleportRewardDesc = 'teleport access to Cuba'
PortRoyalTeleportRewardDesc = 'teleport access to Port Royal'
PadresDelFuegoTeleportRewardDesc = 'teleport access to Padres Del Fuego'
KingsHeadTeleportRewardDesc = 'teleport access to Kingshead'
ReputationRewardDesc = '%s point Notoriety increase'
SpecialQuestRewardDesc = 'a special quest unlock'
PlayingCardRewardDesc = '%s playing card'
PlayingCardRewardDescPlural = '%s playing cards'
Chapter3RewardDesc = 'a special naval ability'
JewelryQuestRewardDesc = 'a special piece of jewelry'
TattooQuestRewardDesc = 'a special tattoo'
ClothingQuestRewardDesc = 'a special piece of clothing'
Temp2xRepQuestRewardDesc = 'Temporary 2x Reputation Points'
QuestDefaultDialogBefore = ('Good luck to ye!',)
QuestDefaultDialogDuring = ("How's that task coming?", 'Have ye finished that task?')
QuestDefaultDialogAfter = ('Great job!', 'Excellent work!')
QuestDefaultDialogBrushoff = ('Got nothing for ye', 'Try someone else, mate')
VisitTaskDefaultDialogAfter = ('Ahoy there!', 'Hello there!')
BribeTaskDefaultDialogAfter = ('Pleasure doing business with ye!', 'Come back any time.')
FishSelectBait = 'Select bait to fish'
FishWaitForBite = 'Wait for fish to bite'
ReelGuiTension = 'Tension'
FishCaughtInfo = "You caught 'er!"
FishEscapedInfo = 'The fish escaped!'
LineSnappedInfo = 'Your line snapped!'
FishTensionWarning = 'Careful!!'
FishDistanceWarning = "She's gonna escape!"
FishEncouragement = "You almost got 'er"
FishPanelTitle = 'You Caught'
FishGenusNames = {
    0: 'Angelfish',
    2: 'Barracuda',
    4: 'Blenny',
    6: 'Boxfish',
    8: 'Cardinalfish',
    10: 'Damselfish',
    12: 'Eel',
    14: 'Flounder',
    16: 'Grouper',
    18: 'Grunt',
    20: 'Hamlet',
    22: 'Jack',
    24: 'Parrotfish',
    26: 'Porgy',
    28: 'Puffer',
    30: 'Razorfish',
    32: 'Seabass',
    34: 'Snapper',
    36: 'Squirrelfish',
    38: 'Triggerfish',
    40: 'Other',
    100: [
        'Seaweed',
        'Old Boot',
        'Empty bottle']}
FishSpeciesNames = {
    0: ('Blue Angelfish', 'Cherubfish', 'French Angelfish', 'Queen Angelfish'),
    2: ('Great Barracuda', 'Southern Sennet'),
    4: ('Arrow Blenny', 'Diamond Blenny', 'Hairy Blenny', 'Seaweed Blenny', 'Spotcheek Bleeny'),
    6: ('Honeycomb Cowfish', 'Scrawled Cowfish', 'Smooth Trunkfish', 'Spotted Trunkfish'),
    8: ('Barred Cardinalfish', 'Dusky Cardinalfish', 'Flamefish', 'Twospot Cardinalfish', 'Whitestar Cardinalfish'),
    100: ('Seaweed', 'Old Boot', 'Empty Bottle')}

def getFishName(genus, species):
    speciesList = FishSpeciesNames.get(genus)
    if speciesList:
        if species < len(speciesList):
            name = speciesList[species]
            return name
        
    

from pirates.ship import ShipGlobals
DeployShip = 'Launch'
Locked = 'Locked'
BoardShip = 'Board'
SelectShip = 'Select'
ParlayShip = 'Parley'
ReturnShip = 'Put Away'
SetCrewShip = 'Crew Ship'
ChooseShipTitle = 'Choose A Ship'
CargoIconHelp = 'Click to show cargo'
CargoIconHelp2 = 'Amount of cargo the ship is carrying'
CrewIconHelp = 'Number of shipmates aboard ship'
KnownCrew = 'Recognized'
PermIconHelp = "Click to see captain's boarding permissions"
PermIconHelpOwn = 'Click to change boarding permissions'
BoardPermTitle = "Captain's\nBoarding Permissions"
YourShip = 'Your Ship'
CrewShip = 'Crew Ship'
GuildShip = 'Guild Ship'
FriendShip = 'Friend Ship'
PublicShip = 'Public Ship'
ShipAtSea = 'Click here to board this ship.'
ShipInBottle = 'Click here to start sailing on this ship.'
ShipSunk = 'You must repair this ship before sailing it again.'
OtherShipOut = 'One of your other ships is already at sea.'
ShipFull = 'This ship has no room left.'
Crate = 'Cargo Crate'
Chest = 'Treasure Chest'
SkChest = 'Royal Chest'
PirateShipPrefix = {
    'Sea': 0,
    'Renegade': 1,
    'Freebooter': 2,
    'Riptide': 3,
    'Skysail': 4,
    'Victory': 5,
    'Windjammer': 6,
    'Buccaneer': 7,
    'Storm': 8,
    'Storm-sail': 9,
    'Dark-sail': 10,
    'Dark-water': 11,
    'Fire-sail': 12,
    'Wave': 13,
    'Barnacle': 14,
    'Gunwale': 15,
    'Wind-racer': 16,
    'Star-chaser': 17,
    'Black': 18,
    'Headhunter': 19,
    'Scallywag': 20,
    'Bountyhunter': 21,
    'Savage': 22,
    'Scarlet': 23,
    'Fugitive': 24,
    'Crimson': 25,
    'Tide': 26,
    'Dark-wind': 27,
    'Fortune': 28,
    'Outlaw': 29,
    'Ravager': 30,
    'Vagrant': 31,
    'Moonraker': 32,
    'Red': 33,
    'Yellow': 34,
    'Silver': 35,
    'Blue': 36,
    'Green': 37,
    'White': 38,
    'Silver': 39,
    'Blade': 40,
    'Dark-blade': 41,
    'Dark': 42,
    'Shadow': 43,
    'Gun': 44,
    'Cutthroat': 45,
    'Bilge': 46}
PirateShipSuffix = {
    'Despoiler': 1,
    'Hunter': 2,
    'Cutter': 3,
    'Runner': 4,
    'Sultan': 8,
    'Defender': 9,
    'Reaver': 10,
    'Brig': 11,
    'Plunderer': 12,
    'Pillager': 13,
    'Raider': 16,
    'Brigand': 17,
    'Mercenary': 18,
    'Raptor': 19,
    'Rogue': 20,
    'Serpent': 24,
    'Seafarer': 26,
    'Forager': 27,
    'Voyager': 28,
    'Wolf': 29,
    'Shark': 30,
    'Raven': 31,
    'Stallion': 32,
    'Eagle': 33,
    'Executioner': 34,
    'Sabre': 35,
    'Dancer': 36,
    'General': 37,
    'Tiger': 38,
    'Lion': 39,
    'Hawk': 40,
    'King': 41,
    'Albatross': 42,
    'Cobra': 43,
    'Swan': 44,
    'Demon': 45,
    'Mongrel': 46,
    'Navigator': 47,
    'Fox': 48,
    'Explorer': 50,
    'Privateer': 51,
    'Bull': 52,
    'Warrior': 53,
    'Conqueror': 54,
    'Queen': 55,
    'Leopard': 56,
    'Destroyer': 57,
    'Eel': 59,
    'Dragon': 60,
    'Fish': 61,
    'Crest': 62,
    'Titan': 63,
    'Revenge': 64,
    'Trident': 66}

def getShipName(nameIndices):
    myName = ''
    for namePart in PirateShipPrefix:
        if PirateShipPrefix[namePart] == nameIndices[0]:
            myName += namePart
    
    myName += ' '
    for namePart in PirateShipSuffix:
        if PirateShipSuffix[namePart] == nameIndices[1]:
            myName += namePart
    
    return myName

defaultShipNames = {
    ItemId.INTERCEPTOR_L1: 'Pirate Sloop',
    ItemId.INTERCEPTOR_L2: 'Pirate Sloop',
    ItemId.INTERCEPTOR_L3: 'Pirate Sloop',
    ItemId.INTERCEPTOR_L4: 'Pirate Sloop',
    ItemId.MERCHANT_L1: 'Pirate Galleon',
    ItemId.MERCHANT_L2: 'Pirate Galleon',
    ItemId.MERCHANT_L3: 'Pirate Galleon',
    ItemId.MERCHANT_L4: 'Pirate Galleon',
    ItemId.WARSHIP_L1: 'Pirate Frigate',
    ItemId.WARSHIP_L2: 'Pirate Frigate',
    ItemId.WARSHIP_L3: 'Pirate Frigate',
    ItemId.WARSHIP_L4: 'Pirate Frigate'}

def getDefaultShipName(itemId):
    return defaultShipNames.get(itemId)

NavyShipTitle = 'HMS'
NavyShipPrefix = [
    'Bonny',
    'Royal',
    'Baron',
    'Duke',
    'Lord',
    'Queen',
    'Intrepid',
    'Invincible',
    'Fearless',
    'Reliant',
    'King',
    'Loyal',
    'Roaring',
    'Defiant',
    'Valiant',
    'Noble',
    'Impervious',
    'Golden',
    'Sturdy',
    'Worthy',
    'Fighting',
    'Flying',
    'Gallant',
    'Brave',
    'Resolute',
    'Iron',
    'Red',
    'Vigilant',
    'Vanguard',
    'White']
NavyShipSuffix = [
    'Bulwark',
    'Hunter',
    'Virtue',
    'Chastity',
    'Victory',
    'Dasher',
    'Barricader',
    'Bounty',
    'Valor',
    'Justice',
    'Leopard',
    'Tiger',
    'Ferret',
    'Beagle',
    'Avenger',
    'Boar',
    'Hawk',
    'Warrior',
    'Conqueror',
    'Rose',
    'AbbotProvidence',
    'Prudence',
    'Courage',
    'Fish',
    'Blockader',
    'Runner',
    'Titan',
    'Man-O-War',
    'Navigator',
    'Warlord',
    'Hero',
    'Soldier',
    'Champion',
    'Triumph',
    'Endeavor',
    'Goliath']
TradingShipTitle = 'EI'
TradingShipPrefix = [
    'Glorious',
    'Rich',
    'Magnificent',
    'Wondrous',
    'Joyful',
    'Shining',
    'Triumphant',
    'Golden',
    'Silver',
    'Platinum']
TradingShipSuffix = [
    'Plunder',
    'Horde',
    'Force',
    'Host',
    'Vanguard',
    'Treasure',
    'Endeavour',
    'Journey']
SkeletonShipTitle = 'SK'
SkeletonShipPrefix = [
    'Dire',
    'Phantom',
    'Dark',
    'Dread',
    'Storm',
    'Midnight',
    'Black',
    'Cursed',
    'Crimson',
    'Carrion',
    'Rancid',
    'Rotten',
    'Bloody',
    'Vile',
    'Venomous',
    'Corrupted']
SkeletonShipSuffix = [
    'Treachery',
    'Wraith',
    'Bane',
    'Pestilence',
    'Gloom',
    'Rebellion',
    'Massacre',
    'Doom',
    'Tyranny',
    'Grudger',
    'Reaper',
    'Revenge',
    'Anarchy',
    'Despair',
    'Raider',
    'Pain',
    'Terror',
    'Betrayal',
    'Mutiny',
    'Nemesis',
    'Villany',
    'Destroyer',
    'Slaughter',
    'Nightmare',
    'Vulture',
    'Predator',
    'Omen',
    'Crow',
    'Buzzard',
    'Vulture',
    'Malice',
    'Blade',
    'Death',
    'Harbinger',
    'Shadow',
    'Torturer']
TheBlackPearl = 'The Black Pearl'
TheDauntless = 'The Dauntless'
TheFlyingDutchman = 'The Flying Dutchman'
TheJollyRoger = "The Tyrant's Blade"
BlackjackActionNames = {
    0: 'No Action',
    1: 'Bid %s',
    2: 'Stay',
    3: 'Hit',
    4: 'Split',
    5: 'Double Down',
    6: 'Would you like a card?',
    7: '',
    8: 'Would you like to bid?'}
PlayingCardSuits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
PlayingCardRanks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
PlayingCardRanksPlural = ('Twos', 'Threes', 'Fours', 'Fives', 'Sixes', 'Sevens', 'Eights', 'Nines', 'Tens', 'Jacks', 'Queens', 'Kings', 'Aces')
PlayingCardHands = {
    'Nothing': '',
    'NoPair': 'High Card',
    'OnePair': 'Pair',
    'TwoPair': 'Two Pair',
    'Trips': 'Three of a Kind',
    'Straight': 'Straight',
    'Flush': 'Flush',
    'FlHouse': 'Full House',
    'Quads': 'Four of a Kind',
    'StFlush': 'Straight Flush'}

def getHandNameSimple(handCode, cards):
    return PlayingCardHands.get(handCode, 'Unknown')


def getHandNameFull(handCode, cards):
    
    def getRank(card):
        return card % 13

    cardNames = map(lambda card: PlayingCardRanks[getRank(card)], cards)
    cardNamesPlural = map(lambda card: PlayingCardRanksPlural[getRank(card)], cards)
    if handCode == 'Nothing':
        return ''
    elif handCode == 'NoPair':
        return '%s High' % cardNames[0]
    elif handCode == 'OnePair':
        return 'Pair of %s\n%s kicker' % (cardNamesPlural[0], cardNames[2])
    elif handCode == 'TwoPair':
        return 'Two Pair\n%s and %s' % (cardNamesPlural[0], cardNamesPlural[2])
    elif handCode == 'Trips':
        return 'Three of a Kind\n%s' % cardNamesPlural[0]
    elif handCode == 'Straight':
        return 'Straight to the %s' % cardNames[0]
    elif handCode == 'Flush':
        return 'Flush\n%s high' % cardNames[0]
    elif handCode == 'FlHouse':
        return 'Full House\n%s over %s' % (cardNamesPlural[0], cardNamesPlural[3])
    elif handCode == 'Quads':
        return 'Four of a Kind\n%s' % cardNamesPlural[0]
    elif handCode == 'StFlush':
        if getRank(cards[0]) == 12:
            return 'Royal Flush'
        else:
            return 'Straight Flush\n%s High' % cardNames[0]
    else:
        return 'Unknown'

PlayingCardTemplate = '%s of %s'
PlayingCardUnknown = 'Unknown'

def getPlayingCardName(suit, rank):
    suitName = PlayingCardSuits[suit]
    rankName = PlayingCardRanks[rank]
    return PlayingCardTemplate % (rankName, suitName)

NameGUI_CheckboxText = [
    'Show',
    'Hide']
NameGUI_RandomButtonText = 'Random Name'
NameGUI_TypeANameButtonText = 'Type a Name'
NameGUI_PickANameButtonText = 'Pick a Name'
NameGUI_SubmitButtonText = lSubmit
NameGUI_NextListItemText = lNext
NameGUI_PrevListItemText = 'Prev'
NameGUI_EmptyNameText = ' \n '
NameGUI_NoNameWarnings = [
    "Don't you want to have any name at all?",
    'You gotta have a first or a last name, mate!']
NameGUI_Guidelines = 'Your name will need to be approved.  \nMake sure it has: \n\n  - No foul language\n  - No personal information\n  - No brand names\n'
NameGUI_URLText = '\x01uline\x01Click here to see all naming guidelines\x02'
PirateNames_NickNamesGeneric = [
    'Crazy',
    'Bloody']
PirateNames_NickNamesFemale = [
    'Angel',
    'Blonde',
    'Bonny',
    'Lady',
    'Little',
    'Lovely',
    'Madam',
    'Miss',
    'Pretty',
    'Pirate']
PirateNames_NickNamesMale = [
    'Gentleman',
    'Fat',
    'Big',
    'Long',
    'Yellow',
    'Calico',
    'Red',
    'Scurvy',
    'Stinky',
    'Smelly',
    'Blind',
    'Dread',
    'Swabby',
    'Shabby',
    'Stumpy',
    'Spanish',
    'Dirty',
    'Drunk',
    'Drunken',
    'Cutthroat',
    'Cross-eyed',
    'Short-stack',
    'Stupid',
    'Lazy',
    'Iron',
    'Coal',
    'Old',
    'Ugly',
    'Gruesome']
PirateNames_FirstNamesMale = [
    'Bart',
    'Bartholomew',
    'Basil',
    'Ben',
    'Benjamin ',
    'Bill',
    'Billy',
    'Charles',
    'Chris',
    'Christopher',
    'David',
    'Davy',
    'Dog',
    'Edgar',
    'Edward',
    'Eric',
    'Enrique',
    'Francis',
    'Geoffrey',
    'George',
    'Gerard',
    'Hector',
    'Henry',
    'Isaiah',
    'Jack',
    'James',
    'Jamie',
    'Jason',
    'Jeffrey',
    'Jeremiah',
    'Jim',
    'John',
    'Johnny',
    'Joseph',
    'Lawrence',
    'Leon',
    'Marc',
    'Mark',
    'Matthew',
    'Nate',
    'Nathaniel',
    'Ned',
    'Peter',
    'Richard',
    'Robert',
    'Roger',
    'Sam',
    'Samuel',
    'Simon',
    'Solomon',
    'Sven',
    'Thomas',
    'Tobias',
    'Tom',
    'Will',
    'William']
PirateNames_FirstNamesFemale = [
    'Amelia',
    'Angel',
    'Anne',
    'Bess',
    'Beth',
    'Bettie',
    'Catherine',
    'Charlotte',
    'Constance',
    'Eliza',
    'Elizabeth',
    'Emily',
    'Esmerelda',
    'Gertrude',
    'Grace',
    'Jade',
    'Jane',
    'Janet',
    'Jeanne',
    'Joan',
    'Kat',
    'Kate',
    'Kelly',
    'Li',
    'Linda',
    'Lisa',
    'Liz',
    'Maggie',
    'Margaret',
    'Marge',
    'Maria',
    'Mary',
    'Meg',
    'Meghan',
    'Molly',
    'Nell',
    'Nelly',
    'Rachel',
    'Rosa',
    'Rose',
    'Samantha',
    'Sarah']
PirateNames_FirstNamesGeneric = []
PirateNames_LastNamePrefixesGeneric = [
    'Bad',
    'Barrel',
    'Bilge',
    'Blade',
    'Blast',
    'Blue',
    'Brawl',
    'Bridge',
    'Burn',
    'Cabin',
    'Calico',
    'Calle',
    'Cannon',
    'Chain',
    'Chip',
    'Coal',
    'Crest',
    'Dagger',
    'Damp',
    'Dark',
    'Deck',
    'Dock',
    'Dread',
    'Edge',
    'Fire',
    'Foul',
    'Gold',
    'Gun',
    'Helm',
    'Hex',
    'Hook',
    'Hull',
    'Iron',
    'Keel',
    'Lock',
    'Pillage',
    'Plank',
    'Plunder',
    'Pond',
    'Prow',
    'Pug',
    'Raid',
    'Red',
    'Rig',
    'Rope',
    'Sail',
    'Scurvy',
    'Sea',
    'Shark',
    'Ship',
    'Shore',
    'Singed',
    'Squid',
    'Stern',
    'Storm',
    'Sun',
    'Sword',
    'Tack',
    'Treasure',
    'True',
    'War',
    'Wave',
    'Yellow',
    'Wild',
    'Whale']
PirateNames_LastNamePrefixesCapped = [
    'Mac',
    'Mc',
    "O'"]
PirateNames_LastNamePrefixesMale = [
    'Grease']
PirateNames_LastNamePrefixesFemale = [
    'Heart']
PirateNames_LastNameSuffixesMale = [
    'beard',
    'davis',
    'dougal',
    'roberts',
    'wallace']
PirateNames_LastNameSuffixesFemale = [
    'bonnet',
    'bonney',
    'fellow',
    'hara']
PirateNames_LastNameSuffixesGeneric = [
    'batten',
    'bellows',
    'bain',
    'bane',
    'bones',
    'bowers',
    'breaker',
    'burn',
    'butler',
    'castle',
    'crash',
    'cutter',
    'eagle',
    'easton',
    'fitte',
    'fish',
    'flint',
    'foote',
    'fury',
    'ginty',
    'grin',
    'grim',
    'gull',
    'hawk',
    'hayes',
    'hazzard',
    'hogge',
    'hound',
    'kidd',
    'loather',
    'martin',
    'malley',
    'menace',
    'monger',
    'morgan',
    'morrigan',
    'morris',
    'monk',
    'paine',
    'parr',
    'pigge',
    'pratt',
    'rackham',
    'rage',
    'rat',
    'ratte',
    'scarlett',
    'shot',
    'shout',
    'silver',
    'skull',
    'slipper',
    'stack',
    'steel',
    'smythe',
    'spinner',
    'stealer',
    'swain',
    'swine',
    'timbers',
    'vane',
    'walker',
    'ward',
    'wash',
    'wrecker']
QuestScriptTutorialJack_1 = "Aren't you a sight, You look like I feel."
QuestScriptTutorialJack_2 = 'Here, use this to pull yourself together, mate.'
QuestScriptTutorialJack_3 = 'Ah, a bonnie lass.'
QuestScriptTutorialJack_4 = "You're a big fella aren't ya?"
QuestScriptTutorialJack_5 = 'Some of these should fit you.'
QuestScriptTutorialJack_6 = "Much better! So now, I'm Captain Jack Sparrow, if you please. Who might you be? Forgot your name as well?"
QuestScriptTutorialJack_10 = 'Well I need something to call you by.'
QuestScriptTutorialJack_11 = 'An honor to meet you...truly.'
QuestScriptTutorialJack_12 = 'Now, time for us to make our exit.'
QuestScriptTutorialJack_14 = 'Works every time!'
QuestScriptTutorialJack_15 = 'You look a bit unsteady, are you sure you can walk?'
QuestScriptTutorialJack_16 = 'You might want to go see Doggerel Dan over at the Black Dog Inn.'
QuestScriptTutorialJack_17 = "He'll fix you up right straight. Tell him Captain Jack sent you."
QuestScriptTutorialDan_a_1 = ''
QuestScriptTutorialDan_1 = 'Ahoy mate! Welcome to Rambleshack! Capn Jack sent ye, did he?'
QuestScriptTutorialDan_2 = 'A finer scallywag never did stumble the halls of this here Inn than Ole Jack!'
QuestScriptTutorialDan_3 = 'Did he mention he still owes me? For that Thing?'
QuestScriptTutorialDan_4 = "Well then, I suppose I've been holding this sea chest for you."
QuestScriptTutorialDan_5 = "Come on, open 'er up."
QuestScriptTutorialDan_5b = "You might want to let it breath a little...that scrap of biscuit there is still crawlin'."
QuestScriptTutorialDan_6 = 'Look straight, a pirate keeps all manner of precious things in his sea chest.'
QuestScriptTutorialDan_7 = 'But the most important of all is the pirate journal.'
QuestScriptTutorialDan_8 = 'Ye see, pirates is forgetful folk, so they need to keep a reckoning.'
QuestScriptTutorialDan_9 = "Now reckon this mate: you best be leavin' this hairy little wart of an island."
QuestScriptTutorialDan_9b = "Winds' a changin' and that means there's trouble about"
QuestScriptTutorialDan_10 = 'Get yourself down to the docks and find Captain Bo Beck.'
QuestScriptTutorialDan_10b = "I'll put that in the journal for ya."
QuestScriptTutorialDan_11 = 'Lost already? Better get down to the dock - '
QuestScriptTutorialDan_12 = "Bo Beck's stinkbucket of a raft will be shipping out for Bilgewater on the tide."
QuestScriptTutorialStumpy_1 = "Go ahead, practice shoot'n that wreck yonder."
QuestScriptTutorialStumpy_6 = "Avast! ye've winged her! Good shootin' matie."
QuestScriptTutorialStumpy_8 = "Look sharp! Wouldn't want them to catch us unawares."
QuestScriptTutorialJR_1 = 'What fools be pirating in my waters?'
QuestScriptTutorialJR_2 = "Mmm, I've not seen ye before... not much mojo to speak of - yet."
QuestScriptTutorialJR_3 = "I'll deal with ye later."
QuestScriptTutorialJR_4 = "Ahoy mates! Send their ship to Davy Jones' locker."
QuestScriptShipwrightWarningA_1 = 'Ahoy, landlubber! A word to the wise, matey...'
QuestScriptShipwrightWarningA_2 = "Ye shouldn't be without a Sword in these parts."
QuestScriptShipwrightWarningA_3 = "Go see me friend Will Turner at the Rowdy Rooster, he take good care o' ya!"
QuestScriptShipwrightIntro_1 = 'Ahoy, ye landlubber! This here be the Shipyard!'
QuestScriptShipwrightIntro_2 = 'Avast! Ye be a pirate and ye have no vessel!?'
QuestScriptShipwrightIntro_3 = "This dingy be all I can spare. She ain't much, but it'll keep ye afloatin!"
QuestScriptShipwrightIntro_4 = 'Come back here when yer ready to buy a real Ship!'
QuestScriptShipwrightIntro_5 = 'Yarrr, and bring a bit more %s too.' % MoneyName
QuestScriptCutlassTutorial_1 = 'I practice three hours a day, so in all likelihood I can help you brush up your skills with the blade...'
QuestScriptCutlassTutorial_2 = "There's no parley with Jolly Roger, so be careful."
QuestScriptCutlassTutorial_3 = 'Very well.  Draw your sword.'
QuestScriptCutlassTutorial_3_5 = "'T will be difficult to cut down a skeleton in your path, if you haven't yet drawn your sword..."
QuestScriptCutlassTutorial_3_6 = 'It seems you are bound by a spell of lethargy.'
QuestScriptCutlassTutorial_4 = "I didn't have time to fashion a proper spell, so this dummy will have to do..."
QuestScriptCutlassTutorial_5 = 'Not to worry, simply advance and strike the dummy'
QuestScriptCutlassTutorial_5_5 = "I assure you.  He won't feel a thing."
QuestScriptCutlassTutorial_6 = "Good effort, but you'll need to be accurate if you're to defeat an enemy"
QuestScriptCutlassTutorial_7 = 'Move close and face the dummy.'
QuestScriptCutlassTutorial_7_5 = 'The lesson is not over, you still have much to learn.'
QuestScriptCutlassTutorial_8 = "Very good.  Alright let's move on. A true swordsman knows that timing and finesse will accomplish more than just swinging the blade around."
QuestScriptCutlassTutorial_8_5 = "If you slow down, you'll inflict more damage by chaining attacks together."
QuestScriptCutlassTutorial_8_6 = 'Too late, try again.'
QuestScriptCutlassTutorial_8_7 = 'Slow down and try again.'
QuestScriptCutlassTutorial_9 = 'Nicely executed!'
QuestScriptCutlassTutorial_9_25 = "A true pirate is defined by his reputation.  The greater your reputation, the easier it will be to defeat your enemies.  Now, let's try another skill."
QuestScriptCutlassTutorial_9_5 = 'The greater your reputation, the easier it will be to best your enemies.'
QuestScriptCutlassTutorial_10 = "Please, try out the new skill I've taught you."
QuestScriptCutlassTutorial_11 = "You're swinging too fast.  Try to swing a second time, just as your first attack ends."
QuestScriptCutlassTutorial_12 = 'Better to practice your new move on the dummy before trying it on Jolly Roger himself... go ahead.'
QuestScriptCutlassTutorial_13 = 'Well done!'
QuestScriptBlacksmithIntro_1 = 'Who are you?'
QuestScriptBlacksmithIntro_2 = "A friend of Jack's, are you?"
QuestScriptBlacksmithIntro_3 = "No sword? That won't do in these parts."
QuestScriptBlacksmithIntro_4 = 'Here, take this Cutlass. Give it a try.'
QuestScriptBlacksmithIntro_5 = 'Unfamiliar with the blade?'
QuestScriptBlacksmithIntro_6 = "It's okay to cross swords with a friend on occasion."
QuestScriptBlacksmithIntro_7 = 'Come on, just so you get the feel of it.'
QuestScriptBlacksmithIntro_8 = 'Okay, that will do.'
QuestScriptBlacksmithIntro_9 = 'Certain circumstances require a bit more firepower.'
QuestScriptBlacksmithIntro_10 = 'Take this pistol to protect against the worst that Jolly Roger has to offer.'
QuestScriptBlacksmithIntro_11 = "But don't go shootin' that thing at human folk... us Pirates must maintain a bit o' decency."
QuestScriptBlacksmithIntro_12 = "It's the Pirate Code, mate."
QuestScriptBlacksmithIntro_13 = "The Code's all we have to separate us from the likes of Jolly Roger."
QuestScriptBlacksmithIntro_14 = 'Besides, blasting away at the Navy will land you in jail faster than a dog can lift his leg.'
QuestScriptBlacksmithIntro_15 = "As for all manner of beasties, both nautical and land-lubber'd... fire away mate!"
QuestScriptBlacksmithIntro_17 = 'Go now, practice your skills with your new weapons on some crabs. Visit me when done.'
QuestScriptBlacksmithIntro_18 = 'After that, Billy Plankbite will be expecting you. Look for him in the swamps.'
QuestScriptPistolTutorial_1 = 'Now, take aim at the cursed simian over there...prove your mettle with the hand cannon!'
QuestScriptPistolTutorial_2 = "Come on, he can't feel a thing."
QuestScriptPistolTutorial_3 = 'A fine shot!  The little wretch had it coming...'
QuestScriptShipIntro = "Okay mate, I'll give ye a ship... but ye'll need to rename her so as no one can trace her back to me."
QuestScriptShipFinal = "Take good care of her... you'll not get a deal like this again."
TiaShowVoodooDoll = 'I been watching you...\x07Greatness lies behind your eyes... still, you have much to learn.\x07I will show you the way of the dark arts...\x07... but you must prove your worth... if you are to succeed.\x07Do not question my methods, only do as I say.\x07We begin with a trifle... a trifle true enough, but in the right hands it can bring down an army...\x07Look upon \x01slant\x01The Doll\x02!\x07The learning of the doll be in the learning of its construction... each must make their own.\x07Now go! We have much work to do.'
QuestScriptGypsyIntro_1 = 'Greetings, stranger.'
QuestScriptGypsyIntro_2 = 'I am Madame Bernadette, a mystic and oracle of the Gypsy people.'
QuestScriptGypsyIntro_3 = 'Have you come to learn of the arcane art of Voodoo?'
QuestScriptTiaDalmaCh2Rung1_1 = 'The claws told me you held great promise.'
QuestScriptTiaDalmaCh2Rung1_2 = 'Help witty Jack when you can.  Seek me in if you want to learn more of the dark arts.'
QuestScriptGrahamMarsh_1b_1 = "Lookin' for some honest pirating, eh?"
QuestScriptGrahamMarsh_1b_2 = "Yellow Dan stole my bloody treasure...but he only got half! And now he's cursed!"
QuestScriptGrahamMarsh_1b_3 = "I buried mine in a proper chest -- find it and I'll share the prize."
QuestScriptGrahamMarsh_1b_4 = "Where?  In the cave by the beach.  Don't recollect precisely...dig around, you lazy scabs!"
QuestScriptGrahamMarsh_1a_1 = "Well done.  You'll make proper scalawags yet..."
QuestScriptGrahamMarsh_2b_1 = 'Find the other earring just like mine -- together they be the prize!'
QuestScriptGrahamMarsh_2b_2 = "A Navy contact told me Yellow Dan was captured by some of Jolly Roger's goons..."
QuestScriptGrahamMarsh_2b_3 = "So you'll have to sink Roger's ships until you find the other earring."
QuestScriptGrahamMarsh_2b_4 = 'When you have both, take them to Sophie on Volcano Island.'
QuestScriptGrahamMarsh_2b_5 = 'She knows what to do with them...and will reward you for your efforts.'
QuestScriptGrahamMarsh_2a_1 = "I was captured by the devils.  Can't stand the smell of 'em."
QuestScriptGrahamMarsh_2a_2 = "Made an appointment with Davy Jones just so my nose'd stop burnin'"
QuestScriptGrahamMarsh_2a_3 = "Didn't realize I was cursed me-self!"
QuestScriptGrahamMarsh_2a_4 = "So here I am back from the dead... and I'll be needin' my treasure back."
QuestScriptGrahamMarsh_3a_1 = 'Do you have the earrings?'
QuestScriptGrahamMarsh_3a_2 = "Voodoo earrings don't like being split up..."
QuestScriptGrahamMarsh_3a_3 = "That's how Yellow Dan found himself cursed."
QuestScriptGrahamMarsh_3a_4 = 'But Marsh knew I could undo it.'
QuestScriptGrahamMarsh_3a_5 = 'Thanks for your help.  This is for your troubles...'
CutSubtitle1_1_1__1 = "Aren't you a sight? Hmm, you look how I feel, mate.\nHere, pull yourself together."
CutSubtitle1_1_1__2 = ''
CutSubtitle1_1_1__3 = ''
CutSubtitle1_1_2__1 = 'An honor to meet you, truly!'
CutSubtitle1_1_2__2 = "And now it's time to make our sortie...\nas in exit... as in leave... as in... NOW!"
CutSubtitle1_1_2__3 = 'Works every time!'
CutSubtitle1_1_2__4 = "That's not thunder mate. If I were you, I'd fetch my personal effects\nand get out of the range of those cannons."
CutSubtitle1_1_2__5 = 'Doggerel Dan will help you out.'
CutSubtitle1_1_2__6 = "That is, if he's still on this scrap of an island."
CutSubtitle1_1_2__7 = "Tell 'em that Captain Jack Sparrow sent you!"
CutSubtitle1_1_5_a__1 = "Nah, nah, nah, nah, we are closed mate, out o' business!"
CutSubtitle1_1_5_a__2 = "Packin' up before those cannons get any closer\nand you'd do the same if you know what's good for ye."
CutSubtitle1_1_5_a__3 = "What's that? Captain Jack sent you?"
CutSubtitle1_1_5_a__4 = 'Did he mention that he still owes me... for that... thing?'
CutSubtitle1_1_5_a__5 = 'Ah, Doggerel!'
CutSubtitle1_1_5_a__6 = 'Let it go Dan, and hand over the chest so we can shove off!'
CutSubtitle1_1_5_a__7 = "Well then, I suppose that I've been holding this sea chest for you."
CutSubtitle1_1_5_b__1 = 'Come on open her up.'
CutSubtitle1_1_5_c__1 = 'Oohh, you might want to let her breathe a little.'
CutSubtitle1_1_5_c__2 = 'That scrap of biscuit there is still crawling.'
CutSubtitle1_1_5_c__3 = 'Look straight.\nA pirate keeps all manner of precious things in his sea chest.'
CutSubtitle1_1_5_c__4 = 'But the most important thing is the pirate journal.'
CutSubtitle1_1_5_c__5 = "See pirates is forgetful folk, so they need to keep a reckonin'."
CutSubtitle1_1_5_c__6 = "Now reckon this mate: Get yourself down to the dock\nand find Captain Bo Beck before it's too late."
CutSubtitle1_1_5_c__7 = "I'll put that in the journal for you!"
CutSubtitle1_1_5_c__8 = 'Oh and one more thing, when you see Jack Sparrow again,\ngive him this message...'
CutSubtitle1_1_5_c__9 = 'FROM THE BOTH OF US!!!'
CutSubtitle1_1_5_c__10 = 'Fair winds mate!'
CutSubtitle1_2_a__1 = 'You there, come aboard quickly!'
CutSubtitle1_2_a__2 = 'I was about to shove off without you.'
CutSubtitle1_2_a__3 = "Jolly Roger will be back in a hair's breadth or my name's not Bo Beck."
CutSubtitle1_2_b__1 = 'Risked my neck to fetch Captain Sparrow I did!'
CutSubtitle1_2_b__2 = 'But he most generously requested that\nI take you to Port Royal in his place!'
CutSubtitle1_2_b__3 = 'Now grab a cannon, and keep an eye peeled for trouble.'
CutSubtitle1_3_a__1 = "Hold your fire! It's Jolly Roger,\nand he's got us dead to rights!"
CutSubtitle1_3_a__2 = 'SPAAARROW!!!'
CutSubtitle1_3_a__3 = "Don't worry, I'll handle this."
CutSubtitle1_3_a__4 = "Where's that yellow coward Sparrow? Beck, we had a deal!"
CutSubtitle1_3_a__5 = "But Sparrow paid me double what you was payin'."
CutSubtitle1_3_a__6 = "A pretty piece of profit, too!\nSo, here's your gold back."
CutSubtitle1_3_a__7 = "'Course I was going to reimburse you... as it were."
CutSubtitle1_3_a__8 = 'ah, ha, ha, ha, ha! It looks like the price of loyalty just went up, eh?'
CutSubtitle1_3_a__9 = "What?  Can't take a joke?"
CutSubtitle1_3_a__10 = "Dead men tell no tales! So, I'm forced to let ye live."
CutSubtitle1_3_a__11 = "Just make sure Jack Sparrow knows I'm comin' for him."
CutSubtitle1_3_a__12 = "Said, I'll be lettin' you live\nbut the sharks may not be so charitable..."
CutSubtitle1_3_a__13 = 'What are you waiting for? Sink her!!!!! NOWWWW!!!!'
CutSubtitle2_1_a__1 = "On my word, do as I say or I'll run you through!"
CutSubtitle2_1_a__2 = "Hmmm, unarmed.  Wait, you're Jack's friend."
CutSubtitle2_1_a__3 = 'Please accept my apologies.'
CutSubtitle2_1_a__4 = "There's some gentleman from the\nEast India Trading Company looking for me."
CutSubtitle2_1_a__5 = "Can't be too cautious."
CutSubtitle2_1_a__6 = "Well, you aren't much use unarmed\nwith Jolly Roger's skeleton army on the move!"
CutSubtitle2_1_a__7 = "Here, the blade's a bit rusty... not well balanced,\nbut it should suffice for the present."
CutSubtitle2_1_a__8 = 'Not familiar with the blade?'
CutSubtitle2_1_a__9 = 'That practice dummy will do.'
CutSubtitle2_1_b__1 = "Keep the sword, you'll need it!"
CutSubtitle2_1_b__2 = "But you'll need more than just a cutlass\nif you're to challenge the likes of Jolly Roger."
CutSubtitle2_1_b__3 = 'Tia Dalma has something for you as well.'
CutSubtitle2_1_b__4 = "Go now, it's me they're after.\nFind Tia Dalma in the jungle."
CutSubtitle2_1_b__5 = "You'll know her by the lantern she carries."
CutSubtitle2_1_b__6 = 'Good luck!'
CutSubtitle2_2__1 = "The claws lie true. There's a touch of destiny in you."
CutSubtitle2_2__2 = 'But know that the skeleton you destroyed\nwas nothing but a drop in the ocean!'
CutSubtitle2_2__3 = "Jolly Roger's servants are many and most be far more dangerous!"
CutSubtitle2_2__4 = 'Look now, from the darkness... comes the light.\nOn one horizon...'
CutSubtitle2_2__5 = "Lord Beckett's deadly assassins, the Black Guard!"
CutSubtitle2_2__6 = "On the other, Jolly Roger's skeleton army."
CutSubtitle2_2__7 = 'Their powers grow! Lord Beckett and Roger!\nNo more, this can be!'
CutSubtitle2_2__8 = 'You must play your part, just as witty Jack will play his part!'
CutSubtitle2_2__9 = 'Now take this, something for you.  Help to find the way, yes.'
CutSubtitle2_2__10 = 'I watch you, when destiny whispers, I will reveal more of the dark arts.'
CutSubtitle2_2__11 = 'But first you must help witty Jack recover his dear Black Pearl.'
CutSubtitle2_2__12 = 'For without the Pearl we all be lost. Go now, hurry!'
CutSubtitle2_3__1 = "Oh, so you're Jack Sparrow's newest prot\xc3\xa9g\xc3\xa9, hmmm?"
CutSubtitle2_3__2 = "Well, I'm afraid dear Jack is in more trouble than he realizes."
CutSubtitle2_3__3 = "Lord Beckett has recruited an army of assassins,\nand there's no parley with Jolly Roger."
CutSubtitle2_3__4 = 'Jack needs our help if he is to take back the Pearl.\nThe Navy has it heavily guarded.'
CutSubtitle2_3__5 = "What's this?  Release orders for the Pearl?"
CutSubtitle2_3__6 = 'I can see why Jack has taken a liking to you!'
CutSubtitle2_3__7 = "But these will do you no good without my father's seal!"
CutSubtitle2_3__8 = "Here, now if the Navy catches you with these orders, there'll be no trial."
CutSubtitle2_3__9 = 'You must leave Port Royal immediately.'
CutSubtitle2_3__10 = "You'll be much safer if you make for Tortuga."
CutSubtitle2_3__11 = "Find Jack, he'll know what to do."
CutSubtitle2_3__12 = "I'd go with you myself, but I am awaiting my father's return,\nand he's long overdue."
CutSubtitle2_3__13 = "I'll arrange a boat for you.  Good luck!"
CutSubtitle2_4_a__1 = "This here's a dark place."
CutSubtitle2_4_a__2 = "You'll need more than that cutlass\nif you're to get out of here with your skin."
CutSubtitle2_4_a__3 = 'Here, take this.\nNow, take aim at the cursed simian over there.'
CutSubtitle2_4_a__4 = 'Prove your mettle with the hand cannon.'
CutSubtitle2_4_b__1 = "Now before ye go blastin' every feckless ingrate in sight,\na word of warning about the code."
CutSubtitle2_4_b__2 = 'The code covers more than just parley.\nIt defines the guidelines of engagement for a pirate.'
CutSubtitle2_4_b__3 = 'I was getting to that, ye mongrel.  This be the part to remember.'
CutSubtitle2_4_b__4 = "There'll be no use of unnecessary force, no shooting other pirates,\nor even Navy swine for that matter."
CutSubtitle2_4_b__5 = "Cheat 'em, steal from 'em, plunder their ships, yes.  But no guns!"
CutSubtitle2_4_b__6 = 'That is, unless you be facing a cursed pirate.'
CutSubtitle2_4_b__7 = "You see, the code don't apply to dead pirates."
CutSubtitle2_4_b__8 = 'So if you want to have a go against your mates,\nbe sure you pick up one of these!'
CutSubtitle2_4_b__9 = 'Now you can blast away at each other all you like!'
CutSubtitle2_4_b__10 = "See, it doesn't hurt a bit!"
CutSubtitle2_5__1 = 'And the buttons popped clear off...'
CutSubtitle2_5__2 = 'and this being Singapore, by custom I had no choice but to-'
CutSubtitle2_5__3 = "You don't happen to have a lovely sister by the name of Ethel, do you?"
CutSubtitle2_5__4 = 'No?  Good, right then!'
CutSubtitle2_5__5 = 'Welcome to Tortuga!  Captain Jack Sparrow at your service.'
CutSubtitle2_5__6 = "And this gentleman who needs no introduction, is...\nWhat's your name again, mate?"
CutSubtitle2_5__7 = 'John! Oh well, uh, James, actually.'
CutSubtitle2_5__8 = 'Right! We were discussing the important matter of my next drink.'
CutSubtitle2_5__9 = 'Is... still there? Aye.'
CutSubtitle2_5__10 = "Now I remember!  You're that scrap of flotsam from the jail."
CutSubtitle2_5__11 = 'Come to square up with me for that free trip to Port Royal, eh?'
CutSubtitle2_5__12 = "We're going after the Black Pearl, mate.  Savvy?"
CutSubtitle2_5__13 = 'So go find Joshamee Gibbs and tell him I sent you!'
CutSubtitle2_5__14 = 'Leave a nice tip, mate! Jeremy here pours a spirited spirit.'
CutSubtitle3_1__1 = 'Halt! Who goes there?'
CutSubtitle3_1__2 = "What's this?  Some sort of letter?"
CutSubtitle3_1__3 = 'Looks official.  Let me see that.'
CutSubtitle3_1__4 = "Can't be too careful.  There's pirates about."
CutSubtitle3_1__5 = "Yeah, we're performing a very important duty."
CutSubtitle3_1__6 = 'Guarding the Black Pearl.'
CutSubtitle3_1__7 = "Not just us, really.  In the harbor there that's the Goliath."
CutSubtitle3_1__8 = 'No one gets in or out of this harbor without facing her eighteen guns.'
CutSubtitle3_1__9 = 'A nigh impossible proposition!'
CutSubtitle3_1__10 = "And, we're supposed to keep an eye out for Jack Sparrow."
CutSubtitle3_1__11 = "He won't make fools of us this time."
CutSubtitle3_1__12 = "Make a fool of you, perhaps.\nBut I don't recall a time where I was ever the fool."
CutSubtitle3_1__13 = 'Me a fool?  I was only being generous by including me self in the equation.'
CutSubtitle3_1__14 = "Oh, so you're the generous one now? I was the generous enough\n to not report you for sleeping on duty yesterday evening!"
CutSubtitle3_1__15 = 'I was just resting me eyelids.\nBesides, I was tired from covering your shift Tuesday!'
CutSubtitle3_1__16 = 'You call that covering? When I showed up you were nowhere in sight!'
CutSubtitle3_1__17 = "A man's got to take care of his business now and again..."
CutSubtitle3_2__1 = '...and proceeded to eat his own finger, to which I replied,'
CutSubtitle3_2__2 = "That's not right even if you did know where that finger has been!"
CutSubtitle3_2__3 = 'Ah yes, Master Gibbs tells me you have taken her.\nSo how is she, as beautiful as ever?'
CutSubtitle3_2__4 = "A word of warning mate, once you have had a taste, you'll only want more!"
CutSubtitle3_2__5 = 'Lest you start to covet the Black Pearl for your own, know this.'
CutSubtitle3_2__6 = 'The wind is her true master....'
CutSubtitle3_2__7 = 'Aye.  It is.'
CutSubtitle3_2__8 = 'To control the wind... is to control her destiny!'
CutSubtitle3_2__9 = 'Aye.  It is.'
CutSubtitle3_2__10 = 'And there is a way... to control the wind.'
CutSubtitle3_2__11 = 'Aye.  There is?'
CutSubtitle3_2__12 = "Don't take my word for it.\nIt's written in stone on a thing called the Headstone."
CutSubtitle3_2__13 = "The Headstone! We're not going back there again, are we?"
CutSubtitle3_2__14 = "You've done well so far.  And this is for your efforts..."
CutSubtitle3_2__15 = 'But, help me find the Headstone and I promise it will be worth your while!'
CutSubtitle3_2__16 = 'The catch is no map will lead you to it.'
CutSubtitle3_2__17 = 'But I happen to know where it is buried... Padres!'
CutSubtitle3_2__18 = 'Padres, del Fuego!  You know, the volcano.\nLava natives chanting. Headstone thrown in it.'
CutSubtitle3_2__19 = 'Rough place, Padres! Very shaky.'
CutSubtitle3_2__20 = 'Go there at once.'
CutSubtitle3_2__21 = "We wouldn't want to lose this prize to our dear friends in the Royal Navy."
CutSubtitle3_2__22 = 'I am told they are on the hunt already.'
CutSubtitle3_2__23 = 'When you get there, find Valentina.  She might know where to start looking.'
CutSubtitle3_2__24 = 'And I will meet up with you as soon as Master Gibbs here can ready the crew!'
CutSubtitle6_1__1 = 'I been watching you...'
CutSubtitle6_1__2 = '... still, you have much to learn.'
CutSubtitle6_1__3 = 'I will show you the way of the dark arts...'
CutSubtitle6_1__4 = 'We begin with a trifle...'
CutSubtitle6_1__5 = 'Look upon it!'
CutSubtitle6_1__6 = 'The learning of the doll be in the learning of its construction...'
CutSubtitle6_1__7 = 'each must make their own.'
CutSubtitle6_1__8 = 'We have much work to do.'
ProgressBlockPopupDialog = {
    'c3visitJoshamee': 'Congratulations! You have reached the start of Chapter 3. Only players with full access may continue beyond this point. To become a full access member visit www.piratesonline.com and subscribe.',
    'c3r2.6visitCarver': 'Congratulations! You have recruited 5 crew members for the Black Pearl and have given Gibbs a clue as to where she is being held by the Navy. Only players with full access may continue beyond this point. To become a full access member visit www.piratesonline.com and subscribe.',
    'c4.1visitValentina': 'Chapter 3 complete! Coming soon: Chapter 4: Search for the Headstone.'}
TownfolkGreetings = [
    'Hello.',
    'Good day.']
TownfolkGoodbyes = [
    'Goodbye.',
    'Farewell.']
TownfolkEncourage = [
    'Keep at it, mate!',
    "Come back when you're finished"]
TownfolkBrushoff = [
    "Sorry, I've got nothing for you."]
PirateGreetings = [
    'Ahoy!',
    'Ahoy there!',
    'Avast me hearties!',
    'Avast!',
    'Avast, ye landlubber!']
PirateGoodbyes = [
    'Arrr!',
    'Arrr matey!',
    "Back to plunderin'!",
    'Best be watchin yer back matey!']
PirateEncourage = [
    'Keep at it, mate!',
    "Ye're not done yet"]
PirateBrushoff = [
    'Bother someone else, mate',
    'Nothing here for ye']
FormalGreetings = [
    'Welcome',
    'Greetings',
    'We meet again.',
    'How may I help you?']
FormalGoodbyes = [
    'Farewell',
    'Goodbye',
    'Come back again sometime.']
GypsyGreetings = [
    'Good-day',
    'Greetings']
GypsyGoodbyes = [
    'Farewell',
    'Goodbye']
GypsyEncourage = [
    'Keep trying',
    'You must finish before you return']
GypsyBrushoff = [
    'I have nothing for you',
    'Try someone else']
ShipPVPLordBrushoff = [
    "There's no battle yet! Come back when there's a use for you.",
    "Can't you see that I'm busy? I'm planning my attack and I have no work for you yet.",
    "There's no way we'll lose! A fierce battle this will be!",
    "We'll need recruits if you are interested. Check back with me soon.",
    "He'll regret the day he crossed me! The islands will be mine!"]
__NavyAggro = [
    'Halt!',
    'Halt!',
    'Who goes there!?',
    'This area is off limits!',
    'Over there!',
    'You are under arrest!',
    'Surrender!',
    "It's that pirate again!",
    'A pirate!',
    'What are you doing here!?']
__NavyTaunt = [
    "It'll be the gallows for you, pirate!",
    'You have a morning appointment with the gallows, pirate!',
    'Drop your weapons!',
    "You're the one who escaped from our jail!",
    "You don't stand a chance!",
    'Not so tough now, eh!?',
    "It's back to jail for you!"]
__NavyTeamTalk = [
    'Hold your fire! We want that pirate alive!',
    "You're outnumbered! Surrender!",
    'We have you surrounded!',
    'Capture that pirate!',
    'Take that pirate alive for questioning!']
__NavyBreakCombat = [
    "That is by far the worst pirate I've ever met.",
    'Coward!',
    'Running away again eh!?',
    'Come back here and fight!',
    'That coward ran away!',
    'Bloody pirate!',
    'Accursed pirate!',
    'I better alert the watch.']

def getNavyAggroPhrase():
    dialogue = random.choice(__NavyAggro)
    return dialogue


def getNavyTauntPhrase():
    dialogue = random.choice(__NavyTaunt)
    return dialogue


def getNavyTeamTalkPhrase():
    dialogue = random.choice(__NavyTeamTalk)
    return dialogue


def getNavyBreakCombatPhrase():
    dialogue = random.choice(__NavyBreakCombat)
    return dialogue

__UndeadAggro = [
    'An intruder!',
    'Trespasser!',
    'After that pirate!',
    'Take no prisoners!',
    'Leave no one alive!',
    'Death cannot stop us!']
__UndeadTaunt = [
    'Jolly Roger will be pleased!',
    'Death comes for ye, pirate!',
    'Yer finished, pirate!',
    "See ye in Davy Jones's locker!",
    'Ye fight like a dog!']
__UndeadTeamTalk = [
    'We outnumber ye, pirate!',
    'Ye cannot defeat us all, pirate!',
    'Fool! We outnumber ye!']
__UndeadBreakCombat = [
    'Weakling!',
    'A waste of time!',
    'Ye cannot escape us forever!',
    'Ye cannot hide from us!',
    'Wherever ye go, we will find ye!',
    'Ye run like a dog!',
    'Ye call yerself a pirate!']

def getUndeadAggroPhrase():
    dialogue = random.choice(__UndeadAggro)
    return dialogue


def getUndeadTauntPhrase():
    dialogue = random.choice(__UndeadTaunt)
    return dialogue


def getUndeadTeamTalkPhrase():
    dialogue = random.choice(__UndeadTeamTalk)
    return dialogue


def getUndeadBreakCombatPhrase():
    dialogue = random.choice(__UndeadBreakCombat)
    return dialogue

__EITCAggro = [
    'An intruder!',
    'Halt!',
    "There's that pirate!",
    'What have we here?',
    'Surrender!',
    'Mind your own business, pirate!',
    "Don't meddle in our affairs!",
    'You will regret crossing swords with us, pirate!']
__EITCTaunt = [
    "You don't stand a chance! Surrender!",
    'Lord Beckett will reward us well for this!',
    'You are no match for us!',
    'Any last words, pirate?',
    'There is no escape!',
    "It's time to finish you off!",
    'This is the last mistake you make with us, pirate!']
__EITCTeamTalk = [
    "You're outnumbered! Surrender!",
    'We have you surrounded!',
    'Give it up! We outnumber you!',
    "Don't let that pirate escape!",
    'Take that pirate alive for questioning!']
__EITCBreakCombat = [
    'Bloody pirate!',
    'That coward ran away.',
    'I grow tired of this.',
    "Let's head him off.",
    'Alert the watch!']

def getEITCAggroPhrase():
    dialogue = random.choice(__EITCAggro)
    return dialogue


def getEITCTauntPhrase():
    dialogue = random.choice(__EITCTaunt)
    return dialogue


def getEITCTeamTalkPhrase():
    dialogue = random.choice(__EITCTeamTalk)
    return dialogue


def getEITCBreakCombatPhrase():
    dialogue = random.choice(__EITCBreakCombat)
    return dialogue

__DavyJonesGuysAggro = [
    'Take no prisoners!',
    'Leave no one alive!',
    "You don't belong here.",
    'Part of the ship... Part of the crew...',
    'We belong to the Flying Dutchman!',
    'We serve Davy Jones!']
__DavyJonesGuysTaunt = [
    'Davy Jones will be pleased!',
    'Do you fear death, pirate!',
    "See ye in Davy Jones's locker!"]
__DavyJonesGuysTeamTalk = [
    'We outnumber ye, pirate!',
    'Ye cannot stop Davy Jones, pirate!',
    'Ye cannot defeat us all, pirate!']
__DavyJonesGuysBreakCombat = [
    'Ye cannot escape us forever!',
    'Ye cannot hide from us!',
    'No one can escape Davy Jones!']

def getDavyJonesGuysAggroPhrase():
    dialogue = random.choice(__DavyJonesGuysAggro)
    return dialogue


def getDavyJonesGuysTauntPhrase():
    dialogue = random.choice(__DavyJonesGuysTaunt)
    return dialogue


def getDavyJonesGuysTeamTalkPhrase():
    dialogue = random.choice(__DavyJonesGuysTeamTalk)
    return dialogue


def getDavyJonesGuysBreakCombatPhrase():
    dialogue = random.choice(__DavyJonesGuysBreakCombat)
    return dialogue

RammingSpeed = 'Ramming Speed!!!'
__LeftBroadside = [
    'Broadside port!!!']
__RightBroadside = [
    'Broadside starboard!!!']
__FullSail = [
    'Full speed ahead!',
    'Full sail!']
__ComeAbout = [
    "Let's turn her around!",
    'Prepare tacking maneuver!']
__OpenFire = [
    'Now! Open fire!!!',
    'Shoot! Open fire!!!',
    "Let 'em have it! Open fire!!!"]
__TakeCover = [
    "She's gona broadside! Take cover!!!",
    'Incoming! Take cover!!!',
    "We're being fired on! Take cover!!!"]
__PowerRecharge = [
    'To the cannons!!!',
    "Let's rule the ocean!",
    "Sink 'em all!!"]
__Taunt = [
    'Hey! Over here!']

def getLeftBroadsidePhrase():
    dialogue = random.choice(__LeftBroadside)
    return dialogue


def getRightBroadsidePhrase():
    dialogue = random.choice(__RightBroadside)
    return dialogue


def getFullSailPhrase():
    dialogue = random.choice(__FullSail)
    return dialogue


def getComeAboutPhrase():
    dialogue = random.choice(__ComeAbout)
    return dialogue


def getOpenFirePhrase():
    dialogue = random.choice(__OpenFire)
    return dialogue


def getTakeCoverPhrase():
    dialogue = random.choice(__TakeCover)
    return dialogue


def getPowerRechargePhrase():
    dialogue = random.choice(__PowerRecharge)
    return dialogue


def getTauntPhrase():
    dialogue = random.choice(__Taunt)
    return dialogue

FriendsPageTitle = 'Friends'
FriendInviterTooMany = 'Your friends list is full.\n\nYou will need to remove some other friends if you want to invite \x01gold\x01%s\x02.'
FriendInviterAskingNPC = 'Asking %s to be your friend.'
GuildInviterAskingNPC = 'Inviting %s to join your guild.'
GuildPageTitle = 'Guild'
GuildPageCreateGuild = 'Create Guild'
GuildPageLeaveGuild = 'Leave Guild'
GuildPageRevertGui = 'Guild Options'
GuildPageNameGuild = 'Request Name'
GuildPageShowMembers = 'Show Members'
GuildCodeOptions = 'Invitation Options'
GuildDefaultName = 'Pirate Guild %d'
GuildNoGuild = 'No Guild'
GuildAskLeave = 'Leave Guild?'
GuildAskCreate = 'Create New Guild?'
GuildInvite = 'Create Invitation'
GuildRedeemInvite = 'Redeem Invitation'
GuildAbout = 'About Guilds'
GuildNotifyTokenCreatorOfRedeem = '%s has redeemed a guild token, and is now a member of your guild.'
GuildEMailInvite = 'E-Mail'
GuildNameApprove = 'Your guild name:\n\n\x01guildName\x01\x01larger\x01%s\x02\x02\n\nwas approved!'
GuildNameApproveTitle = 'Congratulations!'
GuildNameReject = 'Your desired guild name:\n\n"\x01guildName\x01\x01larger\x01%s\x02\x02"\n\nwas rejected.\n\nPlease select another.'
GuildNameRejectTitle = 'Sorry!'
GuildNameDuplicate = 'Desired guild name is already in use.  Please select another.'
GuildInviteResponse = 'Please make note of this code and select a code type'
GuildInviteJoinSucessful = "You're now a member of %s"
GuildInviteTooManyTokens = 'You have too many invite codes pending. Please have your friends redeem them, or wait until they expire.'
GuildInviteSingleButton = 'Single Use Invite'
GuildInviteLimitedButton = 'Multiple Use Invite'
GuildInviteUnlimitedButton = 'Unlimited Use Invite'
GuildManageInvite = 'Token Management'
GuildAboutTokenManagement = 'About Code Management'
GuildClearPerm = 'Clear Unlimited Invite'
GuildClearLimUse = 'Clear Limited Use Invites'
GuildSuspendPerm = 'Suspend Unlimited Invite'
GuildNotificationOptions = 'Notification Options'
GuildTokenAbout = 'About Guild Token Management'
GuildTokenMenuToMembers = 'Show Members'
GuildPermCodeLabel = 'Unlimited Invite Code'
GuildNoPermInviteCodeSet = 'None Set'
GuildMessageClearPermInvite = 'Delete your unlimited use invite code?'
GuildMessageClearLimInvite = 'Delete all active limited use invite codes?'
GuildTokenTut = ('If you have generated an unlimited use invite code, it will be displayed at the top of the panel.', 'Unlimited use invite codes can be deleted by clicking the Clear Unlimited Invite button. Limited use codes (single use and limited multi use) can be deleted by clicking the Clear Limited Use Invites button.')
GuildTut = ('Guilds are useful for grouping with other pirates and staying grouped with them even after you log out.', 'If you are a basic member, you may join a guild by invite.  If you are an unlimited member, you can start your own guild by pressing the Create Guild button.', 'To invite a pirate to your new guild, just click on them and select Guild from the menu. If they are not currently online, click the Create Invitation button to generate a code that can be redeemed for membership in your guild. Give the code to your friend, they can then join your guild via the Redeem Invitation button.', 'Three types of invite codes exist:\n\nSingle Use : Good for one redemption\n\nLimited Multi Use: Redeemable up to the number of times selected\n\nUnlimited Use: Unlimited Redemptions', 'As Guildmaster, you can promote other members to Officer and allow them to invite others into the guild.')
SocialPanelHelpTitle = 'Social Panel Help'
SocialPanelHelpContents = ('The social panel is where you can access and manage your Friends, Crew, and Guild.', 'Friends:\n\nTo make Friends, click on the Pirate you would like to make Friends with. Their Pirate Detail Panel will open. Click Friendship.\n\nYou will get a pop-up that says "Asking (Pirate Name) to be your friend. "Sometime later you get a "You are now friends with (Pirate Name)!" or "(Pirate Name) said no, thank you."', 'Friends:\n\nAll your Friends appear on your Friends Panel, along with a note telling you if they are currently online or not. You can have up to 300 Friends.', 'Crew:\n\nInviting someone to your Crew is very similar to making a Friend. Simply click on the Pirate you would like to invite to join your Crew. Their Pirate Detail Panel will open. Click Crew.\nYou will get a pop-up that says "Would you like to invite (Pirate Name) to join your crew? "Sometime later you get a "(Pirate Name) has joined your crew!" or "(Pirate Name) declined your crew invitation."', 'Crew:\n\nAll Crew members will appear on your Crew Panel. Unlike Friends and Guilds, Crews are not persistent between sessions. You can have up to 8 members in your Crew.', 'Guilds:\n\nGuilds are useful for grouping with other pirates and staying grouped with them even after you log out. If you are a basic member, you may join a guild by invite. If you are an unlimited member, you can start your own guild by pressing the Create Guild button.', 'Guilds:\n\nTo invite a pirate to your new guild, just click on them and select Guild from the menu. If they are not currently online, click the Create Invitation button to generate a code that can be redeemed for membership in your guild. Give the code to your friend, they can then join your guild via the Redeem Invitation button.', 'Guilds:\n\nThree types of invite codes exist:\n\nSingle Use : Good for one redemption\n\nLimited Multi Use: Redeemable up to the number of times selected\n\nUnlimited Use: Unlimited Redemptions', 'Guilds:\n\nAs Guildmaster, you can promote other members to Officer and allow them to invite others into the guild.')
PVPInviterAskingNPC = 'Challenging %s to a battle...'
TeleportConfirmTitle = 'Confirm Teleport'
TeleportConfirmMessage = 'Would you like to go to %s?'
TeleportConfirmOK = lOk
TeleportConfirmNo = lNo
TeleportToPlayerFailMessage = 'Could not successfully complete teleport because the pirate you were going to became unavailable.'
TeleportToGoneShipFailMessage = 'Could not successfully complete teleport because the ship you were going to became unavailable.'
TeleportToBoardingShipFailMessage = 'Could not successfully complete teleport because the ship you were going to is engaged in a flagship battle.'
TeleportGenericFailMessage = 'There was a problem with going to your destination.'
GenericConfirmOK = lOk
GenericConfirmNo = lNo
GenericConfirmNext = 'Next'
GenericConfirmDone = 'Done'
GenericConfirmCancel = 'Cancel'
CrewPageTitle = 'Crew'
CrewPageLeaveCrew = 'Leave Crew'
CrewOptions = 'Crew Options'
CrewList = 'Crew List'
CrewLookingForButton = 'Looking for Crew'
CrewLookingForAd = 'Looking for Crew'
CrewIconButton = 'Toggle Crew Icon'
CrewIconTitle = 'Crew Icon Selection'
CrewClearIconButton = 'Clear Crew Icon'
CrewStartACrewButton = 'Start a Crew'
CrewBoardingAccessButton = 'Boarding Access'
CrewBoardingAccessAllowCrew = 'Allow Crew'
CrewBoardingAccessAllowFriends = 'Allow Friends'
CrewBoardingAccessAllowGuild = 'Allow Guild'
CrewBoardingAccessAllowPublic = 'Allow Public'
CrewBordingAccessBack = 'Back'
CrewInviteeTooManyCrewed = '\x01gold\x01%s\x02 would like to be in your crew, but your crew is full!'
CrewInviteeInvitation = 'Would you like to join the crew of \x01gold\x01%s\x02?'
CrewInviteeOK = lOk
CrewInviteeNo = lNo
CrewInviterTitle = 'Invite Crew'
CrewInviterOK = lOk
CrewInviterCancel = lCancel
CrewInviterStopBeingCrewed = 'Remove'
CrewInviterYes = lYes
CrewInviterNo = lNo
CrewInviterTooMany = 'Your crew is full.\n\nYou will need to remove some crew members if you want to invite \x01gold\x01%s\x02.'
CrewInviterNotYet = 'Would you like to invite \x01gold\x01%s\x02 to join your crew?'
CrewInviterCheckAvailability = 'Seeing if \x01gold\x01%s\x02 is available.'
CrewInviterNotAvailable = '\x01gold\x01%s\x02 is busy right now; try again later.'
CrewInviterWentAway = '\x01gold\x01%s\x02 went away.'
CrewInviterAlready = '\x01gold\x01%s\x02 is already in your crew.'
CrewInviterAlreadyInvited = '\x01gold\x01%s\x02 has already been invited.'
CrewInviterAskingNPC = 'Asking \x01gold\x01%s\x02 to join your crew.'
CrewInviterEndCrewship = 'Are you sure you want to kick \x01gold\x01%s\x02 out of your crew?'
CrewInviterCrewedNoMore = '\x01gold\x01%s\x02 is no longer in your crew.'
CrewInviterSelf = 'You are already in your own crew!'
CrewInviterLeave = 'Are you sure you want to leave your crew?'
CrewInviterLeft = 'You left the crew.'
CrewInviterIgnored = '\x01gold\x01%s\x02 is ignoring you.'
CrewInviterAsking = 'Asking \x01gold\x01%s\x02 to join your crew.'
CrewInviterCrewSaidYes = '\x01gold\x01%s\x02 has joined your crew!'
CrewInviterCrewSaidNo = '\x01gold\x01%s\x02 declined your crew invitation.'
CrewInviterCrewSaidNoNewCrews = '\x01gold\x01%s\x02 is not looking for a new crew right now.'
CrewInviterOtherTooMany = '\x01gold\x01%s\x02 has too many crew members already!'
CrewInviterMaybe = '\x01gold\x01%s\x02 was unable to answer.'
CrewInviterDown = 'Cannot join crews now.'
CrewInviterInOtherCrew = 'Sorry \x01gold\x01%s\x02 is in a different crew.'
CrewInviterNotCaption = 'Sorry you are not the caption of your crew.'
CrewInviterNotCaption1 = 'Sorry only \x01gold\x01%s\x02 can invite new crew members.'
CrewMatchInviteeInvitation = 'Would you like to join the crew of \x01gold\x01%s\x02?\nThey are currently located in \x01gold\x01%s\x02.'
CrewMatchInviteeInvitationNoLocation = 'Would you like to join the crew of \x01gold\x01%s\x02?'
CrewMatchCrewFound = 'Crew Found'
CrewMatchCrewLookout = 'Crew Lookout'
CrewMatchNoCrewFound = 'Crew Matching is now active. Unfortunately, a crew could not be found. The search will continue.'
CrewMatchNoCrewFoundPVP = 'Privateering Crew Matching is now active. Unfortunately, a crew could not be found. The search will continue.'
CrewMatchRecruitButton = 'Recruit Crewmates'
CrewMatchJoinCrewButton = 'Find a Crew'
CrewMatchJoinPVPCrewButton = 'Find a Privateer Crew'
CrewMatchInviterText = 'Please select the notoriety range for the pirates you wish to recruit:'
CrewMatchCrewNowUnavailable = 'Sorry, the crew you just tried to join is now unavailable. Your crew search will continue.'
CrewMatchRemoveAvatarFromLookout = 'Crew Matching has been deactivated'
CrewMatchRemoveAvatarFromLookoutPVP = 'Privateering Crew Matching has been deactivated'
CrewMatchEnabledForCrew = 'Crew Matching has been activated for your crew. New recruits will automatically be made members of your crew.'
CrewMatchEnabledForCrewPVP = 'Privateering Crew Matching has been activated for your crew. New recruits will automatically be made members of your crew.'
CrewMatchAdvancedOptionsButton = 'Advanced Options'
CrewMatchCancelButton = 'Cancel'
CrewMatchAdvancedNotorietyRange = 'Notoriety Range:'
CrewMatchAdvancedMinSailSkillLevel = 'Minimum Sailing Level:'
CrewMatchAdvancedMinCannonSkillLevel = 'Minimum Cannon Level:'
CrewMatchAdvancedText = 'Advanced Options'
CrewMatchSimpleOptionsButton = 'Basic Options'
CrewMatchAvatarAddedToYourCrew = 'Crew Matching has added \x01gold\x01%s\x02 to your crew.'
CrewMatchRangeIndicator = 'Range +/- %s Points'
CrewMatchLevelIndicator = 'Level %s'
CrewMatchEmptyName = 'Pirate'
PrivateerAllTeamsFull = 'Both Privateer teams are full!\n\nYou can join another server or an existing Privateer crew.\n\nDo you wish to join an existing Privateer crew?'
PrivateerSingleTeamFull = 'Sorry, this Privateer team is full!\n\nDo you wish to balance out the battle and join the opposition?'
CrewHUDNoCrew = 'No Crew Bonus'
CrewHUDCrewNearBy = 'Crew: \x01gold\x01%s\x02%% Bonus!'
CrewHUDCrewPanelButton = 'Crew HUD'
TradePanelTitle = 'Trade'
TradeInviterOK = lOk
TradeInviterCancel = lCancel
TradeInviterStopTrading = 'Stop'
TradeInviterYes = lYes
TradeInviterNo = lNo
TradeInviterClickToon = 'Click on the toon you would like to trade with.'
TradeInviterNotYet = 'Would you like to trade with %s?'
TradeInviterCheckAvailability = 'Seeing if %s is available.'
TradeInviterNotAvailable = '%s is busy right now; try again later.'
TradeInviterWentAway = '%s went away.'
TradeInviterAlready = '%s is already trading.'
TradeInviterAlreadyInvited = '%s has already been invited to trade.'
TradeInviterAskingNPC = 'Asking %s to trade.'
TradeInviterEndTrade = 'Are you sure you want to stop trading with %s?'
TradeInviterTradeNoMore = '%s is no longer trading.'
TradeInviterSelf = 'You cannot trade with yourself!'
TradeInviterIgnored = '%s is ignoring you.'
TradeInviterAsking = 'Asking %s to trade with you.'
TradeInviterTradeSaidYes = '%s said yes!'
TradeInviterTradeSaidNo = '%s said no, thank you.'
TradeInviterTradeSaidNoNewTrades = '%s is not interested in trades right now.'
TradeInviterMaybe = '%s was unable to answer.'
TradeInviterDown = 'Cannot trade now.'
PVPInviterBusy = '%s is busy'
PVPInviterNotYet = 'Would you like to issue a Challenge to %s and crew? Your crew members will also be invited.'
PVPInviterCheckAvailability = 'Checking if %s is available for the Challenge...'
PVPInviterEndChallenge = 'Cancel challenge with %s?'
PVPInviterNoMore = 'Removing Challenge with %s.'
PVPInviterNoMore = 'You cannot fight with yourself.'
PVPInviterAsking = 'Issuing Challenge to %s.'
PVPInviterSaidYes = '%s accepted your Challenge!'
PVPInviterSaidNo = '%s declined your Challenge!'
PVPInviterMaybe = "%s didn't bother to answer."
PVPInviterDown = 'Cannot Challenge right now.'
PVPInviterSelf = 'You cannot Challenge yourself to a fight.'
PVPInviteeInvitation = '%s is issuing you a Challenge!'
PVPRulesPanelPlay = 'PLAY'
PVPDefaultTitle = 'Skirmish'
PVPDefaultInstructions = 'Find treasure chests and bring them back to your fort. First crew to amass 200 gold wins.'
PVPPanelTitle = 'Game Score'
SiegePanelTitle = 'Ship PVP High Scores'
PVPPickUpTreasure = 'Press %s to pick up treasure' % InteractKey
PVPStealTreasure = 'Press %s to steal treasure' % InteractKey
PirateerDeckTreasure = 'Sail me to your base to unload me!'
PVPReplay = 'Replay Match'
PVPExit = 'Exit Match'
PVPStatDetail = 'View Details'
PVPStatSummary = 'View Summary'
PVPGoldAbbrev = 'g'
PVPUnknownValue = '??'
PVPTeam = 'Team %s: '
PVPYourTeam = 'Your Team: '
PVPOtherTeam = 'Other Team: '
PVPYourShip = 'Your Ship: '
PVPOtherShip = 'Other Ship: '
PVPYouCarry = 'You are carrying '
PVPYourScoreIs = 'Your score is '
PVPResult = 'Match Result: '
PVPTied = 'Tied...'
PVPWon = 'Won!'
PVPLost = 'Lost.'
PVPYourScore = "Your Team's Gold"
PVPOtherScore = "Other Team's Gold"
PVPLootStolen = 'Gold Stolen'
PVPLootDeposit = 'Gold Deposited'
PVPLootDropped = 'Gold Dropped'
PVPEnemiesDefeated = 'Enemies Defeated'
PVPTimesDefeated = 'Times Defeated'
PVPScore = 'Score'
PVPBounty = 'Bounty'
PVPTime = 'Total Time'
PVPRating = 'Rating'
PVPYourRank = 'You ranked #'
PVPYourTeamRank = 'Your team ranked #'
PVPPlayer = 'Player'
PVPShip = 'Ship'
PVPTeamFull = 'Sorry, you cannot launch your boat because this Privateer team has enough boats--for the moment. Please try again later.'
_pvpRating = {
    0: 'Landlubber',
    10: 'Swabbie',
    20: 'Deck Hand',
    30: 'Old Salt',
    40: 'Mate',
    50: 'Sea Dog',
    60: 'Swarthy',
    70: 'Leatherneck'}
PVPTitleLandRanks = {
    0: 'Noob',
    1: 'Rookie',
    2: 'Brawler',
    3: 'Duelist',
    4: 'Buccaneer',
    5: 'Swashbuckler',
    6: 'Warmonger',
    7: 'War Master'}
PVPTitleSeaRanks = {
    0: 'Swabbie',
    1: 'Mariner',
    2: 'Lieutenant',
    3: 'Commander',
    4: 'Captain',
    5: 'Commodore',
    6: 'Vice Admiral',
    7: 'Admiral'}
FounderTitleRanks = {
    0: None,
    1: 'Founder'}
PVPTitleLandName = 'PvP Title'
PVPTitleSeaName = 'Privateering Title'
FounderTitleName = 'Founder Title'
PVPInfamy = 'Infamy'
PVPInfamySea = 'Infamy'
PVPInfamyLand = 'Infamy'
PVPSalvage = 'Salvage'
PVPInfamySpendable = 'Bounty'
PVPPrivateeringTitle = 'Privateering Infamy'
PVPLandTitle = 'PvP Infamy'
PVPTitleSeaDesc = 'Sink ships in Privateering!'
PVPTitleLandDesc = 'Kill other players in PvP!'
FounderTitleDesc = 'Founders were around during the Beta!'
NoTitle = 'No Title'
TitlesTitle = 'Achievements'
DisplayTitle = 'Display Badges'
DisplayTitleLand = 'Your\nNametag'
DisplayTitleSea = 'Ship\nNametag'
TitleOn = 'On'
TitleOff = 'Off'
import random

def getPVPRating(score):
    return random.choice(_pvpRating.values())

PirateerTitle = 'Dubloon Lagoon'
PirateerInstructions = 'Bring all the treasures to your base to win! But remember only merchant ships can haul treasure.'
PVPTeamBattleInstructions = 'Arrr matey, this be an all-out battle. The team that defeats the most opponents wins.'
PVPShipBattleInstructions = 'Arrr matey, this be an all-out battle at sea. The last team afloat wins.'
PVPBattleInstructions = 'Arrr matey, this be an all-out battle. Every man for himself! The pirate that defeats the most opponents wins.'
PVPDefeat = '%(defeater)s defeated %(defeated)s!'
PVPYouDefeated = 'You defeated %(defeated)s!'
PVPYouWereDefeated = 'You were defeated by %(defeater)s!'
PVPSuicide = '%(defeated)s was clumsy with his grenade!'
PVPYouSuicide = 'You were defeated by your own grenade!'
PVPTeam1name = 'French'
PVPTeam2name = 'Spanish'
PVPSinkAnnouncement = 'The %(shipName)s (%(teamName)s) sank the %(sunkShipName)s (%(sunkTeamName)s)!'
PVPSinkWithAssistAnnouncement = 'The %(shipName)s (%(teamName)s) and the %(assistShipName)s (%(assistTeamName)s) sank the %(sunkShipName)s (%(sunkTeamName)s)!'
PVPSinkStreakAnnouncement = 'The %(shipName)s (%(teamName)s) sank %(amount)s ships in a row!'
LookoutPanelTitle = 'Lookout'
LookoutPanelTitleDesc = 'Choose an activity:'
LookoutPanelTitleDescGame = 'Choose a game:'
LookoutPanelStatus = 'Lookout Status'
LookoutPanelStatusDesc = 'Currently searching for...'
LookoutPanelInvite = 'Lookout Invite'
LookoutPanelInviteDesc = 'Inviting crew members for...'
LookoutPanelJoin = 'Lookout Join'
LookoutPanelJoinDesc = 'Decide if you want to join this game...'
LookoutPanelJoined = 'Lookout Joined'
LookoutPanelJoinedDesc = 'Waiting for others to join the game'
LookoutSearchContinue = 'Continue search'
LookoutSearchCancel = 'Cancel search'
LookoutJoinCancel = 'Cancel join'
LookoutInviteSkip = 'Skip All'
LookoutJoinStatus = 'Waiting for other players...'
LookoutFailedMsg = 'Match failed to be created, continuing search...'
LookoutAbortedMsg = 'Match failed to be created, ending search...'
LookoutFoundTitle = 'Match Found!'
LookoutFoundStatusCat = 'Game Category: %s'
LookoutFoundStatusType = 'Game Type: %s'
LookoutFoundStatusChance = 'Chance to find a match: %s'
LookoutFoundStatusChanceLow = 'Low'
LookoutFoundStatusChanceModerate = 'Moderate'
LookoutFoundStatusChanceHigh = 'High'
LookoutChallengeTitle = 'Challenge!'
LookoutChallengeDesc = 'Pick a game type to accept:'
LookoutSkirmishTitle = 'Skirmish!'
LookoutSkirmishDesc = 'Inviting other players...'
LookoutFoundJoin = 'Join'
LookoutFoundSkip = 'Skip'
LookoutJoinMsg = 'You will be teleported when game is created...'
LookoutTypeTitle = 'Pick type...'
LookoutOptionsTitle = 'Options'
LookoutOptionsDesc = "Select game's options below:"
LookoutSubmit = lSubmit
LookoutCancel = lCancel
LookoutConfirm = lConfirm
LookoutNext = lNext
LookoutBack = lBack
LookoutTimer = 'Time left to join: %d seconds!'
Options = 'Options'
LookoutStartMsg = 'You will be notified when a match is found.'
LookoutFoundMsg = 'Game found, would you like to join?'
LookoutCancelMsg = 'Lookout canceled.'
LeaveInstance = 'Return to Main World'
LookoutInviteFromMsg = 'You are invited by %s to a %s, would you like to join?'
LookoutInviteMsg = 'You are invited to a %s, would you like to join?'
LookoutInviteFail = 'Failed to invite %s crew member(s). They are not allowed to play the chosen game.'
LookoutInviteIgnore = 'Cannot invite your crew at this moment, an invite is already in progress.  You can try again in a minute.'
LookoutInviteNeedCrew = 'You need to join or create a crew to play that type of game.'
ParlorGame = 'Parlor Games'
PVPGame = 'Pirate vs Pirate'
TMGame = 'Treasure Maps'
CrewGame = 'Find a Crew'
QuestGame = 'Do a Quest'
HSAGame = HighSeasAdventureStartTitle
PokerGame = 'Poker Game'
BlackjackGame = 'Blackjack'
FindACrew = 'Find a Crew'
FindAPVPCrew = 'Find a Privateer Crew'
RecruitCrewMembers = 'Recruit Crew Members'
ParlorGameBrief = 'parlor game'
PVPGameBrief = 'Pirate vs Pirate game'
TMGameBrief = 'Treasure Map'
CrewGameBrief = 'crew'
QuestGameBrief = 'quest'
HSAGameBrief = HighSeasAdventureStartTitle
ParlorGameDesc = 'Play a card game or other parlor game with other pirates'
PVPGameDesc = 'Compete with other pirates in a variety of games'
TMGameDesc = 'Work with other pirates to recover some treasure'
CrewGameDesc = 'Look for a crew of other pirates to join'
QuestGameDesc = 'Find other pirates working on a specific quest'
HSAGameDesc = 'Set sail with other pirates and battle enemies in the open waters'
ParlorGameDesc = 'Play a card game or other parlor game with other pirates'
PVPGameDesc = 'Compete with other pirates in a variety of games'
TMGameDesc = 'Work with other pirates to recover some treasure'
CrewGameDesc = 'Look for a crew of other pirates to join'
QuestGameDesc = 'Find other pirates working on a specific quest'
HSAGameDesc = 'Set sail with other pirates and battle enemies in the open waters'
GameStyleBattleDesc = 'Every pirate for his/her self'
GameStyleTeamBattleDesc = 'Pirate team vs. Pirate team'
GameStyleShipBattleDesc = "Sink the other team's ship"
GameStyleCTFDesc = "Capture the other team's pirate flag"
GameStyleCTLDesc = 'Most gold captured wins'
GameStylePirateer = 'Most gold captured with ships wins'
GameStylePoker = 'Standard poker rules'
GameStyleBlackjack = 'Hand closest to 21 wins'
CrewStyleFindACrewDesc = 'Search for a crew to join'
CrewStyleRecruitMembersDesc = 'Find members for your crew'
CrewStyleFindAPVPCrewDesc = 'Search for a privateering crew to join'
AnyGame = 'Any Game'
CTFGame = 'Capture The Flag'
CTLGame = 'Capture The Loot'
PTRGame = 'Pirateer'
BTLGame = 'Mayhem'
TBTGame = 'Team Battle'
SBTGame = 'Ship Battle'
ARMGame = 'Armada'
TKPGame = 'Treasure Keeper'
BTBGame = 'Borrow the Boat'
GameDuration = 'Duration'
GameDurationShort = 'Short'
GameDurationMed = 'Medium'
GameDurationLong = 'Long'
GameMatchCount = 'Match Count'
GamePassword = 'Game Password'
GameMinBet = 'Minimum Bet'
GameNPCPlayers = 'Include AI Players'
GameLocation = 'Game Location'
GameUseCrew = 'Use Current Crew'
GameMinPlayers = 'Min Num Players'
GameDesPlayers = 'Desired Num Players'
GameMaxPlayers = 'Max Num Players'
GameMaxCrew = 'Max Crew Size'
GameMaxShip = 'Max Crew Ship'
GameVIPPass = 'VIP Pass'
GameSoloPlay = 'Play Treasure Map Alone'
PlayTMNow = 'Play ' + BossBattleName + ' Now'
PlayTMNowHelp = 'Give it a shot alone'
PlayTMLookout = BossBattleName + ' With Crew'
PlayTMLookoutHelp = 'Find others to play with'
PlayTMBlackPearlNotReady = 'The Black Pearl boss battle is coming soon!'
PlayTMVelvetRope = '\x01smallCaps\x01Unlimited Access Members Only\x02'
AvatarPanelFriends = 'Friends'
AvatarPanelPlFriends = 'Player Friends'
AvatarPanelWhisper = 'Whisper'
AvatarPanelSecrets = 'Secrets'
AvatarPanelGoTo = 'Go To'
AvatarPanelIgnore = 'Ignore'
AvatarPanelReport = 'Report'
AvatarPanelStopIgnore = 'Stop Ignoring'
AvatarPanelCrew = 'Crew'
AvatarPanelGuild = 'Guild'
AvatarPanelTrade = 'Trade'
AvatarPanelSkirmish = 'Crew Battle'
AvatarPanelRelationships = 'Friendship'
AvatarPanelFriendList = 'List Hearties'
AvatarPanelAvatar = 'Show Pirate'
AvatarPanelPlayer = 'Show Player'
ChatTabAll = 'Local'
ChatTabGuild = 'Guild'
ChatTabCrew = 'Crew'
ChatTabFrench = 'French'
ChatTabSpanish = 'Spanish'
ChatTabShipPVP = 'Privateer'
FriendSecretIntro = "If you are playing Disney's Pirates of the Caribbean Online with someone you know in the real world, you can become Player Friends.  You can chat using the keyboard with your Player Friends.  Other Pirates won't understand what you're saying.\n\nYou do this by getting a Player Friend Code.  Tell the Player Friend Code to your friend, but not to anyone else.  When your friend types in your Player Friend Code on his or her screen, you'll be Player Friends in Pirates!"
NoSecretChatAtAll = 'To chat with a friend, the Player Friends feature must first be enabled.  Player Friends allows one member to chat with another member only by means of a Player Friend Code that must be communicated outside of the game.\n\nTo activate this feature or to learn more about it, exit Pirates and then click on "Account Options" on the Pirates web page.'
RelationshipChooserTitle = '\nWhat Ye be wanting with %s?'
RelationshipChooserAvFriendsMake = 'Make Friends'
RelationshipChooserAvFriendsBreak = 'Break Friends'
RelationshipChooserPlFriendsMake = 'Make Player Friends'
RelationshipChooserPlFriendsBreak = 'Break Player Friends'
RelationshipChooserPlSecrets = 'Use Friend Codes'
AFKFlag = '[AFK]'
from pandac.PandaModules import TextProperties
from pandac.PandaModules import TextPropertiesManager
tpMgr = TextPropertiesManager.getGlobalPtr()
gold = TextProperties()
gold.setTextColor(*PiratesGuiGlobals.TextFG1)
tpMgr.setProperties('gold', gold)
white = TextProperties()
white.setTextColor(*PiratesGuiGlobals.TextFG2)
tpMgr.setProperties('white', white)
slant = TextProperties()
slant.setSlant(0.2)
tpMgr.setProperties('slant', slant)
uline = TextProperties()
uline.setUnderscore(True)
uline.setUnderscoreHeight(-.12)
tpMgr.setProperties('uline', uline)
smallCaps = TextProperties()
smallCaps.setSmallCaps(1)
tpMgr.setProperties('smallCaps', smallCaps)
questObj = TextProperties()
questObj.setTextColor(0.3, 0.7, 0.25, 1)
tpMgr.setProperties('questObj', questObj)
interfaceRed = TextProperties()
interfaceRed.setTextColor(0.9, 0.4, 0.4, 1)
tpMgr.setProperties('Ired', interfaceRed)
brightRed = TextProperties()
brightRed.setTextColor(0.9, 0.1, 0.1, 1)
tpMgr.setProperties('Bred', brightRed)
interfaceBlue = TextProperties()
interfaceBlue.setTextColor(0.1, 0.5, 1.0, 1)
tpMgr.setProperties('Iblue', interfaceBlue)
interfaceGreen = TextProperties()
interfaceGreen.setTextColor(0.1, 1.0, 0.1, 1)
tpMgr.setProperties('Igreen', interfaceGreen)
interfaceYellow = TextProperties()
interfaceYellow.setTextColor(1.0, 1.0, 0.0, 1)
tpMgr.setProperties('Iyellow', interfaceYellow)
interfaceWhite = TextProperties()
interfaceWhite.setTextColor(1.0, 1.0, 1.0, 1)
tpMgr.setProperties('Iwhite', interfaceWhite)
guildName = TextProperties()
guildName.setGlyphScale(0.8)
guildName.setSmallCaps(1)
guildName.setTextColor(1.0, 1.0, 1.0, 1)
tpMgr.setProperties('guildName', guildName)
larger = TextProperties()
larger.setGlyphScale(1.5)
tpMgr.setProperties('larger', guildName)

def getHeadingScale(headingLevel):
    if headingLevel == 1:
        return 1.0
    else:
        return 1.2


def makeHeadingString(str, headingLevel):
    if headingLevel == 1:
        str = '\x01%s\x01%s\x02' % ('slant', str)
    elif headingLevel == 2:
        str = '\x01%s\x01\x01%s\x01%s\x02\x02' % ('gold', 'smallCaps', str)
    elif headingLevel == 3:
        str = str.upper()
    
    return str

TutorialPanelDialog = {
  'seachestOpen': '\nClick on the \x01Ired\x01Sea Chest Icon\x02 to open it.',
  'questPageOpen': '\nClick on the \x01Ired\x01Journal Icon\x02 to view your quests.',
  'questPageClose': '\nThe journal shows what to do next.\nClick on the \x01Ired\x01Sea Chest Icon\x02 to close it.',
  'boardShip': "\nPress \x05shiftButton\x05 to board Bo Beck's boat.",
  'useCannon': '\nPress \x05shiftButton\x05 to use the cannon.',
  'moveCannon': '\nHold down \x01Ired\x01Right Mouse Button\x02 then move the mouse to aim.',
  'fireCannon': '\nClick \x01Ired\x01Left Mouse Button\x02 to shoot.',
  'wreckInstruction': 'Hit the ship wreck 3 times. Hits so far \x01Ired\x01',
  'exitCannon': '\nPress \x01Ired\x01Escape\x02 to stop using the cannon.',
  'showBlacksmith': 'Walk towards the light ray.\nEnter the Old Warehouse to get a sword.',
  'doCutlassTutorial': 'Would you like to learn how to use weapons?',
  'drawSword': '\nClick on the \x01Ired\x01Sword Icon\x02 to draw your weapon.',
  'attackSword': '\nClick with \x01Ired\x01Left Mouse Button\x02 to attack the dummy.',
  'comboSword': '\nTo perform a combo, \x01Ired\x01Click\x02 to swing then \x01Ired\x01Click\x02 again at the end of your swing.  Timing is key!',
  'cutlassLvl': '\nYou earned enough reputation to level up your cutlass.\nClick on the \x01Ired\x01Sea Chest Icon\x02 to open it.',
  'cutlassSkillOpen': '\nClick on the \x01Ired\x01Skill Icon\x02 to view your skills.',
  'cutlassSkillUnlock': '\nYou earned 1 Skill Point which can be used to unlock and improve skills. Click on the \x01Ired\x01Sweep Icon\x02 to unlock it.',
  'cutlassDoneLvl': '\nSweep Skill Unlocked. \nClick on the \x01Ired\x01Sea Chest Icon\x02 to continue.',
  'specialMenu': '\nClick the \x01\\Ired\x01Sweep Icon\x02.',
  'sheatheSword': '\nPress \x01Ired\x01Escape\x02 to put away your weapon.',
  'showSkeleton': '\nDefeat an \x01Ired\x01Undead Gravedigger\x02 before you visit Tia Dalma.',
  'showJungleTia': '\nWalk through the \x01Ired\x01Tree Tunnel\x02 to visit Tia Dalma.',
  'receiveCompass': 'Would you like to learn how to use the compass?',
  'compassActiveQuest': 'The \x01Iyellow\x01ARROW\x02 points to your quest goal.',
  'compassIconsBearing': 'You are the \x01Iwhite\x01DOT\x02 in the center. \nExits are shown as \x01Iwhite\x01RECTANGLES\x02.',
  'compassIconsPeople': 'Enemies are shown in \x01Ired\x01RED\x02. Townfolk are shown in \x01Igreen\x01GREEN\x02. Other players are shown in \x01Iblue\x01BLUE\x02.',
  'showNavy': "Defeat \x01Ired\x01Navy Soldiers\x02 to find the Black Pearl release orders.\nFollow the arrow towards the Governor's Mansion.",
  'showGovMansion': "Enter the \x01Ired\x01Governor's Mansion\x02 to deliver release orders to Elizabeth Swann.",
  'showDarby': 'Walk towards the light ray. \nFind \x01Ired\x01Darby Drydock\x02 to get a ship.',
  'showDinghy': 'Use a \x01Ired\x01dinghy\x02 to launch your ship.',
  'showBarbossa': "Sail to \x01Ired\x01Devil's Anvil\x02 to visit Barbossa.",
  'pistolAim': '\nHold down \x01Ired\x01Right Mouse Button\x02 then move the mouse to aim at the monkey.',
  'pistolTarget': '\nThe aiming circle turns red over an enemy.',
  'pistolHit': '\nClick the \x01Ired\x01Left Mouse Button\x02 to shoot.',
  'pistolPractice': '\nPress \x01Ired\x01Escape\x02 to put away your weapon.',
  'lookoutChestOpen': '\nClick on the \x01Ired\x01Sea Chest Icon\x02 to open it.',
  'lookoutOpen': '\nClick on the \x01Ired\x01Lookout Icon\x02 to look for other players\nin Pirate vs. Pirate combat.',
  'lookoutClose': '\nClick on the \x01Ired\x01Sea Chest Icon\x02 to close it.',
  'showTortugaJack': '\nSail to \x01Ired\x01Tortuga\x02 and find \x01Ired\x01Jack Sparrow\x02.',
  'teleport_tut1': 'Now ....Press the \x05SmallMap\x05 to bring up the Map of the Islands.',
  'teleport_tut2': 'Continents that are available for transport to are highighted. As you unlock additional continents for transport, they will become highlighted ont his map. Double click the left mouse button \x05leftClick\x05 \x05leftClick\x05 on the highlighted continent (Tortuga) to be transported to there.',
  'teleport_tut3': 'You have safely arrived in Tortuga. Tortuga is never more than a double-click away. Click Ok to exit the tutorial.',
  'chat_tut1': 'Chatting with other pirates can be helpful for teaming up on the enemy. \nClick on the \x01Ired\x01Arrow\x02 or press ENTER to start chatting.',
  'chat_tut2': '\nSend a message by typing it at the prompt and pressing ENTER.',
  'chat_tut3': 'You can make friends or start a crew by clicking on another pirate and choosing Friend or Crew from the menu.',
  'chat_tut_alt4': 'You can make friends or start a crew by clicking on another pirate and choosing Friend or Crew from the menu.',
  'chat_tut5': 'To see a list of your friends or crewmates, press F or click the mug icon in your Sea Chest.',
  'chat_tut4': 'In addition to clicking on other players, there are other advanced options for forming a crew in the Crew Panel.',
  'chat_tut_alt5': 'To see a list of your friends or crewmates, press F or click the mug icon in your Sea Chest.',
  'chat_tut_alt1': 'Chatting with other pirates can be helpful for teaming up on the enemy.',
  'chat_tut_alt2': '\nClick on the \x01Ired\x01Skull Icon\x02 in the lower left corner to bring up the SpeedChat menu.',
  'chat_tut_alt3': '\nSend a SpeedChat message by clicking on a menu item.'}
from pirates.uberdog import UberDogGlobals
Reloading = 'Reloading'
CannonAmmoNames = {}
StatusTrayHp = 'Health'
StatusTrayVoodoo = 'Voodoo'
Vitae = 'Groggy'
VitaeDesc = 'You were knocked out. Your current maximum health and voodoo have been temporarily limited.'
WeaponPageInfo1 = 'Choose Slot Above to Equip Weapon'
WeaponPageInfo2 = 'Select Weapon from List Below'
WeaponPageInfo3 = 'Not skilled enough to use weapon'
WeaponPageInfo4 = 'Need Training to use weapon'
SkillPageUnspentPoints = 'Skill Points: %d'
LauncherPhaseNames = {
    0: 'Initialization',
    1: 'Game Engine',
    2: 'Make-A-Pirate',
    3: 'Rambleshack',
    4: 'Port Royal',
    5: 'Islands',
    6: 'Chat Dictionary'}
LauncherProgress = '%(name)s (%(current)s of %(total)s)'
LauncherStartingMessage = 'Starting Pirates Online... '
LauncherDownloadFile = 'Downloading update for ' + LauncherProgress + '...'
LauncherDownloadFileBytes = 'Downloading update for ' + LauncherProgress + ': %(bytes)s'
LauncherDownloadFilePercent = 'Downloading update for ' + LauncherProgress + ': %(percent)s%%'
LauncherDecompressingFile = 'Decompressing update for ' + LauncherProgress + '...'
LauncherDecompressingPercent = 'Decompressing update for ' + LauncherProgress + ': %(percent)s%%'
LauncherExtractingFile = 'Extracting update for ' + LauncherProgress + '...'
LauncherExtractingPercent = 'Extracting update for ' + LauncherProgress + ': %(percent)s%%'
LauncherPatchingFile = 'Applying update for ' + LauncherProgress + '...'
LauncherPatchingPercent = 'Applying update for ' + LauncherProgress + ': %(percent)s%%'
LauncherConnectProxyAttempt = 'Connecting to Pirates: %s (proxy: %s) attempt: %s'
LauncherConnectAttempt = 'Connecting to Pirates: %s attempt %s'
LauncherDownloadServerFileList = 'Updating Pirates...'
LauncherCreatingDownloadDb = 'Updating Pirates...'
LauncherDownloadClientFileList = 'Updating Pirates...'
LauncherFinishedDownloadDb = 'Updating Pirates... '
LauncherStartingGame = 'Starting Pirates...'
LauncherRecoverFiles = 'Updating Pirates. Recovering files...'
LauncherCheckUpdates = 'Checking for updates for ' + LauncherProgress
LauncherVerifyPhase = 'Updating Pirates...'
DownloadBlockerPanelTitle = 'Incomplete Download'
DownloadBlockerMsgGeneric = 'Sorry, your download is incomplete.\nPlease try again later.'
DownloadBlockerMsgIsland = 'Sorry, you may not leave the island until your download is complete.\nPlease try again later.'
DownloadBlockerMsgBoat = 'Sorry, you may not launch a ship until your download is complete.\nPlease try again later.'
DownloadBlockerMsgTeleport = 'Sorry, you may not teleport until your download is complete.\nPlease try again later.'
DownloadBlockerMsgLookout = 'Sorry, you may not use the Lookout until your download is complete.\nPlease try again later.'
CannotBoardProximityText = 'Download is incomplete, cannot board ship yet'
TeleportBlockerPanelTitle = 'Teleport Unavailable'
TeleportBlockerMsgBattle = "Sorry, you can't teleport while in battle."
TeleportBlockerMsgOnShip = "Sorry, you can't teleport while on a ship."
TeleportBlockerMsgOnAdventure = "Sorry, you can't teleport while on a high seas adventure."
TeleportBlockerMsgInPVP = "Sorry, you can't teleport while in PVP."
TeleportNotAvailable = 'Sorry, teleport is not allowed from here.'
NoTeleportInBattle = "Sorry, you can't teleport while in battle."
NoTeleportIslandToken = "Sorry, you don't have teleport access to that island yet."
NoTeleportOnShip = "Sorry, you can't teleport while on a ship."
NoTeleportInWater = "Sorry, you can't teleport while swimming."
NoTeleportInPVP = "Sorry, you can't teleport while in PVP."
NoTeleportInTutorial = "Sorry, you can't teleport yet."
NoTeleportCompass = "Sorry, you can't teleport until you have both your Cutlass and Compass."
NoTeleportVelvetRope = "Sorry, you can't teleport yet."
NoTeleportInTunnel = "Sorry, you can't teleport from here."
NoTeleportInTeleport = 'Sorry, you are already teleporting.'
NoTeleportInJail = "Sorry, you can't teleport from jail."
NoTeleportParlorGame = "Sorry, you can't teleport while playing a parlor game."
NoTeleportFlagshipBattle = "Sorry, you can't teleport while aboard an enemy flagship."
NoTeleportPhaseIncomplete = "Sorry, you can't teleport until your download is complete."
NoTeleportLookoutJoined = "Sorry, you can't teleport while waiting to enter a Lookout game."
NoTeleportSiegeCaptain = "Sorry, you can't teleport while captaining a privateer ship."
NoTeleportTreasureMap = TeleportNotAvailable
NoTeleportZombie = 'Cannot teleport while undead!'
TeleportPlayerNotAvailable = '%s is not available, try again later.'
NoTeleportToUnavailable = 'Sorry, %s is not available at the moment.'
NoTeleportToInPVP = 'Sorry, %s is in PVP at the moment.'
NoTeleportToInTutorial = 'Sorry, %s is still in the tutorial.'
NoTeleportToInTunnel = 'Sorry, %s is temporarily unavailable.'
NoTeleportToInTeleport = 'Sorry, %s is temporarily unavailable.'
NoTeleportToInJail = 'Sorry, %s is in jail.'
NoTeleportToNoPermission = "Sorry, %s is on a ship that\nyou don't have permission to board yet."
NoTeleportToFlagshipBattle = 'Sorry, %s is battling a flagship!'
NoTeleportToIgnore = 'Sorry, %s\\ is ignoring you.'
NoTeleportToNoSpaceOnShip = "Sorry, %s's ship is full at the moment."
NoTeleportToTreasureMap = TeleportPlayerNotAvailable
NoTeleportToWelcomeWorld = NoTeleportToInTutorial
NoTeleportToZombie = 'Sorry, %s is undead!'
CollectionRarities = {
    0: 'Common',
    1: 'Uncommon',
    2: 'Rare'}
CollectionPopupDuplicateText = '%s\nRarity: %s\nValue: %s'
CollectionPopupNewText = '%s \x01CPGreen\x01NEW!\x02\nRarity: %s\nValue: %s Gold'
Collections = {
    InventoryType.Collection_Set1: 'Valuables',
    InventoryType.Collection_Set1_Part1: 'Sapphire',
    InventoryType.Collection_Set1_Part2: 'Ruby',
    InventoryType.Collection_Set1_Part3: 'Gold Nugget',
    InventoryType.Collection_Set1_Part4: 'Silver Coin',
    InventoryType.Collection_Set1_Part5: 'Brass Locket',
    InventoryType.Collection_Set1_Part6: 'Small Diamond',
    InventoryType.Collection_Set1_Part7: 'Emerald',
    InventoryType.Collection_Set1_Part8: 'Crystal Vase',
    InventoryType.Collection_Set1_Part9: 'Sparkling Necklace',
    InventoryType.Collection_Set1_Part10: 'Copper Bits',
    InventoryType.Collection_Set1_Part11: 'Fire Opal',
    InventoryType.Collection_Set1_Part12: 'Gilded Anklet',
    InventoryType.Collection_Set1_Part13: 'Gold Cuff Links',
    InventoryType.Collection_Set1_Part14: 'White Gold Earring',
    InventoryType.Collection_Set1_Part15: 'Pearl Strand',
    InventoryType.Collection_Set1_Part16: 'Jade Toe Ring',
    InventoryType.Collection_Set1_Part17: 'Onyx Pendant',
    InventoryType.Collection_Set1_Part18: 'Turquoise Bangle',
    InventoryType.Collection_Set1_Part19: 'Amethyst',
    InventoryType.Collection_Set1_Part20: 'Topaz',
    InventoryType.Collection_Set2: 'Odds and Ends',
    InventoryType.Collection_Set2_Part1: 'Wood Carving',
    InventoryType.Collection_Set2_Part2: 'Flute',
    InventoryType.Collection_Set2_Part3: 'Silk Napkin',
    InventoryType.Collection_Set2_Part4: 'Cursed Idol',
    InventoryType.Collection_Set2_Part5: 'Shiny Rock',
    InventoryType.Collection_Set2_Part6: 'Gypsy Cloth',
    InventoryType.Collection_Set2_Part7: 'Shrunken Head',
    InventoryType.Collection_Set2_Part8: 'Glass Eye',
    InventoryType.Collection_Set2_Part9: 'Mouse Carving',
    InventoryType.Collection_Set2_Part10: 'Tiny Cage',
    InventoryType.Collection_Set2_Part11: 'Peacock Feather',
    InventoryType.Collection_Set2_Part12: 'Cricket in Amber',
    InventoryType.Collection_Set2_Part13: 'Protection Charm',
    InventoryType.Collection_Set2_Part14: 'Spices',
    InventoryType.Collection_Set2_Part15: 'Letter Opener',
    InventoryType.Collection_Set2_Part16: 'Navy Manacles',
    InventoryType.Collection_Set2_Part17: 'Glass Trinket',
    InventoryType.Collection_Set2_Part18: 'Sextant',
    InventoryType.Collection_Set2_Part19: 'Compass',
    InventoryType.Collection_Set2_Part20: 'Eerie Statue',
    InventoryType.Collection_Set3: 'The Nine Rogues',
    InventoryType.Collection_Set3_Part1: 'Captain Chevalle',
    InventoryType.Collection_Set3_Part2: 'Captain Barbossa',
    InventoryType.Collection_Set3_Part3: 'Mistress Ching',
    InventoryType.Collection_Set3_Part4: 'Captain Jack Sparrow',
    InventoryType.Collection_Set3_Part5: 'Gentleman Jocard',
    InventoryType.Collection_Set3_Part6: 'Sao Feng',
    InventoryType.Collection_Set3_Part7: 'Sri Sumhajee',
    InventoryType.Collection_Set3_Part8: 'Captain Ammand',
    InventoryType.Collection_Set3_Part9: 'Vallenueva',
    InventoryType.Collection_Set4: 'Navy Decorations',
    InventoryType.Collection_Set4_Part1: 'Valiant Cross',
    InventoryType.Collection_Set4_Part2: 'Conspicuous Attendance',
    InventoryType.Collection_Set4_Part3: 'Good Conduct Award',
    InventoryType.Collection_Set4_Part4: 'Distinguished Obedience Pin',
    InventoryType.Collection_Set4_Part5: 'Obsequious Order Badge',
    InventoryType.Collection_Set4_Part6: 'Illustrious Baton',
    InventoryType.Collection_Set4_Part7: 'Companion of Honor Medal',
    InventoryType.Collection_Set4_Part8: 'Sash of Pleasantry',
    InventoryType.Collection_Set4_Part9: 'Effort Ribbon',
    InventoryType.Collection_Set4_Part10: 'Pirate Slayer Mark',
    InventoryType.Collection_Set4_Part11: 'Royal Favor',
    InventoryType.Collection_Set4_Part12: 'Veteran Insignia',
    InventoryType.Collection_Set4_Part13: "Survivor's Medallion",
    InventoryType.Collection_Set4_Part14: 'Noteworthy Bravery Pin',
    InventoryType.Collection_Set5: "Rudyard's Teeth",
    InventoryType.Collection_Set5_Part1: 'Lateral Incisor',
    InventoryType.Collection_Set5_Part2: 'Central Incisor',
    InventoryType.Collection_Set5_Part3: 'Canine',
    InventoryType.Collection_Set5_Part4: 'Bicuspid',
    InventoryType.Collection_Set5_Part5: 'First Molar',
    InventoryType.Collection_Set5_Part6: 'Second Molar',
    InventoryType.Collection_Set5_Part7: 'Wisdom Tooth',
    InventoryType.Collection_Set6: 'Rhineworth Rings',
    InventoryType.Collection_Set6_Part1: 'Left Pinkie',
    InventoryType.Collection_Set6_Part2: 'Left Ring Finger',
    InventoryType.Collection_Set6_Part3: 'Left Middle Finger',
    InventoryType.Collection_Set6_Part4: 'Left Index Finger',
    InventoryType.Collection_Set6_Part5: 'Left Thumb',
    InventoryType.Collection_Set6_Part6: 'Right Thumb',
    InventoryType.Collection_Set6_Part7: 'Right Index Finger',
    InventoryType.Collection_Set6_Part8: 'Right Middle Finger',
    InventoryType.Collection_Set6_Part9: 'Right Ring Finger',
    InventoryType.Collection_Set6_Part10: 'Right Pinkie',
    InventoryType.Collection_Set6_Part11: 'Extra Digit',
    InventoryType.Collection_Set7: 'Treasure Chess',
    InventoryType.Collection_Set7_Part1: 'Silver Pawn',
    InventoryType.Collection_Set7_Part2: 'Silver Knight',
    InventoryType.Collection_Set7_Part3: 'Silver Bishop',
    InventoryType.Collection_Set7_Part4: 'Silver Rook',
    InventoryType.Collection_Set7_Part5: 'Silver Queen',
    InventoryType.Collection_Set7_Part6: 'Silver King',
    InventoryType.Collection_Set7_Part7: 'Gold Pawn',
    InventoryType.Collection_Set7_Part8: 'Gold Knight',
    InventoryType.Collection_Set7_Part9: 'Gold Bishop',
    InventoryType.Collection_Set7_Part10: 'Gold Rook',
    InventoryType.Collection_Set7_Part11: 'Gold Queen',
    InventoryType.Collection_Set7_Part12: 'Gold King',
    InventoryType.Collection_Set8: "Tia Dalma's Menagerie",
    InventoryType.Collection_Set8_Part1: 'Alligator Figure',
    InventoryType.Collection_Set8_Part2: 'Wasp Figure',
    InventoryType.Collection_Set8_Part3: 'Stump Figure',
    InventoryType.Collection_Set8_Part4: 'Fly Trap Figure',
    InventoryType.Collection_Set8_Part5: 'Scorpion Figure',
    InventoryType.Collection_Set8_Part6: 'Vampire Bat Figure',
    InventoryType.Collection_Set8_Part7: 'Rock Crab Figure',
    InventoryType.Collection_Set8_Part8: 'Fly Figure',
    InventoryType.Collection_Set8_Part9: 'Jaguar Figure',
    InventoryType.Collection_Set8_Part10: 'Shark Figure',
    InventoryType.Collection_Set8_Part11: 'Snake Figure',
    InventoryType.Collection_Set8_Part12: 'Wolf Figure',
    InventoryType.Collection_Set8_Part13: 'Cockroach Figure',
    InventoryType.Collection_Set8_Part14: 'Monkey Figure',
    InventoryType.Collection_Set8_Part15: 'Crow Figure',
    InventoryType.Collection_Set9: 'Cannons of the Deep',
    InventoryType.Collection_Set9_Part1: 'Broken Ramrod',
    InventoryType.Collection_Set9_Part2: 'Cannon Flint',
    InventoryType.Collection_Set9_Part3: 'Cannon Ring',
    InventoryType.Collection_Set9_Part4: 'Cannon Wheel',
    InventoryType.Collection_Set9_Part5: 'Dented Cannonball',
    InventoryType.Collection_Set9_Part6: 'Gunpowder Flask',
    InventoryType.Collection_Set9_Part7: 'Ignitor',
    InventoryType.Collection_Set9_Part8: 'Quoin',
    InventoryType.Collection_Set9_Part9: 'Recoil Rope',
    InventoryType.Collection_Set9_Part10: 'Sighting Scope',
    InventoryType.Collection_Set9_Part11: 'Silk Swab',
    InventoryType.Collection_Set9_Part12: 'Silver Ramrod'}
ChatPanelReputationMsg = 'Earned %s %s reputation point.'
ChatPanelReputationMsgPlural = 'Earned %s %s reputation points.'
ChatPanelRepFreeMsg = 'Earned %s %s reputation points. (reduced by %s)'
ChatPanelLevelUpMsg = 'Level Up! %s Level %s'
ChatPanelQuestCompletedMsg = 'Quest Completed'
ChatPanelQuestUpdatedMsg = 'Quest Updated'
ChatPanelQuestAddedMsg = 'New Quest Added'
Loading = 'Loading...'
GuildRankMember = '\x01slant\x01Member\x02'
GuildRankLeader = '\x01slant\x01Guildmaster\x02'
GuildRankSubLead = '\x01slant\x01Officer\x02'
GameOptionsTitle = 'Game Options'
GameOptionsCustom = 'Custom'
GameOptionsVolume = 'Volume'
GameOptionsTextureCompressed = 'Compressed Texture'
GameOptionsAggressiveMemory = 'Aggressive Memory Conservation'
GameOptionsRenderedShadows = 'Rendered Shadows'
GameOptionsHardwareGamma = 'Hardware Gamma'
GameOptionsIntensity = 'Intensity'
GameOptionsVideo = 'Video'
GameOptionsDefaultConfirm = 'Are you sure you want the default settings?'
GameOptionsRestoreConfirm = 'Are you sure you want to restore the last settings?'
GameOptionDisplay = 'Display'
GameOptionsGraphics = 'Graphics'
GameOptionsGeometry = 'Geometry'
GameOptionsAudio = 'Audio'
GameOptionsInterface = 'Interface'
GameOptionsImage = 'Image'
GameOptionsKeys = 'Controls'
GameOptionsFullscreenOnOff = 'Fullscreen On/Off'
GameOptionsWindowedResolutions = 'Windowed Resolutions'
GameOptionsFullscreenResolutions = 'Fullscreen Resolutions'
GameOptions640x480 = '640x480'
GameOptions800x600 = '800x600'
GameOptions1024x768 = '1024x768'
GameOptions1280x1024 = '1280x1024'
GameOptions1600x1200 = '1600x1200'
GameOptions1280x720 = '1280x720'
GameOptions1920x1080 = '1920x1080'
GameOptionsWidescreen = 'Widescreen'
GameOptionsFullscreen = 'Fullscreen'
GameOptionsReflections = 'Reflections'
GameOptionsSkyOnly = 'Sky Only'
GameOptionsAll = 'All'
GameOptionsShaderLevel = 'Shader Level'
GameOptionsRestartRequired = '* = Application restart is required for change to take effect.'
GameOptionsNoShader = 'Shader (Minimum Required Shader Hardware Not Detected)'
GameOptionsShadows = 'Shadows'
GameOptionsSimple = 'Simple'
GameOptionsRendered = 'Rendered'
GameOptionsAntialiasing = 'Antialiasing'
GameOptionsVSync = 'VSync'
GameOptionsFrameRate = 'Frame Rate Meter'
GameOptionsSpecialEffectsLevel = 'Special Effects Level'
GameOptionsTextureDetailLevel = 'Texture Detail Level *'
GameOptionsLow = 'Low'
GameOptionsMedium = 'Medium'
GameOptionsHigh = 'High'
GameOptionsMaximum = 'Maximum'
GameOptionsCompressed = 'Compressed'
GameOptionsAggressive = 'Aggressive'
GameOptionsCharacterDetailLevel = 'Character Detail Level'
GameOptionsTerrainDetailLevel = 'Terrain Detail Level'
GameOptionsMemory = 'Memory Conservation'
GameOptionsShipVis = 'Ship Visibility from Islands'
GameOptionsShipVisOff = 'Off'
GameOptionsShipVisLow = 'Low'
GameOptionsShipVisHigh = 'High'
GameOptionsSoundEffects = 'Sound Effects'
GameOptionsSoundEffectsVolume = 'Sound Effects Volume'
GameOptionsMusic = 'Music'
GameOptionsMusicVolume = 'Music Volume'
GameOptionsInvertMouseLook = 'Invert Mouse Look'
GameOptionsGUIScale = 'Interface Scale'
GameOptionsCpuFrequencyWarning = 'Cpu Frequency Warning'
GameOptionsEnableGamma = 'Enable Hardware Gamma'
GameOptionsGamma = 'Gamma'
GameOptionsHdr = 'High Dynamic Range (Requires Shader On) *'
GameOptionsHdrIntensity = 'High Dynamic Range Intensity'
GameOptionsLogout = 'Logout'
GameOptionsDefault = 'Default'
GameOptionsOptions = 'Options'
GameOptionsRestore = 'Restore'
GameOptionsSave = 'Save'
GameOptionsClose = 'Close'
GameOptionsOn = 'On'
GameOptionsOff = 'Off'
GameOptionsLogoutConfirm = 'Are you sure you want to logout?'
GameOptionsApplicationRestartMessage = 'For this option to take effect you must save the game options and restart application.'
GameOptionsSaved = 'Game Options Saved'
GameOptionsFailedToSaveOptions = 'Failed to Save Game Options'
GameOptionsOnLowerFrameRate = 'Turning this option on may result in a lower frame rate.'
TableLeave = 'Leave'
TableCancel = 'Cancel'
TableIsFullMessage = "You can't sit at this table since it is full."
TableWinGold = 'You won %s gold!'
TableCardsHelp = 'Cards can be obtained from quests.  To swap a card, first select which card to swap.  Then select a card suit.  Lastly select a card rank.'
Card2 = '2'
Card3 = '3'
Card4 = '4'
Card5 = '5'
Card6 = '6'
Card7 = '7'
Card8 = '8'
Card9 = '9'
CardT = 'T'
CardJ = 'J'
CardQ = 'Q'
CardK = 'K'
CardA = 'A'
PokerBet = 'Bet'
PokerCall = 'Call'
PokerCheat1 = 'Swap 1st\nCard'
PokerCheat2 = 'Swap 2nd\nCard'
PokerCheck = 'Check'
PokerFold = 'Fold'
PokerRaise = 'Raise'
PokerAllIn = 'All-In'
PokerBetAmount = 'Bet %s'
PokerCallAmount = 'Call %s'
PokerRaiseAmount = 'Raise to %s'
PokerBigBlindAmount = 'Big Blind %s'
PokerSmallBlindAmount = 'Small Blind %s'
PokerAllInAmount = 'All-In %s'
PokerPotZero = 'Pot: 0'
PokerPotAmount = 'Pot: %s'
PokerWaitingForOtherPlayers = 'Waiting for other players ...'
PokerWaitingForNextGame = 'Waiting for next hand ...'
PokerOutOfChipsMessage = 'You have run out of gold.'
PokerCaughtCheatingMessage = 'The dealer inspects the cards and you have been caught cheating!  You have been fined %s gold.'
PokerInsufficientChipsMessage = "You don't have enough gold to sit at this table.  The minimum gold required to sit at this table is %s."
PokerSwapConfirmMessage = 'Are you sure you want to swap the %s with the %s?'
PokerLeaveConfirmMessage = 'Are you sure you want to leave the table?  If you leave, then any hand in play will be automatically folded.'
PokerSwapSuccessMessage = 'Card swap attempt succeeded!'
PokerSwapFailureMessage = 'Card swap attempt failed.'
PokerChatWinGoldMessage = '%s wins %s gold.'
PokerChatCaughtCheatingMessage = '%s has been caught cheating!'
PokerSitDownPoker = 'Poker'
PokerSitDownHoldEmPoker = "Tortuga Hold'em Poker"
PokerSitDown7StudPoker = '7 Stud Poker'
PokerYouLost = 'You Lost'
VR_Head_StayTuned1 = 'Stay tuned for the next Pirates of the Caribbean Online Expansion!'
VR_Head_StayTuned2 = 'Stay tuned for the next Pirates of the Caribbean Online Expansion!'
VR_UpgradeNow = '\x01smallCaps\x01Upgrade Now!\x02'
VR_UpgradeLater = '\x01smallCaps\x01Continue Playing\x02'
VR_DismissNow = 'Upgrade Later'
VR_Head_Combat = 'Upgrade your account to continue this quest!'
VR_Head_Quest = 'Upgrade your account to take part in this quest!'
VR_Head_Trial = 'Your 7-Day Full-Screen Preview Has Expired'
VR_Head_Guild = 'Upgrade your account to create your own Pirate Guild!'
VR_Head_Island = 'Upgrade your account to gain access to this high-level area!'
VR_Head_Ship = 'Upgrade your account to gain access to additional ships!'
VR_Head_Account = 'Upgrade your account to create more Pirates!'
VR_Head_Weapon = 'Upgrade your account to gain access to additional weapons and skills!'
VR_Head_PVP = 'Upgrade your account to gain access to additional PVP maps and game types!'
VR_Head_Parlor = 'Upgrade your account to gain access to additional parlor games!'
VR_Head_Treasure = 'Upgrade your account to complete this treasure collection!'
VR_Head_Customize = 'Upgrade your account to customize your Pirate with exclusive items!'
VR_StayTuned1 = '-  Coming soon: More fabulous places to explore\n-  More pirate adventures with Jack and friends\n-  Fiendish foes to test your mettle'
VR_StayTuned2 = '-  Coming soon: More fabulous places to explore\n-  More pirate adventures with Jack and friends\n-  Fiendish foes to test your mettle'
VR_Access = '\x01uline\x01Experience Unlimited Access - Click here for details\x02'
VRCustomizeBlurb = 'Customize your Pirates with exclusive clothing, jewelry, and tattoos'
VR_Combat = "You'll also gain access to these exclusive game features:\n   -  Unlock advanced weapons and skills\n   -  " + VRCustomizeBlurb + '\n   -  Captain bigger and better ships...and more!'
VR_Quest = "You'll also gain access to these exclusive game features:\n   -  " + VRCustomizeBlurb + '\n   -  Unlock advanced weapons and skills\n   -  Captain bigger and better ships... and more!'
VR_Trial = 'You can continue to play in windowed mode with free Basic Access or you can upgrade to Unlimited Access for expanded features including full-screen game play.'
VR_Guild = "You'll also gain access to these exclusive game features:\n   -  Unlock advanced weapons and skills\n   -  Captain bigger and better ships\n   -  " + VRCustomizeBlurb
VR_Island = "You'll also gain access to these exclusive game features:\n   -  Unlock advanced weapons and skills\n   -  Embark on expanded quests\n   -  " + VRCustomizeBlurb
VR_Ship = "You'll also gain access to these exclusive game features:\n   -  Unlock more powerful weapons and skills\n   -  Engage in expanded pirate-versus-pirate combat\n   -  " + VRCustomizeBlurb
VR_Account = "You'll also gain access to these exclusive game features:\n   -  " + VRCustomizeBlurb + '\n   -  Unlock advanced weapons and skills\n   -  Captain bigger and better ships....and more!'
VR_Weapon = "You'll also gain access to these exclusive game features:\n   -  Captain bigger and better ships\n   -  " + VRCustomizeBlurb + '\n   -  Engage in expanded pirate-versus-pirate combat... and more!'
VR_PVP = "You'll also gain access to these exclusive game features:\n   -  Unlock more powerful weapons and skills\n   -  Create and lead your own powerful Pirate guild\n   -  Captain bigger and better ships... and more!"
VR_Parlor = "You'll also gain access to these exclusive game features:\n   -  Unlock more powerful weapons and skills\n   -  Captain bigger and better ships\n   -  " + VRCustomizeBlurb
VR_Treasure = "You'll also gain access to these exclusive game features:\n   -  Embark on expanded quests\n   -  " + VRCustomizeBlurb + '\n   -  Captain bigger and better ships... and more!'
VR_Customize = "You'll also gain access to these exclusive game features:\n   -  Unlock advanced weapons and skills\n   -  Captain bigger and better ships\n   -  Create and lead your own Pirate Guild... and more!"
VR_Cap_StayTuned1 = 'Next Expansion in the Works'
VR_Cap_StayTuned2 = 'More Pirate Adventures'
VR_Cap_Parlor1 = 'Play a variety of games'
VR_Cap_Parlor2 = 'Enjoy members-only games'
VR_Cap_Combat1 = 'Retake the Pearl'
VR_Cap_Combat2 = 'Grab the Horizon'
VR_Cap_Trial1 = 'Live the adventure!'
VR_Cap_Trial2 = 'More pirate loot awaits!'
VR_Cap_Quest1 = 'Extend your adventure'
VR_Cap_Quest2 = 'Fully level up your character'
VR_Cap_Ship1 = 'Captain more powerful ships'
VR_Cap_Ship2 = 'Become a legend of the seas'
VR_Cap_Weapon1 = 'Master advanced weapons'
VR_Cap_Weapon2 = 'More powerful ammo and skills'
VR_Cap_Account1 = 'Unleash more characters'
VR_Cap_Account2 = 'Create a variety of Pirates'
VR_Cap_Treasure1 = 'Discover more treasure'
VR_Cap_Treasure2 = 'Complete your collection'
VR_Cap_Guild1 = 'Build a powerful Guild'
VR_Cap_Guild2 = 'Lead them into battle'
VR_Cap_Island1 = 'Explore the dangerous island of Kingshead'
VR_Cap_Island2 = 'Defeat high level Navy Officers'
VR_Cap_PVP1 = 'More PVP Maps'
VR_Cap_PVP2 = 'More PVP Games'
VR_Cap_Customize1 = 'More clothing & unique items'
VR_Cap_Customize2 = 'Stand out from the crowd'
VR_FeaturePopTitle = 'Sorry Mate...'
VR_FeaturePopLongText = 'This feature requires Unlimited Access Membership.\nJoin the crew of advanced players to experience\nall the Caribbean has to offer.'
VR_AuthAccess = '\x01smallCaps\x01Unlimited Access Members Only\x02'
VR_StayTuned = 'Stay Tuned for More Adventures'
VR_MemberOnly = 'This feature is for Unlimited Access Members only!'
VR_LongText = "Unlock the full Pirate adventure waiting for you now!  See what additional help Jack and his friends need!  Can you survive Davy Jones' wrath?  Learn new skills and new weapons!  Gain full mastery of the skills you currently possess.  Open new PVP and Parlor gaming modes!"
TableIsFullMessage = "You can't sit at this table since it is full."
BlackjackHand = 'Blackjack'
BlackjackStay = 'Stay'
BlackjackHit = 'Hit'
BlackjackBid = 'Bid'
BlackjackDoubleDown = 'Double\nDown'
BlackjackSplit = 'Split'
BlackjackCardSwap = 'Swap\nCard'
BlackjackHandofHand = 'Hand %s of %s'
BlackjackBusted = 'Busted  %s'
BlackjackSitDownBlackjack = 'Blackjack'
BlackjackDealerWins = 'Dealer Wins'
ComboOrderWarn = 'Combo skills must be unlocked in order.'
TutorialSweepWarn = 'You must unlock Sweep on Cutlass upgrade.'
noFreebooterCap = 'Unlimited Access Only'
FreebooterSkillLock = '\x01Ired\x01Basic Members may spend only 6 skill points per category.\x02'
FreebooterSkillMax = '\x01Ired\x01Basic Members may raise skills to no more than rank 2.\x02'
FreebooterDisallow = '\x01Ired\x01Locked for Basic Members\x02'
Freebooter = 'Basic Member'
GuildPrefix = '(G):'
CrewPrefix = '(C):'
PVPPrefix = '(P):'
PVPSpanish = '(Spanish):'
PVPFrench = '(French):'
LocationNames = {
    '1150922126.8dzlu': 'Port Royal',
    '1155695180.13sdnaik': 'Port Royal Town',
    '1161798288.34sdnaik': "King's Run",
    '1164141722.61sdnaik': 'Wicked Thicket',
    '1164952144.06sdnaik': 'Royal Caverns',
    '1165001772.05sdnaik': 'Murky Hollow',
    '1169592956.59sdnaik': "Governor's Garden",
    '1175621632.0dxschafe0': 'Fort Charles',
    '1153420207.67dzlu0': 'June Greer Residence',
    '1155773612.45fxlara0': "Smitty's Jewelry Shoppe",
    '1168033330.17kmuller0': "Governor's Mansion",
    '1153419689.81dzlu0': 'Rowdy Rooster',
    '1153419634.08dzlu0': 'Royal Anchor',
    '1155684634.87dzlu0': 'Graham Marsh Imports',
    '1155774289.03fxlara0': "Ewan's Gunnery",
    '1159905354.84jubutler': 'Old Warehouse',
    '1155244887.43dzlu0': 'R. Smith, Pewterer',
    '1155767402.81fxlara0': 'Tattoo Parlor',
    '1153419342.98dzlu0': "Basil's Barbershop",
    '1153419460.35dzlu0': "Blakeley's residence",
    '1153420657.11dzlu0': "Turnbull's Weaponry",
    '1153420647.55dzlu0': "Fuller's Blacksmithing",
    '1153423464.2dzlu0': 'Wallace Blacksmith Shop',
    '1153417506.13dzlu0': "Truehound's Tailor Shop",
    '1156207188.95dzlu': 'Tortuga',
    '1158295517.91sdnaik': 'Tortuga Town',
    '1165004570.58sdnaik': 'Tortuga Graveyard',
    '1158121765.09sdnaik': 'Thieves Den',
    '1165009873.53sdnaik': 'Wildwoods',
    '1169179552.88sdnaik': 'Misty Mire',
    '1165009856.72sdnaik': "Rat's Nest",
    '1156207773.33dzlu0': 'Faithful Bride',
    '1156279370.48dzlu0': "King's Arm",
    '1156207578.91dzlu0': 'Bowdash Mansion',
    '1156371286.47dzlu0': "Orinda's Shack",
    '1156207523.59dzlu0': 'Flatts & Flatts, Importers',
    '1156277937.59dzlu0': "Millie's Cottage",
    '1156270974.95dzlu0': "Seamstress Anne's Shop",
    '1156207423.67dzlu0': "Doctor Grog's",
    '1156279185.81dzlu0': "Flinty's Smithery",
    '1156267951.67dzlu0': 'Trading Co.',
    '1156269565.62dzlu0': "Wright's Blacksmithing",
    '1156207603.55dzlu0': "Boatswain's house",
    '1156267902.64dzlu0': 'Thayers Weapons Shop',
    '1156279255.42dzlu0': 'Daniel Vallance Weaponry',
    '1156268617.43dzlu0': "Callecutter's Tailor Shoppe",
    '1156270917.73dzlu0': "Lockspinner's Barber and Beauty Shop",
    '1156279216.23dzlu0': "Ming's Jewelry Shop",
    '1156279496.29dzlu0': "Bonita's Tattoo Parlor",
    '1142018473.22dxschafe': 'Padres Del Fuego',
    '1156207578.91dzlu': 'Home of Bowdash',
    '1167862588.52sdnaik': "Beckett's Quarry",
    '1168057131.73sdnaik': 'The Catacombs',
    '1164929110.98sdnaik': 'Lava Gorge',
    '1167857698.16sdnaik': 'El Sudoron',
    '1175825280.0dxschafe': 'Fort Dundee',
    '1153435103.16dzlu0': "Skull's Thunder",
    '1153434762.53dzlu0': 'Ratskellar',
    '1153434928.03dzlu0': "Ferrera's Blacksmith Shop",
    '1153436073.35dzlu0': 'Grimsditch Gunsmithing',
    '1153437552.45dzlu0': "Deaf Gunny's Weapons shop",
    '1153778118.18dzlu0': "Powder-Burnt Pete's Weaponry",
    '1153435428.14dzlu0': 'Anton Levy Smithery',
    '1153778153.99dzlu0': 'Thorhammer Blacksmithing',
    '1153434880.63dzlu0': 'Corazon Tattoos',
    '1175729664.0dxschafe0': "Gunner's shack",
    '1153507305.2dzlu0': "Garrett's Imports and Exports",
    '1153436381.55dzlu0': 'Dolores Tailoring Shoppe',
    '1153435388.6dzlu0': "Perla's Jewelry and Gems",
    '1153430887.13dzlu0': "Cesar's Barbershop",
    '1153777945.95dzlu0': "Flavio's Barbershop",
    '1153778017.46dzlu0': "Blanca's Tailor Shop",
    '1153778094.12dzlu0': "Fousto's Jewelry Shop",
    '1190672768.0dxschafe1': "Nina's Tattoo Parlor",
    '1164135492.81dzlu': "Devil's Anvil",
    '1172209006.11sdnaik': "Barbossa's Grotto",
    '1164763706.66sdnaik': 'Driftwood Island',
    '1161282725.84kmuller': "Rumrunner's Isle",
    '1164157132.99dzlu': 'Isla Perdida',
    '1172209955.25sdnaik': "Queen's Nest",
    '1173381952.2sdnaik': 'Outcast Isle',
    '1160614528.73sdnaik': 'Cuba',
    '1161732578.06sdnaik': 'Pantano River',
    '1190741504.0dxschafe0': 'La Bodeguita',
    '1171316864.0dxschafe2': "Daggerflint's Tattoo Shop",
    '1171316864.0dxschafe0': "Pugpratt's Tailoring",
    '1159933206.48sdnaik': 'Kingshead',
    '1190336896.0dxschafe': 'Kingshead Depot',
    '1190397568.0dxschafe0': 'Kingshead Armory',
    '1190397824.0dxschafe': 'Marching Grounds',
    '1190397568.0dxschafe': 'Kingshead Barracks',
    '1190397568.0dxschafe1': 'Kingshead Keep',
    '1156359855.24bbathen': 'Isla Cangrejos',
    '1164150392.42dzlu': 'Isla Tormenta',
    '1172208344.92sdnaik': 'Tormenta Cave',
    '1173382404.64sdnaik': 'Cutthroat Isle',
    '1167857698.16naiksd': 'Cutthroat Jungle',
    '1171761224.13sdnaik': 'Black Pearl Bay',
    '1161805620.28Shochet': 'Parlor Games',
    '1161805620.28Shochet0': 'Underground Parlor Games',
    'AllOfPortRoyal': 'Port Royal',
    'AllOfTortuga': 'Tortuga',
    'AllOfPadresDelFuego': 'Padres Del Fuego',
    'AllOfDevilsAnvil': "Devil's Anvil",
    'AllOfDriftwood': 'Driftwood Island',
    'AllOfRumrunners': "Rumrunner's Isle",
    'AllOfPerdida': 'Isla Perdida',
    'AllOfOutcast': 'Outcast Isle',
    'AllOfCuba': 'Cuba',
    'AllOfKingshead': 'Kingshead',
    'AllOfCangrejos': 'Isla Cangrejos',
    'AllOfCutthroat': 'Cutthroat Isle',
    'AllOfTormenta': 'Isla Tormenta',
    'AnyLargeIsland': 'Any Large Island',
    'AnyLargePort': 'Any Large Island',
    'AnyWildIsland': 'Any Wild Island',
    'AnyWildPort': 'Any Wild Island',
    'AnyLocation': 'Anywhere',
    'Windward_Passage': 'Windward Passage',
    'Brigand_Bay': 'Brigand Bay',
    'Bloody_Bayou': 'Bloody Bayou',
    'Scurvy_Shallows': 'Scurvy Shallows',
    'Blackheart_Strait': 'Blackheart Strait',
    'Salty_Flats': 'Salty Flats',
    'Mar_de_Plata': 'Mar de Plata',
    'Smugglers_Run': 'Smugglers Run',
    'The_Hinterseas': 'The Hinterseas',
    'Dead_Mans_Trough': "Dead Man's Trough",
    'Leeward_Passage': 'Leeward Passage',
    'Boiling_Bay': 'Boiling Bay',
    'Mariners_Reef': 'Mariners Reef',
    'Uncharted_Waters': 'Uncharted Waters',
    '1175562995.67zpavlov': 'Molten Cavern',
    '1170793088.0jubutler': 'Boulder Hill',
    '1170793088.0jubutler': 'Pillagers Pass',
    '1196970035.53sdnaik': 'Isla de la Avaricia',
    '1196970080.56sdnaik': "Ile d'Etable de Porc",
    '1202846053.19akelts0': "Porc's Tavern",
    '1204237124.2akelts0': "Avaricia's Tavern"}
UNDEAD_SPANISH_NAMES = ('Undead Spanish Soldier', 'Undead Spanish Soldiers')
UNDEAD_FRENCH_NAMES = ('Undead French Soldier', 'Undead French Soldiers')
LoadingScreen_Jail = 'Jail'
LoadingScreen_Ocean = 'The High Seas'
LoadingScreen_Hint = 'Hint'
GeneralTip1 = 'Plunder ships for Cargo in order to quickly get Gold!'
GeneralTip2 = 'Defeat skeletons to find rare Treasure Collection valuables.'
GeneralTip3 = 'Going to jail makes you groggy. While groggy, your Health and Voodoo Power will be temporarily reduced.'
GeneralTip4 = 'Use the Map Page (M) to change Servers!'
GeneralTip5 = 'Players cannot hurt each other except in PvP Matches!'
GeneralTip6 = "If you are alone, don't fight too many enemies at once!"
ControlTip1 = 'You can use the WASD Keys to move.'
ControlTip2 = 'Press the Space Bar to jump.'
ControlTip3 = 'Use the Left Mouse Button or the CTRL Button to attack.'
ControlTip4 = 'Use the Right Mouse Button to move the Camera.'
ControlTip5 = 'Press R to enable Auto-run!'
ControlTip6 = 'While using Auto-run (R), you can run and chat at the same time!'
ControlTip7 = 'Press F1 to draw your Cutlass!'
ControlTip8 = 'Press F2 to draw your Pistol!'
ControlTip9 = 'To steer a Ship, grab the Steering Wheel!'
ControlTip10 = "To fire a Ship's Broadsides, grab the Steering Wheel!"
ControlTip11 = 'Crew Members on a Ship should grab a cannon and fire!'
ControlTip12 = 'Sail near an Island and click on the Anchor Button to dock!'
OptimizeTip1 = 'If the game is running slowly, you can lower your graphics settings by pressing F7!'
TonicTip1 = 'You can buy health Tonics from the Gypsy!'
TonicTip2 = 'When you are low on health, Hit T to use a Tonic!'
TonicTip3 = 'Purchase the weaker healing Tonics until you are Level 10 or higher.'
QuestTip1 = 'Look for a Ray of Light if you get lost.'
QuestTip2 = 'Use the Journal (J) to find your next quest objective.'
QuestTip3 = "If you're not sure where to go for a Quest, search the skies for the Ray of Light."
QuestTip4 = 'If you get lost, teleport back to your Port of Call using the Map Page (M)!'
QuestTip5 = 'To navigate the map on the Map Page (M), click and drag it with the Left Mouse Button.'
QuestTip6 = 'Completing Story Quests rewards the most Notoriety!'
QuestTip7 = 'Complete the Teleport Quests as soon as possible. It will make other quests easier to complete.'
QuestTip8 = 'Complete your Weapon Quest to unlock the Voodoo Doll weapon!'
ShipTip0 = 'Maneuver your ship so that your broadside cannons line up with the enemy before firing!'
ShipTip1 = 'Repair a sunken ship at the Shipwright!'
ShipTip2 = 'While sailing, hold down the Right Mouse Button to move the Camera.'
ShipTip3 = 'Find a Crew to help man your ship before going sailing!'
ShipTip4 = "Don't sail alone! Other crewmates can fire cannons while you are steering!"
ShipTip5 = 'When sailing, use the Middle Mouse Wheel to move the Camera in and out!'
ShipTip6 = 'A ship cannot be reduced to zero Sail Points without destroying all the Masts!'
ShipTip7 = "Concentrate your cannon fire on the same section of a ship's Hull until it breaks!"
ShipTip8 = "Shooting a ship's sails will not sink it, but can slow it down!"
ShipTip9 = 'Sailing in a straight line allows your ship to move faster!'
ShipTip10 = 'Higher level ships carry better Cargo.'
ShipTip11 = 'Ships cost more to repair after they are sunk!'
ShipTip12 = 'Cannonballs that hit the Rear of a Ship gain a damage bonus!'
ShipTip13 = 'Sink ships with Cannons to become a better Cannoneer!'
ShipTip14 = 'Sink ships with Broadsides to gain Sailing Reputation!'
ShipTip15 = 'Level-up your Cannon Skill to unlock new Cannon Ammo types!'
ShipTip16 = 'Level-up your Sailing Skill to unlock new Ship Maneuvers and Battle Orders!'
ShipTip17 = 'Different cannonballs are effective against different parts of a ship!'
ShipTip18 = 'Break all the Masts on an enemy ship to stop it from moving!'
ShipTip19 = 'If a player exits the game and his ship has a Crew, the ship stays in use until the voyage ends!'
ShipTip20 = 'If your ship sinks at sea, all your cargo is lost!'
ShipTip21 = 'To sink a ship, aim for the Hull!'
ShipTip22 = 'Expensive ships cost more to repair!'
ShipTip23 = 'If you shoot the same part of a ship, the panel will break, catch fire, and give a damage bonus!'
ShipTip24 = "If one side of a ship's hull is broken, the ship will take extra damage on that side!"
ShipTip25 = "If one side of your ship's hull is broken, avoid taking more fire on that side!"
ShipTip26 = 'Be careful not to take too much damage on the same section of your hull!'
ShipTip27 = "Use the Boarding Access button on your Ship's Health Display to control who can board your ship!"
ShipTip28 = "Looking to join a ship's crew? Use a Dinghy and search for Public Ships!"
ShipTip29 = 'Looking for a crew for your ship? Set the Boarding Access for your ship to Public!'
FlagShipTip1 = 'Ships with a Flag Icon above them are Flagships. They need to be crippled and then boarded!'
FlagShipTip2 = 'Get a crew together before boarding a Flagship!'
FlagShipTip3 = 'Flagship boarding rights are given to the crew who dealt the most damage to it!'
FlagShipTip4 = 'Flagships give more cargo than regular ships!'
FriendTip1 = 'Click on other players to Crew up! Make sure you put away your weapon first!'
FriendTip2 = "You can board a Crew Member's ship from the Dinghy!"
FriendTip3 = 'Rule #1 of the pirate code: Befriend others wisely!'
FriendTip4 = 'Click on other players to make Friends! Make sure you put away your weapon first!'
FriendTip5 = 'Team up with other players against tough enemies!'
FriendTip6 = 'If a friend is in need, teleport to them using the Friends Page (F)!'
ChatTip1 = "If you type a '.' in the chat window before typing, the message will appear as a thought bubble and will stay longer."
TreadmillTip1 = 'Spend skill upgrades wisely. It will cost gold to change your choices later!'
TreadmillTip2 = 'Visit a Trainer at the local blacksmith to retrain your weapons. \n Retraining a weapon refunds all your spent skill points.'
TreadmillTip3 = 'Spending a Skill Point on an attack skill increases its damage 25%!'
TreadmillTip4 = 'Spending a Skill Point on an attack skill increases any Buff duration by 25%!'
TreadmillTip5 = 'Enemies who are lower level than you award less Reputation and Gold!'
TreadmillTip6 = 'Members of a Crew gain a Reputation Bonus for every enemy defeated.  Larger crews provide larger bonuses!'
TreadmillTip7 = 'The Captain of a ship receives a larger share of loot if he has a Crew onboard!'
TreadmillTip8 = 'The pirate steering the ship gains more Sailing Reputation if the ship has a Crew!'
TreadmillTip9 = 'As you Level-up your Cutlass, unlock new Combo Skills for a longer Combo Chain!'
TreadmillTip10 = 'As you Level-up your Pistol, unlock Take-Aim to pick-off enemies from long range!'
CombatTip1 = 'If you are not in battle, your Health will regenerate slowly. \n Avoid fighting until you are fully healed.'
CombatTip2 = 'A Cutlass Combo deals much more damage than just button-mashing!'
CombatTip3 = 'You can aim your attacks by holding down the Right Mouse Button!'
CombatTip4 = 'Watch your Cutlass attack timing to form Combos!'
CombatTip5 = "Don't attack enemies who are much higher level than you!"
CombatTip6 = "You're vulnerable to attack while you dig for buried treasure, so stay alert."
CombatTip7 = 'Switch Weapons using the F1 to F6 Keys!'
CombatTip8 = 'You can also use the Mouse Wheel to Switch Weapons!'
CombatTip9 = 'Clicking the Middle Mouse Button also draws your current Weapon!'
CombatTip10 = 'You can use the Number Keys to activate your Combat Skills or Switch Ammo!'
CombatTip11 = 'The Voodoo Doll will lose Attunement if you get too far away from your target!'
CombatTip12 = 'Voodoo Doll healers gain healing Reputation when their ally defeats their foe!'
CombatTip13 = 'You can Unattune a target with the Voodoo Doll by clicking on the Unattune Menu on the right!'
CombatTip14 = 'Upgrade the Attune Doll skill to be able to Attune the Voodoo Doll to multiple targets!'
CombatTip15 = 'Attacking an enemy in the back with a Dagger Combo will deal extra damage!'
CombatTip16 = "The Dagger's Asp skill can be used to break an enemy's Voodoo Doll Attunement!"
StoreTip1 = 'You can buy new weapons and ammunition from Stores!'
StoreTip2 = 'You can purchase Cannon and Pistol Ammo from the Gunsmith!'
StoreTip3 = 'You can purchase Throwing Knives from the Blacksmith!'
StoreTip4 = 'Blacksmiths sell stronger Cutlasses and Daggers!'
StoreTip5 = 'Gypsies sell stronger Voodoo Dolls and Voodoo Staves!'
StoreTip6 = 'Gunsmiths sell stronger Pistols!'
LevelupTip1 = 'Gaining a Cutlass Level gives you more Health!'
LevelupTip2 = 'Gaining a Grenade Level gives you more Health!'
LevelupTip3 = 'Gaining a Pistol Level gives you some Health and Voodoo Power!'
LevelupTip4 = 'Gaining a Dagger Level gives you some Health and Voodoo Power!'
LevelupTip5 = 'Gaining a Voodoo Doll Level gives you more Voodoo Power!'
LevelupTip6 = 'Gaining a Voodoo Staff Level gives you more Voodoo Power!'
DifficultyTip1 = 'Enemies with Red Level tags are very dangerous enemies! \n They still give standard Reputation rewards, though.'
DifficultyTip2 = 'Enemies with Green Level tags will be easy to defeat! They give reduced Reputation!'
DifficultyTip3 = 'Enemies with Yellow Level tags are a good match for you! \n They give standard Reputation rewards!'
DifficultyTip4 = 'Enemies with Grey Level tags are push-overs! They give very little Reputation rewards!'
DifficultyTip5 = "An enemy with a Skull Icon over its head is a boss! \n They are tough so, don't fight them alone!"
SkillTip1 = 'The Cutlass Sweep skill will hit all surrounding enemies!'
ParlorGameTip1 = 'You can play Poker or Blackjack at any Tavern. To find one, look for the sign with a Mug on it!'
ParlorGameTip2 = "Suits don't matter in Blackjack. All that matters is the total number value of the cards."
ParlorGameTip3 = "Play Poker to quickly earn Gold. But don't lose!"
FunnyTip1 = "Don't throw Grenades at your own feet!"
FunnyTip2 = "Don't feed the Alligators!"
FunnyTip3 = "Don't pet the Scorpions!"
FunnyTip4 = 'If you have been playing for more than 2 hours straight, you should take a break!'
FunnyTip5 = "Don't wear more than one eye-patch when playing this game!"
PortRoyalTip1 = 'Stay away from Fort Charles unless you are looking for trouble with the Navy!'
ShipPVPHint1 = 'Get a crew together! Unmanned cannons stack the odds against you.'
ShipPVPHint2 = "Stockpile cannonballs before sailing because it's a long way back to restock!"
ShipPVPHint3 = 'Shield the smaller, weaker ships on the team if your ship can withstand a pounding.'
ShipPVPHint4 = 'An Interceptor is best for the outskirts of a battle, and should stay away from War Frigates.'
ShipPVPHint5 = "If your team can't launch more ships, teleport to a friend's ship to balance the odds."
ShipPVPHint6 = "Make every cannonball count! Targeting broken panels or an enemy ship's rear earns a bonus. "
ShipPVPHint7 = 'Choose team ships carefully. Some are faster, some are stronger, and each has a vital role in battle.'
ShipPVPHint8 = "Stay clear of the enemy's island! Ships launching from there are temporarily invincible."
ShipPVPHint9 = 'Repair your vessel! Each repair spot on a ship can be manned by a different crew member to speed up repairs.'
ShipPVPHint10 = 'Be careful when doing repairs, leaving the wheel allows enemy ships to sneak up on you!'
ShipPVPHint11 = 'A Privateer ship receives a health boost for sinking enemy ships; a good pirate steals everything, including spare parts.'
ShipPVPHint12 = 'The health bonus that a Privateer ship receives for sinking an enemy ship depends on the amount of damage it did.'
ShipPVPHint13 = 'Privateer teams are automatically balanced. If the team you are trying to join is full, join the other!'
ShipPVPHint14 = 'If you want to check your score, press the ~ button.'
ShipPVPHint15 = 'Looking for a Privateer crew? Find one using the Lookout button or through the Crew section on your Hearties panel!'
ShipPVPHint16 = 'Looking to recruit pirates for your Privateer crew? Look for crewmates using the Lookout button or through the Crew section on your Hearties panel!'
Hints_General = [
    GeneralTip1,
    GeneralTip2,
    GeneralTip4,
    GeneralTip5,
    ControlTip1,
    ControlTip3,
    ControlTip4,
    ControlTip5,
    ControlTip6,
    TonicTip1,
    TonicTip2,
    TonicTip3,
    QuestTip1,
    QuestTip2,
    QuestTip3,
    QuestTip4,
    QuestTip5,
    QuestTip6,
    QuestTip7,
    ShipTip0,
    ShipTip1,
    ShipTip2,
    ShipTip3,
    ShipTip4,
    ShipTip5,
    ShipTip6,
    ShipTip7,
    ShipTip8,
    ShipTip9,
    ShipTip10,
    ShipTip11,
    ShipTip12,
    ShipTip13,
    ShipTip14,
    ShipTip15,
    ShipTip16,
    ShipTip17,
    ShipTip18,
    ShipTip19,
    ShipTip21,
    ShipTip22,
    ShipTip23,
    ShipTip24,
    ShipTip25,
    ShipTip26,
    ShipTip27,
    ShipTip28,
    ShipTip29,
    FriendTip1,
    FriendTip2,
    FriendTip3,
    FriendTip4,
    FriendTip5,
    FriendTip6,
    TreadmillTip1,
    TreadmillTip2,
    TreadmillTip3,
    TreadmillTip4,
    TreadmillTip5,
    TreadmillTip6,
    TreadmillTip7,
    ChatTip1,
    LevelupTip1,
    LevelupTip2,
    LevelupTip3,
    LevelupTip4,
    LevelupTip5,
    LevelupTip6,
    CombatTip1,
    CombatTip2,
    CombatTip3,
    CombatTip4,
    CombatTip5,
    CombatTip6,
    CombatTip7,
    CombatTip8,
    CombatTip9,
    CombatTip10,
    CombatTip11,
    CombatTip12,
    CombatTip13,
    CombatTip14,
    CombatTip15,
    CombatTip16,
    ParlorGameTip1,
    ParlorGameTip2,
    ParlorGameTip3,
    FunnyTip1,
    FunnyTip2,
    FunnyTip3,
    FunnyTip4,
    FunnyTip5,
    DifficultyTip1,
    DifficultyTip2,
    DifficultyTip3,
    DifficultyTip4,
    DifficultyTip5,
    FlagShipTip1,
    FlagShipTip2,
    FlagShipTip3,
    FlagShipTip4]
Hints_Privateering = [
    ShipPVPHint1,
    ShipPVPHint2,
    ShipPVPHint3,
    ShipPVPHint4,
    ShipPVPHint5,
    ShipPVPHint6,
    ShipPVPHint7,
    ShipPVPHint8,
    ShipPVPHint9,
    ShipPVPHint10,
    ShipPVPHint11,
    ShipPVPHint12,
    ShipPVPHint13,
    ShipPVPHint14,
    ShipPVPHint15,
    ShipPVPHint16]
HintMap_Levels = {
    1: (QuestTip1, QuestTip2, ControlTip1, ControlTip2, ControlTip4, PortRoyalTip1),
    2: (QuestTip1, QuestTip2, PortRoyalTip1, ControlTip1, ControlTip2, ControlTip3, ControlTip4, ControlTip7, ControlTip9, ControlTip10, ControlTip12, ShipTip0, ShipTip1, ShipTip20),
    3: (ControlTip3, ControlTip4, ControlTip5, ControlTip7, ControlTip11, CombatTip3, ShipTip1, ShipTip20, ShipTip21, OptimizeTip1, ShipTip0, SkillTip1, QuestTip3),
    4: (ControlTip4, ControlTip5, ControlTip7, ControlTip8, CombatTip3, TonicTip1, TonicTip2, ShipTip0, ShipTip1, ShipTip2, ShipTip20, ShipTip21, OptimizeTip1, SkillTip1, StoreTip1, QuestTip3),
    5: (ControlTip5, ControlTip7, ControlTip8, CombatTip7, CombatTip8, CombatTip9, TonicTip1, TonicTip2, GeneralTip6, StoreTip1, ShipTip0, ShipTip1, ShipTip2, TreadmillTip6, TreadmillTip8, TreadmillTip9, FriendTip2, QuestTip8),
    6: (ControlTip3, ControlTip5, StoreTip2, StoreTip3, TreadmillTip6, TreadmillTip8, TreadmillTip9, FriendTip2, GeneralTip6, QuestTip8, TonicTip3, ShipTip3, ShipTip5, CombatTip2, CombatTip4, CombatTip5, CombatTip7, CombatTip8, CombatTip9),
    7: (StoreTip2, StoreTip3, CombatTip1, CombatTip2, CombatTip3, CombatTip4, CombatTip5, CombatTip10, TreadmillTip6, FriendTip1, QuestTip5, GeneralTip1, ShipTip4, ShipTip5, ShipTip15, ShipTip16),
    8: (StoreTip4, StoreTip5, StoreTip6, CombatTip1, CombatTip3, QuestTip4, FriendTip4, FriendTip5, TreadmillTip1, TreadmillTip6, GeneralTip1, FlagShipTip1, FlagShipTip2, FlagShipTip3, FlagShipTip4),
    9: (LevelupTip1, LevelupTip2, LevelupTip3, LevelupTip4, LevelupTip5, LevelupTip6, CombatTip11, CombatTip12, CombatTip13, CombatTip14, ControlTip6, ShipTip8),
    10: (ShipTip4, ShipTip6, ShipTip22, FriendTip6, QuestTip7, TreadmillTip5, ControlTip6, CombatTip3, ParlorGameTip1, GeneralTip2, GeneralTip3, DifficultyTip1, DifficultyTip2, DifficultyTip3, DifficultyTip4),
    11: (TreadmillTip1, TreadmillTip2, TreadmillTip3, QuestTip6, ControlTip6, CombatTip3, ParlorGameTip2, GeneralTip4, GeneralTip3, ShipTip7),
    12: (ControlTip1, CombatTip10, CombatTip1, CombatTip3, ParlorGameTip3, GeneralTip2, GeneralTip5, GeneralTip3, ShipTip9, ShipTip10, ShipTip11, ShipTip17),
    13: (ShipTip12, ShipTip17, ShipTip18, ShipTip19, ShipTip22, ShipTip23, ShipTip24, ShipTip25, GeneralTip4, TreadmillTip5, TreadmillTip7),
    14: (),
    15: (),
    16: (),
    17: (),
    18: (),
    19: (),
    20: (),
    21: (),
    22: (),
    23: (),
    24: (),
    25: ('High level enemies can be found on Kingshead.', 'You can purchase Grenade Ammunition from the Gunsmith!'),
    26: (),
    27: ('High level enemies can be found on Padres Del Fuego.',),
    28: (),
    29: (),
    30: ('High level enemies can be found on Isla Tormenta.',),
    31: (),
    32: (),
    33: (),
    34: (),
    35: (),
    36: (),
    37: (),
    38: (),
    39: (),
    40: ()}
HintMap_Locations = {
    '1150922126.8dzlu': (),
    '1155695180.13sdnaik': (),
    '1161798288.34sdnaik': (),
    '1164141722.61sdnaik': (),
    '1164952144.06sdnaik': (),
    '1165001772.05sdnaik': (),
    '1169592956.59sdnaik': (),
    '1175621632.0dxschafe0': (),
    '1153420207.67dzlu0': (),
    '1155773612.45fxlara0': (),
    '1168033330.17kmuller0': (),
    '1153419689.81dzlu0': (),
    '1153419634.08dzlu0': (),
    '1155684634.87dzlu0': (),
    '1155774289.03fxlara0': (),
    '1159905354.84jubutler': (),
    '1155244887.43dzlu0': (),
    '1155767402.81fxlara0': (),
    '1156207188.95dzlu': (),
    '1158295517.91sdnaik': (),
    '1165004570.58sdnaik': (),
    '1158121765.09sdnaik': (),
    '1165009873.53sdnaik': (),
    '1169179552.88sdnaik': (),
    '1165009856.72sdnaik': (),
    '1156207773.33dzlu0': (),
    '1156279370.48dzlu0': (),
    '1156207578.91dzlu0': (),
    '1156371286.47dzlu0': (),
    '1156207523.59dzlu0': (),
    '1156277937.59dzlu0': (),
    '1156270974.95dzlu0': (),
    '1156207423.67dzlu0': (),
    '1156279185.81dzlu0': (),
    '1142018473.22dxschafe': (),
    '1164135492.81dzlu': (),
    '1172209006.11sdnaik': (),
    '1164763706.66sdnaik': ('Crabs have been known to infest Driftwood island.',),
    '1161282725.84kmuller': (),
    '1164157132.99dzlu': (),
    '1172209955.25sdnaik': (),
    '1164150392.42dzlu': (),
    '1172208344.92sdnaik': (),
    '1160614528.73sdnaik': (),
    '1159933206.48sdnaik': (),
    '1156359855.24bbathen': (),
    '1173381952.2sdnaik': (),
    '1173382404.64sdnaik': (),
    '1167857698.16sdnaik': (),
    'Windward_Passage': (),
    'Brigand_Bay': (),
    'Bloody_Bayou': (),
    'Scurvy_Shallows': (),
    'Blackheart_Strait': (),
    'Salty_Flats': (),
    'Mar_de_Plata': (),
    'Smugglers_Run': (),
    'The_Hinterseas': (),
    'Dead_Mans_Trough': (),
    'Leeward_Passage': (),
    'Boiling_Bay': (),
    'Mariners_Reef': (),
    '1171761224.13sdnaik': (),
    'AnyLargeIsland': (),
    'AnyLargePort': (),
    'AnyWildPort': (),
    'AnyLocation': ()}
Hints_VelvetRope = [
    'With Unlimited Access, you can use all 6 Weapons!',
    'With Basic Member Access, you earn 40% less Reputation when defeating enemies!',
    'With Unlimited Access, you can purchase all 9 Ship types!',
    'You can play Team Battle PvP with Unlimited Access only!',
    'With Basic Member Access, a Skill cannot be upgraded past Rank 2!',
    'With Unlimited Access, you can start your own Guild!',
    "With Unlimited Access, you can play Tortuga Hold'em!",
    'Grenades can be used to defeat large groups of enemies! \n Unlimited Access only!',
    'Voodoo Dolls cast powerful Hexes to hurt enemies and heal allies! \n Unlimited Access only!',
    'Command dark powers using the Voodoo Staff! \n Unlimited Access only!',
    'Fight enemies up close or from afar with the Dagger! \n Unlimited Access only!',
    'With Unlimited Access, you can create up to 4 Pirate Characters!',
    'With Unlimited Access, you can purchase stronger weapons \n like the Double-Barreled Pistol!',
    'With Unlimited Access, you can unlock new ammo types, \n such as flaming cannonballs!',
    'With Basic Member Access, you cannot play in Fullscreen mode!']
RepCapText_Overall = 'Pirate Master\nLevel %s'
RepCapText_Skill = 'Mastered'
AnyTMName = 'Any Treasure Map'
AttackShipSunk = '1 Attack Ship Sunk!!'
AttackShipsSunk = '%s Attack Ships Sunk!!'
DrawbridgePassable = 'Bridge Destroyed!! '
BridgeNeedsToBeDestroyed = 'Bridge %d needs to be destroyed.'
AttackTheGoliath = 'Attack the Goliath!'
Goliath = 'Goliath'
SailTheBlackPearl = 'Sail the black pearl out of the harbor.'
DestroyTheBridges = ' Destroy the bridges blocking your way.'
BlackPearlTMName = 'Recover the Black Pearl'
BlackPearlTMDesc = "Escape with Jack's ship!"
BlackPearlStageZero = 'Stage One: Defeat the Navy Guards'
BlackPearlStageOne = 'Take the Wheel'
BlackPearlStageTwo = 'Stage Two:  Sink the Attack Ships'
BlackPearlStageThree = 'Stage Three:  Destroy the Drawbridges'
BlackPearlStageFour = 'Stage Four:  Sink the Goliath'
BlackPearlWarningLow = 'Danger!  The Black Pearl is almost sunk!'
BlackPearlLoser = 'The Black Pearl sank!'
BlackPearlWinner = 'You successfully rescued the Black Pearl! \nTake it back to Jack Sparrow to claim your booty'
BlackPearlWaitCutscene = 'Waiting for other players to finish cutscene.'
BlackPearlWaitCutscene2 = 'Other players waiting for you to finish cutscene.'
BlackPearlScoreboard = 'Black Pearl Quest:'
NavyFortName = 'Navy Fort'
EdgeOfWorldWarning = "You've sailed to the edge of the world. Turn your ship around to continue your adventure."
FirstDeathMsg = "You're going to need a moment to pull yourself together.  That skull represents your current groggy condition.  Some good pirating will shake it off though, so get out there!"
ShopBlacksmith = 'Blacksmith'
ShopGunsmith = 'Gunsmith'
ShopCannoneer = 'Cannoneer'
ShopShipwright = 'Shipwright'
ShopGypsy = 'Gypsy'
ShopMedicineMan = 'Medicine Man'
ShopGrenadier = 'Grenadier'
ShopMerchant = 'Merchant'
ShopBartender = 'Bartender'
ShopTailor = 'Tailor'
ShopTattoo = 'Tattoo Artist'
ShopBarber = 'Barber'
ShopJewelry = 'Jeweler'
ShopFree = 'Free'
ShopQuestItem = 'Quest Item'
ShopMusician = 'Musician'
ShopTrainer = 'Trainer'
ShopPvP = 'PvP Bounty Rewards'
SongPlayingAnnouncement = 'Now playing:\n%s'
RBROW = 0
LBROW = 1
LEAR = 2
REAR = 3
NOSE = 4
MOUTH = 5
LHAND = 6
RHAND = 7
JewelryNames = {
    RBROW: 'Right Brow',
    LBROW: 'Left Brow',
    LEAR: 'Left Ear',
    REAR: 'Right Ear',
    NOSE: 'Nose',
    MOUTH: 'Mouth',
    LHAND: 'Left Hand',
    RHAND: 'Right Hand'}
ShopLimitTailor = 'You cannot hold this item.\n\nCurrently the limit for clothing is %s items per category.\n\nYou will not be able to purchase clothing of this type until you have a free spot open.'
ShopLimitJewelry = 'You cannot hold this item.\n\nCurrently the limit for jewelry is %s items per category.\n\nYou will not be able to purchase jewelry of this type until you have a free spot open.'
ShopLimitTattoo = 'You cannot hold this item.\n\nCurrently the limit for tattoos is %s items per category.\n\nYou will not be able to purchase tattoos of this type until you have a free spot open.'
ShopFemaleVestConflict = 'Your current vest selection does not allow for shirts.\n\nPlease change vests to properly see this item'
ShopOwnedBarber = 'You currently have this style.'
ChatManagerOpenChatWarning = 'Your current chat settings do not allow chat. You can change your settings in the Account Options area of the Pirates Online web site.'
ChatManagerUnpaidWarning = 'Your subscription level does not allow chat. You can change your settings in the Account Options area of the Pirates Online web site.'
ChatManagerWhisperWarning = "Whispering text messages is only allowed between two paid subscribers who are adults or have their parent's permission."
ChatManagerNoFriendsWarning = 'You need to exchange Player Friends Codes with your friends in order to use Player Friends chat. To learn more about Player Friends chat or to enable Open chat, visit www.PiratesOnline.com.'
ChatManagerNeedParentWarning = 'Your account must be validated by a parent or guardian in order to use Player Friends chat or Open chat. To learn more about chat, visit www.PiratesOnline.com'
EnterKingsheadMessage = 'Entering Unlimited Access area, Kingshead Island'
EnterKingsheadWarning = 'Sorry, you must be an Unlimited Access member to enter Kingshead Island'
AccessVelvetRope = 'Basic Member Access'
AccessFull = 'Unlimited Access'
AccessUnknown = 'Unknown Access'
VelvetRopeQuestBlock = '\x01Ired\x01This quest is available only to Unlimited Access.\x02'
AccessLevel = {
    OTPGlobals.AccessUnknown: AccessUnknown,
    OTPGlobals.AccessVelvetRope: AccessVelvetRope,
    OTPGlobals.AccessFull: AccessFull}
for i in range(52):
    card = i
    suit = card / 13
    rank = card % 13
    iid = InventoryType.begin_Cards + i
    InventoryTypeNames[iid] = getPlayingCardName(suit, rank)

OceanZoneNames = {
    OceanZone.UNCHARTED_WATERS: 'Uncharted Waters',
    OceanZone.BRIGAND_BAY: 'Brigand Bay',
    OceanZone.BLOODY_BAYOU: 'Bloody Bayou',
    OceanZone.SCURVY_SHALLOWS: 'Scurvy Shallows',
    OceanZone.BLACKHEART_STRAIGHT: 'Blackheart Straight',
    OceanZone.WINDWARD_PASSAGE: 'Windward Passage',
    OceanZone.SALTY_FLATS: 'Salty Flats',
    OceanZone.MAR_DE_PLATA: 'Mar De Plata',
    OceanZone.SMUGGLERS_RUN: "Smuggler's Run",
    OceanZone.LEEWARD_PASSAGE: 'Leeward Passage',
    OceanZone.DEAD_MANS_TROUGH: "Dead Man's Trough",
    OceanZone.MARINERS_REEF: "Mariners' Reef",
    OceanZone.BOILING_BAY: 'Boiling Bay',
    OceanZone.THE_HINTER_SEAS: 'The Hinter Seas'}
EnterOceanZone = 'Entering\n%s'
MapCurrentIsland = 'You are here.'
MapNeedsTeleportToken = 'You do not have the Teleport Totem for this island.'
MapCanTeleport = 'Click to teleport to this island.'
MapCanTeleportReturn = 'Click to return to this island.'
MapCanTeleportPortOfCall = 'Click to return to your Port of Call.'
MapCannotTeleport = 'You cannot teleport to this island.'
MapBasicAccess = 'With %s, you can get a special Voodoo Totem that allows you to teleport to this island!' % AccessFull
LootBounty = '%s Bounty'
LootGold = '%s Gold'
LootGoldDouble = '%s Gold (Event Bonus)'
LootCrate = '%s Cargo Crate'
LootChest = '%s Treasure Chest'
LootSkChest = '%s Royal Chest'
LootCrateP = '%s Cargo Crates'
LootChestP = '%s Treasure Chests'
LootSkChestP = '%s Royal Chests'
TempNameList = [
    'Pirate',
    'Swashbuckler',
    'Buccaneer']
WeaponUnlockText = {
    InventoryType.CutlassRep: 'Unlocked by Will Turner',
    InventoryType.PistolRep: 'Unlocked by Captain Barbossa',
    InventoryType.DollRep: 'Unlocked at Notoriety Level 5',
    InventoryType.DaggerRep: 'Unlocked at Notoriety Level 10',
    InventoryType.GrenadeRep: 'Unlocked at Notoriety Level 20',
    InventoryType.WandRep: 'Unlocked at Notoriety Level 30'}
ReportPlayerTitle = 'Report A Player'
ReportPlayerCancel = 'Cancel'
ReportPlayerContinue = 'Continue'
ReportPlayerReport = 'Report'
ReportPlayerClose = 'Close'
ReportPlayerFoulLanguage = 'Foul Language'
ReportPlayerPersonalInfo = 'Sharing/Requesting Personal Info'
ReportPlayerRudeBehavior = 'Rude or Mean Behavior'
ReportPlayerBadName = 'Bad Name'
ReportPlayerAlreadyReported = '\x01Ired\x01%s\x02 has already been reported this session. Your report has already been sent to a Moderator for review.'
ReportPlayerTopMenu = 'This feature will send a complete report to a moderator.  Instead of sending a report, you might choose to do one of the following:\n\n  - Ignore this player for this session\n  - Switch to another server\n  - Remove friendship\n\n\n\nDo you want to report \x01Ired\x01%s\x02 to a Moderator?'
ReportPlayerChooseCategory = 'You are about to report \x01Ired\x01%s\x02. A Moderator will be alerted to your complaint and will take appropriate action for anyone breaking our rules. Please choose a reason for this report.'
ReportPlayerConfirmFoulLanguage = 'You are about to report that \x01Ired\x01%s\x02 has used obscene, bigoted or sexually explicit language.'
ReportPlayerConfirmPersonalInfo = 'You are about to report that \x01Ired\x01%s\x02 is being unsafe by giving out or requesting a phone number, address, last name, email address, password or account name.'
ReportPlayerConfirmRudeBehavior = 'You are about to report that \x01Ired\x01%s\x02 is bullying, harassing, or using extreme behavior to disrupt the game.'
ReportPlayerConfirmBadName = "You are about to report that \x01Ired\x01%s\x02 has created a name that does not follow Disney's House Rules."
ReportPlayerConfirmCategory = 'We take reporting very seriously. Your report will be viewed by a Moderator who will take appropriate action for anyone breaking our rules. If your account is found to have participated in breaking the rules, or if you make false reports or abuse the "Report a Player" system, a Moderator may take action against your account. Are you absolutely sure you want to report this player?'
ReportPlayerConfirmReport = 'Thank you! Your report has been sent to a Moderator for review. There is no need to contact us again about the issue. The moderation team will take appropriate action for a player found breaking our rules.'
ReportPlayerRemovedFriend = 'We have automatically removed \x01Ired\x01%s\x02 from your Friends List.'
ReportPlayerIgnored = '\x01Ired\x01%s\x02 has automatically been ignored for the remainder of this session.'
DoubleXPStart = makeHeadingString('Double Reputation Event In Progress!', 2) + '\nPlayers will earn double Reputation points for land and sea battles. %s Hours, %s Minutes remain before the end of the event.'
DoubleXPEnd = 'The double reputation point event for all has just ended!'
DoubleXPFullStart = makeHeadingString('Double Reputation Event In Progress!', 2) + '\nAll Unlimited Access Members will receive double Reputation points for all land and sea battles. %s Hours, %s Minutes remain before the end of the event.'
DoubleXPFullEnd = 'The double reputation point event for unlimited access members has just ended!'
DoubleXPStartChat = 'Double Reputation Event In Progress!\nPlayers will earn double reputation points for land and sea battles. %s Hours, %s Minutes remain before the end of the event.'
DoubleXPFullStartChat = 'Double Reputation Event In Progress!\nAll Unlimited Access Members will receive double Reputation points for all land and sea battles. %s Hours, %s Minutes remain before the end of the event.'
DoubleGoldStart = makeHeadingString('Double Gold Event In Progress!', 2) + '\nPlayers will earn double gold rewards for their quests and battles. %s Hours, %s Minutes remain before the end of the event.'
DoubleGoldStartChat = 'Double Gold Event In Progress!\nPlayers will earn double gold rewards for their quests and battles. %s Hours, %s Minutes remain before the end of the event.'
DoubleGoldEnd = 'The double gold event for all has just ended!'
DoubleGoldFullStart = makeHeadingString('Double Gold Event In Progress!', 2) + '\nAll Unlimited Access Members will receive double gold rewards for their quests and battles. %s Hours, %s Minutes remain before the end of the event.'
DoubleGoldFullStartChat = 'Double Gold Event In Progress!\nAll Unlimited Access Members will receive double gold rewards for their quests and battles. %s Hours, %s Minutes remain before the end of the event.'
DoubleGoldFullEnd = 'The double gold event for unlimited access members has just ended!'
DoubleGoldBonus = '2x Gold Bonus'
BlackJackFridayStart = makeHeadingString('Blackjack Friday in progress!', 2) + "\nVisit the Rowdy Rooster in Port Royal or King's Arm in Tortuga to play"
BlackJackFridayStartChat = 'Blackjack Friday currently in progress.'
BlackJackFridayEnd = makeHeadingString('Blackjack Friday has ended!', 2) + "\nPlease attend next week's Blackjack Friday: 3:00PM to 9:00PM (PDT)"
BlackJackFridayEndChat = 'Blackjack Friday has ended.'
FlirtEmoteStart = "To All Pirates... For Valentines Day, we are introducing a new emote, flirt. Flirt can be accessed through your emotes SpeedChat menu and by the emote command '/flirt'."
FreeHatStartUnlimited = makeHeadingString('To all Unlimited Access Members', 2) + "\nDon't forget to pick up your exclusive skull bandana from any Tailor Shop before Midnight (PST), Sunday, March 2nd."
FreeHatStartUnlimitedChat = "Don't forget to pick up your exclusive skull bandana from any Tailor Shop before Midnight (PST), Sunday, March 2nd."
FreeHatStartBasic = makeHeadingString('Claim your exclusive in-game item!', 2) + '\nUpgrade to Unlimited Access and visit any Tailor shop before Midnight (PST), Sunday, March 2nd, to pick up an exclusive skull bandana.'
FreeHatStartBasicChat = 'Upgrade to Unlimited Access and visit any Tailor shop before Midnight (PST), March 2nd, to pick up an exclusive skull bandana!'
StPatricksStartUnlimited = makeHeadingString('To all Unlimited Access Members', 2) + "\nVisit the tattoo parlor for your exclusive St. Patty's Day tattoo & the Barber for some green hair.  Available until Midnight (PST) on March 17th."
StPatricksStartUnlimitedChat = "Don't forget to pick up your St. Patricks day tattoo and green hair before they disappear Midnight (PST), March 17th."
StPatricksStartBasic = makeHeadingString("Get your St. Patrick's day tattoos and hair!", 2) + '\nUpgrade to Unlimited Access and get your St. Patrick\xc2\x92s Day tattoo and green hair before Midnight (PST) on March 17th!'
StPatricksStartBasicChat = "Upgrade to Unlimited Access and pick up your St. Patrick's day tattoo and green hair before they disappear at Midnight (PST), March 17th!"
MothersDayStartUnlimited = makeHeadingString('To all Unlimited Access Members', 2) + "\nVisit the tattoo parlor for exclusive Mother's Day tattoos.  Available until 12:00AM (PDT) on May 12th. %s Hour(s), %s Minute(s) until the end of the event."
MothersDayStartUnlimitedChat = "Visit the tattoo parlor for exclusive Mother's Day tattoos.  Available until 12:00AM (PDT) on May 12th. %s Hour(s), %s Minute(s) until the end of the event."
MothersDayStartBasic = makeHeadingString("Get your Mother's Day tattoos!", 2) + '\nUpgrade to Unlimited Access and get your Mother\xc2\x92s Day tattoos before 12:00AM (PDT) on May 12th! %s Hour(s), %s Minute(s) until the end of the event.'
MothersDayStartBasicChat = "Upgrade to Unlimited Access and pick up your Mother's day tattoos before they disappear at 12:00AM (PDT), May 12th! %s Hour(s), %s Minute(s) until the end of the event."
FathersDayStart = makeHeadingString("Father's Day Event", 2) + "\nVisit Jack Sparrow at the Rowdy Rooster in Port Royal, to take part in a limited time Father's Day Quest.  Available until 12:00AM (PDT) on June 16th. %s Hour(s), %s Minute(s) until the end of the event."
FathersDayStartChat = "Visit Jack Sparrow at the Rowdy Rooster in Port Royal, to take part in a limited time Father's Day quest.  Available until 12:00AM (PDT) on June 16th. %s Hour(s), %s Minute(s) until the end of the event."
FourthOfJulyStart = makeHeadingString('Fourth of July', 2) + '\nGo to the shores of Port Royal, Tortuga or Padres del Fuego to watch fireworks light up the night sky. Show occurs every hour during night time.'
FourthOfJulyStartChat = 'Go to the shores of Port Royal, Tortuga or Padres del Fuego to watch fireworks light up the night sky. Show occurs every hour during night time.'
HalloweenStart = makeHeadingString('All Hallows Eve Holiday is in progress!', 2) + '\nJolly Roger forced an evil atmosphere around the Caribbean.'
HalloweenStartChat = 'All Hallows Eve Holiday is in progress! \nJolly Roger forced an evil atmosphere around the Caribbean.'
HalloweenEnd = 'All Hallows Eve Holiday has ended!'
CursedNightStart = 'Jolly Roger forced an evil atmosphere around the Caribbean once again. Beware! The curse is coming!'
CursedNightEnd = "Jolly Roger's powers have been weakened, evil atmosphere has lifted. At least for now..."
FullMoonWarning1 = 'The Moon will become full in about 5 minutes!'
FullMoonWarning2 = 'The Moon will become full in less than 1 minute!'
JollyRogerCurseComing = 'Jolly Roger\xc2\x92s Curse is coming! \nWhen the moon becomes full, everyone outdoors and on land will become Undead! Hide inside a building during the full moon to be safe from the curse!'
JollyRogerCurseActive = "Beware! Jolly Roger's Curse has turned the pirates outdoors into the Undead. Go defend the towns from the Cursed Pirates!"
JollyRogerCurseIndoors = 'Jolly Roger\xc2\x92s Curse is upon us! You are safe here, but the towns need your help!'
JollyRogerCurseOutdoors = 'Jolly Roger\xc2\x92s Curse is upon us! Jolly Roger commands you to attack other Undead and Humans!'
JollyRogerCurseJail = 'You are restored from Jolly Roger\xc2\x92s Curse! Now, go save the town from the other Undead!'
JollyRogerCurseEnd = 'Jolly Roger\xc2\x92s Curse has been broken! The Caribbean is safe again for now...'
FoundersFeastStart = makeHeadingString('Founders Feast Holiday is in progress!', 2) + '\nCome to the shores of Tortuga to join the festivities.'
FoundersFeastStartChat = 'Founders Feast Holiday is in progress! \nCome to the shores of Tortuga to join the festivities.'
FoundersFeastEnd = 'Founders Feast Holiday has ended!'
FoundersFeastBegin = 'Let the Founders Feast begin!'
FreeBandanaStartUnlimited = makeHeadingString('To all Unlimited Access Members', 2) + "\nDon't forget to pick up your exclusive golden skull bandana from any Tailor Shop before Midnight (PST), Sunday, December 7th."
FreeBandanaStartUnlimitedChat = "Don't forget to pick up your exclusive skull bandana from any Tailor Shop before Midnight (PST), Sunday, December 7th."
FreeBandanaStartBasic = makeHeadingString('Claim your exclusive in-game item!', 2) + '\nUpgrade to Unlimited Access and visit any Tailor shop before Midnight (PST), Sunday, December 7th, to pick up an exclusive golden skull bandana.'
FreeBandanaStartBasicChat = 'Upgrade to Unlimited Access and visit any Tailor shop before Midnight (PST), December 7th, to pick up an exclusive golden skull bandana!'
HalfOffCustomizationStart = 'Half off customization for Unlimited Access players: %s hours, and %s minutes'
HalfOffCustomizationEnd = 'The 50%% off all customization items event has ended.'
HalfOffCustomizationUnlimited = 'Unlimited Access Members Only!  Visit any of the shops for 50%% off all customization items such as Clothing, Tattoos and Jewelry. Now until noon (PDT), August 18. %s Hour(s), %s Minute(s) until the end of the event.'
HalfOffCustomizationBasic = 'Now until noon (PDT), August 18, Unlimited Access members receive 50%% off all Customization Items. (Note: Discounts for paid members only. Upgrade to a paid subscription to take advantage of the shop discounts.) %s Hour(s), %s Minute(s) until the end of the event.'
HalfOffCustomizationStatus = 'Half-Off Customization Event (Unlimited Access Players):\nTime Remaining: %s Hour(s), %s Minute(s)'
AllAccessHolidayStart = 'Free Preview Weekend for the next %s hours, and %s minutes'
UnlimitedAccessEventBasic = "Avast! It's a Free Preview Weekend! Your Basic Access account has been upgraded to Unlimited Access for FREE until noon (PDT), August 18. %s Hour(s), %s Minute(s) until the end of the event."
UnlimitedAccessEventUnlimited = "Avast! It's a Free Preview Weekend for Limited Access crew members. Please feel free to invite friends and family to signup for a free account. They will be able to experience being an Unlimited Access crew member from now until noon (PDT), August 18th. %s Hour(s), %s Minute(s) until the end of the event."
UnlimitedAccessEventUnlimitedChat = "Avast! It's a Free Preview Weekend for Limited Access crew members. Please feel free to invite friends and family to signup for a free account. Now until noon (PDT), August 18th. %s Hour(s), %s Minute(s) until the end of the event."
NO_CURRENT_HOLIDAYS = 'Sorry, there are no holiday events active right now.'
CHAT_STATUS_DOUBLEXP = 'Double Reputation Point Event (All Players):\nTime Remaining: %s Hours, %s Minutes'
CHAT_STATUS_DOUBLEXP_PAID = 'Double Reputation Point Event (Unlimited Access Members):\nTime Remaining: %s Hours, %s Minutes'
CHAT_STATUS_DOUBLEGOLD = 'Double Gold Event (All Players):\nTime Remaining: %s Hours, %s Minutes'
CHAT_STATUS_DOUBLEGOLD_PAID = 'Double Gold Event (Unlimited Access Members):\nTime Remaining: %s Hours, %s Minutes'
CHAT_STATUS_BLACKJACK_FRIDAY = 'BlackJack Friday:\nTime Remaining: %s Hours, %s Minutes'
CHAT_STATUS_MOTHERS_DAY_PAID = "Mother's Day Tattoo Event (Unlimited Access Members):\nTime Remaining: %s Hour(s), %s Minute(s)"
CHAT_STATUS_FATHERS_DAY = "Father's Day Quest Event:\nTime Remaining: %s Hours, %s Minutes"
CHAT_STATUS_FOURTHOFJULY = 'Fourth Of July Holiday:\nTime Remaining: %s Hours, %s Minutes'
CHAT_STATUS_HALLOWEEN = 'Halloween Holiday:\nTime Remaining: %s Hours, %s Minutes'
CHAT_STATUS_JOLLYROGERCURSE = 'Jolly Roger Curse Event:\nTime Remaining: %s Hours, %s Minutes'
CHAT_STATUS_FOUNDERSFEAST = 'Founders Feast Holiday:\nTime Remaining: %s Hours, %s Minutes'
DISCORD_DOUBLE_GOLD_HOLIDAY = 'Double Gold'
DISCORD_DOUBLE_EXP_HOLIDAY = 'Double Experience'
DISCORD_FREE_HAT_WEEK = 'Free Hat Week'
DISCORD_FLIRT_EMOTE = 'Valentines Day'
DISCORD_SAINT_PATRICKS_DAY = 'Saint Patricks Day'
DISCORD_MOTHERS_DAY = 'Mothers Day'
DISCORD_FATHERS_DAY = 'Fathers Day'
DISCORD_FOURTH_OF_JULY = 'Fourth of July'
DISCORD_HALF_OFF_CUSTOMIZATION = 'Half Off Customization'
DISCORD_ALL_ACCESS_WEEKEND = 'All Access Weekend'
DISCORD_HALLOWEEN = 'All Hallows Eve'
DISCORD_JOLLY_ROGER_CURSE = 'Curse of the Muertos Moon'
DISCORD_FOUNDERS_FEAST = 'Founders Feast'
DISCORD_CURSED_NIGHT = 'Curse of the Muertos Moon'
DISCORD_JOLLY_CURSE_AUTO = 'Curse of the Muertos Moon'
DISCORD_MESSAGE_DOUBLEXP = 'Ahoy there ye scallyways! The Gypsies guild has brewed up a secret tonic that doubles your knowledge! All xp earned will be double across the caribbean!'
DISCORD_MESSAGE_DOUBLEGOLD = 'Ahoy ye landlubbers! Jolly Rogers secret stash has been found! All gold rewards across the caribbean are currently doubled!'
DISCORD_MESSAGE_HALLOWEEN = 'Ahoy ye landlubbers! Jolly Roger has casted an evil spell across the Caribbean turning everyone into undead!'
TEMP_DOUBLE_REP = 'You earned a x2 reputation reward.\nYou currently have %s hours(s) and %s minute(s), before the reward expires. Type /x2 at the chat prompt to check the time remaining.'
TEMP_DOUBLE_REP_CHAT = 'You earned a x2 reputation reward.\nYou currently have %s hours(s) and %s minute(s), before the reward expires.'
NO_TEMP_DOUBLE_REP = 'You currently do not have a double reputation award'
EMOTE_RECEIVE_DOLL = 60405
EMOTE_RECEIVE_STAFF = 60406
EMOTE_RECEIVE_DAGGER = 60407
EMOTE_RECEIVE_GRENADE = 60408
EMOTE_COIN_FLIP = 60505
EMOTE_CHANT_A = 60507
EMOTE_CHANT_B = 60508
EMOTE_DANCE_JIG = 60509
EMOTE_FLEX = 60511
EMOTE_LUTE = 60512
EMOTE_FLUTE = 60513
EMOTE_CRAZY = 60514
EMOTE_SEARCHING = 60515
EMOTE_SWEEP = 60518
EMOTE_PRIMP = 60519
EMOTE_AGREE = 60600
EMOTE_AMAZED = 60601
EMOTE_ANGRY = 60602
EMOTE_ARRR = 60603
EMOTE_BARK = 60605
EMOTE_BLINK = 60606
EMOTE_BORED = 60607
EMOTE_BOUNCE = 60608
EMOTE_BOW = 60610
EMOTE_CACKLE = 60611
EMOTE_CHEER = 60612
EMOTE_CHUCKLE = 60613
EMOTE_CLAP = 60614
EMOTE_CONFUSED = 60615
EMOTE_CONGRATS = 60616
EMOTE_CRY = 60618
EMOTE_CURIOUS = 60619
EMOTE_DRINK = 60620
EMOTE_EAT = 60621
EMOTE_FEAR = 60622
EMOTE_FLEE = 60623
EMOTE_FROWN = 60624
EMOTE_GASP = 60625
EMOTE_GIGGLE = 60626
EMOTE_GLARE = 60627
EMOTE_GOODBYE = 60628
EMOTE_GREET = 60629
EMOTE_GRIN = 60630
EMOTE_GROWL = 60631
EMOTE_HAIL = 60632
EMOTE_HAPPY = 60633
EMOTE_HELLO = 60634
EMOTE_HELP = 60635
EMOTE_HISS = 60636
EMOTE_HUNGRY = 60637
EMOTE_IMPATIENT = 60638
EMOTE_JK = 60639
EMOTE_LAUGH = 60640
EMOTE_LOL = 60641
EMOTE_MEOW = 60642
EMOTE_MOO = 60643
EMOTE_NOD = 60645
EMOTE_POWERFUL = 60647
EMOTE_READY = 60649
EMOTE_ROAR = 60650
EMOTE_ROFL = 60651
EMOTE_SAD = 60652
EMOTE_SALUTE = 60653
EMOTE_SCARED = 60654
EMOTE_SHRUG = 60655
EMOTE_SIGH = 60656
EMOTE_SMILE = 60657
EMOTE_SORRY = 60658
EMOTE_TAP = 60659
EMOTE_THIRSTY = 60660
EMOTE_TIRED = 60661
EMOTE_VITTLES = 60662
EMOTE_WAIT = 60663
EMOTE_WAVE = 60664
EMOTE_WINK = 60665
EMOTE_YAWN = 60666
EMOTE_CELEBRATE = 60668
EMOTE_SLEEP = 60669
EMOTE_DANCE = 60670
EMOTE_VALENTINES_A = 60671
EMOTE_VALENTINES_B = 60672
EMOTE_VALENTINES_C = 60673
EMOTE_VALENTINES_D = 60674
EMOTE_VALENTINES_E = 60675
EMOTE_VALENTINES = 60676
EMOTE_HALLOWEEN = 60677
EMOTE_YES = 65000
EMOTE_NO = 65001
receiveWeaponEmotes = {
    EMOTE_RECEIVE_DOLL: ('doll_receive', 1, 'models/handheld/voodoo_doll_high', OL.Emotes_General, None, None),
    EMOTE_RECEIVE_STAFF: ('staff_receive', 1, 'models/handheld/voodoo_staff_high', OL.Emotes_General, None, None),
    EMOTE_RECEIVE_DAGGER: ('dagger_receive', 1, 'models/handheld/dagger_high', OL.Emotes_General, None, None),
    EMOTE_RECEIVE_GRENADE: ('bomb_receive', 1, 'models/ammunition/grenade', OL.Emotes_General, None, None)}
emotes = {
    EMOTE_COIN_FLIP: ('coin_flip_idle', 1, 'models/handheld/coin_high', OL.Emotes_General, None, None),
    EMOTE_DANCE_JIG: ('emote_dance_jig', 1, None, OL.Emotes_General, None, None),
    EMOTE_FLEX: ('idle_flex', 0, None, OL.Emotes_General, None, None),
    EMOTE_PRIMP: ('primp_idle', 1, None, OL.Emotes_General, 'f', None),
    EMOTE_ANGRY: ('emote_anger', 0, None, OL.Emotes_Expressions, None, None),
    EMOTE_CELEBRATE: ('emote_celebrate', 0, None, OL.Emotes_General, None, None),
    EMOTE_CLAP: ('emote_clap', 0, None, OL.Emotes_General, None, 'audio/sfx_emote_clap.wav'),
    EMOTE_FEAR: ('emote_fear', 0, None, OL.Emotes_Expressions, None, None),
    EMOTE_LAUGH: ('emote_laugh', 0, None, OL.Emotes_Expressions, None, None),
    EMOTE_NO: ('emote_no', 0, None, OL.Emotes_General, None, None),
    EMOTE_SAD: ('emote_sad', 0, None, OL.Emotes_Expressions, None, None),
    EMOTE_SMILE: ('emote_smile', 0, None, OL.Emotes_Expressions, None, None),
    EMOTE_WAVE: ('emote_wave', 0, None, OL.Emotes_General, None, None),
    EMOTE_WINK: ('emote_wink', 0, None, OL.Emotes_General, None, None),
    EMOTE_YAWN: ('emote_yawn', 0, None, OL.Emotes_Expressions, None, None),
    EMOTE_YES: ('emote_yes', 0, None, OL.Emotes_General, None, None),
    EMOTE_SLEEP: ('sleep_idle', 1, None, OL.Emotes_General, None, None),
    EMOTE_VALENTINES: ('emote_wink', 0, None, OL.Emotes_General, None, None)}
nonMenuEmoteAnimations = {
    EMOTE_CHEER: ('emote_celebrate', 0, None, OL.Emotes_General, None, None),
    EMOTE_TIRED: ('sleep_idle', 1, None, OL.Emotes_Expressions, None, None),
    EMOTE_NOD: ('emote_yes', 0, None, OL.Emotes_Expressions, None, None),
    EMOTE_GREET: ('emote_wave', 0, None, OL.Emotes_General, None, None),
    EMOTE_LOL: ('emote_laugh', 0, None, OL.Emotes_Expressions, None, None),
    EMOTE_SCARED: ('emote_fear', 0, None, OL.Emotes_Expressions, None, None),
    EMOTE_GRIN: ('emote_smile', 0, None, OL.Emotes_Expressions, None, None),
    EMOTE_HAPPY: ('emote_smile', 0, None, OL.Emotes_Expressions, None, None),
    EMOTE_DANCE: ('emote_dance_jig', 1, None, OL.Emotes_General, None, None),
    EMOTE_HALLOWEEN: ('emote_thriller', 0, None, OL.Emotes_General, None, None)}
EmoteCommands = {
    'coin': EMOTE_COIN_FLIP,
    'dance': EMOTE_DANCE,
    'jig': EMOTE_DANCE_JIG,
    'flex': EMOTE_FLEX,
    'crazy': EMOTE_CRAZY,
    'search': EMOTE_SEARCHING,
    'sweep': EMOTE_SWEEP,
    'primp': EMOTE_PRIMP,
    'agree': EMOTE_AGREE,
    'amazed': EMOTE_AMAZED,
    'angry': EMOTE_ANGRY,
    'celebrate': EMOTE_CELEBRATE,
    'sleep': EMOTE_SLEEP,
    'arrr': EMOTE_ARRR,
    'bark': EMOTE_BARK,
    'blink': EMOTE_BLINK,
    'bored': EMOTE_BORED,
    'bounce': EMOTE_BOUNCE,
    'bow': EMOTE_BOW,
    'cackle': EMOTE_CACKLE,
    'cheer': EMOTE_CHEER,
    'chuckle': EMOTE_CHUCKLE,
    'clap': EMOTE_CLAP,
    'confused': EMOTE_CONFUSED,
    'congrats': EMOTE_CONGRATS,
    'grats': EMOTE_CONGRATS,
    'congratulate': EMOTE_CONGRATS,
    'cry': EMOTE_CRY,
    'curious': EMOTE_CURIOUS,
    'drink': EMOTE_DRINK,
    'eat': EMOTE_EAT,
    'cower': EMOTE_FEAR,
    'fear': EMOTE_FEAR,
    'flee': EMOTE_FLEE,
    'frown': EMOTE_FROWN,
    'gasp': EMOTE_GASP,
    'giggle': EMOTE_GIGGLE,
    'glare': EMOTE_GLARE,
    'bye': EMOTE_GOODBYE,
    'goodbye': EMOTE_GOODBYE,
    'greet': EMOTE_GREET,
    'grin': EMOTE_GRIN,
    'growl': EMOTE_GROWL,
    'hail': EMOTE_HAIL,
    'happy': EMOTE_HAPPY,
    'hello': EMOTE_HELLO,
    'help': EMOTE_HELP,
    'hiss': EMOTE_HISS,
    'hungry': EMOTE_HUNGRY,
    'impatient': EMOTE_IMPATIENT,
    'tap': EMOTE_IMPATIENT,
    'jk': EMOTE_JK,
    'kidding': EMOTE_JK,
    'laugh': EMOTE_LAUGH,
    'lol': EMOTE_LAUGH,
    'meow': EMOTE_MEOW,
    'moo': EMOTE_MOO,
    'no': EMOTE_NO,
    'nod': EMOTE_NOD,
    '9000': EMOTE_POWERFUL,
    'ready': EMOTE_READY,
    'roar': EMOTE_ROAR,
    'rofl': EMOTE_ROFL,
    'sad': EMOTE_SAD,
    'salute': EMOTE_SALUTE,
    'scared': EMOTE_SCARED,
    'shrug': EMOTE_SHRUG,
    'sigh': EMOTE_SIGH,
    'smile': EMOTE_SMILE,
    'sorry': EMOTE_SORRY,
    'sry': EMOTE_SORRY,
    'thirsty': EMOTE_THIRSTY,
    'tired': EMOTE_TIRED,
    'valentine': EMOTE_VALENTINES,
    'vittles': EMOTE_VITTLES,
    'wait': EMOTE_WAIT,
    'wave': EMOTE_WAVE,
    'wink': EMOTE_WINK,
    'yawn': EMOTE_YAWN,
    'yes': EMOTE_YES,
    'zombie': EMOTE_HALLOWEEN}
EmoteMessagesSelf = {
    EMOTE_COIN_FLIP: 'You flip a coin.',
    EMOTE_CHANT_A: 'You dance.',
    EMOTE_CHANT_B: 'You dance.',
    EMOTE_DANCE: 'You dance.',
    EMOTE_DANCE_JIG: 'You dance a jig.',
    EMOTE_FLEX: 'You flex mightily.',
    EMOTE_CRAZY: "You're going crazy!",
    EMOTE_SEARCHING: 'You look around, searching for something.',
    EMOTE_SWEEP: 'You sweep the ground clean.',
    EMOTE_PRIMP: 'You check your nails.',
    EMOTE_AGREE: 'You agree.',
    EMOTE_AMAZED: 'You are amazed!',
    EMOTE_ANGRY: 'You look angry.',
    EMOTE_CELEBRATE: 'You celebrate!',
    EMOTE_SLEEP: 'You look sleepy.',
    EMOTE_ARRR: 'Arrrrrrr!',
    EMOTE_BARK: 'You bark like a wild dog!',
    EMOTE_BLINK: 'You blink.',
    EMOTE_BORED: 'You look bored.',
    EMOTE_BOUNCE: 'You bounce up and down.',
    EMOTE_BOW: 'You bow politely.',
    EMOTE_CACKLE: 'You cackle!',
    EMOTE_CHEER: 'You cheer!',
    EMOTE_CHUCKLE: 'You chuckle softly.',
    EMOTE_CLAP: 'You clap!',
    EMOTE_CONFUSED: 'You look confused.',
    EMOTE_CONGRATS: 'You congratulate everyone.',
    EMOTE_CRY: 'You cry.',
    EMOTE_CURIOUS: 'You look curious.',
    EMOTE_DRINK: 'You pour a drink.',
    EMOTE_EAT: 'You munch on some food.',
    EMOTE_FEAR: 'You cower in fear.',
    EMOTE_FLEE: 'You flee in terror!',
    EMOTE_FROWN: 'You frown.',
    EMOTE_GASP: 'You gasp!',
    EMOTE_GIGGLE: 'You giggle.',
    EMOTE_GLARE: 'You glare angrily.',
    EMOTE_GOODBYE: 'You wave goodbye.',
    EMOTE_GREET: 'You greet everyone around you.',
    EMOTE_GRIN: 'You grin.',
    EMOTE_GROWL: 'You growl angrily.',
    EMOTE_HAIL: 'You hail everyone around you.',
    EMOTE_HALLOWEEN: "You're dancing like a zombie!",
    EMOTE_HAPPY: 'You are happy!',
    EMOTE_HELLO: 'You say hello!',
    EMOTE_HELP: 'You call out for help!',
    EMOTE_HISS: 'You hiss menacingly.',
    EMOTE_HUNGRY: 'You look hungry.',
    EMOTE_IMPATIENT: 'You tap your foot impatiently.',
    EMOTE_JK: "You let everyone know you're just kidding!",
    EMOTE_LAUGH: 'You laugh!',
    EMOTE_MEOW: 'You meow like a cat.',
    EMOTE_MOO: 'You moo.  Moooooooo!',
    EMOTE_NO: 'You say, NO.',
    EMOTE_NOD: 'You nod.',
    EMOTE_POWERFUL: 'You are far too mighty for these weaklings!',
    EMOTE_READY: 'You are ready!',
    EMOTE_ROAR: 'You roar loudly!',
    EMOTE_ROFL: 'You roll on the floor laughing.',
    EMOTE_SAD: 'You look sad.',
    EMOTE_SALUTE: 'You salute.',
    EMOTE_SCARED: 'You are scared!',
    EMOTE_SHRUG: 'You shrug.',
    EMOTE_SIGH: 'You sigh softly.',
    EMOTE_SMILE: 'You smile.',
    EMOTE_SORRY: 'You apologize.  Sorry!',
    EMOTE_THIRSTY: 'You look thirsty.',
    EMOTE_TIRED: 'You look tired.',
    EMOTE_VALENTINES: 'You wink.',
    EMOTE_VALENTINES_A: 'You wink A!',
    EMOTE_VALENTINES_B: 'You wink B!',
    EMOTE_VALENTINES_C: 'You wink C!',
    EMOTE_VALENTINES_D: 'You wink D!',
    EMOTE_VALENTINES_E: 'You wink E!',
    EMOTE_VITTLES: 'You ask around for something to eat.',
    EMOTE_WAIT: 'You ask everyone to wait.',
    EMOTE_WAVE: 'You wave.',
    EMOTE_WINK: 'You wink.',
    EMOTE_YAWN: 'You yawn.',
    EMOTE_YES: 'You say, Yes!'}
EmoteMessagesThirdPerson = {
    EMOTE_COIN_FLIP: '%s flips a coin.',
    EMOTE_CHANT_A: '%s dances.',
    EMOTE_CHANT_B: '%s dances.',
    EMOTE_DANCE: '%s dances.',
    EMOTE_DANCE_JIG: '%s dances a jig.',
    EMOTE_FLEX: '%s flexes mightily.',
    EMOTE_LUTE: '%s pulls out a lute and begins to play.',
    EMOTE_FLUTE: '%s pulls out a flute and begins to play.',
    EMOTE_CRAZY: '%s is going crazy!',
    EMOTE_SEARCHING: '%s looks around, searching for something.',
    EMOTE_SWEEP: '%s sweeps the ground clean.',
    EMOTE_PRIMP: '%s checks her nails.',
    EMOTE_AGREE: '%s agrees.',
    EMOTE_AMAZED: '%s is amazed!',
    EMOTE_ANGRY: '%s looks angry.',
    EMOTE_CELEBRATE: '%s celebrates.',
    EMOTE_SLEEP: '%s looks sleepy.',
    EMOTE_ARRR: '%s says, "Arrrrrrr!"',
    EMOTE_BARK: '%s barks like a wild dog!',
    EMOTE_BLINK: '%s blinks.',
    EMOTE_BORED: '%s looks bored.',
    EMOTE_BOUNCE: '%s bounces up and down.',
    EMOTE_BOW: '%s bows politely.',
    EMOTE_CACKLE: '%s cackles!',
    EMOTE_CHEER: '%s cheers!',
    EMOTE_CHUCKLE: '%s chuckles softly.',
    EMOTE_CLAP: '%s claps!',
    EMOTE_CONFUSED: '%s looks confused.',
    EMOTE_CONGRATS: '%s congratulates everyone.',
    EMOTE_CRY: '%s cries.',
    EMOTE_CURIOUS: '%s looks curious.',
    EMOTE_DRINK: '%s pours a drink.',
    EMOTE_EAT: '%s munches on some food.',
    EMOTE_FEAR: '%s cowers in fear.',
    EMOTE_FLEE: '%s flees in terror!',
    EMOTE_FROWN: '%s frowns.',
    EMOTE_GASP: '%s gasps!',
    EMOTE_GIGGLE: '%s giggles.',
    EMOTE_GLARE: '%s glares angrily.',
    EMOTE_GOODBYE: '%s waves goodbye.',
    EMOTE_GREET: '%s greets everyone nearby.',
    EMOTE_GRIN: '%s grins.',
    EMOTE_GROWL: '%s growls angrily.',
    EMOTE_HAIL: '%s hails everyone nearby.',
    EMOTE_HALLOWEEN: '%s is dancing like a zombie!',
    EMOTE_HAPPY: '%s is happy!',
    EMOTE_HELLO: '%s says hello!',
    EMOTE_HELP: '%s calls out for help!',
    EMOTE_HISS: '%s hisses menacingly.',
    EMOTE_HUNGRY: '%s looks hungry.',
    EMOTE_IMPATIENT: '%s waits impatiently.',
    EMOTE_JK: '%s is just kidding!',
    EMOTE_LAUGH: '%s laughs!',
    EMOTE_MEOW: '%s meows like a cat.',
    EMOTE_MOO: '%s moos.  Moooooooo!',
    EMOTE_NO: '%s says, NO.',
    EMOTE_NOD: '%s nods.',
    EMOTE_POWERFUL: '%s is far too mighty for these weaklings!',
    EMOTE_READY: '%s is ready!',
    EMOTE_ROAR: '%s roars loudly!',
    EMOTE_ROFL: '%s rolls on the floor laughing.',
    EMOTE_SAD: '%s looks sad.',
    EMOTE_SALUTE: '%s salutes.',
    EMOTE_SCARED: '%s is scared!',
    EMOTE_SHRUG: '%s shrugs.',
    EMOTE_SIGH: '%s sighs softly.',
    EMOTE_SMILE: '%s smiles.',
    EMOTE_SORRY: '%s apologizes.  Sorry!',
    EMOTE_THIRSTY: '%s looks thirsty.',
    EMOTE_TIRED: '%s looks tired.',
    EMOTE_VALENTINES: '%s winks.',
    EMOTE_VALENTINES_A: '%s winks A!',
    EMOTE_VALENTINES_B: '%s winks B!',
    EMOTE_VALENTINES_C: '%s winks C!',
    EMOTE_VALENTINES_D: '%s winks D!',
    EMOTE_VALENTINES_E: '%s winks E!',
    EMOTE_VITTLES: '%s asks around for something to eat.',
    EMOTE_WAIT: '%s asks everyone to wait.',
    EMOTE_WAVE: '%s waves.',
    EMOTE_WINK: '%s winks.',
    EMOTE_YAWN: '%s yawns.',
    EMOTE_YES: '%s says, Yes!'}
WeaponReceiveToEmoteCmds = {
    UberDogGlobals.InventoryType.DollToken: EMOTE_RECEIVE_DOLL,
    UberDogGlobals.InventoryType.WandToken: EMOTE_RECEIVE_STAFF,
    UberDogGlobals.InventoryType.DaggerToken: EMOTE_RECEIVE_DAGGER,
    UberDogGlobals.InventoryType.GrenadeToken: EMOTE_RECEIVE_GRENADE}
CpuWarning = "Warning! \n\nYour CPU's frequency is currently running at %.4f GHz instead of the maximum %.4f GHz.  As a result, your gaming experience might be affected."
URL_UpgradeNow = os.getenv('GAME_INGAME_UPGRADE', 'http://apps.pirates.go.com/pirates/redirect?redirectId=upgrade')
URL_MoreInfo = os.getenv('GAME_INGAME_MOREINFO', 'http://apps.pirates.go.com/pirates/redirect?redirectId=memopts')
URL_NamingGuidelines = os.getenv('GAME_INGAME_NAMING', 'http://apps.pirates.go.com/pirates/v3/#/help/name_approvals.html')
URL_FeedbackFormManageAccountURL = os.getenv('GAME_INGAME_MANAGE_ACCT', 'https://apps.pirates.go.com/pirates/v3/index?pageId=manageAccount')
RewardCongratulations = 'Congratulations!'
RewardBlackPearlComplete = 'Black Pearl Chapter Complete'
RewardBlackPearlReward = 'You have unlocked the Leadership sailing skill'
RewardBlackPearlDescription = 'This skill increases the rate of recharge for sailing and cannon\nskills.  Use it strategically to tip a battle against your foes!\n\nYou can replay the Black Pearl Quest anytime through\n Treasure Maps under the Lookout Panel.'
RewardNotorietyLessThanMax = 'Your Notoriety Level: %s\n Current Notoriety Level Cap: %s'
RewardNotorietyAtMax = 'You have reached the current Notoriety level cap of %s\n and mastered the following skills:'
RewardTodo = 'To become more notorious, continue to level your unmastered skills:'
RewardStayTuned = 'Stay tuned for more content expansions as the adventure continues!'
RewardLevelOfMax = 'Level %s of %s'
RewardLevelLocked = 'Locked'
RewardVoodooDollComplete = 'Voodoo Doll Quest Complete'
RewardVoodooDollReward = 'You have received the voodoo doll weapon'
RewardVoodooDollDescription = 'This weapon allows you to battle foes and heal friends!'
RewardDaggerComplete = 'Dagger Quest Complete'
RewardDaggerReward = 'You have received the dagger weapon'
RewardDaggerDescription = 'This weapon is handy for both close and range attacks!'
RewardVoodooStaffComplete = 'Voodoo Staff Quest Complete'
RewardVoodooStaffReward = 'You have received the voodoo staff weapon'
RewardVoodooStaffDescription = 'This weapon does not need to attune to a target,\nbut make sure it is fully charged!'
RewardGrenadeComplete = 'Grenade Quest Complete'
RewardGrenadeReward = 'You have received the grenade weapon'
RewardGrenadeDescription = 'Toss it to kill foes but stay clear from impact spot!'
CodeSubmitting = 'Redeeming Code %s'
CodeRedemptionGood = 'Code Redeemed'
CodeRedemptionBad = 'Code Redemption Failed. Perhaps the code was mistyped or already used'
ShipPVPQuestFrench = 'French'
ShipPVPQuestSpanish = 'Spanish'
ShipPVPQuestKillShip = 'ship'
ShipPVPQuestKillShipCap = 'Ship'
ShipPVPQuestKillPirate = 'pirate'
ShipPVPQuestKillPirateCap = 'Pirate'
ShipPVPQuestUseShip = 'ship'
ShipPVPQuestUseCannon = 'cannon'
ShipPVPQuestUseCannonCap = 'Cannon'
ShipPVPQuestGameName = 'Ship PVP'
ShipPVPQuestSingleNumA = 'Sink a \x01questObj\x01%s\x02 ship in \x01questObj\x01%s\x02'
ShipPVPQuestSingleNumB = 'Defeat a \x01questObj\x01%s\x02 pirate in \x01questObj\x01%s\x02'
ShipPVPQuestSingleAnyNumA = 'Sink a \x01questObj\x01ship\x02 in \x01questObj\x01%s\x02'
ShipPVPQuestSingleAnyNumB = 'Defeat a \x01questObj\x01pirate\x02 in \x01questObj\x01%s\x02'
ShipPVPQuestUsingA = ' using a \x01questObj\x01%s\x02'
ShipPVPQuestUsingACap = ' Using A %s'
ShipPVPQuestWithoutSinking = ' without sinking'
ShipPVPQuestWithoutSinkingCap = ' Without Sinking'
ShipPVPQuestMultA = 'Sink \x01questObj\x01%s %s\x02 ships in \x01questObj\x01%s\x02'
ShipPVPQuestMultB = 'Defeat \x01questObj\x01%s %s\x02 pirates in \x01questObj\x01%s\x02'
ShipPVPQuestMultAnyA = 'Sink \x01questObj\x01%s ships\x02 in \x01questObj\x01%s\x02'
ShipPVPQuestMultAnyB = 'Defeat \x01questObj\x01%s pirates\x02 in \x01questObj\x01%s\x02'
ShipPVPQuestDamageA = 'Do \x01questObj\x01%s\x02 points damage to \x01questObj\x01%s\x02 ships in \x01questObj\x01%s\x02'
ShipPVPQuestDamageB = 'Do \x01questObj\x01%s\x02 points damage to \x01questObj\x01%s\x02 pirates in \x01questObj\x01%s\x02'
ShipPVPQuestDamageAnyA = 'Do \x01questObj\x01%s\x02 points of damage to \x01questObj\x01ships\x02 in \x01questObj\x01%s\x02'
ShipPVPQuestDamageAnyB = 'Do \x01questObj\x01%s\x02 points of damage to \x01questObj\x01pirates\x02 in \x01questObj\x01%s\x02'
ShipPVPQuestDamageAnyC = 'Do \x01questObj\x01%s\x02 points of damage in \x01questObj\x01%s\x02'
ShipPVPQuestProgNumA = 'A %s %s Defeated In %s'
ShipPVPQuestProgNumB = 'A %s Defeated In %s'
ShipPVPQuestProgNumC = '%d/%d %s %ss Defeated In %s'
ShipPVPQuestProgNumD = '%d/%d %ss Defeated In %s'
ShipPVPQuestProgDamA = '%d/%d Points Of Damage To %s %ss In %s'
ShipPVPQuestProgDamB = '%d/%d Points Of Damage Against The %s In %s'
ShipPVPQuestProgDamC = '%d/%d Points Of Damage To %ss In %s'
ShipPVPQuestProgDamD = '%d/%d Points Of Damage In %s'
FeedbackFormTitle = 'Feedback Form'
FeedbackFormMessage = 'Please select a category from the list on the right and provide your feedback below. Thank you for helping us to improve the game!'
FeedbackFormCatItems = [
    'Quests',
    'Weapons',
    'Tech',
    'Ships',
    'PVP',
    'Social',
    'General',
    'Crews',
    'Guilds']
FeedbackButtonHelp = 'Send Feedback'
FeedbackFormSend = 'Send'
FeedbackManageButton = 'Manage Account'
townfolkHelpText = {
    1: [
        "Ready to fly the French colours on that ship of yers?\x07 Be aware that sailing from an island like this, ye must know a thing or two.\x07First, Pirates who choose to embark from this scrap of an island will be thrown into a battle... whether they be wantin' to or not.\x07Second, be wary of the sail colours around ye, that way a pirate knows whose friend and whose foe.\x07And if ye be needin' to check your score, press the ~ button. That gives a ships score AND it's bounty.\x07Pirates earn both for sinkin' enemy ships. The higher a bounty, the more it's worth.\x07Fair winds and good luck, mate... ye be needin' both!"],
    2: [
        "Ready to fly the Spanish colours on that ship of yers?\x07Be aware that sailing from an island like this, ye must know a thing or two.\x07First, Pirates who choose to embark from this scrap of an island will be thrown into a battle... whether they be wantin' to or not.\x07Second, be wary of the sail colours around ye, that way a pirate knows whose friend and whose foe.\x07And if ye be needin' to check your score, press the ~ button. That gives a ships score AND it's bounty.\x07Pirates earn both for sinkin' enemy ships. The higher a bounty, the more it's worth.\x07Fair winds and good luck, mate... ye be needin' both!"],
    3: [
        "Please excuse me master, Pierre le Porc, he's had a bit of stress lately and isn't feeling so grand.\x07In his... absence, I'll brief ye on the situation and specifics of how the French can use your skills.\x07See, Pirate Lord Le Porc has claimed this island and others as his own.\x07There's only one problem though, he's not the only Pirate Lord lookin' to lay claim on what ain't his, savvy?\x07A Spanish Pirate Lord name of Garcia de la Avaricia thinks he's running these islands too!\x07A pirate like yerself can make earn quite a reputation in this fight and Pierre would be most grateful.\x07So consider yerself a true Frenchmen when ye set sail from this island mate, 'cause the Spanish sure will..."],
    4: [
        "Please excuse me master, Garcia de la Avaricia, he's had a bit of stress lately and isn't feeling so grand.\x07In his... absence, I'll brief ye on the situation and specifics of how the Spanish can use your skills.\x07See, Pirate Lord Avaricia has claimed this island and others as his own.\x07There's only one problem though, he's not the only Pirate Lord looking to lay claim on what ain't his, savvy?\x07A French Pirate Lord name of Le Porc thinks he's running these islands too!\x07A pirate like yerself can make earn quite a reputation in this fight and Garcia would be most grateful.\x07So consider yerself a true Spaniard when ye set sail from this island mate, 'cause the French sure will..."]}
MAGICWORD_GMNAMETAG = 'GM NameTag Options:\nenable, disable, setString <string>,\nsetColor <red|green|blue|gold|white>'
CarverAcquired = 'Carver has rejoined the Black Pearl Crew!'
GordonAcquired = 'Gordon Greer has rejoined the Black pearl Crew!'
HendryAcquired = 'Hendry Cutts has rejoined the Black pearl Crew!'
NillAcquired = 'Nill Offrill has rejoined the Black pearl Crew!'
LeCerdoAcquired = 'Le Cerdo has rejoined the Black pearl Crew!'
GunnerAcquired = 'Gunner has rejoined the Black pearl Crew!'
ScaryMaryAcquired = 'Scary Mary has rejoined the Black pearl Crew!'
GiladogaAcquired = 'Giladoga has rejoined the Black pearl Crew!'
JohnAcquired = 'John Smith has rejoined the Black pearl Crew!'
CarverName = 'Carver'
GordonName = 'Gordon Greer'
HendryName = 'Hendry Cutts'
NillName = 'Nill Offrill'
LeCerdoName = 'Le Cerdo'
GunnerName = 'Gunner'
ScaryMaryName = 'Scary Mary'
GiladogaName = 'Giladoga'
JohnName = 'John Smith'
SongTitleUnknown = '???'
SongComingSoon = 'Coming Soon...'
SongUndiscovered = 'Undiscovered'
ZombieNoDoors = 'This door is barricaded from the inside!'
ZombieNoBoats = 'Jolly Roger commands you to attack the island!'
ZombieNoPeople = 'We will never serve Jolly Roger!'
ShipRepaired = 'Your ship has been repaired.'

def getServerTimeString(secondsSinceEpoch):
    import datetime
    return 'Server Time: %s' % datetime.datetime.fromtimestamp(secondsSinceEpoch).ctime()

