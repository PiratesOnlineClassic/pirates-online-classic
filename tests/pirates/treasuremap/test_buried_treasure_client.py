import ast
import math
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import (
    Func, LerpColorScaleInterval, LerpHprInterval, LerpPosInterval, Parallel,
    Sequence, Wait)
from direct.showbase.MessengerGlobal import messenger
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import ClockObject, NodePath, Vec3, Vec4
from tests import REPO_ROOT


ROOT = REPO_ROOT


def load_methods(path, class_name, names, base, namespace):
    source = ast.parse(path.read_text())
    cls = next(node for node in source.body
               if isinstance(node, ast.ClassDef) and node.name == class_name)
    cls.body = [node for node in cls.body
                if isinstance(node, ast.FunctionDef) and node.name in names]
    cls.bases = [ast.Name(id='Base', ctx=ast.Load())]
    cls.decorator_list = []
    namespace['Base'] = base
    exec(compile(ast.fix_missing_locations(ast.Module(body=[cls], type_ignores=[])),
                 str(path), 'exec'), namespace)
    return namespace[class_name]


ClientMethods = load_methods(
    ROOT / 'pirates/treasuremap/DistributedBuriedTreasure.py',
    'DistributedBuriedTreasure', {'setCurrentDepth', 'showTreasure'}, NodePath,
    dict(Vec3=Vec3, Vec4=Vec4, Func=Func, LerpColorScaleInterval=LerpColorScaleInterval,
         LerpHprInterval=LerpHprInterval, LerpPosInterval=LerpPosInterval,
         Parallel=Parallel, Sequence=Sequence, Wait=Wait))


class ClientProbe(ClientMethods):
    UpdateDelay = 2.0

    def __init__(self):
        NodePath.__init__(self, 'treasure')
        self.chest = self.attachNewNode('chest')
        self.dirt = self.attachNewNode('dirt')
        self.chestLidHigh = self.chest.attachNewNode('high')
        self.chestLidMed = self.chest.attachNewNode('med')
        self.chestLidLow = self.chest.attachNewNode('low')
        self.showTreasureIval = None
        self.raiseTreasureIval = None
        self.startingDepth = 10
        self.currentDepth = 0
        self.state = 'Idle'

    def loadChest(self):
        pass


class BuriedTreasureClientTests(unittest.TestCase):
    def setUp(self):
        self.treasure = ClientProbe()
        self.addCleanup(self.cleanup_intervals)

    def cleanup_intervals(self):
        for name in ('showTreasureIval', 'raiseTreasureIval'):
            interval = getattr(self.treasure, name, None)
            if interval:
                interval.pause()

    def assert_reset(self):
        treasure = self.treasure
        self.assertAlmostEqual(treasure.getColorScale()[3], 1)
        self.assertFalse(treasure.hasTransparency())
        self.assertTrue(treasure.chest.isStashed())
        self.assertTrue(treasure.dirt.isStashed())
        for lid in (treasure.chestLidHigh, treasure.chestLidMed, treasure.chestLidLow):
            self.assertAlmostEqual(lid.getP(), 0)
        treasure.setCurrentDepth(9)
        self.assertFalse(treasure.chest.isStashed())
        self.assertFalse(treasure.dirt.isStashed())
        self.assertAlmostEqual(treasure.getColorScale()[3], 1)

    def test_completed_reveal_resets_for_next_dig(self):
        self.treasure.showTreasure(0)
        self.treasure.showTreasureIval.setT(4.5)
        self.assertAlmostEqual(self.treasure.getColorScale()[3], 0)
        self.assertAlmostEqual(self.treasure.chestLidHigh.getP(), -40)
        self.treasure.setCurrentDepth(10)
        self.assert_reset()

    def test_early_reset_stops_reveal_and_raise_intervals(self):
        self.treasure.setCurrentDepth(5)
        raise_interval = self.treasure.raiseTreasureIval
        self.treasure.showTreasure(0)
        reveal = self.treasure.showTreasureIval
        reveal.setT(0.5)
        self.assertTrue(reveal.isPlaying())
        self.treasure.setCurrentDepth(10)
        self.assertFalse(reveal.isPlaying())
        self.assertFalse(raise_interval.isPlaying())
        self.assert_reset()
        clock = ClockObject.getGlobalClock()
        original_mode = clock.getMode()
        self.addCleanup(clock.setMode, original_mode)
        clock.setMode(ClockObject.MNonRealTime)
        clock.setDt(1.0)
        for _ in range(6):
            taskMgr.step()
        self.assertAlmostEqual(self.treasure.getColorScale()[3], 1)
        self.assertAlmostEqual(self.treasure.chestLidHigh.getP(), 0)
        self.assertFalse(self.treasure.chest.isStashed())


