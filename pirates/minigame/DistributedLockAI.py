
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedLockAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLockAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)


    # setOpen(uint8(0-1)) broadcast ram

    def setOpen(self, open):
        self.sendUpdate('setOpen', [open])

    # requestExit() airecv clsend

    def requestExit(self, requestExit):
        pass

    # localAvatarSatDown(uint32, uint8)

    def localAvatarSatDown(self, localAvatarSatDown, todo_uint8_1):
        self.sendUpdate('localAvatarSatDown', [localAvatarSatDown, todo_uint8_1])

    # localAvatarGotUp()

    def localAvatarGotUp(self, localAvatarGotUp):
        self.sendUpdate('localAvatarGotUp', [localAvatarGotUp])

    # requestSeatResponse(uint8(0-2))

    def requestSeatResponse(self, requestSeatResponse):
        self.sendUpdate('requestSeatResponse', [requestSeatResponse])

    # lockSolved(string) broadcast

    def lockSolved(self, lockSolved):
        self.sendUpdate('lockSolved', [lockSolved])

    # d_openLock(string, uint32) airecv clsend

    def d_openLock(self, d_openLock, todo_uint32_1):
        pass


