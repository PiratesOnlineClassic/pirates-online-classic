# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.avatar.AvatarDNA
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
notify = directNotify.newCategory('AvatarDNA')

class AvatarDNA:
    __module__ = __name__

    def __str__(self):
        return 'avatar parent class: type undefined'

    def makeNetString(self):
        notify.error('called makeNetString on avatarDNA parent class')

    def printNetString(self):
        string = self.makeNetString()
        dg = PyDatagram(string)
        dg.dumpHex(ostream)

    def makeFromNetString(self, string):
        notify.error('called makeFromNetString on avatarDNA parent class')

    def getType(self):
        notify.error('Invalid DNA type: ', self.type)
        return type
# okay decompiling .\otp\avatar\AvatarDNA.pyc
