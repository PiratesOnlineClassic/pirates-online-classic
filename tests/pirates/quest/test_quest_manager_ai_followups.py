import types
import unittest
from unittest.mock import Mock

from direct.showbase.MessengerGlobal import messenger

from tests.pirates.quest.test_quest_manager_ai_progression import manager_module
from tests.pirates.quest import test_quest_manager_ai_tasks as tasks_module
from pirates.piratesbase import CollectionMap
from pirates.piratesbase import PiratesGlobals
from pirates.quest.QuestConstants import NPCIds
from pirates.quest.QuestPath import QuestGoal, QuestStep
from pirates.pirate import AvatarTypes
from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType


def stackInventory(inventory):
    inventory.stacks = {}
    inventory.getStackQuantity = lambda stackType: inventory.stacks.get(stackType, 0)

    def setStack(stackType, quantity):
        inventory.stacks[stackType] = quantity

    inventory.b_setStackQuantity = setStack
    return inventory


class FakeSiegeShip(manager_module.DistributedShipAI):

    def __init__(self, doId, team, crew, npc=False):
        self.doId = doId
        self.team = team
        self.crew = list(crew)
        self.npc = npc
        self.lastAttackerShipId = 0
        self.lastAttackSkillId = 0
        self.attackerDamage = {}

    def getSiegeTeam(self):
        return self.team

    def getCrew(self):
        return self.crew

    def getNPCship(self):
        return self.npc

    def getParentObj(self):
        return types.SimpleNamespace(getUniqueId=lambda: 'ocean')


