# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.DistributedPlayerPirate
import string

import PlayerPirateGameFSM
from direct.actor import Actor
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedNode, PyDatagram
from direct.distributed.ClockDelta import *
from direct.distributed.MsgTypes import *
from direct.gui import DirectLabel
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from direct.showbase.PythonUtil import Functor, report
from direct.task import Task
from otp.avatar.DistributedPlayer import DistributedPlayer
from otp.chat import ChatGlobals
from otp.otpbase import OTPGlobals, OTPLocalizer
from pandac.PandaModules import TextProperties, TextPropertiesManager
from pirates.band import BandConstance, DistributedBandMember
from pirates.battle import Consumable, WeaponGlobals
from pirates.battle.DistributedBattleAvatar import DistributedBattleAvatar
from pirates.coderedemption import CodeRedemption
from pirates.demo import DemoGlobals
from pirates.effects.LevelUpEffect import LevelUpEffect
from pirates.effects.VoodooAura import VoodooAura
from pirates.effects.WaterRipple import WaterRipple
from pirates.effects.WaterRippleSplash import WaterRippleSplash
from pirates.effects.WaterRippleWake import WaterRippleWake
from pirates.npc import Skeleton
from pirates.pirate import AvatarTypes, Biped, TitleGlobals
from pirates.pirate.DistributedPirateBase import DistributedPirateBase
from pirates.pirate.PAvatarHandle import PAvatarHandle
from pirates.piratesbase import (Freebooter, PiratesGlobals, PLocalizer,
                                 TeamUtils, UserFunnel)
from pirates.piratesgui import (CrewIconSelector, NamePanelGui,
                                PiratesGuiGlobals)
from pirates.pvp import PVPGlobals
from pirates.quest.DistributedQuestAvatar import DistributedQuestAvatar
from pirates.quest.QuestConstants import LocationIds
from pirates.reputation import ReputationGlobals
from pirates.speedchat import PSCDecoders
from pirates.uberdog.UberDogGlobals import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.world.DistributedGameArea import DistributedGameArea


