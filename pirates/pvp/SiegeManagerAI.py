
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class SiegeManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('SiegeManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.pvpEnabled = False
        self.teamsJoinable = []
        self.useIslandRegen = False
        self.useRepairSpots = False
        self.useRepairKit = False


    # setPvpEnabled(bool) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setPvpEnabled(self, pvpEnabled):
        self.pvpEnabled = pvpEnabled

    def d_setPvpEnabled(self, pvpEnabled):
        self.sendUpdate('setPvpEnabled', [pvpEnabled])

    def b_setPvpEnabled(self, pvpEnabled):
        self.setPvpEnabled(pvpEnabled)
        self.d_setPvpEnabled(pvpEnabled)

    def getPvpEnabled(self):
        return self.pvpEnabled

    # setTeamsJoinable(pvpTeamJoinableItem []) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setTeamsJoinable(self, teamsJoinable):
        self.teamsJoinable = teamsJoinable

    def d_setTeamsJoinable(self, teamsJoinable):
        self.sendUpdate('setTeamsJoinable', [teamsJoinable])

    def b_setTeamsJoinable(self, teamsJoinable):
        self.setTeamsJoinable(teamsJoinable)
        self.d_setTeamsJoinable(teamsJoinable)

    def getTeamsJoinable(self):
        return self.teamsJoinable

    # setUseIslandRegen(bool) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setUseIslandRegen(self, useIslandRegen):
        self.useIslandRegen = useIslandRegen

    def d_setUseIslandRegen(self, useIslandRegen):
        self.sendUpdate('setUseIslandRegen', [useIslandRegen])

    def b_setUseIslandRegen(self, useIslandRegen):
        self.setUseIslandRegen(useIslandRegen)
        self.d_setUseIslandRegen(useIslandRegen)

    def getUseIslandRegen(self):
        return self.useIslandRegen

    # setUseRepairSpots(bool) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setUseRepairSpots(self, useRepairSpots):
        self.useRepairSpots = useRepairSpots

    def d_setUseRepairSpots(self, useRepairSpots):
        self.sendUpdate('setUseRepairSpots', [useRepairSpots])

    def b_setUseRepairSpots(self, useRepairSpots):
        self.setUseRepairSpots(useRepairSpots)
        self.d_setUseRepairSpots(useRepairSpots)

    def getUseRepairSpots(self):
        return self.useRepairSpots

    # setUseRepairKit(bool) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setUseRepairKit(self, useRepairKit):
        self.useRepairKit = useRepairKit

    def d_setUseRepairKit(self, useRepairKit):
        self.sendUpdate('setUseRepairKit', [useRepairKit])

    def b_setUseRepairKit(self, useRepairKit):
        self.setUseRepairKit(useRepairKit)
        self.d_setUseRepairKit(useRepairKit)

    def getUseRepairKit(self):
        return self.useRepairKit

    # sendChat(string, uint8, uint32) airecv clsend

    def sendChat(self, sendChat, todo_uint8_1, todo_uint32_2):
        pass

    # sendWLChat(string, uint8, uint32) airecv clsend

    def sendWLChat(self, sendWLChat, todo_uint8_1, todo_uint32_2):
        pass

    # sendSC(uint16) airecv clsend

    def sendSC(self, sendSC):
        pass

    # recvChat(uint32, string, uint8, uint32, string)

    def recvChat(self, recvChat, todo_string_1, todo_uint8_2, todo_uint32_3, todo_string_4):
        self.sendUpdate('recvChat', [recvChat, todo_string_1, todo_uint8_2, todo_uint32_3, todo_string_4])

    # recvWLChat(uint32, string, uint8, uint32, string)

    def recvWLChat(self, recvWLChat, todo_string_1, todo_uint8_2, todo_uint32_3, todo_string_4):
        self.sendUpdate('recvWLChat', [recvWLChat, todo_string_1, todo_uint8_2, todo_uint32_3, todo_string_4])

    # recvSpeedChat(uint32, uint16, string)

    def recvSpeedChat(self, recvSpeedChat, todo_uint16_1, todo_string_2):
        self.sendUpdate('recvSpeedChat', [recvSpeedChat, todo_uint16_1, todo_string_2])


