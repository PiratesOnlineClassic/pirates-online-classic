from pirates.seapatch import SeaPatchRoot

class LerpSeaPatchInterval():
    __module__ = __name__
    lerpNum = 1

    def __init__(self, name, duration, blendType, patch, initial, target):
        if name == None:
            name = 'LerpSeaPatchInterval-%d' % self.lerpNum
            LerpSeaPatchInterval.lerpNum += 1

        blendType = self.stringBlendType(blendType)
        if target == None:
            target = SeaPatchRoot()