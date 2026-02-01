from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import report
from pirates.pirate import AvatarType, AvatarTypes
from pirates.piratesbase import PiratesGlobals
from pirates.quest import QuestConstants
from pirates.piratesbase import TeamUtils
import types

class QuestGoal:
    Type_Uid = 0
    Type_Custom = 1
    
    def __init__(self, typeInfo):
        self.__goalDataStr = None
        self.__goalData = typeInfo
        self.__goalDataLen = len(self.__goalData)
        self.__goalType = type(self.__goalData)
    
    def getType(self):
        if self.__goalType == list:
            return self.Type_Custom
        
        return self.Type_Uid
    
    def getTargetType(self):
        if self.__goalType == list:
            return self.__goalData[1]
        return None

    def compareTo(self, object, goalOwner = None):
        if self.__goalType == list:
            if self.__goalData[0] > 0 and self.__goalData[0] > object.getLevel():
                return 1
            if object._isShip():
                if self.__goalData[1] == 'ship':
                    if self.__goalDataLen > 2:
                        isEnemy = False
                        if goalOwner:
                            isEnemy = TeamUtils.friendOrFoe(goalOwner, object) == PiratesGlobals.ENEMY
                        objFaction = object.getFaction()
                        if self.__goalData[2] != None and objFaction != None and self.__goalData[2].getFaction() != objFaction.getFaction() or not isEnemy:
                            return 1
                        if self.__goalDataLen > 3:
                            if self.__goalData[3] != None:
                                shipClassList = QuestConstants.getShipList(self.__goalData[3])
                                if shipClassList and object.shipClass not in shipClassList:
                                    return 1
                            if self.__goalDataLen > 4:
                                if self.__goalData[4] != object.isFlagship:
                                    return 1
                    return 0
            elif object.getAvatarType().isA(self.__goalData[1]):
                return 0
        elif self.__goalData == object.getUniqueId():
            return 0
        return 1
    
    def _asString(self):
        if self.__goalDataStr != None:
            return self.__goalDataStr
        
        if self.__goalData == None:
            resultStr = ''
        
        if self.__goalType == bytes:
            resultStr = self.__goalData
        else:
            strRep = ''
            for currField in self.__goalData:
                strRep += str(currField)
                strRep += '-'
            
            resultStr = strRep
        self.__goalDataStr = resultStr
        return resultStr

    def __repr__(self):
        return self._asString()

    def __str__(self):
        return self._asString()

    def __cmp__(self, other):
        strRep = self._asString()
        otherStrRep = other._asString()
        if strRep < otherStrRep:
            return -1
        elif strRep > otherStrRep:
            return 1
        
        return 0

    def __hash__(self):
        result = hash(self._asString())
        return result


class QuestStep:
    STNPC = 1
    STItem = 2
    STArea = 3
    STTunnel = 4
    STExteriorDoor = 5
    STInteriorDoor = 6
    STQuestNode = 7
    STShip = 8
    NullStep = None
    
    def __init__(self, originDoId, stepDoId, stepType, posH = (0, 0, 0, 0), islandId = ''):
        self.originDoId = originDoId
        self.stepDoId = stepDoId
        self.stepType = stepType
        self.posH = posH
        self.islandId = islandId

    def __repr__(self):
        return 'QuestStep(%d, %d, %d, %s, %s)' % (self.getOriginDoId(), self.getStepDoId(), self.getStepType(), repr(self.getPosH()), self.islandId)
    
    def __cmp__(self, other):
        return not isinstance(other, QuestStep) or cmp(self.originDoId, other.originDoId) or cmp(self.stepDoId, other.stepDoId) or cmp(self.stepType, other.stepType) or cmp(self.posH, other.posH) or cmp(self.islandId, other.islandId)
    
    def getOriginDoId(self):
        return self.originDoId

    def getStepDoId(self):
        return self.stepDoId

    def getStepType(self):
        return self.stepType
    
    def getPosH(self):
        return self.posH
    
    def setIsland(self, islandId = ''):
        self.islandId = islandId

    def getIsland(self):
        return self.islandId

    @staticmethod
    def getNullStep():
        if QuestStep.NullStep:
            pass
        else:
            QuestStep.NullStep = QuestStep(0, 0, 0)
        return QuestStep.NullStep


