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

    def restoreDefaults(self):
        """
        Summary:
            Restores the original default values on the UberDOG
        """

        settingsMgr = self.air.settingsMgr
        settingsMgr.restoreDefaults()

        return self._formatResults()

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
        Example response:
            original=5000, new=5001
        """

        settingsMgr = self.air.settingsMgr
        original = settingsMgr.getSettingFromName(settingName)
        if not original:
            return self._formatResults(
                code=ResponseCodes.INVALID_ARGUMENT,
                message='Invalid setting name')
        
        settingsMgr.settingChange(settingName, str(valueStr))
        return self._formatResults(original=original.getValue(), new=valueStr)