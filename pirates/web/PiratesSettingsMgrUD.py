
from otp.web.SettingsMgrUD import SettingsMgrUD
from direct.directnotify import DirectNotifyGlobal

class PiratesSettingsMgrUD(SettingsMgrUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesSettingsMgrUD')

    def __init__(self, air):
        SettingsMgrUD.__init__(self, air)



