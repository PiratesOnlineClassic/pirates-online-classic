# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.web.PiratesSettingsMgr
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.web.SettingsMgr import SettingsMgr
from pirates.web.PiratesSettingsMgrBase import PiratesSettingsMgrBase


class PiratesSettingsMgr(SettingsMgr, PiratesSettingsMgrBase):
    __module__ = __name__
    notify = directNotify.newCategory('PiratesSettingsMgr')

    def _initSettings(self):
        SettingsMgr._initSettings(self)
        PiratesSettingsMgrBase._initSettings(self)
# okay decompiling .\pirates\web\PiratesSettingsMgr.pyc