class QuestPath:
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestPath')
    
    def __init__(self, air):
        self.world = None
        self.posH = (0, 0, 0, 0)
        self.questSteps = {}
        self.islandStep = None
        self.islandDoId = None
        self.preferredStepUids = set()
        if __dev__:
            pass

    def delete(self):
        self.islandDoId = None
        self.islandStep = None
        self.questSteps = {}
        self.world = None

    def setWorld(self, world):
        self.world = world

    def setQuestStepPosH(self, x, y, z, h):
        self.posH = (x, y, z, h)

    def getIslandDoId(self):
        if self.islandDoId:
            pass
        elif self._isIsland():
            self.islandDoId = self.doId
        return self.islandDoId

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def getQuestStepIsland(self):
        if self._isIsland():
            return QuestStep(0, self.getIslandDoId(), self._getQuestStepType())

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def getQuestStep(self, questDestUid, islandDoId, avId):
        if not self.getIslandDoId():
            self.getExitIslandStep()
        questIslandDoId = islandDoId
        questIsland = None
        isPrivate = False
        goalType = questDestUid.getType()
        if goalType != QuestGoal.Type_Custom:
            if islandDoId == None:
                questIslandDoId = self.world.getObjectIslandDoId(questDestUid)
            isPrivate = self.world.getObjectIsPrivate(questDestUid)
            if not questIslandDoId:
                return
            questIsland = self.air.doId2do.get(questIslandDoId)
            if not questIsland:
                return
        if questIslandDoId or goalType == QuestGoal.Type_Custom:
            if (self.getIslandDoId() == questIslandDoId or goalType == QuestGoal.Type_Custom) and questDestUid.getTargetType() != 'ship':
                islandObj = self.getIsland()
                if islandObj and goalType == QuestGoal.Type_Custom and islandObj.notHasQuestGoal(questDestUid):
                    return QuestStep.NullStep
                islandSearchResult = self.getIntoIslandStep(questDestUid, isPrivate, avId)
                if islandObj and (islandSearchResult == None or islandSearchResult == QuestStep.NullStep):
                    islandObj.setNotHasQuestGoal(questDestUid)
                return islandSearchResult
            else:
                step = self.getExitIslandStep()
                if step:
                    return step
                else:
                    destIsland = self.air.doId2do.get(questIslandDoId)
                    if destIsland:
                        return QuestStep(self.doId, questIslandDoId, questIsland._getQuestStepType())

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def getExitIslandStep(self):
        if self._isIsland() or self._isShip():
            return None
        
        if not self.islandStep:
            self._getIslandPath([], [], {})
        
        return self.islandStep

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def getIntoIslandStep(self, questDestUid, isPrivate, avId = None):
        questStep = self.questSteps.get(questDestUid)
        if not questStep:
            self._getQuestPath(questDestUid, isPrivate, [], [], {}, avId)
        
        questStep = self.questSteps.get(questDestUid)
        if questStep and questDestUid.getType() == QuestGoal.Type_Custom:
            self.questSteps.pop(questDestUid, None)
        
        return questStep
    
    def getOntoOceanStep(self, questDestUid, avId):
        questDest = None
        questDoId = self.world.queryGoal(questDestUid, self, avId)
        if questDoId:
            questGoalObj = self.air.doId2do.get(questDoId)
            if questGoalObj:
                questDest = QuestStep(self.world.worldGrid.doId, questDoId, questGoalObj._getQuestStepType(), questGoalObj._getQuestStepPosH())
                avObj = self.air.doId2do.get(avId)
                if avObj:
                    avObj.setQuestGoalDoId(questGoalObj)

        return questDest

    def _getExitLinkDoIds(self, questGoalUid):
        if __dev__:
            pass

        return []
    
    def _getQuestStepType(self):
        if __dev__:
            pass

        return 0

    def _isIsland(self):
        if __dev__:
            pass

        return False
    
    def _isShip(self):
        return False

    def _getQuestStepPosH(self):
        return self.posH

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def _getIslandPath(self, alreadyVisited, needToVisit, pathDict):
        islandPath = []
        needToStore = False
        if not islandPath:
            if self._isIsland():
                islandPath = alreadyVisited + [self.doId]
        if not islandPath:
            if self.islandStep:
                islandPath = alreadyVisited + [self.doId]
        if islandPath:
            finalPath = [
             islandPath[-1]]
            next = pathDict.get(finalPath[-1])
            while next:
                finalPath.append(next)
                next = pathDict.get(finalPath[-1])

            finalPath.reverse()
        else:
            exitLinks = [ linkDoId for linkDoId in self._getExitLinkDoIds(None) if linkDoId not in alreadyVisited if linkDoId not in needToVisit ]
            for link in exitLinks:
                pathDict[link] = self.doId

            needToVisit += exitLinks
            if needToVisit:
                nextDoId = needToVisit.pop(0)
                nextStep = self.air.doId2do[nextDoId]
                finalPath = nextStep._getIslandPath(alreadyVisited + [self.doId], needToVisit, pathDict)
                needToStore = True
            else:
                finalPath = []
        if needToStore and self.doId in finalPath:
            self._storeIslandStep(finalPath)
        return finalPath

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def _storeIslandStep(self, path):
        stepDoId = path[path.index(self.doId) + 1]
        step = self.air.doId2do[stepDoId]
        if __dev__:
            pass

        self.islandStep = QuestStep(self.doId, stepDoId, step._getQuestStepType(), step._getQuestStepPosH())
        self.islandDoId = step.islandDoId

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def _getQuestPath(self, questDestUid, isPrivate, alreadyVisited, needToVisit, pathDict, avId):
        questDest = None
        questPath = []
        needToStore = False
        if not isPrivate:
            if not questPath:
                questDoId = self.world.queryGoal(questDestUid, self, avId)
                if questDoId:
                    questGoalObj = self.air.doId2do.get(questDoId)
                    if questGoalObj:
                        if questGoalObj.getParentObj() is self:
                            if questDoId != self.doId:
                                pathDict.setdefault(questDoId, self.doId)
                            questPath = alreadyVisited + [self.doId, questDoId]
                            questDest = QuestStep(self.doId, questDoId, questGoalObj._getQuestStepType(), questGoalObj._getQuestStepPosH())
                            needToStore = True
                            avObj = self.air.doId2do.get(avId)
                            if avObj:
                                avObj.setQuestGoalDoId(questGoalObj)
            if not questPath and questDestUid.getType() != QuestGoal.Type_Custom:
                try:
                    objInfo = self.air.worldCreator.getObjectDataFromFileByUid(str(questDestUid), self.getFileName())
                    if objInfo and objInfo.get('Type') in ['Quest Node', 'Dinghy']:
                        pos = objInfo['Pos']
                        hpr = objInfo['Hpr']
                        questPath = alreadyVisited + [self.doId]
                        questDest = QuestStep(self.doId, 0, QuestStep.STQuestNode, (
                         pos[0], pos[1], pos[2], hpr[0]))
                        needToStore = True
                except AttributeError:
                    pass

        elif not questPath:
            if self.air.worldCreator.isObjectDefined(str(questDestUid), self.world.getFileName() + '.py'):
                questPath = alreadyVisited + [self.doId]
                needToStore = False
        if questPath:
            finalPath = [
             questPath[-1]]
            next = pathDict.get(finalPath[-1])
            while next:
                finalPath.append(next)
                next = pathDict.get(finalPath[-1])

            finalPath.reverse()
        else:
            exitLinks = [ linkDoId for linkDoId in self._getExitLinkDoIds(str(questDestUid)) if linkDoId not in alreadyVisited if linkDoId not in needToVisit ]
            for link in exitLinks:
                pathDict[link] = self.doId

            needToVisit += exitLinks
            if needToVisit:
                nextDoId = needToVisit.pop(0)
                nextStep = self.air.doId2do[nextDoId]
                finalPath = nextStep._getQuestPath(questDestUid, isPrivate, alreadyVisited + [self.doId], needToVisit, pathDict, avId)
                questStep = nextStep.questSteps.get(questDestUid)
                if questStep and questDestUid.getType() == QuestGoal.Type_Custom:
                    del nextStep.questSteps[questDestUid]
                needToStore = True
            else:
                finalPath = []
                needToStore = True
        if needToStore and self.doId in finalPath:
            self._storeQuestStep(finalPath, questDestUid, questDest)
        if not finalPath:
            self._storeQuestStep(finalPath, questDestUid, questStep=QuestStep.getNullStep())
        return finalPath

    @report(types=['frameCount', 'args'], dConfigParam='want-quest-indicator-report')
    def _storeQuestStep(self, path, questDestUid, questStep = None):
        if not questStep:
            stepDoId = path[path.index(self.doId) + 1]
            step = self.air.doId2do[stepDoId]
            if __dev__:
                pass

            questStep = QuestStep(self.doId, stepDoId, step._getQuestStepType(), step._getQuestStepPosH())
        
        self.questSteps[questDestUid] = questStep
    
    def setAsPreferredStepFor(self, questGoalUid):
        self.preferredStepUids.add(questGoalUid)
    
    def isPreferredStep(self, questGoalUid):
        return questGoalUid in self.preferredStepUids


