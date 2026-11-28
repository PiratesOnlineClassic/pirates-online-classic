import builtins
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

from panda3d.core import Filename, NodePath, VirtualFileSystem, loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')


def _stubWeaponGlobals():
    # WeaponGlobals reads WeaponGlobals.pkl from the game resources at import
    # time; when the resources are unavailable fall back to a stub module.
    searchPath = '../resources/phase_2/etc'
    if VirtualFileSystem.getGlobalPtr().exists(Filename(searchPath + '/WeaponGlobals.pkl')):
        return

    module = types.ModuleType('pirates.battle.WeaponGlobals')

    def __getattr__(name):
        if name.startswith('__'):
            raise AttributeError(name)

        value = MagicMock(name='WeaponGlobals.%s' % name)
        setattr(module, name, value)
        return value

    module.__getattr__ = __getattr__
    sys.modules['pirates.battle.WeaponGlobals'] = module
    import pirates.battle
    pirates.battle.WeaponGlobals = module


_stubWeaponGlobals()

if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

with patch.object(builtins.loader, 'loadFont', Mock()):
    from pirates.battle import BattleManagerAI as battle_manager_module
    from pirates.battle.BattleManagerAI import BattleManagerAI

from pirates.battle import EnemyGlobals
from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI
from pirates.battle.DistributedEnemySpawnerAI import SpawnNodeBase, DistributedEnemySpawnerAI
from pirates.pirate.BattleNPCGameFSMAI import BattleNPCGameFSMAI
from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI
from pirates.uberdog.UberDogGlobals import InventoryType


def makeTarget(doId=42, hp=100, state='LandRoam'):
    target = SimpleNamespace(doId=doId)
    target.isDeleted = lambda: False
    target.getHp = lambda: [hp, False]
    target.gameFSM = SimpleNamespace(getCurrentOrNextState=lambda: state)
    return target


class BattleNPCAITests(unittest.TestCase):
    def makeNPC(self, state='Patrol', sender=None):
        npc = DistributedBattleNPCAI.__new__(DistributedBattleNPCAI)
        npc.doId = 1000
        npc.currentTarget = None
        npc.aggroMode = EnemyGlobals.AGGRO_MODE_DEFAULT
        npc.aggroRadius = 0
        npc.ambush = False
        npc.vehicleDoId = 0
        npc.gameFSM = SimpleNamespace(state=state, getCurrentOrNextState=lambda: state)
        npc.air = SimpleNamespace(doId2do={}, getAvatarIdFromSender=lambda: sender.doId if sender else 0,
            battleMgr=SimpleNamespace(getModifiedExperienceGrade=Mock(return_value=EnemyGlobals.YELLOW)))
        if sender:
            npc.air.doId2do[sender.doId] = sender

        npc.sendUpdate = Mock()
        npc.handleClientAggro = Mock()
        return npc

    def test_set_ambush_is_sent_to_the_client(self):
        npc = self.makeNPC()
        npc.b_setAmbush(True)
        self.assertTrue(npc.getAmbush())
        npc.sendUpdate.assert_called_once_with('setAmbush', [True])

    def test_b_set_spawn_pos_accepts_a_position(self):
        npc = self.makeNPC()
        npc.b_setSpawnPos((1, 2, 3))
        self.assertEqual(npc.getSpawnPos(), [1, 2, 3])
        npc.sendUpdate.assert_called_once_with('setSpawnPos', [1, 2, 3])

    def test_board_vehicle_is_broadcast(self):
        npc = self.makeNPC()
        npc.b_boardVehicle(5000)
        self.assertEqual(npc.getVehicleDoId(), 5000)
        npc.sendUpdate.assert_called_once_with('boardVehicle', [5000])

    def test_ambush_intro_done_springs_the_ambush(self):
        avatar = makeTarget()
        npc = self.makeNPC(state='Ambush', sender=avatar)
        npc.getDistance = Mock(return_value=5)
        npc.ambushIntroDone()
        npc.handleClientAggro.assert_called_once_with(avatar)

    def test_ambush_intro_done_ignores_far_or_non_ambushing(self):
        avatar = makeTarget()
        npc = self.makeNPC(state='Ambush', sender=avatar)
        npc.getDistance = Mock(return_value=EnemyGlobals.INSTANT_AGGRO_RADIUS_DEFAULT + 1)
        npc.ambushIntroDone()

        npc.gameFSM = SimpleNamespace(state='Patrol')
        npc.getDistance = Mock(return_value=1)
        npc.ambushIntroDone()
        npc.handleClientAggro.assert_not_called()

    def test_ambush_aggro_is_only_handled_once(self):
        avatar = makeTarget()
        npc = self.makeNPC(state='Ambush', sender=avatar)
        npc.requestClientAggro()
        npc.handleClientAggro.assert_called_once_with(avatar)
        npc.air.battleMgr.getModifiedExperienceGrade.assert_not_called()

    def test_aggro_ignored_when_already_fighting(self):
        avatar = makeTarget()
        npc = self.makeNPC(state='Battle', sender=avatar)
        npc.currentTarget = makeTarget(doId=43)
        npc.air.doId2do[43] = npc.currentTarget
        npc.requestClientAggro()
        npc.handleClientAggro.assert_not_called()

    def test_aggro_ignores_dead_avatar(self):
        avatar = makeTarget(hp=0)
        npc = self.makeNPC(sender=avatar)
        npc.requestClientAggro()
        npc.handleClientAggro.assert_not_called()

    def test_aggro_on_patrol(self):
        avatar = makeTarget()
        npc = self.makeNPC(sender=avatar)
        npc.requestClientAggro()
        npc.handleClientAggro.assert_called_once_with(avatar)

    def test_handle_client_aggro_ignored_while_breaking_combat(self):
        avatar = makeTarget()
        npc = self.makeNPC(state='BreakCombat')
        del npc.handleClientAggro
        npc.b_setCurrentTarget = Mock()
        npc.b_setGameState = Mock()
        npc.handleClientAggro(avatar)
        npc.b_setCurrentTarget.assert_not_called()
        npc.b_setGameState.assert_not_called()

    def test_refused_game_state_is_not_broadcast(self):
        npc = self.makeNPC(state='BreakCombat')
        npc.gameFSM = SimpleNamespace(request=Mock(), getCurrentOrNextState=lambda: 'BreakCombat')
        npc.b_setGameState('Battle')
        npc.sendUpdate.assert_not_called()

    def test_is_target_valid(self):
        npc = self.makeNPC()
        alive = makeTarget(doId=1)
        dead = makeTarget(doId=2, state='Death')
        gone = makeTarget(doId=3)
        npc.air.doId2do = {1: alive, 2: dead}
        self.assertTrue(npc.isTargetValid(alive))
        self.assertFalse(npc.isTargetValid(dead))
        self.assertFalse(npc.isTargetValid(gone))
        self.assertFalse(npc.isTargetValid(None))


