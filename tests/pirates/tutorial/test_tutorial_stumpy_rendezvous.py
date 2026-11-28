import ast
from types import SimpleNamespace
import unittest
from unittest.mock import Mock
from tests import REPO_ROOT


def load_intro_methods(base):
    source = (REPO_ROOT / 'pirates/tutorial/DistributedPiratesTutorial.py').read_text()
    tree = ast.parse(source)
    cls = next(node for node in tree.body
               if isinstance(node, ast.ClassDef) and node.name == 'DistributedPiratesTutorial')
    methods = [node for node in cls.body if isinstance(node, ast.FunctionDef)
               and node.name in ('_stumpyHere', '_requestStumpyIntro', 'doStumpyBoatIntro')]
    namespace = {'base': base}
    exec(compile(ast.Module(body=methods, type_ignores=[]), str(__file__), 'exec'), namespace)
    return type('IntroMethods', (), {node.name: namespace[node.name] for node in methods})


class StumpyRendezvousTests(unittest.TestCase):
    def setUp(self):
        self.related = SimpleNamespace(requestObjects=Mock())
        boat = SimpleNamespace(proximityCollisionEnterEvent='near-boat', hideName=Mock())
        base = SimpleNamespace(cr=SimpleNamespace(
            doId2do={42: boat}, relatedObjectMgr=self.related))
        intro = load_intro_methods(base)()
        intro.StumpyDoId = None
        intro.BoatStumpyDoId = 42
        intro._waitingForStumpyIntro = False
        intro.notify = SimpleNamespace(debug=Mock())
        intro.accept = Mock()
        intro.acceptOnce = Mock()
        intro.triggerBoBeckCut = Mock()
        intro.enableBoatBoarding = Mock()
        intro.doStumpyIntro = Mock()
        intro.playerNeedsToTalkToDan = lambda callback: callback(False)
        self.intro = intro

    def test_boat_before_npc_waits_for_uid(self):
        self.intro.doStumpyBoatIntro(None)
        self.related.requestObjects.assert_not_called()
        self.intro._stumpyHere(99)
        self.related.requestObjects.assert_called_once_with(
            [99], eachCallback=self.intro.doStumpyIntro)

    def test_npc_before_boat_is_requested_when_boat_arrives(self):
        self.intro._stumpyHere(99)
        self.related.requestObjects.assert_not_called()
        self.intro.doStumpyBoatIntro(None)
        self.related.requestObjects.assert_called_once_with(
            [99], eachCallback=self.intro.doStumpyIntro)


if __name__ == '__main__':
    unittest.main()
