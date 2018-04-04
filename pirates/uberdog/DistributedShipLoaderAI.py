
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedShipLoaderAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipLoaderAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # requestCreateShip(uint32, uint8, string, string, uint32) airecv clsend

    def requestCreateShip(self, requestCreateShip, todo_uint8_1, todo_string_2, todo_string_3, todo_uint32_4):
        pass

    # rejectCreateShip(uint32)

    def rejectCreateShip(self, rejectCreateShip):
        self.sendUpdate('rejectCreateShip', [rejectCreateShip])

    # createShipResponse(uint32, uint32, uint32)

    def createShipResponse(self, createShipResponse, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('createShipResponse', [createShipResponse, todo_uint32_1, todo_uint32_2])

    # requestCreateShippart(uint32, uint8, uint8, uint8, uint32) airecv clsend

    def requestCreateShippart(self, requestCreateShippart, todo_uint8_1, todo_uint8_2, todo_uint8_3, todo_uint32_4):
        pass

    # rejectCreateShippart(uint32)

    def rejectCreateShippart(self, rejectCreateShippart):
        self.sendUpdate('rejectCreateShippart', [rejectCreateShippart])

    # createShippartResponse(uint32, uint32, uint32)

    def createShippartResponse(self, createShippartResponse, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('createShippartResponse', [createShippartResponse, todo_uint32_1, todo_uint32_2])

    # loadShipResponse(uint32, uint32)

    def loadShipResponse(self, loadShipResponse, todo_uint32_1):
        self.sendUpdate('loadShipResponse', [loadShipResponse, todo_uint32_1])

    # requestLoadOwnerview(uint32, uint32, uint32) airecv clsend

    def requestLoadOwnerview(self, requestLoadOwnerview, todo_uint32_1, todo_uint32_2):
        pass

    # rejectLoadOwnerview(uint32)

    def rejectLoadOwnerview(self, rejectLoadOwnerview):
        self.sendUpdate('rejectLoadOwnerview', [rejectLoadOwnerview])

    # loadOwnerviewResponse(uint32, uint32)

    def loadOwnerviewResponse(self, loadOwnerviewResponse, todo_uint32_1):
        self.sendUpdate('loadOwnerviewResponse', [loadOwnerviewResponse, todo_uint32_1])

    # requestDeleteOwnerview(uint32, uint32, uint32) airecv clsend

    def requestDeleteOwnerview(self, requestDeleteOwnerview, todo_uint32_1, todo_uint32_2):
        pass

    # rejectDeleteOwnerview(uint32)

    def rejectDeleteOwnerview(self, rejectDeleteOwnerview):
        self.sendUpdate('rejectDeleteOwnerview', [rejectDeleteOwnerview])

    # deleteOwnerviewResponse(uint32, uint32)

    def deleteOwnerviewResponse(self, deleteOwnerviewResponse, todo_uint32_1):
        self.sendUpdate('deleteOwnerviewResponse', [deleteOwnerviewResponse, todo_uint32_1])


