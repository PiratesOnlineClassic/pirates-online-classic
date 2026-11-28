import builtins
import math
import importlib.abc
import importlib.machinery
import pickle
import sys
import unittest
import zlib
from types import SimpleNamespace
from unittest.mock import ANY, MagicMock, Mock, patch

from direct.showbase.DirectObject import DirectObject
from panda3d.core import (ExecutionEnvironment, NodePath, Point3, Filename, VirtualFileMountRamdisk,
                          VirtualFileSystem, loadPrcFile, loadPrcFileData)

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')


def _bootstrapGameResources():
    # the game resources are not available in the test environment, so provide an
    # empty WeaponGlobals table and stub out the client-only native modules...
    if 'pirates.battle.WeaponGlobals' not in sys.modules:
        vfs = VirtualFileSystem.getGlobalPtr()
        vfs.mount(VirtualFileMountRamdisk(), Filename('/ship_test_stub'), 0)
        vfs.writeFile(Filename('/ship_test_stub/WeaponGlobals.pkl'),
            zlib.compress(pickle.dumps({'columnHeadings': {}})), False)
        cwd = ExecutionEnvironment.getCwd()
        vfs.chdir(Filename('/ship_test_stub'))
        try:
            import pirates.battle.WeaponGlobals
        finally:
            vfs.chdir(cwd)

    class _NativeStubFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):

        def find_spec(self, fullname, path, target=None):
            if fullname == 'libotp' or fullname.startswith('libotp.'):
                return importlib.machinery.ModuleSpec(fullname, self, is_package=True)

        def create_module(self, spec):
            module = MagicMock()
            module.__path__ = []
            module.__spec__ = spec
            return module

        def exec_module(self, module):
            pass

    if not any(type(finder).__name__ == '_NativeStubFinder' for finder in sys.meta_path):
        sys.meta_path.insert(0, _NativeStubFinder())

    if not hasattr(builtins, 'base'):
        from direct.showbase.ShowBase import ShowBase
        ShowBase(windowType='none')

    from direct.showbase import Loader
    for name in ('loadFont', 'loadModel', 'loadSfx', 'loadTexture'):
        setattr(Loader.Loader, name, lambda *args, **kwargs: MagicMock())


_bootstrapGameResources()

from pirates.battle import WeaponGlobals
from pirates.battle.DistributedShipBroadsideAI import DistributedShipBroadsideAI
from pirates.battle.DistributedPCCannonAI import DistributedPCCannonAI
from pirates.flag import DistributedFlagAI as flag_module
from pirates.flag.FlagDNA import FlagDNA
from pirates.ship import ShipGlobals
from pirates.ship.DistributedShipAI import DistributedShipAI
from pirates.ship.GameFSMShipAI import GameFSMShipAI
from direct.task import Task
from pirates.ship.NPCShipAI import NPCShipAI
from pirates.ship.PlayerShipAI import PlayerShipAI
from pirates.ship.ShipManagerAI import ShipManagerAI
from pirates.shipparts.DistributedSailAI import DistributedSailAI
from pirates.shipparts.DistributedShipRepairSpotAI import DistributedShipRepairSpotAI
from pirates.uberdog import DistributedShipLoaderAI as loader_ai
from pirates.uberdog import DistributedShipLoaderUD as loader_ud
from pirates.uberdog.UberDogGlobals import InventoryCategory


def makeAir(**kwargs):
    air = SimpleNamespace(doId2do={}, writeServerEvent=Mock(),
        getAvatarIdFromSender=Mock(return_value=0))
    for key, value in kwargs.items():
        setattr(air, key, value)

    return air


def makeShip(cls=PlayerShipAI, doId=1000, air=None, **kwargs):
    ship = cls.__new__(cls)
    NodePath.__init__(ship, 'ship-%d' % doId)
    ship._team = -1
    ship._pvpTeam = 0
    ship._siegeTeam = kwargs.pop('siegeTeam', 0)
    ship.air = air or makeAir()
    ship.doId = doId
    ship.__dict__.update(dict(
        uniqueId='', baseTeam=0, level=0, shipClass=ShipGlobals.INTERCEPTORL1, name='',
        inventoryId=0, npcShip=0, isBoardable=0, isExitable=0, shipInfoId=0, isFlagship=0,
        maxHp=1000, hp=1000, maxSp=500, sp=500, hullCondition=0, maxCargo=0, cargo=[],
        maxCrew=4, crew=[], gameState=['Adrift', 0, 0], badge=[0, 0], isInBoardingPosition=0,
        landedGrapples=[], wishName='', wishNameState='', clientControllerDoId=0, captainId=0,
        deployState=0, skillEffects=[], _skillEffectTasks={}, sinkTimer=[0, 0], repairCount=0,
        flagDNAString=b'', bandId=[0, 0], guildId=0, boardableShipId=0,
        respectDeployBarriers=[False, 0], parentingRules=['', ''], lastAttackerShipId=0,
        attackerDamage={}, cabin=None, bowSprit=None, hull=None, masts=[], sails=[],
        cannons=[], broadside=None, steeringWheel=None, ownerId=0,
        allowCrewState=True, allowFriendState=True, allowGuildState=False,
        allowPublicState=False, siegeBounty=0, lastAttacked=0, pendingRespawnCrew=set(),
        repairSpots=[], skillRechargeTimes={}, pendingBroadsides={}, missionStartTime=0,
        shipKills=0, cannonAttackerIds=set()))
    ship.__dict__.update(kwargs)
    ship.gameFSM = Mock()
    ship.gameFSM.getCurrentOrNextState.return_value = ship.gameState[0]
    ship.sendUpdate = Mock()
    ship.sendUpdateToAvatarId = Mock()
    ship.uniqueName = lambda name: '%s-%d' % (name, ship.doId)
    ship.isGenerated = lambda: True
    ship.air.doId2do[doId] = ship
    return ship


