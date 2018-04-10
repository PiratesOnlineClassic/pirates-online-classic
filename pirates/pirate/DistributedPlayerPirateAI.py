from direct.directnotify import DirectNotifyGlobal
from otp.avatar.DistributedPlayerAI import DistributedPlayerAI
from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.pirate.HumanDNA import HumanDNA
from pirates.quest.DistributedQuestAvatar import DistributedQuestAvatar
from pirates.piratesbase import PLocalizer
from pirates.quest.QuestConstants import LocationIds
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType

class DistributedPlayerPirateAI(DistributedPlayerAI, DistributedBattleAvatarAI, HumanDNA):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerPirateAI')

    def __init__(self, air):
        DistributedPlayerAI.__init__(self, air)
        DistributedBattleAvatarAI.__init__(self, air)
        HumanDNA.__init__(self)
        self.dnaString = ''
        self.inventoryId = 0
        self.jailCellIndex = 0
        self.returnLocation = ''
        self.currentIsland = ''
        self.emoteId = 0

    def generate(self):
        DistributedPlayerAI.generate(self)
        DistributedBattleAvatarAI.generate(self)

    def announceGenerate(self):
        DistributedPlayerAI.announceGenerate(self)
        DistributedBattleAvatarAI.announceGenerate(self)

    def setLocation(self, parentId, zoneId):
        DistributedPlayerAI.setLocation(self, parentId, zoneId)
        DistributedBattleAvatarAI.setLocation(self, parentId, zoneId)

        parentObj = self.getParentObj()
        if parentObj:
            if isinstance(parentObj, DistributedGameAreaAI):
                if self.currentIsland:
                    self.b_setReturnLocation(self.currentIsland)

                self.b_setCurrentIsland(parentObj.getUniqueId())

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

        # we must send play emote twice because the field is marked broadcast,
        # which means everyone in the same interest will need to hear about the message;
        # we must first send a direct update to our client object, then broadcast the message...
        self.sendUpdateToAvatarId(self.doId, 'playEmote', [emoteId])
        self.sendUpdate('playEmote', [emoteId])

    def getEmote(self):
        return self.emoteId

    def requestCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        self.b_setCurrentWeapon(currentWeaponId, isWeaponDrawn)

    def setCurseStatus(self, curseStat):
        pass

    def spendSkillPoint(self, skillId):
        avatarId = self.air.getAvatarIdFromSender()
        inventory = simbase.air.inventoryManager.getInventory(avatarId)
        if inventory:
            if skillId >= begin_WeaponSkillMelee and skillId < end_WeaponSkillMelee:
                unspentStack = inventory.getStack(InventoryCategory.UnspentMelee)
                if not stack:
                    inventory.b_setStack(InventoryCategory.UnspentMelee, 0)
                    self.notify.warning("Player has no skill points to use!")
                    return
                else:
                    if unspentStack[1] > 0:
                        inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                    else:
                        self.notify.warning("Player has no skill points to use!")
                        return
            elif skillId >= begin_WeaponSkillCutlass and skillId < end_WeaponSkillCutlass:
                unspentStack = inventory.getStack(InventoryCategory.UnspentCutlass)
                if not stack:
                    inventory.b_setStack(InventoryCategory.UnspentCutlass, 0)
                    self.notify.warning("Player has no skill points to use!")
                    return
                else:
                    if unspentStack[1] > 0:
                        inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                    else:
                        self.notify.warning("Player has no skill points to use!")
                        return
            elif skillId >= begin_WeaponSkillPistol and skillId < end_WeaponSkillPistol:
                unspentStack = inventory.getStack(InventoryCategory.UnspentPistol)
                if not stack:
                    inventory.b_setStack(InventoryCategory.UnspentPistol, 0)
                    self.notify.warning("Player has no skill points to use!")
                    return
                else:
                    if unspentStack[1] > 0:
                        inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                    else:
                        self.notify.warning("Player has no skill points to use!")
                        return
            elif skillId >= begin_WeaponSkillMusket and skillId < end_WeaponSkillMusket:
                unspentStack = inventory.getStack(InventoryCategory.UnspentMusket)
                if not stack:
                    inventory.b_setStack(InventoryCategory.UnspentMusket, 0)
                    self.notify.warning("Player has no skill points to use!")
                    return
                else:
                    if unspentStack[1] > 0:
                        inventory.b_setStack(unspentStack[0], unspentStack[1] - 1)
                    else:
                        self.notify.warning("Player has no skill points to use!")
                        return
            else:
                self.notify.warning("SkillID %s has no unspent category!!" % (str(skillId)))
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

    def useTonic(self, tonicId):
        pass

    def useBestTonic(self):
        pass

    def flagFirstDeath(self):
        pass
