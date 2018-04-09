from direct.distributed import DistributedSmoothNode
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.pirate import BattleNPCGameFSM
from pirates.piratesbase import PiratesGlobals


class NPCSkeletonGameFSM(BattleNPCGameFSM.BattleNPCGameFSM):
    __module__ = __name__

    def __init__(self, av):
        BattleNPCGameFSM.BattleNPCGameFSM.__init__(self, av)

    def cleanup(self):
        BattleNPCGameFSM.BattleNPCGameFSM.cleanup(self)