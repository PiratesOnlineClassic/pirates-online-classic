import builtins
import sys
import unittest
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.showbase.MessengerGlobal import messenger
from direct.task.TaskManagerGlobal import taskMgr

builtins.messenger = messenger
builtins.taskMgr = taskMgr

from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase.UniqueIdManager import UniqueIdManager

handlerModule = ModuleType('pirates.tutorial.DistributedPiratesTutorialAI')
handlerModule.DistributedPiratesTutorialAI = object
with patch.dict(sys.modules, {'pirates.tutorial.DistributedPiratesTutorialAI': handlerModule}):
    sys.modules.pop('pirates.tutorial.PiratesTutorialManagerAI', None)
    from pirates.tutorial import PiratesTutorialManagerAI as tutorial

TutorialGlobals = tutorial.TutorialGlobals
DISTRICT_ID = 4000


class _Avatar:

    def __init__(self, doId, tutorialState):
        self.doId = doId
        self.parentId = DISTRICT_ID
        self.zoneId = 0
        self.tutorial = tutorialState

    def getDeleteEvent(self):
        return 'test-locks-avatar-delete-%d' % self.doId

    def d_setTutorialHandlerZone(self, zoneId):
        pass

    def getTutorial(self):
        return self.tutorial

    def enterLocation(self, parentId, zoneId):
        # mirrors DistributedObjectAI.setLocation's zone change notification
        oldZoneId = self.zoneId
        self.parentId, self.zoneId = parentId, zoneId
        messenger.send(DistributedObjectAI.staticGetZoneChangeEvent(self.doId), [zoneId, oldZoneId])


class _Door:

    def __init__(self, doId):
        self.doId = doId
        self.locked = False

    def b_setLocked(self, locked):
        self.locked = locked


class _SceneObject:

    def __init__(self, doId, doors=()):
        self.doId = doId
        self.zoneId = 42
        self.doors = list(doors) + [None, None]
        self.spawnPts = {TutorialGlobals.JAIL_INTERIOR: {0: (1, 2, 3, 4)}}

    def getType(self):
        return 1

    def getFileName(self):
        return 'RambleshackWorld'

    def getSpawnPt(self, *args):
        return (1, 2, 3, 4)

    def getParentObj(self):
        return self

    def d_setTutorialHandlerId(self, doId):
        pass

    def getExteriorFrontDoor(self):
        return self.doors[0]

    def getExteriorBackDoor(self):
        return self.doors[1]


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

    def __init__(self):
        self.avatar2fsm = {}

    def d_initiateTeleport(self, avatar, **kwargs):
        self.avatar2fsm[avatar.doId] = SimpleNamespace(
            cleanup=lambda: self.avatar2fsm.pop(avatar.doId, None))


