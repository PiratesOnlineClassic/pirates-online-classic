import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, call, patch

from direct.showbase.MessengerGlobal import messenger
from direct.task import Task
from pirates.piratesbase import PiratesGlobals
from tests.pirates.quest.test_quest_manager_ai_progression import manager_module
from pirates.quest.DistributedQuestAI import DistributedQuestAI
from pirates.quest.Quest import Quest
from pirates.quest.QuestDNA import QuestDNA
from pirates.quest import QuestDB
from pirates.quest.QuestConstants import QuestItems
from pirates.quest.QuestEvent import TreasureChestOpened
from pirates.quest.QuestTaskDNA import RecoverTreasureItemTaskDNA
from pirates.quest.QuestTaskState import QuestTaskState
from pirates.treasuremap import DistributedBuriedTreasureAI as buried_module
from pirates.treasuremap.DistributedBuriedTreasureAI import DistributedBuriedTreasureAI
from pirates.treasuremap.DistributedSurfaceTreasureAI import DistributedSurfaceTreasureAI


class FakeTaskManager:
    def __init__(self):
        self.tasks = {}

    def doMethodLater(self, delay, callback, name):
        self.tasks[name] = callback

    def remove(self, name):
        self.tasks.pop(name, None)

    def run(self, name):
        callback = self.tasks.pop(name)
        task = SimpleNamespace(done='done', again='again')
        result = callback(task)
        if result == task.again:
            self.tasks[name] = callback
        return result