class DistributedPlayerPirate(DistributedPirateBase, DistributedPlayer, DistributedBattleAvatar, DistributedQuestAvatar, PAvatarHandle):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPirate')
    wantBattle = base.config.GetBool('want-battle', 1)
    deferrable = True
    GoldFounderIcon = None
    SilverFounderIcon = None
    crewIconId = None
    tempDoubleXPStatus = None
    badgeIconDict = None
    gmNameTag = None

    def __init__(self, cr):
        try:
            self.DistributedPirate_initialized
        except:
            self.DistributedPirate_initialized = 1
            self.onWelcomeWorld = False
            if not self.GoldFounderIcon:
                gui = loader.loadModel('models/gui/toplevel_gui')
                self.GoldFounderIcon = gui.find('**/founders_coin').copyTo(NodePath('coinTop'))
                self.GoldFounderIcon.setScale(2.8)
                self.SilverFounderIcon = gui.find('**/founders_silver_coin').copyTo(NodePath('coinTop'))
                self.SilverFounderIcon.setScale(2.8)
                tpMgr = TextPropertiesManager.getGlobalPtr()
                tpMgr.setGraphic('goldFounderIcon', self.GoldFounderIcon)
                tpMgr.setGraphic('silverFounderIcon', self.SilverFounderIcon)
                gold = TextProperties()
                gold.setTextColor(1, 0.8, 0.4, 1)
                tpMgr.setProperties('goldFounder', gold)
                silver = TextProperties()
                silver.setTextColor(0.75, 0.75, 0.75, 1)
                tpMgr.setProperties('silverFounder', silver)
                crewPurpleColor = TextProperties()
                crewPurpleColor.setTextColor(0.9, 0.5, 95, 1)
                tpMgr.setProperties('crewPurple', crewPurpleColor)
            if not self.tempDoubleXPStatus:
                x2XPGui = loader.loadModel('models/gui/toplevel_gui')
                self.x2XPIcon = gui.find('**/2xp')
                self.x2XPIcon.setScale(4.5)
                tpMgr.setGraphic('x2XPAwardIcon', self.x2XPIcon)
            if not self.crewIconId:
                self.crewIconId = True
                crewIconGui = loader.loadModel(CrewIconSelector.CREW_ICON_BAM)
                self.crewIconDict = {}
                for k, v in CrewIconSelector.CREW_ICONS.iteritems():
                    np = crewIconGui.find('**/%s' % v)
                    self.crewIconDict[k] = np.copyTo(NodePath())
                    self.crewIconDict[k].setScale(8.8)
                    if k == 1:
                        np = crewIconGui.find('**/icon_glow')
                        self.myCrewColorGlow = np.copyTo(self.crewIconDict[k])
                        self.myCrewColorGlow.setScale(1.25)
                        self.myCrewColorGlow.setColor(0, 1, 0, 1)
                    else:
                        if k == 2:
                            np = crewIconGui.find('**/icon_glow')
                            self.otherCrewColorGlow = np.copyTo(self.crewIconDict[k])
                            self.otherCrewColorGlow.setScale(1.25)
                            self.otherCrewColorGlow.setColor(1, 0, 0, 1)
                    tpMgr.setGraphic('crewIcon%s' % k, self.crewIconDict[k])

            if not self.badgeIconDict:
                self.badgeIconDict = {}
                for titleId in TitleGlobals.TitlesDict.keys():
                    titleModel = loader.loadModel(TitleGlobals.getModelPath(titleId))
                    for rank in range(TitleGlobals.getMaxRank(titleId) + 1):
                        icName = TitleGlobals.getIconName(titleId, rank)
                        if not icName:
                            continue
                        icon = titleModel.find('**/' + icName)
                        if not icon:
                            continue
                        imgScale = TitleGlobals.getScale(titleId)
                        icon.setScale(1.0 * imgScale)
                        iconKey = 'badge-%s-%s' % (titleId, rank)
                        self.badgeIconDict[iconKey] = icon
                        tpMgr.setGraphic(iconKey, icon)

            if not self.gmNameTag:
                self.gmNameTagIcon = loader.loadModel('models/gui/gmLogo_tflip')
                self.gmNameTagIcon.setScale(2.5)
                tpMgr.setGraphic('gmNameTagLogo', self.gmNameTagIcon)
                gmGoldColor = TextProperties()
                gmGoldColor.setTextColor(1, 0.9, 0.7, 1)
                tpMgr.setProperties('goldGM', gmGoldColor)
                gmRedColor = TextProperties()
                gmRedColor.setTextColor(1.0, 0.1, 0.1, 1)
                tpMgr.setProperties('redGM', gmRedColor)
                gmGreenColor = TextProperties()
                gmGreenColor.setTextColor(0.3, 0.7, 0.25, 1)
                tpMgr.setProperties('greenGM', gmGreenColor)
                gmBlueColor = TextProperties()
                gmBlueColor.setTextColor(0.35, 0.7, 1, 1)
                tpMgr.setProperties('blueGM', gmBlueColor)
                gmWhiteColor = TextProperties()
                gmWhiteColor.setTextColor(1, 1, 1, 1)
                tpMgr.setProperties('whiteGM', gmWhiteColor)
            self.name = ''
            self.title = ''
            DistributedPirateBase.__init__(self, cr)
            DistributedBattleAvatar.__init__(self, cr)
            DistributedPlayer.__init__(self, cr)
            DistributedQuestAvatar.__init__(self)
            self.inPvp = False
            self.setPickable(1)
            self.interactioneer = None
            self.crewShip = None
            self.crewShipId = 0
            self.pendingSetCrewShip = None
            self.activeShipId = 0
            self.pendingTeleportMgr = None
            self.crewInterest = None
            self.captainId = 0
            self.chestIcon = None
            self.lootCarried = 0
            self.inventoryId = 0
            self.undead = 0
            self.undeadStyle = ''
            self.skeleton = None
            self.stickyTargets = []
            self.attuneEffect = None
            self.avatarFriendsList = set()
            self.playerFriendsList = set()
            self.guildName = PLocalizer.GuildNoGuild
            self.guildId = -1
            self.guildRank = -1
            self.defaultShard = 0
            self.returnLocation = ''
            self.currentIsland = ''
            self.jailCellIndex = 100
            self.beacon = None
            self.teleportFriendDoId = 0
            self.teleportFlags = PiratesGlobals.TFInInitTeleport
            self.teleportConfirmCallbacks = {}
            self.questRewardFlags = 0
            self.bandMember = None
            self.gameAccess = OTPGlobals.AccessUnknown
            self.founder = False
            self.port = 0
            self.waterRipple = None
            self.waterWake = None
            self.waterSplash = None
            self.emoteId = 0
            self.emote_track = None
            self.emote_prop = None
            self.founderIcon = None
            self.badge = None
            self.shipBadge = None
            self.isLookingForCrew = 0
            self.tutorialState = 0
            self.hasCrewIcon = 0
            self.isAFK = False
            self.status = 0
            self.isPaid = False
            self.updatePaidStatus()
            self.tempDoubleXPStatus = 0
            self.tempDoubleXPStatusMessaged = False
            self.gmNameTagAllowed = 0
            self.gmNameTagEnabled = 0
            self.gmNameTagColor = 'whiteGM'
            self.gmNameTagString = ''
            self.BandId = None
            self.cursed = False

        return

    def disable(self):
        DistributedPirateBase.disable(self)
        DistributedPlayer.disable(self)
        DistributedBattleAvatar.disable(self)
        self.stopBlink()
        self.ignoreAll()
        self.hideBeacon()
        if self.consumable:
            self.consumable.delete()
            self.consumable = None
        self.crewShip = None
        if self.pendingSetCrewShip:
            self.cr.relatedObjectMgr.abortRequest(self.pendingSetCrewShip)
            self.pendingSetCrewShip = None
        if self.attuneEffect:
            self.attuneEffect.stopLoop()
            self.attuneEffect = None
        if self.waterRipple:
            self.waterRipple.stopLoop()
            self.waterRipple = None
        if self.waterWake:
            self.waterWake.stopLoop()
            self.waterWake = None
        if self.waterSplash:
            self.waterSplash.stopLoop()
            self.waterSplash = None
        if self.pendingTeleportMgr:
            base.cr.relatedObjectMgr.abortRequest(self.pendingTeleportMgr)
            self.pendingTeleportMgr = None
        if self.emote_track is not None:
            self.emote_track.pause()
            self.emote_track = None
        if self.emote_prop is not None:
            self.emote_prop.removeNode()
            self.emote_prop = None
        self.port = 0
        return

    def delete(self):
        try:
            self.DistributedPlayerPirate_deleted
        except:
            self.DistributedPlayerPirate_deleted = 1
            DistributedPirateBase.delete(self)
            DistributedPlayer.delete(self)
            DistributedBattleAvatar.delete(self)
            DistributedQuestAvatar.delete(self)
            if self.skeleton:
                self.skeleton.delete()
                self.skeleton = None

        return

    def generate(self):
        DistributedPirateBase.generate(self)
        DistributedPlayer.generate(self)
        DistributedBattleAvatar.generate(self)
        self.setDefaultDNA()
        if not self.isLocal():
            if self.getTeam() == localAvatar.getTeam():
                allowInteract = False
            else:
                allowInteract = True
            self.setInteractOptions(proximityText='', mouseOver=0, mouseClick=0, isTarget=1, allowInteract=allowInteract)
        self.setPlayerType(NametagGroup.CCNormal)

    def setTeam(self, team):
        DistributedBattleAvatar.setTeam(self, team)
        if team:
            localAvatar.guiMgr.crewPage.crewHUD.setHUDOff()
            localAvatar.guiMgr.crewHUDTurnedOff = False
            localAvatar.guiMgr.crewPage.deactivateCrewHUDButton()
        else:
            localAvatar.guiMgr.crewPage.activateCrewHUDButton()
        if not self.isLocal():
            if self.getTeam() == localAvatar.getTeam():
                self.setAllowInteract(False)
            else:
                self.setAllowInteract(True)

    def setPVPTeam(self, team):
        DistributedBattleAvatar.setPVPTeam(self, team)
        self.setBeacon(team)

    def setBeacon(self, team):
        if self.isLocal():
            localAvatar.guiMgr.showPVPTeamIcon(team)
        else:
            self.showBeacon(team)

    def createGameFSM(self):
        self.gameFSM = PlayerPirateGameFSM.PlayerPirateGameFSM(self)

    def announceGenerate(self):
        DistributedPirateBase.announceGenerate(self)
        DistributedPlayer.announceGenerate(self)
        DistributedBattleAvatar.announceGenerate(self)
        self.setName(self.name)
        self.setLOD(500, 5000, self.switches[500][1])
        self.checkAttuneEffect()
        if base.launcher.getPhaseComplete(4):
            self.createConsumable()
        else:
            self.consumable = None
            self.accept('phaseComplete-4', self.handlePhaseComplete, extraArgs=[4])
        self.initVisibleToCamera()
        yieldThread('current Item')
        return

    def handlePhaseComplete(self, phase):
        if phase == 4:
            self.createConsumable()

    def createConsumable(self):
        self.consumable = Consumable.Consumable(InventoryType.Potion1)

    def setLocation(self, parentId, zoneId, teleport=0):
        DistributedBattleAvatar.setLocation(self, parentId, zoneId, teleport)

    def wrtReparentTo(self, parent):
        DistributedBattleAvatar.wrtReparentTo(self, parent)

    def setName(self, name):
        DistributedBattleAvatar.setName(self, name)
        self.refreshName()

    def setCrewIcon(self, iconId):
        self.sendUpdate('setCrewIconIndicator', [iconId])
        self.hasCrewIcon = iconId
        self.setCrewIconIndicator(iconId)

    def getCrewIcon(self):
        return self.hasCrewIcon

    def setCrewIconIndicator(self, iconId):
        if self.getDoId() != localAvatar.getDoId() and iconId != 0:
            if self.getDoId() not in localAvatar.guiMgr.crewPage.crew:
                iconId = 2
        self.hasCrewIcon = iconId
        self.refreshName()

    def setBadgeIcon(self, titleId, rank):
        self.badge = (
         titleId, rank)
        if titleId < 0 or rank < 0:
            self.badge = None
        self.refreshName()
        return

    def setShipBadgeIcon(self, titleId, rank):
        self.shipBadge = (
         titleId, rank)
        if titleId < 0 or rank < 0:
            self.shipBadge = None
        return

    def sendRequestSetBadgeIcon(self, titleId, rank):
        self.sendUpdate('requestBadgeIcon', [titleId, rank])

    def sendRequestSetShipBadgeIcon(self, titleId, rank):
        self.sendUpdate('requestShipBadgeIcon', [titleId, rank])

    def setStatus(self, status):
        self.isLookingForCrew = status & PiratesGlobals.STATUS_LFG
        self.isAFK = status & PiratesGlobals.STATUS_AFK
        self.refreshName()

    def d_refreshStatus(self):
        status = 0
        if self.isAFK:
            status += PiratesGlobals.STATUS_AFK
        if self.isLookingForCrew:
            status += PiratesGlobals.STATUS_LFG
        self.sendUpdate('setStatus', [status])

    def toggleLookingForCrewSign(self):
        try:
            localAvatar.guiMgr.crewPage.toggleLookingForCrew()
        except:
            pass

    def setLookingForCrew(self, state):
        self.isLookingForCrew = state
        self.refreshName()
        self.d_refreshStatus()

    def getLookingForCrew(self):
        return self.isLookingForCrew

    def b_setAFK(self, isAFK):
        self.isAFK = isAFK
        self.refreshName()
        self.d_refreshStatus()

    def refreshName(self):
        self.refreshStatusTray()
        if hasattr(self, 'nametag'):
            self.nametag.setName(self.getName())
            self.nametag.setDisplayName('        ')
        if self.guildName == '0' or self.guildName == '':
            guildName = PLocalizer.GuildDefaultName % self.guildId
        else:
            guildName = self.guildName
        nameText = self.getNameText()
        if nameText:
            level = self.getLevel()
            if self.inPvp and self != localAvatar:
                levelColor = self.cr.battleMgr.getExperienceColor(base.localAvatar, self)
            else:
                levelColor = '\x01white\x01'
            x2XPTempAwardIndicator = ''
            if self.tempDoubleXPStatus:
                x2XPTempAwardIndicator = 'x2XPAwardIcon'
            if self.guildName == PLocalizer.GuildNoGuild:
                text = '%s%s  \x01smallCaps\x01%s%s%s\x05%s\x05\x02\x02' % (self.title, self.name, levelColor, PLocalizer.Lv, level, x2XPTempAwardIndicator)
            else:
                text = '%s%s  \x01smallCaps\x01%s%s%s\x05%s\x05\x02\x02\n\x01guildName\x01%s\x02' % (self.title, self.name, levelColor, PLocalizer.Lv, level, x2XPTempAwardIndicator, guildName)
            nameText['text'] = text
            if not base.config.GetBool('want-titles-page', 0):
                if Freebooter.getPaidStatus(self.doId):
                    if self.getFounder():
                        nameText['fg'] = (1, 1, 1, 1)
                        nameText['font'] = PiratesGlobals.getPirateOutlineFont()
                        nameText['text'] = '\x05goldFounderIcon\x05 \x01goldFounder\x01%s\x02' % text
                    else:
                        nameText['fg'] = (0.4, 0.3, 0.95, 1)
                        nameText['font'] = PiratesGlobals.getPirateOutlineFont()
                else:
                    nameText['fg'] = (0.5, 0.5, 0.5, 1)
            prefix = ''
            if self.isAFK:
                prefix = '\x01crewPurple\x01%s\x02\n' % PLocalizer.AFKFlag
            else:
                if self.getLookingForCrew():
                    prefix = '\x01crewPurple\x01%s\x02\n' % PLocalizer.CrewLookingForAd
            badges = ''
            if self.badge and base.config.GetBool('want-titles-page', 0):
                badges += '\x05badge-%s-%s\x05 ' % (self.badge[0], self.badge[1])
            nameText['text'] = prefix + badges + nameText['text']
            if self.getCrewIcon() and not self.gmNameTagEnabled:
                if self.getCrewIcon() != 2:
                    oldLabelText = nameText['text']
                    nameText['text'] = '\x05crewIcon%s\x05\n%s' % (self.hasCrewIcon, oldLabelText)
            if self.gmNameTagEnabled and self.gmNameTagAllowed:
                if self.getCrewIcon():
                    nameText['text'] = '\x05gmNameTagLogo\x05\x05crewIcon%s\x05\n\x01%s\x01%s\x02\n%s' % (self.hasCrewIcon, self.getGMNameTagColor(), self.gmNameTagString, nameText['text'])
                else:
                    nameText['text'] = '\x05gmNameTagLogo\x05\n\x01%s\x01%s\x02\n%s' % (self.getGMNameTagColor(), self.gmNameTagString, nameText['text'])

    def setTutorialAck(self, tutorialAck):
        self.tutorialAck = tutorialAck

    def getInventoryId(self):
        return self.inventoryId

    def setInventoryId(self, inventoryId):
        self.inventoryId = inventoryId

    def getInventory(self):
        if not self:
            return
        if not self.cr:
            return
        inventory = self.cr.doId2do.get(self.inventoryId)
        if inventory:
            return inventory
        else:
            return
        return

    def getFriendsListId(self):
        pass

    def setFriendsListId(self, friendsListId):
        pass

    def getFriendsList(self):
        return self.avatarFriendsList

    def getAvatarFriendsList(self):
        return self.avatarFriendsList

    def getPlayerFriendsList(self):
        return self.playerFriendsList

    def getName(self):
        return self.title + self.name

    def setGuildName(self, newname):
        if newname == 'Null':
            self.guildName = PLocalizer.GuildNoGuild
        else:
            self.guildName = newname
        self.refreshName()

    def getGuildName(self):
        return self.guildName

    def setGuildRank(self, rank):
        self.guildRank = rank

    def getGuildRank(self):
        return self.guildRank

    def getGuildId(self):
        return self.guildId

    def setGuildId(self, guildId):
        self.guildId = guildId

    def getCrewMemberId(self):
        return self.crewMemberId

    def setCrewMemberId(self, crewMemberId):
        self.crewMemberId = crewMemberId

    def getDinghyId(self):
        return self.dinghyId

    def setDinghyId(self, dinghyId):
        self.dinghyId = dinghyId

    def getDinghy(self):
        return self.cr.doId2do.get(self.dinghyId)

    def setDNAString(self, dnaString):
        DistributedPirateBase.setDNAString(self, dnaString)

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-shipboard-report')
    def b_setActiveShipId(self, shipId):
        self.d_setActiveShipId(shipId)
        self.setActiveShipId(shipId)

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-shipboard-report')
    def d_setActiveShipId(self, shipId):
        self.sendUpdate('setActiveShipId', [shipId])

    @report(types=['deltaStamp', 'module', 'args'], dConfigParam='want-shipboard-report')
    def setActiveShipId(self, shipId):
        if shipId and localAvatar.getDoId() == self.getDoId():
            messenger.send('localAvatarToSea')
        else:
            if not shipId and localAvatar.getDoId() == self.getDoId():
                messenger.send('localAvatarToLand')
        self.activeShipId = shipId

    def getActiveShip(self):
        return self.cr.doId2do.get(self.activeShipId)

    def getActiveShipId(self):
        return self.activeShipId

    @report(types=['deltaStamp', 'module', 'args'], dConfigParam='want-shipboard-report')
    def setCrewShipId(self, shipId):
        if self.pendingSetCrewShip:
            self.cr.relatedObjectMgr.abortRequest(self.pendingSetCrewShip)
            self.pendingSetCrewShip = None
        self.crewShipId = shipId
        if shipId:
            self.pendingSetCrewShip = self.cr.relatedObjectMgr.requestObjects([shipId], eachCallback=self._setCrewShip)
            messenger.send('localAvatarToSea')
        else:
            self._setCrewShip(None)
            messenger.send('localAvatarToLand')
        return

    def getCrewShipId(self):
        return self.crewShipId

    @report(types=['deltaStamp', 'module', 'args'], dConfigParam='want-shipboard-report')
    def _setCrewShip(self, ship):
        self.crewShip = ship

    def getCrewShip(self):
        return self.crewShip

    def printShips(self):
        print 'activeShip:\t', self.getActiveShipId(), self.getActiveShip()
        print 'crewShip:\t', self.getCrewShipId(), self.getCrewShip()
        print 'ship:\t\t', self.getShip(), self.getShip()

    def getShipString(self):
        return 'A: %s, C: %s, S: %s' % (self.getActiveShipId(), self.getCrewShipId(), self.getShipId())

    def hpChange(self, quietly=0):
        DistributedBattleAvatar.hpChange(self, quietly)

    def updateReputation(self, category, value):
        DistributedBattleAvatar.updateReputation(self, category, value)

    def useTargetedSkill(self, skillId, ammoSkillId, actualResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, timestamp, pos, charge=0, localSignal=0):
        targetEffects = list(targetEffects)
        attackerEffects = list(attackerEffects)
        DistributedBattleAvatar.useTargetedSkill(self, skillId, ammoSkillId, actualResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, timestamp, pos, charge, localSignal)

    def playSkillMovie(self, skillId, ammoSkillId, skillResult, charge=0, targetId=0):
        DistributedBattleAvatar.playSkillMovie(self, skillId, ammoSkillId, skillResult, charge, targetId)

    @report(types=['deltaStamp', 'module'], prefix='------', dConfigParam='want-teleport-report')
    def forceTeleportStart(self, instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone):

        def effectDoneCallback():
            self.cr.teleportMgr.forceTeleportStart(instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone)

        if self.cr.teleportMgr.doEffect and not self.testTeleportFlag(PiratesGlobals.TFInInitTeleport) and not self.testTeleportFlag(PiratesGlobals.TFInWater):
            self.acceptOnce('avatarTeleportEffect-done', effectDoneCallback)
            self.b_setGameState('TeleportOut', ['avatarTeleportEffect-done'])
        else:
            effectDoneCallback()
        self.cr.teleportMgr.doEffect = True

    @report(types=['deltaStamp', 'module', 'args'], prefix='------', dConfigParam='want-teleport-report')
    def relayTeleportLoc(self, shardId, zoneId, teleportMgrDoId):
        self.b_setDefaultShard(shardId)
        self.cr.playingGameLocReceived(shardId, self.doId)
        if self.pendingTeleportMgr:
            base.cr.relatedObjectMgr.abortRequest(self.pendingTeleportMgr)
            self.pendingTeleportMgr = None
        self.pendingTeleportMgr = base.cr.relatedObjectMgr.requestObjects([teleportMgrDoId], eachCallback=self.readyToTeleport)
        return

    @report(types=['deltaStamp', 'module'], prefix='------', dConfigParam='want-teleport-report')
    def readyToTeleport(self, teleportMgr):
        teleportMgr.initiateTeleport(self.teleportToType, self.teleportToName, shardId=self.getDefaultShard(), locationUid=self.returnLocation)

    def requestActivityAccepted(self):
        self.guiMgr.lookoutPage.requestActivityAccepted()

    def lookoutMatchFound(self, timeToJoin, matchId):
        self.guiMgr.lookoutPage.matchFound(matchId, timeToJoin)

    def lookoutMatchFailed(self, restartRequest):
        self.guiMgr.lookoutPage.matchFailed(restartRequest)

    def lookoutFeedback(self, matchChance):
        self.guiMgr.lookoutPage.matchChance(matchChance)

    def beginningTeleport(self, instanceType, fromInstanceType, instanceName, gameType):
        base.cr.loadingScreen.showTarget()
        self.cr.teleportMgr.teleportHasBegun(instanceType, fromInstanceType, instanceName, gameType)
        self.guiMgr.lookoutPage.matchTeleport()

    def setLootCarried(self, amt, maxCarry):
        self.lootCarried = amt

    def startTimer(self, time, timestamp, mode=None):
        if config.GetBool('hide-gui', 0):
            return
        if self == localAvatar:
            self.timerTimestamp = timestamp
            if time:
                ts = globalClockDelta.localElapsedTime(timestamp)
                newTime = time - ts
                if newTime > 0:
                    if mode == PiratesGlobals.HIGHSEAS_ADV_START:
                        pass
                    elif mode in [PiratesGlobals.SHIP_SELECTION_TIMER, PiratesGlobals.SHIP_BOARD_TIMER, PiratesGlobals.SHIP_DOCK_TIMER]:
                        self.guiMgr.setTimer(newTime, mode=mode)
                    else:
                        self.guiMgr.setTimer(newTime)
                else:
                    self.guiMgr.timerExpired()
            else:
                self.guiMgr.timerExpired()

    def cancelTimer(self, mode):
        self.guiMgr.cancelTimer(mode)

    def endMissionPanel(self, missionData, playerData):
        if config.GetBool('hide-gui', 0):
            return
        portName = ''
        if not base.localAvatar.ship.getSiegeTeam():
            self.guiMgr.createHighSeasScoreboard(portName, missionData, playerData, base.localAvatar.ship)

    def createTitle(self, textIndex):
        base.localAvatar.guiMgr.createTitle(textIndex)

    def sendCancelMission(self):
        self.sendUpdate('cancelMission')

    def play(self, *args, **kwArgs):
        Biped.Biped.play(self, *args, **kwArgs)

    def loop(self, *args, **kwArgs):
        Biped.Biped.loop(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        Biped.Biped.stop(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        Biped.Biped.pingpong(self, *args, **kwArgs)

    def putAwayCurrentWeapon(self, blendInT=0.1, blendOutT=0.1):
        self.setStickyTargets([])
        return DistributedBattleAvatar.putAwayCurrentWeapon(self, blendInT, blendOutT)

    def setStickyTargets(self, avList):
        self.stickyTargets = avList
        self.checkAttuneEffect()
        localAvatar.guiMgr.attuneSelection.update()

    def checkAttuneEffect(self):
        if not self.isGenerated():
            return
        if self.stickyTargets:
            if not self.attuneEffect:
                self.attuneEffect = VoodooAura.getEffect()
            if self.attuneEffect:
                self.attuneEffect.reparentTo(self.rightHandNode)
                self.attuneEffect.setPos(0, 0, 0)
                self.attuneEffect.particleDummy.reparentTo(self.rightHandNode)
                self.attuneEffect.startLoop()
                hasFriendly = 0
                hasEnemies = 0
                for targetId in self.stickyTargets:
                    target = self.cr.doId2do.get(targetId)
                    if target:
                        if TeamUtils.damageAllowed(self, target):
                            hasEnemies = 1
                        else:
                            hasFriendly = 1

                if hasFriendly and not hasEnemies:
                    self.attuneEffect.setEffectColor(Vec4(0.2, 0.5, 0.1, 1))
                elif hasEnemies and not hasFriendly:
                    self.attuneEffect.setEffectColor(Vec4(0.2, 0.1, 0.5, 1))
                elif hasEnemies and hasFriendly:
                    self.attuneEffect.setEffectColor(Vec4(0, 0.15, 0.15, 1))
        else:
            if self.attuneEffect:
                self.attuneEffect.stopLoop()
                self.attuneEffect = None
        return

    def getStickyTargets(self):
        return self.stickyTargets

    def addStickyTarget(self, avId):
        if avId not in self.stickyTargets:
            self.stickyTargets.append(avId)
            self.setStickyTargets(self.stickyTargets)
            localAvatar.guiMgr.attuneSelection.update()

    def sendRequestRemoveStickyTargets(self, doIdList):
        self.sendUpdate('requestRemoveStickyTargets', [doIdList])

    def hasStickyTargets(self):
        return self.stickyTargets

    def getFriendlyStickyTargets(self):
        avIdList = []
        for avId in self.stickyTargets:
            av = self.cr.doId2do.get(avId)
            if av:
                if not TeamUtils.damageAllowed(av, self):
                    avIdList.append(avId)

        return avIdList

    def getHostileStickyTargets(self):
        avIdList = []
        for avId in self.stickyTargets:
            av = self.cr.doId2do.get(avId)
            if av:
                if TeamUtils.damageAllowed(self, av):
                    avIdList.append(avId)

        return avIdList

    def setTutorialHandlerZone(self, zoneId):
        localAvatar.setInterest(base.cr.distributedDistrict.doId, zoneId, ['tutorialHandlerInterest'])

    def clearTutorialHandlerZone(self):
        localAvatar.clearInterestNamed(None, ['tutorialHandlerInterest'])
        return

    def sendClothingMessage(self, clothingId, colorId):
        localAvatar.guiMgr.messageStack.showLoot([], gold=0, collect=0, card=0, cloth=clothingId, color=colorId)

    def sendLootMessage(self, lootId):
        localAvatar.guiMgr.messageStack.showLoot([], gold=0, collect=lootId)

    def sendCardMessage(self, cardId):
        localAvatar.guiMgr.messageStack.showLoot([], gold=0, collect=0, card=cardId)

    def sendWeaponMessage(self, weapon):
        localAvatar.guiMgr.messageStack.showLoot([], gold=0, collect=0, weapon=weapon)
        localAvatar.checkWeaponSwitch(weapon, 0)
        localAvatar.guiMgr.setCurrentWeapon(weapon, 0)

    def sendJewelryMessage(self, jewelryUID):
        localAvatar.guiMgr.messageStack.showLoot([], gold=0, collect=0, jewel=jewelryUID)

    def sendTattooMessage(self, tattooUID):
        localAvatar.guiMgr.messageStack.showLoot([], gold=0, collect=0, tattoo=tattooUID)

    def sendReputationMessage(self, targetId, categories, reputationList, basicPenalty, crewBonus, doubleXPBonus, holidayBonus):
        target = base.cr.doId2do.get(targetId)
        if target:
            totalRep = 0
            for i in range(len(categories)):
                totalRep += reputationList[i]

            colorSetting = 4
            if InventoryType.GeneralRep in categories:
                colorSetting = 5
            target.printExpText(totalRep, colorSetting, basicPenalty, crewBonus, doubleXPBonus, holidayBonus)

    def sendRenownMessage(self, targetId, landRenown, seaRenown):
        target = base.cr.doId2do.get(targetId)
        renown = max(landRenown, seaRenown)
        if target:
            colorSetting = 7
            if landRenown:
                colorSetting = 8
            if hasattr(target, 'printExpText'):
                target.printExpText(renown, colorSetting, 0)
        if self.getShip() and self.getShip().renownDisplay:
            prevRank = self.getShip().renownDisplay.rank
            self.getShip().renownDisplay.updateRank(renown)
            newRank = self.getShip().renownDisplay.rank
            if prevRank < newRank:
                self.levelUpMsg(InventoryType.PVPTotalInfamySea, newRank, 0)
        else:
            if self.isLocal() and self.guiMgr and self.guiMgr.pvpPanel and hasattr(self.guiMgr.pvpPanel, 'renownDisplay') and self.guiMgr.pvpPanel.renownDisplay:
                prevRank = self.guiMgr.pvpPanel.renownDisplay.rank
                self.guiMgr.pvpPanel.renownDisplay.updateRank(renown)
                newRank = self.guiMgr.pvpPanel.renownDisplay.rank
                if prevRank < newRank:
                    self.levelUpMsg(InventoryType.PVPTotalInfamyLand, newRank, 0)
        if localAvatar.guiMgr and hasattr(localAvatar.guiMgr, 'titlesPage') and localAvatar.guiMgr.titlesPage:
            taskMgr.doMethodLater(1.4, localAvatar.guiMgr.titlesPage.refresh, 'titles-refresh', [])
        if renown > 0:
            localAvatar.guiMgr.messageStack.showLoot([], bounty=renown)
        self.refreshName()

    def sendSalvageMessage(self, targetId, amount):
        target = base.cr.doId2do.get(targetId)
        if target:
            colorSetting = 9
            if hasattr(target, 'printExpText'):
                target.printExpText(amount, colorSetting, 0, 0, 0, 0)
        self.refreshName()

    def setLevel(self, level):
        DistributedBattleAvatar.setLevel(self, level)
        self.refreshName()

    def getLevel(self):
        return self.level

    def levelUpMsg(self, category, level, messageId):
        if self.isLocal():
            self.guiMgr.showLevelUpText(category, level)
            messenger.send('weaponChange')
        self.playLevelUpEffect()

    def playLevelUpEffect(self):
        effect = LevelUpEffect.getEffect()
        if effect:
            effect.reparentTo(self)
            effect.particleDummy.reparentTo(self)
            effect.setPos(0, 0, 0)
            effect.play()

    @report(types=['frameCount', 'args'], dConfigParam='want-login-report')
    def b_setDefaultShard(self, defaultShard):
        if self.defaultShard != defaultShard:
            self.d_setDefaultShard(defaultShard)
            self.setDefaultShard(defaultShard)

    @report(types=['frameCount', 'args'], dConfigParam='want-login-report')
    def d_setDefaultShard(self, defaultShard):
        self.sendUpdate('setDefaultShard', [defaultShard])

    @report(types=['frameCount', 'args'], dConfigParam='want-login-report')
    def setDefaultShard(self, defaultShard):
        self.defaultShard = defaultShard

    @report(types=['frameCount'], dConfigParam='want-login-report')
    def getDefaultShard(self):
        return self.defaultShard

    def setDefaultZone(self, zone):
        self.defaultZone = zone

    @report(types=['frameCount', 'args'], dConfigParam='want-jail-report')
    def d_requestReturnLocation(self, locationDoId):
        self.sendUpdate('requestReturnLocation', [locationDoId])

    @report(types=['frameCount', 'args'], dConfigParam='want-jail-report')
    def setReturnLocation(self, returnLocation):
        self.returnLocation = returnLocation

    @report(types=['frameCount'], dConfigParam='want-jail-report')
    def getReturnLocation(self):
        return self.returnLocation

    @report(types=['frameCount', 'args'], dConfigParam='want-map-report')
    def d_requestCurrentIsland(self, locationDoId):
        self.sendUpdate('requestCurrentIsland', [locationDoId])

    @report(types=['frameCount', 'args'], dConfigParam='want-map-report')
    def setCurrentIsland(self, islandUid):
        self.currentIsland = islandUid

    @report(types=['frameCount'], dConfigParam='want-jail-report')
    def getCurrentIsland(self):
        return self.currentIsland

    @report(types=['frameCount', 'args'], dConfigParam='want-jail-report')
    def setJailCellIndex(self, index):
        self.jailCellIndex = index
        if index < 100:
            self.b_setTeleportFlag(PiratesGlobals.TFInJail)
        else:
            self.b_clearTeleportFlag(PiratesGlobals.TFInJail)

    @report(types=['frameCount'], dConfigParam='want-jail-report')
    def getJailCellIndex(self):
        return self.jailCellIndex

    def changeBodyType(self):
        self.generateHuman(self.style.gender, base.cr.human)
        if self.motionFSM.state != 'Off':
            self.motionFSM.off()
            self.motionFSM.on()
        if not self.zombie:
            self.hideBeacon()

    def setCursed(self, value):
        self.cursed = value
        self.setZombie(value)

    def setZombie(self, value):
        if self.zombie == value:
            return
        self.zombie = value
        self.changeBodyType()

    def isUndead(self):
        return self.zombie

    def respawn(self):
        self.motionFSM.on()
        self.unstashBattleCollisions()
        self.startCompassEffect()
        self.show()

    def setWishName(self):
        self.cr.sendWishName(self.doId, self.style.name)

    def canTeleport(self):
        return (self.teleportFlags & PiratesGlobals.TFNoTeleportOut).isZero()

    def canTeleportTo(self):
        return (self.teleportFlags & PiratesGlobals.TFNoTeleportTo).isZero()

    def testTeleportFlag(self, flag):
        return not (self.teleportFlags & flag).isZero()

    def getNextTeleportConfirmFlag(self, currentFlag=None, flags=None):
        currentFlag = currentFlag or BitMask32()
        flags = flags or self.teleportFlags
        flags &= PiratesGlobals.TFNoTeleportOut
        return flags.keepNextHighestBit(currentFlag)

    def getNextTeleportToConfirmFlag(self, currentFlag=None, flags=None):
        currentFlag = currentFlag or BitMask32()
        flags = flags or self.teleportFlags
        flags &= PiratesGlobals.TFNoTeleportTo
        return flags.keepNextHighestBit(currentFlag)

    def getNoTeleportString(self, flag=None):
        flag = flag or self.teleportFlags.keepNextHighestBit()
        if not flag.isZero():
            return PiratesGlobals.TFNoTeleportReasons.get(flag, '')
        return ''

    def getNoTeleportToString(self, flag=None):
        flag = flag or self.teleportFlags.keepNextHighestBit()
        if not flag.isZero():
            return PiratesGlobals.TFNoTeleportToReasons.get(flag, '')
        return ''

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def confirmTeleport(self, callback, feedback=False):
        if not self.canTeleport():
            flag = self.getNextTeleportConfirmFlag()
            while not flag.isZero():
                confirmFunc, confirmArgs = self.teleportConfirmCallbacks.get(flag, (None, []))
                if confirmFunc and confirmFunc('from', 0, *confirmArgs):
                    flag = self.getNextTeleportConfirmFlag(flag)
                else:
                    if feedback:
                        self.guiMgr.createWarning(self.getNoTeleportString(flag), PiratesGuiGlobals.TextFG6, duration=10)
                    callback(False)
                    return

        callback(True)
        return

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def confirmTeleportTo(self, callback, avId):
        flag = self.getNextTeleportToConfirmFlag()
        while not flag.isZero():
            confirmFunc, confirmArgs = self.teleportConfirmCallbacks.get(flag, (None, []))
            if confirmFunc and confirmFunc('to', avId, *confirmArgs):
                flag = self.getNextTeleportToConfirmFlag(flag)
            else:
                callback(False, avId, flag)
                return

        callback(True, avId, flag)
        return

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def b_setTeleportFlag(self, flag, confirmCallback=None, confirmArgs=[]):
        self.b_setTeleportFlags(self.teleportFlags | flag, {flag: (confirmCallback, confirmArgs)})

    def setTeleportFlag(self, flag, confirmCallback=None, confirmArgs=[]):
        self.setTeleportFlags(self.teleportFlags | flag, {flag: (confirmCallback, confirmArgs)})

    def b_clearTeleportFlag(self, flag):
        self.b_setTeleportFlags(self.teleportFlags & ~flag, {flag: (None, [])})
        return

    def clearTeleportFlag(self, flag):
        self.setTeleportFlags(self.teleportFlags & ~flag, {flag: (None, [])})
        return

    def b_setTeleportFlags(self, flags, confirmDict):
        if self.teleportFlags != flags:
            self.d_setTeleportFlags(flags)
            self.setTeleportFlags(flags, confirmDict)

    @report(types=['args'])
    def d_setTeleportFlags(self, flags):
        self.sendUpdate('setTeleportFlags', [flags.getWord()])

    def setTeleportFlags(self, flags, confirmDict={}):
        self.teleportFlags = BitMask32(flags)
        b = BitMask32.bit(31)
        while not b.isZero():
            if (b & self.teleportFlags).isZero():
                self.teleportConfirmCallbacks.pop(b, None)
            else:
                if b in confirmDict:
                    self.teleportConfirmCallbacks[b] = confirmDict[b]
            b >>= 1

        return

    def getTeleportFlags(self):
        return self.teleportFlags

    def decipherTeleportFlags(self):
        iter = BitMask32(1)
        print self.teleportFlags, '-' * 80
        while iter.getWord():
            if (iter & self.teleportFlags).getWord():
                print '%-4s' % iter.getHighestOnBit(), self.getNoTeleportString(iter) or self.getNoTeleportToString(iter)
            iter <<= 1

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def sendTeleportQuery(self, sendToId, localShardId):
        self.d_teleportQuery(localAvatar.doId, localShardId, sendToId)

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def d_teleportQuery(self, localAvId, localShardId, sendToId):
        self.sendUpdate('teleportQuery', [localAvId, localShardId], sendToId=sendToId)

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def teleportQuery(self, requesterId, requesterShardId):
        if self.isGenerated():
            self.cr.teleportMgr.handleAvatarTeleportQuery(requesterId, requesterShardId)

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def sendTeleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId=None):
        self.d_teleportResponse(available, shardId, instanceDoId, areaDoId, sendToId)

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def d_teleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId=None):
        self.sendUpdate('teleportResponse', [localAvatar.doId, available, shardId, instanceDoId, areaDoId], sendToId)

    @report(types=['deltaStamp', 'args'], dConfigParam='want-teleport-report')
    def teleportResponse(self, avId, available, shardId, instanceDoId, areaDoId):
        if self.isGenerated():
            self.cr.teleportMgr.handleAvatarTeleportResponse(avId, available, shardId, instanceDoId, areaDoId)

    def teleportTokenCheck(self, token):
        inv = self.getInventory()
        return bool(inv) and inv.getStackQuantity(token)

    def hasIslandTeleportToken(self, islandUid):
        token = InventoryType.getIslandTeleportToken(islandUid)
        return self.teleportTokenCheck(token)

    def confirmIslandTeleport(self, toFrom, incomingAvid=0, islandUid=''):
        if toFrom == 'from':
            return self.hasIslandTeleportToken(islandUid) or self.returnLocation == islandUid or self.currentIsland == islandUid or self.cr.distributedDistrict.worldCreator.isPvpIslandByUid(islandUid) or base.config.GetBool('teleport-all', 0)
        else:
            return True

    def confirmSwimmingTeleport(self, toFrom, incomingAvid=0):
        if toFrom == 'from':
            return True
        else:
            return True

    def setBandId(self, bandmanager, bandId):
        if bandId:
            self.BandId = (
             bandmanager, bandId)
        else:
            self.BandId = None
        return

    def getBandId(self):
        return self.BandId

    def isOnline(self):
        return True

    def isUnderstandable(self):
        return True

    def setPvp(self, value):
        self.hideBeacon()
        self.inPvp = value

    def checkQuestRewardFlag(self, flag):
        return not (self.questRewardFlags & flag).isZero()

    def setQuestRewardFlags(self, flags):
        self.questRewardFlags = BitMask32(flags)

    def getQuestRewardFlags(self):
        return self.questRewardFlags

    def spentSkillPoint(self, category):
        self.guiMgr.combatTray.skillTray.rebuildSkillTray()
        self.guiMgr.combatTray.initCombatTray()

    def resetSkillPoints(self, skillId):
        self.guiMgr.combatTray.skillTray.rebuildSkillTray()
        self.guiMgr.combatTray.initCombatTray()

    def requestLookoutInvite(self, inviterId, inviterName, activityCategory, activityType, options):
        if self.isLocal() and inviterId != localAvatar.doId:
            self.guiMgr.lookoutPage.requestInvite(inviterName, activityCategory, activityType, options)

    def b_setSCEmote(self, emoteId):
        self.setSCEmote(emoteId)
        self.d_setSCEmote(emoteId)

    def d_setSCEmote(self, emoteId):
        self.sendUpdate('setSCEmote', [
         emoteId])

    def setSCEmote(self, emoteId):
        if self.doId in base.localAvatar.ignoreList:
            return
        base.chatAssistant.receiveAvatarOpenSpeedChat(ChatGlobals.SPEEDCHAT_EMOTE, emoteId, self.doId)

    def b_setSpeedChatQuest(self, questInt, msgType, taskNum):
        self.setSpeedChatQuest(questInt, msgType, taskNum)
        self.d_setSpeedChatQuest(questInt, msgType, taskNum)
        return

    def d_setSpeedChatQuest(self, questInt, msgType, taskNum):
        self.sendUpdate('setSpeedChatQuest', [
         questInt, msgType, taskNum])
        return

    def setSpeedChatQuest(self, questInt, msgType, taskNum):
        if self.doId in base.localAvatar.ignoreList:
            return
        chatString = PSCDecoders.decodeSCQuestMsgInt(questInt, msgType, taskNum)
        if chatString:
            self.setChatAbsolute(chatString, CFSpeech | CFQuicktalker | CFTimeout)
        return

    def getAccess(self):
        if Freebooter.AllAccessHoliday:
            return 2
        else:
            return self.getGameAccess()

    def setAccess(self, access):
        self.setGameAccess(access)

    def setGameAccess(self, access):
        self.gameAccess = access
        self.refreshName()

    def getGameAccess(self):
        return self.gameAccess

    def setFounder(self, founder):
        self.founder = founder
        self.refreshName()

    def getFounder(self):
        return self.founder

    def useBestTonic(self):
        self.sendUpdate('useBestTonic', [])

    def useTonic(self, tonicId):
        self.sendUpdate('useTonic', [tonicId])

    @report(types=['frameCount', 'args'], dConfigParam='want-port-report')
    def setPort(self, islandId):
        self.port = islandId
        if self.ship:
            self.ship.checkAbleDropAnchor()

    @report(types=['frameCount', 'args'], dConfigParam='want-port-report')
    def clearPort(self, islandId):
        if islandId == self.port:
            self.port = 0
            if self.ship:
                self.ship.checkAbleDropAnchor()

    def getPort(self):
        return self.port

    def enableWaterEffect(self):
        if base.options.getSpecialEffectsSetting() < base.options.SpecialEffectsMedium:
            return
        if not self.waterRipple:
            self.waterRipple = WaterRipple.getEffect()
            if self.waterRipple:
                self.waterRipple.reparentTo(self)
                self.waterRipple.startLoop()
        if not self.waterWake:
            self.waterWake = WaterRippleWake.getEffect()
            if self.waterWake:
                self.waterWake.reparentTo(self)
                self.waterWake.startLoop()
        if not self.waterSplash:
            self.waterSplash = WaterRippleSplash.getEffect()
            if self.waterSplash:
                self.waterSplash.reparentTo(self)
                self.waterSplash.startLoop()

    def disableWaterEffect(self):
        if base.options.getSpecialEffectsSetting() < base.options.SpecialEffectsMedium:
            return
        if self.waterRipple:
            self.waterRipple.stopLoop()
            self.waterRipple = None
        if self.waterWake:
            self.waterWake.stopLoop()
            self.waterWake = None
        if self.waterSplash:
            self.waterSplash.stopLoop()
            self.waterSplash = None
        return

    def adjustWaterEffect(self, offset, forwardSpeed=0.0, rotateSpeed=0.0, slideSpeed=0.0):
        if base.options.getSpecialEffectsSetting() < base.options.SpecialEffectsMedium:
            return
        if forwardSpeed == 0.0 and slideSpeed == 0.0:
            if not self.waterRipple:
                self.waterRipple = WaterRipple.getEffect()
                if self.waterRipple:
                    self.waterRipple.reparentTo(self)
                    self.waterRipple.startLoop()
            if self.waterWake:
                self.waterWake.stopLoop()
                self.waterWake = None
            if self.waterSplash:
                self.waterSplash.stopLoop()
                self.waterSplash = None
        else:
            if not self.waterWake:
                self.waterWake = WaterRippleWake.getEffect()
                if self.waterWake:
                    self.waterWake.reparentTo(self)
                    self.waterWake.startLoop()
            if not self.waterSplash:
                self.waterSplash = WaterRippleSplash.getEffect()
                if self.waterSplash:
                    self.waterSplash.reparentTo(self)
                    self.waterSplash.startLoop()
            if self.waterRipple:
                self.waterRipple.stopLoop()
                self.waterRipple = None
        if rotateSpeed != 0.0 and self.waterRipple:
            self.waterRipple.disturb.start()
        if self.waterRipple:
            self.waterRipple.setZ(offset)
        if self.waterWake:
            self.waterWake.setY(forwardSpeed / 9.5)
            self.waterWake.setX(slideSpeed / 9.0)
            self.waterWake.setZ(offset)
        if self.waterSplash:
            self.waterSplash.setX(slideSpeed / 20.0)
            self.waterSplash.setZ(offset - 0.75)
        return

    def setCompositeDNA(self, *dna):
        counter = 0
        dclass = base.cr.dclassesByName['DistributedPlayerPirate']
        field = dclass.getFieldByName('setCompositeDNA').asMolecularField()
        for i in xrange(field.getNumAtomics()):
            subField = field.getAtomic(i)
            args = dna[counter:counter + subField.getNumElements()]
            counter += subField.getNumElements()
            getattr(self.style, subField.getName())(*args)

    def setClothes(self, *dna):
        counter = 0
        dclass = base.cr.dclassesByName['DistributedPlayerPirate']
        field = dclass.getFieldByName('setClothes').asMolecularField()
        for i in xrange(field.getNumAtomics()):
            subField = field.getAtomic(i)
            args = dna[counter:counter + subField.getNumElements()]
            counter += subField.getNumElements()
            getattr(self.style, subField.getName())(*args)

        self.generateHuman(self.style.getGender(), base.cr.human)
        self.motionFSM.off()
        self.motionFSM.on()
        messenger.send(self.uniqueName('accessoriesUpdate'))

    def setHair(self, *dna):
        counter = 0
        dclass = base.cr.dclassesByName['DistributedPlayerPirate']
        field = dclass.getFieldByName('setHair').asMolecularField()
        for i in xrange(field.getNumAtomics()):
            subField = field.getAtomic(i)
            args = dna[counter:counter + subField.getNumElements()]
            counter += subField.getNumElements()
            getattr(self.style, subField.getName())(*args)

        self.generateHuman(self.style.getGender(), base.cr.human)
        self.motionFSM.off()
        self.motionFSM.on()

    def setJewelry(self, *dna):
        counter = 0
        dclass = base.cr.dclassesByName['DistributedPlayerPirate']
        field = dclass.getFieldByName('setJewelry').asMolecularField()
        for i in xrange(field.getNumAtomics()):
            subField = field.getAtomic(i)
            args = dna[counter:counter + subField.getNumElements()]
            counter += subField.getNumElements()
            getattr(self.style, subField.getName())(*args)

        self.generateHuman(self.style.getGender(), base.cr.human)
        self.motionFSM.off()
        self.motionFSM.on()
        messenger.send(self.uniqueName('jewelryUpdate'))

    def setTattoos(self, *dna):
        counter = 0
        dclass = base.cr.dclassesByName['DistributedPlayerPirate']
        field = dclass.getFieldByName('setTattoos').asMolecularField()
        for i in xrange(field.getNumAtomics()):
            subField = field.getAtomic(i)
            args = dna[counter:counter + subField.getNumElements()]
            counter += subField.getNumElements()
            getattr(self.style, subField.getName())(*args)

        self.generateHuman(self.style.getGender(), base.cr.human)
        self.motionFSM.off()
        self.motionFSM.on()
        messenger.send(self.uniqueName('tattooUpdate'))

    def requestActivity(self, gameType, gameCategory, options, shipIds):
        self.sendUpdate('requestActivity', [gameType, gameCategory, options, shipIds])

    def requestEmote(self, emoteId):
        gamestate = localAvatar.getGameState()
        emote = self.getEmote(emoteId)
        if emote:
            emote_gender = emote[4]
            if emote_gender and localAvatar.style.gender != emote_gender:
                return False
        else:
            return False
        if self.getGameState() == 'Emote':
            self.b_setGameState('LandRoam')
        if localAvatar.isWeaponDrawn:
            return True
        else:
            if gamestate in ('ShipPilot', 'Cannon', 'WaterRoam', 'WaterTreasureRoam',
                             'ParlorGame', 'NPCInteract', 'DinghyInteract', 'TentacleAlive'):
                return True
            else:
                if localAvatar.controlManager.currentControls.moving:
                    return True
                else:
                    self.d_setEmote(emoteId)
                    self.b_setGameState('Emote')
                    return True

    def playEmote(self, emoteId):
        if self.getGameState() != 'Emote' and self.getGameState() != 'WeaponReceive':
            return
        emote = self.getEmote(emoteId)
        if emote:
            if self.emote_track is not None:
                self.emote_track.pause()
                self.emote_track = None
            if self.emote_prop is not None:
                self.emote_prop.removeNode()
                self.emote_prop = None
            propId = emote[2]
            if propId is not None:
                prop = loader.loadModel(propId)
                if 'grenade' in propId:
                    prop.setScale(0.65)
                motion_blur = prop.find('**/motion_blur')
                if not motion_blur.isEmpty():
                    motion_blur.stash()
                if prop and not prop.isEmpty():
                    handNode = self.rightHandNode
                    if handNode:
                        prop.flattenStrong()
                        prop.reparentTo(handNode)
                        self.emote_prop = prop
            if not emote[1] and self.isLocal():
                anim = emote[0]
                sfx = emote[5]
                if emote[5]:
                    sfx = base.loader.loadSfx(emote[5])
                    self.emote_track = Sequence(Parallel(self.actorInterval(anim), SoundInterval(sfx, node=self, duration=self.getDuration(anim))), Func(self.b_setGameState, 'LandRoam'))
                else:
                    self.emote_track = Sequence(self.actorInterval(anim), Func(self.b_setGameState, 'LandRoam'))
                self.emote_track.start()
            else:
                self.loop(emote[0])
        return

    def getEmote(self, emoteId):
        emote = PLocalizer.emotes.get(emoteId)
        if not emote:
            emote = PLocalizer.nonMenuEmoteAnimations.get(emoteId)
        if not emote:
            emote = PLocalizer.receiveWeaponEmotes.get(emoteId)
        return emote

    def setEmote(self, emoteId):
        self.emoteId = emoteId

    def d_setEmote(self, emoteId):
        self.setEmote(emoteId)
        self.b_setEmote(emoteId)

    def b_setEmote(self, emoteId):
        self.sendUpdate('setEmote', [emoteId])

    def requestInvitesResp(self, invitees, numFailed):
        if len(invitees) > 0:
            self.guiMgr.lookoutPage.requestInvitesResponse(invitees)
        else:
            if self.guiMgr.lookoutPage.currentInviteRequiresInvitees():
                self.guiMgr.lookoutPage.restoreOrCancelSearch()
                if numFailed == 0:
                    if DistributedBandMember.DistributedBandMember.getBandMember(localAvatar.doId):
                        self.guiMgr.messageStack.addTextMessage(PLocalizer.LookoutInviteIgnore, icon=('lookout',
                                                                                                      None))
                    else:
                        self.guiMgr.messageStack.addTextMessage(PLocalizer.LookoutInviteNeedCrew, icon=('lookout',
                                                                                                        None))
            else:
                self.guiMgr.lookoutPage.requestInvitesResponse([])
        if numFailed > 0:
            self.guiMgr.messageStack.addTextMessage(PLocalizer.LookoutInviteFail % numFailed, icon=('lookout',
                                                                                                    None))
        return

    def getTutorialState(self):
        return self.tutorialState

    def updateClientTutorialStatus(self, val):
        self.tutorialState = val

    def getIsPaid(self):
        self.updatePaidStatus()
        return self.isPaid

    def updatePaidStatus(self):
        pStatus = self.getGameAccess()
        if pStatus == 2 or pStatus == 0:
            self.isPaid = True
        else:
            self.isPaid = False

    def initVisibleToCamera(self):
        if self is not localAvatar and localAvatar.getSoloInteraction():
            self.hideFromCamera()
        else:
            self.showToCamera()

    def hideFromCamera(self):
        self.accept('showOtherAvatars', self.showToCamera)
        self.node().adjustDrawMask(BitMask32.allOff(), base.cam.node().getCameraMask(), BitMask32.allOff())

    def showToCamera(self):
        self.accept('hideOtherAvatars', self.hideFromCamera)
        self.node().adjustDrawMask(base.cam.node().getCameraMask(), BitMask32.allOff(), BitMask32.allOff())

    def submitCodeToServer(self, code):
        if code:
            base.cr.codeRedemption.redeemCode(code)

    def getNameText(self):
        return DistributedPirateBase.getNameText(self)

    def setOnWelcomeWorld(self, value):
        self.onWelcomeWorld = value

    def setTempDoubleXPReward(self, value):
        if not self.tempDoubleXPStatusMessaged:
            self.tempDoubleXPStatusMessaged = True
            if self.getDoId() == localAvatar.getDoId() and value != 0:
                h, m = self.getHoursAndMinutes(value)
                base.localAvatar.guiMgr.messageStack.addModalTextMessage(PLocalizer.TEMP_DOUBLE_REP % (h, m), seconds=45, priority=0, color=PiratesGuiGlobals.TextFG14)
        else:
            if value > self.tempDoubleXPStatus:
                h, m = self.getHoursAndMinutes(value)
                base.localAvatar.guiMgr.messageStack.addModalTextMessage(PLocalizer.TEMP_DOUBLE_REP % (h, m), seconds=45, priority=0, color=PiratesGuiGlobals.TextFG14)
        self.tempDoubleXPStatus = value
        self.x2XPIcon.setPos(0.3, 0, -0.15)
        self.refreshName()

    def getTempDoubleXPReward(self):
        return self.tempDoubleXPStatus

    def getHoursAndMinutes(self, seconds):
        t = int(seconds)
        minutes, seconds = divmod(t, 60)
        hours, minutes = divmod(minutes, 60)
        return [
         hours, minutes]

    def setCrewHUDUpdate(self, numberOfNearByCrew, cMemberIcons):
        localAvatar.guiMgr.crewPage.crewHUD.updateAll(numberOfNearByCrew, cMemberIcons)

    def setGMNameTagState(self, state):
        self.gmNameTagEnabled = state

    def setGMNameTagString(self, nameTagString):
        self.gmNameTagString = nameTagString

    def getGMNameTagString(self):
        return self.gmNameTagString

    def setGMNameTagColor(self, color):
        self.gmNameTagColor = color

    def getGMNameTagColor(self):
        return self.gmNameTagColor

    def updateGMNameTag(self, state, color, tagString):
        if color == 'gold':
            color = 'goldGM'
        else:
            if color == 'red':
                color = 'redGM'
            else:
                if color == 'green':
                    color = 'greenGM'
                else:
                    if color == 'blue':
                        color = 'blueGM'
                    else:
                        color = 'whiteGM'
        self.setGMNameTagState(state)
        self.setGMNameTagColor(color)
        self.setGMNameTagString(tagString)
        self.refreshName()

    def nameTag3dInitialized(self):
        DistributedPirateBase.nameTag3dInitialized(self)
        self.refreshName()

    def b_updateGMNameTag(self, state, color, tagString):
        self.d_updateGMNameTag(state, color, tagString)
        self.updateGMNameTag(state, color, tagString)

    def d_updateGMNameTag(self, state, color, tagString):
        self.sendUpdate('updateGMNameTag', [state, color, tagString])

    def setAllowGMNameTag(self, state):
        self.gmNameTagAllowed = state

    def getShortName(self):
        return self.getName()

    def setChatAbsolute(self, chatString, chatFlags, dialogue=None, interrupt=1, quiet=0):
        if not self.gmNameTagAllowed:
            DistributedPlayer.setChatAbsolute(self, chatString, chatFlags, dialogue, interrupt, quiet)
        else:
            if not quiet:
                base.chatAssistant.receiveGMOpenTypedChat(chatString, chatFlags, self.doId)
# okay decompiling .\pirates\pirate\DistributedPlayerPirate.pyc
