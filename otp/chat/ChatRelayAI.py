"""
Chat that the client sends to the AI (an ownsend airecv field) instead of
having the State Server broadcast it. Once it's been checked the AI relays it
to the object's location itself.

The Astron Client Agent forwards a field update sent to a location channel to
every client with interest in that location, whatever the field's keywords,
and drops it for the client whose channel is the update's sender. So relaying
as the client who chatted reaches exactly the same clients a broadcast field
does: everyone in the zone but the sender, who has already shown it locally.
"""

from otp.chat import ChatFilter


class ChatRelayAI:
    """
    Mixed into a DistributedObjectAI. Subclasses provide chatFlood, a
    ChatFilter.ChatFlood, shared by every object of the class.
    """

    chatFlood = None

    def sendUpdateToLocation(self, fieldName, args, senderChannel=None):
        """
        Sends a field update to every client with interest in our location,
        the same as the State Server does for a broadcast field. The update
        goes out as if sent from senderChannel, so the client agent of the
        avatar who chatted doesn't echo it back to them.
        """

        if not self.parentId and not self.zoneId:
            return

        if senderChannel is None:
            senderChannel = self.air.ourChannel

        field = self.dclass.getFieldByName(fieldName)
        locationChannel = (self.parentId << 32) | self.zoneId
        dg = field.aiFormatUpdate(self.doId, locationChannel, senderChannel, args)
        self.air.send(dg)

    def chatViolation(self, issue, eject=False):
        self.notify.warning('Avatar %s: %s' % (self.air.getAvatarIdFromSender(), issue))
        self.air.writeServerEvent('suspicious', avId=self.air.getAvatarIdFromSender(), issue=issue)
        if eject:
            self.air.kickChannel(self.air.getMsgSender(), ChatFilter.ChatBootCode,
                'Chat violation: %s' % issue)

    def _isFlooding(self, avatarId):
        if not self.chatFlood.isFlooding(avatarId):
            return False

        if self.chatFlood.shouldWarn(avatarId):
            self.air.writeServerEvent('chat-flood', avId=avatarId)
            self.notify.info('Dropping chat from %d, too many messages.' % avatarId)

        return True

    def _cleanTypedChat(self, avatarId, fieldName, chatString):
        message = ChatFilter.cleanMessage(chatString)
        if message is None:
            if chatString.strip():
                self.chatViolation('%s too long (%d)' % (fieldName, len(chatString)))

            return None

        if self._isFlooding(avatarId):
            return None

        return message
