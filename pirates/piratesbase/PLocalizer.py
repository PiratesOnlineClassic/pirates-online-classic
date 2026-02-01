from panda3d.core import *
import string
import types

try:
    language = ConfigVariableString('language', 'english').getValue()
    checkLanguage = ConfigVariableBool('check-language', 1).getValue()
except:
    language = 'english'
    checkLanguage = 1


def getLanguage():
    return language

print('PLocalizer: Running in language: %s' % language)
_languageModule = 'pirates.piratesbase.PLocalizer' + language.capitalize()
_questStringModule = 'pirates.piratesbase.PQuestStrings' + language.capitalize()
_greetingStringModule = 'pirates.piratesbase.PGreetingStrings' + language.capitalize()
exec('from ' + _languageModule + ' import *')
exec('from ' + _questStringModule + ' import *')
exec('from ' + _greetingStringModule + ' import *')
if checkLanguage:
    l = {}
    g = {}
    englishModule = __import__('pirates.piratesbase.PLocalizerEnglish', g, l)
    foreignModule = __import__(_languageModule, g, l)
    for (key, val) in list(englishModule.__dict__.items()):
        if key not in foreignModule.__dict__:
            print('WARNING: Foreign module: %s missing key: %s' % (_languageModule, key))
            locals()[key] = val

        elif isinstance(val, dict):
            fval = foreignModule.__dict__.get(key)
            for (dkey, dval) in list(val.items()):
                if dkey not in fval:
                    print('WARNING: Foreign module: %s missing key: %s.%s' % (_languageModule, key, dkey))
                    fval[dkey] = dval

            for dkey in list(fval.keys()):
                if dkey not in val:
                    print('WARNING: Foreign module: %s extra key: %s.%s' % (_languageModule, key, dkey))

    for key in list(foreignModule.__dict__.keys()):
        if key not in englishModule.__dict__:
            print('WARNING: Foreign module: %s extra key: %s' % (_languageModule, key))
