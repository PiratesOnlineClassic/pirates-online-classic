from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
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
import random

class SpawnNodeBase:
    notify = DirectNotifyGlobal.directNotify.newCategory('SpawnNodeBase')

    def __init__(self, spawner, objType, objectData, parent, objKey):

        self._spawner = spawner
        self._objType = objType
        self._objectData = objectData
        self._parent = parent
        self._objKey = objKey
        self._npc = None

        # Spawn initial npc
        self.__spawn()

    @property
    def spawner(self):
        return self._spawner

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

    def getAvatarType(self):
        raise NotImplementedError('%s does not extend getAvatarType!' % self.__class__.__name__)

    def setNPCAttributes(self, npc):
        pass

    def getNPCClass(self, avatarType):
        raise NotImplementedError('%s does not extend getNPCClass!' % self.__class__.__name__)

    def processDeath(self):
        taskMgr.doMethodLater(5, self.__respawn, 'perform-respawn-%s' % self.objKey)

    def __respawn(self, task):
        print(self._npc)
        if not self._npc:
            self.notify.warning('Attempted to perform respawn on a %s without a npc!' % self.__class__.__name__)
            return

        self._npc.requestDelete()
        self._npc = None

        respawns = self.objectData.get('Respawns', True)
        if not respawns:
            #TODO: is this the proper way of handling this?
            removeSpawnNode(self.objType, self)
            return

        #TODO: Is this a constant?
        spawnTimer = 20
        taskMgr.doMethodLater(spawnTimer, self.__spawn, 'perform-spawn-%s' % self.objKey)

        return task.done

    def __spawn(self, task=None):

        # Create the npc class
        avatarType = self.getAvatarType()
        npcCls = self.getNPCClass(avatarType)
        if npcCls is None:
            self.notify.warning('No NPC class defined for AvatarType: %s' % avatarType)
            return
        npc = npcCls(self.spawner.air)

        # Set NPC Node data
        npc.setScale(self.objectData.get('Scale'))
        npc.setUniqueId('' if avatarType.getBoss() else self.objKey)
        npc.setPos(self.objectData.get('Pos', (0, 0, 0)))
        npc.setHpr(self.objectData.get('Hpr', (0, 0, 0)))
        npc.setSpawnPosHpr(npc.getPos(), npc.getHpr())
        npc.setInitZ(npc.getZ())

        npc.setAvatarType(avatarType)
        npc.setAggroRadius(float(self.objectData.get('Aggro Radius', 0)))

        # Load boss data if applicable
        if avatarType.getBoss() and hasattr(npc, 'loadBossData'):
            npc.loadBossData(npc.getUniqueId(), avatarType)

        # Set NPC health
        npc.setLevel(EnemyGlobals.getRandomEnemyLevel(avatarType))
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
        dnaId = self.objKey
        if dnaId and hasattr(npc, 'setDNAId'):
            npc.setDNAId(dnaId)
        elif self.objectData.get('CustomModel', 'None') != 'None':
            npc.setDNAId(self.objectData.get('CustomModel', ''))

        # Name the NPC
        name = avatarType.getName()
        if dnaId and dnaId in NPCList.NPC_LIST:
            name = NPCList.NPC_LIST[dnaId][NPCList.setName]

        if avatarType.getBoss():
            name = random.choice(PLocalizer.BossNames[avatarType.faction][avatarType.track][avatarType.id])
        npc.setName(name)

        # Set starting state info
        npc.setAnimSet(self.objectData.get('AnimSet', 'default'))
        npc.setStartState(self.objectData.get('Start State', 'Idle'))

        # Generate npc
        self.parent.generateChildWithRequired(npc, PiratesGlobals.IslandLocalZone)
        npc.d_setInitZ(npc.getZ())

        # Save a copy of the npc and tell it about myself. This will come in handy
        self._npc = npc
        npc.setSpawner(self)

        # Print out useful debugging information
        locationName = self.parent.getLocalizerName()
        self.notify.debug('Generating %s (%s) under zone %d on %s at %s with doId %d' % (npc.getName(), self.objKey,
            npc.zoneId, locationName, npc.getPos(), npc.doId))

        if avatarType.getBoss():
            self.notify.debug('Spawning boss %s (%s) on %s!' % (npc.getName(), self.objKey, locationName))

        return Task.done

