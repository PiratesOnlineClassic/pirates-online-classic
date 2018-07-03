import random

from direct.fsm import FSM
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import report
from panda3d.core import *
from pirates.effects.Explosion import Explosion
from pirates.effects.FlamingDebris import FlamingDebris
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.piratesbase import PiratesGlobals, PLocalizer


class GameFSMShip(FSM.FSM):
    
    def __init__(self, ship):
        FSM.FSM.__init__(self, 'GameFSMShip')
        self.ship = ship
        self.risingIval = None
        self.sinkIval = None
        self.currentMusic = None
        self.grappleSfx = None
        self.targetSphereStr = 'grappleTargetSphere'
        self.targets = []
        self.pendingAddTarget = None
        return

    def cleanup(self):
        if self.pendingAddTarget:
            base.cr.relatedObjectMgr.abortRequest(self.pendingAddTarget)
            self.pendingAddTarget = None
        self.removeTargets()
        if self.risingIval:
            self.risingIval.finish()
            self.risingIval = None
        if self.sinkIval:
            self.sinkIval.finish()
            self.sinkIval = None
        FSM.FSM.cleanup(self)
        self.ship = None
        return

    def enterNeutral(self):
        pass

    def exitNeutral(self):
        pass

    def enterSpawn(self):
        pass

    def exitSpawn(self):
        pass

    def enterAdrift(self):
        self.currentMusic = 'ship-adrift'
        if self.ship.isInCrew(localAvatar.doId):
            if base.localAvatar and base.localAvatar.gameFSM and not base.localAvatar.gameFSM.lockFSM:
                base.musicMgr.request(self.currentMusic, volume=0.6)

    def exitAdrift(self):
        self.fadeOutMusicIfInCrew()

    def enterAISteering(self, avId):
        self.ship.startSmooth()
        self.ship.clientSteeringBegin(avId)

    def exitAISteering(self):
        self.ship.stopSmooth()
        self.ship.clientSteeringEnd()

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-shipboard-report')
    def enterClientSteering(self, avId):
        self.currentMusic = random.choice(('ship-sailing-a', 'ship-sailing-b', 'ship-sailing-c'))
        self.ship.clientSteeringBegin(avId)
        if self.ship.isInCrew(localAvatar.doId):
            base.musicMgr.request(self.currentMusic)

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-shipboard-report')
    def exitClientSteering(self):
        if self.ship.wheel and self.ship.wheel[1]:
            if base.cr.interactionMgr.getCurrentInteractive() is self:
                self.ship.wheel[1].requestExit()
            else:
                self.ship.wheel[1].refreshState()
        self.ship.clientSteeringEnd()
        self.fadeOutMusicIfInCrew()

    def enterDocked(self):
        self.currentMusic = 'ship-docked'
        if self.ship.isInCrew(localAvatar.doId):
            base.musicMgr.request(self.currentMusic)
        self.ship.rollupSails()

    def exitDocked(self):
        self.fadeOutMusicIfInCrew()

    def enterPinned(self):
        self.ship.actorNode.getPhysicsObject().setVelocity(Vec3.zero())
        self.currentMusic = 'ship-pinned'
        if self.ship.isInCrew(localAvatar.doId):
            base.musicMgr.request(self.currentMusic)
        self.ship.rollupSails()
        self.ship.disableWheelInteraction()

    def exitPinned(self):
        self.fadeOutMusicIfInCrew()
        self.ship.enableWheelInteraction()

    def enterEnsnared(self):
        self.currentMusic = 'ship-ensnared'
        if self.ship.isInCrew(localAvatar.doId):
            base.musicMgr.request(self.currentMusic)
        if self.risingIval:
            self.risingIval.finish()
            self.risingIval = None
        sinking = Sequence(LerpPosInterval(self.ship, 1.0, Point3(0.0, 0, -3.0)))
        listing = Sequence(LerpHprInterval(self.ship, 1.0, Vec3(0, 0, 10)))
        self.sinkIval = Parallel(sinking, listing)
        self.sinkIval.start()
        return

    def exitEnsnared(self):
        self.fadeOutMusicIfInCrew()
        if self.sinkIval:
            self.sinkIval.finish()
            self.sinkIval = None
        rising = Sequence(LerpPosInterval(self.ship, 1.0, Point3(0, 0, 0)))
        unlisting = Sequence(LerpHprInterval(self.ship, 1.0, Vec3(0, 0, 0)))
        self.riseIval = Parallel(rising, unlisting)
        self.riseIval.start()
        return

    def enterShoveOff(self):
        pass

    def exitShoveOff(self):
        pass

    def enterSinking(self):
        self.ship.actorNode.getPhysicsObject().setVelocity(Vec3.zero())
        self.ship.registerMainBuiltFunction(self.ship.sinkingBegin)
        self.currentMusic = 'ship-sinking'
        if self.ship.isInCrew(localAvatar.doId):
            base.musicMgr.request(self.currentMusic, looping=0)

    def exitSinking(self):
        self.ship.sinkingEnd()
        self.fadeOutMusicIfInCrew()

    def enterSunk(self):
        pass

    def enterRecoverFromSunk(self):
        self.ship.recoverFromSunk()

    def enterInBoardingPosition(self):
        pass

    def exitInBoardingPosition(self):
        pass

    def enterPathFollow(self):
        self.ship.startSmooth()

    def exitPathFollow(self):
        self.ship.stopSmooth()

    def enterPatrol(self):
        self.ship.startSmooth()

    def exitPatrol(self):
        self.ship.stopSmooth()

    def enterAttackChase(self):
        self.ship.startSmooth()

    def exitAttackChase(self):
        self.ship.stopSmooth()

    def enterOff(self):
        self.ship.stopAutoSailing()

    def exitOff(self):
        messenger.send('shipStateOn-%s' % self.ship.doId, [self.ship])

    def enterPutAway(self):
        self.ship.stopAutoSailing()

    def exitPutAway(self):
        pass

    def enterScriptedMovement(self):
        self.ship.startSmooth()

    def exitScriptedMovement(self):
        self.ship.stopSmooth()

    def stopCurrentMusic(self):
        if self.currentMusic:
            base.musicMgr.requestFadeOut(self.currentMusic)
        self.currentMusic = None
        return

    def startCurrentMusic(self):
        if self.currentMusic:
            base.musicMgr.request(self.currentMusic)

    def fadeOutMusicIfInCrew(self):
        try:
            if self.ship.isInCrew(localAvatar.doId):
                self.stopCurrentMusic()
        except NameError:
            self.stopCurrentMusic()

    def createGrappleProximitySphere(self):
        self.grappleProximityStr = self.ship.uniqueName('grappleProximity')
        collSphere = CollisionSphere(0, 0, 0, 200)
        collSphere.setTangible(0)
        collSphereNode = CollisionNode(self.grappleProximityStr)
        collSphereNode.addSolid(collSphere)
        collSphereNode.setCollideMask(PiratesGlobals.ShipCollideBitmask)
        collSphereNodePath = self.ship.attachNewNode(collSphereNode)
        self.grappleProximityCollision = collSphereNodePath
        self.stashGrappleProximitySphere()

    def stashGrappleProximitySphere(self):
        self.grappleProximityCollision.stash()

    def unstashGrappleProximitySphere(self):
        self.grappleProximityCollision.unstash()

    def enterWaitingForGrapple(self):
        self.notify.debug('enterWaitingForGrapple')
        self.ship.removeWake()
        if self.ship.boardableShipId == None:
            return
        self.unstashGrappleProximitySphere()
        self.removeTargets()
        self.pendingAddTarget = base.cr.relatedObjectMgr.requestObjects([self.ship.boardableShipId], eachCallback=self.addTargets)
        if localAvatar.ship and localAvatar.ship.doId == self.ship.boardableShipId:
            localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.FlagshipWaitingForGrappleInstructions)
        return

    def exitWaitingForGrapple(self):
        self.ship.removeTarget()

    def addTargets(self, boardableShip):
        if localAvatar.ship != boardableShip:
            return
        attackX = boardableShip.getX(self.ship)
        gStr = '**/grapple_right_*'
        xOffset = -5.0
        if attackX < 0:
            gStr = '**/grapple_left_*'
            xOffset = 5.0
        locators = self.ship.locators.findAllMatches(gStr + ';+s') 
        for locator in locators:
            target = loader.loadModelCopy('models/effects/selectionCursor')
            target.setColorScale(0, 1, 0, 1)
            target.reparentTo(locator)
            target.setTwoSided(1)
            target.setBillboardPointEye()
            target.setFogOff()
            target.setX(xOffset)
            scaleA, scaleB = (10, 16)
            target.setScale(scaleA)
            t = 0.5
            target.wrtReparentTo(self.ship.root)
            ival = Sequence(LerpScaleInterval(target, 2 * t, Vec3(scaleB, scaleB, scaleB), blendType='easeInOut'), LerpScaleInterval(target, t, Vec3(scaleA, scaleA, scaleA), blendType='easeInOut'))
            ival.loop()
            collSphere = CollisionSphere(0, 0, 0, 10)
            collSphere.setTangible(1)
            collSphereNode = CollisionNode('grappleTargetSphere')
            collSphereNode.addSolid(collSphere)
            collSphereNode.setTag('objType', str(PiratesGlobals.COLL_GRAPPLE_TARGET))
            collSphereNode.setTag('shipId', str(self.ship.doId))
            collSphereNode.setTag('targetId', locator.getName())
            collSphereNode.setCollideMask(PiratesGlobals.TargetBitmask)
            collSphereNodePath = self.ship.root.attachNewNode(collSphereNode)
            collSphereNodePath.setPos(locator.getPos(self.ship.root))
            collSphereNodePath.setTag('targetIndex', str(len(self.targets)))
            self.targets.append([target, ival, collSphereNodePath])

        self.accept('enterGrappleTargetSphere', self.handleTargetHit)

    def removeTargets(self):
        for target, ival, csnp in self.targets:
            target.removeNode()
            csnp.removeNode()
            if ival:
                ival.pause()
                del ival

        self.targets = []
        self.ignore('entergrappleTargetSphere')

    def handleTargetHit(self, collEntry):
        print '**********HANDLE TARGET HIT*****************'

    def enterGrappleLerping(self):
        self.notify.debug('enterGrappleLerping')
        self.ship.startSmooth()
        self.grappleSfx = loader.loadSfx('audio/grappling_ratchet_groan.mp3')
        base.playSfx(self.grappleSfx, looping=1)
        if localAvatar.ship and localAvatar.ship.doId == self.ship.boardableShipId:
            localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.FlagshipGrappleLerpingInstructions)

    def exitGrappleLerping(self):
        self.ship.stopSmooth()
        self.ship.removeTarget()
        if self.grappleSfx:
            self.grappleSfx.stop()
            self.grappleSfx = None
        return

    def enterInPosition(self):
        self.notify.debug('enterInPosition')
        self.removeTargets()
        myShip = localAvatar.getShip()
        if myShip and myShip.doId == self.ship.boardableShipId:
            if myShip.isCaptain(localAvatar.doId):
                localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.FlagshipInPositionInstructionsCaptain)
                myShip.showBoardingChoice(self.ship)
            else:
                localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.FlagshipInPositionInstructionsCrew)

    def exitInPosition(self):
        self.ship.removeTarget()
        myShip = localAvatar.getShip()
        if myShip and myShip.doId == self.ship.boardableShipId:
            if myShip.isCaptain(localAvatar.doId):
                myShip.removeBoardingChoice()

    def enterBoarded(self):
        if localAvatar.ship and localAvatar.ship.doId == self.ship.boardableShipId:
            localAvatar.addShipTarget(self.ship, 3)
        self.ship.disableOnDeckInteractions()

    def exitBoarded(self):
        pass

    def enterDefeated(self):
        self.explosionIval = None
        if self.ship:
            self.notify.debug('%s enterDefeated' % self.ship.doId)
            self.ship.removeTarget()
            if self.ship.hull:
                pos = self.ship.hull[0].getClosestBoardingPos()
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    explosionEffect = Explosion.getEffect()
                    if explosionEffect:
                        explosionEffect.reparentTo(self.ship.root)
                        explosionEffect.setPos(self.ship.root, pos)
                    shipSplintersAEffect = ShipSplintersA.getEffect()
                    if shipSplintersAEffect:
                        shipSplintersAEffect.wrtReparentTo(self.ship.root)
                        shipSplintersAEffect.setPos(self.ship.root, pos)
                    effect1 = FlamingDebris.getEffect()
                    if effect1:
                        effect1.wrtReparentTo(self.ship.root)
                        effect1.setPos(self.ship.root, pos)
                        effect1.velocityX = 25
                        effect1.velocityY = 0
                    effect2 = FlamingDebris.getEffect()
                    if effect2:
                        effect2.wrtReparentTo(self.ship.root)
                        effect2.setPos(self.ship.root, pos)
                        effect2.velocityX = 0
                        effect2.velocityY = 25
                    if explosionEffect and shipSplintersAEffect:
                        self.explosionIval = Sequence(Wait(4.0), Parallel(Func(explosionEffect.play), Func(shipSplintersAEffect.play), Func(effect1.play), Func(effect2.play)), Wait(2.0), Parallel(Func(explosionEffect.play), Func(shipSplintersAEffect.play), Func(effect1.play), Func(effect2.play)), Wait(2.0), Parallel(Func(explosionEffect.play), Func(shipSplintersAEffect.play), Func(effect1.play), Func(effect2.play)))
                        self.explosionIval.start()
        return

    def exitDefeated(self):
        self.notify.debug('%s exitDefeated' % self.ship.doId)
        if self.explosionIval:
            self.explosionIval.pause()
            self.explosionIval = None
        return

    def enterInactive(self):
        pass

    def exitDefeated(self):
        pass