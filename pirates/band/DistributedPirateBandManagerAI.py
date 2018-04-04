
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPirateBandManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPirateBandManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # requestInvite(uint32) airecv clsend

    def requestInvite(self, requestInvite):
        pass

    # requestCancel(uint32) airecv clsend

    def requestCancel(self, requestCancel):
        pass

    # requestOutCome(uint32, uint8)

    def requestOutCome(self, requestOutCome, todo_uint8_1):
        self.sendUpdate('requestOutCome', [requestOutCome, todo_uint8_1])

    # invitationFrom(uint32, string)

    def invitationFrom(self, invitationFrom, todo_string_1):
        self.sendUpdate('invitationFrom', [invitationFrom, todo_string_1])

    # invitationCancel(uint32)

    def invitationCancel(self, invitationCancel):
        self.sendUpdate('invitationCancel', [invitationCancel])

    # invitationResponce(uint32, uint8) airecv clsend

    def invitationResponce(self, invitationResponce, todo_uint8_1):
        pass

    # requestRemove(uint32) airecv clsend

    def requestRemove(self, requestRemove):
        pass

    # requestCrewIconUpdate(uint8) airecv clsend

    def requestCrewIconUpdate(self, requestCrewIconUpdate):
        pass

    # receiveUpdatedCrewIcon(uint8)

    def receiveUpdatedCrewIcon(self, receiveUpdatedCrewIcon):
        self.sendUpdate('receiveUpdatedCrewIcon', [receiveUpdatedCrewIcon])


