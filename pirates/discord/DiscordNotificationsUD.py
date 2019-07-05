from direct.directnotify.DirectNotifyGlobal import *

from pirates.ai import HolidayGlobals
from pirates.discord.DiscordNotifcationsBase import DiscordNotificationsBase
from pirates.discord.DiscordMessageUD import DiscordMessageUD, DiscordEmbeded
from pirates.discord.DiscordGlobalsUD import DiscordChannels

import datetime
import semidbm

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

        self.air.netMessenger.accept('publishException', self, self.publishServerException)
        self.holidayDb = semidbm.open(config.GetString('holiday-state-filename', 'local/holiday-state'), 'c')

    def serverHolidayStart(self, holidayId, quietly):
        """
        Called on holiday start
        """
    
        #if self.getHolidayState(holidayId):
        #   return

        self.storeHolidayState(holidayId, True)
        if not quietly:
            self.publishServerHoliday(holidayId)

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
        discordMessage.content = 'Ahoy @everyone! A new event has started in the Caribbean!'
        discordMessage.embedded = DiscordEmbeded()
        discordMessage.embedded.title = holidayTitle
        discordMessage.timestamp = datetime.datetime.now().isoformat()
        discordMessage.embedded.description = holidayDesc
        discordMessage.embedded.setField('Starts', startTime)
        discordMessage.embedded.setField('Ends', endtime)
        discordMessage.send(DiscordChannels.SandboxGeneral)

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
            discordMessage.embedded.setField(fieldKey, fieldValue, inline=False)

        discordMessage.send(DiscordChannels.StaffServerIssues)
        
        
