# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pvp.SiegeManager
from direct.distributed.DistributedObject import DistributedObject
from pirates.pvp.SiegeManagerBase import SiegeManagerBase
from otp.speedchat import SCDecoders
from pirates.speedchat import PSCDecoders
from pirates.piratesbase import PLocalizer
from direct.fsm.StatePush import FunctionCall

class SiegeManager(DistributedObject, SiegeManagerBase):
    __module__ = __name__
    TeamJoinableChangedEvent = 'PVPTeamJoinableChanged'

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        SiegeManagerBase.__init__(self)

    def generate(self):
        self._announcerInterest = None
        self._siegeTeam = 0
        self._siegeTeamUpdater = FunctionCall(self._setSiegeTeam, localAvatar._siegeTeamSV)
        DistributedObject.generate(self)
        self._pvpTeamJoinable = {}
        base.cr.distributedDistrict.siegeManager = self
        return

    def delete(self):
        self._siegeTeamUpdater.destroy()
        del self._siegeTeamUpdater
        self._removeAnnouncerInterest()
        del self._pvpTeamJoinable
        del base.cr.distributedDistrict.siegeManager
        DistributedObject.delete(self)

    def setPvpEnabled(self, enabled):
        self._pvpEnabled = enabled

    def getPvpEnabled(self):
        return self._pvpEnabled

    def setTeamsJoinable(self, teamJoinableItems):
        for teamId, joinable in teamJoinableItems:
            self._pvpTeamJoinable[teamId] = joinable

        messenger.send(SiegeManager.TeamJoinableChangedEvent)

    def teamIsJoinable(self, teamId):
        if not config.GetBool('want-pvp-team-balance', 1):
            return True
        return self._pvpTeamJoinable.get(teamId, True)

    def sendChat(self, message):
        self.sendUpdate('sendChat', [message, 0, 0])

    def sendWLChat(self, message):
        self.sendUpdate('sendWLChat', [message, 0, 0])

    def sendSC(self, msgIndex):
        self.sendUpdate('sendSC', [msgIndex])

    def recvChat(self, avatarId, message, chatFlags, DISLid, name):
        if not self.cr.avatarFriendsManager.checkIgnored(avatarId):
            displayMess = '%s %s %s' % (name, self.getPVPChatTeamName(localAvatar.getSiegeTeam()), message)
            base.chatAssistant.receiveShipPVPMessage(displayMess)

    def recvWLChat(self, avatarId, message, chatFlags, DISLid, name):
        if not self.cr.avatarFriendsManager.checkIgnored(avatarId):
            displayMess = '%s %s %s' % (name, self.getPVPChatTeamName(localAvatar.getSiegeTeam()), message)
            base.chatAssistant.receiveShipPVPMessage(displayMess)

    def recvSpeedChat(self, avatarId, msgIndex, name):
        if not self.cr.avatarFriendsManager.checkIgnored(avatarId):
            displayMess = '%s %s %s' % (name, self.getPVPChatTeamName(localAvatar.getSiegeTeam()), SCDecoders.decodeSCStaticTextMsg(msgIndex))
            base.chatAssistant.receiveShipPVPMessage(displayMess)

    def getPVPChatTeamName(self, teamId):
        if teamId == 2:
            return PLocalizer.PVPSpanish
        else:
            if teamId == 1:
                return PLocalizer.PVPFrench
            else:
                return PLocalizer.PVPPrefix

    def _addAnnouncerInterest(self):
        if not self._announcerInterest:
            self._announcerInterest = self.addInterest(555, 'siegeAnnouncer')

    def _removeAnnouncerInterest(self):
        if self._announcerInterest:
            self.removeInterest(self._announcerInterest)
            self._announcerInterest = None
        return

    def _setSiegeTeam(self, siegeTeam):
        if siegeTeam and not self._siegeTeam:
            self._addAnnouncerInterest()
        else:
            if not siegeTeam and self._siegeTeam:
                self._removeAnnouncerInterest()
        self._siegeTeam = siegeTeam
# okay decompiling .\pirates\pvp\SiegeManager.pyc
