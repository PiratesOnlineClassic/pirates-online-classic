
from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from pirates.distributed.DistributedTargetableObjectAI import DistributedTargetableObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedMovingObjectAI(DistributedSmoothNodeAI, DistributedTargetableObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMovingObjectAI')

    def __init__(self, air):
        DistributedSmoothNodeAI.__init__(self, air)
        DistributedTargetableObjectAI.__init__(self, air)
        self.maxSpeed = 0
        self.startState = ''
        self.aggroRadius = 0
        self.aggroMode = 0


    # setMaxSpeed(uint16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setMaxSpeed(self, maxSpeed):
        self.maxSpeed = maxSpeed

    def d_setMaxSpeed(self, maxSpeed):
        self.sendUpdate('setMaxSpeed', [maxSpeed])

    def b_setMaxSpeed(self, maxSpeed):
        self.setMaxSpeed(maxSpeed)
        self.d_setMaxSpeed(maxSpeed)

    def getMaxSpeed(self):
        return self.maxSpeed

    # setStartState(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setStartState(self, startState):
        self.startState = startState

    def d_setStartState(self, startState):
        self.sendUpdate('setStartState', [startState])

    def b_setStartState(self, startState):
        self.setStartState(startState)
        self.d_setStartState(startState)

    def getStartState(self):
        return self.startState

    # setAggroRadius(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAggroRadius(self, aggroRadius):
        self.aggroRadius = aggroRadius

    def d_setAggroRadius(self, aggroRadius):
        self.sendUpdate('setAggroRadius', [aggroRadius])

    def b_setAggroRadius(self, aggroRadius):
        self.setAggroRadius(aggroRadius)
        self.d_setAggroRadius(aggroRadius)

    def getAggroRadius(self):
        return self.aggroRadius

    # setAggroMode(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAggroMode(self, aggroMode):
        self.aggroMode = aggroMode

    def d_setAggroMode(self, aggroMode):
        self.sendUpdate('setAggroMode', [aggroMode])

    def b_setAggroMode(self, aggroMode):
        self.setAggroMode(aggroMode)
        self.d_setAggroMode(aggroMode)

    def getAggroMode(self):
        return self.aggroMode