ManagerMethods = load_methods(
    ROOT / 'pirates/interact/InteractionManager.py', 'InteractionManager',
    {'setCurrentInteractive', 'getCurrentInteractive', 'getInteractives',
     'addInteractive', 'removeInteractive'}, object,
    dict(InteractiveBase=SimpleNamespace(PROXIMITY=0), HierarchyException=Exception))
manager = ManagerMethods()


class AvatarProbe(NodePath):
    def __init__(self):
        NodePath.__init__(self, 'avatar')
        self.b_setGameState = Mock()
        self.getPos = Mock(return_value=(1, 1, 0))
        self.setPos = Mock()
        self.setH = Mock()
        self.headsUp = Mock()
        self.lootCarried = 0
        self.gameFSM = SimpleNamespace(state='Digging', defaultState='LandRoam')
        self.guiMgr = SimpleNamespace(
            workMeter=SimpleNamespace(updateText=Mock(), startTimer=Mock(), stopTimer=Mock()),
            showQuestProgress=Mock())


avatar = AvatarProbe()
InteractiveMethods = load_methods(
    ROOT / 'pirates/interact/InteractiveBase.py', 'InteractiveBase',
    {'enterUse', 'exitUse', 'enterProximity', 'exitProximity', 'enterIdle'}, FSM,
    dict(base=SimpleNamespace(cr=SimpleNamespace(interactionMgr=manager)),
         END_INTERACT_EVENT='escape', PROXIMITY=0, messenger=messenger))

DistributedInteractiveMethods = load_methods(
    ROOT / 'pirates/distributed/DistributedInteractive.py', 'DistributedInteractive',
    {'acceptInteraction', 'refreshState', 'requestExit'}, InteractiveMethods,
    dict(localAvatar=avatar))

BuriedInteractionMethods = load_methods(
    ROOT / 'pirates/treasuremap/DistributedBuriedTreasure.py', 'DistributedBuriedTreasure',
    {'startDigging', 'stopDigging', 'requestExit'}, DistributedInteractiveMethods,
    dict(localAvatar=avatar, PLocalizer=SimpleNamespace(InteractDigging='Digging'), math=math,
         DistributedInteractive=SimpleNamespace(DistributedInteractive=DistributedInteractiveMethods)))


class InteractionProbe(BuriedInteractionMethods):
    def __init__(self):
        FSM.__init__(self, 'buried-treasure-accept')
        self.parent = NodePath('root')
        avatar.reparentTo(self.parent)
        NodePath.setPos(avatar, 0, 0, 0)
        self.proximityCollisionNodePath = self.parent.attachNewNode('collision')
        self.hasProximityCollision = True
        self.ignoreProximity = False
        self.allowInteract = True
        self._InteractiveBase__endInteract = True
        self._InteractiveBase__mouseClick = False
        self._InteractiveBase__mouseOver = False
        self.proximityCollisionEnterEvent = None
        self.proximityCollisionExitEvent = 'exit-treasure-test'
        self.handleExitProximity = Mock(return_value=None)
        self.showUseInfo = Mock()
        self.hideUseInfo = Mock()
        self.hideProximityInfo = Mock()
        self.handleEndInteractKey = Mock(return_value=None)
        self.sendUpdate = Mock()
        self.showTreasureIval = Mock()
        self.startingDepth = self.currentDepth = 10
        self.doId = 100


