# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pvp.Beacon
from pandac.PandaModules import CardMaker, NodePath

def getBeaconModel():
    return loader.loadModel('models/textureCards/pvp_arrow').find('**/pvp_arrow')


__beacon = None

def initBeacon():
    global __beacon
    geom = getBeaconModel()
    geom.setBillboardAxis(1)
    geom.setZ(1)
    geom.setScale(2)
    __beacon = geom


initBeacon()

def getBeacon(parent):
    return __beacon.copyTo(parent)
# okay decompiling .\pirates\pvp\Beacon.pyc
