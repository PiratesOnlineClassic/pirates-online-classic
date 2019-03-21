from pirates.pirate import AvatarTypes
from pirates.piratesbase import PLocalizer
import random
CANCEL = 0
TALK = 1
TRADE = 2
DUEL = 3
QUEST = 4
SHIPS = 5
STORE = 6
REPAIR = 7
UPGRADE = 8
HEAL_HP = 9
HEAL_MOJO = 10
TRAIN = 11
SAIL = 12
SAILTM = 13
BRIBE = 14
OVERHAUL = 15
SELL_SHIPS = 16
ACCESSORIES_STORE = 17
TATTOO_STORE = 18
JEWELRY_STORE = 19
BARBER_STORE = 20
RESPEC = 21
RESPEC_CUTLASS = 22
RESPEC_PISTOL = 23
RESPEC_DAGGER = 24
RESPEC_DOLL = 25
RESPEC_GRENADE = 26
RESPEC_STAFF = 27
RESPEC_SAILING = 28
RESPEC_CANNON = 29
BACK = 30
MUSICIAN = 31
PVP_REWARDS_TATTOO = 32
PVP_REWARDS_EYE_PATCHES = 33
PVP_REWARDS_HATS = 34
InteractOptionNames = {
    CANCEL: PLocalizer.InteractCancel,
    TALK: PLocalizer.InteractTalk,
    TRADE: PLocalizer.InteractTrade,
    DUEL: PLocalizer.InteractDuel,
    QUEST: PLocalizer.InteractQuest,
    SHIPS: PLocalizer.InteractShips,
    SELL_SHIPS: PLocalizer.InteractSellShips,
    STORE: PLocalizer.InteractStore,
    REPAIR: PLocalizer.InteractRepair,
    OVERHAUL: PLocalizer.InteractOverhaul,
    UPGRADE: PLocalizer.InteractUpgrade,
    HEAL_HP: PLocalizer.InteractHealHp,
    HEAL_MOJO: PLocalizer.InteractHealMojo,
    TRAIN: PLocalizer.InteractTrain,
    SAIL: PLocalizer.InteractSail,
    SAILTM: PLocalizer.InteractSailTM,
    BRIBE: PLocalizer.InteractBribe,
    ACCESSORIES_STORE: PLocalizer.InteractStore,
    TATTOO_STORE: PLocalizer.InteractStore,
    JEWELRY_STORE: PLocalizer.InteractStore,
    BARBER_STORE: PLocalizer.InteractStore,
    RESPEC: PLocalizer.InteractRespec,
    RESPEC_CUTLASS: PLocalizer.InteractRespecCutlass,
    RESPEC_PISTOL: PLocalizer.InteractRespecPistol,
    RESPEC_DAGGER: PLocalizer.InteractRespecDagger,
    RESPEC_DOLL: PLocalizer.InteractRespecDoll,
    RESPEC_GRENADE: PLocalizer.InteractRespecGrenade,
    RESPEC_STAFF: PLocalizer.InteractRespecStaff,
    RESPEC_SAILING: PLocalizer.InteractRespecSailing,
    RESPEC_CANNON: PLocalizer.InteractRespecCannon,
    BACK: PLocalizer.InteractBack,
    MUSICIAN: PLocalizer.InteractMusician,
    PVP_REWARDS_TATTOO: PLocalizer.InteractPvPTattoo,
    PVP_REWARDS_EYE_PATCHES: PLocalizer.InteractPvPEyePatch,
    PVP_REWARDS_HATS: PLocalizer.InteractPvPHat}
