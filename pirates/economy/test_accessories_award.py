import builtins
import dbm.dumb
import os
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

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
)
from pirates.economy.AwardMakerUD import AwardMakerUD
from pirates.makeapirate import ClothingGlobals
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
        self.assertEqual(results, [True, [[uid, 3]], True, False, []])
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


class AwardTests(unittest.TestCase):
    def makeAI(self, avatar=None):
        ai = AvatarAccessoriesManagerAI.__new__(AvatarAccessoriesManagerAI)
        ai.air = Mock()
        ai.air.doId2do = {} if avatar is None else {5: avatar}
        ai.air.getMsgSender.return_value = 1234
        ai.context = 0
        ai.callbacks = {}
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

    def test_unsupported_award_fails(self):
        ai = self.makeAI(Mock())
        ai.requestAward(2, AwardGlobals.HAIR_HAIR, 5, 1, 1)
        ai.d_awardResult.assert_called_with(1234, 2, False)

    def test_award_maker_success_and_timeout(self):
        taskMgr = Mock()
        with patch.object(builtins, 'taskMgr', taskMgr, create=True):
            maker = AwardMakerUD.__new__(AwardMakerUD)
            maker.air = Mock()
            maker.air.dclassesByName = {'AvatarAccessoriesManager': Mock()}
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
        root = os.path.join(os.path.dirname(__file__), '..', '..', 'astron', 'dclass')
        self.assertTrue(dcFile.read(os.path.join(root, 'otp.dc')))
        self.assertTrue(dcFile.read(os.path.join(root, 'pirates.dc')))
        dclass = dcFile.getClassByName('AvatarAccessoriesManager')
        dclass.aiFormatUpdate('requestAward', 4710, 4710, 1, [1, AwardGlobals.GOLD, 5, 0, 100])
        dclass.aiFormatUpdate('responseClothingFromDB', 4710, 1, 2, [1, [packClothing(2000, 30)]])
        dclass.aiFormatUpdate('requestClothingAddDB', 4710, 4710, 1, [1, 5, 0, [[2000, 30, 0]], 0, 0])
        dclass.aiFormatUpdate('requestClothingDropDB', 4710, 4710, 1, [1, 5, 0, 'm', 3])
        dcFile.getClassByName('AwardMaker').aiFormatUpdate('awardSuccess', 4702, 1, 2, [1])


if __name__ == '__main__':
    unittest.main()
