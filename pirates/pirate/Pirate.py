# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.Pirate
from . import AvatarTypes
from .Human import Human
from pirates.piratesbase import PiratesGlobals


class Pirate(Human):
    __module__ = __name__

    def __init__(self, other=None):
        Human.__init__(self, other)
        self.avatarType = AvatarTypes.Pirate


class PirateHeadPortrait(Human):
    __module__ = __name__

    def __init__(self):
        Human.__init__(self)
        self.avatarType = AvatarTypes.Townfolk

    def generatePortrait(self, other):
        highLod = other.getLOD('2000')
        face = highLod.findAllMatches('**/body_master_face')
        face.stash()
        body = highLod.findAllMatches('**/body_*')
        body.stash()
        clothing = highLod.findAllMatches('**/clothing_*')
        clothing.stash()
        face.unstash()
        hairs = highLod.findAllMatches('**/hair_*')
        eyes = highLod.findAllMatches('**/eye*')
        teeth = highLod.findAllMatches('**/teeth*')

    def shapeHead(self, other):
        import pdb
        pdb.set_trace()
        self.style = other.style
        self.generateHuman(self.style.gender, base.cr.human)
# okay decompiling .\pirates\pirate\Pirate.pyc
