# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pvp.DistributedBank
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
from pirates.distributed import DistributedInteractive
from pirates.interact import InteractiveBase
from pirates.piratesbase import PiratesGlobals, PLocalizer


class DistributedBank(DistributedInteractive.DistributedInteractive):
    
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBank')

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedBank')
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        self.belongsToTeam = PiratesGlobals.INVALID_TEAM
        self.value = 0
        self.maxValue = 100
        self.modelPath = None
        self.pendingPlacement = None
        self.parentObjId = None
        return

    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)

    def announceGenerate(self):
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        self.model = loader.loadModelCopy(self.modelPath)
        self.model.reparentTo(self)
        self.model.setColorScale(1, 1, 1, 1, 1)
        self.goldPileCollection = self.findAllMatches('**/pile*')
        self.goldPileList = self.goldPileCollection 
        self.goldPileList.reverse()
        self.goldPileCollection.stash()
        self.initInteractOpts()

    def initInteractOpts(self):
        self.setInteractOptions(sphereScale=12, diskRadius=30, proximityText=PLocalizer.PVPStealTreasure, exclusive=0)

    def disable(self):
        DistributedInteractive.DistributedInteractive.disable(self)
        self.model.removeNode()
        del self.model

    def enterProximity(self):
        if (self.belongsToTeam == PiratesGlobals.INVALID_TEAM or self.belongsToTeam != localAvatar.getTeam()) and localAvatar.lootCarried < self.cr.activeWorld.getMaxCarry() and self.value > 0:
            base.cr.interactionMgr.addInteractive(self, InteractiveBase.PROXIMITY)
            messenger.send('enterProximityOfInteractive')
        else:
            if self.belongsToTeam == localAvatar.getTeam() and localAvatar.lootCarried > 0:
                self.cr.activeWorld.handleDeposit('Team ' + str(self.belongsToTeam), localAvatar.getDoId(), self.getDoId())
            else:
                base.cr.interactionMgr.removeInteractive(self, InteractiveBase.PROXIMITY)
                messenger.send('enterProximityOfInteractive')
        self.accept(self.proximityCollisionExitEvent, self.handleExitProximity)

    def handleExitProximity(self, collEntry):
        DistributedInteractive.DistributedInteractive.handleExitProximity(self, collEntry)

    def showProximityInfo(self):
        self.cr.activeWorld.updateTreasureProximityText(self)
        DistributedInteractive.DistributedInteractive.showProximityInfo(self)

    def startLooting(self, lootType):
        self.acceptInteraction()
        base.localAvatar.b_setGameState('Stealing')

    def stopLooting(self):
        self.rejectInteraction()
        if base.localAvatar.lootCarried > 0:
            base.localAvatar.b_setGameState('LandTreasureRoam')
        else:
            base.localAvatar.b_setGameState(base.localAvatar.gameFSM.defaultState)

    def setBelongsToTeam(self, team):
        self.belongsToTeam = team

    def setValue(self, value):
        self.value = value
        self.showValue()

    def setMaxValue(self, maxValue):
        self.maxValue = maxValue
        self.showValue()

    def showValue(self):
        pass

    def requestInteraction(self, avId, interactType=0):
        base.localAvatar.motionFSM.off()
        DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)

    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def setParentObjId(self, parentObjId):
        self.parentObjId = parentObjId

        def putBankOnParent(parentObj, self=self):
            print 'putBank %s on parent %s' % (self.doId, parentObj)
            self.parentObj = parentObj
            self.reparentTo(parentObj)
            self.setColorScale(1, 1, 1, 1, 1)
            self.pendingPlacement = None
            return

        if parentObjId > 0:
            self.pendingPlacement = base.cr.relatedObjectMgr.requestObjects([self.parentObjId], eachCallback=putBankOnParent)
# okay decompiling .\pirates\pvp\DistributedBank.pyc
