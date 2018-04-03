# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.namepanel.NameCheck
import string
from otp.otpbase import OTPLocalizer
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import TextEncoder
notify = DirectNotifyGlobal.directNotify.newCategory('NameCheck')

def filterString(str, filter):
    result = ''
    for char in str:
        if char in filter:
            result = result + char

    return result


def wordList(str):
    words = str.split()
    result = []
    for word in words:
        subWords = word.split('-')
        for sw in subWords:
            if sw:
                result.append(sw)

    return result


def checkName(name, otherCheckFuncs=[]):

    def longEnough(name):
        if len(name) < 2:
            notify.info('name is too short')
            return OTPLocalizer.NCTooShort

    def emptyName(name):
        if name.strip() == '':
            notify.info('name is empty')
            return OTPLocalizer.NCTooShort

    def printableChars(name):
        for char in name:
            if ord(char) < 128 and char not in string.printable:
                notify.info('name contains non-printable char #%s' % ord(char))
                return OTPLocalizer.NCGeneric

    def badCharacters(name):
        okChars = ".,'-" + string.letters + string.whitespace
        allowUtf8Name = base.config.GetBool('allow-utf8-name', 1)
        for char in name:
            if ord(char) >= 128:
                if not allowUtf8Name:
                    notify.info('name contains utf-8 character.')
                    i = name.index(char)
                    if ord(char) >= 224:
                        char = char + name[i + 1] + name[i + 2]
                    else:
                        char = char + name[i + 1]
                    return OTPLocalizer.NCBadCharacter % char
            elif char not in okChars:
                if char in string.digits:
                    notify.info('name contains digits')
                    return OTPLocalizer.NCNoDigits
                else:
                    notify.info('name contains bad char: %s' % char)
                    return OTPLocalizer.NCBadCharacter % char

    def hasLetters(name):
        words = wordList(name)
        for word in words:
            hasUtf8 = 0
            for char in word:
                if ord(char) >= 128:
                    hasUtf8 = 1

            letters = filterString(word, string.letters)
            if len(letters) == 0 and not hasUtf8:
                notify.info('word "%s" has no letters' % word)
                return OTPLocalizer.NCNeedLetters

    def hasVowels(name):

        def perWord(word):
            if '.' in word:
                return
            for char in word:
                if ord(char) >= 128:
                    return

            letters = filterString(word, string.letters)
            if len(letters) > 2:
                vowels = filterString(letters, 'aeiouyAEIOUY')
                if len(vowels) == 0:
                    notify.info('word "%s" has no vowels' % word)
                    return OTPLocalizer.NCNeedVowels
            return

        for word in wordList(name):
            problem = perWord(word)
            if problem:
                return problem

    def monoLetter(name):

        def perWord(word):
            for char in word:
                if ord(char) >= 128:
                    return

            letters = filterString(word, string.letters)
            letters = TextEncoder.lower(letters)
            if len(letters) > 2:
                filtered = filterString(letters, letters[0])
                if filtered == letters:
                    notify.info('word "%s" uses only one letter' % word)
                    return OTPLocalizer.NCGeneric
            return

        for word in wordList(name):
            problem = perWord(word)
            if problem:
                return problem

    def checkDashes(name):

        def validDash(index, name=name):
            if index == 0 or i == len(name) - 1:
                return 0
            if name[i - 1] not in string.letters:
                return 0
            if name[i + 1] not in string.letters:
                return 0
            return 1

        i = 0
        while 1:
            i = name.find('-', i, len(name))
            if i < 0:
                return
            if not validDash(i):
                notify.info('name makes invalid use of dashes')
                return OTPLocalizer.NCDashUsage
            i += 1

        return

    def checkCommas(name):

        def validComma(index, name=name):
            if index == 0 or i == len(name) - 1:
                return OTPLocalizer.NCCommaEdge
            if name[i - 1] in string.whitespace:
                return OTPLocalizer.NCCommaAfterWord
            if name[i + 1] not in string.whitespace:
                return OTPLocalizer.NCCommaUsage
            return

        i = 0
        while 1:
            i = name.find(',', i, len(name))
            if i < 0:
                return
            problem = validComma(i)
            if problem:
                notify.info('name makes invalid use of commas')
                return problem
            i += 1

        return

    def checkPeriods(name):
        words = wordList(name)
        for word in words:
            if word[-1] == ',':
                word = word[:-1]
            numPeriods = word.count('.')
            if not numPeriods:
                continue
            letters = filterString(word, string.letters)
            numLetters = len(letters)
            if word[-1] != '.':
                notify.info('word "%s" does not end in a period' % word)
                return OTPLocalizer.NCPeriodUsage
            if numPeriods > 2:
                notify.info('word "%s" has too many periods' % word)
                return OTPLocalizer.NCPeriodUsage
            if numPeriods == 2:
                if not (word[1] == '.' and word[3] == '.'):
                    notify.info('word "%s" does not fit the J.T. pattern' % word)
                    return OTPLocalizer.NCPeriodUsage

        return

    def checkApostrophes(name):
        words = wordList(name)
        for word in words:
            numApos = word.count("'")
            if numApos > 2:
                notify.info('word "%s" has too many apostrophes.' % word)
                return OTPLocalizer.NCApostrophes

        numApos = name.count("'")
        if numApos > 3:
            notify.info('name has too many apostrophes.')
            return OTPLocalizer.NCApostrophes

    def tooManyWords(name):
        if len(wordList(name)) > 4:
            notify.info('name has too many words')
            return OTPLocalizer.NCTooManyWords

    def allCaps(name):
        letters = filterString(name, string.letters)
        if len(letters) > 2:
            if TextEncoder.upper(letters) == letters:
                notify.info('name is all caps')
                return OTPLocalizer.NCAllCaps

    def mixedCase(name):
        words = wordList(name)
        for word in words:
            if len(word) > 2:
                capitals = filterString(word, string.uppercase)
                if len(capitals) > 2:
                    notify.info('name has mixed case')
                    return OTPLocalizer.NCMixedCase

    def repeatedChars(name):
        count = 0
        lastChar = None
        i = 0
        while i < len(name):
            char = name[i]
            i += 1
            if ord(char) >= 128:
                char = char + name[i]
                i += 1
                if ord(char[0]) >= 224:
                    char = char + name[i]
                    i += 1
            if char == lastChar:
                count += 1
            else:
                count = 0
            lastChar = char
            if count > 1:
                notify.info('character %s is repeated too many times' % char)
                return OTPLocalizer.NCRepeatedChar % char

        return

    checks = [
     longEnough, emptyName, printableChars, badCharacters, hasLetters, hasVowels, monoLetter, checkDashes, checkCommas, checkPeriods, checkApostrophes, tooManyWords, allCaps, mixedCase, repeatedChars] + otherCheckFuncs
    symmetricChecks = []
    notify.info('checking name "%s"...' % name)
    for check in checks:
        problem = check(name[:])
        if not problem and check in symmetricChecks:
            te = TextEncoder()
            bName = te.decodeText(name)
            bName = list(bName)
            bName.reverse()
            bName = (u'').join(bName)
            bName = te.encodeWtext(bName)
            problem = check(bName)
            print 'problem = %s' % problem
        if problem:
            return problem

    return
# okay decompiling .\otp\namepanel\NameCheck.pyc
