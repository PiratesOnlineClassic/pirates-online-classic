import ast
import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from tests import REPO_ROOT


def load_enable_boat_boarding(namespace):
    source = (REPO_ROOT / 'pirates/tutorial/DistributedPiratesTutorial.py').read_text()
    tree = ast.parse(source)
    cls = next(node for node in tree.body
               if isinstance(node, ast.ClassDef) and node.name == 'DistributedPiratesTutorial')
    method = next(node for node in cls.body
                  if isinstance(node, ast.FunctionDef) and node.name == 'enableBoatBoarding')
    exec(compile(ast.Module(body=[method], type_ignores=[]), str(__file__), 'exec'), namespace)
    return namespace['enableBoatBoarding']


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


if __name__ == '__main__':
    unittest.main()
