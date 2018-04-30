# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.Seagull
from direct.directnotify import DirectNotifyGlobal
from panda3d.core import *
from pirates.creature.Animal import Animal


class Seagull(Animal):
    
    ModelInfo = ('models/char/seagull_hi', 'models/char/seagull_')
    SfxNames = dict(Animal.SfxNames)
    SfxNames.update({})
    AnimList = (
     ('idle', 'flying'), ('walk', 'flying'), ('run', 'flying'), ('flying', 'flying'), ('takeoff', 'takeoff'), ('landing', 'landing'), ('groom_idle', 'groom_idle'))

    class AnimationMixer(Animal.AnimationMixer):
        
        notify = DirectNotifyGlobal.directNotify.newCategory('SeagullAnimationMixer')
        LOOP = Animal.AnimationMixer.LOOP
        ACTION = Animal.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],), 'walk': (LOOP['LOOP'],), 'run': (LOOP['LOOP'],), 'takeoff': (ACTION['ACTION'],), 'landing': (ACTION['ACTION'],), 'flying': (LOOP['LOOP'],), 'groom_idle': (ACTION['ACTION'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('groom_idle', 1.0), ('run', 1.0), ('run', 1.0), ('fly', 1.0), ('fly', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('groom_idle', 1.0), ('run', 1.0), ('run', 1.0), ('fly', 1.0), ('fly', 1.0)))

    def __init__(self):
        Animal.__init__(self)
        if not Seagull.sfx:
            for name in Seagull.SfxNames:
                Seagull.sfx[name] = loader.loadSfx('audio/' + Seagull.SfxNames[name])

        self.generateCreature()
# okay decompiling .\pirates\creature\Seagull.pyc
