
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedSearchableContainerAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSearchableContainerAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.searchTime = 0
        self.type = ''
        self.scale = [0, 0, 0]
        self.containerColor = [0, 0, 0, 0]
        self.sphereScale = 0


    # setSearchTime(uint16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setSearchTime(self, searchTime):
        self.searchTime = searchTime

    def d_setSearchTime(self, searchTime):
        self.sendUpdate('setSearchTime', [searchTime])

    def b_setSearchTime(self, searchTime):
        self.setSearchTime(searchTime)
        self.d_setSearchTime(searchTime)

    def getSearchTime(self):
        return self.searchTime

    # setType(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setType(self, type):
        self.type = type

    def d_setType(self, type):
        self.sendUpdate('setType', [type])

    def b_setType(self, type):
        self.setType(type)
        self.d_setType(type)

    def getType(self):
        return self.type

    # setScale(int16/10, int16/10, int16/10) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setScale(self, scale, todo_int16_10_1, todo_int16_10_2):
        self.scale = scale

    def d_setScale(self, scale, todo_int16_10_1, todo_int16_10_2):
        self.sendUpdate('setScale', [scale, todo_int16_10_1, todo_int16_10_2])

    def b_setScale(self, scale, todo_int16_10_1, todo_int16_10_2):
        self.setScale(scale, todo_int16_10_1, todo_int16_10_2)
        self.d_setScale(scale, todo_int16_10_1, todo_int16_10_2)

    def getScale(self):
        return self.scale

    # setContainerColor(int16/10, int16/10, int16/10, int16/10) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setContainerColor(self, containerColor, todo_int16_10_1, todo_int16_10_2, todo_int16_10_3):
        self.containerColor = containerColor

    def d_setContainerColor(self, containerColor, todo_int16_10_1, todo_int16_10_2, todo_int16_10_3):
        self.sendUpdate('setContainerColor', [containerColor, todo_int16_10_1, todo_int16_10_2, todo_int16_10_3])

    def b_setContainerColor(self, containerColor, todo_int16_10_1, todo_int16_10_2, todo_int16_10_3):
        self.setContainerColor(containerColor, todo_int16_10_1, todo_int16_10_2, todo_int16_10_3)
        self.d_setContainerColor(containerColor, todo_int16_10_1, todo_int16_10_2, todo_int16_10_3)

    def getContainerColor(self):
        return self.containerColor

    # setSphereScale(int16/10) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setSphereScale(self, sphereScale):
        self.sphereScale = sphereScale

    def d_setSphereScale(self, sphereScale):
        self.sendUpdate('setSphereScale', [sphereScale])

    def b_setSphereScale(self, sphereScale):
        self.setSphereScale(sphereScale)
        self.d_setSphereScale(sphereScale)

    def getSphereScale(self):
        return self.sphereScale

    # startSearching()

    def startSearching(self, startSearching):
        self.sendUpdate('startSearching', [startSearching])

    # stopSearching(uint16)

    def stopSearching(self, stopSearching):
        self.sendUpdate('stopSearching', [stopSearching])


