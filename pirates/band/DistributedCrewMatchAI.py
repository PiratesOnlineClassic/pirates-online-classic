
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedCrewMatchAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCrewMatchAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # requestCrewAdd(uint8, uint8, uint8) airecv clsend

    def requestCrewAdd(self, requestCrewAdd, todo_uint8_1, todo_uint8_2):
        pass

    # responseCrewAdd(int8)

    def responseCrewAdd(self, responseCrewAdd):
        self.sendUpdate('responseCrewAdd', [responseCrewAdd])

    # requestCrewDelete() airecv clsend

    def requestCrewDelete(self, requestCrewDelete):
        pass

    # responseCrewDelete(uint8)

    def responseCrewDelete(self, responseCrewDelete):
        self.sendUpdate('responseCrewDelete', [responseCrewDelete])

    # requestInitialAvatarAdd(uint8) airecv clsend

    def requestInitialAvatarAdd(self, requestInitialAvatarAdd):
        pass

    # responseInitialAvatarAdd(uint8, string, string, uint8)

    def responseInitialAvatarAdd(self, responseInitialAvatarAdd, todo_string_1, todo_string_2, todo_uint8_3):
        self.sendUpdate('responseInitialAvatarAdd', [responseInitialAvatarAdd, todo_string_1, todo_string_2, todo_uint8_3])

    # requestInitialAvatarAddResponse(uint8, uint8) airecv clsend

    def requestInitialAvatarAddResponse(self, requestInitialAvatarAddResponse, todo_uint8_1):
        pass

    # responseInitialAvatarAddResponse(uint8)

    def responseInitialAvatarAddResponse(self, responseInitialAvatarAddResponse):
        self.sendUpdate('responseInitialAvatarAddResponse', [responseInitialAvatarAddResponse])

    # requestPutAvatarOnLookoutList(uint8) airecv clsend

    def requestPutAvatarOnLookoutList(self, requestPutAvatarOnLookoutList):
        pass

    # requestdeleteAvatarFromLookoutList() airecv clsend

    def requestdeleteAvatarFromLookoutList(self, requestdeleteAvatarFromLookoutList):
        pass

    # responseCrewFound(string, uint32, string)

    def responseCrewFound(self, responseCrewFound, todo_uint32_1, todo_string_2):
        self.sendUpdate('responseCrewFound', [responseCrewFound, todo_uint32_1, todo_string_2])

    # requestAcceptInvite(uint32) airecv clsend

    def requestAcceptInvite(self, requestAcceptInvite):
        pass

    # requestCrewOfOneCreation() airecv clsend

    def requestCrewOfOneCreation(self, requestCrewOfOneCreation):
        pass

    # requestCrewOfOneDelete() airecv clsend

    def requestCrewOfOneDelete(self, requestCrewOfOneDelete):
        pass

    # notifySponsorNewMember(string)

    def notifySponsorNewMember(self, notifySponsorNewMember):
        self.sendUpdate('notifySponsorNewMember', [notifySponsorNewMember])


