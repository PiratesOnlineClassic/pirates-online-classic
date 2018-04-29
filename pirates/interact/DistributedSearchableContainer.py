import math

from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.task import Task
from panda3d.core import *
from pirates.distributed import DistributedInteractive
from pirates.piratesbase import PiratesGlobals, PLocalizer
from pirates.piratesgui import PiratesGuiGlobals


class DistributedSearchableContainer(DistributedInteractive.DistributedInteractive):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSearchableContainer')

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedSearchableContainer')
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        self.searchTime = None
        self.type = None
        self.containerColorR = 1.0
        self.containerColorG = 1.0
        self.containerColorB = 1.0
        self.containerColorA = 1.0
        self.sphereScale = 10
        self.container = None
        self.startSearchTime = 0.0

    def setSearchTime(self, t):
        self.searchTime = t

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def setSphereScale(self, sphereScale):
        self.sphereScale = sphereScale

    def getSphereScale(self):
        return self.sphereScale

    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)

    def announceGenerate(self):
        self.setInteractOptions(proximityText=PLocalizer.InteractSearchableContainer, sphereScale=self.getSphereScale(), diskRadius=10, exclusive=0)
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        self.loadContainer()

    def disable(self):
        DistributedInteractive.DistributedInteractive.disable(self)
        if self.container:
            self.container.removeNode()
            self.container = None

    def delete(self):
        DistributedInteractive.DistributedInteractive.delete(self)

    def loadContainer(self):
        if self.container:
            return
        modelPath = PiratesGlobals.SearchableModels.get(self.type, 'models/props/crate_04')
        container = loader.loadModel(modelPath)
        containerColor = self.getContainerColor()
        container.setColorScale(containerColor[0], containerColor[1], containerColor[2], containerColor[3])
        container.reparentTo(self)
        container.flattenStrong()

    def requestInteraction(self, avId, interactType=0):
        localAvatar.motionFSM.off()
        DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        localAvatar.guiMgr.createWarning(PLocalizer.AlreadySearched)
        localAvatar.motionFSM.on()
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)

    def startSearching(self):
        self.acceptInteraction()
        localAvatar.guiMgr.workMeter.updateText(PLocalizer.InteractSearching)
        localAvatar.guiMgr.workMeter.startTimer(self.searchTime)
        localAvatar.b_setGameState('Searching')
        pos = localAvatar.getPos(self)
        angle = math.atan2(pos[0], pos[1])
        radius = 4
        localAvatar.setPos(self, math.sin(angle) * radius, math.cos(angle) * radius, 0)
        localAvatar.headsUp(self)
        localAvatar.setH(localAvatar, 0)

    def stopSearching(self, questProgress):
        localAvatar.guiMgr.workMeter.stopTimer()
        localAvatar.guiMgr.showQuestProgress(questProgress)
        if localAvatar.getGameState() == 'Searching':
            localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
        self.refreshState()

    def requestExit(self):
        DistributedInteractive.DistributedInteractive.requestExit(self)
        self.stopSearching(0)

    def setContainerColor(self, r, g, b, a):
        self.containerColorR = r
        self.containerColorG = g
        self.containerColorB = b
        self.containerColorA = a

    def getContainerColor(self):
        return (self.containerColorR, self.containerColorG, self.containerColorB, self.containerColorA)