InteractOptionHelpText = {
    CANCEL: PLocalizer.InteractCancelHelp,
    TALK: PLocalizer.InteractTalkHelp,
    TRADE: PLocalizer.InteractTradeHelp,
    DUEL: PLocalizer.InteractDuelHelp,
    QUEST: PLocalizer.InteractQuestHelp,
    SHIPS: PLocalizer.InteractShipsHelp,
    SELL_SHIPS: PLocalizer.InteractSellShipsHelp,
    STORE: PLocalizer.InteractStoreHelp,
    REPAIR: PLocalizer.InteractRepairHelp,
    OVERHAUL: PLocalizer.InteractOverhaulHelp,
    UPGRADE: PLocalizer.InteractUpgradeHelp,
    HEAL_HP: PLocalizer.InteractHealHpHelp,
    HEAL_MOJO: PLocalizer.InteractHealMojoHelp,
    TRAIN: PLocalizer.InteractTrainHelp,
    SAIL: PLocalizer.InteractSailHelp,
    SAILTM: PLocalizer.InteractSailTMHelp,
    BRIBE: PLocalizer.InteractBribeHelp,
    ACCESSORIES_STORE: PLocalizer.InteractStoreHelp,
    TATTOO_STORE: PLocalizer.InteractStoreHelp,
    JEWELRY_STORE: PLocalizer.InteractStoreHelp,
    BARBER_STORE: PLocalizer.InteractStoreHelp,
    RESPEC: PLocalizer.InteractRespecHelp,
    RESPEC_CUTLASS: PLocalizer.InteractRespecHelp,
    RESPEC_PISTOL: PLocalizer.InteractRespecHelp,
    RESPEC_DAGGER: PLocalizer.InteractRespecHelp,
    RESPEC_DOLL: PLocalizer.InteractRespecHelp,
    RESPEC_GRENADE: PLocalizer.InteractRespecHelp,
    RESPEC_STAFF: PLocalizer.InteractRespecHelp,
    RESPEC_SAILING: PLocalizer.InteractRespecHelp,
    RESPEC_CANNON: PLocalizer.InteractRespecHelp,
    BACK: PLocalizer.InteractBackHelp,
    MUSICIAN: PLocalizer.InteractMusicianHelp,
    PVP_REWARDS_TATTOO: PLocalizer.InteractPvPTattooHelp,
    PVP_REWARDS_EYE_PATCHES: PLocalizer.InteractPvPEyePatchHelp,
    PVP_REWARDS_HATS: PLocalizer.InteractPvPHatHelp}
__NPCInteractMenus = {
    AvatarTypes.Townfolk: (PLocalizer.TownfolkMenuTitle, [
        QUEST,
        BRIBE,
        HEAL_HP,
        CANCEL]),
    AvatarTypes.Cast: (PLocalizer.CastMenuTitle, [
        QUEST,
        BRIBE,
        CANCEL]),
    AvatarTypes.Commoner: (PLocalizer.CommonerMenuTitle, [
        QUEST,
        BRIBE,
        HEAL_HP,
        CANCEL]),
    AvatarTypes.Peasant: (PLocalizer.PeasantMenuTitle, [
        QUEST,
        BRIBE,
        HEAL_HP,
        CANCEL]),
    AvatarTypes.StoreOwner: (PLocalizer.StoreOwnerMenuTitle, [
        QUEST,
        STORE,
        BRIBE,
        CANCEL]),
    AvatarTypes.Gypsy: (PLocalizer.GypsyMenuTitle, [
        QUEST,
        STORE,
        BRIBE,
        HEAL_MOJO,
        CANCEL]),
    AvatarTypes.Blacksmith: (PLocalizer.BlacksmithMenuTitle, [
        QUEST,
        STORE,
        BRIBE,
        CANCEL]),
    AvatarTypes.Shipwright: (PLocalizer.ShipwrightMenuTitle, [
        QUEST,
        SHIPS,
        REPAIR,
        SELL_SHIPS,
        BRIBE,
        CANCEL]),
    AvatarTypes.Merchant: (PLocalizer.MerchantMenuTitle, [
        QUEST,
        STORE,
        BRIBE,
        CANCEL]),
    AvatarTypes.Cannoneer: (PLocalizer.CannoneerMenuTitle, [
        QUEST,
        STORE,
        BRIBE,
        CANCEL]),
    AvatarTypes.Bartender: (PLocalizer.BartenderMenuTitle, [
        QUEST,
        BRIBE,
        HEAL_HP,
        CANCEL]),
    AvatarTypes.Gunsmith: (PLocalizer.GunsmithMenuTitle, [
        QUEST,
        STORE,
        BRIBE,
        CANCEL]),
    AvatarTypes.Grenadier: (PLocalizer.GrenadierMenuTitle, [
        QUEST,
        STORE,
        BRIBE,
        CANCEL]),
    AvatarTypes.MedicineMan: (PLocalizer.MedicineManMenuTitle, [
        QUEST,
        STORE,
        BRIBE,
        CANCEL]),
    AvatarTypes.Tailor: (PLocalizer.ShopTailor, [
        QUEST,
        ACCESSORIES_STORE,
        CANCEL]),
    AvatarTypes.Tattoo: (PLocalizer.ShopTattoo, [
        QUEST,
        TATTOO_STORE,
        CANCEL]),
    AvatarTypes.Jeweler: (PLocalizer.ShopJewelry, [
        QUEST,
        JEWELRY_STORE,
        CANCEL]),
    AvatarTypes.Barber: (PLocalizer.ShopBarber, [
        QUEST,
        BARBER_STORE,
        CANCEL]),
    AvatarTypes.Trainer: (PLocalizer.TrainerMenuTitle, [
        QUEST,
        RESPEC,
        BRIBE,
        CANCEL]),
    AvatarTypes.Musician: (PLocalizer.ShopMusician, [
        MUSICIAN,
        CANCEL]),
    AvatarTypes.PvPRewards: (PLocalizer.ShopPvP, [
        QUEST,
        PVP_REWARDS_TATTOO,
        PVP_REWARDS_EYE_PATCHES,
        PVP_REWARDS_HATS,
        BRIBE,
        CANCEL])}

