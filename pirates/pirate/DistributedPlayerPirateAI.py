from panda3d.core import *

from direct.directnotify import DirectNotifyGlobal

from otp.ai.MagicWordGlobal import *
from otp.avatar.DistributedPlayerAI import DistributedPlayerAI

from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.pirate.HumanDNAAI import HumanDNAAI
from pirates.quest.DistributedQuestAvatarAI import DistributedQuestAvatarAI
from pirates.tutorial import TutorialGlobals
from pirates.pirate.PlayerPirateGameFSMAI import PlayerPirateGameFSMAI
from pirates.quest.DistributedQuestAvatar import DistributedQuestAvatar
from pirates.quest.QuestStatus import QuestStatus
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.pirate import AvatarTypes
from pirates.quest.QuestConstants import LocationIds
from pirates.quest import QuestDB
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType
from pirates.battle import WeaponGlobals
from pirates.reputation import ReputationGlobals


class DistributedPlayerPirateAI(DistributedPlayerAI, DistributedBattleAvatarAI, HumanDNAAI, DistributedQuestAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerPirateAI')

    def __init__(self, air):
        DistributedPlayerAI.__init__(self, air)
        DistributedBattleAvatarAI.__init__(self, air)
        HumanDNAAI.__init__(self)
        DistributedQuestAvatarAI.__init__(self, air)

        self.gameFSM = PlayerPirateGameFSMAI(self.air, self)
        self.questStatus = None
        self.isNpc = False

        self.avatarType = AvatarTypes.Pirate
        self.inventoryId = 0
        self.guildId = 0
        self.guildName = 'Null'
        self.teleportFlags = PiratesGlobals.TFInInitTeleport
        self.jailCellIndex = 0
        self.returnLocation = ''
        self.currentIsland = ''
        self.emoteId = 0
        self.zombie = 0
        self.forcedZombie = 0
        self.gmNameTagAllowed = False
        self.stickyTargets = []
        self.defaultShard = 0
        self.defaultZone = 0
        self.tempDoubleXPReward = 0
        self.toonUpTask = None
        self.constructedShipDoId = 0
        self.activeShipId = 0
        self.crewShipId = 0
        self.canControlInterests = True

    def announceGenerate(self):
        DistributedPlayerAI.announceGenerate(self)
        DistributedBattleAvatarAI.announceGenerate(self)

    def generate(self):
        DistributedPlayerAI.generate(self)
        DistributedBattleAvatarAI.generate(self)

        self.accept('HolidayStarted', self.processHolidayStart)
        self.accept('HolidayEnded', self.processHolidayEnd)
        self.accept('todHalloweenStateChange', self.attemptToSetCursedZombie)

        taskMgr.doMethodLater(0.05, self.__processGroggy, self.uniqueName('process-groggy'))
        taskMgr.doMethodLater(10, self.__processDoubleXP, self.uniqueName('process-double-xp'))

    def __processGroggy(self, task):
        inventory = self.getInventory()
        if not inventory:
            return task.again

        vitaeLevel = inventory.getVitaeLevel()
        if vitaeLevel:
            # increment down the Vitae
            amount = max(inventory.getVitaeLeft() - 1, 0)
            inventory.setVitaeLeft(amount)

            # check if the groggy state has expired
            if amount <= 0:
                inventory.setVitaeLevel(0)

        return task.again

    def __processDoubleXP(self, task):
        if not self.hasTempDoubleXPReward():
            return task.again

        self.tempDoubleXPReward -= 10
        if self.tempDoubleXPReward < 0:
            self.b_setTempDoubleXPReward(0)

        self.b_setTempDoubleXPReward(self.tempDoubleXPReward)

        return task.again

    def processHolidayStart(self, holidayId):
        self.attemptToSetCursedZombie()

    def processHolidayEnd(self, holidayId):
        self.attemptToSetCursedZombie()

    def setLocation(self, parentId, zoneId):
        from pirates.world.DistributedIslandAI import DistributedIslandAI

        DistributedPlayerAI.setLocation(self, parentId, zoneId)
        DistributedBattleAvatarAI.setLocation(self, parentId, zoneId)

        parentObj = self.getParentObj()
        if parentObj:
            if isinstance(parentObj, DistributedIslandAI):
                if self.currentIsland:
                    validReturns = [
                        LocationIds.PORT_ROYAL_ISLAND,
                        LocationIds.TORTUGA_ISLAND,
                        LocationIds.DEL_FUEGO_PORT,
                        LocationIds.CUBA_ISLAND
                    ]

                    if self.currentIsland in validReturns:
                        self.b_setReturnLocation(self.currentIsland)

                self.b_setCurrentIsland(parentObj.getUniqueId())
            else:
                if self.currentIsland:
                    self.b_setCurrentIsland('')

            self.attemptToSetCursedZombie()
            if self.canControlInterests:
                self.air.worldGridManager.handleLocationChanged(parentObj, self, zoneId)

    def getInventory(self):
        return self.air.inventoryManager.getInventory(self.doId)

    def setCurrentTarget(self, currentTargetDoId):
        if self.currentTarget is not None:
            if not currentTargetDoId:
                self.startToonUp()
        else:
            self.stopToonUp()

        DistributedBattleAvatarAI.setCurrentTarget(self, currentTargetDoId)

    def d_setFounder(self, founder):
        self.sendUpdate('setFounder', [founder])

    def setInventoryId(self, inventoryId):
        self.inventoryId = inventoryId

        if not self.questStatus:
            self.questStatus = QuestStatus(self)

    def d_setInventoryId(self, inventoryId):
        self.sendUpdate('setInventoryId', [inventoryId])

    def b_setInventoryId(self, inventoryId):
        self.setInventoryId(inventoryId)
        self.d_setInventoryId(inventoryId)

    def getInventoryId(self):
        return self.inventoryId

    def setGuildId(self, guildId):
        self.guildId = guildId

    def d_setGuildId(self, guildId):
        self.sendUpdate('setGuildId', [guildId])

    def b_setGuildId(self, guildId):
        self.setGuildId(guildId)
        self.d_setGuildId(guildId)

    def getGuildId(self):
        return self.guildId

    def setGuildName(self, guildName):
        self.guildName = guildName

    def d_setGuildName(self, guildName):
        self.sendUpdate('setGuildName', [guildName])

    def b_setGuildName(self, guildName):
        self.setGuildName(guildName)
        self.d_setGuildName(guildName)

    def getGuildName(self):
        return self.guildName

    def setTeleportFlags(self, teleportFlags):
        self.teleportFlags = BitMask32(teleportFlags)

    def d_setTeleportFlags(self, teleportFlags):
        self.sendUpdate('setTeleportFlags', [PiratesGlobals.encodeTeleportFlag(teleportFlags)])

    def b_setTeleportFlag(self, teleportFlags):
        self.setTeleportFlags(teleportFlags)
        self.d_setTeleportFlags(teleportFlags)

    def getTeleportFlags(self):
        return self.teleportFlags

    def testTeleportFlag(self, flag):
        return not (self.teleportFlags & flag).isZero()

    def d_relayTeleportLoc(self, shardId, zoneId, teleportMgrDoId):
        self.sendUpdateToAvatarId(self.doId, 'relayTeleportLoc', [shardId, zoneId,
            teleportMgrDoId])

    def d_forceTeleportStart(self, instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone):
        self.sendUpdateToAvatarId(self.doId, 'forceTeleportStart', [instanceName, tzDoId, thDoId,
            worldGridDoId, tzParent, tzZone])

    def giveDefaultQuest(self):
        if config.GetBool('want-alpha-blockers', False):
            # Don't give a default quest if alpha blockers are enabled
            return

        inventory = self.getInventory()
        if not inventory:
            self.notify.warning('Failed to give default quest for avatar: %d, '
                'no inventory was found!' % self.doId)

            return

        questHistory = self.getQuestHistory()
        questDNA = QuestDB.QuestDict['c2.4recoverOrders']
        if questDNA.getQuestInt() in questHistory:
            self.notify.warning('Failed to give default quest %s for avatar: %d, '
                'avatar already completed quest!' % (questDNA.getQuestId(), self.doId))

            return

        self.air.questMgr.createQuest(self, questDNA.getQuestId())

    def setReturnLocation(self, returnLocation):
        self.returnLocation = returnLocation

    def d_setReturnLocation(self, returnLocation):
        self.sendUpdate('setReturnLocation', [returnLocation])

    def b_setReturnLocation(self, returnLocation):
        self.setReturnLocation(returnLocation)
        self.d_setReturnLocation(returnLocation)

    def getReturnLocation(self):
        return self.returnLocation

    def setJailCellIndex(self, jailCellIndex):
        self.jailCellIndex = jailCellIndex

    def d_setJailCellIndex(self, jailCellIndex):
        self.sendUpdate('setJailCellIndex', [jailCellIndex])

    def b_setJailCellIndex(self, jailCellIndex):
        self.setJailCellIndex(jailCellIndex)
        self.d_setJailCellIndex(jailCellIndex)

    def getJailCellIndex(self):
        return self.jailCellIndex

    def requestCurrentIsland(self, locationDoId):
        pass

    def setCurrentIsland(self, currentIsland):
        self.currentIsland = currentIsland

    def d_setCurrentIsland(self, currentIsland):
        self.sendUpdateToAvatarId(self.doId, 'setCurrentIsland', [currentIsland])

    def b_setCurrentIsland(self, currentIsland):
        self.setCurrentIsland(currentIsland)
        self.d_setCurrentIsland(currentIsland)

    def getCurrentIsland(self):
        return self.currentIsland

    def hasEmote(self, emoteId):
        emote = PLocalizer.emotes.get(emoteId)
        if not emote:
            emote = PLocalizer.nonMenuEmoteAnimations.get(emoteId)

        if not emote:
            emote = PLocalizer.receiveWeaponEmotes.get(emoteId)

        return emote is not None

    def setEmote(self, emoteId):
        if not self.hasEmote(emoteId):
            self.notify.debug('Cannot set emote for %d, invalid emoteId specified!' % (
                self.doId))

            return

        self.emoteId = emoteId
        self.sendUpdate('playEmote', [emoteId])

    def getEmote(self):
        return self.emoteId

    def requestCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        if not self.weapon:
            return

        self.weapon.d_setMovie(WeaponGlobals.WEAPON_MOVIE_START if isWeaponDrawn else \
            WeaponGlobals.WEAPON_MOVIE_STOP, self.doId)

        self.b_setCurrentWeapon(currentWeaponId, isWeaponDrawn)

    def requestCurrentAmmo(self, skillId):
        pass

    def requestUseSkill(self, skillId, index):
        pass

    def requestDeployShip(self, shipId):
        pass

    def requestReturnShip(self, shipId):
        pass

    def setCurseStatus(self, curseStat):
        pass

    def giveClothingMessage(self, clothingId, colorId):
        self.sendUpdate('sendClothingMessage', [clothingId, colorId])

    def d_sendLootMessage(self, lootId):
        self.sendUpdate('sendLootMessage', [lootId])

    def giveCardMessage(self, cardId):
        self.sendUpdate('sendCardMessage', [cardId])

    def giveWeaponMessage(self, weapon):
        self.sendUpdate('sendWeaponMessage', [weapon])

    def giveJewelryMessage(self, jewelryUID):
        self.sendUpdate('sendJewelryMessage', [jewelryUID])

    def giveTattooMessage(self, tattooUID):
        self.sendUpdate('sendTattooMessage', [tattooUID])

    def d_sendReputationMessage(self, targetId, categories, reputationList, basicPenalty, crewBonus, doubleXPBonus, holidayBonus):
        self.sendUpdate('sendReputationMessage', [targetId, categories, reputationList, basicPenalty,
            crewBonus, doubleXPBonus, holidayBonus])

    def spendSkillPoint(self, skillId):
        inventory = self.getInventory()
        if not inventory:
            self.notify.debug('Cannot spend skill point %d for avatar %d, '
                'no inventory present' % (skillId, self.doId))

            return

        def updateStack(stackType):
            unspentStackQuantity = inventory.getStackQuantity(stackType)
            skillQuantity = inventory.getStackQuantity(skillId)

            # check to see if the player has any skill points...
            if not unspentStackQuantity:
                self.notify.debug('Cannot update stack %d, player has no skill points; unspentStackQuantity=%d!' % (
                    stackType, unspentStackQuantity))

                return

            # check to see if the player can purchase anymore stacks
            # for this type...
            if skillQuantity >= 6:
                self.notify.debug('Cannot update stack %d, stack limit reached; skillQuantity=%d, skillLimit=5' % (
                    stackType, skillQuantity))

                return

            # update the player's skill quantity and their skill
            # points quantity stack...
            inventory.b_setStackQuantity(skillId, skillQuantity + 1)
            inventory.b_setStackQuantity(stackType, unspentStackQuantity - 1)
            self.d_spentSkillPoint(skillId)

        if skillId >= InventoryType.begin_WeaponSkillMelee and skillId < InventoryType.end_WeaponSkillMelee:
            updateStack(InventoryType.UnspentMelee)
        elif skillId >= InventoryType.begin_WeaponSkillCutlass and skillId < InventoryType.end_WeaponSkillCutlass:
            updateStack(InventoryType.UnspentCutlass)
        elif skillId >= InventoryType.begin_WeaponSkillPistol and skillId < InventoryType.end_WeaponSkillPistol:
            updateStack(InventoryType.UnspentPistol)
        elif skillId >= InventoryType.begin_WeaponSkillMusket and skillId < InventoryType.end_WeaponSkillMusket:
            updateStack(InventoryType.UnspentMusket)
        elif skillId >= InventoryType.begin_WeaponSkillDagger and skillId < InventoryType.end_WeaponSkillDagger:
            updateStack(InventoryType.UnspentDagger)
        elif skillId >= InventoryType.begin_WeaponSkillGrenade and skillId < InventoryType.end_WeaponSkillGrenade:
            updateStack(InventoryType.UnspentGrenade)
        elif skillId >= InventoryType.begin_SkillSailing and skillId < InventoryType.end_SkillSailing:
            updateStack(InventoryType.UnspentSailing)
        elif skillId >= InventoryType.begin_WeaponSkillCannon and skillId < InventoryType.end_WeaponSkillCannon:
            updateStack(InventoryType.UnspentCannon)
        elif skillId >= InventoryType.begin_WeaponSkillDoll and skillId < InventoryType.end_WeaponSkillDoll:
            updateStack(InventoryType.UnspentDoll)
        elif skillId >= InventoryType.begin_WeaponSkillWand and skillId < InventoryType.end_WeaponSkillWand:
            updateStack(InventoryType.UnspentWand)
        else:
            self.notify.debug('Cannot spend skill point for skill %d,'
                'has no unspent category!' % skillId)

            return

    def resetSkillPoints(self, skillId):
        self.d_spentSkillPoint(skillId)

    def d_spentSkillPoint(self, category):
        self.sendUpdateToAvatarId(self.doId, 'spentSkillPoint', [category])

    def getHighestTonic(self):
        inventory = simbase.air.inventoryManager.getInventory(self.doId)

        if not inventory:
            self.notify.warning('Failed to choose best tonic for %d; Avatar does not have an inventory' % self.doId)
            return 0

        detected = 0
        for tonicId in range(InventoryType.begin_Consumables, InventoryType.end_Consumables, -1):
            amount = inventory.getStackQuantity(tonicId)
            if amount > 0:
                detected = tonicId
                break

        return detected

    def getBestTonic(self):
        inventory = simbase.air.inventoryManager.getInventory(self.doId)

        if not inventory:
            self.notify.warning('Failed to choose best tonic for %d; Avatar does not have an inventory' % self.doId)
            return 0

        tonics = inventory.getTonics()
        idealAmount = max(0, self.getMaxHp() * 0.8 - self.getHp()[0])
        bestTonicId = InventoryType.Potion1
        for tonicId, count in sorted(tonics.iteritems()):
            if count:
                bestTonicId = tonicId
                if WeaponGlobals.getAttackSelfHP(tonicId) > idealAmount:
                    break

        return bestTonicId

    def useTonic(self, tonicId):
        inventory = simbase.air.inventoryManager.getInventory(self.doId)

        if not inventory:
            self.notify.warning('Failed to choose best tonic for %d; Avatar does not have an inventory' % self.doId)
            return

        amount = inventory.getStackQuantity(tonicId)

        if amount <= 0:
            # This should never happen. Log it
            self.air.logPotentialHacker(
                message='Attempted to use a tonic they do not have',
                tonicId=tonicId)

            return

        # Calculate max potential values for restoring
        healedHp = min(WeaponGlobals.getAttackSelfHP(tonicId) + self.getHp()[0], self.getMaxHp())
        restoredMojo = min(WeaponGlobals.getAttackSelfMojo(tonicId) + self.getMojo(), self.getMaxMojo())
        restoredPower = min(WeaponGlobals.getAttackSelfPower(tonicId) + self.getPower(), self.getMaxPower())

        # Apply values
        self.b_setHp(healedHp)
        self.b_setMojo(restoredMojo)
        self.b_setPower(restoredPower)

        inventory.b_setStackQuantity(tonicId, inventory.getStackQuantity(tonicId) - 1)

    def useBestTonic(self):
        tonicId = self.getBestTonic()
        if tonicId == 0:
            self.notify.warning('Failed to determine the best tonic for %d' % self.doId)
            return

        self.useTonic(tonicId)

    def flagFirstDeath(self):
        pass

    def d_levelUpMsg(self, category, level, messageId):
        self.sendUpdate('levelUpMsg', [category, level, messageId])

    def setStickyTargets(self, stickyTargets):
        self.stickyTargets = stickyTargets

    def d_setStickyTargets(self, stickyTargets):
        self.sendUpdate('setStickyTargets', [stickyTargets])

    def b_setStickyTargets(self, stickyTargets):
        self.setStickyTargets(stickyTargets)
        self.d_setStickyTargets(stickyTargets)

    def getStickyTargets(self):
        return self.stickyTargets

    def addStickyTarget(self, targetDoId):
        if targetDoId in self.stickyTargets:
            return

        self.stickyTargets.append(targetDoId)
        self.d_setStickyTargets(self.stickyTargets)

    def removeStickyTarget(self, targetDoId):
        if targetDoId not in self.stickyTargets:
            return

        self.stickyTargets.remove(targetDoId)
        self.d_setStickyTargets(self.stickyTargets)

    def getHostileStickyTargets(self):
        hostile = []
        friendlyTeams = [
            PiratesGlobals.VILLAGER_TEAM,
            PiratesGlobals.PLAYER_TEAM
        ]

        for targetId in self.stickyTargets:
            target = self.air.doId2do.get(targetId)

            if not target:
                continue

            if target.getTeam() not in friendlyTeams:
                hostile.append(target)

        return hostile

    def getFriendlyStickyTargets(self):
        friendly = []
        friendlyTeams = [
            PiratesGlobals.VILLAGER_TEAM,
            PiratesGlobals.PLAYER_TEAM
        ]

        for targetId in self.stickyTargets:
            target = self.air.doId2do.get(targetId)

            if not target:
                continue

            if target.getTeam() in friendlyTeams:
                friendly.append(target)

        return friendly

    def hasStickyTarget(self, avId):
        return avId in self.stickyTargets

    def requestRemoveStickyTargets(self, doIdList):
        for targetDoId in doIdList:
            self.removeStickyTarget(targetDoId)

    def setDefaultShard(self, defaultShard):
        self.defaultShard = defaultShard

    def d_setDefaultShard(self, defaultShard):
        self.sendUpdate('setDefaultShard', [defaultShard])

    def b_setDefaultShard(self, defaultShard):
        self.setDefaultShard(defaultShard)
        self.d_setDefaultShard(defaultShard)

    def getDefaultShard(self):
        return self.defaultShard

    def setDefaultZone(self, defaultZone):
        self.defaultZone = defaultZone

    def d_setDefaultZone(self, defaultZone):
        self.sendUpdate('setDefaultZone', [defaultZone])

    def b_setDefaultZone(self, defaultZone):
        self.setDefaultZone(defaultZone)
        self.d_setDefaultZone(defaultZone)

    def getDefaultZone(self):
        return self.defaultZone

    def attemptToSetCursedZombie(self):
        newState = False

        parentObj = self.getParentObj()
        if self.forcedZombie:
            newState = True
        else:
            # Sanity check for weird conditions
            if not self.air:
                self.notify.warning('Failed to process attemptToSetcursedZombie; Air is NoneType')
                return

            # We are not in PVP. Lets check if its a Cursed Moon
            isOutside = not isinstance(parentObj, DistributedGAInteriorAI)
            isHalloween = self.air.timeOfDayMgr.isHalloweenMoon()
            newState = (isOutside and isHalloween and parentObj)

        if newState != self.getZombie():
            self.b_setZombie(bool(newState))

    def setZombie(self, zombie, cursed=False):
        self.zombie = zombie

    def d_setZombie(self, zombie, cursed=False):
        self.sendUpdate('setZombie', [zombie, cursed])

    def b_setZombie(self, zombie, cursed=False):
        self.setZombie(zombie, cursed)
        self.d_setZombie(zombie, cursed)

    def getZombie(self):
        return self.zombie

    def setAllowGMNameTag(self, gmNameTagAllowed):
        self.gmNameTagAllowed = gmNameTagAllowed

    def d_setAllowGMNameTag(self, gmNameTagAllowed):
        self.sendUpdate('setAllowGMNameTag', [gmNameTagAllowed])

    def b_setAllowGMNameTag(self, gmNameTagAllowed):
        self.setAllowGMNameTag(gmNameTagAllowed)
        self.d_setAllowGMNameTag(gmNameTagAllowed)

    def getAllowGMNameTag(self):
        return self.gmNameTagAllowed

    def updateGMNameTag(self, gmNameTagState, gmNameTagColor, gmNameTagString):
        self.gmNameTagState = gmNameTagState
        self.gmNameTagColor = gmNameTagColor
        self.gmNameTagString = gmNameTagString

    def d_updateGMNameTag(self, gmNameTagState, gmNameTagColor, gmNameTagString):
        self.sendUpdate('updateGMNameTag', [gmNameTagState, gmNameTagColor, gmNameTagString])

    def b_updateGMNameTag(self, gmNameTagState, gmNameTagColor, gmNameTagString):
        self.d_updateGMNameTag(gmNameTagState, gmNameTagColor, gmNameTagString)
        self.updateGMNameTag(gmNameTagState, gmNameTagColor, gmNameTagString)

    def setTempDoubleXPReward(self, tempDoubleXPReward):
        self.tempDoubleXPReward = tempDoubleXPReward

    def d_setTempDoubleXPReward(self, tempDoubleXPReward):
        self.sendUpdate('setTempDoubleXPReward', [tempDoubleXPReward])

    def b_setTempDoubleXPReward(self, tempDoubleXPReward):
        self.setTempDoubleXPReward(tempDoubleXPReward)
        self.d_setTempDoubleXPReward(tempDoubleXPReward)

    def getTempDoubleXPReward(self):
        return self.tempDoubleXPReward

    def hasTempDoubleXPReward(self):
        return self.tempDoubleXPReward > 0

    def updateTempDoubleXPReward(self, tempDoubleXPReward):
        self.b_setTempDoubleXPReward(tempDoubleXPReward)

    def startToonUp(self):
        self.toonUpTask = taskMgr.doMethodLater(2.0, self.toonUp, self.taskName('toonUp'))

    def toonUp(self, task):
        if self.getHp()[0] >= self.getMaxHp() and self.getMojo() >= self.getMaxMojo():
            return task.done

        if self.getHp()[0] < self.getMaxHp():
            self.b_setHp(min(self.getMaxHp(), self.getHp()[0] + 10 * self.getLevel() / 1.25))

        if self.getMojo() < self.getMaxMojo():
            self.b_setMojo(min(self.getMaxMojo(), self.getMojo() + 8 * self.getLevel() / 1.35))

        return task.again

    def stopToonUp(self):
        if self.toonUpTask:
            taskMgr.remove(self.toonUpTask)
            self.toonUpTask = None

    def setActiveShipId(self, activeShipId):
        self.activeShipId = activeShipId

    def d_setActiveShipId(self, activeShipId):
        self.sendUpdate('setActiveShipId', [activeShipId])

    def b_setActiveShipId(self, activeShipId):
        self.setActiveShipId(activeShipId)
        self.d_setActiveShipId(activeShipId)

    def getActiveShipId(self):
        return self.activeShipId

    def setCrewShipId(self, crewShipId):
        self.crewShipId = crewShipId

    def d_setCrewShipId(self, crewShipId):
        self.sendUpdate('setCrewShipId', [crewShipId])

    def b_setCrewShipId(self, crewShipId):
        self.setCrewShipId(crewShipId)
        self.d_setCrewShipId(crewShipId)

    def getCrewShipId(self):
        return self.crewShipId

    def setConstructedShipDoId(self, constructedShipDoId):
        self.constructedShipDoId = constructedShipDoId

    def getConstructedShipDoId(self):
        return self.constructedShipDoId

    def setCanControlInterests(self, canControlInterests):
        self.canControlInterests = canControlInterests

    def getCanControlInterests(self):
        return self.canControlInterests

    def disable(self):
        DistributedPlayerAI.disable(self)
        DistributedBattleAvatarAI.disable(self)

    def delete(self):
        self.air.targetMgr.clearAttacker(self)
        self.air.worldGridManager.clearAvatarInterests(self)
        inventory = self.getInventory()
        if inventory:
            self.air.questMgr.deactivateQuests(self)
            self.air.inventoryManager.removeInventory(inventory)

        self.ignore('HolidayStarted')
        self.ignore('HolidayEnded')
        self.ignore('timeOfDayChange')

        taskMgr.remove(self.uniqueName('process-groggy'))
        taskMgr.remove(self.uniqueName('process-double-xp'))

        DistributedPlayerAI.delete(self)
        DistributedBattleAvatarAI.delete(self)


@magicWord(category=CATEGORY_MODERATION, types=[int, str, str])
def setGMTag(gmNameTagState, gmNameTagColor, gmNameTagString):
    """
    Sets your GM nametag properties
    """

    #TODO: associate tag with rank in the CSM and revoke command properties?
    validColors = ['gold', 'red', 'green', 'blue', 'white']
    if gmNameTagColor not in validColors:
        return 'Invalid color specified!'

    if gmNameTagState < 0 or gmNameTagState > 1:
        return 'Invalid state!'

    invoker = spellbook.getInvoker()
    invoker.b_setAllowGMNameTag(True)
    invoker.d_setFounder(True)
    invoker.b_updateGMNameTag(gmNameTagState, gmNameTagColor, gmNameTagString)

    return 'Nametag set.'

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def setDoubleXP(val):
    target = spellbook.getTarget()
    target.b_setTempDoubleXPReward(val * 60)
    return "Set %s's Double XP Reward to %s minutes" % (target.getName(), val)

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def setFounder(state):
    """
    Sets your founder state
    """

    spellbook.getInvoker().d_setFounder(state)
    return 'Founder set to: %s' % state

@magicWord(category=CATEGORY_MODERATION, types=[str, str, str])
def toggleGM():
    """
    Toggles your GM name tag
    """

    invoker = spellbook.getInvoker()
    invoker.d_setFounder(True)
    invoker.b_setAllowGMNameTag(not invoker.getAllowGMNameTag())
    invoker.b_updateGMNameTag(not invoker.gmNameTagState, 'red',
        'Game Master')

    return 'Nametag toggled to: %s' % str(invoker.gmNameTagState)

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def name(name):
    """
    Sets the targets name
    """

    spellbook.getTarget().b_setName(name)
    return 'Your name has been set to %s.' % name

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def hp(hp=0):
    """
    Sets the targets current HP
    """
    target = spellbook.getTarget()
    if hp == 0:
        target.b_setHp(target.getMaxHp())
        return

    hp = max(0, min(hp, target.getMaxHp()))
    target.b_setHp(hp)
    return 'Your hp has been set to %d.' % hp

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def maxHp(maxHp):
    """
    Sets the targets max HP
    """

    spellbook.getTarget().b_setMaxHp(maxHp)
    return 'Your maxHp has been set to %d.' % maxHp

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def mojo(mojo=0):
    """
    Sets the targets Mojo level
    """
    target = spellbook.getTarget()

    if mojo == 0:
        target.b_setMojo(target.getMaxMojo())
        return

    mojo = max(0, min(mojo, target.getMaxMojo()))
    target.b_setMojo(mojo)
    return 'Your mojo has been set to %d.' % mojo

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def maxMojo(maxMojo):
    """
    Sets the targets max Mojo
    """

    spellbook.getTarget().b_setMaxMojo(maxMojo)
    return 'Your maxMojo has been set to %d.' % maxMojo

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int, int])
def level(repType, level):
    """
    Sets the invokers level
    """

    invoker = spellbook.getInvoker()
    inventory = invoker.getInventory()
    if inventory:
        totalRep = 0

        for levelIndex in xrange(level):
            totalRep += ReputationGlobals.getReputationNeededToLevel(
                repType, levelIndex)

        if repType == InventoryType.OverallRep:
            inventory.setOverallRep(totalRep)
        else:
            inventory.setReputation(repType, totalRep)

    return 'Your level has been set to %d.' % level

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def zombie():
    """
    Toggles the targets zombie state
    """

    target = spellbook.getTarget()
    target.forcedZombie = not target.forcedZombie
    target.attemptToSetCursedZombie()

    return 'Targets Zombie state forced to %s' % target.forcedZombie

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def removeGroggy():
    """
    Removes the invokers groggy effect
    """

    invoker = spellbook.getInvoker()
    inventory = simbase.air.inventoryManager.getInventory(invoker.doId)
    inventory.setVitaeLevel(0)
    return "Removed active groggy effect!"

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def location():
    """
    Returns the avatar's current parentId and zoneId
    """

    invoker = spellbook.getInvoker()
    return "avatarId: %d, parentId: %d, zoneId: %d" % (invoker.doId,
        invoker.parentId, invoker.zoneId)

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def setGuildName(name):
    spellbook.getInvoker().b_setGuildName(name)
    return "Set Guild Name to %s" % name
