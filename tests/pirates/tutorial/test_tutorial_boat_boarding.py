import ast
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from tests import REPO_ROOT


def load_tutorial_methods(namespace, *names):
    source = (REPO_ROOT / 'pirates/tutorial/DistributedPiratesTutorial.py').read_text()
    tree = ast.parse(source)
    cls = next(node for node in tree.body
               if isinstance(node, ast.ClassDef) and node.name == 'DistributedPiratesTutorial')
    methods = [node for node in cls.body
               if isinstance(node, ast.FunctionDef) and node.name in names]
    exec(compile(ast.Module(body=methods, type_ignores=[]), str(__file__), 'exec'), namespace)
    return [namespace[name] for name in names]


def load_enable_boat_boarding(namespace):
    return load_tutorial_methods(namespace, 'enableBoatBoarding')[0]


class TutorialBoatBoardingTests(unittest.TestCase):

    def test_tutorial_cannon_is_offered_whichever_cannon_generated_first(self):
        tutorialCannon = Mock(name='DistributedTutorialShipCannon')
        plainCannon = Mock(name='DistributedShipCannon')
        boat = SimpleNamespace(cannons={})
        # the plain cannon (index 1) reached the client first...
        boat.cannons[1] = ['prop', plainCannon]
        boat.cannons[0] = ['prop', tutorialCannon]

        dialogue = SimpleNamespace(length=lambda: 1.0)
        localAvatar = SimpleNamespace(
            placeOnShip=Mock(), setH=Mock(),
            guiMgr=SimpleNamespace(subtitler=SimpleNamespace(showText=Mock())))
        namespace = {
            'base': SimpleNamespace(cr=SimpleNamespace(doId2do={7: boat}),
                                    loader=SimpleNamespace(loadSfx=lambda name: dialogue)),
            'localAvatar': localAvatar,
            'PLocalizer': SimpleNamespace(QuestScriptTutorialStumpy_1='Shoot!'),
        }
        enableBoatBoarding = load_enable_boat_boarding(namespace)
        tutorial = SimpleNamespace(
            notify=SimpleNamespace(debug=Mock()), BoatStumpyDoId=7,
            island=SimpleNamespace(stopCustomEffects=Mock()),
            stageStumpyPositionOnBoat=Mock(), acceptOnce=Mock(), startShipMovement=Mock())

        enableBoatBoarding(tutorial)

        localAvatar.placeOnShip.assert_called_once_with(boat)
        tutorialCannon.setIgnoreProximity.assert_called_once_with(False)
        plainCannon.setIgnoreProximity.assert_not_called()
        tutorial.acceptOnce.assert_called_once_with('usedCannon', tutorial.startShipMovement)


class TutorialUndeadShipTests(unittest.TestCase):

    def setUp(self):
        dialogue = SimpleNamespace(length=lambda: 1.0)
        self.localAvatar = SimpleNamespace(
            gameFSM=SimpleNamespace(lockFSM=True),
            cannon=SimpleNamespace(fireCannonPanel=SimpleNamespace(setWreckButtonText=Mock())),
            guiMgr=SimpleNamespace(subtitler=SimpleNamespace(showText=Mock())))
        namespace = {
            'base': SimpleNamespace(loader=SimpleNamespace(loadSfx=lambda name: dialogue)),
            'localAvatar': self.localAvatar,
            'PLocalizer': SimpleNamespace(QuestScriptTutorialStumpy_6='Praise',
                                          QuestScriptTutorialStumpy_8='Look sharp!'),
            'print': lambda *args: None,
        }
        methods = load_tutorial_methods(namespace, 'setupUndeadShip', 'undeadShipSunk', 'cannonHitWreck')
        self.tutorial = SimpleNamespace(
            notify=SimpleNamespace(debug=Mock()), acceptOnce=Mock(), cannonDoneShooting=Mock(),
            showCannonExitPanel=Mock(), shipWreckHitCount=0, shipWreckState=0,
            pendingUndeadShipRequest='pending')
        self.setupUndeadShip, self.undeadShipSunk, self.cannonHitWreck = [
            (lambda method: lambda *args: method(self.tutorial, *args))(method) for method in methods]
        self.tutorial.undeadShipSunk = self.undeadShipSunk

    def test_wreck_is_only_practice(self):
        for _ in range(10):
            self.cannonHitWreck(None)

        self.tutorial.cannonDoneShooting.assert_not_called()
        self.tutorial.showCannonExitPanel.assert_not_called()
        self.assertTrue(self.localAvatar.gameFSM.lockFSM)
        # Beck still praises the third hit...
        self.localAvatar.guiMgr.subtitler.showText.assert_called_once()

    def test_sinking_the_undead_ship_ends_target_practice(self):
        undeadShip = SimpleNamespace(hideName=Mock(), uniqueName=lambda name: name + '-77')

        self.setupUndeadShip(undeadShip)

        self.assertIsNone(self.tutorial.pendingUndeadShipRequest)
        self.tutorial.acceptOnce.assert_called_once_with('shipSinking-77', self.undeadShipSunk)
        self.tutorial.cannonDoneShooting.assert_not_called()

        self.undeadShipSunk()

        self.assertFalse(self.localAvatar.gameFSM.lockFSM)
        self.tutorial.cannonDoneShooting.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
