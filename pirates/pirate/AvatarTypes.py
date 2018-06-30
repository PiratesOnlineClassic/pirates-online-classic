import random

from pirates.pirate.AvatarType import AvatarType
from pirates.pirate.AvatarTypeSet import AvatarTypeSet
from pirates.piratesbase import PLocalizer as PL

AnyAvatar = AvatarType()
AnyShip = AvatarType()
BossType = AvatarType(boss=1)
MovieCasts = tuple((AvatarType() for x in range(6)))
JackSparrow, ElizabethSwan, CaptBarbossa, WillTurner, TiaDalma, JoshameeGibbs = MovieCasts
Factions = tuple((AvatarType(faction=x) for x in range(6)))
Undead, Navy, Creature, Townfolk, Pirate, TradingCo = Factions
CreatureTracks = tuple((AvatarType(base=Creature, track=x) for x in range(5)))
LandCreature, SeaCreature, AirCreature, SeaMonster, Animal = CreatureTracks
LandCreatures = tuple((AvatarType(base=LandCreature, id=x) for x in range(16)))
Crab, RockCrab, GiantCrab, Chicken, Rooster, Pig, Stump, FlyTrap, Scorpion, DreadScorpion, Alligator, BigGator, HugeGator, Dog, Seagull, Monkey = LandCreatures
LandCrab = AvatarTypeSet(PL.LandCrabStrings, Crab, RockCrab, GiantCrab)
Animals = tuple((AvatarType(base=Animal, id=x) for x in range(5)))
Chicken, Rooster, Pig, Dog, Seagull = Animals
SeaCreatures = tuple((AvatarType(base=SeaCreature, id=x) for x in range(1)))
Fish, = SeaCreatures
AirCreatures = tuple((AvatarType(base=AirCreature, id=x) for x in range(5)))
Seagull, Bat, VampireBat, Wasp, AngryWasp = AirCreatures
SeaMonsters = tuple((AvatarType(base=SeaMonster, id=x) for x in range(6)))
SeaKraken, Kraken, KrakenBody, GrabberTentacle, HolderTentacle, SeaSerpent = SeaMonsters
UndeadTracks = tuple((AvatarType(base=Undead, track=x) for x in range(8)))
Earth, Air, Fire, Water, Classic, Boss, French, Spanish = UndeadTracks
EarthUndead = tuple((AvatarType(base=Earth, id=x) for x in range(10)))
Clod, Sludge, Mire, Muck, Corpse, Carrion, Cadaver, Zombie, CaptMudmoss, Mossman = EarthUndead
AirUndead = tuple((AvatarType(base=Air, id=x) for x in range(10)))
Whiff, Reek, Billow, Stench, Shade, Specter, Phantom, Wraith, CaptZephyr, Squall = AirUndead
FireUndead = tuple((AvatarType(base=Fire, id=x) for x in range(10)))
Glint, Flicker, Smolder, Spark, Imp, Brand, Lumen, Fiend, CaptCinderbones, Torch = FireUndead
WaterUndead = tuple((AvatarType(base=Water, id=x) for x in range(10)))
Drip, Damp, Drizzle, Spray, Splatter, Drool, Drench, Douse, CaptBriney, Spout = WaterUndead
ClassicUndead = list()
BossUndead = tuple((AvatarType(base=Boss, id=x) for x in range(1)))
JollyRoger, = BossUndead
FrenchUndead = tuple((AvatarType(base=French, id=x) for x in range(4)))
FrenchUndeadA, FrenchUndeadB, FrenchUndeadC, FrenchUndeadD = FrenchUndead
SpanishUndead = tuple((AvatarType(base=Spanish, id=x) for x in range(4)))
SpanishUndeadA, SpanishUndeadB, SpanishUndeadC, SpanishUndeadD = SpanishUndead
UndeadCommon = (EarthUndead[0], EarthUndead[1])
UndeadUncommon = ()
UndeadRare = ()
UndeadUltraRare = ()
AllUndead = []
AllUndead.extend(UndeadCommon)
AllUndead.extend(UndeadUncommon)
AllUndead.extend(UndeadRare)