def getNPCInteractMenu(avatarType):
    menuChoices = __NPCInteractMenus.get(avatarType)
    return menuChoices


ShipwrightNoSwordWarning = 0
ShipwrightTutorial1 = 1
BlacksmithTutorial1 = 11
BlacksmithTutorial2 = 12
GypsyTutorial1 = 21
__NPCTutorialDict = {
    ShipwrightNoSwordWarning: 'quest_tut_shipwright_warning_100',
    ShipwrightTutorial1: 'quest_tut_shipwright_intro_100',
    BlacksmithTutorial1: 'quest_tut_blacksmith_intro_100',
    BlacksmithTutorial2: 'quest_tut_blacksmith_intro_101',
    GypsyTutorial1: 'quest_tut_gypsy_intro_100'}

def getNPCTutorial(index):
    tutorial = __NPCTutorialDict.get(index)
    return tutorial


__NPCSalutations = {
    AvatarTypes.Townfolk: (PLocalizer.TownfolkGreetings, PLocalizer.TownfolkGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Cast: (PLocalizer.TownfolkGreetings, PLocalizer.TownfolkGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Commoner: (PLocalizer.TownfolkGreetings, PLocalizer.TownfolkGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Peasant: (PLocalizer.TownfolkGreetings, PLocalizer.TownfolkGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.StoreOwner: (PLocalizer.FormalGreetings, PLocalizer.FormalGoodbyes, PLocalizer.TownfolkEncourage),
    AvatarTypes.Gypsy: (PLocalizer.GypsyGreetings, PLocalizer.GypsyGoodbyes, PLocalizer.GypsyEncourage, PLocalizer.GypsyBrushoff),
    AvatarTypes.Blacksmith: (PLocalizer.FormalGreetings, PLocalizer.FormalGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Shipwright: (PLocalizer.PirateGreetings, PLocalizer.PirateGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Merchant: (PLocalizer.FormalGreetings, PLocalizer.FormalGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Bartender: (PLocalizer.PirateGreetings, PLocalizer.PirateGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Gunsmith: (PLocalizer.PirateGreetings, PLocalizer.PirateGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Grenadier: (PLocalizer.FormalGreetings, PLocalizer.FormalGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Cannoneer: (PLocalizer.PirateGreetings, PLocalizer.PirateGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.MedicineMan: (PLocalizer.GypsyGreetings, PLocalizer.GypsyGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Tailor: (PLocalizer.FormalGreetings, PLocalizer.FormalGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Tattoo: (PLocalizer.FormalGreetings, PLocalizer.FormalGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Jeweler: (PLocalizer.FormalGreetings, PLocalizer.FormalGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Barber: (PLocalizer.FormalGreetings, PLocalizer.FormalGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Trainer: (PLocalizer.FormalGreetings, PLocalizer.FormalGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.Musician: (PLocalizer.FormalGreetings, PLocalizer.FormalGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff),
    AvatarTypes.PvPRewards: (PLocalizer.PirateGreetings, PLocalizer.PirateGoodbyes, PLocalizer.TownfolkEncourage, PLocalizer.TownfolkBrushoff) }


def getNPCGreeting(avatarType):
    dialogue = random.choice(__NPCSalutations.get(avatarType)[0])
    return dialogue


def getNPCGoodbye(avatarType):
    dialogue = random.choice(__NPCSalutations.get(avatarType)[1])
    return dialogue


def getNPCDuring(avatarType):
    dialogue = random.choice(__NPCSalutations.get(avatarType)[2])
    return dialogue


def getNPCBrushoff(avatarType):
    dialogue = random.choice(__NPCSalutations.get(avatarType)[3])
    return dialogue


DISABLED = 0
NORMAL = 1
HIGHLIGHT = 2
