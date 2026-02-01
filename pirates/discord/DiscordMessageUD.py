from direct.directnotify.DirectNotifyGlobal import *

from pirates.discord import DiscordGlobalsUD

import json

class DiscordEmbeded:
    """
    Represents the embedded field of a bot message
    """

    def __init__(self):
        self.title = ''
        self.type = 'rich'
        self.description = ''
        self.url = ''
        self.timestamp = None
        self.color = 0
        self.fields = {}
        self.image = None
        self.footer = None

    def setFooter(self, text, icon_url=None, proxy_icon_url=None):
        self.footer = {}
        self.footer['text'] = text

        if icon_url:
            self.footer['icon_url'] = icon_url

        if proxy_icon_url:
            self.footer['proxy_icon_url'] = proxy_icon_url

    def setImage(self, url, proxyUrl=None, width=None, height=None):
        self.image = {}
        self.image['url'] = url

        if proxyUrl:
            self.image['proxyUrl'] = proxyUrl
    
        if width:
            self.image['width'] = width

        if height:
            self.image['height'] = height

    def setField(self, name, value=None, inline=True):
        if value == None and name in self.fields:
            del self.fields[name]

        field = {
            'name': name,
            'value': value,
            'inline': inline
        }
        self.fields[name] = field

    def build(self):
        data = {
            'title': self.title,
            'type': self.type,
            'description': self.description,
            'url': self.url,
            'color': self.color,
            'fields': list(self.fields.values())
        }

        if self.timestamp:
            data['timestamp'] = self.timestamp

        if self.image:
            data['image'] = self.image

        if self.footer:
            data['footer'] = self.footer

        return data

class DiscordMessageUD:
    """
    Represents a sendable bot message
    """

    notify = directNotify.newCategory('DiscordMessageUD')
    notify.setInfo(True)

    def __init__(self, air):
        self.air = air
        self.content = ''
        self.tts = False
        self.embedded = None

    def send(self, channel):
        """
        Sends the message to the Discord channel
        """

        headers = {
            'User-Agent': 'UberDOG UserAgent',
            'Authorization': DiscordGlobalsUD.BotAuthorization
        }

        messageBody = {
            'content': self.content,
            'tts': self.tts
        }
        
        if self.embedded:
            messageBody['embed'] = self.embedded.build()

        def processResults(results):
            self.notify.debug('Results: %s' % results)
            if 'code' in results and results.get('code', 0) != 200:
                self.notify.warning('Failed to send Discord message. %s' % results.get('message', 'Undefined'))
            else:
                self.notify.debug('Discord message sent.')
                self.air.writeServerEvent('discord-message-sent',
                    resdults=results,
                    channel=channel,
                    messageBody=messageBody)

        self.notify.info('Sending Discord message to channel: %s' % channel)
        self.air.rest.performJsonPostRequest(
            url=DiscordGlobalsUD.getChannelMessageUrl(channel),
            headers=headers,
            post_body=messageBody,
            callback=processResults)