import sys
import unittest
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock, patch

from otp.ai.MagicWordGlobal import *
from otp.ai.MagicWordManagerAI import MagicWordManagerAI
from pirates.ai import PiratesMagicWordManagerAI as words
from pirates.piratesbase import PiratesGlobals, TODGlobals


class Player:
    def __init__(self, doId, name='Player', access=CATEGORY_SYSTEM_ADMIN.access):
        self.doId = doId
        self.name = name
        self.adminAccess = access
        self.immortal = False
        self.hp = 1
        self.mojo = 1
        self.tutorial = 0
        self.shipId = 0
        self.activeShipId = 0
        self.inventory = None

    def getName(self):
        return self.name

    def getAdminAccess(self):
        return self.adminAccess

    def setImmortal(self, immortal):
        self.immortal = immortal

    def getImmortal(self):
        return self.immortal

    def getMaxHp(self):
        return 100

    def getMaxMojo(self):
        return 50

    def b_setHp(self, hp):
        self.hp = hp

    def b_setMojo(self, mojo):
        self.mojo = mojo

    def getTutorial(self):
        return self.tutorial

    def b_setTutorial(self, tutorial):
        self.tutorial = tutorial

    def getShipId(self):
        return self.shipId

    def getActiveShipId(self):
        return self.activeShipId

    def getInventory(self):
        return self.inventory

    def GetPuppetConnectionChannel(self, doId):
        return doId + (1 << 32)


class Ship:
    def __init__(self, doId):
        self.doId = doId
        self.hp = 10
        self.sp = 10
        self.state = 'Patrol'

    def getName(self):
        return 'Ship'

    def isSailable(self):
        return self.hp > 0

    def getMaxHp(self):
        return 500

    def getMaxSp(self):
        return 200

    def b_setHp(self, hp):
        self.hp = hp

    def b_setSp(self, sp):
        self.sp = sp


class Inventory:
    def __init__(self):
        self.reputation = {}

    def getReputation(self, repType):
        return self.reputation.get(repType, 0)

    def setReputation(self, repType, quantity):
        self.reputation[repType] = quantity


