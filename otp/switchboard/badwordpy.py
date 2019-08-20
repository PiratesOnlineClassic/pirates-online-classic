import string
import sys
import os
import random
from bisect import bisect_left

from panda3d.core import *
from otp.otpbase import OTPLocalizer

wordList = ['']

def cleanText(text):
    text = text.strip('.,?!')
    text = text.lower()
    return text

def isWord(self, text):
    try:
        text = cleanText(text)
        i = bisect_left(wordList, text)
        if i == numWords:
            return False
        return wordList[i] == text
    except UnicodeDecodeError:
        return False

def test(message):
    modifications = []
    words = message.split(' ')
    offset = 0
    for word in words:
        if word and not isWord(word):
            modifications.append((offset, offset+len(word)-1))
        offset += len(word) + 1

    if len(modifications) > 0:
        return True
    return False

def garbleSingle(message):
    newMessage = ''
    numWords = 1
    wordlist = OTPLocalizer.ChatGarblerDefault
    for i in range(1, numWords + 1):
        wordIndex = random.randint(0, len(wordlist) - 1)
        newMessage = newMessage + wordlist[wordIndex]
        if i < numWords:
            newMessage = newMessage + ' '

    return newMessage

def scrubTalk(message, mods):
    scrubbed = 0
    text = copy.copy(message)
    for mod in mods:
        index = mod[0]
        length = mod[1] - mod[0] + 1
        newText = text[0:index] + length * '\x07' + text[index + length:]
        text = newText

    words = text.split(' ')
    newwords = []
    for word in words:
        if word == '':
            newwords.append(word)
        elif word[0] == '\x07' or len(word) > 1 and word[0] == '.' and word[1] == '\x07':
            newwords.append('\x01WLDisplay\x01' + garbleSingle(word) + '\x02')
            scrubbed = 1
        elif not isWord(word):
            newwords.append(word)
        else:
            scrubbed = 1
            newwords.append('\x01WLDisplay\x01' + word + '\x02')

    newText = ' '.join(newwords)
    return (newText, scrubbed)

def replaceBadWords(text):
    words = text.split(' ')
    newwords = []
    for word in words:
        if word == '':
            newwords.append(word)
        elif word[0] == '\x07':
            newwords.append('\x01WLRed\x01' + garbleSingle(word) + '\x02')
        elif not isWord(word):
            newwords.append(word)
        else:
            newwords.append('\x01WLRed\x01' + word + '\x02')

    newText = ' '.join(newwords)
    return newText

def scrub(message):
    modifications = []
    words = message.split(' ')
    offset = 0
    for word in words:
        if word and not isWord(word):
            modifications.append((offset, offset+len(word)-1))
        offset += len(word) + 1

    cleanMessage = message
    for modStart, modStop in modifications:
        cleanMessage = cleanMessage[:modStart] + '*'*(modStop-modStart+1) + cleanMessage[modStop+1:]

    message, scrubbed = scrubTalk(cleanMessage, modifications)
    return message
