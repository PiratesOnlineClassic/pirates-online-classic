# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.LocalPirate
Instruction context:
-> 
1448     117  LOAD_FAST             0  'self'
            120  LOAD_ATTR            12  'handleTeleportToShardDone'
            123  LOAD_FAST             1  'shardId'
            126  LOAD_FAST             2  'zoneId'
            129  LOAD_FAST             3  'callbackEvent'
            132  CALL_FUNCTION_3       3  None
            135  POP_TOP          
import math, copy, types, random
from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.showbase.PythonUtil import *
from direct.directnotify import DirectNotifyGlobal
from direct.controls import ControlManager
from direct.interval.IntervalGlobal import *
from direct.controls import BattleWalker
from direct.actor import Actor
from direct.showbase.InputStateGlobal import inputState
from direct.distributed.ClockDelta import *
from direct.showbase.ShadowPlacer import ShadowPlacer
from direct.fsm.StatePush import StateVar
from otp.avatar.LocalAvatar import LocalAvatar
from otp.avatar import PositionExaminer
from otp.otpbase import OTPGlobals
from otp.speedchat import SCDecoders
from otp.otpgui import OTPDialog
from pirates.piratesgui import PDialog
from pirates.battle import WeaponGlobals
from pirates.battle import DistributedBattleAvatar
from pirates.chat.PiratesChatManager import PiratesChatManager
from pirates.chat.PChatAssistant import PChatAssistant
from pirates.ship import ShipGlobals
from pirates.piratesgui import GuiManager
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.reputation import ReputationGlobals
from pirates.battle import RangeDetector
from pirates.battle import BattleSkillDiary
from pirates.movement.CameraFSM import CameraFSM
from pirates.economy.EconomyGlobals import *
from pirates.economy import EconomyGlobals
from pirates.piratesbase import TeamUtils
from pirates.ship import DistributedShip
from pirates.instance import DistributedMainWorld
from pirates.world import DistributedGameArea
from pirates.world import OceanZone
from pirates.interact import InteractiveBase
from pirates.effects.CloudScud import CloudScud
from direct.controls.GhostWalker import GhostWalker
from direct.controls.PhysicsWalker import PhysicsWalker
from direct.controls.ObserverWalker import ObserverWalker
from pirates.movement.PiratesGravityWalker import PiratesGravityWalker
from pirates.movement.PiratesSwimWalker import PiratesSwimWalker
from pirates.quest import QuestDB
from pirates.quest import QuestStatus
from pirates.quest.QuestConstants import LocationIds
from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
import Pirate, LocalPirateGameFSM
from DistributedPlayerPirate import DistributedPlayerPirate
from direct.gui import OnscreenText
globalClock = ClockObject.getGlobalClock()
from direct.controls.ControlManager import ControlManager
if base.config.GetBool('want-custom-keys', 0):
    ControlManager.wantCustomKeys = 1
    ControlManager.wantWASD = 0
else:
    ControlManager.wantCustomKeys = 0
    ControlManager.wantWASD = 1

