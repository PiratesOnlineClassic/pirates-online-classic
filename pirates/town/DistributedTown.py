# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.town.DistributedTown
import random
import re
import types

from direct.actor import *
from direct.distributed import DistributedCartesianGrid
from pirates.piratesbase import PiratesGlobals
from pirates.world import ClientArea, DistributedGameArea, WorldGlobals


class DistributedTown(DistributedGameArea.DistributedGameArea, DistributedCartesianGrid.DistributedCartesianGrid, ClientArea.ClientArea):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedTown')

    def __init__(self, cr):
        DistributedGameArea.DistributedGameArea.__init__(self, cr)
        DistributedCartesianGrid.DistributedCartesianGrid.__init__(self, cr)
        ClientArea.ClientArea.__init__(self)
        self.__townGeomLoaded = 0
        self.geom = None
        self.uniqueId = ''
        self.name = 'Town Name'
        self.childens = []
        return

    def announceGenerate(self):
        DistributedGameArea.DistributedGameArea.announceGenerate(self)
        self.loadTownGeom()
        self.setName(self.name)
        self.cr.uidMgr.addUid(self.uniqueId, self.getDoId())

    def disable(self):
        DistributedGameArea.DistributedGameArea.disable(self)

    def delete(self):
        DistributedGameArea.DistributedGameArea.delete(self)
        DistributedCartesianGrid.DistributedCartesianGrid.delete(self)
        ClientArea.ClientArea.delete(self)
        self.removeNode()

    def setUniqueId(self, uid):
        if self.uniqueId != '':
            self.cr.uidMgr.removeUid(self.uniqueId)
        self.uniqueId = uid

    def getUniqueId(self):
        return self.uniqueId

    def setModelPath(self, modelPath):
        self.notify.debug('setModelPath %s' % modelPath)
        self.modelPath = modelPath

    def loadTownGeom(self):
        if self.__townGeomLoaded:
            return
        self.geom = None
        self.__townGeomLoaded = 1
        return

    def unloadTownGeom(self):
        self.allDetails.stash()

    def addPropFromFile(self, propData):
        objNode = None
        objModel = None
        if 'SubObjs' in propData:
            objNode = self.loadSubModels(propData)
        else:
            objModel = loader.loadModelCopy(propData['Visual']['Model'])
        if objModel == None and objNode == None:
            self.notify.warning('No model named %s' % propData['Visual']['Model'])
            return
        objNodeName = 'Prop' + propData['Type']
        if objNode == None:
            objNode = self.attachNewNode(objNodeName)
        else:
            objNode.reparentTo(self)
        self.childens.append(objNode)
        if objModel:
            objModel.reparentTo(objNode)
        objNode.setPos(propData['Pos'])
        objNode.setHpr(propData['Hpr'])
        if 'Scale' in propData:
            objNode.setScale(propData['Scale'])
        if 'Color' in propData['Visual']:
            objNode.setColorScale(*propData['Visual']['Color'])
        objNode.flattenStrong()
        wallGeom = objNode.find('**/wall*_n_window*')
        roofGeom = objNode.find('**/roof')
        for c in [wallGeom, roofGeom]:
            if not c.isEmpty():
                self.setupCannonballBldgColl(c, PiratesGlobals.TargetBitmask)
                c.wrtReparentTo(self.highDetailBldgNp)
                c.flattenLight()

        return
# okay decompiling .\pirates\town\DistributedTown.pyc