class TownfolkSpawnNode(SpawnNodeBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('TownfolkSpawnNode')

    def getAvatarType(self):
        category = self.objectData.get('Category', '')
        if not hasattr(AvatarTypes, category):
            self.notify.warning('Failed to spawn Townfolk (%s); Unknown category %s' % (objKey, category))
            return
        return getattr(AvatarTypes, category, AvatarTypes.Commoner)

    def setNPCAttributes(self, npc):
        shopId = self.objectData.get('ShopID', 'PORT_ROYAL_DEFAULTS')
        if not hasattr(PiratesGlobals, shopId):
            self.notify.warning('Failed to spawn Townfolk (%s); Unknown shopId: %s' % (objKey, shopid))
        npc.setShopId(getattr(PiratesGlobals, shopId, 0))

        helpId = self.objectData.get('HelpID', 'NONE')
        if hasattr(PiratesGlobals, helpId):
            npc.setHelpId(getattr(PiratesGlobals, helpId, 0))

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
        if spawnable not in AvatarTypes.NPC_SPAWNABLES:
            self.notify.warning('Failed to spawn %s (%s); Not a valid spawnable.' % (spawnable, objKey))
            return AvatarTypes.FrenchUndeadA

        avatarType = random.choice(AvatarTypes.NPC_SPAWNABLES[spawnable])()
        bossType = avatarType.getRandomBossType()

        # Attempt to pick a RNG boss type
        if bossType and self.wantRandomBosses:
            if random.randint(1, 100) <= self.randomBossChance:
                if bossType not in self.spawner.randomBosses:
                    self.spawner.randomBosses.append(bossType)
                    avatarType = bossType
            elif config.GetBool('force-random-bosses', False):
                if bossType not in self.spawner.randomBosses:
                    self.spawner.randomBosses.append(bossType)
                    avatarType = bossType

        return avatarType

    def setNPCAttributes(self, npc):
        weapons = EnemyGlobals.getEnemyWeapons(npc.getAvatarType(), npc.getLevel()).keys()
        if config.GetBool('want-enemy-weapons', False):
            npc.setCurrentWeapon(weapons[0], True)
        else:
            npc.setCurrentWeapon(weapons[0], False)

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
            self.notify.warning('Failed to generate Animal %s; Species was not defined' % objKey)
            return

        if not hasattr(AvatarTypes, species):
            self.notify.warning('Failed to generate Animal %s; %s is not a valid species' % (objKey, species))
            return
        return getattr(AvatarTypes, species, AvatarTypes.Chicken)

    def getNPCClass(self, avatarType):
        animalClass = DistributedAnimalAI
        if avatarType == AvatarTypes.Seagull:
            animalClass = DistributedSeagullAI
        return animalClass

class DistributedEnemySpawnerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedEnemySpawnerAI')
    notify.setInfo(True)

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.wantTownfolk = config.GetBool('want-townfolk', True)
        self.wantEnemies = config.GetBool('want-enemies', True)
        self.wantAnimals = config.GetBool('want-animals', True)
        self.wantNormalBosses = config.GetBool('want-normal-bosses', True)

        self.randomBosses = []
        self.spawnNodes = {}

    def getSpawnNodesFromType(self, type):
        if type not in self.spawnNodes:
            return []
        return self.spawnNodes[type]

    def getSpawnNodeFromTypeAndKey(self, type, key):
        spawns = self.getSpawnNodesFromType(type)
        found = None
        for spawn in spawns:
            if spawn.objkey == key:
                found = spawn
                break
        return found

    def removeSpawnNode(self, type, spawnNode):
        if not type in self.spawnNodes:
            return
        self.spawnNodes[type].remove(spawnNode)

    def __registerSpawnNode(self, type, spawnNode):
        if not self.getSpawnNodesFromType(type):
            self.spawnNodes[type] = []
        self.spawnNodes[type].append(spawnNode)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic):
        newObj = None

        #TODO: Is there a better more clean way of doing this?
        spawnClasses = {
            'Townsperson': TownfolkSpawnNode,
            'Spawn Node': EnemySpawnNode,
            'Animal': AnimalSpawnNode
        }

        if objType not in spawnClasses:
            self.notify.warning('Received unknown generate: %s' % objType)
            return
        
        spawnClass = spawnClasses[objType]
        spawnNode = spawnClass(self, objType, objectData, parent, objKey)
        self.__registerSpawnNode(objType, spawnNode)

        return newObj

    def __createBossSkeleton(self, objType, objectData, parent, parentUid, objKey, dynamic):
        skeleton = DistributedBossSkeletonAI(self.air)

        skeleton.setScale(objectData.get('Scale'))
        skeleton.setUniqueId(objKey)
        skeleton.setPos(objectData.get('Pos', (0, 0, 0)))
        skeleton.setHpr(objectData.get('Hpr', (0, 0, 0)))
        skeleton.setSpawnPosHpr(skeleton.getPos(), skeleton.getHpr())
        skeleton.setInitZ(skeleton.getZ())

        avId = objectData.get('AvId', 1)
        avTrack = objectData.get('AvTrack', 0)
        avatarType = AvatarType(faction=AvatarTypes.Undead.faction, track=avTrack, id=avId)
        avatarType = avatarType.getBossType()
        skeleton.setAvatarType(avatarType)
        try:
            skeleton.loadBossData(objKey, avatarType)
        except:
            self.notify.warning('Failed to load %s (%s); An error occured while loading boss data' % (objType, objKey))
            return None

        skeleton.setName(skeleton.bossData['Name'])
        skeleton.setLevel(skeleton.bossData['Level'] or EnemyGlobals.getRandomEnemyLevel(avatarType))

        enemyHp, enemyMp = EnemyGlobals.getEnemyStats(avatarType, skeleton.getLevel())
        enemyHp = enemyHp * skeleton.bossData.get('HpScale', 1)
        enemyMp = enemyMp * skeleton.bossData.get('MpScale', 1)

        skeleton.setMaxHp(enemyHp)
        skeleton.setHp(skeleton.getMaxHp(), True)

        skeleton.setMaxMojo(enemyMp)
        skeleton.setMojo(enemyMp)

        weapons = EnemyGlobals.getEnemyWeapons(avatarType, skeleton.getLevel()).keys()
        skeleton.setCurrentWeapon(weapons[0], False)

        skeleton.setAnimSet(objectData.get('AnimSet', 'default'))
        skeleton.setStartState(objectData.get('Start State', 'Idle'))

        zoneId = PiratesGlobals.IslandLocalZone
        parent.generateChildWithRequired(skeleton, zoneId)

        locationName = parent.getLocalizerName()
        self.notify.debug('Generating %s (%s) under zone %d in %s at %s with doId %d' % (skeleton.getName(), objKey,
            skeleton.zoneId, locationName, skeleton.getPos(), skeleton.doId))

        return skeleton
