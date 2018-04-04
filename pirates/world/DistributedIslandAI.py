
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from pirates.battle.Teamable import Teamable
from direct.directnotify import DirectNotifyGlobal

class DistributedIslandAI(DistributedGameAreaAI, DistributedCartesianGridAI, Teamable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedIslandAI')

    def __init__(self, air):
        DistributedGameAreaAI.__init__(self, air)
        DistributedCartesianGridAI.__init__(self, air)
        Teamable.__init__(self, air)
        self.islandTransform = [0, 0, 0, 0]
        self.zoneSphereSize = [0, 0, 0]
        self.zoneSphereCenter = [0, 0]
        self.islandModel = ''
        self.undockable = False
        self.portCollisionSpheres = []
        self.feastFireEnabled = False


    # setIslandTransform(int32/10, int32/10, int32/10, int32/10) broadcast required ram ownsend airecv
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setIslandTransform(self, islandTransform, todo_int32_10_1, todo_int32_10_2, todo_int32_10_3):
        self.islandTransform = islandTransform

    def d_setIslandTransform(self, islandTransform, todo_int32_10_1, todo_int32_10_2, todo_int32_10_3):
        self.sendUpdate('setIslandTransform', [islandTransform, todo_int32_10_1, todo_int32_10_2, todo_int32_10_3])

    def b_setIslandTransform(self, islandTransform, todo_int32_10_1, todo_int32_10_2, todo_int32_10_3):
        self.setIslandTransform(islandTransform, todo_int32_10_1, todo_int32_10_2, todo_int32_10_3)
        self.d_setIslandTransform(islandTransform, todo_int32_10_1, todo_int32_10_2, todo_int32_10_3)

    def getIslandTransform(self):
        return self.islandTransform

    # setZoneSphereSize(uint16, uint16, uint16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setZoneSphereSize(self, zoneSphereSize, todo_uint16_1, todo_uint16_2):
        self.zoneSphereSize = zoneSphereSize

    def d_setZoneSphereSize(self, zoneSphereSize, todo_uint16_1, todo_uint16_2):
        self.sendUpdate('setZoneSphereSize', [zoneSphereSize, todo_uint16_1, todo_uint16_2])

    def b_setZoneSphereSize(self, zoneSphereSize, todo_uint16_1, todo_uint16_2):
        self.setZoneSphereSize(zoneSphereSize, todo_uint16_1, todo_uint16_2)
        self.d_setZoneSphereSize(zoneSphereSize, todo_uint16_1, todo_uint16_2)

    def getZoneSphereSize(self):
        return self.zoneSphereSize

    # setZoneSphereCenter(int32, int32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setZoneSphereCenter(self, zoneSphereCenter, todo_int32_1):
        self.zoneSphereCenter = zoneSphereCenter

    def d_setZoneSphereCenter(self, zoneSphereCenter, todo_int32_1):
        self.sendUpdate('setZoneSphereCenter', [zoneSphereCenter, todo_int32_1])

    def b_setZoneSphereCenter(self, zoneSphereCenter, todo_int32_1):
        self.setZoneSphereCenter(zoneSphereCenter, todo_int32_1)
        self.d_setZoneSphereCenter(zoneSphereCenter, todo_int32_1)

    def getZoneSphereCenter(self):
        return self.zoneSphereCenter

    # setIslandModel(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setIslandModel(self, islandModel):
        self.islandModel = islandModel

    def d_setIslandModel(self, islandModel):
        self.sendUpdate('setIslandModel', [islandModel])

    def b_setIslandModel(self, islandModel):
        self.setIslandModel(islandModel)
        self.d_setIslandModel(islandModel)

    def getIslandModel(self):
        return self.islandModel

    # setUndockable(bool) required broadcast
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setUndockable(self, undockable):
        self.undockable = undockable

    def d_setUndockable(self, undockable):
        self.sendUpdate('setUndockable', [undockable])

    def b_setUndockable(self, undockable):
        self.setUndockable(undockable)
        self.d_setUndockable(undockable)

    def getUndockable(self):
        return self.undockable

    # setPortCollisionSpheres(PortCollisionSphere []) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setPortCollisionSpheres(self, portCollisionSpheres):
        self.portCollisionSpheres = portCollisionSpheres

    def d_setPortCollisionSpheres(self, portCollisionSpheres):
        self.sendUpdate('setPortCollisionSpheres', [portCollisionSpheres])

    def b_setPortCollisionSpheres(self, portCollisionSpheres):
        self.setPortCollisionSpheres(portCollisionSpheres)
        self.d_setPortCollisionSpheres(portCollisionSpheres)

    def getPortCollisionSpheres(self):
        return self.portCollisionSpheres

    # requestEntryToIsland() airecv clsend

    def requestEntryToIsland(self, requestEntryToIsland):
        pass

    # deniedEntryToIsland()

    def deniedEntryToIsland(self, deniedEntryToIsland):
        self.sendUpdate('deniedEntryToIsland', [deniedEntryToIsland])

    # setFeastFireEnabled(bool) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setFeastFireEnabled(self, feastFireEnabled):
        self.feastFireEnabled = feastFireEnabled

    def d_setFeastFireEnabled(self, feastFireEnabled):
        self.sendUpdate('setFeastFireEnabled', [feastFireEnabled])

    def b_setFeastFireEnabled(self, feastFireEnabled):
        self.setFeastFireEnabled(feastFireEnabled)
        self.d_setFeastFireEnabled(feastFireEnabled)

    def getFeastFireEnabled(self):
        return self.feastFireEnabled


