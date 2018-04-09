# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.kraken.Holder
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
from pirates.creature.Creature import Creature
from pirates.kraken.TentacleUtils import TentacleUtils
from pirates.pirate import AvatarTypes


class Holder(Creature, TentacleUtils):
    
    ModelInfo = ('models/char/holderTentacle_high', 'models/char/holderTentacle_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({'pain': 'sfx_crab_pain.mp3', 'death': 'sfx_crab_death.mp3'})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('emerge', 'emerge'))

    class AnimationMixer(Creature.AnimationMixer):
        
        notify = DirectNotifyGlobal.directNotify.newCategory('CrabAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],)}

    def __init__(self):
        Creature.__init__(self)
        TentacleUtils.__init__(self)
        self.setAvatarType(AvatarTypes.Crab)
        if not Holder.sfx:
            for name in Holder.SfxNames:
                Holder.sfx[name] = loader.loadSfx('audio/' + Holder.SfxNames[name])

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
# okay decompiling .\pirates\kraken\Holder.pyc
