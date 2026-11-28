import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from otp.otpbase import OTPGlobals
from pirates.economy.EconomyGlobals import ItemId
from pirates.piratesbase import Freebooter, FreebooterAI, MembershipGlobals
from pirates.quest.QuestConstants import LocationIds
from pirates.reputation import ReputationGlobals
from pirates.ship import ShipGlobals
from pirates.uberdog import InventoryInit
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.uberdog.PirateInventoryAI import PirateInventoryAI
from pirates.uberdog.UberDogGlobals import InventoryType


def membership(enabled=True):
    return patch.object(MembershipGlobals, 'wantMembership', return_value=enabled)


def freebooter(**fields):
    return SimpleNamespace(doId=1000, isPaid=lambda: False, **fields)


def member(**fields):
    return SimpleNamespace(doId=1000, isPaid=lambda: True, **fields)


class AccessTests(unittest.TestCase):

    def test_everybody_has_unlimited_access_without_membership(self):
        with membership(False):
            for access in (OTPGlobals.AccessUnknown, OTPGlobals.AccessVelvetRope, OTPGlobals.AccessFull):
                self.assertTrue(FreebooterAI.isPaidAccess(access))
                self.assertEqual(FreebooterAI.getEffectiveAccess(access), OTPGlobals.AccessFull)
                self.assertEqual(MembershipGlobals.getMaxAvatars(access), 4)

    def test_only_full_access_is_paid_with_membership(self):
        with membership():
            self.assertTrue(FreebooterAI.isPaidAccess(OTPGlobals.AccessFull))
            self.assertFalse(FreebooterAI.isPaidAccess(OTPGlobals.AccessVelvetRope))
            self.assertFalse(FreebooterAI.isPaidAccess(OTPGlobals.AccessUnknown))
            self.assertEqual(FreebooterAI.getEffectiveAccess(OTPGlobals.AccessVelvetRope),
                OTPGlobals.AccessVelvetRope)
            self.assertEqual(MembershipGlobals.getMaxAvatars(OTPGlobals.AccessVelvetRope), 2)
            self.assertEqual(MembershipGlobals.getMaxAvatars(OTPGlobals.AccessFull), 4)

            with patch.object(Freebooter, 'AllAccessHoliday', True):
                self.assertTrue(FreebooterAI.isPaidAccess(OTPGlobals.AccessVelvetRope))

    def test_non_players_are_never_restricted(self):
        self.assertTrue(FreebooterAI.isPaid(SimpleNamespace()))
        self.assertFalse(FreebooterAI.isPaid(None))


class SlotTests(unittest.TestCase):

    def test_free_slots_are_filled_from_the_top(self):
        Available = OTPGlobals.AvatarSlotAvailable
        Unavailable = OTPGlobals.AvatarSlotUnavailable
        self.assertEqual(MembershipGlobals.getAvatarSlotStates([], 2), [Available, Available, Unavailable, Unavailable])
        self.assertEqual(MembershipGlobals.getAvatarSlotStates([3], 2), [Available, Unavailable, Unavailable, 3])
        self.assertEqual(MembershipGlobals.getAvatarSlotStates([0, 2, 3], 2), [0, Unavailable, 2, 3])
        self.assertEqual(MembershipGlobals.getAvatarSlotStates([1], 4), [Available, 1, Available, Available])


