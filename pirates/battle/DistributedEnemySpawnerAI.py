import math
import random

from panda3d.core import Point3, VBase3

from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.distributed.ClockDelta import *

from pirates.creature.DistributedAnimalAI import DistributedAnimalAI
from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
from pirates.npc.DistributedNPCSkeletonAI import DistributedNPCSkeletonAI
from pirates.npc.DistributedNPCNavySailorAI import DistributedNPCNavySailorAI
from pirates.npc.DistributedBossSkeletonAI import DistributedBossSkeletonAI
from pirates.npc.DistributedBossNavySailorAI import DistributedBossNavySailorAI
from pirates.npc import BossNPCList
from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from pirates.creature.DistributedBossCreatureAI import DistributedBossCreatureAI
from pirates.creature.DistributedSeagullAI import DistributedSeagullAI
from pirates.piratesbase import PiratesGlobals
from pirates.pirate.AvatarType import AvatarType
from pirates.pirate import AvatarTypes
from pirates.leveleditor import NPCList
from pirates.piratesbase import PLocalizer
from pirates.battle import EnemyGlobals
from pirates.ai import HolidayGlobals
from pirates.quest.QuestConstants import NPCIds

# the level editor's default values for the spawn node properties,
# see the 'Spawn Node' and 'Object Spawn Node' entries in ObjectList...
SPAWN_DELAY_DEFAULT = 20
MIN_POPULATION_DEFAULT = 1

# spawn node types which may spawn more than one npc at once
POPULATION_SPAWN_TYPES = ['Spawn Node', 'Dormant NPC Spawn Node']

# how far away from the spawn node additional npcs of it's population spawn
POPULATION_SPREAD_RADIUS = (2.0, 5.0)


