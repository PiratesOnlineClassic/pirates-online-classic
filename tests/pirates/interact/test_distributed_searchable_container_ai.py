import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from pirates.interact.DistributedSearchableContainerAI import DistributedSearchableContainerAI


class FakeTaskMgr:

    def __init__(self):
        self.tasks = {}

    def doMethodLater(self, delay, method, name, extraArgs=[]):
        self.tasks[name] = (method, extraArgs)

    def remove(self, name):
        self.tasks.pop(name, None)

    def removeTasksMatching(self, pattern):
        self.tasks.clear()

    def run(self, name):
        method, extraArgs = self.tasks.pop(name)
        method(*extraArgs)


class DistributedSearchableContainerAITests(unittest.TestCase):

    def setUp(self):
        self.taskMgr = FakeTaskMgr()
        self.taskPatch = patch.object(builtins, 'taskMgr', self.taskMgr, create=True)
        self.taskPatch.start()
        self.avatar = SimpleNamespace(doId=42)
        self.questMgr = SimpleNamespace(canSearchContainer=Mock(return_value=True),
                                        containerSearched=Mock(return_value=True))
        self.container = DistributedSearchableContainerAI.__new__(DistributedSearchableContainerAI)
        self.container.doId = 300
        self.container.searchTime = 2.0
        self.container.air = SimpleNamespace(questMgr=self.questMgr, doId2do={42: self.avatar})
        self.container.sendUpdateToAvatarId = Mock()
        self.container.b_setUserId = Mock()
        self.container.uniqueName = lambda name: '%s-%d' % (name, self.container.doId)

    def tearDown(self):
        self.taskPatch.stop()

    def test_containers_without_a_quest_cannot_be_searched(self):
        self.questMgr.canSearchContainer.return_value = False
        self.assertEqual(self.container.handleRequestInteraction(self.avatar, 0, False),
                         self.container.DENY)
        self.container.sendUpdateToAvatarId.assert_not_called()

    def test_search_reports_quest_progress_once_finished(self):
        self.assertEqual(self.container.handleRequestInteraction(self.avatar, 0, False),
                         self.container.ACCEPT)
        self.container.sendUpdateToAvatarId.assert_called_once_with(42, 'startSearching', [])
        self.questMgr.containerSearched.assert_not_called()
        self.taskMgr.run('avatarSearchTask-42-300')
        self.questMgr.containerSearched.assert_called_once_with(self.avatar, self.container)
        self.container.sendUpdateToAvatarId.assert_any_call(42, 'setUserId', [0])
        self.container.sendUpdateToAvatarId.assert_called_with(42, 'stopSearching', [1])

        # every avatar searches on it's own, the user is never broadcast
        self.assertTrue(self.container.MULTIUSE)
        self.container.b_setUserId.assert_not_called()

    def test_searching_again_restarts_the_search(self):
        self.container.handleRequestInteraction(self.avatar, 0, False)
        self.container.handleRequestInteraction(self.avatar, 0, False)
        self.assertEqual(list(self.taskMgr.tasks), ['avatarSearchTask-42-300'])

    def test_leaving_cancels_the_search(self):
        self.container.handleRequestInteraction(self.avatar, 0, False)
        self.assertEqual(self.container.handleRequestExit(self.avatar), self.container.ACCEPT)
        self.assertEqual(self.taskMgr.tasks, {})
        self.questMgr.containerSearched.assert_not_called()


if __name__ == '__main__':
    unittest.main()
