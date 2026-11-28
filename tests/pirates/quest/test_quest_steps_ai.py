import types
import unittest

from panda3d.core import NodePath

from tests.pirates.quest.test_quest_manager_ai_progression import manager_module
from tests.pirates.quest import test_quest_manager_ai_tasks as tasks_module
from pirates.pirate import AvatarTypes
from pirates.quest import QuestTaskDNA
from pirates.quest.QuestConstants import LocationIds
from pirates.quest.QuestPath import QuestStep
from pirates.quest.QuestTaskState import QuestTaskState


def worldClass(*classes):
    # the world classes are stubbed by the manager's loader, the fakes are
    # real node paths so the quest step positions come from a scene graph...
    return type('Fake' + classes[0].__name__, classes + (NodePath,), {})


Island = worldClass(manager_module.DistributedIslandAI, manager_module.DistributedGameAreaAI)
Interior = worldClass(manager_module.DistributedGAInteriorAI, manager_module.DistributedGameAreaAI)
BuildingDoor = worldClass(manager_module.DistributedBuildingDoorAI)
InteriorDoor = worldClass(manager_module.DistributedInteriorDoorAI)
Tunnel = worldClass(manager_module.DistributedGATunnelAI)
Townfolk = worldClass(manager_module.DistributedNPCTownfolkAI)
Enemy = worldClass(manager_module.DistributedBattleAvatarAI)
Ship = worldClass(manager_module.DistributedShipAI)
Container = worldClass(manager_module.DistributedSearchableContainerAI)
OceanGrid = type('FakeOceanGrid', (NodePath,), {})


class FakeStepQuest:

    def __init__(self, *tasks):
        self.tasks = list(tasks)
        self.taskStates = [QuestTaskState(goal=1) for task in tasks]
        self.dna = types.SimpleNamespace(getTasks=lambda: self.tasks, getReturnGiverIds=lambda: None)

    def getQuestDNA(self):
        return self.dna

    def getTasks(self):
        return self.tasks

    def getTaskStates(self):
        return self.taskStates

    def isComplete(self):
        return all(taskState.isComplete() for taskState in self.taskStates)


