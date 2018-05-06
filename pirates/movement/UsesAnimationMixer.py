from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import ActorInterval
from direct.showbase.PythonUtil import report

class UsesAnimationMixer:

    def __init__(self, animationMixerType=None):
        if hasattr(self, 'animationMixer') and self.animationMixer:
            if not isinstance(self.animationMixer, animationMixerType):
                pass
        if animationMixerType:
            self.animationMixer = animationMixerType(self)
            self.mixingEnabled = True
        else:
            self.animationMixer = None
            self.mixingEnabled = False

    def lateInit(self, animationMixerType):
        if self.animationMixer:
            UsesAnimationMixer.delete(self)
        UsesAnimationMixer.__init__(self, animationMixerType)

    def delete(self):
        self.animationMixer.delete()
        self.animationMixer = None

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-animmixer-report', 'want-jump-report'])
    def loop(self, *args, **kwargs):
        self.notify.debug("loop: Performing loop with argumets %s! and kwargs %s" % (str(args), str(kwargs)))
        if self.mixingEnabled:
            defaultBlendT = self.animationMixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendT = kwargs.pop('blendT', defaultBlendT)
        blendDelay = kwargs.pop('blendDelay', 0)
        kwargs['blendT'] = blendT
        kwargs['blendDelay'] = blendDelay
        if self.mixingEnabled:
            self.animationMixer.loop(*args, **kwargs)
        else:
            Actor.loop(self, *args, **kwargs)

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-animmixer-report', 'want-jump-report'])
    def play(self, *args, **kwargs):
        self.notify.debug("play: Performing play with argumets %s! and kwargs %s" % (str(args), str(kwargs)))
        if self.mixingEnabled:
            defaultBlendT = self.animationMixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendInT = kwargs.pop('blendInT', defaultBlendT)
        blendOutT = kwargs.pop('blendOutT', defaultBlendT)
        blendInto = kwargs.pop('blendInto', None)
        kwargs['blendInT'] = blendInT
        kwargs['blendOutT'] = blendOutT
        kwargs['blendInto'] = blendInto
        if self.mixingEnabled:
            self.animationMixer.play(*args, **kwargs)
        else:
            Actor.play(self, *args, **kwargs)

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-animmixer-report', 'want-jump-report'])
    def pingpong(self, *args, **kwargs):
        self.notify.debug("pingpong: Performing pingpong with argumets %s! and kwargs %s" % (str(args), str(kwargs)))
        if self.mixingEnabled:
            defaultBlendT = self.animationMixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendT = kwargs.pop('blendT', defaultBlendT)
        kwargs['blendT'] = blendT
        if self.mixingEnabled:
            self.animationMixer.pingpong(*args, **kwargs)
        else:
            Actor.pingpong(self, *args, **kwargs)

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-animmixer-report', 'want-jump-report'])
    def pose(self, *args, **kwargs):
        self.notify.debug("pose: Performing pose with argumets %s! and kwargs %s" % (str(args), str(kwargs)))
        if self.mixingEnabled:
            defaultBlendT = self.animationMixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendT = kwargs.pop('blendT', defaultBlendT)
        kwargs['blendT'] = blendT
        if self.mixingEnabled:
            self.animationMixer.pose(*args, **kwargs)
        else:
            Actor.pose(self, *args, **kwargs)

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-animmixer-report', 'want-jump-report'])
    def stop(self, *args, **kwargs):
        self.notify.debug("stop: Stopping animation with argumets %s! and kwargs %s" % (str(args), str(kwargs)))
        if self.mixingEnabled:
            self.animationMixer.stop(*args, **kwargs)
        else:
            Actor.stop(self, *args, **kwargs)

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-animmixer-report', 'want-jump-report'])
    def actorInterval(self, *args, **kwargs):
        self.notify.debug("actorInterval: Performing actorInterval with argumets %s! and kwargs %s" % (str(args), str(kwargs)))
        mixingWanted = kwargs.pop('mixingWanted', self.mixingEnabled)
        if mixingWanted:
            defaultBlendT = self.animationMixer.defaultBlendT
        else:
            defaultBlendT = 0
        blendInT = kwargs.pop('blendInT', defaultBlendT)
        blendOutT = kwargs.pop('blendOutT', defaultBlendT)
        blendInto = kwargs.pop('blendInto', None)
        if mixingWanted:
            partName = kwargs.get('partName', None)
            return self.animationMixer.actorInterval(ActorInterval(self, *args, **kwargs), partName, blendInT, blendOutT, blendInto)
        return ActorInterval(self, *args, **kwargs)

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-animmixer-report', 'want-jump-report'])
    def disableMixing(self):
        self.mixingEnabled = False
        self.animationMixer.cleanup()
        Actor.disableBlend(self)
        Actor.stop(self)

    @report(types=['args', 'deltaStamp'], dConfigParam=['want-animmixer-report', 'want-jump-report'])
    def enableMixing(self):
        self.mixingEnabled = True
        Actor.enableBlend(self)
        self.animationMixer.cleanup()

    def isMixingEnabled(self):
        return self.mixingEnabled