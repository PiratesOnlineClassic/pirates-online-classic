from pandac.PandaModules import *
from otp.otpbase import OTPRender
from direct.actor.Actor import Actor
from pirates.kraken.TentacleUtils import TentacleUtils

class DoomTentacle(Actor, TentacleUtils):
    ModelInfo = ('models/char/doomTentacle_high', 'models/char/doomTentacle_')
    SfxNames = dict()
    SfxNames.update({
        'pain': 'sfx_crab_pain.mp3',
        'death': 'sfx_crab_death.mp3'})
    sfx = {}
    AnimList = (('emerge', 'emerge'),)
    
    def __init__(self):
        Actor.__init__(self, None, None, None, flattenable = 0, setFinal = 1)
        TentacleUtils.__init__(self)
        if not DoomTentacle.sfx:
            for name in DoomTentacle.SfxNames:
                DoomTentacle.sfx[name] = loader.loadSfx('audio/' + DoomTentacle.SfxNames[name])

        filePrefix = self.ModelInfo[1]
        if loader.loadModelCopy(filePrefix + '1000') != None:
            hasLOD = True
            self.setLODs()
            self.loadModel(filePrefix + '2000', 'modelRoot', 'hi', copy = 1)
            self.loadModel(filePrefix + '1000', 'modelRoot', 'med', copy = 1)
            self.loadModel(filePrefix + '500', 'modelRoot', 'low', copy = 1)
        else:
            hasLOD = False
            self.loadModel(self.ModelInfo[0], copy = 1)
        AnimDict = dict()
        for anim in self.AnimList:
            AnimDict[anim[0]] = filePrefix + anim[1]
        
        if hasLOD:
            self.loadAnims(AnimDict, 'modelRoot', 'all')
        else:
            self.loadAnims(AnimDict)
        OTPRender.renderReflection(True, self, 'doomTentacle', None)
        self.initStatusTable()
        self.startUpdateTask()

    def disable(self):
        self.removeEffects()
        self.stopUpdateTask()


