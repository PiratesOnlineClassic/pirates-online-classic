import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, Mock, patch

from panda3d.core import loadPrcFile, loadPrcFileData

loadPrcFile('config/dev.prc')
loadPrcFileData('', 'audio-library-name null')
import builtins
if not hasattr(builtins, 'base'):
    from direct.showbase.ShowBase import ShowBase
    ShowBase(windowType='none')

from tests.pirates.kraken.testutil import installStubs
installStubs()

from pirates.kraken import KrakenAI as KrakenAIModule
from pirates.kraken.KrakenAI import KrakenAI
from pirates.kraken.GrabberTentacleAI import GrabberTentacleAI
from pirates.kraken.HolderTentacleAI import HolderTentacleAI
from pirates.kraken.KrakenBodyAI import KrakenBodyAI
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals
from pirates.ship import ShipGlobals


def makeAir():
    air = MagicMock()
    air.doId2do = {}
    return air


class FakeShip:

    def __init__(self, air, doId=500, shipClass=ShipGlobals.INTERCEPTORL1):
        self.air = air
        self.doId = doId
        self.shipClass = shipClass
        self.crew = []
        self.masts = [object(), object()]
        self.hp = 1000
        self.level = 30
        self.children = []
        self.nextDoId = doId + 1
        air.doId2do[doId] = self

    def getDeleteEvent(self):
        return 'ship-delete-%d' % self.doId

    def getShipClass(self):
        return self.shipClass

    def getLevel(self):
        return self.level

    def getCrew(self):
        return self.crew

    def getHp(self):
        return self.hp

    def b_setHp(self, hp):
        self.hp = hp

    def generateChildWithRequired(self, do, zoneId):
        do.doId = self.nextDoId
        self.nextDoId += 1
        do.parentId = self.doId
        do.zoneId = zoneId
        self.air.doId2do[do.doId] = do
        self.children.append(do)
        do.announceGenerate()


class FakeAvatar:

    def __init__(self, doId, shipId, hp=500):
        self.doId = doId
        self.shipId = shipId
        self.hp = hp
        self.inventory = Mock()

    def getShipId(self):
        return self.shipId

    def getHp(self):
        return [self.hp, False]

    def b_setHp(self, hp):
        self.hp = hp

    def getInventory(self):
        return self.inventory


