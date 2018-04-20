import json
import requests
import traceback
from panda3d.core import ConfigVariableList
from direct.directnotify.DirectNotifyGlobal import *
from pirates.ai import HolidayGlobals

__all__ = [
    'WebhookException', 'WebhookBase', 'GenericWebhook', 'GithubWebhook', 'SlackWebhook',
    'SlackAttachmentException', 'SlackAttachment', 'SlackField', 'PiratesWebhookManager']

class WebhookException(Exception):
    """
    Generic Discord Webhook Exception
    """

class WebhookBase(object):

    """
    Base class for all Discord webhooks
    """

    def __init__(self, url, extension=None):
        self.url = url
        self.extension = extension

    def getExtension(self):
        return self.extension

    def formatMessage(self):
        """
        Called prior to posting to the url. Returns a formatted message
        """
        return NotImplemented

    def send(self):
        """
        Sends the formatted message to the specified `self.url`
        """

        formatted = self.formatMessage()
        if not formatted:
            raise WebhookException('Unable to send webhook post; formatMessage returned None')

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        url = self.url
        if self.extension:
            url += self.extension

        result = requests.post(url, headers=headers, data=formatted).text
        if result != '' and result != 'ok':
            raise WebhookException('Unexpected error occured while sending post; %s' % str(result))

        return True

class GenericWebhook(WebhookBase):

    """
    Represents a generic basic message Discord webhook
    """

    def __init__(self, url, message, author=None, avatar=None):
        WebhookBase.__init__(self, url)
        self.message = message
        self.author = author
        self.avatar = avatar

    def formatMessage(self):
        """
        Called prior to posting to the url. Returns a formatted message
        """

        data = {}
        data['content']= self.message

        if self.author:
            data['username'] = self.author

        if self.avatar:
            data['avatar_url'] = self.avatar

        return json.dumps(data)

class GithubWebhook(WebhookBase):

    """
    Represents a Github Discord webhook
    """

    def init(self, url):
        WebhookBase.__init__(self, url, '/github')

    def formatMessage(self):
        """
        Called prior to posting to the url. Returns a formatted message
        """

        return NotImplemented   

class SlackWebhook(WebhookBase):

    """
    Represents a Slack Discord webhook
    """

    def __init__(self, url, message='', author='', avatar=None):
        WebhookBase.__init__(self, url, '/slack')
        self.message = message
        self.author = author
        self.avatar = avatar
        self.attachments = []

    def getAttachments(self):
        return self.attachments

    def addAttachment(self, attachment):
        """
        Adds the specified SlackAttachment to self.attachments for later usage.
        """

        if isinstance(attachment, SlackAttachment):
            self.attachments.append(attachment)
        else:
            raise WebhookException('Unable to add attachment. %s is not an instance of %s' % (attachment.__class__.__name__, SlackAttachment.__name__))

    def formatMessage(self):
        """
        Called prior to posting to the url. Returns a formatted message
        """

        data = {}
        data['text'] = self.message
        data['username'] = self.author
        if self.avatar:
            data['icon_url'] = self.avatar

        data['attachments'] = [] 
        for attachment in self.attachments:
            att = {}
            att['author_name'] = attachment.author_name
            att['author_icon'] = attachment.author_icon
            att['color'] = attachment.color
            att['pretext'] = attachment.pretext
            att['title'] = attachment.title
            att['title_link'] = attachment.title_link
            att['image_url'] = attachment.image_url
            att['thumb_url'] = "http://example.com/path/to/thumb.png"
            att['footer'] = attachment.footer
            att['footer_icon'] = attachment.footer_icon
            att['ts'] = attachment.ts
            att['fields'] = []

            for field in attachment.fields:
                f = {}
                f['title'] = field.title
                f['value'] = field.value
                f['short'] = field.short

                att['fields'].append(f)

            data['attachments'].append(att)

        formatted = json.dumps(data)

        return formatted

class SlackAttachmentException(Exception):
    """
    Exception specified to the SlackAttachment object
    """

class SlackAttachment(object):

    """
    Represents a attachment for the SlackWebhook object
    """
    
    def __init__(self, author_name='', author_icon='', color='', pretext='', title='', title_link='', image_url='', footer='', footer_icon='', ts=0, fields=[]):
        self.author_name = author_name
        self.author_icon = author_icon
        self.color = color
        self.pretext = pretext
        self.title = title
        self.title_link = title_link
        self.image_url = image_url
        self.footer = footer
        self.footer_icon = footer_icon
        self.ts = ts
        self.fields = fields

    def addField(self, field):
        """
        Adds the specified field t o the current SlackAttachment object.
        """

        if isinstance(field, SlackField):
            self.fields.append(field)
        else:
            raise SlackAttachmentException('Unable to add field; %s is not an instance of %s' % (field.__class__.__name__, SlackField.__name__))

class SlackField(object):
    
    """
    Represents a SlackAttachment field
    """

    def __init__(self, title='', value='', short=False):
        self.title = title
        self.value = value
        self.short = short

