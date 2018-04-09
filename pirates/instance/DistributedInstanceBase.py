# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.instance.DistributedInstanceBase
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from pirates.world.WorldNode import WorldNode
from pirates.world.DistributedGameArea import DistributedGameArea
from pirates.world.DistributedOceanGrid import DistributedOceanGrid
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TimeOfDayManager
from pirates.piratesgui import PiratesGuiGlobals
from direct.interval.IntervalGlobal import *
from pirates.uberdog import DistributedInventoryBase
from pirates.cutscene import Cutscene
from pirates.battle import EnemyGlobals
import random

class DistributedInstanceBase(DistributedObject, WorldNode):
    __module__ = __name__

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        WorldNode.__init__(self)
        self.islands = {}
        self.playerSpawnPts = {}
        self.playerBootPts = {}
        self.cutsceneOriginNodes = {}
        self.type = PiratesGlobals.INSTANCE_GENERIC
        self.spawnInfo = None
        self.pendingJail = None
        self._onOffState = False
        if hasattr(localAvatar, 'gameFSM') and localAvatar.gameFSM:
            localAvatar.gameFSM.setDefaultGameState('LandRoam')

        self.worldGrid = None
        self.fireworkShowMgr = None

    def disable(self):
        DistributedObject.disable(self)
        WorldNode.disable(self)
        self.ignoreAll()

    def delete(self):
        if self.pendingJail:
            self.cr.relatedObjectMgr.abortRequest(self.pendingJail)
            self.pendingJail = None

        del self.islands
        del self.playerSpawnPts
        del self.playerBootPts
        del self.worldGrid
        WorldNode.delete(self)
        DistributedObject.delete(self)

    def announceGenerate(self):
        WorldNode.announceGenerate(self)
        DistributedObject.announceGenerate(self)

    def queryActiveQuests(self):

        def receiveActiveQuests(inventory):
            if inventory:
                for currQuest in inventory.getQuestList():
                    currQuest.setActive()

        DistributedInventoryBase.DistributedInventoryBase.getInventory(localAvatar.inventoryId,
            receiveActiveQuests)

    def getInstanceNodePath(self):
        return render

    def setWorldGrid(self, grid):
        self.worldGrid = grid
        if not self._onOffState and self.worldGrid:
            self.worldGrid.turnOff()

    def getWater(self):
        if self.worldGrid:
            if hasattr(self.worldGrid, 'water'):
                return self.worldGrid.water

        return None

    def addCutsceneOriginNode(self, node, name):
        self.cutsceneOriginNodes[name] = node

    def getCutsceneOriginNode(self, name):
        if name in self.cutsceneOriginNodes:
            return self.cutsceneOriginNodes.get(name)

        node = render.find('**/%s' % name)
        if not node.isEmpty():
            return node

    def addPlayerSpawnPt(self, parent, spawnPt, index=-1):
        spawnPts = self.playerSpawnPts.setdefault(parent.getDoId(), {})
        spawnPts.setdefault(index, []).append(spawnPt)

    def getPlayerSpawnPt(self, parentDoId, index=-1):
        spawnPts = self.playerSpawnPts.get(parentDoId, {})
        spawnPt = random.choice(spawnPts.get(index, [None]))
        if not spawnPt and index >= 0:
            return getPlayerSpawnPt(parentDoId, index=-1)
        else:
            return spawnPt

    def addPlayerBootPt(self, areaUid, bootPt, parentDoId):
        self.playerBootPts[areaUid] = [bootPt, parentDoId]

    def getPlayerBootPt(self, areaUid):
        return self.playerBootPts.get(areaUid)

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    @report(types=['deltaStamp', 'args'], prefix='------', dConfigParam=('want-jail-report',
                                                                         'want-teleport-report'))
    def setSpawnInfo(self, xPos, yPos, zPos, h, spawnZone, parents):
        self.spawnInfo = [(xPos, yPos, zPos, h, 0, 0), spawnZone, parents]
        messenger.send(self.uniqueName('spawnInfoReceived'))

    def getAvTeam(self, av):
        return [False, None]

    def setAvTeam(self, av, team):
        return [False, None]

    def localAvEnterDeath(self, av):
        self.showDeathLoadingScreen(av)

    def localAvExitDeath(self, av):
        pass

    def showDeathLoadingScreen(self, av):
        base.cr.loadingScreen.showHint()
        base.cr.loadingScreen.showTarget(jail=True)
        base.cr.loadingScreen.show()

    def hideDeathLoadingScreen(self, av):
        base.cr.loadingScreen.hide()

    def updateShipProximityText(self, ship):
        pass

    def handleShipUse(self, ship):
        return False

    def updateTreasureProximityText(self, treasure):
        pass

    def handleTreasureUse(self, treasure):
        return False

    def handleDeposit(self, team, avId, bankId):
        pass

    def handleUseKey(self, interactiveObj):
        return False

    def setLocalAvatarDefaultGameState(self, loot):
        localAvatar.gameFSM.setDefaultGameState('LandRoam')

    def handleLocalAvatarEnterWater(self):
        localAvatar.b_setGameState('WaterRoam')

    def handleLocalAvatarExitWater(self):
        localAvatar.b_setGameState('LandRoam')

    def handleChildArrive(self, child, zoneId):
        DistributedObject.handleChildArrive(self, child, zoneId)
        if isinstance(child, DistributedOceanGrid):
            child.setWorld(self)
            self.setWorldGrid(child)
            for key in self.islands:
                self.islands[key].addToOceanSeapatch()

    def handleChildLeave(self, child, zoneId):
        if isinstance(child, DistributedOceanGrid):
            if child == self.worldGrid:
                self.setWorldGrid(None)

        DistributedObject.handleChildLeave(self, child, zoneId)

    @report(types=['frameCount', 'args'], dConfigParam=['want-connector-report', 'want-jail-report'])
    def addWorldInterest(self, area=None):
        self.cr.setActiveWorld(self)
        self.turnOn(localAvatar)

    @report(types=['frameCount', 'args'], dConfigParam=['want-connector-report', 'want-jail-report'])
    def removeWorldInterest(self, area=None):
        if area:
            self.turnOff([area])
        else:
            self.turnOff()

    @report(types=['frameCount', 'args'], dConfigParam=['want-connector-report', 'want-jail-report'])
    def turnOff(self, cacheIslands=[]):
        self._turnOffIslands(cacheIslands)
        self.stash()
        self._onOffState = False
        if self.worldGrid:
            self.worldGrid.turnOff()

    @report(types=['frameCount', 'args'], dConfigParam=['want-connector-report', 'want-jail-report'])
    def turnOn(self, av=None):
        self.unstash()
        self._onOffState = True
        self.worldGrid.turnOn(av)

    def _turnOffIslands(self, cacheIslands=[]):
        for island in self.islands.values():
            cache = island in cacheIslands
            island.turnOff(cache)

    def _turnOnIslands(self):
        for island in self.islands.values():
            island.turnOn()

    def isOn(self):
        return self._onOffState

    def enteredSphere(self, params, collEntry):
        msgName = params[0]
        sphere = collEntry.getIntoNodePath()
        uniqueId = sphere.getTag('uid')
        if not uniqueId:
            uniqueId = params[1]

        objId = None
        if collEntry.getFromNodePath().hasNetTag('avId'):
            objId = int(collEntry.getFromNodePath().getNetTag('avId'))
            if objId:
                messenger.send(msgName + PiratesGlobals.SPHERE_ENTER_SUFFIX, [uniqueId, objId])

        if collEntry.getFromNodePath().hasNetTag('shipId'):
            objId = int(collEntry.getFromNodePath().getNetTag('shipId'))
            if objId:
                messenger.send(msgName + PiratesGlobals.SPHERE_ENTER_SUFFIX, [uniqueId, objId])

        if msgName == PiratesGlobals.LOCATION_SPHERE:
            displayName = PLocalizer.LocationNames.get(uniqueId, '')
            base.localAvatar.guiMgr.createTitle(displayName, PiratesGuiGlobals.TextFG2)
            parentUid = sphere.getTag('parentUid')
            parentDoId = base.cr.uidMgr.getDoId(parentUid)
            areaParent = base.cr.doId2do[parentDoId]
            locationInfo = areaParent.getLocationInfo(uniqueId)
            #f locationInfo:
            #    localAvatar.sendUpdate('enterAreaSphere', [uniqueId, parentUid])

    def exitedSphere(self, params, collEntry):
        msgName = params[0]
        sphere = collEntry.getIntoNodePath()
        uniqueId = sphere.getTag('uid')
        if not uniqueId:
            uniqueId = params[1]

        objId = None
        if collEntry.getFromNodePath().hasNetTag('avId'):
            objId = int(collEntry.getFromNodePath().getNetTag('avId'))
            if objId:
                messenger.send(msgName + PiratesGlobals.SPHERE_EXIT_SUFFIX, [uniqueId, objId])

        if collEntry.getFromNodePath().hasNetTag('shipId'):
            objId = int(collEntry.getFromNodePath().getNetTag('shipId'))
            if objId:
                messenger.send(msgName + PiratesGlobals.SPHERE_EXIT_SUFFIX, [uniqueId, objId])

        if msgName == PiratesGlobals.LOCATION_SPHERE:
            parentUid = sphere.getTag('parentUid')
            parentDoId = base.cr.uidMgr.getDoId(parentUid)
            areaParent = base.cr.doId2do[parentDoId]
            locationInfo = areaParent.getLocationInfo(uniqueId)
            #if locationInfo:
            #    print 'left area %s' % locationInfo[2]
            #    localAvatar.sendUpdate('leaveAreaSphere', [uniqueId, parentUid])

    def d_localAvatarDied(self):
        self.sendUpdate('avatarDied')

    @report(types=['frameCount', 'args'], dConfigParam='want-jail-report')
    def sendLocalAvatarToJail(self, jailDoId, jailWorldParentId, jailWorldZone):
        messenger.send('sendingLocalAvatarToJail')
        if jailDoId == 0 and jailWorldParentId == 0 and jailWorldZone == 0:
            localAvatar.b_setGameState('LandRoam')
        else:
            currentWorld = self
            parentObj = localAvatar.getParentObj()
            if isinstance(parentObj, DistributedGameArea):
                currentArea = parentObj
            else:
                currentArea = None

            alreadyHere = parentObj is base.cr.doId2do.get(jailDoId)

            @report(types=['frameCount'], dConfigParam='want-jail-report')
            def loadJailWorld():
                localAvatar.setInterest(jailWorldParentId, jailWorldZone, [
                 'instanceInterest-Jail'])

                if self.pendingJail:
                    self.cr.relatedObjectMgr.abortRequest(self.pendingJail)

                self.pendingJail = self.cr.relatedObjectMgr.requestObjects([jailDoId],
                    eachCallback=jailAreaLoaded)

            @report(types=['frameCount'], dConfigParam='want-jail-report')
            def jailAreaLoaded(jailArea):
                self.pendingJail = None
                if isinstance(currentWorld, DistributedInstanceBase):
                    currentWorld.removeWorldInterest()
                    localAvatar.clearInterestNamed(None, ['instanceInterest'])
                    localAvatar.replaceInterestTag('instanceInterest-Jail', 'instanceInterest')

                world = jailArea.getParentObj()
                world.addWorldInterest(jailArea)
                localAvatar.reparentTo(jailArea)
                localAvatar.setPos(Point3(0))
                zone = jailArea.getZoneFromXYZ(Point3(0))
                localAvatar.b_setLocation(jailArea.doId, zone)
                if alreadyHere:
                    jailArea.sendUpdate('avatarAlreadyInJail', [])

            ship = localAvatar.getShip()
            if ship:
                localAvatar.removeFromShip(ship)

            loadJailWorld()

    def getWorldPos(self, node):
        return

    def getAggroRadius(self):
        return EnemyGlobals.INTERIOR_MAX_SEARCH_RADIUS

    def enableFireworkShow(self, timestamp=0.0, showType=None):
        pass

    def disableFireworkShow(self):
        pass
# okay decompiling .\pirates\instance\DistributedInstanceBase.pyc
