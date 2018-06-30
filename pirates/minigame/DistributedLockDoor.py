# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.minigame.DistributedLockDoor
from direct.interval.IntervalGlobal import *
from pirates.minigame import DistributedLock


class DistributedLockDoor(DistributedLock.DistributedLock):

    def __init__(self, cr):
        DistributedLock.DistributedLock.__init__(self, cr)
        self.isDoor = 1

    def loadModel(self):
        self.table = loader.loadModel('models/props/jail_door_03')
        self.table.setScale(1.0, 1.0, 1.0)
        self.table.reparentTo(self)

    def finalOpen(self):
        colNode = self.table.find('**/collisions')
        colNode.stash()
        self.hinge = self.table.find('**/jail_door')
        lidopener = LerpHprInterval(self.hinge, 1, Vec3(-140, 0, 0))
        lidopener.start()
        self.setAllowInteract(False)


# okay decompiling .\pirates\minigame\DistributedLockDoor.pyc