class RestrictionTests(unittest.TestCase):

    def test_weapons(self):
        self.assertFalse(FreebooterAI.canUseWeapon(freebooter(), InventoryType.DaggerRep))
        self.assertTrue(FreebooterAI.canUseWeapon(freebooter(), InventoryType.CutlassRep))
        self.assertTrue(FreebooterAI.canUseWeapon(member(), InventoryType.WandRep))

    def test_skills_ammo_and_ship_skills(self):
        for skillId in (InventoryType.CutlassSweep, InventoryType.PistolVenomShot, InventoryType.CannonChainShot,
                        InventoryType.SailFullSail):
            self.assertTrue(FreebooterAI.canUseSkill(freebooter(), skillId), skillId)

        for skillId in (InventoryType.CutlassBladestorm, InventoryType.PistolHexEaterShot, InventoryType.CannonFirebrand,
                        InventoryType.SailOpenFire):
            self.assertFalse(FreebooterAI.canUseSkill(freebooter(), skillId), skillId)
            self.assertTrue(FreebooterAI.canUseSkill(member(), skillId), skillId)

    def test_skill_training(self):
        # a free skill may be raised to rank 2 (quantity 3), six skill points
        # may be spent on a weapon...
        self.assertTrue(FreebooterAI.canTrainSkill(freebooter(), InventoryType.CutlassSweep, 3, 10, 4))
        self.assertFalse(FreebooterAI.canTrainSkill(freebooter(), InventoryType.CutlassSweep, 4, 10, 4))
        self.assertFalse(FreebooterAI.canTrainSkill(freebooter(), InventoryType.CutlassSweep, 3, 10, 3))
        self.assertFalse(FreebooterAI.canTrainSkill(freebooter(), InventoryType.CutlassBladestorm, 2, 10, 4))
        self.assertTrue(FreebooterAI.canTrainSkill(member(), InventoryType.CutlassBladestorm, 6, 30, 0))

    def test_store_items(self):
        for itemId in (ItemId.POTION_1, ItemId.VENOMSHOT, InventoryType.AmmoChainShot, InventoryType.AmmoAsp):
            self.assertTrue(FreebooterAI.canBuyItem(freebooter(), itemId), itemId)

        for itemId in (ItemId.CUTLASS_L2, ItemId.PISTOL_POUCH_L1):
            self.assertFalse(FreebooterAI.canBuyItem(freebooter(), itemId), itemId)
            self.assertTrue(FreebooterAI.canBuyItem(member(), itemId), itemId)

    def test_ships_and_areas(self):
        self.assertTrue(FreebooterAI.canUseShipClass(freebooter(), ShipGlobals.INTERCEPTORL1))
        self.assertTrue(FreebooterAI.canUseShipClass(freebooter(), ItemId.MERCHANT_L1))
        self.assertFalse(FreebooterAI.canUseShipClass(freebooter(), ShipGlobals.WARSHIPL1))
        self.assertTrue(FreebooterAI.canUseShipClass(member(), ShipGlobals.WARSHIPL1))

        self.assertFalse(FreebooterAI.canEnterArea(freebooter(), LocationIds.KINGSHEAD_ISLAND))
        self.assertFalse(FreebooterAI.canEnterArea(freebooter(), LocationIds.KINGSHEAD_DOOR))
        self.assertTrue(FreebooterAI.canEnterArea(freebooter(), LocationIds.PORT_ROYAL_ISLAND))
        self.assertTrue(FreebooterAI.canEnterArea(member(), LocationIds.KINGSHEAD_ISLAND))

    def test_quests_and_treasure_maps(self):
        velvet = SimpleNamespace(getVelvetRoped=lambda: True)
        free = SimpleNamespace(getVelvetRoped=lambda: False)
        self.assertFalse(FreebooterAI.canProgressQuest(freebooter(), velvet))
        self.assertTrue(FreebooterAI.canProgressQuest(freebooter(), free))
        self.assertTrue(FreebooterAI.canProgressQuest(member(), velvet))
        self.assertFalse(FreebooterAI.canStartTreasureMap(freebooter()))
        self.assertTrue(FreebooterAI.canStartTreasureMap(member()))

    def test_reputation_caps(self):
        weaponCap = ReputationGlobals.TotalReputationAtLevel[Freebooter.FreeLevelCap]
        overallCap = ReputationGlobals.GlobalReputationAtLevel[Freebooter.FreeOverallLevelCap]
        self.assertEqual(FreebooterAI.capReputation(freebooter(), InventoryType.CutlassRep, 0, weaponCap * 2), weaponCap)
        self.assertEqual(FreebooterAI.capReputation(freebooter(), InventoryType.SailingRep, 0, weaponCap * 2), weaponCap)
        self.assertEqual(FreebooterAI.capReputation(freebooter(), InventoryType.OverallRep, 0, overallCap * 2), overallCap)
        self.assertEqual(FreebooterAI.capReputation(freebooter(), InventoryType.GeneralRep, 0, 999999), 999999)
        self.assertEqual(FreebooterAI.capReputation(member(), InventoryType.CutlassRep, 0, weaponCap * 2), weaponCap * 2)

        # reputation earned as a member is kept, but no more is earned...
        self.assertEqual(FreebooterAI.capReputation(freebooter(), InventoryType.CutlassRep, weaponCap * 3, weaponCap * 4),
            weaponCap * 3)
        self.assertEqual(ReputationGlobals.getLevelFromTotalReputation(InventoryType.CutlassRep, weaponCap)[0],
            Freebooter.FreeLevelCap)

        self.assertTrue(FreebooterAI.isAtOverallLevelCap(freebooter(getLevel=lambda: 25)))
        self.assertFalse(FreebooterAI.isAtOverallLevelCap(freebooter(getLevel=lambda: 24)))
        self.assertFalse(FreebooterAI.isAtOverallLevelCap(member(getLevel=lambda: 40)))


class FakeAvatar:

    def __init__(self, paid):
        self.doId = 1000
        self.paid = paid
        self.level = 1
        self.maxHp = 100
        self.maxMojo = 50
        self.levelUps = []

    def isPaid(self):
        return self.paid

    def getLevel(self):
        return self.level

    def b_setLevel(self, level):
        self.level = level

    def getMaxHp(self):
        return self.maxHp

    def b_setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def getMaxMojo(self):
        return self.maxMojo

    def b_setMaxMojo(self, maxMojo):
        self.maxMojo = maxMojo

    def b_setHp(self, hp):
        pass

    def b_setMojo(self, mojo):
        pass

    def d_levelUpMsg(self, category, level, messageId):
        self.levelUps.append((category, level))

    def getInventory(self):
        return self.inventory


