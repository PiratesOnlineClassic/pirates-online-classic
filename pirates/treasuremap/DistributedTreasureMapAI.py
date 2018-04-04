
from pirates.uberdog.DistributedInventoryAI import DistributedInventoryAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTreasureMapAI(DistributedInventoryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTreasureMapAI')

    def __init__(self, air):
        DistributedInventoryAI.__init__(self, air)
        self.mapId = 0
        self.isEnabled = 0


    # setObjectiveIds(string []) broadcast ram

    def setObjectiveIds(self, objectiveIds):
        self.sendUpdate('setObjectiveIds', [objectiveIds])

    # setMapId(uint16) required broadcast db
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setMapId(self, mapId):
        self.mapId = mapId

    def d_setMapId(self, mapId):
        self.sendUpdate('setMapId', [mapId])

    def b_setMapId(self, mapId):
        self.setMapId(mapId)
        self.d_setMapId(mapId)

    def getMapId(self):
        return self.mapId

    # requestIsEnabled() airecv clsend

    def requestIsEnabled(self, requestIsEnabled):
        pass

    # setIsEnabled(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setIsEnabled(self, isEnabled):
        self.isEnabled = isEnabled

    def d_setIsEnabled(self, isEnabled):
        self.sendUpdate('setIsEnabled', [isEnabled])

    def b_setIsEnabled(self, isEnabled):
        self.setIsEnabled(isEnabled)
        self.d_setIsEnabled(isEnabled)

    def getIsEnabled(self):
        return self.isEnabled

    # requestStart(uint32) airecv clsend

    def requestStart(self, requestStart):
        pass