class BattleNPCGameFSMAITests(unittest.TestCase):
    def makeFSM(self, attackers=()):
        fsm = BattleNPCGameFSMAI.__new__(BattleNPCGameFSMAI)
        avatar = SimpleNamespace(doId=1000, currentTarget=None, isTargetValid=lambda target: bool(target and target.alive),
            getSkillEffectIds=lambda: [])
        avatar.currentWeaponId = 0
        avatar.b_setCurrentTarget = Mock()
        avatar.getSpawnNode = Mock(return_value=None)
        avatar.uniqueName = lambda name: '%s-1000' % name
        fsm.avatar = avatar
        fsm.air = SimpleNamespace(doId2do={}, targetMgr=Mock(), battleMgr=Mock())
        fsm.air.targetMgr.getAttackers.return_value = list(attackers)
        fsm.demand = Mock()
        fsm.ignore = Mock()
        return fsm

    def test_choose_next_attack_breaks_combat_without_targets(self):
        fsm = self.makeFSM()
        fsm.air.targetMgr.findTargetableObject.return_value = None
        task = SimpleNamespace(done='done')
        self.assertEqual(fsm._chooseNextAttack(task), 'done')
        fsm.demand.assert_called_once_with('BreakCombat')

    def test_choose_next_attack_waits_until_in_range(self):
        fsm = self.makeFSM()
        fsm.avatar.currentTarget = SimpleNamespace(doId=42, alive=True)
        fsm.avatar.avatarType = SimpleNamespace()
        fsm.avatar.useTargetedSkill = Mock()
        fsm.air.battleMgr.getTargetInRange.return_value = False
        task = SimpleNamespace(again='again', setDelay=Mock())
        with patch('pirates.pirate.BattleNPCGameFSMAI.EnemyGlobals.getBaseSkills', return_value=([], [1])):
            self.assertEqual(fsm._chooseNextAttack(task), 'again')

        fsm.avatar.useTargetedSkill.assert_not_called()

    def test_find_new_attack_target_prunes_dead_attackers(self):
        fsm = self.makeFSM(attackers=[1, 2])
        dead = SimpleNamespace(doId=1, alive=False)
        alive = SimpleNamespace(doId=2, alive=True)
        fsm.air.doId2do = {1: dead, 2: alive}
        fsm.air.targetMgr.findTargetableObject.return_value = 2
        self.assertIs(fsm.findNewAttackTarget(), alive)
        fsm.air.targetMgr.removeAttacker.assert_called_once_with(dead, fsm.avatar)
        fsm.avatar.b_setCurrentTarget.assert_called_once_with(2)

    def test_stop_movement_pauses_instead_of_finishing(self):
        fsm = self.makeFSM()
        interval = Mock()
        fsm._BattleNPCGameFSMAI__movementInterval = interval
        fsm._BattleNPCGameFSMAI__pausedTask = None
        fsm._BattleNPCGameFSMAI__attackChaseTask = None
        fsm._stopMovement()
        interval.pause.assert_called_once_with()
        interval.finish.assert_not_called()
        fsm.ignore.assert_called_once_with(fsm.getWalkToPointDoneName())

    def test_death_rewards_then_clears_attackers(self):
        fsm = self.makeFSM()
        spawnNode = Mock()
        fsm.avatar.getSpawnNode.return_value = spawnNode
        fsm.enterDeath()
        fsm.air.battleMgr.rewardAttackers.assert_called_once_with(fsm.avatar)
        fsm.air.targetMgr.clearTarget.assert_called_once_with(fsm.avatar)
        spawnNode.processDeath.assert_called_once_with()


