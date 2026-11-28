import itertools
import time

from panda3d.core import VBase3
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta
from direct.directnotify import DirectNotifyGlobal

from otp.ai.MagicWordManagerAI import MagicWordManagerAI
from otp.ai.MagicWordGlobal import *

from pirates.ai import HolidayGlobals
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TODGlobals
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


# =========================================================================
# Player Magic Words
# =========================================================================

def _findAvatar(air, name):
    """
    Locates a player avatar on this district by either it's doId or name.
    """

    from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI

    try:
        avatar = air.doId2do.get(int(name))
        if isinstance(avatar, DistributedPlayerPirateAI):
            return avatar
    except ValueError:
        pass

    name = name.strip().lower()
    for avatar in list(air.doId2do.values()):
        if not isinstance(avatar, DistributedPlayerPirateAI):
            continue

        if avatar.getName().strip().lower() == name:
            return avatar

    return None


@magicWord(category=CATEGORY_GAME_MASTER)
def players():
    """
    Lists the players currently on this district
    """

    from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI

    air = spellbook.getManager().air
    avatars = [avatar for avatar in list(air.doId2do.values()) if
               isinstance(avatar, DistributedPlayerPirateAI)]

    return '%d player(s): %s' % (len(avatars), ', '.join(
        ['%s (%d)' % (avatar.getName(), avatar.doId) for avatar in avatars]))


@magicWord(category=CATEGORY_GAME_MASTER, types=[str])
def goto(name):
    """
    Teleports the invoker to the player with the given name or avatarId
    """

    air = spellbook.getManager().air
    invoker = spellbook.getInvoker()
    avatar = _findAvatar(air, name)
    if not avatar:
        return 'Could not find player: %s!' % name

    if avatar is invoker:
        return 'You cannot teleport to yourself!'

    if not air.teleportMgr.teleportToAvatar(invoker, avatar):
        return 'Could not teleport to %s!' % avatar.getName()

    return 'Teleporting to %s...' % avatar.getName()


@magicWord(category=CATEGORY_GAME_MASTER, types=[str])
def summon(name):
    """
    Teleports the player with the given name or avatarId to the invoker
    """

    air = spellbook.getManager().air
    invoker = spellbook.getInvoker()
    avatar = _findAvatar(air, name)
    if not avatar:
        return 'Could not find player: %s!' % name

    if avatar is invoker:
        return 'You cannot summon yourself!'

    if avatar.getAdminAccess() > spellbook.getInvokerAccess():
        return 'Target must have lower or equal access'

    if not air.teleportMgr.teleportToAvatar(avatar, invoker):
        return 'Could not summon %s!' % avatar.getName()

    return 'Summoning %s...' % avatar.getName()


@magicWord(category=CATEGORY_MODERATION, types=[str])
def kick(name):
    """
    Disconnects the player with the given name or avatarId from the game
    """

    air = spellbook.getManager().air
    avatar = _findAvatar(air, name)
    if not avatar:
        return 'Could not find player: %s!' % name

    if avatar is spellbook.getInvoker():
        return 'You cannot kick yourself!'

    if avatar.getAdminAccess() > spellbook.getInvokerAccess():
        return 'Target must have lower or equal access'

    # 151: You have been logged out by an administrator working on the servers.
    air.kickChannel(avatar.GetPuppetConnectionChannel(avatar.doId), 151,
        'You have been logged out by an administrator.')

    return 'Kicked %s (%d).' % (avatar.getName(), avatar.doId)


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def god():
    """
    Toggles the targets god mode, a god is immortal and fully healed
    """

    target = spellbook.getTarget()
    target.setImmortal(not target.getImmortal())
    if target.getImmortal():
        target.b_setHp(target.getMaxHp())
        target.b_setMojo(target.getMaxMojo())

    return 'God mode set to: %s' % bool(target.getImmortal())


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int, int])
def rep(repType, amount):
    """
    Gives the target an amount of reputation in the given InventoryType category
    """

    from pirates.uberdog.UberDogGlobals import InventoryType

    if not InventoryType.begin_Accumulator <= repType < InventoryType.end_Accumulator:
        return 'Invalid reputation type: %d!' % repType

    target = spellbook.getTarget()
    inventory = target.getInventory()
    if not inventory:
        return 'Target does not have an inventory!'

    inventory.setReputation(repType, max(0, inventory.getReputation(repType) + amount))
    return 'Reputation %d set to %d.' % (repType, inventory.getReputation(repType))


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def tutorial(state=-1):
    """
    Sets the targets tutorial progress, see PiratesGlobals.TUT_*
    """

    target = spellbook.getTarget()
    if state < 0:
        return 'Tutorial state: %d' % target.getTutorial()

    if state > PiratesGlobals.TUT_FINISHED:
        return 'Invalid tutorial state, 0-%d!' % PiratesGlobals.TUT_FINISHED

    target.b_setTutorial(state)
    return 'Tutorial state set to %d.' % state


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def quests():
    """
    Lists the targets active quests
    """

    target = spellbook.getTarget()
    questMgr = spellbook.getManager().air.questMgr
    questIds = [quest.getQuestId() for quest in
                list(questMgr.quests.get(target.doId, {}).values())]

    if not questIds:
        return 'No active quests.'

    return 'Active quests: %s' % ', '.join(questIds)


