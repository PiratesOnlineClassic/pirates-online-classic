# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestEvent
from direct.showbase.PythonUtil import POD
from direct.task.Task import Task
import random

class QuestEvent(POD):
    __module__ = __name__
    DataSet = {'location': None, 'progressResults': dict}

    def applyTo(self, taskState, taskDNA):
        raise 'derived class must override applyTo()'

    def complete(self, taskState, taskDNA):
        taskDNA.complete(self, taskState)

    def getRng(self, extraSeed=None):
        if not hasattr(self, '_randSeed'):
            self._randSeed = random.random()
        if extraSeed:
            newSeed = self._randSeed * extraSeed
            return random.Random(newSeed)
        else:
            return random.Random(self._randSeed)

    def addProgressResult(self, holder, progress):
        curProgress = self.progressResults.get(holder.getDoId(), 0)
        self.progressResults[holder.getDoId()] = curProgress + progress

    def getProgressResult(self, holder):
        return self.progressResults.get(holder.getDoId(), 0)


class EnemyDefeated(QuestEvent):
    __module__ = __name__
    DataSet = {'enemyType': None, 'level': 0, 'weaponType': None}

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleEnemyDefeat(self, taskState)


class ShipPVPEnemyDefeated(QuestEvent):
    __module__ = __name__
    DataSet = {'enemyClass': None, 'gameType': None, 'num': 0, 'killType': None, 'killWeapon': None}

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleShipPVPEnemyDefeat(self, taskState)


class ShipPVPShipDamage(QuestEvent):
    __module__ = __name__
    DataSet = {'enemyClass': None, 'gameType': None, 'damage': None, 'damageWeapon': None}

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleShipPVPShipDamage(self, taskState)


class ShipPVPPlayerDamage(QuestEvent):
    __module__ = __name__
    DataSet = {'enemyClass': None, 'gameType': None, 'damage': None, 'damageWeapon': None}

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleShipPVPPlayerDamage(self, taskState)


class ShipPVPSpawn(QuestEvent):
    __module__ = __name__

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleShipPVPSpawn(self, taskState)


class ShipPVPSink(QuestEvent):
    __module__ = __name__

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleShipPVPSink(self, taskState)


class NPCDefeated(QuestEvent):
    __module__ = __name__
    DataSet = {'npcId': None}

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleNPCDefeat(self, taskState)


class PokerHandWon(QuestEvent):
    __module__ = __name__
    DataSet = {'gold': 0}

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handlePokerHandWon(self, taskState)


class DockedAtPort(QuestEvent):
    __module__ = __name__

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleDockedAtPort(self, taskState)


class DeployedShip(QuestEvent):
    __module__ = __name__

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleDeployedShip(self, taskState)


class BlackjackHandWon(QuestEvent):
    __module__ = __name__
    DataSet = {'gold': 0}

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleBlackjackHandWon(self, taskState)


class TreasureChestOpened(QuestEvent):
    __module__ = __name__
    DataSet = {'treasureType': None, 'treasureId': None}

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleTreasureOpened(self, taskState)


class ContainerSearched(QuestEvent):
    __module__ = __name__
    DataSet = {'containerId': None, 'containerType': None}

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleContainerSearched(self, taskState)


class ShipDefeated(QuestEvent):
    __module__ = __name__
    DataSet = {'faction': None, 'hull': None, 'isFlagship': False, 'level': 0}

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleShipDefeat(self, taskState)


class NPCVisited(QuestEvent):
    __module__ = __name__
    DataSet = {'npcId': None, 'avId': None}

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleNPCVisit(self, taskState)

    def visitTarget(self):
        return self.npcId


class ObjectVisited(QuestEvent):
    __module__ = __name__
    DataSet = {'objectId': None, 'avId': None}

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleObjectVisit(self, taskState)

    def visitTarget(self):
        return self.objectId


class CutsceneWatched(QuestEvent):
    __module__ = __name__
    DataSet = {'npcId': None}

    def applyTo(self, taskState, taskDNA):
        return taskDNA.cutsceneWatched(self, taskState)


class NPCBribed(QuestEvent):
    __module__ = __name__
    DataSet = {'npcId': None, 'gold': 0}

    def applyTo(self, taskState, taskDNA):
        return taskDNA.handleNPCBribe(self, taskState)


class BossBattleCompleted(QuestEvent):
    __module__ = __name__
    DataSet = {'treasureMapId': None}

    def applyTo(self, taskState, taskDNA):
        if hasattr(taskDNA, 'handleBossBattleCompleted'):
            return taskDNA.handleBossBattleCompleted(self, taskState)
        else:
            print 'BossBattleCompleted. Warnning taskDNA %s does not have method handleBossBattleCompleted' % taskDNA
            return False
# okay decompiling .\pirates\quest\QuestEvent.pyc
