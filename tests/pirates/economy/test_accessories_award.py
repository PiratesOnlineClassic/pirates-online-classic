import builtins
import dbm.dumb
import os
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch
from tests import REPO_ROOT

try:
    import semidbm
except ImportError:
    # semidbm is only needed by the live UberDOG; dbm.dumb has the same API.
    sys.modules['semidbm'] = types.SimpleNamespace(open=dbm.dumb.open)

from pirates.economy import AwardGlobals
from pirates.economy.AvatarAccessoriesManagerAI import AvatarAccessoriesManagerAI
from pirates.economy.AvatarAccessoriesManagerUD import (
    AccessoriesDB,
    AvatarAccessoriesManagerUD,
    packClothing,
    unpackClothing,
)
from pirates.economy.AwardMakerUD import AwardMakerUD
from pirates.makeapirate import ClothingGlobals
from pirates.pirate.HumanDNA import HumanDNA
from pirates.uberdog.UberDogGlobals import InventoryType


def clothingOfType(itemType, count):
    uids = [uid for uid, item in sorted(ClothingGlobals.UNIQUE_ID.items()) if item[0] == itemType]
    return uids[:count]


class Wire:
    """
    Connects an AI accessories manager straight to a UD one so the request
    and response fields can be exercised without a message director.
    """

    def __init__(self, tmpdir):
        self.ud = AvatarAccessoriesManagerUD.__new__(AvatarAccessoriesManagerUD)
        self.ud.air = Mock()
        self.ud.air.getMsgSender.return_value = 999
        self.ud.accessoriesDB = AccessoriesDB(os.path.join(tmpdir, 'accessories'))

        self.ai = AvatarAccessoriesManagerAI.__new__(AvatarAccessoriesManagerAI)
        self.ai.air = Mock()
        self.ai.air.doId2do = {}
        self.ai.context = 0
        self.ai.callbacks = {}
        self.ai.clothing = {}
        self.ai.jewelry = {}
        self.ai.tattoos = {}
        self.ai.acceptOnce = Mock()

        self.ai.sendUpdate = lambda fieldName, args: getattr(self.ud, fieldName)(*args)
        self.ud.sendUpdateToChannel = lambda channel, fieldName, args: getattr(self.ai, fieldName)(*args)


class AccessoriesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.wire = Wire(self.tmp.name)

    def tearDown(self):
        self.wire.ud.accessoriesDB.close()
        self.tmp.cleanup()

    def test_clothing_round_trip(self):
        uid = clothingOfType(ClothingGlobals.SHIRT, 1)[0]
        results = []
        self.wire.ai.addClothing(5, [(uid, 3)], callback=results.append)
        self.wire.ai.getClothing(5, results.append)
        self.wire.ai.removeClothing(5, [(uid, 3)], callback=results.append)
        self.wire.ai.removeClothing(5, [(uid, 3)], callback=results.append)
        self.wire.ai.getClothing(5, results.append)
        self.assertEqual(results, [True, [[uid, 3, 0]], True, False, []])
        self.assertEqual(self.wire.ai.callbacks, {})

    def test_clothing_type_limit(self):
        uids = clothingOfType(ClothingGlobals.HAT, AvatarAccessoriesManagerUD.ClothingLimit + 1)
        results = []
        for uid in uids:
            self.wire.ai.addClothing(5, [(uid, 0)], callback=results.append)

        self.assertEqual(results[-1], False)
        self.assertTrue(all(results[:-1]))

    def test_unknown_clothing_rejected(self):
        results = []
        self.wire.ai.addClothing(5, [(0xFFFFFF, 0)], callback=results.append)
        self.assertEqual(results, [False])

    def test_jewelry_and_tattoos(self):
        results = []
        self.wire.ai.addJewelry(5, 12, callback=results.append)
        self.wire.ai.getJewelry(5, results.append)
        self.wire.ai.addTattoo(5, 7, callback=results.append)
        self.wire.ai.removeTattoo(5, 7, callback=results.append)
        self.wire.ai.getTattoos(5, results.append)
        self.assertEqual(results, [True, [12], True, True, []])

    def test_pack_clothing(self):
        self.assertEqual(packClothing(300, 7) >> 8, 300)
        self.assertEqual(packClothing(300, 7) & 0xFF, 7)
        self.assertEqual(unpackClothing(packClothing(160024, 20, 1)), (160024, 20, 1))
        self.assertEqual(unpackClothing(packClothing(160024, 20)), (160024, 20, 0))
        self.assertLess(packClothing(160024, 255, 1), 1 << 32)

    def test_old_clothing_entries_are_not_original(self):
        uid = clothingOfType(ClothingGlobals.SHIRT, 1)[0]
        self.wire.ud.accessoriesDB.setWardrobe(5, {'clothing': [[uid, 3]], 'jewelry': [], 'tattoos': []})
        results = []
        self.wire.ai.getClothing(5, results.append)
        self.assertEqual(results, [[[uid, 3, 0]]])

    def test_starting_clothing_migrated_from_dna(self):
        avatar = HumanDNA('f')
        self.wire.ai.air.doId2do[5] = avatar
        expected = self.wire.ai.getDNAClothing(avatar)
        self.assertTrue(expected)
        self.assertTrue(all(item[2] == 1 for item in expected))

        results = []
        self.wire.ai.getClothing(5, results.append)
        self.assertEqual(results, [expected])

        # the UberDOG now has them as starting items...
        self.wire.ai.clothing = {}
        self.wire.ai.getClothing(5, results.append)
        self.assertEqual(results[1], expected)

        # and will not migrate a second time.
        self.wire.ud.migrateDNAElements(0, 5, 0, [packClothing(clothingOfType(ClothingGlobals.HAT, 1)[0], 0)], 0)
        self.assertEqual(len(self.wire.ud.getClothingList(5)), len(expected))

    def test_cache_follows_changes(self):
        uid = clothingOfType(ClothingGlobals.HAT, 1)[0]
        results = []
        self.wire.ai.getClothing(5, results.append)
        self.wire.ai.acceptOnce.assert_called_once()
        self.wire.ai.addClothing(5, [(uid, 2)])
        self.wire.ai.addJewelry(5, 12)
        self.wire.ai.getClothing(5, results.append, useCache=True)
        self.assertEqual(results, [[], [[uid, 2, 0]]])

        self.wire.ai.removeClothing(5, [(uid, 2)])
        self.wire.ai.getClothing(5, results.append, useCache=True)
        self.assertEqual(results[-1], [])

        # a failed change drops the cache so it is loaded again...
        self.wire.ai.removeClothing(5, [(uid, 2)])
        self.assertNotIn(5, self.wire.ai.clothing)

        self.wire.ai.getTattoos(5, results.append)
        self.wire.ai.addTattoo(5, 7)
        self.wire.ai.getTattoos(5, results.append, useCache=True)
        self.assertEqual(results[-1], [7])

        self.wire.ai._AvatarAccessoriesManagerAI__handleAvatarExit(5)
        self.assertEqual((self.wire.ai.clothing, self.wire.ai.jewelry, self.wire.ai.tattoos), ({}, {}, {}))


