# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.PlayerPirateGameFSM
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.destructibles import ShatterableSkeleton
from pirates.pirate.BattleAvatarGameFSM import BattleAvatarGameFSM


class PlayerPirateGameFSM(BattleAvatarGameFSM):
    

    def __init__(self, av, fsmName='PlayerPirateGameFSM'):
        BattleAvatarGameFSM.__init__(self, av, fsmName)

    def enterDeath(self, extraArgs=[]):
        BattleAvatarGameFSM.enterDeath(self, extraArgs)

    def exitDeath(self):
        BattleAvatarGameFSM.exitDeath(self)
# okay decompiling .\pirates\pirate\PlayerPirateGameFSM.pyc
