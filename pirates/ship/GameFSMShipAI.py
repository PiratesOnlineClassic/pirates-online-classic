import random

from pandac.PandaModules import *

from direct.fsm import FSM

class GameFSMShipAI(FSM.FSM):

    def __init__(self, air, ship):
        FSM.FSM.__init__(self, 'GameFSMShipAI')

        self.air = air
        self.ship = ship

        self.oceanGrid = self.ship.getParentObj()
        self.world = self.oceanGrid.getParentObj()

        self._sinkingTask = None
        self._pathFollowInterval = None

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterNeutral(self):
        pass

    def exitNeutral(self):
        pass

    def enterSpawn(self):
        pass

    def exitSpawn(self):
        pass

    def enterAdrift(self):
        pass

    def exitAdrift(self):
        pass

    def enterAISteering(self, avId):
        pass

    def exitAISteering(self):
        pass

    #def enterClientSteering(self, avId):
    #    pass
    #
    #def exitClientSteering(self):
    #    pass

    def enterDocked(self):
        pass

    def exitDocked(self):
        pass

    def enterPinned(self):
        pass

    def exitPinned(self):
        pass

    def enterEnsnared(self):
        pass

    def exitEnsnared(self):
        pass

    def enterShoveOff(self):
        pass

    def exitShoveOff(self):
        pass

    def enterSinking(self):

        def _shipSunk():
            self.ship.requestDelete()

        self._sinkingTask = taskMgr.doMethodLater(60, _shipSunk, self.ship.uniqueName('shipSunk'), extraArgs=[])

    def exitSinking(self):
        if self._sinkingTask is not None:
            taskMgr.remove(self._sinkingTask)
            self._sinkingTask = None

    def enterSunk(self):
        pass

    def enterRecoverFromSunk(self):
        pass

    def enterInBoardingPosition(self):
        pass

    def exitInBoardingPosition(self):
        pass

    def getPathFollowDoneName(self):
        return 'path-follow-done-%d' % self.ship.doId

    def enterPathFollow(self):
        self._followPath()

    def _followPath(self):
        followSpeed = 800.0
        dx, dy = self.air.worldCreator.oceanAreaManager.getRandomOceanPos(self.world.getUniqueId())

        destNode = NodePath('dest-node-%d' % self.ship.doId)
        destNode.setPos(dx, dy, 0)

        self.ship.setSailAnimState('Idle')
        self.ship.lookAt(destNode)

        self._pathFollowInterval = self.ship.posInterval(followSpeed, (dx, dy, 0), other=self.oceanGrid)
        self._pathFollowInterval.setDoneEvent(self.getPathFollowDoneName())

        self.acceptOnce(self.getPathFollowDoneName(), self._pathFollowDone)
        self._pathFollowInterval.start()

    def _pathFollowDone(self):
        self._followPath()

    def exitPathFollow(self):
        if self._pathFollowInterval is not None:
            self._pathFollowInterval.finish()
            self._pathFollowInterval = None

    def enterPatrol(self):
        pass

    def exitPatrol(self):
        pass

    def enterAttackChase(self):
        pass

    def exitAttackChase(self):
        pass

    def enterPutAway(self):
        pass

    def exitPutAway(self):
        pass

    def enterScriptedMovement(self):
        pass

    def exitScriptedMovement(self):
        pass