def pickUndead(minVal, maxVal, undeadType=EarthUndead):
    return undeadType[random.randint(minVal, maxVal)]


def pickEarthUndead(minVal=0, maxVal=len(EarthUndead) - 1):
    return EarthUndead[random.randint(minVal, maxVal)]


def pickWaterUndead(minVal=0, maxVal=len(WaterUndead) - 1):
    return WaterUndead[random.randint(minVal, maxVal)]


def pickSpanishUndead(minVal=0, maxVal=len(SpanishUndead) - 1):
    return SpanishUndead[random.randint(minVal, maxVal)]


def pickFrenchUndead(minVal=0, maxVal=len(FrenchUndead) - 1):
    return FrenchUndead[random.randint(minVal, maxVal)]


def randomUndead(level):
    retval = level / 3
    rnd = random.randint(0, 14)
    if rnd < 5:
        retval -= 1
    else:
        if rnd > 12:
            retval += 1
    if retval < 0:
        retval = 0
    if retval > 7:
        retval = 7
    return EarthUndead[retval]


NavyTracks = tuple((AvatarType(base=Navy, track=x) for x in range(3)))
Soldier, Marksman, Leader = NavyTracks
Soldiers = tuple((AvatarType(base=Soldier, id=x) for x in range(5)))
Axeman, Swordsman, RoyalGuard, MasterSwordsman, WeaponsMaster = Soldiers
Marksmen = tuple((AvatarType(base=Marksman, id=x) for x in range(5)))
Cadet, Guard, Sergeant, Veteran, Officer = Marksmen
Leaders = tuple((AvatarType(base=Leader, id=x) for x in range(5)))
FirstMate, Captain, Lieutenant, Admiral, Commodore = Leaders
NavyCommon = (Cadet, Guard, Sergeant, Veteran, Officer)


def randomNavy(level):
    retval = level / 4
    rnd = random.randint(0, 14)
    if rnd < 5:
        retval -= 1
    else:
        if rnd > 12:
            retval += 1
    if retval < 0:
        retval = 0
    if retval > 4:
        retval = 4
    return Marksmen[retval]


def pickTrading(tradlow, tradhigh):
    return Mercenaries[random.randint(tradlow, tradhigh)]


def pickNavy(navylow, navyhigh):
    return Marksmen[random.randint(navylow, navyhigh)]


TownfolkTracks = tuple((AvatarType(base=Townfolk, track=x) for x in range(3)))
Commoner, StoreOwner, Cast = TownfolkTracks
Commoners = tuple((AvatarType(base=Commoner, id=x) for x in range(1)))
Peasant = Commoners
StoreOwners = tuple((AvatarType(base=StoreOwner, id=x) for x in range(16)))
Gypsy, Blacksmith, Shipwright, Cannoneer, Merchant, Bartender, Gunsmith, Grenadier, MedicineMan, Tailor, Tattoo, Jeweler, Barber, Musician, Trainer, PvPRewards = StoreOwners
PirateTracks = tuple((AvatarType(base=Pirate, track=x) for x in range(3)))
Player, Brawler, Gunner = PirateTracks
Players = tuple((AvatarType(base=Player, id=x) for x in range(2)))
LocalPirateType, NonLocalPirateType = Players
Brawlers = tuple((AvatarType(base=Brawler, id=x) for x in range(5)))
Landlubber, Scallywag, Buccaneer, Swashbuckler, Warmonger = Brawlers
Gunners = tuple((AvatarType(base=Gunner, id=x) for x in range(5)))
Bandit, Brigand, Sharpshooter, Rifleman, Gunner = Gunners
TradingCoTracks = tuple((AvatarType(base=TradingCo, track=x) for x in range(3)))
Mercenary, Assassin, Official = TradingCoTracks
Mercenaries = tuple((AvatarType(base=Mercenary, id=x) for x in range(5)))
Thug, Grunt, Hiredgun, Mercenary, Assassin = Mercenaries
Officials = tuple((AvatarType(base=Official, id=x) for x in range(5)))
OffA, OffB, OffC, OffD, Viceroy = Officials
Assassins = tuple((AvatarType(base=Assassin, id=x) for x in range(5)))
Rogue, Stalker, Cutthroat, Executioner, Professional = Assassins
AVATAR_TYPE_IDX = 0