class LocalPirate(DistributedPlayerPirate, LocalAvatar):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('LocalPirate')
    neverDisable = 1

    def __init__(self, cr):
        try:
            self.LocalPirate_initialized
        except:
            self.LocalPirate_initialized = 1
            DistributedPlayerPirate.__init__(self, cr)
            chatMgr = PiratesChatManager()
            chatAssistant = PChatAssistant()
            LocalAvatar.__init__(self, cr, chatMgr, chatAssistant)
            self.gameFSM = None
            self.equippedWeapons = []
            self.setLocalAvatarUsingWeapon(1)
            self.cameraFSM = CameraFSM(self)
            self.guiMgr = GuiManager.GuiManager(self)
            self.interestHandles = []
            if base.config.GetBool('debug-local-animMixer', 0):
                self.animMixer.setVerbose(True)
            self.currentMouseOver = None
            self.currentAimOver = None
            self.currentSelection = None
            self.tutObject = None
            self.currentDialogMovie = None
            self.ship = None
            self.shipList = []
            self.interior = None
            self.cannon = None
            self.__turboOn = 0
            self.__marioOn = 0
            self.speedIndex = 0
            self.curMoveSound = None
            self.setupMovementSounds()
            self.rangeDetector = RangeDetector.RangeDetector()
            self.rangeDetector.detachNode()
            self.showQuest = True
            self.currentOcean = 0
            self.soundWhisper = loader.loadSfx('audio/sfx_gui_whisper.mp3')
            self.positionExaminer = PositionExaminer.PositionExaminer()
            self.skillDiary = BattleSkillDiary.BattleSkillDiary(self.cr, self)
            self.lookAtTarget = None
            self.lookAtTimer = None
            self.lookAtDummy = self.attachNewNode('lookAtDummy')
            self.lookFromNode = self.attachNewNode('lookFromTargetHelper')
            self.lookFromNode.setZ(self.getHeight())
            self.lookToNode = NodePath('lookToTargetHelper')
            if base.config.GetBool('want-dev', False):
                self.accept('shift-f12', self.toggleAvVis)
            self.money = 0
            self.enableAutoRun = 0
            self.kickEvents = None
            self.battleTeleportFlagTask = None
            self.openJailDoorTrack = None
            self.questArrow = None
            self.arrowPlacer = None
            self.noQuestArrow = False
            self.emote_track = None
            self.emote_prop = None
            self.currentStoryQuests = []
            self.cloudScudEffect = None
            self.questStatus = QuestStatus.QuestStatus(self)
            self.soloInteraction = False
            self.emoteAccess = []
            self.AFKDelay = base.config.GetInt('afk-delay', 600)
            self.playRewardAnimation = None
            self.localProjectiles = []
            self._cannonAmmoSkillId = InventoryType.CannonRoundShot
            self._siegeTeamSV = StateVar(0)
            self.guildPopupDialog = None
            self.moralePopupDialog = None
            self.gmNameTagEnabledLocal = 0
            self.gmNameTagStringLocal = ''
            self.gmNameTagColorLocal = ''
            if self.gmNameTagAllowed:
                if base.config.GetInt('gm-nametag-enabled', 0):
                    self.gmNameTagEnabledLocal = 1
            if base.config.GetString('gm-nametag-string', '') != '':
                self.gmNameTagStringLocal = base.config.GetString('gm-nametag-string')
            if base.config.GetString('gm-nametag-color', '') != '':
                self.gmNameTagColorLocal = base.config.GetString('gm-nametag-color')
            soundEffects = ['jollyroger_laugh_01.mp3', 'jollyroger_laugh_02.mp3', 'jollyroger_enjoy.mp3', 'jollyroger_submit.mp3', 'jollyroger_joinme.mp3']
            self.jollySfx = loader.loadSfx('audio/' + random.choice(soundEffects))

        return

    def sendUpdate(self, *args, **kw):
        if self.isGenerated():
            return DistributedPlayerPirate.sendUpdate(self, *args, **kw)

    def setupWalkControls(self, avatarRadius=1.4, floorOffset=OTPGlobals.FloorOffset, reach=4.0, wallBitmask=OTPGlobals.WallBitmask, floorBitmask=OTPGlobals.FloorBitmask, ghostBitmask=OTPGlobals.GhostBitmask):
        walkControls = PiratesGravityWalker(gravity=-32.174 * 2.0)
        walkControls.setWallBitMask(wallBitmask)
        walkControls.setFloorBitMask(floorBitmask)
        walkControls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, reach)
        walkControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(walkControls, 'walk')
        self.physControls = walkControls
        swimControls = PiratesSwimWalker()
        swimControls.setWallBitMask(wallBitmask)
        swimControls.setFloorBitMask(floorBitmask)
        swimControls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, 4.0)
        swimControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(swimControls, 'swim')
        ghostControls = GhostWalker()
        ghostControls.setWallBitMask(ghostBitmask)
        ghostControls.setFloorBitMask(floorBitmask)
        ghostControls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, reach)
        ghostControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(ghostControls, 'ghost')
        observerControls = ObserverWalker()
        observerControls.setWallBitMask(ghostBitmask)
        observerControls.setFloorBitMask(floorBitmask)
        observerControls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, reach)
        observerControls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(observerControls, 'observer')
        self.controlManager.use('walk', self)
        self.controlManager.disable()

    def createGameFSM(self):
        self.gameFSM = LocalPirateGameFSM.LocalPirateGameFSM(self)

    def updateReputation(self, category, value):
        DistributedPlayerPirate.updateReputation(self, category, value)
        self.guiMgr.updateReputation(category, value)

    def playSkillMovie(self, skillId, ammoSkillId, skillResult, charge=0, targetId=0):
        self.skillDiary.startRecharging(skillId, ammoSkillId)
        DistributedPlayerPirate.playSkillMovie(self, skillId, ammoSkillId, skillResult, charge, targetId)

    def toggleWeapon(self, newWeaponId, fromWheel=0):
        if newWeaponId != self.currentWeaponId and self.isWeaponDrawn:
            self.d_requestCurrentWeapon(newWeaponId, 1)
            self.l_setCurrentWeapon(newWeaponId, 1)
            self.b_setGameState('Battle')
        else:
            if not self.isWeaponDrawn and fromWheel:
                self.d_requestCurrentWeapon(newWeaponId, 1)
                self.l_setCurrentWeapon(newWeaponId, 1)
                self.b_setGameState('Battle')
            else:
                if not self.isWeaponDrawn:
                    self.d_requestCurrentWeapon(newWeaponId, 1)
                    self.l_setCurrentWeapon(newWeaponId, 1)
                    self.b_setGameState('Battle')
                    messenger.send('weaponEquipped')
                else:
                    self.d_requestCurrentWeapon(newWeaponId, 0)
                    self.l_setCurrentWeapon(newWeaponId, 0)
                    self.b_setGameState('LandRoam')
                    messenger.send('weaponSheathed')

    def setCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        pass

    def l_setCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        if not self.gameFSM.isInTransition() and self.getGameState() in ['WaterRoam', 'WaterTreasureRoam']:
            return
        if self.currentWeaponId != currentWeaponId or self.isWeaponDrawn != isWeaponDrawn:
            DistributedPlayerPirate.sendRequestRemoveStickyTargets(self, self.stickyTargets)
            self.setStickyTargets([])
        if WeaponGlobals.getWeaponCategory(currentWeaponId) == WeaponGlobals.VOODOO and isWeaponDrawn == True:
            self.guiMgr.attuneSelection.show()
        else:
            self.guiMgr.attuneSelection.hide()
        self.checkWeaponSwitch(currentWeaponId, isWeaponDrawn)
        self.guiMgr.setCurrentWeapon(currentWeaponId, isWeaponDrawn)

    def d_requestCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        self.sendUpdate('requestCurrentWeapon', [currentWeaponId, isWeaponDrawn])

    def d_requestCurrentAmmo(self, currentAmmoId):
        self.sendUpdate('requestCurrentAmmo', [currentAmmoId])

    def __drawWeapon(self):
        self.guiMgr.combatTray.toggleWeapon(self.currentWeaponId)

    def __drawWeaponIfTarget(self):
        if self.isWeaponDrawn:
            return
        if self.cr.targetMgr:
            target = self.cr.targetMgr.pickObject()
            if target and TeamUtils.damageAllowed(target, self):
                self.guiMgr.combatTray.toggleWeapon(self.currentWeaponId)

    def enableMouseWeaponDraw(self):
        self.accept('control', self.__drawWeapon)
        self.accept('mouse1', self.__drawWeaponIfTarget)
        self.accept('mouse2', self.__drawWeapon)

    def disableMouseWeaponDraw(self):
        self.ignore('control')
        self.ignore('mouse1')
        self.ignore('mouse2')

    def setMoney(self, money):
        self.guiMgr.setMoney(money)
        if self.money != 0:
            gain = money - self.money
            if gain > 0:
                if self.gameFSM.getCurrentOrNextState() == 'ParlorGame':
                    pass
                else:
                    self.guiMgr.messageStack.showLoot([], gold=gain)
        self.money = money

    @report(types=['deltaStamp', 'module', 'args'], dConfigParam='want-shipboard-report')
    def _setCrewShip(self, ship):
        crewShip = self.crewShip
        if crewShip and crewShip != ship:
            crewShip.hideStatusDisplay()
            if self.guiMgr and self.guiMgr.mapPage:
                self.guiMgr.mapPage.removeShip(crewShip.doId)
        DistributedPlayerPirate._setCrewShip(self, ship)
        if ship:
            self.b_setTeleportFlag(PiratesGlobals.TFOnShip, self.crewShip.confirmOnShipTeleport)
            self.b_setTeleportFlag(PiratesGlobals.TFNotSameCrew, self.crewShip.confirmSameCrewTeleport)
            self.b_setTeleportFlag(PiratesGlobals.TFSiegeCaptain, self.crewShip.confirmSiegeCaptainTeleport)
            ship.showStatusDisplay()
            self.d_requestCurrentIsland(0)
            if self.guiMgr and self.guiMgr.mapPage:
                pos = base.cr.activeWorld.getWorldPos(ship)
                self.guiMgr.mapPage.addShip(ship.getShipInfo(), pos)
        else:
            self.b_clearTeleportFlag(PiratesGlobals.TFOnShip)
            self.b_clearTeleportFlag(PiratesGlobals.TFNotSameCrew)
            self.b_clearTeleportFlag(PiratesGlobals.TFSiegeCaptain)

    @report(types=['deltaStamp', 'module', 'args'], dConfigParam='want-shipboard-report')
    def setActiveShipId(self, shipId):
        DistributedPlayerPirate.setActiveShipId(self, shipId)
        messenger.send('activeShipChange', sentArgs=[shipId])

    def setReturnLocation(self, returnLocation):
        DistributedPlayerPirate.setReturnLocation(self, returnLocation)

        def setIt(inventory, returnLocation=returnLocation):
            if inventory:
                if inventory.getShipDoIdList():
                    self.guiMgr.mapPage.setReturnIsland(returnLocation)
                else:
                    self.guiMgr.mapPage.setReturnIsland(LocationIds.PORT_ROYAL_ISLAND)

        DistributedInventoryBase.getInventory(self.inventoryId, setIt)

    @report(types=['frameCount', 'args'], dConfigParam='want-map-report')
    def setCurrentIsland(self, islandUid):
        DistributedPlayerPirate.setCurrentIsland(self, islandUid)
        if self.guiMgr:
            if self.guiMgr.mapPage:
                self.guiMgr.mapPage.setCurrentIsland(islandUid)
            self.guiMgr.radarGui.showLocation(islandUid)

    def setJailCellIndex(self, index):
        DistributedPlayerPirate.setJailCellIndex(self, index)
        messenger.send('localAvatar-setJailCellIndex', [index])

    def setCurrentTarget(self, targetId):
        target = self.cr.doId2do.get(targetId)
        if target == self.currentTarget:
            return
        if self.currentTarget:
            self.currentTarget.setLocalTarget(0)
            if self.currentTarget.state == 'Use':
                self.currentTarget.request('Idle')
        self.currentTarget = target
        if target:
            if (not hasattr(target, 'currentDialogMovie') or target.currentDialogMovie == None) and target.hideHpMeterFlag == 0:
                target.showHpMeter()
            if self.gameFSM.state == 'Battle':
                self.startLookAtTarget()
            target.setLocalTarget(1)
            target.request('Use')
        else:
            self.stopLookAtTarget()
        self.cr.interactionMgr.start()
        DistributedPlayerPirate.setCurrentTarget(self, targetId)
        return

    def delete(self):
        try:
            self.LocalPirate_deleted
        except:
            self.LocalPirate_deleted = 1
            self.guiMgr.delete()
            del self.guiMgr
            self.cameraFSM.cleanup()
            del self.cameraFSM
            del self.currentMouseOver
            self.currentAimOver = None
            del self.currentSelection
            del self.skillDiary
            self.cr.avatarFriendsManager.reset()
            DistributedPlayerPirate.delete(self)
            taskMgr.remove(self.uniqueName('questShow'))
            taskMgr.remove(self.uniqueName('oceanCheck'))
            self.currentStoryQuests = []
            LocalAvatar.delete(self)
            if self.cloudScudEffect:
                self.cloudScudEffect.stopLoop()
                self.cloudScudEffect = None
            self.questStatus.delete()
            del self.questStatus
            self.__cleanupGuildDialog()
            self.__cleanupMoraleDialog()
            del base.localAvatar
            del __builtins__['localAvatar']

        return

    def targetMgrCreated(self):
        self.startLookAroundTask()

    def generate(self):
        base.localAvatar = self
        __builtins__['localAvatar'] = self
        DistributedPlayerPirate.generate(self)

    def announceGenerate(self):
        self.invInterest = self.addInterest(2, 'localAvatar-inventory')
        if self.guildId:
            self.cr.guildManager.addInterest(self.guildId, self.uniqueName('guild'))
        self.nametag.manage(base.marginManager)
        self.controlManager.setTag('avId', str(self.getDoId()))
        pe = PolylightEffect.make()
        brightness = 1.25
        darkness = 0.8
        pe.setWeight(brightness)
        self.node().setEffect(pe)
        DistributedPlayerPirate.announceGenerate(self)
        posHpr = (0, 0, 0, 0, 0, 0)
        self.setPosHpr(*posHpr)
        self.acceptOnce('targetMgrCreated', self.targetMgrCreated)
        if base.config.GetBool('osd-anim-blends', 0):
            self.toggleOsdAnimBlends(True)
        self.acceptOnce('generate-%s' % self.getInventoryId(), self.initInventoryGui)
        self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), InventoryType.GoldInPocket), self.setMoney)
        for weaponId in WeaponGlobals.getHumanWeaponTypes():
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), weaponId), self.refreshInventoryWeapons)

        for skillId in range(InventoryType.begin_WeaponSkillMelee, InventoryType.end_WeaponSkillMelee):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs=[skillId])

        for skillId in range(InventoryType.begin_WeaponSkillCutlass, InventoryType.end_WeaponSkillCutlass):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs=[skillId])

        for skillId in range(InventoryType.begin_WeaponSkillPistol, InventoryType.end_WeaponSkillPistol):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs=[skillId])

        for skillId in range(InventoryType.begin_WeaponSkillMusket, InventoryType.end_WeaponSkillMusket):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs=[skillId])

        for skillId in range(InventoryType.begin_WeaponSkillBayonet, InventoryType.end_WeaponSkillBayonet):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs=[skillId])

        for skillId in range(InventoryType.begin_WeaponSkillDagger, InventoryType.end_WeaponSkillDagger):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs=[skillId])

        for skillId in range(InventoryType.begin_SkillSailing, InventoryType.end_SkillSailing):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs=[skillId])

        for skillId in range(InventoryType.begin_WeaponSkillCannon, InventoryType.end_ExtendedWeaponSkillCannon):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs=[skillId])

        for skillId in range(InventoryType.begin_WeaponSkillDoll, InventoryType.end_WeaponSkillDoll):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs=[skillId])

        for skillId in range(InventoryType.begin_WeaponSkillWand, InventoryType.end_WeaponSkillWand):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), skillId), self.guiMgr.updateSkillUnlock, extraArgs=[skillId])

        for teleportTokenId in range(InventoryType.begin_TeleportToken, InventoryType.end_TeleportToken):
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), teleportTokenId), self.guiMgr.mapPage.updateTeleportIsland, extraArgs=[teleportTokenId])

        for repCategory in ReputationGlobals.getReputationCategories():
            self.accept('inventoryAccumulator-%s-%s' % (self.getInventoryId(), repCategory), self.updateReputation, extraArgs=[repCategory])

        for unCat in ReputationGlobals.getUnspentCategories():
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), unCat), self.guiMgr.updateUnspent, extraArgs=[unCat])

        for tonicId in InventoryType.Potions:
            self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), tonicId), self.guiMgr.updateTonic)

        self.guiMgr.combatTray.updateBestTonic()
        self.accept('inventoryQuantity-%s-%s' % (self.getInventoryId(), InventoryType.ShipRepairKit), self.guiMgr.updateShipRepairKit)
        self.guiMgr.combatTray.updateShipRepairKits()
        taskMgr.add(self.shadowReach, 'shadowReach', priority=40)
        self.accept('enterWater', self.handleWaterIn)
        self.accept('againWater', self.handleWaterAgain)
        self.accept('exitWater', self.handleWaterOut)
        if self.style.getTutorial() < PiratesGlobals.TUT_GOT_COMPASS and not base.config.GetBool('teleport-all', 0):
            self.b_setTeleportFlag(PiratesGlobals.TFNoCompass)
        if not base.launcher.getPhaseComplete(5):
            self.b_setTeleportFlag(PiratesGlobals.TFPhaseIncomplete)
            self.accept('phaseComplete-5', self.handlePhaseComplete, extraArgs=[5])
        self.accept('InputState-forward', self.checkInputState)
        self.accept('InputState-reverse', self.checkInputState)
        self.accept('InputState-turnLeft', self.checkInputState)
        self.accept('InputState-turnRight', self.checkInputState)

    def disable(self):
        self.ignore('generate-%s' % self.getInventoryId())
        self.ignore('inventoryQuantity-%s-%s' % (self.getInventoryId(), InventoryType.GoldInPocket))
        self.ignore('inventoryQuantity-%s-%s' % (self.getInventoryId(), InventoryType.Dinghy))
        self.ignore('inventoryAddDoId-%s-%s' % (self.getInventoryId(), InventoryCategory.SHIPS))
        self.ignore('inventoryRemoveDoId-%s-%s' % (self.getInventoryId(), InventoryCategory.SHIPS))
        self.ignore('control-f3')
        self.ignore('shift-f12')
        self.ignore('enterWater')
        self.ignore('againWater')
        self.ignore('exitWater')
        self.ignore('phaseComplete-5')
        self.ignore(self.cr.getAllInterestsCompleteEvent())
        taskMgr.remove(self.taskName('irisIn'))
        self.disableQuestArrow()
        if self.arrowPlacer:
            self.arrowPlacer.delete()
            self.arrowPlacer = None
        self.clearBattleTeleportFlag(send=False)
        self.shipList = []
        self.nametag.unmanage(base.marginManager)
        del self.invInterest
        if self.openJailDoorTrack:
            self.openJailDoorTrack.pause()
            self.openJailDoorTrack = None
        taskMgr.remove(self.uniqueName('monitorStickyTargets'))
        taskMgr.remove('localAvLookAtTarget')
        base.chatAssistant.clearHistory()
        base.chatPanel.updateDisplay()
        self.ignore('InputState-forward')
        self.ignore('InputState-backward')
        self.ignore('uber-enter')
        taskMgr.remove('autoAFK')
        self.cleanupLocalProjectiles()
        messenger.send('localPirateDisabled')
        DistributedPlayerPirate.disable(self)
        return

    def clearInventoryInterest(self):
        self.removeInterest(self.invInterest, event=self.uniqueName('localAvatar-close-inventory'))

    def handlePhaseComplete(self, phase):
        DistributedPlayerPirate.handlePhaseComplete(self, phase)
        if phase == 5:
            self.b_clearTeleportFlag(PiratesGlobals.TFPhaseIncomplete)

    def initInventoryGui(self, inventory):
        gold = inventory.getGoldInPocket()
        self.setMoney(gold)
        self.refreshInventoryWeapons()

    def refreshInventoryWeapons(self, args=None):
        self.equipBestWeapons()
        self.guiMgr.refreshInventoryWeapons()

    def equipBestWeapons(self):
        inventory = self.getInventory()
        if not inventory:
            return
        self.equippedWeapons = [0, 0, 0, 0, 0, 0]
        if inventory.getStackQuantity(InventoryType.CutlassWeaponL6) > 0:
            self.equippedWeapons[0] = InventoryType.CutlassWeaponL6
        else:
            if inventory.getStackQuantity(InventoryType.CutlassWeaponL5) > 0:
                self.equippedWeapons[0] = InventoryType.CutlassWeaponL5
            else:
                if inventory.getStackQuantity(InventoryType.CutlassWeaponL4) > 0:
                    self.equippedWeapons[0] = InventoryType.CutlassWeaponL4
                else:
                    if inventory.getStackQuantity(InventoryType.CutlassWeaponL3) > 0:
                        self.equippedWeapons[0] = InventoryType.CutlassWeaponL3
                    else:
                        if inventory.getStackQuantity(InventoryType.CutlassWeaponL2) > 0:
                            self.equippedWeapons[0] = InventoryType.CutlassWeaponL2
                        else:
                            if inventory.getStackQuantity(InventoryType.CutlassWeaponL1) > 0:
                                self.equippedWeapons[0] = InventoryType.CutlassWeaponL1
        if inventory.getStackQuantity(InventoryType.PistolWeaponL6) > 0:
            self.equippedWeapons[1] = InventoryType.PistolWeaponL6
        else:
            if inventory.getStackQuantity(InventoryType.PistolWeaponL5) > 0:
                self.equippedWeapons[1] = InventoryType.PistolWeaponL5
            else:
                if inventory.getStackQuantity(InventoryType.PistolWeaponL4) > 0:
                    self.equippedWeapons[1] = InventoryType.PistolWeaponL4
                else:
                    if inventory.getStackQuantity(InventoryType.PistolWeaponL3) > 0:
                        self.equippedWeapons[1] = InventoryType.PistolWeaponL3
                    else:
                        if inventory.getStackQuantity(InventoryType.PistolWeaponL2) > 0:
                            self.equippedWeapons[1] = InventoryType.PistolWeaponL2
                        else:
                            if inventory.getStackQuantity(InventoryType.PistolWeaponL1) > 0:
                                self.equippedWeapons[1] = InventoryType.PistolWeaponL1
        if inventory.getStackQuantity(InventoryType.DollWeaponL6) > 0:
            self.equippedWeapons[2] = InventoryType.DollWeaponL6
        else:
            if inventory.getStackQuantity(InventoryType.DollWeaponL5) > 0:
                self.equippedWeapons[2] = InventoryType.DollWeaponL5
            else:
                if inventory.getStackQuantity(InventoryType.DollWeaponL4) > 0:
                    self.equippedWeapons[2] = InventoryType.DollWeaponL4
                else:
                    if inventory.getStackQuantity(InventoryType.DollWeaponL3) > 0:
                        self.equippedWeapons[2] = InventoryType.DollWeaponL3
                    else:
                        if inventory.getStackQuantity(InventoryType.DollWeaponL2) > 0:
                            self.equippedWeapons[2] = InventoryType.DollWeaponL2
                        else:
                            if inventory.getStackQuantity(InventoryType.DollWeaponL1) > 0:
                                self.equippedWeapons[2] = InventoryType.DollWeaponL1
        if inventory.getStackQuantity(InventoryType.DaggerWeaponL6) > 0:
            self.equippedWeapons[3] = InventoryType.DaggerWeaponL6
        else:
            if inventory.getStackQuantity(InventoryType.DaggerWeaponL5) > 0:
                self.equippedWeapons[3] = InventoryType.DaggerWeaponL5
            else:
                if inventory.getStackQuantity(InventoryType.DaggerWeaponL4) > 0:
                    self.equippedWeapons[3] = InventoryType.DaggerWeaponL4
                else:
                    if inventory.getStackQuantity(InventoryType.DaggerWeaponL3) > 0:
                        self.equippedWeapons[3] = InventoryType.DaggerWeaponL3
                    else:
                        if inventory.getStackQuantity(InventoryType.DaggerWeaponL2) > 0:
                            self.equippedWeapons[3] = InventoryType.DaggerWeaponL2
                        else:
                            if inventory.getStackQuantity(InventoryType.DaggerWeaponL1) > 0:
                                self.equippedWeapons[3] = InventoryType.DaggerWeaponL1
        if inventory.getStackQuantity(InventoryType.GrenadeWeaponL6) > 0:
            self.equippedWeapons[4] = InventoryType.GrenadeWeaponL6
        else:
            if inventory.getStackQuantity(InventoryType.GrenadeWeaponL5) > 0:
                self.equippedWeapons[4] = InventoryType.GrenadeWeaponL5
            else:
                if inventory.getStackQuantity(InventoryType.GrenadeWeaponL4) > 0:
                    self.equippedWeapons[4] = InventoryType.GrenadeWeaponL4
                else:
                    if inventory.getStackQuantity(InventoryType.GrenadeWeaponL3) > 0:
                        self.equippedWeapons[4] = InventoryType.GrenadeWeaponL3
                    else:
                        if inventory.getStackQuantity(InventoryType.GrenadeWeaponL2) > 0:
                            self.equippedWeapons[4] = InventoryType.GrenadeWeaponL2
                        else:
                            if inventory.getStackQuantity(InventoryType.GrenadeWeaponL1) > 0:
                                self.equippedWeapons[4] = InventoryType.GrenadeWeaponL1
        if inventory.getStackQuantity(InventoryType.WandWeaponL6) > 0:
            self.equippedWeapons[5] = InventoryType.WandWeaponL6
        else:
            if inventory.getStackQuantity(InventoryType.WandWeaponL5) > 0:
                self.equippedWeapons[5] = InventoryType.WandWeaponL5
            else:
                if inventory.getStackQuantity(InventoryType.WandWeaponL4) > 0:
                    self.equippedWeapons[5] = InventoryType.WandWeaponL4
                else:
                    if inventory.getStackQuantity(InventoryType.WandWeaponL3) > 0:
                        self.equippedWeapons[5] = InventoryType.WandWeaponL3
                    else:
                        if inventory.getStackQuantity(InventoryType.WandWeaponL2) > 0:
                            self.equippedWeapons[5] = InventoryType.WandWeaponL2
                        else:
                            if inventory.getStackQuantity(InventoryType.WandWeaponL1) > 0:
                                self.equippedWeapons[5] = InventoryType.WandWeaponL1
        if not self.currentWeaponId:
            self.currentWeaponId = self.equippedWeapons[0]
        self.guiMgr.setEquippedWeapons(self.equippedWeapons)
        self.l_setCurrentWeapon(self.currentWeaponId, self.isWeaponDrawn)
        self.d_requestCurrentWeapon(self.currentWeaponId, self.isWeaponDrawn)

    def died(self):
        pass

    def setupControls(self):
        floorOffset = OTPGlobals.FloorOffset
        reach = 8.0
        avatarRadius = 1.4
        controls = BattleWalker.BattleWalker()
        controls.setWallBitMask(OTPGlobals.WallBitmask | PiratesGlobals.GoldBitmask)
        controls.setFloorBitMask(OTPGlobals.FloorBitmask)
        controls.initializeCollisions(self.cTrav, self, avatarRadius, floorOffset, reach)
        controls.setAirborneHeightFunc(self.getAirborneHeight)
        self.controlManager.add(controls, 'battle')
        self.setupWalkControls(avatarRadius=1.4, floorOffset=OTPGlobals.FloorOffset, reach=reach, wallBitmask=OTPGlobals.WallBitmask | PiratesGlobals.GoldBitmask, floorBitmask=OTPGlobals.FloorBitmask, ghostBitmask=OTPGlobals.GhostBitmask)
        self.enableRun()
        self.startListenAutoRun()

    def startListenAutoRun(self):
        self.accept('shift-r', self.startAutoRun)
        self.accept('r', self.toggleAutoRun)

    def stopListenAutoRun(self):
        self.ignore('shift-r')
        self.ignore('r')

    def toggleAutoRun(self):
        if self.enableAutoRun:
            self.stopAutoRun()
        else:
            self.startAutoRun()

    def toggleTurbo(self):
        if self.__turboOn:
            self.__turboOn = 0
        else:
            self.__turboOn = 1

    def getTurbo(self):
        return self.__turboOn

    def toggleMario(self):
        if __dev__:
            if self.__marioOn:
                self.__marioOn = 0
                self.setSwiftness(1.0)
            else:
                self.__marioOn = 1
                self.setSwiftness(6.0)

    def getMario(self):
        return self.__marioOn

    def initializeCollisions(self):
        LocalAvatar.initializeCollisions(self)
        cRay = CollisionRay(0.0, 0.0, 8.0, 0.0, 0.0, -1.0)
        cRayNode = CollisionNode('LP.cRayNode')
        cRayNode.addSolid(cRay)
        cRayNode.setFromCollideMask(OTPGlobals.FloorBitmask)
        cRayNode.setIntoCollideMask(BitMask32.allOff())
        self.cFloorNodePath = self.attachNewNode(cRayNode)
        self.floorEventHandler = CollisionHandlerEvent()
        self.floorEventHandler.addInPattern('enterFloor%in')
        self.floorEventHandler.addOutPattern('exitFloor%in')
        cRay = CollisionRay(0.0, 0.0, 8.0, 0.0, 0.0, -1.0)
        cRayNode2 = CollisionNode('LP.cRayNode2')
        cRayNode2.addSolid(cRay)
        cRayNode2.setFromCollideMask(PiratesGlobals.WaterBitmask)
        cRayNode2.setIntoCollideMask(BitMask32.allOff())
        self.cWaterNodePath = self.attachNewNode(cRayNode2)
        self.waterEventHandler = CollisionHandlerEvent()
        self.waterEventHandler.addInPattern('enterWater')
        self.waterEventHandler.addAgainPattern('againWater')
        self.waterEventHandler.addOutPattern('exitWater')

    def deleteCollisions(self):
        LocalAvatar.deleteCollisions(self)
        self.cFloorNodePath.removeNode()
        self.cWaterNodePath.removeNode()
        del self.floorEventHandler
        del self.waterEventHandler

    def collisionsOn(self):
        LocalAvatar.collisionsOn(self)
        self.cTrav.addCollider(self.cFloorNodePath, self.floorEventHandler)
        self.cTrav.addCollider(self.cWaterNodePath, self.waterEventHandler)

    def collisionsOff(self):
        LocalAvatar.collisionsOff(self)
        self.cTrav.removeCollider(self.cFloorNodePath)
        self.cTrav.removeCollider(self.cWaterNodePath)

    def initializeBattleCollisions(self):
        if self.aimTubeNodePaths:
            return
        self.aimTubeEvent = self.uniqueName('aimTube')
        aimTube = CollisionTube(0, 0, 0, 0, 0, self.height, self.battleTubeRadius * 1.5)
        aimTube.setTangible(0)
        aimTubeNode = CollisionNode(self.aimTubeEvent)
        aimTubeNode.addSolid(aimTube)
        aimTubeNode.setIntoCollideMask(PiratesGlobals.BattleAimBitmask)
        aimTubeNodePath = self.attachNewNode(aimTubeNode)
        aimTubeNodePath.setTag('objType', str(PiratesGlobals.COLL_AV))
        aimTubeNodePath.setTag('avId', str(self.doId))
        self.aimTubeNodePaths.append(aimTubeNodePath)

    def setupAnimationEvents(self):
        pass

    def clearPageUpDown(self):
        if self.isPageDown or self.isPageUp:
            self.lerpCameraFov(PiratesGlobals.DefaultCameraFov, 0.6)
            self.isPageDown = 0
            self.isPageUp = 0
            self.setCameraPositionByIndex(self.cameraIndex)

    def getClampedAvatarHeight(self):
        return max(self.getHeight(), 3.0)

    def isLocal(self):
        return 1

    def canChat(self):
        if self.cr.allowOpenChat():
            return 1
        if self.commonChatFlags & (OTPGlobals.CommonChat | OTPGlobals.SuperChat):
            return 1
        return 0

    def startChat(self):
        LocalAvatar.startChat(self)
        self.accept('chatUpdateSCQuest', self.b_setSpeedChatQuest)
        self.ignore(PiratesGlobals.ThinkPosHotkey)
        self.accept(PiratesGlobals.ThinkPosHotkey, self.thinkPos)
        self.ignore(PiratesGlobals.SpeedChatHotkey)
        self.accept(PiratesGlobals.SpeedChatHotkey, self.openSpeedChat)

    def stopChat(self):
        LocalAvatar.stopChat(self)
        self.ignore('chatUpdateSCQuest')
        self.ignore(PiratesGlobals.ThinkPosHotkey)
        self.ignore(PiratesGlobals.SpeedChatHotkey)

    def isMap(self):
        return self.name == 'map'

    def thinkPos(self):
        pos = self.getPos(render)
        hpr = self.getHpr(render)
        serverVersion = base.cr.getServerVersion()
        districtName = base.cr.getShardName(self.defaultShard)
        parentId = self.parentId
        zoneId = self.zoneId
        parent = self.cr.doId2do.get(parentId)
        model = None
        if parent:
            pos = self.getPos(parent)
            hpr = self.getHpr(parent)
            if isinstance(parent, DistributedShip.DistributedShip):
                model = parent.getPrefix()
                model = model.split('/')[-1]
            elif isinstance(parent, DistributedGameArea.DistributedGameArea):
                model = parent.modelPath
                model = model.split('/')[-1]
        strPos = '\nMaya Pos: \n%.1f, %.1f, %.1f' % (pos[0], pos[2], -pos[1]) + '\nPanda Pos: \n%.1f, %.1f, %.1f' % (pos[0], pos[1], pos[2]) + '\nH: %.1f' % hpr[0] + '\nModel: %s' % model + '\nTexture: %s, Terrain: %s, Avatar: %s' % (base.options.getTextureScaleString(), base.options.getGameOptionString(base.options.terrain_detail_level), base.options.getGameOptionString(base.options.character_detail_level)) + '\nLoc: (%s, %s)' % (str(parentId), str(zoneId)) + ',\nVer: %s, ' % serverVersion + '\nDistrict: %s' % districtName
        print 'Current position=', strPos.replace('\n', ', ')
        self.setChatAbsolute(strPos, CFThought | CFTimeout)
        return

    def openSpeedChat(self):
        pass

    def setSwiftness(self, swiftness):
        DistributedPlayerPirate.setSwiftness(self, swiftness)
        self.updatePlayerSpeed()

    def setSwiftnessMod(self, swiftness):
        DistributedPlayerPirate.setSwiftnessMod(self, swiftness)
        self.notify.debug('LocalPirate: setSwiftnessMod %s' % swiftness)
        self.updatePlayerSpeed()

    def setStunMod(self, stun):
        DistributedPlayerPirate.setStunMod(self, stun)
        self.notify.debug('LocalPirate: setStunMod %s' % stun)
        self.updatePlayerSpeed()

    def setHasteMod(self, haste):
        DistributedPlayerPirate.setHasteMod(self, haste)
        self.notify.debug('LocalPirate: setHasteMod %s' % haste)
        self.updatePlayerSpeed()

    def setAimMod(self, stun):
        DistributedPlayerPirate.setAimMod(self, stun)
        self.updatePlayerSpeed()

    def updatePlayerSpeed(self):
        speedMult = self.swiftness + self.hasteMod + self.stunMod
        speedMult = max(speedMult, -1.0)
        if self.swiftness + self.swiftnessMod <= 0.0:
            speedMult = 0.0
        if speedMult > 0.5:
            speedMult += self.aimMod
        self.notify.debug('speedMult = %s' % speedMult)
        oldSpeeds = PiratesGlobals.PirateSpeeds[self.speedIndex]
        newSpeeds = map(lambda x: speedMult * x, oldSpeeds)
        self.controlManager.setSpeeds(*newSpeeds)

    def setWalkForWeapon(self):
        DistributedPlayerPirate.setWalkForWeapon(self)
        self.updatePlayerSpeed()

    def requestEnterBattle(self):
        if self.gameFSM.state == 'LandRoam':
            self.b_setGameState('Battle')
        else:
            if self.gameFSM.state == 'Battle':
                self.notify.debug('You are already in battle!')
            else:
                self.notify.debug('You cannot use weapons now.')

    def requestExitBattle(self):
        if self.gameFSM.state == 'Battle':
            if self.gameFSM.defaultState == 'Battle':
                self.b_setGameState('LandRoam')
            else:
                self.b_setGameState(self.gameFSM.defaultState)
        messenger.send('weaponSheathed')

    def autoBoardStopMove(self, task=None):
        inputState.releaseInputs('forward')
        inputState.releaseInputs('reverse')

    def enterSwimMode(self, task=None):
        self.prevDistSq = -1

    def exitSwimMode(self, task=None):
        pass

    def setupAutoShipBoarding(self):
        self.accept('use-swim-controls', self.enterSwimMode)
        self.accept('use-walk-controls', self.exitSwimMode)
        self.accept('use-ship-controls', self.exitSwimMode)
        self.prevDistSq = -1

    def togglePrintAnimBlends(self, enable=None):
        if not hasattr(self, '_printAnimBlends'):
            self._printAnimBlends = False
        if enable is None:
            enable = not self._printAnimBlends
        self._printAnimBlends = enable
        if enable:

            def doPrint(task, self=self):
                print 'AnimBlends:'
                self.printAnimBlends()
                print ''
                return task.cont

            taskMgr.add(doPrint, 'printAnimBlends')
            print 'togglePrintAnimBlends ON'
        else:
            taskMgr.remove('printAnimBlends')
            print 'togglePrintAnimBlends OFF'
        return

    def toggleOsdAnimBlends(self, enable=None):
        if not hasattr(self, '_osdAnimBlends'):
            self._osdAnimBlends = False
        if enable is None:
            enable = not self._osdAnimBlends
        self._osdAnimBlends = enable
        if enable:

            def doOsd(task, self=self):
                self.osdAnimBlends()
                return task.cont

            taskMgr.add(doOsd, 'osdAnimBlends')
            print 'toggleOsdAnimBlends ON'
        else:
            taskMgr.remove('osdAnimBlends')
            print 'toggleOsdAnimBlends OFF'
        return

    def toggleAvVis(self):
        self.getLOD('2000').toggleVis()
        self.find('**/drop_shadow*').toggleVis()

    def getAddInterestEventName(self):
        return self.uniqueName('addInterest')

    def getRemoveInterestEventName(self):
        return self.uniqueName('removeInterest')

    @report(types=['deltaStamp', 'module', 'args'], prefix='------', dConfigParam='want-teleport-report')
    def setInterest(self, parentId, zone, interestTags, event=None):
        context = self.cr.addInterest(parentId, zone, interestTags[0], event)
        if context:
            self.notify.debug('adding interest %d: %d %d' % (context.asInt(), parentId, zone))
            self.interestHandles.append([interestTags, context])
        else:
            self.notify.warning('Tried to set interest when shard was closed')

    @report(types=['deltaStamp', 'module', 'args'], prefix='------', dConfigParam='want-teleport-report')
    def clearInterest(self, event):
        if len(self.interestHandles) > 0:
            contextInfo = self.interestHandles[0]
            self.notify.debug('removing interest %d' % contextInfo[1])
            self.cr.removeInterest(contextInfo[1], event)
            self.interestHandles.remove(contextInfo)

    @report(types=['deltaStamp', 'module', 'args'], prefix='------', dConfigParam='want-teleport-report')
    def clearInterestNamed(self, callback, interestTags):
        toBeRemoved = []
        numInterests = 0
        for currContext in self.interestHandles:
            matchFound = False
            for currTag in interestTags:
                if currTag in currContext[0]:
                    matchFound = True
                    break

            if matchFound:
                context = currContext[1]
                self.notify.debug('removing interest %s' % context)
                self.cr.removeInterest(context, callback)
                toBeRemoved.append(currContext)
                numInterests += 1

        for currToBeRemoved in toBeRemoved:
            self.interestHandles.remove(currToBeRemoved)

        if numInterests == 0 and callback:
            messenger.send(callback)
        return numInterests

    @report(types=['deltaStamp', 'module', 'args'], prefix='------', dConfigParam='want-teleport-report')
    def replaceInterestTag(self, oldTag, newTag):
        for tags, handle in self.interestHandles:
            if oldTag in tags:
                tags.remove(oldTag)
                tags.append(newTag)
                base.cr.updateInterestDescription(handle, newTag)

    @report(types=['deltaStamp', 'module', 'args'], prefix='------', dConfigParam='want-teleport-report')
    def b_setLocation(self, parentId, zoneId, teleport=0):
        self.d_setLocation(parentId, zoneId)
        self.setLocation(parentId, zoneId, teleport)

    @report(types=['deltaStamp', 'module', 'args'], prefix='------', dConfigParam=['want-teleport-report', 'want-shipboard-report'])
    def setLocation(self, parentId, zoneId, teleport=0):
        messenger.send('localAvatar-setLocation', sentArgs=[parentId, zoneId])
        DistributedPlayerPirate.setLocation(self, parentId, zoneId, teleport)
        if self.isGenerated():
            self.cnode.setCurrL(zoneId)

    @report(types=['deltaStamp', 'module', 'args'], prefix='------', dConfigParam='want-teleport-report')
    def teleportToShard--- This code section failed: ---