class DistributedShipAITests(unittest.TestCase):

    def test_set_hp_is_clamped_and_sinks_once(self):
        ship = makeShip()
        ship.setHp(5000)
        self.assertEqual(ship.hp, 1000)
        ship.b_setGameState = Mock()
        ship.setHp(-50)
        self.assertEqual(ship.hp, 0)
        ship.b_setGameState.assert_called_once_with('Sinking', 0)
        ship.setHp(0)
        ship.b_setGameState.assert_called_once_with('Sinking', 0)

    def test_sinking_is_announced_with_the_ship(self):
        ship = makeShip()
        ship.b_setGameState = Mock()
        sunk = []
        listener = DirectObject()
        listener.accept(ship.uniqueName('shipSinking'), sunk.append)
        self.addCleanup(listener.ignoreAll)

        ship.setHp(-50)

        self.assertEqual(sunk, [ship])

    def test_damage_tracks_final_blow_and_assist_for_siege(self):
        siegeManager = Mock()
        air = makeAir(siegeManager=siegeManager)
        ship = makeShip(air=air, siegeTeam=1)
        ship.b_setGameState = Mock()
        attacker = makeShip(doId=2000, air=air)
        assist = makeShip(doId=3000, air=air)

        ship.handleShipDamage(-600, assist)
        ship.handleShipDamage(-100, attacker)
        siegeManager.handleShipSunk.assert_not_called()
        ship.handleShipDamage(-500, attacker)

        siegeManager.handleShipSunk.assert_called_once_with(ship, attacker, assist)
        ship.b_setGameState.assert_called_once_with('Sinking', 0)

    def test_damage_ignored_with_spawn_buff_or_while_sinking(self):
        ship = makeShip(skillEffects=[[WeaponGlobals.C_SPAWN, 8, 0, 0]])
        ship.handleShipDamage(-100)
        self.assertEqual(ship.hp, 1000)

        ship = makeShip()
        ship.gameFSM.getCurrentOrNextState.return_value = 'Sinking'
        ship.handleShipDamage(-100)
        self.assertEqual(ship.hp, 1000)

    def test_purchase_repair_all(self):
        inventory = Mock()
        inventory.getGoldInPocket.return_value = 1000
        air = makeAir(inventoryManager=SimpleNamespace(getInventory=lambda avId: inventory))
        ship = makeShip(air=air, captainId=42, hp=500, sp=250)
        ship.air.doId2do[42] = SimpleNamespace(doId=42)
        hull = Mock()
        hull.getMaxArrayHp.return_value = [10, 20]
        ship.hull = hull
        air.getAvatarIdFromSender.return_value = 42

        cost = ship.getRepairCost()
        self.assertGreater(cost, 0)
        ship.purchaseRepairAll()

        inventory.setGoldInPocket.assert_called_once_with(1000 - cost)
        self.assertEqual(ship.hp, 1000)
        self.assertEqual(ship.sp, 500)
        hull.b_setArrayHp.assert_called_once_with([10, 20])
        self.assertEqual(ship.repairCount, 1)

    def test_purchase_repair_all_rejected(self):
        inventory = Mock()
        inventory.getGoldInPocket.return_value = 0
        air = makeAir(inventoryManager=SimpleNamespace(getInventory=lambda avId: inventory))
        ship = makeShip(air=air, captainId=42, hp=500)
        ship.air.doId2do[42] = SimpleNamespace(doId=42)
        ship.air.doId2do[43] = SimpleNamespace(doId=43)

        air.getAvatarIdFromSender.return_value = 43
        ship.purchaseRepairAll()
        air.getAvatarIdFromSender.return_value = 42
        ship.purchaseRepairAll()

        inventory.setGoldInPocket.assert_not_called()
        self.assertEqual(ship.hp, 500)

    def test_ship_ram_requires_ramming_speed(self):
        battleMgr = Mock()
        battleMgr.getModifiedHullDamage.return_value = -200
        air = makeAir(battleMgr=battleMgr)
        ship = makeShip(air=air, clientControllerDoId=42)
        target = makeShip(doId=2000, air=air)
        parent = object()
        ship.getParentObj = target.getParentObj = lambda: parent
        ship.getDistance = lambda other: 100
        air.doId2do[42] = SimpleNamespace(doId=42)
        air.getAvatarIdFromSender.return_value = 42

        ship.requestShipRam(target.doId, [0, 0, 0], 0)
        self.assertEqual(target.hp, 1000)
        air.writeServerEvent.assert_called_once()

        ship.skillEffects = [[WeaponGlobals.C_RAM, 10, 0, 0]]
        ship.requestShipRam(target.doId, [1, 2, 3], 0)
        self.assertEqual(target.hp, 800)
        self.assertFalse(ship.hasSkillEffect(WeaponGlobals.C_RAM))
        target.sendUpdate.assert_any_call('useShipRam', [[1, 2, 3]])
        self.assertEqual(target.lastAttackerShipId, ship.doId)

    def test_request_board_validates_sender(self):
        air = makeAir()
        ship = makeShip(air=air, isBoardable=1)
        avatar = SimpleNamespace(doId=42, getCrewShipId=lambda: 0)
        air.doId2do[42] = avatar
        air.getAvatarIdFromSender.return_value = 42
        ship.d_setMovie = Mock()

        ship.requestBoard(43)
        ship.d_setMovie.assert_not_called()
        ship.requestBoard(42)
        ship.d_setMovie.assert_called_once_with(ShipGlobals.SHIP_MOVIE_BOARD, 42, 0, 0)

    def test_drop_anchor_requires_crew(self):
        air = makeAir()
        ship = makeShip(air=air)
        air.doId2do[42] = SimpleNamespace(doId=42)
        air.getAvatarIdFromSender.return_value = 42
        ship.d_sendCrewToIsland = Mock()
        ship.dropAnchor(5)
        air.writeServerEvent.assert_called_once()
        ship.d_sendCrewToIsland.assert_not_called()

    def test_relay_teleport_info(self):
        air = makeAir(districtId=77)
        ship = makeShip(air=air)
        world = SimpleNamespace(doId=88)
        ship.getParentObj = lambda: SimpleNamespace(getParentObj=lambda: world)
        ship.relayTeleportInfo()
        ship.sendUpdate.assert_called_once_with('sendTeleportInfo', [77, 88])

    def test_sinking_state_uses_ship_sink_hooks(self):
        ship = makeShip(cls=NPCShipAI)
        ship.getSinkDuration = Mock(return_value=12.0)
        fsm = GameFSMShipAI.__new__(GameFSMShipAI)
        fsm.ship = ship
        fsm._stopAllTasks = Mock()
        with patch.object(builtins, 'taskMgr', Mock(), create=True) as taskMgr:
            fsm.enterSinking()
            delay, callback, name = taskMgr.doMethodLater.call_args[0]

        self.assertEqual(delay, 12.0)
        ship.handleShipSunk = Mock()
        callback(None)
        ship.handleShipSunk.assert_called_once_with()


