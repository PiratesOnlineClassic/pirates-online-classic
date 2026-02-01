from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import report
from pirates.instance import DistributedInstanceBase
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TODGlobals
from pirates.battle import EnemyGlobals
from pirates.pvp import PVPGlobals
from pirates.effects.FireworkGlobals import *
from pirates.effects.FireworkShowManager import FireworkShowManager

class DistributedMainWorld(DistributedInstanceBase.DistributedInstanceBase):
    notify = directNotify.newCategory('DistributedMainWorld')
    
    def __init__(self, cr):
        DistributedInstanceBase.DistributedInstanceBase.__init__(self, cr)
        self.pvpRespawnCall = None
    
    def announceGenerate(self):
        DistributedInstanceBase.DistributedInstanceBase.announceGenerate(self)
        self.accept('sendingLocalAvatarToJail', self.resetIslandZoneLevels)
        self._siegeMgrInterest = self.addInterest(777, 'siegeMgr')
        if not self.playerControlledObj.hasParent():
            self.playerControlledObj.reparentTo(self)

    def disable(self):
        self.removeInterest(self._siegeMgrInterest)
        self._siegeMgrInterest = None
        if self.pvpRespawnCall:
            self.pvpRespawnCall.destroy()
            self.pvpRespawnCall = None
        
        DistributedInstanceBase.DistributedInstanceBase.disable(self)
    
    def delete(self):
        self.ignore('sendingLocalAvatarToJail')
        DistributedInstanceBase.DistributedInstanceBase.delete(self)
    
    def addWorldInterest(self, area = None):
        DistributedInstanceBase.DistributedInstanceBase.addWorldInterest(self, area)
        if area:
            area.turnOn(localAvatar)
    
    def removeWorldInterest(self, area = None):
        if not (area and area.gridVisContext):
            area = None
        DistributedInstanceBase.DistributedInstanceBase.removeWorldInterest(self, area)
    
    def turnOff(self, cacheIslands = []):
        self.disableFireworkShow()
        DistributedInstanceBase.DistributedInstanceBase.turnOff(self, cacheIslands)

    def turnOn(self, av = None):
        DistributedInstanceBase.DistributedInstanceBase.turnOn(self, None)
        if self.worldGrid and av and av.getShip():
            self.worldGrid.turnOn(av)
        
        self._turnOnIslands()
        base.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_DEFAULT)

    @report(types=['frameCount'], dConfigParam='want-jail-report')
    def localAvEnterDeath(self, av):
        DistributedInstanceBase.DistributedInstanceBase.localAvEnterDeath(self, av)
        self.d_localAvatarDied()
        if av.getSiegeTeam():
            self._startPvpRespawn(PVPGlobals.MainWorldAvRespawnDelay)
    
    def _startPvpRespawn(self, delay):
        self.pvpRespawnCall = DelayedCall(self._doPvpRespawn, name = 'PVPrespawn', delay = delay)

    def _doPvpRespawn(self):
        
        try:
            localAvatar
        except:
            return

        if hasattr(localAvatar, 'ship') and localAvatar.ship and not localAvatar.ship.isSailable():
            self._startPvpRespawn(0.2)
            return
        
        self.hideDeathLoadingScreen(localAvatar)
        localAvatar.b_setGameState('LandRoam')

    @report(types=['frameCount'], dConfigParam='want-jail-report')
    def localAvExitDeath(self, av):
        DistributedInstanceBase.DistributedInstanceBase.localAvExitDeath(self, av)

    @report(types=['frameCount'], dConfigParam='want-jail-report')
    def resetIslandZoneLevels(self):
        for island in self.islands.values():
            island.setZoneLevel(3)
    
    def getWorldPos(self, node):
        if not node.isEmpty() and self.isOn():
            return node.getPos(self)
    
    def getAggroRadius(self):
        return EnemyGlobals.MAX_SEARCH_RADIUS

    def enableFireworkShow(self, timestamp = 0.0, showType = None):
        if showType != None:
            if not self.fireworkShowMgr:
                self.fireworkShowMgr = FireworkShowManager()
                self.fireworkShowMgr.enable(showType, timestamp)
            
        elif base.fourthOfJuly:
            if not self.fireworkShowMgr:
                self.fireworkShowMgr = FireworkShowManager()
                self.fireworkShowMgr.enable(FireworkShowType.FourthOfJuly, timestamp)

    def disableFireworkShow(self):
        if self.fireworkShowMgr:
            self.fireworkShowMgr.disable()
            self.fireworkShowMgr = None

    if __dev__:
        
        def printIslands(self):
            for (doId, island) in self.islands.items():
                print(doId, repr(island))

