import ast
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from pirates.leveleditor import NPCList
from pirates.leveleditor.worldData.RambleshackWorld import objectStruct
from pirates.piratesbase import PiratesGlobals
from pirates.ship import ShipGlobals
from pirates.tutorial import TutorialGlobals
from pirates.world import WorldGlobals


ROOT = Path(__file__).parent


def load_builder_methods():
    source = (ROOT / 'pirates/world/ClientAreaBuilderAI.py').read_text()
    parsed = ast.parse(source)
    builder_class = next(
        node for node in parsed.body
        if isinstance(node, ast.ClassDef) and node.name == 'ClientAreaBuilderAI')
    methods = [
        node for node in builder_class.body
        if isinstance(node, ast.FunctionDef)
        and node.name in {
            'addObject', 'removeObject', 'createObject', 'createTutorialShip',
            'createTutorialStumpy',
        }
    ]
    namespace = {
        'ObjectList': types.SimpleNamespace(
            AREA_TYPE_ISLAND='Island',
            AREA_TYPE_SHIP_PART='Ship Part'),
        'PiratesGlobals': PiratesGlobals,
        'ShipGlobals': ShipGlobals,
        'TutorialGlobals': TutorialGlobals,
        'WorldGlobals': WorldGlobals,
    }
    exec(compile(ast.Module(body=methods, type_ignores=[]), str(ROOT), 'exec'), namespace)
    return type('BuilderMethods', (), {
        method.name: namespace[method.name] for method in methods
    })


def load_tutorial_ship_methods():
    source = (ROOT / 'pirates/ship/TutorialShipAI.py').read_text()
    parsed = ast.parse(source)
    ship_class = next(
        node for node in parsed.body
        if isinstance(node, ast.ClassDef) and node.name == 'TutorialShipAI')
    methods = [
        node for node in ship_class.body
        if isinstance(node, ast.FunctionDef)
        and node.name in {
            '_buildAuthoredRoute', '_getTutorialSailingRoute',
            'startSailing', '_sailToNextWaypoint',
            '_startAuthoredMovementTo', 'stopSailing',
            'setTutorialStumpy', 'setTutorialAuthoredPose',
            'resetSailingToAuthoredPose', 'delete',
        }
    ]
    class StubDistributedShipAI:
        def delete(self):
            self.baseDeleted = True

    namespace = {'DistributedShipAI': StubDistributedShipAI}
    exec(compile(ast.Module(body=methods, type_ignores=[]), str(ROOT), 'exec'), namespace)
    return type('TutorialShipMethods', (), {
        method.name: namespace[method.name] for method in methods
    })


class StubShip:
    def __init__(self, air):
        self.air = air
        self.doId = 42
        self.values = {}

    def getUniqueId(self):
        return self.values['setUniqueId']

    def __getattr__(self, name):
        if name.startswith('set'):
            def set_value(*args):
                self.values[name] = args[0] if len(args) == 1 else args
            return set_value
        raise AttributeError(name)

    def sendCurrentPosition(self):
        self.values['sentCurrentPosition'] = True

    def startPosHprBroadcast(self):
        self.values['startedPositionBroadcast'] = True

    def b_setGameState(self, state, avatarId):
        self.values['gameState'] = (state, avatarId)

    def generateChildWithRequired(self, child, zoneId):
        self.values.setdefault('generatedChildren', []).append((child, zoneId))

    def setTutorialStumpy(self, stumpy, builder):
        self.values['tutorialStumpy'] = (stumpy, builder)


class StubTownfolk:
    def __init__(self, air):
        self.air = air
        self.doId = 43
        self.values = {}
        self.setPosCalls = []

    def getUniqueId(self):
        return self.values['setUniqueId']

    def getZ(self):
        return 9

    def getStartState(self):
        return self.values['setStartState']

    def requestDelete(self):
        self.values['requestDelete'] = True

    def __getattr__(self, name):
        if name.startswith('set'):
            def set_value(*args):
                self.values[name] = args[0] if len(args) == 1 else args
                if name == 'setPos':
                    self.setPosCalls.append(args)
            return set_value
        if name in {'d_setInitZ', 'd_setSpawnIn', 'b_setGameState'}:
            return lambda *args: self.values.__setitem__(name, args)
        raise AttributeError(name)

