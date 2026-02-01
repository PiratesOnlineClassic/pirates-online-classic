from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature

class FlyTrap(Creature):
    ModelInfo = ('models/char/flytrap_hi', 'models/char/flytrap_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({
        'death': 'sfx_flytrap_death.mp3',
        'pain': 'sfx_flytrap_hit.mp3',
        'spawn': 'sfx_flytrap_rise_ground.mp3' })
    sfx = {}
    AnimList = (('idle', 'idle'), ('attack_a', 'attack_a'), ('attack_jab', 'attack_jab'), ('attack_left_fake', 'attack_left_fake'), ('attack_right_fake', 'attack_right_fake'), ('intro', 'rise_from_ground'), ('shoot', 'spit'), ('pain', 'hit'), ('death', 'death'))
    
    class AnimationMixer(Creature.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('FlyTrapAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {
            'idle': (LOOP['LOOP'],),
            'attack_a': (ACTION['ACTION'],),
            'attack_jab': (ACTION['ACTION'],),
            'attack_left_fake': (ACTION['ACTION'],),
            'attack_right_fake': (ACTION['ACTION'],),
            'intro': (ACTION['ACTION'],),
            'shoot': (ACTION['ACTION'],),
            'pain': (ACTION['ACTION'],),
            'death': (ACTION['MOVIE'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
    
    def __init__(self):
        Creature.__init__(self)
        if not FlyTrap.sfx:
            for name in FlyTrap.SfxNames:
                FlyTrap.sfx[name] = loader.loadSfx('audio/' + FlyTrap.SfxNames[name])

        self.nametagOffset = 23
        self.generateCreature()
        self.headNode = self.find('**/def_stem10')
    
    def generateCreature(self):
        filePrefix = self.ModelInfo[1]
        if loader.loadModel(filePrefix + '1000', okMissing=True) != None:
            hasLOD = True
            self.setLODs()
            self.loadModel(filePrefix + '2000', 'modelRoot', 'hi', copy = 1, okMissing=True)
            self.loadModel(filePrefix + '1000', 'modelRoot', 'med', copy = 1, okMissing=True)
            self.loadModel(filePrefix + '500', 'modelRoot', 'low', copy = 1, okMissing=True)
        else:
            hasLOD = False
            self.loadModel(self.ModelInfo[0], copy = 1, okMissing=True)
        self.getGeomNode().setH(180)
        self.setAvatarScale(0.7)
        CreatureAnimDict = {}
        for anim in self.AnimList:
            CreatureAnimDict[anim[0]] = filePrefix + anim[1]

        if hasLOD:
            self.loadAnims(CreatureAnimDict, 'modelRoot', 'all')
        else:
            self.loadAnims(CreatureAnimDict)


