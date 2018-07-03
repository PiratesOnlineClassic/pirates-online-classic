# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.Monkey
from direct.directnotify import DirectNotifyGlobal
from panda3d.core import *
from pirates.creature.Creature import Creature


class Monkey(Creature):
    
    ModelInfo = ('models/char/monkey_hi', 'models/char/monkey_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('run', 'run'), ('pain', 'get_hit'), ('jump', 'jump'), ('taunt', 'taunt'))

    class AnimationMixer(Creature.AnimationMixer):
        
        notify = DirectNotifyGlobal.directNotify.newCategory('MonkeyAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],), 'run': (LOOP['LOOP'],), 'pain': (ACTION['ACTION'],), 'jump': (ACTION['ACTION'],), 'taunt': (ACTION['ACTION'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        if not Monkey.sfx:
            for name in Monkey.SfxNames:
                Monkey.sfx[name] = loader.loadSfx('audio/' + Monkey.SfxNames[name])

        self.generateCreature()
# okay decompiling .\pirates\creature\Monkey.pyc
