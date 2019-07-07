from direct.directnotify.DirectNotifyGlobal import directNotify

from otp.web.SettingsMgrUD import SettingsMgrUD
from otp.web.Setting import Setting

from pirates.web.PiratesSettingsMgrBase import PiratesSettingsMgrBase
from pirates.web.RPCGlobals import rpcservice, ResponseCodes
from pirates.web.RPCServiceUD import RPCServiceUD

class PiratesSettingsMgrUD(SettingsMgrUD, PiratesSettingsMgrBase):
    notify = directNotify.newCategory('PiratesSettingsMgrUD')
    notify.setInfo(True)
    
    def _initSettings(self):
        SettingsMgrUD._initSettings(self)
        PiratesSettingsMgrBase._initSettings(self)

@rpcservice(serviceName='settingsMgr')
class SettingsService(RPCServiceUD):
    """
    Handles all cluster web settings for the RPC
    """

    def getSettings(self):
        """
        Summary:
            Responds with all the currently configured settings for the cluster
        Example response: 
            'settings': {'test': 'hello world'}
        """

        results = {}
        settingsMgr = self.air.settingsMgr
        settings = settingsMgr.getSettings()
        for settingKey in settings:
            setting = settings[settingKey]
            if isinstance(setting, Setting):
                settingValue = setting.getValue()
            else:
                settingValue = setting
            results[settingKey] = settingValue

        return self._formatResults(settings=results)

    def setSetting(self, settingName, valueStr):
        """
        Summary:
            Changes a currently configured setting on the cluster
        Parameters:
            [str settingName] = The settings key to change
            [str valueStr] = The value to assign to the settings key
        """

        settingsMgr = self.air.settingsMgr
        settingsMgr.settingChange(settingName, str(valueStr))

        return self._formatResults()