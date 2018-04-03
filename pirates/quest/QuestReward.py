# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestReward
import random
from direct.showbase.PythonUtil import POD, invertDict
from direct.directnotify import DirectNotifyGlobal
from pirates.quest import QuestRewardStruct
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory
from pirates.piratesbase import CollectionMap
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.economy import EconomyGlobals
from pirates.battle import EnemyGlobals
from pirates.minigame import PlayingCardDropper
from pirates.makeapirate import JewelryGlobals, TattooGlobals, ClothingGlobals
from pirates.economy.EconomyGlobals import ItemId
from pirates.piratesbase import Freebooter
REPFACTOR_HOLIDAY = 1
GOLDFACTOR_HOLIDAY = 1
REWARD_TO = 3

class QuestReward(POD):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestReward')
    DataSet = {'amount': 1, 'questId': ''}

    def __init__(self, amount=None, **kwArgs):
        if amount is not None:
            kwArgs['amount'] = amount
        POD.__init__(self, **kwArgs)
        return

    def applyTo(self, trade, av):
        raise 'derived must override'

    def getQuestRewardStruct(self):
        rewardStruct = QuestRewardStruct.QuestRewardStruct().copyFrom(self)
        rewardStruct.setRewardType(Class2DBId[self.__class__])
        return rewardStruct

    @staticmethod
    @exceptionLogged()
    def makeFromStruct(rewardStruct):
        return DBId2Class[rewardStruct.rewardType]().copyFrom(rewardStruct, strict=True)

    @staticmethod
    def getDescriptionText(rewards):
        if len(rewards) == 0:
            return ''
        if len(rewards) == 1:
            str = PLocalizer.QuestRewardDescS % rewards[0].getDescriptionText()
        else:
            rewardsStr = ''
            for reward in rewards:
                rewardsStr += PLocalizer.QuestRewardDescItem % reward.getDescriptionText()

            str = PLocalizer.QuestRewardDescM % rewardsStr
        return str


class GoldAmountReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        global GOLDFACTOR_HOLIDAY
        avId = av.getDoId()
        goldAmt = self.amount
        if Freebooter.getPaidStatusAI(avId) and (REWARD_TO == 2 or REWARD_TO == 3):
            goldAmt *= GOLDFACTOR_HOLIDAY
        else:
            if not Freebooter.getPaidStatusAI(avId) and (REWARD_TO == 1 or REWARD_TO == 3):
                goldAmt *= GOLDFACTOR_HOLIDAY
        trade.giveGoldInPocket(goldAmt)

    def getDescriptionText(self):
        goldAmt = self.amount
        text = PLocalizer.GoldRewardDesc % goldAmt
        if GOLDFACTOR_HOLIDAY == 2:
            text = +'\\ + ' + PLocalizer.LootGoldDouble % goldAmt
        return text

    def setGoldFactor(self, multiplier):
        global GOLDFACTOR_HOLIDAY
        GOLDFACTOR_HOLIDAY = multiplier


class GoldReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        avId = av.getDoId()
        goldAmt = EnemyGlobals.getMaxGoldDrop(None, self.amount, 5)
        if Freebooter.getPaidStatusAI(avId) and (REWARD_TO == 2 or REWARD_TO == 3):
            goldAmt *= GOLDFACTOR_HOLIDAY
        else:
            if not Freebooter.getPaidStatusAI(avId) and (REWARD_TO == 1 or REWARD_TO == 3):
                goldAmt *= GOLDFACTOR_HOLIDAY
        trade.giveGoldInPocket(goldAmt)
        return

    def getDescriptionText(self):
        goldAmt = EnemyGlobals.getMaxGoldDrop(None, self.amount, 5)
        text = PLocalizer.GoldRewardDesc % goldAmt
        if GOLDFACTOR_HOLIDAY == 2:
            text = +'\\ + ' + PLocalizer.LootGoldDouble % goldAmt
        return text

    def setGoldFactor(self, multiplier):
        global GOLDFACTOR_HOLIDAY
        GOLDFACTOR_HOLIDAY = multiplier


class PlayingCardReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        for i in range(self.amount):
            cardId = random.randint(0, 51)
            trade.giveStack(InventoryType.begin_Cards + cardId, 1)

        av.giveCardMessage(InventoryType.begin_Cards + cardId)

    def getDescriptionText(self):
        if self.amount > 1:
            return PLocalizer.PlayingCardRewardDescPlural % self.amount
        else:
            return PLocalizer.PlayingCardRewardDesc % self.amount


class PlayingCardTier0Reward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        card = PlayingCardDropper.dropTier0()
        trade.givePlayingCard(card)
        av.giveCardMessage(card)

    def getDescriptionText(self):
        return PLocalizer.PlayingCardRewardDesc % self.amount


class PlayingCardTier1Reward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        card = PlayingCardDropper.dropTier1()
        trade.givePlayingCard(card)
        av.giveCardMessage(card)

    def getDescriptionText(self):
        return PLocalizer.PlayingCardRewardDesc % self.amount


class PlayingCardTier2Reward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        card = PlayingCardDropper.dropTier2()
        trade.givePlayingCard(card)
        av.giveCardMessage(card)

    def getDescriptionText(self):
        return PLocalizer.PlayingCardRewardDesc % self.amount


class PlayingCardTier3Reward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        card = PlayingCardDropper.dropTier3()
        trade.givePlayingCard(card)
        av.giveCardMessage(card)

    def getDescriptionText(self):
        return PLocalizer.PlayingCardRewardDesc % self.amount


class MaxHpReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveStack(InventoryType.Hp, self.amount)

    def getDescriptionText(self):
        return PLocalizer.MaxHpRewardDesc % self.amount


class MaxMojoReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveStack(InventoryType.Mojo, self.amount)

    def getDescriptionText(self):
        return PLocalizer.MaxMojoRewardDesc % self.amount


class LuckReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        raise 'TODO'

    def getDescriptionText(self):
        return PLocalizer.LuckRewardDesc % self.amount


class SwiftnessReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        raise 'TODO'

    def getDescriptionText(self):
        return PLocalizer.SwiftnessRewardDesc % self.amount


class CollectReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        if self.amount >= InventoryType.begin_Collections and self.amount < InventoryType.end_Collections:
            trade.giveStackableTypeLimit(self.amount, 2)
            trade.giveStack(self.amount, 1)
            for i in range(CollectionMap.Collection_Set_Sizes[self.amount]):
                curItem = 1 + self.amount + i
                trade.giveStackableTypeLimit(curItem, 99)

    def getDescriptionText(self):
        return PLocalizer.Collections[self.amount]


class TreasureMapReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveNewTreasureMap('DistributedTreasureMap')

    def getDescriptionText(self):
        return PLocalizer.TreasureMapDesc


class ShipReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        if av.constructedShipDoId:
            trade.giveShip(av.constructedShipDoId)
            trade.giveNewShipToken()
        av.constructedShipDoId = None
        return

    def getDescriptionText(self):
        return PLocalizer.ShipRewardDesc


class PistolUpgradeReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        if self.amount == ItemId.PISTOL_L1:
            trade.giveStack(InventoryType.PistolWeaponL1, 1)
        else:
            if self.amount == ItemId.PISTOL_L2:
                trade.giveStack(InventoryType.PistolWeaponL2, 1)
            else:
                if self.amount == ItemId.PISTOL_L3:
                    trade.giveStack(InventoryType.PistolWeaponL3, 1)
                else:
                    if self.amount == ItemId.PISTOL_L4:
                        trade.giveStack(InventoryType.PistolWeaponL4, 1)
                    else:
                        if self.amount == ItemId.PISTOL_L5:
                            trade.giveStack(InventoryType.PistolWeaponL5, 1)
                        else:
                            if self.amount == ItemId.PISTOL_L6:
                                trade.giveStack(InventoryType.PistolWeaponL6, 1)
                            else:
                                return
        av.giveWeaponMessage(self.amount)

    def getDescriptionText(self):
        if PLocalizer.InventoryTypeNames.has_key(self.amount):
            return PLocalizer.InventoryTypeNames.get(self.amount)
        else:
            return PLocalizer.PistolRewardDesc


class PistolReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.givePistolTraining()

    def getDescriptionText(self):
        return PLocalizer.PistolRewardDesc


class DollReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveDollTraining()
        trade.giveStack(InventoryType.DollWeaponL1, 1)

    def getDescriptionText(self):
        return PLocalizer.DollRewardDesc


class DaggerUpgradeReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        if self.amount == ItemId.DAGGER_L1:
            trade.giveStack(InventoryType.DaggerWeaponL1, 1)
        else:
            if self.amount == ItemId.DAGGER_L2:
                trade.giveStack(InventoryType.DaggerWeaponL2, 1)
            else:
                if self.amount == ItemId.DAGGER_L3:
                    trade.giveStack(InventoryType.DaggerWeaponL3, 1)
                else:
                    if self.amount == ItemId.DAGGER_L4:
                        trade.giveStack(InventoryType.DaggerWeaponL4, 1)
                    else:
                        if self.amount == ItemId.DAGGER_L5:
                            trade.giveStack(InventoryType.DaggerWeaponL5, 1)
                        else:
                            if self.amount == ItemId.DAGGER_L6:
                                trade.giveStack(InventoryType.DaggerWeaponL6, 1)
                            else:
                                return
        av.giveWeaponMessage(self.amount)

    def getDescriptionText(self):
        if PLocalizer.InventoryTypeNames.has_key(self.amount):
            return PLocalizer.InventoryTypeNames.get(self.amount)
        else:
            return PLocalizer.DaggerRewardDesc


class CutlassUpgradeReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        if self.amount == ItemId.CUTLASS_L1:
            trade.giveStack(InventoryType.CutlassWeaponL1, 1)
        else:
            if self.amount == ItemId.CUTLASS_L2:
                trade.giveStack(InventoryType.CutlassWeaponL2, 1)
            else:
                if self.amount == ItemId.CUTLASS_L3:
                    trade.giveStack(InventoryType.CutlassWeaponL3, 1)
                else:
                    if self.amount == ItemId.CUTLASS_L4:
                        trade.giveStack(InventoryType.CutlassWeaponL4, 1)
                    else:
                        if self.amount == ItemId.CUTLASS_L5:
                            trade.giveStack(InventoryType.CutlassWeaponL5, 1)
                        else:
                            if self.amount == ItemId.CUTLASS_L6:
                                trade.giveStack(InventoryType.CutlassWeaponL6, 1)
                            else:
                                return
        av.giveWeaponMessage(self.amount)

    def getDescriptionText(self):
        if PLocalizer.InventoryTypeNames.has_key(self.amount):
            return PLocalizer.InventoryTypeNames.get(self.amount)
        else:
            return PLocalizer.CutlassRewardDesc


class DollUpgradeReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        if self.amount == ItemId.DOLL_L1:
            trade.giveStack(InventoryType.DollWeaponL1, 1)
        else:
            if self.amount == ItemId.DOLL_L2:
                trade.giveStack(InventoryType.DollWeaponL2, 1)
            else:
                if self.amount == ItemId.DOLL_L3:
                    trade.giveStack(InventoryType.DollWeaponL3, 1)
                else:
                    if self.amount == ItemId.DOLL_L4:
                        trade.giveStack(InventoryType.DollWeaponL4, 1)
                    else:
                        if self.amount == ItemId.DOLL_L5:
                            trade.giveStack(InventoryType.DollWeaponL5, 1)
                        else:
                            if self.amount == ItemId.DOLL_L6:
                                trade.giveStack(InventoryType.DollWeaponL6, 1)
                            else:
                                return
        av.giveWeaponMessage(self.amount)

    def getDescriptionText(self):
        if PLocalizer.InventoryTypeNames.has_key(self.amount):
            return PLocalizer.InventoryTypeNames.get(self.amount)
        else:
            return PLocalizer.DollRewardDesc


class WandUpgradeReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        if self.amount == ItemId.WAND_L1:
            trade.giveStack(InventoryType.WandWeaponL1, 1)
        else:
            if self.amount == ItemId.WAND_L2:
                trade.giveStack(InventoryType.WandWeaponL2, 1)
            else:
                if self.amount == ItemId.WAND_L3:
                    trade.giveStack(InventoryType.WandWeaponL3, 1)
                else:
                    if self.amount == ItemId.WAND_L4:
                        trade.giveStack(InventoryType.WandWeaponL4, 1)
                    else:
                        if self.amount == ItemId.WAND_L5:
                            trade.giveStack(InventoryType.WandWeaponL5, 1)
                        else:
                            if self.amount == ItemId.WAND_L6:
                                trade.giveStack(InventoryType.WandWeaponL6, 1)
                            else:
                                return
        av.giveWeaponMessage(self.amount)

    def getDescriptionText(self):
        if PLocalizer.InventoryTypeNames.has_key(self.amount):
            return PLocalizer.InventoryTypeNames.get(self.amount)
        else:
            return PLocalizer.DollRewardDesc


class DaggerReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveDaggersTraining()
        trade.giveStack(InventoryType.DaggerWeaponL1, 1)

    def getDescriptionText(self):
        return PLocalizer.DaggerRewardDesc


class GrenadeReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveGrenadeTraining()
        trade.giveStack(InventoryType.GrenadeWeaponL1, 1)
        trade.giveStack(InventoryType.GrenadeExplosion, 2)

    def getDescriptionText(self):
        return PLocalizer.GrenadeRewardDesc


class StaffReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveWandTraining()
        trade.giveStack(InventoryType.WandWeaponL1, 1)

    def getDescriptionText(self):
        return PLocalizer.StaffRewardDesc


class TeleportTotemReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveTortugaTeleportToken()

    def getDescriptionText(self):
        return PLocalizer.TeleportTotemRewardDesc


class CubaTeleportReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveCubaTeleportToken()

    def getDescriptionText(self):
        return PLocalizer.CubaTeleportRewardDesc


class PortRoyalTeleportReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.givePortRoyalTeleportToken()

    def getDescriptionText(self):
        return PLocalizer.PortRoyalTeleportRewardDesc


class PadresDelFuegoTeleportReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.givePadresDelFuegoTeleportToken()

    def getDescriptionText(self):
        return PLocalizer.PadresDelFuegoTeleportRewardDesc


class KingsHeadTeleportReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveKingsheadTeleportToken()

    def getDescriptionText(self):
        return PLocalizer.KingsHeadTeleportRewardDesc


class MainStoryReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        if not av.checkQuestRewardFlag(PiratesGlobals.QRFlagMainStory):
            av.assignQuestRewardFlag(PiratesGlobals.QRFlagMainStory)
            trade.giveStackableTypeLimit(InventoryType.SailPowerRecharge, 2)
            trade.giveStack(InventoryType.SailPowerRecharge, 2)

    def getDescriptionText(self):
        return PLocalizer.Chapter3RewardDesc


class ReputationReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        global REPFACTOR_HOLIDAY
        avId = av.getDoId()
        rewardAmount = self.amount
        if Freebooter.getPaidStatusAI(avId) and (REWARD_TO == 2 or REWARD_TO == 3):
            rewardAmount = self.amount * REPFACTOR_HOLIDAY
        else:
            if not Freebooter.getPaidStatusAI(avId) and (REWARD_TO == 1 or REWARD_TO == 3):
                rewardAmount = self.amount * REPFACTOR_HOLIDAY
        if av.getTempDoubleXPReward():
            rewardAmount = rewardAmount * 2
        trade.giveReputation(InventoryType.GeneralRep, rewardAmount)

    def getDescriptionText(self):
        rewardAmount = self.amount * REPFACTOR_HOLIDAY
        return PLocalizer.ReputationRewardDesc % rewardAmount

    def setReputationFactor(self, multiplier):
        global REPFACTOR_HOLIDAY
        REPFACTOR_HOLIDAY = multiplier


class SpecialQuestReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        av.acceptSpecialQuestReward(self.questId, trade)

    def getDescriptionText(self):
        return PLocalizer.SpecialQuestRewardDesc


class JewelryQuestReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        gender = av.dna.getGender()
        questDrop = JewelryGlobals.questDrops.get(self.amount)
        if questDrop is None:
            return
        if gender == 'm':
            uid = questDrop[0]
            if not uid >= JewelryGlobals.MALE_RBROW or not uid <= JewelryGlobals.MALE_RHAND + 9999:
                return
        else:
            uid = questDrop[1]
            if not uid >= JewelryGlobals.FEMALE_RBROW or not uid <= JewelryGlobals.FEMALE_RHAND + 9999:
                return
        simbase.air.avatarAccessoriesManager.requestJewelryAdd(av.getDoId(), uid, forceAdd=True)
        av.giveJewelryMessage(uid)
        simbase.air.writeServerEvent('QUEST_JEWELRY_ADDED', av.getDoId(), 'UID=%s|' % uid)
        return

    def getDescriptionText(self):
        return PLocalizer.JewelryQuestRewardDesc


class TattooQuestReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        doId = av.getDoId()
        keys = TattooGlobals.tattoos.keys()
        questDrop = TattooGlobals.questDrops.get(self.amount)
        for drop in questDrop:
            if drop in keys:
                simbase.air.avatarAccessoriesManager.requestTattooAdd(doId, drop, forceAdd=True)
                av.giveTattooMessage(drop)
                simbase.air.writeServerEvent('QUEST_TATTOO_ADDED', doId, 'UID=%s|' % drop)

    def getDescriptionText(self):
        return PLocalizer.TattooQuestRewardDesc


class ClothingQuestReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        doId = av.getDoId()
        gender = av.dna.getGender()
        keys = ClothingGlobals.UNIQUE_ID.keys()
        questDrop = ClothingGlobals.questDrops.get(self.amount)
        if questDrop is None:
            return
        dropForGender = questDrop.get(gender)
        if dropForGender is None:
            return
        dropId = dropForGender[0]
        colorId = dropForGender[1]
        if dropId in keys:
            simbase.air.avatarAccessoriesManager.requestClothingAdd(doId, dropId, colorId, forceAdd=True)
            av.giveClothingMessage(dropId, colorId)
            simbase.air.writeServerEvent('QUEST_CLOTHING_ADDED', doId, 'UID=%s|' % dropId)
        return

    def getDescriptionText(self):
        return PLocalizer.ClothingQuestRewardDesc


class TempDoubleRepReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        av.updateTempDoubleXPReward(self.amount)

    def getDescriptionText(self):
        return PLocalizer.Temp2xRepQuestRewardDesc


DBId2Class = {0: GoldReward, 1: MaxHpReward, 2: MaxMojoReward, 3: LuckReward, 4: SwiftnessReward, 5: TreasureMapReward, 6: CollectReward, 7: ShipReward, 8: ReputationReward, 9: PistolReward, 10: SpecialQuestReward, 11: DollReward, 12: DaggerReward, 13: PlayingCardReward, 14: GrenadeReward, 15: StaffReward, 16: TeleportTotemReward, 17: PlayingCardTier0Reward, 18: PlayingCardTier1Reward, 19: PlayingCardTier2Reward, 20: PlayingCardTier3Reward, 21: CubaTeleportReward, 22: PortRoyalTeleportReward, 23: PadresDelFuegoTeleportReward, 24: KingsHeadTeleportReward, 25: GoldAmountReward, 26: MainStoryReward, 27: JewelryQuestReward, 28: TattooQuestReward, 29: ClothingQuestReward, 30: PistolUpgradeReward, 31: DaggerUpgradeReward, 32: CutlassUpgradeReward, 33: DollUpgradeReward, 34: WandUpgradeReward, 35: TempDoubleRepReward}
Class2DBId = invertDict(DBId2Class)
# okay decompiling .\pirates\quest\QuestReward.pyc
