from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.fsm import FSM
from direct.task import Task
from direct.showbase.PythonUtil import lerp
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.reputation import ReputationGlobals
from pirates.destructibles import ShatterableSkeleton
from pirates.ship import ShipGlobals
from pirates.effects.SmallSplash import SmallSplash
from pirates.effects.Twister import Twister
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.effects.ThrowDirt2 import ThrowDirt2
import random

class BattleAvatarGameFSM(FSM.FSM):
    notify = directNotify.newCategory('BattleAvatarGameFSM')
    diggingSfx = None
    
    def __init__(self, av, fsmName = 'BattleAvatarGameFSM'):
        FSM.FSM.__init__(self, fsmName)
        self.av = av
        self.deathTrack = None
        self.swingTrack = None
        self.steeringTrack = None
        self.kneelingTrack = None
        self.teleportTrack = None
        self.diggingTrack = None
        self.diggingSfxTrack = None
        self.repairHammerTrack = None
        self.putAwayHammerTrack = None
        self.repairIntroTrack = None
        self.repairingTrack = None
        self.repairingSfxTrack = None
        self.repairHammer = None
        self.hammerSfx = None
        self.teleportEffect = None
        self.dirtEffect = None
        self.jailTrack = None
        self.kickTrack = None
        self._shipBoardingFinishCall = None
        self.treasureChest = None
        if not self.diggingSfx:
            self.diggingSfx = loader.loadSfx('audio/sfx_avatar_dig.mp3')
    
    def cleanup(self):
        FSM.FSM.cleanup(self)
        if self.treasureChest:
            self.treasureChest.remove()
            del self.treasureChest
        
        if self.av:
            self.av = None
        
        if self._shipBoardingFinishCall:
            self._shipBoardingFinishCall.destroy()
        
        if self.swingTrack:
            self.swingTrack.pause()
            self.swingTrack = None
        
        if self.deathTrack:
            self.deathTrack.pause()
            self.deathTrack = None
        
        if self.teleportTrack:
            self.teleportTrack.pause()
            self.teleportTrack = None
        
        if self.teleportEffect:
            self.teleportEffect.cleanUpEffect()
            self.teleportEffect = None
        
        if self.jailTrack:
            self.jailTrack.pause()
            self.jailTrack = None
        
        if self.kickTrack:
            self.kickTrack.pause()
            self.kickTrack = None
        
        if self.diggingTrack:
            self.diggingTrack.pause()
            self.diggingTrack = None
        
        if self.repairHammerTrack:
            self.repairHammerTrack.pause()
            self.repairHammerTrack = None
        
        if self.putAwayHammerTrack:
            self.putAwayHammerTrack.pause()
            self.putAwayHammerTrack = None
        
        if self.repairIntroTrack:
            self.repairIntroTrack.pause()
            self.repairIntroTrack = None
        
        if self.repairingTrack:
            self.repairingTrack.pause()
            self.repairingTrack = None
        
        if self.repairingSfxTrack:
            self.repairingSfxTrack.pause()
            self.repairingSfxTrack = None
        
        if self.repairHammer:
            self.repairHammer = None
        
        if self.hammerSfx:
            self.hammerSfx = None
        
        if self.diggingSfxTrack:
            self.diggingSfxTrack.pause()
            self.diggingSfxTrack = None
        
        if self.dirtEffect:
            self.dirtEffect.stopLoop()
            self.dirtEffect = None

    def enterOff(self, extraArgs = []):
        pass

    def enterLandRoam(self, extraArgs = []):
        self.av.startCompassEffect()
        self.av.setActiveShadow(1)
        animState = 'LandRoam'
        if self.av.currentWeapon:
            animState = self.av.currentWeapon.getAnimState(animState)
        
        self.av.motionFSM.setAnimInfo(self.av.getAnimInfo(animState))
        if self.av.motionFSM.getCurrentOrNextState() != 'On':
            self.av.motionFSM.on()
    
    def exitLandRoam(self):
        self.av.setActiveShadow(0)

    def enterWaterRoam(self, extraArgs = []):
        self.av.setActiveShadow(0)
        self.av.startCompassEffect()
        self.av.motionFSM.setAnimInfo(self.av.getAnimInfo('WaterRoam'))
        if self.av.motionFSM.getCurrentOrNextState() != 'On':
            self.av.motionFSM.on()
        
        self.av.nametag3d.setZ(-3)
        self.av.motionFSM.setAllowAirborne(False)

    def exitWaterRoam(self):
        self.av.nametag3d.setZ(0)
        self.av.setActiveShadow(1)
        self.av.motionFSM.setAllowAirborne(True)

    def enterDeath(self, extraArgs = []):
        if self.av.motionFSM:
            self.av.motionFSM.off()
        
        self.av.stashBattleCollisions()
        if self.av.voodooSmokeEffect2:
            self.av.voodooSmokeEffect2.stopLoop()
            self.av.voodooSmokeEffect2 = None
        
        if base.localAvatar.guiMgr.targetStatusTray.doId == self.av.getDoId():
            base.localAvatar.guiMgr.targetStatusTray.fadeOut()
        
        if self.deathTrack:
            self.deathTrack.finish()
        
        self.deathTrack = self.av.getEnterDeathTrack()
        self.deathTrack.start()
    
    def exitDeath(self):
        self.av.respawn()
        if self.deathTrack:
            self.deathTrack.finish()
        
        self.deathTrack = self.av.getExitDeathTrack()
        self.deathTrack.start()

    def enterSpawn(self, extraArgs = []):
        pass

    def exitSpawn(self):
        pass
    
    def enterBattle(self, extraArgs = []):
        self.av.setActiveShadow(1)
        if self.av.motionFSM.getCurrentOrNextState() != 'On':
            self.av.motionFSM.on()

    def exitBattle(self):
        self.av.setActiveShadow(0)
        animState = 'LandRoam'
        if self.av.currentWeapon:
            animState = self.av.currentWeapon.getAnimState(animState)
        
        self.av.motionFSM.setAnimInfo(self.av.getAnimInfo(animState))
    
    def enterDigging(self, extraArgs = []):
        self.shovel = loader.loadModel('models/handheld/shovel_high')
        self.shovel.reparentTo(self.av.rightHandNode)
        self.av.motionFSM.off()
        animDur = self.av.getDuration('shovel')
        sfxDur = self.diggingSfx.length()
        self.diggingSfxTrack = Sequence(Wait(0.25), SoundInterval(self.diggingSfx, node = self.av), Wait(animDur - sfxDur - 0.25))
        self.diggingSfxTrack.loop()
        self.diggingTrack = self.av.actorInterval('shovel', loop = 1, duration = 1000)
        self.diggingTrack.loop()
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
            self.dirtEffect = ThrowDirt2.getEffect()
            if self.dirtEffect:
                self.dirtEffect.particleDummy.setH(self.av.getH(render))
                self.dirtEffect.reparentTo(self.shovel.find('**/shovel_end'))
                self.dirtEffect.startLoop()

    def exitDigging(self):
        self.shovel.removeNode()
        self.av.motionFSM.on()
        self.diggingTrack.pause()
        self.diggingSfxTrack.pause()
        if self.dirtEffect:
            self.dirtEffect.stopLoop()
            self.dirtEffect = None
        
        del self.shovel

    def enterStealing(self, extraArgs = []):
        self.shovel = loader.loadModel('models/handheld/shovel_high')
        self.shovel.reparentTo(self.av.leftHandNode)
        self.shovel.setPos(0.3, 0, -0.3)
        self.av.loop('shovel')

    def exitStealing(self):
        self.shovel.removeNode()
        del self.shovel

    def enterSearching(self, extraArgs = []):
        self.av.loop('search_med')

    def exitSearching(self):
        pass
    
    def enterStunned(self, extraArgs = []):
        self.av.motionFSM.off()
        self.av.motionFSM.lock()
        self.stunnedTrack = Sequence(self.av.actorInterval('boxing_hit_head_right'))
        self.stunnedTrack.loop()
    
    def exitStunned(self):
        self.stunnedTrack.pause()
        del self.stunnedTrack
        self.av.motionFSM.unlock()
        self.av.motionFSM.on()

    def enterLandTreasureRoam(self, extraArgs = []):
        self.av.setActiveShadow(1)
        self.av.motionFSM.setAnimInfo(self.av.getAnimInfo('LandTreasureRoam'))
        if self.av.motionFSM.getCurrentOrNextState() != 'On':
            self.av.motionFSM.on()
        
        if self.treasureChest:
            self.treasureChest.unstash()
        else:
            self.treasureChest = loader.loadModel('models/props/treasureChest')
            self.treasureChest.findAllMatches('**/+CollisionNode').detach()
        self.treasureChest.reparentTo(self.av.rightHandNode)
        self.treasureChest.setTransform(PiratesGlobals.treasureCarryTransforms[self.av.style.gender][self.av.style.getBodyShape()])
    
    def exitLandTreasureRoam(self):
        self.treasureChest.stash()
        self.av.setActiveShadow(0)

    def enterWaterTreasureRoam(self, extraArgs = []):
        self.av.setActiveShadow(0)
        self.av.hideShadow()
        self.av.nametag3d.setZ(-3)
        self.av.motionFSM.setAnimInfo(self.av.getAnimInfo('WaterRoam'))
        self.av.startCompassEffect()
        if self.av.motionFSM.getCurrentOrNextState() != 'On':
            self.av.motionFSM.on()
        
        self.av.motionFSM.setAllowAirborne(False)
        if self.treasureChest:
            self.treasureChest.unstash()
        else:
            self.treasureChest = loader.loadModel('models/props/treasureChest')
            self.treasureChest.findAllMatches('**/+CollisionNode').detach()
        self.treasureChest.reparentTo(self.av)
        self.treasureChest.setTransform(PiratesGlobals.treasureSwimTransform)
        self.treasureChest.setZ(1.3)
        self.treasureChest.setScale(0.4)
    
    def exitWaterTreasureRoam(self):
        self.treasureChest.stash()
        self.av.nametag3d.setZ(0)
        self.av.setActiveShadow(1)

    def enterTeleportOut(self, extraArgs = []):
        self.av.motionFSM.off()
        self.av.nametag3d.hide()
        timeOffset = 0.0
        if len(extraArgs) >= 1:
            timeOffset = extraArgs[0]
        
        if not self.teleportEffect:
            teleportAnimPlayRate = 1.5
            teleportAnimLength = self.av.getDuration('teleport') / teleportAnimPlayRate
            twisterFadeLength = 1.0
            totalLength = teleportAnimLength + twisterFadeLength
            avFadeOutLength = 2.0
            avFlyTime = 1.5
            avFlyHeight = 7
            screenFadeLength = 0.5
            
            def setRelZ(t):
                self.av.getGeomNode().setZ(lerp(0, avFlyHeight, t))

            teleportTrack = Sequence()
            teleportPar = Parallel()
            self.teleportEffect = Twister.getEffect()
            if self.teleportEffect:
                teleportTrack.append(Func(self.teleportEffect.reparentTo, self.av.getEffectParent()))
                teleportPar.append(self.teleportEffect.getParticleInterval(totalLength))
            
            def playTeleportAnim():
                self.av.play('teleport', blendOutT = 0.0)
                self.av.setPlayRate(teleportAnimPlayRate, 'teleport')

            teleportPar.append(Func(playTeleportAnim))
            teleportPar.append(Sequence(Wait(teleportAnimLength - avFadeOutLength), Func(self.av.setTransparency, 1, 1001), LerpFunc(self.av.setColorScale, duration = avFadeOutLength, toData = Vec4(1, 1, 1, 0), fromData = Vec4(1, 1, 1, 1))))
            teleportPar.append(Sequence(Wait(avFlyTime), LerpFunc(setRelZ, duration = teleportAnimLength - avFlyTime)))
            teleportTrack.append(teleportPar)
            self.teleportTrack = teleportTrack
        
        self.teleportTrack.start(timeOffset)
    
    def exitTeleportOut(self):
        self.av.motionFSM.on()
        self.teleportTrack.finish()
        self.av.getGeomNode().setZ(0)
        self.av.clearColorScale()
        self.av.clearTransparency()
        self.av.nametag3d.show()
    
    def enterTeleportIn(self, extraArgs = []):
        pass

    def exitTeleportIn(self):
        pass

    def enterShipPilot(self, extraArgs = []):
        self.av.motionFSM.off()
        self.av.stopCompassEffect()
        if len(extraArgs) > 1:
            ship = extraArgs[1]
        else:
            ship = self.av.getParentObj()
        ship.placeAvatarAtWheel(self.av)
        if not self.steeringTrack:
            self.steeringTrack = Func(self.av.loop, 'wheel_idle')
            self.steeringTrack.start()
    
    def exitShipPilot(self):
        self.av.startCompassEffect()
        if self.steeringTrack:
            self.steeringTrack.pause()
            self.steeringTrack = None
    
    def enterCannon(self, extraArgs = []):
        self.av.motionFSM.off()
        self.av.stopCompassEffect()
        if not self.kneelingTrack:
            self.kneelingTrack = Sequence(self.av.actorInterval('kneel_fromidle', playRate = 1, blendOutT = 0), Func(self.av.loop, 'kneel', blendT = 0))
            self.kneelingTrack.start()

    def exitCannon(self):
        self.av.actorInterval('kneel_fromidle', startFrame = 26, endFrame = 1).start()
        self.av.startCompassEffect()
        if self.kneelingTrack:
            self.kneelingTrack.pause()
            self.kneelingTrack = None
    
    def enterParlorGame(self, extraArgs = []):
        pass

    def exitParlorGame(self):
        pass

    def enterNPCInteract(self, extraArgs = []):
        self.av.motionFSM.off()
    
    def exitNPCInteract(self):
        self.av.motionFSM.on()

    def enterWeaponReceive(self, extraArgs=[]):
        self.av.motionFSM.off()

    def exitWeaponReceive(self):
        self.av.motionFSM.on()

    def enterDinghyInteract(self, extraArgs=[]):
        self.av.motionFSM.off()

    def exitDinghyInteract(self):
        pass
    
    def enterShipBoarding(self, extraArgs = []):
        (ship, fromShip, mode, instant, ts) = extraArgs
        if ship:
            self.av.motionFSM.off()
            self.av.stopCompassEffect()
            self.av.setActiveShadow(0)
            showMovie = not instant
            if base.cr.tutorial == 1:
                showMovie = False
            
            if mode == ShipGlobals.SHIP_BOARD_FROM_SWIM:
                self.avatarBoardShip(ship, showMovie, ts, fromWater = 1)
            elif mode == ShipGlobals.SHIP_BOARD_FROM_WALK:
                if fromShip:
                    self.avatarBoardShipFromShip(ship, fromShip, showMovie, ts)
                else:
                    self.avatarBoardShip(ship, showMovie, ts, fromWater = 0)
            
        else:
            self.notify.warning('enterShipBoarding: ship not found')

    def exitShipBoarding(self):
        self.av.setActiveShadow(1)
        self.av.motionFSM.on()
        self.av.startCompassEffect()
    
    def avatarBoardShip(self, ship, showMovie, ts, fromWater=0):
        boardingPosHpr = ship.getBoardingPosHpr()
        if self.av.isLocal() and boardingPosHpr:
            self.notify.warning('local avatar boarding from %s' % boardingPosHpr)
            self.av.reparentTo(render)
            self.av.setPos(boardingPosHpr[0])
            self.av.setH(boardingPosHpr[1][0])
        startingPos = self.av.getPos()
        deckPos = None
        if ship:
            deckPos = ship.getClosestBoardingPos()
        endPos = self.av.getParent().getRelativePoint(ship.root, deckPos)
        if showMovie:
            if fromWater:
                grabAnim = 'rope_grab'
            else:
                grabAnim = 'rope_grab_from_idle'
            tRopeSwingDown = 0.75
            tWaitToAttachRope = self.av.getDuration(grabAnim, fromFrame=0, toFrame=42)
            rope, ropeActor, ropeEndNode = self.av.getRope()
            ropeAnchorNode = ship.getRopeAnchorNode(self.av, ropeEndNode)
            ropeMidNode = ship.attachNewNode('ropeMidNode')
            midNodeStartPos = (ropeAnchorNode.getPos(ship) + ropeEndNode.getPos(ship)) * 0.5
            midNodeStartPos.setX(midNodeStartPos.getX() * 0.8)
            ropeMidNode.setPos(midNodeStartPos)
            midNodeEndPos = (ropeAnchorNode.getPos(ship) + deckPos) * 0.5
            midNodeEndPos.setX(midNodeEndPos.getX() * 1.2)
            rightHand = self.av.rightHandNode

            def playSplash():
                if fromWater:
                    splashEffect = SmallSplash.getEffect()
                    if splashEffect:
                        splashEffect.reparentTo(self.av)
                        splashEffect.play()

            def setupRope(ropeParent):
                rope.setup(2, ((None, Point3(0, 0, 0)), (ropeAnchorNode, Point3(0, 0, 0))))
                rope.reparentTo(ropeParent)

            setupRope(ropeEndNode)
            if self.swingTrack:
                self.swingTrack.pause()
                self.swingTrack = None
            boardAnimDur = self.av.getDuration('rope_board')
            boardingRopeH = ShipGlobals.getBoardingRopeH(ship.shipClass)
            boardingInterval = Sequence(Func(ropeEndNode.wrtReparentTo, self.av),
                                        Sequence(Wait(tWaitToAttachRope - tRopeSwingDown),
                                        Parallel(ActorInterval(self.av, grabAnim),  LerpPosInterval(ropeEndNode, tRopeSwingDown, Point3(1.0, 0, 1.0)))),
                                        Func(self.av.lookAt, ship), Func(setupRope, rightHand),
                                        Parallel(ProjectileInterval(self.av, startPos=startingPos, endPos=endPos, duration=boardAnimDur, gravityMult=boardingRopeH),
                                        ProjectileInterval(ropeMidNode, startPos=midNodeStartPos, endPos=midNodeEndPos, duration=boardAnimDur), Sequence(Wait(0.2), Func(ship.boardingInit, self.av, ship)),
                                        Sequence(Wait(boardAnimDur - 0.2), Func(rope.detachNode)), self.av.actorInterval('rope_board', playRate=1.0)),
                                        Parallel(self.av.actorInterval('rope_dismount', endFrame=24), Sequence(Wait(0.5), Func(ropeMidNode.detachNode), Func(ship.boardingFinish, self.av, deckPos))))
            self.swingTrack = boardingInterval
            self.swingTrack.start(ts)
        else:
            base.transitions.fadeOut(0.0)
            if self.swingTrack:
                self.swingTrack.pause()
                self.swingTrack = None
            ship.boardingInit(self.av, ship)
            self.av.setPos(endPos)
            if self._shipBoardingFinishCall:
                self._shipBoardingFinishCall.destroy()
            self._shipBoardingFinishCall = FrameDelayedCall('shipBoardingFinish-%s-%s' % (ship.doId, self.av.doId), Functor(ship.boardingFinish, self.av, deckPos, False))
    
    def avatarBoardShipFromShip(self, ship, fromShip, showMovie, ts):
        self.av.wrtReparentTo(fromShip.root)
        avPos = self.av.getPos()
        deckPos = None
        if ship.hull:
            deckPos = ship.hull[0].getClosestBoardingPos()
        if not deckPos:
            deckPos, h = ShipGlobals.getBoardingSpherePosH(ship.modelClass)
        offset = Point3(4 * random.random() - 2, 4 * random.random() - 2, 0)
        deckPos += offset
        endPos = self.av.getParent().getRelativePoint(ship.root, Point3(deckPos) + Point3(0, 0, 10))
        if showMovie:
            rope, ropeActor, ropeEndNode = self.av.getRope()
            ropeAnchorNode = fromShip.getRopeAnchorNode(self.av, ropeEndNode)
            rightHand = self.av.rightHandNode
            leftHand = self.av.leftHandNode
            rope.setup(3, ((None, Point3(0, 0, 0)), (self.av, Point3(10, 20, 40)), (ropeAnchorNode, Point3(0, 0, 0))))
            rope.reparentTo(ropeEndNode)
            ropeActor.reparentTo(leftHand)
            ropeActor.hide()
            midPos = (avPos + endPos) * 0.5
            tWaitToTranslateZ = self.av.getDuration('swing_aboard', fromFrame=0, toFrame=42)
            tTranslateZ = self.av.getDuration('swing_aboard', fromFrame=42, toFrame=45)
            tWaitToAttachRope = self.av.getDuration('swing_aboard', fromFrame=0, toFrame=45)
            tWaitToDetachRope = self.av.getDuration('swing_aboard', fromFrame=0, toFrame=75)
            tRopeSwingDown = 0.75
            tRopeSwing = tWaitToDetachRope - tWaitToAttachRope
            tRopeSwingAway = 0.75
            if self.swingTrack:
                self.swingTrack.pause()
                self.swingTrack = None
            swingTrack = Sequence(Func(self.av.lookAt, ship.root),
                                  Func(ship.boardingInit, self.av, fromShip),
                                  Func(ropeEndNode.wrtReparentTo, self.av),
                                  Parallel(self.av.actorInterval('swing_aboard'),
                                  ActorInterval(ropeActor, 'swing_aboard'),
                                  Sequence(Wait(tWaitToAttachRope - tRopeSwingDown),
                                  LerpPosInterval(ropeEndNode, tRopeSwingDown, Point3(1.0, 0, 3.0))),
                                  Sequence(Wait(tWaitToTranslateZ),
                                  LerpPosInterval(self.av, tTranslateZ, avPos + Point3(0.0, 0, 25.0))),
                                  Sequence(Wait(tWaitToAttachRope), Func(rope.reparentTo, leftHand), Func(ropeActor.show),
                                  LerpPosInterval(self.av, tRopeSwing / 2.0, midPos),
                                  Func(self.av.wrtReparentTo, ship.root),
                                  LerpPosInterval(self.av, tRopeSwing / 2.0, deckPos)),
                                  Sequence(Wait(tWaitToDetachRope), Func(rope.reparentTo, ropeEndNode),
                                  Func(ropeActor.detachNode),
                                  LerpPosInterval(ropeEndNode, tRopeSwingAway, Point3(0, 50, 50)))),
                                  Func(fromShip.boardingLeaveShip, self.av),
                                  Func(ship.boardingFinish, self.av, deckPos))
            self.swingTrack = swingTrack
            self.swingTrack.start(ts)
        else:
            if self.swingTrack:
                self.swingTrack.pause()
                self.swingTrack = None
            ship.boardingInit(self.av, ship)
            self.av.setPos(deckPos)
            fromShip.boardingLeaveShip(self.av)
            if self._shipBoardingFinishCall:
                self._shipBoardingFinishCall.destroy()
            self._shipBoardingFinishCall = FrameDelayedCall('shipToShipBoardingFinish-%s-%s' % (ship.doId, self.av.doId), Functor(ship.boardingFinish, self.av, deckPos))

    def enterEnsnared(self, extraArgs = []):
        self.av.motionFSM.off()
        self.av.stashBodyCollisions()
        if self.av.cannon:
            self.av.cannon.requestExit()
        
        self.ensnareTrack = Sequence(Wait(1.2), Func(self.av.stopCompassEffect), Func(self.av.loop, 'tentacle_squeeze'))
        self.ensnareTrack.start()
    
    def filterEnsnared(self, request, args = []):
        if request == 'advance':
            return 'Knockdown'
        
        if request in ('Idle', 'LandRoam', 'Battle', 'WaterRoam', 'Cannon', 'ShipBoarding'):
            return None
        
        return self.defaultFilter(request, args)

    def exitEnsnared(self):
        self.av.motionFSM.on()
        self.av.unstashBodyCollisions()
        if self.ensnareTrack != None:
            self.ensnareTrack.pause()
            del self.ensnareTrack
    
    def enterThrown(self, extraArgs = []):
        self.av.motionFSM.off()
        self.av.stopCompassEffect()

    def exitThrown(self):
        self.av.motionFSM.on()
        self.av.startCompassEffect()

    def enterKnockdown(self, extraArgs = []):
        self.av.motionFSM.off()
        self.knockdownTrack = Sequence(self.av.actorInterval('jail_standup'), Func(self.demand, 'LandRoam'))
        self.knockdownTrack.start()
    
    def filterKnockdown(self, request, args = []):
        if request == 'advance':
            return 'Idle'
        
        if request == 'Battle' or request == 'Cannon' or request == 'ShipBoarding':
            return
        
        return self.defaultFilter(request, args)
    
    def exitKnockdown(self):
        self.av.motionFSM.on()
        if self.knockdownTrack != None:
            self.knockdownTrack.pause()
            del self.knockdownTrack

    def enterUnconcious(self, extraArgs = []):
        self.av.motionFSM.off()
        self.av.stashBodyCollisions()
        if self.av.cannon:
            self.av.cannon.requestExit()
        
        self.av.loop('unconcious')

    def exitUnconcious(self):
        self.av.motionFSM.on()
        self.av.unstashBodyCollisions()

    def enterThrownInJail(self, extraArgs = []):
        if self.jailTrack:
            self.jailTrack.finish()
        
        self.av.motionFSM.off()
        self.av.stashBodyCollisions()
        self.jailTrack = Sequence(Func(self.av.hide), Wait(3), Func(self.av.show), self.av.actorInterval('jail_dropinto', blendOutT = 0), self.av.actorInterval('jail_standup', blendInT = 0))
        self.jailTrack.start()

    def exitThrownInJail(self):
        if self.jailTrack:
            self.jailTrack.finish()
        
        self.av.motionFSM.on()
        self.av.unstashBodyCollisions()
    
    def enterDoorKicking(self, extraArgs = []):
        self.av.motionFSM.off()
        kickT = self.av.getDuration('kick_door_loop')
        self.kickSfx = base.loadSfx('phase_4/audio/sfx_kick_door_loop.mp3')
        self.kickTrack = Sequence(Func(base.playSfx, self.kickSfx, node = self.av), Wait(kickT))
        self.av.loop('kick_door_loop')
        self.kickTrack.loop()
    
    def exitDoorKicking(self):
        self.kickTrack.pause()
        self.kickTrack = None
        loader.unloadSfx(self.kickSfx)
        del self.kickSfx
        self.av.motionFSM.on()
    
    def enterEnterTunnel(self, extraArgs = []):
        pass

    def exitEnterTunnel(self):
        pass

    def enterLeaveTunnel(self, extraArgs=[]):
        pass

    def exitLeaveTunnel(self):
        pass
    
    def enterEmote(self, extraArgs = []):
        if hasattr(self.av, 'emote_track') and self.av.emote_track is not None:
            self.av.emote_track.pause()
            self.av.emote_track = None
        
        if hasattr(self.av, 'emote_prop') and self.av.emote_prop is not None:
            self.av.emote_prop.removeNode()
            self.av.emote_prop = None
    
    def exitEmote(self):
        if self.av.emote_track is not None:
            self.av.emote_track.pause()
            self.av.emote_track = None
        
        if self.av.emote_prop is not None:
            self.av.emote_prop.removeNode()
            self.av.emote_prop = None

    def enterShipRepair(self, extraArgs = []):
        self.av.motionFSM.off()
        self.av.stopSmooth()
        if not self.repairHammer:
            self.repairHammer = loader.loadModel('models/props/hammer_high')
        
        if not self.hammerSfx:
            self.hammerSfx = loader.loadSfx('audio/ship_deck_hammer.mp3')
        
        self.av.stop('repairfloor_outof')
        if self.putAwayHammerTrack:
            self.putAwayHammerTrack.finish()
            self.putAwayHammerTrack = None
        
        self.repairHammerTrack = Sequence(Func(self.repairHammer.reparentTo, self.av.rightHandNode))
        self.repairHammerTrack.start()
        intoDur = self.av.getDuration('repairfloor_into')
        self.av.loop('repairfloor_idle', blendT = 0)
        self.doRepairSfxTaskName = 'startRepairSfx-%s' % self.av.doId
        self._repairingFrame = 0
        self._repairingStartT = globalClock.getRealTime()
        self._repairingIntoDur = intoDur
        taskMgr.add(self._doRepairingSfx, self.doRepairSfxTaskName)
    
    def _doRepairingSfx(self, task = None):
        if globalClock.getRealTime() - self._repairingStartT > self._repairingIntoDur + 0.5:
            lastFrame = self._repairingFrame
            curFrame = self.av.getCurrentFrame('repairfloor_loop')
            hitFrame = 15
            if lastFrame < hitFrame and curFrame >= hitFrame:
                base.playSfx(self.hammerSfx, node = self.av)
            
            self._repairingFrame = curFrame
        
        return task.cont

    def exitShipRepair(self):
        self.repairHammerTrack.pause()
        taskMgr.remove(self.doRepairSfxTaskName)
        if self.repairingSfxTrack:
            self.repairingSfxTrack.pause()
        
        self.av.play('repairfloor_outof')
        self.putAwayHammerTrack = Sequence(Wait(3.35), Func(self.repairHammer.detachNode))
        self.putAwayHammerTrack.start()
        self.av.motionFSM.on()
    
    def enterBeginFeast(self, extraArgs = []):
        self.torch = loader.loadModel('models/props/torch')
        self.torch.reparentTo(self.av.rightHandNode)
        self.torch.setPos(0.2, -.2, -.1)
        self.torch.setHpr(0, -110, 0)
        self.torch.setScale(0.6)
        from pirates.effects.SmallFire import SmallFire
        self.fireEffect = SmallFire()
        if self.fireEffect:
            self.fireEffect.reparentTo(self.torch.find('**/torch_effect_*'))
            self.fireEffect.startLoop()
        
        self.av.motionFSM.off()
        self.animationTrack = Sequence(self.av.actorInterval('wand_cast_start', blendOutT = 0), Func(self.av.loop, 'wand_cast_idle', blendT = 0), Wait(3.0), self.av.actorInterval('wand_cast_fire', playRate = 0.75))
        self.animationTrack.start()

    def exitBeginFeast(self):
        self.torch.removeNode()
        if self.fireEffect:
            self.fireEffect.stopLoop()
            self.fireEffect = None
        
        self.animationTrack.finish()
        self.av.motionFSM.on()
    
    def enterTentacleTargeted(self, extraArgs = []):
        pass
    
    def exitTentacleTargeted(self):
        pass
    
    def enterTentacleGrabbed(self, extraArgs = []):
        self.av.stopCompassEffect()
    
    def exitTentacleGrabbed(self):
        pass


