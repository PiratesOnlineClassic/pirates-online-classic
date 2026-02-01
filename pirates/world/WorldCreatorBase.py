from panda3d.core import *
from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals
import os
import re
import imp
import types

class WorldCreatorBase:
    
    def __init__(self, repository, worldFile = None):
        self.parentWorlds = []
        self.creatingInstance = False
        self.creatingInstanceParams = None
        self.repository = repository

    def makeMainWorld(self, worldFile):
        self.worldType = PiratesGlobals.INSTANCE_MAIN
        if worldFile is not None:
            self.loadObjectsFromFile(worldFile, self.repository)
        
        self.worldType = None
    
    def loadObjectsFromFile(self, filename, parent, zoneLevel = 0, startTime = None, parentIsObj = False):
        fileDict = self.openFile(filename)
        objDict = fileDict.get('Objects')
        parentUid = None
        if hasattr(parent, 'getUniqueId'):
            parentUid = parent.getUniqueId()
        
        objects = self.loadObjectDict(objDict, parent, parentUid, dynamic = 0, zoneLevel = zoneLevel, startTime = startTime, parentIsObj = parentIsObj, fileName = re.sub('.py', '', filename))
        return [
            fileDict,
            objects]
    
    def loadObjectDict(self, objDict, parent, parentUid, dynamic, zoneLevel = 0, startTime = None, parentIsObj = False, fileName = None, actualParentObj = None):
        objects = []
        for objKey in list(objDict.keys()):
            newObj = self.loadObject(objDict[objKey], parent, parentUid, objKey, dynamic, zoneLevel = zoneLevel, startTime = startTime, parentIsObj = parentIsObj, fileName = fileName, actualParentObj = actualParentObj)
            if newObj:
                objects.append(newObj)
        
        return objects
    
    def loadInstancedObject(self, object, parent, parentUid, objKey, instanceParams = []):
        self.creatingInstance = True
        self.creatingInstanceParams = instanceParams
        newObj = self.loadObject(object, parent, parentUid, objKey, False)
        self.creatingInstance = False
        self.creatingInstanceParams = None
        return newObj

    def loadObject(self, object, parent, parentUid, objKey, dynamic, zoneLevel = 0, startTime = None, parentIsObj = False, fileName = None, actualParentObj = None):
        if not self.isObjectInCurrentGamePhase(object):
            return
        
        prevWorld = self.world
        newObjInfo = self.createObject(object, parent, parentUid, objKey, dynamic, zoneLevel = zoneLevel, startTime = startTime, parentIsObj = parentIsObj, fileName = fileName, actualParentObj = actualParentObj)
        if newObjInfo:
            (newObj, newActualParent) = newObjInfo
        else:
            return None
        instanced = object.get('Instanced')
        if instanced:
            self.world.setCanBePrivate(instanced)
        
        objDict = object.get('Objects')
        if objDict:
            if newObj == None:
                newObj = parent
                if hasattr(newObj, 'getUniqueId'):
                    objKey = newObj.getUniqueId()

            self.loadObjectDict(objDict, newObj, objKey, dynamic, zoneLevel = zoneLevel, startTime = startTime, fileName = fileName, actualParentObj = newActualParent)
        
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

    def createObject(self, object, parent, parentUid, objKey, dynamic, zoneLevel = 0, startTime = None, parentIsObj = False, fileName = None, actualParentObj = None):
        objType = object.get('Type')
        self.notify.debug('createObject: type = %s' % objType)
        if dynamic and object.get('ExtUid'):
            return objType
        
        childFilename = object.get('File')
        if childFilename and object['Type'] != 'Building Exterior' and object['Type'] != 'Island Game Area':
            self.loadObjectsFromFile(childFilename + '.py', parent, zoneLevel = zoneLevel, startTime = startTime)
            return None
        
        return objType

    def openFile(self, filename):
        objectStruct = None
        moduleName = filename[:-3]
        
        try:
            obj = __import__('pirates.leveleditor.worldData.' + moduleName)
        except ImportError:
            obj = None
        except ValueError as e:
            self.notify.error('%s when loading %s' % (e, filename))

        for symbol in [
            'leveleditor',
            'worldData',
            moduleName,
            'objectStruct']:
            if obj:
                obj = getattr(obj, symbol, None)
        
        if not obj:
            self.notify.warning('Loading old-style file %s' % filename)
            spfSearchPath = DSearchPath()
            spfSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$PIRATES/src/leveleditor/worldData')))
            spfSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('pirates/src/leveleditor/worldData')))
            spfSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('pirates/leveleditor/worldData')))
            spfSearchPath.appendDirectory(Filename('.'))
            pfile = Filename(filename)
            found = vfs.resolveFilename(pfile, spfSearchPath)
            data = vfs.readFile(pfile, 1)
            data = data.replace('\r', '')
            
            try:
                obj = eval(data)
            except SyntaxError:
                obj = None

        return obj

    def getObjectDataByUid(self, uid, fileDict = None):
        if fileDict is None:
            fileDict = self.fileDicts
        
        objectInfo = None
        for name in fileDict:
            fileData = fileDict[name]
            if uid not in fileData['ObjectIds']:
                continue
            
            getSyntax = 'fileData' + fileData['ObjectIds'][uid]
            try:
                objectInfo = eval(getSyntax)
            except:
                objectInfo = None
            if objectInfo is not None and ('File' not in objectInfo or objectInfo.get('File') == ''):
                break
        
        return objectInfo
    
    def getObjectDataFromFileByUid(self, uid, fileName):
        objectInfo = None
        if fileName:
            if '.py' not in fileName:
                fileName += '.py'
            
            if self.isObjectDefined(uid, fileName):
                fileData = self.fileDicts[fileName]
                getSyntax = 'fileData' + fileData['ObjectIds'][uid]
                try:
                    objectInfo = eval(getSyntax)
                except:
                    objectInfo = None

        return objectInfo

    def getFilelistByUid(self, uid, fileDict = None):
        objectInfo = None
        if not fileDict:
            fileDict = self.fileDicts
        
        fileList = set()
        for name in fileDict:
            fileData = fileDict[name]
            if uid not in fileData['ObjectIds']:
                continue
            
            getSyntax = 'fileData' + fileData['ObjectIds'][uid]
            try:
                objectInfo = eval(getSyntax)
            except:
                objectInfo = None
            if objectInfo is None:
                continue
            fileList.add(name)
            objects = objectInfo.get('Objects')
            if objects:
                for obj in list(objects.values()):
                    visual = obj.get('Visual')
                    if visual:
                        model = visual.get('Model')
                        if model:
                            if type(model) is list:
                                for currModel in model:
                                    fileList.add(currModel + '.bam')
                                
                            else:
                                fileList.add(model + '.bam')

            objects = fileData.get('Objects')
            if objects:
                for obj in list(objects.values()):
                    visual = obj.get('Visual')
                    if visual:
                        model = visual.get('Model')
                        if model:
                            fileList.add(model + '.bam')

            if 'File' not in objectInfo or objectInfo.get('File') == '':
                break
        
        return list(fileList)

    def getObjectIslandUid(self, objUid, fileDict = None):
        if not fileDict:
            fileDict = self.fileDicts
        
        found = False
        curUid = objUid
        isPrivate = False
        while curUid:
            curFile = None
            for name in fileDict:
                fileData = fileDict[name]
                if str(curUid) not in fileData['ObjectIds']:
                    continue
                
                if str(curUid) in fileData['Objects']:
                    if fileData['Objects'][str(curUid)].get('Type') == 'Island':
                        return (str(curUid), isPrivate)
                    continue
                objData = list(fileData['Objects'].values())[0]['Objects']
                if str(curUid) in objData:
                    if curUid == objUid:
                        if objData[str(curUid)].get('Private Status') == 'Private Only':
                            isPrivate = True

                    if objData[str(curUid)].get('Type') == 'Island':
                        return (str(curUid), isPrivate)

                curFile = fileData
                break
            
            if not curFile:
                return None
            else:
                curUid = list(curFile.get('Objects', {}).keys())[0]
                if curFile['Objects'][str(curUid)].get('Type') == 'Island':
                    return (curUid, isPrivate)

    def isObjectDefined(self, objUid, fileName):
        fileDict = self.fileDicts
        fileData = fileDict.get(fileName)
        if fileData and objUid in fileData['ObjectIds']:
            return True
        else:
            return False

    def isPvpIslandByUid(self, islandUid):
        if not getBase().config.GetBool('want-privateering', 1):
            return False
        
        objData = self.getObjectDataByUid(islandUid)
        return 0 if objData == None else 'PVPTeam' in objData
    
    def getPvpIslandTeam(self, islandUid):
        objData = self.getObjectDataByUid(islandUid)
        if objData is None:
            return 0
        team = objData.get('PVPTeam', 0)
        try:
            return int(team)
        except (ValueError, TypeError):
            return 0