class KrakenAITests(unittest.TestCase):

    def setUp(self):
        self.air = makeAir()
        self.ship = FakeShip(self.air)
        self.sent = []
        patcher = patch('direct.distributed.DistributedObjectAI.DistributedObjectAI.sendUpdate',
            autospec=True, side_effect=lambda obj, field, args=[]: self.sent.append((obj, field, list(args))))
        patcher.start()
        self.addCleanup(patcher.stop)
        deletePatcher = patch('direct.distributed.DistributedObjectAI.DistributedObjectAI.requestDelete',
            autospec=True)
        self.requestDelete = deletePatcher.start()
        self.addCleanup(deletePatcher.stop)

    def tearDown(self):
        for obj in list(self.air.doId2do.values()):
            if hasattr(obj, 'doId'):
                taskMgr.removeTasksMatching('*%d*' % obj.doId)

    def spawn(self):
        kraken = KrakenAIModule.spawnKraken(self.air, self.ship)
        self.assertIsNotNone(kraken)
        return kraken

    def test_spawn_creates_parts_for_every_locator(self):
        kraken = self.spawn()
        self.assertEqual(kraken.getShipId(), self.ship.doId)
        self.assertEqual(kraken.zoneId, PiratesGlobals.ShipZoneSilhouette)
        numLocators = len(ShipGlobals.KrakenLocators[ShipGlobals.INTERCEPTORL1]) * 2
        self.assertEqual(sorted(kraken.grabberTentacles.keys()), list(range(numLocators)))
        self.assertEqual(len(kraken.holderTentacles), KrakenAI.NumHolderTentacles)
        self.assertIsInstance(kraken.body, KrakenBodyAI)
        self.assertEqual(kraken.state, 'Attack')

        for grabber in kraken.grabberTentacles.values():
            self.assertEqual(grabber.getKrakenId(), kraken.doId)
            self.assertEqual(grabber.getAvatarType(), AvatarTypes.GrabberTentacle)
            self.assertEqual(grabber.getEmerged(), 1)
            self.assertEqual(grabber.getTeam(), PiratesGlobals.UNDEAD_TEAM)
            self.assertGreater(grabber.getMaxHp(), 0)
            self.assertIn((grabber, 'emerge', [1]), self.sent)

    def test_level_is_clamped(self):
        self.ship.level = 1
        self.assertEqual(self.spawn().getLevel(), KrakenAI.MinLevel)

    def test_unsupported_ship_has_no_kraken(self):
        self.ship.shipClass = ShipGlobals.DINGHY
        self.assertIsNone(KrakenAIModule.spawnKraken(self.air, self.ship))

    def test_grab_and_squeeze_avatar(self):
        kraken = self.spawn()
        avatar = FakeAvatar(900, self.ship.doId)
        self.air.doId2do[avatar.doId] = avatar
        self.ship.crew.append(avatar.doId)

        grabber = kraken.grabberTentacles[0]
        grabber.grabAvatar(avatar.doId)
        self.assertEqual(grabber.getGrabbedAvatar(), avatar.doId)
        self.assertIn((grabber, 'grabAvatar', [avatar.doId]), self.sent)
        self.assertIn((grabber, 'setGrabbedAvatar', [avatar.doId]), self.sent)
        self.assertEqual(kraken.getGrabbableAvatars(), [])

        task = SimpleNamespace()
        grabber._GrabberTentacleAI__squeeze(task)
        self.assertEqual(avatar.hp, 500 - grabber.getSqueezeDamage())

        # avatar leaves the ship
        avatar.shipId = 0
        grabber._GrabberTentacleAI__squeeze(task)
        self.assertEqual(grabber.getGrabbedAvatar(), 0)
        self.assertIn((grabber, 'grabAvatar', [0]), self.sent)

    def test_masts_damage_ship(self):
        kraken = self.spawn()
        kraken.GrabAvatarChance = 0
        kraken.GrabMastChance = 1
        with patch('random.random', return_value=0.0):
            kraken._KrakenAI__attack(SimpleNamespace())

        held = kraken.getGrabbedMasts()
        self.assertEqual(sorted(held), [1, 2])
        hp = self.ship.hp
        kraken._KrakenAI__attack(SimpleNamespace())
        self.assertLess(self.ship.hp, hp)

    def test_ship_sunk_makes_kraken_retreat(self):
        kraken = self.spawn()
        self.ship.hp = 0
        kraken._KrakenAI__attack(SimpleNamespace())
        self.assertEqual(kraken.state, 'Retreat')
        for grabber in kraken.grabberTentacles.values():
            self.assertEqual(grabber.getEmerged(), 0)

    def test_body_death_defeats_kraken_and_rewards_crew(self):
        kraken = self.spawn()
        avatar = FakeAvatar(900, self.ship.doId)
        self.air.doId2do[avatar.doId] = avatar
        self.ship.crew.append(avatar.doId)

        kraken.body.setHp(0)
        self.air.battleMgr.rewardAttackers.assert_called_with(kraken.body)
        self.assertEqual(kraken.state, 'Retreat')
        avatar.inventory.addGoldInPocket.assert_called_once()

    def test_all_grabbers_dying_defeats_kraken(self):
        kraken = self.spawn()
        grabbers = list(kraken.grabberTentacles.values())
        for grabber in grabbers[:-1]:
            grabber.setHp(0)
            self.assertEqual(kraken.state, 'Attack')
            self.assertEqual(grabber.getEmerged(), 0)

        grabbers[-1].setHp(0)
        self.assertEqual(kraken.state, 'Retreat')

    def test_delete_removes_parts(self):
        kraken = self.spawn()
        parts = list(kraken.grabberTentacles.values()) + kraken.holderTentacles + [kraken.body]
        kraken.delete()
        deleted = [call.args[0] for call in self.requestDelete.call_args_list]
        for part in parts:
            self.assertIn(part, deleted)


if __name__ == '__main__':
    unittest.main()
