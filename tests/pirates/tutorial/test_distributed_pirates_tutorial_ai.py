import importlib
import sys
import types
import unittest
from unittest.mock import patch


def _load_handler_module():
    module_name = 'pirates.tutorial.DistributedPiratesTutorialAI'
    if module_name in sys.modules:
        return sys.modules[module_name]

    quest_package = importlib.import_module('pirates.quest')
    npc_package = importlib.import_module('pirates.npc')
    original_quest_db = sys.modules.get('pirates.quest.QuestDB')
    original_quest_attr = getattr(quest_package, 'QuestDB', None)
    original_constants = sys.modules.get('pirates.quest.QuestConstants')
    original_constants_attr = getattr(quest_package, 'QuestConstants', None)
    original_townfolk = sys.modules.get(
        'pirates.npc.DistributedNPCTownfolkAI')
    original_townfolk_attr = getattr(
        npc_package, 'DistributedNPCTownfolkAI', None)

    quest_db = types.ModuleType('pirates.quest.QuestDB')
    quest_db.QuestDict = {}
    townfolk_module = types.ModuleType(
        'pirates.npc.DistributedNPCTownfolkAI')
    townfolk_module.DistributedNPCTownfolkAI = type(
        'DistributedNPCTownfolkAI', (), {})
    quest_constants = types.ModuleType('pirates.quest.QuestConstants')
    quest_constants.LocationIds = types.SimpleNamespace(
        PORT_ROYAL_ISLAND='1150922126.8dzlu')
    sys.modules['pirates.quest.QuestDB'] = quest_db
    sys.modules['pirates.quest.QuestConstants'] = quest_constants
    quest_package.QuestConstants = quest_constants
    sys.modules['pirates.npc.DistributedNPCTownfolkAI'] = townfolk_module
    quest_package.QuestDB = quest_db
    npc_package.DistributedNPCTownfolkAI = (
        townfolk_module.DistributedNPCTownfolkAI)

    try:
        return importlib.import_module(module_name)
    finally:
        if original_constants is None:
            sys.modules.pop('pirates.quest.QuestConstants', None)
        else:
            sys.modules['pirates.quest.QuestConstants'] = original_constants
        if original_constants_attr is None:
            delattr(quest_package, 'QuestConstants')
        else:
            quest_package.QuestConstants = original_constants_attr

        if original_quest_db is None:
            sys.modules.pop('pirates.quest.QuestDB', None)
        else:
            sys.modules['pirates.quest.QuestDB'] = original_quest_db
        if original_quest_attr is None:
            delattr(quest_package, 'QuestDB')
        else:
            quest_package.QuestDB = original_quest_attr

        if original_townfolk is None:
            sys.modules.pop('pirates.npc.DistributedNPCTownfolkAI', None)
        else:
            sys.modules['pirates.npc.DistributedNPCTownfolkAI'] = (
                original_townfolk)
        if original_townfolk_attr is None:
            delattr(npc_package, 'DistributedNPCTownfolkAI')
        else:
            npc_package.DistributedNPCTownfolkAI = original_townfolk_attr


Handler = _load_handler_module().DistributedPiratesTutorialAI


class _Notify:

    def warning(self, *args):
        pass

    def info(self, *args):
        pass


class _Avatar:

    def __init__(self, do_id):
        self.doId = do_id
        self.returnLocation = ''
        self.inventory = object()

    def getReturnLocation(self):
        return self.returnLocation

    def b_setReturnLocation(self, returnLocation):
        self.returnLocation = returnLocation

    def getInventory(self):
        return self.inventory


class _QuestManager:

    def __init__(self, events):
        self.events = events
        self.signalCount = 0
        self.waitRegistered = False
        self.eventPending = False
        self.waitReleased = False

    def tutorialJROnStage(self, avatar):
        self.signalCount += 1
        self.events.append(('tutorialJROnStage', avatar.doId))
        if self.waitRegistered:
            self.waitReleased = True
        else:
            self.eventPending = True

    def registerJollyRogerWait(self):
        self.waitRegistered = True
        if self.eventPending:
            self.waitReleased = True
            self.eventPending = False


class _Air:

    def __init__(self, avatar, quest_manager):
        self.doId2do = {avatar.doId: avatar}
        self.questMgr = quest_manager
        self.senderId = avatar.doId

    def getAvatarIdFromSender(self):
        return self.senderId


