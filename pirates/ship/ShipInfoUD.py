
from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class ShipInfoUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipInfoUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
        self.shipId = 0
        self.avatarId = 0
        self.name = ''
        self.hp = 0
        self.maxHp = 0
        self.sp = 0
        self.maxSp = 0
        self.locationName = 0
        self.activity = 0


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

    # setAvatarId(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setAvatarId(self, avatarId):
        self.avatarId = avatarId

    def d_setAvatarId(self, avatarId):
        self.sendUpdate('setAvatarId', [avatarId])

    def b_setAvatarId(self, avatarId):
        self.setAvatarId(avatarId)
        self.d_setAvatarId(avatarId)

    def getAvatarId(self):
        return self.avatarId

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

    # setHp(int16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setHp(self, hp):
        self.hp = hp

    def d_setHp(self, hp):
        self.sendUpdate('setHp', [hp])

    def b_setHp(self, hp):
        self.setHp(hp)
        self.d_setHp(hp)

    def getHp(self):
        return self.hp

    # setMaxHp(int16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def d_setMaxHp(self, maxHp):
        self.sendUpdate('setMaxHp', [maxHp])

    def b_setMaxHp(self, maxHp):
        self.setMaxHp(maxHp)
        self.d_setMaxHp(maxHp)

    def getMaxHp(self):
        return self.maxHp

    # setSp(int16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setSp(self, sp):
        self.sp = sp

    def d_setSp(self, sp):
        self.sendUpdate('setSp', [sp])

    def b_setSp(self, sp):
        self.setSp(sp)
        self.d_setSp(sp)

    def getSp(self):
        return self.sp

    # setMaxSp(int16) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setMaxSp(self, maxSp):
        self.maxSp = maxSp

    def d_setMaxSp(self, maxSp):
        self.sendUpdate('setMaxSp', [maxSp])

    def b_setMaxSp(self, maxSp):
        self.setMaxSp(maxSp)
        self.d_setMaxSp(maxSp)

    def getMaxSp(self):
        return self.maxSp

    # setLocationName(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setLocationName(self, locationName):
        self.locationName = locationName

    def d_setLocationName(self, locationName):
        self.sendUpdate('setLocationName', [locationName])

    def b_setLocationName(self, locationName):
        self.setLocationName(locationName)
        self.d_setLocationName(locationName)

    def getLocationName(self):
        return self.locationName

    # setActivity(uint32) required broadcast ram
    
    # AUTO GENERATED GETTER/SETTER. Inspection/Redoing recommended
    def setActivity(self, activity):
        self.activity = activity

    def d_setActivity(self, activity):
        self.sendUpdate('setActivity', [activity])

    def b_setActivity(self, activity):
        self.setActivity(activity)
        self.d_setActivity(activity)

    def getActivity(self):
        return self.activity