class StubOceanGrid:
    def __init__(self):
        self.generated = []
        self.added = []

    def getZoneFromXYZ(self, pos):
        self.position = tuple(pos)
        return 987

    def generateChildWithRequired(self, ship, zoneId):
        self.generated.append((ship, zoneId))

    def addObjectToOceanGrid(self, ship):
        self.added.append(ship)


class StubUidManager:
    def __init__(self):
        self.uids = {}

    def addUid(self, uniqueId, doId):
        self.uids[uniqueId] = doId

    def removeUid(self, uniqueId):
        self.uids.pop(uniqueId, None)

    def justGetMeMeObject(self, uniqueId):
        return None


class StubParent:
    def __init__(self):
        self.oceanGrid = StubOceanGrid()

    def getFileName(self):
        return WorldGlobals.PiratesTutorialSceneFileBase

    def getUniqueId(self):
        return '1115838788a.58jubutler'


class StubAir:
    def __init__(self):
        self.uidMgr = StubUidManager()
        self.movementLinks = []
        self.worldCreator = types.SimpleNamespace(
            movementLinkManager=types.SimpleNamespace(
                registerMovementLinkData=self.movementLinks.append))


class TutorialCannonProjectileTests(unittest.TestCase):
    def setUp(self):
        source = (ROOT / 'pirates/battle/DistributedTutorialShipCannonAI.py').read_text()
        parsed = ast.parse(source)
        cannon_class = next(
            node for node in parsed.body
            if isinstance(node, ast.ClassDef)
            and node.name == 'DistributedTutorialShipCannonAI')

        class BaseCannon:
            def __init__(self, air):
                self.air = air

        self.weapon_globals = types.SimpleNamespace(WEAPON_MOVIE_START=1)
        self.inventory = types.SimpleNamespace(CannonShoot=12900, CannonRoundShot=12901)
        namespace = {
            'DistributedShipCannonAI': BaseCannon,
            'DirectNotifyGlobal': types.SimpleNamespace(
                directNotify=types.SimpleNamespace(
                    newCategory=lambda name: types.SimpleNamespace(
                        warning=lambda message: None))),
            'WeaponGlobals': self.weapon_globals,
            'InventoryType': self.inventory,
            'globalClockDelta': types.SimpleNamespace(
                getRealNetworkTime=lambda bits: 123),
        }
        exec(compile(ast.Module(body=[cannon_class], type_ignores=[]),
                     str(ROOT / 'pirates/battle/DistributedTutorialShipCannonAI.py'),
                     'exec'), namespace)
        self.sender = 42
        self.avatar = types.SimpleNamespace(doId=self.sender)
        air = types.SimpleNamespace(
            doId2do={self.sender: self.avatar},
            getAvatarIdFromSender=lambda: self.sender)
        self.cannon = namespace['DistributedTutorialShipCannonAI'](air)
        self.cannon.userId = self.sender
        self.cannon.avatarId = self.sender
        self.cannon.mode = self.weapon_globals.WEAPON_MOVIE_START
        self.updates = []
        self.cannon.sendUpdate = lambda name, args: self.updates.append((name, args))

    def fire(self, skill=None, ammo=None):
        self.cannon.requestProjectileSkill(
            self.inventory.CannonShoot if skill is None else skill,
            self.inventory.CannonRoundShot if ammo is None else ammo,
            [0] * 6, 10, 0.8)

    def test_wreck_hits_do_not_block_subsequent_shots(self):
        for _ in range(3):
            self.fire()
        self.assertEqual(len(self.updates), 3)
        self.assertTrue(all(name == 'useProjectileSkill' and args[3] == 123
                            for name, args in self.updates))

    def test_rejects_non_user_inactive_cannon_and_wrong_skills(self):
        self.sender = 43
        self.cannon.air.doId2do[43] = types.SimpleNamespace(doId=43)
        self.fire()
        self.sender = 42
        self.cannon.mode = 0
        self.fire()
        self.cannon.mode = self.weapon_globals.WEAPON_MOVIE_START
        self.fire(skill=1)
        self.fire(ammo=2)
        self.assertEqual(self.updates, [])


