import builtins
import collections
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

from direct.distributed.DistributedObjectAI import DistributedObjectAI

# WeaponGlobals needs game resources which are not available to the tests,
# and the instance base classes pull in the entire client avatar stack...
_stubbedModules = ['pirates.battle.WeaponGlobals', 'pirates.instance.DistributedInstanceWorldAI']
_originalModules = dict([(name, sys.modules.get(name)) for name in _stubbedModules])
sys.modules.setdefault('pirates.battle.WeaponGlobals', MagicMock())


class FakeInstanceWorldAI(DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.uniqueId = ''
        self.fileName = ''
        self.type = 0
        self.spawnPts = {}
        self.oceanGrid = None
        self.builder = SimpleNamespace(objectList={}, getIslands=lambda: [],
            getObject=lambda doId=None, uniqueId=None: None)

    def getType(self):
        return self.type

    def getFileName(self):
        return self.fileName

    def getUniqueId(self):
        return self.uniqueId

    def getSpawnPt(self, area, index=None):
        return (0, 0, 0, 0)

    def d_setSpawnInfo(self, avatarId, x, y, z, h, spawnZone, parents):
        self.sendUpdateToAvatarId(avatarId, 'setSpawnInfo', [x, y, z, h, spawnZone, parents])

    def getSubInstances(self):
        return []

    def removeSubInstance(self, subInstance):
        pass


instanceModule = types.ModuleType('pirates.instance.DistributedInstanceWorldAI')
instanceModule.DistributedInstanceWorldAI = FakeInstanceWorldAI
sys.modules['pirates.instance.DistributedInstanceWorldAI'] = instanceModule

from pirates.piratesbase import PiratesGlobals
from pirates.pvp import PVPGlobals
from pirates.pvp import PVPManagerAI as manager_module
from pirates.pvp.DistributedPVPInstanceAI import DistributedPVPInstanceAI, READY
from pirates.pvp.DistributedPVPBattleAI import DistributedPVPBattleAI
from pirates.pvp.DistributedPVPTeamBattleAI import DistributedPVPTeamBattleAI
from pirates.pvp.DistributedPVPShipBattleAI import DistributedPVPShipBattleAI
from pirates.pvp.PVPGameCTLAI import PVPGameCTLAI
from pirates.pvp.PVPGamePirateerAI import PVPGamePirateerAI
from pirates.pvp.DistributedBankAI import DistributedBankAI
from pirates.pvp.DistributedWreckAI import DistributedWreckAI
from pirates.pvp.ScoreboardAI import ScoreboardAI
from pirates.uberdog.UberDogGlobals import InventoryType

# put back the real modules so other tests in the same session are unaffected
for _name, _module in list(_originalModules.items()):
    if _module is None:
        sys.modules.pop(_name, None)
    else:
        sys.modules[_name] = _module


class FakeInventory:

    def __init__(self):
        self.stacks = {}

    def getStackQuantity(self, stackType):
        return self.stacks.get(stackType, 0)

    def b_setStackQuantity(self, stackType, quantity):
        self.stacks[stackType] = quantity


class FakeAvatar:

    def __init__(self, doId, name='Pirate'):
        self.doId = doId
        self.name = name
        self.pvpTeam = 0
        self.hp = 0
        self.mojo = 0
        self.inventory = FakeInventory()
        self.lootCarried = (0, 0)
        self.world = None

    def getName(self):
        return self.name

    def getDeleteEvent(self):
        return 'distObjDelete-%d' % self.doId

    def b_setPVPTeam(self, team):
        self.pvpTeam = team

    def getPVPTeam(self):
        return self.pvpTeam

    def getMaxHp(self):
        return 100

    def getMaxMojo(self):
        return 50

    def b_setHp(self, hp):
        self.hp = hp

    def b_setMojo(self, mojo):
        self.mojo = mojo

    def getInventory(self):
        return self.inventory

    def getReturnLocation(self):
        return 'returnIsland'

    def getWorld(self):
        return self.world

    def getInventory(self):
        return self.inventory

    def b_setLootCarried(self, amount, maxCarry):
        self.lootCarried = (amount, maxCarry)

    def getBandId(self):
        return getattr(self, 'bandId', (0, 0))

    def addSkillEffect(self, effectId, duration, attackerId):
        self.skillEffects = getattr(self, 'skillEffects', []) + [[effectId, duration, 0, attackerId]]

    def removeSkillEffect(self, effectId):
        self.skillEffects = [effect for effect in getattr(self, 'skillEffects', [])
                             if effect[0] != effectId]


def makeAir(avatars, senderId=0):
    air = SimpleNamespace(dclassesByName=collections.defaultdict(MagicMock))
    air.doId2do = dict([(avatar.doId, avatar) for avatar in avatars])
    air.senderId = senderId
    air.getAvatarIdFromSender = lambda: air.senderId
    air.allocateZone = Mock(return_value=5000)
    air.clientAddInterest = Mock()
    air.clientRemoveInterest = Mock()
    air.logPotentialHacker = Mock()
    air.teleportMgr = SimpleNamespace(d_initiateTeleport=Mock(), avatar2fsm={})
    air.uidMgr = SimpleNamespace(getDoId=Mock(return_value=None), removeUid=Mock())
    return air


def makeInstance(instanceClass, avatars, senderId=0):
    air = makeAir(avatars, senderId)
    instance = instanceClass(air)
    instance.doId = 9000
    instance.parentId = 4000
    instance.zoneId = 5000
    instance.uniqueId = 'region'
    instance.fileName = 'pvp_captureWorld'
    instance.sendUpdate = Mock()
    instance.sendUpdateToAvatarId = Mock()
    instance.beginBarrier = Mock(return_value=1)
    instance.ignoreBarrier = Mock()
    island = SimpleNamespace(doId=7000, zoneId=7001, parentId=9000,
        getUniqueId=lambda: 'island')
    instance.builder = SimpleNamespace(objectList={}, getIslands=lambda: [island],
        getObject=lambda doId=None, uniqueId=None: island if uniqueId == 'island' else None)
    instance.teamSpawnPts = {
        1: [('island', (1, 1, 1, 0))],
        2: [('island', (2, 2, 2, 0))]}
    instance.isReady = True
    for avatar in avatars:
        avatar.world = instance

    return instance


def updatesNamed(mock, fieldName):
    return [call for call in mock.call_args_list if call[0][1 if len(call[0]) == 3 else 0] == fieldName]


class PVPInstanceTests(unittest.TestCase):

    def tearDown(self):
        taskMgr.removeTasksMatching('*-9000')

    def startTeamBattle(self, avatars=None):
        avatars = avatars or [FakeAvatar(1, 'Jack'), FakeAvatar(2, 'Will')]
        instance = makeInstance(DistributedPVPTeamBattleAI, avatars)
        instance.setupMatch([[1], [2]])
        return instance, avatars

    def test_match_setup_assigns_teams_and_teleports(self):
        instance, avatars = self.startTeamBattle()
        self.assertEqual(instance.state, 'WaitClientsReady')
        self.assertEqual(avatars[0].pvpTeam, 1)
        self.assertEqual(avatars[1].pvpTeam, 2)
        self.assertEqual(sorted(instance.getMatchPlayers()),
            [[1, 'Jack', 1], [2, 'Will', 2]])
        self.assertEqual(instance.stats[1][PVPGlobals.TEAM], 1)
        self.assertEqual(instance.air.clientAddInterest.call_count, 2)
        instance.beginBarrier.assert_called_once()
        self.assertEqual(instance.beginBarrier.call_args[0][0], 'avatarsReady-9000')

        teleport = instance.air.teleportMgr.d_initiateTeleport
        self.assertEqual(teleport.call_count, 2)
        kwargs = teleport.call_args_list[0][1]
        self.assertEqual(kwargs['instanceType'], PiratesGlobals.INSTANCE_PVP)
        self.assertEqual(kwargs['locationUid'], 'island')
        self.assertEqual(kwargs['spawnPt'], (1, 1, 1, 0))
        self.assertIs(kwargs['targetWorld'], instance)

    def test_setup_match_waits_for_instance(self):
        instance = makeInstance(DistributedPVPTeamBattleAI, [FakeAvatar(1)])
        instance.isReady = False
        instance.setupMatch([[1]])
        self.assertEqual(instance.pendingTeams, [[1]])
        self.assertEqual(instance.players, {})

    def test_battle_gives_each_player_own_team(self):
        avatars = [FakeAvatar(1), FakeAvatar(2), FakeAvatar(3)]
        instance = makeInstance(DistributedPVPBattleAI, avatars)
        instance.setupMatch([[1, 2], [3]])
        self.assertEqual([avatar.pvpTeam for avatar in avatars], [1, 2, 3])

    def test_barrier_starts_game(self):
        instance, avatars = self.startTeamBattle()
        callback = instance.beginBarrier.call_args[0][3]
        callback([1, 2])
        self.assertEqual(instance.state, 'Game')
        self.assertEqual(instance.playerStates[1], READY)
        self.assertTrue(updatesNamed(instance.sendUpdate, 'setGameStart'))

    def test_damage_rules(self):
        avatars = [FakeAvatar(1), FakeAvatar(2), FakeAvatar(3)]
        instance = makeInstance(DistributedPVPTeamBattleAI, avatars)
        instance.setupMatch([[1, 3], [2]])
        self.assertFalse(instance.isDamageAllowed(avatars[0], avatars[1]))
        instance.request('Game')
        self.assertTrue(instance.isDamageAllowed(avatars[0], avatars[1]))
        self.assertFalse(instance.isDamageAllowed(avatars[0], avatars[2]))

    def test_defeat_updates_stats_and_wins(self):
        instance, avatars = self.startTeamBattle()
        instance.ScoreLimit = 2
        instance.request('Game')
        instance.avatarAttacked(avatars[0], avatars[1])
        instance.avatarDefeated(avatars[1])
        self.assertEqual(instance.stats[1][PVPGlobals.KILLS], 1)
        self.assertEqual(instance.stats[1][PVPGlobals.SCORE], 1)
        self.assertEqual(instance.stats[2][PVPGlobals.DEATHS], 1)
        events = updatesNamed(instance.sendUpdate, 'setPvpEvent')
        self.assertEqual(events[-1][0][1], [PVPGlobals.EventDefeat, [1, 2]])
        self.assertEqual(instance.state, 'Game')

        instance.avatarAttacked(avatars[0], avatars[1])
        instance.avatarDefeated(avatars[1])
        self.assertEqual(instance.state, 'Completed')
        results = dict([(call[0][0], call[0][2]) for call in
            updatesNamed(instance.sendUpdateToAvatarId, 'setResults')])
        self.assertEqual(results[1][1:], [1, 2, False])
        self.assertEqual(results[2][1:], [2, 2, False])
        self.assertTrue(updatesNamed(instance.sendUpdate, 'setPVPComplete'))
        self.assertEqual(avatars[0].inventory.getStackQuantity(InventoryType.TBTGame), 1)
        self.assertEqual(avatars[1].inventory.getStackQuantity(InventoryType.TBTGame), 0)
        self.assertTrue(avatars[0].inventory.getStackQuantity(InventoryType.PVPTotalInfamyLand) > 0)

    def test_suicide_without_attacker(self):
        instance, avatars = self.startTeamBattle()
        instance.request('Game')
        instance.avatarDefeated(avatars[0])
        self.assertEqual(instance.stats[1][PVPGlobals.DEATHS], 1)
        self.assertEqual(instance.stats[1][PVPGlobals.SCORE], 0)
        events = updatesNamed(instance.sendUpdate, 'setPvpEvent')
        self.assertEqual(events[-1][0][1], [PVPGlobals.EventDefeat, [1, 1]])

    def test_time_limit_tie(self):
        instance, avatars = self.startTeamBattle()
        instance.request('Game')
        instance.request('Completed')
        results = updatesNamed(instance.sendUpdateToAvatarId, 'setResults')
        self.assertTrue(all(call[0][2][3] for call in results))

    def test_respawn_restores_avatar(self):
        instance, avatars = self.startTeamBattle()
        instance.air.senderId = 2
        instance.requestSpawnLoc()
        self.assertEqual(avatars[1].hp, 100)
        self.assertEqual(avatars[1].mojo, 50)
        spawn = updatesNamed(instance.sendUpdateToAvatarId, 'setSpawnInfo')
        self.assertEqual(spawn[-1][0][2], [2, 2, 2, 0, 0, [7000, 7001, 9000]])

    def test_respawn_rejects_outsiders(self):
        outsider = FakeAvatar(5)
        instance, avatars = self.startTeamBattle()
        instance.air.doId2do[5] = outsider
        instance.air.senderId = 5
        instance.requestSpawnLoc()
        instance.air.logPotentialHacker.assert_called_once()

    def test_leave_ends_game_without_opponents(self):
        instance, avatars = self.startTeamBattle()
        instance.request('Game')
        instance.air.senderId = 2
        instance.requestLeave()
        self.assertNotIn(2, instance.players)
        self.assertEqual(avatars[1].pvpTeam, 0)
        self.assertEqual(instance.state, 'Completed')

        # the client teleports itself home, the AI must not start a second teleport...
        teleport = instance.air.teleportMgr.d_initiateTeleport
        self.assertEqual(teleport.call_count, 2)
        self.assertTrue(all(call[1]['instanceType'] == PiratesGlobals.INSTANCE_PVP
                            for call in teleport.call_args_list))
        self.assertTrue(taskMgr.hasTaskNamed('leaveTeleport-2-9000'))

        # the instance interest is closed once the avatar has left
        messenger.send('teleportDone-2')
        instance.air.clientRemoveInterest.assert_called_once()
        self.assertFalse(taskMgr.hasTaskNamed('leaveTeleport-2-9000'))

    def test_leave_falls_back_to_ai_teleport(self):
        instance, avatars = self.startTeamBattle()
        instance.request('Game')
        instance.air.senderId = 2
        instance.requestLeave()
        teleport = instance.air.teleportMgr.d_initiateTeleport

        # the avatar's own teleport is still running, nothing to do...
        instance.air.teleportMgr.avatar2fsm[2] = object()
        instance._DistributedPVPInstanceAI__leaveTeleportTimeout(2)
        self.assertEqual(teleport.call_count, 2)

        # the client never left, send it home ourselves...
        del instance.air.teleportMgr.avatar2fsm[2]
        instance._DistributedPVPInstanceAI__leaveTeleportTimeout(2)
        self.assertEqual(teleport.call_count, 3)
        kwargs = teleport.call_args[1]
        self.assertEqual(kwargs['instanceType'], PiratesGlobals.INSTANCE_MAIN)
        self.assertEqual(kwargs['locationUid'], 'returnIsland')

    def test_completed_leave_waits_for_client_teleport(self):
        instance, avatars = self.startTeamBattle()
        instance.request('Game')
        instance.request('Completed')
        instance._DistributedPVPInstanceAI__completedLeave(None)
        self.assertEqual(len(updatesNamed(instance.sendUpdateToAvatarId, 'performAILeave')), 2)
        self.assertEqual(instance.air.teleportMgr.d_initiateTeleport.call_count, 2)
        self.assertEqual(instance.state, 'Cleanup')

    def test_respawn_gives_spawn_protection(self):
        instance, avatars = self.startTeamBattle()
        instance.request('Game')
        instance.air.senderId = 2
        instance.requestSpawnLoc()
        self.assertTrue(instance.hasSpawnProtection(2))
        weaponGlobals = sys.modules[DistributedPVPInstanceAI.__module__].WeaponGlobals
        self.assertEqual(avatars[1].skillEffects[0][0], weaponGlobals.C_SPAWN)
        self.assertFalse(instance.isDamageAllowed(avatars[0], avatars[1]))
        self.assertTrue(taskMgr.hasTaskNamed('spawnProtection-2-9000'))

        instance._DistributedPVPInstanceAI__spawnProtectionExpired(2)
        self.assertFalse(instance.hasSpawnProtection(2))
        self.assertEqual(avatars[1].skillEffects, [])
        self.assertTrue(instance.isDamageAllowed(avatars[0], avatars[1]))

    def test_load_spawn_points_from_world_data(self):
        instance = makeInstance(DistributedPVPTeamBattleAI, [])
        worlds = {
            'pvp_captureWorld.py': {'Objects': {'region': {'Type': 'Region', 'Objects': {
                'island': {'Type': 'Island', 'File': 'pvp_captureIsland2'}}}}},
            'pvp_captureIsland2.py': {'Objects': {'island': {'Type': 'Island', 'Objects': {
                'fort': {'Type': 'Simple Fort', 'Objects': {
                    'spawn1': {'Type': 'Player Spawn Node', 'Spawnables': 'Team 1',
                        'Pos': (1, 2, 3), 'GridPos': (10, 20, 30), 'Hpr': (90, 0, 0)}}},
                'spawn2': {'Type': 'Player Spawn Node', 'Spawnables': 'Team 2',
                    'Pos': (4, 5, 6), 'Hpr': (0, 0, 0)},
                'spawn3': {'Type': 'Player Spawn Node', 'Spawnables': 'All',
                    'Pos': (7, 8, 9)}}}}}}
        instance.air.worldCreator = SimpleNamespace(openFile=lambda name: worlds.get(name))
        instance.loadSpawnPoints()
        self.assertEqual(instance.teamSpawnPts, {
            1: [('island', (10, 20, 30, 90))],
            2: [('island', (4, 5, 6, 0))],
            0: [('island', (7, 8, 9, 0))]})

    def test_load_spawn_points_from_island_game_areas(self):
        instance = makeInstance(DistributedPVPTeamBattleAI, [])
        worlds = {
            'pvp_captureWorld.py': {'Objects': {'region': {'Type': 'Region', 'Objects': {
                'island': {'Type': 'Island', 'File': 'pvp_deathmatchIsland1'}}}}},
            'pvp_deathmatchIsland1.py': {'Objects': {'island': {'Type': 'Island', 'Objects': {
                'jungle': {'Type': 'Island Game Area', 'File': 'pvp_jungle', 'Objects': {
                    'locator': {'Type': 'Locator Node'}}}}}}},
            'pvp_jungle.py': {'Objects': {'jungle': {'Type': 'Island Game Area', 'Objects': {
                'spawn1': {'Type': 'Player Spawn Node', 'Spawnables': 'Team 1',
                    'Pos': (1, 2, 3), 'Hpr': (0, 0, 0)},
                'spawn2': {'Type': 'Player Spawn Node', 'Spawnables': 'Team 2',
                    'Pos': (4, 5, 6), 'Hpr': (180, 0, 0)}}}}}}
        instance.air.worldCreator = SimpleNamespace(openFile=lambda name: worlds.get(name))
        instance.loadSpawnPoints()
        self.assertEqual(instance.teamSpawnPts, {
            1: [('jungle', (1, 2, 3, 0))],
            2: [('jungle', (4, 5, 6, 180))]})

    def test_cleanup_removes_game_areas_and_sub_instances(self):
        instance = makeInstance(DistributedPVPTeamBattleAI, [])
        island = SimpleNamespace(requestDelete=Mock())
        gameArea = SimpleNamespace(requestDelete=Mock())
        removed = []
        instance.builder = SimpleNamespace(objectList={1: island, 2: gameArea},
            removeObject=lambda obj: removed.append(obj))

        subArea = SimpleNamespace(requestDelete=Mock())
        subInstance = SimpleNamespace(requestDelete=Mock(),
            builder=SimpleNamespace(objectList={3: subArea}, removeObject=lambda obj: removed.append(obj)))

        instance.getSubInstances = lambda: [subInstance]
        instance.removeSubInstance = Mock()
        instance.requestDelete = Mock()
        instance._DistributedPVPInstanceAI__cleanupInstance(None)

        self.assertEqual(set(map(id, removed)), set(map(id, [island, gameArea, subArea])))
        island.requestDelete.assert_called_once_with()
        gameArea.requestDelete.assert_called_once_with()
        subInstance.requestDelete.assert_called_once_with()
        instance.removeSubInstance.assert_called_once_with(subInstance)
        instance.requestDelete.assert_called_once_with()


class ShipBattleTests(unittest.TestCase):

    def tearDown(self):
        taskMgr.removeTasksMatching('*-9000')

    def test_ship_sunk_scores_for_opponents(self):
        avatars = [FakeAvatar(1), FakeAvatar(2)]
        instance = makeInstance(DistributedPVPShipBattleAI, avatars)
        instance.createTeamShip = Mock()
        instance.sendPlayerToInstance = Mock()
        instance.setupMatch([[1], [2]])
        self.assertEqual(instance.createTeamShip.call_count, 2)
        instance.request('Game')

        ship = SimpleNamespace(doId=600, parentId=1, zoneId=2,
            getDeleteEvent=lambda: 'distObjDelete-600')
        instance.teamShips[1] = ship
        instance.sendPlayerToShip(1)
        instance.sendUpdateToAvatarId.assert_any_call(1, 'setShipDoId', [600])

        instance.handleShipSunk(1, ship)
        self.assertNotIn(1, instance.teamShips)
        self.assertEqual(instance.stats[2][PVPGlobals.SCORE], 1)
        self.assertEqual(instance.stats[1][PVPGlobals.DEATHS], 1)
        self.assertTrue(taskMgr.hasTaskNamed('respawnShip-1-9000'))


class PVPManagerTests(unittest.TestCase):

    def makeManager(self, senderId):
        avatars = [FakeAvatar(1), FakeAvatar(2)]
        for avatar in avatars:
            avatar.world = SimpleNamespace(getType=lambda: PiratesGlobals.INSTANCE_MAIN)

        air = makeAir(avatars, senderId)
        manager = manager_module.PVPManagerAI(air)
        manager.doId = 8000
        manager.sendUpdateToAvatarId = Mock()
        manager.createPVPInstance = Mock()
        return manager

    def tearDown(self):
        taskMgr.removeTasksMatching('challenge-*')

    def test_challenge_and_accept(self):
        manager = self.makeManager(1)
        manager.requestChallenge(2)
        manager.sendUpdateToAvatarId.assert_called_once_with(2, 'challengeFrom', [1])
        self.assertTrue(manager.hasChallenge(1, 2))

        manager.air.senderId = 2
        manager.acceptChallenge(1)
        self.assertFalse(manager.hasChallenge(1, 2))
        manager.sendUpdateToAvatarId.assert_any_call(1, 'challengeAccepted', [2])
        manager.sendUpdateToAvatarId.assert_any_call(2, 'challengeAccepted', [1])
        manager.createPVPInstance.assert_called_once_with(manager.ChallengeGameStyle, [[1], [2]])

    def test_challenge_brings_crews(self):
        manager = self.makeManager(1)
        mainWorld = manager.air.doId2do[1].world
        crew = [FakeAvatar(3), FakeAvatar(4), FakeAvatar(5), FakeAvatar(6)]
        for avatar in crew:
            avatar.world = mainWorld
            manager.air.doId2do[avatar.doId] = avatar

        manager.air.doId2do[1].bandId = (100, 1)
        crew[0].bandId = (100, 1)
        crew[1].bandId = (100, 1)
        manager.air.doId2do[2].bandId = (100, 2)
        crew[2].bandId = (100, 2)

        # crew members already in a pvp match or teleporting stay behind
        crew[1].world = SimpleNamespace(getType=lambda: PiratesGlobals.INSTANCE_PVP)
        manager.air.teleportMgr.avatar2fsm[5] = object()

        manager.requestChallenge(2)
        manager.air.senderId = 2
        manager.acceptChallenge(1)
        manager.createPVPInstance.assert_called_once_with(manager.ChallengeGameStyle, [[1, 3], [2]])

    def test_challenge_within_crew_only_brings_the_two_players(self):
        manager = self.makeManager(1)
        crewmate = FakeAvatar(3)
        crewmate.world = manager.air.doId2do[1].world
        manager.air.doId2do[3] = crewmate
        for avatarId in (1, 2, 3):
            manager.air.doId2do[avatarId].bandId = (100, 1)

        manager.requestChallenge(2)
        manager.air.senderId = 2
        manager.acceptChallenge(1)
        manager.createPVPInstance.assert_called_once_with(manager.ChallengeGameStyle, [[1], [2]])

    def test_accept_without_challenge_is_rejected(self):
        manager = self.makeManager(2)
        manager.acceptChallenge(1)
        manager.air.logPotentialHacker.assert_called_once()
        manager.createPVPInstance.assert_not_called()

    def test_cannot_challenge_self_or_players_in_pvp(self):
        manager = self.makeManager(1)
        manager.requestChallenge(1)
        manager.air.doId2do[2].world = SimpleNamespace(getType=lambda: PiratesGlobals.INSTANCE_PVP)
        manager.requestChallenge(2)
        manager.sendUpdateToAvatarId.assert_not_called()

    def test_world_classes_cover_game_styles(self):
        for gameStyle, worldFiles in list(manager_module.PVPGameStyleWorlds.items()):
            for worldFile in worldFiles:
                self.assertIn(worldFile, manager_module.PVPWorldClasses)


class CTLTests(unittest.TestCase):

    def makeGame(self):
        avatars = [FakeAvatar(1), FakeAvatar(2)]
        avatars[0].pvpTeam = 1
        avatars[1].pvpTeam = 2
        air = makeAir(avatars)
        game = PVPGameCTLAI(air)
        game.doId = 9100
        game.sendUpdate = Mock()
        game.sendUpdateToAvatarId = Mock()
        game.maxTeamScore = 5
        banks = []
        for team in (1, 2):
            bank = DistributedBankAI(air)
            bank.doId = 9200 + team
            bank.sendUpdate = Mock()
            bank.sendUpdateToAvatarId = Mock()
            bank.setBelongsToTeam(team)
            bank.setValue(10)
            game.addBank(bank)
            banks.append(bank)

        for avatar in avatars:
            game.addPlayer(avatar.doId)

        game.request('Game')
        return game, avatars, banks

    def tearDown(self):
        taskMgr.removeTasksMatching('*-92*')
        taskMgr.removeTasksMatching('*-9100')

    def test_bank_interaction_rules(self):
        game, avatars, banks = self.makeGame()
        self.assertEqual(banks[0].handleRequestInteraction(avatars[0], 0, False), banks[0].DENY)
        self.assertEqual(banks[1].handleRequestInteraction(avatars[0], 0, False), banks[1].ACCEPT)
        game.setLootCarried(1, game.getMaxCarry())
        self.assertEqual(banks[1].handleRequestInteraction(avatars[0], 0, False), banks[1].DENY)

    def test_steal_and_deposit(self):
        game, avatars, banks = self.makeGame()
        self.assertEqual(game.addLoot(1, 3), 3)
        banks[1].b_setValue(7)
        self.assertEqual(avatars[0].lootCarried, (3, game.getMaxCarry()))

        game.air.senderId = 1
        game.treasureDeposited(banks[1].doId)
        game.air.logPotentialHacker.assert_called_once()
        self.assertEqual(game.getLootCarried(1), 3)

        game.treasureDeposited(banks[0].doId)
        self.assertEqual(game.getLootCarried(1), 0)
        self.assertEqual(banks[0].getValue(), 13)
        self.assertEqual(game.getPlayerStat(1, PVPGlobals.SCORE), 3)
        self.assertEqual(game.state, 'ScoreScreen')

    def test_drop_returns_treasure(self):
        game, avatars, banks = self.makeGame()
        game.addLoot(1, 4)
        game.air.senderId = 1
        game.requestDropTreasure()
        self.assertEqual(game.getLootCarried(1), 0)
        self.assertEqual(banks[1].getValue(), 14)


class PirateerTests(unittest.TestCase):

    def test_load_and_capture_coin(self):
        avatar = FakeAvatar(1)
        ship = SimpleNamespace(doId=500, getPVPTeam=lambda: 1)
        air = makeAir([avatar], senderId=1)
        air.doId2do[500] = ship
        game = PVPGamePirateerAI(air)
        game.doId = 9300
        game.sendUpdate = Mock()
        game.sendUpdateToAvatarId = Mock()
        game.maxTeamScore = 1
        wreck = DistributedWreckAI(air)
        wreck.doId = 9400
        wreck.sendUpdate = Mock()
        wreck.setValue(2)
        game.addWreck(wreck)
        game.addPlayer(1)
        game.request('Game')

        game.lootWreck(9400, 500)
        self.assertIn(500, game.loading)
        for i in range(game.LoadSteps):
            game._PVPGamePirateerAI__loadTask(500, SimpleNamespace())

        self.assertEqual(wreck.getValue(), 1)
        self.assertEqual(game.coinCarriers, [500])
        game.sendUpdate.assert_any_call('displayCoins', [[500]])

        game.portEntered('Team 2', 500)
        self.assertEqual(game.coinCarriers, [500])
        game.portEntered('Team 1', 500)
        game.sendUpdate.assert_any_call('coinCaptured', [500])
        self.assertEqual(game.teamScores, {1: 1})
        self.assertEqual(game.state, 'ScoreScreen')
        taskMgr.removeTasksMatching('*-9300')


class ScoreboardTests(unittest.TestCase):

    def test_scores_and_stats(self):
        scoreboard = ScoreboardAI(SimpleNamespace(dclassesByName=collections.defaultdict(MagicMock)))
        scoreboard.doId = 9500
        scoreboard.sendUpdate = Mock()
        scoreboard.setStats([PVPGlobals.KILLS])
        scoreboard.addScore(10, 'Ship', 1)
        scoreboard.addToScore(10, 5)
        scoreboard.addToStat(10, PVPGlobals.KILLS, 2)
        self.assertEqual(scoreboard.getScores(),
            [[10, 'Ship', 5, 1, PVPGlobals.SHIP_SCORE, [[PVPGlobals.KILLS, 2]]]])
        scoreboard.sendUpdate.assert_any_call('setScore', [10, 5])
        scoreboard.sendUpdate.assert_any_call('setStat', [10, PVPGlobals.KILLS, 2])
        self.assertEqual(scoreboard.getTeamScore(1), 5)


if __name__ == '__main__':
    unittest.main()
