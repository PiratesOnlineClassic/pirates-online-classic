# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.world.WorldNode
from pandac.PandaModules import *
from direct.distributed import DistributedNode
from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals
from direct.showbase.PythonUtil import HotkeyBreaker

class WorldNode(NodePath):
    __module__ = __name__
    notify = directNotify.newCategory('WorldNode')

    def __init__(self):
        NodePath.__init__(self, 'WorldNode')
        self.playerControlledObj = base.localAvatar

    def delete(self):
        self.removeNode()
        del self.playerControlledObj
        if self.cr.activeWorld and (self.cr.activeWorld.isEmpty() or self.cr.activeWorld.compareTo(self) == 0):
            self.cr.setActiveWorld(None)
        self.ignoreAll()
        return

    def disable(self):
        WorldNode.notify.debug('removing old activeWorld')
        self.detachNode()

    def announceGenerate(self):
        base.cr.setActiveWorld(self)
        self.reparentTo(render)
# okay decompiling .\pirates\world\WorldNode.pyc
