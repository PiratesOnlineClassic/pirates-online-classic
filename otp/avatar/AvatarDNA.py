import random

from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from panda3d.core import *


class AvatarDNA:
    notify = directNotify.newCategory('AvatarDNA')

    def __str__(self):
        return 'avatar parent class: type undefined'

    def makeNetString(self):
        self.notify.error('called makeNetString on avatarDNA parent class')

    def printNetString(self):
        string = self.makeNetString()
        dg = PyDatagram(string)
        dg.dumpHex(ostream)

    def makeFromNetString(self, string):
        self.notify.error('called makeFromNetString on avatarDNA parent class')

    def getType(self):
        self.notify.error('Invalid DNA type: ', self.type)
