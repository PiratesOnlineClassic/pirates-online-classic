from direct.directnotify import DirectNotifyGlobal
from otp.avatar.DistributedPlayerAI import DistributedPlayerAI
from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.pirate.HumanDNA import HumanDNA
from pirates.quest.DistributedQuestAvatarAI import DistributedQuestAvatarAI
from pirates.battle.BattleRandom import BattleRandom
from pirates.pirate.PlayerPirateGameFSMAI import PlayerPirateGameFSMAI
from pirates.quest.DistributedQuestAvatar import DistributedQuestAvatar
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.quest.QuestConstants import LocationIds
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType
from otp.ai.MagicWordGlobal import *
from pirates.battle import WeaponGlobals
from pirates.reputation import ReputationGlobals
from pirates.battle.BattleSkillDiaryAI import BattleSkillDiaryAI

class DistributedPlayerPirateAI(DistributedPlayerAI, DistributedBattleAvatarAI, HumanDNA, DistributedQuestAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerPirateAI')

    def __init__(self, air):
        DistributedPlayerAI.__init__(self, air)
        DistributedBattleAvatarAI.__init__(self, air)
        HumanDNA.__init__(self)
        DistributedQuestAvatarAI.__init__(self, air)

        self.gameFSM = PlayerPirateGameFSMAI(self.air, self)
        self.isNpc = False
        self.battleRandom = None

        self.dnaString = ''
        self.inventoryId = 0
        self.guildId = 0
        self.guildName = 'Null'
        self.teleportFlags = None
        self.jailCellIndex = 0
        self.returnLocation = ''
        self.currentIsland = ''
        self.emoteId = 0
        self.zombie = 0
        self.forcedZombie = 0
        self.gmNameTagAllowed = False

        self.stickyTargets = []

    def announceGenerate(self):
        DistributedPlayerAI.announceGenerate(self)
        DistributedBattleAvatarAI.announceGenerate(self)

    def generate(self):
        DistributedPlayerAI.generate(self)
        DistributedBattleAvatarAI.generate(self)

        self.battleRandom = BattleRandom(self.doId)
        self.battleSkillDiary = BattleSkillDiaryAI(self.air, self)

        self.accept('HolidayStarted', self.processHolidayStart)
        self.accept('HolidayEnded', self.processHolidayEnd)
        self.accept('todHalloweenStateChange', self.attemptToSetCursedZombie)

        taskMgr.doMethodLater(0.05, self.__processGroggy, self.uniqueName('process-groggy'))

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

    def processHolidayStart(self, holidayId):
        self.attemptToSetCursedZombie()

    def processHolidayEnd(self, holidayId):
        self.attemptToSetCursedZombie()

    def setLocation(self, parentId, zoneId):
        DistributedPlayerAI.setLocation(self, parentId, zoneId)
        DistributedBattleAvatarAI.setLocation(self, parentId, zoneId)

        parentObj = self.getParentObj()
        if parentObj:
            if isinstance(parentObj, DistributedGameAreaAI):
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

            self.attemptToSetCursedZombie()

    def getWorld(self):
        parentObj = self.getParentObj()
        if parentObj:
            if isinstance(parentObj, DistributedGameAreaAI):
                parentObj = parentObj.getParentObj()

        if not parentObj:
            return None

        if isinstance(parentObj, DistributedInstanceBaseAI):
            return parentObj

        return None

    def getInventory(self):
        return self.air.inventoryManager.getInventory(self.doId)

    def setDNAString(self, dnaString):
        self.dnaString = dnaString
        self.makeFromNetString(dnaString)

    def d_setDNAString(self, dnaString):
        self.sendUpdate('setDNAString', [dnaString])

    def b_setDNAString(self, dnaString):
        self.setDNAString(dnaString)
        self.d_setDNAString(dnaString)

    def getDNAString(self):
        return self.dnaString

    def sendDNAUpdate(self):
        self.d_setDNAString(self.makeNetString())

    def d_setFounder(self, founder):
        self.sendUpdate('setFounder', [founder])

    def setInventoryId(self, inventoryId):
        self.inventoryId = inventoryId

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
        self.teleportFlags = teleportFlags

    def d_setTeleportFlags(self, teleportFlags):
        self.sendUpdate('setTeleportFlags', [PiratesGlobals.encodeTeleportFlag(
            teleportFlags)])

    def b_setTeleportFlag(self, teleportFlags):
        self.setTeleportFlags(teleportFlags)
        self.d_setTeleportFlags(teleportFlags)

    def getTeleportFlags(self):
        return self.teleportFlags

    def d_relayTeleportLoc(self, shardId, zoneId, teleportMgrDoId):
        self.sendUpdateToAvatarId(self.doId, 'relayTeleportLoc', [shardId, zoneId,
            teleportMgrDoId])

    def d_forceTeleportStart(self, instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone):
        self.sendUpdateToAvatarId(self.doId, 'forceTeleportStart', [instanceName, tzDoId, thDoId,
            worldGridDoId, tzParent, tzZone])

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

    def sendClothingMessage(self, clothingId, colorId):
        self.sendUpdate("sendClothingMessage", [clothingId, colorId])

    def sendLootMessage(self, lootId):
        self.sendUpdate("sendLootMessage", [lootId])

    def sendCardMessage(self, cardId):
        self.sendUpdate("sendCardMessage", [cardId])

    def sendWeaponMessage(self, weapon):
        self.sendUpdate("sendWeaponMessage", [weapon])

    def sendJewelryMessage(self, jewelryUID):
        self.sendUpdate("sendJewelryMessage", [jewelryUID])

    def sendTattooMessage(self, tattooUID):
        self.sendUpdate("sendTattooMessage", [tattooUID])

    def sendReputationMessage(self, targetId, categories, reputationList, basicPenalty, crewBonus, doubleXPBonus, holidayBonus):
        self.sendUpdate("sendReputationMessage", [targetId, categories, reputationList, basicPenalty,
            crewBonus, doubleXPBonus, holidayBonus])

    def spendSkillPoint(self, skillId):
        inventory = self.getInventory()

        if not inventory:
            self.notify.debug('Cannot spend skill point %d for avatar %d, no inventory present' % (
                skillId, self.doId))

            return

        def updateStack(stackType):
            unspentStack = inventory.getStackQuantity(stackType)
            if not unspentStack:
                self.notify.debug('Cannot update stack %d, player has no skill points!' % (
                    stackType))

                return

            inventory.b_setStackQuantity(stackType, unspentStack - 1)

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
        elif skillId >= InventoryType.begin_WeaponSkillDoll and skillId < InventoryType.end_WeaponSkillDoll:
            updateStack(InventoryType.UnspentDoll)
        elif skillId >= InventoryType.begin_WeaponSkillWand and skillId < InventoryType.end_WeaponSkillWand:
            updateStack(InventoryType.UnspentWand)
        else:
            self.notify.debug('SkillId %d has no unspent category!' % (
                skillId))

            return

        stack = inventory.getStackQuantity(skillId)
        if not stack:
            inventory.b_setStackQuantity(skillId, 1)
        else:
            inventory.b_setStackQuantity(skillId, stack + 1)

        self.spentSkillPoint(skillId)

    def spentSkillPoint(self, category):
        self.sendUpdate("spentSkillPoint", [category])

    def resetSkillPoints(self, skillId):
        self.sendUpdate("resetSkillPoints", [skillId])

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

        amount = inventory.getStackQuantity(tonicId)[1]
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

        inventory.b_setStackQuantity(tonicId, inventory.getStackQuantity(tonicId)[1] - 1)

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

    def setZombie(self, zombie):
        self.zombie = zombie

    def d_setZombie(self, zombie):
        self.sendUpdate('setZombie', [zombie])

    def b_setZombie(self, zombie):
        self.setZombie(zombie)
        self.d_setZombie(zombie)

    def getZombie(self):
        return self.zombie

    def setAllowGMNameTag(self, gmNameTagAllowed):
        self.gmNameTagAllowed = gmNameTagAllowed

    def d_setAllowGMNameTag(self, gmNameTagAllowed):
        self.sendUpdate('setAllowGMNameTag', gmNameTagAllowed)

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

    def disable(self):
        DistributedPlayerAI.disable(self)
        DistributedBattleAvatarAI.disable(self)

    def delete(self):
        inventory = self.getInventory()

        if inventory:
            self.air.inventoryManager.removeInventory(inventory)

        if self.battleRandom:
            self.battleRandom.delete()

        self.battleRandom = None

        self.ignore('HolidayStarted')
        self.ignore('HolidayEnded')
        self.ignore('timeOfDayChange')

        taskMgr.remove(self.uniqueName('process-groggy'))

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

    spellbook.getInvoker().b_updateGMNameTag(gmNameTagState, gmNameTagColor, gmNameTagString)
    return 'Nametag set.'

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
    invoker.b_updateGMNameTag(not invoker.gmNameTagState, invoker.gmNameTagColor, invoker.gmNameTagString)

    return 'Nametag toggled to: %s' % str(invoker.gmNameTagState)

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def name(name):
    """
    Sets the targets name
    """

    spellbook.getTarget().b_setName(name)
    return 'Your name has been set to %s.' % name

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def hp(hp):
    """
    Sets the targets current HP
    """
    target = spellbook.getTarget()

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
def mojo(mojo):
    """
    Sets the targets Mojo level
    """


    target = spellbook.getTarget()

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

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def level(level):
    """
    Sets the invokers level
    """

    invoker = spellbook.getInvoker()
    inventory = simbase.air.inventoryManager.getInventory(invoker.doId)
    if inventory:
        totalRep = 0

        for levelIndex in xrange(level):
            totalRep += ReputationGlobals.getReputationNeededToLevel(
                InventoryType.OverallRep, levelIndex)

        inventory.setOverallRep(totalRep)

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
