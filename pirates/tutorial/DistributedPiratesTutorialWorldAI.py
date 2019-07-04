from direct.directnotify import DirectNotifyGlobal

from pirates.instance.DistributedInstanceWorldAI import DistributedInstanceWorldAI
from pirates.world import WorldGlobals
from pirates.piratesbase import PiratesGlobals


class DistributedPiratesTutorialWorldAI(DistributedInstanceWorldAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPiratesTutorialWorldAI')

    def __init__(self, air):
        DistributedInstanceWorldAI.__init__(self, air)

        self.fileName = WorldGlobals.PiratesTutorialSceneFileBase
        self.type = PiratesGlobals.INSTANCE_TUTORIAL

    def d_setTutorialHandlerId(self, tutorialHandlerId):
        self.sendUpdate('setTutorialHandlerId', [tutorialHandlerId])
