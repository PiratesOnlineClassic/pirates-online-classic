
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedCellDoorAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCellDoorAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.cellIndex = 0
        self.health = 0


    # setCellIndex(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setCellIndex(self, cellIndex):
        self.cellIndex = cellIndex

    def d_setCellIndex(self, cellIndex):
        self.sendUpdate('setCellIndex', [cellIndex])

    def b_setCellIndex(self, cellIndex):
        self.setCellIndex(cellIndex)
        self.d_setCellIndex(cellIndex)

    def getCellIndex(self):
        return self.cellIndex

    # setHealth(uint16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setHealth(self, health):
        self.health = health

    def d_setHealth(self, health):
        self.sendUpdate('setHealth', [health])

    def b_setHealth(self, health):
        self.setHealth(health)
        self.d_setHealth(health)

    def getHealth(self):
        return self.health

    # doorKicked() airecv clsend

    def doorKicked(self, doorKicked):
        pass


