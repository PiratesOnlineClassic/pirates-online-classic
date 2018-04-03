# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesbase.PiratesPreloader
from direct.directnotify.DirectNotifyGlobal import giveNotify
import PiratesGlobals

class PiratesPreloader(object):
    __module__ = __name__

    def __init__(self):
        self.baseLoadCounter = 0
        self.preloadPool = []
        self.doLoad()

    def doLoad(self):
        if self.baseLoadCounter >= len(PiratesGlobals.preLoadSet):
            return
        loader.loadModel(PiratesGlobals.preLoadSet[self.baseLoadCounter], callback=self.callback)

    def callback(self, model):
        self.preloadPool.append(model)
        self.baseLoadCounter += 1
        self.doLoad()


giveNotify(PiratesPreloader)
# okay decompiling .\pirates\piratesbase\PiratesPreloader.pyc
