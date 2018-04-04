# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.world.WorldCreatorBase
import imp
import os
import re
import types

from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals


class WorldCreatorBase:

    def __init__(self, repository, worldFile=None):
        self.parentWorlds = []
        self.creatingInstance = False
        self.creatingInstanceParams = None
        self.repository = repository

    def makeMainWorld(self, worldFile):
        self.worldType = PiratesGlobals.INSTANCE_MAIN
        if worldFile is not None:
            self.loadObjectsFromFile(worldFile, self.repository)

        self.worldType = None

    def loadObjectsFromFile(self, filename, parent, zoneLevel=0, startTime=None, parentIsObj=False):
        fileDict = self.openFile(filename)
        objDict = fileDict.get('Objects')
        parentUid = None
        if hasattr(parent, 'getUniqueId'):
            parentUid = parent.getUniqueId()

        objects = self.loadObjectDict(objDict, parent, parentUid, dynamic=0, zoneLevel=zoneLevel, startTime=startTime,
            parentIsObj=parentIsObj, fileName=re.sub('.py', '', filename))

        return [fileDict, objects]

    def loadObjectDict(self, objDict, parent, parentUid, dynamic, zoneLevel=0, startTime=None, parentIsObj=False, fileName=None, actualParentObj=None):
        objects = []
        for objKey in objDict.keys():
            newObj = self.loadObject(objDict[objKey], parent, parentUid, objKey, dynamic, zoneLevel=zoneLevel, startTime=startTime,
                parentIsObj=parentIsObj, fileName=fileName, actualParentObj=actualParentObj)

            if newObj:
                objects.append(newObj)

        return objects

    def loadInstancedObject(self, object, parent, parentUid, objKey, instanceParams=[]):
        self.creatingInstance = True
        self.creatingInstanceParams = instanceParams
        newObj = self.loadObject(object, parent, parentUid, objKey, False)
        self.creatingInstance = False
        self.creatingInstanceParams = None
        return newObj

    def loadObject(self, object, parent, parentUid, objKey, dynamic, zoneLevel=0, startTime=None, parentIsObj=False, fileName=None, actualParentObj=None):
        if not self.isObjectInCurrentGamePhase(object):
            return

        prevWorld = self.world
        newObjInfo = self.createObject(object, parent, parentUid, objKey, dynamic, zoneLevel=zoneLevel, startTime=startTime, parentIsObj=parentIsObj,
            fileName=fileName, actualParentObj=actualParentObj)

        if newObjInfo:
            newObj, newActualParent = newObjInfo
        else:
            return

        instanced = object.get('Instanced')
        if instanced:
            self.world.setCanBePrivate(instanced)

        objDict = object.get('Objects')
        if objDict:
            if newObj == None:
                newObj = parent
                if hasattr(newObj, 'getUniqueId'):
                    objKey = newObj.getUniqueId()

            self.loadObjectDict(objDict, newObj, objKey, dynamic, zoneLevel=zoneLevel, startTime=startTime,
                fileName=fileName, actualParentObj=newActualParent)

        self._restoreWorld(prevWorld)
        return newObj

    def _restoreWorld(self, prevWorld):
        parentWorld = None
        if self.parentWorlds:
            parentWorld = self.parentWorlds[-1]

        if parentWorld:
            if prevWorld is not self.world:
                self.world = self.parentWorlds.pop()
        else:
            self.world = prevWorld

    def createObject(self, object, parent, parentUid, objKey, dynamic, zoneLevel=0, startTime=None, parentIsObj=False, fileName=None, actualParentObj=None):
        objType = object.get('Type')
        self.notify.debug('createObject: type = %s' % objType)
        if dynamic and object.get('ExtUid'):
            return objType

        childFilename = object.get('File')
        if childFilename and object['Type'] != 'Building Exterior' and object['Type'] != 'Island Game Area':
            self.loadObjectsFromFile(childFilename + '.py', parent, zoneLevel=zoneLevel, startTime=startTime)
            return

        return objType

    def openFile(self, filename):
        objectStruct = None
        moduleName = filename[:-3]

        try:
            obj = __import__('pirates.leveleditor.worldData.%s' % moduleName)
        except ImportError:
            obj = None
        except ValueError, e:
            self.notify.error('%s when loading %s' % (e, filename))

        for symbol in ['leveleditor', 'worldData', moduleName, 'objectStruct']:
            if obj:
                obj = getattr(obj, symbol, None)

        if not obj:
            self.notify.error('Failed to load worldData file: %s!' % moduleName)

        return obj

    def getObjectDataByUid(self, uid, fileDict=None):
        if fileDict is None:
            fileDict = self.fileDicts

        objectInfo = None
        for name in fileDict:
            fileData = fileDict[name]
            if not fileData['ObjectIds'].has_key(uid):
                continue

            getSyntax = 'objectInfo = fileData' + fileData['ObjectIds'][uid]
            exec getSyntax
            if not objectInfo.has_key('File') or objectInfo.get('File') == '':
                break

        return objectInfo

    def getObjectDataFromFileByUid(self, uid, fileName):
        objectInfo = None
        if fileName:
            if '.py' not in fileName:
                fileName += '.py'

            if self.isObjectDefined(uid, fileName):
                fileData = self.fileDicts[fileName]
                getSyntax = 'objectInfo = fileData' + fileData['ObjectIds'][uid]
                exec getSyntax

        return objectInfo

    def getFilelistByUid(self, uid, fileDict = None):
        objectInfo = None
        if not fileDict:
            fileDict = self.fileDicts

        fileList = set()
        for name in fileDict:
            fileData = fileDict[name]
            if not fileData['ObjectIds'].has_key(uid):
                continue

            getSyntax = 'objectInfo = fileData' + fileData['ObjectIds'][uid]
            exec getSyntax
            fileList.add(name)
            objects = objectInfo.get('Objects')
            if objects:
                for obj in objects.values():
                    visual = obj.get('Visual')
                    if visual:
                        model = visual.get('Model')
                        if model:
                            if type(model) is types.ListType:
                                for currModel in model:
                                    fileList.add(currModel + '.bam')
                            else:
                                fileList.add(model + '.bam')

            objects = fileData.get('Objects')
            if objects:
                for obj in objects.values():
                    visual = obj.get('Visual')
                    if visual:
                        model = visual.get('Model')
                        if model:
                            fileList.add(model + '.bam')

            if not objectInfo.has_key('File') or objectInfo.get('File') == '':
                break
                continue

        return list(fileList)

    def getObjectIslandUid(self, objUid, fileDict=None):
        if not fileDict:
            fileDict = self.fileDicts

        found = False
        curUid = objUid
        isPrivate = False
        while curUid:
            curFile = None
            for name in fileDict:
                fileData = fileDict[name]
                if not fileData['ObjectIds'].has_key(str(curUid)):
                    continue

                if fileData['Objects'].has_key(str(curUid)):
                    if fileData['Objects'][str(curUid)].get('Type') == 'Island':
                        return (str(curUid), isPrivate)

                    continue

                objData = fileData['Objects'].values()[0]['Objects']
                if objData.has_key(str(curUid)):
                    if curUid == objUid:
                        if objData[str(curUid)].get('Private Status') == 'Private Only':
                            isPrivate = True
                    if objData[str(curUid)].get('Type') == 'Island':
                        return (str(curUid), isPrivate)

                curFile = fileData
                break

            if not curFile:
                return
            else:
                curUid = curFile.get('Objects', {}).keys()[0]
                if curFile['Objects'][str(curUid)].get('Type') == 'Island':
                    return (curUid, isPrivate)

    def isObjectDefined(self, objUid, fileName):
        fileDict = self.fileDicts
        fileData = fileDict.get(fileName)
        if fileData and fileData['ObjectIds'].has_key(objUid):
            return True
        else:
            return False

    def isPvpIslandByUid(self, islandUid):
        if not getBase().config.GetBool('want-privateering', 1):
            return False

        return 'PVPTeam' in self.getObjectDataByUid(islandUid)

    def getPvpIslandTeam(self, islandUid):
        return int(self.getObjectDataByUid(islandUid).get('PVPTeam', 0))
