
from direct.directnotify.DirectNotifyGlobal import *

from pirates.discord.DiscordWebHooksUD import *
from pirates.discord.DiscordGlobalsUD import DiscordMentions

import traceback

class DiscordNotificationsBase:

    notify = directNotify.newCategory('DiscordNotificationsBase')

    def __init__(self, air):
        self.air = air
        self.exceptionBacklog = config.GetInt('discord-exception-backlog', 10)
        self.exceptionPingAll = config.GetBool('discord-exception-ping', False)
        self.hackerPingall = config.GetBool('discord-hacker-ping', False)
        self.notify.info('%s going online' % self.__class__.__name__)

    def getServerTypeName(self):
        if self.air.dcSuffix == 'AI':
            return 'District'
        else:
            return 'UberDOG'

    def getExceptionHeader(self):
        return 'Internal exception occured on server (%s)' % self.air.getServerName()

    def getExceptionTraceback(self, exception):
        trace = traceback.format_exc()
        discordStack = trace.split('\n')

        exceptionBacklog = self.exceptionBacklog
        if exceptionBacklog > len(discordStack):
           exceptionBacklog = len(discordStack)
        discordStack = discordStack[-exceptionBacklog:]
        discordStacktrace = '%s\n' % str(exception)
        for stack in discordStack:
            if not stack:
                continue
            discordStacktrace += '%s\n' % stack

        discordStacktrace = discordStacktrace if discordStacktrace else 'N/A'
        return discordStacktrace

    def reportServerException(self, exception, avatarId=0, accountId=0):
        """
        Logs a server exception to Discord
        """

        self.notify.info('Reporting exception to Discord: %s' % str(exception))
        try:
            message = DiscordMentions.Everyone if self.exceptionPingAll else ''
            header = self.getExceptionHeader()
            
            fields = {}
            fields['Traceback'] = self.getExceptionTraceback(exception)
            fields['Dev Server'] = self.air.isDevServer()

            self.publishServerException(message, header, fields)
        except Exception as e:
            self.notify.warning('Failed to report exception: %s' % str(e))
            print((traceback.format_exc()))

    def publishServerException(self, message, header, fields={}):
        """
        Publishes a server exception to Discord
        """

    def getHackerHeader(self):
        return 'Potential Hacker found on server (%s)' % self.air.getServerName()

    def reportServerHacker(self, message, avatarId=0, accountId=0):
        """
        Logs a server hacker to Discord
        """

        avatar = self.air.doId2do.get(avatarId)

        self.notify.info('Reporting hacker (%s) to Discord: %s' % (accountId, message))
        try:
            message = DiscordMentions.Everyone if self.hackerPingall else ''
            header = self.getHackerHeader()
            fields = {}

            if avatar:
                fields['Character Position'] = str(avatar.getPos())
                fields['Character Name'] = avatar.getName()
                if self.getServerTypeName() == 'District':
                    fields['Island'] = avatar.getParentObj().getLocalizerName()
                else:
                    fields['Island'] = 'N/A'
            else:
                fields['Character Position'] = 'N/A'
                fields['Character Name'] = 'N/A'
                fields['Island'] = 'N/A'
            
            self.publishServerHacker(message, header, fields)

        except Exception as e:
            self.notify.warning('Failed to report hacker to Discord: %s' % str(e))
            print((traceback.format_exc()))

    def publishServerHacker(self, message, header, fields={}):
        """
        Publishes a server hacker to Discord
        """