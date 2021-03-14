import random

from direct.showbase.DirectObject import DirectObject
from direct.directnotify.DirectNotifyGlobal import directNotify

from otp.distributed.OtpDoGlobals import *

from pirates.world.WorldCreatorBase import WorldCreatorBase
from pirates.piratesbase import PiratesGlobals
from pirates.leveleditor import ObjectList
from pirates.leveleditor import WorldDataGlobals
from pirates.world import WorldGlobals
from pirates.instance.DistributedMainWorldAI import DistributedMainWorldAI
from pirates.instance.DistributedInstanceWorldAI import DistributedInstanceWorldAI
from pirates.tutorial import TutorialGlobals
from pirates.tutorial.DistributedPiratesTutorialWorldAI import DistributedPiratesTutorialWorldAI
from pirates.treasuremap.TreasureMapBlackPearlAI import TreasureMapBlackPearlAI


class LinkManager(object):

    def __init__(self, air, linkData={}):
        self.air = air
        self._linkData = linkData

    @property
    def linkData(self):
        return self._linkData

    def addLinkData(self, parentUid, linkData):
        links = self._linkData.setdefault(parentUid, [])
        links.append(linkData)

    def removeLink(self, parentUid, linkData):
        if parentUid not in self._linkData:
            return

        links = self._linkData[parentUid]
        links.remove(linkData)

    def getLinkData(self, linkUid):
        for parentUid, links in list(self._linkData.items()):
            for link in links:
                if linkUid not in link:
                    continue

                return link

        return None

    def getOtherLinkUid(self, linkUid):
        links = self.getLinkData(linkUid)
        if not links:
            return None

        if links.index(linkUid) == 0:
            return links[1]

        return links[0]

    def registerLinkData(self, uniqueId):
        fileName = self.air.worldCreator.getObjectFilenameByUid(uniqueId)
        fileData = self.air.worldCreator.openFile(fileName + '.py')

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

    @property
    def locators(self):
        return self._locators

    def addLocator(self, parentUid, uniqueId, objectData):
        locators = self._locators.setdefault(parentUid, {})
        locators[uniqueId] = Locator(parentUid, uniqueId, objectData)

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

    def getLocators(self, parentUid):
        if parentUid not in self._locators:
            return []

        return self._locators[parentUid]

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
        self._callbacks = {}

    @property
    def connectors(self):
        return self._connectors

    def hasConnector(self, parentUid, uniqueId):
        return self.getConnector(parentUid, uniqueId) is not None

    def addConnector(self, parentUid, uniqueId, objectData):
        if uniqueId in self._connectors:
            return

        connectors = self._connectors.setdefault(parentUid, {})
        connectors[uniqueId] = Connector(self.air, parentUid, uniqueId, objectData)

        if uniqueId in self._callbacks:
            self._callbacks[uniqueId]()

    def removeConnector(self, parentUid, uniqueId):
        if parentUid not in self._connectors:
            return

        if uniqueId not in self._connectors[parentUid]:
            return

        del self._connectors[parentUid][uniqueId]

    def getConnector(self, parentUid, uniqueId):
        if parentUid not in self._connectors:
            return None

        return self._connectors[parentUid].get(uniqueId)

    def addConnectorCallback(self, uniqueId, function, *args, **kwargs):
        if uniqueId in self._callbacks:
            return

        self._callbacks[uniqueId] = lambda: function(*args, **kwargs)

class MovementLinkManager(object):

    def __init__(self, air, movementLinkData={}):
        self.air = air
        self._movementLinkData = movementLinkData

    @property
    def movementLinkData(self):
        return self._movementLinkData

    def addMovementLinkData(self, parentUid, movementLinkData):
        movementLinks = self._movementLinkData.setdefault(parentUid, [])
        movementLinks.append(movementLinkData)

    def removeMovementLink(self, parentUid, movementLinkData):
        if parentUid not in self._movementLinkData:
            return

        movementLinks = self._movementLinkData[parentUid]
        movementLinks.remove(movementLinkData)

    def getMovementLinkData(self, movementLinkUid):
        for parentUid, movementLinks in list(self._movementLinkData.items()):
            for movementLink in movementLinks:
                if movementLinkUid not in movementLink:
                    continue

                return movementLink

        return None

    def movementLinkExists(self, movementLinkUid):
        return self.getMovementLinkData(movementLinkUid) != None

    def getOtherMovementLinkUid(self, movementLinkUid):
        movementLinks = self.getMovementLinkData(movementLinkUid)
        if not movementLinks:
            return None

        if movementLinks.index(movementLinkUid) == 0:
            return movementLinks[1]

        return movementLinks[0]

    def registerMovementLinkData(self, uniqueId):
        fileName = self.air.worldCreator.getObjectFilenameByUid(uniqueId)
        fileData = self.air.worldCreator.openFile(fileName + '.py')

        for movementLinkData in fileData.get(WorldDataGlobals.LINK_TYPE_AI_NODE, []):
            self.addMovementLinkData(uniqueId, movementLinkData)

    def unregisterMovementLinkData(self, uniqueId):
        movementLinks = self._movementLinkData[uniqueId]
        for movementLinkData in movementLinks:
            self.removeMovementLink(uniqueId, movementLinkData)


