from panda3d.core import *

from direct.directnotify import DirectNotifyGlobal

from otp.ai.MagicWordGlobal import *
from otp.otpbase import OTPGlobals
from otp.avatar.DistributedPlayerAI import DistributedPlayerAI
from otp.distributed.OtpDoGlobals import OTP_DO_ID_AVATAR_FRIENDS_MANAGER

from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.pirate.HumanDNAAI import HumanDNAAI
from pirates.quest.DistributedQuestAvatarAI import DistributedQuestAvatarAI
from pirates.tutorial import TutorialGlobals
from pirates.pirate.PlayerPirateGameFSMAI import PlayerPirateGameFSMAI
from pirates.quest.DistributedQuestAvatar import DistributedQuestAvatar
from pirates.quest.QuestStatus import QuestStatus
from pirates.piratesbase import PLocalizer
from pirates.chat import PChatFilter
from pirates.piratesbase import PiratesGlobals
from pirates.pirate import AvatarTypes
from pirates.pirate import TitleGlobals
from pirates.quest.QuestConstants import LocationIds
from pirates.quest import QuestDB
from pirates.quest.QuestReward import CutlassReward
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI
from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType, getNumRespecType
from pirates.economy import EconomyGlobals
from pirates.battle import WeaponGlobals
from pirates.reputation import ReputationGlobals
from pirates.piratesbase import Freebooter
from pirates.piratesbase import FreebooterAI