class TutorialShipBoardingTests(unittest.TestCase):
    def setUp(self):
        ship_source = (ROOT / 'pirates/ship/DistributedShipAI.py').read_text()
        ship_tree = ast.parse(ship_source)
        ship_class = next(node for node in ship_tree.body
                          if isinstance(node, ast.ClassDef)
                          and node.name == 'DistributedShipAI')
        methods = [node for node in ship_class.body
                   if isinstance(node, ast.FunctionDef)
                   and node.name in {'handleChildArrive', '_sendBoardingMovie'}]

        class Avatar:
            doId = 42

        class Moving:
            @staticmethod
            def handleChildArrive(ship, child, zone):
                ship.events.append(('moving', child.doId, zone))

        class Charterable:
            @staticmethod
            def handleChildArrive(ship, child, zone):
                ship.events.append(('charterable', child.doId, zone))

        namespace = {'DistributedPlayerPirateAI': Avatar,
                     'DistributedMovingObjectAI': Moving,
                     'DistributedCharterableObjectAI': Charterable}
        exec(compile(ast.Module(body=methods, type_ignores=[]),
                     str(ROOT / 'pirates/ship/DistributedShipAI.py'), 'exec'),
             namespace)

        class Ship:
            handleChildArrive = namespace['handleChildArrive']
            if '_sendBoardingMovie' in namespace:
                _sendBoardingMovie = namespace['_sendBoardingMovie']

            def __init__(self):
                self.events = []

            def _playerBoarded(self, avatar):
                self.events.append(('boarded', avatar.doId))

            def sendUpdateToAvatarId(self, av_id, name, args):
                self.events.append((name, av_id, args))

        tutorial_source = (ROOT / 'pirates/ship/TutorialShipAI.py').read_text()
        tutorial_tree = ast.parse(tutorial_source)
        tutorial_class = next(node for node in tutorial_tree.body
                              if isinstance(node, ast.ClassDef)
                              and node.name == 'TutorialShipAI')
        tutorial_methods = [node for node in tutorial_class.body
                            if isinstance(node, ast.FunctionDef)
                            and node.name == '_sendBoardingMovie']
        tutorial_namespace = {}
        exec(compile(ast.Module(body=tutorial_methods, type_ignores=[]),
                     str(ROOT / 'pirates/ship/TutorialShipAI.py'), 'exec'),
             tutorial_namespace)
        self.TutorialShip = type('TutorialShip', (Ship,), tutorial_namespace)
        self.Ship = Ship
        self.avatar = Avatar()

    def test_tutorial_boarding_does_not_restart_the_cutscene(self):
        ship = self.TutorialShip()
        ship.handleChildArrive(self.avatar, PiratesGlobals.ShipZoneOnDeck)
        self.assertEqual(ship.events, [
            ('boarded', 42),
            ('moving', 42, PiratesGlobals.ShipZoneOnDeck),
            ('charterable', 42, PiratesGlobals.ShipZoneOnDeck),
        ])

    def test_normal_ship_still_sends_boarding_movie(self):
        ship = self.Ship()
        ship.handleChildArrive(self.avatar, PiratesGlobals.ShipZoneOnDeck)
        self.assertEqual(ship.events[1], ('setMovie', 42, [0, 42, 0, 1, 0]))


