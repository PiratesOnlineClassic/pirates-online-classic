from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

from pirates.piratesbase import PiratesGlobals


class DistributedPiratesTutorialAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPiratesTutorialAI')

    def __init__(self, air, avatar, interior):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'DistributedPiratesTutorialAI')

        self.avatar = avatar
        self.interior = interior

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterAct0Tutorial(self):
        self.currentQuest = self.air.questMgr.addQuest(
            self.avatar, 'Chapter1.rung1')

        self.currentQuest.d_startFinalizeScene(0, 0)

    def exitAct0Tutorial(self):
        pass

    def enterMakeAPirateComplete(self):

        def questFinalizeCallback():
            self.sendUpdate('makeAPirateCompleteResp', [])

        self.acceptOnce('quest-finalize-%d' % self.currentQuest.doId,
            questFinalizeCallback)

        self.currentQuest.d_startFinalizeScene(1, 0)

    def exitMakeAPirateComplete(self):
        pass

    def clientEnterAct0Tutorial(self):
        if self.state != 'Off':
            return

        self.request('Act0Tutorial')

    def makeAPirateComplete(self):
        if self.state != 'Act0Tutorial':
            return

        self.request('MakeAPirateComplete')

    def delete(self):
        self.cleanup()
        DistributedObjectAI.delete(self)
