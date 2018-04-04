
from pirates.battle.DistributedWeaponAI import DistributedWeaponAI
from direct.directnotify import DirectNotifyGlobal

class DistributedShipBroadsideAI(DistributedWeaponAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipBroadsideAI')

    def __init__(self, air):
        DistributedWeaponAI.__init__(self, air)
        self.shipId = 0
        self.geomParentId = 0
        self.leftBroadside = 0
        self.rightBroadside = 0
        self.leftBroadsideEnabledState = 0
        self.rightBroadsideEnabledState = 0
        self.baseTeam = 0
        self.ammoType = 0


    # requestBroadside(uint8, uint8/100 [], PosList, uint32, uint8) airecv clsend

    def requestBroadside(self, requestBroadside, todo_uint8_100_1, todo_PosList_2, todo_uint32_3, todo_uint8_4):
        pass

    # doBroadside(uint8, uint8/100 [], PosList, uint32, uint8, int16) broadcast

    def doBroadside(self, doBroadside, todo_uint8_100_1, todo_PosList_2, todo_uint32_3, todo_uint8_4, todo_int16_5):
        self.sendUpdate('doBroadside', [doBroadside, todo_uint8_100_1, todo_PosList_2, todo_uint32_3, todo_uint8_4, todo_int16_5])

    # setShipId(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setShipId(self, shipId):
        self.shipId = shipId

    def d_setShipId(self, shipId):
        self.sendUpdate('setShipId', [shipId])

    def b_setShipId(self, shipId):
        self.setShipId(shipId)
        self.d_setShipId(shipId)

    def getShipId(self):
        return self.shipId

    # setGeomParentId(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setGeomParentId(self, geomParentId):
        self.geomParentId = geomParentId

    def d_setGeomParentId(self, geomParentId):
        self.sendUpdate('setGeomParentId', [geomParentId])

    def b_setGeomParentId(self, geomParentId):
        self.setGeomParentId(geomParentId)
        self.d_setGeomParentId(geomParentId)

    def getGeomParentId(self):
        return self.geomParentId

    # requestCannonEnabledState(uint8, uint8, uint8) airecv clsend

    def requestCannonEnabledState(self, requestCannonEnabledState, todo_uint8_1, todo_uint8_2):
        pass

    # setCannonAnim(uint8, uint8, uint8, int16) airecv clsend broadcast

    def setCannonAnim(self, cannonAnim, todo_uint8_1, todo_uint8_2, todo_int16_3):
        pass

    # setLeftBroadside(uint16array) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setLeftBroadside(self, leftBroadside):
        self.leftBroadside = leftBroadside

    def d_setLeftBroadside(self, leftBroadside):
        self.sendUpdate('setLeftBroadside', [leftBroadside])

    def b_setLeftBroadside(self, leftBroadside):
        self.setLeftBroadside(leftBroadside)
        self.d_setLeftBroadside(leftBroadside)

    def getLeftBroadside(self):
        return self.leftBroadside

    # setRightBroadside(uint16array) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setRightBroadside(self, rightBroadside):
        self.rightBroadside = rightBroadside

    def d_setRightBroadside(self, rightBroadside):
        self.sendUpdate('setRightBroadside', [rightBroadside])

    def b_setRightBroadside(self, rightBroadside):
        self.setRightBroadside(rightBroadside)
        self.d_setRightBroadside(rightBroadside)

    def getRightBroadside(self):
        return self.rightBroadside

    # setLeftBroadsideEnabledState(uint8 []) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setLeftBroadsideEnabledState(self, leftBroadsideEnabledState):
        self.leftBroadsideEnabledState = leftBroadsideEnabledState

    def d_setLeftBroadsideEnabledState(self, leftBroadsideEnabledState):
        self.sendUpdate('setLeftBroadsideEnabledState', [leftBroadsideEnabledState])

    def b_setLeftBroadsideEnabledState(self, leftBroadsideEnabledState):
        self.setLeftBroadsideEnabledState(leftBroadsideEnabledState)
        self.d_setLeftBroadsideEnabledState(leftBroadsideEnabledState)

    def getLeftBroadsideEnabledState(self):
        return self.leftBroadsideEnabledState

    # setRightBroadsideEnabledState(uint8 []) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setRightBroadsideEnabledState(self, rightBroadsideEnabledState):
        self.rightBroadsideEnabledState = rightBroadsideEnabledState

    def d_setRightBroadsideEnabledState(self, rightBroadsideEnabledState):
        self.sendUpdate('setRightBroadsideEnabledState', [rightBroadsideEnabledState])

    def b_setRightBroadsideEnabledState(self, rightBroadsideEnabledState):
        self.setRightBroadsideEnabledState(rightBroadsideEnabledState)
        self.d_setRightBroadsideEnabledState(rightBroadsideEnabledState)

    def getRightBroadsideEnabledState(self):
        return self.rightBroadsideEnabledState

    # setBaseTeam(int8) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setBaseTeam(self, baseTeam):
        self.baseTeam = baseTeam

    def d_setBaseTeam(self, baseTeam):
        self.sendUpdate('setBaseTeam', [baseTeam])

    def b_setBaseTeam(self, baseTeam):
        self.setBaseTeam(baseTeam)
        self.d_setBaseTeam(baseTeam)

    def getBaseTeam(self):
        return self.baseTeam

    # setAmmoType(SkillId) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAmmoType(self, ammoType):
        self.ammoType = ammoType

    def d_setAmmoType(self, ammoType):
        self.sendUpdate('setAmmoType', [ammoType])

    def b_setAmmoType(self, ammoType):
        self.setAmmoType(ammoType)
        self.d_setAmmoType(ammoType)

    def getAmmoType(self):
        return self.ammoType