class PlayerShipAITests(unittest.TestCase):

    def test_sunk_player_ship_is_kept_and_crew_sent_home(self):
        teleportMgr = Mock()
        shipManager = ShipManagerAI.__new__(ShipManagerAI)
        shipManager.playerShips = set()
        air = makeAir(teleportMgr=teleportMgr, shipManager=shipManager)
        ship = makeShip(air=air, crew=[42, 43])
        shipManager.playerShips.add(ship)
        self.assertTrue(shipManager.hasActiveShip(ship.doId))

        island = SimpleNamespace(getUndockable=lambda: 0, getUniqueId=lambda: 'fallback')
        builder = SimpleNamespace(getObject=lambda uniqueId: uniqueId == 'home', getIslands=lambda: [island])
        world = SimpleNamespace(builder=builder)
        ship.getParentObj = lambda: SimpleNamespace(getParentObj=lambda: world)
        air.doId2do[42] = SimpleNamespace(doId=42, getReturnLocation=lambda: 'home')
        air.doId2do[43] = SimpleNamespace(doId=43, getReturnLocation=lambda: 'elsewhere')
        ship.requestDelete = Mock()

        ship.handleShipSunk()

        ship.requestDelete.assert_not_called()
        self.assertEqual(ship.gameState[0], 'Sunk')
        self.assertFalse(shipManager.hasActiveShip(ship.doId))
        teleportMgr.d_initiateTeleport.assert_any_call(air.doId2do[42], locationUid='home', targetWorld=world)
        teleportMgr.d_initiateTeleport.assert_any_call(air.doId2do[43], locationUid='fallback', targetWorld=world)

    def test_attacked_is_broadcast(self):
        ship = makeShip()
        with patch.object(builtins, 'globalClock', Mock(getFrameTime=lambda: 100.0), create=True):
            ship.handleShipDamage(-10)

        ship.sendUpdate.assert_any_call('attacked', [])
        self.assertEqual(ship.lastAttacked, 100.0)
        ship._clearDockTimer()
        self.assertEqual(ship.getAttackTimerRemaining(), 0)

    def test_band_id_follows_captain(self):
        air = makeAir()
        ship = makeShip(air=air)
        ship.accept = Mock()
        ship.ignore = Mock()
        captain = SimpleNamespace(doId=42, getBandId=lambda: (5, 6))
        air.doId2do[42] = captain

        ship.setCaptainId(42)
        ship.accept.assert_called_once_with('bandIdChanged-42', ship._captainBandIdChanged)
        ship.sendUpdate.assert_any_call('setBandId', [5, 6])

        captain.getBandId = lambda: (0, 0)
        ship._captainBandIdChanged(0, 0)
        ship.sendUpdate.assert_any_call('setBandId', [0, 0])

    def test_respawn_waits_for_crew(self):
        ship = makeShip(crew=[42, 43])
        ship.b_setLocation = Mock()
        ship._respawnComplete = Mock()
        ship.respawnShip(10, 20)
        ship.sendUpdateToAvatarId.assert_any_call(42, 'setRespawnLocation', [10, 20])

        ship.air.getAvatarIdFromSender.return_value = 42
        ship.clientReachedRespawnLocation()
        ship._respawnComplete.assert_not_called()
        ship.air.getAvatarIdFromSender.return_value = 43
        ship.clientReachedRespawnLocation()
        ship._respawnComplete.assert_called_once_with()


