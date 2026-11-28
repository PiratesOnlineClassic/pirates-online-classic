import math

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.StatePush import FunctionCall
from direct.task import Task

from otp.chat import ChatFilter
from pirates.battle import WeaponGlobals
from pirates.pvp.SiegeManagerBase import SiegeManagerBase
from pirates.pvp.SiegeAnnouncerAI import SiegeAnnouncerAI
from pirates.pvp import PVPGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType


class SiegeManagerAI(DistributedObjectAI, SiegeManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('SiegeManagerAI')

    # the client opens interest on this zone under the siege manager
    # once the local avatar joins a siege team (see SiegeManager._addAnnouncerInterest)
    ANNOUNCER_ZONE = 555

    # siege team ids, these match PVPGlobals.siegeTeamNames
    TEAM_FRENCH = 1
    TEAM_SPANISH = 2
    TeamIds = (TEAM_FRENCH, TEAM_SPANISH)

    TEAM_UPDATE_PERIOD = 2.0

    # how often the respawn invulnerability cutoff sphere is checked
    INVULNERABILITY_CHECK_PERIOD = 1.0

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        SiegeManagerBase.__init__(self)

        self._pvpEnabled = config.GetBool('want-privateering', 1)
        self._wantTeamBalance = config.GetBool('want-pvp-team-balance', 1)
        self._teamBalanceMargin = config.GetInt('pvp-team-balance-margin', 20)

        self._teamsJoinable = {}
        self._teamShips = {}
        self._teamScores = {}
        for teamId in self.TeamIds:
            self._teamsJoinable[teamId] = True
            self._teamShips[teamId] = set()
            self._teamScores[teamId] = 0

        self._avatar2team = {}
        self._avatar2ship = {}
        self._invulnerableAvatars = {}
        self._sinkStreaks = {}
        self._teamIslands = None
        self._regenElapsed = 0.0

        self.announcer = None

        self._useIslandRegen = PVPGlobals.WantIslandRegen.getValue()
        self._useRepairSpots = PVPGlobals.WantShipRepairSpots.getValue()
        self._useRepairKit = PVPGlobals.WantShipRepairKit.getValue()

        self._islandRegenUpdater = None
        self._repairSpotsUpdater = None
        self._repairKitUpdater = None

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        self.announcer = SiegeAnnouncerAI(self.air)
        self.announcer.generateWithRequiredAndId(self.air.allocateChannel(), self.doId, self.ANNOUNCER_ZONE)

        # the siege settings are state var settings that can be changed live
        # by the settings manager, make sure we keep the clients up to date...
        self._islandRegenUpdater = FunctionCall(self.b_setUseIslandRegen, PVPGlobals.WantIslandRegen)
        self._repairSpotsUpdater = FunctionCall(self.b_setUseRepairSpots, PVPGlobals.WantShipRepairSpots)
        self._repairKitUpdater = FunctionCall(self.b_setUseRepairKit, PVPGlobals.WantShipRepairKit)

        taskMgr.doMethodLater(self.TEAM_UPDATE_PERIOD, self._updateTeamsTask, self.uniqueName('updateSiegeTeams'))

    def delete(self):
        taskMgr.remove(self.uniqueName('updateSiegeTeams'))

        for updater in (self._islandRegenUpdater, self._repairSpotsUpdater, self._repairKitUpdater):
            if updater:
                updater.destroy()

        self._islandRegenUpdater = None
        self._repairSpotsUpdater = None
        self._repairKitUpdater = None

        for teamId in self.TeamIds:
            for shipId in list(self._teamShips[teamId]):
                self.ignore('distObjDelete-%d' % shipId)

        for avatarId in list(self._avatar2team.keys()):
            self.ignore(self.air.getAvatarExitEvent(avatarId))

        for avatarId in list(self._invulnerableAvatars.keys()):
            self._clearInvulnerabilityTasks(avatarId)

        self._teamShips = {}
        self._avatar2team = {}
        self._avatar2ship = {}
        self._invulnerableAvatars = {}
        self._sinkStreaks = {}
        self._teamIslands = None

        if self.announcer:
            self.announcer.requestDelete()
            self.announcer = None

        DistributedObjectAI.delete(self)

    def setPvpEnabled(self, pvpEnabled):
        self._pvpEnabled = pvpEnabled

    def d_setPvpEnabled(self, pvpEnabled):
        self.sendUpdate('setPvpEnabled', [pvpEnabled])

    def b_setPvpEnabled(self, pvpEnabled):
        self.setPvpEnabled(pvpEnabled)
        self.d_setPvpEnabled(pvpEnabled)

    def getPvpEnabled(self):
        return self._pvpEnabled

    def setTeamsJoinable(self, teamJoinableItems):
        for teamId, joinable in teamJoinableItems:
            self._teamsJoinable[teamId] = joinable

    def d_setTeamsJoinable(self, teamJoinableItems):
        self.sendUpdate('setTeamsJoinable', [teamJoinableItems])

    def b_setTeamsJoinable(self, teamJoinableItems):
        self.setTeamsJoinable(teamJoinableItems)
        self.d_setTeamsJoinable(teamJoinableItems)

    def getTeamsJoinable(self):
        return [[teamId, self._teamsJoinable[teamId]] for teamId in self.TeamIds]

    def d_setUseIslandRegen(self, useIslandRegen):
        self.sendUpdate('setUseIslandRegen', [useIslandRegen])

    def b_setUseIslandRegen(self, useIslandRegen):
        self.setUseIslandRegen(useIslandRegen)
        self.d_setUseIslandRegen(useIslandRegen)

    def setUseRepairSpots(self, useRepairSpots):
        SiegeManagerBase.setUseRepairSpots(self, useRepairSpots)

        # the privateer ships only have repair spots while they are enabled...
        for teamId in self.TeamIds:
            for ship in self.getTeamShips(teamId):
                if useRepairSpots:
                    self.createShipRepairSpots(ship)
                else:
                    self.deleteShipRepairSpots(ship)

    def d_setUseRepairSpots(self, useRepairSpots):
        self.sendUpdate('setUseRepairSpots', [useRepairSpots])

    def b_setUseRepairSpots(self, useRepairSpots):
        self.setUseRepairSpots(useRepairSpots)
        self.d_setUseRepairSpots(useRepairSpots)

    def d_setUseRepairKit(self, useRepairKit):
        self.sendUpdate('setUseRepairKit', [useRepairKit])

    def b_setUseRepairKit(self, useRepairKit):
        self.setUseRepairKit(useRepairKit)
        self.d_setUseRepairKit(useRepairKit)

    def _getChatSender(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return None, 0

        teamId = self.getAvatarTeam(avatar.doId)
        if not teamId:
            self.notify.debug('Avatar %d tried to send siege chat without a siege team!' % avatar.doId)
            return None, 0

        return avatar, teamId

    def sendChat(self, message, chatFlags, DISLid):
        avatar, teamId = self._getChatSender()
        message = ChatFilter.cleanMessage(message)
        if not avatar or not message:
            return

        chatFlags = ChatFilter.cleanChatFlags(chatFlags)

        for avatarId in self.getTeamAvatars(teamId):
            self.d_recvChat(avatarId, avatar.doId, message, chatFlags, avatar.getDISLid(), avatar.getName())

    def sendWLChat(self, message, chatFlags, DISLid):
        avatar, teamId = self._getChatSender()
        message = ChatFilter.cleanMessage(message)
        if not avatar or not message:
            return

        message = ChatFilter.filterWhiteList(message)
        chatFlags = ChatFilter.cleanChatFlags(chatFlags)

        for avatarId in self.getTeamAvatars(teamId):
            self.d_recvWLChat(avatarId, avatar.doId, message, chatFlags, avatar.getDISLid(), avatar.getName())

    def sendSC(self, msgIndex):
        avatar, teamId = self._getChatSender()
        if not avatar or not ChatFilter.isValidSpeedChat(msgIndex):
            return

        for avatarId in self.getTeamAvatars(teamId):
            self.d_recvSpeedChat(avatarId, avatar.doId, msgIndex, avatar.getName())

    def d_recvChat(self, toAvatarId, avatarId, message, chatFlags, DISLid, name):
        self.sendUpdateToAvatarId(toAvatarId, 'recvChat', [avatarId, message, chatFlags, DISLid, name])

    def d_recvWLChat(self, toAvatarId, avatarId, message, chatFlags, DISLid, name):
        self.sendUpdateToAvatarId(toAvatarId, 'recvWLChat', [avatarId, message, chatFlags, DISLid, name])

    def d_recvSpeedChat(self, toAvatarId, avatarId, msgIndex, name):
        self.sendUpdateToAvatarId(toAvatarId, 'recvSpeedChat', [avatarId, msgIndex, name])

    def getOtherTeam(self, teamId):
        if teamId == self.TEAM_FRENCH:
            return self.TEAM_SPANISH

        return self.TEAM_FRENCH

    def getTeamShips(self, teamId):
        ships = []
        for shipId in self._teamShips.get(teamId, ()):
            ship = self.air.doId2do.get(shipId)
            if ship:
                ships.append(ship)

        return ships

    def getShipTeam(self, shipId):
        for teamId in self.TeamIds:
            if shipId in self._teamShips[teamId]:
                return teamId

        return 0

    def getTeamAvatars(self, teamId):
        return [avatarId for avatarId, avatarTeam in self._avatar2team.items() if avatarTeam == teamId]

    def getAvatarTeam(self, avatarId):
        return self._avatar2team.get(avatarId, 0)

    def getTeamBalanceValue(self, teamId):
        value = 0
        for ship in self.getTeamShips(teamId):
            value += PVPGlobals.TeamBalanceValues.Ships.get(ship.getShipClass(),
                PVPGlobals.TeamBalanceValues.Player)

        return value

    def teamIsJoinable(self, teamId):
        if not self._wantTeamBalance:
            return True

        return self._teamsJoinable.get(teamId, True)

    def getJoinDenialCode(self, teamId):
        # returns the dinghy denyAccess code for a team that cannot be joined
        if teamId not in self.TeamIds:
            return PiratesGlobals.PrivateerBothTeamFull

        if self.teamIsJoinable(teamId):
            return None

        if self.teamIsJoinable(self.getOtherTeam(teamId)):
            return PiratesGlobals.PrivateerSingleTeamFull

        return PiratesGlobals.PrivateerBothTeamFull

    def addShipToTeam(self, ship, teamId):
        if teamId not in self.TeamIds:
            self.notify.warning('Cannot add ship %d to invalid siege team %s!' % (ship.doId, teamId))
            return False

        oldTeam = self.getShipTeam(ship.doId)
        if oldTeam == teamId:
            return True

        if oldTeam:
            self._teamShips[oldTeam].discard(ship.doId)
        else:
            self.accept('distObjDelete-%d' % ship.doId, self._handleShipDeleted, extraArgs=[ship.doId])

        self._teamShips[teamId].add(ship.doId)
        ship.b_setSiegeTeam(teamId)
        self.notify.debug('Ship %d joined siege team %d' % (ship.doId, teamId))

        if self._useRepairSpots:
            self.createShipRepairSpots(ship)

        self._updateShipCrew(ship, teamId)
        self.updateTeamsJoinable()
        return True

    def removeShipFromTeam(self, ship):
        self._removeShip(ship.doId)
        if ship.getSiegeTeam():
            ship.b_setSiegeTeam(0)

        self.deleteShipRepairSpots(ship)
        for avatarId in list(ship.getCrew()):
            if self._avatar2team.get(avatarId):
                avatar = self.air.doId2do.get(avatarId)
                if avatar:
                    self.removeAvatarFromTeam(avatar)

        self.updateTeamsJoinable()

    def createShipRepairSpots(self, ship):
        if hasattr(ship, 'createRepairSpots') and not getattr(ship, 'repairSpots', None):
            ship.createRepairSpots()

    def deleteShipRepairSpots(self, ship):
        if hasattr(ship, 'deleteRepairSpots'):
            ship.deleteRepairSpots()

    def _removeShip(self, shipId):
        teamId = self.getShipTeam(shipId)
        if not teamId:
            return

        self._teamShips[teamId].discard(shipId)
        self._sinkStreaks.pop(shipId, None)
        self.ignore('distObjDelete-%d' % shipId)

        # the pirates who sailed this ship have now lost their privateer crew...
        for avatarId, avatarShipId in list(self._avatar2ship.items()):
            if avatarShipId != shipId:
                continue

            avatar = self.air.doId2do.get(avatarId)
            if avatar and avatar.doId not in self._getTeamCrewIds():
                self.removeAvatarFromTeam(avatar)

    def _handleShipDeleted(self, shipId):
        self._removeShip(shipId)
        self.updateTeamsJoinable()

    def addAvatarToTeam(self, avatar, teamId):
        if teamId not in self.TeamIds:
            return

        if avatar.doId not in self._avatar2team:
            self.accept(self.air.getAvatarExitEvent(avatar.doId), self._handleAvatarExit, extraArgs=[avatar.doId])

        self._avatar2team[avatar.doId] = teamId
        if avatar.getSiegeTeam() != teamId:
            avatar.b_setSiegeTeam(teamId)

    def removeAvatarFromTeam(self, avatar):
        self._avatar2ship.pop(avatar.doId, None)
        self.removeInvulnerability(avatar)
        if avatar.doId not in self._avatar2team:
            return

        del self._avatar2team[avatar.doId]
        self.ignore(self.air.getAvatarExitEvent(avatar.doId))
        if avatar.getSiegeTeam():
            avatar.b_setSiegeTeam(0)

    def _handleAvatarExit(self, avatarId):
        self._avatar2team.pop(avatarId, None)
        self._avatar2ship.pop(avatarId, None)
        self._clearInvulnerabilityTasks(avatarId)
        self._invulnerableAvatars.pop(avatarId, None)
        self.ignore(self.air.getAvatarExitEvent(avatarId))

    def _updateShipCrew(self, ship, teamId):
        for avatarId in ship.getCrew():
            avatar = self.air.doId2do.get(avatarId)
            if avatar:
                self.addAvatarToTeam(avatar, teamId)
                self._avatar2ship[avatar.doId] = ship.doId

    def _getTeamCrewIds(self):
        crewAvatarIds = set()
        for teamId in self.TeamIds:
            for ship in self.getTeamShips(teamId):
                crewAvatarIds.update(ship.getCrew())

        return crewAvatarIds

    def isAvatarStillPrivateer(self, avatar):
        # privateers keep their siege team ashore (see TeamUtils.damageAllowed) until
        # their ship leaves the team or they join the crew of another ship...
        teamId = self._avatar2team.get(avatar.doId)
        shipId = self._avatar2ship.get(avatar.doId)
        if not teamId or not shipId:
            return False

        if self.getShipTeam(shipId) != teamId or not self.air.doId2do.get(shipId):
            return False

        crewShipId = avatar.getCrewShipId()
        if crewShipId and crewShipId != shipId:
            return False

        return True

    def updateTeamsJoinable(self):
        maxShips = PVPGlobals.MaxPrivateerShipsPerTeam.getValue()
        changed = False
        for teamId in self.TeamIds:
            joinable = len(self._teamShips[teamId]) < maxShips
            if joinable:
                difference = self.getTeamBalanceValue(teamId) - self.getTeamBalanceValue(self.getOtherTeam(teamId))
                joinable = difference <= self._teamBalanceMargin

            if self._teamsJoinable.get(teamId) != joinable:
                changed = True

            self._teamsJoinable[teamId] = joinable

        if changed:
            self.d_setTeamsJoinable(self.getTeamsJoinable())

    def _updateTeamsTask(self, task):
        # keep the siege team of the avatars in sync with the crew of the
        # privateer ships they are currently sailing on...
        crewAvatarIds = set()
        for teamId in self.TeamIds:
            for ship in self.getTeamShips(teamId):
                self._updateShipCrew(ship, teamId)
                crewAvatarIds.update(ship.getCrew())

        for avatarId in list(self._avatar2team.keys()):
            if avatarId in crewAvatarIds:
                continue

            avatar = self.air.doId2do.get(avatarId)
            if not avatar:
                self._handleAvatarExit(avatarId)
            elif not self.isAvatarStillPrivateer(avatar):
                self.removeAvatarFromTeam(avatar)

        self.updateTeamsJoinable()

        if self._useIslandRegen:
            self._regenElapsed += self.TEAM_UPDATE_PERIOD
            regenPeriod = PVPGlobals.ShipRegenPeriod.getValue()
            if self._regenElapsed >= regenPeriod:
                self._regenElapsed = 0.0
                self.applyIslandRegen(regenPeriod)

        return Task.again

    def getTeamIslands(self):
        if not self._teamIslands:
            from pirates.world.DistributedIslandAI import DistributedIslandAI
            self._teamIslands = [obj for obj in list(self.air.doId2do.values())
                if isinstance(obj, DistributedIslandAI) and obj.getSiegeTeam()]

        return self._teamIslands

    def isShipInIslandRegenSphere(self, ship, island):
        x, y, z, h = island.getIslandTransform()
        centerX, centerY = island.getZoneSphereCenter()
        radius = island.getZoneSphereSize()[0] * PVPGlobals.ShipRegenRadiusScale.getValue()

        # the sphere center is relative to the island, so rotate it into world space:
        rad = math.radians(h)
        worldX = x + (centerX * math.cos(rad)) - (centerY * math.sin(rad))
        worldY = y + (centerX * math.sin(rad)) + (centerY * math.cos(rad))

        pos = ship.getPos()
        return math.hypot(pos[0] - worldX, pos[1] - worldY) <= radius

    def applyIslandRegen(self, elapsed):
        hpRegen = int(PVPGlobals.ShipRegenHps.getValue() * elapsed)
        spRegen = int(PVPGlobals.ShipRegenSps.getValue() * elapsed)
        for teamId in self.TeamIds:
            islands = [island for island in self.getTeamIslands() if island.getSiegeTeam() == teamId]
            if not islands:
                continue

            for ship in self.getTeamShips(teamId):
                if ship.getHp() <= 0:
                    continue

                for island in islands:
                    if self.isShipInIslandRegenSphere(ship, island):
                        if ship.getHp() < ship.getMaxHp():
                            ship.b_setHp(min(ship.getHp() + hpRegen, ship.getMaxHp()))

                        if ship.getSp() < ship.getMaxSp():
                            ship.b_setSp(min(ship.getSp() + spRegen, ship.getMaxSp()))

                        break

    def useShipRepairKit(self, avatar, ship):
        # the client only offers the kit to privateers (see LocalPirateGameFSM._handleUseRepairKit)
        if not self._pvpEnabled or not self._useRepairKit:
            return False

        teamId = self.getAvatarTeam(avatar.doId)
        if not teamId or not ship or self.getShipTeam(ship.doId) != teamId:
            return False

        if not ship.hasCrewMember(avatar.doId) or ship.getHp() <= 0:
            return False

        if ship.getHp() >= ship.getMaxHp() and ship.getSp() >= ship.getMaxSp():
            return False

        inventory = avatar.getInventory()
        if not inventory:
            return False

        quantity = inventory.getStackQuantity(InventoryType.ShipRepairKit)
        if quantity <= 0:
            return False

        inventory.b_setStackQuantity(InventoryType.ShipRepairKit, quantity - 1)
        ship.b_setHp(min(ship.getMaxHp(), ship.getHp() + PVPGlobals.RepairKitHp.getValue()))
        ship.b_setSp(min(ship.getMaxSp(), ship.getSp() + PVPGlobals.RepairKitSp.getValue()))
        return True

    def handleAvatarDefeated(self, avatar):
        # privateers are respawned in place rather than sent to jail
        # (see DistributedMainWorld._startPvpRespawn)...
        if not self.getAvatarTeam(avatar.doId):
            return False

        self._clearInvulnerabilityTasks(avatar.doId)
        taskMgr.doMethodLater(PVPGlobals.MainWorldAvRespawnDelay, self._respawnAvatar,
            self.uniqueName('respawn-%d' % avatar.doId), extraArgs=[avatar.doId])

        return True

    def _respawnAvatar(self, avatarId):
        avatar = self.air.doId2do.get(avatarId)
        if not avatar:
            return Task.done

        avatar.b_setHp(avatar.getMaxHp())
        avatar.b_setMojo(avatar.getMaxMojo())
        self.addInvulnerability(avatar)
        return Task.done

    def addInvulnerability(self, avatar):
        duration = PVPGlobals.MainWorldInvulnerabilityDuration.getValue()
        if duration <= 0:
            return

        self.removeInvulnerability(avatar)

        # the invulnerability is cut off once the avatar leaves
        # the area of the island it respawned on...
        island = avatar.getParentObj()
        if not hasattr(island, 'getZoneSphereSize'):
            island = None

        self._invulnerableAvatars[avatar.doId] = island
        avatar.addSkillEffect(WeaponGlobals.C_SPAWN, duration, avatar.doId)
        taskMgr.doMethodLater(duration, self._invulnerabilityExpired,
            self.uniqueName('invulnerability-%d' % avatar.doId), extraArgs=[avatar.doId])

        if PVPGlobals.MainWorldInvulnerabilityWantCutoff.getValue():
            taskMgr.doMethodLater(self.INVULNERABILITY_CHECK_PERIOD, self._checkInvulnerabilityCutoff,
                self.uniqueName('invulnerabilityCutoff-%d' % avatar.doId), extraArgs=[avatar.doId],
                appendTask=True)

    def removeInvulnerability(self, avatar):
        self._clearInvulnerabilityTasks(avatar.doId)
        if avatar.doId not in self._invulnerableAvatars:
            return

        del self._invulnerableAvatars[avatar.doId]
        avatar.removeSkillEffect(WeaponGlobals.C_SPAWN)

    def isAvatarInvulnerable(self, avatarId):
        return avatarId in self._invulnerableAvatars

    def _clearInvulnerabilityTasks(self, avatarId):
        taskMgr.remove(self.uniqueName('respawn-%d' % avatarId))
        taskMgr.remove(self.uniqueName('invulnerability-%d' % avatarId))
        taskMgr.remove(self.uniqueName('invulnerabilityCutoff-%d' % avatarId))

    def _invulnerabilityExpired(self, avatarId):
        avatar = self.air.doId2do.get(avatarId)
        if avatar:
            self.removeInvulnerability(avatar)
        else:
            self._clearInvulnerabilityTasks(avatarId)
            self._invulnerableAvatars.pop(avatarId, None)

        return Task.done

    def isAvatarInCutoffSphere(self, avatar, island):
        if not island or avatar.getParentObj() is not island:
            return False

        # the avatar's position is relative to the island, as is it's zone sphere...
        centerX, centerY = island.getZoneSphereCenter()
        radius = island.getZoneSphereSize()[0] * PVPGlobals.MainWorldInvulnerabilityCutoffRadiusScale.getValue()
        pos = avatar.getPos()
        return math.hypot(pos[0] - centerX, pos[1] - centerY) <= radius

    def _checkInvulnerabilityCutoff(self, avatarId, task):
        avatar = self.air.doId2do.get(avatarId)
        if not avatar or avatarId not in self._invulnerableAvatars:
            return Task.done

        if not self.isAvatarInCutoffSphere(avatar, self._invulnerableAvatars[avatarId]):
            self.removeInvulnerability(avatar)
            return Task.done

        return Task.again

    def getTeamScore(self, teamId):
        return self._teamScores.get(teamId, 0)

    def getShipSinkStreak(self, shipId):
        return self._sinkStreaks.get(shipId, 0)

    def handleShipSunk(self, sunkShip, attackerShip=None, assistShip=None):
        sunkTeam = sunkShip.getSiegeTeam()
        if not sunkTeam:
            return

        self._sinkStreaks.pop(sunkShip.doId, None)
        if not attackerShip or not attackerShip.getSiegeTeam():
            return

        team = attackerShip.getSiegeTeam()
        if team == sunkTeam:
            self.notify.debug('Ship %d sunk friendly ship %d, ignoring' % (attackerShip.doId, sunkShip.doId))
            return

        self.applySinkHpBonus(sunkShip, sunkTeam)

        worth = PVPGlobals.RenownWorthValues.get(sunkShip.getShipClass(), 0)
        self._teamScores[team] = self._teamScores.get(team, 0) + worth
        self.awardInfamy(attackerShip, worth)

        if assistShip and assistShip.getSiegeTeam() == team and assistShip.doId != attackerShip.doId:
            self.awardInfamy(assistShip, worth // 2)
            if self.announcer:
                self.announcer.d_announceSinkWithAssist(team, attackerShip.getName(), team, assistShip.getName(),
                    sunkTeam, sunkShip.getName())
        elif self.announcer:
            self.announcer.d_announceSink(team, attackerShip.getName(), sunkTeam, sunkShip.getName())

        streak = self._sinkStreaks.get(attackerShip.doId, 0) + 1
        self._sinkStreaks[attackerShip.doId] = streak
        streakPeriod = PVPGlobals.SinkStreakPeriod.getValue()
        if streakPeriod and streak % streakPeriod == 0 and self.announcer:
            self.announcer.d_announceSinkStreak(team, attackerShip.getName(), streak)

    def applySinkHpBonus(self, sunkShip, sunkTeam):
        # every enemy ship that helped sink the ship receives a health boost, which depends
        # on the amount of damage it did (see PLocalizer.ShipPVPHint11 and ShipPVPHint12)...
        bonusPercent = PVPGlobals.SinkHpBonusPercent.getValue()
        attackerDamage = getattr(sunkShip, 'attackerDamage', None) or {}
        for shipId, damage in list(attackerDamage.items()):
            ship = self.air.doId2do.get(shipId)
            if not ship or not ship.getSiegeTeam() or ship.getSiegeTeam() == sunkTeam:
                continue

            if ship.getHp() <= 0 or ship.getHp() >= ship.getMaxHp():
                continue

            bonus = int(max(0, damage) * bonusPercent)
            if bonus:
                ship.b_setHp(min(ship.getMaxHp(), ship.getHp() + bonus))

    def awardInfamy(self, ship, amount):
        if amount <= 0:
            return

        for avatarId in ship.getCrew():
            avatar = self.air.doId2do.get(avatarId)
            if not avatar:
                continue

            inventory = avatar.getInventory()
            if not inventory:
                continue

            for stackType in (InventoryType.PVPTotalInfamySea, InventoryType.PVPCurrentInfamy):
                inventory.b_setStackQuantity(stackType, inventory.getStackQuantity(stackType) + amount)