def typePassthrough(type):
    return type


NPC_SPAWNABLES = {
    'Skeleton': [lambda p0=0, p1=3: pickEarthUndead(p0, p1)],
    'EvilNavy': [lambda p0=0, p1=1: pickNavy(p0, p1)],
    'Noob Skeleton': [lambda p0=0: pickEarthUndead(p0, p0)],
    'Low Skeleton': [lambda p0=0, p1=1: pickEarthUndead(p0, p1)],
    'Early Skeleton': [lambda p0=1, p1=2: pickEarthUndead(p0, p1)],
    'Mid Skeleton': [lambda p0=2, p1=3: pickEarthUndead(p0, p1)],
    'Mean Skeleton': [lambda p0=3, p1=4: pickEarthUndead(p0, p1)],
    'High Skeleton': [lambda p0=4, p1=5: pickEarthUndead(p0, p1)],
    'Fierce Skeleton': [lambda p0=5, p1=6: pickEarthUndead(p0, p1)],
    'Elite Skeleton': [lambda p0=6, p1=7: pickEarthUndead(p0, p1)],
    'Low EITC': [lambda p0=1: pickTrading(p0, p0)],
    'Mid EITC': [lambda p0=1, p1=3: pickTrading(p0, p1)],
    'High EITC': [lambda p0=3, p1=4: pickTrading(p0, p1)],
    'Crab': [lambda p0=Crab: typePassthrough(p0)],
    'Rock Crab': [lambda p0=RockCrab: typePassthrough(p0)],
    'Giant Crab': [lambda p0=GiantCrab: typePassthrough(p0)],
    'Scorpion': [lambda p0=Scorpion: typePassthrough(p0)],
    'Dread Scorpion': [lambda p0=DreadScorpion: typePassthrough(p0)],
    'Alligator': [lambda p0=Alligator: typePassthrough(p0)],
    'Big Gator': [lambda p0=BigGator: typePassthrough(p0)],
    'Huge Gator': [lambda p0=HugeGator: typePassthrough(p0)],
    'Bat': [lambda p0=Bat: typePassthrough(p0)],
    'Vampire Bat': [lambda p0=VampireBat: typePassthrough(p0)],
    'Wasp': [lambda p0=Wasp: typePassthrough(p0)],
    'Angry Wasp': [lambda p0=AngryWasp: typePassthrough(p0)],
    'FlyTrap': [lambda p0=FlyTrap: typePassthrough(p0)],
    'Stump': [lambda p0=Stump: typePassthrough(p0)],
    'Noob Navy': [lambda p0=0: pickNavy(p0, p0)],
    'Low Navy': [lambda p0=0, p1=1: pickNavy(p0, p1)],
    'Mid Navy': [lambda p0=2, p1=3: pickNavy(p0, p1)],
    'High Navy': [lambda p0=3, p1=4: pickNavy(p0, p1)],
    'Low DJCrew': [lambda p0=0, p1=1: pickWaterUndead(p0, p1)],
    'Early DJCrew': [lambda p0=1, p1=2: pickWaterUndead(p0, p1)],
    'Mid DJCrew': [lambda p0=2, p1=3: pickWaterUndead(p0, p1)],
    'Mean DJCrew': [lambda p0=3, p1=4: pickWaterUndead(p0, p1)],
    'High DJCrew': [lambda p0=4, p1=5: pickWaterUndead(p0, p1)],
    'Fierce DJCrew': [lambda p0=5, p1=6: pickWaterUndead(p0, p1)],
    'Elite DJCrew': [lambda p0=6, p1=7: pickWaterUndead(p0, p1)],
    'Area': [lambda p0=0, p1=3: pickEarthUndead(p0, p1)],
    'French Undead': [lambda p0=0, p1=3: pickFrenchUndead(p0, p1)],
    'French Undead Low': [lambda p0=0, p1=1: pickFrenchUndead(p0, p1)],
    'French Undead Mid': [lambda p0=1, p1=2: pickFrenchUndead(p0, p1)],
    'French Undead High': [lambda p0=2, p1=3: pickFrenchUndead(p0, p1)],
    'French Undead Maitre': [lambda p0=FrenchUndeadA: typePassthrough(p0)],
    'French Undead Quarter Master':
    [lambda p0=FrenchUndeadB: typePassthrough(p0)],
    'French Undead Lieutenant': [lambda p0=FrenchUndeadC: typePassthrough(p0)],
    'French Undead Capitaine': [lambda p0=FrenchUndeadD: typePassthrough(p0)],
    'Spanish Undead': [lambda p0=0, p1=3: pickSpanishUndead(p0, p1)],
    'Spanish Undead Low': [lambda p0=0, p1=1: pickSpanishUndead(p0, p1)],
    'Spanish Undead Mid': [lambda p0=1, p1=2: pickSpanishUndead(p0, p1)],
    'Spanish Undead High': [lambda p0=2, p1=3: pickSpanishUndead(p0, p1)],
    'Spanish Undead Conquistador':
    [lambda p0=SpanishUndeadA: typePassthrough(p0)],
    'Spanish Undead Bandido': [lambda p0=SpanishUndeadB: typePassthrough(p0)],
    'Spanish Undead Pirata': [lambda p0=SpanishUndeadC: typePassthrough(p0)],
    'Spanish Undead Captain': [lambda p0=SpanishUndeadD: typePassthrough(p0)]
}