class AuthoredTutorialShipTests(unittest.TestCase):
    def test_missing_ocean_grid_fails_tutorial_ship_creation(self):
        builder_methods = load_builder_methods()
        builder = builder_methods.__new__(builder_methods)
        builder.parent = types.SimpleNamespace(oceanGrid=None)
        fake_ship_module = types.ModuleType('pirates.ship.TutorialShipAI')
        fake_ship_module.TutorialShipAI = StubShip
        with patch.dict(sys.modules, {'pirates.ship.TutorialShipAI': fake_ship_module}):
            with self.assertRaisesRegex(RuntimeError, 'without an ocean grid'):
                builder.createTutorialShip({}, TutorialGlobals.STUMPY_BOAT_UID)

    def test_missing_stumpy_dna_fails_tutorial_ship_creation(self):
        builder_methods = load_builder_methods()
        builder = builder_methods.__new__(builder_methods)
        fake_townfolk_module = types.ModuleType('pirates.npc.DistributedNPCTownfolkAI')
        fake_townfolk_module.DistributedNPCTownfolkAI = StubTownfolk
        with patch.dict(sys.modules, {'pirates.npc.DistributedNPCTownfolkAI': fake_townfolk_module}):
            with patch.dict(NPCList.NPC_LIST, {'1153439632.21darren': None}):
                with self.assertRaisesRegex(RuntimeError, 'without townsperson DNA'):
                    builder.createTutorialStumpy(None)

    def test_authored_stumpy_ship_generates_and_registers_its_uid(self):
        region = objectStruct['Objects']['1115838788a.58jubutler']
        boatId = TutorialGlobals.STUMPY_BOAT_UID
        boatData = region['Objects'][boatId]
        self.assertEqual(boatData['Type'], 'Ship Part')
        self.assertEqual(boatData['Category'], 'InterceptorTutorial')

        fake_ship_module = types.ModuleType('pirates.ship.TutorialShipAI')
        fake_ship_module.TutorialShipAI = StubShip
        fake_townfolk_module = types.ModuleType(
            'pirates.npc.DistributedNPCTownfolkAI')
        fake_townfolk_module.DistributedNPCTownfolkAI = StubTownfolk
        builder_methods = load_builder_methods()
        builder = builder_methods.__new__(builder_methods)
        builder.air = StubAir()
        builder.parent = StubParent()
        builder.objectList = {}

        with patch.dict(sys.modules, {
            'pirates.ship.TutorialShipAI': fake_ship_module,
            'pirates.npc.DistributedNPCTownfolkAI': fake_townfolk_module,
        }):
            with patch('pirates.battle.EnemyGlobals.getRandomEnemyLevel', return_value=1):
                with patch('pirates.battle.EnemyGlobals.getEnemyStats', return_value=(100, 25)):
                    ship = builder.createObject(
                        boatData['Type'], boatData, builder.parent,
                        '1115838788a.58jubutler', boatId, False)

        self.assertIsInstance(ship, StubShip)
        self.assertEqual(ship.values['setUniqueId'], boatId)
        self.assertEqual(ship.values['setShipClass'], ShipGlobals.STUMPY_SHIP)
        self.assertEqual(ship.values['setBaseTeam'], ShipGlobals.PLAYER_TEAM)
        self.assertEqual(ship.values['setNPCship'], 1)
        self.assertEqual(ship.values['setIsBoardable'], 1)
        self.assertEqual(ship.values['gameState'], (boatData['Start State'], 0))
        self.assertEqual(
            ship.values['setPos'],
            (builder.parent.oceanGrid,) + tuple(boatData['Pos']))
        self.assertEqual(
            ship.values['setHpr'],
            (builder.parent.oceanGrid,) + tuple(boatData['Hpr']))
        self.assertEqual(builder.parent.oceanGrid.position, tuple(boatData['Pos']))
        self.assertEqual(builder.parent.oceanGrid.generated, [(ship, 987)])
        self.assertEqual(builder.parent.oceanGrid.added, [ship])
        self.assertTrue(ship.values['sentCurrentPosition'])
        self.assertTrue(ship.values['startedPositionBroadcast'])
        stumpy, owner = ship.values['tutorialStumpy']
        self.assertIsInstance(stumpy, StubTownfolk)
        self.assertIs(owner, builder)
        self.assertEqual(builder.air.uidMgr.uids[boatId], ship.doId)
        self.assertEqual(builder.air.movementLinks, [builder.parent.getUniqueId()])
        self.assertEqual(
            builder.air.uidMgr.uids[TutorialGlobals.STUMPY_UID], stumpy.doId)
        self.assertIs(builder.objectList[ship.doId], ship)
        self.assertIs(builder.objectList[stumpy.doId], stumpy)

    def test_tutorial_stumpy_is_registered_on_deck_with_client_dna_and_pose(self):
        dnaId = '1153439632.21darren'
        self.assertEqual(NPCList.NPC_LIST[dnaId + '_type'], 'Townsperson')
        builder_methods = load_builder_methods()
        builder = builder_methods.__new__(builder_methods)
        builder.air = StubAir()
        builder.objectList = {}
        builder.notify = types.SimpleNamespace(warning=lambda message: None)
        ship = StubShip(builder.air)

        fake_townfolk_module = types.ModuleType(
            'pirates.npc.DistributedNPCTownfolkAI')
        fake_townfolk_module.DistributedNPCTownfolkAI = StubTownfolk
        with patch.dict(sys.modules, {
            'pirates.npc.DistributedNPCTownfolkAI': fake_townfolk_module,
        }):
            with patch('pirates.battle.EnemyGlobals.getRandomEnemyLevel', return_value=1):
                with patch('pirates.battle.EnemyGlobals.getEnemyStats', return_value=(100, 25)):
                    stumpy = builder.createTutorialStumpy(ship)

        self.assertIsInstance(stumpy, StubTownfolk)
        self.assertEqual(stumpy.values['setUniqueId'], TutorialGlobals.STUMPY_UID)
        self.assertEqual(stumpy.values['setDNAId'], dnaId)
        self.assertEqual(stumpy.values['setName'], NPCList.NPC_LIST[dnaId][NPCList.setName])
        self.assertEqual(stumpy.setPosCalls[-1], (ship, 0, -1.2, 9))
        self.assertEqual(stumpy.values['setHpr'], (ship, 180, 0, 0))
        self.assertEqual(
            ship.values['generatedChildren'],
            [(stumpy, PiratesGlobals.ShipZoneOnDeck)])
        self.assertEqual(builder.air.uidMgr.uids[TutorialGlobals.STUMPY_UID], stumpy.doId)
        self.assertIs(builder.objectList[stumpy.doId], stumpy)
        self.assertEqual(stumpy.values['setStartState'], 'Idle')
        self.assertEqual(stumpy.values['b_setGameState'], ('Idle',))


