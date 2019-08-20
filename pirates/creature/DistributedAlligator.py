from pirates.creature.DistributedCreature import DistributedCreature
from pirates.creature.Alligator import Alligator

class DistributedAlligator(DistributedCreature):
    
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


