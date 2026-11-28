from direct.distributed.ClockDelta import globalClockDelta
from direct.showbase.PythonUtil import randFloat
from direct.task import Task

from pirates.piratesbase import PiratesGlobals


class PosHprBroadcasterAI:
    """
    Broadcasts an AI driven smooth node's position the way the client's own
    DistributedSmoothNode broadcast (CDistributedSmoothNodeBase.broadcastPosHprFull) does:
    only the components that changed since the last broadcast are sent, using the smallest
    of the setSm* fields that covers them, and a single setSmStop is sent once the object
    comes to rest. The setSm* fields are ram fields, so the state server keeps the last
    position for anyone gaining interest later on.

    With autoStop the broadcast task removes itself once the stop has been sent, whatever
    moves the object again (a walk, a look at) has to restart it, so an object standing
    still costs nothing...
    """

    PosHprBroadcastPeriod = PiratesGlobals.AI_BROADCAST_PERIOD

    # the precision of the setComponent fields, int32/10 and int16%360/10:
    _posScale = 10
    _hprScale = 10

    def __init__(self):
        self._posHprBroadcastTask = None
        self._posHprAutoStop = False
        self._sentPosHpr = None
        self._sentStop = False

    def getPosHprBroadcastTaskName(self):
        return self.uniqueName('broadcast-pos')

    def posHprBroadcastStarted(self):
        return self._posHprBroadcastTask is not None

    def _getNetPosHpr(self):
        x, y, z = self.getPos()
        h, p, r = self.getHpr()
        posScale, hprScale = self._posScale, self._hprScale
        return (int(round(x * posScale)), int(round(y * posScale)), int(round(z * posScale)),
            int(round((h % 360.0) * hprScale)), int(round((p % 360.0) * hprScale)),
            int(round((r % 360.0) * hprScale)))

    def sendCurrentPosition(self):
        x, y, z = self.getPos()
        h, p, r = self.getHpr()
        self._sentPosHpr = self._getNetPosHpr()
        self._sentStop = False
        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        self.sendUpdate('setSmPosHpr', [x, y, z, h, p, r, timestamp])

    def broadcastPosHprFull(self):
        """
        Sends the components that changed since the last broadcast, returns False
        when nothing did (after the one stop message has been sent).
        """

        if self._sentPosHpr is None:
            self.sendCurrentPosition()
            return True

        netPosHpr = self._getNetPosHpr()
        changed = [netPosHpr[i] != self._sentPosHpr[i] for i in range(6)]
        if not any(changed):
            if not self._sentStop:
                self._sentStop = True
                self.sendUpdate('setSmStop', [globalClockDelta.getRealNetworkTime(bits=16)])

            return False

        self._sentPosHpr = netPosHpr
        self._sentStop = False

        cx, cy, cz, ch, cp, cr = changed
        x, y, z = self.getPos()
        h, p, r = self.getHpr()
        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        if not (cx or cy or cz or cp or cr):
            self.sendUpdate('setSmH', [h, timestamp])
        elif not (cx or cy or ch or cp or cr):
            self.sendUpdate('setSmZ', [z, timestamp])
        elif not (cz or ch or cp or cr):
            self.sendUpdate('setSmXY', [x, y, timestamp])
        elif not (cy or ch or cp or cr):
            self.sendUpdate('setSmXZ', [x, z, timestamp])
        elif not (ch or cp or cr):
            self.sendUpdate('setSmPos', [x, y, z, timestamp])
        elif not (cx or cy or cz):
            self.sendUpdate('setSmHpr', [h, p, r, timestamp])
        elif not (cz or cp or cr):
            self.sendUpdate('setSmXYH', [x, y, h, timestamp])
        elif not (cp or cr):
            self.sendUpdate('setSmXYZH', [x, y, z, h, timestamp])
        else:
            self.sendUpdate('setSmPosHpr', [x, y, z, h, p, r, timestamp])

        return True

    def startPosHprBroadcast(self, period=None, stagger=0, autoStop=False):
        """
        Starts broadcasting our position every period seconds, an already running
        broadcast is left alone (it may only lose it's autoStop).
        """

        if self._posHprBroadcastTask is not None:
            self._posHprAutoStop = self._posHprAutoStop and autoStop
            return

        if period is None:
            period = self.PosHprBroadcastPeriod

        self._posHprAutoStop = autoStop
        self._posHprBroadcastPeriod = period

        # send what changed right away, a walk shouldn't wait a period to show...
        self.broadcastPosHprFull()

        delay = period
        if stagger:
            delay = randFloat(period)

        self._posHprBroadcastTask = taskMgr.doMethodLater(delay, self._posHprBroadcast,
            self.getPosHprBroadcastTaskName())

    def _posHprBroadcast(self, task):
        if self.isEmpty():
            self._posHprBroadcastTask = None
            return Task.done

        moved = self.broadcastPosHprFull()
        if not moved and self._posHprAutoStop:
            self._posHprBroadcastTask = None
            return Task.done

        task.delayTime = self._posHprBroadcastPeriod
        return Task.again

    def stopPosHprBroadcast(self):
        if self._posHprBroadcastTask is not None:
            taskMgr.remove(self._posHprBroadcastTask)
            self._posHprBroadcastTask = None

    def kickPosHprBroadcast(self):
        """
        Called by anything that moves the object, broadcasts the move and keeps
        broadcasting until the object comes to rest again.
        """

        self.startPosHprBroadcast(autoStop=True)
