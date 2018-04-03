# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.shipparts.TextureFlattenManager
from direct.task import Task

class TextureFlattenManager:
    __module__ = __name__

    def __init__(self):
        self.splattableObjects = {}
        self.sailObjects = {}
        taskMgr.add(self.flattenTask, 'multitexFlatten', priority=45)

    def delete(self):
        taskMgr.remove('multitexFlatten')
        self.splattableObjects.clear()

    def addSplattable(self, obj, panelIndex):
        holeCount = self.splattableObjects.get((obj, panelIndex), 0)
        holeCount += 1
        self.splattableObjects[(obj, panelIndex)] = holeCount
        return holeCount

    def clearSplattables(self, objToClear):
        self.splattabeObjects = dict(filter(lambda x: x[0] != objToClear, self.splattableObjects))

    def addSail(self, obj):
        holeCount = self.sailObjects.get(obj, 0)
        holeCount += 1
        self.sailObjects[obj] = holeCount
        return holeCount

    def clearSail(self, objToClear):
        if self.sailObjects.get(objToClear):
            del self.sailObjects[objToClear]

    def flattenTask(self, task):
        for obj, panelIndex in self.splattableObjects:
            if panelIndex >= len(obj.panelsMed):
                continue
            panel = obj.panelsMed[panelIndex]
            attribList = obj.cutGeomTextureStates(panel.node())
            panel.flattenMultitex(useGeom=0, target=obj.holeLayer)
            holeTex = panel.findTexture(obj.holeLayer)
            obj.pasteGeomTextureStates(panel.node(), attribList)
            panel.setTexture(obj.holeLayer, holeTex)
            obj.panelsHigh[panelIndex].setTexture(obj.holeLayer, holeTex)

        self.splattableObjects.clear()
        for sail in self.sailObjects:
            attribList = sail.cutGeomTextureStates(sail.sailGeom.node())
            sail.sailGeom.flattenMultitex(useGeom=0, target=sail.holeLayer)
            holeTex = sail.sailGeom.findTexture(sail.holeLayer)
            sail.pasteGeomTextureStates(sail.sailGeom.node(), attribList)
            sail.sailGeom.setTexture(sail.holeLayer, holeTex)

        self.sailObjects.clear()
        return Task.cont
# okay decompiling .\pirates\shipparts\TextureFlattenManager.pyc
