# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.DistributedStump
from direct.interval.IntervalGlobal import *
from pirates.creature.DistributedCreature import DistributedCreature
from pirates.creature.Stump import Stump

class DistributedStump(DistributedCreature):
    __module__ = __name__

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, Stump())
# okay decompiling .\pirates\creature\DistributedStump.pyc
