import builtins
import unittest

from panda3d.core import ClockObject

if not hasattr(builtins, 'globalClock'):
    builtins.globalClock = ClockObject.getGlobalClock()

from pirates.battle.ComboDiary import ComboDiary
from pirates.distributed.DistributedTargetableObjectAI import DistributedTargetableObjectAI
from pirates.uberdog.UberDogGlobals import InventoryType


class TargetableObjectComboTests(unittest.TestCase):

    def makeProp(self):
        # an interactive prop (e.g. a training dummy) is targetable but not a battle avatar...
        return DistributedTargetableObjectAI.__new__(DistributedTargetableObjectAI)

    def test_expired_combo_on_a_prop_resets_without_crashing(self):
        prop = self.makeProp()
        diary = ComboDiary(prop)
        diary.recordAttack(1, InventoryType.CutlassHack, 10)
        # an attack out of combo order expires the combo, which resets the owner's combo level...
        diary.recordAttack(1, InventoryType.CutlassStab, 10)
        diary.recordAttack(1, InventoryType.CutlassHack, 10)
        prop.resetComboLevel()

    def test_team_combo_on_a_prop_is_kept_locally(self):
        prop = self.makeProp()
        prop.b_setCombo(2, 1, 30, 7)
        self.assertEqual((prop.combo, prop.teamCombo, prop.comboDamage, prop.attackerId), (2, 1, 30, 7))


if __name__ == '__main__':
    unittest.main()
