import builtins
import unittest

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

from pirates.quest.QuestPath import QuestGoal, QuestStep


class QuestStepComparisonTests(unittest.TestCase):
    # Python 3 ignores __cmp__ (and has no cmp()), so these used to compare by
    # identity and a step received over the network never matched NullStep.

    def test_steps_compare_by_value(self):
        self.assertEqual(QuestStep(1, 2, 3, (1, 2, 3, 4), 'island'), QuestStep(1, 2, 3, (1, 2, 3, 4), 'island'))
        self.assertNotEqual(QuestStep(1, 2, 3), QuestStep(1, 5, 3))
        self.assertFalse(QuestStep(1, 2, 3) != QuestStep(1, 2, 3))

    def test_network_null_step_matches_null_step(self):
        # dc arrays arrive as lists, the null step is built with a tuple.
        self.assertEqual(QuestStep(0, 0, 0, [0, 0, 0, 0], ''), QuestStep.getNullStep())

    def test_step_is_not_equal_to_other_types(self):
        self.assertNotEqual(QuestStep(0, 0, 0), None)
        self.assertNotEqual(QuestStep(0, 0, 0), 0)

    def test_steps_are_hashable(self):
        self.assertEqual(len({QuestStep(1, 2, 3), QuestStep(1, 2, 3, [0, 0, 0, 0])}), 1)


class QuestGoalComparisonTests(unittest.TestCase):

    def test_uid_goal_string_is_the_uid(self):
        self.assertEqual(str(QuestGoal('1234567890.00abc')), '1234567890.00abc')

    def test_goals_compare_and_hash_by_value(self):
        self.assertEqual(QuestGoal('uid-1'), QuestGoal('uid-1'))
        self.assertNotEqual(QuestGoal('uid-1'), QuestGoal('uid-2'))
        self.assertIn(QuestGoal('uid-1'), {QuestGoal('uid-1')})
        self.assertTrue(QuestGoal('a') < QuestGoal('b'))


if __name__ == '__main__':
    unittest.main()
