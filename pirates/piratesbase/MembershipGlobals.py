"""
The account side of membership (Basic Access "Freebooters" and Unlimited
Access members), shared by the client and the UberDOG. It only needs the
config, unlike Freebooter.py it does not load the game resources.
"""

from panda3d.core import ConfigVariableBool, ConfigVariableInt

from otp.otpbase import OTPGlobals

# Every account has the same number of pirate slots on the avatar chooser, a
# Freebooter may only fill some of them, the rest are "Unlimited Access Only"
# (see AvatarChooser and PLocalizer.VR_Head_Account):
AvatarSlots = 4
FreeAvatars = 2


def wantMembership():
    # with want-membership off (the default) every account has Unlimited Access...
    return ConfigVariableBool('want-membership', False).getValue()


def getMaxAvatars(access):
    """
    Returns how many of the account's avatar slots may hold a pirate.
    """

    if not wantMembership() or access == OTPGlobals.AccessFull:
        return AvatarSlots

    return max(0, min(AvatarSlots, ConfigVariableInt('freebooter-max-avatars', FreeAvatars).getValue()))


def getAvatarSlotStates(avatarPositions, maxAvatars, maxSlots=AvatarSlots):
    """
    Returns what each of the account's slots shows on the avatar chooser: the
    slot's position when a pirate is in it, otherwise AvatarSlotAvailable or
    AvatarSlotUnavailable ("Unlimited Access Only"). The pirates already made
    are always kept, the free slots are filled from the top up to maxAvatars
    (like DistributedAvatarManager.avatarListResponse does).
    """

    avatarPositions = set(position for position in avatarPositions if 0 <= position < maxSlots)
    available = max(0, maxAvatars - len(avatarPositions))
    slots = []
    for position in range(maxSlots):
        if position in avatarPositions:
            slots.append(position)
        elif available > 0:
            slots.append(OTPGlobals.AvatarSlotAvailable)
            available -= 1
        else:
            slots.append(OTPGlobals.AvatarSlotUnavailable)

    return slots
