import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from panda3d.core import NodePath, loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')

if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

with patch.object(builtins.loader, 'loadFont', Mock()):
    from pirates.battle import BattleManagerAI as battle_manager_module

from pirates.battle import WeaponBaseAI as weapon_base_module
from pirates.battle.WeaponBaseAI import WeaponBaseAI
from pirates.uberdog.UberDogGlobals import InventoryType

# the WeaponGlobals module the code under test actually uses...
WeaponGlobals = weapon_base_module.WeaponGlobals


class FakeTarget(NodePath):

    def __init__(self, doId, parent, pos=(0, 0, 0)):
        NodePath.__init__(self, 'target-%d' % doId)
        self.doId = doId
        self.isNpc = True
        self.parentArea = parent
        self.reparentTo(parent)
        self.setPos(*pos)

    def getParentObj(self):
        return self.parentArea


class WeaponBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.area = NodePath('area')
        self.avatar = WeaponBaseAI.__new__(WeaponBaseAI)
        self.avatar.doId = 100
        self.avatar.isNpc = False
        self.avatar.currentTarget = None
        self.avatar.getCurrentTarget = lambda: self.avatar.currentTarget.doId if self.avatar.currentTarget else 0
        self.avatar.b_setCurrentTarget = Mock(side_effect=self.setCurrentTarget)
        self.avatar.sendUpdate = Mock()

        self.battleMgr = Mock()
        self.battleMgr.requestSkillUse.return_value = True
        self.battleMgr.isPlayerSkillHandledElsewhere.return_value = False
        self.battleMgr.getModifiedAttackRange.return_value = 10.0
        self.battleMgr.getRelativePosition.side_effect = lambda attacker, target: target.getDistance(self.area)
        self.battleMgr.getTargetedSkillResult.side_effect = self.getTargetedSkillResult

        self.avatar.air = SimpleNamespace(doId2do={self.avatar.doId: self.avatar},
            getAvatarIdFromSender=lambda: self.avatar.doId, battleMgr=self.battleMgr, targetMgr=Mock())

    def setCurrentTarget(self, doId):
        self.avatar.currentTarget = self.avatar.air.doId2do.get(doId)

    def getTargetedSkillResult(self, avatar, target, skillId, ammoSkillId, areaIdList, timestamp, pos, charge=0,
                               clientResult=None):
        # the other clients must know of the avatar's target before the attack...
        self.targetWhenAttacking = self.avatar.getCurrentTarget()
        return [skillId, ammoSkillId, WeaponGlobals.RESULT_HIT, target.doId if target else 0, [], [0] * 5, [0] * 5,
            [], 0, pos, charge]

    def addTarget(self, doId, distance=0):
        target = FakeTarget(doId, self.area, (distance, 0, 0))
        self.avatar.air.doId2do[doId] = target
        return target

    def request(self, targetId, skillId=InventoryType.CutlassHack, clientResult=WeaponGlobals.RESULT_HIT):
        self.avatar.requestTargetedSkill(skillId, 0, clientResult, targetId, [], 0, [0, 0, 0], 0)
        return self.battleMgr.getTargetedSkillResult.call_args[1]['clientResult']

    def sentUpdates(self, fieldName):
        return [args for (name, args), _ in self.avatar.sendUpdate.call_args_list if name == fieldName]


class AttackRangeTests(WeaponBaseTestCase):

    def test_out_of_range_target_is_never_hit(self):
        self.addTarget(200, distance=100)
        self.assertEqual(self.request(200), WeaponGlobals.RESULT_OUT_OF_RANGE)

    def test_target_within_tolerance_is_hit(self):
        # just beyond the skill's range, our position of the target lags behind...
        self.addTarget(200, distance=14)
        self.assertEqual(self.request(200), WeaponGlobals.RESULT_HIT)

    def test_unlimited_range_skills_always_reach(self):
        self.battleMgr.getModifiedAttackRange.return_value = WeaponGlobals.INF_RANGE
        self.addTarget(200, distance=5000)
        self.assertEqual(self.request(200), WeaponGlobals.RESULT_HIT)

    def test_skills_handled_elsewhere_skip_the_range_check(self):
        self.battleMgr.isPlayerSkillHandledElsewhere.return_value = True
        self.addTarget(200, distance=5000)
        self.assertEqual(self.request(200, InventoryType.UseItem), WeaponGlobals.RESULT_HIT)

    def test_big_creatures_are_reached_along_their_battle_tube(self):
        target = self.addTarget(200, distance=20)
        target.avatarType = object()
        with patch.object(weapon_base_module.EnemyGlobals, 'getBattleTubeRadius', return_value=10):
            self.assertEqual(self.request(200), WeaponGlobals.RESULT_HIT)


class CurrentTargetTests(WeaponBaseTestCase):

    def test_remote_clients_learn_of_a_target_switch_before_the_attack(self):
        self.addTarget(200)
        self.addTarget(201)
        self.avatar.currentTarget = self.avatar.air.doId2do[200]

        self.request(201)
        self.avatar.b_setCurrentTarget.assert_called_once_with(201)
        self.assertEqual(self.targetWhenAttacking, 201)

        # attacking the same target again doesn't send it again...
        self.request(201)
        self.avatar.b_setCurrentTarget.assert_called_once_with(201)

    def test_attacks_without_a_target_keep_the_current_target(self):
        self.addTarget(200)
        self.avatar.currentTarget = self.avatar.air.doId2do[200]
        self.request(0)
        self.avatar.b_setCurrentTarget.assert_not_called()


class ProjectileTests(WeaponBaseTestCase):

    def test_projectile_may_be_used_while_another_is_in_the_air(self):
        self.avatar.requestProjectileSkill(InventoryType.GrenadeThrow, InventoryType.GrenadeExplosion, [0] * 6, 0, 0)
        self.avatar.requestProjectileSkill(InventoryType.GrenadeThrow, InventoryType.GrenadeExplosion, [0] * 6, 0, 0)
        self.assertEqual(len(self.sentUpdates('useProjectileSkill')), 2)

    def test_rejected_projectile_is_never_sent(self):
        self.battleMgr.requestSkillUse.return_value = False
        self.avatar.requestProjectileSkill(InventoryType.GrenadeThrow, InventoryType.GrenadeExplosion, [0] * 6, 0, 0)
        self.assertEqual(self.sentUpdates('useProjectileSkill'), [])


if __name__ == '__main__':
    unittest.main()
