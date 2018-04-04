
from pirates.instance.DistributedInstanceWorldAI import DistributedInstanceWorldAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTreasureMapInstanceAI(DistributedInstanceWorldAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTreasureMapInstanceAI')

    def __init__(self, air):
        DistributedInstanceWorldAI.__init__(self, air)
        self.state = ['', 0]


    # setTreasureMapDoId(uint32) broadcast ram

    def setTreasureMapDoId(self, treasureMapDoId):
        self.sendUpdate('setTreasureMapDoId', [treasureMapDoId])

    # setObjectives(uint32 []) broadcast ram

    def setObjectives(self, objectives):
        self.sendUpdate('setObjectives', [objectives])

    # setTMComplete(resultPair [], resultPair [])

    def setTMComplete(self, tMComplete, todo_resultPair_1):
        self.sendUpdate('setTMComplete', [tMComplete, todo_resultPair_1])

    # requestLeave(uint32) airecv clsend

    def requestLeave(self, requestLeave):
        pass

    # requestLeaveApproved(uint32, uint32, uint32)

    def requestLeaveApproved(self, requestLeaveApproved, todo_uint32_1, todo_uint32_2):
        self.sendUpdate('requestLeaveApproved', [requestLeaveApproved, todo_uint32_1, todo_uint32_2])

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

    # setFortIds(uint32 []) broadcast ram

    def setFortIds(self, fortIds):
        self.sendUpdate('setFortIds', [fortIds])

    # requestState(string) airecv clsend

    def requestState(self, requestState):
        pass


