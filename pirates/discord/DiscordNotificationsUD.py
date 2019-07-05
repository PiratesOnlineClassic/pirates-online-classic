from direct.directnotify.DirectNotifyGlobal import *

from pirates.discord.DiscordNotifcationsBase import DiscordNotificationsBase
from pirates.discord.DiscordMessageUD import DiscordMessageUD, DiscordEmbeded
from pirates.discord.DiscordGlobalsUD import DiscordChannels

import datetime

class DiscordNotificationsUD(DiscordNotificationsBase):
    """
    Manages all webhook notications for the UberDOG server
    """

    notify = directNotify.newCategory('DiscordNotificationsUD')
    notify.setInfo(True)

    def __init__(self, air):
        DiscordNotificationsBase.__init__(self, air)

        self.logExceptions = config.GetBool('discord-log-exceptions', True)

        self.air.netMessenger.accept('publishException', self, self.publishServerException)

    def publishServerException(self, message, header, fields={}):
        """
        Publishes a server exception to Discord
        """

        self.notify.warning('Exception: %s' % message)

        # Verify we want to publish an exception
        if not self.logExceptions:
            self.notify.warning('Discord publishing disabled; Ignoring request')
            return

        self.notify.debug('Message: %s' % message)
        self.notify.debug('Header: %s' % header)
        self.notify.debug('Fields: %s' % fields)

        discordMessage = DiscordMessageUD(self.air)
        discordMessage.content = message
        discordMessage.embedded = DiscordEmbeded()
        discordMessage.embedded.title = header
        discordMessage.embedded.color = 16711680
        discordMessage.timestamp = datetime.datetime.now().isoformat()
        discordMessage.embedded.description = message

        for fieldKey in fields:
            fieldValue = fields[fieldKey]
            discordMessage.embedded.setField(fieldKey, fieldValue)

        discordMessage.send(DiscordChannels.SandboxWebhooks)
        
        
