# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.SeaSerpent
from pandac.PandaModules import *
from pirates.creature.SeaMonster import SeaMonster
from pirates.pirate import AvatarTypes


class SeaSerpent(SeaMonster):
    __module__ = __name__
    ModelInfo = ('models/char/serpent_hi', 'models/char/serpent_')
    SfxNames = dict(SeaMonster.SfxNames)
    SfxNames.update({'death': 'sfx_wasp_death.mp3', 'pain': 'sfx_wasp_ouch.mp3'})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('swim', 'swim'), ('walk', 'swim'), ('submerge', 'submerge'), ('attack', 'attack'), ('emerge', 'emerge'), ('death', 'submerge'))

    class AnimationMixer(SeaMonster.AnimationMixer):
        __module__ = __name__
        LOOP = SeaMonster.AnimationMixer.LOOP
        ACTION = SeaMonster.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],), 'swim': (LOOP['LOOP'],), 'walk': (LOOP['LOOP'],), 'submerge': (ACTION['ACTION'],), 'attack': (ACTION['ACTION'],), 'emerge': (ACTION['ACTION'],), 'death': (ACTION['MOVIE'],)}

    def __init__(self):
        SeaMonster.__init__(self)
        self.setAvatarType(AvatarTypes.SeaSerpent)
        if not SeaSerpent.sfx:
            for name in SeaSerpent.SfxNames:
                SeaSerpent.sfx[name] = loader.loadSfx('audio/' + SeaSerpent.SfxNames[name])

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
# okay decompiling .\pirates\creature\SeaSerpent.pyc