class EnemySpawnerAITests(unittest.TestCase):
    def test_non_respawning_node_is_removed(self):
        air = SimpleNamespace(enemySpawner=Mock())
        node = SpawnNodeBase(air, 'Spawn Node', {'Respawns': False}, None, 'objKey')
        npc = Mock()
        npc.uniqueName = lambda name: name
        node._npc = npc
        task = SimpleNamespace(done='done')
        self.assertEqual(node._SpawnNodeBase__respawn(task), 'done')
        npc.requestDelete.assert_called_once_with()
        air.enemySpawner.removeSpawnNode.assert_called_once_with('Spawn Node', node)
        self.assertIsNone(node.npc)

    def test_holiday_despawn_forgets_npc(self):
        node = SpawnNodeBase(SimpleNamespace(), 'Spawn Node', {}, None, 'objKey')
        npc = Mock()
        npc.uniqueName = lambda name: name
        node._npc = npc
        node._SpawnNodeBase__died(npc)
        npc.requestDelete.assert_called_once_with()
        self.assertIsNone(node.npc)

    def test_get_spawn_node_from_type_and_key(self):
        spawner = DistributedEnemySpawnerAI.__new__(DistributedEnemySpawnerAI)
        node = SimpleNamespace(objKey='abc')
        spawner.spawnNodes = {'Spawn Node': [node]}
        self.assertIs(spawner.getSpawnNodeFromTypeAndKey('Spawn Node', 'abc'), node)


class BattleManagerRewardTests(unittest.TestCase):
    def test_reward_sends_reputation_message(self):
        manager = BattleManagerAI.__new__(BattleManagerAI)
        manager.air = SimpleNamespace(questMgr=Mock())
        inventory = Mock()
        inventory.getReputation.return_value = 0
        inventory.getOverallRep.return_value = 0
        # no treasure collections have been started...
        inventory.getStackQuantity.return_value = 0
        attacker = DistributedPlayerPirateAI.__new__(DistributedPlayerPirateAI)
        attacker.doId = 42
        attacker.getInventory = Mock(return_value=inventory)
        attacker.isPaid = Mock(return_value=True)
        attacker.getLevel = Mock(return_value=5)
        attacker.d_sendReputationMessage = Mock()
        attacker.battleSkillDiary = Mock()
        attacker.battleSkillDiary.getSkills.return_value = [100]
        attacker.battleSkillDiary.getSkill.return_value = [0, 0, 25]
        target = SimpleNamespace(doId=1000, getAvatarType=Mock(), getLevel=Mock(return_value=1))

        with patch.object(battle_manager_module.WeaponGlobals, 'getSkillReputationCategoryId', return_value=InventoryType.CutlassRep), \
                patch.object(battle_manager_module.random, 'random', return_value=0.0):
            manager.rewardAttacker(attacker, target)

        inventory.setOverallRep.assert_called_once_with(25)
        attacker.d_sendReputationMessage.assert_called_once_with(1000, [InventoryType.CutlassRep], [25], 0, 0, 0, 0)
        manager.air.questMgr.enemyDefeated.assert_called_once_with(attacker, target)

    def test_reward_skips_missing_and_non_player_attackers(self):
        manager = BattleManagerAI.__new__(BattleManagerAI)
        npcAttacker = SimpleNamespace(doId=7, getInventory=Mock())
        manager.air = SimpleNamespace(doId2do={7: npcAttacker}, targetMgr=Mock())
        manager.air.targetMgr.getAttackers.return_value = [6, 7]
        manager.rewardAttackers(SimpleNamespace(doId=1000))
        npcAttacker.getInventory.assert_not_called()


