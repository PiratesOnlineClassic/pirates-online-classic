import ast
from types import SimpleNamespace
import unittest
from tests import REPO_ROOT


ROOT = REPO_ROOT / 'pirates/world'


class GeneratedObject:
    def __init__(self, air):
        self.uniqueId = ''
        self.doId = air.nextId
        air.nextId += 1

    def setUniqueId(self, uid):
        self.uniqueId = uid

    def getUniqueId(self):
        return self.uniqueId

    def setPos(self, pos):
        self.pos = pos

    def getPos(self):
        return self.pos

    def setHpr(self, hpr):
        self.hpr = hpr

    def setScale(self, scale):
        self.scale = scale

    def setInteractRadius(self, radius):
        self.radius = radius

    def setStartingDepth(self, depth):
        self.depth = depth

    def getStartingDepth(self):
        return self.depth

    def setCurrentDepth(self, depth):
        self.currentDepth = depth


class SurfaceTreasure(GeneratedObject):
    pass


class BuriedTreasure(GeneratedObject):
    pass


class Dinghy(GeneratedObject):
    pass


def builder_methods():
    methods = []
    for filename, names in (
        ('ClientAreaBuilderAI.py', {'addObject'}),
        ('IslandAreaBuilderAI.py', {'createDinghy'}),
        ('GameAreaBuilderAI.py', {'createObjectSpawnNode'}),
    ):
        tree = ast.parse((ROOT / filename).read_text())
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef))
        methods.extend(node for node in cls.body
                       if isinstance(node, ast.FunctionDef) and node.name in names)
    namespace = {
        'DistributedDinghyAI': Dinghy,
        'DistributedSurfaceTreasureAI': SurfaceTreasure,
        'DistributedBuriedTreasureAI': BuriedTreasure,
    }
    exec(compile(ast.Module(body=methods, type_ignores=[]), str(ROOT), 'exec'), namespace)
    return type('Builder', (), {node.name: namespace[node.name] for node in methods})


class WorldObjectGenerationTests(unittest.TestCase):
    def setUp(self):
        self.uidMap = {}
        self.generated = []
        self.air = SimpleNamespace(
            nextId=100,
            uidMgr=SimpleNamespace(addUid=self.addUid))
        self.parent = SimpleNamespace(
            getZoneFromXYZ=lambda pos: 20,
            generateChildWithRequired=self.generate)
        self.builder = builder_methods()()
        self.builder.air = self.air
        self.builder.parent = self.parent
        self.builder.objectList = {}
        self.builder.parentObjectToCell = lambda *args: None

    def addUid(self, uid, doId):
        if uid:
            self.uidMap[uid] = doId

    def generate(self, obj, zone):
        self.generated.append((obj.getUniqueId(), zone))

    def test_dinghy_uid_is_set_before_generation(self):
        obj = self.builder.createDinghy(
            self.parent, 'island', 'dinghy-uid', {'Pos': (1, 2, 3)})
        self.assertEqual(self.generated, [('dinghy-uid', 20)])
        self.assertEqual(self.uidMap, {'dinghy-uid': obj.doId})

    def test_treasure_uids_are_set_before_generation(self):
        for spawnable, cls in (
            ('Surface Treasure', SurfaceTreasure),
            ('Buried Treasure', BuriedTreasure),
        ):
            with self.subTest(spawnable=spawnable):
                uid = spawnable.replace(' ', '-')
                obj = self.builder.createObjectSpawnNode(
                    self.parent, 'area', uid, {'Spawnables': spawnable})
                self.assertIsInstance(obj, cls)
                self.assertEqual(self.generated[-1], (uid, 20))
                self.assertEqual(self.uidMap[uid], obj.doId)


if __name__ == '__main__':
    unittest.main()
