from direct.task import Task

class TextureFlattenManager:
    
    def __init__(self):
        self.splattableObjects = {}
        self.sailObjects = {}
        taskMgr.add(self.flattenTask, 'multitexFlatten', priority = 45)

    def delete(self):
        taskMgr.remove('multitexFlatten')
        self.splattableObjects.clear()
    
    def addSplattable(self, obj, panelIndex):
        holeCount = self.splattableObjects.get((obj, panelIndex), 0)
        holeCount += 1
        self.splattableObjects[(obj, panelIndex)] = holeCount
        return holeCount
    
    def clearSplattables(self, objToClear):
        self.splattabeObjects = dict([x for x in self.splattableObjects if x[0] != objToClear])

    def addSail(self, obj):
        holeCount = self.sailObjects.get(obj, 0)
        holeCount += 1
        self.sailObjects[obj] = holeCount
        return holeCount
    
    def clearSail(self, objToClear):
        if self.sailObjects.get(objToClear):
            del self.sailObjects[objToClear]
    
    def flattenTask(self, task):
        for (obj, panelIndex) in self.splattableObjects:
            if panelIndex >= len(obj.panelsMed):
                continue
            
            panel = obj.panelsMed[panelIndex]
            attribList = obj.cutGeomTextureStates(panel.node())
            panel.flattenMultitex(useGeom = 0, target = obj.holeLayer)
            holeTex = panel.findTexture(obj.holeLayer)
            obj.pasteGeomTextureStates(panel.node(), attribList)
            panel.setTexture(obj.holeLayer, holeTex)
            obj.panelsHigh[panelIndex].setTexture(obj.holeLayer, holeTex)
        
        self.splattableObjects.clear()
        for sail in self.sailObjects:
            attribList = sail.cutGeomTextureStates(sail.sailGeom.node())
            sail.sailGeom.flattenMultitex(useGeom = 0, target = sail.holeLayer)
            holeTex = sail.sailGeom.findTexture(sail.holeLayer)
            sail.pasteGeomTextureStates(sail.sailGeom.node(), attribList)
            sail.sailGeom.setTexture(sail.holeLayer, holeTex)
        
        self.sailObjects.clear()
        return Task.cont


