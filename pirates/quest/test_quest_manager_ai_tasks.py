import builtins
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from direct.showbase.MessengerGlobal import messenger
from panda3d.direct import DCFile, DCPacker

from pirates.quest.test_quest_manager_ai_progression import manager_module
from pirates.quest.DistributedQuestAvatarAI import DistributedQuestAvatarAI
from pirates.quest.DistributedQuestGiverAI import DistributedQuestGiverAI
from pirates.quest import QuestDB, QuestEvent
from pirates.quest.Quest import Quest
from pirates.quest.QuestBase import QuestBase
from pirates.quest.QuestConstants import NPCIds, LocationIds, PropIds
from pirates.quest.QuestOffer import QuestOffer
from pirates.quest.QuestLadderOffer import QuestLadderOffer
from pirates.quest.QuestRewardStruct import QuestRewardStruct
from pirates.quest.QuestStatus import QuestStatus
from pirates.quest.QuestTaskState import QuestTaskState
from pirates.pirate import AvatarTypes
from pirates.pirate.AvatarType import AvatarType
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


def loadTownfolk():
    modules = {}
    for path in ('pirates.battle.DistributedBattleNPCAI', 'pirates.economy.DistributedShopKeeperAI'):
        module = types.ModuleType(path)
        name = path.rsplit('.', 1)[1]
        setattr(module, name, type(name, (), {}))
        modules[path] = module

    spec = importlib.util.spec_from_file_location('_quest_tasks_townfolk_test',
        Path(__file__).parent.parent / 'npc' / 'DistributedNPCTownfolkAI.py')
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(module)

    return module.DistributedNPCTownfolkAI


DistributedNPCTownfolkAI = loadTownfolk()


class FakeQuest(Quest, QuestBase):

    def __init__(self, doId, questId, holder, giverId=''):
        dna = QuestDB.QuestDict[questId]
        Quest.__init__(self, questId, giverId, dna.getInitialTaskStates(holder), dna.getRewards())
        self.doId = doId
        self.requestDelete = Mock()

    def getTaskStates(self):
        return self.taskStates


class FakeInventory:

    def __init__(self, manager, avatar):
        self.manager = manager
        self.avatar = avatar
        self.ids = []
        self.gold = 0
        self.reputation = {}

    def getDoIdListCategory(self, category):
        return list(self.ids)

    def setQuestList(self, ids):
        self.ids = list(ids)

    def getQuestList(self):
        quests = self.manager.quests.get(self.avatar.doId, {})
        return [quests[doId] for doId in self.ids if doId in quests]

    def getGoldInPocket(self):
        return self.gold

    def setGoldInPocket(self, gold):
        self.gold = gold

    def getReputation(self, repType):
        return self.reputation.get(repType, 0)


class FakeAvatar(DistributedQuestAvatarAI):

    def __init__(self, air, doId=1):
        DistributedQuestAvatarAI.__init__(self, air)
        self.doId = doId
        self.level = 1
        self.tutorial = PiratesGlobals.TUT_FINISHED if hasattr(PiratesGlobals, 'TUT_FINISHED') else 100
        self.location = 'location'
        self.inventory = None
        self.updates = []

    def getDoId(self):
        return self.doId

    def uniqueName(self, name):
        return '%s-%d' % (name, self.doId)

    def getTempDoubleXPReward(self):
        return 0

    def giveCardMessage(self, cardId):
        self.updates.append(('sendCardMessage', [cardId]))

    def getParentObj(self):
        return types.SimpleNamespace(getUniqueId=lambda: self.location)

    def getInventory(self):
        return self.inventory

    def getLevel(self):
        return self.level

    def getAccess(self):
        return 2

    def getTutorial(self):
        return self.tutorial

    def b_setTutorial(self, tutorial):
        self.tutorial = tutorial

    def sendUpdate(self, fieldName, args=[]):
        self.updates.append((fieldName, args))

    def sendUpdateToAvatarId(self, avatarId, fieldName, args=[]):
        self.updates.append((fieldName, args))


