# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.npc.NPCSkeletonGameFSM
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
# okay decompiling .\pirates\npc\NPCSkeletonGameFSM.pyc
