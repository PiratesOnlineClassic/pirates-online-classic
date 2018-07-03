import random

from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm import FSM
from direct.interval.IntervalGlobal import *
from direct.task import Task
from panda3d.core import *
from pirates.piratesbase import (AvatarShadowCaster, PiratesGlobals, SkyGroup,
                                 TODGlobals)


class TimeOfDayManager(FSM.FSM):
    
    notify = directNotify.newCategory('TimeOfDayManager')

    def __init__(self):
        FSM.FSM.__init__(self, 'TimeOfDayManager')
        self.cycleType = TODGlobals.TOD_REGULAR_CYCLE
        self.cycleDuration = 0
        self.currentState = -1
        self.environment = TODGlobals.ENV_DEFAULT
        self.waitTaskName = 'waitForNextTODState-' + str(hash(self))
        self.nextDoLater = None
        self.startingTime = 0
        self.startingState = -1
        self.transitionIval = None
        if base.config.GetBool('advanced-weather', 1):
            pass
        self.skyGroup = SkyGroup.SkyGroup()
        self.skyGroup.reparentTo(camera)
        self.fixedSky = False
        self.skyEnabled = True
        self.sunLight = self.skyGroup.dirLightSun
        self.moonLight = self.skyGroup.dirLightMoon
        self.dlight = self.skyGroup.dirLightSun
        self.grassLight = self.skyGroup.grassLight
        self.alight = self.skyGroup.ambLight
        self.fog = Fog('TimeOfDayFog')
        self.fog.setExpDensity(TODGlobals.DAY_FOG_EXP)
        render.setFog(self.fog)
        self.avatarShadowCaster = None
        if base.config.GetBool('want-avatar-shadows', 1):
            self.enableAvatarShadows()
        self.fireworkShowMgr = None
        return

    def enableAvatarShadows(self):
        if not self.avatarShadowCaster:
            self.avatarShadowCaster = AvatarShadowCaster.AvatarShadowCaster(self.sunLight)
        self.avatarShadowCaster.enable()
        self.skyGroup.shadowCaster = self.avatarShadowCaster

    def disableAvatarShadows(self):
        if self.avatarShadowCaster:
            self.avatarShadowCaster.disable()
        self.skyGroup.shadowCaster = None
        return

    def disable(self):
        self.ignore('gotTimeSync')
        self.request('Off')

    def delete(self):
        render.clearLight(self.alight)
        render.clearLight(self.dlight)
        self.alight.removeNode()
        self.dlight.removeNode()
        del self.alight
        del self.dlight
        if self.avatarShadowCaster:
            self.avatarShadowCaster.disable()
            self.avatarShadowCaster = None
        self.skyGroup.stopCloudIval()
        self.skyGroup.removeNode()
        del self.skyGroup
        if self.transitionIval:
            self.transitionIval.pause()
        del self.transitionIval
        del self.fog
        if base.cr.activeWorld:
            base.cr.activeWorld.disableFireworkShow()
        self.ignoreAll()
        return

    def enterInitState(self):
        if not self.environment == TODGlobals.ENV_OFF:
            self.syncTimeOfDay()

    def syncTimeOfDay(self):
        if self.environment == TODGlobals.ENV_OFF:
            return
        self.notify.debug('Syncing time of day...')
        self.ignore('gotTimeSync')
        stateId, stateTime = self._computeCurrentState()
        stateName = TODGlobals.getStateName(stateId)
        self.request(stateName, stateTime)
        self.acceptOnce('gotTimeSync', self.syncTimeOfDay)

    def _computeCurrentState(self):
        if self.cycleDuration == 0:
            return (self.startingState, 0.0)
        elapsedTime = globalClockDelta.localElapsedTime(self.startingTime, bits=32)
        remTime = elapsedTime % self.cycleDuration
        stateId = self.startingState
        while 1:
            stateDuration = self.cycleDuration * TODGlobals.getStateDuration(self.cycleType, stateId)
            if remTime < stateDuration:
                return (stateId, remTime)
            else:
                remTime -= stateDuration
                stateId = TODGlobals.getNextStateId(self.cycleType, stateId)

    def _waitForNextStateRequest(self, stateId, elapsedTime):
        taskMgr.remove(self.waitTaskName)
        if self.cycleDuration == 0:
            return 0
        nextStateId = TODGlobals.getNextStateId(self.cycleType, stateId)
        nextStateName = TODGlobals.getStateName(nextStateId)
        stateDuration = self.cycleDuration * TODGlobals.getStateDuration(self.cycleType, stateId)
        delayTime = stateDuration - elapsedTime
        self.nextDoLater = taskMgr.doMethodLater(delayTime, self._doLaterRequest, self.waitTaskName, extraArgs=[])
        return stateDuration

    def _doLaterRequest(self):
        stateId, elapsedTime = self._computeCurrentState()
        nextStateName = TODGlobals.getStateName(stateId)
        self.request(nextStateName, elapsedTime)
        return Task.done

    def getStateName(self, stateId):
        return TODGlobals.getStateName(stateId)

    def pause(self):
        if self.transitionIval:
            self.transitionIval.pause()
        taskMgr.remove(self.waitTaskName)

    def unpause(self):
        self.enterInitState()

    def _transitionTimeOfDay(self, fromState, toState, t):
        if self.environment == TODGlobals.ENV_INTERIOR:
            environment = TODGlobals.ENV_DEFAULT
        else:
            environment = self.environment
        ival = Parallel(LerpFunctionInterval(self.alight.node().setColor, duration=t, toData=TODGlobals.AmbientLightColors[environment][toState], fromData=TODGlobals.AmbientLightColors[environment][fromState], name='TOD_aLightColor-%d'), LerpFunctionInterval(self.grassLight.node().setColor, duration=t, toData=TODGlobals.GrassLightColors[toState], fromData=TODGlobals.GrassLightColors[fromState], name='TOD_grassLightColor-%d'), LerpFunctionInterval(self.fog.setColor, duration=t, toData=TODGlobals.FogColors[environment][toState], fromData=TODGlobals.FogColors[environment][fromState], name='TOD_fogColor-%d'), LerpFunctionInterval(self.fog.setExpDensity, duration=t, toData=TODGlobals.FogExps[environment][toState], fromData=TODGlobals.FogExps[environment][fromState], name='TOD_fogExp-%d'), name='TOD_transitionTimeOfDay')
        if not self.fixedSky:
            fromSkyColor = TODGlobals.SkyColors[fromState]
            toSkyColor = TODGlobals.SkyColors[toState]
            ival.append(LerpFunctionInterval(base.win.setClearColor, duration=t, fromData=fromSkyColor, toData=toSkyColor))
            if hasattr(base, 'pe'):
                ival.append(LerpFunctionInterval(base.setBackgroundColor, duration=t, fromData=fromSkyColor, toData=toSkyColor))
            ival.append(self.skyGroup.transitionSky(fromState, toState, duration=t))
        self.currLight = self.skyGroup.getLight(fromState)
        self.dLight = self.skyGroup.getLight(toState)
        if self.currLight != self.dLight:
            ival.append(LerpFunctionInterval(self.currLight.node().setColor, duration=t, fromData=TODGlobals.DirectionalLightColors[environment][fromState], toData=Vec4(0, 0, 0, 0), name='TOD_dLightColorA-%d'))
            ival.append(LerpFunctionInterval(self.dLight.node().setColor, duration=t, toData=TODGlobals.DirectionalLightColors[environment][toState], fromData=Vec4(0, 0, 0, 0), name='TOD_dLightColorB-%d'))
        else:
            ival.append(LerpFunctionInterval(self.dlight.node().setColor, duration=t, toData=TODGlobals.DirectionalLightColors[environment][toState], fromData=TODGlobals.DirectionalLightColors[environment][fromState], name='TOD_dLightColor-%d'))
        return ival

    def _prepareState(self, stateId):
        if self.environment == TODGlobals.ENV_INTERIOR:
            environment = TODGlobals.ENV_DEFAULT
        else:
            environment = self.environment
        if not self.fixedSky:
            base.win.setClearColor(TODGlobals.SkyColors[stateId])
            if hasattr(base, 'pe'):
                base.setBackgroundColor(base.win.getClearColor())
            self.skyGroup.setSky(stateId)
        self.alight.node().setColor(TODGlobals.AmbientLightColors[environment][stateId])
        self.grassLight.node().setColor(TODGlobals.GrassLightColors[stateId])
        self.fog.setColor(TODGlobals.FogColors[environment][stateId])
        self.fog.setExpDensity(TODGlobals.FogExps[environment][stateId])
        self.sunLight.node().setColor(Vec4(0, 0, 0, 0))
        self.moonLight.node().setColor(Vec4(0, 0, 0, 0))
        self.dlight = self.skyGroup.getLight(stateId)
        render.setLight(self.dlight)
        self.dlight.node().setColor(TODGlobals.DirectionalLightColors[environment][stateId])
        if self.avatarShadowCaster:
            self.avatarShadowCaster.setLightSrc(self.dlight)

    def enterDawn(self, elapsedTime=0.0):
        self.currentState = PiratesGlobals.TOD_DAWN
        stateDuration = self._waitForNextStateRequest(self.currentState, elapsedTime)
        self._prepareState(self.currentState)
        beginTime = TODGlobals.getStateBeginTime(self.cycleType, self.currentState)
        endTime = beginTime + stateDuration / max(1.0, self.cycleDuration)
        self.transitionIval = self.skyGroup.transitionSun(beginTime, endTime, stateDuration)
        self.transitionIval.start(elapsedTime)
        self.skyGroup.unstashSun()
        self.skyGroup.stashMoon()
        messenger.send('timeOfDayChange', [self.currentState, stateDuration, elapsedTime])

    def exitDawn(self):
        taskMgr.remove(self.waitTaskName)
        self.transitionIval.finish()

    def enterDawn2Day(self, elapsedTime=0.0):
        self.currentState = PiratesGlobals.TOD_DAWN2DAY
        stateDuration = self._waitForNextStateRequest(self.currentState, elapsedTime)
        self.transitionIval = self._transitionTimeOfDay(PiratesGlobals.TOD_DAWN, PiratesGlobals.TOD_DAY, stateDuration)
        beginTime = TODGlobals.getStateBeginTime(self.cycleType, self.currentState)
        endTime = beginTime + stateDuration / max(1.0, self.cycleDuration)
        self.transitionIval.append(self.skyGroup.transitionSun(beginTime, endTime, stateDuration))
        self.transitionIval.start(elapsedTime)
        self.skyGroup.unstashSun()
        self.skyGroup.stashMoon()
        messenger.send('timeOfDayChange', [self.currentState, stateDuration, elapsedTime])

    def exitDawn2Day(self):
        taskMgr.remove(self.waitTaskName)
        self.transitionIval.finish()

    def enterDay(self, elapsedTime=0.0):
        self.currentState = PiratesGlobals.TOD_DAY
        stateDuration = self._waitForNextStateRequest(self.currentState, elapsedTime)
        self._prepareState(self.currentState)
        beginTime = TODGlobals.getStateBeginTime(self.cycleType, self.currentState)
        endTime = beginTime + stateDuration / max(1.0, self.cycleDuration)
        self.transitionIval = self.skyGroup.transitionSun(beginTime, endTime, stateDuration)
        self.transitionIval.start(elapsedTime)
        self.skyGroup.unstashSun()
        self.skyGroup.stashMoon()
        messenger.send('timeOfDayChange', [self.currentState, stateDuration, elapsedTime])

    def exitDay(self):
        taskMgr.remove(self.waitTaskName)
        self.transitionIval.finish()

    def enterDay2Dusk(self, elapsedTime=0.0):
        self.currentState = PiratesGlobals.TOD_DAY2DUSK
        stateDuration = self._waitForNextStateRequest(self.currentState, elapsedTime)
        self.transitionIval = self._transitionTimeOfDay(PiratesGlobals.TOD_DAY, PiratesGlobals.TOD_DUSK, stateDuration)
        beginTime = TODGlobals.getStateBeginTime(self.cycleType, self.currentState)
        endTime = beginTime + stateDuration / max(1.0, self.cycleDuration)
        self.transitionIval.append(self.skyGroup.transitionSun(beginTime, endTime, stateDuration))
        self.transitionIval.start(elapsedTime)
        self.skyGroup.unstashSun()
        self.skyGroup.stashMoon()
        messenger.send('timeOfDayChange', [self.currentState, stateDuration, elapsedTime])

    def exitDay2Dusk(self):
        taskMgr.remove(self.waitTaskName)
        self.transitionIval.finish()

    def enterDusk(self, elapsedTime=0.0):
        self.currentState = PiratesGlobals.TOD_DUSK
        stateDuration = self._waitForNextStateRequest(self.currentState, elapsedTime)
        self._prepareState(self.currentState)
        beginTime = TODGlobals.getStateBeginTime(self.cycleType, self.currentState)
        endTime = beginTime + stateDuration / max(1.0, self.cycleDuration)
        self.transitionIval = self.skyGroup.transitionSun(beginTime, endTime, stateDuration)
        self.transitionIval.start(elapsedTime)
        self.skyGroup.unstashSun()
        self.skyGroup.stashMoon()
        messenger.send('timeOfDayChange', [self.currentState, stateDuration, elapsedTime])

    def exitDusk(self):
        taskMgr.remove(self.waitTaskName)
        self.transitionIval.finish()

    def enterDusk2Night(self, elapsedTime=0.0):
        self.currentState = PiratesGlobals.TOD_DUSK2NIGHT
        stateDuration = self._waitForNextStateRequest(self.currentState, elapsedTime)
        self.transitionIval = self._transitionTimeOfDay(PiratesGlobals.TOD_DUSK, PiratesGlobals.TOD_NIGHT, stateDuration)
        beginTime = TODGlobals.getStateBeginTime(self.cycleType, self.currentState)
        endTime = beginTime + stateDuration / max(1.0, self.cycleDuration)
        self.transitionIval.append(self.skyGroup.transitionSun(beginTime, endTime, stateDuration))
        self.transitionIval.append(self.skyGroup.fadeOutSun(stateDuration))
        self.transitionIval.append(self.skyGroup.fadeInMoon(stateDuration))
        self.transitionIval.append(self.skyGroup.fadeInStars(stateDuration))
        self.transitionIval.start(elapsedTime)
        self.skyGroup.unstashSun()
        self.skyGroup.unstashMoon()
        messenger.send('timeOfDayChange', [self.currentState, stateDuration, elapsedTime])

    def exitDusk2Night(self):
        taskMgr.remove(self.waitTaskName)
        self.transitionIval.finish()

    def enterNight(self, elapsedTime=0.0):
        self.currentState = PiratesGlobals.TOD_NIGHT
        stateDuration = self._waitForNextStateRequest(self.currentState, elapsedTime)
        self._prepareState(self.currentState)
        self.skyGroup.setSunAngle(0)
        self.skyGroup.stashSun()
        self.skyGroup.unstashMoon()
        messenger.send('timeOfDayChange', [self.currentState, stateDuration, elapsedTime])

    def exitNight(self):
        taskMgr.remove(self.waitTaskName)

    def enterNight2Stars(self, elapsedTime=0.0):
        self.currentState = PiratesGlobals.TOD_NIGHT2STARS
        stateDuration = self._waitForNextStateRequest(self.currentState, elapsedTime)
        self.transitionIval = self._transitionTimeOfDay(PiratesGlobals.TOD_NIGHT, PiratesGlobals.TOD_STARS, stateDuration)
        self.transitionIval.append(self.skyGroup.fadeInStarsMore(stateDuration))
        self.transitionIval.start(elapsedTime)
        self.skyGroup.setSunAngle(0)
        self.skyGroup.stashSun()
        self.skyGroup.unstashMoon()
        messenger.send('timeOfDayChange', [self.currentState, stateDuration, elapsedTime])

    def exitNight2Stars(self):
        taskMgr.remove(self.waitTaskName)
        self.transitionIval.finish()

    def enterStars(self, elapsedTime=0.0):
        self.currentState = PiratesGlobals.TOD_STARS
        stateDuration = self._waitForNextStateRequest(self.currentState, elapsedTime)
        self._prepareState(self.currentState)
        self.skyGroup.setSunAngle(0)
        self.skyGroup.stashSun()
        self.skyGroup.unstashMoon()
        messenger.send('timeOfDayChange', [self.currentState, stateDuration, elapsedTime])
        if base.cr.activeWorld:
            base.cr.activeWorld.enableFireworkShow(elapsedTime)

    def exitStars(self):
        taskMgr.remove(self.waitTaskName)
        if base.cr.activeWorld:
            base.cr.activeWorld.disableFireworkShow()

    def enterStars2Dawn(self, elapsedTime=0.0):
        self.currentState = PiratesGlobals.TOD_STARS2DAWN
        stateDuration = self._waitForNextStateRequest(self.currentState, elapsedTime)
        self.transitionIval = self._transitionTimeOfDay(PiratesGlobals.TOD_STARS, PiratesGlobals.TOD_DAWN, stateDuration)
        beginTime = TODGlobals.getStateBeginTime(self.cycleType, self.currentState)
        endTime = beginTime + stateDuration / max(1.0, self.cycleDuration)
        self.transitionIval.append(self.skyGroup.transitionSun(beginTime, endTime, stateDuration))
        self.transitionIval.append(self.skyGroup.fadeInSun(stateDuration))
        self.transitionIval.append(self.skyGroup.fadeOutMoon(stateDuration))
        self.transitionIval.append(self.skyGroup.fadeOutStars(stateDuration))
        self.transitionIval.start(elapsedTime)
        self.skyGroup.unstashSun()
        self.skyGroup.unstashMoon()
        messenger.send('timeOfDayChange', [self.currentState, stateDuration, elapsedTime])

    def exitStars2Dawn(self):
        taskMgr.remove(self.waitTaskName)
        self.transitionIval.finish()

    def enterHalloweenNight(self, elapsedTime=0.0):
        self.currentState = PiratesGlobals.TOD_HALLOWEEN
        stateDuration = self._waitForNextStateRequest(self.currentState, elapsedTime)
        self._prepareState(self.currentState)
        self.skyGroup.setSunAngle(0)
        self.skyGroup.stashSun()
        self.skyGroup.unstashMoonBig()
        self.skyGroup.moonOverlay.stash()
        self.skyGroup.setMoonState(0.0)
        messenger.send('timeOfDayChange', [self.currentState, stateDuration, elapsedTime])

    def exitHalloweenNight(self):
        taskMgr.remove(self.waitTaskName)

    def enterFullMoon(self, elapsedTime=0.0):
        self.currentState = PiratesGlobals.TOD_FULLMOON
        stateDuration = self._waitForNextStateRequest(self.currentState, elapsedTime)
        self._prepareState(PiratesGlobals.TOD_HALLOWEEN)
        self.skyGroup.setSunAngle(0)
        self.skyGroup.stashSun()
        self.skyGroup.setMoonState(1.0)
        self.skyGroup.unstashMoonBig()
        self.transitionIval = self.skyGroup.fadeInMoonOverlay()
        self.transitionIval.start()
        messenger.send('timeOfDayChange', [self.currentState, stateDuration, elapsedTime])

    def exitFullMoon(self):
        taskMgr.remove(self.waitTaskName)
        self.transitionIval.finish()

    def enterHalf2FullMoon(self, elapsedTime=0.0):
        self.currentState = PiratesGlobals.TOD_HALF2FULLMOON
        stateDuration = self._waitForNextStateRequest(self.currentState, elapsedTime)
        self._prepareState(PiratesGlobals.TOD_HALLOWEEN)
        self.skyGroup.setSunAngle(0)
        self.skyGroup.stashSun()
        self.skyGroup.unstashMoonBig()
        self.transitionIval = self.skyGroup.transitionMoon(0.0, 0.95, stateDuration)
        self.transitionIval.start(elapsedTime)
        messenger.send('timeOfDayChange', [self.currentState, stateDuration, elapsedTime])

    def exitHalf2FullMoon(self):
        taskMgr.remove(self.waitTaskName)
        self.transitionIval.finish()

    def enterFull2HalfMoon(self, elapsedTime=0.0):
        self.currentState = PiratesGlobals.TOD_FULL2HALFMOON
        stateDuration = self._waitForNextStateRequest(self.currentState, elapsedTime)
        self._prepareState(PiratesGlobals.TOD_HALLOWEEN)
        self.skyGroup.setSunAngle(0)
        self.skyGroup.stashSun()
        self.skyGroup.unstashMoonBig()
        self.transitionIval = Parallel(self.skyGroup.fadeOutMoonOverlay(), self.skyGroup.transitionMoon(1.0, 0.0, stateDuration))
        self.transitionIval.start(elapsedTime)
        messenger.send('timeOfDayChange', [self.currentState, stateDuration, elapsedTime])

    def exitFull2HalfMoon(self):
        taskMgr.remove(self.waitTaskName)
        self.skyGroup.moonOverlay.stash()
        self.transitionIval.finish()

    def enterNoLighting(self):
        if self.transitionIval:
            self.transitionIval.pause()
            self.transitionIval = None
        render.clearLight(self.alight)
        render.clearLight(self.dlight)
        render.setFogOff()
        messenger.send('nametagAmbientLightChanged', [None])
        if self.nextDoLater:
            self.nextDoLater.remove()
            self.nextDoLater = None
        return

    def exitNoLighting(self):
        render.setLight(self.alight)
        render.setLight(self.dlight)
        render.setFog(self.fog)
        messenger.send('nametagAmbientLightChanged', [self.alight])

    def enterOff(self):
        if self.transitionIval:
            self.transitionIval.pause()
            self.transitionIval = None
        self.disableAvatarShadows()
        taskMgr.remove(self.waitTaskName)
        render.clearLight(self.alight)
        render.clearLight(self.dlight)
        messenger.send('nametagAmbientLightChanged', [None])
        if self.nextDoLater:
            self.nextDoLater.remove()
            self.nextDoLater = None
        return

    def exitOff(self):
        render.setLight(self.alight)
        render.setLight(self.dlight)
        if base.win and not base.win.isClosed():
            if base.config.GetBool('want-avatar-shadows', 1):
                self.enableAvatarShadows()
        messenger.send('nametagAmbientLightChanged', [self.alight])

    def setEnvironment(self, envId, geom=None):
        if envId == TODGlobals.ENV_OFF:
            self.request('Off')
        elif envId == TODGlobals.ENV_SWAMP and self.currentState not in [PiratesGlobals.TOD_HALLOWEEN, PiratesGlobals.TOD_FULLMOON, PiratesGlobals.TOD_HALF2FULLMOON, PiratesGlobals.TOD_FULL2HALFMOON]:
            self.fixedSky = True
            base.win.setClearColor(TODGlobals.SkyColors[PiratesGlobals.TOD_SWAMP])
            self.skyGroup.setSky(PiratesGlobals.TOD_SWAMP)
        elif envId == TODGlobals.ENV_CAVE:
            self._prepareState(PiratesGlobals.TOD_NIGHT)
            self.skyGroup.stash()
            self.fixedSky = True
            self.pause()
        else:
            self.unpause()
            self.fixedSky = False
            if self.skyEnabled:
                self.skyGroup.unstash()
        self.environment = envId
        self.enterInitState()
