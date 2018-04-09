# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.DistributedBat
from pirates.creature.Bat import Bat
from pirates.creature.DistributedCreature import DistributedCreature


class DistributedBat(DistributedCreature):
    __module__ = __name__

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, Bat())
# okay decompiling .\pirates\creature\DistributedBat.pyc
