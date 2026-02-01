from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import globalClockDelta
from direct.fsm.FSM import FSM

from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.pirate.BattleNPCGameFSMAI import BattleNPCGameFSMAI
from pirates.piratesbase import PLocalizer
from pirates.pirate import AvatarTypes
from pirates.battle import EnemyGlobals


class DistributedBattleNPCAI(DistributedBattleAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleNPCAI')

    def __init__(self, air):
        DistributedBattleAvatarAI.__init__(self, air)

        self.gameFSM = BattleNPCGameFSMAI(self.air, self)

        self.name = ''
        self.spawnPos = [0, 0, 0]
        self.animSet = ''
        self.collisionMode = 0
        self.initZ = 0
        self.ambush = False

        self.spawnNode = None

    def generate(self):
        DistributedBattleAvatarAI.generate(self)
        self.air.targetMgr.addTarget(self)

    def getMonsterDmg(self):
        return EnemyGlobals.getMonsterDmg(self.level)

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def setSpawnPos(self, xxx_todo_changeme):
        (x, y, z) = xxx_todo_changeme
        self.spawnPos = [x, y, z]

    def d_setSpawnPos(self, xxx_todo_changeme1):
        (x, y, z) = xxx_todo_changeme1
        self.sendUpdate('setSpawnPos', [x, y, z])

    def b_setSpawnPos(self, xxx_todo_changeme2):
        (x, y, z) = xxx_todo_changeme2
        self.setSpawnPos(x, y, z)
        self.d_setSpawnPos(x, y, z)

    def getSpawnPos(self):
        return self.spawnPos

    def d_setSpawnIn(self):
        self.sendUpdate('setSpawnIn', [globalClockDelta.getRealNetworkTime(bits=32)])

    def setAmbush(self, ambush):
        self.ambush = ambush

    def d_setAmbush(self, ambush):
        self.ambush = ambush

    def b_setAmbush(self, ambush):
        self.setAmbush(ambush)
        self.d_setAmbush(ambush)

    def d_setChat(self, chatString, chatFlags=0):
        self.sendUpdate('setChat', [chatString, chatFlags])

    def setAnimSet(self, animSet):
        self.animSet = animSet

    def d_setAnimSet(self, animSet):
        self.sendUpdate('setAnimSet', [animSet])

    def b_setAnimSet(self, animSet):
        self.setAnimSet(animSet)
        self.d_setAnimSet(animSet)

    def getAnimSet(self):
        return self.animSet

    def setCollisionMode(self, collisionMode):
        self.collisionMode = collisionMode

    def d_setCollisionMode(self, collisionMode):
        self.sendUpdate('setCollisionMode', [collisionMode])

    def b_setCollisionMode(self, collisionMode):
        self.setCollisionMode(collisionMode)
        self.d_setCollisionMode(collisionMode)

    def getCollisionMode(self):
        return self.collisionMode

    def setInitZ(self, initZ):
        self.initZ = initZ

    def d_setInitZ(self, initZ):
        self.sendUpdate('setInitZ', [initZ])

    def b_setInitZ(self, initZ):
        self.setInitZ(initZ)
        self.d_setInitZ(initZ)

    def getInitZ(self):
        return self.initZ

    def setSpawnNode(self, spawnNode):
        self.spawnNode = spawnNode

    def getSpawnNode(self):
        return self.spawnNode

    def lookAtTarget(self, task):
        if self.currentTarget:
            self.headsUp(self.currentTarget)
            return task.cont

        return task.done

    def getUpdateLookAtTaskName(self):
        return self.taskName('lookAtTarget')

    def startLookAt(self):
        taskMgr.add(self.lookAtTarget, self.getUpdateLookAtTaskName())

    def stopLookAt(self):
        taskMgr.remove(self.getUpdateLookAtTaskName())

    def getAggroPhrase(self):
        if self.avatarType == AvatarTypes.Navy:
            return PLocalizer.getNavyAggroPhrase()
        elif self.avatarType == AvatarTypes.Undead:
            return PLocalizer.getUndeadAggroPhrase()
        elif self.avatarType == AvatarTypes.TradingCo:
            return PLocalizer.getEITCAggroPhrase()
        elif self.avatarType == AvatarTypes.EarthUndead:
            return PLocalizer.getDavyJonesGuysAggroPhrase()

        return ''

    def getBreakCombatPhrase(self):
        if self.avatarType == AvatarTypes.Navy:
            return PLocalizer.getNavyBreakCombatPhrase()
        elif self.avatarType == AvatarTypes.Undead:
            return PLocalizer.getUndeadBreakCombatPhrase()
        elif self.avatarType == AvatarTypes.TradingCo:
            return PLocalizer.getEITCBreakCombatPhrase()
        elif self.avatarType == AvatarTypes.EarthUndead:
            return PLocalizer.getDavyJonesGuysBreakCombatPhrase()

        return ''

    def getTauntPhrase(self):
        if self.avatarType == AvatarTypes.Navy:
            return PLocalizer.getNavyTauntPhrase()
        elif self.avatarType == AvatarTypes.Undead:
            return PLocalizer.getUndeadTauntPhrase()
        elif self.avatarType == AvatarTypes.TradingCo:
            return PLocalizer.getEITCTauntPhrase()
        elif self.avatarType == AvatarTypes.EarthUndead:
            return PLocalizer.getDavyJonesGuysTauntPhrase()

        return ''

    def getTeamTalkPhrase(self):
        if self.avatarType == AvatarTypes.Navy:
            return PLocalizer.getNavyTeamTalkPhrase()
        elif self.avatarType == AvatarTypes.Undead:
            return PLocalizer.getUndeadTeamTalkPhrase()
        elif self.avatarType == AvatarTypes.TradingCo:
            return PLocalizer.getEITCTeamTalkPhrase()
        elif self.avatarType == AvatarTypes.EarthUndead:
            return PLocalizer.getDavyJonesGuysTeamTalkPhrase()

        return ''

    def requestClientAggro(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            return

        # verify we are not in a death state prior to processing
        # any aggro logic
        if self.gameFSM.state == 'Death':
            return

        # if we are in ambush mode and an avatar just entered our aggro
        # sphere, ambush them and try to kill them.
        if self.gameFSM.state == 'Ambush':
            self.handleClientAggro(avatar)

        # check if we should auto aggro to the avatar that entered
        # our aggro sphere
        experienceGrade = self.air.battleMgr.getModifiedExperienceGrade(avatar, self)
        if experienceGrade >= EnemyGlobals.GREEN:
            self.handleClientAggro(avatar)

    def handleClientAggro(self, avatar):
        self.b_setCurrentTarget(avatar.doId)
        self.b_setGameState('Battle')
        self.d_setChat(self.getAggroPhrase())

    def delete(self):
        self.air.targetMgr.removeTarget(self)
        DistributedBattleAvatarAI.delete(self)
