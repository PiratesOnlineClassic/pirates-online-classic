import builtins
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')


def _stubModule(name, **attrs):
    module = types.ModuleType(name)
    module.__dict__.update(attrs)
    return module


# Without the game resources (WeaponGlobals.pkl) and libotp the full AI import
# chain cannot load; stand in for the few leaf modules that need them while the
# creature modules are imported, then drop everything imported here so other
# tests in the same session get the real modules.
_stubs = {
    'pirates.world.DistributedGameAreaAI': _stubModule('pirates.world.DistributedGameAreaAI',
        DistributedGameAreaAI=type('DistributedGameAreaAI', (object,), {})),
    'pirates.leveleditor.ObjectList': _stubModule('pirates.leveleditor.ObjectList'),
    'otp.avatar.Avatar': _stubModule('otp.avatar.Avatar', Avatar=type('Avatar', (object,), {})),
}

try:
    from pirates.battle import WeaponGlobals
except Exception:
    WeaponGlobals = _stubModule('pirates.battle.WeaponGlobals', NO_DELAY=0.0, SHORT_DELAY=1.0,
        MED_DELAY=2.0, LONG_DELAY=3.0, getAttackDelay=lambda *args, **kw: 2.0,
        getAttackDuration=lambda *args, **kw: 1.0, isVoodooWeapon=lambda *args, **kw: False)
    WeaponGlobals.__getattr__ = lambda name: (lambda *args, **kw: 0)
    _stubs['pirates.battle.WeaponGlobals'] = WeaponGlobals

_previousModules = set(sys.modules)
_replacedModules = {name: sys.modules.get(name) for name in _stubs}
sys.modules.update(_stubs)
try:
    from pirates.pirate import AvatarTypes
    from pirates.piratesbase import PiratesGlobals
    from pirates.battle.EnemySkills import EnemySkills
    from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
    from pirates.creature.DistributedAnimalAI import DistributedAnimalAI
    from pirates.creature.DistributedBossCreatureAI import DistributedBossCreatureAI
    from pirates.creature.DistributedSeagullAI import DistributedSeagullAI
    from pirates.creature.DistributedSeaSerpentAI import DistributedSeaSerpentAI
    from pirates.creature.CreatureGameFSMAI import CreatureGameFSMAI
    from pirates.creature.AnimalGameFSMAI import AnimalGameFSMAI
    from pirates.pirate.BattleNPCGameFSMAI import BattleNPCGameFSMAI
    from pirates.battle import DistributedEnemySpawnerAI as spawner
finally:
    for _name in set(sys.modules) - _previousModules:
        sys.modules.pop(_name, None)

    for _name, _module in _replacedModules.items():
        if _module is not None:
            sys.modules[_name] = _module


def makeAir():
    air = MagicMock()
    air.doId2do = {}
    return air


def makeCreature(cls, avatarType):
    npc = cls(makeAir())
    npc.setAvatarType(avatarType)
    npc.doId = 1000
    npc.sendUpdate = Mock()
    return npc


