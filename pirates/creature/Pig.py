# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.Pig
from direct.directnotify import DirectNotifyGlobal
from panda3d.core import *
from pirates.creature.Animal import Animal


class Pig(Animal):
    
    ModelInfo = ('models/char/pig_hi', 'models/char/pig_')
    SfxNames = dict(Animal.SfxNames)
    SfxNames.update({})
    AnimList = (
     ('walk', 'walk'), ('run', 'walk'), ('idle', 'rooting'), ('rooting', 'rooting'))

    class AnimationMixer(Animal.AnimationMixer):
        
        notify = DirectNotifyGlobal.directNotify.newCategory('PigAnimationMixer')
        LOOP = Animal.AnimationMixer.LOOP
        ACTION = Animal.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],), 'run': (LOOP['LOOP'],), 'walk': (LOOP['LOOP'],), 'rooting': (LOOP['LOOP'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', -1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', -1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Animal.__init__(self)
        self.generateCreature()
# okay decompiling .\pirates\creature\Pig.pyc