class QuestStepTests(unittest.TestCase):
    """
    The quest step leads the client's ray of light (QuestStepIndicator) from
    the area the avatar is in towards the goal of it's tracked quest
    """

    tearDown = tasks_module.QuestTaskTests.tearDown

    def setUp(self):
        tasks_module.QuestTaskTests.setUp(self)
        self.air = self.harness.air
        self.uids = {}
        self.air.uidMgr = types.SimpleNamespace(justGetMeMeObject=self.uids.get)
        self.air.worldCreator = types.SimpleNamespace(fileDicts={})
        self.world = NodePath('world')
        self.nextDoId = 1000

    def make(self, cls, parent, uid='', pos=(0, 0, 0), h=0, node=None, **fields):
        obj = cls.__new__(cls)
        NodePath.__init__(obj, cls.__name__)
        obj.doId = self.nextDoId
        self.nextDoId += 1
        obj.parentId = parent.doId if parent is not None else 0
        obj.zoneId = 0
        obj.getParentObj = lambda: parent
        obj.getUniqueId = lambda: uid
        obj.reparentTo(node or parent or self.world)
        obj.setPos(*pos)
        obj.setH(h)
        for name, value in fields.items():
            setattr(obj, name, value)

        self.air.doId2do[obj.doId] = obj
        if uid:
            self.uids[uid] = obj

        return obj

    def placeAvatar(self, area, pos=(0, 0, 0)):
        self.avatar.parentId = area.doId
        self.avatar.getParentObj = lambda: area
        self.avatar.isEmpty = lambda: True
        self.avatar.getPos = lambda: pos

    def makeInterior(self, island, uid, doorPos, backDoorPos=None):
        interior = self.make(Interior, None, uid=uid)
        doors = []
        for pos in filter(None, (doorPos, backDoorPos)):
            outside = self.make(BuildingDoor, island, pos=pos, interiorDoId=interior.doId)
            inside = self.make(InteriorDoor, interior, pos=(5, 0, 0), otherDoor=outside)
            outside.otherDoor = inside
            doors.append((outside, inside))

        return interior, doors

    def visit(self, npcId):
        return FakeStepQuest(QuestTaskDNA.VisitTaskDNA(npcId=npcId))

    def step(self, quest):
        return self.manager.getQuestStep(self.avatar, quest)

    def test_null_step_is_the_clients_null_step(self):
        island = self.make(Island, None, uid='island')
        self.placeAvatar(island)
        step = self.step(self.visit('nobody'))
        self.assertEqual(QuestStep(*step), QuestStep.getNullStep())

    def test_npc_on_the_same_island_is_placed_relative_to_the_island(self):
        island = self.make(Island, None, uid='island')
        cell = island.attachNewNode('cellOrigin-600')
        cell.setPos(-450, -1950, 0)
        npc = self.make(Townfolk, island, uid='npc', pos=(36, 44, 2), h=90, node=cell)
        self.placeAvatar(island)
        self.assertEqual(self.step(self.visit('npc')),
                         [island.doId, npc.doId, QuestStep.STNPC, [-414, -1906, 2, 90], 'island'])

    def test_npc_in_a_building_leads_to_the_closest_door_and_back_out(self):
        island = self.make(Island, None, uid='island')
        tavern, doors = self.makeInterior(island, 'tavern', (100, 0, 0), (-10, 0, 0))
        npc = self.make(Townfolk, tavern, uid='npc', pos=(3, 4, 0))
        self.placeAvatar(island)
        step = self.step(self.visit('npc'))
        self.assertEqual(step[:3], [island.doId, doors[1][0].doId, QuestStep.STExteriorDoor])
        self.assertEqual(step[3], [-10, 0, 0, 0])
        self.assertEqual(step[4], 'island')

        self.placeAvatar(tavern)
        self.assertEqual(self.step(self.visit('npc'))[:3], [tavern.doId, npc.doId, QuestStep.STNPC])

        outsider = self.make(Townfolk, island, uid='outsider')
        step = self.step(self.visit('outsider'))
        self.assertEqual(step[:3], [tavern.doId, doors[0][1].doId, QuestStep.STInteriorDoor])

    def test_npc_in_a_cave_leads_through_the_tunnel(self):
        island = self.make(Island, None, uid='island')
        cave = self.make(Interior, None, uid='cave')
        links = [False, 'cave', [['portal_connector_1', island.doId, 'island'],
                                 ['portal_connector_2', cave.doId, 'cave']]]
        tunnel = self.make(Tunnel, island, getLinks=lambda: links)
        caveTunnel = self.make(Tunnel, cave, getLinks=lambda: links)
        npc = self.make(Townfolk, cave, uid='npc')
        self.placeAvatar(island)
        step = self.step(self.visit('npc'))
        self.assertEqual(step[:3], [island.doId, tunnel.doId, QuestStep.STTunnel])
        self.assertEqual(step[4], 'island')

        self.placeAvatar(cave)
        self.assertEqual(self.step(self.visit('npc'))[:3], [cave.doId, npc.doId, QuestStep.STNPC])
        self.make(Townfolk, island, uid='outsider')
        self.assertEqual(self.step(self.visit('outsider'))[:3], [cave.doId, caveTunnel.doId, QuestStep.STTunnel])

    def test_npc_on_another_island_points_at_the_island(self):
        island = self.make(Island, None, uid='island')
        tortuga = self.make(Island, None, uid='tortuga')
        tavern, doors = self.makeInterior(tortuga, 'tavern', (1, 0, 0))
        self.make(Townfolk, tavern, uid='npc')
        self.placeAvatar(island)
        self.assertEqual(self.step(self.visit('npc')),
                         [island.doId, tortuga.doId, QuestStep.STArea, [0, 0, 0, 0], 'tortuga'])

        # from inside of a building the avatar is lead outside first...
        shop, shopDoors = self.makeInterior(island, 'shop', (2, 0, 0))
        self.placeAvatar(shop)
        step = self.step(self.visit('npc'))
        self.assertEqual(step[:3], [shop.doId, shopDoors[0][1].doId, QuestStep.STInteriorDoor])
        self.assertEqual(step[4], 'tortuga')

        # and from the deck of a ship the island is pointed at...
        ship = self.make(Ship, None)
        self.placeAvatar(ship)
        self.assertEqual(self.step(self.visit('npc'))[:3], [ship.doId, tortuga.doId, QuestStep.STArea])

    def test_quest_nodes_are_placed_from_the_world_data(self):
        island = self.make(Island, None, uid='island')
        fileData = {'ObjectIds': {'node': '["Objects"]["island"]["Objects"]["node"]'},
                    'Objects': {'island': {'Objects': {'node': {'Type': 'Quest Node', 'Pos': (1, 2, 3), 'Hpr': (45, 0, 0)}}}}}
        self.air.worldCreator.fileDicts['island.py'] = fileData
        self.air.worldCreator.getObjectDataFromFileByUid = lambda uid, fileName: fileData['Objects']['island']['Objects'].get(uid)
        self.placeAvatar(island)
        self.assertEqual(self.step(self.visit('node')),
                         [island.doId, 0, QuestStep.STQuestNode, [1, 2, 3, 45], 'island'])

    def makeEnemy(self, area, pos, avatarType=AvatarTypes.Navy, hp=10):
        enemy = self.make(Enemy, area, pos=pos)
        enemy.getAvatarType = lambda: avatarType
        enemy.getLevel = lambda: 5
        enemy.getHp = lambda: (hp, 10)
        return enemy

    def test_defeat_tasks_point_at_the_closest_enemy(self):
        island = self.make(Island, None, uid=LocationIds.PORT_ROYAL_ISLAND)
        self.makeEnemy(island, (100, 0, 0))
        closest = self.makeEnemy(island, (10, 0, 0))
        self.makeEnemy(island, (1, 0, 0), avatarType=AvatarTypes.Undead)
        self.makeEnemy(island, (2, 0, 0), hp=0)
        self.placeAvatar(island)
        quest = FakeStepQuest(QuestTaskDNA.DefeatTaskDNA(enemyType=AvatarTypes.Navy, num=3))
        self.assertEqual(self.step(quest)[:3], [island.doId, closest.doId, QuestStep.STNPC])

        # defeat tasks at a location lead there, then to the enemies there...
        quest = FakeStepQuest(QuestTaskDNA.DefeatTaskDNA(enemyType=AvatarTypes.Navy, num=3, location=LocationIds.PORT_ROYAL_ISLAND))
        self.assertEqual(self.step(quest)[:3], [island.doId, closest.doId, QuestStep.STNPC])
        other = self.make(Island, None, uid='other')
        self.placeAvatar(other)
        self.assertEqual(self.step(quest)[:3], [other.doId, island.doId, QuestStep.STArea])

        # any area of the location counts, the caves of the island as well...
        cave = self.make(Interior, None, uid=LocationIds.PORT_ROYAL_CAVE_A)
        cavern = self.makeEnemy(cave, (3, 0, 0))
        self.placeAvatar(cave)
        quest = FakeStepQuest(QuestTaskDNA.DefeatTaskDNA(enemyType=AvatarTypes.Navy, num=3, location=LocationIds.PORT_ROYAL_ALL))
        self.assertEqual(self.step(quest)[:3], [cave.doId, cavern.doId, QuestStep.STNPC])

    def test_ship_tasks_point_at_the_closest_ship_at_sea(self):
        oceanGrid = self.make(OceanGrid, None)
        ship = self.make(Ship, oceanGrid, pos=(0, 0, 0))
        enemy = self.make(Ship, oceanGrid, pos=(500, 0, 0), getNPCship=lambda: True, isSailable=lambda: True,
                          getIsFlagship=lambda: False)
        quest = FakeStepQuest(QuestTaskDNA.DefeatShipTaskDNA(num=1))
        self.placeAvatar(ship)
        self.assertEqual(self.step(quest), [oceanGrid.doId, enemy.doId, QuestStep.STShip, [500, 0, 0, 0], ''])

        island = self.make(Island, None, uid='island')
        self.placeAvatar(island)
        self.assertEqual(self.step(quest)[:3], [0, 0, 0])

    def test_container_tasks_point_at_a_container_yet_to_be_searched(self):
        island = self.make(Island, None, uid='island')
        searched = self.make(Container, island, uid='barrel-1', pos=(1, 0, 0))
        barrel = self.make(Container, island, uid='barrel-2', pos=(9, 0, 0))
        quest = FakeStepQuest(QuestTaskDNA.RecoverContainerItemTaskDNA(containerId='barrel-1'))
        self.placeAvatar(island)
        self.assertEqual(self.step(quest)[:3], [island.doId, searched.doId, QuestStep.STNPC])
        quest.getTaskStates()[0].searchedContainer('barrel-1')
        self.assertEqual(self.step(quest)[:3], [0, 0, 0])

    def test_progress_on_a_defeat_task_resends_the_step(self):
        quest = FakeStepQuest(QuestTaskDNA.DefeatTaskDNA(enemyType=AvatarTypes.Navy, num=3))
        key = self.manager.getQuestStepGoalKey(self.avatar, quest)
        quest.getTaskStates()[0].setGoal(3)
        quest.getTaskStates()[0].handleProgress()
        self.assertNotEqual(self.manager.getQuestStepGoalKey(self.avatar, quest), key)

        visit = self.visit('npc')
        self.assertEqual(self.manager.getQuestStepGoalKey(self.avatar, visit), 'npc')


if __name__ == '__main__':
    unittest.main()
