# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.instance.DistributedWelcomeWorld
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import report
from pirates.instance import DistributedInstanceBase
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TimeOfDayManager, TODGlobals
from pirates.battle import EnemyGlobals
from pirates.pvp import PVPGlobals

class DistributedWelcomeWorld(DistributedInstanceBase.DistributedInstanceBase):
    
    notify = directNotify.newCategory('DistributedWelcomeWorld')

    def announceGenerate(self):
        DistributedInstanceBase.DistributedInstanceBase.announceGenerate(self)
        if not self.playerControlledObj.hasParent():
            self.playerControlledObj.reparentTo(self)

    def delete(self):
        self.ignore('sendingLocalAvatarToJail')
        DistributedInstanceBase.DistributedInstanceBase.delete(self)

    def addWorldInterest(self, area=None):
        DistributedInstanceBase.DistributedInstanceBase.addWorldInterest(self, area)
        if area:
            area.turnOn(localAvatar)

    def removeWorldInterest(self, area=None):
        if not (area and area.gridVisContext):
            area = None
        DistributedInstanceBase.DistributedInstanceBase.removeWorldInterest(self, area)
        return

    def turnOff(self, cacheIslands=[]):
        DistributedInstanceBase.DistributedInstanceBase.turnOff(self, cacheIslands)

    def turnOn(self, av=None):
        DistributedInstanceBase.DistributedInstanceBase.turnOn(self, None)
        self._turnOnIslands()
        base.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_DEFAULT)
        return

    def getWorldPos(self, node):
        if not node.isEmpty() and self.isOn():
            return node.getPos(self)

    def getAggroRadius(self):
        return EnemyGlobals.MAX_SEARCH_RADIUS

    @report(types=['frameCount'], dConfigParam='want-jail-report')
    def localAvEnterDeath(self, av):
        DistributedInstanceBase.DistributedInstanceBase.localAvEnterDeath(self, av)
        self.d_localAvatarDied()
# okay decompiling .\pirates\instance\DistributedWelcomeWorld.pyc
