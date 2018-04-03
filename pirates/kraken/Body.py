# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.kraken.Body
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature
from pirates.pirate import AvatarTypes

class Body(Creature):
    __module__ = __name__
    ModelInfo = ('models/char/krakenHead-high', 'models/char/krakenHead-')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({'pain': 'sfx_crab_pain.mp3', 'death': 'sfx_crab_death.mp3'})
    sfx = {}
    AnimList = (('idle', 'idle'), )

    class AnimationMixer(Creature.AnimationMixer):
        __module__ = __name__
        notify = DirectNotifyGlobal.directNotify.newCategory('CrabAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],)}

    def __init__(self):
        Creature.__init__(self)
        self.setAvatarType(AvatarTypes.Crab)
        if not Body.sfx:
            for name in Body.SfxNames:
                Body.sfx[name] = loader.loadSfx('audio/' + Body.SfxNames[name])

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
# okay decompiling .\pirates\kraken\Body.pyc