class BuriedTreasureAITests(unittest.TestCase):
    def setUp(self):
        self.sender = 42
        self.avatar = SimpleNamespace(
            doId=self.sender, uniqueName=lambda event: '%s-42' % event,
            getParentObj=lambda: SimpleNamespace(getUniqueId=lambda: 'island'),
            getAccess=lambda: 2, getQuestHistory=lambda: self.history,
            b_setQuestHistory=lambda value: setattr(self, 'history', value),
            getTutorial=lambda: 0)
        self.history = []
        self.stub = SimpleNamespace(complete=False, handleQuestComplete=Mock())
        self.avatar.questStatus = SimpleNamespace(
            getQuestStub=lambda questId: self.stub, getNPCInteractMode=lambda: False)
        self.air = SimpleNamespace(
            getAvatarIdFromSender=lambda: self.sender,
            doId2do={self.sender: self.avatar},
            logPotentialHacker=Mock())
        self.air.questMgr = manager_module.QuestManagerAI(self.air)
        self.treasure = DistributedBuriedTreasureAI.__new__(DistributedBuriedTreasureAI)
        self.treasure.air = self.air
        self.treasure.doId = 100
        self.treasure.uniqueId = 'treasure'
        self.treasure.userId = 0
        self.treasure.currentUser = None
        self.treasure.currentDepth = 2
        self.treasure.startingDepth = 2
        self.treasure.digging = False
        self.treasure.uniqueName = lambda name: '%s-100' % name
        self.updates = []
        self.treasure.sendUpdate = lambda field, args: self.updates.append((field, args))
        self.treasure.sendUpdateToAvatarId = lambda av, field, args: self.updates.append(
            (field, args))
        self.tasks = FakeTaskManager()
        self.task_patch = patch.object(buried_module, 'taskMgr', self.tasks)
        self.task_patch.start()
        self.addCleanup(self.task_patch.stop)
        self.messenger_patch = patch.object(builtins, 'messenger', messenger, create=True)
        self.messenger_patch.start()
        self.addCleanup(self.messenger_patch.stop)
        self.set_quest()

    def set_quest(self, goal=1, probability=1.0, max_attempts=1,
                  requires_visit=False):
        quest = DistributedQuestAI.__new__(DistributedQuestAI)
        Quest.__init__(quest)
        quest.doId = 200
        quest.questId = 'treasure-quest'
        quest.rewards = []
        task_dna = RecoverTreasureItemTaskDNA(
            item=QuestItems.Treasure, num=goal, maxAttempts=max_attempts,
            probability=probability)
        quest.questDNA = QuestDNA(tasks=task_dna, velvetRoped=False, questInt=123,
                                  completeRequiresVisit=requires_visit)
        quest.tasks = quest.questDNA.getTasks()
        quest.combineOp = QuestDNA.OR
        quest.taskStates = [QuestTaskState(goal=goal)]
        quest.taskStates[0].acquire()
        quest.sendTaskStates = Mock(wraps=quest.sendTaskStates)
        self.air.questMgr.quests[self.sender] = {quest.doId: quest}
        self.quest = quest

    def start_dig(self):
        self.treasure.requestInteraction(self.sender, 0, False)

    def test_quest_progress_and_completion_only_after_digging(self):
        self.assertFalse(hasattr(self.quest, 'getProgress'))
        self.start_dig()

        self.assertEqual(self.quest.getTaskProgress(), [(0, 1)])
        self.assertEqual(self.quest.taskStates[0].getAttempts(), 0)
        self.assertEqual(self.history, [])
        self.quest.sendTaskStates.assert_not_called()
        self.assertEqual([field for field, _ in self.updates],
                         ['setUserId', 'acceptInteraction', 'startDigging'])
        self.assertEqual(self.treasure.currentUser, self.sender)
        self.assertEqual(self.treasure.userId, self.sender)
        self.assertEqual(self.treasure.handleRequestInteraction(self.avatar, 0, False),
                         self.treasure.DENY)

        self.assertEqual(self.tasks.run('digTask-100'), 'again')
        self.assertEqual(self.quest.getTaskProgress(), [(0, 1)])
        self.assertEqual(self.tasks.run('digTask-100'), 'done')
        self.assertEqual(self.quest.getTaskProgress(), [(1, 1)])
        self.assertEqual(self.history, [123])
        self.stub.handleQuestComplete.assert_called_once_with(self.quest, [])
        self.assertIn(('stopDigging', [1]), self.updates)
        self.assertIn(('showTreasure', [0]), self.updates)
        self.assertEqual(self.tasks.run('digResetTask-100'), 'done')
        self.assertIsNone(self.treasure.currentUser)
        self.assertEqual(self.treasure.userId, 0)
        self.assertEqual(self.treasure.currentDepth, 2)
        self.assertEqual(self.tasks.tasks, {})

    def test_exit_during_reveal_cancels_the_reset_task(self):
        self.start_dig()
        self.tasks.run('digTask-100')
        self.tasks.run('digTask-100')
        self.assertIn('digResetTask-100', self.tasks.tasks)
        self.treasure.requestExit()
        self.assertIsNone(self.treasure.currentUser)
        self.assertEqual(self.treasure.userId, 0)
        self.assertEqual(self.treasure.currentDepth, 2)
        self.assertEqual(self.tasks.tasks, {})

    def test_demand_exit_stops_digging_and_releases_user(self):
        self.start_dig()
        self.treasure.demandExit()
        self.assertIn(('stopDigging', [1]), self.updates)
        self.assertIsNone(self.treasure.currentUser)
        self.assertEqual(self.treasure.userId, 0)
        self.assertEqual(self.tasks.tasks, {})

    def test_exit_is_owner_only_and_cancels_the_active_task(self):
        self.start_dig()
        self.tasks.run('digTask-100')
        self.sender = 99
        self.air.doId2do[99] = SimpleNamespace(doId=99, uniqueName=lambda event: event)
        self.treasure.requestExit()
        self.assertEqual(self.treasure.currentUser, 42)
        self.assertIn('digTask-100', self.tasks.tasks)
        self.sender = 42
        self.treasure.requestExit()
        self.assertIsNone(self.treasure.currentUser)
        self.assertEqual(self.treasure.userId, 0)
        self.assertEqual(self.treasure.currentDepth, 2)
        self.assertEqual(self.tasks.tasks, {})

        self.assertFalse(self.quest.isComplete())
        self.assertEqual(self.quest.taskStates[0].getAttempts(), 0)
        self.assertEqual(self.history, [])
        self.quest.sendTaskStates.assert_not_called()

    def test_disconnect_during_dig_resets_and_releases_user(self):
        self.start_dig()
        del self.air.doId2do[42]
        self.assertEqual(self.tasks.run('digTask-100'), 'done')
        self.assertIsNone(self.treasure.currentUser)
        self.assertEqual(self.treasure.userId, 0)
        self.assertEqual(self.treasure.currentDepth, 2)
        self.assertEqual(self.tasks.tasks, {})
        self.assertEqual(self.quest.getTaskProgress(), [(0, 1)])
        self.assertEqual(self.quest.taskStates[0].getAttempts(), 0)

    def test_delete_stops_active_dig_and_removes_tasks(self):
        self.start_dig()
        with patch.object(buried_module.DistributedInteractiveAI, 'delete'):
            self.treasure.delete()
        self.assertIn(('stopDigging', [1]), self.updates)
        self.assertIsNone(self.treasure.currentUser)
        self.assertEqual(self.tasks.tasks, {})
        self.assertEqual(self.quest.getTaskProgress(), [(0, 1)])
        self.assertEqual(self.quest.taskStates[0].getAttempts(), 0)

    def test_delete_during_reveal_removes_reset_task(self):
        self.start_dig()
        self.tasks.run('digTask-100')
        self.tasks.run('digTask-100')
        with patch.object(buried_module.DistributedInteractiveAI, 'delete'):
            self.treasure.delete()
        self.assertEqual(self.tasks.tasks, {})
        self.assertEqual([field for field, _ in self.updates].count('stopDigging'), 1)

    def test_partial_progress_is_reported_without_completing_quest(self):
        self.set_quest(goal=2)
        self.start_dig()
        self.assertEqual(self.quest.getTaskProgress(), [(0, 2)])
        self.tasks.run('digTask-100')
        self.tasks.run('digTask-100')
        self.assertEqual(self.quest.getTaskProgress(), [(1, 2)])
        self.assertIn(('stopDigging', [1]), self.updates)
        self.assertEqual(self.history, [])
        self.stub.handleQuestComplete.assert_not_called()
        self.tasks.run('digResetTask-100')
        self.start_dig()
        self.tasks.run('digTask-100')
        self.tasks.run('digTask-100')
        self.assertEqual(self.quest.getTaskProgress(), [(2, 2)])
        self.assertEqual(self.history, [123])

    def test_unsuccessful_roll_reports_no_progress(self):
        self.set_quest(probability=0.0, max_attempts=3)
        with patch.object(TreasureChestOpened, 'getRng',
                          return_value=SimpleNamespace(random=lambda: 0.5)):
            self.start_dig()
            self.tasks.run('digTask-100')
            self.tasks.run('digTask-100')
        self.assertEqual(self.quest.getTaskProgress(), [(0, 1)])
        self.assertEqual(self.quest.taskStates[0].getAttempts(), 1)
        self.assertIn(('stopDigging', [0]), self.updates)
        self.assertEqual(self.history, [])
        self.quest.sendTaskStates.assert_called_once()
        self.tasks.run('digResetTask-100')
        with patch.object(TreasureChestOpened, 'getRng',
                          return_value=SimpleNamespace(random=lambda: 0.5)):
            self.start_dig()
            self.tasks.run('digTask-100')
            self.tasks.run('digTask-100')
        self.assertEqual(self.quest.taskStates[0].getAttempts(), 2)
        self.tasks.run('digResetTask-100')
        self.start_dig()
        self.tasks.run('digTask-100')
        self.tasks.run('digTask-100')
        self.assertEqual(self.quest.getTaskProgress(), [(1, 1)])
        self.assertEqual(self.history, [123])
        self.assertEqual(self.updates[-2], ('stopDigging', [1]))

    def test_multiple_active_treasure_quests_receive_the_event(self):
        first = self.quest
        self.set_quest(goal=2)
        second = self.quest
        second.doId = 201
        second.questDNA.setQuestInt(124)
        self.air.questMgr.quests[self.sender] = {first.doId: first, second.doId: second}
        self.start_dig()
        self.tasks.run('digTask-100')
        self.tasks.run('digTask-100')
        self.assertEqual(first.getTaskProgress(), [(1, 1)])
        self.assertEqual(second.getTaskProgress(), [(1, 2)])
        self.assertEqual(self.history, [123])
        self.assertIn(('stopDigging', [1]), self.updates)

    def test_nonmatching_treasure_does_not_change_quest(self):
        task_dna = self.quest.questDNA.getTasks()[0]
        task_dna.treasureId = 'specific'
        with patch('pirates.quest.QuestTaskDNA.getTreasureList', return_value=['elsewhere']):
            self.start_dig()
            self.tasks.run('digTask-100')
            self.tasks.run('digTask-100')
        self.assertEqual(self.quest.getTaskProgress(), [(0, 1)])
        self.assertEqual(self.quest.taskStates[0].getAttempts(), 0)
        self.assertIn(('stopDigging', [0]), self.updates)

    def test_auto_finalize_scene_starts_after_digging(self):
        self.quest.questDNA.setFinalizeInfo(({'type': 'cutscene'},))
        self.air.questMgr.finalizeCutscene = Mock()
        self.start_dig()
        self.air.questMgr.finalizeCutscene.assert_not_called()
        self.tasks.run('digTask-100')
        self.tasks.run('digTask-100')
        self.air.questMgr.finalizeCutscene.assert_called_once_with(self.avatar, self.quest)
        self.assertEqual(self.history, [])

    def test_quest_error_does_not_leave_dig_locked(self):
        self.air.questMgr.finishBuriedTreasure = Mock(side_effect=RuntimeError('quest failed'))
        self.start_dig()
        self.tasks.run('digTask-100')
        with self.assertRaisesRegex(RuntimeError, 'quest failed'):
            self.tasks.run('digTask-100')
        self.assertIsNone(self.treasure.currentUser)
        self.assertEqual(self.treasure.userId, 0)
        self.assertEqual(self.tasks.tasks, {})

    def test_completed_quest_requiring_visit_is_not_turned_in_early(self):
        self.set_quest(requires_visit=True)
        quest_id = 'c3r2r3.2recoverEffects'
        dna = QuestDB.QuestDict[quest_id]
        self.quest.questId = quest_id
        self.quest.questDNA = dna
        self.quest.tasks = dna.getTasks()
        self.quest.rewards = dna.getRewards()
        self.quest.taskStates[0].setAttempts(dna.getTasks()[0].maxAttempts - 1)
        self.treasure.uniqueId = '1178300160.0dxschafe'
        self.air.questMgr._giveRewards = Mock(return_value=True)
        self.start_dig()
        self.tasks.run('digTask-100')
        self.tasks.run('digTask-100')
        self.assertTrue(self.quest.isComplete())
        self.assertIn(('stopDigging', [1]), self.updates)
        self.assertEqual(self.history, [])
        self.stub.handleQuestComplete.assert_not_called()
        npc = manager_module.DistributedNPCTownfolkAI()
        npc.doId = 300
        npc.getUniqueId = lambda: 'other-npc'
        npc.d_setQuestsCompleted = Mock()
        self.air.questMgr.requestInteract(self.avatar, npc)
        npc.d_setQuestsCompleted.assert_not_called()
        npc.getUniqueId = lambda: dna.getReturnGiverIds()[0]
        self.air.questMgr.requestInteract(self.avatar, npc)
        npc.d_setQuestsCompleted.assert_called_once_with(
            self.avatar.doId, completedQuestIds=[quest_id], completedQuestDoIds=[200])
        self.air.questMgr.requestInteract(self.avatar, npc)
        npc.d_setQuestsCompleted.assert_called_once()
        self.assertEqual(self.history, [])
        messenger.send(self.avatar.uniqueName('interact-canceled'))
        self.assertEqual(self.history, [dna.getQuestInt()])
        self.air.questMgr._giveRewards.assert_called_once_with(self.avatar, dna.getRewards())
        self.stub.handleQuestComplete.assert_called_once_with(self.quest, [])

    def test_dig_without_quest_still_reports_no_progress(self):
        self.air.questMgr.quests.clear()
        self.start_dig()
        self.tasks.run('digTask-100')
        self.tasks.run('digTask-100')
        self.assertIn(('stopDigging', [0]), self.updates)