class CreatureFSMTests(unittest.TestCase):
    def test_creatures_use_creature_fsm(self):
        npc = makeCreature(DistributedCreatureAI, AvatarTypes.Crab)
        self.assertIsInstance(npc.gameFSM, CreatureGameFSMAI)

        animal = makeCreature(DistributedAnimalAI, AvatarTypes.Chicken)
        self.assertIsInstance(animal.gameFSM, AnimalGameFSMAI)

        boss = makeCreature(DistributedBossCreatureAI, AvatarTypes.FlyTrap.getBossType())
        self.assertIsInstance(boss.gameFSM, CreatureGameFSMAI)

    def test_species_classes(self):
        self.assertTrue(issubclass(DistributedSeagullAI, DistributedAnimalAI))
        self.assertTrue(issubclass(DistributedSeaSerpentAI, DistributedCreatureAI))

    def test_flytrap_is_stationary(self):
        for avatarType in (AvatarTypes.FlyTrap, AvatarTypes.FlyTrap.getBossType()):
            npc = makeCreature(DistributedCreatureAI, avatarType)
            self.assertTrue(npc.isStationary())

            npc.setStartState('Patrol')
            self.assertEqual(npc.getStartState(), 'Idle')

            npc.gameFSM.request('Patrol')
            self.assertEqual(npc.gameFSM.state, 'Idle')
            npc.gameFSM.request('Walk')
            self.assertEqual(npc.gameFSM.state, 'Idle')

            self.assertFalse(npc.gameFSM.shouldFollowTarget(Mock()))

    def test_mobile_creatures_still_patrol(self):
        npc = makeCreature(DistributedCreatureAI, AvatarTypes.Crab)
        self.assertFalse(npc.isStationary())

        npc.setStartState('Patrol')
        self.assertEqual(npc.getStartState(), 'Patrol')

        with patch.object(BattleNPCGameFSMAI, 'findNextWalkToPoint'):
            npc.gameFSM.request('Patrol')

        self.assertEqual(npc.gameFSM.state, 'Patrol')

    def test_stationary_attack_only_uses_skills_in_range(self):
        npc = makeCreature(DistributedCreatureAI, AvatarTypes.FlyTrap)
        target = Mock(doId=5)
        npc.currentTarget = target
        npc.useTargetedSkill = Mock()
        npc.air.targetMgr.getAttackers.return_value = []

        npc.air.battleMgr.getTargetInRange.side_effect = \
            lambda attacker, tgt, skillId, ammo: skillId == EnemySkills.FLYTRAP_SPIT

        task = Mock()
        npc.gameFSM._chooseNextAttack(task)
        npc.useTargetedSkill.assert_called_once()
        self.assertEqual(npc.useTargetedSkill.call_args[0][2], EnemySkills.FLYTRAP_SPIT)

        # nothing in range: no attack, just wait a moment
        npc.useTargetedSkill.reset_mock()
        npc.air.battleMgr.getTargetInRange.side_effect = None
        npc.air.battleMgr.getTargetInRange.return_value = False
        npc.gameFSM._chooseNextAttack(task)
        npc.useTargetedSkill.assert_not_called()
        task.setDelay.assert_called_with(WeaponGlobals.SHORT_DELAY)

    def test_creatures_do_not_send_empty_chat(self):
        npc = makeCreature(DistributedCreatureAI, AvatarTypes.Crab)
        npc.d_setChat('')
        npc.sendUpdate.assert_not_called()
        npc.d_setChat('hello', 0)
        npc.sendUpdate.assert_called_once_with('setChat', ['hello', 0])

    def test_passive_creature_ignores_aggro(self):
        npc = makeCreature(DistributedCreatureAI, AvatarTypes.Monkey)
        npc.handleClientAggro = Mock()
        npc.requestClientAggro()
        npc.handleClientAggro.assert_not_called()


class AnimalTests(unittest.TestCase):
    def test_animals_never_battle(self):
        animal = makeCreature(DistributedAnimalAI, AvatarTypes.Pig)
        for state in ('Battle', 'AttackChase', 'BreakCombat'):
            animal.gameFSM.request(state)
            self.assertEqual(animal.gameFSM.state, 'Off')

        animal.gameFSM.request('Ambush')
        self.assertEqual(animal.gameFSM.state, 'Idle')

        animal.setStartState('Ambush')
        self.assertEqual(animal.getStartState(), 'Idle')
        animal.setStartState('Walk')
        self.assertEqual(animal.getStartState(), 'Walk')

    def test_animals_are_not_targets(self):
        animal = makeCreature(DistributedAnimalAI, AvatarTypes.Chicken)
        self.assertFalse(animal.getDamagable())
        self.assertFalse(animal.isBattleable())

        animal.handleClientAggro = Mock()
        animal.requestClientAggro()
        animal.handleClientAggro.assert_not_called()

        with patch.object(DistributedCreatureAI, 'generate'):
            animal.generate()
        animal.air.targetMgr.removeTarget.assert_called_once_with(animal)


class SpawnerTests(unittest.TestCase):
    def test_animal_team(self):
        node = spawner.AnimalSpawnNode.__new__(spawner.AnimalSpawnNode)
        self.assertEqual(node.getNPCTeam(AvatarTypes.Chicken), PiratesGlobals.VILLAGER_TEAM)
        self.assertIs(node.getNPCClass(AvatarTypes.Seagull), DistributedAnimalAI)

    def makeBossNode(self, objType, objectData):
        node = spawner.BossEnemySpawnNode.__new__(spawner.BossEnemySpawnNode)
        node._objType = objType
        node._objectData = objectData
        return node

    def test_creature_boss_flag(self):
        node = self.makeBossNode('Creature', {'Species': 'Crab'})
        avatarType = node.getAvatarType()
        self.assertEqual(avatarType, AvatarTypes.Crab)
        self.assertIs(node.getNPCClass(avatarType), DistributedCreatureAI)

        node = self.makeBossNode('Creature', {'Species': 'Huge Gator', 'Boss': True})
        avatarType = node.getAvatarType()
        self.assertTrue(avatarType.getBoss())
        self.assertIs(node.getNPCClass(avatarType), DistributedBossCreatureAI)

    def test_enemy_creature_classes(self):
        node = spawner.EnemySpawnNode.__new__(spawner.EnemySpawnNode)
        for name in ('Crab', 'FlyTrap', 'Stump', 'Bat', 'Wasp', 'Scorpion', 'Alligator', 'Monkey'):
            avatarType = getattr(AvatarTypes, name)
            self.assertIs(node.getNPCClass(avatarType), DistributedCreatureAI)
            self.assertIs(node.getNPCClass(avatarType.getBossType()), DistributedBossCreatureAI)


if __name__ == '__main__':
    unittest.main()
