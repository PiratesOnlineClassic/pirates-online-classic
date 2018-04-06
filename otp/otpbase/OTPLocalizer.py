# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.otpbase.OTPLocalizer
import string
import types

from panda3d.core import *

try:
    language = getConfigExpress().GetString('language', 'english')
    checkLanguage = getConfigExpress().GetBool('check-language', 0)
except:
    language = simbase.config.GetString('language', 'english')
    checkLanguage = simbase.config.GetBool('check-language', 0)
else:
    print 'OTPLocalizer: Running in language: %s' % language
    if language != 'english':
        checkLanguage = 1
        _languageModule = 'otp.otpbase.OTPLocalizer_' + language
    else:
        _languageModule = 'otp.otpbase.OTPLocalizer' + string.capitalize(language)
    exec 'from ' + _languageModule + ' import *'

    def getLanguage():
        return language


    if checkLanguage:
        l = {}
        g = {}
        englishModule = __import__('otp.otpbase.OTPLocalizerEnglish', g, l)
        foreignModule = __import__(_languageModule, g, l)
        for key, val in englishModule.__dict__.items():
            if not foreignModule.__dict__.has_key(key):
                print 'WARNING: Foreign module: %s missing key: %s' % (_languageModule, key)
                locals()[key] = val
            elif isinstance(val, types.DictType):
                fval = foreignModule.__dict__.get(key)
                for dkey, dval in val.items():
                    if not fval.has_key(dkey):
                        print 'WARNING: Foreign module: %s missing key: %s.%s' % (_languageModule, key, dkey)
                        fval[dkey] = dval

                for dkey in fval.keys():
                    if not val.has_key(dkey):
                        print 'WARNING: Foreign module: %s extra key: %s.%s' % (_languageModule, key, dkey)

        for key in foreignModule.__dict__.keys():
            if not englishModule.__dict__.has_key(key):
                print 'WARNING: Foreign module: %s extra key: %s' % (_languageModule, key)
# okay decompiling .\otp\otpbase\OTPLocalizer.pyc
