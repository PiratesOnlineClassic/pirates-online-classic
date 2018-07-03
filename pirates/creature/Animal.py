from pirates.creature.Creature import Creature

class Animal(Creature):
    def __init__(self, animationMixer=None):
        Creature.__init__(self, animationMixer)

    @report(types=['module', 'args'], dConfigParam='want-nametag-report')
    def initializeNametag3d(self):
        pass