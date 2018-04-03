# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.ship.PlayerShip
import direct.interval.IntervalGlobal as IG
from direct.fsm.StatePush import StateVar
from otp.otpbase import OTPGlobals
from pandac.PandaModules import Vec4
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.pvp import PVPGlobals
from pirates.ship.DistributedShip import DistributedShip
from pirates.ship.ShipRepairSpotMgr import ShipRepairSpotMgr


class PlayerShip(DistributedShip):
    __module__ = __name__
    RepairSpotFadeAfter = 2.0
    RepairSpotFadeDur = 3.0

    def __init__(self, cr):
        DistributedShip.__init__(self, cr)
        self._respawnLocation = None
        self.checkAnchor = None
        self.lastAttacked = None
        self.bounty = 0
        self.allowCrewState = True
        self.allowFriendState = True
        self.allowGuildState = False
        self.allowPublicState = False
        return

    def generate(self):
        DistributedShip.generate(self)
        self._repairSpotWoodPile = None
        self._repairSpotWoodPiles = {}
        self._repairSpotHole = None
        self._repairSpotHoleFixed = None
        self._repairSpotHoles = {}
        self._repairSpotIvals = {}
        self._wheelInUse = StateVar(False)
        self._repairSpotMgr = ShipRepairSpotMgr(self.cr, self.doId)
        return

    def announceGenerate(self):
        if __dev__ and config.GetBool('want-broadside-assist', 0):
            self.startMonitorBroadside()
        if self.ownerId:
            self.inventoryInterest = self.addInterest(2, self.uniqueName('ship-inventory'))
        self.registerMainBuiltFunction(self._doSiegeAndPVPTeamColors)
        self._respawnLocation = None
        self._respawnResponseDelayedCall = None
        DistributedShip.announceGenerate(self)
        return

    def disable(self):
        self._wheelInUse.destroy()
        if self.ownerId:
            if self.inventoryInterest:
                self.removeInterest(self.inventoryInterest)
            del self.inventoryInterest
        if self._respawnResponseDelayedCall:
            self._respawnResponseDelayedCall.destroy()
            self._respawnResponseDelayedCall = None
        if self.checkAnchor:
            self.checkAnchor.remove()
            self.checkAnchor = None
        self._repairSpotMgr.destroy()
        for ival in self._repairSpotIvals.itervalues():
            ival.pause()

        del self._repairSpotIvals
        DistributedShip.disable(self)
        return

    def getNPCship(self):
        return False

    def setShipClass(self, shipClass):
        DistributedShip.setShipClass(self, shipClass)
        self._repairSpotMgr.updateShipClass(self.shipClass)

    def setHp(self, hp):
        DistributedShip.setHp(self, hp)
        self._repairSpotMgr.updateHp(self.Hp)

    def setMaxHp(self, maxHp):
        DistributedShip.setMaxHp(self, maxHp)
        self._repairSpotMgr.updateMaxHp(self.maxHp)

    def setSp(self, sp):
        DistributedShip.setSp(self, sp)
        self._repairSpotMgr.updateSp(self.Sp)

    def setMaxSp(self, maxSp):
        DistributedShip.setMaxSp(self, maxSp)
        self._repairSpotMgr.updateMaxSp(self.maxSp)

    def setSiegeTeam(self, team):
        different = team != self.getSiegeTeam()
        DistributedShip.setSiegeTeam(self, team)
        if different:
            self._doSiegeAndPVPTeamColors()
            self._repairSpotMgr.updateSiegeTeam(team)

    def setPVPTeam(self, team):
        different = team != self.getPVPTeam()
        DistributedShip.setPVPTeam(self, team)
        if different:
            self._doSiegeAndPVPTeamColors()
            self._repairSpotMgr.updatePVPTeam(team)

    def _doSiegeColors(self):
        team = self.getSiegeTeam()
        if self.flat:
            self.flat.removeNode()
            self.flat = None
            self.loadFlat()
        if team:
            color = PVPGlobals.getSiegeColor(team)
            for d in self.sails.itervalues():
                for sail, distSail in d.itervalues():
                    sail.sailGeom.setColorScale(color)

        for d in self.sails.itervalues():
            for sail, distSail in d.itervalues():
                sail.sailGeom.clearColorScale()

        return

    def _doSiegeAndPVPTeamColors(self):
        if self.getPVPTeam():
            self._doPVPTeamColors()
        else:
            if self.getSiegeTeam():
                pass

    def _doPVPTeamColors(self):
        team = self.getPVPTeam()
        if self.flat:
            self.flat.removeNode()
            self.flat = None
            self.loadFlat()
        if team:
            color = PVPGlobals.getTeamColor(team)
            for d in self.sails.itervalues():
                for sail, distSail in d.itervalues():
                    sail.sailGeom.setColorScale(color)

        for d in self.sails.itervalues():
            for sail, distSail in d.itervalues():
                sail.sailGeom.clearColorScale()

        return

    def getWheelInUseSV(self):
        return self._wheelInUse

    def setWheelInUse(self, wheelInUse):
        DistributedShip.setWheelInUse(self, wheelInUse)
        self._wheelInUse.set(wheelInUse)

    def canTakeWheel(self, wheel, av):
        available = True
        if self.queryGameState() in ('Pinned', ):
            base.localAvatar.guiMgr.createWarning(PLocalizer.ShipPinnedWarning, PiratesGuiGlobals.TextFG6)
            available = False
        else:
            if wheel.getUserId() and base.localAvatar.getDoId() != self.ownerId:
                base.localAvatar.guiMgr.createWarning(PLocalizer.AlreadyInUseWarning, PiratesGuiGlobals.TextFG6)
                available = False
        return available

    def startMonitorBroadside(self):
        taskMgr.doMethodLater(0.5, self.monitorBroadsideAim, self.uniqueName('monitorBroadside'))

    def stopMonitorBroadside(self):
        taskMgr.remove(self.uniqueName('monitorBroadside'))

    def monitorBroadsideAim(self, task):
        if self.oldLeftTarget:
            self.oldLeftTarget.setColor(1, 1, 1, 1)
            self.oldLeftTarget = None
        if self.oldRightTarget:
            self.oldRightTarget.setColor(1, 1, 1, 1)
            self.oldRightTarget = None
        if self.broadside:
            if self.broadside[1]:
                leftTarget = self.autoAimBroadside(0)
                if leftTarget:
                    target = self.cr.doId2do.get(leftTarget)
                    if target:
                        target.setColor(1, 0, 0, 1)
                        self.oldLeftTarget = target
                rightTarget = self.autoAimBroadside(1)
                if rightTarget:
                    target = self.cr.doId2do.get(rightTarget)
                    if target:
                        target.setColor(1, 0, 0, 1)
                        self.oldRightTarget = target
        return Task.again

    def canBoard(self, avId):
        allowed = False
        if self.getSiegeTeam() or self.getPVPTeam():
            allowed = True
        else:
            if self.ownerID and DistributedBandMember.areSameCrew(avId, self.ownerId):
                if self.captainId not in self.getCrew() and len(self.getCrew()) >= self.maxCrew - 1 and avId != self.captainId:
                    base.localAvatar.guiMgr.createWarning(PLocalizer.NoBoardingCaptainReserved, PiratesGuiGlobals.TextFG6)
                else:
                    allowed = True
            else:
                base.localAvatar.guiMgr.createWarning(PLocalizer.NoBoardingPermissionWarning, PiratesGuiGlobals.TextFG6)
        return allowed

    def setRespawnLocation(self, parentId, zoneId):
        self._respawnLocation = (
         parentId, zoneId)

    def setLocation(self, parentId, zoneId):
        DistributedShip.setLocation(self, parentId, zoneId)
        if self._respawnLocation is not None and self._respawnLocation == (parentId, zoneId):
            self._respawnLocation = None
            if not self._respawnResponseDelayedCall:
                self._respawnResponseDelayedCall = FrameDelayedCall('PlayerShip-respawnLocation-gridInterestComplete', Functor(base.cr.setAllInterestsCompleteCallback, self._sendRespawnLocationResponse))
        if self.isGenerated():
            self.cnode.setCurrL(zoneId)
        return

    def _sendRespawnLocationResponse(self):
        self.sendUpdate('clientReachedRespawnLocation')
        self._respawnResponseDelayedCall = None
        return

    def recoverFromSunk(self):
        self.lastAttacked = None
        DistributedShip.recoverFromSunk(self)
        return

    def attacked(self):
        self.lastAttacked = globalClock.getFrameTime()

    def attackTimerRemaining(self):
        timer = 0
        if self.lastAttacked:
            timer = int(30 - (globalClock.getFrameTime() - self.lastAttacked))
        return timer

    def __recheckAbleDropAnchor(self, task):
        self.checkAnchor = None
        self.checkAbleDropAnchor()
        return

    def checkAbleDropAnchor(self):
        if localAvatar.doId == self.steeringAvId:
            if self.shipStatusDisplay:
                if localAvatar.getPort():
                    remaining = self.attackTimerRemaining()
                    if self.getSiegeTeam() and remaining > 0:
                        self.shipStatusDisplay.disableAnchorButton()
                        localAvatar.guiMgr.createWarning(PLocalizer.CannotDockYet % remaining, PiratesGuiGlobals.TextFG6)
                        self.checkAnchor = taskMgr.doMethodLater(remaining, self.__recheckAbleDropAnchor, 'checkAnchor')
                    else:
                        self.shipStatusDisplay.enableAnchorButton()
                else:
                    self.shipStatusDisplay.disableAnchorButton()

    def _addRepairSpotModels(self):
        if not self._repairSpotWoodPile:
            self._repairSpotWoodPile = loader.loadModel('models/props/repair_spot_wood')
            collFloors = self._repairSpotWoodPile.find('**/collision_floor')
            if not collFloors.isEmpty():
                collideMask = collFloors.getCollideMask()
                collideMask ^= PiratesGlobals.FloorBitmask
                collideMask |= PiratesGlobals.ShipFloorBitmask
                collFloors.setCollideMask(collideMask)
        for locIndex in PVPGlobals.ShipClass2repairLocators[self.shipClass].getValue():
            locName = PVPGlobals.RepairSpotLocatorNames[locIndex]
            self._repairSpotWoodPiles[locName] = self.root.attachNewNode('repairSpotWoodPile-%s' % locName)
            self._repairSpotWoodPile.instanceTo(self._repairSpotWoodPiles[locName])
            locator = self.getLocator(locName)
            self._repairSpotWoodPiles[locName].setPosHpr(locator.getPos(), locator.getHpr())

    def _removeRepairSpotModels(self):
        for woodPile in self._repairSpotWoodPiles.itervalues():
            woodPile.detachNode()

        self._repairSpotWoodPiles = {}

    def _placeRepairSpotModel(self, locIndex, model):
        locName = PVPGlobals.RepairSpotLocatorNames[locIndex]
        parentNode = self.root.attachNewNode('repairSpotHole-%s' % locName)
        parentNode.setTransparency(1, 100)
        model.instanceTo(parentNode)
        locator = self.getLocator(locName)
        parentNode.setPosHpr(locator.getPos(), locator.getHpr())
        self._repairSpotHoles[locIndex] = parentNode

    def _removeRepairSpotModel(self, locIndex):
        if locIndex in self._repairSpotHoles:
            self._repairSpotHoles[locIndex].detachNode()
            del self._repairSpotHoles[locIndex]

    def _fadeOutRepairSpotModel(self, locIndex):
        if locIndex in self._repairSpotIvals:
            self._repairSpotIvals[locIndex].pause()
        self._repairSpotHoles[locIndex].setTransparency(1, 100)
        ival = IG.Sequence(IG.Wait(PlayerShip.RepairSpotFadeAfter), IG.LerpColorScaleInterval(self._repairSpotHoles[locIndex], PlayerShip.RepairSpotFadeDur, Vec4(1.0, 1.0, 1.0, 0.0), blendType='easeInOut'))
        ival.start()
        self._repairSpotIvals[locIndex] = ival

    def _addRepairSpotHoles(self):
        if not self._repairSpotHole:
            repairSpotHoleModels = loader.loadModel('models/props/repair_spot_hole')
            self._repairSpotHole = repairSpotHoleModels.find('**/floor_hole')
            self._repairSpotHoleFixed = repairSpotHoleModels.find('**/floor_hole_fixed')
        for locIndex in PVPGlobals.ShipClass2repairLocators[self.shipClass].getValue():
            self._removeRepairSpotModel(locIndex)
            self._placeRepairSpotModel(locIndex, self._repairSpotHole)

    def _removeRepairSpotHoles(self):
        for locIndex in PVPGlobals.ShipClass2repairLocators[self.shipClass].getValue():
            self._removeRepairSpotModel(locIndex)
            if self._repairSpotHoleFixed:
                self._placeRepairSpotModel(locIndex, self._repairSpotHoleFixed)
                self._fadeOutRepairSpotModel(locIndex)
                self._repairSpotIvals[locIndex] = IG.Sequence(self._repairSpotIvals[locIndex], IG.Func(self._removeRepairSpotModel, locIndex))

    def setSiegeBounty(self, bounty):
        self.bounty = bounty
        self.setGUIBounty(bounty)

    def setupSmoothing(self):
        self.activateSmoothing(1, 1)
        self.smoother.setDelay(0.0)
        broadcastPeriod = 0.2
        self.smoother.setMaxPositionAge(broadcastPeriod * 1.25 * 10)
        self.smoother.setExpectedBroadcastPeriod(broadcastPeriod)
        self.smoother.setDefaultToStandingStill(False)
        self.setSmoothWrtReparents(True)
        self.startSmooth()

    def b_setAllowCrewState(self, state):
        self.d_setAllowCrewState(state)
        self.setAllowCrewState(state)

    def b_setAllowFriendState(self, state):
        self.d_setAllowFriendState(state)
        self.setAllowFriendState(state)

    def b_setAllowGuildState(self, state):
        self.d_setAllowGuildState(state)
        self.setAllowGuildState(state)

    def b_setAllowPublicState(self, state):
        self.d_setAllowPublicState(state)
        self.setAllowPublicState(state)

    def d_setAllowCrewState(self, state):
        self.sendUpdate('setAllowCrewState', [state])

    def d_setAllowFriendState(self, state):
        self.sendUpdate('setAllowFriendState', [state])

    def d_setAllowGuildState(self, state):
        self.sendUpdate('setAllowGuildState', [state])

    def d_setAllowPublicState(self, state):
        self.sendUpdate('setAllowPublicState', [state])

    def setAllowCrewState(self, state):
        self.allowCrewState = state
        if self.shipStatusDisplay:
            self.shipStatusDisplay.setAllowCrew(state)

    def setAllowFriendState(self, state):
        self.allowFriendState = state
        if self.shipStatusDisplay:
            self.shipStatusDisplay.setAllowFriends(state)

    def setAllowGuildState(self, state):
        self.allowGuildState = state
        if self.shipStatusDisplay:
            self.shipStatusDisplay.setAllowGuild(state)

    def setAllowPublicState(self, state):
        self.allowPublicState = state
        if self.shipStatusDisplay:
            self.shipStatusDisplay.setAllowPublic(state)

    def getAllowCrewState(self):
        return self.allowCrewState

    def getAllowFriendState(self):
        return self.allowFriendState

    def getAllowGuildState(self):
        return self.allowGuildState

    def getAllowPublicState(self):
        return self.allowPublicState
# okay decompiling .\pirates\ship\PlayerShip.pyc
