from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.distributed.ClockDelta import globalClockDelta

from pirates.piratesbase import TODGlobals, PiratesGlobals


class DistributedTimeOfDayManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTimeOfDayManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.cycleType = config.GetInt('tod-starting-cycle', TODGlobals.TOD_REGULAR_CYCLE)
        self.startingState = TODGlobals.getStartingState(self.cycleType)
        self.startingTime = globalClockDelta.getFrameNetworkTime(bits=32)
        self.cycleDuration = config.GetFloat('tod-cycle-duration', PiratesGlobals.TOD_CYCLE_DURATION)
        self.stateTime = 0
        self.nextProcessStateChange = None
        self.timeOfDayStateMethodList = []

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        self.notify.debug('Starting time of day...')
        self._processStateChange()

        self.accept('HolidayStarted', self.processHolidayChanged)
        self.accept('HolidayEnded', self.processHolidayChanged)

    def delete(self):
        DistributedObjectAI.delete(self)
        if self.nextProcessStateChange:
            taskMgr.remove(self.nextProcessStateChange)

        self.ignore('HolidayStarted')
        self.ignore('HolidayEnded')

    def addTimeOfDayStateMethod(self, state, uniqueName, method, extraArgs=None):
        methodTuple = (state, uniqueName, method, extraArgs)
        for entry in self.timeOfDayStateMethodList:
            if entry[1] == uniqueName:
                self.notify.warning('Double registered TOD method: %s' % uniqueName)

        self.timeOfDayStateMethodList.append(methodTuple)
        self.notify.debug('Registered TOD method: %s' % uniqueName)

    def _computeCurrentState(self):
        if self.cycleDuration == 0:
            return (self.startingState, 0.0)

        elapsedTime = globalClockDelta.localElapsedTime(self.startingTime, bits=32)
        remTime = elapsedTime % self.cycleDuration
        stateId = self.startingState
        while True:
            stateDuration = self.cycleDuration * TODGlobals.getStateDuration(self.cycleType, stateId)
            if remTime < stateDuration:
                return (stateId, remTime)
            else:
                remTime -= stateDuration
                stateId = TODGlobals.getNextStateId(self.cycleType, stateId)

    def _waitForNextState(self):
        if self.nextProcessStateChange:
            taskMgr.remove(self.nextProcessStateChange)

        if self.cycleDuration == 0:
            return 0

        nextStateId = TODGlobals.getNextStateId(self.cycleType, self.startingState)
        nextStateName = TODGlobals.getStateName(nextStateId)
        stateDuration = self.cycleDuration * TODGlobals.getStateDuration(self.cycleType, self.startingState)
        delayTime = stateDuration - self.stateTime

        self.notify.debug('Delay until next state: %s' % delayTime)
        self.nextProcessStateChange = taskMgr.doMethodLater(delayTime, self._processStateChange, 'tod-wait-task-%s' % self.doId, extraArgs=[])

        return stateDuration

    def _handleTimeOfDayStateMethods(self, state, stateTime):
        for entry in self.timeOfDayStateMethodList:
            if entry[0] == state:
                entry[2](self.cycleType, state, stateTime)

    def _processStateChange(self):
        lastState = self.startingState
        newState, stateTime = self._computeCurrentState()
        self.notify.debug('New State (%s) with remaining time: %s' % (newState, stateTime))
        self._handleTimeOfDayStateMethods(newState, stateTime)

        self.startingState = newState
        self.stateTime = stateTime
        self._waitForNextState()

        return Task.done

    def sync(self, cycleType, startingState, startingTime, cycleDuration):
        self.cycleType = cycleType
        self.startingState = startingState
        self.startingTime = startingTime
        self.cycleDuration = cycleDuration

    def d_sync(self, cycleType, startingState, startingTime, cycleDuration):
        self.sendUpdate('sync', [cycleType, startingState, startingTime, cycleDuration])

    def b_sync(self, cycleType, startingState, startingTime, cycleDuration):
        self.sync(cycleType, startingState, startingTime, cycleDuration)
        self.d_sync(cycleType, startingState, startingTime, cycleDuration)

    def getSync(self):
        return [self.cycleType, self.startingState, self.startingTime, self.cycleDuration]

    def changeCycleType(self, cycleType):
        if self.cycleType == cycleType:
            return

        self.notify.debug('TimeOfDayManager cycle changing..')
        startingState = TODGlobals.getStartingState(cycleType)
        self._processStateChange()

        self.b_sync(cycleType, startingState, self.startingTime, self.cycleDuration)

    def isNight(self):
        nightStates = [
            PiratesGlobals.TOD_NIGHT,
            PiratesGlobals.TOD_NIGHT2STARS,
            PiratesGlobals.TOD_STARS,
            PiratesGlobals.TOD_STARS2DAWN
        ]

        return self.startingState in nightStates

    def isDay(self):
        return not isNight()

    def isHalloweenMoon(self):
        return self.startingState == PiratesGlobals.TOD_HALLOWEEN

    def processHolidayChanged(self, holidayId):
        HolidayTODS = {
            PiratesGlobals.HALLOWEEN: TODGlobals.TOD_HALLOWEEN_CYCLE,
            PiratesGlobals.JOLLYROGERCURSE: TODGlobals.TOD_JOLLYCURSE_CYCLE,
            PiratesGlobals.JOLLYCURSEAUTO: TODGlobals.TOD_JOLLYCURSE_CYCLE,
            PiratesGlobals.CURSEDNIGHT: TODGlobals.TOD_JOLLYCURSE_CYCLE
        }

        found = None
        for holidayId in HolidayTODS:
            if self.air.newsManager.isHolidayActive(holidayId):
                found = holidayId
                break

        # Update TOD Cycle
        if found is not None:
            self.changeCycleType(HolidayTODS[found])
        else:
            if self.cycleType != TODGlobals.TOD_REGULAR_CYCLE:
                self.changeCycleType(TODGlobals.TOD_REGULAR_CYCLE)
