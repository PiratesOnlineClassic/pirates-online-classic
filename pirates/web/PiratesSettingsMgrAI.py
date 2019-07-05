from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.web.SettingsMgrAI import SettingsMgrAI
from pirates.web.PiratesSettingsMgrBase import PiratesSettingsMgrBase

class PiratesSettingsMgrAI(SettingsMgrAI, PiratesSettingsMgrBase):
    notify = directNotify.newCategory('PiratesSettingsMgrAI')
    notify.setInfo(True)

    def _initSettings(self):
        SettingsMgrAI._initSettings(self)
        PiratesSettingsMgrBase._initSettings(self)