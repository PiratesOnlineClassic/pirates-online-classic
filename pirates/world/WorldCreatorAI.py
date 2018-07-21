from direct.showbase.DirectObject import DirectObject
from direct.directnotify.DirectNotifyGlobal import directNotify

from pirates.world.WorldCreatorBase import WorldCreatorBase
from pirates.piratesbase import PiratesGlobals
from pirates.leveleditor import ObjectList
from pirates.world import WorldGlobals
from pirates.instance.DistributedMainWorldAI import DistributedMainWorldAI
from pirates.tutorial import TutorialGlobals
from pirates.tutorial.DistributedPiratesTutorialWorldAI import DistributedPiratesTutorialWorldAI


class WorldCreatorAI(WorldCreatorBase, DirectObject):
    notify = directNotify.newCategory('WorldCreatorAI')

    def __init__(self, air):
        self.air = air

        self.fileDicts = {}

        self.world = None
        self.worldDict = None

        WorldCreatorBase.__init__(self, air)

    @classmethod
    def isObjectInCurrentGamePhase(cls, object):
        return True

    def loadFileDataRecursive(self, file):
        fileDict = self.openFile(file)
        objects = fileDict.get('Objects')
        if objects:
            self.rFindFile(objects)

        self.fileDicts[file] = fileDict

    def rFindFile(self, objSet):
        for obj in objSet.values():
            fileName = obj.get('File')
            if fileName:
                self.loadFileDataRecursive(fileName + '.py')

            objects = obj.get('Objects')
            if objects:
                self.rFindFile(objects)

    def getModelPathFromFile(self, file):
        fileDict = self.openFile(file + '.py')
        return fileDict['Objects'].values()[0]['Visual']['Model']

    def loadObjectsFromFile(self, filename, parent=None, zoneLevel=0, startTime=None, parentIsObj=False):
        # load the object data recursive into the file dictionary,
        # so we have the file data and files before any object is created...
        self.loadFileDataRecursive(filename)

        # now load the objects from the file in which will utilize the data
        # stored from other files as seem above...
        return WorldCreatorBase.loadObjectsFromFile(self, filename, parent, zoneLevel,
            startTime, parentIsObj)

    def getObjectParentUid(self, objKey):
        found = None
        for fileName in self.fileDicts.keys():
            found = self.getObjectDataFromFileByUid(objKey, fileName)
            if found:
                break

        return found

    def getObjectFilenameByUid(self, objKey, getParentUid=True):
        file = None
        for fileName in self.fileDicts.keys():
            found = self.getObjectDataFromFileByUid(objKey, fileName)
            if found:
                file = fileName
                break

        return file

    def getIslandWorldDataByUid(self, uid):
        return self.worldDict['Objects'].get(uid, None)

    def createObject(self, object, parent, parentUid, objKey, dynamic, zoneLevel=0, startTime=None, parentIsObj=False, fileName=None, actualParentObj=None):
        objType = WorldCreatorBase.createObject(self, object, parent, parentUid, objKey, dynamic, zoneLevel,
            startTime, parentIsObj, fileName, actualParentObj)

        if not objType:
            return (None, None)

        newObj = None
        objParent = None

        if objType == ObjectList.AREA_TYPE_WORLD_REGION:
            objParent = self.__createWorldInstance(object, parent, parentUid, objKey, dynamic)
        else:
            newObj = self.world.builder.createObject(objType, object, parent, parentUid, objKey, dynamic,
                parentIsObj, fileName, actualParentObj)

        return (newObj, objParent)

    def __createWorldInstance(self, objectData, parent, parentUid, objKey, dynamic):
        worldName = objectData['Name']

        if worldName == WorldGlobals.PiratesTutorialSceneFileBase:
            self.world = DistributedPiratesTutorialWorldAI(self.air)
        else:
            self.world = DistributedMainWorldAI(self.air)

        self.world.setUniqueId(objKey)
        self.world.setName(worldName)
        self.world.generateWithRequired(PiratesGlobals.InstanceUberZone)

        self.worldDict = objectData
        self.air.uidMgr.addUid(self.world.getUniqueId(), self.world.doId)

        return self.world
