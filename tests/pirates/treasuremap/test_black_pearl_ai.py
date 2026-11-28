import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import ANY, Mock, call, patch

from panda3d.core import NodePath, loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

from direct.task import Task
from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.ai import AIInterestHandles
from otp.ai import Barrier
from pirates.piratesbase import PiratesGlobals
from pirates.quest.QuestEvent import BossBattleCompleted
from pirates.quest.QuestTaskDNA import BossBattleTaskDNA
from pirates.quest.QuestTaskState import QuestTaskState
from pirates.treasuremap.DistributedTreasureMapAI import DistributedTreasureMapAI
from pirates.treasuremap.TreasureMapBlackPearlAI import TreasureMapBlackPearlAI
from pirates.treasuremap import TreasureMapBlackPearlWorldBuilderAI as builder_module
from pirates.ship.BlackPearlShipAI import BlackPearlShipAI
from pirates.ship import ShipBalance
from pirates.world.ClientAreaBuilderAI import ClientAreaBuilderAI
from pirates.world.DistributedFortAI import DistributedFortAI
from pirates.world import WorldGlobals
from pirates.world.WorldCreator import WorldCreator


class BlackPearlAITests(unittest.TestCase):
    def make_instance(self):
        instance = TreasureMapBlackPearlAI.__new__(TreasureMapBlackPearlAI)
        instance.doId = 100
        instance.state = 'Off'
        instance.participants = []
        instance.arrivedParticipants = set()
        instance.readyAvatars = []
        instance.cutsceneEndedAvatars = set()
        instance.cutsceneFinished = False
        instance.blackPearlInterests = {}
        instance.blackPearl = SimpleNamespace(zoneId=2400)
        instance.goliath = SimpleNamespace(zoneId=2500)
        instance.attackShips = [SimpleNamespace(zoneId=2600)]
        instance.forts = {'fort': SimpleNamespace(zoneId=600)}
        instance._getBlackPearlIsland = lambda: SimpleNamespace(doId=300)
        instance.isReady = True
        instance.readyBarrier = None
        instance.oceanGrid = SimpleNamespace(doId=200)
        instance.air = SimpleNamespace(
            doId2do={}, clientAddInterestMultiple=Mock(), clientRemoveInterest=Mock())
        instance.uniqueName = lambda name: name
        return instance

    def test_map_start_uses_existing_style_table(self):
        avatar = SimpleNamespace(doId=42)
        treasure_map = DistributedTreasureMapAI.__new__(DistributedTreasureMapAI)
        treasure_map.ownerId = 42
        treasure_map.air = SimpleNamespace(
            getAvatarIdFromSender=lambda: 42, doId2do={42: avatar})
        treasure_map.mapId = PiratesGlobals.GAME_STYLE_TM_BLACK_PEARL
        treasure_map.isEnabled = 1
        treasure_map.participants = []
        treasure_map.startPending = False
        treasure_map.activeInstance = None
        treasure_map._createTreasureMapInstance = Mock()
        treasure_map.requestStart(5)
        treasure_map._createTreasureMapInstance.assert_called_once_with(
            avatar, 'BlackpearlWorld')

    def make_created_instance(self, teleportResult=True):
        avatar = SimpleNamespace(doId=42)
        island = SimpleNamespace(getUniqueId=lambda: 'island')
        instance = SimpleNamespace(
            doId=100, isReady=False, pendingTeleportCallbacks=[],
            addParticipant=Mock(), removeParticipant=Mock(),
            builder=SimpleNamespace(getIslands=lambda: [island]),
            getSpawnPt=lambda uid, index: (1, 2, 3, 4),
            getType=lambda: PiratesGlobals.INSTANCE_TM,
            getFileName=lambda: 'BlackpearlWorld')
        air = SimpleNamespace(doId2do={42: avatar, 100: instance},
                              teleportMgr=SimpleNamespace(
                                  d_initiateTeleport=Mock(return_value=teleportResult)))
        treasure_map = DistributedTreasureMapAI.__new__(DistributedTreasureMapAI)
        treasure_map.doId = 99
        treasure_map.air = air
        treasure_map.participants = []
        return avatar, instance, air, treasure_map

    def test_instance_teleport_waits_for_world_setup(self):
        avatar, instance, air, treasure_map = self.make_created_instance()
        treasure_map._onInstanceCreated(100, avatar)
        air.teleportMgr.d_initiateTeleport.assert_not_called()
        instance.pendingTeleportCallbacks.pop()()
        air.teleportMgr.d_initiateTeleport.assert_called_once_with(
            avatar, instanceType=PiratesGlobals.INSTANCE_TM,
            instanceName='BlackpearlWorld', locationUid='island',
            spawnPt=(1, 2, 3, 4), targetWorld=instance)
        instance.addParticipant.assert_called_once_with(42)
        instance.removeParticipant.assert_not_called()

    def test_failed_instance_teleport_removes_participant(self):
        avatar, instance, air, treasure_map = self.make_created_instance(teleportResult=False)
        instance.isReady = True
        treasure_map._onInstanceCreated(100, avatar)
        air.teleportMgr.d_initiateTeleport.assert_called_once()
        instance.removeParticipant.assert_called_once_with(42)

    def test_ships_are_kept_out_of_interest_until_the_cutscene_ends(self):
        instance = self.make_instance()
        instance.air.doId2do[42] = SimpleNamespace(
            GetPuppetConnectionChannel=lambda avatar_id: avatar_id + 1000)
        instance.participants = [42]
        instance.readyAvatars = [42]
        instance.state = 'StageOne'
        instance._addBlackPearlInterestForAllParticipants()
        instance.air.clientAddInterestMultiple.assert_not_called()
        instance.cutsceneFinished = True
        instance._addBlackPearlInterestForAllParticipants()
        instance.air.clientAddInterestMultiple.assert_any_call(
            1042, AIInterestHandles.PIRATES_TREASUREMAP, 200, (2400, 2500, 2600), False)

    def test_interest_is_reserved_idempotent_and_removed(self):
        instance = self.make_instance()
        instance.cutsceneFinished = True
        avatar = SimpleNamespace(GetPuppetConnectionChannel=lambda avatar_id: avatar_id + 1000)
        instance.air.doId2do[42] = avatar
        instance.readyAvatars = [42]
        instance.addParticipant(42)
        instance.addParticipant(42)
        instance.air.clientAddInterestMultiple.assert_any_call(
            1042, AIInterestHandles.PIRATES_TREASUREMAP, 200, (2400, 2500, 2600), False)
        instance.air.clientAddInterestMultiple.assert_any_call(
            1042, AIInterestHandles.PIRATES_TREASUREMAP_FORTS, 300, (600,), False)
        self.assertEqual(instance.air.clientAddInterestMultiple.call_count, 2)
        instance.blackPearl.zoneId = 2401
        instance._addBlackPearlInterestForAllParticipants()
        instance.air.clientAddInterestMultiple.assert_called_with(
            1042, AIInterestHandles.PIRATES_TREASUREMAP, 200, (2401, 2500, 2600), False)
        instance.removeParticipant(42)
        instance.air.clientRemoveInterest.assert_any_call(
            1042, AIInterestHandles.PIRATES_TREASUREMAP, False)
        instance.air.clientRemoveInterest.assert_any_call(
            1042, AIInterestHandles.PIRATES_TREASUREMAP_FORTS, False)
        self.assertEqual(instance.air.clientRemoveInterest.call_count, 2)
        self.assertEqual(instance.blackPearlInterests, {})

    def test_interests_wait_for_ready_and_remove_empty_fort_interest(self):
        instance = self.make_instance()
        instance.cutsceneFinished = True
        instance.air.doId2do[42] = SimpleNamespace(
            GetPuppetConnectionChannel=lambda avatar_id: avatar_id + 1000)
        instance.addParticipant(42)
        instance._addBlackPearlInterestForAllParticipants()
        instance.air.clientAddInterestMultiple.assert_not_called()
        instance.readyAvatars = [42]
        instance._addBlackPearlInterestForAllParticipants()
        instance.forts = {}
        instance._addBlackPearlInterestForAllParticipants()
        instance.air.clientRemoveInterest.assert_called_once_with(
            1042, AIInterestHandles.PIRATES_TREASUREMAP_FORTS, False)
        instance.removeParticipant(42)
        self.assertEqual(instance.air.clientRemoveInterest.call_count, 2)

    def test_disconnected_participant_is_removed_on_interest_refresh(self):
        instance = self.make_instance()
        instance.participants = [42]
        instance.readyAvatars = [42]
        instance.blackPearlInterests = {42: ((2400,), (600,))}
        instance._addBlackPearlInterestForAllParticipants()
        self.assertEqual(instance.participants, [])
        self.assertEqual(instance.readyAvatars, [])
        self.assertEqual(instance.blackPearlInterests, {})

    def test_cutscene_waits_for_each_participant_once(self):
        instance = self.make_instance()
        instance.state = 'StageOne'
        instance.participants = [1, 2]
        sender = [1]
        instance.air.getAvatarIdFromSender = lambda: sender[0]
        instance.d_endCutscene = Mock()
        instance.d_displayCutsceneMessage = Mock()
        with patch.object(builtins, 'taskMgr') as tasks:
            instance.requestEndCutscene()
            instance.requestEndCutscene()
            instance.d_endCutscene.assert_not_called()
            # the avatar waits on the crew, the crew still watching is told so once...
            self.assertEqual(instance.d_displayCutsceneMessage.mock_calls, [call(1, 1), call(2, 0)])
            sender[0] = 3
            instance.requestEndCutscene()
            instance.d_endCutscene.assert_not_called()
            sender[0] = 2
            instance.requestEndCutscene()
            instance.requestEndCutscene()
            instance.d_endCutscene.assert_called_once_with()
            tasks.remove.assert_any_call('cutsceneTimeout')

    def test_wait_clients_uses_client_ready_barrier(self):
        instance = self.make_instance()
        instance.state = 'WaitClientsReady'
        instance.participants = [1, 2]
        instance.arrivedParticipants = {1, 2}
        instance.readyBarrier = None
        instance.beginBarrier = Mock(return_value=4)
        task = SimpleNamespace(done=Task.done, again=Task.again)
        self.assertEqual(instance._waitClientsReadyTimeout(task), Task.done)
        instance.beginBarrier.assert_called_once_with(
            'allAvatarsReady', [1, 2], instance.CUTSCENE_WAIT_TIME,
            instance._clientsReady)
        instance.d_setAllPlayersReady = Mock()
        instance.b_setState = Mock()
        instance._addBlackPearlInterestForAllParticipants = Mock()
        instance._clientsReady([1, 2])
        instance.d_setAllPlayersReady.assert_called_once_with(1)
        instance.b_setState.assert_called_once_with('StageOne')

    def test_real_client_ready_barrier_serializes_name_and_waits_for_avatars(self):
        sender = [1]
        air = SimpleNamespace(
            dclassesByName={'TreasureMapBlackPearlAI': None},
            getAvatarIdFromSender=lambda: sender[0])
        instance = TreasureMapBlackPearlAI.__new__(TreasureMapBlackPearlAI)
        DistributedObjectAI.__init__(instance, air)
        instance.doId = 100
        instance.state = 'WaitClientsReady'
        instance.participants = [1, 2]
        instance.arrivedParticipants = {1, 2}
        instance.readyBarrier = None
        instance.sendUpdate = Mock()
        instance._addBlackPearlInterestForAllParticipants = Mock()
        instance.b_setState = Mock()
        instance._waitClientsReadyTimeout(None)
        context = instance.readyBarrier
        self.addCleanup(instance.ignoreBarrier, context)
        instance.sendUpdate.assert_called_once_with(
            'setBarrierData', [[(context, 'allAvatarsReady-100', [1, 2])]])
        client = DistributedObject(SimpleNamespace(isLocalId=lambda avId: avId == sender[0]))
        client.doId = 100
        client.sendUpdate = lambda name, args: instance.setBarrierReady(*args)
        data = instance.getBarrierData()
        client.setBarrierData(data)
        client.doneBarrier(client.uniqueName('allAvatarsReady'))
        client.doneBarrier(client.uniqueName('allAvatarsReady'))
        instance.b_setState.assert_not_called()
        sender[0] = 2
        client.setBarrierData(data)
        client.doneBarrier(client.uniqueName('allAvatarsReady'))
        self.assertEqual(instance.readyAvatars, [1, 2])
        instance.b_setState.assert_called_once_with('StageOne')
        self.assertEqual(instance.getBarrierData(), [])

    def test_wait_clients_does_not_start_without_participants(self):
        instance = self.make_instance()
        instance.state = 'WaitClientsReady'
        instance.beginBarrier = Mock()
        task = SimpleNamespace(done=Task.done, again=Task.again)
        self.assertEqual(instance._waitClientsReadyTimeout(task), Task.again)
        instance.beginBarrier.assert_not_called()

    def test_barrier_waits_for_teleport_completion(self):
        instance = self.make_instance()
        instance.state = 'WaitClientsReady'
        instance.participants = [1, 2]
        instance.arrivedParticipants = set()
        instance.readyBarrier = None
        instance.beginBarrier = Mock(return_value=4)
        task = SimpleNamespace(again=Task.again)
        self.assertEqual(instance._waitClientsReadyTimeout(task), Task.again)
        instance._participantArrived(1)
        instance.beginBarrier.assert_not_called()
        instance._participantArrived(2)
        instance.beginBarrier.assert_called_once_with(
            'allAvatarsReady', [1, 2], instance.CUTSCENE_WAIT_TIME,
            instance._clientsReady)

    def test_participant_teleport_event_starts_barrier_once(self):
        instance = self.make_instance()
        instance.state = 'WaitClientsReady'
        instance.beginBarrier = Mock(return_value=4)
        instance.addParticipant(42)
        instance.addParticipant(42)
        self.addCleanup(instance.ignore, 'teleportDone-42')
        builtins.messenger.send('teleportDone-42')
        builtins.messenger.send('teleportDone-42')
        instance.beginBarrier.assert_called_once_with(
            'allAvatarsReady', [42], instance.CUTSCENE_WAIT_TIME,
            instance._clientsReady)

    def test_pier_cutscene_origin_preserves_authored_transform(self):
        area = NodePath('island')
        pier = area.attachNewNode('pier')
        pier.setPosHpr(239.051, -407.882, 0.241, 124.702, 0, 0)
        origins = {}
        cr = SimpleNamespace(
            uidMgr=SimpleNamespace(getDoId=lambda uid: 3),
            doId2do={3: area},
            activeWorld=SimpleNamespace(addCutsceneOriginNode=lambda node, name: origins.update({name: node})))
        creator = WorldCreator(cr, None, None)
        data = {
            'Type': 'Cutscene Origin Node',
            'CutsceneId': '3.1: Sneaking to BlackPearl',
            'Pos': (-26.381, 1.027, 1.0),
            'Hpr': (-3.812, 0, 0),
        }
        with patch.object(builtins.base, 'cr', cr, create=True):
            creator.createObject(data, area, 'island', 'origin', 0,
                                 actualParentObj=pier)
        origin = origins[data['CutsceneId']]
        self.assertAlmostEqual(origin.getX(area), 253.226, places=2)
        self.assertAlmostEqual(origin.getY(area), -430.155, places=2)
        self.assertAlmostEqual(origin.getH(area), 120.89, places=2)
        pier.flattenStrong()
        self.assertFalse(origin.isEmpty())
        self.assertAlmostEqual(origin.getX(area), 253.226, places=2)

    def test_barrier_timeout_reports_only_ready_avatars(self):
        done = Mock()
        with patch.object(Barrier, 'taskMgr') as tasks:
            barrier = Barrier.Barrier('name', 'task', [1, 2], 60, done)
            barrier.clear(1)
            barrier.clear(1)
            barrier.clear(3)
            self.assertEqual(barrier._timedOut(None), Task.done)
            done.assert_called_once_with([1])
            barrier._timedOut(None)
            done.assert_called_once()
            tasks.remove.assert_called_with('task')

    def test_cancelled_barrier_never_calls_completion(self):
        done = Mock()
        with patch.object(Barrier, 'taskMgr') as tasks:
            barrier = Barrier.Barrier('name', 'task', [1], 60, done)
            barrier.cleanup()
            barrier.clear(1)
            done.assert_not_called()
            tasks.remove.assert_called_with('task')

    def test_guard_death_is_checked_after_health_update(self):
        instance = self.make_instance()
        guard = SimpleNamespace(doId=77, getHp=Mock(return_value=[10, False]))
        instance.navyGuards = [guard]
        instance.deadNavyGuards = []
        instance.navyGuardsKilled = 0
        instance.NUM_NAVY_GUARDS = 1
        instance.shipCaptured = True
        instance.state = 'StageOne'
        instance.npcsKilled = False
        instance.blackPearl = SimpleNamespace(removeNPCOnDeck=Mock())
        instance.d_handleNPCsKilled = Mock()
        instance._checkStageOneComplete = Mock()
        with patch.object(builtins, 'taskMgr') as tasks:
            instance.processDeath()
            self.assertEqual(instance.navyGuardsKilled, 0)
            guard.getHp.return_value = [0, False]
            callback = tasks.doMethodLater.call_args.args[1]
            callback(SimpleNamespace(done=Task.done))
            callback(SimpleNamespace(done=Task.done))
        self.assertEqual(instance.navyGuardsKilled, 1)
        instance.blackPearl.removeNPCOnDeck.assert_called_once_with(77)
        instance.d_handleNPCsKilled.assert_called_once_with()
        instance._checkStageOneComplete.assert_called_once_with()
        self.assertEqual(instance.deadNavyGuards, [guard])

    def test_attack_ship_sink_is_counted_once(self):
        instance = self.make_instance()
        instance.attackShipIds = [10, 11]
        instance.sunkAttackShipIds = set()
        instance.attackShipsSunk = 0
        instance.d_handleAttackShipSunk = Mock()
        instance._allAttackShipsDestroyed = Mock()
        instance.handleAttackShipDestroyed(10)
        instance.handleAttackShipDestroyed(10)
        instance.handleAttackShipDestroyed(99)
        instance._allAttackShipsDestroyed.assert_not_called()
        instance.handleAttackShipDestroyed(11)
        self.assertEqual(instance.attackShipsSunk, 2)
        self.assertEqual(instance.d_handleAttackShipSunk.call_count, 2)
        instance._allAttackShipsDestroyed.assert_called_once_with()

    def test_victory_dispatches_correct_quest_event_and_result_shape(self):
        instance = self.make_instance()
        avatar = SimpleNamespace(doId=42)
        instance.participants = [42]
        instance.air.doId2do[42] = avatar
        instance.air.questMgr = SimpleNamespace(completeTaskState=Mock())
        instance.sendUpdateToAvatarId = Mock()
        with patch.object(builtins, 'taskMgr'):
            instance.enterReward()
        arguments = instance.air.questMgr.completeTaskState.call_args.args
        self.assertIs(arguments[0], avatar)
        self.assertIsInstance(arguments[1], BossBattleCompleted)
        self.assertEqual(arguments[1].getTreasureMapId(),
                         PiratesGlobals.GAME_STYLE_TM_BLACK_PEARL)
        task_dna = BossBattleTaskDNA(treasureMapId=PiratesGlobals.GAME_STYLE_TM_BLACK_PEARL)
        task_state = QuestTaskState(goal=1)
        task_state.acquire()
        self.assertTrue(arguments[1].applyTo(task_state, task_dna))
        arguments[1].complete(task_state, task_dna)
        self.assertTrue(task_state.isComplete())
        instance.sendUpdateToAvatarId.assert_called_once_with(
            42, 'setTMComplete', [[], []])

    def make_pearl(self):
        ship = BlackPearlShipAI.__new__(BlackPearlShipAI)
        ship.air = SimpleNamespace(doId2do={})
        ship.hp = 100
        ship.maxHp = 100
        ship.hasSpawnBuff = lambda: False
        ship.isSailable = lambda: True
        ship.b_setHp = ship.setHp
        return ship

    def test_pearl_damage_accepts_broadside_signature(self):
        ship = self.make_pearl()
        ship.handleHpDepleted = Mock()
        ship.gameFSM = SimpleNamespace(onDamageReceived=Mock())
        with patch.object(ShipBalance.ArmorAbsorb, 'getValue', return_value=0), \
                patch.object(ShipBalance.NPCArmorModifier, 'getValue', return_value=0):
            self.assertEqual(ship.takeDamage(40, 23, applyModifiers=False), 60)
            self.assertEqual(ship.takeDamage(60, 23, applyModifiers=False), 0)
        ship.handleHpDepleted.assert_called_once_with()

    def test_sunk_pearl_reports_defeat_and_is_kept(self):
        ship = self.make_pearl()
        ship.questInstance = SimpleNamespace(handleBlackPearlDestroyed=Mock())
        ship.b_setGameState = Mock()
        ship.handleShipSinking = Mock()
        ship.requestDelete = Mock()
        ship.handleHpDepleted()
        ship.b_setGameState.assert_called_once_with('Sinking', 0)
        ship.questInstance.handleBlackPearlDestroyed.assert_called_once_with()

        ship.handleShipSunk()
        ship.b_setGameState.assert_called_with('Sunk', 0)
        ship.requestDelete.assert_not_called()

    def test_pearl_wheel_waits_for_the_guards(self):
        ship = self.make_pearl()
        ship.npcsOnDeck = [1]
        self.assertFalse(ship.canTakeWheel(None))
        ship.npcsOnDeck = []
        self.assertTrue(ship.canTakeWheel(None))
        self.assertTrue(ship.isCrewedByPlayers())

    def test_pearl_damage_applies_npc_modifiers_and_reports_attack(self):
        ship = self.make_pearl()
        ship.gameFSM = SimpleNamespace(onDamageReceived=Mock())
        with patch.object(ShipBalance.NPCDamageIn, 'getValue', return_value=2), \
                patch.object(ShipBalance.ArmorAbsorb, 'getValue', return_value=0.5), \
                patch.object(ShipBalance.NPCArmorModifier, 'getValue', return_value=0.5):
            self.assertEqual(ship.takeDamage(40, 23), 40)
        ship.gameFSM.onDamageReceived.assert_called_once_with(23, 60)

    def test_fort_required_fields_are_set_before_generation(self):
        fort = Mock()
        fort.getFortLevel.return_value = 1
        fort.getMaxHp.return_value = 5000
        fort.getHp.return_value = [5000, False]
        fort.doId = 321
        island = SimpleNamespace(doId=20, getZoneFromXYZ=lambda pos: 600,
                                 generateChildWithRequired=Mock())
        island.generateChildWithRequired.side_effect = lambda obj, zone: (
            fort.setIslandId.assert_called_once_with(20),
            fort.setLevel.assert_called_once_with(1))
        builder = builder_module.TreasureMapBlackPearlWorldBuilderAI.__new__(
            builder_module.TreasureMapBlackPearlWorldBuilderAI)
        builder.air = SimpleNamespace(uidMgr=SimpleNamespace(addUid=Mock()))
        builder.island = island
        builder.treasureMapInstance = None
        builder.forts = {}
        builder.wantFortCannons = False
        with patch.object(builder_module, 'DistributedFortAI', return_value=fort):
            builder._createSimpleFort('fort', {'CreateObject': True})
        island.generateChildWithRequired.assert_called_once_with(fort, 600)

    def test_world_builder_cleanup_only_removes_uids_still_owned_by_objects(self):
        old_fort = Mock(doId=20)
        owned_fort = Mock(doId=10)
        old_cannon = Mock(doId=21)
        old_cannon.getUniqueId.return_value = 'cannon-old'
        owned_cannon = Mock(doId=11)
        owned_cannon.getUniqueId.return_value = 'cannon-owned'
        uid_map = {
            'fort-old': 200,
            'fort-owned': owned_fort.doId,
            'cannon-old': 201,
            'cannon-owned': owned_cannon.doId,
        }
        uid_mgr = SimpleNamespace(
            getDoId=lambda uid: uid_map.get(uid),
            removeUid=Mock())
        builder = builder_module.TreasureMapBlackPearlWorldBuilderAI.__new__(
            builder_module.TreasureMapBlackPearlWorldBuilderAI)
        builder.air = SimpleNamespace(
            doId2do={obj.doId: obj for obj in
                     (old_fort, owned_fort, old_cannon, owned_cannon)},
            uidMgr=uid_mgr)
        builder.forts = {'fort-old': old_fort, 'fort-owned': owned_fort}
        builder.fortCannons = {'fort': [old_cannon, owned_cannon]}
        builder.cutsceneNodes = {}
        builder.piers = {}

        builder.cleanup()

        self.assertEqual(
            uid_mgr.removeUid.call_args_list,
            [call('cannon-owned'), call('fort-owned')])
        for obj in (old_fort, owned_fort, old_cannon, owned_cannon):
            obj.requestDelete.assert_called_once_with()
        self.assertEqual(builder.forts, {})
        self.assertEqual(builder.fortCannons, {})

    def test_fort_projectile_uses_dc_arguments_and_sender(self):
        fort = DistributedFortAI.__new__(DistributedFortAI)
        fort.destroyed = False
        fort.air = SimpleNamespace(getAvatarIdFromSender=lambda: 42, doId2do={})
        fort.takeDamage = Mock()
        fort.hitByProjectile(1, 2)
        fort.takeDamage.assert_called_once_with(ANY, 42)

    def test_shared_fort_opens_each_destroyed_pair_only_when_both_forts_fall(self):
        instance = SimpleNamespace(handleBarricadeDestroyed=Mock())
        fort = DistributedFortAI.__new__(DistributedFortAI)
        fort.objKey = '1175907906.7kmuller'
        fort.destroyed = False
        fort.cannons = []
        fort.stopAttacking = Mock()
        fort.treasureMapInstance = instance
        first = SimpleNamespace(isDestroyed=lambda: True)
        second = SimpleNamespace(isDestroyed=lambda: False)
        instance.forts = {
            '1175905981.42kmuller': first,
            fort.objKey: fort,
            '1171851678.08sdnaik': second}
        fort._handleDestroyed(42)
        instance.handleBarricadeDestroyed.assert_called_once_with(0)

    def test_treasure_map_island_uses_bounded_interest_zones(self):
        island = Mock()
        island.doId = 20
        island.getUniqueId.return_value = 'island'
        data = {
            'Visual': {'Model': 'island'},
            'Objects': {'lod': {'Type': 'LOD Sphere',
                                'Pos': (0, 0, 0),
                                'Radi': [9000, 25000, 40000]}}}
        parent = SimpleNamespace(
            getType=lambda: PiratesGlobals.INSTANCE_TM,
            generateChildWithRequired=Mock())
        creator = SimpleNamespace(
            getIslandWorldDataByUid=lambda uid: data,
            linkManager=SimpleNamespace(registerLinkData=Mock()),
            movementLinkManager=SimpleNamespace(registerMovementLinkData=Mock()))
        builder = ClientAreaBuilderAI(
            SimpleNamespace(worldCreator=creator,
                            uidMgr=SimpleNamespace(addUid=Mock())), parent)
        def verify_grid(*args):
            self.assertEqual(island.cellWidth, WorldGlobals.ISLAND_TM_CELL_SIZE)
            self.assertEqual(island.gridRadius, WorldGlobals.ISLAND_TM_GRID_RADIUS)
        island.setZoneSphereSize.side_effect = verify_grid
        with patch('pirates.world.DistributedIslandAI.DistributedIslandAI',
                   return_value=island):
            builder.createIsland({}, parent, '', 'island', False)
        island.setZoneSphereSize.assert_called_once()


if __name__ == '__main__':
    unittest.main()
