import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

class _StandInModule(types.ModuleType):
    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError(name)
        return Mock(name='%s.%s' % (self.__name__, name))


try:
    from pirates.battle import WeaponGlobals
except (OSError, IOError):
    # the game resources (WeaponGlobals.pkl) aren't available; the container
    # tasks don't use the weapon or enemy globals so stand-ins are enough.
    for _name in ('pirates.battle.WeaponGlobals', 'pirates.battle.EnemyGlobals'):
        sys.modules[_name] = _StandInModule(_name)

from pirates.interact import DistributedSearchableContainerAI as container_ai_module
from pirates.minigame.minigame_test_util import FakeTaskMgr, FakeAvatar, makeAir
from pirates.quest import QuestTaskDNA
from pirates.quest.QuestConstants import LocationIds


class FakeQuest:
    def __init__(self, tasks, requiresVisit=True):
        self.tasks = tasks
        self.taskStates = [task.getInitialTaskState(None) for task in tasks]
        self.requiresVisit = requiresVisit
        self.questDNA = SimpleNamespace(getTasks=lambda: self.tasks, getFinalizeInfo=lambda: None)

    def getQuestDNA(self):
        return self.questDNA

    def getTaskStates(self):
        return self.taskStates

    def handleEvent(self, holder, questEvent):
        # mirrors DistributedQuestAI.handleEvent
        for taskState, taskDNA in zip(self.taskStates, self.tasks):
            if taskDNA.locationMatches(questEvent) and questEvent.applyTo(taskState, taskDNA):
                questEvent.complete(taskState, taskDNA)

    def isComplete(self):
        return all(state.isComplete() for state in self.taskStates)

    def completeRequiresVisit(self):
        return self.requiresVisit


class SearchableContainerTests(unittest.TestCase):
    def setUp(self):
        self.fakeTaskMgr = FakeTaskMgr()
        self.patcher = patch.object(container_ai_module, 'taskMgr', self.fakeTaskMgr)
        self.patcher.start()
        self.air, self.avatars = makeAir({101: None}, [101])
        self.avatar = self.avatars[101]
        self.avatar.getParentObj = lambda: SimpleNamespace(getUniqueId=lambda: 'island-1')
        self.quests = []
        self.air.questMgr.getQuestsFromTaskDNAType = lambda avatar, cls: self.quests

        self.container = container_ai_module.DistributedSearchableContainerAI(self.air)
        self.container.doId = 6000
        self.container.setUniqueId('crate-1')
        self.container.setSearchTime(6.0)
        self.container.sendUpdate = Mock()
        self.container.sendUpdateToAvatarId = Mock()
        self.container.acceptOnce = Mock()
        self.container.ignore = Mock()

    def tearDown(self):
        self.patcher.stop()

    def makeTask(self, **kwargs):
        params = {'location': LocationIds.ANY_LOCATION, 'item': 1, 'num': 1,
                  'maxAttempts': 1, 'probability': 0.0}
        params.update(kwargs)
        return QuestTaskDNA.RecoverContainerItemTaskDNA(**params)

    def search(self):
        result = self.container.handleRequestInteraction(self.avatar, 0, False)
        if result:
            self.container.handlePostRequestInteraction(self.avatar)
        return result

    def test_no_quest_is_denied(self):
        self.assertEqual(self.search(), self.container.DENY)

    def test_finds_item_after_search_time(self):
        quest = FakeQuest([self.makeTask()])
        self.quests.append(quest)
        self.assertEqual(self.search(), self.container.ACCEPT)
        self.container.sendUpdateToAvatarId.assert_called_with(101, 'startSearching', [])
        # no progress until the search finishes
        self.assertEqual(quest.getTaskStates()[0].getProgress(), 0)

        self.fakeTaskMgr.run()
        self.assertTrue(quest.isComplete())
        self.container.sendUpdateToAvatarId.assert_any_call(101, 'stopSearching', [1])
        # quest requires a visit to the npc, so it is not completed here
        self.air.questMgr.completeQuest.assert_not_called()

    def test_nothing_found_and_container_not_searchable_again(self):
        quest = FakeQuest([self.makeTask(maxAttempts=4, probability=-1.0)])
        self.quests.append(quest)
        self.assertEqual(self.search(), self.container.ACCEPT)
        self.fakeTaskMgr.run()
        self.container.sendUpdateToAvatarId.assert_any_call(101, 'stopSearching', [0])
        self.assertEqual(self.search(), self.container.DENY)

    def test_exit_cancels_search(self):
        quest = FakeQuest([self.makeTask()])
        self.quests.append(quest)
        self.search()
        self.assertEqual(self.container.handleRequestExit(self.avatar), self.container.ACCEPT)
        self.assertFalse(self.fakeTaskMgr.tasks)
        self.assertEqual(quest.getTaskStates()[0].getProgress(), 0)

    def test_completes_quest_without_visit(self):
        quest = FakeQuest([self.makeTask()], requiresVisit=False)
        self.quests.append(quest)
        self.search()
        self.fakeTaskMgr.run()
        self.air.questMgr.completeQuest.assert_called_with(self.avatar, quest)

    def test_wrong_container_is_denied(self):
        self.quests.append(FakeQuest([self.makeTask(containerId='some-other-crate')]))
        self.assertEqual(self.search(), self.container.DENY)


if __name__ == '__main__':
    unittest.main()