class OceanArea(object):

    def __init__(self, startPos, endPos, oceanName, oceanUid):
        self.startPos = startPos
        self.endPos = endPos
        self.oceanName = oceanName
        self.oceanUid = oceanUid


class OceanAreaManager(object):

    def __init__(self, air):
        self.air = air
        self.oceanAreas = {}

    def hasOceanArea(self, parentUid):
        return parentUid in self.oceanAreas

    def addOceanArea(self, parentUid, oceanArea):
        oceanAreas = self.oceanAreas.setdefault(parentUid, {})
        assert(parentUid not in oceanAreas)
        oceanAreas[oceanArea.oceanUid] = oceanArea

    def removeOceanArea(self, parentUid, oceanUid):
        oceanAreas = self.oceanAreas.get(parentUid)
        assert(parentUid is not None)
        del oceanAreas[oceanUid]

    def registerOceanAreaData(self, parentUid, worldFileName):
        fileData = self.air.worldCreator.openFile(worldFileName + '.py')
        for oceanAreaData in fileData.get(WorldDataGlobals.OCEAN_AREAS, []):
            oceanArea = OceanArea(*oceanAreaData)
            self.addOceanArea(parentUid, oceanArea)

    def unregisterOceanAreaData(self, parentUid):
        assert(parentUid in self.oceanAreas)
        del self.oceanAreas[parentUid]

    def getRandomOceanPos(self, parentUid):
        oceanArea = random.choice(self.oceanAreas[parentUid].values())
        sx, sy, sz = oceanArea.startPos
        ex, ey, ez = oceanArea.endPos
        return random.uniform(sx, ex), random.uniform(sy, ey)


class WorldCreatorAI(WorldCreatorBase, DirectObject):
    notify = directNotify.newCategory('WorldCreatorAI')
    notify.setInfo(True)

    def __init__(self, air):
        self.air = air

        self.fileDicts = {}

        self.world = None
        self.worldDict = None

        WorldCreatorBase.__init__(self, air)

        self.linkManager = LinkManager(self.air)
        self.locatorManager = LocatorManager(self.air)
        self.connectorManager = ConnectorManager(self.air)
        self.movementLinkManager = MovementLinkManager(self.air)
        self.oceanAreaManager = OceanAreaManager(self.air)

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
            if WorldGlobals.PiratesWorldSceneFileBase in fileName:
                continue

            found = self.getObjectDataFromFileByUid(objKey, fileName)
            if found:
                file = fileName
                break

        if file is not None:
            file = file.replace('.py', '')

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
            objParent = self.createWorldInstance(object, parent, parentUid, objKey, dynamic, fileName)
        else:
            newObj = self.world.builder.createObject(objType, object, parent, parentUid, objKey, dynamic, parentIsObj, fileName, actualParentObj)

        return (newObj, objParent)

    def createWorldInstance(self, objectData, parent, parentUid, objKey, dynamic, fileName=None):
        worldFileName = self.getObjectFilenameByUid(objKey)
        if not worldFileName:
            worldFileName = fileName

        worldName = objectData.get('Name', '')
        if worldFileName == WorldGlobals.PiratesTutorialSceneFileBase:
            self.world = DistributedPiratesTutorialWorldAI(self.air)
        elif worldFileName == 'BlackpearlWorld':
            self.world = TreasureMapBlackPearlAI(self.air)
        elif worldFileName == WorldGlobals.PiratesWorldSceneFileBase:
            self.world = DistributedMainWorldAI(self.air)
        elif 'Parlor' in worldFileName:
            self.world = DistributedInstanceWorldAI(self.air)
            self.world.setType(PiratesGlobals.INSTANCE_PG)
        else:
            self.world = DistributedInstanceWorldAI(self.air)

        if not parent:
            self.notify.info('Creating World Instance %s (%s) (%d)' % (worldFileName,
                self.world.__class__.__name__, self.world.getType()))

        self.world.setUniqueId(objKey)
        self.world.setName(worldName)
        self.world.setFileName(worldFileName)
        self.world.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)
        if parent is None:
            self.worldDict = objectData

        self.air.uidMgr.addUid(self.world.getUniqueId(), self.world.doId)
        self.oceanAreaManager.registerOceanAreaData(objKey, worldFileName)
        if self.oceanAreaManager.hasOceanArea(objKey):
            self.air.shipManager.startSpawnEnemyShips(self.world)

        return self.world