class AwardTests(unittest.TestCase):
    def makeAI(self, avatar=None):
        ai = AvatarAccessoriesManagerAI.__new__(AvatarAccessoriesManagerAI)
        ai.air = Mock()
        ai.air.doId2do = {} if avatar is None else {5: avatar}
        ai.air.getMsgSender.return_value = 1234
        ai.context = 0
        ai.callbacks = {}
        ai.clothing = {}
        ai.jewelry = {}
        ai.tattoos = {}
        ai.acceptOnce = Mock()
        ai.d_awardResult = Mock()
        return ai

    def test_award_ignored_when_avatar_elsewhere(self):
        ai = self.makeAI()
        ai.requestAward(1, AwardGlobals.GOLD, 5, 0, 100)
        ai.d_awardResult.assert_not_called()

    def test_gold_award(self):
        inventory = Mock()
        inventory.getStackQuantity.return_value = 50
        inventory.getStackLimit.return_value = 1000
        avatar = Mock()
        avatar.getInventory.return_value = inventory
        ai = self.makeAI(avatar)
        ai.requestAward(1, AwardGlobals.GOLD, 5, 0, 100)
        inventory.b_setStackQuantity.assert_called_with(InventoryType.GoldInPocket, 150)
        ai.d_awardResult.assert_called_with(1234, 1, True)

    def test_clothing_award_lands_in_wardrobe(self):
        avatar = types.SimpleNamespace(getGender=lambda: 'm', giveClothingMessage=Mock())
        ai = self.makeAI(avatar)
        ai.clothing[5] = []
        ai.sendUpdate = Mock()
        uid = clothingOfType(ClothingGlobals.HAT, 1)[0]
        ai.requestAward(1, AwardGlobals.CLOTHING, 5, uid, 3)
        fieldName, args = ai.sendUpdate.call_args[0]
        self.assertEqual(fieldName, 'requestClothingAddDB')
        self.assertEqual(args[3], [[uid, 3, 0]])
        self.assertEqual(ai.clothing[5], [[uid, 3, 0]])

        ai.responseClothingAddDB(args[0], 1, 5)
        avatar.giveClothingMessage.assert_called_with(uid, 3)
        ai.d_awardResult.assert_called_with(1234, 1, True)

    def test_award_for_other_gender_fails(self):
        avatar = types.SimpleNamespace(getGender=lambda: 'f', giveClothingMessage=Mock(), giveJewelryMessage=Mock())
        ai = self.makeAI(avatar)
        ai.sendUpdate = Mock()
        ai.requestAward(1, AwardGlobals.CLOTHING, 5, clothingOfType(ClothingGlobals.HAT, 1)[0], 0)
        ai.requestAward(2, AwardGlobals.JEWELRY, 5, 0, 1)
        ai.sendUpdate.assert_not_called()
        ai.d_awardResult.assert_any_call(1234, 1, False)
        ai.d_awardResult.assert_any_call(1234, 2, False)

    def test_tattoo_award_message(self):
        avatar = types.SimpleNamespace(getGender=lambda: 'f', giveTattooMessage=Mock())
        ai = self.makeAI(avatar)
        ai.sendUpdate = Mock()
        ai.requestAward(1, AwardGlobals.TATTOO, 5, 7, 1)
        context = ai.sendUpdate.call_args[0][1][0]
        ai.responseTattooAddDB(context, 1, 5, 7)
        avatar.giveTattooMessage.assert_called_with(7)
        ai.d_awardResult.assert_called_with(1234, 1, True)

    def test_unsupported_award_fails(self):
        ai = self.makeAI(Mock())
        ai.requestAward(2, AwardGlobals.HAIR_HAIR, 5, 1, 1)
        ai.d_awardResult.assert_called_with(1234, 2, False)

    def test_award_maker_success_and_timeout(self):
        taskMgr = Mock()
        with patch.object(builtins, 'taskMgr', taskMgr, create=True):
            maker = AwardMakerUD.__new__(AwardMakerUD)
            maker.air = Mock()
            maker.air.dclassesByName = {'AvatarAccessoriesManagerUD': Mock()}
            maker.doId = 4702
            maker.context = 0
            maker.pendingAwards = {}

            results = []
            context = maker.giveAward(5, AwardGlobals.GOLD, 0, 100, callback=results.append)
            maker.air.send.assert_called_once()
            maker.awardSuccess(context)
            maker.awardSuccess(context)

            context = maker.giveAward(5, AwardGlobals.STACK, 1, 1, callback=results.append)
            maker._AwardMakerUD__awardTimeout(context)

            self.assertEqual(maker.giveAward(5, 99, 0, 0, callback=results.append), 0)
            self.assertEqual(results, [True, False, False])
            self.assertEqual(maker.pendingAwards, {})


    def test_award_fields_pack_with_dc(self):
        from panda3d.direct import DCFile
        dcFile = DCFile()
        root = os.path.join(str(REPO_ROOT), 'astron', 'dclass')
        self.assertTrue(dcFile.read(os.path.join(root, 'otp.dc')))
        self.assertTrue(dcFile.read(os.path.join(root, 'pirates.dc')))
        dclass = dcFile.getClassByName('AvatarAccessoriesManager')
        dclass.aiFormatUpdate('requestAward', 4710, 4710, 1, [1, AwardGlobals.GOLD, 5, 0, 100])
        dclass.aiFormatUpdate('responseClothingFromDB', 4710, 1, 2, [1, [packClothing(2000, 30)]])
        dclass.aiFormatUpdate('requestClothingAddDB', 4710, 4710, 1, [1, 5, 0, [[2000, 30, 0]], 0, 0])
        dclass.aiFormatUpdate('requestClothingDropDB', 4710, 4710, 1, [1, 5, 0, 'm', 3])
        dclass.aiFormatUpdate('migrateDNAElements', 4710, 4710, 1, [0, 5, 0, [packClothing(160024, 20, 1)], 0])
        dcFile.getClassByName('AwardMaker').aiFormatUpdate('awardSuccess', 4702, 1, 2, [1])


if __name__ == '__main__':
    unittest.main()
