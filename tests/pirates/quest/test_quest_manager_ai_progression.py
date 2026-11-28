import builtins
import importlib.util
import sys
import types
import unittest
from unittest.mock import Mock, patch
from tests import REPO_ROOT


def load_manager():
    modules = {}
    for path in (
        'pirates.battle.DistributedBattleAvatarAI',
        'pirates.ship.DistributedShipAI',
        'pirates.npc.DistributedNPCTownfolkAI',
        'pirates.world.DistributedGameAreaAI',
        'pirates.world.DistributedIslandAI',
        'pirates.world.DistributedGAInteriorAI',
        'pirates.world.DistributedBuildingDoorAI',
        'pirates.world.DistributedInteriorDoorAI',
        'pirates.world.DistributedDinghyAI',
    ):
        module = types.ModuleType(path)
        name = path.rsplit('.', 1)[1]
        setattr(module, name, type(name, (), {}))
        modules[path] = module
    cutscenes = types.ModuleType('pirates.cutscene.CutsceneData')
    cutscenes.Cutscene2_1 = '2.1: Will Turner Sword'
    cutscenes.Cutscene2_4 = '2.4'
    modules[cutscenes.__name__] = cutscenes
    spec = importlib.util.spec_from_file_location(
        '_quest_manager_progression_test', REPO_ROOT / 'pirates/quest/QuestManagerAI.py')
    module = importlib.util.module_from_spec(spec)
    previous = {name: sys.modules.get(name) for name in modules}
    sys.modules.update(modules)
    try:
        with patch.object(builtins, '__dev__', False, create=True):
            spec.loader.exec_module(module)
    finally:
        for name, value in previous.items():
            if value is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = value
    return module


manager_module = load_manager()
from pirates.quest.DistributedQuestAvatarAI import DistributedQuestAvatarAI
from pirates.quest import QuestDB, QuestLadderDB
from pirates.quest.QuestStatus import QuestStatus
from pirates.quest.QuestLadder import QuestStub
from pirates.uberdog.UberDogGlobals import InventoryType


