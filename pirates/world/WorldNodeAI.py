from panda3d.core import *

from direct.directnotify.DirectNotifyGlobal import directNotify


class WorldNodeAI(NodePath):
    notify = directNotify.newCategory('WorldNodeAI')

    def __init__(self, air):
        NodePath.__init__(self, 'WorldNodeAI')
