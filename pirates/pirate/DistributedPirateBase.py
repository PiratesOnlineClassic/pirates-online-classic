# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.DistributedPirateBase
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.pirate import Pirate
from pirates.piratesbase import PiratesGlobals
from pirates.pvp import Beacon
from pirates.pvp import PVPGlobals

class DistributedPirateBase(DistributedObject.DistributedObject, Pirate.Pirate):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPirateBase')

    def __init__(self, cr):
        self.notify.debug('__init__')
        DistributedObject.DistributedObject.__init__(self, cr)
        Pirate.Pirate.__init__(self)
        self.beacon = None
        return

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
        return
# okay decompiling .\pirates\pirate\DistributedPirateBase.pyc
