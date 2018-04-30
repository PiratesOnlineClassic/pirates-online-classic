import random
import types

from direct.distributed.ClockDelta import *
from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import Enum
from pirates.battle import EnemyGlobals
from pirates.effects.WaterRipple import WaterRipple
from pirates.pirate import Human
from pirates.piratesbase import PiratesGlobals

WALK_CUTOFF = 0.5
NPC_WALK_CUTOFF = 0.5
RUN_CUTOFF = PiratesGlobals.ToonForwardSpeed
NPC_RUN_CUTOFF = 17.0

class MotionAnimFSM(FSM):
    BLENDAMT = 0.4
    GROUNDSTATE = Enum('OverSolid, OverWater')
    notify = directNotify.newCategory('MotionAnimFSM')

    def __init__(self, av):
        FSM.__init__(self, 'MotionAnimFSM')
        self.av = av
        self.groundState = self.GROUNDSTATE.OverSolid
        self.airborneState = False
        self.setAllowAirborne(True)
        self.landIval = None
        self.landRunIval = None
        self.idleJumpIval = None
        self.lastMoveSpeed = 0
        self.zeroSpeedTimer = 0
        self.motionFSMLag = base.config.GetBool('motionfsm-lag', True)

    def cleanup(self):
        if not self.isInTransition():
            FSM.cleanup(self)

        self.landIval = None
        self.landRunIval = None
        self.idleJumpIval = None
        if hasattr(self, 'av'):
            self.ignoreAll()
            del self.av

    def setAnimInfo(self, animInfo, reset=True):
        self.animInfo = animInfo
        if reset:
            self.request(self.state)

    def trackAnimToSpeed(self, task=None):
        if self.airborneState != self.av.controlManager.getIsAirborne():
            self.av.b_setAirborneState(not self.airborneState)

        speeds = self.av.controlManager.getSpeeds()
        if speeds:
            self.updateAnimState(*speeds)

        if task:
            return task.cont

    def adjustAnimScale(self, state, moveSpeed, slideSpeed=0):
        currAnimName = self.av.getCurrentAnim()
        if self.av.isNpc == False or currAnimName != 'walk' and currAnimName != 'run' and currAnimName != 'bayonet_walk' and currAnimName != 'bayonet_run':
            return
        style = self.av.style
        scale = None
        if hasattr(self.av, 'walkAnimScale'):
            scale = self.av.walkAnimScale
        if self.av is not localAvatar and style or scale:
            if scale:
                newScale = moveSpeed * scale
            else:
                if type(style) is not types.StringType:
                    style = style.getBodyShape()

                animFileName = self.av.getAnimFilename(self.av.getCurrentAnim())
                animSpeedScale = PiratesGlobals.GetAnimScale(animFileName)
                if animSpeedScale == None:
                    if currAnimName == 'walk' or currAnimName == 'bayonet_walk':
                        animSpeedScale = 0.244
                    else:
                        animSpeedScale = 0.03

                newScale = moveSpeed * animSpeedScale
                avScale = EnemyGlobals.getEnemyScale(self.av)
                if avScale:
                    newScale /= avScale

            newScale = max(newScale, 0.25)
            if currAnimName == 'walk' or currAnimName == 'bayonet_walk':
                animIdx = PiratesGlobals.WALK_INDEX
            else:
                animIdx = PiratesGlobals.RUN_INDEX

            currPlayRate = self.av.getPlayRate(self.animInfo[animIdx][0])
            if currPlayRate == None or abs(currPlayRate - newScale) < 0.075:
                return

            if animIdx == PiratesGlobals.WALK_INDEX:
                newAnimInfo = ((self.animInfo[PiratesGlobals.STAND_INDEX][0], self.animInfo[PiratesGlobals.STAND_INDEX][1]),
                    (self.animInfo[PiratesGlobals.WALK_INDEX][0], newScale)) + self.animInfo[2:]
            else:
                newAnimInfo = ((self.animInfo[PiratesGlobals.STAND_INDEX][0], self.animInfo[PiratesGlobals.STAND_INDEX][1]),
                    (self.animInfo[PiratesGlobals.WALK_INDEX][0], self.animInfo[PiratesGlobals.WALK_INDEX][1]),
                    (self.animInfo[PiratesGlobals.RUN_INDEX][0], newScale)) + self.animInfo[3:]

            if slideSpeed:
                slideSpeed = max(slideSpeed, 0.45)
                newAnimInfo = ((self.animInfo[PiratesGlobals.STAND_INDEX][0], self.animInfo[PiratesGlobals.STAND_INDEX][1]),
                    (self.animInfo[PiratesGlobals.WALK_INDEX][0], self.animInfo[PiratesGlobals.WALK_INDEX][1]),
                    (self.animInfo[PiratesGlobals.RUN_INDEX][0], self.animInfo[PiratesGlobals.RUN_INDEX][1]),
                    (self.animInfo[PiratesGlobals.REVERSE_INDEX][0], self.animInfo[PiratesGlobals.REVERSE_INDEX][1]),
                    (self.animInfo[PiratesGlobals.STRAFE_LEFT_INDEX][0], slideSpeed),
                    (self.animInfo[PiratesGlobals.STRAFE_RIGHT_INDEX][0], slideSpeed)) + self.animInfo[6:]

            self.av.motionFSM.setAnimInfo(newAnimInfo, reset=False)
            self.av.setPlayRate(newScale, self.animInfo[animIdx][0])

    def updateNPCAnimState(self, forwardSpeed, rotateSpeed=0, slideSpeed=0):
        animScaleAdjust = False
        if self.canBeAirborne and self.airborneState:
            state = 'Airborne'
        elif slideSpeed >= WALK_CUTOFF:
            if self.av.getAnimFilename('strafe_right'):
                state = 'StrafeRight'
            else:
                state = 'WalkForward'
        elif slideSpeed <= -WALK_CUTOFF:
            if self.av.getAnimFilename('strafe_left'):
                state = 'StrafeLeft'
            else:
                state = 'WalkForward'
        elif forwardSpeed >= NPC_RUN_CUTOFF:
            state = 'Run'
            animScaleAdjust = True
        elif forwardSpeed > NPC_WALK_CUTOFF:
            state = 'WalkForward'
            animScaleAdjust = True
        elif rotateSpeed > 0.0:
            if self.av.getAnimFilename('spin_left'):
                state = 'SpinLeft'
            else:
                state = 'WalkForward'
        elif rotateSpeed < 0.0:
            if self.av.getAnimFilename('spin_right'):
                state = 'SpinRight'
            else:
                state = 'WalkForward'
        else:
            state = 'Idle'

        zeroSpeedLimit = 0.1
        if globalClock.getFrameTime() - self.zeroSpeedTimer < zeroSpeedLimit and self.motionFSMLag:
            if state != self.state and self.state != 'Idle':
                return

        if animScaleAdjust:
            self.adjustAnimScale(state, forwardSpeed, slideSpeed)

        if self.state != state:
            if self.isInTransition():
                self.demand(state)
            else:
                self.request(state)

        self.lastMoveSpeed = forwardSpeed
        self.zeroSpeedTimer = globalClock.getFrameTime()

    def updateAnimState(self, forwardSpeed, rotateSpeed, slideSpeed=0.0):
        if self.canBeAirborne and self.airborneState:
            state = 'Airborne'
        elif forwardSpeed >= WALK_CUTOFF and slideSpeed >= WALK_CUTOFF:
            state = 'StrafeRightDiag'
        elif forwardSpeed >= WALK_CUTOFF and slideSpeed <= -WALK_CUTOFF:
            state = 'StrafeLeftDiag'
        elif forwardSpeed >= RUN_CUTOFF:
            state = 'Run'
        elif forwardSpeed >= WALK_CUTOFF:
            state = 'WalkForward'
            self.adjustAnimScale(state, forwardSpeed)
        elif forwardSpeed <= -WALK_CUTOFF and slideSpeed >= WALK_CUTOFF:
            state = 'StrafeRightDiagReverse'
        elif forwardSpeed <= -WALK_CUTOFF and slideSpeed <= -WALK_CUTOFF:
            state = 'StrafeLeftDiagReverse'
        elif forwardSpeed <= -WALK_CUTOFF:
            state = 'WalkReverse'
        elif slideSpeed >= WALK_CUTOFF:
            state = 'StrafeRight'
        elif slideSpeed <= -WALK_CUTOFF:
            state = 'StrafeLeft'
        elif rotateSpeed > 0.0:
            state = 'SpinLeft'
        elif rotateSpeed < 0.0:
            state = 'SpinRight'
        else:
            state = 'Idle'

        if self.state != state:
            if self.isInTransition():
                self.demand(state)
            else:
                self.request(state)

            if self.av.isLocal() and self.av.getGameState() == 'Emote':
                messenger.send('localAvatarExitEmote')

            if not self.av.isLocal() and self.av.getGameState() == 'Emote':
                self.av.playEmote(self.av.emoteId)

    def setAllowAirborne(self, allow):
        self.canBeAirborne = allow

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def handleAirborneEvent(self, event):
        if event == 'Jump':
            self.av.b_playMotionAnim('jump')
        elif event == 'Land':
            self.av.b_playMotionAnim('land')

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def playMotionAnim(self, anim, local=True):
        if anim == 'jump':
            if local:
                self.jump()
            else:
                self.jump()
        else:
            if anim == 'land':
                if local:
                    speeds = self.av.controlManager.getSpeeds()
                    if speeds[0] == 0.0:
                        self.land()
                    else:
                        self.landRun()
                else:
                    self.land()

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def jump(self):
        if self.state == 'Idle':
            startFrame = 1
            endFrame = 31
            if self.idleJumpIval:
                self.idleJumpIval.finish()

            self.idleJumpIval = self.av.actorInterval('jump', startFrame=startFrame, endFrame=endFrame, playRate=1.5,
                blendInT=0.0, blendOutT=self.BLENDAMT * 0.5)

            self.idleJumpIval.start()
        else:
            startFrame = 6
            endFrame = 31
            self.av.play('jump', fromFrame=startFrame, toFrame=endFrame, blendInT=self.BLENDAMT * 0.5,
                blendOutT=self.BLENDAMT * 0.5)

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def land(self):
        if self.landIval:
            self.landIval.finish()

        startFrame = 31
        endFrame = 43
        self.landIval = self.av.actorInterval('jump', startFrame=startFrame, endFrame=endFrame, blendInT=0.0,
            blendOutT=self.BLENDAMT * 0.5)

        self.landIval.start()

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def landRun(self):
        if not self.landRunIval:
            startFrame = 32
            endFrame = startFrame + 5
            self.landRunIval = self.av.actorInterval('jump', startFrame=startFrame, endFrame=endFrame,
                blendInT=0.0, blendOutT=0.15)

        self.landRunIval.start()

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def setAirborneState(self, airborneState):
        self.airborneState = airborneState

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def getAirborneState(self):
        return self.airborneState

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def isAirborne(self):
        return self.airborneState

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def setGroundState(self, groundState):
        if self.groundState != groundState:
            self.groundState = groundState
            if self.state == 'Airborne':
                self.request('Airborne')

    def startTrackAnimToSpeed(self):
        taskName = self.av.taskName('trackAnimToSpeed')
        taskMgr.remove(taskName)
        self.trackAnimToSpeed(None)
        taskMgr.add(self.trackAnimToSpeed, taskName)

    def stopTrackAnimToSpeed(self):
        taskName = self.av.taskName('trackAnimToSpeed')
        taskMgr.remove(taskName)

    def enterOff(self):
        if self.landIval:
            self.landIval.finish()

        if self.landRunIval:
            self.landRunIval.finish()

        if self.idleJumpIval:
            self.idleJumpIval.finish()

        if self.av.isLocal():
            self.ignore('jumpStart')
            self.ignore('jumpLand')
            self.ignore('jumpLandHard')

        if self.av.isLocal():
            self.av.setMovementIndex(-1)

    def exitOff(self):
        if self.av.isLocal():
            self.accept('jumpStart', self.handleAirborneEvent, ['Jump'])
            self.accept('jumpLand', self.handleAirborneEvent, ['Land'])
            self.accept('jumpLandHard', self.handleAirborneEvent, ['Land'])

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def enterIdle(self):
        anim, rate = self.animInfo[PiratesGlobals.STAND_INDEX]
        blendT = self.BLENDAMT * 0.5
        if anim and rate:
            self.av.loop(anim, rate, blendT=blendT)

        self.av.startLookAroundTask()
        self.av.motionFSMEnterState(self.newState)
        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.STAND_INDEX)

    def exitIdle(self):
        self.av.stopLookAroundTask()
        self.av.motionFSMExitState(self.oldState)

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def enterWalkForward(self):
        anim, rate = self.animInfo[PiratesGlobals.WALK_INDEX]
        blendT = self.BLENDAMT * 0.5
        if anim and rate:
            self.av.loop(anim, rate, blendT=blendT)

        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.WALK_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()

    def exitWalkForward(self):
        pass

    def enterWalkReverse(self):
        anim, rate = self.animInfo[PiratesGlobals.REVERSE_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT=self.BLENDAMT)

        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.REVERSE_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()

    def exitWalkReverse(self):
        pass

    def enterSpinLeft(self):
        anim, rate = self.animInfo[PiratesGlobals.SPIN_LEFT_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT=self.BLENDAMT)

        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.SPIN_LEFT_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()

    def exitSpinLeft(self):
        pass

    def enterSpinRight(self):
        anim, rate = self.animInfo[PiratesGlobals.SPIN_RIGHT_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT=self.BLENDAMT)

        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.SPIN_RIGHT_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()

    def exitSpinRight(self):
        pass

    def enterStrafeRight(self):
        anim, rate = self.animInfo[PiratesGlobals.STRAFE_RIGHT_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT=self.BLENDAMT)

        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.STRAFE_RIGHT_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()

    def exitStrafeRight(self):
        pass

    def enterStrafeLeft(self):
        anim, rate = self.animInfo[PiratesGlobals.STRAFE_LEFT_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT=self.BLENDAMT)

        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.STRAFE_LEFT_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()

    def exitStrafeLeft(self):
        pass

    def enterStrafeRightDiag(self):
        anim, rate = self.animInfo[PiratesGlobals.STRAFE_RIGHT_DIAG_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT=self.BLENDAMT)

        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.STRAFE_RIGHT_DIAG_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()

    def exitStrafeRightDiag(self):
        pass

    def enterStrafeLeftDiag(self):
        anim, rate = self.animInfo[PiratesGlobals.STRAFE_LEFT_DIAG_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT=self.BLENDAMT)

        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.STRAFE_LEFT_DIAG_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()

    def exitStrafeLeftDiag(self):
        pass

    def enterStrafeRightDiagReverse(self):
        anim, rate = self.animInfo[PiratesGlobals.STRAFE_RIGHT_DIAG_REV_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT=self.BLENDAMT)

        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.STRAFE_RIGHT_DIAG_REV_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()

    def exitStrafeRightDiagReverse(self):
        pass

    def enterStrafeLeftDiagReverse(self):
        anim, rate = self.animInfo[PiratesGlobals.STRAFE_LEFT_DIAG_REV_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT=self.BLENDAMT)

        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.STRAFE_LEFT_DIAG_REV_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()

    def exitStrafeLeftDiagReverse(self):
        pass

    def enterAdvance(self):
        anim, rate = self.animInfo[PiratesGlobals.ADVANCE_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT=self.BLENDAMT)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()

    def exitAdvance(self):
        pass

    def enterRetreat(self):
        anim, rate = self.animInfo[PiratesGlobals.RETREAT_INDEX]
        if anim and rate:
            self.av.loop(anim, rate, blendT=self.BLENDAMT)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()

    def exitRetreat(self):
        pass

    def enterRun(self):
        anim, rate = self.animInfo[PiratesGlobals.RUN_INDEX]
        blendT = self.BLENDAMT * 0.5
        if anim and rate:
            self.av.loop(anim, rate, blendT=blendT)

        if self.av.isLocal():
            self.av.setMovementIndex(PiratesGlobals.RUN_INDEX)
            if self.av.cameraFSM.currentCamera:
                self.av.cameraFSM.currentCamera.avFaceCamera()

    def exitRun(self):
        pass

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def enterAirborne(self):
        if self.groundState == self.GROUNDSTATE.OverSolid:
            idleAnim = self.animInfo[PiratesGlobals.OVER_SOLID_INDEX][0]
            self.av.loop(idleAnim, blendT=0.0)
        else:
            if self.groundState == self.GROUNDSTATE.OverWater:
                idleAnim = self.animInfo[PiratesGlobals.OVER_WATER_INDEX][0]
                self.av.loop(idleAnim, blendT=0.0)

        if self.av.isLocal():
            self.av.setMovementIndex(-1)

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def exitAirborne(self):
        pass

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-jump-report'])
    def request(self, *args, **kwargs):
        FSM.request(self, *args, **kwargs)


class MotionFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('MotionFSM')
    BLENDAMT = 0.25

    def __init__(self, av):
        FSM.__init__(self, 'MotionFSM')
        self.av = av
        self.cannotFloat = 0
        self.motionAnimFSM = MotionAnimFSM(self.av)
        if hasattr(self.av, 'getAnimInfo'):
            self.setAnimInfo(self.av.getAnimInfo('LandRoam'))

        self.lifterDelayFrames = 0
        self.__locked = 0

    def setAvatar(self, av):
        self.av = av
        self.motionAnimFSM.av = av

    def cleanup(self):
        FSM.cleanup(self)
        if hasattr(self, 'av'):
            self.ignoreAll()
            self.motionAnimFSM.cleanup()
            del self.motionAnimFSM
            del self.av

    def off(self):
        if self.__locked:
            return

        self.request('Off')

    def on(self):
        if self.__locked:
            return

        self.request('On')

    def moveLock(self):
        if self.__locked:
            return

        self.request('MoveLock')

    def lock(self):
        self.__locked = 1

    def unlock(self):
        self.__locked = 0

    def setAnimInfo(self, animInfo, reset=True):
        self.animInfo = animInfo
        self.motionAnimFSM.setAnimInfo(animInfo, reset)

    def setAllowAirborne(self, allow):
        self.motionAnimFSM.setAllowAirborne(allow)

    def filterOff(self, request, args):
        return self.defaultFilter(request, args)

    def defaultFilter(self, request, args):
        if self.av.isLocal():
            if localAvatar.gameFSM and localAvatar.gameFSM.state == 'Cutscene':
                return

        return FSM.defaultFilter(self, request, args)

    def enterOff(self):
        idleAnim = self.animInfo[PiratesGlobals.STAND_INDEX][0]
        if idleAnim:
            self.av.loop(idleAnim, blendT=self.BLENDAMT)

        self.av.stopLookAroundTask()
        if hasattr(self.av, 'loadAnimatedHead'):
            if self.av.loadAnimatedHead == False:
                self.av.headNode.setHpr(self.av.headFudgeHpr)

    def exitOff(self):
        pass

    def enterOn(self):
        if self.av.canMove:
            self.av.startSmooth()

        if self.av.isLocal():
            self.av.startPosHprBroadcast()
            self.av.collisionsOn()
            self.motionAnimFSM.startTrackAnimToSpeed()
            self.av.enableAvatarControls()
            if not self.av.ship:
                self.startCheckUnderWater()

    def exitOn(self):
        if self.av.isLocal():
            self.av.stopLookAroundTask()
            if self.av.loadAnimatedHead == False:
                self.av.headNode.setHpr(self.av.headFudgeHpr)

            self.av.stopPosHprBroadcast()
            self.av.collisionsOff()
            self.motionAnimFSM.stopTrackAnimToSpeed()
            self.av.disableAvatarControls()
            self.stopCheckUnderWater()
            self.av.setActiveShadow(0)
            self.motionAnimFSM.request('Off')

    def enterMoveLock(self):
        idleAnim = self.animInfo[PiratesGlobals.STAND_INDEX][0]
        if idleAnim:
            self.av.loop(idleAnim, blendT=self.BLENDAMT)

        self.av.startSmooth()
        if self.av.isLocal():
            self.av.startLookAroundTask()
            self.av.startPosHprBroadcast()
            self.av.collisionsOn()
            self.startCheckUnderWater()

    def exitMoveLock(self):
        self.av.stopSmooth()
        if self.av.isLocal():
            self.av.stopLookAroundTask()
            if self.av.loadAnimatedHead == False:
                self.av.headNode.setHpr(self.av.headFudgeHpr)

            self.av.stopPosHprBroadcast()
            self.av.collisionsOff()
            self.av.setActiveShadow(0)
            self.motionAnimFSM.request('Off')

    def startCheckUnderWater(self):
        if self.cannotFloat:
            return

        self.stopCheckUnderWater()
        if self.getCurrentOrNextState() is not 'Off':
            task = taskMgr.add(self.__checkUnderWater, 'localAvatarCheckUnderWater', priority=34)
            task.oldParent = self.av.getParent()

    def stopCheckUnderWater(self):
        if self.cannotFloat:
            return

        taskMgr.remove('localAvatarCheckUnderWater')
        self.__submerged = None
        self.__overwater = None
        self.__inwater = None
        self.av.disableWaterEffect()

    def __checkUnderWater(self, task):
        if not (hasattr(self.av.controlManager.currentControls, 'lifter') and base.cr.isOceanEnabled()):
            return task.cont

        if self.lifterDelayFrames:
            self.lifterDelayFrames -= 1
            return task.cont

        avHeight = 5.0
        waterZ = base.cr.getWaterHeight(self.av)
        avZ = self.av.getZ(render)
        if avZ <= waterZ and not self.__inwater:
            self.__inwater = True
            self.av.enableWaterEffect()

        if avZ > waterZ and self.__inwater:
            self.__inwater = False
            self.av.disableWaterEffect()

        if self.__inwater:
            offset = waterZ - avZ + 0.15
            speeds = self.av.controlManager.getSpeeds()
            self.av.adjustWaterEffect(offset, *speeds)

        curControls = self.av.controlManager.currentControls
        if curControls.lifter.hasContact():
            avAirborneHeight = curControls.lifter.getAirborneHeight()
            if self.__submerged:
                if avAirborneHeight < avHeight and not self.av.bobbing:
                    self.__submerged = False
                    self.__overwater = False
                    if task.oldParent == self.av.getParent():
                        self.av.setZ(avZ - avAirborneHeight)

                    self.av.cameraFSM.fpsCamera.lerpFromZOffset(avAirborneHeight, PiratesGlobals.SWIM_WALK_TRANSITION_TIME)
                    self.av.controlManager.currentControls.oneTimeCollide()
                    messenger.send('localAvatarExitWater')
                    self.av.b_setGroundState(self.motionAnimFSM.GROUNDSTATE.OverSolid)
            else:
                if avZ + avHeight - avAirborneHeight <= waterZ and not self.__overwater:
                    self.__overwater = True
                    self.av.b_setGroundState(self.motionAnimFSM.GROUNDSTATE.OverWater)

                if avZ + avHeight <= waterZ:
                    self.__submerged = True
                    messenger.send('localAvatarEnterWater')
                    self.av.controlManager.currentControls.isAirborne = 0
                    curControls.abortJump()

                if avZ == waterZ and avAirborneHeight > avHeight:
                    self.__submerged = True
                    self.__overwater = True
        else:
            if self.__submerged != True:
                self.__submerged = True
                self.__overwater = True
                messenger.send('localAvatarEnterWater')

        task.oldParent = self.av.getParent()
        return task.cont

    def isAirborne(self):
        return not self.__submerged and self.motionAnimFSM.airborneState

    def setWaterState(self, overWater, submerged):
        self.__submerged = submerged
        self.__overWater = overWater

    def setLifterDelayFrames(self, frames):
        self.lifterDelayFrames = frames
