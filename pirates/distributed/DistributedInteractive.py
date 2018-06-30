from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedNode
from direct.showbase.PythonUtil import report
from pirates.interact import InteractiveBase
from pirates.piratesgui import InteractGUI
from pirates.world import DistributedLocatableObject


class DistributedInteractive(
        DistributedNode.DistributedNode, InteractiveBase.InteractiveBase,
        DistributedLocatableObject.DistributedLocatableObject):
    notify = DirectNotifyGlobal.directNotify.newCategory(
        'DistributedInteractive')

    def __init__(self, cr):
        DistributedNode.DistributedNode.__init__(self, cr)
        InteractiveBase.InteractiveBase.__init__(self)
        DistributedLocatableObject.DistributedLocatableObject.__init__(self, cr)

        self.interactGUI = None
        self.hideHpMeterFlag = 0
        self.userId = 0
        self.uniqueId = None

    def delete(self):
        DistributedNode.DistributedNode.delete(self)
        InteractiveBase.InteractiveBase.delete(self)
        DistributedLocatableObject.DistributedLocatableObject.delete(self)

    def generate(self):
        DistributedNode.DistributedNode.generate(self)
        InteractiveBase.InteractiveBase.generate(self)
        DistributedLocatableObject.DistributedLocatableObject.generate(self)

    def disable(self):
        DistributedNode.DistributedNode.disable(self)
        InteractiveBase.InteractiveBase.disable(self)
        DistributedLocatableObject.DistributedLocatableObject.disable(self)

    def announceGenerate(self):
        DistributedNode.DistributedNode.announceGenerate(self)
        DistributedLocatableObject.DistributedLocatableObject.announceGenerate(
            self)

    def isBattleable(self):
        return 0

    @report(
        types=['frameCount', 'deltaStamp'],
        dConfigParam='want-shipboard-report')
    def requestInteraction(self, avId, interactType=0, instant=0):
        self.sendUpdate('requestInteraction',
                        [base.localAvatar.doId, interactType, instant])
        self.cr.interactionMgr.stop()
        self.request('Waiting')

    def setLocation(self, parentId, zoneId):
        DistributedNode.DistributedNode.setLocation(self, parentId, zoneId)

    def requestExit(self):
        self.sendUpdate('requestExit')
        self.refreshState()

    def demandExit(self):
        self.sendUpdate('demandExit')
        self.refreshState()

    def refreshState(self):
        if self.hasProximityCollision and self.allowInteract and not self.ignoreProximity and not self.proximityCollisionNodePath.isEmpty(
        ):
            distance = self.proximityCollisionNodePath.getDistance(localAvatar)
            proxSphereRadius = self.proximityCollisionNodePath.getScale()[0]
            avRadius = 1.4
            if distance <= proxSphereRadius + avRadius:
                self.request('Proximity')
            else:
                self.request('Idle')
        else:
            self.request('Idle')

    def acceptInteraction(self):
        self.request('Use')

    def rejectInteraction(self):
        self.cr.interactionMgr.start()
        self.refreshState()

    def rejectExit(self):
        pass

    def offerOptions(self, optionIds, statusCodes):
        if self.interactGUI:
            self.notify.warning('offerOptions: old interact GUI still around')
            self.interactGUI.destroy()
            self.interactGUI = None

        self.interactGUI = InteractGUI.InteractGUI()
        title = self.getMenuTitle()
        self.interactGUI.setOptions(title, optionIds, statusCodes,
                                    self.b_selectOption)

    def b_selectOption(self, optionId):
        self.d_selectOption(optionId)
        self.selectOption(optionId)

    def d_selectOption(self, optionId):
        self.sendUpdate('selectOption', [optionId])

    def selectOption(self, optionId):
        if self.interactGUI:
            self.interactGUI.destroy()
            self.interactGUI = None

    def getMenuTitle(self):
        return ''

    def setUserId(self, avId):
        self.userId = avId

    def getUserId(self):
        return self.userId

    def setUniqueId(self, uid):
        if self.uniqueId != '' and uid != self.uniqueId:
            base.cr.uidMgr.removeUid(self.uniqueId)

        self.uniqueId = uid
        base.cr.uidMgr.addUid(self.uniqueId, self.getDoId())

    def getUniqueId(self):
        return self.uniqueId

    def getWorld(self):
        return base.cr.activeWorld
