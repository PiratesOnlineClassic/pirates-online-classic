import string
import types

from panda3d.core import *

try:
    language = ConfigVariableString('language', 'english').getValue()
    checkLanguage = ConfigVariableBool('check-language', False).getValue()
except BaseException:
    language = simbase.config.GetString('language', 'english')
    checkLanguage = simbase.config.GetBool('check-language', False)
else:
    print 'OTPLocalizer: Running in language: %s' % language
    if language != 'english':
        checkLanguage = 1
        _languageModule = 'otp.otpbase.OTPLocalizer_' + language
    else:
        _languageModule = 'otp.otpbase.OTPLocalizer' + \
            string.capitalize(language)
    exec 'from ' + _languageModule + ' import *'

    def getLanguage():
        return language

    if checkLanguage:
        l = {}
        g = {}
        englishModule = __import__('otp.otpbase.OTPLocalizerEnglish', g, l)
        foreignModule = __import__(_languageModule, g, l)
        for key, val in englishModule.__dict__.items():
            if key not in foreignModule.__dict__:
                print 'WARNING: Foreign module: %s missing key: %s' % (
                    _languageModule, key)
                locals()[key] = val
            elif isinstance(val, types.DictType):
                fval = foreignModule.__dict__.get(key)
                for dkey, dval in val.items():
                    if dkey not in fval:
                        print 'WARNING: Foreign module: %s missing key: %s.%s' % (
                            _languageModule, key, dkey)
                        fval[dkey] = dval

                for dkey in fval.keys():
                    if dkey not in val:
                        print 'WARNING: Foreign module: %s extra key: %s.%s' % (
                            _languageModule, key, dkey)

        for key in foreignModule.__dict__.keys():
            if key not in englishModule.__dict__:
                print 'WARNING: Foreign module: %s extra key: %s' % (
                    _languageModule, key)
