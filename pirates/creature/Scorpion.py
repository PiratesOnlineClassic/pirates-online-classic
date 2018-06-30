# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.Scorpion
from direct.directnotify import DirectNotifyGlobal
from panda3d.core import *
from pirates.creature.Creature import Creature


class Scorpion(Creature):

    ModelInfo = ('models/char/scorpion_hi', 'models/char/scorpion_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({
        'death': 'sfx_scorp_death.mp3',
        'pain': 'sfx_scorp_knockback.mp3'
    })
    sfx = {}
    AnimList = (('idle', 'idle'), ('walk', 'walk'), ('run', 'run'),
                ('attack_left', 'attack_left'), ('attack_right',
                                                 'attack_right'),
                ('attack_both',
                 'attack_both'), ('attack_tail_sting',
                                  'attack_tail_sting'), ('pick_up_human',
                                                         'pick_up_human'),
                ('react_left', 'react_left'), ('react_right', 'react_right'),
                ('pain', 'knockback'), ('rear_up', 'rear_up'), ('death',
                                                                'death'))

    class AnimationMixer(Creature.AnimationMixer):

        notify = DirectNotifyGlobal.directNotify.newCategory(
            'ScorpionAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {
            'idle': (LOOP['LOOP'],),
            'walk': (LOOP['LOOP'],),
            'run': (LOOP['LOOP'],),
            'attack_left': (ACTION['ACTION'],),
            'attack_right': (ACTION['ACTION'],),
            'attack_both': (ACTION['ACTION'],),
            'attack_tail_sting': (ACTION['ACTION'],),
            'pick_up_human': (ACTION['ACTION'],),
            'react_left': (ACTION['ACTION'],),
            'react_right': (ACTION['ACTION'],),
            'pain': (ACTION['ACTION'],),
            'rear_up': (ACTION['ACTION'],),
            'death': (ACTION['MOVIE'],)
        }

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam',
                               (('idle', 1.0), ('walk', 1.0), ('run', 1.0),
                                ('walk', -1.0), ('run', 1.0), ('run', 1.0),
                                ('run', 1.0), ('run', 1.0), ('run', 1.0),
                                ('run', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam',
                               (('idle', 1.0), ('walk', 1.0), ('run', 1.0),
                                ('walk', -1.0), ('run', 1.0), ('run', 1.0),
                                ('run', 1.0), ('run', 1.0), ('run', 1.0),
                                ('run', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        if not Scorpion.sfx:
            for name in Scorpion.SfxNames:
                Scorpion.sfx[name] = loader.loadSfx('audio/' +
                                                    Scorpion.SfxNames[name])

        self.nametagOffset = 12.0
        self.generateCreature()
        self.headNode = self.find('**/def_root')


# okay decompiling .\pirates\creature\Scorpion.pyc