class DistributedPiratesTutorialAITests(unittest.TestCase):

    def makeHandler(self):
        events = []
        avatar = _Avatar(42)
        quest_manager = _QuestManager(events)
        handler = Handler.__new__(Handler)
        handler.avatarId = avatar.doId
        handler.air = _Air(avatar, quest_manager)
        handler.notify = _Notify()
        handler.request = lambda state: events.append(('state', state))
        return handler, avatar, quest_manager, events

    def sinkUndeadShip(self, handler, sunk=True):
        handler._getTutorialShip = lambda: types.SimpleNamespace(
            isTutorialTargetSunk=lambda: sunk)

    def test_target_practice_done_requires_owner_sender(self):
        handler, avatar, quest_manager, events = self.makeHandler()
        handler.air.senderId = avatar.doId + 1

        handler.targetPracticeDone()

        self.assertEqual(quest_manager.signalCount, 0)
        self.assertEqual(events, [])

    def test_target_practice_signal_is_latched_before_jolly_wait(self):
        handler, avatar, quest_manager, events = self.makeHandler()
        self.sinkUndeadShip(handler)

        handler.targetPracticeDone()

        self.assertEqual(quest_manager.signalCount, 1)
        self.assertTrue(quest_manager.eventPending)
        self.assertFalse(quest_manager.waitReleased)
        self.assertEqual(
            events,
            [('tutorialJROnStage', avatar.doId),
             ('state', 'TargetPracticeDone')])

        quest_manager.registerJollyRogerWait()

        self.assertTrue(quest_manager.waitReleased)
        self.assertFalse(quest_manager.eventPending)

    def test_sailing_requires_owner_and_current_tutorial_handler(self):
        handler, avatar, _, events = self.makeHandler()
        handler.air.tutorialManager = types.SimpleNamespace(
            avatar2fsm={avatar.doId: types.SimpleNamespace(
                tutorialHandler=handler)})
        handler.air.senderId = avatar.doId + 1
        handler.startSailingStumpy()
        self.assertEqual(events, [])

        handler.air.senderId = avatar.doId
        handler.air.tutorialManager.avatar2fsm[avatar.doId].tutorialHandler = None
        handler.startSailingStumpy()
        self.assertEqual(events, [])

    def test_sailing_starts_only_the_authored_tutorial_ship(self):
        handler, avatar, _, events = self.makeHandler()
        handler.air.tutorialManager = types.SimpleNamespace(
            avatar2fsm={avatar.doId: types.SimpleNamespace(
                tutorialHandler=handler)})
        world = types.SimpleNamespace(getFileName=lambda: 'RambleshackWorld')

        class Ship:
            tutorialBuilder = types.SimpleNamespace(parent=world)

            def __init__(self):
                self.uid = '1124236671.37jubutler'
                self.startCount = 0
                self.targetCount = 0

            def getUniqueId(self):
                return self.uid

            def startSailing(self):
                self.startCount += 1
                return True

            def spawnTutorialTarget(self):
                self.targetCount += 1
                return object()

        ship = Ship()
        handler.air.uidMgr = types.SimpleNamespace(
            justGetMeMeObject=lambda uid: ship)
        ship_module = types.ModuleType('pirates.ship.TutorialShipAI')
        ship_module.TutorialShipAI = Ship
        world_globals = types.ModuleType('pirates.world.WorldGlobals')
        world_globals.PiratesTutorialSceneFileBase = 'RambleshackWorld'
        world_package = importlib.import_module('pirates.world')

        with patch.dict(sys.modules, {
                'pirates.ship.TutorialShipAI': ship_module,
                'pirates.world.WorldGlobals': world_globals,
        }), patch.object(world_package, 'WorldGlobals', world_globals, create=True):
            ship.uid = 'wrong-uid'
            handler.startSailingStumpy()
            self.assertEqual(ship.startCount, 0)
            self.assertEqual(events, [])

            ship.uid = '1124236671.37jubutler'
            handler.startSailingStumpy()

        self.assertEqual(ship.startCount, 1)
        self.assertEqual(ship.targetCount, 1)
        self.assertEqual(events, [('state', 'Sailing')])


    def test_target_practice_sends_new_pirate_to_port_royal(self):
        handler, avatar, _, _ = self.makeHandler()
        self.sinkUndeadShip(handler)

        handler.targetPracticeDone()

        self.assertEqual(avatar.returnLocation, '1150922126.8dzlu')

    def test_target_practice_needs_the_undead_ship_sunk(self):
        handler, avatar, quest_manager, events = self.makeHandler()
        self.sinkUndeadShip(handler, sunk=False)

        handler.targetPracticeDone()

        self.assertEqual(quest_manager.signalCount, 0)
        self.assertEqual(events, [])
        self.assertNotEqual(avatar.returnLocation, '1150922126.8dzlu')

    def test_enter_act0_waits_for_inventory_then_starts_first_quest(self):
        handler, avatar, _, events = self.makeHandler()
        avatar.inventory = None
        handler.uniqueName = lambda name: '%s-%d' % (name, avatar.doId)
        handler._ensureFirstQuest = lambda av: events.append(('firstQuest', av.doId))
        handler.d_inventoryFailed = lambda: events.append(('inventoryFailed',))
        handler.getAvatar = lambda: avatar
        tasks = []
        module = sys.modules[Handler.__module__]

        with patch.object(module, 'taskMgr', create=True) as task_mgr:
            task_mgr.doMethodLater.side_effect = (
                lambda delay, method, name: tasks.append(method))
            handler.clientEnterAct0Tutorial()

        self.assertEqual(events, [('state', 'Act0Tutorial')])
        self.assertEqual(len(tasks), 1)

        self.assertEqual(tasks[0](None), module.Task.again)
        avatar.inventory = object()
        self.assertEqual(tasks[0](None), module.Task.done)
        self.assertEqual(events[-1], ('firstQuest', avatar.doId))

    def test_enter_act0_reports_inventory_failure(self):
        handler, avatar, _, events = self.makeHandler()
        avatar.inventory = None
        handler.getAvatar = lambda: avatar
        handler.d_inventoryFailed = lambda: events.append(('inventoryFailed',))
        handler._inventoryWaitAttempts = 0
        module = sys.modules[Handler.__module__]
        waitForInventory = getattr(handler, '_%s__waitForInventory' % Handler.__name__)

        for attempt in range(Handler.INVENTORY_WAIT_ATTEMPTS - 1):
            self.assertEqual(waitForInventory(None), module.Task.again)
        self.assertEqual(waitForInventory(None), module.Task.done)
        self.assertEqual(events, [('inventoryFailed',)])


if __name__ == '__main__':
    unittest.main()
