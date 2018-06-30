# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.Dog
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DistancePhasedNode import BufferedDistancePhasedNode
from otp.otpbase import OTPGlobals
from panda3d.core import *
from pirates.creature.Animal import Animal


class Dog(Animal):

    ModelInfo = ('models/char/dog_hi', 'models/char/dog_')
    SfxNames = dict(Animal.SfxNames)
    SfxNames.update({})
    AnimList = (('idle', 'idle_sitting_keys'), ('idle_sitting',
                                                'idle_sitting_keys'),
                ('walk', 'walk_keys'), ('idle_standing', 'idle_standing_keys'),
                ('bark_sitting', 'bark_sitting_keys'), ('bark_standing',
                                                        'bark_standing_keys'),
                ('into_sit', 'into_sit_keys'), ('into_lying_down',
                                                'into_lying_down'),
                ('wag_sitting', 'wag_sitting_keys'), ('wag_standing',
                                                      'wag_standing_keys'))

    class AnimationMixer(Animal.AnimationMixer):

        notify = DirectNotifyGlobal.directNotify.newCategory(
            'DogAnimationMixer')
        LOOP = Animal.AnimationMixer.LOOP
        ACTION = Animal.AnimationMixer.ACTION
        AnimRankings = {
            'idle': (LOOP['LOOP'],),
            'idle_sitting': (LOOP['LOOP'],),
            'idle_standing': (LOOP['LOOP'],),
            'bark_sitting': (ACTION['ACTION'],),
            'bark_standing': (ACTION['ACTION'],),
            'into_sit': (ACTION['ACTION'],),
            'into_lying_down': (ACTION['ACTION'],),
            'walk': (LOOP['LOOP'],),
            'wag_sitting': (LOOP['LOOP'],),
            'wag_sitting': (LOOP['LOOP'],)
        }

    class PhasedNode(BufferedDistancePhasedNode):

        def __init__(self, dog):
            self.dog = dog
            self.ival = None
            phaseDefs = {'At': (20, 30)}
            enterPrefix = 'enter'
            exitPrefix = 'exit'
            collideMask = OTPGlobals.WallBitmask | OTPGlobals.GhostBitmask
            BufferedDistancePhasedNode.__init__(
                self,
                'PhaseNode',
                phaseDefs,
                autoCleanup=False,
                enterPrefix=enterPrefix,
                exitPrefix=exitPrefix,
                phaseCollideMask=collideMask)
            return

        def delete(self):
            self.cleanup()
            self.dog = None
            return

        def cleanup(self):
            if self.ival:
                self.ival.pause()
            self.ival = None
            BufferedDistancePhasedNode.cleanup(self)
            return

        def loadPhaseAt(self):
            if self.ival:
                self.ival.pause()
            self.ival = self.dog.actorInterval('into_sit', playRate=-1)
            self.ival.start()
            self.dog.loop('idle_standing')

        def unloadPhaseAt(self):
            if self.ival:
                self.ival.pause()
            self.ival = self.dog.actorInterval('into_sit')
            self.ival.start()
            self.dog.loop('idle')

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState(
            'LandRoam',
            (('idle', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', -1.0),
             ('walk', 1.0), ('walk', 1.0), ('wag_standing', 1.0), ('walk', 1.0),
             ('idle', 1.0), ('walk', 1.0), ('walk', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState(
            'WaterRoam',
            (('idle', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', -1.0),
             ('walk', 1.0), ('walk', 1.0), ('wag_standing', 1.0), ('walk', 1.0),
             ('idle', 1.0), ('walk', 1.0), ('walk', 1.0), ('idle', 1.0)))

    def __init__(self):
        Animal.__init__(self, Dog.AnimationMixer)
        if not Dog.sfx:
            for name in Dog.SfxNames:
                Dog.sfx[name] = loader.loadSfx('audio/' + Dog.SfxNames[name])

        self.generateCreature()
        self.phaseNode = Dog.PhasedNode(self)
        self.phaseNode.reparentTo(self)

    def delete(self):
        if self.phaseNode:
            self.phaseNode.delete()
            self.phaseNode.removeNode()
            self.phaseNode = None
        Animal.delete(self)
        return


# okay decompiling .\pirates\creature\Dog.pyc