class QuestHarness:

    def __init__(self):
        self.air = types.SimpleNamespace(doId2do={}, logPotentialHacker=Mock(),
            tradeMgr=types.SimpleNamespace(createTrade=lambda avatarId: self.trade))
        self.trade = types.SimpleNamespace(giveReputation=Mock(), giveGoldInPocket=Mock(),
            giveStack=Mock(), giveCutlassTraining=Mock())
        self.manager = manager_module.QuestManagerAI(self.air)
        self.air.questMgr = self.manager
        self.avatar = FakeAvatar(self.air)
        self.air.doId2do[self.avatar.doId] = self.avatar
        self.inventory = FakeInventory(self.manager, self.avatar)
        self.avatar.inventory = self.inventory
        status = QuestStatus.__new__(QuestStatus)
        status.av, status.ladders, status.choiceContainers = self.avatar, {}, {}
        status.NPCInteractMode, status.cacheHistoryMode = False, False
        status.ladderDeleteList = []
        status.initialized = True
        self.avatar.questStatus = status
        self.manager.quests[self.avatar.doId] = {}
        self.nextDoId = 100
        self.created = []
        self.manager.createQuest = self.createQuest
        self.manager.createQuests = self.createQuests

    def addQuest(self, questId):
        doId = self.nextDoId
        self.nextDoId += 1
        giverId = self.manager.getQuestGiverId(self.avatar)
        offer = self.manager.popQuestOffer(self.avatar, questId)
        quest = FakeQuest(doId, questId, self.avatar, giverId)
        if offer:
            quest.setTaskStates(list(offer.getInitialTaskStates()))
            quest.setRewardStructs(offer.getRewardStructs())

        self.manager.quests[self.avatar.doId][doId] = quest
        self.inventory.ids.append(doId)
        self.avatar.questStatus.assignQuest(quest, True)
        self.created.append(quest)
        return quest

    def createQuest(self, avatar, questId, callback=None):
        quest = self.addQuest(questId)
        if callback:
            callback(quest)

    def createQuests(self, avatar, questIds, callback=None):
        for questId in questIds:
            self.addQuest(questId)

        if callback:
            callback()

    def getQuestIds(self):
        return sorted(quest.getQuestId() for quest in self.inventory.getQuestList())


class FakeNPC(manager_module.DistributedNPCTownfolkAI):
    notify = DistributedQuestGiverAI.notify
    d_setQuestOffer = DistributedQuestGiverAI.d_setQuestOffer
    d_setQuestLadderOffer = DistributedQuestGiverAI.d_setQuestLadderOffer
    getOffers = DistributedQuestGiverAI.getOffers
    setOfferResponse = DistributedQuestGiverAI.setOfferResponse
    offerQuests = DistributedNPCTownfolkAI.offerQuests
    handleOfferResponse = DistributedNPCTownfolkAI.handleOfferResponse


def makeNPC(uniqueId, doId=500):
    npc = FakeNPC()
    npc.doId = doId
    npc.getUniqueId = lambda: uniqueId
    npc.d_setQuestsCompleted = Mock()
    return npc