1439       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             1  'notify'
           6  LOAD_ATTR             2  'debug'
           9  LOAD_CONST            1  'teleportToShard %s,%s'
          12  LOAD_FAST             1  'shardId'
          15  LOAD_FAST             2  'zoneId'
          18  BUILD_TUPLE_2         2  None
          21  BINARY_MODULO    
          22  CALL_FUNCTION_1       1  None
          25  POP_TOP          

1440      26  LOAD_FAST             0  'self'
          29  LOAD_ATTR             5  'cr'
          32  LOAD_ATTR             6  'loadingScreen'
          35  LOAD_ATTR             7  'show'
          38  CALL_FUNCTION_0       0  None
          41  POP_TOP          

1443      42  LOAD_FAST             0  'self'
          45  LOAD_ATTR             8  'getAddInterestEventName'
          48  CALL_FUNCTION_0       0  None
          51  STORE_FAST            4  'addEvent'

1444      54  LOAD_FAST             0  'self'
          57  LOAD_ATTR            10  'setInterest'
          60  LOAD_FAST             1  'shardId'
          63  LOAD_FAST             2  'zoneId'
          66  LOAD_CONST            3  'instanceInterest'
          69  BUILD_LIST_1          1  None
          72  LOAD_FAST             4  'addEvent'
          75  CALL_FUNCTION_4       4  None
          78  POP_TOP          

