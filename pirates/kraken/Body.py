from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature
from pirates.pirate import AvatarTypes

class Body(Creature):
    ModelInfo = ('models/char/krakenHead-high', 'models/char/krakenHead-')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({
        'pain': 'sfx_crab_pain.mp3',
        'death': 'sfx_crab_death.mp3'})
    sfx = {}
    AnimList = (('idle', 'idle'),)
    
    class AnimationMixer(Creature.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('CrabAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {
            'idle': (LOOP['LOOP'],)}

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


