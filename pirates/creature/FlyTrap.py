from direct.directnotify import DirectNotifyGlobal
from panda3d.core import *
from pirates.creature.Creature import Creature


class FlyTrap(Creature):
    
    ModelInfo = ('models/char/flytrap_hi', 'models/char/flytrap_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({'death': 'sfx_flytrap_death.mp3', 'pain': 'sfx_flytrap_hit.mp3', 'spawn': 'sfx_flytrap_rise_ground.mp3'})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('attack_a', 'attack_a'), ('attack_jab', 'attack_jab'), ('attack_left_fake', 'attack_left_fake'), ('attack_right_fake', 'attack_right_fake'), ('intro', 'rise_from_ground'), ('shoot', 'spit'), ('pain', 'hit'), ('death', 'death'))

    class AnimationMixer(Creature.AnimationMixer):
        
        notify = DirectNotifyGlobal.directNotify.newCategory('FlyTrapAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],), 'attack_a': (ACTION['ACTION'],), 'attack_jab': (ACTION['ACTION'],), 'attack_left_fake': (ACTION['ACTION'],), 'attack_right_fake': (ACTION['ACTION'],), 'intro': (ACTION['ACTION'],), 'shoot': (ACTION['ACTION'],), 'pain': (ACTION['ACTION'],), 'death': (ACTION['MOVIE'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        if not FlyTrap.sfx:
            for name in FlyTrap.SfxNames:
                FlyTrap.sfx[name] = loader.loadSfx('audio/' + FlyTrap.SfxNames[name])

        self.nametagOffset = 23
        self.generateCreature()
        self.headNode = self.find('**/def_stem10')

    def generateCreature(self):
        Creature.generateCreature(self)
        self.getGeomNode().setH(180)
        self.setAvatarScale(0.7)