if __name__ == '__main__':
    unittest.main()


class EnemySkillSelectionTests(unittest.TestCase):
    def makeFSM(self, fsmClass, avatarType, weaponId):
        fsm = fsmClass.__new__(fsmClass)
        target = SimpleNamespace(doId=42, alive=True)
        avatar = SimpleNamespace(doId=1000, currentTarget=target, avatarType=avatarType, currentWeaponId=weaponId,
            isTargetValid=lambda target: bool(target and target.alive), getSkillEffectIds=lambda: [])
        avatar.useTargetedSkill = Mock()
        avatar.getPos = Mock(return_value=(0, 0, 0))
        fsm.avatar = avatar
        fsm.air = SimpleNamespace(doId2do={}, targetMgr=Mock(), battleMgr=Mock())
        fsm.air.battleMgr.getTargetInRange.return_value = True
        fsm.demand = Mock()
        return fsm

    def test_enemies_only_use_the_skills_of_the_weapon_they_hold(self):
        from pirates.battle import WeaponGlobals
        from pirates.pirate import AvatarTypes

        # the undead raider knows both cutlass and dagger skills...
        fsm = self.makeFSM(BattleNPCGameFSMAI, AvatarTypes.Zombie, InventoryType.DaggerWeaponL1)
        repId = WeaponGlobals.getRepId(InventoryType.DaggerWeaponL1)
        skills = fsm.getUsableSkills()
        self.assertTrue(skills)
        self.assertTrue(all(WeaponGlobals.isValidSkill(skillId, InventoryType.DaggerWeaponL1, repId) for skillId in skills))
        self.assertLess(len(skills), len(fsm.getAttackSkills()))

        task = SimpleNamespace(again='again', setDelay=Mock())
        for _ in range(10):
            fsm._chooseNextAttack(task)

        usedSkills = set(c[0][2] for c in fsm.avatar.useTargetedSkill.call_args_list)
        self.assertTrue(usedSkills.issubset(set(skills)))

        # enemy attacks never carry any area targets...
        self.assertTrue(all(c[0][4] == [] for c in fsm.avatar.useTargetedSkill.call_args_list))

    def test_enemies_without_skills_never_attack(self):
        fsm = self.makeFSM(BattleNPCGameFSMAI, SimpleNamespace(), 0)
        task = SimpleNamespace(again='again', setDelay=Mock())
        with patch('pirates.pirate.BattleNPCGameFSMAI.EnemyGlobals.getBaseSkills', return_value=([], [])):
            self.assertEqual(fsm._chooseNextAttack(task), 'again')

        fsm.avatar.useTargetedSkill.assert_not_called()

    def test_bosses_choose_attacks_like_every_other_enemy(self):
        from pirates.npc.BossNPCGameFSMAI import BossNPCGameFSMAI

        fsm = self.makeFSM(BossNPCGameFSMAI, SimpleNamespace(), 0)
        fsm.avatar.getAttackSkills = Mock(return_value=[InventoryType.CutlassHack])
        fsm.air.targetMgr.getAttackers.return_value = [7, 8]
        task = SimpleNamespace(again='again', setDelay=Mock())

        # bosses wait for their target to come within range of their skill...
        fsm.air.battleMgr.getTargetInRange.return_value = False
        fsm._chooseNextAttack(task)
        fsm.avatar.useTargetedSkill.assert_not_called()

        fsm.air.battleMgr.getTargetInRange.return_value = True
        fsm._chooseNextAttack(task)
        args = fsm.avatar.useTargetedSkill.call_args[0]
        self.assertEqual(args[2], InventoryType.CutlassHack)
        self.assertEqual(args[4], [])

        # and look for a new target when their target is gone...
        fsm.avatar.currentTarget.alive = False
        fsm.air.targetMgr.findTargetableObject.return_value = None
        fsm.avatar.b_setCurrentTarget = Mock()
        fsm._chooseNextAttack(SimpleNamespace(done='done'))
        fsm.demand.assert_called_once_with('BreakCombat')
