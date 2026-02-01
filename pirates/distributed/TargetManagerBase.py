class TargetManagerBase:
    
    def __init__(self):
        self.objectDict = {}

    def delete(self):
        del self.objectDict

    def getUniqueId(self, obj):
        return obj.get_key()

    def addTarget(self, nodePathId, obj):
        self.objectDict[nodePathId] = obj

    def removeTarget(self, nodePathId):
        if nodePathId in self.objectDict:
            del self.objectDict[nodePathId]

    def getObjectFromNodepath(self, nodePath):
        return self.objectDict.get(nodePath.get_key(), None)


