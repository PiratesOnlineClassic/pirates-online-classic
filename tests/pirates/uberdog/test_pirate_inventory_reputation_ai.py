import builtins
import sys
import types
import unittest
from unittest.mock import Mock, patch

import pirates.battle

# WeaponGlobals requires game resources (WeaponGlobals.pkl) which are not
# available to the tests; the reputation code does not depend on it.
if 'pirates.battle.WeaponGlobals' not in sys.modules:
    try:
        from pirates.battle import WeaponGlobals
    except Exception:
        stub = types.ModuleType('pirates.battle.WeaponGlobals')
        sys.modules['pirates.battle.WeaponGlobals'] = stub
        pirates.battle.WeaponGlobals = stub

from pirates.reputation import RepChart, ReputationGlobals
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.uberdog.PirateInventoryAI import PirateInventoryAI
from pirates.uberdog.UberDogGlobals import InventoryType


class FakeAvatar:
    def __init__(self):
        self.doId = 1000
        self.level = 1
        self.maxHp = 100
        self.maxMojo = 50
        self.hp = 10
        self.mojo = 5
        self.levelUps = []

    def getName(self):
        return 'Test Pirate'

    def b_setLevel(self, level):
        self.level = level

    def getLevel(self):
        return self.level

    def getMaxHp(self):
        return self.maxHp

    def b_setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def getMaxMojo(self):
        return self.maxMojo

    def b_setMaxMojo(self, maxMojo):
        self.maxMojo = maxMojo

    def b_setHp(self, hp):
        self.hp = hp

    def b_setMojo(self, mojo):
        self.mojo = mojo

    def d_levelUpMsg(self, category, level, messageId):
        self.levelUps.append((category, level))


class PirateInventoryReputationTests(unittest.TestCase):

    def setUp(self):
        # the inventory stores it's accumulators a moment after they change
        taskMgrPatch = patch.object(builtins, 'taskMgr', Mock(), create=True)
        taskMgrPatch.start()
        self.addCleanup(taskMgrPatch.stop)

        self.avatar = FakeAvatar()
        self.inventory = PirateInventoryAI.__new__(PirateInventoryAI)
        DistributedInventoryBase.__init__(self.inventory, None)
        self.inventory.doId = 5000
        self.inventory.ownerId = self.avatar.doId
        self.inventory.air = Mock()
        self.inventory.air.doId2do = {self.avatar.doId: self.avatar}
        self.inventory.air.questMgr.hasQuest.return_value = False
        self.inventory.sendUpdateToAvatarId = Mock()

    def repForLevel(self, repType, level):
        if repType == InventoryType.OverallRep:
            return ReputationGlobals.GlobalReputationAtLevel[level]

        return ReputationGlobals.TotalReputationAtLevel[level]

    def test_every_level_earned_grants_a_skill_point(self):
        self.inventory.setReputation(InventoryType.CutlassRep, self.repForLevel(InventoryType.CutlassRep, 4))

        self.assertEqual(self.inventory.getReputation(InventoryType.CutlassRep),
            self.repForLevel(InventoryType.CutlassRep, 4))
        self.assertEqual([level for category, level in self.avatar.levelUps], [2, 3, 4])
        self.assertEqual(self.inventory.getStackQuantity(InventoryType.UnspentCutlass), 3)
        self.assertEqual(self.inventory.getStackQuantity(InventoryType.CutlassSweep), 1)
        self.assertEqual(self.inventory.getStackQuantity(InventoryType.CutlassCleave), 1)
        self.assertEqual(self.inventory.getStackQuantity(InventoryType.CutlassHack), 1)

        hpGain = RepChart.getHpGain(InventoryType.CutlassRep) * 3
        self.assertEqual(self.avatar.maxHp, 100 + hpGain)
        self.assertEqual(self.inventory.getStackLimit(InventoryType.Hp), 100 + hpGain)

    def test_unlocked_skill_rank_is_not_reset(self):
        self.inventory.stacks[InventoryType.CutlassSweep] = 3
        self.inventory.stacks[InventoryType.UnspentCutlass] = 2

        self.inventory.setReputation(InventoryType.CutlassRep, self.repForLevel(InventoryType.CutlassRep, 2))

        self.assertEqual(self.inventory.getStackQuantity(InventoryType.CutlassSweep), 3)
        self.assertEqual(self.inventory.getStackQuantity(InventoryType.UnspentCutlass), 3)

    def test_overall_level_up_sets_level_and_heals(self):
        self.inventory.setReputation(InventoryType.OverallRep, self.repForLevel(InventoryType.OverallRep, 5))

        self.assertEqual(self.avatar.level, 5)
        self.assertEqual(self.avatar.levelUps[-1], (InventoryType.OverallRep, 5))
        self.assertEqual(self.avatar.hp, self.avatar.maxHp)
        self.assertEqual(self.avatar.maxHp, 100 + RepChart.getHpGain(InventoryType.OverallRep) * 4)
        self.inventory.air.questMgr.createQuest.assert_called_once_with(self.avatar, 'wd.1visitTia')

    def test_no_level_change_only_updates_accumulator(self):
        self.inventory.setReputation(InventoryType.CutlassRep, 10)

        self.assertEqual(self.avatar.levelUps, [])
        self.assertEqual(self.inventory.getReputation(InventoryType.CutlassRep), 10)
        self.inventory.sendUpdateToAvatarId.assert_called_once_with(
            self.avatar.doId, 'accumulator', [InventoryType.CutlassRep, 10])

    def test_reputation_is_capped_at_accumulator_limit(self):
        self.inventory.handleLevelUp = Mock()
        self.inventory.setReputation(InventoryType.CutlassRep, 10 ** 7)

        self.assertEqual(self.inventory.getReputation(InventoryType.CutlassRep), 56600)


if __name__ == '__main__':
    unittest.main()
