
from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal

class DistributedGAConnectorAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGAConnectorAI')

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)
        self.modelPath = ''
        self.uniqueId = ''


    # setModelPath(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def d_setModelPath(self, modelPath):
        self.sendUpdate('setModelPath', [modelPath])

    def b_setModelPath(self, modelPath):
        self.setModelPath(modelPath)
        self.d_setModelPath(modelPath)

    def getModelPath(self):
        return self.modelPath

    # setLinks(uint8, string, Link []) broadcast ram

    def setLinks(self, links, todo_string_1, todo_Link_2):
        self.sendUpdate('setLinks', [links, todo_string_1, todo_Link_2])

    # setUniqueId(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def d_setUniqueId(self, uniqueId):
        self.sendUpdate('setUniqueId', [uniqueId])

    def b_setUniqueId(self, uniqueId):
        self.setUniqueId(uniqueId)
        self.d_setUniqueId(uniqueId)

    def getUniqueId(self):
        return self.uniqueId

    # requestPrivateArea(uint32) airecv clsend

    def requestPrivateArea(self, requestPrivateArea):
        pass

    # setPrivateArea(uint32, uint32, uint32, bool) airecv clsend

    def setPrivateArea(self, privateArea, todo_uint32_1, todo_uint32_2, todo_bool_3):
        pass


