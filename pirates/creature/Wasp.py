# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.Wasp
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature

class Wasp(Creature):
    __module__ = __name__
    ModelInfo = ('models/char/wasp_hi', 'models/char/wasp_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({'death': 'sfx_wasp_death.mp3', 'pain': 'sfx_wasp_ouch.mp3'})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('idle_flying', 'idle_fly'), ('walk', 'walk'), ('drop', 'react_drop'), ('advance', 'attack_advance'), ('sting', 'attack_sting'), ('leap_sting', 'attack_leap_sting'), ('pain', 'react_pull_back'), ('death', 'react_death'))

    class AnimationMixer(Creature.AnimationMixer):
        __module__ = __name__
        notify = DirectNotifyGlobal.directNotify.newCategory('WaspAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],), 'idle_flying': (LOOP['LOOP'],), 'walk': (LOOP['LOOP'],), 'advance': (ACTION['ACTION'],), 'drop': (ACTION['ACTION'],), 'sting': (ACTION['ACTION'],), 'leap_sting': (ACTION['ACTION'],), 'ouch': (ACTION['ACTION'],), 'death': (ACTION['MOVIE'],), 'pain': (ACTION['ACTION'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        if not Wasp.sfx:
            for name in Wasp.SfxNames:
                Wasp.sfx[name] = loader.loadSfx('audio/' + Wasp.SfxNames[name])

        self.nametagOffset = 11.5
        self.generateCreature()
# okay decompiling .\pirates\creature\Wasp.pyc
