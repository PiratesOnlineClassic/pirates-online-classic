import builtins
import sys
import unittest
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

from direct.showbase import ShowBaseGlobal
from direct.showbase.MessengerGlobal import messenger
from direct.task.TaskManagerGlobal import taskMgr

builtins.messenger = messenger
builtins.taskMgr = taskMgr

from pirates.piratesbase.UniqueIdManager import UniqueIdManager

handlerModule = ModuleType('pirates.tutorial.DistributedPiratesTutorialAI')
handlerModule.DistributedPiratesTutorialAI = object
with patch.dict(sys.modules, {'pirates.tutorial.DistributedPiratesTutorialAI': handlerModule}):
    from pirates.tutorial import PiratesTutorialManagerAI as tutorial


class Avatar:
    def __init__(self, doId):
        self.doId = doId
        self.zones = []

    def getDeleteEvent(self):
        return 'test-avatar-delete-%d' % self.doId

    def d_setTutorialHandlerZone(self, zone):
        self.zones.append(zone)


class SceneObject:
    def __init__(self, doId, zoneId=42):
        self.doId = doId
        self.zoneId = zoneId
        self.handlerIds = []
        self.parent = self
        self.spawnPt = (1, 2, 3, 4)
        self.spawnPts = {tutorial.TutorialGlobals.JAIL_INTERIOR: {0: self.spawnPt}}

    def isGenerated(self):
        return True

    def getType(self):
        return 1

    def getFileName(self):
        return 'RambleshackWorld'

    def getSpawnPt(self, *args):
        return self.spawnPt

    def getParentObj(self):
        return self.parent

    def d_setTutorialHandlerId(self, doId):
        self.handlerIds.append(doId)


class Handler:
    def __init__(self, air):
        self.air = air

    def setAvatarId(self, avatarId):
        self.avatarId = avatarId

    def generateWithRequiredAndId(self, doId, parentId, zoneId):
        self.doId = doId
        messenger.send('generate-%d' % doId, [self])

    def getDeleteEvent(self):
        return 'distObjDelete-%d' % self.doId

    def requestDelete(self):
        self.air.deletedHandlers.append(self)


class TeleportManager:
    def __init__(self):
        self.avatar2fsm = {}
        self.calls = []

    def d_initiateTeleport(self, avatar, **kwargs):
        self.calls.append(kwargs)
        def cleanup():
            self.avatar2fsm.pop(avatar.doId, None)

        self.avatar2fsm[avatar.doId] = SimpleNamespace(cleanup=cleanup)