class QuestProgressionTests(unittest.TestCase):
    def test_map_reward_waits_for_success_and_retries_after_failure(self):
        callbacks = []
        trade = types.SimpleNamespace(
            giveNewTreasureMap=lambda mapId, callback: callbacks.append((mapId, callback)))
        air = types.SimpleNamespace(tradeMgr=types.SimpleNamespace(createTrade=lambda avId: trade),
                                    doId2do={})
        manager = manager_module.QuestManagerAI(air)
        manager._giveRewards = Mock(return_value=True)
        stub = types.SimpleNamespace(complete=False, handleQuestComplete=Mock())
        avatar = types.SimpleNamespace(doId=1, history=[],
            getQuestHistory=lambda: avatar.history,
            b_setQuestHistory=lambda history: setattr(avatar, 'history', history),
            getTutorial=lambda: 0, b_setTutorial=Mock(),
            questStatus=types.SimpleNamespace(getQuestStub=lambda questId: stub,
                                               getNPCInteractMode=lambda: False))
        dna = QuestDB.QuestDict['c3.6deliverMap']
        quest = types.SimpleNamespace(doId=2, getQuestId=lambda: 'c3.6deliverMap',
                                      getQuestDNA=lambda: dna, isComplete=lambda: True,
                                      getRewards=dna.getRewards)
        manager.quests[1] = {2: quest}
        air.doId2do[1] = avatar
        manager.completeQuest(avatar, quest)
        manager.completeQuest(avatar, quest)
        self.assertEqual(len(callbacks), 1)
        self.assertEqual(callbacks[0][0], 0)
        manager._giveRewards.assert_not_called()
        callbacks[0][1](False)
        self.assertEqual(avatar.history, [])
        manager.completeQuest(avatar, quest)
        self.assertEqual(len(callbacks), 2)
        callbacks[1][1](True)
        self.assertEqual(avatar.history, [dna.getQuestInt()])
        manager._giveRewards.assert_called_once()
        stub.handleQuestComplete.assert_called_once()

    def test_map_reward_completion_ignores_disconnected_avatar(self):
        callback = []
        air = types.SimpleNamespace(doId2do={}, tradeMgr=types.SimpleNamespace(
            createTrade=lambda avId: types.SimpleNamespace(
                giveNewTreasureMap=lambda mapId, done: callback.append(done))))
        manager = manager_module.QuestManagerAI(air)
        manager._giveRewards = Mock(return_value=True)
        stub = types.SimpleNamespace(complete=False, handleQuestComplete=Mock())
        avatar = types.SimpleNamespace(doId=1, getQuestHistory=lambda: [],
            b_setQuestHistory=Mock(), questStatus=types.SimpleNamespace(
                getQuestStub=lambda questId: stub, getNPCInteractMode=lambda: False))
        dna = QuestDB.QuestDict['c3.6deliverMap']
        quest = types.SimpleNamespace(doId=2, getQuestId=lambda: 'c3.6deliverMap',
                                      getQuestDNA=lambda: dna, isComplete=lambda: True,
                                      getRewards=dna.getRewards)
        manager.quests[1] = {2: quest}
        air.doId2do[1] = avatar
        manager.completeQuest(avatar, quest)
        del air.doId2do[1]
        callback[0](True)
        avatar.b_setQuestHistory.assert_not_called()
        manager._giveRewards.assert_not_called()
        self.assertNotIn(2, manager.completingQuests)

    def test_ladder_successors(self):
        avatar = types.SimpleNamespace(getQuestHistory=lambda: [])
        ladder = QuestLadderDB.FameQuestLadderDict['MainStory'].constructDynamicCopy(avatar)
        self.assertEqual(
            [ladder.getNextQuestId(q) for q in (
                'Chapter1.rung1', 'Chapter1.rung2', 'Chapter1.rung3')],
            ['Chapter1.rung2', 'Chapter1.rung3', 'c2_visit_will_turner'])

    def test_completion_waits_for_fsm_and_awards_once(self):
        manager = manager_module.QuestManagerAI(types.SimpleNamespace())
        manager._giveRewards = Mock()
        manager.resumeCompletedTutorialQuest = Mock()
        stub = types.SimpleNamespace(complete=False)
        stub.handleQuestComplete = Mock(side_effect=lambda *args: setattr(stub, 'complete', True))
        avatar = types.SimpleNamespace(
            doId=1, history=[], tutorial=0,
            getQuestHistory=lambda: avatar.history,
            b_setQuestHistory=lambda value: setattr(avatar, 'history', value),
            getTutorial=lambda: avatar.tutorial,
            b_setTutorial=lambda value: setattr(avatar, 'tutorial', value),
            questStatus=types.SimpleNamespace(
                getQuestStub=lambda questId: stub, getNPCInteractMode=lambda: False))
        dna = QuestDB.QuestDict['Chapter1.rung2']
        quest = types.SimpleNamespace(
            doId=2, getQuestId=lambda: 'Chapter1.rung2', getQuestDNA=lambda: dna,
            isComplete=lambda: True, getRewards=lambda: ['reward'])
        manager.quests[1] = {2: quest}
        manager.avatar2fsm[1] = object()
        manager.completeQuest(avatar, quest)
        manager.completeQuest(avatar, quest)
        self.assertEqual(len(manager.deferredQuestCompletions[1]), 1)
        self.assertEqual(avatar.history, [])
        del manager.avatar2fsm[1]
        manager.runDeferredQuestCompletions(avatar)
        manager.completeQuest(avatar, quest)
        self.assertEqual(avatar.history, [1001])
        self.assertEqual(avatar.tutorial, dna.getCheckPoint())
        manager._giveRewards.assert_called_once_with(avatar, ['reward'])
        stub.handleQuestComplete.assert_called_once()

    def test_batch_creation_waits_for_each_activation(self):
        fsm = manager_module.CreateQuestsFSM.__new__(manager_module.CreateQuestsFSM)
        inventory = types.SimpleNamespace(
            ids=[], getDoIdListCategory=lambda category: inventory.ids[:],
            setQuestList=lambda ids: setattr(inventory, 'ids', ids))
        fsm.avatar = types.SimpleNamespace(doId=1, getInventory=lambda: inventory)
        fsm.cleanup = Mock()
        created, activated = [], []
        fsm.createQuestEntry = lambda quest_id, callback: (
            created.append((quest_id, callback)) or True)
        fsm.activateQuestEntry = lambda do_id, callback: (
            activated.append((do_id, callback)) or True)
        fsm.enterStart(['first', 'second'])
        self.assertEqual([entry[0] for entry in created], ['first'])
        created[0][1](101)
        self.assertEqual(len(created), 1)
        activated[0][1](types.SimpleNamespace(doId=101, getQuestId=lambda: 'first'))
        self.assertEqual([entry[0] for entry in created], ['first', 'second'])
        created[1][1](102)
        activated[1][1](types.SimpleNamespace(doId=102, getQuestId=lambda: 'second'))
        self.assertEqual(inventory.ids, [101, 102])
        fsm.cleanup.assert_called_once_with()

    def test_idle_callbacks_wait_for_running_operations(self):
        manager = manager_module.QuestManagerAI(types.SimpleNamespace())
        avatar = types.SimpleNamespace(doId=1)
        first = Mock(side_effect=lambda: manager.avatar2fsm.update({1: object()}))
        second = Mock()
        manager.avatar2fsm[1] = object()
        manager.whenQuestIdle(avatar, first)
        manager.whenQuestIdle(avatar, first)
        manager.whenQuestIdle(avatar, second)
        del manager.avatar2fsm[1]
        manager.runDeferredQuestCompletions(avatar)
        first.assert_called_once()
        second.assert_not_called()
        del manager.avatar2fsm[1]
        manager.runDeferredQuestCompletions(avatar)
        second.assert_called_once()

    def test_resume_skips_already_completed_successors(self):
        manager = manager_module.QuestManagerAI(types.SimpleNamespace())
        dna = QuestDB.QuestDict['Chapter1.rung1']
        quest = types.SimpleNamespace(
            doId=5, getQuestId=lambda: 'Chapter1.rung1', getQuestDNA=lambda: dna)
        next_ids = {'Chapter1.rung1': 'Chapter1.rung2',
                    'Chapter1.rung2': 'Chapter1.rung3'}
        avatar = types.SimpleNamespace(
            doId=1, getQuestHistory=lambda: [1000, 1001],
            questStatus=types.SimpleNamespace(getNextQuestId=next_ids.get),
            _swapQuest=Mock())
        manager.quests[1] = {5: quest}
        manager.resumeCompletedTutorialQuest(avatar)
        avatar._swapQuest.assert_called_once_with([quest], questIds=['Chapter1.rung3'])

    def test_intro_waits_for_make_a_pirate_and_finishes_once(self):
        manager = manager_module.QuestManagerAI(types.SimpleNamespace())
        events = {}
        manager.acceptOnce = lambda event, callback, extraArgs=[]: events.update(
            {event: lambda: callback(*extraArgs)})
        manager.completeQuest = Mock()
        avatar = types.SimpleNamespace(
            doId=1, tutorial=0, getTutorial=lambda: avatar.tutorial, getQuestHistory=lambda: [])
        dna = QuestDB.QuestDict['Chapter1.rung1']
        scenes = []
        quest = types.SimpleNamespace(
            doId=5, questDNA=dna, getQuestDNA=lambda: dna,
            getQuestId=lambda: 'Chapter1.rung1',
            setFinalizeStateIndex=lambda idx: None,
            d_startFinalizeScene=lambda idx, giver: scenes.append((idx, giver)),
            d_amFinalized=Mock(), completeRequiresVisit=lambda: False)
        manager.finalizeCutscene(avatar, quest)
        manager.finalizeCutscene(avatar, quest)
        self.assertEqual(scenes, [(0, 0)])
        events.pop('quest-finalize-5')()
        self.assertEqual(scenes, [(0, 0)])
        avatar.tutorial = 1
        events.pop('makeAPirateComplete-5')()
        self.assertEqual(scenes, [(0, 0), (1, 0)])
        events.pop('quest-finalize-5')()
        quest.d_amFinalized.assert_called_once()
        manager.completeQuest.assert_called_once_with(avatar, quest)

    def test_jolly_waits_for_the_matching_avatars_target_practice(self):
        from direct.showbase.MessengerGlobal import messenger

        manager = manager_module.QuestManagerAI(types.SimpleNamespace())
        manager.completeQuest = Mock()
        dna = QuestDB.QuestDict['Chapter1.rung3']
        scenes = []

        def make_pair(avatar_id, quest_id):
            avatar = types.SimpleNamespace(
                doId=avatar_id, getTutorial=lambda: 2, getQuestHistory=lambda: [])
            quest = types.SimpleNamespace(
                doId=quest_id, questId='Chapter1.rung3', questDNA=dna,
                getQuestDNA=lambda: dna, getQuestId=lambda: 'Chapter1.rung3',
                setFinalizeStateIndex=lambda idx: None,
                d_startFinalizeScene=lambda idx, giver: scenes.append((quest_id, idx)),
                d_amFinalized=Mock(), completeRequiresVisit=lambda: False)
            manager.quests[avatar_id] = {quest_id: quest}
            return avatar, quest

        first, first_quest = make_pair(1, 101)
        second, second_quest = make_pair(2, 102)
        with patch.object(builtins, 'messenger', messenger, create=True):
            manager.finalizeCutscene(first, first_quest)
            manager.finalizeCutscene(second, second_quest)
            messenger.send('quest-finalize-101')
            messenger.send('quest-finalize-102')
            self.assertEqual(scenes, [(101, 0), (102, 0)])
            manager.tutorialJROnStage(first)
            manager.tutorialJROnStage(first)
            self.assertEqual(scenes, [(101, 0), (102, 0), (101, 1)])
            messenger.send('quest-finalize-101')
            first_quest.d_amFinalized.assert_called_once()
            manager.completeQuest.assert_called_once_with(first, first_quest)
            self.assertIn(102, manager.tutorialJollyWaiters)
            manager.tutorialJROnStage(second)
            self.assertEqual(scenes[-1], (102, 1))
            messenger.send('quest-finalize-102')
        second_quest.d_amFinalized.assert_called_once()

    def test_jolly_signal_before_beck_finishes_is_latched_and_cleaned_up(self):
        from direct.showbase.MessengerGlobal import messenger

        manager = manager_module.QuestManagerAI(types.SimpleNamespace())
        manager.completeQuest = Mock()
        dna = QuestDB.QuestDict['Chapter1.rung3']
        avatar = types.SimpleNamespace(doId=1, getTutorial=lambda: 2, getQuestHistory=lambda: [])
        scenes = []
        quest = types.SimpleNamespace(
            doId=101, questId='Chapter1.rung3', questDNA=dna,
            getQuestDNA=lambda: dna, getQuestId=lambda: 'Chapter1.rung3',
            setFinalizeStateIndex=lambda idx: None,
            d_startFinalizeScene=lambda idx, giver: scenes.append(idx),
            d_amFinalized=Mock(), completeRequiresVisit=lambda: False,
            requestDelete=Mock())
        manager.quests[1] = {101: quest}
        with patch.object(builtins, 'messenger', messenger, create=True):
            manager.tutorialJROnStage(avatar)
            manager.tutorialJROnStage(avatar)
            manager.finalizeCutscene(avatar, quest)
            self.assertEqual(scenes, [0])
            messenger.send('quest-finalize-101')
            self.assertEqual(scenes, [0, 1])
            manager.deactivateQuest(avatar, 101)
            messenger.send('quest-finalize-101')
        self.assertNotIn(101, manager.tutorialJollyReady)
        self.assertNotIn(101, manager.tutorialJollyWaiters)
        quest.d_amFinalized.assert_not_called()
        manager.completeQuest.assert_not_called()

    def test_jolly_wait_is_cancelled_when_quest_deactivates(self):
        from direct.showbase.MessengerGlobal import messenger

        manager = manager_module.QuestManagerAI(types.SimpleNamespace())
        dna = QuestDB.QuestDict['Chapter1.rung3']
        avatar = types.SimpleNamespace(doId=1, getTutorial=lambda: 2, getQuestHistory=lambda: [],
            getReturnLocation=lambda: '', b_setReturnLocation=Mock())
        quest = types.SimpleNamespace(
            doId=101, questId='Chapter1.rung3', questDNA=dna,
            getQuestDNA=lambda: dna, getQuestId=lambda: 'Chapter1.rung3',
            setFinalizeStateIndex=lambda idx: None, d_startFinalizeScene=Mock(),
            requestDelete=Mock())
        manager.quests[1] = {101: quest}
        with patch.object(builtins, 'messenger', messenger, create=True):
            manager.finalizeCutscene(avatar, quest)
            messenger.send('quest-finalize-101')
            self.assertIn(101, manager.tutorialJollyWaiters)
            manager.deactivateQuest(avatar, 101)
            manager.tutorialJROnStage(avatar)
        self.assertNotIn(101, manager.tutorialJollyWaiters)
        self.assertNotIn(101, manager.tutorialJollyReady)
        quest.d_startFinalizeScene.assert_called_once_with(0, 0)

    def test_handler_target_practice_releases_real_quest_wait(self):
        from direct.showbase.MessengerGlobal import messenger

        npc_name = 'pirates.npc.DistributedNPCTownfolkAI'
        npc_module = types.ModuleType(npc_name)
        npc_module.DistributedNPCTownfolkAI = manager_module.DistributedNPCTownfolkAI
        spec = importlib.util.spec_from_file_location(
            '_tutorial_quest_handler_test',
            REPO_ROOT / 'pirates/tutorial/DistributedPiratesTutorialAI.py')
        handler_module = importlib.util.module_from_spec(spec)
        previous = sys.modules.get(npc_name)
        sys.modules[npc_name] = npc_module
        try:
            spec.loader.exec_module(handler_module)
        finally:
            if previous is None:
                sys.modules.pop(npc_name, None)
            else:
                sys.modules[npc_name] = previous

        manager = manager_module.QuestManagerAI(types.SimpleNamespace())
        dna = QuestDB.QuestDict['Chapter1.rung3']
        avatar = types.SimpleNamespace(doId=1, getTutorial=lambda: 2, getQuestHistory=lambda: [],
            getReturnLocation=lambda: '', b_setReturnLocation=Mock())
        quest = types.SimpleNamespace(
            doId=101, questId='Chapter1.rung3', questDNA=dna,
            getQuestDNA=lambda: dna, getQuestId=lambda: 'Chapter1.rung3',
            setFinalizeStateIndex=lambda idx: None, d_startFinalizeScene=Mock())
        manager.quests[1] = {101: quest}
        handler = handler_module.DistributedPiratesTutorialAI.__new__(
            handler_module.DistributedPiratesTutorialAI)
        handler.avatarId = 1
        handler.air = types.SimpleNamespace(
            questMgr=manager, doId2do={1: avatar}, getAvatarIdFromSender=lambda: 1)
        handler.request = Mock()
        with patch.object(builtins, 'messenger', messenger, create=True):
            manager.finalizeCutscene(avatar, quest)
            handler.targetPracticeDone()
            quest.d_startFinalizeScene.assert_called_once_with(0, 0)
            messenger.send('quest-finalize-101')
            self.assertEqual(quest.d_startFinalizeScene.call_args_list,
                             [unittest.mock.call(0, 0), unittest.mock.call(1, 0)])
            manager.ignoreAll()
        handler.request.assert_called_once_with('TargetPracticeDone')

    def test_non_tutorial_finalization_waits_for_npc_interaction(self):
        from direct.showbase.MessengerGlobal import messenger

        manager = manager_module.QuestManagerAI(types.SimpleNamespace())
        manager.completeQuest = Mock()
        dna = QuestDB.QuestDict['wd.1visitTia']
        avatar = types.SimpleNamespace(
            doId=1, getTutorial=lambda: 12, getQuestHistory=lambda: [],
            uniqueName=lambda event: '%s-1' % event)
        quest = types.SimpleNamespace(
            doId=101, questDNA=dna, getQuestDNA=lambda: dna,
            getQuestId=lambda: 'wd.1visitTia', setFinalizeStateIndex=lambda idx: None,
            d_startFinalizeScene=Mock(), d_amFinalized=Mock(),
            completeRequiresVisit=lambda: True)
        npc = types.SimpleNamespace(doId=22, d_setQuestsCompleted=Mock())
        with patch.object(builtins, 'messenger', messenger, create=True):
            manager.finalizeCutscene(avatar, quest, npc=npc)
            messenger.send('quest-finalize-101')
            npc.d_setQuestsCompleted.assert_called_once()
            manager.completeQuest.assert_not_called()
            messenger.send('interact-canceled-1')
        manager.completeQuest.assert_called_once_with(avatar, quest)

    def test_failed_reward_delivery_preserves_retry_and_history(self):
        trade = object()
        air = types.SimpleNamespace(tradeMgr=types.SimpleNamespace(createTrade=Mock(return_value=trade)))
        manager = manager_module.QuestManagerAI(air)
        dna = QuestDB.QuestDict['wd.1visitTia']
        stub = types.SimpleNamespace(complete=False)
        stub.handleQuestComplete = Mock(side_effect=lambda *args: setattr(stub, 'complete', True))
        avatar = types.SimpleNamespace(
            doId=1, history=[], inventory=None, getInventory=lambda: avatar.inventory,
            getQuestHistory=lambda: avatar.history,
            b_setQuestHistory=lambda value: setattr(avatar, 'history', value),
            getTutorial=lambda: 12, b_setTutorial=Mock(),
            questStatus=types.SimpleNamespace(
                getQuestStub=lambda questId: stub, getNPCInteractMode=lambda: False))
        reward = types.SimpleNamespace(applyTo=Mock())
        quest = types.SimpleNamespace(
            doId=2, getQuestId=lambda: 'wd.1visitTia', getQuestDNA=lambda: dna,
            isComplete=lambda: True, getRewards=lambda: [reward])
        manager.completeQuest(avatar, quest)
        self.assertEqual(avatar.history, [])
        avatar.b_setTutorial.assert_not_called()
        stub.handleQuestComplete.assert_not_called()
        avatar.inventory = object()
        air.tradeMgr.createTrade.return_value = None
        manager.completeQuest(avatar, quest)
        self.assertEqual(avatar.history, [])
        air.tradeMgr.createTrade.return_value = trade
        reward.applyTo.side_effect = lambda *args: manager.completeQuest(avatar, quest)
        manager.completeQuest(avatar, quest)
        self.assertEqual(avatar.history, [dna.getQuestInt()])
        reward.applyTo.assert_called_once_with(trade, avatar)
        stub.handleQuestComplete.assert_called_once()

    def test_will_scene_can_retry_when_inventory_was_missing(self):
        from direct.showbase.MessengerGlobal import messenger

        quantities = {InventoryType.CutlassToken: 0, InventoryType.CutlassWeaponL1: 0}
        trade = types.SimpleNamespace(
            giveCutlassTraining=lambda: quantities.update({InventoryType.CutlassToken: 1}),
            giveStack=lambda item, count: quantities.update({item: count}))
        manager = manager_module.QuestManagerAI(
            types.SimpleNamespace(tradeMgr=types.SimpleNamespace(createTrade=lambda _: trade)))
        dna = QuestDB.QuestDict['c2_visit_will_turner']
        avatar = types.SimpleNamespace(
            doId=1, inventory=None, getInventory=lambda: avatar.inventory,
            getTutorial=lambda: 3, getQuestHistory=lambda: [])
        scenes = []
        quest = types.SimpleNamespace(
            doId=101, questDNA=dna, getQuestDNA=lambda: dna,
            getQuestId=lambda: 'c2_visit_will_turner',
            setFinalizeStateIndex=lambda idx: None,
            d_startFinalizeScene=lambda idx, giver: scenes.append(idx))
        npc = types.SimpleNamespace(doId=22)
        with patch.object(builtins, 'messenger', messenger, create=True):
            manager.finalizeCutscene(avatar, quest, npc=npc)
            messenger.send('quest-finalize-101')
            self.assertEqual(scenes, [0])
            self.assertNotIn(101, manager.finalizingQuests)
            avatar.inventory = types.SimpleNamespace(getStackQuantity=quantities.get)
            manager.finalizeCutscene(avatar, quest, npc=npc)
            messenger.send('quest-finalize-101')
            self.assertEqual(scenes, [0, 0, 1])
            manager.ignoreAll()
        self.assertEqual(quantities, {
            InventoryType.CutlassToken: 1, InventoryType.CutlassWeaponL1: 1})

    def test_completed_automatic_quest_retries_rewards_on_later_event(self):
        trade = object()
        manager = manager_module.QuestManagerAI(types.SimpleNamespace(
            tradeMgr=types.SimpleNamespace(createTrade=lambda _: trade)))
        dna = QuestDB.QuestDict['c3r2r1.9captureSteadman']
        stub = types.SimpleNamespace(complete=False)
        stub.handleQuestComplete = Mock(side_effect=lambda *args: setattr(stub, 'complete', True))
        avatar = types.SimpleNamespace(
            doId=1, history=[], inventory=None, getInventory=lambda: avatar.inventory,
            getQuestHistory=lambda: avatar.history,
            b_setQuestHistory=lambda value: setattr(avatar, 'history', value),
            getTutorial=lambda: 12, b_setTutorial=Mock(),
            questStatus=types.SimpleNamespace(
                getQuestStub=lambda questId: stub, getNPCInteractMode=lambda: False))
        reward = types.SimpleNamespace(applyTo=Mock())
        quest = types.SimpleNamespace(
            doId=2, questId='c3r2r1.9captureSteadman',
            getQuestId=lambda: 'c3r2r1.9captureSteadman', getQuestDNA=lambda: dna,
            isComplete=lambda: True, completeRequiresVisit=lambda: False,
            getRewards=lambda: [reward])
        manager.quests[1] = {2: quest}
        manager.completeTaskState(avatar, object())
        self.assertEqual(avatar.history, [])
        avatar.inventory = object()
        manager.completeTaskState(avatar, object())
        self.assertEqual(avatar.history, [dna.getQuestInt()])
        reward.applyTo.assert_called_once_with(trade, avatar)

    def test_cutlass_grants_only_missing_items(self):
        quantities = {InventoryType.CutlassToken: 1, InventoryType.CutlassWeaponL1: 0}
        inventory = types.SimpleNamespace(getStackQuantity=lambda item: quantities[item])
        trade = types.SimpleNamespace(
            giveCutlassTraining=Mock(side_effect=lambda: quantities.update(
                {InventoryType.CutlassToken: 1})),
            giveStack=Mock(side_effect=lambda item, count: quantities.update({item: count})))
        air = types.SimpleNamespace(tradeMgr=types.SimpleNamespace(createTrade=lambda _: trade))
        avatar = types.SimpleNamespace(doId=1, getInventory=lambda: inventory)
        manager = manager_module.QuestManagerAI(air)
        manager._giveRewards(avatar, [manager_module.CutlassReward()])
        manager._giveRewards(avatar, [manager_module.CutlassReward()])
        trade.giveCutlassTraining.assert_not_called()
        trade.giveStack.assert_called_once_with(InventoryType.CutlassWeaponL1, 1)
        quantities[InventoryType.CutlassToken] = 0
        manager._giveRewards(avatar, [manager_module.CutlassReward()])
        trade.giveCutlassTraining.assert_called_once_with()
        trade.giveStack.assert_called_once_with(InventoryType.CutlassWeaponL1, 1)

    def test_visit_restarts_interrupted_finalization_only_for_its_target(self):
        manager = manager_module.QuestManagerAI(types.SimpleNamespace())
        dna = QuestDB.QuestDict['Chapter1.rung2']
        quest = types.SimpleNamespace(
            doId=5, getQuestDNA=lambda: dna, isComplete=lambda: True)
        avatar = types.SimpleNamespace(doId=1, getQuestHistory=lambda: [])
        manager.quests[1] = {5: quest}
        event = manager_module.QuestEvent.NPCVisited()
        event.setLocation('anywhere')
        event.setNpcId('someone-else')
        callback = Mock()
        self.assertFalse(manager.completeTaskState(avatar, event, callback))
        event.setNpcId(dna.getTasks()[0].getNpcId())
        manager.finalizingQuests.add(5)
        self.assertFalse(manager.completeTaskState(avatar, event, callback))
        manager.finalizingQuests.clear()
        self.assertTrue(manager.completeTaskState(avatar, event, callback))
        callback.assert_called_once_with(quest)

    def test_will_scene_grants_cutlass_before_training_dialog(self):
        manager = manager_module.QuestManagerAI(types.SimpleNamespace())
        events = {}
        manager.acceptOnce = lambda event, callback, extraArgs=[]: events.update(
            {event: lambda: callback(*extraArgs)})
        manager._giveRewards = Mock()
        manager.completeQuest = Mock()
        avatar = types.SimpleNamespace(
            doId=1, getTutorial=lambda: 3, getQuestHistory=lambda: [])
        dna = QuestDB.QuestDict['c2_visit_will_turner']
        scenes = []
        quest = types.SimpleNamespace(
            doId=5, questDNA=dna, getQuestDNA=lambda: dna,
            getQuestId=lambda: 'c2_visit_will_turner',
            setFinalizeStateIndex=lambda idx: None,
            d_startFinalizeScene=lambda idx, giver: scenes.append((idx, giver)),
            d_amFinalized=Mock(), completeRequiresVisit=lambda: False)
        npc = types.SimpleNamespace(doId=10)
        manager.finalizeCutscene(avatar, quest, npc=npc)
        self.assertEqual(scenes, [(0, 10)])
        events.pop('quest-finalize-5')()
        self.assertEqual(scenes[-1], (1, 10))
        self.assertIsInstance(manager._giveRewards.call_args_list[0].args[1][0],
                              manager_module.CutlassReward)
        events.pop('quest-finalize-5')()
        self.assertEqual(scenes[-1], (2, 10))
        events.pop('quest-finalize-5')()
        quest.d_amFinalized.assert_called_once()
        manager.completeQuest.assert_called_once_with(avatar, quest)

    def test_swap_waits_for_creation_and_retains_old_on_failure(self):
        quests = {1: types.SimpleNamespace(doId=1, getCompleteEventString=lambda: 'complete')}
        callbacks = []
        manager = types.SimpleNamespace(
            hasQuest=lambda av, questDoId=None, questId=None: (
                questDoId in quests if questDoId is not None
                else any(getattr(q, 'questId', None) == questId for q in quests.values())),
            whenQuestIdle=lambda av, callback: callback(),
            createQuests=lambda av, ids, callback: callbacks.append(callback),
            dropQuest=lambda av, quest, completed=False: quests.pop(quest.doId))
        avatar = types.SimpleNamespace(
            doId=1, air=types.SimpleNamespace(questMgr=manager),
            getInventory=lambda: types.SimpleNamespace(getQuestList=lambda: list(quests.values())),
            b_setActiveQuest=Mock())
        messenger = types.SimpleNamespace(send=Mock())
        old = [quests[1]]
        with patch.object(builtins, 'messenger', messenger, create=True):
            DistributedQuestAvatarAI._swapQuest(avatar, old, questIds=['Chapter1.rung2'])
            old.clear()
            self.assertIn(1, quests)
            callbacks.pop()()
            self.assertIn(1, quests)
            DistributedQuestAvatarAI._swapQuest(avatar, [quests[1]], questIds=['Chapter1.rung2'])
            quests[2] = types.SimpleNamespace(doId=2, questId='Chapter1.rung2')
            callbacks.pop()()
        self.assertNotIn(1, quests)
        avatar.b_setActiveQuest.assert_called_once_with('Chapter1.rung2')

    def test_non_tutorial_swap_preserves_active_quest(self):
        old = types.SimpleNamespace(doId=1, getCompleteEventString=lambda: 'complete')
        quests = {1: old}
        callbacks = []
        manager = types.SimpleNamespace(
            hasQuest=lambda av, questDoId=None, questId=None: (
                questDoId in quests if questDoId is not None
                else any(getattr(q, 'questId', None) == questId for q in quests.values())),
            whenQuestIdle=lambda av, callback: callback(),
            createQuests=lambda av, ids, callback: callbacks.append(callback),
            dropQuest=lambda av, quest, completed=False: quests.pop(quest.doId))
        avatar = types.SimpleNamespace(
            doId=1, air=types.SimpleNamespace(questMgr=manager),
            getInventory=lambda: types.SimpleNamespace(getQuestList=lambda: list(quests.values())),
            b_setActiveQuest=Mock())
        messenger = types.SimpleNamespace(send=Mock())
        with patch.object(builtins, 'messenger', messenger, create=True):
            DistributedQuestAvatarAI._swapQuest(avatar, [old], questIds=['wd.1visitTia'])
            quests[2] = types.SimpleNamespace(doId=2, questId='wd.1visitTia')
            callbacks.pop()()
        avatar.b_setActiveQuest.assert_not_called()
        messenger.send.assert_called_once_with('complete')

    def test_completed_droppable_quest_unlinks_without_drop_event(self):
        from direct.showbase.MessengerGlobal import messenger
        from direct.showbase.DirectObject import DirectObject

        manager = manager_module.QuestManagerAI(types.SimpleNamespace())
        dna = types.SimpleNamespace(getQuestInt=lambda: 19945)
        quest = types.SimpleNamespace(
            doId=101, questId='ccbm.1poker', questDNA=dna,
            getQuestId=lambda: 'ccbm.1poker', isDroppable=lambda: True,
            getDroppedEventString=lambda: 'dropped-101', requestDelete=Mock())
        inventory = types.SimpleNamespace(
            getDoIdListCategory=lambda category: [101], setQuestList=Mock())
        avatar = types.SimpleNamespace(
            doId=1, getInventory=lambda: inventory, getQuestHistory=lambda: [19945],
            b_setQuestHistory=Mock(), getActiveQuest=lambda: 'another-quest',
            b_setActiveQuest=Mock())
        stub = QuestStub('ccbm.1poker', avatar, 19945, None, None, ())
        avatar.questStatus = types.SimpleNamespace(
            getQuestStub=lambda questId: stub, handleQuestDropped=Mock())
        manager.quests[1] = {101: quest}
        observer = DirectObject()
        dropped = Mock()
        with patch.object(builtins, 'messenger', messenger, create=True):
            observer.accept('dropped-101', dropped)
            stub.linkQuest(quest)
            manager.dropQuest(avatar, quest, completed=True)
            observer.ignoreAll()
        self.assertIsNone(stub.quest)
        dropped.assert_not_called()
        avatar.questStatus.handleQuestDropped.assert_not_called()
        avatar.b_setQuestHistory.assert_not_called()
        avatar.b_setActiveQuest.assert_not_called()
        quest.requestDelete.assert_called_once()

    def test_ladder_completes_tutorial_and_will_with_async_swaps(self):
        from direct.showbase.MessengerGlobal import messenger

        manager = manager_module.QuestManagerAI(types.SimpleNamespace())
        manager._giveRewards = Mock()
        manager.deactivateQuest = lambda av, doId: manager.quests[av.doId].pop(doId)
        pending = []
        manager.createQuests = lambda av, ids, callback: pending.append((ids, callback))
        avatar = types.SimpleNamespace(
            doId=1, history=[], ladderHistory=[], choices=[], tutorial=0, active='',
            air=types.SimpleNamespace(questMgr=manager),
            getQuestHistory=lambda: avatar.history,
            b_setQuestHistory=lambda value: setattr(avatar, 'history', value),
            getQuestLadderHistory=lambda: avatar.ladderHistory,
            b_setQuestLadderHistory=lambda value: setattr(avatar, 'ladderHistory', value),
            setQuestLadderHistory=lambda value: setattr(avatar, 'ladderHistory', value),
            getCurrentQuestChoiceContainers=lambda: avatar.choices,
            b_setCurrentQuestChoiceContainers=lambda value: setattr(avatar, 'choices', value),
            setCurrentQuestChoiceContainers=lambda value: setattr(avatar, 'choices', value),
            getTutorial=lambda: avatar.tutorial,
            b_setTutorial=lambda value: setattr(avatar, 'tutorial', value),
            getActiveQuest=lambda: avatar.active,
            b_setActiveQuest=lambda value: setattr(avatar, 'active', value),
            requestActiveQuest=lambda value: setattr(avatar, 'active', value),
            getDoId=lambda: 1)
        avatar._swapQuest = lambda *args, **kwargs: DistributedQuestAvatarAI._swapQuest(
            avatar, *args, **kwargs)
        inventory = types.SimpleNamespace(
            ids=[],
            getDoIdListCategory=lambda category: inventory.ids[:],
            setQuestList=lambda ids: setattr(inventory, 'ids', ids),
            getQuestList=lambda: list(manager.quests[1].values()))
        avatar.getInventory = lambda: inventory
        status = QuestStatus.__new__(QuestStatus)
        status.av, status.ladders, status.choiceContainers = avatar, {}, {}
        status.NPCInteractMode, status.cacheHistoryMode = False, False
        status.ladderDeleteList = []
        avatar.questStatus = status
        manager.quests[1] = {}

        def add_quest(quest_id, do_id):
            dna = QuestDB.QuestDict[quest_id]
            quest = types.SimpleNamespace(
                doId=do_id, questId=quest_id, questDNA=dna,
                getQuestId=lambda: quest_id, getQuestDNA=lambda: dna,
                getRewards=lambda: [], isComplete=lambda: True, isDroppable=lambda: False,
                getCompleteEventString=lambda: 'complete-%d' % do_id,
                getDroppedEventString=lambda: 'dropped-%d' % do_id)
            manager.quests[1][do_id] = quest
            inventory.ids.append(do_id)
            status.assignQuest(quest, True)
            return quest

        with patch.object(builtins, 'messenger', messenger, create=True):
            current = add_quest('Chapter1.rung1', 1)
            for index, expected in enumerate(
                    ('Chapter1.rung2', 'Chapter1.rung3', 'c2_visit_will_turner',
                     'c2.2defeatSkeletons'), 2):
                if index == 2:
                    manager._giveRewards.side_effect = lambda *args: manager.avatar2fsm.update(
                        {1: object()}) or True
                manager.completeQuest(avatar, current)
                self.assertIn(current.doId, manager.quests[1])
                if index == 2:
                    self.assertFalse(pending)
                    manager._giveRewards.side_effect = None
                    del manager.avatar2fsm[1]
                    manager.runDeferredQuestCompletions(avatar)
                ids, callback = pending.pop()
                self.assertEqual(ids, [expected])
                previous = current
                current = add_quest(expected, index)
                callback()
                self.assertNotIn(previous.doId, manager.quests[1])
                self.assertEqual(avatar.active, expected if index < 5 else '')
        self.assertEqual(avatar.history, [1000, 1001, 1002, 2000])
        self.assertEqual(avatar.tutorial, QuestDB.QuestDict['c2_visit_will_turner'].getCheckPoint())


if __name__ == '__main__':
    unittest.main()
