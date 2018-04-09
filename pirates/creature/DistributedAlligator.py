# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.DistributedAlligator
from pirates.creature.Alligator import Alligator
from pirates.creature.DistributedCreature import DistributedCreature


class DistributedAlligator(DistributedCreature):
    __module__ = __name__

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, Alligator())

    def announceGenerate(self):
        DistributedCreature.announceGenerate(self)
        texCard = loader.loadModel('models/char/undead_creatures')
        if texCard:
            tex = texCard.findTexture('alligator_undead')
            lodnames = self.getLODNames()
            for lod in lodnames:
                lodptr = self.getLOD(lod)
                lodptr.setTexture(tex, 1)
# okay decompiling .\pirates\creature\DistributedAlligator.pyc
