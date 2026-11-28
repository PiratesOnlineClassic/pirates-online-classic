import random

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task

from otp.ai.MagicWordGlobal import *

from pirates.piratesbase import PiratesGlobals
from pirates.pvp.DistributedPVPInstanceAI import DistributedPVPInstanceAI
from pirates.pvp.DistributedPVPBattleAI import DistributedPVPBattleAI
from pirates.pvp.DistributedPVPTeamBattleAI import DistributedPVPTeamBattleAI
from pirates.pvp.DistributedPVPShipBattleAI import DistributedPVPShipBattleAI

# the world creator uses this to decide which instance class should
# be generated when one of the pvp world files is loaded...
PVPWorldClasses = {
    'pvp_captureWorld': DistributedPVPTeamBattleAI,
    'pvp_deathmatchWorld1': DistributedPVPTeamBattleAI,
    'pvp_deathmatchWorld2': DistributedPVPTeamBattleAI,
    'pvp_mayhemWorld1': DistributedPVPBattleAI,
    'pvpTestv2': DistributedPVPBattleAI,
    'pvp_shipBattleWorld1': DistributedPVPShipBattleAI,
    'pvp_shipBattle4IslandWorld1': DistributedPVPShipBattleAI,
}

PVPGameStyleWorlds = {
    PiratesGlobals.GAME_STYLE_BATTLE: config.GetString('pvp-battle-worlds', 'pvpTestv2').split(),
    PiratesGlobals.GAME_STYLE_TEAM_BATTLE: config.GetString('pvp-team-battle-worlds', 'pvp_captureWorld').split(),
    PiratesGlobals.GAME_STYLE_SHIP_BATTLE: config.GetString('pvp-ship-battle-worlds', 'pvp_shipBattleWorld1').split(),
}


class PVPManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPManagerAI')

    ChallengeTimeout = config.GetFloat('pvp-challenge-timeout', 60.0)
    ChallengeGameStyle = config.GetInt('pvp-challenge-game-style', PiratesGlobals.GAME_STYLE_TEAM_BATTLE)

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        # challengeeId -> [challengerIds]
        self.challenges = {}
        self.instances = {}

    def delete(self):
        for challengeeId, challengerIds in list(self.challenges.items()):
            for challengerId in challengerIds:
                taskMgr.remove(self.getChallengeTaskName(challengerId, challengeeId))

        self.challenges = {}
        self.instances = {}
        self.ignoreAll()
        DistributedObjectAI.delete(self)

    def getParentingRules(self):
        return ['', '']

    # -------------------------------------------------------------------
    # Challenges
    # -------------------------------------------------------------------

    def isAvatarInPVP(self, avatar):
        world = avatar.getWorld()
        if world and world.getType() == PiratesGlobals.INSTANCE_PVP:
            return True

        for instance in list(self.instances.values()):
            if instance.hasPlayer(avatar.doId):
                return True

        return False

    def canChallenge(self, challenger, challengee):
        if challenger.doId == challengee.doId:
            return False

        if self.isAvatarInPVP(challenger) or self.isAvatarInPVP(challengee):
            return False

        teleportMgr = self.air.teleportMgr
        if challenger.doId in teleportMgr.avatar2fsm or challengee.doId in teleportMgr.avatar2fsm:
            return False

        return True

    def getChallengeTaskName(self, challengerId, challengeeId):
        return self.uniqueName('challenge-%d-%d' % (challengerId, challengeeId))

    def hasChallenge(self, challengerId, challengeeId):
        return challengerId in self.challenges.get(challengeeId, [])

    def addChallenge(self, challengerId, challengeeId):
        challengerIds = self.challenges.setdefault(challengeeId, [])
        if challengerId not in challengerIds:
            challengerIds.append(challengerId)

        taskName = self.getChallengeTaskName(challengerId, challengeeId)
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(self.ChallengeTimeout, self.__challengeExpired, taskName,
            extraArgs=[challengerId, challengeeId])

    def removeChallenge(self, challengerId, challengeeId):
        taskMgr.remove(self.getChallengeTaskName(challengerId, challengeeId))
        challengerIds = self.challenges.get(challengeeId)
        if not challengerIds or challengerId not in challengerIds:
            return

        challengerIds.remove(challengerId)
        if not challengerIds:
            del self.challenges[challengeeId]

    def __challengeExpired(self, challengerId, challengeeId):
        self.removeChallenge(challengerId, challengeeId)
        return Task.done

    def requestChallenge(self, challengeeId):
        challengerId = self.air.getAvatarIdFromSender()
        challenger = self.air.doId2do.get(challengerId)
        if not challenger:
            return

        challengee = self.air.doId2do.get(challengeeId)
        if not challengee or not hasattr(challengee, 'getInventory'):
            self.notify.debug('Avatar %d tried to challenge unknown avatar %d' % (
                challengerId, challengeeId))

            return

        if not self.canChallenge(challenger, challengee):
            self.notify.debug('Avatar %d cannot challenge avatar %d' % (
                challengerId, challengeeId))

            return

        self.addChallenge(challengerId, challengeeId)
        self.d_challengeFrom(challengeeId, challengerId)

    def acceptChallenge(self, challengerId):
        challengeeId = self.air.getAvatarIdFromSender()
        challengee = self.air.doId2do.get(challengeeId)
        if not challengee:
            return

        if not self.hasChallenge(challengerId, challengeeId):
            self.air.logPotentialHacker(
                message='Avatar accepted a pvp challenge that was never issued',
                targetAvId=challengeeId,
                challengerId=challengerId)

            return

        self.removeChallenge(challengerId, challengeeId)
        challenger = self.air.doId2do.get(challengerId)
        if not challenger:
            return

        if not self.canChallenge(challenger, challengee):
            return

        # once an avatar has accepted a challenge, any other challenges
        # issued by or to either of the avatars are no longer valid...
        for avatarId in (challengerId, challengeeId):
            for otherChallengerId in list(self.challenges.get(avatarId, [])):
                self.removeChallenge(otherChallengerId, avatarId)

        self.d_challengeAccepted(challengerId, challengeeId)
        self.d_challengeAccepted(challengeeId, challengerId)
        self.createPVPInstance(self.ChallengeGameStyle, [[challengerId], [challengeeId]])

    def d_challengeFrom(self, avatarId, challengerId):
        self.sendUpdateToAvatarId(avatarId, 'challengeFrom', [challengerId])

    def d_challengeAccepted(self, avatarId, otherAvatarId):
        self.sendUpdateToAvatarId(avatarId, 'challengeAccepted', [otherAvatarId])

    # -------------------------------------------------------------------
    # Instances
    # -------------------------------------------------------------------

    def getWorldFile(self, gameStyle):
        worldFiles = PVPGameStyleWorlds.get(gameStyle)
        if not worldFiles:
            return None

        return random.choice(worldFiles)

    def getRegionUid(self, worldFile):
        fileData = self.air.worldCreator.openFile(worldFile + '.py')
        if not fileData:
            return None

        for objKey, objData in list(fileData.get('Objects', {}).items()):
            if objData.get('Type') == 'Region':
                return objKey

        return None

    def createPVPInstance(self, gameStyle, teams):
        worldFile = self.getWorldFile(gameStyle)
        if not worldFile or worldFile not in PVPWorldClasses:
            self.notify.warning('Cannot create pvp instance, no world for game style %d!' %
                gameStyle)

            return None

        regionUid = self.getRegionUid(worldFile)
        if not regionUid:
            self.notify.warning('Cannot create pvp instance, no region found in %s!' %
                worldFile)

            return None

        self.notify.info('Creating pvp instance %s for teams: %r' % (worldFile, teams))

        # the region uid is shared with every other instance of this world,
        # so capture the doId of the newly generated instance straight away...
        previousDoId = self.air.uidMgr.getDoId(regionUid)
        self.air.worldCreator.loadObjectsFromFile(worldFile + '.py')
        instanceDoId = self.air.uidMgr.getDoId(regionUid)
        if not instanceDoId or instanceDoId == previousDoId:
            self.notify.warning('Pvp world %s did not generate an instance!' % worldFile)
            return None

        instance = self.air.doId2do.get(instanceDoId)
        if not isinstance(instance, DistributedPVPInstanceAI):
            self.notify.warning('Pvp world %s generated an invalid instance: %r!' % (
                worldFile, instance))

            return None

        self.instances[instance.doId] = instance
        self.acceptOnce(instance.getDeleteEvent(), self.__instanceDeleted,
            extraArgs=[instance.doId])

        instance.setupMatch(teams)
        return instance

    def __instanceDeleted(self, instanceDoId):
        self.instances.pop(instanceDoId, None)

    def getInstances(self):
        return list(self.instances.values())


@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int, int])
def pvp(gameStyle=PiratesGlobals.GAME_STYLE_TEAM_BATTLE, opponentId=0):
    """
    Starts a pvp game of the given style for the target, optionally against an opponent
    """
    avatar = spellbook.getTarget()
    pvpManager = spellbook.getManager().air.pvpManager
    if gameStyle not in PVPGameStyleWorlds:
        return 'Invalid pvp game style %d' % gameStyle

    teams = [[avatar.doId]]
    if opponentId:
        teams.append([opponentId])

    instance = pvpManager.createPVPInstance(gameStyle, teams)
    if not instance:
        return 'Failed to create pvp instance!'

    return 'Created pvp instance %d (%s)' % (instance.doId, instance.getFileName())