class MagicWordTests(unittest.TestCase):
    def setUp(self):
        self.air = SimpleNamespace(doId2do={}, events=[])
        self.air.writeServerEvent = lambda *args, **kwargs: self.air.events.append((args, kwargs))
        self.air.teleportMgr = MagicMock()
        self.air.kickChannel = MagicMock()
        self.manager = SimpleNamespace(air=self.air)

        playerModule = ModuleType('pirates.pirate.DistributedPlayerPirateAI')
        playerModule.DistributedPlayerPirateAI = Player
        patcher = patch.dict(sys.modules, {'pirates.pirate.DistributedPlayerPirateAI': playerModule})
        patcher.start()
        self.addCleanup(patcher.stop)

    def addPlayer(self, doId, name='Player', access=CATEGORY_SYSTEM_ADMIN.access):
        player = Player(doId, name, access)
        self.air.doId2do[doId] = player
        return player

    def invoke(self, invoker, incantation, target=None):
        return spellbook.process(self.manager, invoker, target or invoker, incantation)

    def test_invoker_access_is_enforced(self):
        tester = self.addPlayer(1, access=CATEGORY_TESTER.access)
        self.assertEqual(self.invoke(tester, 'god'), 'Insufficient access')
        self.assertFalse(tester.immortal)

    def test_target_access_is_enforced(self):
        invoker = self.addPlayer(1, access=CATEGORY_SYSTEM_ADMIN.access)
        target = self.addPlayer(2, access=CATEGORY_SYSTEM_ADMIN.access + 100)
        self.assertEqual(self.invoke(invoker, 'god', target), 'Target must have lower or equal access')

    def test_prefix_and_case_are_ignored(self):
        invoker = self.addPlayer(1)
        self.assertEqual(self.invoke(invoker, '~GOD'), 'God mode set to: True')
        self.assertEqual((invoker.hp, invoker.mojo), (100, 50))

    def test_untyped_arguments_are_passed_as_strings(self):
        @magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
        def testUntypedArgs(a, b):
            return '%r %r' % (a, b)

        invoker = self.addPlayer(1)
        self.assertEqual(self.invoke(invoker, 'testUntypedArgs 1 two words'), "1 'two words'")
        self.assertEqual(self.invoke(invoker, 'testUntypedArgs x y'),
                         'Argument 0 of magic word testUntypedArgs must be int')

    def test_manager_treats_zero_target_as_invoker(self):
        invoker = self.addPlayer(1)
        mgr = MagicWordManagerAI.__new__(MagicWordManagerAI)
        mgr.air = self.air
        mgr.air.getAvatarIdFromSender = lambda: 1
        mgr.sendUpdateToAvatarId = MagicMock()
        mgr.sendMagicWord('~tutorial 4', 0)
        self.assertEqual(invoker.tutorial, 4)
        mgr.sendUpdateToAvatarId.assert_called_with(1, 'sendMagicWordResponse',
                                                    ['Tutorial state set to 4.'])

    def test_manager_rejects_low_access_invokers(self):
        invoker = self.addPlayer(1, access=0)
        mgr = MagicWordManagerAI.__new__(MagicWordManagerAI)
        mgr.air = self.air
        mgr.air.getAvatarIdFromSender = lambda: 1
        mgr.sendUpdateToAvatarId = MagicMock()
        mgr.sendMagicWord('~tutorial 4', 1)
        self.assertEqual(invoker.tutorial, 0)
        mgr.sendUpdateToAvatarId.assert_not_called()

    def test_goto_and_summon_use_teleport_manager(self):
        invoker = self.addPlayer(1, 'Admin')
        other = self.addPlayer(2, 'Jack Sparrow', access=0)
        self.assertEqual(self.invoke(invoker, 'goto jack sparrow'), 'Teleporting to Jack Sparrow...')
        self.air.teleportMgr.teleportToAvatar.assert_called_with(invoker, other)
        self.assertEqual(self.invoke(invoker, 'summon 2'), 'Summoning Jack Sparrow...')
        self.air.teleportMgr.teleportToAvatar.assert_called_with(other, invoker)
        self.assertEqual(self.invoke(invoker, 'goto nobody'), 'Could not find player: nobody!')

    def test_kick_respects_target_access(self):
        invoker = self.addPlayer(1, 'Mod', access=CATEGORY_MODERATION.access)
        self.addPlayer(2, 'Admin', access=CATEGORY_SYSTEM_ADMIN.access)
        player = self.addPlayer(3, 'Player', access=0)
        self.assertEqual(self.invoke(invoker, 'kick Admin'), 'Target must have lower or equal access')
        self.air.kickChannel.assert_not_called()
        self.assertEqual(self.invoke(invoker, 'kick player'), 'Kicked Player (3).')
        self.air.kickChannel.assert_called_once()
        self.assertEqual(self.air.kickChannel.call_args[0][:2],
                         (player.GetPuppetConnectionChannel(3), 151))

    def test_rep_adds_reputation(self):
        from pirates.uberdog.UberDogGlobals import InventoryType
        invoker = self.addPlayer(1)
        invoker.inventory = Inventory()
        self.invoke(invoker, 'rep %d 500' % InventoryType.CutlassRep)
        self.invoke(invoker, 'rep %d 250' % InventoryType.CutlassRep)
        self.assertEqual(invoker.inventory.getReputation(InventoryType.CutlassRep), 750)
        self.assertEqual(self.invoke(invoker, 'rep 1 1'), 'Invalid reputation type: 1!')

    def test_tutorial_validates_state(self):
        invoker = self.addPlayer(1)
        self.assertEqual(self.invoke(invoker, 'tutorial'), 'Tutorial state: 0')
        self.invoke(invoker, 'tutorial %d' % (PiratesGlobals.TUT_FINISHED + 1))
        self.assertEqual(invoker.tutorial, 0)
        self.invoke(invoker, 'tutorial %d' % PiratesGlobals.TUT_FINISHED)
        self.assertEqual(invoker.tutorial, PiratesGlobals.TUT_FINISHED)

    def test_tod_resyncs_cycle_from_state(self):
        invoker = self.addPlayer(1)
        todMgr = MagicMock(cycleType=TODGlobals.TOD_REGULAR_CYCLE, cycleDuration=3600.0)
        self.air.timeOfDayMgr = todMgr
        self.assertEqual(self.invoke(invoker, 'tod %d 0' % PiratesGlobals.TOD_NIGHT), 'Time of day set to Night (6).')
        cycleType, state, startingTime, duration = todMgr.b_sync.call_args[0]
        self.assertEqual((cycleType, state, duration), (TODGlobals.TOD_REGULAR_CYCLE, PiratesGlobals.TOD_NIGHT, 0.0))
        todMgr._processStateChange.assert_called_once_with()

        self.invoke(invoker, 'tod %d' % PiratesGlobals.TOD_DAY)
        self.assertEqual(todMgr.b_sync.call_args[0][3], 3600.0)
        self.assertIn('Invalid', self.invoke(invoker, 'tod %d' % PiratesGlobals.TOD_HALLOWEEN))

    def test_ship_repair_and_sink(self):
        invoker = self.addPlayer(1)
        self.assertEqual(self.invoke(invoker, 'repairShip'), 'You must be aboard a ship!')
        ship = Ship(50)
        self.air.doId2do[50] = ship
        invoker.shipId = 50
        self.invoke(invoker, 'repairShip')
        self.assertEqual((ship.hp, ship.sp), (500, 200))
        self.invoke(invoker, 'sinkShip')
        self.assertEqual(ship.hp, 0)
        self.assertEqual(self.invoke(invoker, 'sinkShip'), 'This ship is already sinking!')

    def test_siege_toggles_pvp(self):
        invoker = self.addPlayer(1)
        self.air.siegeManager = MagicMock()
        self.invoke(invoker, 'siege 1')
        self.air.siegeManager.b_setPvpEnabled.assert_called_with(True)


if __name__ == '__main__':
    unittest.main()