def makeInventory(avatar):
    inventory = PirateInventoryAI.__new__(PirateInventoryAI)
    DistributedInventoryBase.__init__(inventory, None)
    inventory.doId = 5000
    inventory.ownerId = avatar.doId
    inventory.air = Mock()
    inventory.air.doId2do = {avatar.doId: avatar}
    inventory.air.questMgr.hasQuest.return_value = False
    inventory.stackLimits = dict(InventoryInit.StackLimits)
    inventory.sendUpdate = Mock()
    inventory.sendUpdateToAvatarId = Mock()
    avatar.inventory = inventory
    return inventory


class InventoryTests(unittest.TestCase):

    def setUp(self):
        patcher = patch('builtins.messenger', Mock(), create=True)
        patcher.start()
        self.addCleanup(patcher.stop)

        # the inventory stores it's lists a moment after they change
        patcher = patch('builtins.taskMgr', Mock(), create=True)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_freebooters_stop_earning_reputation_at_the_caps(self):
        avatar = FakeAvatar(paid=False)
        inventory = makeInventory(avatar)
        inventory.setReputation(InventoryType.CutlassRep, 10 ** 6)
        self.assertEqual(inventory.getReputation(InventoryType.CutlassRep),
            ReputationGlobals.TotalReputationAtLevel[Freebooter.FreeLevelCap])
        self.assertEqual(avatar.levelUps[-1], (InventoryType.CutlassRep, Freebooter.FreeLevelCap))

        inventory.setOverallRep(10 ** 6)
        self.assertEqual(avatar.level, Freebooter.FreeOverallLevelCap)

        member = FakeAvatar(paid=True)
        inventory = makeInventory(member)
        rep = ReputationGlobals.TotalReputationAtLevel[Freebooter.FreeLevelCap + 3]
        inventory.setReputation(InventoryType.CutlassRep, rep)
        self.assertEqual(inventory.getReputation(InventoryType.CutlassRep), rep)

    def test_max_hp_and_mojo_rewards_raise_the_maximums(self):
        from pirates.quest.QuestReward import MaxHpReward, MaxMojoReward
        from pirates.trades.TradeAI import LocalTrade

        avatar = FakeAvatar(paid=True)
        inventory = makeInventory(avatar)
        trade = LocalTrade(Mock())
        trade.avatar = avatar

        MaxHpReward(amount=25).applyTo(trade, avatar)
        MaxMojoReward(amount=10).applyTo(trade, avatar)
        self.assertEqual((avatar.maxHp, avatar.maxMojo), (125, 60))
        self.assertEqual(inventory.getStackLimit(InventoryType.Hp), 125)
        self.assertEqual(inventory.getStackLimit(InventoryType.Mojo), 60)
        self.assertEqual(inventory.getStackQuantity(InventoryType.Hp), 0)

    def test_vitae_stacks_hold_the_jail_cost(self):
        avatar = FakeAvatar(paid=True)
        inventory = makeInventory(avatar)
        inventory.stackLimits[InventoryType.Vitae_Left] = 10000
        inventory.updateStackLimits()
        self.assertEqual(inventory.getStackLimit(InventoryType.Vitae_Left), InventoryInit.VitaeCost)

        inventory.b_setStackQuantity(InventoryType.Vitae_Cost, InventoryInit.VitaeCost)
        self.assertEqual(inventory.getStackQuantity(InventoryType.Vitae_Cost), 36000)


class KingsheadDoorTests(unittest.TestCase):

    def makeDoor(self, interiorUid):
        from pirates.world.DistributedBuildingDoorAI import DistributedBuildingDoorAI

        door = DistributedBuildingDoorAI.__new__(DistributedBuildingDoorAI)
        door.buildingUid = DistributedBuildingDoorAI.ZombieBuildingUid
        door.interiorUid = interiorUid
        door.interiorDoId = 0
        door.doId = 3000
        door.air = SimpleNamespace(doId2do={})
        door.notify = Mock()
        return door

    def test_only_members_enter_the_kingshead_fort(self):
        from pirates.world.DistributedDoorBaseAI import DistributedDoorBaseAI

        door = self.makeDoor(LocationIds.KINGSHEAD_DOOR)
        with patch.object(DistributedDoorBaseAI, 'handleRequestInteraction', return_value=1) as base:
            self.assertEqual(door.handleRequestInteraction(freebooter(zombie=0), 0, 0), door.DENY)
            base.assert_not_called()

            door.handleRequestInteraction(member(zombie=0), 0, 0)
            base.assert_called_once()

            door = self.makeDoor('1156207188.95dzlu')
            door.handleRequestInteraction(freebooter(zombie=0), 0, 0)
            self.assertEqual(base.call_count, 2)


if __name__ == '__main__':
    unittest.main()
