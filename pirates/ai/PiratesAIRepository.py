import time
import random

from panda3d.core import *

from direct.directnotify.DirectNotifyGlobal import directNotify

from otp.distributed.OtpDoGlobals import *
from otp.ai.TimeManagerAI import TimeManagerAI
from otp.friends.FriendManagerAI import FriendManagerAI

from pirates.ai.PiratesMagicWordManagerAI import PiratesMagicWordManagerAI
from pirates.distributed.PiratesInternalRepository import PiratesInternalRepository
from pirates.piratesbase import PiratesGlobals
from pirates.distributed.PiratesDistrictAI import PiratesDistrictAI
from pirates.distributed.DistrictTrackerAI import DistrictTrackerAI
from pirates.world import WorldGlobals
from pirates.ai.NewsManagerAI import NewsManagerAI
from pirates.quest.QuestManagerAI import QuestManagerAI
from pirates.piratesbase.UniqueIdManager import UniqueIdManager
from pirates.distributed.DistributedPopulationTrackerAI import DistributedPopulationTrackerAI
from pirates.instance.DistributedTeleportMgrAI import DistributedTeleportMgrAI
from pirates.piratesbase.DistributedTimeOfDayManagerAI import DistributedTimeOfDayManagerAI
from pirates.distributed.TargetManagerAI import TargetManagerAI
from pirates.battle.DistributedEnemySpawnerAI import DistributedEnemySpawnerAI
from pirates.trades.TradeManagerAI import TradeManagerAI
from pirates.world.WorldCreatorAI import WorldCreatorAI
from pirates.battle.BattleManagerAI import BattleManagerAI
from pirates.band.DistributedCrewMatchAI import DistributedCrewMatchAI
from pirates.band.DistributedPirateBandManagerAI import DistributedPirateBandManagerAI
from pirates.tutorial.PiratesTutorialManagerAI import PiratesTutorialManagerAI
from pirates.world.WorldGridManagerAI import WorldGridManagerAI
from pirates.ship.ShipManagerAI import ShipManagerAI
from pirates.discord.DiscordNotificationsAI import DiscordNotificationsAI


class PiratesAIRepository(PiratesInternalRepository):
    notify = directNotify.newCategory('PiratesAIRepository')

    def __init__(self, baseChannel, serverId, districtName):
        PiratesInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='AI')

        self.districtName = districtName
        self.zoneAllocator = UniqueIdAllocator(PiratesGlobals.DynamicZonesBegin,
            PiratesGlobals.DynamicZonesEnd)

        self.zoneId2owner = {}
        self.disconnectReasons = {}
        self.uidMgr = UniqueIdManager(self)
        self.districtTracker = None

    def getAvatarExitEvent(self, avId):
        return 'distObjDelete-%d' % avId

    def allocateZone(self, owner=None):
        zoneId = self.zoneAllocator.allocate()
        if owner:
            self.zoneId2owner[zoneId] = owner

        return zoneId

    def deallocateZone(self, zone):
        if self.zoneId2owner.get(zone):
            del self.zoneId2owner[zone]

        self.zoneAllocator.free(zone)

    def handleConnected(self):
        PiratesInternalRepository.handleConnected(self)
        self.districtId = self.allocateChannel()
        self.distributedDistrict = PiratesDistrictAI(self)
        self.distributedDistrict.setName(self.districtName)
        self.distributedDistrict.setMainWorld(WorldGlobals.PiratesWorldSceneFile)
        self.distributedDistrict.generateWithRequiredAndId(self.districtId,
            self.getGameDoId(), OTP_ZONE_ID_MANAGEMENT)

        self.setAI(self.districtId, self.ourChannel)

        self.createGlobals()
        self.createWorlds()

        self.distributedDistrict.b_setAvailable(1)
        self.serverSetupFinished()

    def serverSetupFinished(self):
        PiratesInternalRepository.serverSetupFinished(self)
        self.notify.info('District (%s) is now ready.' % self.districtName)
        messenger.send('district-ready')

    def incrementPopulation(self):
        self.populationTracker.b_setPopulation(self.populationTracker.getPopulation() + 1)

    def decrementPopulation(self):
        self.populationTracker.b_setPopulation(self.populationTracker.getPopulation() - 1)

    def createGlobals(self):
        """
        Create "global" objects, e.g. TimeManager et al.
        """

        self.populationTracker = DistributedPopulationTrackerAI(self)
        self.populationTracker.setShardId(self.districtId)
        self.populationTracker.setPopLimits(config.GetInt('shard-pop-limit-low', 100),
            config.GetInt('shard-pop-limit-high', 300))

        self.populationTracker.generateWithRequiredAndId(self.allocateChannel(),
            self.getGameDoId(), OTP_ZONE_ID_DISTRICTS_STATS)

        self.centralLogger = self.generateGlobalObject(OTP_DO_ID_CENTRAL_LOGGER, 'CentralLogger')
        self.settingsMgr = self.generateGlobalObject(OTP_DO_ID_PIRATES_SETTINGS_MANAGER, 'PiratesSettingsMgr')

        self.timeManager = TimeManagerAI(self)
        self.timeManager.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.travelAgent = self.generateGlobalObject(OTP_DO_ID_PIRATES_TRAVEL_AGENT, 'DistributedTravelAgent')

        self.teleportMgr = DistributedTeleportMgrAI(self)
        self.teleportMgr.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.timeOfDayMgr = DistributedTimeOfDayManagerAI(self)
        self.timeOfDayMgr.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.newsManager = NewsManagerAI(self)
        self.newsManager.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.questMgr = QuestManagerAI(self)

        self.friendManager = FriendManagerAI(self)
        self.friendManager.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.enemySpawner = DistributedEnemySpawnerAI(self)
        self.enemySpawner.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.battleMgr = BattleManagerAI(self)

        self.targetMgr = TargetManagerAI(self)
        self.targetMgr.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)
        self.targetMgr.startup()

        self.inventoryManager = self.generateGlobalObject(OTP_DO_ID_PIRATES_INVENTORY_MANAGER, 'DistributedInventoryManager')

        self.magicWords = PiratesMagicWordManagerAI(self)
        self.magicWords.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.tradeMgr = TradeManagerAI(self)
        self.tradeMgr.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.guildManager = self.generateGlobalObject(OTP_DO_ID_PIRATES_GUILD_MANAGER, 'PCGuildManager')

        self.districtTracker = DistrictTrackerAI(self)

        self.shipLoader = self.generateGlobalObject(OTP_DO_ID_PIRATES_SHIP_MANAGER, 'DistributedShipLoader')

        self.crewMatch = DistributedCrewMatchAI(self)
        self.crewMatch.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.bandManager = DistributedPirateBandManagerAI(self)
        self.bandManager.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.tutorialManager = PiratesTutorialManagerAI(self)
        self.tutorialManager.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.worldGridManager = WorldGridManagerAI(self)
        self.discordNotifications = DiscordNotificationsAI(self)

        self.shipManager = ShipManagerAI(self)

    def createWorlds(self):
        """
        Create "world" objects, e.g. DistributedInstanceBase, DistributedOceanGrid et al.
        """

        self.worldCreator = WorldCreatorAI(self)
        self.worldCreator.loadObjectsFromFile(WorldGlobals.PiratesWorldSceneFile)
        worldFiles = ConfigVariableList('world-file')
        for worldFile in worldFiles:
            self.worldCreator.loadObjectsFromFile('%s.py' % worldFile)