class QuestFollowupTests(unittest.TestCase):
    tearDown = tasks_module.QuestTaskTests.tearDown
    visit = tasks_module.QuestTaskTests.visit

    def setUp(self):
        tasks_module.QuestTaskTests.setUp(self)
        stackInventory(self.harness.inventory)
        self.avatar.siegeTeam = 0
        self.avatar.getSiegeTeam = lambda: self.avatar.siegeTeam

    # -- treasure collections -------------------------------------------------

    def giveCollection(self, collectionId, missing=0):
        for pieceId, needed in self.manager.getCollectionPieces(collectionId):
            self.harness.inventory.stacks[pieceId] = needed

        if missing:
            self.harness.inventory.stacks[collectionId + 1] -= missing

    def test_collection_deliver_requires_and_takes_the_whole_collection(self):
        quest = self.harness.addQuest('tr2.1deliverPaintings')
        self.giveCollection(InventoryType.Collection_Set3, missing=1)
        elizabeth = tasks_module.makeNPC(NPCIds.ELIZABETH)
        self.visit(elizabeth)
        self.assertFalse(quest.isComplete())
        self.assertEqual(self.harness.inventory.stacks[InventoryType.Collection_Set3_Part2], 1)

        self.giveCollection(InventoryType.Collection_Set3)
        self.manager.requestInteract(self.avatar, elizabeth)
        self.assertTrue(quest.getTaskStates()[0].isComplete())
        self.assertTrue(all(quantity == 0 for quantity in self.harness.inventory.stacks.values()))

    def test_collection_sizes_match_their_deliver_tasks(self):
        tasks = {'tr2.1deliverPaintings': 9, 'tt2.1deliverTeeth': 28, 'tm2.1deliverMedals': 14,
                 'trr2.1deliverRings': 10, 'tc2.1deliverChess': 32, 'tf2.1deliverFigurines': 15}
        for questId, num in tasks.items():
            task = manager_module.QuestDB.QuestDict[questId].getTasks()[0]
            collectionId = self.manager.DeliverCollections[task.getItem()]
            self.assertEqual(sum(needed for pieceId, needed in self.manager.getCollectionPieces(collectionId)), num)
            self.assertIn(collectionId, CollectionMap.Collection_Set_Sizes)

    def test_single_item_delivery_does_not_need_a_collection(self):
        questId = [questId for questId, dna in manager_module.QuestDB.QuestDict.items()
                   if any(type(task).__name__ == 'DeliverItemTaskDNA' and
                          task.getItem() == manager_module.QuestItems.Medal and task.getNum() == 1
                          for task in dna.getTasks())][0]
        quest = self.harness.addQuest(questId)
        self.manager.requestInteract(self.avatar, tasks_module.makeNPC(NPCIds.WILL_TURNER))
        self.assertTrue(quest.getTaskStates()[0].isComplete())

    # -- quest containers -----------------------------------------------------

    def test_final_main_story_quest_completes_the_main_story(self):
        quest = self.harness.addQuest('c3.8visitJack')
        self.assertEqual(self.manager.getCompletedContainerIds(self.avatar, quest), [])
        for taskState in quest.getTaskStates():
            taskState.forceComplete()

        self.assertEqual(self.manager.getCompletedContainerIds(self.avatar, quest), ['MainStory'])
        stub = self.avatar.questStatus.getQuestStub('c3.8visitJack')
        self.assertFalse(stub.processed)

    def test_quest_mid_ladder_completes_no_container(self):
        quest = self.harness.addQuest('c3.7recoverPearl')
        for taskState in quest.getTaskStates():
            taskState.forceComplete()

        self.assertEqual(self.manager.getCompletedContainerIds(self.avatar, quest), [])

    # -- ship sinking ---------------------------------------------------------

    def test_every_crew_that_damaged_an_npc_ship_is_credited(self):
        quest = self.harness.addQuest('c3r1.1sinkNavyShips')
        killer = FakeSiegeShip(50, 0, [999])
        helper = FakeSiegeShip(51, 0, [self.avatar.doId])
        self.harness.air.doId2do.update({50: killer, 51: helper})
        ship = FakeSiegeShip(60, 0, [], npc=True)
        ship.getBaseTeam = lambda: PiratesGlobals.NAVY_TEAM
        ship.getShipClass = lambda: 0
        ship.getIsFlagship = lambda: 0
        ship.getLevel = lambda: 10
        ship.lastAttackerShipId = 50
        ship.attackerDamage = {50: 100, 51: 300}
        self.assertEqual(self.manager.getShipAttackerIds(ship), [50, 51])
        self.manager.shipSinking(ship)
        self.assertTrue(quest.isComplete())

    # -- ship pvp ----------------------------------------------------------------

    def makeSiege(self):
        self.avatar.siegeTeam = 2
        own = FakeSiegeShip(70, 2, [self.avatar.doId])
        enemy = FakeSiegeShip(80, 1, [])
        self.harness.air.doId2do.update({70: own, 80: enemy})
        return own, enemy

    def test_sinking_an_enemy_privateer_ship(self):
        own, enemy = self.makeSiege()
        trial = self.harness.addQuest('spanish.ShipPVPFirstTrial')
        cannon = self.harness.addQuest('spanish.ShipPVPTaskC')
        ram = self.harness.addQuest('spanish.ShipPVPTaskB')
        enemy.lastAttackerShipId = 70
        enemy.lastAttackSkillId = InventoryType.CannonShoot
        enemy.attackerDamage = {70: 500}
        self.manager.shipSinking(enemy)
        self.assertTrue(trial.isComplete())
        self.assertEqual(cannon.getTaskProgress(), [(1, 5)])
        self.assertEqual(ram.getTaskProgress(), [(0, 5)])

    def test_assisting_ships_get_credit_without_the_weapon(self):
        own, enemy = self.makeSiege()
        other = FakeSiegeShip(71, 2, [998])
        self.harness.air.doId2do[71] = other
        trial = self.harness.addQuest('spanish.ShipPVPFirstTrial')
        cannon = self.harness.addQuest('spanish.ShipPVPTaskC')
        enemy.lastAttackerShipId = 71
        enemy.lastAttackSkillId = InventoryType.CannonShoot
        enemy.attackerDamage = {71: 500, 70: 100}
        self.manager.shipSinking(enemy)
        self.assertTrue(trial.isComplete())
        self.assertEqual(cannon.getTaskProgress(), [(0, 5)])

    def test_friendly_ships_are_not_credited(self):
        own, enemy = self.makeSiege()
        enemy.team = 2
        trial = self.harness.addQuest('spanish.ShipPVPFirstTrial')
        enemy.lastAttackerShipId = 70
        enemy.attackerDamage = {70: 500}
        self.manager.shipSinking(enemy)
        self.assertFalse(trial.isComplete())

    def test_ship_damage_and_sinking_resets(self):
        own, enemy = self.makeSiege()
        damage = self.harness.addQuest('spanish.ShipPVPTaskA')
        withoutSink = self.harness.addQuest('spanish.ShipPVPTaskM')
        self.manager.shipPVPShipDamaged(enemy, self.avatar, 4000, InventoryType.CannonShoot)
        self.assertEqual(damage.getTaskProgress(), [(4000, 10000)])
        self.assertEqual(withoutSink.getTaskProgress(), [(4000, 25000)])

        # rams are done with the ship, the cannon task is not credited...
        self.manager.shipPVPShipDamaged(enemy, own, 1000)
        self.assertEqual(withoutSink.getTaskProgress(), [(4000, 25000)])
        self.assertEqual(damage.getTaskProgress(), [(5000, 10000)])

        self.manager.shipSinking(own)
        self.assertEqual(withoutSink.getTaskProgress(), [(0, 25000)])
        self.assertEqual(damage.getTaskProgress(), [(5000, 10000)])

    def test_defeating_an_enemy_privateer(self):
        self.makeSiege()
        pirates = self.harness.addQuest('spanish.ShipPVPTaskO')
        cannon = self.harness.addQuest('spanish.ShipPVPTaskE')
        self.avatar.battleSkillDiary = types.SimpleNamespace(getCurrentSkill=lambda: InventoryType.CannonShoot)
        target = types.SimpleNamespace(getSiegeTeam=lambda: 1)
        self.manager.shipPVPPirateDefeated(target, [self.avatar, None])
        self.assertEqual(pirates.getTaskProgress(), [(1, 25)])
        self.assertEqual(cannon.getTaskProgress(), [(1, 10)])

    # -- quest steps ----------------------------------------------------------

    def test_completed_quest_step_leads_to_the_return_npc(self):
        quest = self.harness.addQuest('ccbm.1poker')
        self.assertNotEqual(self.manager.getQuestStepGoalUid(self.avatar, quest), NPCIds.BLACK_MACK)
        for taskState in quest.getTaskStates():
            taskState.forceComplete()

        self.assertEqual(self.manager.getQuestStepGoalUid(self.avatar, quest), NPCIds.BLACK_MACK)

    def test_goal_changes_resend_the_active_quest_step(self):
        quest = self.harness.addQuest('ccbm.1poker')
        self.harness.air.uidMgr = types.SimpleNamespace(justGetMeMeObject=lambda uid: None)
        self.avatar.activeQuest = 'ccbm.1poker'
        self.avatar.requestQuestStep = Mock()
        self.manager.pokerHandWon(self.avatar, 1)
        self.avatar.requestQuestStep.assert_not_called()
        self.manager.pokerHandWon(self.avatar, 100000)
        self.avatar.requestQuestStep.assert_called_once_with('ccbm.1poker')

    # -- sharing and limits ---------------------------------------------------

    def test_share_requests_are_ignored(self):
        quest = self.harness.addQuest('ccbm.1poker')
        self.avatar.requestShareQuest('ccbm.1poker')
        self.harness.air.logPotentialHacker.assert_not_called()
        self.avatar.requestShareQuest('nope')
        self.harness.air.logPotentialHacker.assert_called_once()
        self.assertEqual(self.harness.getQuestIds(), ['ccbm.1poker'])

    def test_quest_offers_respect_the_quest_list_limit(self):
        dna = manager_module.QuestDB.QuestDict['ccbm.1poker']
        self.assertTrue(self.manager.canOfferQuest(self.avatar, 'ccbm.1poker', dna, NPCIds.BLACK_MACK))
        self.harness.inventory.ids = list(range(1000, 1255))
        self.assertFalse(self.manager.canOfferQuest(self.avatar, 'ccbm.1poker', dna, NPCIds.BLACK_MACK))


