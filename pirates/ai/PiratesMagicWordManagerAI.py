import time

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

from otp.ai.MagicWordManagerAI import MagicWordManagerAI
from otp.ai.MagicWordGlobal import *

from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals


class PiratesMagicWordManagerAI(MagicWordManagerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesMagicWordManagerAI')

    def __init__(self, air):
        MagicWordManagerAI.__init__(self, air)

    def requestServerTime(self):
        avatarId = self.air.getAvatarIdFromSender()
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return

        sinceEpoch = time.time()
        self.d_recvServerTime(avatar.doId, sinceEpoch)

    def d_recvServerTime(self, avatarId, sinceEpoch):
        self.sendUpdateToAvatarId(avatarId, 'recvServerTime', [sinceEpoch])


# =========================================================================
# Black Pearl Magic Word - Teleport to Black Pearl instance
# =========================================================================

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def blackpearlai():
    """
    Creates and teleports the invoker to a Black Pearl treasure map instance.
    This is a debug command for testing the Black Pearl quest.
    """
    invoker = spellbook.getInvoker()
    if not invoker:
        return "No invoker found"

    air = spellbook.getManager().air

    # Check if a Black Pearl instance already exists
    existingInstance = None
    from pirates.treasuremap.TreasureMapBlackPearlAI import TreasureMapBlackPearlAI
    for obj in air.doId2do.values():
        if isinstance(obj, TreasureMapBlackPearlAI):
            existingInstance = obj
            break

    if existingInstance:
        # Instance exists, teleport to it
        return _teleportToBlackPearl(air, invoker, existingInstance)
    else:
        # Create a new instance
        return _createBlackPearlInstance(air, invoker)


def _createBlackPearlInstance(air, avatar):
    """Create a new Black Pearl instance and teleport the avatar there"""
    from pirates.treasuremap.TreasureMapBlackPearlAI import TreasureMapBlackPearlAI

    # Load the Black Pearl world
    air.notify.info('Creating Black Pearl instance for avatar %d' % avatar.doId)

    # Load the world file - this will create the TreasureMapBlackPearlAI through WorldCreatorAI
    air.worldCreator.loadObjectsFromFile('BlackpearlWorld.py')

    # The region UID for BlackpearlWorld
    regionUid = '1171761196.78sdnaik'

    # Wait for the instance to be created via callback
    def onInstanceCreated(instanceDoId):
        instance = air.doId2do.get(instanceDoId)
        if instance:
            air.notify.info('Black Pearl instance created: %d' % instanceDoId)
            # Wait for the instance to be fully ready before teleporting
            if instance.isReady:
                _teleportToBlackPearl(air, avatar, instance)
            else:
                air.notify.info('Waiting for Black Pearl instance to be ready...')
                instance.pendingTeleportCallbacks.append(
                    lambda: _teleportToBlackPearl(air, avatar, instance)
                )
        else:
            air.notify.warning('Failed to get Black Pearl instance %d' % instanceDoId)

    air.uidMgr.addUidCallback(regionUid, onInstanceCreated)

    return "Creating Black Pearl instance..."


def _teleportToBlackPearl(air, avatar, instance):
    """Teleport an avatar to the Black Pearl instance"""
    air.notify.info('Teleporting avatar %d to Black Pearl instance %d' % (avatar.doId, instance.doId))

    # Add avatar as participant
    instance.addParticipant(avatar.doId)

    # The island UID in BlackpearlWorld
    islandUid = '1171761224.13sdnaik'

    # Get spawn point from the instance (uses the island's Player Spawn Node)
    # Default spawn is near the pier at Point3(145.77, -276.202, 5.433)
    spawnPt = instance.getSpawnPt(islandUid, 0)
    if spawnPt == (0, 0, 0, 0):
        # Fallback spawn point near the pier
        spawnPt = (145.77, -276.202, 5.433, 0)

    air.notify.info('Teleporting to spawn point: %s' % str(spawnPt))

    # Use the teleport manager to teleport the avatar
    air.teleportMgr.d_initiateTeleport(
        avatar,
        instanceType=instance.getType(),
        instanceName=instance.getFileName(),
        locationUid=islandUid,
        spawnPt=spawnPt
    )

    return "Teleporting to Black Pearl instance %d" % instance.doId


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def bpstate(state='StageOne'):
    """
    Set the Black Pearl instance state.
    Valid states: StageOne, StageTwo, StageThree, StageFour, Reward, NotCompleted
    """
    invoker = spellbook.getInvoker()
    if not invoker:
        return "No invoker found"

    air = spellbook.getManager().air

    # Find the Black Pearl instance
    from pirates.treasuremap.TreasureMapBlackPearlAI import TreasureMapBlackPearlAI
    instance = None
    for obj in air.doId2do.values():
        if isinstance(obj, TreasureMapBlackPearlAI):
            instance = obj
            break

    if not instance:
        return "No Black Pearl instance found"

    validStates = ['StageOne', 'StageTwo', 'StageThree', 'StageFour', 'Reward', 'NotCompleted', 'Completed']
    if state not in validStates:
        return "Invalid state. Valid states: %s" % ', '.join(validStates)

    instance.b_setState(state)
    return "Set Black Pearl state to: %s" % state


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def bpdestroy(barricadeId=0):
    """
    Destroy a barricade in the Black Pearl instance (0-4).
    """
    invoker = spellbook.getInvoker()
    if not invoker:
        return "No invoker found"

    air = spellbook.getManager().air

    # Find the Black Pearl instance
    from pirates.treasuremap.TreasureMapBlackPearlAI import TreasureMapBlackPearlAI
    instance = None
    for obj in air.doId2do.values():
        if isinstance(obj, TreasureMapBlackPearlAI):
            instance = obj
            break

    if not instance:
        return "No Black Pearl instance found"

    if barricadeId < 0 or barricadeId > 4:
        return "Invalid barricade ID (0-4)"

    instance.handleBarricadeDestroyed(barricadeId)
    return "Destroyed barricade %d" % barricadeId