class ShipPartAITests(unittest.TestCase):

    def test_sail_anim_state_only_from_crew(self):
        air = makeAir()
        ship = makeShip(air=air, crew=[42])
        sail = DistributedSailAI.__new__(DistributedSailAI)
        NodePath.__init__(sail, 'sail')
        sail.air = air
        sail.shipId = ship.doId
        sail.ship = ship
        sail.maxHp = 100
        sail.hp = 100
        sail.animState = ''
        sail.sendUpdate = Mock()
        sail.doId = 5
        air.doId2do[42] = SimpleNamespace(doId=42)
        air.doId2do[43] = SimpleNamespace(doId=43)

        air.getAvatarIdFromSender.return_value = 43
        sail.requestSetAnimState('Idle')
        self.assertEqual(sail.animState, '')
        air.getAvatarIdFromSender.return_value = 42
        sail.requestSetAnimState('Idle')
        self.assertEqual(sail.animState, 'Idle')

        sail.setHp(-5)
        self.assertEqual(sail.hp, 0)

    def test_broadside_cannon_port_disable(self):
        air = makeAir()
        broadside = DistributedShipBroadsideAI.__new__(DistributedShipBroadsideAI)
        broadside.air = air
        broadside.doId = 7
        broadside.leftBroadsideEnabledState = [1, 1]
        broadside.rightBroadsideEnabledState = [1]
        broadside.sendUpdate = Mock()
        air.doId2do[42] = SimpleNamespace(doId=42)
        air.getAvatarIdFromSender.return_value = 42

        broadside.requestCannonEnabledState(ShipGlobals.BROADSIDE_LEFT, 1, 0)
        self.assertEqual(broadside.leftBroadsideEnabledState, [1, 0])
        broadside.requestCannonEnabledState(ShipGlobals.BROADSIDE_RIGHT, 5, 0)
        broadside.requestCannonEnabledState(ShipGlobals.BROADSIDE_RIGHT, 0, 1)
        self.assertEqual(broadside.rightBroadsideEnabledState, [1])
        air.writeServerEvent.assert_called_once()
        broadside.setCannonAnim(0, 0, 1, 0)

    def test_pc_cannon_gain_skill_is_rejected(self):
        air = makeAir()
        cannon = DistributedPCCannonAI.__new__(DistributedPCCannonAI)
        cannon.air = air
        cannon.doId = 9
        cannon.gainSkill(1)
        air.writeServerEvent.assert_called_once()

    def test_repair_spot_heals_ship(self):
        air = makeAir()
        ship = makeShip(air=air, crew=[42], hp=900, sp=490)
        spot = DistributedShipRepairSpotAI.__new__(DistributedShipRepairSpotAI)
        NodePath.__init__(spot, 'spot')
        spot.sendUpdate = Mock()
        spot.air = air
        spot.shipId = ship.doId
        spot.userId = 0
        spot.repairTask = None
        ship.repairSpots = [spot]
        avatar = SimpleNamespace(doId=42)
        self.assertEqual(spot.handleRequestInteraction(avatar, 0, 0), spot.ACCEPT)
        self.assertEqual(spot.handleRequestInteraction(SimpleNamespace(doId=43), 0, 0), spot.DENY)

        spot.userId = 42
        spot.getRepairAmount = lambda ship: 50
        spot._DistributedShipRepairSpotAI__repairShip(None)
        self.assertEqual(ship.hp, 950)
        self.assertEqual(ship.sp, 500)


class FlagAITests(unittest.TestCase):

    def makeDNAString(self, **kwargs):
        dna = FlagDNA()
        dna.setEmblem(0, 1, 2, 3, 4, 5)
        return dna.getDNAString()

    def test_valid_flag_dna(self):
        dnaString = self.makeDNAString()
        self.assertEqual(flag_module.getValidatedFlagDNAString(dnaString), dnaString)

    def test_invalid_flag_dna(self):
        dnaString = bytearray(self.makeDNAString())
        dnaString[0] = 200
        self.assertIsNone(flag_module.getValidatedFlagDNAString(bytes(dnaString)))
        self.assertIsNone(flag_module.getValidatedFlagDNAString(b'\x00'))

        dnaString = bytearray(self.makeDNAString())
        dnaString += bytes([0, 0, 0, 0, 0]) * 3
        self.assertIsNone(flag_module.getValidatedFlagDNAString(bytes(dnaString)))

    def test_request_dna_string_requires_ownership(self):
        inventory = Mock()
        inventory.getDoIdListCategory.return_value = []
        air = makeAir(inventoryManager=SimpleNamespace(getInventory=lambda avId: inventory))
        flag = flag_module.DistributedFlagAI.__new__(flag_module.DistributedFlagAI)
        flag.air = air
        flag.doId = 500
        flag.dnaString = b''
        flag.sendUpdate = Mock()
        air.doId2do[42] = SimpleNamespace(doId=42)
        air.getAvatarIdFromSender.return_value = 42

        dnaString = self.makeDNAString()
        flag.requestDNAString(dnaString)
        flag.sendUpdate.assert_not_called()

        inventory.getDoIdListCategory.return_value = [500]
        flag.requestDNAString(dnaString)
        inventory.getDoIdListCategory.assert_called_with(InventoryCategory.FLAGS)
        flag.sendUpdate.assert_called_once_with('setDNAString', [dnaString])


