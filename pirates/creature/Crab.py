# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.Crab
from direct.directnotify import DirectNotifyGlobal
from panda3d.core import *
from pirates.creature.Creature import Creature


class Crab(Creature):

    ModelInfo = ('models/char/crab_hi', 'models/char/crab_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({
        'pain': 'sfx_crab_pain.mp3',
        'death': 'sfx_crab_death.mp3'
    })
    sfx = {}
    AnimList = (('idle', 'idle'), ('walk', 'walk'),
                ('attack_left', 'attack_left'), ('attack_right',
                                                 'attack_right'),
                ('attack_both', 'attack_both'), ('pain', 'pain'), ('death',
                                                                   'death'))

    class AnimationMixer(Creature.AnimationMixer):

        notify = DirectNotifyGlobal.directNotify.newCategory(
            'CrabAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {
            'idle': (LOOP['LOOP'],),
            'walk': (LOOP['LOOP'],),
            'attack_left': (ACTION['ACTION'],),
            'attack_right': (ACTION['ACTION'],),
            'attack_both': (ACTION['ACTION'],),
            'pain': (ACTION['ACTION'],),
            'death': (ACTION['MOVIE'],)
        }

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam',
                               (('idle', 1.0), ('walk', 1.0), ('walk', 1.0),
                                ('walk', -1.0), ('walk', 1.0), ('walk', 1.0),
                                ('walk', 1.0), ('walk', 1.0), ('walk', 1.0),
                                ('walk', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam',
                               (('idle', 1.0), ('walk', 1.0), ('walk', 1.0),
                                ('walk', -1.0), ('walk', 1.0), ('walk', 1.0),
                                ('walk', 1.0), ('walk', 1.0), ('walk', 1.0),
                                ('walk', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        if not Crab.sfx:
            for name in Crab.SfxNames:
                Crab.sfx[name] = loader.loadSfx('audio/' + Crab.SfxNames[name])

        self.nametagOffset = 1.6
        self.generateCreature()
        self.headNode = self.find('**/def_root')


# okay decompiling .\pirates\creature\Crab.pyc
