
from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBattleNPCAI(DistributedBattleAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleNPCAI')

    def __init__(self, air):
        DistributedBattleAvatarAI.__init__(self, air)
        self.name = ''
        self.spawnPos = [0, 0, 0]
        self.animSet = ''
        self.collisionMode = 0
        self.initZ = 0


    # setName(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    # setSpawnPos(int16/10, int16/10, int16/10) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setSpawnPos(self, spawnPos, todo_int16_10_1, todo_int16_10_2):
        self.spawnPos = spawnPos

    def d_setSpawnPos(self, spawnPos, todo_int16_10_1, todo_int16_10_2):
        self.sendUpdate('setSpawnPos', [spawnPos, todo_int16_10_1, todo_int16_10_2])

    def b_setSpawnPos(self, spawnPos, todo_int16_10_1, todo_int16_10_2):
        self.setSpawnPos(spawnPos, todo_int16_10_1, todo_int16_10_2)
        self.d_setSpawnPos(spawnPos, todo_int16_10_1, todo_int16_10_2)

    def getSpawnPos(self):
        return self.spawnPos

    # setAmbush(uint8) broadcast ram

    def setAmbush(self, ambush):
        self.sendUpdate('setAmbush', [ambush])

    # ambushIntroDone() airecv clsend

    def ambushIntroDone(self, ambushIntroDone):
        pass

    # boardVehicle(uint32) broadcast ram

    def boardVehicle(self, boardVehicle):
        self.sendUpdate('boardVehicle', [boardVehicle])

    # setSpawnIn(int32) broadcast ram

    def setSpawnIn(self, spawnIn):
        self.sendUpdate('setSpawnIn', [spawnIn])

    # setChat(string, uint8) broadcast ownsend

    def setChat(self, chat, todo_uint8_1):
        self.sendUpdate('setChat', [chat, todo_uint8_1])

    # setAnimSet(string) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAnimSet(self, animSet):
        self.animSet = animSet

    def d_setAnimSet(self, animSet):
        self.sendUpdate('setAnimSet', [animSet])

    def b_setAnimSet(self, animSet):
        self.setAnimSet(animSet)
        self.d_setAnimSet(animSet)

    def getAnimSet(self):
        return self.animSet

    # setCollisionMode(uint8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setCollisionMode(self, collisionMode):
        self.collisionMode = collisionMode

    def d_setCollisionMode(self, collisionMode):
        self.sendUpdate('setCollisionMode', [collisionMode])

    def b_setCollisionMode(self, collisionMode):
        self.setCollisionMode(collisionMode)
        self.d_setCollisionMode(collisionMode)

    def getCollisionMode(self):
        return self.collisionMode

    # setInitZ(int16/10) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setInitZ(self, initZ):
        self.initZ = initZ

    def d_setInitZ(self, initZ):
        self.sendUpdate('setInitZ', [initZ])

    def b_setInitZ(self, initZ):
        self.setInitZ(initZ)
        self.d_setInitZ(initZ)

    def getInitZ(self):
        return self.initZ

    # requestClientAggro() airecv clsend

    def requestClientAggro(self, requestClientAggro):
        pass


