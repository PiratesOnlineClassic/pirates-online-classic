import math

from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.distributed import DistributedInteractive
from pirates.piratesbase import PiratesGlobals, PLocalizer

class DistributedBuriedTreasure(DistributedInteractive.DistributedInteractive):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuriedTreasure')
    UpdateDelay = 2.0

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedBuriedTreasure')
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        self.showTreasureIval = None
        self.raiseTreasureIval = None
        self.currentDepth = 0.0
        self.startingDepth = 0.0

    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)
        self.chest = None
        self.setInteractOptions(proximityText=PLocalizer.InteractBuriedTreasure, sphereScale=10, diskRadius=10, exclusive=0)

    def disable(self):
        DistributedInteractive.DistributedInteractive.disable(self)
        if self.chest:
            self.chest.removeNode()
            self.chest = None
        if self.showTreasureIval:
            self.showTreasureIval.pause()
            self.showTreasureIval = None
        if self.raiseTreasureIval:
            self.raiseTreasureIval.pause()
            self.raiseTreasureIval = None

    def loadChest(self):
        if self.chest:
            return
        self.chest = loader.loadModel('models/props/treasureChest')
        self.chest.findAllMatches('**/pile_group').stash()
        self.chest.reparentTo(self)
        self.chest.setScale(0.8)
        self.chestLidHigh = self.chest.find('**/lod_high/top')
        self.chestLidMed = self.chest.find('**/lod_med/top')
        self.chestLidLow = self.chest.find('**/lod_low/top')
        self.dirt = loader.loadModel('models/props/dirt_pile')
        self.dirt.reparentTo(self)
        self.dirt.flattenStrong()

    def handleEnterProximity(self, collEntry):
        DistributedInteractive.DistributedInteractive.handleEnterProximity(self, collEntry)

    def handleExitProximity(self, collEntry):
        DistributedInteractive.DistributedInteractive.handleExitProximity(self, collEntry)

    def requestInteraction(self, avId, interactType=0):
        localAvatar.motionFSM.off()
        DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        localAvatar.guiMgr.createWarning(PLocalizer.AlreadySearched)
        localAvatar.motionFSM.on()
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)

    def startDigging(self):
        self.acceptInteraction()
        localAvatar.b_setGameState('Digging')
        localAvatar.guiMgr.workMeter.updateText(PLocalizer.InteractDigging)
        localAvatar.guiMgr.workMeter.startTimer(self.startingDepth, self.currentDepth)
        pos = localAvatar.getPos(self)
        angle = math.atan2(pos[0], pos[1])
        radius = 5
        localAvatar.setPos(self, math.sin(angle) * radius, math.cos(angle) * radius, 0)
        localAvatar.headsUp(self)
        localAvatar.setH(localAvatar, -90)

    def stopDigging(self, questProgress):
        localAvatar.guiMgr.workMeter.stopTimer()
        localAvatar.guiMgr.showQuestProgress(questProgress)
        if localAvatar.gameFSM.state == 'Digging':
            if localAvatar.lootCarried > 0:
                localAvatar.b_setGameState('LandTreasureRoam')
            else:
                localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)

    def requestExit(self):
        DistributedInteractive.DistributedInteractive.requestExit(self)
        self.stopDigging(0)

    def enterWaiting(self):
        DistributedInteractive.DistributedInteractive.enterWaiting(self)

    def exitWaiting(self):
        DistributedInteractive.DistributedInteractive.exitWaiting(self)

    def enterUse(self):
        DistributedInteractive.DistributedInteractive.enterUse(self)

    def exitUse(self):
        DistributedInteractive.DistributedInteractive.exitUse(self)

    def setStartingDepth(self, depth):
        self.startingDepth = depth

    def setCurrentDepth(self, depth):
        oldZ = self.currentDepth / float(self.startingDepth) * -2.6
        self.currentDepth = depth
        z = self.currentDepth / float(self.startingDepth) * -2.6
        dirtZ = min(z + 0.5, -1.5)
        dirtOldZ = min(oldZ + 0.5, -1.5)
        if self.currentDepth == self.startingDepth:
            if self.chest:
                self.chest.stash()
                self.dirt.stash()
                self.chest.setZ(z)
                self.dirt.setZ(z * 1.5)
            return
        self.loadChest()
        self.chest.unstash()
        self.dirt.unstash()
        if self.raiseTreasureIval:
            self.raiseTreasureIval.pause()
        self.raiseTreasureIval = Parallel(LerpPosInterval(self.chest, self.UpdateDelay, Vec3(0, 0, z), startPos=Vec3(0, 0, oldZ)), LerpPosInterval(self.dirt, self.UpdateDelay, Vec3(0, 0, dirtZ), startPos=Vec3(0, 0, dirtOldZ)))
        self.raiseTreasureIval.start()
        if self.state == 'Use':
            localAvatar.guiMgr.workMeter.startTimer(self.startingDepth, self.currentDepth)

    def showTreasure(self, gold):
        self.loadChest()
        self.showTreasureIval = Sequence(Parallel(LerpHprInterval(self.chestLidHigh, 1, Vec3(0, -40, 0)), LerpHprInterval(self.chestLidMed, 1, Vec3(0, -40, 0)), LerpHprInterval(self.chestLidLow, 1, Vec3(0, -40, 0))), Wait(3.0), Func(self.setTransparency, 1), LerpColorScaleInterval(self, 0.5, Vec4(1, 1, 1, 0)), Func(self.chest.stash))
        self.showTreasureIval.start()