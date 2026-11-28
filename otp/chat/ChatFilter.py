"""
Server side chat rules shared by the AI and UberDOG.

The client does its own whitelist substitution and only ever offers SpeedChat
phrases out of the localizer, but a modified client can send anything. Every
place the server relays chat runs it through here first so that what reaches
the other clients is something a real client could have sent.
"""

import time
import collections

from panda3d.core import ConfigVariableInt, ConfigVariableDouble, ConfigVariableString
from panda3d.core import Filename, VirtualFileSystem, getModelPath
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from otp.chat.WhiteList import WhiteList

notify = DirectNotifyGlobal.directNotify.newCategory('ChatFilter')

# Longest message the server will relay. The client's typed entry tops out
# well below this (one line plus 100 characters of sliding window).
MaxChatLength = 255

# The word the client's whitelist entry puts in place of a word it doesn't know.
WhiteListDefaultWord = 'arrr'

# The client chat flags (libotp ChatFlags) a player is allowed to send with
# typed chat. Anything else (quicktalker, page and quit buttons...) is only
# ever set locally.
CFSpeech = 1
CFThought = 2
CFTimeout = 8
AllowedChatFlags = CFSpeech | CFThought | CFTimeout

# The boot code the client describes as a problem with the account's
# authorization to use keyboard chat.
ChatBootCode = 120

_whiteList = None
_whiteListLoaded = False


def setWhiteList(whiteList):
    global _whiteList, _whiteListLoaded
    _whiteList = whiteList
    _whiteListLoaded = True


def getWhiteList():
    """
    Returns the whitelist the client ships (pwhitelist.txt), or None if the
    resources can't be found on the model path.
    """

    global _whiteList, _whiteListLoaded
    if _whiteListLoaded:
        return _whiteList

    _whiteListLoaded = True
    filename = Filename(ConfigVariableString('chat-whitelist-file', 'phase_3/etc/pwhitelist.txt').getValue())
    vfs = VirtualFileSystem.getGlobalPtr()
    if not vfs.resolveFilename(filename, getModelPath().getValue()):
        notify.warning("Couldn't find the whitelist %s, whitelist chat will not be filtered!" % filename)
        return None

    data = vfs.readFile(filename, 1)
    if isinstance(data, bytes):
        data = data.decode('latin-1')

    _whiteList = WhiteList(data.split('\n'))
    notify.info('Loaded %d whitelist words.' % _whiteList.numWords)
    return _whiteList


def cleanMessage(message):
    """
    Returns the message ready to relay, or None if it shouldn't be relayed at
    all. Control characters are removed since the client uses them to switch
    text properties and a typed entry can't produce them.
    """

    if len(message) > MaxChatLength:
        return None

    message = ''.join(char for char in message if char >= ' ' and char != '\x7f')
    message = message.strip()
    if not message:
        return None

    return message


def filterWhiteList(message, whiteList=None):
    """
    Replaces every word that isn't on the whitelist the same way the client's
    whitelist entry does before it sends.
    """

    if whiteList is None:
        whiteList = getWhiteList()
        if whiteList is None:
            return message

    words = []
    for word in message.split(' '):
        if word == '' or whiteList.isWord(word):
            words.append(word)
        else:
            words.append(WhiteListDefaultWord)

    return ' '.join(words)


def isWhiteListed(message, whiteList=None):
    return filterWhiteList(message, whiteList) == message


def cleanChatFlags(chatFlags):
    return chatFlags & AllowedChatFlags


def isValidSpeedChat(msgIndex):
    return msgIndex in OTPLocalizer.SpeedChatStaticText


def isValidSpeedChatCustom(msgIndex):
    return msgIndex in OTPLocalizer.CustomSCStrings


def isValidSpeedChatEmote(emoteId):
    return 0 <= emoteId < len(OTPLocalizer.EmoteWhispers)


class ChatFlood:
    """
    Keeps track of how often each avatar has chatted recently, so a client
    spamming chat can be cut off instead of every message being relayed.
    """

    def __init__(self, limit=None, window=None):
        if limit is None:
            limit = ConfigVariableInt('chat-flood-limit', 8).getValue()

        if window is None:
            window = ConfigVariableDouble('chat-flood-window', 5.0).getValue()

        self.limit = limit
        self.window = window
        self.history = {}
        self.warned = set()

    def isFlooding(self, avatarId, now=None):
        """
        Records a chat message from the avatar and returns True if it's over
        the limit and should be dropped.
        """

        if self.limit <= 0:
            return False

        if now is None:
            now = time.monotonic()

        history = self.history.setdefault(avatarId, collections.deque())
        while history and now - history[0] >= self.window:
            history.popleft()

        if len(history) >= self.limit:
            return True

        history.append(now)
        self.warned.discard(avatarId)
        return False

    def shouldWarn(self, avatarId):
        """
        Returns True the first time an avatar floods in a row, so that a spammer
        doesn't also flood the logs.
        """

        if avatarId in self.warned:
            return False

        self.warned.add(avatarId)
        return True

    def clear(self, avatarId):
        self.history.pop(avatarId, None)
        self.warned.discard(avatarId)