# =========================================================================
# World Magic Words
# =========================================================================

@magicWord(category=CATEGORY_GAME_MASTER, types=[int, float])
def tod(state=-1, cycleDuration=-1.0):
    """
    Sets the district's time of day state and optionally the cycle duration,
    a duration of zero freezes the time of day at the given state
    """

    todMgr = spellbook.getManager().air.timeOfDayMgr
    if state < 0:
        return 'Time of day: %s (%d), cycle: %d, duration: %s' % (
            TODGlobals.getStateName(todMgr.getCurrentState()), todMgr.getCurrentState(),
            todMgr.cycleType, todMgr.cycleDuration)

    if not TODGlobals.isStateIdValid(todMgr.cycleType, state):
        return 'Invalid time of day state %d for cycle %d!' % (state, todMgr.cycleType)

    if cycleDuration < 0:
        cycleDuration = todMgr.cycleDuration

    # restart the cycle from the requested state as of right now,
    # the clients compute their current state from this anchor...
    startingTime = globalClockDelta.getRealNetworkTime(bits=32)
    todMgr.b_sync(todMgr.cycleType, state, startingTime, cycleDuration)
    todMgr._processStateChange()

    return 'Time of day set to %s (%d).' % (TODGlobals.getStateName(state), state)


@magicWord(category=CATEGORY_GAME_MASTER)
def holidays():
    """
    Lists the currently active holidays
    """

    newsManager = spellbook.getManager().air.newsManager
    active = [holidayId for holidayId in list(newsManager.holidayList.keys()) if
              newsManager.isHolidayActive(holidayId)]

    if not active:
        return 'No active holidays.'

    return 'Active holidays: %s' % ', '.join(['%s (%d)' % (
        HolidayGlobals.getHolidayName(holidayId), holidayId) for holidayId in active])


@magicWord(category=CATEGORY_GAME_MASTER, types=[int])
def siege(pvpEnabled=-1):
    """
    Enables or disables privateer siege pvp on this district
    """

    siegeManager = spellbook.getManager().air.siegeManager
    if pvpEnabled < 0:
        return 'Siege pvp enabled: %s' % bool(siegeManager.getPvpEnabled())

    siegeManager.b_setPvpEnabled(bool(pvpEnabled))
    return 'Siege pvp enabled set to: %s' % bool(pvpEnabled)


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def spawn(spawnable):
    """
    Spawns a non respawning enemy at the invoker's location,
    see AvatarTypes.NPC_SPAWNABLES (e.g. Noob Skeleton)
    """

    from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI

    if spawnable not in AvatarTypes.NPC_SPAWNABLES:
        return 'Invalid spawnable: %s!' % spawnable

    invoker = spellbook.getInvoker()
    parent = invoker.getParentObj()
    if not isinstance(parent, DistributedGameAreaAI):
        return 'You must be in a game area to spawn an enemy!'

    objectData = {
        'Spawnables': spawnable,
        'Pos': invoker.getPos(),
        'Hpr': invoker.getHpr(),
        'Scale': VBase3(1, 1, 1),
        'Respawns': False
    }

    objKey = 'magic-word-spawn-%d' % next(_spawnKeys)
    air = spellbook.getManager().air
    air.enemySpawner.createObject('Spawn Node', objectData, parent,
        parent.getUniqueId(), objKey, True)

    return 'Spawned %s.' % spawnable

_spawnKeys = itertools.count()


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def spawnShip(shipClass):
    """
    Spawns an enemy ship of the given ShipGlobals ship class on the ocean
    """

    shipManager = spellbook.getManager().air.shipManager
    if not shipManager.world:
        return 'The ship manager has no world to spawn ships in!'

    ship = shipManager._spawnEnemyShip(shipClass)
    if not ship:
        return 'Failed to spawn ship class %d!' % shipClass

    return 'Spawned %s (%d) in zone %d.' % (ship.getName(), ship.doId, ship.zoneId)


def _getInvokerShip():
    invoker = spellbook.getInvoker()
    air = spellbook.getManager().air
    return air.doId2do.get(invoker.getShipId()) or air.doId2do.get(invoker.getActiveShipId())


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def repairShip():
    """
    Fully repairs the hull and sails of the ship the invoker is aboard
    """

    ship = _getInvokerShip()
    if not ship:
        return 'You must be aboard a ship!'

    if not ship.isSailable():
        return 'This ship can not be repaired!'

    ship.b_setHp(ship.getMaxHp())
    ship.b_setSp(ship.getMaxSp())
    return 'Repaired %s.' % ship.getName()


@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def sinkShip():
    """
    Sinks the ship the invoker is aboard
    """

    ship = _getInvokerShip()
    if not ship:
        return 'You must be aboard a ship!'

    if not ship.isSailable():
        return 'This ship is already sinking!'

    ship.b_setHp(0)
    return 'Sinking %s...' % ship.getName()
