from direct.distributed.DistributedObject import DistributedObject
from pirates.band import BandConstance


class DistributedPirateBandManager(DistributedObject):
    __module__ = __name__
    notify = directNotify.newCategory('PirateBandManager')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

    def generate(self):
        DistributedObject.generate(self)
        base.cr.PirateBandManager = self

    def disable(self):
        DistributedObject.disable(self)
        base.cr.PirateBandManager = None

    def d_requestInvite(self, avatarId):
        self.sendUpdate('requestInvite', [avatarId])

    def d_requestCancel(self, avatarId):
        self.sendUpdate('requestCancel', [avatarId])

    def requestOutCome(self, avatarId, responce):
        if responce == 0:
            if len(localAvatar.guiMgr.crewPage.crew) <= 1 and localAvatar.getLookingForCrew() == 1:
                localAvatar.toggleLookingForCrewSign()
            messenger.send('BandAdded-%s' % (avatarId,), [avatarId])
            return
        messenger.send('BandRequestRejected-%s' % (avatarId,), [avatarId, responce])

    def invitationFrom(self, avatarId, avatarName):
        messenger.send(BandConstance.BandInvitationEvent, [avatarId, avatarName])

    def invitationCancel(self, avatarId):
        messenger.send('BandRequestCancel-%s' % (avatarId,), [])

    def d_invitationResponce(self, avatarId, responce):
        if responce == 0 and len(localAvatar.guiMgr.crewPage.crew) == 0 and localAvatar.getLookingForCrew() == 1:
            localAvatar.toggleLookingForCrewSign()
        self.sendUpdate('invitationResponce', [avatarId, responce])

    def d_requestRemove(self, avatarId):
        self.sendUpdate('requestRemove', [avatarId])

    def d_requestCrewIconUpdate(self, iconKey):
        self.sendUpdate('requestCrewIconUpdate', [iconKey])

    def receiveUpdatedCrewIcon(self, iconKey):
        base.localAvatar.setCrewIcon(iconKey)