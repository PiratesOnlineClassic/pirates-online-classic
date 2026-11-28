import sys
import types
import unittest
from unittest.mock import Mock, patch

import pirates.battle

# WeaponGlobals requires game resources (WeaponGlobals.pkl) which may not
# be available to the tests; the inventory code does not depend on it.
if 'pirates.battle.WeaponGlobals' not in sys.modules:
    try:
        from pirates.battle import WeaponGlobals
    except Exception:
        stub = types.ModuleType('pirates.battle.WeaponGlobals')
        sys.modules['pirates.battle.WeaponGlobals'] = stub
        pirates.battle.WeaponGlobals = stub

from pirates.reputation import ReputationGlobals
from pirates.uberdog import InventoryInit
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.uberdog.PirateInventoryAI import PirateInventoryAI
from pirates.uberdog.UberDogGlobals import InventoryType


def makeInventory(stacks=None, stackLimits=None):
    inventory = PirateInventoryAI.__new__(PirateInventoryAI)
    DistributedInventoryBase.__init__(inventory, None)
    inventory.doId = 5000
    inventory.ownerId = 1000
    inventory.air = Mock()
    inventory.stacks = dict(stacks or {})
    inventory.stackLimits = dict(InventoryInit.StackLimits if stackLimits is None else stackLimits)
    inventory.sendUpdate = Mock()
    inventory.sendUpdateToAvatarId = Mock()
    return inventory


def lastUpdate(inventory, fieldName):
    for call in reversed(inventory.sendUpdate.call_args_list):
        if call[0][0] == fieldName:
            return dict((key, value) for key, value in call[0][1][0])

    return None


class InventoryPersistenceTests(unittest.TestCase):

    def test_stack_changes_are_stored(self):
        inventory = makeInventory({InventoryType.CutlassWeaponL1: 1})
        inventory.b_setStackQuantity(InventoryType.PistolWeaponL1, 1)

        inventory.sendUpdateToAvatarId.assert_called_once_with(
            inventory.ownerId, 'stack', [InventoryType.PistolWeaponL1, 1])
        self.assertEqual(lastUpdate(inventory, 'setStacks'), {
            InventoryType.CutlassWeaponL1: 1, InventoryType.PistolWeaponL1: 1})

    def test_empty_stacks_are_not_stored(self):
        inventory = makeInventory({InventoryType.Potion1: 1, InventoryType.Potion2: 2})
        inventory.b_setStackQuantity(InventoryType.Potion1, 0)

        self.assertEqual(lastUpdate(inventory, 'setStacks'), {InventoryType.Potion2: 2})

    def test_stacks_are_clamped(self):
        inventory = makeInventory()
        inventory.b_setStackQuantity(InventoryType.Potion1, 10)
        self.assertEqual(inventory.getStackQuantity(InventoryType.Potion1), 3)
        inventory.sendUpdateToAvatarId.assert_called_with(inventory.ownerId, 'stack', [InventoryType.Potion1, 3])

        inventory.b_setStackQuantity(InventoryType.Potion1, -2)
        self.assertEqual(inventory.getStackQuantity(InventoryType.Potion1), 0)

        # stacks without a limit still fit the stack field...
        inventory.b_setStackQuantity(InventoryType.ShipRepairKit, 70000)
        self.assertEqual(inventory.getStackQuantity(InventoryType.ShipRepairKit), 65535)

    def test_gold_is_capped_by_it_stack_limit(self):
        inventory = makeInventory()
        inventory.setGoldInPocket(70000)
        self.assertEqual(inventory.getGoldInPocket(), 65000)

        inventory.setGoldInPocket(-5)
        self.assertEqual(inventory.getGoldInPocket(), 0)

    def test_accumulator_changes_are_stored(self):
        inventory = makeInventory()
        inventory.accumulators[InventoryType.OverallRep] = 10
        inventory.b_setAccumulator(InventoryType.CutlassRep, 20)

        self.assertEqual(lastUpdate(inventory, 'setAccumulators'), {
            InventoryType.OverallRep: 10, InventoryType.CutlassRep: 20})

    def test_stack_limit_changes_are_stored(self):
        inventory = makeInventory(stackLimits={InventoryType.AmmoAsp: 100})
        inventory.b_setStackLimit(InventoryType.AmmoAsp, 125)

        inventory.sendUpdateToAvatarId.assert_called_once_with(
            inventory.ownerId, 'stackLimit', [InventoryType.AmmoAsp, 125])
        self.assertEqual(lastUpdate(inventory, 'setStackLimits'), {InventoryType.AmmoAsp: 125})


class InventoryUpgradeTests(unittest.TestCase):

    def setUp(self):
        # the base inventory announces limit changes through the messenger...
        messengerPatch = patch('builtins.messenger', Mock(), create=True)
        messengerPatch.start()
        self.addCleanup(messengerPatch.stop)

    def test_missing_stack_limits_are_added(self):
        inventory = makeInventory(stackLimits={InventoryType.CutlassHack: 6, InventoryType.Hp: 250})
        inventory.updateStackLimits()

        self.assertEqual(inventory.getStackLimit(InventoryType.CutlassSweep), 6)
        self.assertEqual(inventory.getStackLimit(InventoryType.GoldInPocket), 65000)
        self.assertEqual(inventory.getStackLimit(InventoryType.Hp), 250)
        self.assertEqual(lastUpdate(inventory, 'setStackLimits'), inventory.stackLimits)

    def test_complete_stack_limits_are_not_resent(self):
        inventory = makeInventory()
        inventory.updateStackLimits()
        inventory.sendUpdate.assert_not_called()

    def test_owned_pouches_raise_ammo_limits(self):
        inventory = makeInventory({InventoryType.DaggerPouchL1: 1})
        inventory.updateStackLimits()

        self.assertEqual(inventory.getStackLimit(InventoryType.AmmoAsp), 125)
        self.assertEqual(inventory.getStackLimit(InventoryType.AmmoAdder), 75)
        self.assertEqual(inventory.getStackLimit(InventoryType.AmmoSidewinder), 75)
        self.assertEqual(inventory.getStackLimit(InventoryType.AmmoViperNest), 35)
        self.assertEqual(inventory.getStackLimit(InventoryType.AmmoBaneShot), 100)

    def test_unlocked_skills_are_given(self):
        inventory = makeInventory({InventoryType.CutlassHack: 2, InventoryType.CutlassSweep: 4})
        inventory.accumulators[InventoryType.CutlassRep] = ReputationGlobals.TotalReputationAtLevel[6]
        inventory.updateSkillUnlocks()

        self.assertEqual(inventory.getStackQuantity(InventoryType.CutlassHack), 2)
        self.assertEqual(inventory.getStackQuantity(InventoryType.CutlassSweep), 4)
        self.assertEqual(inventory.getStackQuantity(InventoryType.CutlassCleave), 1)
        self.assertEqual(inventory.getStackQuantity(InventoryType.CutlassParry), 1)
        self.assertEqual(inventory.getStackQuantity(InventoryType.CutlassBrawl), 0)
        self.assertEqual(inventory.getStackQuantity(InventoryType.UnspentCutlass), 0)

    def test_new_pirates_have_not_seen_the_first_defeat_message(self):
        self.assertEqual(InventoryInit.StartingStacks[InventoryType.FirstDeathToken], 0)


if __name__ == '__main__':
    unittest.main()
