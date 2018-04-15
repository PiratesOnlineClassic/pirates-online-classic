from direct.directnotify import DirectNotifyGlobal
from otp.avatar.DistributedPlayerAI import DistributedPlayerAI
from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.pirate.HumanDNA import HumanDNA
from pirates.battle.BattleRandom import BattleRandom
from pirates.quest.DistributedQuestAvatar import DistributedQuestAvatar
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.quest.QuestConstants import LocationIds
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.battle.DistributedWeaponAI import DistributedWeaponAI
from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType
from otp.ai.MagicWordGlobal import *
from pirates.battle import WeaponGlobals
from pirates.reputation import ReputationGlobals

class DistributedPlayerPirateAI(DistributedPlayerAI, DistributedBattleAvatarAI, HumanDNA):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerPirateAI')

    def __init__(self, air):
        DistributedPlayerAI.__init__(self, air)
        DistributedBattleAvatarAI.__init__(self, air)
        HumanDNA.__init__(self)

        self.isNpc = False
        self.battleRandom = None

        self.dnaString = ''
        self.inventoryId = 0
        self.jailCellIndex = 0
        self.returnLocation = ''
        self.currentIsland = ''
        self.emoteId = 0
        self.zombie = 0

        self.stickyTargets = []

    def announceGenerate(self):
        DistributedPlayerAI.announceGenerate(self)
        DistributedBattleAvatarAI.announceGenerate(self)

    def generate(self):
        DistributedPlayerAI.generate(self)
        DistributedBattleAvatarAI.generate(self)

        self.battleRandom = BattleRandom(self.doId)

        self.weapon = DistributedWeaponAI(self.air)
        self.weapon.generateWithRequiredAndId(self.air.allocateChannel(), 0, 0)

    def setLocation(self, parentId, zoneId):
        DistributedPlayerAI.setLocation(self, parentId, zoneId)
        DistributedBattleAvatarAI.setLocation(self, parentId, zoneId)

        parentObj = self.getParentObj()

        if parentObj:
            if self.weapon:
                self.weapon.b_setLocation(parentId, zoneId)

    def setLocation(self, parentId, zoneId):
        DistributedPlayerAI.setLocation(self, parentId, zoneId)
        DistributedBattleAvatarAI.setLocation(self, parentId, zoneId)

        parentObj = self.getParentObj()
        if parentObj:
            if isinstance(parentObj, DistributedGameAreaAI):
                if self.currentIsland:
                    self.b_setReturnLocation(self.currentIsland)

                self.b_setCurrentIsland(parentObj.getUniqueId())

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
        self.air.inventoryManager.getInventory(self.doId)

    def setDNAString(self, dnaString):
        self.dnaString = dnaString

    def d_setDNAString(self, dnaString):
        self.sendUpdate('setDNAString', [dnaString])

    def b_setDNAString(self, dnaString):
        self.setDNAString(dnaString)
        self.d_setDNAString(dnaString)

    def getDNAString(self):
        return self.dnaString

    def setInventoryId(self, inventoryId):
        self.inventoryId = inventoryId

    def d_setInventoryId(self, inventoryId):
        self.sendUpdate('setInventoryId', [inventoryId])

    def b_setInventoryId(self, inventoryId):
        self.setInventoryId(inventoryId)
        self.d_setInventoryId(inventoryId)

    def getInventoryId(self):
        return self.inventoryId

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
        self.sendUpdateToAvatarId(self.doId, 'playEmote', [emoteId])
        self.sendUpdate('playEmote', [emoteId])

    def getEmote(self):
        return self.emoteId

    def requestCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        if not self.weapon:
            self.notify.warning('Cannot request current weapon for avatar %d, does not have a weapon object!' % \
                self.doId)

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
        inventory = simbase.air.inventoryManager.getInventory(self.doId)

        if inventory:
            if skillId >= InventoryType.begin_WeaponSkillMelee and skillId < InventoryType.end_WeaponSkillMelee:
                unspentStack = inventory.getStack(InventoryType.UnspentMelee)
                if not unspentStack:
                    self.notify.debug("Player has no skill points to use!")
                    return
                else:
                    if unspentStack[1] > 0:
                        inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                    else:
                        self.notify.debug("Player has no skill points to use!")
                        return
            elif skillId >= InventoryType.begin_WeaponSkillCutlass and skillId < InventoryType.end_WeaponSkillCutlass:
                unspentStack = inventory.getStack(InventoryType.UnspentCutlass)
                if not unspentStack:
                    self.notify.warning("Player has no skill points to use!")
                    return
                elif unspentStack[1] > 0:
                    inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                else:
                    if unspentStack[1] > 0:
                        inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                    else:
                        self.notify.debug("Player has no skill points to use!")
                        return
            elif skillId >= InventoryType.begin_WeaponSkillPistol and skillId < InventoryType.end_WeaponSkillPistol:
                unspentStack = inventory.getStack(InventoryType.UnspentPistol)
                if not unspentStack:
                    self.notify.warning("Player has no skill points to use!")
                    return
                elif unspentStack[1] > 0:
                    inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                else:
                    if unspentStack[1] > 0:
                        inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                    else:
                        self.notify.debug("Player has no skill points to use!")
                        return
            elif skillId >= InventoryType.begin_WeaponSkillMusket and skillId < InventoryType.end_WeaponSkillMusket:
                unspentStack = inventory.getStack(InventoryType.UnspentMusket)
                if not unspentStack:
                    self.notify.warning("Player has no skill points to use!")
                    return
                elif unspentStack[1] > 0:
                    inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                else:
                    if unspentStack[1] > 0:
                        inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                    else:
                        self.notify.debug("Player has no skill points to use!")
                        return
            elif skillId >= InventoryType.begin_WeaponSkillDagger and skillId < InventoryType.end_WeaponSkillDagger:
                unspentStack = inventory.getStack(InventoryType.UnspentDagger)
                if not unspentStack:
                    self.notify.warning("Player has no skill points to use!")
                    return
                else:
                    if unspentStack[1] > 0:
                        inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                    else:
                        self.notify.debug("Player has no skill points to use!")
                        return
            elif skillId >= InventoryType.begin_WeaponSkillGrenade and skillId < InventoryType.end_WeaponSkillGrenade:
                unspentStack = inventory.getStack(InventoryType.UnspentGrenade)
                if not unspentStack:
                    self.notify.debug("Player has no skill points to use!")
                    return
                else:
                    if unspentStack[1] > 0:
                        inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                    else:
                        self.notify.debug("Player has no skill points to use!")
                        return
            elif skillId >= InventoryType.begin_WeaponSkillDoll and skillId < InventoryType.end_WeaponSkillDoll:
                unspentStack = inventory.getStack(InventoryType.UnspentDoll)
                if not unspentStack:
                    self.notify.debug("Player has no skill points to use!")
                    return
                else:
                    if unspentStack[1] > 0:
                        inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                    else:
                        self.notify.debug("Player has no skill points to use!")
                        return
            elif skillId >= InventoryType.begin_WeaponSkillWand and skillId < InventoryType.end_WeaponSkillWand:
                unspentStack = inventory.getStack(InventoryType.UnspentWand)
                if not unspentStack:
                    self.notify.debug("Player has no skill points to use!")
                    return
                elif unspentStack[1] > 0:
                    inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                else:
                    self.notify.debug("Player has no skill points to use!")
                    return
            else:
                self.notify.debug("SkillId %s has no unspent category!!" % (str(skillId)))
                return

            stack = inventory.getStack(skillId)
            if not stack:
                inventory.b_setStack(skillId, 1)
            else:
                inventory.b_setStack(skillId, stack[1] + 1)

            self.spentSkillPoint(skillId)
        else:
            self.notify.debug("Player has no inventory!")

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
            amount = inventory.getStack(tonicId)
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

        amount = inventory.getStack(tonicId)
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

        inventory.b_setStack(tonicId, inventory.getStack(tonicId)[1] - 1)

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

    def delete(self):
        DistributedPlayerAI.delete(self)
        DistributedBattleAvatarAI.delete(self)

        if self.battleRandom:
            self.battleRandom.delete()

        if self.weapon:
            self.weapon.requestDelete()

        self.battleRandom = None
        self.weapon = None

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

    def requestRemoveStickyTargets(self, doIdList):
        for targetDoId in doIdList:
            targetData = self.air.battleMgr.getTargetData(targetDoId)

            if targetData:
                attackerData = targetData.getAttackerData(self.doId)

                if attackerData:
                    for skillData in attackerData.skillData.values():
                        if self.air.battleMgr.getIsVoodooDoll(skillData.skillId):
                            attackerData.removeSkillData(skillData)

            self.removeStickyTarget(targetDoId)

    def setZombie(self, zombie):
        self.zombie = zombie

    def d_setZombie(self, zombie):
        self.sendUpdate('setZombie', [zombie])

    def b_setZombie(self, zombie):
        self.setZombie(zombie)
        self.d_setZombie(zombie)

    def getZombie(self):
        return self.zombie

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[str])
def name(name):
    spellbook.getTarget().b_setName(name)
    return "Your name has been set to %s." % name

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def hp(hp):
    spellbook.getTarget().b_setHp(hp)
    return "Your hp has been set to %d." % hp

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def maxHp(maxHp):
    spellbook.getTarget().b_setMaxHp(maxHp)
    return "Your maxHp has been set to %d." % maxHp

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def mojo(mojo):
    spellbook.getTarget().b_setMojo(mojo)
    return "Your mojo has been set to %d." % mojo

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def maxMojo(maxMojo):
    spellbook.getTarget().b_setMaxMojo(maxMojo)
    return "Your maxMojo has been set to %d." % maxMojo

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def level(level):
    invoker = spellbook.getInvoker()
    inventory = simbase.air.inventoryManager.getInventory(invoker.doId)
    if inventory:
        totalRep = 0

        for levelIndex in xrange(level):
            totalRep += ReputationGlobals.getReputationNeededToLevel(
                InventoryType.OverallRep, levelIndex)

        inventory.setGeneralRep(totalRep)

    return "Your level has been set to %d." % level
