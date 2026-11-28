import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
import builtins
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

from pirates.kraken.testutil import installStubs
installStubs()

from pirates.npc.BossAI import BossAI
from pirates.npc.BossNPCGameFSMAI import BossNPCGameFSMAI
from pirates.npc.DistributedBossSkeletonAI import DistributedBossSkeletonAI
from pirates.npc.DistributedBossNavySailorAI import DistributedBossNavySailorAI
from pirates.npc.BossNPCList import BOSS_NPC_LIST
from pirates.battle import EnemyGlobals

def importBattleManagerAI():
    # the player pirate pulls in the client gui (fonts etc.), which are not
    # available to the tests.
    import sys
    import types
    name = 'pirates.pirate.DistributedPlayerPirateAI'
    previous = sys.modules.get(name)
    if previous is None:
        module = types.ModuleType(name)
        module.DistributedPlayerPirateAI = type('DistributedPlayerPirateAI', (), {})
        sys.modules[name] = module

    try:
        from pirates.battle.BattleManagerAI import BattleManagerAI
    finally:
        if previous is None:
            del sys.modules[name]

    return BattleManagerAI

BattleManagerAI = importBattleManagerAI()
from pirates.piratesbase import PLocalizer
from pirates.pirate import AvatarTypes
from pirates.pirate.AvatarType import AvatarType


def makeAir():
    air = MagicMock()
    air.doId2do = {}
    return air


class BossAITests(unittest.TestCase):

    def test_boss_classes_use_boss_fsm(self):
        for cls in (DistributedBossSkeletonAI, DistributedBossNavySailorAI):
            boss = cls(makeAir())
            self.assertIsInstance(boss.gameFSM, BossNPCGameFSMAI)
            self.assertIsInstance(boss, BossAI)

    def test_named_boss_data(self):
        boss = DistributedBossSkeletonAI(makeAir())
        bossType = AvatarTypes.Undead.getBossType()
        boss.loadBossData('dynamicBoss_1', bossType)
        self.assertEqual(boss.getBossName(), PLocalizer.BossNPCNames['dynamicBoss_1'])
        self.assertEqual(boss.getBossLevel(), 14)
        self.assertEqual(boss.getModelScale(), 1.3)
        self.assertEqual(boss.getHpScale(), 5)
        # values missing from the entry fall back to the defaults
        self.assertEqual(boss.getDamageScale(), BOSS_NPC_LIST['']['DamageScale'])
        self.assertIn(EnemyGlobals.CUTLASS, [BOSS_NPC_LIST['dynamicBoss_1']['Weapon']])

    def test_named_boss_without_avatar_type_gets_one(self):
        boss = DistributedBossSkeletonAI(makeAir())
        bossType = AvatarTypes.Undead.getBossType()
        boss.loadBossData('1219428571.98mtucker', bossType)
        self.assertEqual(boss.bossData['AvatarType'], bossType)
        self.assertEqual(boss.getDamageScale(), 1.5)

    def test_unknown_uid_falls_back_to_avatar_type(self):
        boss = DistributedBossSkeletonAI(makeAir())
        bossType = AvatarType(faction=0, track=0, id=0).getBossType()
        boss.loadBossData('not-a-boss', bossType)
        name = PLocalizer.BossNames[bossType.faction][bossType.track][bossType.id][bossType.boss - 1]
        self.assertEqual(boss.getBossName(), name)

    def test_damage_scale(self):
        boss = DistributedBossNavySailorAI(makeAir())
        boss.loadBossData('1219426331.38mtucker', AvatarTypes.Navy.getBossType())
        boss.setLevel(20)
        self.assertEqual(boss.getMonsterDmg(), EnemyGlobals.getMonsterDmg(20, 1.75))

    def test_attack_skills_include_boss_skills(self):
        boss = DistributedBossSkeletonAI(makeAir())
        bossType = AvatarTypes.FrenchUndeadA.getBossType()
        boss.setAvatarType(bossType)
        boss.loadBossData('dynamicBoss_1', bossType)
        skills = boss.getAttackSkills()
        for skillId in BOSS_NPC_LIST['dynamicBoss_1']['Skills']:
            self.assertIn(skillId, skills)

        for skillId in EnemyGlobals.getBaseSkills(bossType)[1]:
            self.assertIn(skillId, skills)

    def test_gold_reward_uses_gold_scale(self):
        battleMgr = BattleManagerAI.__new__(BattleManagerAI)
        battleMgr.air = makeAir()
        inventory = Mock()
        inventory.getOverallRep.return_value = 0
        attacker = Mock()
        attacker.getInventory.return_value = inventory
        attacker.battleSkillDiary.getSkills.return_value = []
        del attacker.getGameAccess
        target = Mock()
        target.getGoldScale.return_value = 2
        with patch.object(EnemyGlobals, 'getGoldDrop', return_value=10) as getGoldDrop, \
                patch('random.random', return_value=0.0):
            battleMgr.rewardAttacker(attacker, target)

        self.assertEqual(getGoldDrop.call_args.args[2], 2)
        inventory.addGoldInPocket.assert_called_once_with(10)


if __name__ == '__main__':
    unittest.main()