if __name__ == '__main__':
    unittest.main()


class MainStoryWalkTests(unittest.TestCase):
    tearDown = tasks_module.QuestTaskTests.tearDown

    def setUp(self):
        tasks_module.QuestTaskTests.setUp(self)
        stackInventory(self.harness.inventory)
        # the rewards themselves are covered by the other quest tests...
        self.manager._giveRewards = lambda avatar, rewards=[]: True
        self.harness.trade.giveNewTreasureMap = lambda gameStyle, callback: callback(True)

    def chooseContainers(self):
        # the avatar picks every container offered by it's quest choices...
        chosen = False
        status = self.avatar.questStatus
        for choice in list(status.choiceContainers.values()):
            self.assertIsNotNone(choice.av, 'choice %s outlived it\'s ladder' % choice.getName())
            for container in choice.getValidContainers():
                if container.getQuestInt() in self.avatar.getQuestLadderHistory():
                    continue

                if container.isComplete():
                    continue

                giver = tasks_module.makeNPC(choice.getGiverId() or '')
                offer = manager_module.QuestLadderOffer(container.getName(), container.getTitle(), [])
                before = len(self.harness.created)
                self.manager.acceptQuestOffer(self.avatar, giver, offer, True)
                chosen = chosen or len(self.harness.created) > before

        return chosen

    def walk(self, firstQuestId, finalQuestId, ladderInt):
        self.harness.addQuest(firstQuestId)
        seen = []
        completedContainers = []
        for step in range(2000):
            quests = self.harness.inventory.getQuestList()
            if not quests:
                if not self.chooseContainers():
                    break

                continue

            quest = quests[0]
            seen.append(quest.getQuestId())
            for taskState in quest.getTaskStates():
                taskState.forceComplete()

            if quest.getQuestId() == finalQuestId:
                completedContainers = self.manager.getCompletedContainerIds(self.avatar, quest)

            self.manager.completeQuest(self.avatar, quest)
            self.manager.runDeferredQuestCompletions(self.avatar)
            if self.manager.getQuest(self.avatar, questDoId=quest.doId) is quest:
                # quests that do not advance a ladder (revisits) are simply rewarded
                if not self.avatar.questStatus.getQuestStub(quest.getQuestId()):
                    continue

                self.fail('quest %s did not advance it\'s ladder after %s' % (quest.getQuestId(), seen[-5:]))

        return seen, completedContainers

    def test_walk_the_main_story(self):
        seen, completedContainers = self.walk('Chapter1.rung1', 'c3.8visitJack', 1100)
        # every chapter is played through, including the quests of every quest choice...
        self.assertGreater(len(set(seen)), 450)
        self.assertEqual(seen[:3], ['Chapter1.rung1', 'Chapter1.rung2', 'Chapter1.rung3'])
        self.assertIn('c3.8visitJack', seen)
        self.assertEqual(completedContainers, ['MainStory'])
        self.assertIn(1100, self.avatar.getQuestLadderHistory())
        self.assertEqual(self.harness.getQuestIds(), [])
        self.assertEqual(self.avatar.getCurrentQuestChoiceContainers(), [])
        for name in ('Chapter 1', 'Chapter 2', 'Chapter 3'):
            container = manager_module.QuestLadderDB.getContainer(name)
            self.assertTrue(container.getQuestInt() in self.avatar.getQuestLadderHistory() or
                            1100 in self.avatar.getQuestLadderHistory())

    def test_walk_the_other_story_ladders(self):
        for name, ladder in list(manager_module.QuestLadderDB.FameQuestLadderDict.items()):
            if name == 'MainStory':
                continue

            self.tearDown()
            self.setUp()
            self.walk(ladder.getFirstQuestId(), None, ladder.getQuestInt())
            self.assertIn(ladder.getQuestInt(), self.avatar.getQuestLadderHistory(), name)
            self.assertEqual(self.harness.getQuestIds(), [], name)
            self.assertEqual(self.avatar.getCurrentQuestChoiceContainers(), [], name)