class ShipLoaderTests(unittest.TestCase):

    def test_ai_queues_ship_activation(self):
        loader = loader_ai.DistributedShipLoaderAI.__new__(loader_ai.DistributedShipLoaderAI)
        loader.avatar2fsm = {}
        loader.avatar2pendingShips = {}
        loader.air = SimpleNamespace(shipLoader=loader)
        loader.sendActivateShip = Mock()
        avatar = SimpleNamespace(doId=42, getInventory=lambda: object(), isDeleted=lambda: False)

        with patch.object(loader_ai.ActivateShipFSM, 'ignoreAll', create=True):
            loader.activateShip(avatar, 1)
            loader.activateShip(avatar, 2)
            loader.activateShip(avatar, 3)
            loader.sendActivateShip.assert_called_once_with(42, 1)

            loader.activateShipResponse(42, 1, True)
            loader.sendActivateShip.assert_called_with(42, 2)
            loader.activateShipResponse(42, 2, False)
            loader.sendActivateShip.assert_called_with(42, 3)
            loader.activateShipResponse(42, 3, True)

        self.assertEqual(loader.avatar2fsm, {})
        self.assertEqual(loader.avatar2pendingShips, {})

    def test_ud_activation_without_shipparts_finishes(self):
        fsm = loader_ud.ActivateShipFSM.__new__(loader_ud.ActivateShipFSM)
        fsm.shipId = 1
        fsm.avatarId = 42
        fsm.cleanup = Mock()
        fsm.loadShippart = Mock()
        fsm._shipInventoryQueryCallback(object(), {'setDoIds': ([[InventoryCategory.QUESTS, 5]],)})
        fsm.cleanup.assert_called_once_with(True)
        fsm.loadShippart.assert_not_called()

    def test_ud_shippart_activation_sends_post_remove(self):
        air = Mock(ourChannel=4000)
        fsm = loader_ud.ActivateShipFSM.__new__(loader_ud.ActivateShipFSM)
        fsm.air = air
        fsm.shipId = 1
        fsm.avatarId = 42
        fsm.accountId = 7
        fsm.pendingShipparts = [100, 101]
        fsm.cleanup = Mock()

        fsm._shippartQueryCallback(100, object(), {'setOwnerId': (42,)})
        self.assertEqual(air.send.call_count, 1)
        fsm.cleanup.assert_not_called()
        fsm._shippartQueryCallback(101, object(), {'setOwnerId': (42,)})
        fsm.cleanup.assert_called_once_with(True)

        fsm._shippartQueryCallback(102, None, None)
        fsm.cleanup.assert_called_with(False)


def trackGameState(ship):
    def b_setGameState(stateName, avId, timeStamp=0):
        ship.gameState = [stateName, avId, timeStamp]
        ship.gameFSM.getCurrentOrNextState.return_value = stateName

    ship.b_setGameState = Mock(side_effect=b_setGameState)


def makeFSM(ship, state='Patrol'):
    fsm = GameFSMShipAI(ship.air, ship)
    fsm.state = state
    fsm.oceanGrid = ship.getParentObj()
    ship.gameFSM = fsm
    return fsm


class _TaskPatchedTestCase(unittest.TestCase):

    def setUp(self):
        self.taskMgr = Mock()
        self.patches = [
            patch.object(builtins, 'taskMgr', self.taskMgr, create=True),
            patch.object(builtins, 'globalClock', Mock(getFrameTime=lambda: 100.0), create=True)]
        for item in self.patches:
            item.start()

    def tearDown(self):
        for item in self.patches:
            item.stop()