class QuestTaskTests(unittest.TestCase):

    def setUp(self):
        self.messengerPatch = patch.object(builtins, 'messenger', messenger, create=True)
        self.messengerPatch.start()
        self.paidPatch = patch('pirates.piratesbase.Freebooter.getPaidStatusAI', return_value=True)
        self.paidPatch.start()
        self.harness = QuestHarness()
        self.manager = self.harness.manager
        self.avatar = self.harness.avatar

    def tearDown(self):
        for quest in self.harness.created:
            for ladder in list(self.avatar.questStatus.ladders.values()):
                ladder.destroy()

        self.avatar.questStatus.ladders = {}
        self.manager.ignoreAll()
        self.paidPatch.stop()
        self.messengerPatch.stop()

    def visit(self, npc):
        result = self.manager.requestInteract(self.avatar, npc)
        messenger.send(self.avatar.uniqueName('interact-canceled'))
        return result

    def test_quest_giver_is_the_npc_the_avatar_is_talking_to(self):
        npc = makeNPC(NPCIds.BLACK_MACK)
        self.visit(npc)
        quest = self.harness.addQuest('ccbm.1poker')
        self.assertEqual(quest.getGiverId(), NPCIds.BLACK_MACK)

    def test_offers_are_gated_by_giver_level_history_and_active_quests(self):
        offers = self.manager.getQuestOffers(self.avatar, NPCIds.BLACK_MACK)
        self.assertEqual([offer.getQuestId() for offer in offers], ['ccbm.1poker'])
        self.assertIsInstance(offers[0], QuestOffer)
        self.assertEqual(self.manager.getQuestOffers(self.avatar, 'nobody'), [])

        tier2 = QuestDB.QuestDict['cards.prt2.recoverNavyMuskets']
        self.assertFalse(self.manager.canOfferQuest(self.avatar, tier2.getQuestId(), tier2,
            NPCIds.PORT_ROYAL_CARD_GIVER if hasattr(NPCIds, 'PORT_ROYAL_CARD_GIVER') else
            tier2.getPrereqs()[0].questGivers[0]))

        self.avatar.level = tier2.getMinLevel()
        self.assertTrue(self.manager.canOfferQuest(self.avatar, tier2.getQuestId(), tier2,
            tier2.getPrereqs()[0].questGivers[0]))

        # acquire once quest ladders are never offered again once completed
        ladderInt = self.manager.questDynMap.findQuestLadderInt(tier2.getQuestId())
        self.avatar.questLadderHistory = [ladderInt]
        self.assertFalse(self.manager.canOfferQuest(self.avatar, tier2.getQuestId(), tier2,
            tier2.getPrereqs()[0].questGivers[0]))

        self.harness.addQuest('ccbm.1poker')
        self.assertEqual(self.manager.getQuestOffers(self.avatar, NPCIds.BLACK_MACK), [])

    def test_quest_offers_pack_against_the_dclass(self):
        dcFile = DCFile()
        self.assertTrue(dcFile.read('astron/dclass/otp.dc'))
        self.assertTrue(dcFile.read('astron/dclass/pirates.dc'))
        for name, classDef in (('QuestOffer', QuestOffer), ('QuestLadderOffer', QuestLadderOffer),
                               ('QuestTaskState', QuestTaskState), ('QuestRewardStruct', QuestRewardStruct),
                               ('AvatarType', AvatarType)):
            dcFile.getClassByName(name).setClassDef(classDef)

        dclass = dcFile.getClassByName('DistributedQuestGiver')
        npc = makeNPC(NPCIds.BLACK_MACK)
        npc.air = self.harness.air
        npc.avatar2offers = {}
        sent = []
        npc.sendUpdateToAvatarId = lambda avatarId, fieldName, args: sent.append((fieldName, args))
        npc.offerQuests(self.avatar)

        fieldName, args = sent[-1]
        self.assertEqual(fieldName, 'setQuestOffer')
        field = dclass.getFieldByName(fieldName)
        packer = DCPacker()
        packer.beginPack(field)
        field.packArgs(packer, args)
        self.assertTrue(packer.endPack())

        unpacker = DCPacker()
        unpacker.setUnpackData(packer.getBytes())
        unpacker.beginUnpack(field)
        offers = field.unpackArgs(unpacker)[0]
        self.assertTrue(unpacker.endUnpack())
        self.assertEqual(offers[0].getQuestId(), 'ccbm.1poker')
        self.assertEqual([reward.getAmount() for reward in offers[0].getRewards()],
                         [reward.getAmount() for reward in QuestDB.QuestDict['ccbm.1poker'].getRewards()])

        # quest choices are offered as ladder offers, not as the raw
        # quest container objects which can not be packed...
        offer = self.manager.getQuestLadderOffers(self.avatar, [
            types.SimpleNamespace(getName=lambda: 'c3r1.1sinkNavyShips', getTitle=lambda: '',
                                  getRewards=lambda: QuestDB.QuestDict['c3r1.1sinkNavyShips'].getRewards())])
        field = dclass.getFieldByName('setQuestLadderOffer')
        packer = DCPacker()
        packer.beginPack(field)
        field.packArgs(packer, [offer, 1])
        self.assertTrue(packer.endPack())

    def test_accepting_an_offer_creates_the_offered_quest(self):
        npc = makeNPC(NPCIds.BLACK_MACK)
        npc.air = self.harness.air
        npc.avatar2offers = {}
        npc.sendUpdateToAvatarId = Mock()
        npc.offerQuests(self.avatar)
        offer = npc.getOffers(self.avatar.doId)[0]
        offer.getInitialTaskStates()[0].setGoal(7)
        self.harness.air.getAvatarIdFromSender = lambda: self.avatar.doId
        npc.setOfferResponse(0, 0)
        quest = self.manager.getQuest(self.avatar, questId='ccbm.1poker')
        self.assertIsNotNone(quest)
        self.assertEqual(quest.getGiverId(), NPCIds.BLACK_MACK)
        self.assertEqual(quest.getTaskStates()[0].getGoal(), 7)

        # offers that were never made are rejected
        self.manager.acceptQuestOffer(self.avatar, makeNPC('nobody'),
            QuestOffer.create('ccbm.1poker', self.avatar), False)
        self.harness.air.logPotentialHacker.assert_called_once()

    def test_field_completed_quest_waits_to_be_returned(self):
        self.manager.setQuestGiverId(self.avatar, NPCIds.BLACK_MACK)
        quest = self.harness.addQuest('ccbm.1poker')
        self.manager.pokerHandWon(self.avatar, QuestDB.QuestDict['ccbm.1poker'].getTasks()[0].getGold())
        self.assertTrue(quest.isComplete())
        self.assertNotIn(19945, self.avatar.getQuestHistory())

        other = makeNPC('someone-else')
        self.visit(other)
        other.d_setQuestsCompleted.assert_not_called()
        self.assertNotIn(19945, self.avatar.getQuestHistory())

        mack = makeNPC(NPCIds.BLACK_MACK)
        self.manager.requestInteract(self.avatar, mack)
        mack.d_setQuestsCompleted.assert_called_once_with(
            self.avatar.doId, completedQuestIds=['ccbm.1poker'], completedQuestDoIds=[quest.doId])
        self.assertNotIn(19945, self.avatar.getQuestHistory())
        messenger.send(self.avatar.uniqueName('interact-canceled'))
        self.assertIn(19945, self.avatar.getQuestHistory())
        self.harness.trade.giveReputation.assert_called_once()
        self.assertIsNone(self.manager.getQuest(self.avatar, questId='ccbm.1poker'))

    def test_defeat_progress_applies_to_every_quest(self):
        first = self.harness.addQuest('c3r1.2defeatNavyGuards')
        second = self.harness.addQuest('c2.2defeatSkeletons')
        enemy = types.SimpleNamespace(getAvatarType=lambda: AvatarTypes.Navy, getLevel=lambda: 5,
                                      getCurrentWeapon=lambda: (0, 0), getUniqueId=lambda: '')
        self.manager.enemyDefeated(self.avatar, enemy)
        self.assertEqual(first.getTaskProgress(), [(1, 4)])
        self.assertEqual(second.getTaskProgress(), [(0, 1)])

    def test_named_enemies_raise_npc_defeated(self):
        dnaId = [questId for questId, dna in QuestDB.QuestDict.items()
                 if any(task.__class__.__name__ == 'DefeatNPCTaskDNA' for task in dna.getTasks())][0]
        quest = self.harness.addQuest(dnaId)
        task = QuestDB.QuestDict[dnaId].getTasks()[0]
        enemy = types.SimpleNamespace(getAvatarType=lambda: AvatarTypes.Navy, getLevel=lambda: 5,
                                      getCurrentWeapon=lambda: (0, 0), getUniqueId=lambda: task.getNpcId())
        self.avatar.location = LocationIds.ANY_LOCATION
        with patch.object(task.__class__, 'locationMatches', return_value=True):
            self.manager.enemyDefeated(self.avatar, enemy)

        self.assertTrue(quest.getTaskStates()[0].isComplete())

    def test_sinking_a_ship_credits_the_attacking_crew(self):
        quest = self.harness.addQuest('c3r1.1sinkNavyShips')
        attacker = manager_module.DistributedShipAI()
        attacker.getCrew = lambda: [self.avatar.doId, 999]
        self.harness.air.doId2do[50] = attacker
        ship = types.SimpleNamespace(getBaseTeam=lambda: PiratesGlobals.NAVY_TEAM, getShipClass=lambda: 0,
                                     getIsFlagship=lambda: 0, getLevel=lambda: 10,
                                     getParentObj=lambda: types.SimpleNamespace(getUniqueId=lambda: 'ocean'))
        self.manager.shipSunk(ship, [50])
        self.assertTrue(quest.isComplete())

        undead = self.harness.addQuest('c3r2r2r8r2.2sinkShips')
        ship.getBaseTeam = lambda: PiratesGlobals.UNDEAD_TEAM
        before = undead.getTaskProgress()
        self.manager.shipSunk(ship, [self.avatar.doId])
        self.assertEqual(self.manager.getShipFaction(ship), AvatarTypes.Undead)
        self.assertIsNotNone(before)

    def test_docking_at_port_maroons_npcs(self):
        quest = self.harness.addQuest('c3r2r1.10maroonSteadman')
        island = types.SimpleNamespace(getUniqueId=lambda: 'not-a-wild-island')
        self.manager.dockedAtPort(self.avatar, island)
        self.assertFalse(quest.isComplete())
        island.getUniqueId = lambda: LocationIds.ANVIL_ISLAND
        self.manager.dockedAtPort(self.avatar, island)
        self.assertNotIn(quest.doId, self.manager.quests[self.avatar.doId])
        self.assertIn(QuestDB.QuestDict['c3r2r1.10maroonSteadman'].getQuestInt(),
                      self.avatar.getQuestHistory())

    def test_container_search_requires_a_matching_task(self):
        container = types.SimpleNamespace(getUniqueId=lambda: 'some-crate', getType=lambda: 0)
        self.assertFalse(self.manager.canSearchContainer(self.avatar, container))
        quest = self.harness.addQuest('c3r2r1.11stealList')
        self.assertFalse(self.manager.canSearchContainer(self.avatar, container))
        container.getUniqueId = lambda: PropIds.T_EITC_DESK
        self.assertTrue(self.manager.canSearchContainer(self.avatar, container))
        self.assertTrue(self.manager.containerSearched(self.avatar, container))
        self.assertFalse(self.manager.canSearchContainer(self.avatar, container))
        self.assertNotIn(quest.doId, self.manager.quests[self.avatar.doId])

    def test_bribes_cost_gold_and_complete_at_the_npc(self):
        questId = 'c3r2r1.6.5bribeBonita'
        task = QuestDB.QuestDict[questId].getTasks()[0]
        quest = self.harness.addQuest(questId)
        npc = makeNPC(task.getNpcId())
        self.harness.inventory.gold = task.getGold() - 1
        self.manager.attemptBribeNPC(self.avatar, npc)
        self.assertFalse(quest.isComplete())
        self.harness.inventory.gold = task.getGold() + 5
        self.manager.attemptBribeNPC(self.avatar, npc)
        self.assertTrue(quest.isComplete())
        self.assertEqual(self.harness.inventory.gold, 5)
        npc.d_setQuestsCompleted.assert_called_once()

    def test_dropping_a_quest_does_not_add_it_to_history(self):
        quest = self.harness.addQuest('ccbm.1poker')
        self.avatar.activeQuest = 'ccbm.1poker'
        self.avatar.requestDropQuest('ccbm.1poker')
        self.assertIsNone(self.manager.getQuest(self.avatar, questId='ccbm.1poker'))
        self.assertEqual(self.avatar.getQuestHistory(), [])
        self.assertEqual(self.avatar.getActiveQuest(), '')
        self.assertNotIn('BlackMack', self.avatar.questStatus.ladders)
        quest.requestDelete.assert_called_once()

        # the quest may be offered again
        self.assertEqual([offer.getQuestId() for offer in
                          self.manager.getQuestOffers(self.avatar, NPCIds.BLACK_MACK)], ['ccbm.1poker'])

    def test_quest_choice_quests_are_handed_in_one_at_a_time(self):
        visit = self.harness.addQuest('c3visitJoshamee')
        joshamee = makeNPC(NPCIds.JOSHAMEE)
        self.visit(joshamee)
        self.assertEqual(self.harness.getQuestIds(), ['c3r1.1sinkNavyShips', 'c3r1.2defeatNavyGuards'])
        self.assertIn(3001, self.avatar.getQuestHistory())
        self.assertIn('c3r1Joshamee', self.avatar.questStatus.choiceContainers)
        self.assertIn(3901, self.avatar.getCurrentQuestChoiceContainers())
        for quest in self.harness.created[1:]:
            self.assertEqual(quest.getGiverId(), NPCIds.JOSHAMEE)

        sink = self.manager.getQuest(self.avatar, questId='c3r1.1sinkNavyShips')
        for taskState in sink.getTaskStates():
            taskState.forceComplete()

        self.visit(joshamee)
        self.assertEqual(self.harness.getQuestIds(), ['c3r1.2defeatNavyGuards'])
        self.assertNotIn(visit.doId, self.manager.quests[self.avatar.doId])

        guards = self.manager.getQuest(self.avatar, questId='c3r1.2defeatNavyGuards')
        for taskState in guards.getTaskStates():
            taskState.forceComplete()

        self.visit(joshamee)
        self.assertEqual(self.harness.getQuestIds(), ['c3r2r1.1visitScarlet'])
        self.assertNotIn(3901, self.avatar.getCurrentQuestChoiceContainers())

    def test_quests_without_a_ladder_are_rewarded_and_removed(self):
        quest = self.harness.addQuest('c3r1Joshamee-revisit')
        self.visit(makeNPC(NPCIds.JOSHAMEE))
        self.assertIn(QuestDB.QuestDict['c3r1Joshamee-revisit'].getQuestInt(), self.avatar.getQuestHistory())
        self.assertNotIn(quest.doId, self.manager.quests[self.avatar.doId])

    def test_completed_fortune_ladder_can_be_taken_again(self):
        self.manager.setQuestGiverId(self.avatar, NPCIds.BLACK_MACK)
        self.harness.addQuest('ccbm.1poker')
        for questId in ('ccbm.1poker', 'ccbm.2defeatSkeleton'):
            self.assertEqual(self.harness.getQuestIds(), [questId])
            quest = self.manager.getQuest(self.avatar, questId=questId)
            for taskState in quest.getTaskStates():
                taskState.forceComplete()

            self.visit(makeNPC(NPCIds.BLACK_MACK))

        self.assertEqual(self.harness.getQuestIds(), [])
        self.assertIn(19919, self.avatar.getQuestLadderHistory())
        self.assertNotIn('BlackMack', self.avatar.questStatus.ladders)

        npc = makeNPC(NPCIds.BLACK_MACK)
        self.manager.acceptQuestOffer(self.avatar, npc, QuestOffer.create('ccbm.1poker', self.avatar), False)
        self.assertEqual(self.harness.getQuestIds(), ['ccbm.1poker'])
        self.assertNotIn(19945, self.avatar.getQuestHistory())

    def test_relogin_restores_quest_choice_containers(self):
        self.avatar.currentQuestChoiceContainers = [3901]
        self.harness.addQuest('c3r1.1sinkNavyShips')
        self.assertEqual(self.avatar.questStatus.choiceContainers, {})
        self.manager.restoreQuestChoiceContainers(self.avatar)
        self.assertIn('c3r1Joshamee', self.avatar.questStatus.choiceContainers)

    def test_tracked_quest_can_be_cleared(self):
        self.harness.addQuest('ccbm.1poker')
        self.avatar.requestActiveQuest('ccbm.1poker')
        self.assertEqual(self.avatar.getActiveQuest(), 'ccbm.1poker')
        self.avatar.requestActiveQuest('')
        self.assertEqual(self.avatar.getActiveQuest(), '')
        self.avatar.requestActiveQuest('not-a-quest')
        self.assertEqual(self.avatar.getActiveQuest(), '')


if __name__ == '__main__':
    unittest.main()