1445      79  LOAD_FAST             0  'self'
          82  LOAD_ATTR            11  'acceptOnce'
          85  LOAD_FAST             4  'addEvent'
          88  LOAD_FAST             0  'self'
          91  LOAD_ATTR            12  'handleTeleportToShardDone'

1446      94  LOAD_CONST            4  'extraArgs'
          97  LOAD_FAST             1  'shardId'
         100  LOAD_FAST             2  'zoneId'
         103  LOAD_FAST             3  'callbackEvent'
         106  BUILD_LIST_3          3  None
         109  CALL_FUNCTION_258   258  None
         112  POP_TOP          
         113  JUMP_FORWARD         20  'to 136'
         116  POP_TOP          

1448     117  LOAD_FAST             0  'self'
         120  LOAD_ATTR            12  'handleTeleportToShardDone'
         123  LOAD_FAST             1  'shardId'
         126  LOAD_FAST             2  'zoneId'
         129  LOAD_FAST             3  'callbackEvent'
         132  CALL_FUNCTION_3       3  None
         135  POP_TOP          
       136_0  COME_FROM           113  '113'

Parse error at or near `LOAD_FAST' instruction at offset 117

    @report(types=['deltaStamp', 'module', 'args'], prefix='------', dConfigParam='want-teleport-report')
    def handleTeleportToShardDone(self, shardId, zoneId, callbackEvent):
        self.notify.debug('handleTeleportToShardDone %s, %s' % (shardId, zoneId))
        self.b_setLocation(shardId, zoneId, teleport=1)
        messenger.send(callbackEvent)

    def setLootCarried(self, amt, maxCarry):
        DistributedPlayerPirate.setLootCarried(self, amt, maxCarry)
        if amt > 0 and maxCarry > 0:
            speedMult = 1.0 - 0.5 * self.lootCarried / maxCarry
            regularSpeeds = PiratesGlobals.PirateSpeeds[self.speedIndex]
            scaledSpeeds = map(lambda x: speedMult * x, regularSpeeds)
            self.controlManager.setSpeeds(*scaledSpeeds)
            self.av.updatePlayerSpeed()

    def printState(self):
        self.notify.warning('%s\n  %s\n  %s\n  %s\n  %s\n  %s' % (localAvatar, self.gameFSM, self.motionFSM, self.motionFSM.motionAnimFSM, self.cameraFSM, base.cr.interactionMgr))

    def playOuch(self, skillId, ammoSkillId, targetEffects, attacker, pos, targetBonus=0):
        DistributedPlayerPirate.playOuch(self, skillId, ammoSkillId, targetEffects, attacker, pos, targetBonus)
        self.setBattleTeleportFlag()
        if attacker and not attacker.isEmpty():
            self.guiMgr.hitFromOffscreen(attacker)
        if self.gameFSM.state in ('Digging', 'Searching', 'DoorKicking'):
            if TeamUtils.damageAllowed(attacker, self):
                messenger.send(InteractiveBase.END_INTERACT_EVENT)
                self.b_setGameState(self.gameFSM.defaultState)
        if WeaponGlobals.getSkillInterrupt(skillId) and self.isWeaponDrawn:
            if WeaponGlobals.getRepId(self.currentWeaponId) in WeaponGlobals.CHARGEABLE_WEAPONS:
                if self.guiMgr.combatTray.chargeTime > 0.8:
                    self.guiMgr.combatTray.interruptCharge()
                    self.sendUpdate('interrupted', [WeaponGlobals.C_INTERRUPTED])

    def hasEffect(self, effectId):
        for key in self.skillEffects.keys():
            if effectId == self.skillEffects[key][0]:
                return 1

        return 0

    def setBattleTeleportFlag(self):
        self.clearBattleTeleportFlag(send=False)
        self.b_setTeleportFlag(PiratesGlobals.TFInBattle)
        self.battleTeleportFlagTask = taskMgr.doMethodLater(15, self.clearBattleTeleportFlag, 'battleTeleportFlag', extraArgs=[])

    def clearBattleTeleportFlag(self, send=True):
        if self.battleTeleportFlagTask:
            taskMgr.remove(self.battleTeleportFlagTask)
            self.battleTeleportFlagTask = None
        if send:
            self.b_clearTeleportFlag(PiratesGlobals.TFInBattle)
        return

    def setupMovementSounds(self):
        runSand = base.loadSfx('audio/sfx_avatar_run_sandx2.mp3')
        walkSand = base.loadSfx('audio/sfx_avatar_walk_sandx2.mp3')
        runWood = base.loadSfx('audio/sfx_avatar_run_woodx2.mp3')
        walkWood = base.loadSfx('audio/sfx_avatar_walk_woodx2.mp3')
        swimSound = base.loadSfx('audio/sfx_avatar_swim.mp3')
        self.surfaceIndex = PiratesGlobals.SURFACE_DEFAULT
        self.movementIndex = PiratesGlobals.STAND_INDEX
        self.curMoveSound = None
        self.moveSound = {PiratesGlobals.STAND_INDEX: {PiratesGlobals.SURFACE_DEFAULT: None, PiratesGlobals.SURFACE_WATER: swimSound}, PiratesGlobals.WALK_INDEX: {PiratesGlobals.SURFACE_DEFAULT: walkSand, PiratesGlobals.SURFACE_WATER: swimSound, PiratesGlobals.SURFACE_WOOD: walkWood}, PiratesGlobals.RUN_INDEX: {PiratesGlobals.SURFACE_DEFAULT: runSand, PiratesGlobals.SURFACE_WATER: swimSound, PiratesGlobals.SURFACE_WOOD: runWood}, PiratesGlobals.REVERSE_INDEX: {PiratesGlobals.SURFACE_DEFAULT: walkSand, PiratesGlobals.SURFACE_WATER: swimSound, PiratesGlobals.SURFACE_WOOD: walkWood}, PiratesGlobals.STRAFE_LEFT_INDEX: {PiratesGlobals.SURFACE_DEFAULT: runSand, PiratesGlobals.SURFACE_WATER: swimSound, PiratesGlobals.SURFACE_WOOD: runWood}, PiratesGlobals.STRAFE_RIGHT_INDEX: {PiratesGlobals.SURFACE_DEFAULT: runSand, PiratesGlobals.SURFACE_WATER: swimSound, PiratesGlobals.SURFACE_WOOD: runWood}, PiratesGlobals.STRAFE_LEFT_DIAG_INDEX: {PiratesGlobals.SURFACE_DEFAULT: runSand, PiratesGlobals.SURFACE_WATER: swimSound, PiratesGlobals.SURFACE_WOOD: runWood}, PiratesGlobals.STRAFE_RIGHT_DIAG_INDEX: {PiratesGlobals.SURFACE_DEFAULT: runSand, PiratesGlobals.SURFACE_WATER: swimSound, PiratesGlobals.SURFACE_WOOD: runWood}, PiratesGlobals.STRAFE_LEFT_DIAG_REV_INDEX: {PiratesGlobals.SURFACE_DEFAULT: walkSand, PiratesGlobals.SURFACE_WATER: swimSound, PiratesGlobals.SURFACE_WOOD: walkWood}, PiratesGlobals.STRAFE_RIGHT_DIAG_REV_INDEX: {PiratesGlobals.SURFACE_DEFAULT: walkSand, PiratesGlobals.SURFACE_WATER: swimSound, PiratesGlobals.SURFACE_WOOD: walkWood}}
        return

    def setSurfaceIndex(self, surfaceIndex):
        if surfaceIndex != self.surfaceIndex:
            self._changeMoveSound(surfaceIndex, self.movementIndex)

    def setMovementIndex(self, movementIndex):
        if movementIndex != self.movementIndex:
            self._changeMoveSound(self.surfaceIndex, movementIndex)

    def _changeMoveSound(self, surfaceIndex, movementIndex):
        sound = None
        moveSound = self.moveSound.get(movementIndex)
        if moveSound:
            sound = moveSound.get(surfaceIndex)
            if not sound:
                sound = moveSound.get(PiratesGlobals.SURFACE_DEFAULT)
        if sound != self.curMoveSound:
            self.stopSound()
            if sound:
                base.playSfx(sound, looping=1, node=self, volume=0.4)
            self.curMoveSound = sound
        self.surfaceIndex = surfaceIndex
        self.movementIndex = movementIndex
        return

    def stopSound(self):
        if self.curMoveSound:
            self.curMoveSound.stop()
            self.curMoveSound = None
            self.surfaceIndex = None
            self.movementIndex = None
        return

    def refreshStatusTray(self):
        if self.isGenerated():
            self.guiMgr.gameGui.statusTray.updateHp(self.hp, self.maxHp)
            self.guiMgr.gameGui.statusTray.updateVoodoo(self.getTotalMojo(), self.maxMojo)
            self.guiMgr.gameGui.statusTray.updateStatusEffects(self.skillEffects)
            self.guiMgr.combatTray.updateBestTonic()
            if self.maxHp:
                hpFraction = float(self.hp) / float(self.maxHp)
                if hpFraction < 0.4:
                    self.guiMgr.gameGui.startHealthAlert()

    def getConeOriginNode(self):
        if self.cannon:
            return self.cannon.prop.pivot
        else:
            return self

    def composeRequestProjectileSkill(self, skillId, ammoSkillId, posHpr, charge=0):
        timestamp = 0
        self.sendRequestProjectileSkill(skillId, ammoSkillId, posHpr, charge, timestamp)
        skillResult = WeaponGlobals.RESULT_DELAY
        self.playSkillMovie(skillId, ammoSkillId, skillResult, charge)

    def composeRequestTargetedSkill(self, skillId, ammoSkillId, combo=0, charge=0):
        newPos = self.cr.targetMgr.getAimHitPos(self)
        if newPos:
            pos = [
             newPos[0], newPos[1], newPos[2]]
        else:
            pos = [
             0, 0, 0]
        if WeaponGlobals.getIsShipSkill(skillId) or ammoSkillId == InventoryType.ShipRepairKit:
            targetId = self.ship.getDoId()
            areaCenter = self.ship
            areaIdList = []
            if WeaponGlobals.getIsShout(skillId):
                if self.ship:
                    areaIdList = self.ship.getCrew()[:]
                    doId = self.getDoId()
                    if areaIdList.count(doId):
                        areaIdList.remove(doId)
        else:
            if WeaponGlobals.getIsDollAttackSkill(skillId):
                targetId = 0
                areaIdList = copy.copy(self.stickyTargets)
                friendlySkill = WeaponGlobals.isFriendlyFire(skillId)
                toRemove = []
                for avId in areaIdList:
                    av = self.cr.doId2do.get(avId)
                    if av:
                        if friendlySkill and TeamUtils.damageAllowed(self, av):
                            toRemove.append(avId)
                        elif not friendlySkill and not TeamUtils.damageAllowed(self, av):
                            toRemove.append(avId)
                    else:
                        toRemove.append(avId)

                for currToRemove in toRemove:
                    areaIdList.remove(currToRemove)

            else:
                if self.currentTarget and WeaponGlobals.getNeedTarget(skillId, ammoSkillId):
                    targetId = self.currentTarget.getDoId()
                    areaCenter = self.currentTarget
                else:
                    targetId = 0
                    areaCenter = self
                areaIdList = self.getAreaList(skillId, ammoSkillId, areaCenter, Point3(*pos), self.doId)
        skillResult = self.cr.battleMgr.doAttack(self, skillId, ammoSkillId, targetId, areaIdList, Point3(*pos), combo, charge)
        if skillResult == WeaponGlobals.RESULT_NOT_AVAILABLE and WeaponGlobals.getNeedTarget(skillId, ammoSkillId):
            messenger.send('skillFinished')
            return
        timestamp32 = 0
        self.sendRequestTargetedSkill(skillId, ammoSkillId, skillResult, targetId, areaIdList, timestamp32, pos, charge)
        attackerEffects, targetEffects = self.cr.battleMgr.getModifiedSkillEffects(self, self.currentTarget, skillId, ammoSkillId, charge)
        areaEffects = []
        for avId in areaIdList:
            av = base.cr.doId2do.get(avId)
            if av:
                skillTargetEffects = self.cr.battleMgr.getModifiedSkillEffects(self, av, skillId, ammoSkillId, charge)[1]
                areaEffects.append(skillTargetEffects)

        self.useTargetedSkill(skillId, ammoSkillId, skillResult, targetId, areaIdList, attackerEffects, targetEffects, areaEffects, timestamp32, pos, charge, localSignal=1)
        if attackerEffects != [0, 0, 0, 0, 0]:
            self.targetedWeaponHit(skillId, ammoSkillId, WeaponGlobals.RESULT_HIT, attackerEffects, self, pos)

    def composeRequestShipSkill(self, skillId, ammoSkillId):
        targetId = self.ship.getDoId()
        areaCenter = self.ship
        areaIdList = []
        skillResult = self.cr.battleMgr.doAttack(self, skillId, ammoSkillId, targetId, areaIdList, Point3(0, 0, 0), 0)
        if skillResult == WeaponGlobals.RESULT_NOT_AVAILABLE and WeaponGlobals.getNeedTarget(skillId, ammoSkillId):
            messenger.send('skillFinished')
            return
        timestamp32 = 0
        self.sendRequestShipSkill(skillId, ammoSkillId, skillResult, targetId, timestamp32)
        selfEffects, targetEffects = self.cr.battleMgr.getModifiedSkillEffects(self, self.currentTarget, skillId, ammoSkillId)
        target = base.cr.doId2do.get(targetId)
        if target:
            target.useShipSkill(skillId, ammoSkillId, skillResult, targetId, selfEffects, targetEffects, timestamp32, localSignal=1)
        self.skillDiary.startRecharging(skillId, ammoSkillId)

    def initCombatTray(self, rep):
        self.guiMgr.combatTray.initCombatTray(rep)

    def setStickyTargets(self, avList):
        DistributedPlayerPirate.setStickyTargets(self, avList)
        self.guiMgr.targetStatusTray.updateSticky(self.stickyTargets)
        if self.stickyTargets == []:
            taskMgr.remove(self.uniqueName('monitorStickyTargets'))
        else:
            self.startMonitorStickyTargets()

    def startMonitorStickyTargets(self):
        self.lastTick = 0
        if not taskMgr.hasTaskNamed(self.uniqueName('monitorStickyTargets')):
            taskMgr.add(self.monitorStickyTargets, self.uniqueName('monitorStickyTargets'))

    def monitorStickyTargets(self, task):
        TICK_DELAY = 1.0
        if task.time - self.lastTick > TICK_DELAY:
            for avId in self.stickyTargets:
                av = base.cr.doId2do.get(avId)
                if av is None or self.getDistance(av) > WeaponGlobals.getAttackRange(InventoryType.DollPoke):
                    self.sendRequestRemoveStickyTargets([avId])

            self.lastTick = task.time
        return task.cont

    def openJailDoor(self, index=1):
        stringIndex = str(index)
        jail = self.getParent().getParent()
        if jail == None or jail.isEmpty():
            return
        jail_door = jail.find('**/jail_door0' + stringIndex)
        jail_lock = jail.find('**/lock0' + stringIndex)
        jail_door_collision = jail.find('**/door_collision_0' + stringIndex)
        seq = Sequence(LerpHprInterval(jail_door, 1, VBase3(120, jail_door.getP(), jail_door.getR()), blendType='easeInOut'), duration=1.0)
        seq.start()
        self.openJailDoorTrack = seq
        jail_door_collision.setR(30)
        if not jail_lock.isEmpty():
            jail_lock.stash()
        return

    def beginTrackTarget(self, target, timer=-1):
        self.lookAtTarget = target
        self.lookAtTimer = timer
        taskMgr.add(self.trackTarget, 'localAvTrackTarget')

    def trackTarget(self, task):
        if self.lookAtTimer >= 0:
            if task.time > self.lookAtTimer:
                return task.done
        self.lookAt(self.lookAtTarget)
        return task.cont

    def endTrackTarget(self):
        taskMgr.remove('localAvTrackTarget')
        self.lookAtTarget = None
        return

    def startLookAtTarget(self):
        self.stopLookAroundTask()
        taskMgr.remove('localAvLookAtTarget')
        taskMgr.add(self.__lookAtTarget, 'localAvLookAtTarget', 49)

    def __lookAtTarget(self, task):
        if self.currentTarget and not self.currentTarget.isEmpty():
            if self.currentTarget.getY(self) < 0.0:
                self.headNode.setHpr(0, 0, 0)
            else:
                hFov = 120
                vFov = 60
                fromNode = self.lookFromNode
                toNode = self.lookToNode
                toNode.reparentTo(self.currentTarget)
                toNode.setZ(self.currentTarget.getHeight())
                fromNode.lookAt(toNode)
                pitch = max(-vFov * 0.5, min(vFov * 0.5, fromNode.getP()))
                heading = max(-hFov * 0.5, min(hFov * 0.5, fromNode.getH()))
                self.headNode.setHpr(0, heading, -pitch)
                toNode.detachNode()
        else:
            self.headNode.setHpr(0, 0, 0)
        return task.cont

    def stopLookAtTarget(self):
        taskMgr.remove('localAvLookAtTarget')
        self.lookToNode.detachNode()

    def testFacing(self):
        self.lastTick = 0
        taskMgr.add(self.findLegalTargets, self.uniqueName('findLegalTargets'))

    def findLegalTargets(self, task):
        TICK_DELAY = 0.5
        if task.time - self.lastTick > TICK_DELAY:
            for do in self.cr.doId2do.values():
                if hasattr(do, 'isNpc') and do.doId != self.doId:
                    self.checkViewingArc(do)

            self.lastTick = task.time
        return task.cont

    def checkViewingArc(self, target):
        self.lookAtDummy.lookAt(target)
        targetHeading = self.lookAtDummy.getH()
        if targetHeading > -45 and targetHeading < 45:
            return 1
        else:
            return 0

    def displayWhisper(self, fromAvId, chatString, whisperType):
        if base.cr.avatarFriendsManager.checkIgnored(fromAvId):
            return
        sender = base.cr.identifyAvatar(fromAvId)
        if not sender:
            self.notify.warning('displayWhisper: fromAvId: %s not found' % fromAvId)
            return
        if self.soundWhisper:
            base.playSfx(self.soundWhisper)

    def whisperTo(self, chatString, sendToId):
        recv = base.cr.identifyAvatar(sendToId)
        if recv:
            panelString = 'To %s: %s' % (recv.getName(), chatString)
        else:
            panelString = chatString
        DistributedPlayerPirate.whisperTo(self, chatString, sendToId)

    def setKickEvents(self, kickEventStart, kickEventConnect):
        self.kickEvents = [
         kickEventStart, kickEventConnect]

    def spendSkillPoint(self, skillId):
        self.sendUpdate('spendSkillPoint', [skillId])

    def resetSkillPoints(self, skillId):
        self.sendUpdate('resetSkillPoints', [skillId])

    def checkForAutoTrigger(self, objDoId):
        avInv = self.getInventory()
        if avInv == None:
            return
        questList = avInv.getQuestList()
        objRef = self.cr.doId2do.get(objDoId)
        if objRef == None:
            return
        instanceArea = False
        for currQuest in questList:
            questDNA = currQuest.getQuestDNA()
            if questDNA:
                questTasks = questDNA.getTasks()
            else:
                self.notify.warning('quest %s: does not contain a dna; is it a rogue quest, given in error?' % currQuest.getQuestId())
                return
            for currTask in questTasks:
                autoTriggerInfo = currTask.getAutoTriggerInfo()
                if len(autoTriggerInfo) > 0 and autoTriggerInfo[0] == QuestDB.AUTO_TRIGGER_OBJ_EXISTS:
                    firstObjId = autoTriggerInfo[1][0]
                    allObjsPresent = True
                    if objRef.getUniqueId() == firstObjId:
                        for objId in autoTriggerInfo[1]:
                            doId = self.cr.uidMgr.uid2doId.get(objId)
                            if self.cr.doId2do.get(doId) == None:
                                allObjsPresent = False
                                break

                        if allObjsPresent:
                            objRef.handleUseKey()
                        else:
                            taskMgr.doMethodLater(3, objRef.autoTriggerCheck, objRef.uniqueName('autoTriggerCheck'), extraArgs=[])
                        return

        return

    def swapFloorCollideMask(self, oldMask, newMask):
        cMask = self.cFloorNodePath.node().getFromCollideMask()
        cMask = cMask & ~oldMask
        cMask |= newMask
        self.cFloorNodePath.node().setFromCollideMask(cMask)
        for name in ['walk', 'battle', 'swim']:
            controls = self.controlManager.get(name)
            if controls:
                controls.swapFloorBitMask(oldMask, newMask)

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='want-shipboard-report')
    def placeOnShip(self, ship, pvp=False):
        messenger.send('islandPlayerBarrier', [0])
        oldParent = self.getParentObj()
        if oldParent and oldParent.isGridParent() and not pvp:
            oldParent.stopProcessVisibility()
        self.b_setLocation(ship.doId, PiratesGlobals.ShipZoneOnDeck)
        pos, h = ship.getClosestBoardingPosH()
        self.setPos(pos)
        self.setH(h)
        ship.turnOn()
        ship.localAvatarBoardShip()
        self.enterZoneLOD(ship)
        ship.unstashFloorCollisions()
        self.cnode.broadcastPosHprFull()
        ship.sendUpdate('shipBoarded')

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='want-shipboard-report')
    def removeFromShip(self, ship):
        ship.disableOnDeckInteractions()
        ship.stashFloorCollisions()
        ship.localAvatarExitShip()

    def startAutoRun(self):
        if self.enableAutoRun:
            return
        self.enableAutoRun = 1
        self.setAutoRun(1)
        self.accept('arrow_up', self.stopAutoRun)
        self.accept('arrow_down', self.stopAutoRun)
        self.accept('w', self.stopAutoRun)
        self.accept('s', self.stopAutoRun)

    def stopAutoRun(self):
        if not self.enableAutoRun:
            return
        self.enableAutoRun = 0
        self.setAutoRun(0)
        self.ignore('arrow_up')
        self.ignore('arrow_down')
        self.ignore('w')
        self.ignore('s')

    def getName(self):
        return self.title + self.name

    def doShowReset(self):
        self.showQuest = True

    def resetQuestShow(self):
        self.showQuest = False
        taskMgr.doMethodLater(2.0, self.doShowReset, self.uniqueName('questShow'), extraArgs=[])

    def setGuildId(self, guildId):
        DistributedPlayerPirate.setGuildId(self, guildId)
        if self.guildId:
            self.chatMgr.enableGuildChat()
        else:
            self.chatMgr.disableGuildChat()

    def setBandId(self, bandmanager, bandId):
        DistributedPlayerPirate.setBandId(self, bandmanager, bandId)
        if self.BandId:
            self.chatMgr.enableCrewChat()
        else:
            self.chatMgr.disableCrewChat()

    def setSiegeTeam(self, team):
        self._siegeTeamSV.set(team)
        if team:
            self.chatMgr.enableShipPVPChat()
        else:
            self.chatMgr.disableShipPVPChat()
        DistributedPlayerPirate.setSiegeTeam(self, team)

    def setTutorial(self, val):
        DistributedPlayerPirate.setTutorial(self, val)
        if val >= PiratesGlobals.TUT_GOT_COMPASS or base.config.GetBool('teleport-all', 0):
            self.b_clearTeleportFlag(PiratesGlobals.TFNoCompass)
        else:
            self.b_setTeleportFlag(PiratesGlobals.TFNoCompass)
        if val == PiratesGlobals.TUT_GOT_PISTOL:
            self.guiMgr.setEquippedWeapons(self.equippedWeapons)

    def startOceanCheck(self):
        if not taskMgr.hasTaskNamed(self.uniqueName('oceanCheck')):
            taskMgr.doMethodLater(10, self.checkCurrentOcean, self.uniqueName('oceanCheck'))

    def checkCurrentOcean(self, task):
        if self.ship:
            pos = self.ship.getPos(render)
            newOcean = OceanZone.getOceanZone(pos[0], pos[1])
            if self.currentOcean != newOcean:
                self.currentOcean = newOcean
                self.guiMgr.flashOceanMsg(PLocalizer.OceanZoneNames.get(newOcean))
            return task.again
        else:
            return task.done

    def l_setQuestStep(self, questStep):
        DistributedPlayerPirate.l_setQuestStep(self, questStep)
        if self.gameFSM.getCurrentOrNextState() == 'Cutscene':
            self.hideQuestArrow()

    def l_setActiveQuest(self, questId):
        DistributedPlayerPirate.l_setActiveQuest(self, questId)
        if hasattr(self.guiMgr, 'questPage'):
            if self.guiMgr.questPage is not None:
                self.guiMgr.questPage.titleList.showTracked(questId)
        return

    @report(types=['deltaStamp', 'args'], dConfigParam=['want-shipboard-report', 'want-teleport-report'])
    def wrtReparentTo(self, *args, **kw):
        DistributedPlayerPirate.wrtReparentTo(self, *args, **kw)

    def handleWaterIn(self, entry):
        self.enableWaterEffect()

    def handleWaterAgain(self, entry):
        offset = entry.getSurfacePoint(self).getZ()
        if offset < 0.0:
            self.disableWaterEffect()
        else:
            speeds = self.controlManager.getSpeeds()
            self.adjustWaterEffect((offset + 0.15), *speeds)

    def handleWaterOut(self, entry):
        self.disableWaterEffect()

    def enableQuestArrow(self, questIndicatorNode):
        if not questIndicatorNode or questIndicatorNode.isEmpty():
            return
        if not self.isGenerated():
            return
        if self.style.getTutorial() >= PiratesGlobals.TUT_GOT_PISTOL:
            self.disableQuestArrow()
            return
        if not self.questArrow:
            self.questArrow = loader.loadModelCopy('models/effects/arrow_ground')
            g = self.questArrow.getChild(0)
            g.setPos(0, -4, 0)
            g.setHpr(180, 0, 0)
            g.setScale(1.5)
            self.questArrow.reparentTo(self)
            self.questArrow.setDepthTest(0)
            self.questArrow.setBin('shadow', 1)
            self.questArrow.setLightOff()
            self.questArrow.setColorScale(PiratesGuiGlobals.TextFG8[0], PiratesGuiGlobals.TextFG8[1], 0, PiratesGuiGlobals.TextFG8[3])
            self.questArrow.node().setBounds(BoundingSphere(Point3(0, 0, 0), 6))
            self.questArrow.flattenStrong()
            self.arrowPlacer = ShadowPlacer(base.shadowTrav, self.questArrow, OTPGlobals.WallBitmask, OTPGlobals.FloorBitmask)
        self.questArrow.setEffect(BillboardEffect.make(Vec3(0, 0, 1), False, True, 0, questIndicatorNode, Point3(0)))
        self.questArrow.unstash()
        self.arrowPlacer.on()

    def setLifterDelayFrames(self, frames=0):
        self.motionFSM.setLifterDelayFrames(frames)

    def disableQuestArrow(self):
        if self.questArrow:
            self.questArrow.stash()
        if self.arrowPlacer:
            self.arrowPlacer.off()

    def showQuestArrow(self):
        if self.questArrow:
            if not self.noQuestArrow:
                self.questArrow.show()
                self.questArrow.setZ(0)
                self.questIndicator.showEffect()

    def hideQuestArrow(self):
        if self.questArrow:
            self.questArrow.hide()
            self.questIndicator.hideEffect()

    def queueStoryQuest(self, quest):
        self.currentStoryQuests.append(quest)
        if self.style.getTutorial() >= PiratesGlobals.TUT_MADE_PIRATE:
            self.l_setActiveQuest(quest.getQuestId())
            self.guiMgr.initQuestPage()

    def resetStoryQuest(self):
        self.currentStoryQuests = []

    def triggerNPCInteract(self):
        quest = self.getQuestById(self.activeQuestId)
        questGiverUid = quest.questDNA.getTasks()[0].npcId
        questGiverDoId = base.cr.uidMgr.uid2doId[questGiverUid]
        questGiver = base.cr.doId2do[questGiverDoId]
        questGiver.setQuestsCompleted(1, [self.activeQuestId], [], [], [])

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam=['want-shipboard-report', 'want-teleport-report'])
    def leaveZoneLOD(self, zoneLODObj):
        if __dev__:
            import pirates.world.ZoneLOD as ZoneLOD
        zoneLODObj.setZoneLevelOuter()

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam=['want-shipboard-report', 'want-teleport-report'])
    def enterZoneLOD(self, zoneLODObj):
        if __dev__:
            import pirates.world.ZoneLOD as ZoneLOD
        if self.controlManager.currentControls:
            collisionsOn = self.controlManager.currentControls.getCollisionsActive()
            self.collisionsOn()
            eventMgr.doEvents()
            self.controlManager.currentControls.cTrav.traverse(render)
            base.shadowTrav.traverse(render)
            eventMgr.doEvents()
            zoneLODObj.disableAllLODSpheres()
            self.controlManager.currentControls.cTrav.traverse(render)
            base.shadowTrav.traverse(render)
            eventMgr.eventQueue.clear()
            zoneLODObj.enableAllLODSpheres()
            self.controlManager.currentControls.cTrav.traverse(render)
            base.shadowTrav.traverse(render)
            eventMgr.doEvents()
            zoneLODObj.clearAllEnabled(True)
            if not collisionsOn:
                self.collisionsOff()
        else:
            self.notify.warning('localAvatar has no controls during teleport')

    if __dev__:

        def b_setGameState(self, *args, **kw):
            DistributedPlayerPirate.b_setGameState(self, *args, **kw)
            print 'b_setGameState', args, kw

        def printTS(self):
            print 'TeleportState\n-----------------------------'
            print 'location:', localAvatar.getLocation()
            print 'pos:', localAvatar.getPos(localAvatar.getParentObj())
            try:
                print 'lastZoneLevel:', localAvatar.getParentObj().lastZoneLevel
            except AttributeError:
                pass
            else:
                print '\nzoneSpheres:'
                for x in localAvatar.getParentObj().zoneSphere:
                    x.ls()

                print '\naccepting:'
                for x in localAvatar.getParentObj().getAllAccepting():
                    print x

            print '\ncTrav:'
            print base.cTrav

    def printIZL(self, reset=False):
        for x in self.cr.activeWorld.islands.itervalues():
            if reset:
                x.setZoneLevel(min(3, x.lastZoneLevel))
            print x.lastZoneLevel, x.getName(), x.doId

    def addStatusEffect(self, effectId, attackerId, duration):
        DistributedPlayerPirate.addStatusEffect(self, effectId, attackerId, duration)
        if effectId == WeaponGlobals.C_STUN:
            self.motionFSM.off()

    def removeStatusEffect(self, effectId, attackerId):
        DistributedPlayerPirate.removeStatusEffect(self, effectId, attackerId)
        if effectId == WeaponGlobals.C_STUN:
            self.motionFSM.on()

    def setDefaultShard(self, defaultShard):
        DistributedPlayerPirate.setDefaultShard(self, defaultShard)
        self.logDefaultShard()

    def logDefaultShard(self):
        pcrCat = DirectNotifyGlobal.directNotify.getCategory('PiratesClientRepository')
        sev = pcrCat.getSeverity()
        pcrCat.info('Current shard is: %s' % self.getDefaultShard())
        pcrCat.setSeverity(sev)

    def enableCloudScudEffect(self):
        if self.cloudScudEffect:
            return
        self.cloudScudEffect = CloudScud.getEffect()
        if self.cloudScudEffect:
            self.cloudScudEffect.reparentTo(self)
            self.cloudScudEffect.startLoop()

    def disableCloudScudEffect(self):
        if self.cloudScudEffect:
            self.cloudScudEffect.stopLoop()
            self.cloudScudEffect = None
        return

    @report(types=['deltaStamp'], prefix='------', dConfigParam='want-teleport-report')
    def teleportCleanupComplete(self, instanceType):
        if self.getJailCellIndex() == 100:
            self.b_setGameState(self.gameFSM.defaultState)
        self.setLifterDelayFrames(frames=3)
        self.cr.loadingScreen.scheduleHide(self.cr.getAllInterestsCompleteEvent())
        self.acceptOnce(self.cr.getAllInterestsCompleteEvent(), taskMgr.doMethodLater, [
         1, self.doFadeIn, self.taskName('irisIn')])
        if instanceType == PiratesGlobals.INSTANCE_PVP:
            self.setTeleportFlag(PiratesGlobals.TFInPVP)
        else:
            if instanceType == PiratesGlobals.INSTANCE_TUTORIAL:
                self.setTeleportFlag(PiratesGlobals.TFInTutorial)

    @report(types=['deltaStamp'], prefix='------', dConfigParam='want-teleport-report')
    def doFadeIn(self, task):
        try:
            task.fadeInDone
            if self.getJailCellIndex() == 100 and self.getGameState() not in ('WaterRoam', ):
                self.b_setGameState(self.gameFSM.defaultState)
            return task.done
        except AttributeError:
            task.fadeInDone = 1
            tutorialException = base.cr.tutorial & (self.style.tutorial == PiratesGlobals.TUT_STARTED)
            if not tutorialException:
                base.transitions.fadeIn()
            if self.teleportFriendDoId:
                friendId = self.teleportFriendDoId
                self.teleportFriendDoId = 0
            return task.again

    def setSoloInteraction(self, solo):
        self.soloInteraction = solo
        if solo:
            messenger.send('hideOtherAvatars')
        else:
            messenger.send('showOtherAvatars')

    def getSoloInteraction(self):
        return self.soloInteraction

    def initVisibleToCamera(self):
        pass

    def setGameState(self, gameState, timestamp=None, localArgs=[]):
        DistributedPlayerPirate.setGameState(self, gameState, timestamp, localArgs)
        if self.getGameState() not in ('LandRoam', ):
            self.cameraFSM.getFPSCamera().ignoreWheel()

    def motionFSMEnterState(self, anim):
        if anim == 'Idle' and self.getGameState() in ('LandRoam', ):
            self.cameraFSM.getFPSCamera().acceptWheel()
        else:
            self.cameraFSM.getFPSCamera().ignoreWheel()

    def motionFSMExitState(self, anim):
        if anim == 'Idle':
            self.cameraFSM.getFPSCamera().ignoreWheel()

    def updatePaidStatus(self):
        pStatus = base.cr.isPaid()
        if pStatus == 2:
            self.isPaid = True
        else:
            if pStatus == 1:
                self.isPaid = False

    def goAFK(self, task):
        if not self.isAFK:
            self.toggleAFK()
        return task.done

    def checkInputState(self, msg=None):
        if msg is True:
            self.delayAFK()

    def delayAFK(self, msg=None):
        if self.isAFK:
            self.toggleAFK()
        else:
            taskMgr.remove('autoAFK')
            taskMgr.doMethodLater(self.AFKDelay, self.goAFK, 'autoAFK')

    def toggleAFK(self):
        self.b_setAFK(not self.isAFK)
        if self.isAFK and self.getGameState() != 'Emote':
            self.requestEmote(PLocalizer.EMOTE_SLEEP)
        if not self.isAFK and self.getGameState() == 'Emote':
            self.b_setGameState('LandRoam')
        if not self.isAFK:
            taskMgr.remove('autoAFK')
            taskMgr.doMethodLater(self.AFKDelay, self.goAFK, 'autoAFK')

    def gotWeaponReward(self, rewardType):
        self.playRewardAnimation = PLocalizer.WeaponReceiveToEmoteCmds[rewardType]
        print 'received Weapon %s' % self.playRewardAnimation

    def addLocalProjectile(self, projectile):
        self.localProjectiles.append(projectile)

    def clearLocalProjectile(self, projectile):
        if projectile in self.localProjectiles:
            self.localProjectiles.remove(projectile)

    def cleanupLocalProjectiles(self):
        for currProj in self.localProjectiles:
            currProj.destroy()

    def addShipTarget(self, ship, priority=0):
        myShip = self.getShip()
        if myShip:
            myShip.addShipTarget(ship, priority)

    def setCannonAmmoSkillId(self, ammoSkillId):
        self._cannonAmmoSkillId = ammoSkillId

    def getCannonAmmoSkillId(self):
        return self._cannonAmmoSkillId

    def getShortName(self):
        return PLocalizer.You

    def setAllowGMNameTag(self, state):
        DistributedPlayerPirate.setAllowGMNameTag(self, state)
        if self.gmNameTagAllowed:
            if base.config.GetString('gm-nametag-string', '') != '':
                self.gmNameTagStringLocal = base.config.GetString('gm-nametag-string')
            if base.config.GetString('gm-nametag-color', '') != '':
                self.gmNameTagColorLocal = base.config.GetString('gm-nametag-color')
            if base.config.GetInt('gm-nametag-enabled', 0):
                self.gmNameTagEnabledLocal = 1
                self.b_updateGMNameTag(state, self.gmNameTagColorLocal, self.gmNameTagStringLocal)

    def setBadgeIcon(self, titleId, rank):
        DistributedPlayerPirate.setBadgeIcon(self, titleId, rank)
        if self.guiMgr.titlesPage:
            self.guiMgr.titlesPage.initLandTitleActive(titleId)
        self.refreshName()

    def changeBodyType(self):
        if self.gameFSM.getCurrentOrNextState() == 'Battle':
            self.b_setGameState('LandRoam')
        DistributedPlayerPirate.changeBodyType(self)

    def setZombie(self, value):
        DistributedPlayerPirate.setZombie(self, value)
        if value:
            self.b_setTeleportFlag(PiratesGlobals.TFZombie)
        else:
            self.b_clearTeleportFlag(PiratesGlobals.TFZombie)

    def triggerZombieEffect(self):
        from pirates.effects.JRSpawnEffect import JRSpawnEffect
        self.zombieEffect = JRSpawnEffect.getEffect()
        if self.zombieEffect:
            self.zombieEffect.reparentTo(self)
            self.zombieEffect.effectScale = 1.0
            self.zombieEffect.setPos(0, 1, 0)
            self.zombieIval = Sequence(Func(localAvatar.motionFSM.off), Func(self.zombieEffect.play), Func(localAvatar.play, 'death3'), Wait(1.7), Func(self.changeBodyType), Func(localAvatar.play, 'jail_standup', fromFrame=65), Wait(2.25), Func(localAvatar.motionFSM.on))
            self.zombieIval.start()

    def setCursed(self, value):
        self.cursed = True
        if self.zombie == value:
            return
        self.zombie = value
        if value and self.gameFSM.getCurrentOrNextState() != 'WaterRoam':
            self.triggerZombieEffect()
        else:
            self.changeBodyType()

    def setCursedStatus(self, value):
        if value == 0:
            base.cr.newsManager.displayMessage(6)
        else:
            if value == 1:
                base.cr.newsManager.displayMessage(5)
                base.playSfx(self.jollySfx)
            else:
                if value == 2:
                    base.cr.newsManager.displayMessage(4)

    def setShipBadgeIcon(self, titleId, rank):
        DistributedPlayerPirate.setShipBadgeIcon(self, titleId, rank)
        if self.guiMgr and hasattr(self.guiMgr, 'titlesPage') and self.guiMgr.titlesPage:
            localAvatar.guiMgr.titlesPage.initSeaTitleActive(titleId)

    def getAllowSocialPanel(self):
        return not hasattr(self, 'allowSocialPanel') or self.allowSocialPanel == True

    def setAllowSocialPanel(self, allow):
        self.allowSocialPanel = allow

    def displayMoraleMessage(self):
        inv = self.getInventory()
        if inv and self.getLevel() > 9:
            if inv.getStackQuantity(InventoryType.FirstDeathToken) > 0:
                return
            else:
                self.sendUpdate('flagFirstDeath', [])
        else:
            return
        self.__cleanupMoraleDialog()
        self.moralePopupDialog = PDialog.PDialog(text=PLocalizer.FirstDeathMsg, style=OTPDialog.Acknowledge, command=self.__cleanupMoraleDialog, destroyedCallback=self.__destroyedMoraleDialog)

    def __cleanupMoraleDialog(self, value=None):
        if self.moralePopupDialog:
            self.moralePopupDialog.destroy()
            self.moralePopupDialog = None
        return

    def __destroyedMoraleDialog(self):
        self.moralePopupDialog = None
        return

    def guildStatusUpdate(self, guildId, guildName, guildRank):
        self.setGuildId(guildId)
        self.setGuildRank(guildRank)
        self.setGuildName(guildName)
        self.guiMgr.guildPage.initGuildPage()
        messenger.send('Guild Status Updated', [])

    def guildNameReject(self, guildId):
        self.__cleanupGuildDialog()
        self.guildPopupDialog = PDialog.PDialog(text=PLocalizer.GuildNameDuplicate, style=OTPDialog.Acknowledge, command=self.__cleanupGuildDialog, destroyedCallback=self.__destroyedGuildDialog)

    def guildNameChange(self, guildName, change):
        if change == 2:
            title = PLocalizer.GuildNameRejectTitle
            mess = PLocalizer.GuildNameReject % guildName
        else:
            title = PLocalizer.GuildNameApproveTitle
            mess = PLocalizer.GuildNameApprove % guildName
        self.__cleanupGuildDialog()
        self.guildPopupDialog = PDialog.PDialog(text=mess, title_text=title, text_align=TextNode.ACenter, text_pos=(0, -0.4), style=OTPDialog.Acknowledge, command=self.__cleanupGuildDialog, destroyedCallback=self.__destroyedGuildDialog)

    def __cleanupGuildDialog(self, value=None):
        if self.guildPopupDialog:
            self.guildPopupDialog.destroy()
            self.guildPopupDialog = None
        return

    def __destroyedGuildDialog(self):
        self.guildPopupDialog = None
        return
