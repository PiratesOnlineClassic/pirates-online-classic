
from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal

class DistributedGameAreaAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGameAreaAI')

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)
        self.modelPath = ''
        self.links = []
        self.uniqueId = ''
        self.name = ''


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

    # setLinks(Link []) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setLinks(self, links):
        self.links = links

    def d_setLinks(self, links):
        self.sendUpdate('setLinks', [links])

    def b_setLinks(self, links):
        self.setLinks(links)
        self.d_setLinks(links)

    def getLinks(self):
        return self.links

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

    # setName(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    # addSpawnTriggers(triggerSphere []) broadcast ram

    def addSpawnTriggers(self, addSpawnTriggers):
        self.sendUpdate('addSpawnTriggers', [addSpawnTriggers])

    # spawnNPC(string, uint32) airecv clsend

    def spawnNPC(self, spawnNPC, todo_uint32_1):
        pass

    # requestNPCRemoval(uint32) airecv clsend

    def requestNPCRemoval(self, requestNPCRemoval):
        pass


