import builtins
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from direct.showbase.MessengerGlobal import messenger
from panda3d.direct import DCFile
from otp.distributed.AstronDatabaseInterface import AstronDatabaseInterface
from pirates.uberdog.TreasureMapInventoryAI import TreasureMapInventoryAI
from pirates.uberdog.UberDogGlobals import InventoryCategory


class Inventory:
    doId = 100
    ownerId = 10

    def __init__(self, air):
        self.air = air
        self.slots = []

    def getDoIds(self):
        return [list(slot) for slot in self.slots]

    def getDoIdListCategory(self, category):
        return [doId for cat, doId in self.slots if cat == category]

    def b_setDoIdListCategory(self, category, ids):
        self.slots = [slot for slot in self.slots if slot[0] != category]
        self.slots.extend([[category, doId] for doId in ids])


class TreasureMapInventoryTests(unittest.TestCase):
    def setUp(self):
        self.taskMgr = SimpleNamespace(doMethodLater=Mock(), remove=Mock())
        self.messenger = messenger
        self.patches = [
            patch.object(builtins, 'taskMgr', self.taskMgr, create=True),
            patch.object(builtins, 'messenger', self.messenger, create=True),
        ]
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)
        self.db = SimpleNamespace(queryObject=Mock(), createObject=Mock(), updateObject=Mock())
        self.air = SimpleNamespace(dbInterface=self.db, dbId=1,
            dclassesByName={'PirateInventoryAI': 'inventory',
                            'DistributedTreasureMapAI': 'map'},
            doId2do={10: object()}, sendActivate=Mock())
        self.inv = Inventory(self.air)
        self.air.doId2do[100] = self.inv
        self.service = TreasureMapInventoryAI(self.inv)
        self.result = Mock()

    def query(self, slots):
        callback = self.db.queryObject.call_args.args[2]
        callback('inventory', {'setDoIds': (slots,)})

    def create(self, doId=200):
        self.db.createObject.call_args.args[3](doId)

    def map_generated(self, doId=200):
        obj = SimpleNamespace(doId=doId, getOwnerId=lambda: 10,
                              getMapId=lambda: 0, requestDelete=Mock())
        self.air.doId2do[doId] = obj
        self.messenger.send('generate-%d' % doId, [obj])
        return obj

    def test_creation_links_conditionally_and_waits_for_activation(self):
        self.service.give(0, self.result)
        self.query([])
        fields = self.db.createObject.call_args.args[2]
        self.assertEqual(fields['setMapId'], (0,))
        self.assertEqual(fields['setOwnerId'], (10,))
        self.create()
        kwargs = self.db.updateObject.call_args.kwargs
        self.assertEqual(kwargs['oldFields'], {'setDoIds': ([],)})
        self.assertEqual(self.inv.slots, [])
        kwargs['callback'](None)
        self.result.assert_not_called()
        self.assertEqual(self.inv.slots, [[InventoryCategory.TREASURE_MAPS, 200]])
        self.assertEqual(self.air.sendActivate.call_args.args[-1], {'setIsEnabled': (1,)})
        self.map_generated()
        self.result.assert_called_once_with(True)

    def test_conflict_and_late_callback_do_not_complete_or_mutate_new_request(self):
        self.service.give(0, self.result)
        self.query([])
        self.create()
        old_callback = self.db.updateObject.call_args.kwargs['callback']
        old_callback({'setDoIds': ([(1, 44)],)})
        self.result.assert_called_once_with(False)
        self.assertEqual(self.inv.slots, [])
        second = Mock()
        self.service.give(0, second)
        old_callback(None)
        self.assertEqual(self.inv.slots, [])
        second.assert_not_called()
        self.query([])
        self.db.createObject.call_args.args[3](0)
        second.assert_called_once_with(False)

    def test_timeout_after_committed_link_recovers_without_duplicate(self):
        self.service.give(0, self.result)
        self.query([])
        self.create()
        self.service._awardTimedOut(None)
        self.result.assert_called_once_with(False)
        retry = Mock()
        self.service.give(0, retry)
        self.query([(InventoryCategory.TREASURE_MAPS, 200)])
        self.assertEqual(self.db.createObject.call_count, 1)
        self.map_generated()
        retry.assert_called_once_with(True)
        self.assertEqual(self.inv.slots, [[InventoryCategory.TREASURE_MAPS, 200]])

    def test_login_activation_and_disconnect(self):
        self.inv.slots = [[InventoryCategory.TREASURE_MAPS, 200]]
        self.service.activateAll()
        self.assertEqual(self.air.sendActivate.call_args.args[:3], (200, 100, 2))
        waiter = Mock()
        self.service.activate(200, waiter)
        self.service.close()
        waiter.assert_called_once_with(None)
        self.map_generated()
        waiter.assert_called_once()

    def test_database_failure_does_not_report_success(self):
        self.db.queryObject.side_effect = RuntimeError('unavailable')
        self.service.give(0, self.result)
        self.result.assert_called_once_with(False)

    def test_activation_failure_keeps_link_for_retry(self):
        self.air.sendActivate.side_effect = RuntimeError('activation failed')
        self.service.give(0, self.result)
        self.query([])
        self.create()
        self.db.updateObject.call_args.kwargs['callback'](None)
        self.result.assert_called_once_with(False)
        self.assertEqual(self.inv.slots, [[InventoryCategory.TREASURE_MAPS, 200]])
        self.air.sendActivate.side_effect = None
        retry = Mock()
        self.service.give(0, retry)
        self.query([(InventoryCategory.TREASURE_MAPS, 200)])
        self.map_generated()
        retry.assert_called_once_with(True)
        self.assertEqual(self.db.createObject.call_count, 1)

    def test_created_fields_pack_against_real_dc(self):
        dc = DCFile()
        self.assertTrue(dc.read('astron/dclass/otp.dc'))
        self.assertTrue(dc.read('astron/dclass/pirates.dc'))
        self.air.dclassesByName['DistributedTreasureMapAI'] = dc.getClassByName(
            'DistributedTreasureMap')
        self.air.getContext = lambda: 1
        self.air.ourChannel = 10
        self.air.send = Mock()
        self.air.dbInterface = AstronDatabaseInterface(self.air)
        self.service.award = {'mapId': 0}
        self.service._create()
        self.air.send.assert_called_once()


if __name__ == '__main__':
    unittest.main()
