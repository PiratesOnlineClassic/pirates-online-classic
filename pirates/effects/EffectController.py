from pandac.PandaModules import *


class EffectController:
    particleDummy = None

    def __init__(self):
        self.track = None
        self.startEffect = None
        self.endEffect = None
        self.f = None
        self.p0 = None

    def createTrack(self):
        pass

    def destroy(self):
        self.finish()
        if self.f:
            self.f.cleanup()
        self.f = None
        self.p0 = None
        self.removeNode()

    def cleanUpEffect(self):
        self.setPosHpr(0, 0, 0, 0, 0, 0)
        if self.f:
            self.f.disable()
        self.detachNode()

    def setPoolSize(self, size):
        if self.p0:
            self.p0.setPoolSize(int(size))

    def reallyCleanUpEffect(self):
        self.cleanUpEffect()
        self.finish()

    def play(self, lod=None):
        if lod != None:
            try:
                self.createTrack(lod)
            except TypeError as e:
                raise TypeError(
                    'Error loading %s effect.' % self.__class__.__name__)

        else:
            self.createTrack()
        self.track.start()
        return

    def stop(self):
        if self.track:
            self.track.pause()
            self.track = None
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        if self.endEffect:
            self.endEffect.pause()
            self.endEffect = None
        self.cleanUpEffect()

    def finish(self):
        if self.track:
            self.track.pause()
            self.track = None
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        if self.endEffect:
            self.endEffect.pause()
            self.endEffect = None

    def startLoop(self, lod=None):
        if lod != None:
            try:
                self.createTrack(lod)
            except TypeError as e:
                raise TypeError(
                    'Error loading %s effect.' % self.__class__.__name__)

        else:
            self.createTrack()
        if self.startEffect:
            self.startEffect.start()

    def stopLoop(self):
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        if self.endEffect and not self.endEffect.isPlaying():
            self.endEffect.start()

    def getTrack(self):
        if not self.track:
            self.createTrack()
        return self.track
