from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal


class DistributedBandMemberAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBandMemberAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.avatarId = 0
        self.name = ''
        self.hp = 0
        self.maxHp = 0
        self.bandManagerId = 0
        self.bandId = 0
        self.isManager = 0
        self.shipId = 0
        self.shipName = ''
        self.shipClass = 0
        self.mastInfo = []
        self.shipHasSpace = False

    def setAvatarId(self, avatarId):
        self.avatarId = avatarId

    def getAvatarId(self):
        return self.avatarId

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def setHp(self, hp):
        self.hp = max(0, hp)

    def d_setHp(self, hp):
        self.sendUpdate('setHp', [max(0, hp)])

    def b_setHp(self, hp):
        self.setHp(hp)
        self.d_setHp(hp)

    def getHp(self):
        return self.hp

    def setMaxHp(self, maxHp):
        self.maxHp = max(0, maxHp)

    def d_setMaxHp(self, maxHp):
        self.sendUpdate('setMaxHp', [max(0, maxHp)])

    def b_setMaxHp(self, maxHp):
        self.setMaxHp(maxHp)
        self.d_setMaxHp(maxHp)

    def getMaxHp(self):
        return self.maxHp

    def setBandId(self, bandManagerId, bandId):
        self.bandManagerId = bandManagerId
        self.bandId = bandId

    def getBandId(self):
        return (self.bandManagerId, self.bandId)

    def setIsManager(self, isManager):
        self.isManager = isManager

    def d_setIsManager(self, isManager):
        self.sendUpdate('setIsManager', [isManager])

    def b_setIsManager(self, isManager):
        self.setIsManager(isManager)
        self.d_setIsManager(isManager)

    def getIsManager(self):
        return self.isManager

    def setShipInfo(self, shipId, shipName, shipClass, mastInfo):
        self.shipId = shipId
        self.shipName = shipName
        self.shipClass = shipClass
        self.mastInfo = mastInfo

    def d_setShipInfo(self, shipId, shipName, shipClass, mastInfo):
        self.sendUpdate('setShipInfo', [shipId, shipName, shipClass, mastInfo])

    def b_setShipInfo(self, shipId, shipName, shipClass, mastInfo):
        self.setShipInfo(shipId, shipName, shipClass, mastInfo)
        self.d_setShipInfo(shipId, shipName, shipClass, mastInfo)

    def getShipInfo(self):
        return (self.shipId, self.shipName, self.shipClass, self.mastInfo)

    def setShipHasSpace(self, shipHasSpace):
        self.shipHasSpace = shipHasSpace

    def d_setShipHasSpace(self, shipHasSpace):
        self.sendUpdate('setShipHasSpace', [shipHasSpace])

    def b_setShipHasSpace(self, shipHasSpace):
        self.setShipHasSpace(shipHasSpace)
        self.d_setShipHasSpace(shipHasSpace)

    def getShipHasSpace(self):
        return self.shipHasSpace

    def d_setMessage(self, fromAvatarId, message):
        self.sendUpdate('setMessage', [fromAvatarId, message])

    def d_setShipDeployMessage(self, fromAvatarId, shipName, locationName):
        self.sendUpdate('setShipDeployMessage', [fromAvatarId, shipName, locationName])