class SpawnNodeBase:
    notify = DirectNotifyGlobal.directNotify.newCategory('SpawnNodeBase')

    def __init__(self, air, objType, objectData, parent, objKey, parentUid=None, populationIndex=0):
        self.air = air

        self._objType = objType
        self._objectData = objectData
        self._parent = parent
        self._objKey = objKey
        self._parentUid = parentUid
        self._populationIndex = populationIndex
        self._npc = None
        self._spawnPosHpr = None
        self._linkedWaypoints = {}

        # allow our logger to send notify messages...
        self.notify.setInfo(True)

    @property
    def objType(self):
        return self._objType

    @property
    def objectData(self):
        return self._objectData

    @property
    def parent(self):
        return self._parent

    @property
    def objKey(self):
        return self._objKey

    @property
    def npc(self):
        return self._npc

    @property
    def populationIndex(self):
        return self._populationIndex

    def getIntProperty(self, name, default=0):
        try:
            return int(float(self.objectData.get(name, default)))
        except (TypeError, ValueError):
            return default

    def getFloatProperty(self, name, default=0.0):
        try:
            return float(self.objectData.get(name, default))
        except (TypeError, ValueError):
            return default

    def getAreaPosHpr(self, uid, objectData):
        worldCreator = getattr(self.air, 'worldCreator', None)
        if not worldCreator:
            return Point3(*objectData.get('Pos', (0, 0, 0))), VBase3(*objectData.get('Hpr', (0, 0, 0)))

        return worldCreator.getObjectAreaPosHpr(uid, objectData, self._parentUid)

    def getSpawnPosHpr(self):
        if self._spawnPosHpr:
            return self._spawnPosHpr

        pos, hpr = self.getAreaPosHpr(self.objKey, self.objectData)

        # the rest of the node's population spawns spread out around the node,
        # rather than all on top of one another...
        if self._populationIndex:
            angle = random.uniform(0, math.pi * 2)
            distance = random.uniform(*POPULATION_SPREAD_RADIUS)
            pos = Point3(pos[0] + math.cos(angle) * distance, pos[1] + math.sin(angle) * distance, pos[2])

        self._spawnPosHpr = (Point3(*pos), VBase3(*hpr))
        return self._spawnPosHpr

    def getSpawnHpr(self):
        return self.getSpawnPosHpr()[1]

    def getSpawnDelay(self):
        return self.getFloatProperty('SpawnDelay', SPAWN_DELAY_DEFAULT)

    def getSpawnLevel(self, avatarType):
        level = self.getIntProperty('Level')
        if level > 0:
            return level

        return EnemyGlobals.getRandomEnemyLevel(avatarType)

    def getLinkedWaypoints(self, waypointUid=None):
        """
        Returns the uid and object data of each movement node linked to the given
        waypoint, or to this spawn node, which our npcs patrol between...
        """

        waypointUid = waypointUid or self.objKey
        if waypointUid not in self._linkedWaypoints:
            worldCreator = getattr(self.air, 'worldCreator', None)
            linkedWaypoints = []
            if worldCreator:
                linkedWaypoints = worldCreator.getLinkedMovementNodes(waypointUid, self._parentUid)

            self._linkedWaypoints[waypointUid] = linkedWaypoints

        return self._linkedWaypoints[waypointUid]

    def hasWaypoints(self):
        return len(self.getLinkedWaypoints()) > 0

    def getWaypointPos(self, waypointUid, waypointData):
        if waypointUid == self.objKey:
            return self.getSpawnPosHpr()[0]

        return self.getAreaPosHpr(waypointUid, waypointData)[0]

    def getAvatarType(self):
        raise NotImplementedError('%s does not extend getAvatarType!' % \
            self.__class__.__name__)

    def setNPCAttributes(self, npc):
        pass

    def getNPCClass(self, avatarType):
        raise NotImplementedError('%s does not extend getNPCClass!' % \
            self.__class__.__name__)

    def setup(self):
        # spawn the initial avatar...
        self.__attemptSpawn()

    def processDeath(self):
        if not self._npc:
            self.notify.debug('Attempted to perform death on a %s without a npc!' % \
                self.__class__.__name__)

            return

        taskMgr.doMethodLater(5, self.__respawn, self.getRespawnTaskName())

    def getSpawnTaskName(self):
        return 'perform-spawn-%s-%d' % (self.objKey, self._populationIndex)

    def getRespawnTaskName(self):
        return 'perform-respawn-%s-%d' % (self.objKey, self._populationIndex)

    def canRespawn(self):

        # Check for holiday requirements
        holidayName = self.objectData.get('Holiday', None)
        if holidayName:
            for holidayId, name in list(HolidayGlobals.holidayNames.items()):
                if name == holidayName:
                    return self.air.newsManager.isHolidayActive(holidayId)
            return False

        return True

    def processHolidayStart(self, holidayId):
        if self._npc:
            return

        if self.canRespawn():
            self.notify.debug('Spawning holiday npc for holiday: %s' % holidayId)
            self.__attemptSpawn()

    def processHolidayEnd(self, holidayId):
        if not self._npc:
            return

        if not self.canRespawn():
            self.notify.debug('Despawning holiday npc for holiday: %s' % holidayId)
            self.__died(self._npc)

    def __died(self, npc):
        taskMgr.remove(npc.uniqueName('update-pos-task'))
        npc.requestDelete()
        self._npc = None

    def __respawn(self, task):
        if not self._npc:
            self.notify.warning('Attempted to perform respawn on a %s without a npc!' % \
                self.__class__.__name__)

            return

        taskMgr.remove(self._npc.uniqueName('update-pos-task'))
        self._npc.requestDelete()
        self._npc = None

        respawns = self.objectData.get('Respawns', True)
        if not respawns:
            self.air.enemySpawner.removeSpawnNode(self.objType, self)
            return task.done

        taskMgr.doMethodLater(self.getSpawnDelay(), self.__attemptSpawn, self.getSpawnTaskName())

        return task.done

    def getNPCTeam(self, avatarType):
        if avatarType.isA(AvatarTypes.Navy):
            return PiratesGlobals.NAVY_TEAM
        elif avatarType.isA(AvatarTypes.TradingCo):
            return PiratesGlobals.TRADING_CO_TEAM
        elif avatarType.isA(AvatarTypes.Undead):
            if avatarType.isA(AvatarTypes.French):
                return PiratesGlobals.FRENCH_UNDEAD_TEAM
            elif avatarType.isA(AvatarTypes.Spanish):
                return PiratesGlobals.SPANISH_UNDEAD_TEAM
            else:
                return PiratesGlobals.UNDEAD_TEAM
        elif avatarType.isA(AvatarTypes.Creature):
            return PiratesGlobals.UNDEAD_TEAM
        elif avatarType.isA(AvatarTypes.Townfolk):
            return PiratesGlobals.VILLAGER_TEAM
        else:
            return PiratesGlobals.PLAYER_TEAM

    def __attemptSpawn(self, task=None):
        if not self.canRespawn():
            return

        self.__spawn()
        return Task.done

    def __updateNPC(self, task):
        if not self._npc:
            return task.done

        x, y, z = self._npc.getPos()
        h, p, r = self._npc.getHpr()
        timestamp = globalClockDelta.getRealNetworkTime(bits=16)
        self._npc.sendUpdate('setSmPosHpr', [x, y, z, h, p, r, timestamp])
        return task.again

    def __spawn(self, task=None):
        # Create the npc class
        avatarType = self.getAvatarType()
        npcCls = self.getNPCClass(avatarType)
        if npcCls is None:
            self.notify.warning('No NPC class defined for AvatarType: %s' % avatarType)
            return

        npc = npcCls(self.air)

        # Set NPC Node data
        npc.setScale(self.objectData.get('Scale'))
        npc.setUniqueId('' if avatarType.getBoss() else self.objKey)

        spawnPos, spawnHpr = self.getSpawnPosHpr()
        sx, sy, sz = spawnPos
        npc.setPos(sx, sy, sz)
        npc.setHpr(spawnHpr)

        # Set collision mode
        npc.setCollisionMode(PiratesGlobals.COLL_MODE_FLOORS_CL)

        npc.setSpawnPos(npc.getPos())
        npc.setInitZ(npc.getZ())

        npc.setAvatarType(avatarType)

        aggroRadius = self.objectData.get('Aggro Radius')
        aggroInfo = EnemyGlobals.determineAggroInfo(aggroRadius)

        npc.setAggroMode(aggroInfo[0])
        npc.setAggroRadius(aggroInfo[1])

        # Load boss data if applicable
        if avatarType.getBoss() and hasattr(npc, 'loadBossData'):
            bossId = self.objKey if self.objType != 'Spawn Node' else npc.getUniqueId()
            if not bossId in BossNPCList.BOSS_NPC_LIST:
                bossId = ''
            try:
                npc.loadBossData(bossId, avatarType)
            except Exception as e:
                npc.setAvatarType(avatarType.getNonBossType())
                self.notify.warning('Failed to load boss data for boss (%s): %s' % (str(npc.getAvatarType()), self.objKey))
                bossId = ''

            # named bosses need their unique id so the client can load the same boss data
            npc.setUniqueId(bossId)

        avType = self.objectData.get('Type', '')

        # In special cases, we may need to check the 'type' string in the worlddata,
        # if we don't, an EITC boss for example would spawn as a level 1 navy sailor
        # instead of it's normal level as an eitc type.
        if avType == 'NavySailor' and avatarType.getBoss():
            factionName = self.objectData.get('NavyFaction', 'Navy')
            if not hasattr(AvatarTypes, factionName):
                return

            faction = getattr(AvatarTypes, factionName, AvatarTypes.Navy)

            avId = self.objectData.get('AvId', 1)
            avTrack = self.objectData.get('AvTrack', 0)
            avatarType = AvatarType(faction=faction.faction, track=avTrack, id=avId)
            avatarType = avatarType.getBossType()

            if factionName == 'TradingCo':
                npc.setLevel(npc.bossData['Level'] or EnemyGlobals.getRandomEnemyLevel(avatarType))

            npc.setAvatarType(avatarType)

        npc.setTeam(self.getNPCTeam(avatarType))

        # Set NPC health
        if hasattr(npc, 'bossData'):
            npc.setLevel(npc.bossData.get('Level', 0) or self.getSpawnLevel(avatarType))
        else:
            npc.setLevel(self.getSpawnLevel(avatarType))

        npcHp, npcMp = EnemyGlobals.getEnemyStats(avatarType, npc.getLevel())
        if avatarType.getBoss() and hasattr(npc, 'bossData'):
            npcHp = npcHp * npc.bossData['HpScale']
            npcMp = npcMp * npc.bossData['MpScale']

        npc.setMaxHp(npcHp)
        npc.setHp(npc.getMaxHp(), True)

        npc.setMaxMojo(npcMp)
        npc.setMojo(npc.getMaxMojo())

        # Set custom spawner based attributes
        self.setNPCAttributes(npc)

        # Set NPC DNA if applicable
        dnaId = self.objectData.get('DNA', self.objKey)
        if hasattr(npc, 'setDNAId'):
            if self.objectData.get('CustomModel', 'None') != 'None':
                npc.setDNAId(self.objectData.get('CustomModel', ''))
            elif dnaId:
                npc.setDNAId(dnaId)

        # Name the NPC
        name = avatarType.getName()
        if dnaId and dnaId in NPCList.NPC_LIST:
            name = NPCList.NPC_LIST[dnaId][NPCList.setName]
        if dnaId == NPCIds.ELIZABETH:
            name = 'Elizabeth Swann'
        elif dnaId == NPCIds.BARBOSSA:
            name = 'Captain Barbossa'

        if hasattr(npc, 'bossData'):
            name = npc.bossData.get('Name', PLocalizer.Unknown)
        elif avatarType.getBoss():
            try:
                name = PLocalizer.BossNames[avatarType.faction][avatarType.track][avatarType.id][avatarType.boss]
            except (IndexError, KeyError, TypeError):
                pass

        npc.setName(name)

        # Set starting state info
        npc.setAnimSet(self.objectData.get('AnimSet', 'default'))
        startState = self.objectData.get('Start State', 'Idle')
        if isinstance(npc, DistributedNPCTownfolkAI):
            startState = 'Idle'

        npc.setStartState(startState)
        npc.setAmbush(startState == 'Ambush')

        # Generate npc
        zoneId = self.parent.getZoneFromXYZ(npc.getPos())
        self.parent.generateChildWithRequired(npc, zoneId)
        self.parent.builder.addObject(npc)
        self.parent.addObjectToGrid(npc, zoneId)

        # position the npc relative to it's parent object
        npc.setPos(self.parent, (sx, sy, sz))
        npc.setZ(sz)

        # TODO FIXME!
        #npc.startPosHprBroadcast()

        # Save a copy of the npc and tell it about myself. This will come in handy
        self._npc = npc
        npc.setSpawnNode(self)

        npc.d_setInitZ(npc.getZ())

        # setAmbush is not a required field, the client only checks for it's
        # existance so only send it to the npcs that are actually ambushing...
        if npc.getAmbush():
            npc.d_setAmbush(True)

        npc.d_setSpawnIn()
        npc.b_setGameState(npc.getStartState())

        taskMgr.doMethodLater(0.2, self.__updateNPC, npc.uniqueName('update-pos-task'))

        # Print out useful debugging information
        locationName = self.parent.getLocalizerName()
        self.notify.debug('Generating %s (%s) under zone %d on %s at %s with doId %d' % (npc.getName(), self.objKey,
            npc.zoneId, locationName, npc.getPos(), npc.doId))

        if avatarType.getBoss():
            if not locationName or locationName == '':
                locationName = self.parent.getUniqueId()
            self.notify.info('Spawning boss %s (%s) on %s!' % (npc.getName(), self.objKey, locationName))

        return Task.done

