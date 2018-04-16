from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from pirates.pirate import Pirate
from pirates.piratesbase import PiratesGlobals
from pirates.pvp import Beacon, PVPGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

class DistributedPirateBase(DistributedObject.DistributedObject, Pirate.Pirate):
    
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPirateBase')

    def __init__(self, cr):
        self.notify.debug('__init__')
        DistributedObject.DistributedObject.__init__(self, cr)
        Pirate.Pirate.__init__(self)
        self.beacon = None

    def delete(self):
        Pirate.Pirate.delete(self)
        DistributedObject.DistributedObject.delete(self)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        if not self.loaded:
            self.generateHuman(self.style.gender, base.cr.human)

    def showBeacon(self, team):
        if self.beacon:
            self.hideBeacon()

        if team > 0:
            self.beaconNodePath = self.nametag3d.attachNewNode('beacon')
            self.beacon = Beacon.getBeacon(self.beaconNodePath)
            self.beacon.setZ(2)
            self.beacon.setBillboardPointWorld()
            self.exposeJoint(self.beaconNodePath, 'modelRoot', 'name_tag', '2000')
            self.beacon.setColor(PVPGlobals.getTeamColor(team))

    def hideBeacon(self):
        if self.beacon:
            self.beacon.remove()

        self.beacon = None