class GameFSMShipAITests(_TaskPatchedTestCase):

    def makeShips(self):
        air = makeAir(shipManager=SimpleNamespace(getPlayerShips=lambda: [self.target]))
        grid = NodePath('grid')
        self.ship = makeShip(cls=NPCShipAI, air=air, npcShip=1, baseTeam=ShipGlobals.NAVY_TEAM,
            shipClass=ShipGlobals.NAVY_FERRET)
        self.target = makeShip(doId=2000, air=air, baseTeam=ShipGlobals.PLAYER_TEAM)
        for ship in (self.ship, self.target):
            ship.reparentTo(grid)
            ship.getParentObj = lambda: grid
            ship.isDeleted = lambda: False

        trackGameState(self.ship)
        fsm = makeFSM(self.ship)
        fsm.getCurrentOrNextState = lambda: 'Patrol'
        fsm._islandSpheres = []
        fsm.world = SimpleNamespace()
        return fsm

    def test_ship_sails_at_ai_speed_and_turns_at_turn_rate(self):
        fsm = self.makeShips()
        speeds, turnRates = ShipGlobals.getAIShipSpeed(ShipGlobals.NAVY_FERRET)
        fsm._startMovementTo(Point3(5000, 0, 0), fsm._getShipSpeed())
        fsm._moveTask(None)

        self.assertAlmostEqual(abs(self.ship.getH()), turnRates[0] * fsm.MovePeriod, places=3)
        self.assertAlmostEqual(self.ship.getPos().length(), speeds[1] * fsm.MovePeriod, places=3)

    def test_ship_sails_in_ocean_grid_space_from_a_cell_origin(self):
        # like DistributedNodeAI.setLocation, the ship sits under the cell origin of
        # it's grid zone, so it's own position is relative to that cell...
        fsm = self.makeShips()
        grid = self.ship.getParentObj()
        cellOrigin = grid.attachNewNode('cellOrigin-1234')
        cellOrigin.setPos(20000, -14000, 0)
        self.ship.reparentTo(cellOrigin)
        self.ship.setPos(grid, 20000, -14000, 0)
        fsm.oceanGrid = grid

        fsm._startMovementTo(Point3(20000, -13000, 0), 100.0)
        for _ in range(200):
            if fsm._moveTask(None) == Task.done:
                break

        pos = self.ship.getPos(grid)
        self.assertLess((pos - Point3(20000, -13000, 0)).length(), fsm.WaypointRadius)
        self.assertIsNone(fsm._currentDestination)

    def test_ship_steers_around_islands(self):
        fsm = self.makeShips()
        fsm._islandSpheres = [(0, 1000, 500)]
        fsm._startMovementTo(Point3(0, 5000, 0), fsm._getShipSpeed())
        self.ship.setY(300)
        self.assertNotAlmostEqual(fsm._getDesiredHeading(), 0.0)

    def sailTo(self, fsm, destination, speed, steps=2000):
        closest = {}
        fsm._startMovementTo(destination, speed)
        for _ in range(steps):
            pos = self.ship.getPos()
            for centerX, centerY, radius in fsm._islandSpheres:
                dist = math.hypot(pos[0] - centerX, pos[1] - centerY)
                closest[(centerX, centerY)] = min(closest.get((centerX, centerY), dist), dist)

            if fsm._moveTask(None) == Task.done:
                return True, closest

        return False, closest

    def test_ship_sails_around_an_island_in_its_way(self):
        fsm = self.makeShips()
        fsm._islandSpheres = [(0, 3000, 1000)]
        arrived, closest = self.sailTo(fsm, Point3(0, 6000, 0), fsm._getShipSpeed(combatMode=True))
        self.assertTrue(arrived)
        self.assertGreater(closest[(0, 3000)], 1000)

    def test_ship_threads_between_two_islands(self):
        fsm = self.makeShips()
        fsm._islandSpheres = [(-1600, 3000, 1000), (1600, 3000, 1000)]
        arrived, closest = self.sailTo(fsm, Point3(0, 6000, 0), fsm._getShipSpeed())
        self.assertTrue(arrived)
        for dist in closest.values():
            self.assertGreater(dist, 1000)

    def test_ship_inside_an_islands_buffer_heads_back_out(self):
        fsm = self.makeShips()
        fsm._islandSpheres = [(0, 0, 1000)]
        self.ship.setPos(0, -1100, 0)
        fsm._startMovementTo(Point3(0, 5000, 0), fsm._getShipSpeed())
        self.assertAlmostEqual(abs(fsm._normalizeAngle(fsm._getDesiredHeading())), 180.0, places=3)

    def test_ship_never_sails_further_into_an_island(self):
        fsm = self.makeShips()
        fsm._islandSpheres = [(0, 0, 1000)]
        self.ship.setPos(0, -900, 0)
        self.assertTrue(fsm._isRunningAground(0, -900, 0, -850))
        self.assertFalse(fsm._isRunningAground(0, -900, 0, -950))

    def test_patrol_engages_player_ship_within_aggro_radius(self):
        fsm = self.makeShips()
        self.target.setPos(500, 0, 0)
        self.assertIs(fsm._findNearestEnemy(), self.target)
        fsm._GameFSMShipAI__patrolThink(None)
        self.ship.b_setGameState.assert_called_once_with('AttackChase', 0)
        self.assertIs(fsm.targetShip, self.target)

        self.target.setPos(50000, 0, 0)
        self.assertIsNone(fsm._findNearestEnemy())

    def test_npc_ships_ignore_each_other(self):
        fsm = self.makeShips()
        self.target.baseTeam = ShipGlobals.NAVY_TEAM
        self.assertFalse(fsm._isValidTarget(self.target))

    def test_broadside_fires_when_target_is_abeam(self):
        fsm = self.makeShips()
        self.ship.broadside = Mock()
        self.ship.broadside.fireAtTarget.return_value = True

        self.target.setPos(0, 500, 0)
        self.assertFalse(fsm._attemptBroadside(self.target))

        self.target.setPos(500, 0, 0)
        self.assertTrue(fsm._attemptBroadside(self.target))
        self.ship.broadside.fireAtTarget.assert_called_once_with(self.target, ShipGlobals.BROADSIDE_RIGHT)
        self.assertFalse(fsm._attemptBroadside(self.target))

    def test_broadside_lands_on_player_ship(self):
        fsm = self.makeShips()
        broadside = DistributedShipBroadsideAI.__new__(DistributedShipBroadsideAI)
        NodePath.__init__(broadside, 'broadside')
        broadside.air = self.ship.air
        broadside.doId = 77
        broadside.shipId = self.ship.doId
        broadside.leftBroadside = [1, 1]
        broadside.rightBroadside = [1, 1, 1]
        broadside.sendUpdate = Mock()
        class Grid(NodePath):
            def getZoneFromXYZ(self, pos):
                return 100 if pos[0] < 2000 else 101

            def getZoneCellOrigin(self, zoneId):
                return (0, 0, 0)

        grid = Grid('grid')
        cell = grid.attachNewNode('cell')
        cell.setPos(2000, 0, 0)
        self.ship.reparentTo(grid)
        self.ship.getParentObj = lambda: grid
        self.target.reparentTo(cell)
        self.target.setPos(grid, 500, 0, 0)
        self.assertTrue(broadside.fireAtTarget(self.target, ShipGlobals.BROADSIDE_RIGHT))

        args = broadside.sendUpdate.call_args[0][1]
        self.assertEqual(len(args[1]), 3)
        # the shots land around the target on the ocean grid, not around it's cell position:
        self.assertEqual(args[3], 100)
        self.assertAlmostEqual(sum(pos[0] for pos in args[2]) / 3.0, 500, delta=100)
        delay, callback, name = self.taskMgr.doMethodLater.call_args[0]
        extraArgs = self.taskMgr.doMethodLater.call_args[1]['extraArgs']

        self.target.handleShipDamage = Mock()
        with patch('random.random', return_value=0.0):
            callback(*extraArgs)

        self.target.handleShipDamage.assert_called_once()
        self.assertLess(self.target.handleShipDamage.call_args[0][0], 0)

    def test_damage_engages_attacker(self):
        fsm = self.makeShips()
        fsm.onDamageReceived(self.target.doId, 50)
        self.ship.b_setGameState.assert_called_once_with('AttackChase', 0)