class TutorialShipSailingTests(unittest.TestCase):
    def test_sailing_follows_authored_loop_and_can_stop(self):
        region = objectStruct['Objects']['1115838788a.58jubutler']
        objects = region['Objects']
        boatId = TutorialGlobals.STUMPY_BOAT_UID
        expectedWaypointIds = [
            '1125013326.85jubutler',
            '1171449664.73MAsaduzz',
            '1171449676.98MAsaduzz',
            '1171449691.62MAsaduzz',
            '1171449714.51MAsaduzz',
        ]

        class WorldCreator:
            movementLinkManager = types.SimpleNamespace(
                movementLinkData={'rambleshack': objectStruct['Node Links']})

            def getObjectDataByUid(self, uniqueId):
                return objects.get(uniqueId)

        class SailingFSM:
            def __init__(self):
                self.moves = []
                self.stops = 0

            def _initWorldRefs(self):
                pass

            def _isWithinGridBounds(self, x, y):
                return True

            def _isPositionSafe(self, pos):
                return True

            def _isPathSafe(self, start, end):
                return True

            def _getShipSpeed(self):
                return 25

            def _startMovementTo(self, destination, speed, onComplete=None):
                self.moves.append((destination, speed, onComplete))

            def _stopMovement(self):
                self.stops += 1

        ship_class = load_tutorial_ship_methods()
        ship = ship_class()
        ship.air = types.SimpleNamespace(worldCreator=WorldCreator())
        ship.getUniqueId = lambda: boatId
        ship.getPos = lambda: objects[boatId]['Pos']
        ship.gameFSM = SailingFSM()
        ship.notify = types.SimpleNamespace(warning=lambda message: None)
        ship.parentId = 987
        ship.zoneId = 1
        ship.b_setLocation = lambda parentId, zoneId: setattr(
            ship, 'locationUpdate', (parentId, zoneId))
        ship.sendCurrentPosition = lambda: setattr(ship, 'positionSent', True)
        ship.values = {}
        ship.setPos = lambda *args: ship.values.__setitem__('setPos', args)
        ship.setHpr = lambda *args: ship.values.__setitem__('setHpr', args)
        ship._tutorialSailing = False
        ship._tutorialSailingRoute = []
        ship._tutorialSailingIndex = 0
        ship._startAuthoredMovementTo = lambda destination, speed, onComplete=None: (
            ship.gameFSM.moves.append((destination, speed, onComplete)) or True)
        ship.tutorialOceanGrid = types.SimpleNamespace(
            doId=987, getZoneFromXYZ=lambda pos: 2330)
        ship.tutorialAuthoredPos = tuple(objects[boatId]['Pos'])
        ship.tutorialAuthoredHpr = tuple(objects[boatId]['Hpr'])

        route = ship._getTutorialSailingRoute()
        self.assertEqual([uid for uid, _ in route], expectedWaypointIds)

        self.assertTrue(ship.startSailing())
        firstMove = ship.gameFSM.moves[0]
        self.assertEqual(tuple(firstMove[0]), tuple(objects[expectedWaypointIds[0]]['Pos']))
        self.assertEqual(firstMove[1], 25)
        self.assertTrue(callable(firstMove[2]))
        firstMove[2]()
        self.assertEqual(
            tuple(ship.gameFSM.moves[1][0]),
            tuple(objects[expectedWaypointIds[1]]['Pos']))

        self.assertTrue(ship.resetSailingToAuthoredPose())
        self.assertFalse(ship._tutorialSailing)
        self.assertEqual(ship._tutorialSailingRoute, [])
        self.assertEqual(ship._tutorialSailingIndex, 0)
        self.assertEqual(ship.gameFSM.stops, 1)
        self.assertEqual(ship.locationUpdate, (987, 2330))
        self.assertEqual(
            ship.values['setPos'],
            (ship.tutorialOceanGrid,) + ship.tutorialAuthoredPos)
        self.assertEqual(
            ship.values['setHpr'],
            (ship.tutorialOceanGrid,) + ship.tutorialAuthoredHpr)
        self.assertTrue(ship.positionSent)

        self.assertTrue(ship.startSailing())
        self.assertEqual(
            tuple(ship.gameFSM.moves[2][0]),
            tuple(objects[expectedWaypointIds[0]]['Pos']))
        ship.stopSailing()
        self.assertEqual(ship.gameFSM.stops, 2)

    def test_authored_leg_uses_interval_and_position_broadcast_contract(self):
        from panda3d.core import Point3

        class DestinationNode:
            def setPos(self, pos):
                self.pos = pos

            def removeNode(self):
                self.removed = True

        class OceanGrid:
            def attachNewNode(self, name):
                self.destinationNode = DestinationNode()
                self.destinationName = name
                return self.destinationNode

        class SailingFSM:
            oceanGrid = OceanGrid()

            def __init__(self):
                self.stopped = 0

            def _stopMovement(self):
                self.stopped += 1

            def _getMovementDoneName(self):
                return 'tutorial-movement-done'

            def _onMovementComplete(self):
                pass

        ship_class = load_tutorial_ship_methods()
        ship = ship_class()
        ship.doId = 42
        ship.gameFSM = SailingFSM()
        ship.getPos = lambda: Point3(128.511, 152.104, 0)
        ship.lookAt = lambda node: setattr(ship, 'lookAtNode', node)
        ship.posInterval = lambda duration, pos, other: self._make_interval(
            duration, pos, other)
        ship.acceptOnce = lambda event, callback: setattr(
            ship, 'acceptedMovement', (event, callback))

        callback = lambda: None
        destination = Point3(295.185, 181.66, 0)
        self.assertTrue(ship._startAuthoredMovementTo(destination, 25, callback))

        interval = ship.gameFSM._moveInterval
        self.assertAlmostEqual(interval.duration, (destination - ship.getPos()).length() / 25)
        self.assertEqual(interval.pos, tuple(destination))
        self.assertIs(interval.other, ship.gameFSM.oceanGrid)
        self.assertEqual(interval.doneEvent, 'tutorial-movement-done')
        self.assertTrue(interval.started)
        self.assertEqual(
            ship.acceptedMovement,
            ('tutorial-movement-done', ship.gameFSM._onMovementComplete))
        self.assertIs(ship.gameFSM._movementCallback, callback)
        self.assertTrue(ship.gameFSM.stopped)

    @staticmethod
    def _make_interval(duration, pos, other):
        class StubInterval:
            def setDoneEvent(self, event):
                self.doneEvent = event

            def start(self):
                self.started = True

        interval = StubInterval()
        interval.duration = duration
        interval.pos = pos
        interval.other = other
        return interval

    def test_ship_delete_unregisters_and_deletes_its_stumpy_child(self):
        ship_class = load_tutorial_ship_methods()
        builder_methods = load_builder_methods()
        builder = builder_methods.__new__(builder_methods)
        builder.air = StubAir()
        builder.objectList = {}

        ship = ship_class()
        ship.doId = 42
        ship.getUniqueId = lambda: TutorialGlobals.STUMPY_BOAT_UID
        ship._tutorialSailing = False
        ship._tutorialSailingRoute = []
        ship._tutorialSailingIndex = 0

        stumpy = StubTownfolk(builder.air)
        stumpy.doId = 43
        stumpy.values['setUniqueId'] = TutorialGlobals.STUMPY_UID
        builder.objectList = {ship.doId: ship, stumpy.doId: stumpy}
        builder.air.uidMgr.uids = {
            TutorialGlobals.STUMPY_BOAT_UID: ship.doId,
            TutorialGlobals.STUMPY_UID: stumpy.doId,
        }
        ship.setTutorialStumpy(stumpy, builder)

        ship.delete()

        self.assertNotIn(ship.doId, builder.objectList)
        self.assertNotIn(stumpy.doId, builder.objectList)
        self.assertNotIn(TutorialGlobals.STUMPY_BOAT_UID, builder.air.uidMgr.uids)
        self.assertNotIn(TutorialGlobals.STUMPY_UID, builder.air.uidMgr.uids)
        self.assertTrue(stumpy.values['requestDelete'])
        self.assertTrue(ship.baseDeleted)

    def test_authored_sailing_route_relocates_at_ocean_interest_boundary(self):
        from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI

        region = objectStruct['Objects']['1115838788a.58jubutler']
        objects = region['Objects']
        routeIds = [
            TutorialGlobals.STUMPY_BOAT_UID,
            '1125013326.85jubutler',
            '1171449664.73MAsaduzz',
            '1171449676.98MAsaduzz',
            '1171449691.62MAsaduzz',
            '1171449714.51MAsaduzz',
        ]
        oceanGrid = types.SimpleNamespace(
            startingZone=WorldGlobals.OCEAN_GRID_STARTING_ZONE,
            gridSize=WorldGlobals.OCEAN_GRID_SIZE,
            cellWidth=WorldGlobals.OCEAN_CELL_SIZE)

        zones = {
            uid: DistributedCartesianGridAI.getZoneFromXYZ(
                oceanGrid, objects[uid]['Pos'])
            for uid in routeIds
        }
        self.assertEqual(len(set(zones.values())), 2)
        self.assertEqual(zones[TutorialGlobals.STUMPY_BOAT_UID], 2330)
        self.assertEqual(zones['1171449714.51MAsaduzz'], 2329)


