"""
Shared fakes for the minigame AI unit tests.  These stand in for the AI
repository, inventories and task manager so the table logic can be run
without a running Astron cluster or any game resources.
"""

from collections import defaultdict
from types import SimpleNamespace
from unittest.mock import Mock

from pirates.uberdog.UberDogGlobals import InventoryType


class FakeTaskMgr:
    def __init__(self):
        self.tasks = {}

    def doMethodLater(self, delay, func, name, extraArgs=None, appendTask=False):
        self.tasks[name] = (func, list(extraArgs or []), appendTask)

    def add(self, func, name, extraArgs=None, appendTask=False):
        self.doMethodLater(0, func, name, extraArgs, appendTask)

    def remove(self, name):
        self.tasks.pop(name, None)

    def hasTask(self, name):
        return name in self.tasks

    def runTask(self, name):
        func, args, appendTask = self.tasks.pop(name)
        if appendTask:
            args = args + [None]
        func(*args)

    def run(self, limit=500):
        count = 0
        while self.tasks and count < limit:
            self.runTask(sorted(self.tasks)[0])
            count += 1

        return count


class FakeInventory:
    def __init__(self, gold):
        self.stacks = {InventoryType.GoldInPocket: gold}
        self.accumulators = {}

    def getGoldInPocket(self):
        return self.stacks.get(InventoryType.GoldInPocket, 0)

    def setGoldInPocket(self, gold):
        self.stacks[InventoryType.GoldInPocket] = gold

    def getStackQuantity(self, stackType):
        return self.stacks.get(stackType, 0)

    def b_setStackQuantity(self, stackType, quantity):
        self.stacks[stackType] = quantity

    def getReputation(self, repType):
        return self.accumulators.get(repType, 0)

    def setReputation(self, repType, quantity):
        self.accumulators[repType] = quantity


class FakeAvatar:
    def __init__(self, doId):
        self.doId = doId

    def getDeleteEvent(self):
        return 'delete-%d' % self.doId

    def getName(self):
        return 'Pirate %d' % self.doId


def makeAir(inventories, sender):
    avatars = dict((doId, FakeAvatar(doId)) for doId in inventories)
    air = SimpleNamespace(
        doId2do=avatars,
        getAvatarIdFromSender=lambda: sender[0],
        inventoryManager=SimpleNamespace(getInventory=lambda doId: inventories.get(doId)),
        questMgr=Mock(),
        logPotentialHacker=Mock(),
        dclassesByName=defaultdict(Mock))
    return air, avatars


def makeTable(cls, inventories, sender, aiSeats=()):
    air, avatars = makeAir(inventories, sender)
    table = cls(air)
    table.doId = 5000
    table.sendUpdate = Mock()
    table.sendUpdateToAvatarId = Mock()
    table.acceptOnce = Mock()
    table.ignore = Mock()
    for seatIndex in aiSeats:
        table.seats[seatIndex] = table.AISeat

    return table, avatars


def sentFields(obj, fieldName):
    return [c[0][1] for c in obj.sendUpdate.call_args_list if c[0][0] == fieldName]


def sentToAvatar(obj, fieldName):
    return [(c[0][0], c[0][2]) for c in obj.sendUpdateToAvatarId.call_args_list if c[0][1] == fieldName]
