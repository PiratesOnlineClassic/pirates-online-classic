# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestTaskDNA
import random
import string

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import POD, invertDict, makeTuple
from pirates.battle import EnemyGlobals
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.quest import QuestEvent, QuestReward, QuestTaskState
from pirates.quest.QuestConstants import (LocationIds, NPCIds, PropIds,
                                          ShipIds, TreasureIds,
                                          getLocationList, getPropList,
                                          getShipList, getTreasureList)
from pirates.quest.QuestPath import QuestGoal
from pirates.ship import ShipGlobals


class QuestTaskDNA(POD):
    __module__ = __name__
    notify = directNotify.newCategory('QuestTaskDNA')
    DataSet = {'location': LocationIds.ANY_LOCATION, 'autoTriggerInfo': tuple(), 'goalLocation': None}

    def getNPCName(self, npcId):
        return PLocalizer.NPCNames.get(npcId, PLocalizer.DefaultTownfolkName)

    def getInitialTaskState(self, holder):
        return QuestTaskState.QuestTaskState(taskType=Class2DBId[self.__class__])

    def computeRewards(self, initialTaskState, holder):
        return []

    def locationMatches(self, questEvent):
        if self.getLocation() == LocationIds.ANY_LOCATION:
            return True
        if questEvent.location is None:
            return False
        locationList = getLocationList(self.getLocation())
        if locationList:
            for location in locationList:
                if location == questEvent.getLocation():
                    return True

        else:
            self.notify.warning('No location list for: %s' % self.getLocation())
            return False
        return False

    def getGoalUid(self):
        if self.getGoalLocation():
            return self.getGoalLocation()
        locationList = getLocationList(self.getLocation())
        if locationList:
            return locationList[0]
        else:
            return
        return

    def getGoalNum(self):
        return 1

    def handleEnemyDefeat(self, questEvent, taskState):
        pass

    def handleNPCDefeat(self, questEvent, taskState):
        pass

    def handlePokerHandWon(self, questEvent, taskState):
        pass

    def handleBlackjackHandWon(self, questEvent, taskState):
        pass

    def handleTreasureOpened(self, questEvent, taskState):
        pass

    def handleContainerSearched(self, questEvent, taskState):
        pass

    def handleDockedAtPort(self, questEvent, taskState):
        pass

    def handleDeployedShip(self, questEvent, taskState):
        pass

    def handleShipDefeat(self, questEvent, taskState):
        pass

    def handleNPCVisit(self, questEvent, taskState):
        pass

    def handleNPCBribe(self, questEvent, taskState):
        pass

    def handleObjectVisit(self, questEvent, taskState):
        pass

    def handleShipPVPSpawn(self, questEvent, taskState):
        pass

    def handleShipPVPSink(self, questEvent, taskState):
        pass

    def handleShipPVPEnemyDefeat(self, questEvent, taskState):
        pass

    def handleShipPVPShipDamage(self, questEvent, taskState):
        pass

    def handleShipPVPPlayerDamage(self, questEvent, taskState):
        pass

    def handleStart(self, avId):
        pass

    def complete(self, questEvent, taskState):
        taskState.handleProgress()

    def cutsceneWatched(self, questEvent, taskState):
        pass

    def getDescriptionText(self, state):
        raise 'derived must override'

    def getTitle(self):
        raise 'derived must override'

    def getDialogBefore(self):
        return random.choice(PLocalizer.QuestDefaultDialogBefore)

    def getDialogDuring(self):
        return random.choice(PLocalizer.QuestDefaultDialogDuring)

    def getDialogAfter(self):
        return random.choice(PLocalizer.QuestDefaultDialogAfter)

    def getSCSummaryText(self, state):
        return ''

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return ''

    def getReturnGiverIds(self):
        return

    def getTargetInfo(self, world):
        return

    def compileStats(self, questStatData):
        pass

    def getProgressMessage(self, taskState):
        return (None, None)


class VisitTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'npcId': None}

    def handleNPCVisit(self, questEvent, taskState):
        if questEvent.npcId == self.npcId:
            return True
        return False

    def handleObjectVisit(self, questEvent, taskState):
        if questEvent.objectId == self.npcId:
            return True
        return False

    def getDescriptionText(self, state):
        return PLocalizer.VisitTaskDesc % {'toNpcName': self.getNPCName(self.npcId)}

    def getSCSummaryText(self, state):
        return PLocalizer.QuestSCFindNPC % {'npcName': self.getNPCName(self.npcId)}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsNPC % {'npcName': self.getNPCName(self.npcId)}

    def getSCHowToText(self, state):
        return ''

    def getTitle(self):
        return PLocalizer.VisitTaskTitle % self.getNPCName(self.npcId)

    def getDialogAfter(self):
        return random.choice(PLocalizer.VisitTaskDefaultDialogAfter)

    def getReturnGiverIds(self):
        return makeTuple(self.npcId)

    def getTargetInfo(self, world):
        targetInfo = world.uid2doSearch(self.npcId)
        if targetInfo == None:
            return
        npcDoId = targetInfo[0]
        npcInstance = targetInfo[1]
        if npcDoId == None:
            return
        targetNpc = simbase.air.doId2do.get(npcDoId)
        if targetNpc == None:
            return
        location = targetNpc.getPos(npcInstance.worldGrid)
        object = targetNpc
        return (
         location, object.getUniqueId(), npcInstance)

    def getGoalUid(self):
        return self.getGoalLocation() or self.getNpcId()

    def compileStats(self, questStatData):
        questStatData.incrementTasks('visitTasks')
        questStatData.incrementMisc('visits')


class RecoverAvatarItemTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'item': None, 'num': 1, 'maxAttempts': 4, 'probability': 0.75, 'enemyType': AvatarTypes.AnyAvatar, 'level': 0}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def handleEnemyDefeat(self, questEvent, taskState):
        if not questEvent.enemyType.isA(self.enemyType):
            return False
        if questEvent.level < self.level:
            return False
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        found = False
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        if attempts == self.maxAttempts:
            found = True
        else:
            if attempts > self.maxAttempts:
                found = True
            else:
                if questEvent.getRng(self.item).random() <= self.probability:
                    found = True
        return found

    def complete(self, questEvent, taskState):
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        taskState.handleProgress()

    def getSCSummaryText(self, state):
        if self.num == 1:
            if self.level == 0:
                return PLocalizer.QuestSCRecoverItem % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'enemyName': self.enemyType.getStrings()[0]}
            else:
                return PLocalizer.QuestSCRecoverItemLvl % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'enemyName': self.enemyType.getStrings()[0], 'level': self.level}
        else:
            if self.level == 0:
                return PLocalizer.QuestSCRecoverItemNum % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'enemyName': self.enemyType.getStrings()[0]}
            else:
                return PLocalizer.QuestSCRecoverItemNumLvl % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'level': self.level, 'enemyName': self.enemyType.getStrings()[0]}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsEnemy % {'enemyName': self.enemyType.getStrings()[0]}

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowDoIRecover % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'enemyName': self.enemyType.getStrings()[0]}

    def getDescriptionText(self, state):
        if self.num == 1:
            if self.level == 0:
                return PLocalizer.RecoverAvatarItemTaskDescS % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'enemyName': self.enemyType.getStrings()[0]}
            else:
                return PLocalizer.RecoverAvatarItemTaskDescSL % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'enemyName': self.enemyType.getStrings()[0], 'level': self.level}
        else:
            if self.level == 0:
                return PLocalizer.RecoverAvatarItemTaskDescP % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'enemyName': self.enemyType.getStrings()[1]}
            else:
                return PLocalizer.RecoverAvatarItemTaskDescPL % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'level': self.level, 'enemyName': self.enemyType.getStrings()[1]}

    def getTitle(self):
        return PLocalizer.RecoverAvatarItemTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('recoverAvatarItemTasks')
        count = self.num * int((1.0 - self.probability) * self.maxAttempts)
        if count < self.num:
            count = self.num
        questStatData.incrementEnemies(self.enemyType.getName(), count)
        questStatData.incrementMisc('totalEnemies', count)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        itemName = PLocalizer.QuestItemNames[self.item][2]
        progressMsg = PLocalizer.RecoverItemProgress % (taskState.progress, taskState.goal, itemName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)

    def getGoalUid(self):
        result = QuestTaskDNA.getGoalUid(self)
        if result:
            return result
        level = max(0, self.getLevel())
        typeInfo = [level, self.getEnemyType()]
        goal = QuestGoal(typeInfo)
        return goal


class RecoverAvatarGroupItemTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'item': None, 'num': 1, 'maxAttempts': 4, 'probability': 0.75, 'enemyType': AvatarTypes.AnyAvatar, 'level': 0, 'enemyList': (AvatarTypes.AnyAvatar,), 'enemyNames': ('', '')}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def handleEnemyDefeat(self, questEvent, taskState):
        matchFound = False
        for enemy in self.enemyList:
            if questEvent.enemyType.isA(enemy):
                matchFound = True

        if not matchFound:
            return False
        if questEvent.level < self.level:
            return False
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        found = False
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        if attempts == self.maxAttempts:
            found = True
        else:
            if attempts > self.maxAttempts:
                found = True
            else:
                if questEvent.getRng(self.item).random() <= self.probability:
                    found = True
        return found

    def complete(self, questEvent, taskState):
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        taskState.handleProgress()

    def getSCSummaryText(self, state):
        if self.num == 1:
            if self.level == 0:
                return PLocalizer.QuestSCRecoverItem % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'enemyName': self.enemyNames[0]}
            else:
                return PLocalizer.QuestSCRecoverItemLvl % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'enemyName': self.enemyNames[0], 'level': self.level}
        else:
            if self.level == 0:
                return PLocalizer.QuestSCRecoverItemNum % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'enemyName': self.enemyNames[1]}
            else:
                return PLocalizer.QuestSCRecoverItemNumLvl % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'level': self.level, 'enemyName': self.enemyNames[1]}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsEnemy % {'enemyName': self.enemyNames[0]}

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowDoIRecover % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'enemyName': self.enemyNames[0]}

    def getDescriptionText(self, state):
        if self.num == 1:
            if self.level == 0:
                return PLocalizer.RecoverAvatarItemTaskDescS % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'enemyName': self.enemyNames[0]}
            else:
                return PLocalizer.RecoverAvatarItemTaskDescSL % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'enemyName': self.enemyNames[0], 'level': self.level}
        else:
            if self.level == 0:
                return PLocalizer.RecoverAvatarItemTaskDescP % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'enemyName': self.enemyNames[1]}
            else:
                return PLocalizer.RecoverAvatarItemTaskDescPL % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'level': self.level, 'enemyName': self.enemyNames[1]}

    def getTitle(self):
        return PLocalizer.RecoverAvatarItemTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('recoverAvatarGroupItemTasks')
        count = self.num * int((1.0 - self.probability) * self.maxAttempts)
        if count < self.num:
            count = self.num
        questStatData.incrementEnemies(self.enemyNames[0], count)
        questStatData.incrementMisc('totalEnemies', count)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        itemName = PLocalizer.QuestItemNames[self.item][2]
        progressMsg = PLocalizer.RecoverItemProgress % (taskState.progress, taskState.goal, itemName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)

    def getGoalUid(self):
        result = QuestTaskDNA.getGoalUid(self)
        if result:
            return result
        level = max(0, self.getLevel())
        typeInfo = [level, self.enemyList[0]]
        goal = QuestGoal(typeInfo)
        return goal


class RecoverShipItemTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'item': None, 'num': 1, 'maxAttempts': 4, 'probability': 0.75, 'faction': None, 'hull': None, 'level': 0, 'isFlagship': False, 'level': 0}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def handleShipDefeat(self, questEvent, taskState):
        if self.faction is not None:
            if not questEvent.faction.isA(self.faction):
                return False
        if self.hull is not None:
            shipClassList = getShipList(self.hull)
            if shipClassList:
                if questEvent.hull not in shipClassList:
                    return False
        if self.level > 0:
            if questEvent.level < self.level:
                return False
        if self.isFlagship == True and questEvent.isFlagship == False:
            return False
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        found = False
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        if attempts == self.maxAttempts:
            found = True
        else:
            if attempts > self.maxAttempts:
                found = True
            else:
                if questEvent.getRng(self.item).random() <= self.probability:
                    found = True
        return found

    def complete(self, questEvent, taskState):
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        taskState.handleProgress()

    def getSCSummaryText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.num == 1:
            if self.faction is None or self.faction == AvatarTypes.AnyShip:
                if shipType:
                    return PLocalizer.QuestSCRecoverShipItemShip % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'shipType': shipType}
                else:
                    return PLocalizer.QuestSCRecoverShipItem % {'itemName': PLocalizer.QuestItemNames[self.item][0]}
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
                if shipType:
                    return PLocalizer.QuestSCRecoverFactionShipItemShip % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'faction': faction, 'shipType': shipType}
                else:
                    return PLocalizer.QuestSCRecoverFactionShipItem % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'faction': faction}
        else:
            if self.faction is None or self.faction == AvatarTypes.AnyShip:
                if shipType:
                    return PLocalizer.QuestSCRecoverShipItemNumShip % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'shipType': shipType}
                else:
                    return PLocalizer.QuestSCRecoverShipItemNum % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1]}
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
                if shipType:
                    return PLocalizer.QuestSCRecoverFactionShipItemNumShip % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'faction': faction, 'shipType': shipType}
                else:
                    return PLocalizer.QuestSCRecoverFactionShipItemNum % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'faction': faction}
        return

    def getSCWhereIsText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                return PLocalizer.QuestSCWhereIsShip % {'shipType': shipType}
            else:
                return ''
        else:
            if shipType:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
                return PLocalizer.QuestSCWhereIsFactionShip % {'shipType': shipType, 'faction': faction}
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
                return PLocalizer.QuestSCWhereIsFaction % {'faction': faction}
        return

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowDoIRecoverShipItem % {'itemName': PLocalizer.QuestItemNames[self.item][0]}

    def getDescriptionText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.num == 1:
            if self.level == 0:
                if self.faction is None or self.faction == AvatarTypes.AnyShip:
                    if shipType:
                        return PLocalizer.RecoverShipItemTaskDescSN % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'shipType': shipType}
                    else:
                        return PLocalizer.RecoverShipItemTaskDescS % {'itemName': PLocalizer.QuestItemNames[self.item][0]}
                else:
                    faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
                    if shipType:
                        return PLocalizer.RecoverShipFactionItemTaskDescSN % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'faction': faction, 'shipType': shipType}
                    else:
                        return PLocalizer.RecoverShipFactionItemTaskDescS % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'faction': faction}
            elif self.faction is None or self.faction == AvatarTypes.AnyShip:
                if shipType:
                    return PLocalizer.RecoverShipItemLevelTaskDescSN % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'shipType': shipType, 'level': self.level}
                else:
                    return PLocalizer.RecoverShipItemLevelTaskDescS % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'level': self.level}
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
                if shipType:
                    return PLocalizer.RecoverShipFactionItemLevelTaskDescSN % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'faction': faction, 'shipType': shipType, 'level': self.level}
                else:
                    return PLocalizer.RecoverShipFactionItemLevelTaskDescS % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'faction': faction, 'level': self.level}
        else:
            if self.level == 0:
                if self.faction is None or self.faction == AvatarTypes.AnyShip:
                    if shipType:
                        return PLocalizer.RecoverShipItemTaskDescPN % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'shipType': shipType}
                    else:
                        return PLocalizer.RecoverShipItemTaskDescP % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1]}
                else:
                    faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
                    if shipType:
                        return PLocalizer.RecoverShipFactionItemTaskDescPN % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'faction': faction, 'shipType': shipType}
                    else:
                        return PLocalizer.RecoverShipFactionItemTaskDescP % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'faction': faction}
            else:
                if self.faction is None or self.faction == AvatarTypes.AnyShip:
                    if shipType:
                        return PLocalizer.RecoverShipItemLevelTaskDescPN % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'shipType': shipType, 'level': self.level}
                    else:
                        return PLocalizer.RecoverShipItemLevelTaskDescP % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'level': self.level}
                else:
                    faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
                    if shipType:
                        return PLocalizer.RecoverShipFactionItemLevelTaskDescPN % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'faction': faction, 'shipType': shipType, 'level': self.level}
                    else:
                        return PLocalizer.RecoverShipFactionItemLevelTaskDescP % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'faction': faction, 'level': self.level}
        return

    def getTitle(self):
        return PLocalizer.RecoverShipItemTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('recoverShipItemTasks')
        count = self.num * int((1.0 - self.probability) * self.maxAttempts)
        if count < self.num:
            count = self.num
        if self.faction:
            questStatData.incrementEnemies(self.faction.getName() + '-ship', count)
        questStatData.incrementMisc('totalShips', count)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        itemName = PLocalizer.QuestItemNames[self.item][2]
        progressMsg = PLocalizer.RecoverItemProgress % (taskState.progress, taskState.goal, itemName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)

    def getGoalUid(self):
        result = QuestTaskDNA.getGoalUid(self)
        if result:
            return result
        level = max(0, self.getLevel())
        typeInfo = [level, 'ship', self.getFaction(), self.getHull(), self.getIsFlagship()]
        goal = QuestGoal(typeInfo)
        return goal


class RecoverContainerItemTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'containerId': PropIds.ANY_PROP, 'item': None, 'num': 1, 'maxAttempts': 4, 'probability': 0.75}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def handleContainerSearched(self, questEvent, taskState):
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        allowedToSearch = taskState.searchedContainer(questEvent.containerId)
        if not allowedToSearch:
            return False
        containerMatches = False
        if self.containerId != PropIds.ANY_PROP:
            propList = getPropList(self.containerId)
            if propList:
                for prop in propList:
                    if prop == questEvent.containerId:
                        containerMatches = True

            elif self.containerId == questEvent.containerId:
                containerMatches = True
        else:
            containerMatches = True
        if not containerMatches:
            return False
        found = False
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        if attempts == self.maxAttempts:
            found = True
        else:
            if attempts > self.maxAttempts:
                found = True
            else:
                if questEvent.getRng(self.item).random() <= self.probability:
                    found = True
        return found

    def complete(self, questEvent, taskState):
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        taskState.handleProgress()

    def getSCSummaryText(self, state):
        if self.num == 1:
            return PLocalizer.QuestSCContainerItem % {'itemName': PLocalizer.QuestItemNames[self.item][0]}
        else:
            return PLocalizer.QuestSCContainerItemNum % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1]}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsContainers

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCFindHiddenContainer

    def getDescriptionText(self, state):
        if self.num == 1:
            return PLocalizer.RecoverContainerItemTaskDescS % {'itemName': PLocalizer.QuestItemNames[self.item][0]}
        else:
            return PLocalizer.RecoverContainerItemTaskDescP % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1]}

    def getTitle(self):
        return PLocalizer.RecoverContainerItemTaskTitle

    def getGoalUid(self):
        if self.getGoalLocation():
            return self.getGoalLocation()
        return

    def compileStats(self, questStatData):
        questStatData.incrementTasks('recoverContainerItemTasks')
        count = self.num * int((1.0 - self.probability) * self.maxAttempts)
        if count < self.num:
            count = self.num
        questStatData.incrementMisc('treasures', count)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        itemName = PLocalizer.QuestItemNames[self.item][2]
        progressMsg = PLocalizer.RecoverItemProgress % (taskState.progress, taskState.goal, itemName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)


class DeliverItemTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'item': None, 'num': 1, 'npcId': None, 'location': None}

    def handleNPCVisit(self, questEvent, taskState):
        if questEvent.npcId == self.npcId:
            return True
        return False

    def handleObjectVisit(self, questEvent, taskState):
        if questEvent.objectId == self.npcId:
            return True
        return False

    def handleDockedAtPort(self, questEvent, taskState):
        if self.getLocation():
            if self.locationMatches(questEvent):
                return True
        return False

    def getSCSummaryText(self, state):
        if self.npcId:
            locationName = self.getNPCName(self.npcId)
        else:
            if self.location:
                locationName = PLocalizer.LocationNames.get(self.location)
                if locationName == None:
                    return ''
            else:
                locationName = 'ErrorLocation'
        if self.num == 1:
            return PLocalizer.QuestSCDeliverItem % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'location': locationName}
        else:
            return PLocalizer.QuestSCDeliverItemNum % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'location': locationName}
        return

    def getSCWhereIsText(self, state):
        if self.npcId:
            locationName = self.getNPCName(self.npcId)
        else:
            if self.location:
                locationName = PLocalizer.LocationNames.get(self.location)
                if locationName == None:
                    locationName = 'Unknown Location'
            else:
                return ''
        return PLocalizer.QuestSCWhereIsNPC % {'npcName': locationName}

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        if self.npcId:
            locationName = self.getNPCName(self.npcId)
        else:
            if self.location:
                locationName = PLocalizer.LocationNames.get(self.location)
                if locationName == None:
                    locationName = 'Unknown Location'
            else:
                locationName = 'ErrorLocation'
        if self.num == 1:
            return PLocalizer.DeliverItemTaskDescS % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'location': locationName}
        else:
            return PLocalizer.DeliverItemTaskDescP % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'location': locationName}
        return

    def getTitle(self):
        return PLocalizer.DeliverItemTaskTitle

    def getGoalUid(self):
        return self.getNpcId()

    def compileStats(self, questStatData):
        questStatData.incrementTasks('deliverItemTasks')
        questStatData.incrementMisc('visits')

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        itemName = PLocalizer.QuestItemNames[self.item][2]
        progressMsg = PLocalizer.DeliverItemProgress % (self.num, self.num, itemName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)


class SmuggleItemTaskDNA(DeliverItemTaskDNA):
    __module__ = __name__

    def getSCSummaryText(self, state):
        if self.npcId:
            locationName = self.getNPCName(self.npcId)
        else:
            if self.location:
                locationName = PLocalizer.LocationNames.get(self.location)
                if locationName == None:
                    locationName = 'Unknown Location'
            else:
                return ''
        if self.num == 1:
            return PLocalizer.QuestSCSmuggleItem % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'location': locationName}
        else:
            return PLocalizer.QuestSCSmuggleItemNum % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'location': locationName}
        return

    def getSCWhereIsText(self, state):
        if self.npcId:
            locationName = self.getNPCName(self.npcId)
        else:
            if self.location:
                locationName = PLocalizer.LocationNames.get(self.location)
                if locationName == None:
                    locationName = 'Unknown Location'
            else:
                return ''
        return PLocalizer.QuestSCWhereIsNPC % {'npcName': locationName}

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        if self.npcId:
            locationName = self.getNPCName(self.npcId)
        else:
            if self.location:
                locationName = PLocalizer.LocationNames.get(self.location)
                if locationName == None:
                    locationName = 'Unknown Location'
            else:
                locationName = 'ErrorLocation'
        if self.num == 1:
            return PLocalizer.SmuggleItemTaskDescS % {'itemName': PLocalizer.QuestItemNames[self.item][0], 'location': locationName}
        else:
            return PLocalizer.SmuggleItemTaskDescP % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1], 'location': locationName}
        return

    def getTitle(self):
        return PLocalizer.SmuggleItemTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('smuggleItemTasks')

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        itemName = PLocalizer.QuestItemNames[self.item][2]
        progressMsg = PLocalizer.SmuggleItemProgress % (taskState.progress, taskState.goal, itemName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)


class MaroonNPCTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'npcId': None}

    def handleDockedAtPort(self, questEvent, taskState):
        if self.getLocation():
            if self.locationMatches(questEvent):
                return True
        return False

    def getSCSummaryText(self, state):
        npcName = self.getNPCName(self.npcId)
        locationName = PLocalizer.LocationNames.get(self.location)
        if locationName == None:
            locationName = 'Unknown Location'
        return PLocalizer.QuestSCMaroonNPC % {'npcName': npcName, 'location': locationName}

    def getSCWhereIsText(self, state):
        locationName = PLocalizer.LocationNames.get(self.location)
        if locationName == None:
            locationName = 'Unknown Location'
        return PLocalizer.QuestSCWhereIsLocation % {'location': locationName}

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowDoIMaroon

    def getDescriptionText(self, state):
        npcName = self.getNPCName(self.npcId)
        locationName = PLocalizer.LocationNames.get(self.location)
        if locationName == None:
            locationName = 'Unknown Location'
        return PLocalizer.MaroonNPCTaskDesc % {'npcName': npcName, 'location': locationName}

    def getTitle(self):
        return PLocalizer.MaroonNPCTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('maroonNPCTasks')


class BribeNPCTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'npcId': None, 'gold': 1, 'bribeType': 0}

    def handleNPCBribe(self, questEvent, taskState):
        if questEvent.npcId == self.npcId and questEvent.gold >= self.gold:
            return True
        return False

    def getSCSummaryText(self, state):
        return PLocalizer.QuestSCBribe % {'npcName': self.getNPCName(self.npcId)}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsNPC % {'npcName': self.getNPCName(self.npcId)}

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowToBribe

    def getDescriptionText(self, state):
        if self.bribeType == 1:
            return PLocalizer.BribeTaskAltDesc % {'toNpcName': self.getNPCName(self.npcId), 'gold': self.gold}
        else:
            return PLocalizer.BribeTaskDesc % {'toNpcName': self.getNPCName(self.npcId), 'gold': self.gold}

    def getTitle(self):
        return PLocalizer.BribeTaskTitle % self.getNPCName(self.npcId)

    def getDialogAfter(self):
        return random.choice(PLocalizer.BribeTaskDefaultDialogAfter)

    def getReturnGiverIds(self):
        return makeTuple(self.npcId)

    def getTargetInfo(self, world):
        targetInfo = world.uid2doSearch(self.npcId)
        if targetInfo == None:
            return
        npcDoId = targetInfo[0]
        npcInstance = targetInfo[1]
        if npcDoId == None:
            return
        targetNpc = simbase.air.doId2do.get(npcDoId)
        if targetNpc == None:
            return
        location = targetNpc.getPos(npcInstance.worldGrid)
        object = targetNpc
        return (
         location, object.getUniqueId(), npcInstance)

    def getGoalUid(self):
        return self.getNpcId()

    def compileStats(self, questStatData):
        questStatData.incrementTasks('bribeNPCTasks')
        questStatData.incrementMisc('gold', self.gold)


class PurchaseItemTaskDNA(QuestTaskDNA):
    __module__ = __name__


class PokerTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'gold': 1}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getGold())
        return state

    def handlePokerHandWon(self, questEvent, taskState):
        return True

    def complete(self, questEvent, taskState):
        taskState.handleProgress(questEvent.gold)

    def getSCSummaryText(self, state):
        if self.gold == 1:
            return PLocalizer.QuestSCPokerWinGold % {'gold': self.gold}
        else:
            return PLocalizer.QuestSCPokerWinGold % {'gold': self.gold}

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCWinPoker

    def getDescriptionText(self, state):
        if self.gold == 1:
            return PLocalizer.PokerTaskDescS % {'gold': self.gold}
        else:
            return PLocalizer.PokerTaskDescP % {'gold': self.gold}

    def getTitle(self):
        return PLocalizer.PokerTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('pokerTasks')
        questStatData.incrementMisc('poker-gold', self.gold)

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        progressMsg = PLocalizer.PokerProgress % (taskState.progress, taskState.goal)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)


class BlackjackTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'gold': 1}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getGold())
        return state

    def handleBlackjackHandWon(self, questEvent, taskState):
        return True

    def complete(self, questEvent, taskState):
        taskState.handleProgress(questEvent.gold)

    def getSCSummaryText(self, state):
        if self.gold == 1:
            return PLocalizer.QuestSCBlackjackWinGold % {'gold': self.gold}
        else:
            return PLocalizer.QuestSCBlackjackWinGold % {'gold': self.gold}

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCWinBlackjack

    def getDescriptionText(self, state):
        if self.gold == 1:
            return PLocalizer.BlackjackTaskDescS % {'gold': self.gold}
        else:
            return PLocalizer.BlackjackTaskDescP % {'gold': self.gold}

    def getTitle(self):
        return PLocalizer.BlackjackTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('blackjackTasks')
        questStatData.incrementMisc('poker-gold', self.gold)

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        progressMsg = PLocalizer.BlackjackProgress % (taskState.progress, taskState.goal)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)


class RecoverTreasureItemTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'treasureId': TreasureIds.ANY_TREASURE, 'item': None, 'num': 1, 'maxAttempts': 4, 'probability': 0.75}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def handleTreasureOpened(self, questEvent, taskState):
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        treasureMatches = False
        if self.treasureId != TreasureIds.ANY_TREASURE:
            treasureList = getTreasureList(self.treasureId)
            if treasureList:
                for treasure in treasureList:
                    if treasure == questEvent.treasureId:
                        treasureMatches = True

            else:
                self.notify.warning('No treasure list for: %s' % self.treasureId)
                return False
        else:
            treasureMatches = True
        if not treasureMatches:
            return False
        found = False
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        if attempts == self.maxAttempts:
            found = True
        else:
            if attempts > self.maxAttempts:
                found = True
            else:
                if questEvent.getRng(self.item).random() <= self.probability:
                    found = True
        return found

    def complete(self, questEvent, taskState):
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        taskState.handleProgress()

    def getSCSummaryText(self, state):
        if self.num == 1:
            return PLocalizer.QuestSCTreasureItem % {'itemName': PLocalizer.QuestItemNames[self.item][0]}
        else:
            return PLocalizer.QuestSCTreasureItemNum % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1]}

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCFindTreasure

    def getDescriptionText(self, state):
        if self.num == 1:
            return PLocalizer.RecoverTreasureItemTaskDescS % {'itemName': PLocalizer.QuestItemNames[self.item][0]}
        else:
            return PLocalizer.RecoverTreasureItemTaskDescP % {'num': self.num, 'itemName': PLocalizer.QuestItemNames[self.item][1]}

    def getTitle(self):
        return PLocalizer.RecoverTreasureItemTaskTitle

    def getGoalUid(self):
        if self.getGoalLocation():
            return self.getGoalLocation()
        return self.getTreasureId()

    def compileStats(self, questStatData):
        questStatData.incrementTasks('recoverTreasureItemTasks')
        count = self.num * int((1.0 - self.probability) * self.maxAttempts)
        if count < self.num:
            count = self.num
        questStatData.incrementMisc('treasures', count)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        itemName = PLocalizer.QuestItemNames[self.item][2]
        progressMsg = PLocalizer.TreasureItemProgress % (taskState.progress, taskState.goal, itemName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)


class DefeatTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'enemyType': AvatarTypes.AnyAvatar, 'num': 1, 'level': 0, 'weaponType': None}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def _getEnemyType(self, taskState):
        return self.getEnemyType()

    def _getNum(self, taskState):
        return self.getNum()

    def _getLevel(self, taskState):
        return self.getLevel()

    def handleEnemyDefeat(self, questEvent, taskState):
        if not questEvent.enemyType.isA(self._getEnemyType(taskState)):
            return False
        if questEvent.level < self._getLevel(taskState):
            return False
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        desiredWeapon = self.weaponType
        if desiredWeapon is not None:
            if questEvent.weaponType == desiredWeapon:
                return True
            else:
                return False
        return True

    def getSCSummaryText(self, state):
        strings = self.enemyType.getStrings()
        weaponName = PLocalizer.InventoryTypeNames.get(self.weaponType)
        if self.num == 1:
            if self.level == 0:
                if weaponName is not None:
                    return PLocalizer.QuestSCDefeatEnemyWeapon % {'enemyName': strings[0], 'weaponType': weaponName}
                else:
                    return PLocalizer.QuestSCDefeatEnemy % {'enemyName': strings[0]}
            elif weaponName is not None:
                return PLocalizer.QuestSCDefeatEnemyLvlWeapon % {'enemyName': strings[0], 'level': self.level, 'weaponType': weaponName}
            else:
                return PLocalizer.QuestSCDefeatEnemyLvl % {'enemyName': strings[0], 'level': self.level}
        else:
            if self.level == 0:
                if weaponName is not None:
                    return PLocalizer.QuestSCDefeatEnemiesWeapon % {'num': self.num, 'enemyName': strings[1], 'weaponType': weaponName}
                else:
                    return PLocalizer.QuestSCDefeatEnemies % {'num': self.num, 'enemyName': strings[1]}
            else:
                if weaponName is not None:
                    return PLocalizer.QuestSCDefeatEnemiesLvlWeapon % {'num': self.num, 'level': self.level, 'enemyName': strings[1], 'weaponType': weaponName}
                else:
                    return PLocalizer.QuestSCDefeatEnemiesLvl % {'num': self.num, 'level': self.level, 'enemyName': strings[1]}
        return

    def getSCWhereIsText(self, state):
        strings = self.enemyType.getStrings()
        return PLocalizer.QuestSCWhereIsEnemy % {'enemyName': strings[0]}

    def getSCSummaryText_Dynamic(self, state):
        strings = self._getEnemyType(state).getStrings()
        weaponName = PLocalizer.InventoryTypeNames.get(self.weaponType)
        if self._getNum(state) == 1:
            if self._getLevel(state) == 0:
                if weaponName is not None:
                    return PLocalizer.QuestSCDefeatEnemyWeapon % {'enemyName': strings[0], 'weaponType': weaponName}
                else:
                    return PLocalizer.QuestSCDefeatEnemy % {'enemyName': strings[0]}
            elif weaponName is not None:
                return PLocalizer.QuestSCDefeatEnemyLvlWeapon % {'enemyName': strings[0], 'level': self._getLevel(state), 'weaponType': weaponName}
            else:
                return PLocalizer.QuestSCDefeatEnemyLvl % {'enemyName': strings[0], 'level': self._getLevel(state)}
        else:
            if self._getLevel(state) == 0:
                if weaponName is not None:
                    return PLocalizer.QuestSCDefeatEnemiesWeapon % {'num': state.goal, 'enemyName': strings[1], 'weaponType': weaponName}
                else:
                    return PLocalizer.QuestSCDefeatEnemies % {'num': state.goal, 'enemyName': strings[1]}
            else:
                if weaponName is not None:
                    return PLocalizer.QuestSCDefeatEnemiesLvlWeapon % {'num': state.goal, 'level': self._getLevel(state), 'enemyName': strings[1], 'weaponType': weaponName}
                else:
                    return PLocalizer.QuestSCDefeatEnemiesLvl % {'num': state.goal, 'level': self._getLevel(state), 'enemyName': strings[1]}
        return

    def getSCWhereIsText_Dynamic(self, state):
        strings = self._getEnemyType(state).getStrings()
        return PLocalizer.QuestSCWhereIsEnemy % {'enemyName': strings[0]}

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        strings = self._getEnemyType(state).getStrings()
        weaponName = PLocalizer.InventoryTypeNames.get(self.weaponType)
        if self._getNum(state) == 1:
            if self._getLevel(state) == 0:
                if weaponName is not None:
                    return PLocalizer.DefeatTaskDescSWeapon % {'enemyName': strings[0], 'weaponType': weaponName}
                else:
                    return PLocalizer.DefeatTaskDescS % {'enemyName': strings[0]}
            elif weaponName is not None:
                return PLocalizer.DefeatTaskDescSLWeapon % {'enemyName': strings[0], 'level': self._getLevel(state), 'weaponType': weaponName}
            else:
                return PLocalizer.DefeatTaskDescSL % {'enemyName': strings[0], 'level': self._getLevel(state)}
        else:
            if self.level == 0:
                if weaponName is not None:
                    return PLocalizer.DefeatTaskDescPWeapon % {'num': self._getNum(state), 'enemyName': strings[1], 'weaponType': weaponName}
                else:
                    return PLocalizer.DefeatTaskDescP % {'num': self._getNum(state), 'enemyName': strings[1]}
            else:
                if weaponName is not None:
                    return PLocalizer.DefeatTaskDescPLWeapon % {'num': self._getNum(state), 'level': self._getLevel(state), 'enemyName': strings[1], 'weaponType': weaponName}
                else:
                    return PLocalizer.DefeatTaskDescPL % {'num': self._getNum(state), 'level': self._getLevel(state), 'enemyName': strings[1]}
        return

    def getTitle(self):
        if self.weaponType is not None:
            weaponName = PLocalizer.InventoryTypeNames.get(self.weaponType)
            if weaponName is not None:
                return PLocalizer.DefeatWithWeaponTaskTitle % (self.enemyType.getStrings()[1], weaponName)
        return PLocalizer.DefeatTaskTitle % self.enemyType.getStrings()[1]

    def compileStats(self, questStatData):
        questStatData.incrementTasks('recoverAvatarItemTasks')
        questStatData.incrementEnemies(self.enemyType.getName(), self.num)
        questStatData.incrementMisc('totalEnemies', self.num)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        enemyTypeName = self.enemyType.getStrings()[1]
        weaponName = PLocalizer.InventoryTypeNames.get(self.weaponType)
        if weaponName is not None:
            progressMsg = PLocalizer.DefeatProgressWeapon % (taskState.progress, taskState.goal, enemyTypeName, weaponName)
        else:
            progressMsg = PLocalizer.DefeatProgress % (taskState.progress, taskState.goal, enemyTypeName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (
         progressMsg, color)

    def getGoalUid(self):
        result = QuestTaskDNA.getGoalUid(self)
        if result:
            return result
        level = max(0, self.getLevel())
        typeInfo = [level, self.getEnemyType()]
        goal = QuestGoal(typeInfo)
        return goal


class DefeatGroupTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'enemyList': (AvatarTypes.AnyAvatar,), 'num': 1, 'level': 0, 'weaponType': None, 'enemyNames': ('', '')}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def handleEnemyDefeat(self, questEvent, taskState):
        matchFound = False
        for enemy in self.enemyList:
            if questEvent.enemyType.isA(enemy):
                matchFound = True

        if not matchFound:
            return False
        if questEvent.level < self.level:
            return False
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        desiredWeapon = self.weaponType
        if desiredWeapon is not None:
            if questEvent.weaponType == desiredWeapon:
                return True
            else:
                return False
        return True

    def getDescriptionText(self, state):
        weaponName = PLocalizer.InventoryTypeNames.get(self.weaponType)
        if self.getNum() == 1:
            if self.getLevel() == 0:
                if weaponName is not None:
                    return PLocalizer.DefeatTaskDescSWeapon % {'enemyName': self.enemyNames[0], 'weaponType': weaponName}
                else:
                    return PLocalizer.DefeatTaskDescS % {'enemyName': self.enemyNames[0]}
            elif weaponName is not None:
                return PLocalizer.DefeatTaskDescSLWeapon % {'enemyName': self.enemyNames[0], 'level': self.getLevel(), 'weaponType': weaponName}
            else:
                return PLocalizer.DefeatTaskDescSL % {'enemyName': self.enemyNames[0], 'level': self.getLevel()}
        else:
            if self.level == 0:
                if weaponName is not None:
                    return PLocalizer.DefeatTaskDescPWeapon % {'num': self.getNum(), 'enemyName': self.enemyNames[1], 'weaponType': weaponName}
                else:
                    return PLocalizer.DefeatTaskDescP % {'num': self.getNum(), 'enemyName': self.enemyNames[1]}
            else:
                if weaponName is not None:
                    return PLocalizer.DefeatTaskDescPLWeapon % {'num': self.getNum(), 'level': self.getLevel(), 'enemyName': self.enemyNames[1], 'weaponType': weaponName}
                else:
                    return PLocalizer.DefeatTaskDescPL % {'num': self.getNum(), 'level': self.getLevel(), 'enemyName': self.enemyNames[1]}
        return

    def getSCSummaryText(self, state):
        weaponName = PLocalizer.InventoryTypeNames.get(self.weaponType)
        if self.num == 1:
            if self.level == 0:
                if weaponName is not None:
                    return PLocalizer.QuestSCDefeatEnemyWeapon % {'enemyName': self.enemyNames[0], 'weaponType': weaponName}
                else:
                    return PLocalizer.QuestSCDefeatEnemy % {'enemyName': self.enemyNames[0]}
            elif weaponName is not None:
                return PLocalizer.QuestSCDefeatEnemyLvlWeapon % {'enemyName': self.enemyNames[0], 'level': self.level, 'weaponType': weaponName}
            else:
                return PLocalizer.QuestSCDefeatEnemyLvl % {'enemyName': self.enemyNames[0], 'level': self.level}
        else:
            if self.level == 0:
                if weaponName is not None:
                    return PLocalizer.QuestSCDefeatEnemiesWeapon % {'num': self.num, 'enemyName': self.enemyNames[1], 'weaponType': weaponName}
                else:
                    return PLocalizer.QuestSCDefeatEnemies % {'num': self.num, 'enemyName': self.enemyNames[1]}
            else:
                if weaponName is not None:
                    return PLocalizer.QuestSCDefeatEnemiesLvlWeapon % {'num': self.num, 'level': self.level, 'enemyName': self.enemyNames[1], 'weaponType': weaponName}
                else:
                    return PLocalizer.QuestSCDefeatEnemiesLvl % {'num': self.num, 'level': self.level, 'enemyName': self.enemyNames[1]}
        return

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsEnemy % {'enemyName': self.enemyNames[0]}

    def getSCSummaryText_Dynamic(self, state):
        return ''

    def getSCWhereIsText_Dynamic(self, state):
        return ''

    def getTitle(self):
        if self.weaponType is not None:
            weaponName = PLocalizer.InventoryTypeNames.get(self.weaponType)
            if weaponName is not None:
                return PLocalizer.DefeatWithWeaponTaskTitle % (self.enemyNames[1], weaponName)
        return PLocalizer.DefeatTaskTitle % self.enemyNames[1]

    def compileStats(self, questStatData):
        questStatData.incrementTasks('defeatgroupTasks')
        questStatData.incrementEnemies(self.enemyNames[0], self.num)
        questStatData.incrementMisc('totalEnemies', self.num)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        enemyTypeName = self.enemyNames[1]
        weaponName = PLocalizer.InventoryTypeNames.get(self.weaponType)
        if weaponName is not None:
            progressMsg = PLocalizer.DefeatProgressWeapon % (taskState.progress, taskState.goal, enemyTypeName, weaponName)
        else:
            progressMsg = PLocalizer.DefeatProgress % (taskState.progress, taskState.goal, enemyTypeName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (
         progressMsg, color)

    def getGoalUid(self):
        result = QuestTaskDNA.getGoalUid(self)
        if result:
            return result
        level = max(0, self.getLevel())
        typeInfo = [level, self.enemyList[0]]
        goal = QuestGoal(typeInfo)
        return goal


class ShipPVPDefeatTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'enemyClass': None, 'num': None, 'damage': None, 'gameType': None, 'killType': None, 'killWeapon': None, 'damageWeapon': None, 'withoutSink': False}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        if self.getNum() is not None:
            state.setGoal(self.getNum())
        else:
            state.setGoal(self.getDamage())
        return state

    def handleShipPVPPlayerDamage(self, questEvent, taskState):
        if self.getNum() is not None:
            return
        if self.enemyClass is not None:
            if self.enemyClass != questEvent.enemyClass:
                return False
        if self.gameType is not None:
            if self.gameType != questEvent.gameType:
                return False
        if self.killWeapon is not None:
            if self.killWeapon != questEvent.damageWeapon:
                return False
        if self.damageWeapon is not None:
            if self.damageWeapon != questEvent.damageWeapon:
                return False
        if self.killType is not None:
            if self.killType != PiratesGlobals.ShipPVPPirate:
                return False
        if questEvent.damage > 0:
            if questEvent.damage + taskState.progress > taskState.goal:
                taskState.progress = taskState.goal
            else:
                taskState.progress += questEvent.damage
            taskState.modified = True
        return

    def handleShipPVPShipDamage(self, questEvent, taskState):
        if self.getNum() is not None:
            return
        if self.enemyClass is not None:
            if self.enemyClass != questEvent.enemyClass:
                return False
        if self.gameType is not None:
            if self.gameType != questEvent.gameType:
                return False
        if self.killWeapon is not None:
            if self.killWeapon != questEvent.damageWeapon:
                return False
        if self.damageWeapon is not None:
            if self.damageWeapon != questEvent.damageWeapon:
                return False
        if self.killType is not None:
            if self.killType != PiratesGlobals.ShipPVPShip:
                return False
        if questEvent.damage > 0:
            if questEvent.damage + taskState.progress > taskState.goal:
                taskState.progress = taskState.goal
            else:
                taskState.progress += questEvent.damage
            taskState.modified = True
        return

    def handleShipPVPSpawn(self, questEvent, taskState):
        if self.withoutSink is True:
            taskState.progress = 0
            taskState.modified = True
        return False

    def handleShipPVPSink(self, questEvent, taskState):
        if self.withoutSink is True:
            taskState.progress = 0
            taskState.modified = True
        return False

    def handleShipPVPEnemyDefeat(self, questEvent, taskState):
        if self.enemyClass is not None:
            if self.enemyClass != questEvent.enemyClass:
                return False
        if self.gameType is not None:
            if self.gameType != questEvent.gameType:
                return False
        if self.killType is not None:
            if self.killType != questEvent.killType:
                return False
        if self.killWeapon is not None:
            if self.killWeapon != questEvent.killWeapon:
                return False
        if self.getDamage() is not None:
            return False
        return True

    def getSCSummaryText(self, state):
        return self.getDescriptionText(state)

    def getDescriptionText(self, state):
        enemyText = None
        weaponText = None
        gameTypeText = None
        killTypeText = None
        summaryText = None
        if self.enemyClass == PiratesGlobals.ShipPVPFrench:
            enemyText = PLocalizer.ShipPVPQuestFrench
        else:
            if self.enemyClass == PiratesGlobals.ShipPVPSpanish:
                enemyText = PLocalizer.ShipPVPQuestSpanish
        if self.killType == PiratesGlobals.ShipPVPShip:
            killTypeText = PLocalizer.ShipPVPQuestKillShip
        else:
            if self.killType == PiratesGlobals.ShipPVPPirate:
                killTypeText = PLocalizer.ShipPVPQuestKillPirate
        if self.killWeapon == PiratesGlobals.ShipPVPKillCannon:
            weaponText = PLocalizer.ShipPVPQuestUseCannon
        else:
            if self.killWeapon == PiratesGlobals.ShipPVPKillShip:
                weaponText = PLocalizer.ShipPVPQuestUseShip
        if self.gameType == PiratesGlobals.ShipPVPSiege:
            gameTypeText = PLocalizer.ShipPVPQuestGameName
        if self.num is not None:
            if self.num == 1:
                if enemyText is not None:
                    if self.killType == PiratesGlobals.ShipPVPShip:
                        summaryText = PLocalizer.ShipPVPQuestSingleNumA % (enemyText, gameTypeText)
                    else:
                        summaryText = PLocalizer.ShipPVPQuestSingleNumB % (enemyText, gameTypeText)
                else:
                    if self.killType == PiratesGlobals.ShipPVPShip:
                        summaryText = PLocalizer.ShipPVPQuestSingleAnyNumA % gameTypeText
                    else:
                        summaryText = PLocalizer.ShipPVPQuestSingleAnyNumB % gameTypeText
                if weaponText is not None:
                    summaryText += PLocalizer.ShipPVPQuestUsingA % weaponText
                if self.withoutSink is True:
                    summaryText += PLocalizer.ShipPVPQuestWithoutSinking
            else:
                numString = str(self.num)
                if enemyText is not None:
                    if self.killType == PiratesGlobals.ShipPVPShip:
                        summaryText = PLocalizer.ShipPVPQuestMultA % (numString, enemyText, gameTypeText)
                    else:
                        summaryText = PLocalizer.ShipPVPQuestMultB % (numString, enemyText, gameTypeText)
                else:
                    if self.killType == PiratesGlobals.ShipPVPShip:
                        summaryText = PLocalizer.ShipPVPQuestMultAnyA % (numString, gameTypeText)
                    else:
                        summaryText = PLocalizer.ShipPVPQuestMultAnyB % (numString, gameTypeText)
                if weaponText is not None:
                    summaryText += PLocalizer.ShipPVPQuestUsingA % weaponText
                if self.withoutSink is True:
                    summaryText += PLocalizer.ShipPVPQuestWithoutSinking
        else:
            numString = str(self.damage)
            if enemyText is not None:
                if self.killType == PiratesGlobals.ShipPVPShip:
                    summaryText = PLocalizer.ShipPVPQuestDamageA % (numString, enemyText, gameTypeText)
                else:
                    summaryText = PLocalizer.ShipPVPQuestDamageB % (numString, enemyText, gameTypeText)
            else:
                if killTypeText is not None:
                    if self.killType == PiratesGlobals.ShipPVPShip:
                        summaryText = PLocalizer.ShipPVPQuestDamageAnyA % (numString, gameTypeText)
                    else:
                        summaryText = PLocalizer.ShipPVPQuestDamageAnyB % (numString, gameTypeText)
                else:
                    summaryText = PLocalizer.ShipPVPQuestDamageAnyC % (numString, gameTypeText)
            if weaponText is not None:
                summaryText += PLocalizer.ShipPVPQuestUsingA % weaponText
            if self.withoutSink is True:
                summaryText += PLocalizer.ShipPVPQuestWithoutSinking
        return summaryText

    def compileStats(self, questStatData):
        if self.getNum() is not None:
            questStatData.incrementEnemies(str(self.enemyClass), self.num)
            questStatData.incrementMisc('totalEnemies', self.num)
        else:
            questStatData.incrementMisc('totalDamage', self.damage)
        return

    def getGoalNum(self):
        if self.getNum() is not None:
            return self.num
        else:
            return self.damage
        return

    def getProgressMessage(self, taskState):
        enemyText = None
        gameTypeText = None
        killTypeText = None
        weaponText = None
        progressText = None
        if self.enemyClass == PiratesGlobals.ShipPVPFrench:
            enemyText = PLocalizer.ShipPVPQuestFrench
        else:
            if self.enemyClass == PiratesGlobals.ShipPVPSpanish:
                enemyText = PLocalizer.ShipPVPQuestSpanish
        if self.gameType == PiratesGlobals.ShipPVPSiege:
            gameTypeText = PLocalizer.ShipPVPQuestGameName
        if self.killType == PiratesGlobals.ShipPVPShip:
            killTypeText = PLocalizer.ShipPVPQuestKillShipCap
        else:
            if self.killType == PiratesGlobals.ShipPVPPirate:
                killTypeText = PLocalizer.ShipPVPQuestKillPirateCap
        if self.killWeapon == PiratesGlobals.ShipPVPKillCannon:
            weaponText = PLocalizer.ShipPVPQuestUseCannonCap
        else:
            if self.killWeapon == PiratesGlobals.ShipPVPKillShip:
                weaponText = PLocalizer.ShipPVPQuestKillShipCap
        if self.num is not None:
            if self.num == 1:
                if enemyText is not None:
                    text = PLocalizer.ShipPVPQuestProgNumA % (enemyText, killTypeText, gameTypeText)
                else:
                    text = PLocalizer.ShipPVPQuestProgNumB % (killTypeText, gameTypeText)
            elif enemyText is not None:
                text = PLocalizer.ShipPVPQuestProgNumC % (taskState.progress, taskState.goal, enemyText, killTypeText, gameTypeText)
            else:
                text = PLocalizer.ShipPVPQuestProgNumD % (taskState.progress, taskState.goal, killTypeText, gameTypeText)
        else:
            if enemyText is not None:
                if killTypeText is not None:
                    text = PLocalizer.ShipPVPQuestProgDamA % (taskState.progress, taskState.goal, enemyText, killTypeText, gameTypeText)
                else:
                    text = PLocalizer.ShipPVPQuestProgDamB % (taskState.progress, taskState.goal, enemyText, gameTypeText)
            else:
                if killTypeText is not None:
                    text = PLocalizer.ShipPVPQuestProgDamC % (taskState.progress, taskState.goal, killTypeText, gameTypeText)
                else:
                    text = PLocalizer.ShipPVPQuestProgDamD % (taskState.progress, taskState.goal, gameTypeText)
        if weaponText is not None:
            text += PLocalizer.ShipPVPQuestUsingACap % weaponText
        if self.withoutSink is True:
            text += PLocalizer.ShipPVPQuestWithoutSinkingCap
        return (
         text, PiratesGuiGlobals.TextFG10)


class DefeatNPCTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'npcId': None}

    def handleNPCDefeat(self, questEvent, taskState):
        if questEvent.npcId == self.npcId:
            return True
        return False

    def getSCSummaryText(self, state):
        return PLocalizer.QuestSCDefeatEnemy % {'enemyName': self.getNPCName(self.npcId)}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsEnemy % {'enemyName': self.getNPCName(self.npcId)}

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        return PLocalizer.DefeatNPCTaskDesc % {'npcName': self.getNPCName(self.npcId)}

    def getTitle(self):
        return PLocalizer.DefeatNPCTaskTitle % self.getNPCName(self.npcId)

    def getGoalUid(self):
        return self.getNpcId()

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        npcName = self.getNPCName(self.npcId)
        progressMsg = PLocalizer.DefeatNPCProgress % npcName
        color = PiratesGuiGlobals.TextFG10
        return (
         progressMsg, color)


class DefeatShipTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'faction': None, 'hull': None, 'level': 0, 'isFlagship': False, 'num': 1, 'level': 0}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def _getFaction(self, taskState):
        return self.getFaction()

    def _getHull(self, taskState):
        return self.getHull()

    def _getIsFlagship(self, taskState):
        return self.getIsFlagship()

    def _getNum(self, taskState):
        return self.getNum()

    def handleShipDefeat(self, questEvent, taskState):
        if self._getFaction(taskState) is not None:
            if not questEvent.faction.isA(self._getFaction(taskState)):
                return False
        if self._getHull(taskState) is not None:
            shipClassList = getShipList(self._getHull(taskState))
            if shipClassList:
                if questEvent.hull not in shipClassList:
                    return False
        if self.level > 0:
            if questEvent.level < self.level:
                return False
        if self._getIsFlagship(taskState) == True and questEvent.isFlagship == False:
            return False
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        return True

    def getSCSummaryText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.num == 1:
            if self.faction is None or self.faction == AvatarTypes.AnyShip:
                if shipType:
                    return PLocalizer.QuestSCSinkShip % {'shipType': shipType}
                else:
                    return PLocalizer.QuestSCSink
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
                if shipType:
                    return PLocalizer.QuestSCSinkFactionShip % {'faction': faction, 'shipType': shipType}
                else:
                    return PLocalizer.QuestSCSinkFaction % {'faction': faction}
        else:
            if self.faction is None or self.faction == AvatarTypes.AnyShip:
                if shipType:
                    return PLocalizer.QuestSCSinkShipNum % {'num': self.num, 'shipType': shipType}
                else:
                    return PLocalizer.QuestSCSinkNum % {'num': self.num}
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
                if shipType:
                    return PLocalizer.QuestSCSinkFactionNumShip % {'num': self.num, 'faction': faction, 'shipType': shipType}
                else:
                    return PLocalizer.QuestSCSinkFactionNum % {'num': self.num, 'faction': faction}
        return

    def getSCWhereIsText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                return PLocalizer.QuestSCWhereIsShip % {'shipType': shipType}
            else:
                return ''
        else:
            if shipType:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
                return PLocalizer.QuestSCWhereIsFactionShip % {'faction': faction, 'shipType': shipType}
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
                return PLocalizer.QuestSCWhereIsFaction % {'faction': faction}
        return

    def getSCSummaryText_Dynamic(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if state.goal == 1:
            if self.faction is None or self.faction == AvatarTypes.AnyShip:
                if shipType:
                    return PLocalizer.QuestSCSinkShip % {'shipType': shipType}
                else:
                    return PLocalizer.QuestSCSink
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
                if shipType:
                    return PLocalizer.QuestSCSinkFactionShip % {'faction': faction, 'shipType': shipType}
                else:
                    return PLocalizer.QuestSCSinkFaction % {'faction': faction}
        else:
            if self.faction is None or self.faction == AvatarTypes.AnyShip:
                if shipType:
                    return PLocalizer.QuestSCSinkShipNum % {'num': state.goal, 'shipType': shipType}
                else:
                    return PLocalizer.QuestSCSinkNum % {'num': state.goal}
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
                if shipType:
                    return PLocalizer.QuestSCSinkFactionNumShip % {'num': state.goal, 'faction': faction, 'shipType': shipType}
                else:
                    return PLocalizer.QuestSCSinkFactionNum % {'num': state.goal, 'faction': faction}
        return

    def getSCWhereIsText_Dynamic(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                return PLocalizer.QuestSCWhereIsShip % {'shipType': shipType}
            else:
                return ''
        else:
            if shipType:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
                return PLocalizer.QuestSCWhereIsFactionShip % {'faction': faction, 'shipType': shipType}
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
                return PLocalizer.QuestSCWhereIsFaction % {'faction': faction}
        return

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if state.goal == 1:
            if self.faction is None or self.faction == AvatarTypes.AnyShip:
                if shipType:
                    return PLocalizer.DefeatShipTaskDescSN % {'shipType': shipType}
                else:
                    return PLocalizer.DefeatShipTaskDescS
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
                if shipType:
                    return PLocalizer.DefeatShipFactionTaskDescSN % {'faction': faction, 'shipType': shipType}
                else:
                    return PLocalizer.DefeatShipFactionTaskDescS % {'faction': faction}
        else:
            if self.faction is None or self.faction == AvatarTypes.AnyShip:
                if shipType:
                    return PLocalizer.DefeatShipTaskDescPN % {'num': state.goal, 'shipType': shipType}
                else:
                    return PLocalizer.DefeatShipTaskDescP % {'num': state.goal}
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
                if shipType:
                    return PLocalizer.DefeatShipFactionTaskDescPN % {'num': state.goal, 'faction': faction, 'shipType': shipType}
                else:
                    return PLocalizer.DefeatShipFactionTaskDescP % {'num': state.goal, 'faction': faction}
        return

    def getTitle(self):
        return PLocalizer.DefeatShipTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('defeatShipTasks')
        if self.faction:
            questStatData.incrementEnemies(self.faction.getName() + '-ship', self.num)
        questStatData.incrementMisc('totalShips', self.num)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                progressMsg = PLocalizer.DefeatShipTypeProgress % (taskState.progress, taskState.goal, shipType)
            else:
                progressMsg = PLocalizer.DefeatShipProgress % (taskState.progress, taskState.goal)
        else:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
            if shipType:
                progressMsg = PLocalizer.DefeatShipFactionTypeProgress % (taskState.progress, taskState.goal, faction, shipType)
            else:
                progressMsg = PLocalizer.DefeatShipFactionProgress % (taskState.progress, taskState.goal, faction)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)

    def getGoalUid(self):
        result = QuestTaskDNA.getGoalUid(self)
        if result:
            return result
        level = max(0, self.getLevel())
        typeInfo = [level, 'ship', self.getFaction(), self.getHull(), self.getIsFlagship()]
        goal = QuestGoal(typeInfo)
        return goal


class RandomizedDefeatTaskDNA(DefeatTaskDNA):
    __module__ = __name__

    def getInitialTaskState(self, holder):
        state = DefeatTaskDNA.getInitialTaskState(self, holder)
        enemyType, num = EnemyGlobals.getRandomEncounter(holder.getLevel())
        state.setEnemyType(enemyType)
        state.setGoal(num)
        return state

    def _getEnemyType(self, taskState):
        return taskState.enemyType

    def _getNum(self, taskState):
        return taskState.goal

    def computeRewards(self, initialTaskState, holder):
        return QuestReward.GoldReward(holder.getLevel())

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        enemyTypeName = taskState.enemyType.getStrings()[1]
        progressMsg = PLocalizer.DefeatProgress % (taskState.progress, taskState.goal, enemyTypeName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (
         progressMsg, color)


class RandomizedDefeatShipTaskDNA(DefeatShipTaskDNA):
    __module__ = __name__

    def getInitialTaskState(self, holder):
        state = DefeatShipTaskDNA.getInitialTaskState(self, holder)
        faction = random.choice([AvatarTypes.Navy])
        hull = random.choice([ShipGlobals.WARSHIPL1, ShipGlobals.WARSHIPL2])
        num = random.randint(2, 4)
        state.setFaction(faction)
        state.setHull(hull)
        state.setGoal(num)
        return state

    def _getFaction(self, taskState):
        return taskState.faction

    def _getHull(self, taskState):
        return taskState.hull

    def _getNum(self, taskState):
        return taskState.goal

    def computeRewards(self, initialTaskState, holder):
        return QuestReward.GoldReward(holder.getLevel())

    def getProgressMessage(self, taskState):
        if not taskState.progress:
            return (None, None)
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if taskState.faction is None or taskState.faction == AvatarTypes.AnyShip:
            if shipType:
                progressMsg = PLocalizer.DefeatShipTypeProgress % (taskState.progress, taskState.goal, shipType)
            else:
                progressMsg = PLocalizer.DefeatShipProgress % (taskState.progress, taskState.goal)
        else:
            faction = PLocalizer.FactionShipTypeNames[taskState.faction.getFaction()][1][1]
            if shipType:
                progressMsg = PLocalizer.DefeatShipFactionTypeProgress % (taskState.progress, taskState.goal, faction, shipType)
            else:
                progressMsg = PLocalizer.DefeatShipFactionProgress % (taskState.progress, taskState.goal, faction)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)


class ViewCutsceneTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'npcId': None, 'cutsceneId': None, 'dialogId': None, 'waitEvent': None}

    def handleStart(self, avId):
        self.avId = avId
        if self.waitEvent:
            playerAv = simbase.air.doId2do[self.avId]
            messenger.accept(playerAv.uniqueName(self.waitEvent), self, self._playCutscene, [], 0)
        else:
            self._playCutscene()

    def _playCutscene(self):
        playerAv = simbase.air.doId2do[self.avId]
        currWorld = playerAv.world
        npcId = currWorld.uidMgr.getDoId(self.npcId)
        npc = simbase.air.doId2do.get(npcId)
        if self.dialogId:
            npc.playDialogMovie(self.avId, self.dialogId)
        else:
            if self.cutsceneId:
                pass

    def handleNPCVisit(self, questEvent, taskState):
        if questEvent.npcId == self.npcId:
            playerAv = simbase.air.doId2do[self.avId]
            currWorld = playerAv.world
            npcId = currWorld.uidMgr.getDoId(self.npcId)
            npc = simbase.air.doId2do.get(npcId)
            playerAv.b_setGameState('NPCInteract', localArgs=[npc, True])
            if self.dialogId:
                npc.playDialogMovie(questEvent.avId, self.dialogId)
            else:
                if self.cutsceneId:
                    pass
            return True
        return False

    def cutsceneWatched(self, questEvent, taskState):
        if questEvent.npcId == self.npcId:
            return True
        return False

    def getDescriptionText(self, state):
        return PLocalizer.ViewCutsceneTaskDesc % {'toNpcName': self.getNPCName(self.npcId)} + ' to view cutscene'

    def getTitle(self):
        return PLocalizer.ViewCutsceneTaskTitle % self.getNPCName(self.npcId)

    def getDialogAfter(self):
        return random.choice(PLocalizer.QuestDefaultDialogBefore)

    def getReturnGiverIds(self):
        return makeTuple(self.npcId)

    def getTargetInfo(self, world):
        targetInfo = world.uid2doSearch(self.npcId)
        if targetInfo == None:
            return
        npcDoId = targetInfo[0]
        npcInstance = targetInfo[1]
        if npcDoId == None:
            return
        targetNpc = simbase.air.doId2do.get(npcDoId)
        if targetNpc == None:
            return
        location = targetNpc.getPos(npcInstance.worldGrid)
        object = targetNpc
        return (
         location, object.getUniqueId(), npcInstance)


class CaptureShipNPCTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'npcId': None, 'maxAttempts': 2, 'probability': 0.9, 'faction': None, 'hull': None, 'level': 0, 'isFlagship': False, 'level': 0}

    def handleShipDefeat(self, questEvent, taskState):
        if self.faction is not None:
            if not questEvent.faction.isA(self.faction):
                return False
        if self.hull is not None:
            shipClassList = getShipList(self.hull)
            if shipClassList:
                if questEvent.hull not in shipClassList:
                    return False
        if self.level > 0:
            if questEvent.level < self.level:
                return False
        if self.isFlagship == True and questEvent.isFlagship == False:
            return False
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        found = False
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        if attempts == self.maxAttempts:
            found = True
        else:
            if attempts > self.maxAttempts:
                found = True
            else:
                if questEvent.getRng(hash(self.npcId)).random() <= self.probability:
                    found = True
        return found

    def complete(self, questEvent, taskState):
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        taskState.handleProgress()

    def getSCSummaryText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                return PLocalizer.QuestSCCaptureNPCShip % {'npcName': self.getNPCName(self.npcId), 'shipType': shipType}
            else:
                return PLocalizer.QuestSCCaptureNPC % {'npcName': self.getNPCName(self.npcId)}
        else:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
            if shipType:
                return PLocalizer.QuestSCCaptureNPCFactionShip % {'npcName': self.getNPCName(self.npcId), 'faction': faction, 'shipType': shipType}
            else:
                return PLocalizer.QuestSCCaptureNPCFaction % {'npcName': self.getNPCName(self.npcId), 'faction': faction}
        return

    def getSCWhereIsText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                return ''
            else:
                return ''
        else:
            if shipType:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
                return PLocalizer.QuestSCWhereIsFactionShip % {'faction': faction, 'shipType': shipType}
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
                return PLocalizer.QuestSCWhereIsFaction % {'faction': faction}
        return

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowToCaptureShip

    def getDescriptionText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                return PLocalizer.CaptureShipNPCTaskDescSN % {'npcName': self.getNPCName(self.npcId), 'shipType': shipType}
            else:
                return PLocalizer.CaptureShipNPCTaskDescS % {'npcName': self.getNPCName(self.npcId)}
        else:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
            if shipType:
                return PLocalizer.CaptureShipFactionNPCTaskDescSN % {'npcName': self.getNPCName(self.npcId), 'faction': faction, 'shipType': shipType}
            else:
                return PLocalizer.CaptureShipFactionNPCTaskDescS % {'npcName': self.getNPCName(self.npcId), 'faction': faction}
        return

    def getTitle(self):
        return PLocalizer.CaptureShipNPCTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('captureShipNPCTasks')

    def getGoalUid(self):
        result = QuestTaskDNA.getGoalUid(self)
        if result:
            return result
        level = max(0, self.getLevel())
        typeInfo = [level, 'ship', self.getFaction(), self.getHull(), self.getIsFlagship()]
        goal = QuestGoal(typeInfo)
        return goal


class CaptureNPCTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'npcId': None, 'itemId': None}

    def getSCSummaryText(self, state):
        return PLocalizer.QuestSCCaptureNPC % {'npcName': self.getNPCName(self.npcId)}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsNPC % {'npcName': self.getNPCName(self.npcId)}

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        return PLocalizer.CaptureNPCTaskDesc % {'npcName': self.getNPCName(self.npcId)}

    def getTitle(self):
        return PLocalizer.CaptureNPCTaskTitle % self.getNPCName(self.npcId)


class BossBattleTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'treasureMapId': None}

    def handleBossBattleCompleted(self, questEvent, taskState):
        if questEvent.treasureMapId == self.treasureMapId:
            return True
        return False

    def getSCSummaryText(self, state):
        tmName = PiratesGlobals.DYNAMIC_GAME_STYLE_PROPS[PiratesGlobals.GAME_TYPE_TM][self.treasureMapId]['Name']
        return PLocalizer.QuestSCBossBattleMap % {'treasureMapId': tmName}

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        tmName = PiratesGlobals.DYNAMIC_GAME_STYLE_PROPS[PiratesGlobals.GAME_TYPE_TM][self.treasureMapId]['Name']
        return PLocalizer.BossBattleTaskDesc % {'treasureMapId': tmName}

    def getTitle(self):
        tmName = PiratesGlobals.DYNAMIC_GAME_STYLE_PROPS[PiratesGlobals.GAME_TYPE_TM][self.treasureMapId]['Name']
        return PLocalizer.BossBattleTaskTitle % tmName


class DeployShipTaskDNA(QuestTaskDNA):
    __module__ = __name__
    DataSet = {'location': None}

    def handleDeployedShip(self, questEvent, taskState):
        if self.getLocation():
            if self.locationMatches(questEvent):
                return True
            else:
                return False
        return True

    def getSCSummaryText(self, state):
        return PLocalizer.QuestSCDeployShip

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereDoIDeployShip

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowDoIDeployShip

    def getDescriptionText(self, state):
        return PLocalizer.DeployShipTaskDesc

    def getTitle(self):
        return PLocalizer.DeployShipTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('deployShipTasks')


DBId2Class = {0: VisitTaskDNA, 1: RecoverAvatarItemTaskDNA, 2: DefeatTaskDNA, 3: DefeatShipTaskDNA, 4: RecoverTreasureItemTaskDNA, 5: ViewCutsceneTaskDNA, 6: CaptureNPCTaskDNA, 7: PokerTaskDNA, 8: BlackjackTaskDNA, 9: DeliverItemTaskDNA, 10: RecoverShipItemTaskDNA, 11: RecoverContainerItemTaskDNA, 12: SmuggleItemTaskDNA, 13: PurchaseItemTaskDNA, 14: BribeNPCTaskDNA, 15: DefeatNPCTaskDNA, 16: MaroonNPCTaskDNA, 17: CaptureShipNPCTaskDNA, 18: BossBattleTaskDNA, 19: RandomizedDefeatTaskDNA, 20: RandomizedDefeatShipTaskDNA, 21: DeployShipTaskDNA, 22: ShipPVPDefeatTaskDNA, 23: RecoverAvatarGroupItemTaskDNA, 24: DefeatGroupTaskDNA}
Class2DBId = invertDict(DBId2Class)
RecoverItemClasses = (
 RecoverAvatarItemTaskDNA, RecoverTreasureItemTaskDNA, RecoverShipItemTaskDNA, RecoverContainerItemTaskDNA, RecoverAvatarGroupItemTaskDNA)
# okay decompiling .\pirates\quest\QuestTaskDNA.pyc
