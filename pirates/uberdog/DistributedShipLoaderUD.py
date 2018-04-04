
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class DistributedShipLoaderUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipLoaderUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)



    # rejectCreateShip(uint32)

    def rejectCreateShip(self, rejectCreateShip):
        self.sendUpdate('rejectCreateShip', [rejectCreateShip])

    # createShipResponse(uint32, uint32, uint32)

    def createShipResponse(self, createShipResponse, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('createShipResponse', [createShipResponse, todo_uint32_1, todo_uint32_2])


    # rejectCreateShippart(uint32)

    def rejectCreateShippart(self, rejectCreateShippart):
        self.sendUpdate('rejectCreateShippart', [rejectCreateShippart])

    # createShippartResponse(uint32, uint32, uint32)

    def createShippartResponse(self, createShippartResponse, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('createShippartResponse', [createShippartResponse, todo_uint32_1, todo_uint32_2])

    # loadShipResponse(uint32, uint32)

    def loadShipResponse(self, loadShipResponse, todo_uint32_1):
        self.sendUpdate('loadShipResponse', [loadShipResponse, todo_uint32_1])


    # rejectLoadOwnerview(uint32)

    def rejectLoadOwnerview(self, rejectLoadOwnerview):
        self.sendUpdate('rejectLoadOwnerview', [rejectLoadOwnerview])

    # loadOwnerviewResponse(uint32, uint32)

    def loadOwnerviewResponse(self, loadOwnerviewResponse, todo_uint32_1):
        self.sendUpdate('loadOwnerviewResponse', [loadOwnerviewResponse, todo_uint32_1])


    # rejectDeleteOwnerview(uint32)

    def rejectDeleteOwnerview(self, rejectDeleteOwnerview):
        self.sendUpdate('rejectDeleteOwnerview', [rejectDeleteOwnerview])

    # deleteOwnerviewResponse(uint32, uint32)

    def deleteOwnerviewResponse(self, deleteOwnerviewResponse, todo_uint32_1):
        self.sendUpdate('deleteOwnerviewResponse', [deleteOwnerviewResponse, todo_uint32_1])


