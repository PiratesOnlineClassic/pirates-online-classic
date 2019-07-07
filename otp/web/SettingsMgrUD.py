    
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.web.SettingsMgrBase import SettingsMgrBase

class SettingsMgrUD(DistributedObjectGlobalUD, SettingsMgrBase):
    notify = directNotify.newCategory('SettingsMgrUD')
    notify.setInfo(True)

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        SettingsMgrBase.announceGenerate(self)
        self.notify.info('SettingsManager going online')

        self.air.netMessenger.accept('UberDOGSettingsRequest', self, self.handleUberDOGSettingsRequest)

    def delete(self):        
        SettingsMgrBase.delete(self)
        DistributedObjectGlobalUD.delete(self)

    def settingChange(self, settingName, valueStr):
        if valueStr == self._getCurrentValueRepr(settingName):
            return
        
        self.notify.info('changed setting change: %s -> %s' % (settingName, valueStr))
        self._changeSetting(settingName, valueStr)
        self.d_settingChange(settingName, valueStr)

    def handleUberDOGSettingsRequest(self, channel):
        for settingName in self._settings:
            valueStr = str(self._settings[settingName].getValue())
            self.d_settingChangeToChannel(channel, settingName, valueStr)

    def d_settingChange(self, settingName, valueStr):
        self.sendUpdate('settingChange', [settingName, valueStr])

    def d_settingChangeToChannel(self, channel, settingName, valueStr):
        self.sendUpdateToChannel(channel, 'settingChange', [settingName, valueStr])

    def getSettingValueFromName(self, settingName):
        setting = self._settings.get(settingName)
        if not setting:
            return None
        return setting.getValue()

    def getSettingFromInstance(self, settingInstance):
        settingName = settingInstance.getName()
        return self.getSettingValueFromName(settingName)