class FlagshipBoardingTests(_TaskPatchedTestCase):

    def setUp(self):
        _TaskPatchedTestCase.setUp(self)
        air = makeAir(battleMgr=Mock(), questMgr=Mock())
        grid = NodePath('grid')
        self.flagship = makeShip(cls=NPCShipAI, air=air, npcShip=1, isFlagship=1, isBoardable=1,
            baseTeam=ShipGlobals.NAVY_TEAM, shipClass=ShipGlobals.NAVY_FERRET, deckCrew=[], objectData={})
        self.attacker = makeShip(doId=2000, air=air, captainId=42, crew=[42, 43])
        for ship in (self.flagship, self.attacker):
            ship.reparentTo(grid)
            ship.getParentObj = lambda: grid
            ship.getDeleteEvent = lambda ship=ship: 'delete-%d' % ship.doId
            ship.accept = Mock()
            ship.ignore = Mock()
            trackGameState(ship)

        makeFSM(self.flagship, 'AttackChase')
        self.flagship.gameState = ['AttackChase', 0, 0]
        self.flagship.gameFSM.getCurrentOrNextState = lambda: self.flagship.gameState[0]
        self.captain = SimpleNamespace(doId=42, getCrewShipId=lambda: 2000)
        air.doId2do[42] = self.captain

    def cripple(self):
        self.flagship.handleShipDamage(-5000, self.attacker)
        self.assertEqual(self.flagship.gameState[0], 'WaitingForGrapple')

    def test_crippled_flagship_waits_for_grapples(self):
        self.cripple()
        self.assertEqual(self.flagship.boardableShipId, self.attacker.doId)
        self.assertEqual(self.attacker.boardableShipId, self.flagship.doId)
        self.flagship.sendUpdate.assert_any_call('setSinkTimer', [int(self.flagship.CrippledTimeout), ANY])

    def test_regular_ship_still_sinks(self):
        self.flagship.isFlagship = 0
        self.flagship.handleShipDamage(-5000, self.attacker)
        self.assertEqual(self.flagship.gameState[0], 'Sinking')

    def test_grapples_pull_the_flagship_into_position(self):
        self.cripple()
        stranger = SimpleNamespace(doId=99, getCrewShipId=lambda: 0)
        self.flagship.handleGrappleHit(stranger, 1)
        self.assertEqual(self.attacker.landedGrapples, [])

        self.flagship.handleGrappleHit(self.captain, 1)
        self.assertEqual(self.attacker.landedGrapples, [[self.flagship.doId, 1]])
        self.assertEqual(self.flagship.gameState[0], 'GrappleLerping')
        self.flagship.handleGrappleHit(self.captain, 2)
        self.assertEqual(len(self.attacker.landedGrapples), 2)
        self.assertEqual(self.flagship.grappleArriveTime, 100.0 + self.flagship.GrapplePullTime / 2)

        self.flagship.setPos(500, 0, 0)
        self.flagship.grappleArriveTime = 0
        self.flagship._NPCShipAI__grappleLerpTask(None)
        self.assertEqual(self.flagship.gameState[0], 'InPosition')
        self.assertEqual(self.attacker.gameState[0], 'InBoardingPosition')
        self.assertTrue(self.attacker.isInBoardingPosition)
        self.assertAlmostEqual(self.flagship.getX(), self.flagship.BoardingOffset)

    def test_captain_starts_boarding_and_crew_swing_over(self):
        self.cripple()
        self.flagship.gameState = ['InPosition', 0, 0]
        self.flagship.spawnDeckCrew = Mock()
        self.attacker.air.getAvatarIdFromSender.return_value = 42
        self.attacker.requestBoardFlagship(self.flagship.doId)

        self.assertEqual(self.flagship.gameState[0], 'Boarded')
        self.flagship.spawnDeckCrew.assert_called_once_with()
        self.attacker.sendUpdate.assert_any_call('setBoardingSuccess', [self.flagship.doId, ANY])

        self.flagship.d_setMovie = Mock()
        self.flagship.requestBoard(42)
        self.flagship.d_setMovie.assert_called_once_with(ShipGlobals.SHIP_MOVIE_BOARD, 42, self.attacker.doId, 0)

    def test_npc_ships_cannot_be_boarded_directly(self):
        self.attacker.boardableShipId = 0
        self.flagship.air.getAvatarIdFromSender.return_value = 42
        self.flagship.d_setMovie = Mock()
        self.flagship.requestBoard(42)
        self.flagship.d_setMovie.assert_not_called()

    def test_defeating_the_crew_sinks_the_flagship(self):
        self.cripple()
        self.flagship.gameState = ['Boarded', 0, 0]
        self.flagship.crew = [42]
        npc = SimpleNamespace(getHp=lambda: [0, 0], isDeleted=lambda: False)
        self.flagship.deckCrew = [npc]
        self.attacker.d_setMovie = Mock()
        self.flagship._NPCShipAI__checkDeckCrew(None)

        self.assertEqual(self.flagship.gameState[0], 'Defeated')
        self.attacker.d_setMovie.assert_called_once_with(ShipGlobals.SHIP_MOVIE_BOARD, 42, self.flagship.doId, 0)

        self.flagship._NPCShipAI__defeatedSink(None)
        self.assertEqual(self.flagship.gameState[0], 'Sinking')
        self.assertEqual(self.attacker.boardableShipId, 0)

    def test_boarding_timeout_sinks_the_flagship(self):
        self.cripple()
        self.flagship._NPCShipAI__crippledTimeout(None)
        self.assertEqual(self.flagship.gameState[0], 'Sinking')
        self.assertEqual(self.attacker.landedGrapples, [])

    def test_grapple_projectile_is_routed_to_the_flagship(self):
        from pirates.battle.WeaponBaseAI import WeaponBaseAI
        from pirates.uberdog.UberDogGlobals import InventoryType

        weapon = WeaponBaseAI.__new__(WeaponBaseAI)
        weapon.air = self.flagship.air
        weapon.air.targetMgr = Mock()
        weapon.air.getAvatarIdFromSender.return_value = 42
        weapon.sendUpdate = Mock()
        self.flagship.handleGrappleHit = Mock()
        weapon.suggestProjectileSkillResult(InventoryType.CannonShoot, InventoryType.CannonGrappleHook,
            0, self.flagship.doId, [], [0, 0, 0], [0, 0, 1], [0, 99, 3], 0)

        self.flagship.handleGrappleHit.assert_called_once_with(self.captain, 3)
        self.flagship.air.battleMgr.willWeaponHit.assert_not_called()


