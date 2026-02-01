from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature
from pirates.kraken.TentacleUtils import TentacleUtils
from pirates.pirate import AvatarTypes

class Holder(Creature, TentacleUtils):
    ModelInfo = ('models/char/holderTentacle_high', 'models/char/holderTentacle_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({
        'pain': 'sfx_crab_pain.mp3',
        'death': 'sfx_crab_death.mp3'})
    sfx = {}
    AnimList = (('idle', 'idle'), ('emerge', 'emerge'))
    
    class AnimationMixer(Creature.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('CrabAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {
            'idle': (LOOP['LOOP'],)}

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


