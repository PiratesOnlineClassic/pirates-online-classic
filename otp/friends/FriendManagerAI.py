
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class FriendManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # friendQuery(int32) airecv clsend

    def friendQuery(self, friendQuery):
        pass

    # cancelFriendQuery(int32) airecv clsend

    def cancelFriendQuery(self, cancelFriendQuery):
        pass

    # inviteeFriendConsidering(int8, int32) airecv clsend

    def inviteeFriendConsidering(self, inviteeFriendConsidering, todo_int32_1):
        pass

    # inviteeFriendResponse(int8, int32) airecv clsend

    def inviteeFriendResponse(self, inviteeFriendResponse, todo_int32_1):
        pass

    # inviteeAcknowledgeCancel(int32) airecv clsend

    def inviteeAcknowledgeCancel(self, inviteeAcknowledgeCancel):
        pass

    # friendConsidering(int8, int32)

    def friendConsidering(self, friendConsidering, todo_int32_1):
        self.sendUpdate('friendConsidering', [friendConsidering, todo_int32_1])

    # friendResponse(int8, int32)

    def friendResponse(self, friendResponse, todo_int32_1):
        self.sendUpdate('friendResponse', [friendResponse, todo_int32_1])

    # inviteeFriendQuery(int32, string, blob, int32)

    def inviteeFriendQuery(self, inviteeFriendQuery, todo_string_1, todo_blob_2, todo_int32_3):
        self.sendUpdate('inviteeFriendQuery', [inviteeFriendQuery, todo_string_1, todo_blob_2, todo_int32_3])

    # inviteeCancelFriendQuery(int32)

    def inviteeCancelFriendQuery(self, inviteeCancelFriendQuery):
        self.sendUpdate('inviteeCancelFriendQuery', [inviteeCancelFriendQuery])

    # requestSecret() airecv clsend

    def requestSecret(self, requestSecret):
        pass

    # requestSecretResponse(int8, string)

    def requestSecretResponse(self, requestSecretResponse, todo_string_1):
        self.sendUpdate('requestSecretResponse', [requestSecretResponse, todo_string_1])

    # submitSecret(string) airecv clsend

    def submitSecret(self, submitSecret):
        pass

    # submitSecretResponse(int8, int32)

    def submitSecretResponse(self, submitSecretResponse, todo_int32_1):
        self.sendUpdate('submitSecretResponse', [submitSecretResponse, todo_int32_1])