class ShipManagerTutorialShipTests(unittest.TestCase):

    def test_tutorial_ships_are_passive_level_one_tutorial_ships(self):
        from unittest.mock import patch

        from pirates.ship import ShipGlobals, ShipManagerAI as shipManagerModule
        from tests.pirates.ship.test_tutorial_ship_ai import StubNPCShip
        from pirates.tutorial import TutorialGlobals

        grid = SimpleNamespace(
            getZoneFromXYZ=lambda pos: 2399,
            generateChildWithRequired=lambda child, zoneId: setattr(child, 'generated', zoneId),
            addObjectToOceanGrid=lambda child: setattr(child, 'onGrid', True))
        shipManager = shipManagerModule.ShipManagerAI.__new__(shipManagerModule.ShipManagerAI)
        shipManager.air = SimpleNamespace()
        with patch.object(shipManagerModule, 'TutorialShipAI', StubNPCShip):
            ship = shipManager.spawnTutorialShip(grid, ShipGlobals.SKEL_PHANTOM, 1, 1000,
                (110, 540, 0), 80, uniqueId=TutorialGlobals.UNDEAD_SHIP_UID)

        # a TutorialShip, not an NPCShip, and never part of the ship population...
        self.assertIsInstance(ship, StubNPCShip)
        self.assertNotIn(ship, getattr(shipManager, 'npcShips', set()))
        self.assertEqual(ship.generated, 2399)
        self.assertTrue(ship.onGrid)
        self.assertEqual(ship.values['setUniqueId'], (TutorialGlobals.UNDEAD_SHIP_UID,))
        self.assertEqual(ship.values['setShipClass'], (ShipGlobals.SKEL_PHANTOM,))
        self.assertEqual(ship.values['setLevel'], (1,))
        self.assertEqual(ship.values['setHp'], (1000,))
        self.assertEqual(ship.values['setIsBoardable'], (0,))
        # the AI never engages from Idle, a new pirate can't be sunk by it...
        self.assertEqual(ship.values['b_setGameState'], ('Idle', 0))


class SteeredShipGridZoneTests(unittest.TestCase):

    def makeOceanGrid(self):
        from pirates.world import WorldGlobals
        from pirates.world.DistributedOceanGridAI import DistributedOceanGridAI
        oceanGrid = DistributedOceanGridAI.__new__(DistributedOceanGridAI)
        NodePath.__init__(oceanGrid, 'oceanGrid')
        oceanGrid.doId = 4000
        oceanGrid.startingZone = WorldGlobals.OCEAN_GRID_STARTING_ZONE
        oceanGrid.gridSize = WorldGlobals.OCEAN_GRID_SIZE
        oceanGrid.gridRadius = WorldGlobals.OCEAN_GRID_RADIUS
        oceanGrid.cellWidth = WorldGlobals.OCEAN_CELL_SIZE
        oceanGrid.style = 'Cartesian'
        return oceanGrid

    def test_steered_ship_follows_its_position_into_the_next_cell(self):
        oceanGrid = self.makeOceanGrid()
        gridManager = Mock()
        air = makeAir(worldGridManager=gridManager)
        crew = SimpleNamespace(doId=42)
        air.doId2do[crew.doId] = crew
        ship = makeShip(air=air, crew=[42])
        ship.reparentTo(oceanGrid)
        ship.getParentObj = lambda: oceanGrid
        ship.zoneId = oceanGrid.getZoneFromXYZ((0, 0, 0))
        ship.b_setLocation = Mock()

        with patch.object(builtins, 'taskMgr', Mock(), create=True) as taskMgr:
            ship.setClientController(42)
            delay, callback, name = taskMgr.doMethodLater.call_args[0]

        self.assertEqual(name, 'updateGridZone-1000')
        task = Mock()

        # still in the cell the ship launched in, nothing to do...
        self.assertIs(callback(task), task.again)
        ship.b_setLocation.assert_not_called()

        # sailed a full cell east, the ship moves into that cell so everyone sees it there...
        ship.setPos(oceanGrid.cellWidth, 0, 0)
        callback(task)
        ship.b_setLocation.assert_called_once_with(
            oceanGrid.doId, oceanGrid.getZoneFromXYZ((oceanGrid.cellWidth, 0, 0)))

        # the crew's own clients look after what they can see on the ocean...
        gridManager.handleLocationChanged.assert_not_called()

    def test_boarding_at_sea_leaves_the_crews_interest_alone(self):
        oceanGrid = self.makeOceanGrid()
        gridManager = Mock()
        ship = makeShip(air=makeAir(worldGridManager=gridManager))
        ship.reparentTo(oceanGrid)
        ship.getParentObj = lambda: oceanGrid
        ship.addCrewMember = Mock()
        avatar = Mock(spec=['doId', 'b_setShipId', 'b_setActiveShipId',
            'b_setCrewShipId', 'b_setCurrentIsland'], doId=42)

        with patch('pirates.ship.DistributedShipAI.isinstance',
                   lambda obj, cls: True if obj is avatar else builtins.isinstance(obj, cls),
                   create=True):
            ship._playerBoarded(avatar)

        ship.addCrewMember.assert_called_once_with(avatar)
        gridManager.handleLocationChanged.assert_not_called()

    def test_letting_go_of_the_wheel_stops_the_zone_checks(self):
        ship = makeShip()
        with patch.object(builtins, 'taskMgr', Mock(), create=True) as taskMgr:
            ship.setClientController(0)

        taskMgr.remove.assert_called_once_with('updateGridZone-1000')
        taskMgr.doMethodLater.assert_not_called()


if __name__ == '__main__':
    unittest.main()
