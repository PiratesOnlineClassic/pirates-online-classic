from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
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

class DistributedEnemySpawnerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedEnemySpawnerAI')
    notify.setInfo(True)

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.wantTownfolk = config.GetBool('want-townfolk', True)
        self.wantEnemies = config.GetBool('want-enemies', True)
        self.wantAnimals = config.GetBool('want-animals', True)
        self.wantNormalBosses = config.GetBool('want-normal-bosses', True)
        self.wantRandomBosses = config.GetBool('want-random-bosses', True)

        self.randomBosses = []
        self.randomBossChance = config.GetInt('random-boss-spawn-change', 5)
        self.ignoreDoubleRandom = config.GetBool('ignore-double-random-bosses', False)

        self._enemies = {}

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic):
        newObj = None

        if objType == 'Townsperson':
            if self.wantTownfolk:
                newObj = self.__createTownsperon(objType, objectData, parent, parentUid, objKey, dynamic)
        elif objType == 'Spawn Node':
            if self.wantEnemies:
                newObj = self.__createEnemy(objType, objectData, parent, parentUid, objKey, dynamic)
        else:
            self.notify.warning('Received unknown generate: %s' % objType)

        return newObj

    def __createTownsperon(self, objType, objectData, parent, parentUid, objKey, dynamic):
        townfolk = DistributedNPCTownfolkAI(self.air)

        townfolk.setScale(objectData.get('Scale'))
        townfolk.setUniqueId(objKey)
        townfolk.setPos(objectData.get('Pos', (0, 0, 0)))
        townfolk.setHpr(objectData.get('Hpr', (0, 0, 0)))
        townfolk.setSpawnPosHpr(townfolk.getPos(), townfolk.getHpr())
        townfolk.setInitZ(townfolk.getZ())

        animSet = objectData.get('AnimSet', 'default')
        noticeAnim1 = objectData.get('Notice Animation 1', '')
        noticeAnim2 = objectData.get('Notice Animation 2', '')
        greetingAnim = objectData.get('Greeting Animation', '')
        townfolk.setActorAnims(animSet, noticeAnim1, noticeAnim2, greetingAnim)

        townfolk.setLevel(int(objectData.get('Level', 0)))

        townfolk.setAggroRadius(float(objectData.get('Aggro Radius', 0)))

        name = PLocalizer.Unknown
        if objKey in NPCList.NPC_LIST:
            name = NPCList.NPC_LIST[objKey][NPCList.setName]
        townfolk.setName(name)

        if 'Start State' in objectData:
            townfolk.setStartState(objectData['Start State'])

        townfolk.setDNAId(objKey)
        if objectData.get('CustomModel', 'None') != 'None':
            townfolk.setDNAId(objectData.get('CustomModel', ''))

        category = objectData.get('Category', '')
        if not hasattr(AvatarTypes, category):
            self.notify.warning('Failed to spawn Townfolk (%s); Unknown category %s' % (objKey, category))
            return
        townfolk.setAvatarType(getattr(AvatarTypes, category, AvatarTypes.Commoner))

        shopId = objectData.get('ShopID', 'PORT_ROYAL_DEFAULTS')
        if not hasattr(PiratesGlobals, shopId):
            self.notify.warning('Failed to spawn Townfolk (%s); Unknown shopId: %s' % (objKey, shopid))
        townfolk.setShopId(getattr(PiratesGlobals, shopId, 0))

        helpId = objectData.get('HelpID', 'NONE')
        if hasattr(PiratesGlobals, helpId):
            townfolk.setHelpId(getattr(PiratesGlobals, helpId, 0))

        zoneId = PiratesGlobals.IslandLocalZone
        parent.generateChildWithRequired(townfolk, zoneId)
        townfolk.d_setInitZ(townfolk.getZ())

        townfolkName = townfolk.getName()
        self.notify.debug('Generating %s (%s) under zone %d on %s at %s with doId %d' % (townfolk.getName(), objKey, townfolk.zoneId, parent.getLocalizerName(), townfolk.getPos(), townfolk.doId))

        return townfolk


    def __createEnemy(self, objType, objectData, parent, parentUid, objKey, dynamic):

        spawnable = objectData.get('Spawnables', '')
        if spawnable not in AvatarTypes.NPC_SPAWNABLES:
            self.notify.warning('Failed to spawn %s (%s); Not a valid spawnable.' % (spawnable, objKey))

        avatarType = random.choice(AvatarTypes.NPC_SPAWNABLES[spawnable])()
        bossType = avatarType.getRandomBossType()
        
        if bossType and self.wantRandomBosses:
            if random.randint(1, 100) <= self.randomBossChance:
                if bossType not in self.randomBosses or self.ignoreDoubleRandom:
                    self.randomBosses.append(bossType)
                    avatarType = bossType
            elif config.GetBool('force-random-bosses', False):
                if bossType not in self.randomBosses or self.ignoreDoubleRandom:
                    self.randomBosses.append(bossType)
                    avatarType = bossType

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
            return

        if enemyCls is None:
            self.notify.warning('No Enemy class defined for AvatarType: %s' % avatarType)
            return

        enemy = enemyCls(self.air)

        enemy.setScale(objectData.get('Scale'))
        enemy.setUniqueId(objKey)
        enemy.setPos(objectData.get('Pos', (0, 0, 0)))
        enemy.setHpr(objectData.get('Hpr', (0, 0, 0)))
        enemy.setSpawnPosHpr(enemy.getPos(), enemy.getHpr())
        enemy.setInitZ(enemy.getZ())

        if avatarType.getBoss():
            enemy.setUniqueId('')
        else:
            enemy.setUniqueId(objKey)

        enemy.setAvatarType(avatarType)

        if avatarType.getBoss() and hasattr(enemy, 'loadBossData'):
            enemy.loadBossData(enemy.getUniqueId(), avatarType)

        enemy.setLevel(EnemyGlobals.getRandomEnemyLevel(avatarType))

        enemyHp, enemyMp = EnemyGlobals.getEnemyStats(avatarType, enemy.getLevel())

        if avatarType.getBoss() and hasattr(enemy, 'bossData'):
            enemyHp = enemyHp * enemy.bossData['HpScale']
            enemyMp = enemyMp * enemy.bossData['MpScale']

        enemy.setMaxHp(enemyHp)
        enemy.setHp(enemy.getMaxHp(), True)

        enemy.setMaxMojo(enemyMp)
        enemy.setMojo(enemyMp)

        weapons = EnemyGlobals.getEnemyWeapons(avatarType, enemy.getLevel()).keys()
        enemy.setCurrentWeapon(weapons[0], False)
        
        dnaId = objKey
        if dnaId and hasattr(enemy,'setDNAId'):
            enemy.setDNAId(dnaId)

        name = avatarType.getName()
        if dnaId and dnaId in NPCList.NPC_LIST:
            name = NPCList.NPC_LIST[dnaId][NPCList.setName]

        if avatarType.getBoss():
            name = PLocalizer.BossNames[avatarType.faction][avatarType.track][avatarType.id][0]
        enemy.setName(name)  

        if 'Start State' in objectData:
            enemy.setStartState(objectData['Start State'])

        self._enemies[objKey] = enemy

        zoneId = PiratesGlobals.IslandLocalZone
        parent.generateChildWithRequired(enemy, zoneId)
        enemy.d_setInitZ(enemy.getZ())

        locationName = parent.getLocalizerName()
        self.notify.debug('Generating %s (%s) under zone %d on %s at %s with doId %d' % (enemy.getName(), objKey, enemy.zoneId, locationName, enemy.getPos(), enemy.doId))

        if avatarType.getBoss():
            self.notify.info('Spawning boss %s (%s) on %s!' % (enemy.getName(), objKey, locationName))

        return enemy