"""
The server side of the Freebooter (Basic Access) velvet rope.

Every restriction the client puts on a Freebooter (see Freebooter.py and the
"Unlimited Access" upsells in piratesgui) is checked here, so the AI and
UberDOG enforce them the same way everywhere. With want-membership off (the
default) everybody has Unlimited Access and nothing here restricts anyone.
"""

from otp.otpbase import OTPGlobals
from pirates.battle import WeaponGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import ItemType
from pirates.piratesbase import Freebooter
from pirates.piratesbase import MembershipGlobals
from pirates.quest.QuestConstants import LocationIds
from pirates.reputation import ReputationGlobals
from pirates.ship import ShipGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

# The only ships a Freebooter may buy, deploy or board as captain,
# see ShipStoreGUI and ShipFrameDeploy:
FreeShipClasses = (ShipGlobals.INTERCEPTORL1, ShipGlobals.MERCHANTL1)

# The places only members may go to, see DistributedIsland.enterSneak
# (Kingshead island) and DistributedDoorBase.requestInteraction (the fort):
PaidAreas = (LocationIds.KINGSHEAD_ISLAND, LocationIds.KINGSHEAD_DOOR)

# Freebooter.FreeLevelCap holds every other reputation (the weapons, sailing,
# cannon...) and FreeOverallLevelCap holds the notoriety (OverallRep):
NotCappedReputation = (InventoryType.GeneralRep,)


def wantMembership():
    return MembershipGlobals.wantMembership()


def isPaidAccess(access):
    """
    Returns True when the access level (OTPGlobals.Access*) is Unlimited Access.
    """

    if not wantMembership() or Freebooter.AllAccessHoliday:
        return True

    return access == OTPGlobals.AccessFull


def getEffectiveAccess(access):
    """
    The access the client sees, see DistributedPlayerPirate.getAccess.
    """

    if isPaidAccess(access):
        return OTPGlobals.AccessFull

    return access


def isPaid(avatar):
    """
    Returns True when the avatar has Unlimited Access. Anything that is not a
    player (npcs, ships...) is never held back by the velvet rope.
    """

    if avatar is None:
        return False

    if not hasattr(avatar, 'isPaid'):
        return True

    return bool(avatar.isPaid())


def canUseWeapon(avatar, repId):
    return isPaid(avatar) or Freebooter.allowedFreebooterWeapon(repId)


def canUseSkill(avatar, skillId):
    """
    Covers weapon skills, ammo, cannon ammo, ship skills and items alike,
    see WeaponGlobals.canFreeUse and Freebooter.pruneFreebooterSkills.
    """

    return not skillId or isPaid(avatar) or bool(WeaponGlobals.canFreeUse(skillId))


def canTrainSkill(avatar, skillId, newQuantity, weaponLevel, unspent):
    """
    Returns True when the avatar may raise the skill to newQuantity, a skill
    unlocked but never trained has a quantity of 1. See SkillPage.addPoint.
    """

    if isPaid(avatar):
        return True

    if not WeaponGlobals.canFreeUse(skillId):
        return False

    if newQuantity > Freebooter.FreeSkillCap:
        return False

    # the skill points spent on the weapon so far...
    if weaponLevel - 1 - unspent >= Freebooter.FreeMaxSkillSpend:
        return False

    return True


def canBuyItem(avatar, itemId):
    """
    The general stores only sell a Freebooter consumables and ammunition,
    see InventoryItemGui.checkFreebooter. Ships are checked by canUseShipClass.
    """

    if isPaid(avatar):
        return True

    if EconomyGlobals.getItemCategory(itemId) == ItemType.CONSUMABLE:
        return True

    for begin, end in ((InventoryType.begin_WeaponCannonAmmo, InventoryType.end_WeaponCannonAmmo),
                       (InventoryType.begin_WeaponPistolAmmo, InventoryType.end_WeaponGrenadeAmmo),
                       (InventoryType.begin_WeaponDaggerAmmo, InventoryType.end_WeaponDaggerAmmo)):
        if begin <= itemId <= end:
            return True

    return False


def canUseCosmetics(avatar):
    """
    The tailor, jeweler, tattoo parlor and barber only serve members,
    see the Accessories/Jewelry/Tattoo/BarberStoreGUI velvet rope.
    """

    return isPaid(avatar)


def canUseShipClass(avatar, shipClass):
    return isPaid(avatar) or shipClass in FreeShipClasses


def canEnterArea(avatar, uniqueId):
    return isPaid(avatar) or uniqueId not in PaidAreas


def canStartTreasureMap(avatar):
    """
    See QuestPage.startTreasureMap.
    """

    return isPaid(avatar)


def canProgressQuest(avatar, questDNA):
    """
    A velvet roped quest cannot be progressed by a Freebooter,
    see Quest.handleEvent.
    """

    return isPaid(avatar) or not questDNA.getVelvetRoped()


def getReputationCap(avatar, repType):
    """
    Returns the most reputation the avatar may have of the type, or None when
    the avatar is not held to a cap.
    """

    if isPaid(avatar) or repType in NotCappedReputation:
        return None

    if repType == InventoryType.OverallRep:
        return ReputationGlobals.GlobalReputationAtLevel[Freebooter.FreeOverallLevelCap]

    return ReputationGlobals.TotalReputationAtLevel[Freebooter.FreeLevelCap]


def capReputation(avatar, repType, currentRep, newRep):
    """
    Returns the reputation the avatar ends up with. A Freebooter stops earning
    reputation at the level caps, reputation already earned (as a member) is
    never taken away.
    """

    cap = getReputationCap(avatar, repType)
    if cap is None or newRep <= currentRep:
        return newRep

    return max(currentRep, min(newRep, cap))


def isAtOverallLevelCap(avatar):
    """
    A Freebooter at the overall level cap no longer earns anything for
    defeating enemies.
    """

    return not isPaid(avatar) and avatar.getLevel() >= Freebooter.FreeOverallLevelCap