class TutorialShip:
    def __init__(self):
        self.doId = 4
        self.pose = 'sailing'
        self.resets = 0

    def resetSailingToAuthoredPose(self):
        self.resets += 1
        self.pose = 'authored'
        return True


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.air = SimpleNamespace(
            dclassesByName={'PiratesTutorialManagerAI': None},
            doId2do={}, districtId=1, deletedHandlers=[], freedZones=[],
            allocateChannel=lambda: 900, allocateZone=lambda: 901,
            deallocateZone=lambda zone: self.air.freedZones.append(zone),
            teleportMgr=TeleportManager())
        self.failures = []
        self.air.kickChannel = lambda *args: self.failures.append(args)
        self.air.uidMgr = UniqueIdManager(self.air)
        self.loads = []
        self.air.worldCreator = SimpleNamespace(loadObjectsFromFile=self.loads.append)
        self.air.tutorialManager = tutorial.PiratesTutorialManagerAI(self.air)
        self.manager = self.air.tutorialManager
        self.updates = []
        self.manager.d_enterTutorial = lambda *args: self.updates.append(args)
        self.avatar = Avatar(100)
        self.air.doId2do[100] = self.avatar
        self.handlerPatch = patch.object(tutorial, 'DistributedPiratesTutorialAI', Handler)
        self.handlerPatch.start()

    def tearDown(self):
        self.manager._deleting = True
        taskMgr.remove(self.manager._queueTaskName)
        for avatarId in list(self.manager._queued):
            self.manager._removeQueued(avatarId)
        for fsm in list(self.manager.avatar2fsm.values()):
            fsm.cleanup()
        for handler in self.air.deletedHandlers:
            messenger.send(handler.getDeleteEvent())
        self.handlerPatch.stop()

    def register(self, uid, obj):
        self.air.doId2do[obj.doId] = obj
        self.air.uidMgr.uid2doId[uid] = obj.doId
        self.air.uidMgr._requestUidCallback(uid, obj.doId)

    def test_duplicates_busy_cleanup_and_reuse(self):
        self.manager._requestTutorial(self.avatar)
        first = self.manager.avatar2fsm[self.avatar.doId]
        self.manager._requestTutorial(self.avatar)
        second = Avatar(101)
        self.air.doId2do[101] = second
        self.manager._requestTutorial(second)
        self.manager._requestTutorial(second)
        self.assertEqual(len(self.loads), 1)
        self.assertEqual(list(self.manager.avatar2fsm), [100])
        self.assertEqual(list(self.manager._queued), [101])

        world, island, interior = SceneObject(1), SceneObject(2), SceneObject(3)
        self.register(tutorial.RAMBLESHACK_REGION_UID, world)
        self.register(tutorial.TutorialGlobals.RAMBLESHACK_ISLE_UID, island)
        self.register(tutorial.TutorialGlobals.JAIL_INTERIOR, interior)
        self.assertIs(self.air.teleportMgr.calls[0]['tutorialFsm'], first)
        self.air.teleportMgr.avatar2fsm[100].cleanup()
        messenger.send('teleportDone-100')
        self.assertEqual(self.updates, [(100, island.zoneId)])
        self.assertEqual(world.handlerIds, [900])

        first.cleanup()
        first.cleanup()
        self.assertEqual(world.handlerIds, [900, 0])
        self.assertEqual(self.air.freedZones, [])
        messenger.send('distObjDelete-900')
        self.assertEqual(self.air.freedZones, [901])
        self.assertFalse(self.manager.avatar2fsm)

        taskMgr.step()
        taskMgr.step()
        self.assertEqual(len(self.loads), 1)
        self.assertIn(101, self.manager.avatar2fsm)
        self.assertFalse(self.manager._queued)

    def test_jail_spawn_comes_from_its_own_instance(self):
        self.manager._requestTutorial(self.avatar)
        world, island, interior = SceneObject(1), SceneObject(2), SceneObject(3)
        world.spawnPt = (0, 0, 0, 0)
        interior.parent = SceneObject(4)
        interior.parent.spawnPt = (25.955, 19.1, -1.5, -175)
        self.register(tutorial.RAMBLESHACK_REGION_UID, world)
        self.register(tutorial.TutorialGlobals.RAMBLESHACK_ISLE_UID, island)
        self.register(tutorial.TutorialGlobals.JAIL_INTERIOR, interior)
        self.assertEqual(self.air.teleportMgr.calls[0]['spawnPt'],
                         (25.955, 19.1, -1.5, -175))

    def test_missing_authored_jail_spawn_fails_instead_of_using_origin(self):
        self.manager._requestTutorial(self.avatar)
        interior = SceneObject(3)
        interior.spawnPts.clear()
        self.register(tutorial.RAMBLESHACK_REGION_UID, SceneObject(1))
        self.register(tutorial.TutorialGlobals.RAMBLESHACK_ISLE_UID, SceneObject(2))
        self.register(tutorial.TutorialGlobals.JAIL_INTERIOR, interior)
        self.assertFalse(self.air.teleportMgr.calls)
        self.assertFalse(self.manager.avatar2fsm)
        self.assertEqual(len(self.failures), 1)

    def test_disconnect_removes_pending_callback_and_ignores_late_delivery(self):
        self.manager._requestTutorial(self.avatar)
        fsm = self.manager.avatar2fsm[100]
        late = self.air.uidMgr.uidCallbacks[tutorial.RAMBLESHACK_REGION_UID][0][0]
        messenger.send(self.avatar.getDeleteEvent())
        self.assertNotIn(tutorial.RAMBLESHACK_REGION_UID, self.air.uidMgr.uidCallbacks)
        late(123)
        self.assertIsNone(fsm.instance)
        self.assertFalse(self.manager.avatar2fsm)

    def test_cleanup_from_uid_dispatch_does_not_remove_executing_callback(self):
        self.manager._requestTutorial(self.avatar)
        self.air.uidMgr._requestUidCallback(tutorial.RAMBLESHACK_REGION_UID, 123)
        self.assertFalse(self.manager.avatar2fsm)
        self.assertNotIn(tutorial.RAMBLESHACK_REGION_UID, self.air.uidMgr.uidCallbacks)

    def test_failed_load_cleans_up_and_blocks_unsafe_retry(self):
        def fail(filename):
            raise RuntimeError('partial load')

        self.air.worldCreator.loadObjectsFromFile = fail
        with self.assertRaisesRegex(RuntimeError, 'partial load'):
            self.manager._requestTutorial(self.avatar)
        self.assertFalse(self.manager.avatar2fsm)
        self.assertFalse(self.air.uidMgr.uidCallbacks)
        second = Avatar(101)
        self.air.doId2do[101] = second
        self.manager._requestTutorial(second)
        self.assertFalse(self.manager.avatar2fsm)
        self.assertEqual(len(self.failures), 2)

    def test_handler_callback_failure_cleans_up(self):
        def fail(*args, **kwargs):
            raise RuntimeError('teleport failed')

        self.air.teleportMgr.d_initiateTeleport = fail
        self.manager._requestTutorial(self.avatar)
        self.register(tutorial.RAMBLESHACK_REGION_UID, SceneObject(1))
        self.register(tutorial.TutorialGlobals.RAMBLESHACK_ISLE_UID, SceneObject(2))
        with patch.object(tutorial.TutorialFSM.notify, 'warning') as warning:
            self.register(tutorial.TutorialGlobals.JAIL_INTERIOR, SceneObject(3))
        self.assertIn('Traceback (most recent call last)', warning.call_args[0][0])
        self.assertIn('RuntimeError: teleport failed', warning.call_args[0][0])
        self.assertFalse(self.manager.avatar2fsm)
        self.assertEqual(len(self.air.deletedHandlers), 1)
        self.assertFalse(self.air.uidMgr.uidCallbacks)

    def test_async_handler_callback_failure_is_reraised(self):
        class DelayedHandler(Handler):
            def generateWithRequiredAndId(self, doId, parentId, zoneId):
                self.doId = doId

        def fail(*args, **kwargs):
            raise RuntimeError('teleport failed')

        self.air.teleportMgr.d_initiateTeleport = fail
        with patch.object(tutorial, 'DistributedPiratesTutorialAI', DelayedHandler):
            self.manager._requestTutorial(self.avatar)
            self.register(tutorial.RAMBLESHACK_REGION_UID, SceneObject(1))
            self.register(tutorial.TutorialGlobals.RAMBLESHACK_ISLE_UID, SceneObject(2))
            self.register(tutorial.TutorialGlobals.JAIL_INTERIOR, SceneObject(3))
            handler = self.manager.avatar2fsm[100].tutorialHandler
            with self.assertRaisesRegex(RuntimeError, 'teleport failed'):
                messenger.send('generate-900', [handler])
        self.assertFalse(self.manager.avatar2fsm)
        self.assertEqual(len(self.failures), 1)

    def test_disconnect_cancels_only_its_tutorial_teleport(self):
        self.manager._requestTutorial(self.avatar)
        self.register(tutorial.RAMBLESHACK_REGION_UID, SceneObject(1))
        self.register(tutorial.TutorialGlobals.RAMBLESHACK_ISLE_UID, SceneObject(2))
        self.register(tutorial.TutorialGlobals.JAIL_INTERIOR, SceneObject(3))
        self.assertIn(100, self.air.teleportMgr.avatar2fsm)
        messenger.send(self.avatar.getDeleteEvent())
        self.assertNotIn(100, self.air.teleportMgr.avatar2fsm)
        messenger.send('teleportDone-100')
        self.assertFalse(self.updates)

    def test_ship_reset_before_handler_cleanup_and_queued_reuse(self):
        ship = TutorialShip()
        self.register(tutorial.TutorialGlobals.STUMPY_BOAT_UID, ship)
        self.manager._requestTutorial(self.avatar)
        self.register(tutorial.RAMBLESHACK_REGION_UID, SceneObject(1))
        self.register(tutorial.TutorialGlobals.RAMBLESHACK_ISLE_UID, SceneObject(2))
        self.register(tutorial.TutorialGlobals.JAIL_INTERIOR, SceneObject(3))
        handler = self.manager.avatar2fsm[100].tutorialHandler
        originalDelete = handler.requestDelete
        handler.requestDelete = lambda: (self.assertEqual(ship.pose, 'authored'), originalDelete())
        queued = Avatar(101)
        self.air.doId2do[101] = queued
        self.manager._requestTutorial(queued)

        self.air.getAvatarIdFromSender = lambda: 100
        self.manager.allDone()
        self.assertEqual(ship.resets, 1)
        taskMgr.step()
        taskMgr.step()
        self.assertIn(101, self.manager.avatar2fsm)
        self.assertEqual(ship.pose, 'authored')

    def test_ship_reset_on_disconnect_and_startup_failure(self):
        ship = TutorialShip()
        self.register(tutorial.TutorialGlobals.STUMPY_BOAT_UID, ship)
        self.manager._requestTutorial(self.avatar)
        messenger.send(self.avatar.getDeleteEvent())
        self.assertEqual(ship.resets, 1)
        ship.pose = 'sailing'
        self.manager._requestTutorial(self.avatar)
        self.manager.avatar2fsm[100]._startTimedOut(None)
        self.assertEqual(ship.resets, 2)
        self.assertEqual(ship.pose, 'authored')

    def test_stale_fsm_does_not_reset_owned_ship(self):
        ship = TutorialShip()
        self.register(tutorial.TutorialGlobals.STUMPY_BOAT_UID, ship)
        self.manager._requestTutorial(self.avatar)
        stale = self.manager.avatar2fsm[100]
        self.manager.avatar2fsm[100] = object()
        stale.cleanup()
        self.assertEqual(ship.resets, 0)
        self.manager.avatar2fsm.clear()

    def test_reset_failure_blocks_world_reuse_but_cleans_up(self):
        ship = TutorialShip()
        ship.resetSailingToAuthoredPose = lambda: False
        self.register(tutorial.TutorialGlobals.STUMPY_BOAT_UID, ship)
        self.manager._requestTutorial(self.avatar)
        self.manager.avatar2fsm[100].cleanup()
        self.assertFalse(self.manager.avatar2fsm)
        self.assertTrue(self.manager._worldLoadFailed)
        queued = Avatar(101)
        self.air.doId2do[101] = queued
        self.manager._requestTutorial(queued)
        self.assertFalse(self.manager.avatar2fsm)
        self.assertEqual(self.failures[-1][0], self.manager.GetPuppetConnectionChannel(101))

    def test_reset_exception_is_logged_and_cleanup_continues(self):
        ship = TutorialShip()

        def fail():
            raise RuntimeError('ship reset failed')

        ship.resetSailingToAuthoredPose = fail
        self.register(tutorial.TutorialGlobals.STUMPY_BOAT_UID, ship)
        self.manager._requestTutorial(self.avatar)
        with patch.object(tutorial.TutorialFSM.notify, 'warning') as warning:
            self.manager.avatar2fsm[100].cleanup()
        self.assertIn('RuntimeError: ship reset failed', warning.call_args[0][0])
        self.assertTrue(self.manager._worldLoadFailed)
        self.assertFalse(self.manager.avatar2fsm)

    def test_refused_teleport_releases_operation(self):
        self.air.teleportMgr.d_initiateTeleport = lambda *a, **k: None
        self.manager._requestTutorial(self.avatar)
        self.register(tutorial.RAMBLESHACK_REGION_UID, SceneObject(1))
        self.register(tutorial.TutorialGlobals.RAMBLESHACK_ISLE_UID, SceneObject(2))
        self.register(tutorial.TutorialGlobals.JAIL_INTERIOR, SceneObject(3))
        self.assertFalse(self.manager.avatar2fsm)

    def test_existing_teleport_is_not_cancelled(self):
        other = SimpleNamespace(cleanup=lambda: self.fail('cancelled unrelated teleport'))
        self.air.teleportMgr.avatar2fsm[100] = other
        self.manager._requestTutorial(self.avatar)
        self.register(tutorial.RAMBLESHACK_REGION_UID, SceneObject(1))
        self.register(tutorial.TutorialGlobals.RAMBLESHACK_ISLE_UID, SceneObject(2))
        self.register(tutorial.TutorialGlobals.JAIL_INTERIOR, SceneObject(3))
        self.assertFalse(self.manager.avatar2fsm)
        self.assertIs(self.air.teleportMgr.avatar2fsm[100], other)

    def test_manager_delete_stops_active_operation(self):
        self.manager._requestTutorial(self.avatar)
        queued = Avatar(101)
        self.air.doId2do[101] = queued
        self.manager._requestTutorial(queued)
        queueTask = self.manager._queued[101][1]
        with patch.object(tutorial.DistributedObjectAI, 'delete') as delete:
            self.manager.delete()
        delete.assert_called_once_with(self.manager)
        self.assertFalse(self.manager.avatar2fsm)
        self.assertFalse(self.manager._queued)
        self.assertFalse(taskMgr.hasTaskNamed(queueTask))
        self.assertEqual(len(self.failures), 2)
        self.assertFalse(self.air.uidMgr.uidCallbacks)

    def test_request_uses_sender_and_ignores_unknown_avatar(self):
        self.air.getAvatarIdFromSender = lambda: 100
        del self.air.doId2do[100]
        self.manager.requestTutorial()
        self.assertFalse(self.loads)
        self.air.doId2do[100] = self.avatar
        self.manager.requestTutorial()
        self.assertEqual(len(self.loads), 1)
        self.assertIn(100, self.manager.avatar2fsm)

    def test_existing_scene_is_not_claimed_or_reloaded(self):
        self.air.uidMgr.uid2doId[tutorial.RAMBLESHACK_REGION_UID] = 123
        self.manager._requestTutorial(self.avatar)
        self.assertFalse(self.manager.avatar2fsm)
        self.assertFalse(self.loads)
        self.assertEqual(self.failures[0][0], self.manager.GetPuppetConnectionChannel(100))

    def test_uid_timeout_disconnects_and_cancels_wait(self):
        self.manager._requestTutorial(self.avatar)
        fsm = self.manager.avatar2fsm[100]
        self.assertTrue(taskMgr.hasTaskNamed(fsm._timeoutTaskName))
        fsm._startTimedOut(None)
        self.assertFalse(self.manager.avatar2fsm)
        self.assertFalse(self.air.uidMgr.uidCallbacks)
        self.assertFalse(taskMgr.hasTaskNamed(fsm._timeoutTaskName))
        self.assertEqual(self.failures[0][0], self.manager.GetPuppetConnectionChannel(100))

    def test_teleport_timeout_disconnects_and_cancels_teleport(self):
        self.manager._requestTutorial(self.avatar)
        fsm = self.manager.avatar2fsm[100]
        self.register(tutorial.RAMBLESHACK_REGION_UID, SceneObject(1))
        self.register(tutorial.TutorialGlobals.RAMBLESHACK_ISLE_UID, SceneObject(2))
        self.register(tutorial.TutorialGlobals.JAIL_INTERIOR, SceneObject(3))
        fsm._startTimedOut(None)
        self.assertNotIn(100, self.air.teleportMgr.avatar2fsm)
        self.assertEqual(len(self.failures), 1)
        messenger.send('teleportDone-100')
        self.assertFalse(self.updates)

    def test_success_cancels_start_timeout(self):
        self.manager._requestTutorial(self.avatar)
        fsm = self.manager.avatar2fsm[100]
        self.register(tutorial.RAMBLESHACK_REGION_UID, SceneObject(1))
        self.register(tutorial.TutorialGlobals.RAMBLESHACK_ISLE_UID, SceneObject(2))
        self.register(tutorial.TutorialGlobals.JAIL_INTERIOR, SceneObject(3))
        self.air.teleportMgr.avatar2fsm[100].cleanup()
        messenger.send('teleportDone-100')
        self.assertFalse(taskMgr.hasTaskNamed(fsm._timeoutTaskName))
        self.assertIn(100, self.manager.avatar2fsm)
        self.assertFalse(self.failures)

    def test_queue_logout_timeout_and_fifo(self):
        self.manager._requestTutorial(self.avatar)
        avatars = [Avatar(101), Avatar(102), Avatar(103)]
        for avatar in avatars:
            self.air.doId2do[avatar.doId] = avatar
            self.manager._requestTutorial(avatar)
        messenger.send(avatars[0].getDeleteEvent())
        self.manager._queueTimedOut(102)
        self.assertEqual(list(self.manager._queued), [103])
        self.assertEqual(self.failures[0][0], self.manager.GetPuppetConnectionChannel(102))
        self.manager.avatar2fsm[100].cleanup()
        taskMgr.step()
        taskMgr.step()
        self.assertEqual(list(self.manager.avatar2fsm), [103])
        self.assertFalse(self.manager._queued)

    def test_queue_full_fails_without_adding_waiter(self):
        self.manager.MAX_QUEUED = 1
        self.manager._requestTutorial(self.avatar)
        for avatarId in (101, 102):
            avatar = Avatar(avatarId)
            self.air.doId2do[avatarId] = avatar
            self.manager._requestTutorial(avatar)
        self.assertEqual(list(self.manager._queued), [101])
        self.assertEqual(self.failures[0][0], self.manager.GetPuppetConnectionChannel(102))

    def test_failed_load_notifies_queued_waiter(self):
        queued = Avatar(101)
        self.air.doId2do[101] = queued

        def fail(filename):
            self.manager._requestTutorial(queued)
            raise RuntimeError('partial load')

        self.air.worldCreator.loadObjectsFromFile = fail
        with self.assertRaisesRegex(RuntimeError, 'partial load'):
            self.manager._requestTutorial(self.avatar)
        taskMgr.step()
        taskMgr.step()
        self.assertFalse(self.manager._queued)
        self.assertEqual([entry[0] for entry in self.failures], [
            self.manager.GetPuppetConnectionChannel(100),
            self.manager.GetPuppetConnectionChannel(101)])


if __name__ == '__main__':
    unittest.main()
