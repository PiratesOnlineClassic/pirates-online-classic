# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.DistributedSeagull
from pirates.creature.DistributedAnimal import DistributedAnimal
from pirates.creature.Seagull import Seagull

class DistributedSeagull(DistributedAnimal):
    __module__ = __name__

    def __init__(self, cr):
        DistributedAnimal.__init__(self, cr, Seagull())
# okay decompiling .\pirates\creature\DistributedSeagull.pyc