NPC_SPAWNABLES_KEYS = [
    'Noob Skeleton', 'Low Skeleton', 'Early Skeleton', 'Mid Skeleton',
    'Mean Skeleton', 'High Skeleton', 'Fierce Skeleton', 'Elite Skeleton',
    'Low EITC', 'Mid EITC', 'High EITC', 'Crab', 'Rock Crab', 'Giant Crab',
    'Scorpion', 'Dread Scorpion', 'Alligator', 'Big Gator', 'Huge Gator', 'Bat',
    'Vampire Bat', 'Wasp', 'Angry Wasp', 'FlyTrap', 'Stump', 'Noob Navy',
    'Low Navy', 'Mid Navy', 'High Navy', 'Low DJCrew', 'Early DJCrew',
    'Mid DJCrew', 'Mean DJCrew', 'High DJCrew', 'Fierce DJCrew', 'Elite DJCrew',
    'Area', 'French Undead', 'French Undead Low', 'French Undead Mid',
    'French Undead High', 'French Undead Maitre',
    'French Undead Quarter Master', 'French Undead Lieutenant',
    'French Undead Capitaine', 'Spanish Undead', 'Spanish Undead Low',
    'Spanish Undead Mid', 'Spanish Undead High', 'Spanish Undead Conquistador',
    'Spanish Undead Bandido', 'Spanish Undead Pirata', 'Spanish Undead Captain'
]


def buildEditorSpawnableTypes():
    category = [[
        ['Cadet', 'Guard', 'Sergeant', 'Veteran', 'Officer'], 'Navy - '
    ], [['Thug', 'Grunt', 'Hiredgun', 'Mercenary', 'Assassin'], 'EITC - '], [[
        'Clod', 'Sludge', 'Mire', 'Muck', 'Corpse', 'Carrion', 'Cadaver',
        'Zombie', 'CaptMudmoss', 'Mossman', 'Drip', 'Damp', 'Drizzle', 'Spray',
        'Splatter', 'Drool', 'Drench', 'Douse', 'CaptBriney', 'Spout'
    ], 'Undead - ']]
    for currCategory in category:
        for currType in currCategory[0]:
            name = currCategory[1] + currType
            NPC_SPAWNABLES[name] = [
                lambda p0=eval(currType): typePassthrough(p0)
            ]
            NPC_SPAWNABLES_KEYS.append(name)


buildEditorSpawnableTypes()