class DistributedPlayerPirateAI(DistributedPlayerAI, DistributedBattleAvatarAI, HumanDNAAI, DistributedQuestAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerPirateAI')

    # the groggy (vitae) state is counted down once every second,
    # this is the amount of vitae removed each time...
    GroggyUpdateTime = 1.0
    GroggyUpdateAmount = 20

    # the islands (ports of call) with a jail we may be sent back to when we are defeated,
    # these are island uids so Padres Del Fuego is the island and not it's port...
    ValidReturnLocations = (
        LocationIds.PORT_ROYAL_ISLAND,
        LocationIds.TORTUGA_ISLAND,
        LocationIds.DEL_FUEGO_ISLAND,
        LocationIds.CUBA_ISLAND
    )

    # the avatar's health and voodoo regenerate every few seconds
    # while it is not in battle...
    ToonUpTime = 2.0

    # the avatar's voodoo keeps regenerating while it fights, only slower;
    # without it voodoo users could never cast again once their mojo ran out...
    BattleMojoRegenDivisor = 4

    # the amount of seconds a skill may be used before it has finished
    # recharging, the client only starts recharging a skill once it has
    # received the skill's result from us...
    RechargeTolerance = 1.0

    # how long the avatar shows it's charge being interrupted
    InterruptedDuration = 1

    # weapons that every avatar may use, even when they are not in the
    # avatar's inventory; the combat tray falls back to the avatar's fists
    # when the avatar has not been given any weapons yet...
    DefaultWeapons = (0, InventoryType.MeleeWeaponL1)

    # the skills of each weapon and the skill points spent on them,
    # see SkillPage.respec...
    SkillTracks = {
        InventoryType.MeleeRep: (InventoryType.begin_WeaponSkillMelee,
            InventoryType.end_WeaponSkillMelee, InventoryType.UnspentMelee),
        InventoryType.CutlassRep: (InventoryType.begin_WeaponSkillCutlass,
            InventoryType.end_WeaponSkillCutlass, InventoryType.UnspentCutlass),
        InventoryType.PistolRep: (InventoryType.begin_WeaponSkillPistol,
            InventoryType.end_WeaponSkillPistol, InventoryType.UnspentPistol),
        InventoryType.MusketRep: (InventoryType.begin_WeaponSkillMusket,
            InventoryType.end_WeaponSkillMusket, InventoryType.UnspentMusket),
        InventoryType.DaggerRep: (InventoryType.begin_WeaponSkillDagger,
            InventoryType.end_WeaponSkillDagger, InventoryType.UnspentDagger),
        InventoryType.GrenadeRep: (InventoryType.begin_WeaponSkillGrenade,
            InventoryType.end_WeaponSkillGrenade, InventoryType.UnspentGrenade),
        InventoryType.DollRep: (InventoryType.begin_WeaponSkillDoll,
            InventoryType.end_WeaponSkillDoll, InventoryType.UnspentDoll),
        InventoryType.SailingRep: (InventoryType.begin_SkillSailing,
            InventoryType.end_SkillSailing, InventoryType.UnspentSailing),
        InventoryType.WandRep: (InventoryType.begin_WeaponSkillWand,
            InventoryType.end_WeaponSkillWand, InventoryType.UnspentWand),
        InventoryType.CannonRep: (InventoryType.begin_WeaponSkillCannon,
            InventoryType.end_WeaponSkillCannon, InventoryType.UnspentCannon)}

    # combo skills which require the previous skill in the combo
    # chain to be learned first, see the client's SkillPage.addPoint...
    ComboOrderSkills = (
        InventoryType.CutlassSlash,
        InventoryType.CutlassCleave,
        InventoryType.CutlassFlourish,
        InventoryType.CutlassStab,
        InventoryType.DaggerSwipe,
        InventoryType.DaggerGouge,
        InventoryType.DaggerEviscerate)

    def __init__(self, air):
        DistributedPlayerAI.__init__(self, air)
        DistributedBattleAvatarAI.__init__(self, air)
        HumanDNAAI.__init__(self)
        DistributedQuestAvatarAI.__init__(self, air)

        self.gameFSM = PlayerPirateGameFSMAI(self.air, self)
        self.questStatus = None
        self.isNpc = False

        # players are always on the player team, the client's TeamUtils and the
        # pvp damage rules of BattleManagerBase depend on it...
        self.setTeam(PiratesGlobals.PLAYER_TEAM)

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
        self.gmNameTagState = 0
        self.gmNameTagColor = ''
        self.gmNameTagString = ''
        self.defaultQuestGiven = False
        self.stickyTargets = []
        self.defaultShard = 0
        self.defaultZone = 0
        self.tempDoubleXPReward = 0
        self.toonUpTask = None
        self.constructedShipDoId = 0
        self.activeShipId = 0
        self.crewShipId = 0
        self.questRewardFlags = 0
        self.bandManagerId = 0
        self.bandId = 0
        self.lootCarried = 0
        self.maxLootCarried = 0
        self.skillRechargeTimes = {}
        self.badgeIcon = (-1, -1)
        self.shipBadgeIcon = (-1, -1)
        self.onWelcomeWorld = False
        self.areaSphereStack = []

    def announceGenerate(self):
        DistributedPlayerAI.announceGenerate(self)
        DistributedBattleAvatarAI.announceGenerate(self)

        # Let the guild manager know we've arrived on this district:
        self.air.guildManager.avatarOnline(self)

        # Make sure the crew we arrived with still exists:
        self.air.bandManager.verifyAvatarBandId(self)

    def generate(self):
        DistributedPlayerAI.generate(self)
        DistributedBattleAvatarAI.generate(self)

        taskMgr.doMethodLater(self.GroggyUpdateTime, self.__processGroggy, self.uniqueName('process-groggy'))
        taskMgr.doMethodLater(10, self.__processDoubleXP, self.uniqueName('process-double-xp'))

    def __processGroggy(self, task):
        inventory = self.getInventory()
        if not inventory:
            return task.again

        vitaeLevel = inventory.getVitaeLevel()
        if vitaeLevel:
            # increment down the Vitae
            amount = max(inventory.getVitaeLeft() - self.GroggyUpdateAmount, 0)
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

    def setLocation(self, parentId, zoneId):
        from pirates.world.DistributedIslandAI import DistributedIslandAI

        # leaving the area we were fighting in (a door, a teleport...) leaves
        # every battle we were in, our targets are no longer around us...
        previousParentId = self.parentId
        if previousParentId and previousParentId != parentId and self.isGenerated():
            self.air.targetMgr.clearAttacker(self)

        DistributedPlayerAI.setLocation(self, parentId, zoneId)
        DistributedBattleAvatarAI.setLocation(self, parentId, zoneId)

        parentObj = self.getParentObj()
        if parentObj:
            if isinstance(parentObj, DistributedIslandAI):
                if self.currentIsland != parentObj.getUniqueId():
                    self.b_setCurrentIsland(parentObj.getUniqueId())

                # the island we have just arrived at becomes our return location
                # (where we are jailed and respawn), the client also requests this...
                self.updateReturnLocation(parentObj)

        jollyCurseMgr = getattr(self.air, 'jollyCurseMgr', None)
        if jollyCurseMgr:
            jollyCurseMgr.avatarChangedLocation(self, parentObj)

    def getInventory(self):
        return self.air.inventoryManager.getInventory(self.doId)

    def isInBattle(self):
        return self.currentTarget is not None or self.gameFSM.getCurrentOrNextState() != 'LandRoam'

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

    def setBandId(self, bandManagerId, bandId):
        changed = (bandManagerId, bandId) != (self.bandManagerId, self.bandId)
        self.bandManagerId = bandManagerId
        self.bandId = bandId
        messenger.send(self.getBandIdChangedEvent(), [bandManagerId, bandId])

        if changed and self.isGenerated():
            # Let our friends and guild mates know we've changed crew:
            self.d_setFriendsBandId(bandManagerId, bandId)
            self.air.guildManager.d_sendAvatarBandId(self.doId, bandManagerId, bandId)

    def d_setFriendsBandId(self, bandManagerId, bandId):
        # The district has no handle on the avatar friends manager UberDOG,
        # so send the update to it directly:
        dclass = self.air.dclassesByName['PCAvatarFriendsManager']
        datagram = dclass.aiFormatUpdate('setBandId', OTP_DO_ID_AVATAR_FRIENDS_MANAGER,
            OTP_DO_ID_AVATAR_FRIENDS_MANAGER, self.air.ourChannel, [self.doId, bandManagerId, bandId])
        self.air.send(datagram)

    def getBandIdChangedEvent(self):
        return 'bandIdChanged-%d' % self.doId

    def d_setBandId(self, bandManagerId, bandId):
        self.sendUpdate('setBandId', [bandManagerId, bandId])

    def b_setBandId(self, bandManagerId, bandId):
        self.setBandId(bandManagerId, bandId)
        self.d_setBandId(bandManagerId, bandId)

    def getBandId(self):
        return (self.bandManagerId, self.bandId)

    def setHp(self, hp, quietly=False):
        DistributedBattleAvatarAI.setHp(self, hp, quietly)
        if self.isGenerated():
            self.air.bandManager.updateAvatarHp(self)

    def setMaxHp(self, maxHp):
        DistributedBattleAvatarAI.setMaxHp(self, maxHp)
        if self.isGenerated():
            self.air.bandManager.updateAvatarHp(self)

    def isGroggy(self):
        inventory = self.getInventory()
        if not inventory:
            return False

        return inventory.getStackQuantity(InventoryType.Vitae_Level) > 0

    def getAdjMaxHp(self):
        # groggy avatars may only regain a portion of their max hp,
        # this matches the client's DistributedBattleAvatar.getAdjMaxHp...
        if self.isGroggy():
            return int(self.maxHp * 0.75)

        return self.maxHp

    def getAdjMaxMojo(self):
        if self.isGroggy():
            return int(self.maxMojo * 0.75)

        return self.maxMojo

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
        self.sendUpdateToAvatarId(self.doId, 'relayTeleportLoc', [shardId, zoneId, teleportMgrDoId])

    def d_forceTeleportStart(self, instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone):
        self.sendUpdateToAvatarId(self.doId, 'forceTeleportStart', [instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone])

    def d_beginningTeleport(self, instanceType, fromInstanceType, instanceName, gameType):
        """
        Notify the client that a teleport is beginning. This triggers the loading screen
        and calls the startedCallback on the client's teleport manager.
        """
        self.sendUpdateToAvatarId(self.doId, 'beginningTeleport', [instanceType, fromInstanceType, instanceName, gameType])

    def requestActivity(self, gameType, gameCategory, options, shipIds):
        self.air.matchMaker.requestActivity(self, gameType, gameCategory, options, shipIds)

    def requestInvites(self, inviteModes, gameCategory, gameType, options, additionalAvs):
        self.air.matchMaker.requestInvites(self, inviteModes, gameCategory, gameType, options, additionalAvs)

    def d_requestInvitesResp(self, invitees, numFailed):
        self.sendUpdateToAvatarId(self.doId, 'requestInvitesResp', [invitees, numFailed])

    def d_lookoutMatchFailed(self, restartRequest):
        self.sendUpdateToAvatarId(self.doId, 'lookoutMatchFailed', [restartRequest])

    def d_setTutorialHandlerZone(self, handlerZoneId):
        self.sendUpdateToAvatarId(self.doId, 'setTutorialHandlerZone', [handlerZoneId])

    def _isSenderSelf(self, fieldName, **kwargs):
        """
        Returns True if the current clsend message was sent by this avatar's own
        client. clsend fields on an avatar can be sent by any client that can see it.
        """

        avatarId = self.air.getAvatarIdFromSender()
        if avatarId == self.doId:
            return True

        self.air.logPotentialHacker(
            message='Received %s for another avatar!' % fieldName,
            targetAvId=self.doId,
            **kwargs)

        return False

    def giveDefaultQuest(self):
        if not self._isSenderSelf('giveDefaultQuest'):
            return

        if config.GetBool('want-alpha-blockers', False):
            # Don't give a default quest if alpha blockers are enabled
            return

        # the client only asks for the default quest when it skips the tutorial
        # with a brand new avatar (PlayGame.enterPlay), never part way through...
        if self.getTutorial() != PiratesGlobals.TUT_STARTED:
            self.air.logPotentialHacker(
                message='Received giveDefaultQuest for an avatar that can not skip the tutorial!',
                tutorial=self.getTutorial())

            return

        if self.defaultQuestGiven:
            self.notify.debug('Ignoring giveDefaultQuest for avatar %d, '
                'the default quest was already given!' % self.doId)

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

        if self.air.questMgr.getQuest(self, questId=questDNA.getQuestId()):
            self.notify.warning('Failed to give default quest %s for avatar: %d, '
                'avatar already has the quest!' % (questDNA.getQuestId(), self.doId))

            return

        # the quest is created asynchronously, don't let a repeated request
        # hand out the cutlass reward again before it exists...
        self.defaultQuestGiven = True

        # skipping the tutorial also skips Will Turner's sword lesson,
        # so give the avatar the cutlass they would have received there...
        self.air.questMgr._giveRewards(self, [CutlassReward()])
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

    def getReturnIslandFromArea(self, area):
        """
        Returns the island a game area belongs to if that island is one we can return to,
        building interiors belong to the island their exterior door is on...
        """

        from pirates.world.DistributedIslandAI import DistributedIslandAI

        if isinstance(area, DistributedGAInteriorAI) and area.getIsBuilding():
            exteriorDoor = area.getExteriorFrontDoor() or area.getExteriorBackDoor()
            area = exteriorDoor.getParentObj() if exteriorDoor else None

        if not isinstance(area, DistributedIslandAI):
            return None

        world = area.getParentObj()
        if not world or not hasattr(world, 'getType') or world.getType() != PiratesGlobals.INSTANCE_MAIN:
            return None

        if area.getUniqueId() not in self.ValidReturnLocations:
            return None

        return area

    def updateReturnLocation(self, area):
        island = self.getReturnIslandFromArea(area)
        if not island:
            return

        if self.returnLocation != island.getUniqueId():
            self.b_setReturnLocation(island.getUniqueId())

    def requestReturnLocation(self, locationDoId):
        """
        Sent by the client's island or interior once it has added us to it's grid,
        we only trust the area we are actually located within...
        """

        area = self.air.doId2do.get(locationDoId)
        if not isinstance(area, DistributedGameAreaAI):
            return

        if area.doId != self.parentId:
            self.notify.debug('Ignoring return location request from avatar %d, '
                'avatar is not located within area %d!' % (self.doId, locationDoId))

            return

        self.updateReturnLocation(area)

    def requestCurrentIsland(self, locationDoId):
        """
        The client clears it's current island (0) once it is aboard a crew ship, otherwise
        it sends the island it has been added to, only accept the island we are on...
        """

        from pirates.world.DistributedIslandAI import DistributedIslandAI

        parentObj = self.getParentObj()
        if not locationDoId:
            if not isinstance(parentObj, DistributedIslandAI) and self.currentIsland:
                self.b_setCurrentIsland('')

            return

        island = self.air.doId2do.get(locationDoId)
        if not isinstance(island, DistributedIslandAI) or island is not parentObj:
            return

        if self.currentIsland != island.getUniqueId():
            self.b_setCurrentIsland(island.getUniqueId())

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

    def hasWeapon(self, weaponId):
        if weaponId in self.DefaultWeapons:
            return True

        if not WeaponGlobals.getRepId(weaponId):
            return False

        inventory = self.getInventory()
        if not inventory:
            return False

        return inventory.getStackQuantity(weaponId) > 0

    def d_setSCEmote(self, emoteId, senderChannel=None):
        self.sendUpdateToLocation('setSCEmote', [emoteId], senderChannel)

    def setSCEmote(self, emoteId):
        if self._getSpeedChatSender('setSCEmote', PChatFilter.isValidSpeedChatEmote(emoteId),
                                    'SpeedChat emote %d' % emoteId):
            self.d_setSCEmote(emoteId, self.air.getMsgSender())

    def d_setSpeedChatQuest(self, questInt, msgType, taskNum, senderChannel=None):
        self.sendUpdateToLocation('setSpeedChatQuest', [questInt, msgType, taskNum], senderChannel)

    def setSpeedChatQuest(self, questInt, msgType, taskNum):
        if self._getSpeedChatSender('setSpeedChatQuest',
                                    PChatFilter.isValidSpeedChatQuest(questInt, msgType, taskNum),
                                    'SpeedChat quest message (%d, %d, %d)' % (questInt, msgType, taskNum)):
            self.d_setSpeedChatQuest(questInt, msgType, taskNum, self.air.getMsgSender())

    def requestCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        if not self._isSenderSelf('requestCurrentWeapon', weaponId=currentWeaponId):
            return

        isWeaponDrawn = bool(isWeaponDrawn)
        if not self.hasWeapon(currentWeaponId):
            self.notify.warning('Avatar %d requested weapon %d which is not in their inventory!' % (
                self.doId, currentWeaponId))

            # the client only draws the weapons in it's inventory (LocalPirate.setEquippedWeapons)...
            if isWeaponDrawn:
                self.air.logPotentialHacker(
                    message='Received requestCurrentWeapon for a weapon the avatar does not have!',
                    currentWeaponId=currentWeaponId)

            # put away whichever weapon the avatar was using, so the
            # avatar cannot attack with a weapon it does not own...
            currentWeaponId = self.currentWeaponId if self.hasWeapon(self.currentWeaponId) else 0
            isWeaponDrawn = False

        # an avatar without a weapon has nothing to draw...
        if not currentWeaponId:
            isWeaponDrawn = False

        repId = WeaponGlobals.getRepId(currentWeaponId)
        if isWeaponDrawn and not FreebooterAI.canUseWeapon(self, repId):
            self.notify.warning('Freebooter %d attempted to draw paid weapon %d!' % (
                self.doId, currentWeaponId))

            isWeaponDrawn = False

        if self.weapon:
            self.weapon.d_setMovie(WeaponGlobals.WEAPON_MOVIE_START if isWeaponDrawn else \
                WeaponGlobals.WEAPON_MOVIE_STOP, self.doId)

        self.b_setCurrentWeapon(currentWeaponId, isWeaponDrawn)

    def requestCurrentAmmo(self, skillId):
        if skillId:
            repId = WeaponGlobals.getRepId(self.currentWeaponId)
            if not repId or WeaponGlobals.getSkillReputationCategoryId(skillId) != repId:
                self.notify.debug('Avatar %d requested ammo %d for weapon %d!' % (
                    self.doId, skillId, self.currentWeaponId))

                return

            inventory = self.getInventory()
            if not inventory or inventory.getStackQuantity(skillId) < 2:
                self.notify.debug('Avatar %d requested ammo %d they have not learned!' % (
                    self.doId, skillId))

                return

        self.b_setCurrentAmmo(skillId)

    def interrupted(self, effectId):
        # the client lets us know their charged attack was interrupted by
        # an enemy's attack, the charge is never tracked by the AI...
        if effectId != WeaponGlobals.C_INTERRUPTED:
            self.notify.debug('Avatar %d sent unknown interrupt effect %d!' % (
                self.doId, effectId))

            return

        # the other clients show the avatar being interrupted, see
        # DistributedBattleAvatar.addStatusEffect...
        self.addSkillEffect(WeaponGlobals.C_INTERRUPTED, self.InterruptedDuration, self.doId)

    def requestUseSkill(self, skillId, index):
        pass

    def requestDeployShip(self, shipId):
        pass

    def requestReturnShip(self, shipId):
        pass

    def setCurseStatus(self, curseStat):
        pass

    def d_setCurseStatus(self, curseStat):
        self.sendUpdate('setCurseStatus', [curseStat])

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

    def getSkillTrack(self, skillId):
        for repId, (begin, end, unspentId) in list(self.SkillTracks.items()):
            if begin <= skillId < end:
                return repId, unspentId

        return None, None

    def spendSkillPoint(self, skillId):
        if not self._isSenderSelf('spendSkillPoint', skillId=skillId):
            return

        inventory = self.getInventory()
        if not inventory:
            self.notify.debug('Cannot spend skill point %d for avatar %d, '
                'no inventory present' % (skillId, self.doId))

            return

        repId, unspentId = self.getSkillTrack(skillId)
        if not unspentId:
            self.notify.debug('Cannot spend skill point for skill %d,'
                'has no unspent category!' % skillId)

            return

        unspentStackQuantity = inventory.getStackQuantity(unspentId)
        skillQuantity = inventory.getStackQuantity(skillId)

        # check to see if the player has any skill points...
        if not unspentStackQuantity:
            self.notify.debug('Cannot update stack %d, player has no skill points; unspentStackQuantity=%d!' % (
                unspentId, unspentStackQuantity))

            return

        # skills are unlocked by leveling up the weapon, a skill that has
        # not been unlocked yet cannot be trained, see SkillPage.addPoint...
        if not skillQuantity or not inventory.getStackLimit(skillId):
            self.notify.debug('Cannot update stack %d, skill %d is not unlocked!' % (
                unspentId, skillId))

            return

        # check to see if the player can purchase anymore stacks
        # for this type...
        if skillQuantity >= 6:
            self.notify.debug('Cannot update stack %d, stack limit reached; skillQuantity=%d, skillLimit=5' % (
                unspentId, skillQuantity))

            return

        # in the tutorial a new pirate is shown how to train Sweep, the first
        # cutlass skill point has to go there, see SkillPage.addPoint...
        if repId == InventoryType.CutlassRep and self.getTutorial() < PiratesGlobals.TUT_GOT_CUTLASS and \
                skillId != InventoryType.CutlassSweep and inventory.getStackQuantity(InventoryType.CutlassSweep) < 2:
            self.notify.debug('Cannot update stack %d, skill %d trained before Sweep in the tutorial!' % (
                unspentId, skillId))

            return

        # freebooters may only train the skills free to use, up to a
        # certain rank and only spend so many of the weapon's skill points...
        level, _ = ReputationGlobals.getLevelFromTotalReputation(repId, inventory.getReputation(repId))
        if not FreebooterAI.canTrainSkill(self, skillId, skillQuantity + 1, level, unspentStackQuantity):
            self.notify.debug('Cannot update stack %d, freebooter %d may not train skill %d; skillQuantity=%d!' % (
                unspentId, self.doId, skillId, skillQuantity))

            return

        # combo skills must be learned in the order they are chained...
        if skillId in self.ComboOrderSkills and inventory.getStackQuantity(skillId - 1) <= 1:
            self.notify.debug('Cannot update stack %d, previous combo skill %d was never learned!' % (
                unspentId, skillId - 1))

            return

        # update the player's skill quantity and their skill
        # points quantity stack...
        inventory.b_setStackQuantity(skillId, skillQuantity + 1)
        inventory.b_setStackQuantity(unspentId, unspentStackQuantity - 1)
        self.d_spentSkillPoint(skillId)

    def resetSkillPoints(self, repId):
        # the client sends this alongside the respec option it selects on the
        # trainer (DistributedNPCTownfolk.respecTransaction), the trainer charges
        # for and performs the respec so only the request is checked here...
        if not self._isSenderSelf('resetSkillPoints', skillId=repId):
            return

        if repId not in self.SkillTracks or getNumRespecType(repId) is None:
            self.air.logPotentialHacker(
                message='Attempted to reset the skill points of an invalid weapon',
                targetAvId=self.doId,
                repId=repId)

    def d_spentSkillPoint(self, category):
        self.sendUpdateToAvatarId(self.doId, 'spentSkillPoint', [category])

    def assignQuestRewardFlag(self, flag):
        flags = BitMask32(self.getQuestRewardFlags()) | flag
        self.b_setQuestRewardFlags(flags.getWord())

    def checkQuestRewardFlag(self, flag):
        return not (self.questRewardFlags & flag).isZero()

    def setQuestRewardFlags(self, flags):
        self.questRewardFlags = BitMask32(flags)

    def d_setQuestRewardFlags(self, flags):
        self.sendUpdateToAvatarId(self.doId, 'setQuestRewardFlags', [flags])

    def b_setQuestRewardFlags(self, flags):
        self.setQuestRewardFlags(flags)
        self.d_setQuestRewardFlags(flags)

    def getQuestRewardFlags(self):
        return self.questRewardFlags

    def getHighestTonic(self):
        inventory = self.getInventory()

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
        inventory = self.getInventory()

        if not inventory:
            self.notify.warning('Failed to choose best tonic for %d; Avatar does not have an inventory' % self.doId)
            return 0

        tonics = inventory.getTonics()
        idealAmount = max(0, self.getAdjMaxHp() * 0.8 - self.getHp()[0])
        bestTonicId = 0
        for tonicId, count in sorted(tonics.items()):
            if count:
                bestTonicId = tonicId
                if WeaponGlobals.getAttackSelfHP(tonicId) > idealAmount:
                    break

        return bestTonicId

    def isSkillRecharging(self, skillId, ammoSkillId=0):
        lastUsed = self.skillRechargeTimes.get(skillId)
        if lastUsed is None:
            return False

        # allow some leeway, the client starts recharging the skill when
        # it receives the skill's result and not when it was requested...
        rechargeTime = self.air.battleMgr.getModifiedRechargeTime(self, skillId, ammoSkillId)
        return globalClock.getRealTime() - lastUsed < rechargeTime - self.RechargeTolerance

    def startSkillRecharge(self, skillId):
        self.skillRechargeTimes[skillId] = globalClock.getRealTime()

    def useTonic(self, tonicId):
        avatarId = self.air.getAvatarIdFromSender()
        if avatarId and avatarId != self.doId:
            self.air.logPotentialHacker(
                message='Attempted to use a tonic for another avatar',
                targetAvId=self.doId,
                tonicId=tonicId)

            return False

        if tonicId not in InventoryType.Potions:
            self.air.logPotentialHacker(
                message='Attempted to use an invalid tonic',
                tonicId=tonicId)

            return False

        if self.getHp()[0] <= 0:
            self.notify.debug('Avatar %d cannot use tonic %d while defeated!' % (
                self.doId, tonicId))

            return False

        # all tonics share the same recharge time...
        if self.isSkillRecharging(InventoryType.UseItem, tonicId):
            self.notify.debug('Avatar %d cannot use tonic %d, tonics are still recharging!' % (
                self.doId, tonicId))

            return False

        inventory = self.getInventory()

        if not inventory:
            self.notify.warning('Failed to choose best tonic for %d; Avatar does not have an inventory' % self.doId)
            return False

        if tonicId not in InventoryType.Potions:
            self.air.logPotentialHacker(
                message='Attempted to use an item that is not a tonic',
                tonicId=tonicId)

            return

        amount = inventory.getStackQuantity(tonicId)

        if amount <= 0:
            # This should never happen. Log it
            self.air.logPotentialHacker(
                message='Attempted to use a tonic they do not have',
                tonicId=tonicId)

            return False

        # Calculate max potential values for restoring, groggy avatars
        # cannot be restored past their adjusted max hp and mojo...
        healedHp = max(self.getHp()[0], min(WeaponGlobals.getAttackSelfHP(tonicId) + self.getHp()[0], self.getAdjMaxHp()))
        restoredMojo = max(self.getMojo(), min(WeaponGlobals.getAttackSelfMojo(tonicId) + self.getMojo(), self.getAdjMaxMojo()))
        restoredPower = max(self.getPower(), min(WeaponGlobals.getAttackSelfPower(tonicId) + self.getPower(), self.getMaxPower()))

        # Apply values
        self.b_setHp(int(healedHp))
        self.b_setMojo(int(restoredMojo))
        self.b_setPower(int(restoredPower))

        inventory.b_setStackQuantity(tonicId, amount - 1)
        self.startSkillRecharge(InventoryType.UseItem)
        return True

    def useBestTonic(self):
        tonicId = self.getBestTonic()
        if tonicId == 0:
            self.notify.debug('Failed to determine the best tonic for %d' % self.doId)
            return

        self.useTonic(tonicId)

    def flagFirstDeath(self):
        # the client displays the morale message the first time a
        # high enough level avatar is defeated, remember that it has...
        inventory = self.getInventory()
        if not inventory:
            return

        if inventory.getStackQuantity(InventoryType.FirstDeathToken) > 0:
            return

        inventory.b_setStackQuantity(InventoryType.FirstDeathToken, 1)

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
        # the doll's attunement leaves the target as well...
        for targetDoId in doIdList:
            self.air.battleMgr.unattuneTarget(self, targetDoId)

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

    def setLootCarried(self, lootCarried, maxCarry):
        self.lootCarried = lootCarried
        self.maxLootCarried = maxCarry

    def d_setLootCarried(self, lootCarried, maxCarry):
        self.sendUpdate('setLootCarried', [lootCarried, maxCarry])

    def b_setLootCarried(self, lootCarried, maxCarry):
        self.setLootCarried(lootCarried, maxCarry)
        self.d_setLootCarried(lootCarried, maxCarry)

    def getLootCarried(self):
        return [self.lootCarried, self.maxLootCarried]

    def setZombie(self, zombie, cursed=False):
        self.zombie = zombie

    def d_setZombie(self, zombie, cursed=False):
        self.sendUpdate('setZombie', [zombie, cursed])

    def b_setZombie(self, zombie, cursed=False):
        self.setZombie(zombie, cursed)
        self.d_setZombie(zombie, cursed)

    def getZombie(self):
        return self.zombie

    def isUndead(self):
        # see DistributedPlayerPirate.isUndead and TeamUtils.friendOrFoe...
        return bool(self.zombie)

    def attemptToSetCursedZombie(self):
        # avatars stay zombies while the zombie magic word forces them to be one,
        # or while Jolly Roger's Curse has them cursed...
        jollyCurseMgr = getattr(self.air, 'jollyCurseMgr', None)
        cursed = bool(jollyCurseMgr and jollyCurseMgr.isAvatarCursed(self.doId))
        zombie = int(bool(self.forcedZombie or cursed))
        if zombie != self.zombie:
            self.b_setZombie(zombie, zombie)

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
        # updateGMNameTag is ownsend, the state server has already broadcast the
        # client's value; only an avatar the AI allowed a GM nametag may set one...
        if self.air.getAccountIdFromSender() and not self.gmNameTagAllowed:
            self.air.logPotentialHacker(
                message='Received updateGMNameTag from an avatar without a GM nametag!',
                targetAvId=self.doId,
                gmNameTagState=gmNameTagState,
                gmNameTagColor=gmNameTagColor,
                gmNameTagString=gmNameTagString)

            self.d_updateGMNameTag(*self.getGMNameTag())
            return

        self._setGMNameTag(gmNameTagState, gmNameTagColor, gmNameTagString)

    def _setGMNameTag(self, gmNameTagState, gmNameTagColor, gmNameTagString):
        self.gmNameTagState = gmNameTagState
        self.gmNameTagColor = gmNameTagColor
        self.gmNameTagString = gmNameTagString

    def getGMNameTag(self):
        return [self.gmNameTagState, self.gmNameTagColor, self.gmNameTagString]

    def d_updateGMNameTag(self, gmNameTagState, gmNameTagColor, gmNameTagString):
        self.sendUpdate('updateGMNameTag', [gmNameTagState, gmNameTagColor, gmNameTagString])

    def b_updateGMNameTag(self, gmNameTagState, gmNameTagColor, gmNameTagString):
        self.d_updateGMNameTag(gmNameTagState, gmNameTagColor, gmNameTagString)
        self._setGMNameTag(gmNameTagState, gmNameTagColor, gmNameTagString)

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
        self.stopToonUp()
        self.toonUpTask = taskMgr.doMethodLater(self.ToonUpTime, self.toonUp, self.taskName('toonUp'))

    def toonUp(self, task):
        hp = self.getHp()[0]

        # defeated avatars do not regenerate, they are healed by the jail...
        if hp <= 0:
            return task.again

        # the avatar's health does not regenerate while it is fighting a target...
        inBattle = self.isInBattle()
        maxHp = self.getAdjMaxHp()
        maxMojo = self.getAdjMaxMojo()
        if hp < maxHp and not inBattle:
            self.b_setHp(min(maxHp, hp + max(1, int(10 * self.getLevel() / 1.25))))

        if self.getMojo() < maxMojo:
            mojoRegen = max(1, int(8 * self.getLevel() / 1.35))
            if inBattle:
                mojoRegen = max(1, mojoRegen // self.BattleMojoRegenDivisor)

            self.b_setMojo(min(maxMojo, self.getMojo() + mojoRegen))

        return task.again

    def stopToonUp(self):
        if self.toonUpTask:
            taskMgr.remove(self.toonUpTask)
            self.toonUpTask = None

    def setActiveShipId(self, activeShipId):
        self.activeShipId = activeShipId
        if self.isGenerated():
            self.air.bandManager.updateAvatarShipInfo(self)

    def d_setActiveShipId(self, activeShipId):
        self.sendUpdate('setActiveShipId', [activeShipId])

    def b_setActiveShipId(self, activeShipId):
        self.setActiveShipId(activeShipId)
        self.d_setActiveShipId(activeShipId)

    def getActiveShipId(self):
        return self.activeShipId

    @property
    def ship(self):
        # the ship the avatar is aboard, the battle formulas shared with the client
        # look at the ship's buffs through it (see BattleManagerBase.getModifiedRechargeTime)...
        crewShipId = getattr(self, 'crewShipId', 0)
        if not crewShipId:
            return None

        return self.air.doId2do.get(crewShipId)

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

    def setOnWelcomeWorld(self, onWelcomeWorld):
        self.onWelcomeWorld = onWelcomeWorld

    def getOnWelcomeWorld(self):
        return self.onWelcomeWorld

    def enterAreaSphere(self, uniqueId, parentUid):
        # the client tells us whenever its avatar walks into one of the named
        # locations (location spheres) of an area, we echo the location back
        # so that the client shows it on the radar...
        if not self._isSenderSelf('enterAreaSphere', uniqueId=uniqueId):
            return

        if uniqueId not in PLocalizer.LocationNames:
            return

        # the spheres of the area the avatar was in before no longer apply...
        self.areaSphereStack = [(sphereUid, sphereParentUid) for sphereUid, sphereParentUid in self.areaSphereStack
                                if sphereParentUid == parentUid and sphereUid != uniqueId]
        self.areaSphereStack.append((uniqueId, parentUid))
        self.d_locationChange(uniqueId)

    def leaveAreaSphere(self, uniqueId, parentUid):
        if not self._isSenderSelf('leaveAreaSphere', uniqueId=uniqueId):
            return

        if (uniqueId, parentUid) not in self.areaSphereStack:
            return

        self.areaSphereStack.remove((uniqueId, parentUid))

        # the avatar is back in the location it was in before, or in the area itself...
        if self.areaSphereStack:
            self.d_locationChange(self.areaSphereStack[-1][0])
        elif parentUid in PLocalizer.LocationNames:
            self.d_locationChange(parentUid)

    def d_locationChange(self, locationName):
        self.sendUpdateToAvatarId(self.doId, 'locationChange', [locationName])

    def getAreaSphereUid(self):
        if self.areaSphereStack:
            return self.areaSphereStack[-1][0]

        return ''

    def setBadgeIcon(self, titleId, rank):
        self.badgeIcon = (titleId, rank)

    def d_setBadgeIcon(self, titleId, rank):
        self.sendUpdate('setBadgeIcon', [titleId, rank])

    def b_setBadgeIcon(self, titleId, rank):
        self.setBadgeIcon(titleId, rank)
        self.d_setBadgeIcon(titleId, rank)

    def getBadgeIcon(self):
        return self.badgeIcon

    def setShipBadgeIcon(self, titleId, rank):
        self.shipBadgeIcon = (titleId, rank)

    def d_setShipBadgeIcon(self, titleId, rank):
        self.sendUpdate('setShipBadgeIcon', [titleId, rank])

    def b_setShipBadgeIcon(self, titleId, rank):
        self.setShipBadgeIcon(titleId, rank)
        self.d_setShipBadgeIcon(titleId, rank)

    def getShipBadgeIcon(self):
        return self.shipBadgeIcon

    def __hasTitleRank(self, titleId, rank):
        """
        Returns True if the avatar has earned the title at least up to the rank,
        the rank is worked out from the title's inventory stack as the client's
        TitlesPage does it.
        """

        if titleId not in TitleGlobals.TitlesDict:
            return False

        if rank < 0 or rank > TitleGlobals.getMaxRank(titleId):
            return False

        inventoryType = TitleGlobals.getInventoryType(titleId)
        inventory = self.getInventory()
        if not inventoryType or not inventory:
            return rank == 0

        return rank <= TitleGlobals.getRank(titleId, inventory.getStackQuantity(inventoryType))

    def requestBadgeIcon(self, titleId, rank):
        if not self._isSenderSelf('requestBadgeIcon', titleId=titleId, rank=rank):
            return

        # a negative title or rank takes the badge off...
        if titleId < 0 or rank < 0:
            self.b_setBadgeIcon(-1, -1)
            return

        if not self.__hasTitleRank(titleId, rank):
            self.air.logPotentialHacker(
                message='Requested a badge for a title rank the avatar has not earned!',
                targetAvId=self.doId,
                titleId=titleId,
                rank=rank)

            return

        self.b_setBadgeIcon(titleId, rank)

    def requestShipBadgeIcon(self, titleId, rank):
        if not self._isSenderSelf('requestShipBadgeIcon', titleId=titleId, rank=rank):
            return

        if titleId < 0 or rank < 0:
            self.b_setShipBadgeIcon(-1, -1)
            return

        if not self.__hasTitleRank(titleId, rank):
            self.air.logPotentialHacker(
                message='Requested a ship badge for a title rank the avatar has not earned!',
                targetAvId=self.doId,
                titleId=titleId,
                rank=rank)

            return

        self.b_setShipBadgeIcon(titleId, rank)

    def isPaid(self):
        return FreebooterAI.isPaidAccess(self.getGameAccess())

    def getAccess(self):
        # with want-membership off everybody has Unlimited Access,
        # see DistributedPlayerPirate.getAccess...
        return FreebooterAI.getEffectiveAccess(self.getGameAccess())

    def setAccess(self, access):
        self.setGameAccess(access)

    def d_setAccess(self, access):
        self.sendUpdate('setAccess', [access])

    def b_setAccess(self, access):
        self.setAccess(access)
        self.d_setAccess(access)

    def setGameAccess(self, access):
        self.gameAccess = access

    def getGameAccess(self):
        return getattr(self, 'gameAccess', OTPGlobals.AccessUnknown)

    def disable(self):
        DistributedPlayerAI.disable(self)
        DistributedBattleAvatarAI.disable(self)

    def delete(self):
        jollyCurseMgr = getattr(self.air, 'jollyCurseMgr', None)
        if jollyCurseMgr:
            jollyCurseMgr.avatarLeft(self)

        # the targets our doll was attuned to are no longer attuned...
        for targetDoId in list(self.stickyTargets):
            target = self.air.doId2do.get(targetDoId)
            if target and hasattr(target, 'removeSkillEffect'):
                target.removeSkillEffect(WeaponGlobals.C_ATTUNE, self.doId)

        self.air.targetMgr.clearAttacker(self)
        self.air.worldGridManager.clearAvatarInterests(self)
        inventory = self.getInventory()
        if inventory:
            self.air.questMgr.deactivateQuests(self)
            self.air.inventoryManager.removeInventory(inventory)

        taskMgr.remove(self.uniqueName('process-groggy'))
        taskMgr.remove(self.uniqueName('process-double-xp'))
        self.stopToonUp()

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

        for levelIndex in range(level):
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
    inventory = base.air.inventoryManager.getInventory(invoker.doId)
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
def guildname(name):
    spellbook.getInvoker().b_setGuildName(name)
    return "Set Guild Name to %s" % name

@magicWord(category=CATEGORY_SYSTEM_ADMIN)
def immortal():
    avatar = spellbook.getInvoker()
    avatar.setImmortal(not avatar.getImmortal())
    return 'Immortal state set to: %s' % avatar.getImmortal()

@magicWord(category=CATEGORY_SYSTEM_ADMIN, types=[int])
def access(access=-1):
    """
    Interface for manually verifying or changing your ingame access level
    """

    if access != -1:
        if access < 0 or access > 2:
            return 'Invalid access level 0-2'

        spellbook.getInvoker().b_setAccess(access)
        return 'Access level changed: %d' % access
    else:
        access = spellbook.getInvoker().getAccess()
        if access == Freebooter.NONE:
            msg = 'Unpaid'
        elif access == Freebooter.VELVET_ROPE:
            msg = 'Velvet Rope'
        elif access == Freebooter.FULL:
            msg = 'Full'
        return '%s (%s)' % (msg, int(access))
