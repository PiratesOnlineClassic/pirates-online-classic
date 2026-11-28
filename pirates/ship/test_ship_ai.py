import builtins
import importlib.abc
import importlib.machinery
import pickle
import sys
import unittest
import zlib
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

from panda3d.core import (ExecutionEnvironment, NodePath, Filename, VirtualFileMountRamdisk,
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
        repairSpots=[]))
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


if __name__ == '__main__':
    unittest.main()
