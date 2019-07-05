from direct.directnotify.DirectNotifyGlobal import *

from pirates.discord.DiscordNotifcationsBase import DiscordNotificationsBase

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
            return

        
