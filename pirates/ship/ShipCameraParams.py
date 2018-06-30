# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.ship.ShipCameraParams
from pandac.PandaModules import Vec3
from pirates.pirate import ShipCamera
from pirates.ship import ShipGlobals

CamParams = ShipCamera.ShipCamera.ParamSet
ShipModelClass2CameraParams = {
    ShipGlobals.DINGHY:
    CamParams(
        idealDistance=35.0,
        autoFaceForward=True,
        minDistance=30.0,
        maxDistance=80.0,
        lookAtOffset=Vec3(0, 0, 20)),
    ShipGlobals.WARSHIPL1:
    CamParams(
        idealDistance=350.0,
        autoFaceForward=True,
        minDistance=150.0,
        maxDistance=500.0,
        lookAtOffset=Vec3(0, 0, 40)),
    ShipGlobals.WARSHIPL2:
    CamParams(
        idealDistance=600.0,
        autoFaceForward=True,
        minDistance=200.0,
        maxDistance=800.0,
        lookAtOffset=Vec3(0, 0, 60)),
    ShipGlobals.WARSHIPL3:
    CamParams(
        idealDistance=700.0,
        autoFaceForward=True,
        minDistance=250.0,
        maxDistance=1000.0,
        lookAtOffset=Vec3(0, 0, 80)),
    ShipGlobals.WARSHIPL4:
    CamParams(
        idealDistance=850.0,
        autoFaceForward=True,
        minDistance=350.0,
        maxDistance=1400.0,
        lookAtOffset=Vec3(0, 0, 100)),
    ShipGlobals.MERCHANTL1:
    CamParams(
        idealDistance=350.0,
        autoFaceForward=True,
        minDistance=150.0,
        maxDistance=500.0,
        lookAtOffset=Vec3(0, 0, 40)),
    ShipGlobals.MERCHANTL2:
    CamParams(
        idealDistance=600.0,
        autoFaceForward=True,
        minDistance=200.0,
        maxDistance=800.0,
        lookAtOffset=Vec3(0, 0, 60)),
    ShipGlobals.MERCHANTL3:
    CamParams(
        idealDistance=700.0,
        autoFaceForward=True,
        minDistance=250.0,
        maxDistance=1000.0,
        lookAtOffset=Vec3(0, 0, 80)),
    ShipGlobals.MERCHANTL4:
    CamParams(
        idealDistance=850.0,
        autoFaceForward=True,
        minDistance=350.0,
        maxDistance=1400.0,
        lookAtOffset=Vec3(0, 0, 100)),
    ShipGlobals.INTERCEPTORL1:
    CamParams(
        idealDistance=270.0,
        autoFaceForward=True,
        minDistance=100.0,
        maxDistance=500.0,
        lookAtOffset=Vec3(0, 0, 40)),
    ShipGlobals.INTERCEPTORL2:
    CamParams(
        idealDistance=550.0,
        autoFaceForward=True,
        minDistance=200.0,
        maxDistance=800.0,
        lookAtOffset=Vec3(0, 0, 60)),
    ShipGlobals.INTERCEPTORL3:
    CamParams(
        idealDistance=600.0,
        autoFaceForward=True,
        minDistance=250.0,
        maxDistance=1000.0,
        lookAtOffset=Vec3(0, 0, 80)),
    ShipGlobals.INTERCEPTORL4:
    CamParams(
        idealDistance=850.0,
        autoFaceForward=True,
        minDistance=350.0,
        maxDistance=1400.0,
        lookAtOffset=Vec3(0, 0, 100)),
    ShipGlobals.BLACK_PEARL:
    CamParams(
        idealDistance=600.0,
        autoFaceForward=True,
        minDistance=250.0,
        maxDistance=1000.0,
        lookAtOffset=Vec3(0, 0, 50)),
    ShipGlobals.SKEL_WARSHIPL3:
    CamParams(
        idealDistance=600.0,
        autoFaceForward=True,
        minDistance=250.0,
        maxDistance=1000.0,
        lookAtOffset=Vec3(0, 0, 80)),
    ShipGlobals.SKEL_INTERCEPTORL3:
    CamParams(
        idealDistance=550.0,
        autoFaceForward=True,
        minDistance=250.0,
        maxDistance=1000.0,
        lookAtOffset=Vec3(0, 0, 80))
}
del CamParams
# okay decompiling .\pirates\ship\ShipCameraParams.pyc
