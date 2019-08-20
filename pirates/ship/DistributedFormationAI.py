from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from direct.directnotify import DirectNotifyGlobal


class DistributedFormationAI(DistributedSmoothNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFormationAI')

    def __init__(self, air):
        DistributedSmoothNodeAI.__init__(self, air)

        self.state = ['', 0]
        self.radius = 0

    def setState(self, stateName, timeStamp):
        self.state = [stateName, timeStamp]

    def d_setState(self, stateName, timeStamp):
        self.sendUpdate('setState', [stateName, timeStamp])

    def b_setState(self, stateName, timeStamp):
        self.setState(stateName, timeStamp)
        self.d_setState(stateName, timeStamp)

    def getState(self):
        return self.state

    def setRadius(self, radius):
        self.radius = radius

    def d_setRadius(self, radius):
        self.sendUpdate('setRadius', [radius])

    def b_setRadius(self, radius):
        self.setRadius(radius)
        self.d_setRadius(radius)

    def getRadius(self):
        return self.radius
