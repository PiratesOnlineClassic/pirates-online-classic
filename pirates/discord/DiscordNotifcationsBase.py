
from direct.directnotify.DirectNotifyGlobal import *

from pirates.discord.DiscordWebHooksUD import *
from pirates.discord.DiscordGlobalsUD import DiscordWebhooks

import traceback

class DiscordNotificationsBase:

    notify = directNotify.newCategory('DiscordNotificationsBase')

    def __init__(self, air):
        self.air = air
        self.exceptionBacklog = config.GetInt('discord-exception-backlog', 10)
        self.notify.info('%s going online' % self.__class__.__name__)

    def getServerTypeName(self):
        if self.air.dcSuffix == 'AI':
            return 'District'
        else:
            return 'UberDOG'

    def getExceptionHeader(self):
        if self.air.dcSuffix == 'AI':
            headerMessage = 'Internal exception occured on %s' % self.air.distributedDistrict.getName()
        else:
            headerMessage = 'Internal exception occured on the UberDOG'

        return headerMessage

    def getExceptionTraceback(self, exception):
        trace = traceback.format_exc()
        discordStack = trace.split('\n')

        exceptionBacklog = self.exceptionBacklog
        if exceptionBacklog > len(discordStack):
           exceptionBacklog = len(discordStack)
        discordStack = discordStack[-exceptionBacklog:]
        discordStacktrace = '%s\n' % str(exception)
        for stack in discordStack:
            discordStacktrace += '%s\n' % stack

        return discordStacktrace

    def reportServerException(self, exception, avatarId=0, accountId=0):
        """
        Logs a server exception to Discord
        """

        self.notify.info('Reporting exception to Discord: %s' % str(exception))
        try:
            pass #TODO
        except:
            self.notify.warning('Failed to report exception: %s' % str(exception))
