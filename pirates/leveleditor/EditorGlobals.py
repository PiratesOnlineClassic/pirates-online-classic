# uncompyle6 version 3.1.1
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.leveleditor.EditorGlobals
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from pandac.PandaModules import *
from pirates.creature import Creature
from pirates.creature.Alligator import Alligator
from pirates.creature.Bat import Bat
from pirates.creature.Chicken import Chicken
from pirates.creature.Crab import Crab
from pirates.creature.Dog import Dog
from pirates.creature.FlyTrap import FlyTrap
from pirates.creature.Monkey import Monkey
from pirates.creature.Pig import Pig
from pirates.creature.Rooster import Rooster
from pirates.creature.Scorpion import Scorpion
from pirates.creature.Seagull import Seagull
from pirates.creature.Stump import Stump
from pirates.creature.Wasp import Wasp
from pirates.effects import DynamicLight, SoundFX
from pirates.mockup import PythonNodePath
from pirates.pirate import AvatarTypes
from pirates.ship import ShipGlobals

LOD_STATE_NORMAL = 0
LOD_STATE_HIGH = 1
LOD_STATE_LOW = 2
LOD_STATE_MED = 3
flickerTracks = []

def LightDynamic(objData, parent=render, drawIcon=True):
    if objData and 'Pos' in objData:
        objPos = objData['Pos']
    else:
        objPos = Vec3(0, 0, 0)
    if objData and 'Hpr' in objData:
        objHpr = objData['Hpr']
    else:
        objHpr = Vec3(0, 0, 0)
    color = None
    if objData and 'Visual' in objData:
        if 'Color' in objData['Visual']:
            color = objData['Visual']['Color']
    attenuation = None
    if objData and 'Attenuation' in objData:
        attenuation = (
         0, 0, float(objData['Attenuation']))
    intensity = None
    if objData and 'Intensity' in objData:
        intensity = float(objData['Intensity'])
    coneAngle = None
    dropOff = None
    if objData and 'ConeAngle' in objData:
        coneAngle = float(objData['ConeAngle'])
        if coneAngle == 0.0:
            objData['ConeAngle'] = '60.0'
            coneAngle = 60.0
    if objData and 'DropOff' in objData:
        dropOff = float(objData['DropOff'])
    exponent = None
    flickering = False
    if objData and 'Flickering' in objData and objData['Flickering'] == True:
        flickering = True
    flickRate = 1.0
    if objData and 'FlickRate' in objData:
        flickRate = float(objData['FlickRate'])
    lightType = DynamicLight.DYN_LIGHT_POINT
    if objData and 'LightType' in objData:
        typeString = objData['LightType']
        if typeString == 'AMBIENT':
            lightType = DynamicLight.DYN_LIGHT_AMBIENT
        elif typeString == 'DIRECTIONAL':
            lightType = DynamicLight.DYN_LIGHT_DIRECTIONAL
        elif typeString == 'SPOT':
            lightType = DynamicLight.DYN_LIGHT_SPOT
    light = DynamicLight.DynamicLight(type=lightType, parent=parent, pos=objPos, hpr=objHpr, color=color, atten=attenuation, exp=exponent, flicker=flickering, drawIcon=drawIcon)
    light.turnOff()
    if intensity:
        light.setIntensity(intensity)
    if coneAngle:
        light.setConeAngle(coneAngle)
    if dropOff:
        light.setDropOff(dropOff)
    light.setFlickRate(flickRate)
    light.turnOn()
    if hasattr(base, 'pe'):
        base.pe.dynamicLights.append(light)
    return light


def CreateAnimal(species=None):
    if not species:
        species = 'Pig'
    exec('animal = %s()' % species)
    animal.generateCreature()
    return animal


def CreateCreature(species=None):
    if not species:
        species = 'Crab'
    exec('creature = %s()' % species)
    creature.show()
    creature.generateCreature()
    return creature


def CreateSFX(sfxFile=None, volume=0.5, looping=True, delayMin=0, delayMax=0, pos=None, hpr=None, parent=None, drawIcon=True):
    soundFX = SoundFX.SoundFX(sfxFile=sfxFile, volume=volume, looping=looping, delayMin=delayMin, delayMax=delayMax, pos=pos, hpr=hpr, parent=parent, listenerNode=base.cam, drawIcon=drawIcon)
    return soundFX


shipList = ShipGlobals.SHIP_CLASS_LIST
notUsedShipList = ['DINGHY', 'INTERCEPTORL4', 'MERCHANTL4', 'WARSHIPL4', 'DAUNTLESS', 'FLYING_DUTCHMAN', 'SKEL_WARSHIPL3', 'SKEL_INTERCEPTORL3']
numShips = len(shipList) - 1
for index in range(numShips, -1, -1):
    if shipList[index] in notUsedShipList:
        del shipList[index]
# okay decompiling .\pirates\leveleditor\EditorGlobals.pyc
