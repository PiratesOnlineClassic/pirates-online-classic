import builtins
import sys
import unittest
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

from direct.showbase import ShowBaseGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.showbase.MessengerGlobal import messenger
from direct.task.TaskManagerGlobal import taskMgr

builtins.messenger = messenger
builtins.taskMgr = taskMgr

from pirates.piratesbase.UniqueIdManager import UniqueIdManager

handlerModule = ModuleType('pirates.tutorial.DistributedPiratesTutorialAI')
handlerModule.DistributedPiratesTutorialAI = object
with patch.dict(sys.modules, {'pirates.tutorial.DistributedPiratesTutorialAI': handlerModule}):
    sys.modules.pop('pirates.tutorial.PiratesTutorialManagerAI', None)
    from pirates.tutorial import PiratesTutorialManagerAI as tutorial

DISTRICT_ID = 4000


class _Avatar:

    def __init__(self, doId):
        self.doId = doId
        self.parentId = 0
        self.zoneId = 0
        self.handlerZones = []

    def getDeleteEvent(self):
        return 'test-order-avatar-delete-%d' % self.doId

    def d_setTutorialHandlerZone(self, zoneId):
        self.handlerZones.append(zoneId)

    def enterLocation(self, parentId, zoneId):
        # mirrors DistributedObjectAI.setLocation's zone change notification
        oldZoneId = self.zoneId
        self.parentId, self.zoneId = parentId, zoneId
        messenger.send(DistributedObjectAI.staticGetZoneChangeEvent(self.doId), [zoneId, oldZoneId])


class _SceneObject:

    def __init__(self, doId, zoneId=42):
        self.doId = doId
        self.zoneId = zoneId
        self.handlerIds = []
        self.spawnPts = {tutorial.TutorialGlobals.JAIL_INTERIOR: {0: (1, 2, 3, 4)}}

    def getType(self):
        return 1

    def getFileName(self):
        return 'RambleshackWorld'

    def getSpawnPt(self, *args):
        return (1, 2, 3, 4)

    def getParentObj(self):
        return self

    def d_setTutorialHandlerId(self, doId):
        self.handlerIds.append(doId)


class _Handler:

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
        pass


class _TeleportManager:

    def __init__(self, events):
        self.avatar2fsm = {}
        self.events = events

    def d_initiateTeleport(self, avatar, **kwargs):
        self.events.append(('jailTeleport', avatar.parentId))
        self.avatar2fsm[avatar.doId] = SimpleNamespace(
            cleanup=lambda: self.avatar2fsm.pop(avatar.doId, None))


class TutorialJailTeleportOrderTests(unittest.TestCase):

    def setUp(self):
        self.events = []
        self.air = SimpleNamespace(
            dclassesByName={'PiratesTutorialManagerAI': None},
            doId2do={}, districtId=DISTRICT_ID,
            allocateChannel=lambda: 900, allocateZone=lambda: 901,
            deallocateZone=lambda zoneId: None,
            kickChannel=lambda *args: self.events.append(('kick',) + args),
            teleportMgr=_TeleportManager(self.events),
            worldCreator=SimpleNamespace(loadObjectsFromFile=lambda fileName: None))
        self.air.uidMgr = UniqueIdManager(self.air)
        self.air.tutorialManager = tutorial.PiratesTutorialManagerAI(self.air)
        self.manager = self.air.tutorialManager
        self.manager.d_enterTutorial = lambda *args: self.events.append(('enterTutorial',) + args)
        self.avatar = _Avatar(100)
        self.air.doId2do[self.avatar.doId] = self.avatar
        self.handlerPatch = patch.object(tutorial, 'DistributedPiratesTutorialAI', _Handler)
        self.handlerPatch.start()

    def tearDown(self):
        for fsm in list(self.manager.avatar2fsm.values()):
            fsm.cleanup()
        messenger.send('distObjDelete-900')
        self.handlerPatch.stop()

    def register(self, uid, obj):
        self.air.doId2do[obj.doId] = obj
        self.air.uidMgr.uid2doId[uid] = obj.doId
        self.air.uidMgr._requestUidCallback(uid, obj.doId)

    def loadScene(self):
        world, island, interior = _SceneObject(1), _SceneObject(2), _SceneObject(3)
        self.register(tutorial.RAMBLESHACK_REGION_UID, world)
        self.register(tutorial.TutorialGlobals.RAMBLESHACK_ISLE_UID, island)
        self.register(tutorial.TutorialGlobals.JAIL_INTERIOR, interior)
        return island

    def test_jail_teleport_waits_for_the_client_to_enter_the_district(self):
        # the client's login teleport request arrives while it is still in the uber zone...
        self.manager._requestTutorial(self.avatar)
        island = self.loadScene()
        self.assertEqual(self.events, [])

        # ...an unrelated location change does not start the teleport either...
        self.avatar.enterLocation(DISTRICT_ID + 1, 5)
        self.assertEqual(self.events, [])

        # ...only once PlayGame's teleportToShard places the avatar in the district.
        self.avatar.enterLocation(DISTRICT_ID, self.avatar.doId)
        self.assertEqual(self.events, [('jailTeleport', DISTRICT_ID)])

        # the jail teleport then completes through the normal client teleport flow,
        # and only afterwards is the client told about the tutorial.
        self.avatar.enterLocation(DISTRICT_ID, 7)
        self.assertEqual(len(self.events), 1)
        self.air.teleportMgr.avatar2fsm[self.avatar.doId].cleanup()
        messenger.send('teleportDone-%d' % self.avatar.doId)
        self.assertEqual(self.events[-1], ('enterTutorial', self.avatar.doId, island.zoneId))
        self.assertEqual(self.avatar.handlerZones, [901])

    def test_avatar_already_in_the_district_teleports_immediately(self):
        self.avatar.parentId = DISTRICT_ID
        self.manager._requestTutorial(self.avatar)
        self.loadScene()
        self.assertEqual(self.events, [('jailTeleport', DISTRICT_ID)])

    def test_disconnect_while_waiting_stops_listening(self):
        self.manager._requestTutorial(self.avatar)
        self.loadScene()
        messenger.send(self.avatar.getDeleteEvent())
        self.assertFalse(self.manager.avatar2fsm)

        self.avatar.enterLocation(DISTRICT_ID, self.avatar.doId)
        self.assertEqual(self.events, [])


if __name__ == '__main__':
    unittest.main()
