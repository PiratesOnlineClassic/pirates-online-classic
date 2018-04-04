
from otp.web.SettingsMgrAI import SettingsMgrAI
from direct.directnotify import DirectNotifyGlobal

class PiratesSettingsMgrAI(SettingsMgrAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesSettingsMgrAI')

    def __init__(self, air):
        SettingsMgrAI.__init__(self, air)



