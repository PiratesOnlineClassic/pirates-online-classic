
from pirates.instance.DistributedInstanceWorldAI import DistributedInstanceWorldAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPVPInstanceAI(DistributedInstanceWorldAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPVPInstanceAI')

    def __init__(self, air):
        DistributedInstanceWorldAI.__init__(self, air)


    # setAvatarReady() airecv clsend

    def setAvatarReady(self, avatarReady):
        pass

    # setMatchPlayers(playerInfo []) broadcast ram

    def setMatchPlayers(self, matchPlayers):
        self.sendUpdate('setMatchPlayers', [matchPlayers])

    # setGameStart(int16) broadcast

    def setGameStart(self, gameStart):
        self.sendUpdate('setGameStart', [gameStart])

    # setPlayerStat(uint32, uint8, int32) broadcast

    def setPlayerStat(self, playerStat, todo_uint8_1, todo_int32_2):
        self.sendUpdate('setPlayerStat', [playerStat, todo_uint8_1, todo_int32_2])

    # setStats(playerStats []) broadcast ram

    def setStats(self, stats):
        self.sendUpdate('setStats', [stats])

    # setResults(playerStats [], uint16, uint8, bool)

    def setResults(self, results, todo_uint16_1, todo_uint8_2, todo_bool_3):
        self.sendUpdate('setResults', [results, todo_uint16_1, todo_uint8_2, todo_bool_3])

    # setPVPComplete() broadcast

    def setPVPComplete(self, pVPComplete):
        self.sendUpdate('setPVPComplete', [pVPComplete])

    # requestLeave() airecv clsend

    def requestLeave(self, requestLeave):
        pass

    # performAILeave()

    def performAILeave(self, performAILeave):
        self.sendUpdate('performAILeave', [performAILeave])

    # requestLeaveApproved()

    def requestLeaveApproved(self, requestLeaveApproved):
        self.sendUpdate('requestLeaveApproved', [requestLeaveApproved])

    # setPvpEvent(uint8, uint32 []) broadcast

    def setPvpEvent(self, pvpEvent, todo_uint32_1):
        self.sendUpdate('setPvpEvent', [pvpEvent, todo_uint32_1])