class PiratesWebhookManager(object):

    """
    Manages Webhook transactions for the server
    """

    notify = directNotify.newCategory('PiratesWebhookManager')
    notify.setInfo(True)

    def __init__(self, air):
        self.air = air
        self.want_webhooks = config.GetBool('want-webhooks', True)
        self.want_everyone = config.GetBool('want-at-everyone', True)

        self.want_hacker_logs = config.GetBool('discord-log-hacks', True)
        self.hacker_log_url = config.GetString('discord-hacker-url', '')

        self.want_exception_logs = config.GetBool('discord-log-exceptions')
        self.exception_log_url = config.GetString('discord-exception-url', '')
        self.discord_except_backlog = config.GetInt('discord-exception-backlog', 10)

        self.want_holiday_logs = config.GetBool('discord-log-holidays', True)
        self.holiday_log_urls = ConfigVariableList('discord-holiday-url')

    def __internallyLogWebhook(self, url):
        """
        Internally logs the webhook transaction
        """
        self.notify.info('Sending Webhook message')
        self.air.writeServerEvent('webhook-sent', url=url)

    def __sendWebhook(self, webhook, verify):
        """
        Sends a webhook to its destination
        """
        if not self.want_webhooks and verify:
            return

        if not webhook:
            return

        self.__internallyLogWebhook(webhook.url)
        webhook.send()

    def __attemptAttachAvatarInfo(self, attachment, avatarId, accountId):
        """
        Attempts to attach avatar info using the avatarId
        """
        avatar = self.air.doId2do.get(avatarId)
        if avatar:
            attachment.addField(SlackField())
            attachment.addField(SlackField(title='Character Pos', value=str(avatar.getPos())))
            attachment.addField(SlackField(title='Character Name', value=avatar.getName()))
            attachment.addField(SlackField(title='Island', value=avatar.getParentObj().getLocalizerName()))

        #TODO: add account name?
        attachment.addField(SlackField())
        attachment.addField(SlackField(title='Dev Server', value=self.air.isDevServer()))   

    def logPotentialHacker(self, avatarId, accountId, message, **kwargs):
        """
        Logs a potential hacker message to Discord
        """
        if self.want_hacker_logs and not self.hacker_log_url:
            self.notify.warning('Failed to send hacker webhook; Hacker url not defined!')
            return
        
        # Generate header message
        districtName = self.air.distributedDistrict if hasattr(self.air, 'distributedDistrict') else None
        if districtName:
            headerMessage = 'Detected potential hacker on %d.' % districtName
        else:
            if self.air.dcSuffix == 'AI':
                headerMessage = 'Detected potential hacker on the AI'
            else:
                headerMessage = 'Detected potential hacker on the UberDOG'

        hookMessage = '@everyone' if self.want_everyone else ''
        webhookMessage = SlackWebhook(self.hacker_log_url, message=hookMessage)
        attachment = SlackAttachment(pretext=message, title=headerMessage)

        # Attach generic arguments
        for kwarg in kwargs:
            attachment.addField(SlackField(title=kwarg, value=kwargs[kwarg]))

        # Attempt to attach avatar information
        self.__attemptAttachAvatarInfo(attachment, avatarId, accountId)
 
        webhookMessage.addAttachment(attachment)
        self.__sendWebhook(webhookMessage, self.want_hacker_logs)

    def logServerException(self, exception, avatarId=0, accountId=0):
        """
        Logs a server exception to Discord
        """
        if self.want_exception_logs and not self.exception_log_url:
            self.notify.warning('Failed to send exception webhook; Exception url not defined!')
            return
        
        # Generate header message
        districtName = self.air.distributedDistrict if hasattr(self.air, 'distributedDistrict') else None
        if districtName:
            headerMessage = 'Internal exception occured on %s.' % districtName
        else:
            if self.air.dcSuffix == 'AI':
                headerMessage = 'Internal exception occured on the AI'
            else:
                headerMessage = 'Internal exception occured on the UberDOG'

        trace = traceback.format_exc()
        discordStack = trace.split('\n')
        backlog = self.discord_except_backlog
        if backlog > len(discordStack):
            backlog = len(discordStack)
        discordStack = discordStack[-backlog:]
        discordStacktrace = '%s\n' % str(exception)
        for stack in discordStack:
            discordStacktrace += '%s\n' % stack

        hookMessage = '@everyone' if self.want_everyone else ''
        webhookMessage = SlackWebhook(self.exception_log_url, message=hookMessage)
        attachment = SlackAttachment(title=headerMessage)

        attachment.addField(SlackField(title='Trackback', value=discordStacktrace))

        # Attempt to attach avatar information
        self.__attemptAttachAvatarInfo(attachment, avatarId, accountId)
 
        webhookMessage.addAttachment(attachment)
        self.__sendWebhook(webhookMessage, self.want_exception_logs)

    def logGenericMessage(self, url, message, author=None, avatar=None, verify=True):
        """
        Sends a basic message to Discord
        Avatar must be a valid URL image
        """
        webHookMessage = GenericWebhook(url, message, author, avatar=avatar)
        self.__sendWebhook(webHookMessage, verify)

    def logHolidayMessage(self, holidayId):
        """
        Logs a holiday message to Discord
        """

        if self.want_holiday_logs and len(self.holiday_log_urls) == 0:
            self.notify.warning('Failed to send holiday webhook; No holiday webhook urls defined!')
            return

        baseMessage = HolidayGlobals.getHolidayDiscordMessage(holidayId)
        hookMessage = '@everyone ' + baseMessage if self.want_everyone else baseMessage

        for endpoint in self.holiday_log_urls:
            webhookMessage = SlackWebhook(endpoint, message=hookMessage)
            attachment = SlackAttachment(
                pretext=HolidayGlobals.getHolidayDiscordPrefixMessage(holidayId), 
                title=HolidayGlobals.getHolidayDiscordName(holidayId),
                image_url=HolidayGlobals.getHolidayDiscordImage(holidayId),
                footer=HolidayGlobals.getHolidayDiscordDates(holidayId)
            )

            webhookMessage.addAttachment(attachment)
            self.__sendWebhook(webhookMessage, self.want_holiday_logs)