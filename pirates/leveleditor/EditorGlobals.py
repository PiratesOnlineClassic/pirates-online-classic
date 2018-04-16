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
    if objData and objData.has_key('Pos'):
        objPos = objData['Pos']
    else:
        objPos = Vec3(0, 0, 0)
    if objData and objData.has_key('Hpr'):
        objHpr = objData['Hpr']
    else:
        objHpr = Vec3(0, 0, 0)
    color = None
    if objData and objData.has_key('Visual'):
        if objData['Visual'].has_key('Color'):
            color = objData['Visual']['Color']
    attenuation = None
    if objData and objData.has_key('Attenuation'):
        attenuation = (
         0, 0, float(objData['Attenuation']))
    intensity = None
    if objData and objData.has_key('Intensity'):
        intensity = float(objData['Intensity'])
    coneAngle = None
    dropOff = None
    if objData and objData.has_key('ConeAngle'):
        coneAngle = float(objData['ConeAngle'])
        if coneAngle == 0.0:
            objData['ConeAngle'] = '60.0'
            coneAngle = 60.0
    if objData and objData.has_key('DropOff'):
        dropOff = float(objData['DropOff'])
    exponent = None
    flickering = False
    if objData and objData.has_key('Flickering') and objData['Flickering'] == True:
        flickering = True
    flickRate = 1.0
    if objData and objData.has_key('FlickRate'):
        flickRate = float(objData['FlickRate'])
    lightType = DynamicLight.DYN_LIGHT_POINT
    if objData and objData.has_key('LightType'):
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
    exec 'animal = %s()' % species
    animal.generateCreature()
    return animal


def CreateCreature(species=None):
    if not species:
        species = 'Crab'
    exec 'creature = %s()' % species
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
