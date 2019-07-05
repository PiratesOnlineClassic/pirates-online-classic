from direct.directnotify.DirectNotifyGlobal import *

from pirates.discord.DiscordNotifcationsBase import DiscordNotificationsBase

class DiscordNotificationsAI(DiscordNotificationsBase):
    """
    Manages all webhook notications for the AI server
    """

    notify = directNotify.newCategory('DiscordNotificationsAI')
    notify.setInfo(True)

    def __init__(self, air):
        DiscordNotificationsBase.__init__(self, air)

    def publishServerException(self, message, header, fields={}):
        """
        Publishes a server exception to Discord
        """

        self.notify.info('Publishing exception to Discord through the UberDOG')
        self.air.netMessenger.send('publishException', [message, header, fields])