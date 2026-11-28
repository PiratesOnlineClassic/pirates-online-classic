import random

from pirates.battle import WeaponGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import ItemId
from pirates.piratesbase import CollectionMap
from pirates.uberdog.UberDogGlobals import InventoryType

# the chance a defeated enemy carries a piece of one of the
# treasure collections the avatar has started...
COLLECTION_DROP_CHANCE = 0.1

# the chance a defeated enemy carries a playing card...
CARD_DROP_CHANCE = 0.2

# the amount of loot plundered from a sunk ship, flagships carry more...
SHIP_LOOT_RANGE = (1, 3)
FLAGSHIP_LOOT_BONUS = 2

# the weight of each cargo container type, a royal chest is the rarest
# (see EconomyGlobals.__crateCargoList)...
CARGO_CONTAINER_WEIGHTS = {
    ItemId.CARGO_CRATE: 50,
    ItemId.CARGO_CHEST: 45,
    ItemId.CARGO_SKCHEST: 5}


def getCollectionSetParts(setKey):
    setSize = CollectionMap.Collection_Set_Sizes.get(setKey, 0)
    return [setKey + 1 + i for i in range(setSize)]


def getCollectionPartWeight(partId):
    # rarer items are worth more gold and are found less often, the client
    # shows each item's value in it's loot popup (see LootPopupPanel.showLoot)...
    rarity = CollectionMap.Collection_Rarity.get(partId, 0)
    value = EconomyGlobals.CollectionValues.get(rarity, 1)
    return 1.0 / value


def getCollectionSetsFound(avatarType):
    # the client only lists where some of the collections are found,
    # see CollectionMap.Collection_Found...
    if not avatarType:
        return []

    return [setKey for setKey in InventoryType.Collection_Sets
            if setKey in CollectionMap.Collection_Found and
            avatarType.isA(CollectionMap.Collection_Found[setKey])]


def getCollectionDrop(avatarType, inventory):
    """
    Returns a random collection item found on a defeated enemy of the
    given avatar type, only collections the avatar has started (been
    given by a quest, see QuestReward.CollectReward) are ever dropped
    """

    candidates = []
    for setKey in getCollectionSetsFound(avatarType):
        if inventory.getStackQuantity(setKey) <= 0:
            continue

        for partId in getCollectionSetParts(setKey):
            limit = inventory.getStackLimit(partId)
            if limit and inventory.getStackQuantity(partId) >= limit:
                continue

            candidates.append(partId)

    if not candidates:
        return None

    return weightedChoice([(partId, getCollectionPartWeight(partId)) for partId in candidates])


def getTreasureSenseBonus(rank):
    # Treasure Sense increases the quality of cargo drops, see
    # SkillButton.showDetails for the percentage shown to the client...
    return (WeaponGlobals.TREASURE_SENSE_BONUS / 2.0) * max(rank, 0) / 100.0


def getCargoContainerWeights(treasureSenseRank=0):
    bonus = 1.0 + getTreasureSenseBonus(treasureSenseRank)
    weights = []
    for itemId, weight in sorted(CARGO_CONTAINER_WEIGHTS.items()):
        if itemId != ItemId.CARGO_CRATE:
            weight *= bonus

        weights.append((itemId, weight))

    return weights


def getShipLoot(isFlagship=False, treasureSenseRank=0):
    """
    Returns a list of the cargo containers plundered from a sunk ship
    """

    minLoot, maxLoot = SHIP_LOOT_RANGE
    numLoot = random.randint(minLoot, maxLoot)
    if isFlagship:
        numLoot += FLAGSHIP_LOOT_BONUS

    weights = getCargoContainerWeights(treasureSenseRank)
    return [weightedChoice(weights) for _ in range(numLoot)]


def weightedChoice(choices):
    total = sum(weight for _, weight in choices)
    roll = random.random() * total
    for item, weight in choices:
        roll -= weight
        if roll < 0:
            return item

    return choices[-1][0]
