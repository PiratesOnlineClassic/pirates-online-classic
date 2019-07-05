from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.web.SettingsMgrBase import SettingsMgrBase

class SettingsMgrAI(DistributedObjectGlobalAI, SettingsMgrBase):
    notify = directNotify.newCategory('SettingsMgrAI')
    notify.setInfo(True)

    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)
        SettingsMgrBase.announceGenerate(self)
        self.notify.info('SettingsManager going online')
        self.d_requestAllUberDOGSettings()

    def delete(self):        
        SettingsMgrBase.delete(self)
        DistributedObjectGlobalAI.delete(self)
    
    def requestAllChangedSettings(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())
        if not avatar:
            self.notify.warning('Received changed settings request from unknown source')
            return 
        
        for settingName in self._settings:
            valueStr = self._getSetting(settingName)
            self.sendUpdateToAvatarId(avatar.doId, 'settingChange', [settingName, valueStr])
    
    def settingChange(self, settingName, valueStr):
        if valueStr == self._getCurrentValueRepr(settingName):
            return
        
        self.notify.info('changed setting change: %s -> %s' % (settingName, valueStr))
        self._changeSetting(settingName, valueStr)
        self.d_settingChange(settingName, valueStr)

    def d_requestAllUberDOGSettings(self):
        self.notify.info('Requesting latest settings from UberDOG')
        self.air.netMessenger.send('UberDOGSettingsRequest', [self.air.ourChannel])

    def d_settingChange(self, settingName, valueStr):
        self.sendUpdate('settingChange', [settingName, valueStr])