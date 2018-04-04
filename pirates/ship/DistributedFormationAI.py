
from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from direct.directnotify import DirectNotifyGlobal

class DistributedFormationAI(DistributedSmoothNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFormationAI')

    def __init__(self, air):
        DistributedSmoothNodeAI.__init__(self, air)
        self.state = ['', 0]
        self.radius = 0


    # setState(string, int16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setState(self, state, todo_int16_1):
        self.state = state

    def d_setState(self, state, todo_int16_1):
        self.sendUpdate('setState', [state, todo_int16_1])

    def b_setState(self, state, todo_int16_1):
        self.setState(state, todo_int16_1)
        self.d_setState(state, todo_int16_1)

    def getState(self):
        return self.state

    # setRadius(uint16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setRadius(self, radius):
        self.radius = radius

    def d_setRadius(self, radius):
        self.sendUpdate('setRadius', [radius])

    def b_setRadius(self, radius):
        self.setRadius(radius)
        self.d_setRadius(radius)

    def getRadius(self):
        return self.radius