class TutorialCannonTests(unittest.TestCase):
    def test_tutorial_cannon_uses_initialized_ship_cannon_ai(self):
        notify = types.SimpleNamespace(
            directNotify=types.SimpleNamespace(newCategory=lambda name: name))

        class StubPCCannonAI:
            def __init__(self, air):
                self.pcCannonAir = air

        class StubShippartAI:
            def __init__(self, air):
                self.shippartAir = air

        class StubCannonDNA:
            def __init__(self):
                self.baseTeam = 0
                self.cannonType = 0
                self.ammoType = 2

        namespace = {
            'DirectNotifyGlobal': notify,
            'DistributedPCCannonAI': StubPCCannonAI,
            'DistributedShippartAI': StubShippartAI,
            'CannonDNA': StubCannonDNA,
            'InventoryType': types.SimpleNamespace(
                CannonShoot=1, CannonRoundShot=2),
        }
        cannon_source = (ROOT / 'pirates/battle/DistributedShipCannonAI.py').read_text()
        cannon_tree = ast.parse(cannon_source)
        cannon_classes = [
            node for node in cannon_tree.body
            if isinstance(node, ast.ClassDef)
            and node.name in {'DistributedCannonDNA', 'DistributedShipCannonAI'}
        ]
        exec(compile(
            ast.Module(body=cannon_classes, type_ignores=[]),
            str(ROOT / 'pirates/battle/DistributedShipCannonAI.py'),
            'exec'), namespace)

        tutorial_source = (ROOT / 'pirates/battle/DistributedTutorialShipCannonAI.py').read_text()
        tutorial_tree = ast.parse(tutorial_source)
        tutorial_class = next(
            node for node in tutorial_tree.body
            if isinstance(node, ast.ClassDef)
            and node.name == 'DistributedTutorialShipCannonAI')
        # Execute the real constructors while replacing game-runtime base classes.
        exec(compile(
            ast.Module(body=[tutorial_class], type_ignores=[]),
            str(ROOT / 'pirates/battle/DistributedTutorialShipCannonAI.py'),
            'exec'), namespace)

        air = object()
        cannon = namespace['DistributedTutorialShipCannonAI'](air)
        self.assertIsInstance(cannon, namespace['DistributedShipCannonAI'])
        self.assertIs(cannon.pcCannonAir, air)
        self.assertIs(cannon.shippartAir, air)
        self.assertEqual(cannon.baseTeam, 0)
        self.assertEqual(cannon.cannonType, 0)
        self.assertEqual(cannon.ammoType, 2)
        self.assertEqual(cannon.cannonIndex, 0)

    def test_ship_generator_selects_tutorial_class_only_for_tutorial_type(self):
        source = (ROOT / 'pirates/ship/DistributedShipAI.py').read_text()
        parsed = ast.parse(source)
        ship_class = next(
            node for node in parsed.body
            if isinstance(node, ast.ClassDef) and node.name == 'DistributedShipAI')
        announce = next(
            node for node in ship_class.body
            if isinstance(node, ast.FunctionDef) and node.name == 'announceGenerate')
        selection = next(
            node for node in ast.walk(announce)
            if isinstance(node, ast.If)
            and isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == 'cannonType'
            and isinstance(node.test.comparators[0], ast.Attribute)
            and node.test.comparators[0].attr == 'TUTORIAL_CANNON')

        class GenericCannon:
            def __init__(self, air):
                self.air = air

        class TutorialCannon:
            def __init__(self, air):
                self.air = air

        class Ship:
            air = object()

        namespace = {
            'ShipGlobals': ShipGlobals,
            'DistributedShipCannonAI': GenericCannon,
            'DistributedTutorialShipCannonAI': TutorialCannon,
            'self': Ship(),
            'cannonType': ShipGlobals.TUTORIAL_CANNON,
        }
        exec(compile(
            ast.Module(body=[selection], type_ignores=[]),
            str(ROOT / 'pirates/ship/DistributedShipAI.py'),
            'exec'), namespace)
        self.assertIsInstance(namespace['cannon'], TutorialCannon)

        namespace['cannonType'] = ShipGlobals.TUTORIAL_CANNON + 1
        exec(compile(
            ast.Module(body=[selection], type_ignores=[]),
            str(ROOT / 'pirates/ship/DistributedShipAI.py'),
            'exec'), namespace)
        self.assertIsInstance(namespace['cannon'], GenericCannon)


if __name__ == '__main__':
    unittest.main()
