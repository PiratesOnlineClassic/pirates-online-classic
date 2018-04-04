
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class SettingsMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('SettingsMgrAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # requestAllChangedSettings() airecv clsend

    def requestAllChangedSettings(self, requestAllChangedSettings):
        pass

    # settingChange(string, string) airecv

    def settingChange(self, tingChange, todo_string_1):
        pass


