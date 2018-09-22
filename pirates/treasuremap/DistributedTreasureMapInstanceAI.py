from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from otp.ai.MagicWordGlobal import *

from pirates.instance.DistributedInstanceWorldAI import DistributedInstanceWorldAI
from pirates.piratesbase import PiratesGlobals


class DistributedTreasureMapInstanceAI(DistributedInstanceWorldAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTreasureMapInstanceAI')

    def __init__(self, air):
        DistributedInstanceWorldAI.__init__(self, air)
        FSM.__init__(self, self.__class__.__name__)

        self.type = PiratesGlobals.INSTANCE_TM

        self.state = 'Off'

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterStageOne(self):
        pass

    def exitStageOne(self):
        pass

    def setState(self, state, *args):
        self.request(state, *args)

    def d_setState(self, state):
        self.sendUpdate('setState', [state, 0])

    def b_setState(self, state):
        self.setState(state)
        self.d_setState(state)

    def getState(self):
        return [self.state, 0]
