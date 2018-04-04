
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PVPGameBaseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameBaseAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.instanceId = 0


    # setAvatarReady() airecv clsend

    def setAvatarReady(self, avatarReady):
        pass

    # allPresent(uint32 []) broadcast

    def allPresent(self, allPresent):
        self.sendUpdate('allPresent', [allPresent])

    # setPlayerStat(uint32, uint8, int32) broadcast

    def setPlayerStat(self, playerStat, todo_uint8_1, todo_int32_2):
        self.sendUpdate('setPlayerStat', [playerStat, todo_uint8_1, todo_int32_2])

    # setStats(playerStats []) broadcast ram

    def setStats(self, stats):
        self.sendUpdate('setStats', [stats])

    # setResults(playerStats [], int32)

    def setResults(self, results, todo_int32_1):
        self.sendUpdate('setResults', [results, todo_int32_1])

    # setGameStart(int16) broadcast

    def setGameStart(self, gameStart):
        self.sendUpdate('setGameStart', [gameStart])

    # setGameExit() broadcast

    def setGameExit(self, gameExit):
        self.sendUpdate('setGameExit', [gameExit])

    # setGameAbort() broadcast

    def setGameAbort(self, gameAbort):
        self.sendUpdate('setGameAbort', [gameAbort])

    # setInstanceId(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setInstanceId(self, instanceId):
        self.instanceId = instanceId

    def d_setInstanceId(self, instanceId):
        self.sendUpdate('setInstanceId', [instanceId])

    def b_setInstanceId(self, instanceId):
        self.setInstanceId(instanceId)
        self.d_setInstanceId(instanceId)

    def getInstanceId(self):
        return self.instanceId

    # setPvpEvent(uint8, uint32 []) broadcast

    def setPvpEvent(self, pvpEvent, todo_uint32_1):
        self.sendUpdate('setPvpEvent', [pvpEvent, todo_uint32_1])


