from panda3d.core import Vec4
import direct.interval.IntervalGlobal as IG
from direct.fsm.StatePush import StateVar
from pirates.ship.DistributedShip import DistributedShip
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.ship.ShipRepairSpotMgr import ShipRepairSpotMgr
from pirates.pvp import PVPGlobals
from otp.otpbase import OTPGlobals

class PlayerShip(DistributedShip):
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

    def announceGenerate(self):
        if __dev__ and config.GetBool('want-broadside-assist', 0):
            self.startMonitorBroadside()
        
        if self.ownerId:
            self.inventoryInterest = self.addInterest(2, self.uniqueName('ship-inventory'))
        
        self.registerMainBuiltFunction(self._doSiegeAndPVPTeamColors)
        self._respawnLocation = None
        self._respawnResponseDelayedCall = None
        DistributedShip.announceGenerate(self)

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
        for ival in self._repairSpotIvals.values():
            ival.pause()
        
        del self._repairSpotIvals
        DistributedShip.disable(self)

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
            for d in self.sails.values():
                for (sail, distSail) in d.values():
                    sail.sailGeom.setColorScale(color)

        else:
            for d in self.sails.values():
                for (sail, distSail) in d.values():
                    sail.sailGeom.clearColorScale()
    
    def _doSiegeAndPVPTeamColors(self):
        if self.getPVPTeam():
            self._doPVPTeamColors()
        elif self.getSiegeTeam():
            pass

    def _doPVPTeamColors(self):
        team = self.getPVPTeam()
        if self.flat:
            self.flat.removeNode()
            self.flat = None
            self.loadFlat()
        
        if team:
            color = PVPGlobals.getTeamColor(team)
            for d in self.sails.values():
                for (sail, distSail) in d.values():
                    sail.sailGeom.setColorScale(color)

        else:
            for d in self.sails.values():
                for (sail, distSail) in d.values():
                    sail.sailGeom.clearColorScale()

    def getWheelInUseSV(self):
        return self._wheelInUse

    def setWheelInUse(self, wheelInUse):
        DistributedShip.setWheelInUse(self, wheelInUse)
        self._wheelInUse.set(wheelInUse)

    def canTakeWheel(self, wheel, av):
        available = True
        if self.queryGameState() in ('Pinned', 'Sinking', 'Sunk', 'OtherShipBoarded'):
            base.localAvatar.guiMgr.createWarning(PLocalizer.ShipPinnedWarning, PiratesGuiGlobals.TextFG6)
            available = False
        elif wheel.getUserId() and base.localAvatar.getDoId() != self.ownerId:
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
        elif self.ownerID and DistributedBandMember.areSameCrew(avId, self.ownerId):
            if self.captainId not in self.getCrew() and len(self.getCrew()) >= self.maxCrew - 1 and avId != self.captainId:
                base.localAvatar.guiMgr.createWarning(PLocalizer.NoBoardingCaptainReserved, PiratesGuiGlobals.TextFG6)
            else:
                allowed = True
        else:
            base.localAvatar.guiMgr.createWarning(PLocalizer.NoBoardingPermissionWarning, PiratesGuiGlobals.TextFG6)
        return allowed
    
    def setRespawnLocation(self, parentId, zoneId):
        self._respawnLocation = (parentId, zoneId)

    def setLocation(self, parentId, zoneId):
        DistributedShip.setLocation(self, parentId, zoneId)
        if self._respawnLocation is not None and self._respawnLocation == (parentId, zoneId):
            self._respawnLocation = None
            if not self._respawnResponseDelayedCall:
                self._respawnResponseDelayedCall = FrameDelayedCall('PlayerShip-respawnLocation-gridInterestComplete', Functor(base.cr.setAllInterestsCompleteCallback, self._sendRespawnLocationResponse))

    def _sendRespawnLocationResponse(self):
        self.sendUpdate('clientReachedRespawnLocation')
        self._respawnResponseDelayedCall = None

    def recoverFromSunk(self):
        self.lastAttacked = None
        DistributedShip.recoverFromSunk(self)

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
        for woodPile in self._repairSpotWoodPiles.values():
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
        ival = IG.Sequence(IG.Wait(PlayerShip.RepairSpotFadeAfter), IG.LerpColorScaleInterval(self._repairSpotHoles[locIndex], PlayerShip.RepairSpotFadeDur, Vec4(1.0, 1.0, 1.0, 0.0), blendType = 'easeInOut'))
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
        self.sendUpdate('setAllowCrewState', [
            state])

    def d_setAllowFriendState(self, state):
        self.sendUpdate('setAllowFriendState', [
            state])

    def d_setAllowGuildState(self, state):
        self.sendUpdate('setAllowGuildState', [
            state])

    def d_setAllowPublicState(self, state):
        self.sendUpdate('setAllowPublicState', [
            state])

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
    
    def hasSpace(self, avId = 0, bandMgrId = 0, bandId = 0, guildId = 0):
        if avId == self.ownerId:
            return True
        
        if self.isInCrew(avId):
            return True
        
        if self.isInCrew(self.ownerId) and len(self.crew) >= self.maxCrew:
            return False
        
        if len(self.crew) >= self.maxCrew - 1:
            return False
        
        return True

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-shipboard-report')
    def confirmSameCrewTeleport(self, toFrom, incomingAvId = 0, bandMgrId = 0, bandId = 0, guildId = 0):
        if toFrom == 'from':
            return True
        else:
            if not self.isGenerated():
                self.notify.warning('confirmSameCrewTeleport(%s)' % localAvatar.getShipString())
                return False

            if incomingAvId == self.ownerId:
                return True

            if bandMgrId and bandId and self.getAllowCrewState() and (bandMgrId, bandId) == self.getBandId():
                return True

            if localAvatar.doId == self.ownerId and self.getAllowFriendState() and self.cr.identifyFriend(incomingAvId):
                return True

            if guildId and self.getAllowGuildState() and guildId == self.getGuildId():
                return True

            if self.getAllowPublicState():
                return True
        
            return False

