from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.distributed.ClockDelta import globalClockDelta
from direct.task import Task

from otp.ai.MagicWordGlobal import *

from pirates.instance.DistributedInstanceWorldAI import DistributedInstanceWorldAI
from pirates.piratesbase import PiratesGlobals


class DistributedTreasureMapInstanceAI(DistributedInstanceWorldAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTreasureMapInstanceAI')

    # how long an instance with nobody left in it waits before it is
    # removed, long enough for the last avatars to finish teleporting out...
    CleanupDelay = 15.0

    def __init__(self, air):
        DistributedInstanceWorldAI.__init__(self, air)
        FSM.__init__(self, self.__class__.__name__)

        self.type = PiratesGlobals.INSTANCE_TM

        self.state = 'Off'
        self.treasureMapDoId = 0
        self.objectives = []
        self.fortIds = []
        self.participants = []  # List of avatar doIds participating
        self.barrierData = {}
        self.readyAvatars = []

    def announceGenerate(self):
        DistributedInstanceWorldAI.announceGenerate(self)

    def delete(self):
        taskMgr.remove(self.uniqueName('cleanupInstance'))
        self.participants = []
        self.readyAvatars = []
        DistributedInstanceWorldAI.delete(self)

    def addParticipant(self, avatarId):
        """Add an avatar to the instance participants"""
        taskMgr.remove(self.uniqueName('cleanupInstance'))
        if avatarId not in self.participants:
            self.participants.append(avatarId)
            self.notify.info('Added participant %d to instance %d' % (avatarId, self.doId))

    def removeParticipant(self, avatarId):
        """Remove an avatar from the instance participants"""
        if avatarId in self.participants:
            self.participants.remove(avatarId)
            self.notify.info('Removed participant %d from instance %d' % (avatarId, self.doId))

            # once the last avatar has left (or was disconnected) there is
            # nobody left to finish the treasure map, the instance is removed...
            if not self.participants:
                taskMgr.remove(self.uniqueName('cleanupInstance'))
                taskMgr.doMethodLater(self.CleanupDelay, self.__cleanupInstance,
                    self.uniqueName('cleanupInstance'))
        if avatarId in self.readyAvatars:
            self.readyAvatars.remove(avatarId)

    def __cleanupInstance(self, task):
        if self.participants or self.air.doId2do.get(self.doId) is not self:
            return Task.done

        self.notify.info('Removing empty treasure map instance %d' % self.doId)

        # the islands and their game areas are all generated beneath us, along
        # with any sub instance (interiors) a game area may have been given...
        for subInstance in self.getSubInstances():
            self.removeSubInstance(subInstance)
            self._deleteBuilderObjects(subInstance.builder)
            subInstance.requestDelete()

        self._deleteBuilderObjects(self.builder)
        if self.oceanGrid and self.air.doId2do.get(self.oceanGrid.doId) is self.oceanGrid:
            self.oceanGrid.requestDelete()

        if self.air.uidMgr.getDoId(self.getUniqueId()) == self.doId:
            self.air.uidMgr.removeUid(self.getUniqueId())

        self.requestDelete()
        return Task.done

    def _deleteBuilderObjects(self, builder):
        for object in list(builder.objectList.values()):
            childBuilder = getattr(object, 'builder', None)
            if childBuilder is not None and childBuilder is not builder and hasattr(childBuilder, 'objectList'):
                self._deleteBuilderObjects(childBuilder)

            builder.removeObject(object)
            if self.air.doId2do.get(object.doId) is object:
                object.requestDelete()

    def getParticipants(self):
        return self.participants

    # --- Parenting Rules ---
    def getParentingRules(self):
        return ['', '']

    # --- Treasure Map ID ---
    def setTreasureMapDoId(self, doId):
        self.treasureMapDoId = doId

    def d_setTreasureMapDoId(self, doId):
        self.sendUpdate('setTreasureMapDoId', [doId])

    def b_setTreasureMapDoId(self, doId):
        self.setTreasureMapDoId(doId)
        self.d_setTreasureMapDoId(doId)

    def getTreasureMapDoId(self):
        return self.treasureMapDoId

    # --- Objectives ---
    def setObjectives(self, objectives):
        self.objectives = objectives

    def d_setObjectives(self, objectives):
        self.sendUpdate('setObjectives', [objectives])

    def b_setObjectives(self, objectives):
        self.setObjectives(objectives)
        self.d_setObjectives(objectives)

    def getObjectives(self):
        return self.objectives

    # --- Fort IDs ---
    def setFortIds(self, fortIds):
        self.fortIds = fortIds

    def d_setFortIds(self, fortIds):
        self.sendUpdate('setFortIds', [fortIds])

    def b_setFortIds(self, fortIds):
        self.setFortIds(fortIds)
        self.d_setFortIds(fortIds)

    def getFortIds(self):
        return self.fortIds

    # --- State Management ---
    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterWaitClientsReady(self):
        """Waiting for all clients to signal they are ready"""
        self.notify.info('Entering WaitClientsReady state')

    def exitWaitClientsReady(self):
        pass

    def enterStageOne(self):
        self.notify.info('Entering StageOne')

    def exitStageOne(self):
        pass

    def enterStageTwo(self):
        self.notify.info('Entering StageTwo')

    def exitStageTwo(self):
        pass

    def enterStageThree(self):
        self.notify.info('Entering StageThree')

    def exitStageThree(self):
        pass

    def enterStageFour(self):
        self.notify.info('Entering StageFour')

    def exitStageFour(self):
        pass

    def enterReward(self):
        self.notify.info('Entering Reward state')

    def exitReward(self):
        pass

    def enterNotCompleted(self):
        self.notify.info('Instance not completed')

    def exitNotCompleted(self):
        pass

    def enterCompleted(self):
        self.notify.info('Instance completed successfully')
        for avatarId in list(self.participants):
            if avatarId not in self.air.doId2do:
                self.removeParticipant(avatarId)
                continue

            self._approveParticipantLeave(avatarId)

    def exitCompleted(self):
        pass

    def setState(self, state, *args):
        self.request(state, *args)

    def d_setState(self, state):
        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        self.sendUpdate('setState', [state, timestamp])

    def b_setState(self, state):
        self.setState(state)
        self.d_setState(state)

    def getState(self):
        return [self.state, 0]

    # --- Client Messages ---
    def requestState(self, state):
        """Client requests a state change"""
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return

        self.notify.info('Avatar %d requests state %s' % (avatarId, state))
        # Validate state transition is allowed
        if self._isValidStateTransition(state):
            self.b_setState(state)

    def _isValidStateTransition(self, newState):
        """Check if state transition is valid"""
        validTransitions = {
            'Off': ['WaitClientsReady', 'StageOne'],
            'WaitClientsReady': ['StageOne', 'NotCompleted'],
            'StageOne': ['StageTwo', 'NotCompleted'],
            'StageTwo': ['StageThree', 'NotCompleted'],
            'StageThree': ['StageFour', 'NotCompleted'],
            'StageFour': ['Reward', 'NotCompleted'],
            'Reward': ['Completed'],
            'NotCompleted': ['Completed'],
            'Completed': []
        }
        allowed = validTransitions.get(self.state, [])
        return newState in allowed

    def requestLeave(self, reason):
        """Client requests to leave the instance"""
        avatarId = self.air.getAvatarIdFromSender()
        if not avatarId:
            return

        if avatarId not in self.participants:
            self.notify.warning('Avatar %d requested to leave instance %d without being a participant' %
                (avatarId, self.doId))
            return

        self.notify.info('Avatar %d requests to leave instance (reason=%d)' % (avatarId, reason))

        # an avatar defeated in a treasure map is not sent to jail, the client
        # leaves the treasure map instead, so it is revived on it's way out...
        avatar = self.air.doId2do.get(avatarId)
        if avatar and avatar.getHp()[0] <= 0:
            self._reviveDefeatedAvatar(avatar)

        self._approveParticipantLeave(avatarId)

    def _reviveDefeatedAvatar(self, avatar):
        self.notify.info('Reviving defeated avatar %d leaving instance %d' % (avatar.doId, self.doId))
        self.air.targetMgr.clearAttacker(avatar)
        avatar.b_setHp(avatar.getMaxHp())
        avatar.b_setMojo(avatar.getMaxMojo())

    def _approveParticipantLeave(self, avatarId):
        """Return a participant and remove them only after a return is available."""
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return False

        if not self._sendAvatarToMainWorld(avatar):
            return False

        self.removeParticipant(avatarId)
        return True

    def _sendAvatarToMainWorld(self, avatar):
        """Send an avatar back to the main world"""
        # Find the main world instance
        teleportMgr = getattr(self.air, 'teleportMgr', None)
        mainWorld = teleportMgr and teleportMgr.getWorld(
            PiratesGlobals.INSTANCE_MAIN, 'PiratesWorld')
        if not mainWorld:
            self.notify.warning('Could not find main world to return avatar to')
            return False

        # The Black Pearl client uses this interest while it requests a main-world teleport.
        islands = mainWorld.builder.getIslands()
        if not islands:
            self.notify.warning('Could not find an island for avatar %d to return to' % avatar.doId)
            return False

        island = islands[0]
        self.sendUpdateToAvatarId(avatar.doId, 'requestLeaveApproved', [
            mainWorld.doId, island.zoneId, 0])
        return True

    # --- Treasure Map Complete ---
    def d_setTMComplete(self, instanceResults, playerResults):
        """Send completion results to clients"""
        self.sendUpdate('setTMComplete', [instanceResults, playerResults])
