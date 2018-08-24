from direct.showbase.DirectObject import DirectObject
from direct.directnotify.DirectNotifyGlobal import directNotify

from otp.distributed.OtpDoGlobals import *

from pirates.world.WorldCreatorBase import WorldCreatorBase
from pirates.piratesbase import PiratesGlobals
from pirates.leveleditor import ObjectList
from pirates.leveleditor import WorldDataGlobals
from pirates.world import WorldGlobals
from pirates.instance.DistributedMainWorldAI import DistributedMainWorldAI
from pirates.tutorial import TutorialGlobals
from pirates.tutorial.DistributedPiratesTutorialWorldAI import DistributedPiratesTutorialWorldAI


class LinkManager(object):

    def __init__(self, air, linkData={}):
        self.air = air
        self._linkData = linkData

    def addLinkData(self, parentUid, linkData):
        links = self._linkData.setdefault(parentUid, [])
        if linkData in links:
            return

        links.append(linkData)

    def removeLink(self, parentUid, linkData):
        if parentUid not in self._linkData:
            return None

        links = self._linkData[parentUid]
        if linkData not in links:
            return

        links.remove(linkData)

    def getLinkData(self, linkUid):
        for parentUid in self._linkData:
            for linkData in self._linkData[parentUid]:
                if linkUid in linkData:
                    return linkData

        return None

    def getOtherLinkUid(self, linkUid):
        links = self.getLinkData(linkUid)
        if not links:
            return None

        if links.index(linkUid) == 0:
            return links[1]

        return links[0]

    def registerLinkData(self, uniqueId):
        filename = self.air.worldCreator.getObjectFilenameByUid(uniqueId)
        fileData = self.air.worldCreator.openFile(filename)

        for linkData in fileData.get(WorldDataGlobals.LINK_TYPE_LOC_NODE, []):
            self.addLinkData(uniqueId, linkData)

    def unregisterLinkData(self, uniqueId):
        links = self._linkData[uniqueId]
        for linkData in links:
            self.removeLink(uniqueId, linkData)

class Locator(object):

    def __init__(self, parentUid, uniqueId, objectData):
        self._parentUid = parentUid
        self._uniqueId = uniqueId
        self._objectData = objectData

    @property
    def parentUid(self):
        return self._parentUid

    @property
    def uniqueId(self):
        return self._uniqueId

    @property
    def objectData(self):
        return self._objectData

class LocatorManager(object):

    def __init__(self, air, locators={}):
        self.air = air
        self._locators = locators
        self._callbacks = {}

    def addLocator(self, parentUid, uniqueId, objectData):
        locators = self._locators.setdefault(parentUid, {})
        if uniqueId in locators:
            return

        locator = Locator(parentUid, uniqueId, objectData)
        locators[uniqueId] = locator

        if uniqueId in self._callbacks:
            self._callbacks[uniqueId]()

    def removeLocator(self, parentUid, uniqueId):
        locators = self._locators.setdefault(parentUid, {})
        if uniqueId not in locators:
            return

        del locators[uniqueId]

    def getLocator(self, uniqueId):
        for parentUid, locators in self._locators.iteritems():
            if uniqueId in locators:
                return locators[uniqueId]

        return None

    def addLocatorCallback(self, uniqueId, function, *args, **kwargs):
        if uniqueId in self._callbacks:
            return

        self._callbacks[uniqueId] = lambda: function(*args, **kwargs)

class Connector(LocatorManager):

    def __init__(self, air, parentUid, uniqueId, objectData):
        LocatorManager.__init__(self, air)

        self._parentUid = parentUid
        self._uniqueId = uniqueId
        self._objectData = objectData

    @property
    def parentUid(self):
        return self._parentUid

    @property
    def uniqueId(self):
        return self._uniqueId

    @property
    def objectData(self):
        return self._objectData

class ConnectorManager(object):

    def __init__(self, air, connectors={}):
        self.air = air
        self._connectors = connectors

    def addConnector(self, parentUid, uniqueId, objectData):
        if uniqueId in self._connectors:
            return

        connector = Connector(self.air, parentUid,
            uniqueId, objectData)

        self._connectors[uniqueId] = connector

    def removeConnector(self, uniqueId):
        if uniqueId not in self._connectors:
            return

        del self._connectors[uniqueId]

    def getConnector(self, uniqueId):
        return self._connectors.get(uniqueId)

class WorldCreatorAI(WorldCreatorBase, DirectObject):
    notify = directNotify.newCategory('WorldCreatorAI')

    def __init__(self, air):
        self.air = air

        self.fileDicts = {}

        self.world = None
        self.worldDict = None

        WorldCreatorBase.__init__(self, air)

        self.linkManager = LinkManager(self.air)
        self.locatorManager = LocatorManager(self.air)
        self.connectorManager = ConnectorManager(self.air)

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

        if worldName == 'default':
            self.world = DistributedMainWorldAI(self.air)
        elif worldName == WorldGlobals.PiratesTutorialSceneFileBase:
            self.world = DistributedPiratesTutorialWorldAI(self.air)
        else:
            self.notify.warning('Failed to create world instance with unknown name: %s!' % (
                worldName))

            return

        self.world.setUniqueId(objKey)
        self.world.setName(worldName)
        self.world.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.worldDict = objectData
        self.air.uidMgr.addUid(self.world.getUniqueId(), self.world.doId)
        return self.world