class TownfolkSpawnNode(SpawnNodeBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('TownfolkSpawnNode')

    def getAvatarType(self):
        category = self.objectData.get('Category', '')
        if not hasattr(AvatarTypes, category):
            self.notify.warning('Failed to spawn Townfolk (%s); Unknown category %s' % (self.objKey, category))
            return
        return getattr(AvatarTypes, category, AvatarTypes.Commoner)

    def setNPCAttributes(self, npc):
        shopId = self.objectData.get('ShopID', 'PORT_ROYAL_DEFAULTS')
        if not hasattr(PiratesGlobals, shopId):
            self.notify.warning('Failed to spawn Townfolk (%s); Unknown shopId: %s' % (self.objKey, shopId))
        npc.setShopId(getattr(PiratesGlobals, shopId, 0))

        helpId = self.objectData.get('HelpID', 'NONE')
        if hasattr(PiratesGlobals, helpId):
            npc.setHelpId(getattr(PiratesGlobals, helpId, 0))

    def getNPCTeam(self, avatarType):
        # townsfolk are either on the villager or the player team,
        # both of which are neutral towards the player...
        team = self.objectData.get('Team', PiratesGlobals.VILLAGER_TEAM_STR)
        if team not in (PiratesGlobals.VILLAGER_TEAM_STR, PiratesGlobals.PLAYER_TEAM_STR):
            return SpawnNodeBase.getNPCTeam(self, avatarType)

        return PiratesGlobals.teamStr2TeamId(team, PiratesGlobals.VILLAGER_TEAM)

    def getNPCClass(self, avatarType):
        return DistributedNPCTownfolkAI

class EnemySpawnNode(SpawnNodeBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('EnemySpawnNode')

    def __init__(self, *args, **kwargs):
        self.wantRandomBosses = config.GetBool('want-random-bosses', True)
        self.randomBossChance = config.GetInt('random-boss-spawn-change', 5)

        SpawnNodeBase.__init__(self, *args, **kwargs)

    def getAvatarType(self):
        spawnable = self.objectData.get('Spawnables', '')
        species = self.objectData.get('Species', '')
        if spawnable not in AvatarTypes.NPC_SPAWNABLES:
            if species == 'Monkey':
                return AvatarTypes.Monkey

            self.notify.warning('Failed to spawn %s (%s); Not a valid spawnable.' % (spawnable, self.objKey))
            return AvatarTypes.FrenchUndeadA

        avatarType = random.choice(AvatarTypes.NPC_SPAWNABLES[spawnable])()
        bossType = avatarType.getRandomBossType()

        # Attempt to pick a RNG boss type
        if bossType and self.wantRandomBosses:
            if random.randint(1, 100) <= self.randomBossChance:
                if bossType not in self.air.enemySpawner.randomBosses:
                    self.air.enemySpawner.randomBosses.append(bossType)
                    avatarType = bossType
            elif config.GetBool('force-random-bosses', False):
                if bossType not in self.air.enemySpawner.randomBosses:
                    self.air.enemySpawner.randomBosses.append(bossType)
                    avatarType = bossType

        return avatarType

    def getNPCTeam(self, avatarType):
        team = SpawnNodeBase.getNPCTeam(self, avatarType)

        # the level editor allows a spawn node to override the team of the
        # enemies it spawns, 'default' leaves it up to the avatar type...
        teamId = self.objectData.get('Team', 'default')
        if teamId == 'default':
            return team

        try:
            teamId = int(teamId)
        except (TypeError, ValueError):
            return team

        # never place an enemy on the player's team, and the french and spanish
        # undead are both still part of the undead team...
        if teamId not in (PiratesGlobals.UNDEAD_TEAM, PiratesGlobals.NAVY_TEAM, PiratesGlobals.TRADING_CO_TEAM):
            return team

        if teamId == PiratesGlobals.UNDEAD_TEAM and team in (PiratesGlobals.FRENCH_UNDEAD_TEAM, PiratesGlobals.SPANISH_UNDEAD_TEAM):
            return team

        return teamId

    def setNPCAttributes(self, npc):
        weapons = list(EnemyGlobals.getEnemyWeapons(npc.getAvatarType(), npc.getLevel()).keys())
        if hasattr(npc, 'getBossWeapons'):
            weapons = npc.getBossWeapons() or weapons

        animSet = self.objectData.get('AnimSet', '')
        drawnAnimSets = ['attention', 'bayonet_drill']
        defaultDrawn = True if animSet in drawnAnimSets or 'attack_' in animSet else False
        npc.setCurrentWeapon(random.choice(weapons), config.GetBool('want-enemy-weapons', defaultDrawn))

    def getNPCClass(self, avatarType):
        enemyCls = None

        if avatarType.isA(AvatarTypes.Undead):
            if avatarType.getBoss():
                enemyCls = DistributedBossSkeletonAI
            else:
                enemyCls = DistributedNPCSkeletonAI
        elif avatarType.isA(AvatarTypes.TradingCo) or avatarType.isA(AvatarTypes.Navy):
            if avatarType.getBoss():
                enemyCls = DistributedBossNavySailorAI
            else:
                enemyCls = DistributedNPCNavySailorAI
        elif avatarType.isA(AvatarTypes.LandCreature) or avatarType.isA(AvatarTypes.AirCreature):
            if avatarType.getBoss():
                enemyCls = DistributedBossCreatureAI
            else:
                enemyCls = DistributedCreatureAI
        else:
            self.notify.warning('Received unknown AvatarType: %s' % avatarType)

        return enemyCls

class AnimalSpawnNode(SpawnNodeBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('AnimalSpawnNode')

    def getAvatarType(self):
        species = self.objectData.get('Species', None)
        if not species:
            self.notify.warning('Failed to generate Animal %s; Species was not defined' % self._objKey)
            return

        if not hasattr(AvatarTypes, species):
            self.notify.warning('Failed to generate Animal %s; %s is not a valid species' % (self._objKey, species))
            return
        return getattr(AvatarTypes, species, AvatarTypes.Chicken)

    def getNPCTeam(self, avatarType):
        # animals are ambient townsfolk creatures, not undead enemies...
        return PiratesGlobals.VILLAGER_TEAM

    def getNPCClass(self, avatarType):
        animalClass = DistributedAnimalAI
        #if avatarType == AvatarTypes.Seagull:
        #    animalClass = DistributedSeagullAI
        return animalClass

class BossEnemySpawnNode(EnemySpawnNode):

    def getAvatarType(self):
        avId = self.objectData.get('AvId', 1)
        avTrack = self.objectData.get('AvTrack', 0)
        species = self.objectData.get('Species', '')

        faction = AvatarTypes.Undead.faction
        if self.objType == 'Creature':
            faction = AvatarTypes.Creature.faction
        elif self.objType == 'NavySailor':
            faction = AvatarTypes.Navy.faction

        if species:
            self.spawnable = self.objectData['Species']
            if self.spawnable not in AvatarTypes.NPC_SPAWNABLES:
                return

            avatarType = AvatarTypes.NPC_SPAWNABLES[self.spawnable][0]()

            # creatures placed in the world are only bosses when flagged as one
            if self.objType == 'Creature' and not self.objectData.get('Boss', False):
                return avatarType

            return avatarType.getBossType()

        avatarType = AvatarType(faction=faction, track=avTrack, id=avId)
        return avatarType.getBossType()

class DistributedEnemySpawnerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedEnemySpawnerAI')
    notify.setInfo(True)

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.randomBosses = []
        self.spawnNodes = {}

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        self.accept('HolidayStarted', self.__processHolidayStart)
        self.accept('HolidayEnded', self.__processHolidayEnd)

    def delete(self):
        DistributedObjectAI.delete(self)

        self.ignore('HolidayStarted')
        self.ignore('HolidayEnded')

    def __processHolidayStart(self, holidayId):
        for spawnNodeKey in self.spawnNodes:
            spawnNodes = self.spawnNodes[spawnNodeKey]
            for spawnNode in spawnNodes:
                spawnNode.processHolidayStart(holidayId)

    def __processHolidayEnd(self, holidayId):
        for spawnNodeKey in self.spawnNodes:
            spawnNodes = self.spawnNodes[spawnNodeKey]
            for spawnNode in spawnNodes:
                spawnNode.processHolidayEnd(holidayId)

    def getSpawnNodesFromType(self, type):
        if type not in self.spawnNodes:
            return []

        return self.spawnNodes[type]

    def getSpawnNodeFromTypeAndKey(self, type, key):
        spawns = self.getSpawnNodesFromType(type)
        found = None
        for spawn in spawns:
            if spawn.objKey == key:
                found = spawn
                break

        return found

    def removeSpawnNode(self, type, spawnNode):
        if not type in self.spawnNodes:
            return

        if spawnNode in self.spawnNodes[type]:
            self.spawnNodes[type].remove(spawnNode)

    def __registerSpawnNode(self, type, spawnNode):
        if not self.getSpawnNodesFromType(type):
            self.spawnNodes[type] = []

        self.spawnNodes[type].append(spawnNode)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic):
        newObj = None

        spawnClasses = {
            'Townsperson': TownfolkSpawnNode,
            'Spawn Node': EnemySpawnNode,
            'Dormant NPC Spawn Node': EnemySpawnNode,
            'Animal': AnimalSpawnNode,
            'Skeleton': BossEnemySpawnNode,
            'NavySailor': BossEnemySpawnNode,
            'Creature': BossEnemySpawnNode
        }

        if objType not in spawnClasses:
            self.notify.warning('Received unknown generate: %s' % objType)
            return

        # check to see if we have any explicit objects that need
        # to be generated in some other way...
        if objType == 'Animal':
            if objectData['Species'] == 'Monkey':
                objType = 'Spawn Node'

        # Verify private status of object
        #isPrivate = objectData.get('Private Status', 'All') != 'All'
        #if isPrivate:
        #    return

        # spawn nodes may spawn more than one npc at once, each of them is
        # handled by it's own spawn node so they can die and respawn on their own...
        population = 1
        if objType in POPULATION_SPAWN_TYPES:
            try:
                population = max(int(objectData.get('Min Population', MIN_POPULATION_DEFAULT)), 1)
            except (TypeError, ValueError):
                population = MIN_POPULATION_DEFAULT

        spawnClass = spawnClasses[objType]
        for populationIndex in range(population):
            spawnNode = spawnClass(self.air, objType, objectData, parent, objKey, parentUid, populationIndex)
            spawnNode.setup()
            self.__registerSpawnNode(objType, spawnNode)

        return newObj
