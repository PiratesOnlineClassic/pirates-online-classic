
from pirates.world.DistributedDoorBaseAI import DistributedDoorBaseAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBuildingDoorAI(DistributedDoorBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuildingDoorAI')

    def __init__(self, air):
        DistributedDoorBaseAI.__init__(self, air)
        self.interiorId = [0, '', 0, 0]


    # setInteriorId(uint32, string, uint32, uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setInteriorId(self, interiorId, todo_string_1, todo_uint32_2, todo_uint32_3):
        self.interiorId = interiorId

    def d_setInteriorId(self, interiorId, todo_string_1, todo_uint32_2, todo_uint32_3):
        self.sendUpdate('setInteriorId', [interiorId, todo_string_1, todo_uint32_2, todo_uint32_3])

    def b_setInteriorId(self, interiorId, todo_string_1, todo_uint32_2, todo_uint32_3):
        self.setInteriorId(interiorId, todo_string_1, todo_uint32_2, todo_uint32_3)
        self.d_setInteriorId(interiorId, todo_string_1, todo_uint32_2, todo_uint32_3)

    def getInteriorId(self):
        return self.interiorId

    # requestPrivateInteriorInstance() airecv clsend

    def requestPrivateInteriorInstance(self, requestPrivateInteriorInstance):
        pass

    # setPrivateInteriorInstance(uint32, uint32, uint32, bool)

    def setPrivateInteriorInstance(self, privateInteriorInstance, todo_uint32_1, todo_uint32_2, todo_bool_3):
        self.sendUpdate('setPrivateInteriorInstance', [privateInteriorInstance, todo_uint32_1, todo_uint32_2, todo_bool_3])


