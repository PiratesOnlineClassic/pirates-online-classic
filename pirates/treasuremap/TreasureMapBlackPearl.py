import random

from pirates.ship import ShipPilot
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import report
from direct.task import Task
from pandac.PandaModules import *
from pirates.cutscene import Cutscene, CutsceneData
from pirates.effects.DarkWaterFog import DarkWaterFog
from pirates.piratesbase import (PiratesGlobals, PLocalizer, TimeOfDayManager, TODGlobals)
from pirates.ship import ShipGlobals
from pirates.treasuremap import (DistributedTreasureMapInstance, TreasureMapBlackPearlGlobals, TreasureMapRulesPanel)
from pirates.uberdog import DistributedInventoryBase
from pirates.world import FortBarricade


class TreasureMapBlackPearl(DistributedTreasureMapInstance.DistributedTreasureMapInstance):
    
    notify = directNotify.newCategory('TreasureMapBlackPearl')

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def __init__(self, cr):
        DistributedTreasureMapInstance.DistributedTreasureMapInstance.__init__(self, cr)
        self.cutscene = None
        self.camIval = None
        self.attackShipsSunk = 0
        self.pearlId = 0
        self.goliathId = 0
        self.readyToPlayCutscene = 0
        base.musicMgr.requestFadeOut('island-general')
        self.pearlRequest = None
        self.pearl = None
        self.goliath = None
        self.rulesPanel = None
        self.messageHolder = None
        self.warned = False
        self.newEventSphereNodePath = None
        self.fortRequest = None
        self.forts = []
        self.fortIds = []
        self.barricades = {}
        self.barricadesDestroyed = []
        self.barricadesWarned = []
        self.fortIdToUidDict = {}
        self.stageInstructions = [PLocalizer.BlackPearlStageZero, PLocalizer.BlackPearlStageOne, PLocalizer.BlackPearlStageTwo, PLocalizer.BlackPearlStageThree, PLocalizer.BlackPearlStageFour, PLocalizer.BlackPearlLoser, PLocalizer.BlackPearlWinner, PLocalizer.BlackPearlWaitCutscene, PLocalizer.BlackPearlWaitCutscene2]
        from pirates.ship import ShipGlobals
        if launcher.getPhaseComplete(5):
            ShipGlobals.preprocessBlackPearl()
            ShipGlobals.preprocessGoliath()
        else:
            base.accept('phaseComplete-5', ShipGlobals.preprocessBlackPearl)
            base.accept('phaseComplete-5', ShipGlobals.preprocessGoliath)
        base.tmbp = self
        self.requestEndCutSent = False
        self.pearlCopy = None
        self.goliathCopy = None
        self.pearlCopyIval = None
        self.goliathCopyIval = None
        self.stageFourCutscene = False
        self.stageFourIval = None
        self.cameraState = None
        self.cameraSubject = None

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def delete(self):
        DistributedTreasureMapInstance.DistributedTreasureMapInstance.delete(self)
        if self.pearl:
            self.pearl.localAvatarExitShip()
        if self.newEventSphereNodePath:
            self.newEventSphereNodePath.removeNode()
            self.newEventSphereNodePath = None
        if self.camIval:
            self.camIval.pause()
            self.camIval = None
        if self.rulesPanel:
            self.rulesPanel.destroy()
            self.rulesPanel = None
        if self.stageFourIval:
            self.stageFourIval.pause()
            self.stageFourIval = None
        if self.stageFourCutscene:
            self.stopPearlAndGoliathCopy()
        taskMgr.remove('fireNPCCannon')
        taskMgr.remove('disablePearlInteractions')
        self.stopCutsceneTask()
        if self.fortRequest:
            if self.cr and self.cr.relatedObjectMgr:
                self.cr.relatedObjectMgr.abortRequest(self.fortRequest)
        if self.pearlRequest:
            if self.cr and self.cr.relatedObjectMgr:
                self.cr.relatedObjectMgr.abortRequest(self.pearlRequest)
        base.musicMgr.requestFadeOut('victory')
        base.musicMgr.request('island-general', priority=1)
        self.customTimeOfDayOff()
        self.ignoreAll()

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def announceGenerate(self):
        DistributedTreasureMapInstance.DistributedTreasureMapInstance.announceGenerate(self)
        self.customTimeOfDayOn()
        f = render.getFog()
        f.setLinearRange(500, 2500)

    def startCutsceneTask(self):
        if not taskMgr.hasTaskNamed('tryToGoToStageOneTask'):
            taskMgr.doMethodLater(0.5, self.tryToStartCutscene, 'tryToGoToCutscene')

    def stopCutsceneTask(self):
        taskMgr.remove('tryToGoToCutscene')

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def tryToStartCutscene(self, task):
        pier = render.find('**/pier_port_royal_1deck')
        if not pier.isEmpty() and 'Teleport' not in localAvatar.gameFSM.state:
            self.playCutscene()
            return Task.done
        task.delayTime = 0.2
        return Task.again

    def __requestState(self, state):
        self.sendUpdate('requestState', [state])

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def setFortIds(self, fortIds):
        self.fortIds = fortIds
        self.cr.relatedObjectMgr.abortRequest(self.fortRequest)
        self.fortRequest = self.cr.relatedObjectMgr.requestObjects(self.fortIds, eachCallback=self.__gotOneFort)

    def __gotOneFort(self, fort):
        self.notify.debug('got one fort %s' % fort)
        if self.state == 'StageThree' or self.state == 'StageFour':
            fort.showFortHpMeter()

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def setState(self, state, timestamp=None):
        self.request(state)

    def setBlackPearlId(self, doId):
        self.pearlId = doId
        self.pearl = base.cr.doId2do.get(doId)
        if not self.pearl:
            self.cr.relatedObjectMgr.abortRequest(self.pearlRequest)
            self.pearlRequest = self.cr.relatedObjectMgr.requestObjects([self.pearlId], eachCallback=self.__gotPearl)

    def getPearl(self):
        if self.pearlId:
            pearl = base.cr.doId2do.get(self.pearlId)
            return pearl

    def __gotPearl(self, pearl):
        self.pearlRequest = None
        self.pearl = pearl
        self.accept('setShipHp-%s' % pearl.doId, self.handleHpWarning)

    def handleHpWarning(self, hp, maxHp):
        if not self.warned and hp < 1000:
            self.warned = True
            localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.BlackPearlWarningLow)

    def __gotGoliath(self, goliath):
        self.goliath = goliath[0]

    def setGoliathId(self, doId):
        self.goliathId = doId
        self.goliath = base.cr.doId2do.get(doId)
        if not self.goliath:
            base.cr.relatedObjectMgr.requestObjects([self.goliathId], allCallback=self.__gotGoliath)

    def setAttackShipIds(self, shipIds):
        self.attackShipIds = shipIds
        for shipId in shipIds:
            ship = base.cr.doId2do.get(shipId)
            if ship:
                ship.classNameText.hide()

    def stashAttackShips(self):
        if self.attackShipIds:
            for shipId in self.attackShipIds:
                ship = base.cr.doId2do.get(shipId)
                if ship:
                    ship.root.stash()

    def unstashAttackShips(self):
        if self.attackShipIds:
            for shipId in self.attackShipIds:
                ship = base.cr.doId2do.get(shipId)
                if ship:
                    ship.root.unstash()

    def hideAttackShipTags(self):
        if self.attackShipIds:
            for shipId in self.attackShipIds:
                ship = base.cr.doId2do.get(shipId)
                if ship:
                    ship.classNameText.hide()
                    ship.hideName()

    def showAttackShipTags(self):
        if self.attackShipIds:
            for shipId in self.attackShipIds:
                ship = base.cr.doId2do.get(shipId)
                if ship:
                    ship.classNameText.show()

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def customTimeOfDayOff(self):
        if base.cr.timeOfDayManager:
            base.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_DEFAULT)
            base.cr.timeOfDayManager.unpause()

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def customTimeOfDayOn(self):
        base.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_DEFAULT)
        if base.cr.timeOfDayManager.cycleType == TODGlobals.TOD_REGULAR_CYCLE:
            base.cr.timeOfDayManager.request(base.cr.timeOfDayManager.getStateName(PiratesGlobals.TOD_NIGHT), 0)
        base.cr.timeOfDayManager.pause()

    def stashGoliath(self):
        if self.goliath:
            self.goliath.stash()

    def stashPearlAndGoliath(self):
        self.stashGoliath()
        blackPearl = self.getPearl()
        if blackPearl:
            blackPearl.stash()

    def unstashPearlAndGoliath(self):
        blackPearl = self.getPearl()
        if blackPearl:
            blackPearl.unstash()
        if self.goliath:
            self.goliath.unstash()

    def stashPortCollision(self):
        deck = render.find('**/pier_port_royal_1deck')
        if not deck.isEmpty():
            shipCol = deck.find('**/collision_ship')
            if not shipCol.isEmpty():
                shipCol.stash()

    def showRulesPanel(self, stage):
        if not self.messageHolder:
            self.messageHolder = aspect2d.attachNewNode('message')
            self.rulesPanel = TreasureMapRulesPanel.TreasureMapRulesPanel(PLocalizer.BlackPearlTMName, PLocalizer.BlackPearlStageOne, self.messageHolder)
        self.messageHolder.setPos(Vec3(0, 0, 0.85))
        instructions = self.stageInstructions[stage]
        self.rulesPanel.setInstructions(instructions)
        self.rulesPanel.show()

    def _startFog(self):
        self._fog = DarkWaterFog(radius=500)
        self._fog.reparentTo(localAvatar)
        self._fog.p0.renderer.getColorInterpolationManager().addConstant(0.0, 1.0, Vec4(0.9, 0.9, 0.9, 0.4), 1)
        self._fog.p0.renderer.getColorInterpolationManager().clearSegment(1)
        self._fog.startLoop()
        self._moveFogDownEvent = 'moveFogDown'
        taskMgr.add(self._fogPositionTask, self._moveFogDownEvent, priority=49)

    def _stopFog(self):
        if hasattr(self, '_fog'):
            taskMgr.remove(self._moveFogDownEvent)
            del self._moveFogDownEvent
            self._fog.stopLoop()
            self._fog.destroy()
            del self._fog

    def _fogPositionTask(self, task):
        self._fog.setZ(render, 0)
        return task.cont

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def enterWaitClientsReady(self):
        DistributedTreasureMapInstance.DistributedTreasureMapInstance.enterWaitClientsReady(self)
        base.transitions.fadeOut()

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def exitWaitClientsReady(self):
        base.transitions.fadeIn()

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def enterStageOne(self):
        ShipPilot.ShipPilot.MAX_STRAIGHT_SAIL_BONUS = 0
        self.stashPortCollision()
        self.stashPearlAndGoliath()
        island = self.islands.values()[0]
        island.turnOn()
        island.forceZoneLevel(0)
        self.startCutsceneTask()

    def setReadyToPlayCutscene(self):
        self.readyToPlayCutscene = 1
        if self.state == 'StageOne':
            self.playCutscene()

    def playCutscene(self):
        name = CutsceneData.Cutscene3_1
        self.requestEndCutSent = False
        self.cutscene = Cutscene.Cutscene(self.cr, name, self.tryToEndCutscene)
        self.cutscene.play()
        self.cutscene.allowSkip = False
        self.acceptOnce('cutscene-not-skipped', self.tryToEndCutscene)

    def tryToEndCutscene(self):
        if self.requestEndCutSent == False:
            self.requestEndCutSent = True
            self.ignore('cutscene-not-skipped')
            self.sendUpdate('requestEndCutscene', [])

    def endCutscene(self):
        self.cutscene.skipNow()
        if self.messageHolder:
            self.messageHolder.removeNode()
            self.messageHolder = None
        self.stageOneCutsceneDone()

    def displayCutsceneMessage(self, doId, messageNum):
        if localAvatar.doId == doId:
            if not self.messageHolder or messageNum:
                if self.messageHolder:
                    self.messageHolder.removeNode()
                self.messageHolder = render2d.attachNewNode('message')
                self.rulesPanel = TreasureMapRulesPanel.TreasureMapRulesPanel(PLocalizer.BlackPearlTMName, self.stageInstructions[8 - messageNum], self.messageHolder, duration=45.0)
                self.messageHolder.setPos(Vec3(0, 0, 1.0))
                self.messageHolder.setScale(Vec3(0.75, 1, 1))
                self.rulesPanel.show()

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def exitStageOne(self):
        if self.cutscene:
            self.cutscene.destroy()
            self.cutscene = None

    def filterStageOne(self, request, args=[]):
        if request in ['StageTwo', 'NotCompleted']:
            return self.defaultFilter(request, args)
        elif __dev__ and request in ['StageFour']:
            return self.defaultFilter(request, args)

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def stageOneCutsceneDone(self):
        self.acceptOnce('localAvBoardedShip-' + str(self.pearlId), self.handleBoardedPearl)
        self.cr.teleportMgr.localTeleportToId(self.pearlId, localAvatar, showLoadingScreen=False)

    def setupCaptureSphere(self, parent):
        if not self.newEventSphereNodePath:
            newEventSphere = CollisionSphere(1447, -2363, 0, 1300)
            newEventSphere.setTangible(0)
            newEventSphereName = self.uniqueName('shipCapture')
            newEventSphereNode = CollisionNode(newEventSphereName)
            newEventSphereNode.setFromCollideMask(BitMask32.allOff())
            newEventSphereNode.setIntoCollideMask(PiratesGlobals.ShipCollideBitmask)
            newEventSphereNode.addSolid(newEventSphere)
            self.newEventSphereName = newEventSphereName
            self.newEventSphereNodePath = parent.attachNewNode(newEventSphereNode)
            self.acceptOnce('enter' + newEventSphereName, self.handleShipCapture)

    def disableCaptureSphere(self):
        self.ignore('enter' + self.newEventSphereName)
        if self.newEventSphereNodePath:
            self.newEventSphereNodePath.removeNode()
            self.newEventSphereNodePath = None

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def handleShipCapture(self, entry):
        self.ignore('enter' + self.newEventSphereName)
        self.sendUpdate('requestShipCapture')

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def handleBoardedPearl(self):
        base.cr.loadingScreen.hide()
        self.stashGoliath()
        base.localAvatar.guiMgr.radarGui.zoomFSM.request('Zoom2')
        island = self.islands.values()[0]
        island.setZoneLevel(0)
        island.startProcessVisibility(base.localAvatar)
        self.setupCaptureSphere(island)
        base.transitions.fadeIn()
        pearl = self.getPearl()
        pearl.showStatusDisplay()
        pearl.forceZoneLevel(0)
        localAvatar.clearPort(island.doId)
        self.showRulesPanel(0)
        taskMgr.doMethodLater(1.0, self.disablePearlInteractions, 'disablePearlInteractions')
        self.hideAttackShipTags()
        self.stashAttackShips()
        for mast in self.pearl.sails.values():
            for sail in mast.values():
                if sail[1]:
                    sail[1].setAnimState('TiedUp')

    def disablePearlInteractions(self, task):
        self.pearl.disableOnDeckInteractions()

    def handleNPCsKilled(self):
        self.pearl.enableOnDeckInteractions()
        self.showRulesPanel(1)

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def enterStageTwo(self):
        self.disableCaptureSphere()
        island = self.islands.values()[0]
        self.unstashPearlAndGoliath()
        self.unstashAttackShips()
        self.attackShipsSunk = 0
        currentInteractive = base.cr.interactionMgr.getCurrentInteractive()
        if currentInteractive:
            currentInteractive.requestExit()
        localAvatar.cameraFSM.request('Control')
        base.silenceInput()
        for fortId in self.fortIds:
            fort = base.cr.doId2do.get(fortId)
            if fort:
                fort.setDrawbridgesLerpR(1)

        base.transitions.letterboxOn()
        if self.camIval:
            self.camIval.pause()
            self.camIval = None
        camera.wrtReparentTo(render)
        self.camIval = self.getCameraMove1()
        self.camIval.start()

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def exitStageTwo(self):
        self.camIval.finish()

    def filterStageTwo(self, request, args=[]):
        if request in ['StageThree', 'NotCompleted']:
            return self.defaultFilter(request, args)

    def getCameraMove1(self):
        firstShipId = self.attackShipIds[0]
        firstShip = self.cr.doId2do[firstShipId]

        def lerpLookAtAttackShip(t):
            if firstShip and not firstShip.isEmpty():
                camera.lookAt(firstShip)

        def headsUpFirstShip():
            if firstShip and not firstShip.isEmpty():
                localAvatar.headsUp(firstShip)

        def gotoFps():
            if self.state:
                localAvatar.cameraFSM.request('FPS')

        camera.reparentTo(localAvatar)
        camera.setPos(0, 0, 0)
        camera.setHpr(0, 0, 0)
        pearl = self.getPearl()
        dummyNode = pearl.attachNewNode('cameraDummy')
        dummyNode.setPos(-20, 10, 45)
        dummyNode.lookAt(firstShip)
        camera.reparentTo(dummyNode)
        pos0 = Point3(0, 10, 0)
        pos1 = Point3(50, 100, 400)
        camera.lookAt(firstShip)
        ival = Sequence(Func(aspect2d.hide), Func(base.transitions.letterboxOn), Parallel(LerpPosInterval(camera, 5, pos1, startPos=pos0, blendType='easeInOut'), LerpFunc(lerpLookAtAttackShip, 10)), Func(base.transitions.fadeOut), Func(base.transitions.letterboxOff), Wait(1.0), Func(headsUpFirstShip), Func(gotoFps), Func(base.transitions.fadeIn), Func(localAvatar.setH, 120), Func(dummyNode.removeNode), Func(self.showRulesPanel, 2), Func(base.reviveInput), Func(aspect2d.show))
        return ival

    def getStageFourIval(self):
        pos0 = Point3(-172, 664, 75)
        pos1 = Point3(555, 316, 90)
        hpr0 = Point3(200, 5, 0)
        hpr1 = Point3(112, 0, 0)
        dummyNode = self.pearlCopy.attachNewNode('cameraDummy')
        dummyNode.setH(180)
        ival = Sequence(Func(aspect2d.hide), Func(base.transitions.fadeOut), Wait(1.0), Func(localAvatar.cameraFSM.request, 'Control'), Func(camera.wrtReparentTo, render), Func(camera.reparentTo, dummyNode), Func(base.transitions.letterboxOn), Func(self.startPearlAndGoliathCopy), Func(base.transitions.fadeIn), Parallel(LerpPosInterval(camera, 14, pos1, startPos=pos0, blendType='easeInOut'), LerpHprInterval(camera, 10, hpr1, startHpr=hpr0, blendType='easeInOut')), Func(base.transitions.letterboxOff), Func(base.transitions.fadeOut))
        return ival

    def startPearlAndGoliathCopy(self):
        pearlStartPos = Point3(-483, -5813, 0)
        pearlStartHpr = Point3(354, 0, 0)
        pearlEndPos = Point3(-815, -8200, 0)
        pearlEndHpr = Point3(340, 0, 0)
        self.pearl.modelGeom.instanceTo(self.pearlCopy)
        wake = self.pearlCopy.attachNewNode('wakeDummy')
        pearlWake = self.pearl.find('wake')
        if pearlWake and self.pearl.wake:
            pearlWake.instanceTo(wake)
            self.pearl.wake.startFakeAnimate()
            wake.setH(180)
        self.pearl.hide()
        self.pearlCopyIval = LerpPosHprInterval(self.pearlCopy, 16.0, pearlEndPos, pearlEndHpr, startPos=pearlStartPos, startHpr=pearlStartHpr)
        self.pearlCopyIval.start()
        goliathStartPos = Point3(1672, -6688, 0)
        goliathStartHpr = Point3(328, 0, 0)
        goliathEndPos = Point3(-224, -8780, 0)
        goliathEndHpr = Point3(328, 0, 0)
        self.goliath.modelGeom.instanceTo(self.goliathCopy)
        wake = self.goliathCopy.attachNewNode('wakeDummy')
        goliathWake = self.goliath.find('wake')
        if goliathWake and self.goliath.wake:
            goliathWake.instanceTo(wake)
            self.goliath.wake.startFakeAnimate()
            wake.setH(180)
        self.goliathCopy.setScale(1.25)
        self.goliath.hide()
        self.goliathCopyIval = Sequence(Wait(4.0))
        self.goliathCopyIval.append(LerpPosHprInterval(self.goliathCopy, 16.0, goliathEndPos, goliathEndHpr, startPos=goliathStartPos, startHpr=goliathStartHpr))
        self.goliathCopyIval.start()

    def stopPearlAndGoliathCopy(self):
        if self.pearlCopyIval:
            self.pearlCopyIval.pause()
            self.pearlCopy.detachNode()
            self.pearlCopyIval = None
        if self.goliathCopyIval:
            self.goliathCopyIval.pause()
            self.goliathCopy.detachNode()
            self.goliathCopyIval = None
        if self.pearl and not self.pearl.isEmpty():
            self.pearl.setLockSails(False)
            if self.pearl.wake:
                self.pearl.wake.stopFakeAnimate()
                self.pearl.wake.startAnimate(self.pearl)
        if self.goliath and not self.goliath.isEmpty():
            if self.goliath.wake:
                self.goliath.wake.stopFakeAnimate()
                self.goliath.wake.startAnimate(self.goliath)

    def startStageFourCutscene(self):
        if localAvatar.ship.clientController == localAvatar.doId:
            localAvatar.ship.controlManager.disable()
        base.silenceInput()
        self.cameraState = localAvatar.cameraFSM.state
        if self.cameraState == 'Cannon':
            self.cameraSubject = localAvatar.cameraFSM.cannonCamera.cannonProp
        else:
            if self.cameraState == 'Orbit':
                self.cameraSubject = localAvatar.cameraFSM.orbitCamera.subject
        self.stageFourCutscene = True
        if localAvatar.ship.steeringAvId == localAvatar.doId:
            localAvatar.ship.stopPosHprBroadcast()
        self.pearl.setLockSails(True)
        self.pearlCopy = render.attachNewNode('rootDummy')
        self.goliathCopy = render.attachNewNode('rootDummy')
        f = render.getFog()
        f.setLinearRange(500, 2500)
        base.musicMgr.requestFadeOut('ship-pinned')
        base.musicMgr.request('final_battle', priority=1, looping=0)
        base.hideEffects()
        self.stageFourIval = self.getStageFourIval()
        self.stageFourIval.start()

    def stopStageFourCutscene(self):
        base.reviveInput()
        if localAvatar.ship.clientController == localAvatar.doId:
            localAvatar.ship.controlManager.enable()
        self.pearl.show()
        self.goliath.show()
        self.stageFourCutscene = False
        if localAvatar.ship.steeringAvId == localAvatar.doId:
            localAvatar.ship.startPosHprBroadcast()
        self.stopPearlAndGoliathCopy()
        base.transitions.fadeIn()
        if self.cameraState == 'Orbit' or self.cameraState == 'Cannon':
            localAvatar.cameraFSM.request(self.cameraState, self.cameraSubject)
        else:
            localAvatar.cameraFSM.request(self.cameraState)
        base.showEffects()
        self.showRulesPanel(4)
        aspect2d.show()

    def fireShipCannonsAtTarget(self, ship, target):
        if not (ship and target):
            return
        for cannonData in ship.cannons.values():
            cannonProp, cannon = cannonData
            relPos = target.getPos(cannonProp.cannonPost)
            print 'relPos = %s' % relPos
            if relPos[1] > 0:
                delay = random.random()
                if delay < 0.9:
                    taskMgr.doMethodLater(delay, self.fireCannon, 'fireNPCCannon', extraArgs=[cannon])
                    taskMgr.doMethodLater(2 * delay, self.fireCannon, 'fireNPCCannon', extraArgs=[cannon])
                    taskMgr.doMethodLater(3 * delay, self.fireCannon, 'fireNPCCannon', extraArgs=[cannon])

    def fireCannon(self, cannon):
        cannon.prop.playAttack(12900, 12908, 'blackPearlHitEvent')

    def handleAttackShipSunk(self):
        self.attackShipsSunk += 1
        if self.attackShipsSunk > 1:
            strToDisplay = PLocalizer.AttackShipsSunk % self.attackShipsSunk
            if self.attackShipsSunk == 4:
                strToDisplay += PLocalizer.DestroyTheBridges
            localAvatar.guiMgr.messageStack.addTextMessage(strToDisplay)
        else:
            localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.AttackShipSunk)

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def enterStageThree(self):
        self.unstashPearlAndGoliath()
        base.musicMgr.request('ship-pinned', priority=1, looping=0)
        self.ignore(PiratesGlobals.EVENT_SPHERE_CAPTURE + PiratesGlobals.SPHERE_ENTER_SUFFIX)
        for fortId in self.fortIds:
            fort = base.cr.doId2do.get(fortId)
            if fort:
                fort.setupHpMeter()
                fort.setupRadarGui()
                fort.showFortHpMeter()
                fort.setDrawbridgesLerpR(0)
                self.fortIdToUidDict[fortId] = fort.objKey

        self.setupBarricades()
        self.showRulesPanel(3)

    def setupBarricades(self):
        if not self.barricades.keys():
            for key in TreasureMapBlackPearlGlobals.DrawbridgeCollisionDict.keys():
                barricadePair = TreasureMapBlackPearlGlobals.DrawbridgeCollisionDict[key]
                newBarricade = FortBarricade.FortBarricade(self.islands.values()[0], barricadePair)
                self.barricades[key] = newBarricade
                if key == 2 or key == 3:
                    self.barricades[key].disableCollisions()

    def destroyBarricade(self, barricadeId):
        if barricadeId in self.barricades.keys():
            self.barricades[barricadeId].disableCollisions()
            if barricadeId not in self.barricadesDestroyed:
                self.barricadesDestroyed.append(barricadeId)
            if barricadeId in [0, 1, 4]:
                localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.DrawbridgePassable)

    def disableBarricadeCollisions(self, barricadeId):
        if barricadeId in self.barricades.keys():
            self.barricades[barricadeId].disableCollisions()

    def enableBarricadeCollisions(self, barricadeId):
        if barricadeId in self.barricades.keys():
            self.barricades[barricadeId].enableCollisions()

    def barricadeWarning(self, barricadeId):
        if barricadeId in self.barricades.keys():
            if barricadeId not in self.barricadesWarned:
                self.barricadesWarned.append(barricadeId)
                localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.BridgeNeedsToBeDestroyed % (barricadeId + 1))

    def exitStageThree(self):
        pass

    def filterStageThree(self, request, args=[]):
        if request in ['StageFour', 'NotCompleted']:
            return self.defaultFilter(request, args)

    def enterStageFour(self):
        self.unstashPearlAndGoliath()

    def exitStageFour(self):
        pass

    def filterStageFour(self, request, args=[]):
        if request in ['NotCompleted', 'Reward']:
            return self.defaultFilter(request, args)

    def enterReward(self):

        def showRewardPanel(inventory):
            questList = inventory.getQuestList()
            for quest in questList:
                if quest.getQuestId() == 'c3.7recoverPearl':
                    self.showRulesPanel(6)

        DistributedInventoryBase.DistributedInventoryBase.getInventory(localAvatar.inventoryId, showRewardPanel)
        currentInteractive = base.cr.interactionMgr.getCurrentInteractive()
        if currentInteractive:
            currentInteractive.requestExit()
        base.localAvatar.gameFSM.request('Cutscene')
        pearl = self.getPearl()
        pearl.shipStatusDisplay.hide()
        if self.camIval:
            self.camIval.pause()
            self.camIval = None
        camera.wrtReparentTo(render)
        self.camIvalReward = self.getCameraMoveReward()
        self.camIvalReward.start()
        base.musicMgr.requestFadeOut('final_battle')
        base.musicMgr.request('victory', priority=1, looping=0)

    def exitReward(self):
        self.camIvalReward.finish()
        base.transitions.letterboxOff()
        localAvatar.cameraFSM.request('FPS')

    def getCameraMoveReward(self):

        def lerpLookAtAttackShip(t):
            camera.lookAt(self.pearl)

        startPos = Vec3(150, 300, 80)
        endPos = Vec3(400, -550, 110)
        dummyNode = self.pearl.attachNewNode('cameraDummy')
        dummyNode.setPos(0, 0, 0)
        dummyNode.lookAt(self.pearl)
        camera.reparentTo(dummyNode)
        camera.setPos(150, 300, 80)
        ival = Sequence(Func(base.transitions.letterboxOn), Parallel(LerpPosInterval(camera, 12.0, endPos, startPos=startPos, blendType='easeInOut'), LerpFunc(lerpLookAtAttackShip, 12.0), Sequence(Wait(12.0), Func(base.transitions.fadeOut, 2))))
        return ival

    def enterNotCompleted(self):
        ShipPilot.ShipPilot.MAX_STRAIGHT_SAIL_BONUS = 4.0
        base.musicMgr.requestFadeOut('final_battle')
        self.showRulesPanel(5)

    def exitNotCompleted(self):
        pass

    def enterCompleted(self):
        ShipPilot.ShipPilot.MAX_STRAIGHT_SAIL_BONUS = 4.0
        base.cr.loadingScreen.showTarget(localAvatar.getReturnLocation())

    def exitCompleted(self):
        pass

    def localAvEnterDeath(self, av):
        DistributedTreasureMapInstance.DistributedTreasureMapInstance.localAvEnterDeath(self, av)
        self.requestTreasureMapLeave()

    def localAvExitDeath(self, av):
        DistributedTreasureMapInstance.DistributedTreasureMapInstance.localAvExitDeath(self, av)

    def requestLeaveApproved(self, parentId, zoneId, shipId):
        localAvatar.setInterest(parentId, zoneId, ['tmExit'])
        self.cr.loadingScreen.showTarget()
        self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, 'mainWorld', doEffect=False)

    def getBarricadeWarning(self):
        retval = -1
        if retval == -1 and not (0 in self.barricadesDestroyed or 1 in self.barricadesDestroyed):
            retval = 1
        if retval == -1:
            for id in range(2, 5):
                if id not in self.barricadesDestroyed:
                    retval = id
                    break

        return retval

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def setAllPlayersReady(self, ready):
        self.gotAllPlayers = True