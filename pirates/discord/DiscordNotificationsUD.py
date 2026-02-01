from direct.directnotify.DirectNotifyGlobal import *

from pirates.ai import HolidayGlobals
from pirates.discord.DiscordNotificationsBase import DiscordNotificationsBase
from pirates.discord.DiscordMessageUD import DiscordMessageUD, DiscordEmbeded
from pirates.discord.DiscordGlobalsUD import DiscordChannels, DiscordColorCode
from pirates.piratesbase import PLocalizer
from pirates.web.RPCGlobals import rpcservice, ResponseCodes
from pirates.web.RPCServiceUD import RPCServiceUD

import datetime
import semidbm
import traceback

class DiscordNotificationsUD(DiscordNotificationsBase):
    """
    Manages all webhook notications for the UberDOG server
    """

    notify = directNotify.newCategory('DiscordNotificationsUD')
    notify.setInfo(True)

    def __init__(self, air):
        DiscordNotificationsBase.__init__(self, air)

        self.logExceptions = config.GetBool('discord-log-exceptions', True)
        self.logHolidays = config.GetBool('discord-log-holidays', True)
        self.logHackers = config.GetBool('discord-log-hackers', True)

        self.air.netMessenger.accept('publishException', self, self.publishServerException)
        self.air.netMessenger.accept('publishHacker', self, self.publishServerHacker)
        self.holidayDb = semidbm.open(config.GetString('holiday-state-filename', 'local/holiday-state'), 'c')

    def serverHolidayStart(self, holidayId, quietly):
        """
        Called on holiday start
        """
    
        if self.getHolidayState(holidayId):
           return

        self.storeHolidayState(holidayId, True)
        if not quietly:
            try:
                self.publishServerHoliday(holidayId)
            except:
                self.notify.warning('Failed to publish holiday Discord notification (%s)' % holidayId)
                print((traceback.format_exc()))

    def serverHolidayEnd(self, holidayId):
        """
        Called on holiday end
        """

        self.storeHolidayState(holidayId, False)

    def getHolidayState(self, holidayId):
        """
        Retrieves the holiday state from the local db
        """

        if str(holidayId) in self.holidayDb:
            return bool(self.holidayDb[str(holidayId)])
        else:
            return False

    def storeHolidayState(self, holidayId, state):
        """
        Stores the holiday state in the local db
        """

        self.holidayDb[str(holidayId)] = str(state)
        if getattr(self.holidayDb, 'sync', None):
            self.holidayDb.sync()
        else:
            self.notify.warning('Unable to store holiday (%s) state %s' % (holidayId, state))

    def publishServerHoliday(self, holidayId):
        """
        Publishes the requested holiday to Discord
        """

        # Verify we want to publish the holiday
        if not self.logHolidays:
            self.notify.warning('Discord publishing disabled; Ignoring request')
            return

        holidayTitle = HolidayGlobals.getHolidayDiscordTitle(holidayId)
        holidayDesc = HolidayGlobals.getHolidayDiscordDescription(holidayId)

        self.notify.debug('Title: %s' % holidayTitle)
        self.notify.debug('Desc: %s' % holidayDesc)

        if not holidayTitle or not holidayDesc:
            self.notify.warning('Holiday (%s) does not have the required fields for Discord use' % holidayId)
            return 

        holidayDate = HolidayGlobals.getHolidayDates(holidayId)
        startTime = holidayDate.getReadableStartDate(0)
        endtime = holidayDate.getReadableEndDate(0)

        discordMessage = DiscordMessageUD(self.air)
        discordMessage.content = PLocalizer.DISCORD_NEW_EVENT
        discordMessage.embedded = DiscordEmbeded()
        discordMessage.embedded.title = holidayTitle
        discordMessage.embedded.color = DiscordColorCode.Green
        discordMessage.timestamp = datetime.datetime.now().isoformat()
        discordMessage.embedded.description = holidayDesc
        discordMessage.embedded.setField('Starts', startTime)
        discordMessage.embedded.setField('Ends', endtime)
        discordMessage.embedded.setFooter('Pirates Online Classic')

        discordMessage.send(DiscordChannels.StaffDiscordSandbox)

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
        discordMessage.embedded.color = DiscordColorCode.Red
        discordMessage.timestamp = datetime.datetime.now().isoformat()
        discordMessage.embedded.description = message
        discordMessage.embedded.setFooter('Pirates Online Classic')

        for fieldKey in fields:
            fieldValue = fields[fieldKey]
            discordMessage.embedded.setField(fieldKey, fieldValue, inline=False)

        discordMessage.send(DiscordChannels.StaffServerIssues)

    def publishServerHacker(self, message, header, fields={}):
        """
        Publishes a server hacker message to Discord
        """

        self.notify.warning('Hacker: %s' % message)

        # Verify we want to publish potential hacker messages
        if not self.logHackers:
            self.notify.warning('Discord publishing disabled; Ignoring request')
            return

        self.notify.debug('Message: %s' % message)
        self.notify.debug('Header: %s' % header)
        self.notify.debug('Fields: %s' % fields)

        discordMessage = DiscordMessageUD(self.air)
        discordMessage.content = message
        discordMessage.embedded = DiscordEmbeded()
        discordMessage.embedded.title = header
        discordMessage.embedded.color = DiscordColorCode.Red
        discordMessage.timestamp = datetime.datetime.now().isoformat()
        discordMessage.embedded.description = message
        discordMessage.embedded.setFooter('Pirates Online Classic')

        for fieldKey in fields:
            fieldValue = fields[fieldKey]
            discordMessage.embedded.setField(fieldKey, fieldValue)

        discordMessage.send(DiscordChannels.StaffDiscordSandbox)
        
@rpcservice(serviceName='discordNotifications')
class DiscordNotificationService(RPCServiceUD):
    """
    Handles all Discord notification related handlers for the RPC
    """

    def publishServerHoliday(self, holidayId):
        """
        Summary:
            Manually publishes a holiday to Discord through the Discord notification object.
        Parameters:
            [int] = The holiday id to publish
        Response:
            None
        """

        self.air.discordNotifications.publishServerHoliday(holidayId)
        return self._formatResults()