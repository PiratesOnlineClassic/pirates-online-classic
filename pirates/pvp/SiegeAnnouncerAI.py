
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class SiegeAnnouncerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('SiegeAnnouncerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)


    # announceSink(uint8, string, uint8, string) broadcast

    def announceSink(self, announceSink, todo_string_1, todo_uint8_2, todo_string_3):
        self.sendUpdate('announceSink', [announceSink, todo_string_1, todo_uint8_2, todo_string_3])

    # announceSinkWithAssist(uint8, string, uint8, string, uint8, string) broadcast

    def announceSinkWithAssist(self, announceSinkWithAssist, todo_string_1, todo_uint8_2, todo_string_3, todo_uint8_4, todo_string_5):
        self.sendUpdate('announceSinkWithAssist', [announceSinkWithAssist, todo_string_1, todo_uint8_2, todo_string_3, todo_uint8_4, todo_string_5])

    # announceSinkStreak(uint8, string, uint32) broadcast

    def announceSinkStreak(self, announceSinkStreak, todo_string_1, todo_uint32_2):
        self.sendUpdate('announceSinkStreak', [announceSinkStreak, todo_string_1, todo_uint32_2])