class SurfaceTreasureAITests(unittest.TestCase):
    def test_withdraw_type_is_stored_and_broadcast(self):
        treasure = DistributedSurfaceTreasureAI.__new__(DistributedSurfaceTreasureAI)
        treasure.withdrawType = 0
        treasure.sendUpdate = Mock()

        treasure.b_setWithdrawType(3)

        self.assertEqual(treasure.getWithdrawType(), 3)
        treasure.sendUpdate.assert_called_once_with('setWithdrawType', [3])

    def makeTreasure(self, withdrawType, value=0, maxCarry=20):
        treasure = DistributedSurfaceTreasureAI.__new__(DistributedSurfaceTreasureAI)
        treasure.withdrawType = withdrawType
        treasure.value = value
        treasure.belongToTeam = 0
        treasure.looters = []
        treasure.doId = 300
        treasure.air = SimpleNamespace(doId2do={7: object()})
        treasure.sendUpdate = Mock()
        treasure.sendUpdateToAvatarId = Mock()
        carried = {}

        def addLoot(avatarId, amount):
            amount = max(0, min(amount, maxCarry - carried.get(avatarId, 0)))
            carried[avatarId] = carried.get(avatarId, 0) + amount
            return amount

        treasure.gameRules = SimpleNamespace(getPlayers=lambda: {7: ['Jack', 2]},
            getLootCarried=lambda avatarId: carried.get(avatarId, 0),
            getMaxCarry=lambda: maxCarry, addLoot=addLoot)
        return treasure, carried

    def test_empty_treasure_denies_interaction(self):
        treasure, carried = self.makeTreasure(PiratesGlobals.WITHDRAW_LUMP_SUM)
        avatar = SimpleNamespace(doId=7, getTeam=lambda: 1)

        self.assertEqual(treasure.handleRequestInteraction(avatar, 0, 0), treasure.DENY)

        treasure.b_setValue(50)
        treasure.sendUpdate.assert_called_once_with('setValue', [50])
        self.assertEqual(treasure.handleRequestInteraction(avatar, 0, 0), treasure.ACCEPT)

        # pirates outside of the game cannot take the loot
        outsider = SimpleNamespace(doId=8, getTeam=lambda: 1)
        self.assertEqual(treasure.handleRequestInteraction(outsider, 0, 0), treasure.DENY)

    def test_lump_sum_withdraw_takes_what_can_be_carried(self):
        treasure, carried = self.makeTreasure(PiratesGlobals.WITHDRAW_LUMP_SUM, value=50)
        avatar = SimpleNamespace(doId=7, getTeam=lambda: 1)
        treasure.handlePostRequestInteraction(avatar)

        self.assertEqual(carried[7], 20)
        self.assertEqual(treasure.getValue(), 30)
        self.assertEqual(treasure.sendUpdateToAvatarId.call_args_list,
            [call(7, 'startLooting', [PiratesGlobals.WITHDRAW_LUMP_SUM]), call(7, 'stopLooting', [])])

        # a pirate who cannot carry any more is not offered the treasure
        self.assertEqual(treasure.handleRequestInteraction(avatar, 0, 0), treasure.DENY)

    def test_incremental_withdraw_steals_until_empty(self):
        treasure, carried = self.makeTreasure(PiratesGlobals.WITHDRAW_INCREMENTAL, value=2)
        tasks = Mock()
        treasure.uniqueName = lambda name: '%s-300' % name
        avatar = SimpleNamespace(doId=7, getTeam=lambda: 1)
        with patch.object(builtins, 'taskMgr', tasks, create=True):
            treasure.handlePostRequestInteraction(avatar)
            treasure.sendUpdateToAvatarId.assert_called_once_with(7, 'startLooting',
                [PiratesGlobals.WITHDRAW_INCREMENTAL])

            self.assertEqual(treasure.handleRequestInteraction(avatar, 0, 0), treasure.DENY)
            args, kwargs = tasks.doMethodLater.call_args
            self.assertEqual(args[2], 'loot-7-300')
            self.assertEqual(kwargs['extraArgs'], [7])
            callback = args[1]
            self.assertEqual(callback(7, SimpleNamespace()), Task.again)
            self.assertEqual(callback(7, SimpleNamespace()), Task.done)
            tasks.remove.assert_called_with('loot-7-300')

        self.assertEqual(carried[7], 2)
        self.assertEqual(treasure.getValue(), 0)
        treasure.sendUpdate.assert_any_call('setEmpty', [True])
        treasure.sendUpdateToAvatarId.assert_called_with(7, 'stopLooting', [])
        self.assertEqual(treasure.looters, [])

    def test_withdraw_none_denies_interaction(self):
        treasure, carried = self.makeTreasure(PiratesGlobals.WITHDRAW_NONE, value=50)
        avatar = SimpleNamespace(doId=7, getTeam=lambda: 1)
        self.assertEqual(treasure.handleRequestInteraction(avatar, 0, 0), treasure.DENY)


if __name__ == '__main__':
    unittest.main()
