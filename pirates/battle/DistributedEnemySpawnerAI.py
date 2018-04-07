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

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.wantTownfolk = config.GetBool('want-townfolk', True)
        self.wantEnemies = config.GetBool('want-enemies', True)

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
        return None

    def __createEnemy(self, objType, objectData, parent, parentUid, objKey, dynamic):
        
        spawnable = objectData.get('Spawnables', '')
        if spawnable not in AvatarTypes.NPC_SPAWNABLES:
            self.notify.warning('Failed to spawn %s (%s); Not a valid spawnable.' % (spawnable, objKey))

        avatarType = random.choice(AvatarTypes.NPC_SPAWNABLES[spawnable])()
        bossType = avatarType.getRandomBossType()

        enemyCls = None
        if avatarType.isA(AvatarTypes.Undead):
            if avatarType.getBoss():
                enemyCls = DistributedBossSkeletonAI
                return
            else:
                enemyCls = DistributedNPCSkeletonAI
        elif avatarType.isA(AvatarTypes.TradingCo) or avatarType.isA(AvatarTypes.Navy):
            if avatarType.getBoss():
                enemyCls = DistributedBossNavySailorAI
                return
            else:
                enemyCls = DistributedNPCNavySailorAI
        else:
            self.notify.warning('Received unknown AvatarType: %s' % avatarType)
            return

        if enemyCls is None:
            self.notify.warning('No Enemy class defined for AvatarType: %s' % avatarType)
            return

        enemy = enemyCls(self.air)
        enemy.setPos(objectData.get('Pos', (0, 0, 0)))
        enemy.setHpr(objectData.get('Hpr', (0, 0, 0)))
        enemy.setSpawnPosHpr(enemy.getPos(), enemy.getHpr())
        enemy.setScale(objectData.get('Scale'))
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

        print('Generating %s (%s) under zone %d at %s with doId %d' % (enemy.getName(), objKey, enemy.zoneId, enemy.getPos(), enemy.doId))
        return enemy