class TutorialDoorLockTests(unittest.TestCase):

    def setUp(self):
        self.air = SimpleNamespace(
            dclassesByName={'PiratesTutorialManagerAI': None},
            doId2do={}, districtId=DISTRICT_ID,
            allocateChannel=lambda: 910, allocateZone=lambda: 911,
            deallocateZone=lambda zoneId: None,
            kickChannel=lambda *args: None,
            teleportMgr=_TeleportManager(),
            worldCreator=SimpleNamespace(loadObjectsFromFile=lambda fileName: None))
        self.air.uidMgr = UniqueIdManager(self.air)
        self.air.tutorialManager = tutorial.PiratesTutorialManagerAI(self.air)
        self.manager = self.air.tutorialManager
        self.manager.d_enterTutorial = lambda *args: None
        self.handlerPatch = patch.object(tutorial, 'DistributedPiratesTutorialAI', _Handler)
        self.handlerPatch.start()

        self.jailDoor = _Door(20)
        self.tavernFront, self.tavernBack = _Door(30), _Door(31)
        self.world = _SceneObject(1)
        self.island = _SceneObject(2)
        self.jail = _SceneObject(3, [self.jailDoor])
        self.tavern = _SceneObject(4, [self.tavernFront, self.tavernBack])
        for obj in (self.jailDoor, self.tavernFront, self.tavernBack, self.tavern):
            self.air.doId2do[obj.doId] = obj
        self.air.uidMgr.uid2doId[TutorialGlobals.TAVERN_INTERIOR] = self.tavern.doId

    def tearDown(self):
        for fsm in list(self.manager.avatar2fsm.values()):
            fsm.cleanup()
        messenger.send('distObjDelete-910')
        self.handlerPatch.stop()

    def register(self, uid, obj):
        self.air.doId2do[obj.doId] = obj
        self.air.uidMgr.uid2doId[uid] = obj.doId
        self.air.uidMgr._requestUidCallback(uid, obj.doId)

    def startTutorial(self, tutorialState):
        avatar = _Avatar(100, tutorialState)
        self.air.doId2do[avatar.doId] = avatar
        self.manager._requestTutorial(avatar)
        self.register(tutorial.RAMBLESHACK_REGION_UID, self.world)
        self.register(TutorialGlobals.RAMBLESHACK_ISLE_UID, self.island)
        self.register(TutorialGlobals.JAIL_INTERIOR, self.jail)
        avatar.enterLocation(self.jail.doId, 2710)
        self.air.teleportMgr.avatar2fsm[avatar.doId].cleanup()
        messenger.send('teleportDone-%d' % avatar.doId)
        return avatar

    def locks(self):
        return (self.jailDoor.locked, self.tavernFront.locked, self.tavernBack.locked)

    def test_doors_lock_behind_the_avatar_as_it_passes_each_stage(self):
        avatar = self.startTutorial(PiratesGlobals.TUT_STARTED)
        self.assertEqual(self.locks(), (False, False, False))

        # making the pirate inside the jail does not lock the jail it is still in...
        avatar.tutorial = PiratesGlobals.TUT_MADE_PIRATE
        avatar.enterLocation(self.jail.doId, 2711)
        self.assertEqual(self.locks(), (False, False, False))

        # ...walking out onto the island locks the jail behind it.
        avatar.enterLocation(self.island.doId, 100)
        self.assertEqual(self.locks(), (True, False, False))

        # the tavern stays open until the sea chest has been handed over...
        avatar.enterLocation(self.tavern.doId, 200)
        avatar.tutorial = PiratesGlobals.TUT_GOT_SEACHEST
        avatar.enterLocation(self.tavern.doId, 201)
        self.assertEqual(self.locks(), (True, False, False))

        # ...and both of its doors lock once the avatar leaves it.
        avatar.enterLocation(self.island.doId, 101)
        self.assertEqual(self.locks(), (True, True, True))

    def test_resuming_at_a_later_checkpoint_locks_the_passed_doors(self):
        avatar = self.startTutorial(PiratesGlobals.TUT_GOT_SEACHEST)
        # resumed pirates start in the jail again and may still walk out of it...
        self.assertEqual(self.locks(), (False, True, True))
        avatar.enterLocation(self.island.doId, 100)
        self.assertEqual(self.locks(), (True, True, True))

    def test_doors_unlock_for_the_next_pirate(self):
        avatar = self.startTutorial(PiratesGlobals.TUT_GOT_SEACHEST)
        avatar.enterLocation(self.island.doId, 100)
        self.manager.avatar2fsm[avatar.doId].cleanup()
        self.assertEqual(self.locks(), (False, False, False))

        # a finished tutorial no longer follows the avatar around.
        avatar.enterLocation(self.island.doId, 102)
        self.assertEqual(self.locks(), (False, False, False))


class BuildingDoorLockTests(unittest.TestCase):

    def test_locked_door_does_not_hand_out_its_interior(self):
        from pirates.world.DistributedBuildingDoorAI import DistributedBuildingDoorAI

        sent = []
        door = DistributedBuildingDoorAI.__new__(DistributedBuildingDoorAI)
        door.doId = 20
        door.locked = True
        door.interiorDoId = 3
        door.air = SimpleNamespace(
            doId2do={100: SimpleNamespace(doId=100)},
            getAvatarIdFromSender=lambda: 100)
        door.d_setPrivateInteriorInstance = lambda *args: sent.append(args)
        door.requestPrivateInteriorInstance()
        self.assertEqual(sent, [])


if __name__ == '__main__':
    unittest.main()
