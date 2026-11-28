import ast
import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from panda3d.core import loadPrcFile, loadPrcFileData
from tests import REPO_ROOT

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

from pirates.treasuremap.DistributedTreasureMapInstanceAI import (
    DistributedTreasureMapInstanceAI,
)


class TreasureMapCompletionTests(unittest.TestCase):
    def make_instance(self, participants=(42,)):
        instance = DistributedTreasureMapInstanceAI.__new__(
            DistributedTreasureMapInstanceAI)
        instance.doId = 100
        instance.participants = list(participants)
        instance.readyAvatars = []
        instance.sendUpdateToAvatarId = Mock()
        instance.air = SimpleNamespace(
            doId2do={avatarId: SimpleNamespace(doId=avatarId, getHp=lambda: [100, 0])
                     for avatarId in participants},
            teleportMgr=SimpleNamespace(),
            getAvatarIdFromSender=lambda: 42,
        )
        island = SimpleNamespace(zoneId=310)
        main_world = SimpleNamespace(
            doId=200,
            builder=SimpleNamespace(getIslands=lambda: [island]),
        )
        instance.air.teleportMgr.getWorld = Mock(return_value=main_world)
        return instance

    def test_leave_approves_return_before_removing_participant(self):
        instance = self.make_instance()
        instance.requestLeave(0)
        instance.sendUpdateToAvatarId.assert_called_once_with(
            42, 'requestLeaveApproved', [200, 310, 0])
        self.assertEqual(instance.participants, [])

    def test_leave_without_main_world_preserves_participant_for_retry(self):
        instance = self.make_instance()
        instance.air.teleportMgr.getWorld.return_value = None
        instance.requestLeave(0)
        instance.sendUpdateToAvatarId.assert_not_called()
        self.assertEqual(instance.participants, [42])

    def test_leave_without_return_island_preserves_participant(self):
        instance = self.make_instance()
        main_world = instance.air.teleportMgr.getWorld.return_value
        main_world.builder.getIslands = lambda: []
        instance.requestLeave(0)
        instance.sendUpdateToAvatarId.assert_not_called()
        self.assertEqual(instance.participants, [42])

    def test_nonparticipant_cannot_request_return(self):
        instance = self.make_instance(participants=(7,))
        instance.requestLeave(0)
        instance.sendUpdateToAvatarId.assert_not_called()
        self.assertEqual(instance.participants, [7])

    def test_completed_state_returns_all_remaining_participants(self):
        instance = self.make_instance(participants=(42, 43))
        instance.air.doId2do[43] = SimpleNamespace(doId=43)
        instance.enterCompleted()
        self.assertEqual(instance.sendUpdateToAvatarId.call_args_list, [
            unittest.mock.call(42, 'requestLeaveApproved', [200, 310, 0]),
            unittest.mock.call(43, 'requestLeaveApproved', [200, 310, 0]),
        ])
        self.assertEqual(instance.participants, [])

    def test_completed_state_cleans_disconnected_participants(self):
        instance = self.make_instance(participants=(42, 43))
        del instance.air.doId2do[43]
        instance.enterCompleted()
        self.assertEqual(instance.sendUpdateToAvatarId.call_args_list, [
            unittest.mock.call(42, 'requestLeaveApproved', [200, 310, 0]),
        ])
        self.assertEqual(instance.participants, [])

    def test_completion_panel_is_shown_and_rebuilt_with_current_results(self):
        manager = SimpleNamespace(
            showTMCompleteLerp=Mock(),
            tmCompleteUI=Mock(),
        )
        old_lerp = manager.showTMCompleteLerp
        old_panel = manager.tmCompleteUI
        interval = Mock()
        interval_factory = Mock(return_value=interval)
        new_panel = Mock()
        create_panel = Mock(side_effect=lambda tm, results: setattr(
            manager, 'tmCompleteUI', new_panel))
        manager.createTMCompleteUI = create_panel

        source = REPO_ROOT / 'pirates/piratesgui/GuiManager.py'
        module = ast.parse(source.read_text())
        gui_manager = next(node for node in module.body
                           if isinstance(node, ast.ClassDef) and node.name == 'GuiManager')
        show_method = next(node for node in gui_manager.body
                           if isinstance(node, ast.FunctionDef) and
                           node.name == 'showTMCompleteUI')
        isolated = ast.Module(body=[show_method], type_ignores=[])
        namespace = {
            'LerpColorScaleInterval': interval_factory,
            'Vec4': lambda *values: values,
        }
        exec(compile(isolated, str(source), 'exec'), namespace)

        results = [['reward', '1']]
        namespace['showTMCompleteUI'](manager, 'blackPearl', results)

        old_lerp.pause.assert_called_once_with()
        old_panel.destroy.assert_called_once_with()
        create_panel.assert_called_once_with('blackPearl', results)
        new_panel.setAlphaScale.assert_called_once_with(0)
        new_panel.show.assert_called_once_with()
        interval_factory.assert_called_once_with(new_panel, 1, (1, 1, 1, 1))
        interval.start.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