class DuplicateAcceptTests(unittest.TestCase):
    def test_duplicate_accept_restores_use_state_and_single_exit_handler(self):
        interactive = InteractionProbe()
        self.addCleanup(interactive.ignoreAll)
        nearest = Mock()
        mouse_over = Mock()
        manager._InteractionManager__nearest = nearest
        manager._InteractionManager__mouseOver = mouse_over
        manager._InteractionManager__interactives = []
        avatar.b_setGameState.reset_mock()
        interactive.acceptInteraction()
        interactive.startDigging()
        self.assertEqual(interactive.state, 'Use')
        self.assertIs(manager.getCurrentInteractive(), interactive)
        self.assertTrue(interactive.proximityCollisionNodePath.isStashed())
        nearest.hideProximityInfo.assert_called_once_with()
        mouse_over.hideMouseOverInfo.assert_called_once_with()
        self.assertEqual(interactive.showUseInfo.call_count, 2)
        interactive.hideUseInfo.assert_called_once()
        avatar.b_setGameState.assert_called_once_with('Digging')
        messenger.send('escape')
        interactive.handleEndInteractKey.assert_called_once_with()


class StopDiggingTests(unittest.TestCase):
    def setUp(self):
        self.interactive = InteractionProbe()
        self.addCleanup(self.interactive.ignoreAll)
        manager._InteractionManager__nearest = None
        manager._InteractionManager__mouseOver = None
        manager._InteractionManager__interactives = []
        avatar.gameFSM.state = 'Digging'
        avatar.b_setGameState.reset_mock()
        avatar.guiMgr.workMeter.stopTimer.reset_mock()
        avatar.guiMgr.showQuestProgress.reset_mock()
        self.interactive.acceptInteraction()

    def test_completed_dig_releases_use_without_sending_exit(self):
        self.interactive.stopDigging(1)
        self.assertEqual(self.interactive.state, 'Proximity')
        self.assertIsNone(manager.getCurrentInteractive())
        self.assertFalse(self.interactive.proximityCollisionNodePath.isStashed())
        self.assertEqual(manager.getInteractives(), [(self.interactive, 0)])
        self.interactive.sendUpdate.assert_not_called()
        self.interactive.showTreasureIval.pause.assert_not_called()
        avatar.guiMgr.workMeter.stopTimer.assert_called_once_with()
        avatar.guiMgr.showQuestProgress.assert_called_once_with(1)
        avatar.b_setGameState.assert_called_once_with('LandRoam')

    def test_request_exit_does_not_refresh_a_second_time(self):
        self.interactive.refreshState = Mock(wraps=self.interactive.refreshState)
        self.interactive.requestExit()
        self.assertEqual(self.interactive.state, 'Proximity')
        self.assertIsNone(manager.getCurrentInteractive())
        self.assertFalse(self.interactive.proximityCollisionNodePath.isStashed())
        self.assertEqual(manager.getInteractives(), [(self.interactive, 0)])
        self.interactive.sendUpdate.assert_called_once_with('requestExit')
        self.interactive.refreshState.assert_called_once_with()
        avatar.guiMgr.workMeter.stopTimer.assert_called_once_with()
        avatar.guiMgr.showQuestProgress.assert_called_once_with(0)
        self.interactive.refreshState.reset_mock()
        self.interactive.stopDigging(0)
        self.interactive.refreshState.assert_not_called()
        self.interactive.sendUpdate.assert_called_once_with('requestExit')
        self.assertEqual(manager.getInteractives(), [(self.interactive, 0)])

    def test_completed_dig_outside_proximity_returns_idle(self):
        NodePath.setPos(avatar, 100, 0, 0)
        avatar.gameFSM.state = 'Combat'
        self.interactive.stopDigging(0)
        self.assertEqual(self.interactive.state, 'Idle')
        self.assertIsNone(manager.getCurrentInteractive())
        self.assertFalse(self.interactive.proximityCollisionNodePath.isStashed())
        self.assertEqual(manager.getInteractives(), [])
        self.interactive.sendUpdate.assert_not_called()
        avatar.b_setGameState.assert_not_called()


if __name__ == '__main__':
    unittest.main()
