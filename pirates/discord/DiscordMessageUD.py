from direct.directnotify.DirectNotifyGlobal import *

from pirates.discord import DiscordGlobalsUD

class DiscordEmbeded:
    """
    Represents the embedded field of a bot message
    """

class DiscordMessageUD:
    """
    Represents a sendable bot message
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('DiscordMessageUD')

    def __init__(self, air):
        self.air = air
        self.content = ''
        self.nonce = 0
        self.tts = False
        self.file = None
        self.embeded = None

    def send(self, channel):
        """
        Sends the message to the Discord channel
        """

        headers = {
            'User-Agent': 'PiratesClassic UserAgent',
            'Authorization': DiscordGlobalsUD.BotAuthorization
        }

        