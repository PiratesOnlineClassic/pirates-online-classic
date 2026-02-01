import random
import re
import types
from panda3d.core import *
from direct.task.Task import Task
from direct.actor import *
from direct.showbase.DirectObject import DirectObject
from pirates.world import WorldGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.npc import NavySailor
from pirates.pirate.HumanDNA import *
from pirates.npc import Skeleton
from pirates.npc import Townfolk
from pirates.battle import Sword
from pirates.ai import HolidayGlobals
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import report
from otp.otpbase import OTPRender
from otp.otpbase import OTPGlobals
from pirates.leveleditor import CustomAnims
from pirates.effects import ObjectEffects
from pirates.effects import SoundFX
AREA_CHILD_TYPE_PROP = 1

class GridLODDef:
    
    def __init__(self, area, zoneId):
        self.gridNode = NodePath('Grid-' + str(zoneId) + 'Node')
        OTPRender.renderReflection(False, self.gridNode, 'p_grid', None)
        lod = LODNode.makeDefaultLod('LodNode')
        self.lodNode = self.gridNode.attachNewNode(lod)
        gridDetail = base.gridDetail
        if gridDetail == 'high':
            lod.addSwitch(500, 0)
            lod.addSwitch(1000, 500)
            lod.addSwitch(1500, 1000)
            high = self.lodNode.attachNewNode('High')
            med = self.lodNode.attachNewNode('Med')
            low = self.lodNode.attachNewNode('Low')
            self.highLodNode = high
        elif gridDetail == 'med':
            lod.addSwitch(750, 0)
            lod.addSwitch(1500, 750)
            high = None
            med = self.lodNode.attachNewNode('Med')
            low = self.lodNode.attachNewNode('Low')
            self.highLodNode = med
        elif gridDetail == 'low':
            lod.addSwitch(1500, 0)
            high = None
            med = None
            low = self.lodNode.attachNewNode('Low')
            self.highLodNode = low
        else:
            raise Exception('Invalid grid-detail: %s' % gridDetail)
        low.setLightOff(area.cr.timeOfDayManager.dlight)
        self.children = [
            high,
            med,
            low]
        if zoneId == PiratesGlobals.FakeZoneId:
            pos = area.getPos()
        else:
            pos = area.getZoneCellOriginCenter(zoneId)
        self.gridNode.setPos(pos[0], pos[1], pos[2])

    def cleanup(self):
        self.gridNode.removeNode()
        self.lodNode = None
        self.highLodNode = None
        self.children = None


class ClientArea(DirectObject):
    LARGE_OBJECTS_HIGH = [
        'Arch',
        'Tavern',
        'Building Exterior',
        'Ship Wreck',
        'Jungle_Props_large',
        'Simple Fort',
        'Pier']
    LARGE_OBJECTS_LOW = [
        'Arch',
        'Tavern',
        'Building Exterior',
        'Ship Wreck',
        'Jungle_Props_large',
        'Simple Fort',
        'Pier']
    MED_OBJECTS_HIGH = [
        'Tree',
        'Tree - Animated',
        'Swamp_props',
        'Military_props']
    MED_OBJECTS_LOW = [
        'Tree',
        'Tree - Animated',
        'Swamp_props',
        'Military_props']
    LOOKUP_TABLE_OBJECTS = [
        'Building Exterior',
        'Simple Fort',
        'Ship Wreck']
    LOD_RADIUS_FACTOR_MOST = [
        0,
        3.0,
        6.0,
        20.0,
        100.0]
    LOD_RADIUS_FACTOR_TALL = [
        0,
        6.0,
        12.0,
        20.0,
        100.0]
    AREA_NOT_LOADED = 999
    notify = directNotify.newCategory('ClientArea')
    
    def __init__(self):
        self.gridLODs = {}
        self.largeObjects = []
        self.mediumObjects = []
        self.smallObjects = []
        self.largeObjectsHigh = None
        self.largeObjectsLow = None
        self.medObjectsHigh = None
        self.medObjectsLow = None
        self.smallObjectsHigh = None
        self.smallObjectsLow = None
        self.allDetails = self.attachNewNode('allDetails')
        self.collisions = self.attachNewNode('collisions')
        self.uniqueNum = 0
        self.staticGridRoot = self.attachNewNode('staticGrid')
        self.animNode = self.attachNewNode('animations')
        self.anims = {}
        self.bound = False
        self.interactives = []
        self.haveLODs = False
        self.toBeLoaded = {}
        self.areaInitialLoad = self.AREA_NOT_LOADED
        self.uid2obj = {}
        self.isGridLod = self.isGridParent() and base.config.GetBool('make-grid-lod', 1)
        self.dynamicLights = []
        self.namedAreas = {}
        self.minLowLodSD = None
        self.sfxNodes = []
    
    def makeNPCNavy(self, dna):
        dna.makeNPCNavySailor()
        dna.gender = 'n'
        dna.body.color = 0
        dna.body.shape = 3
        dna.body.height = random.choice([
            0.8,
            0.9,
            1,
            1.1,
            1.2])
        dna.clothes.shirt = 0
        dna.clothes.vest = 0
        dna.clothes.coat = 3
        dna.clothes.pant = 4
        dna.clothes.sock = 0
        dna.clothes.shoe = 3
        dna.clothes.belt = 0
        dna.head.hair.hair = 1
        dna.head.hair.beard = 0
        dna.head.hair.mustache = 0
        dna.head.hair.color = 0

    def createPropAvatar(self, objType, object, parent, uid):
        
        def playPropAvAnim(task, propAv, object, createDefault = True):
            anim = object['Animation Track']
            createDefSword = createDefault
            if anim == 'Track 1':
                ivals = []
                randWait = random.random() * 4.0
                ival = Sequence(ActorInterval(propAv, 'sword_slash'), ActorInterval(propAv, 'sword_thrust', duration = 1), ActorInterval(propAv, 'sword_idle'), ActorInterval(propAv, 'sword_slash'), ActorInterval(propAv, 'sword_idle', duration = randWait))
                ival.loop()
                ivals.append(ival)
                propAv.swordIvals = ivals
            elif anim == 'Track 2':
                ivals = []
                ival = Sequence(ActorInterval(propAv, 'sword_slash'), ActorInterval(propAv, 'sword_thrust', duration = 1), ActorInterval(propAv, 'sword_idle'), ActorInterval(propAv, 'boxing_kick'), ActorInterval(propAv, 'sword_idle'))
                ival.loop()
                ivals.append(ival)
                propAv.swordIvals = ivals
            else:
                allAnims = CustomAnims.INTERACT_ANIMS.get(anim)
                if allAnims:
                    allIdles = allAnims.get('idles')
                    allProps = allAnims.get('props')
                    currChoice = random.choice(allIdles)
                    anim = currChoice
                    createDefSword = False
                    if allProps:
                        propInfo = random.choice(allProps)
                        if type(propInfo) == list:
                            propInfo = propInfo[0]
                        
                        prop = loader.loadModel(propInfo)
                        prop.reparentTo(propAv.rightHandNode)
                
                propAv.loop(anim)
            if createDefSword:
                s = Sword.Sword(10103)
                s.attachTo(propAv)
            
            return Task.done

        propAv = None
        createDefaultProp = True
        if objType == 'Animated Avatar - Skeleton':
            propAv = Skeleton.Skeleton()
            propAv.setAvatarType()
            propAv.setName('Extra')
        elif objType == 'Animated Avatar - Navy':
            propAv = NavySailor.NavySailor()
            dna = HumanDNA()
            self.makeNPCNavy(dna)
            propAv.setDNAString(dna)
            propAv.generateHuman(propAv.style.gender, base.cr.human)
            propAv.setName('Extra')
        elif objType == 'Animated Avatar - Townfolk':
            propAv = Townfolk.Townfolk()
            dna = HumanDNA()
            dna.makeNPCPirate()
            dna.gender = object['Visual']['Gender']
            dna.body.shape = object['Visual']['Shape']
            dna.head.hair.hair = object['Visual']['Hair']
            dna.head.hair.beard = object['Visual']['Beard']
            dna.head.hair.mustache = object['Visual']['Mustache']
            dna.head.hair.color = object['Visual']['HairColor']
            dna.body.color = object['Visual']['Skin']
            dna.clothes.coat = object['Visual']['Coat']
            dna.clothes.coatColor = object['Visual']['CoatColor']
            dna.clothes.shirt = object['Visual']['Shirt']
            dna.clothes.shirtColor = object['Visual']['ShirtColor']
            dna.clothes.pant = object['Visual']['Pants']
            dna.clothes.pantColor = object['Visual']['PantsColor']
            dna.clothes.sock = object['Visual']['Sock']
            dna.clothes.shoe = object['Visual']['Shoe']
            dna.clothes.belt = object['Visual']['Belt']
            dna.clothes.beltColor = object['Visual']['BeltColor']
            dna.head.hat = object['Visual']['Hat']
            propAv.setDNAString(dna)
            propAv.generateHuman(propAv.style.gender, base.cr.human)
            propAv.setName('Extra')
        else:
            propAv = Townfolk.Townfolk()
            subCat = object.get('SubCategory')
            if subCat:
                propAv.loadCast(subCat)
                propAv.loop('idle')
                __builtins__['propAv'] = propAv
            
            createDefaultProp = False
            if 'Effect Type' in object and object['Effect Type'] != None and object['Effect Type'] in ObjectEffects.OBJECT_EFFECTS:
                ObjectEffects.OBJECT_EFFECTS[object['Effect Type']](propAv)
            
        if propAv:
            playPropAvAnim(None, propAv, object, createDefaultProp)
            propAv.reparentTo(parent)
            propAv.setPos(object['Pos'])
            propAv.setHpr(object['Hpr'])
            if 'Scale' in object:
                propAv.setScale(object['Scale'])
            
            if 'Visual' in object and 'Color' in object['Visual']:
                propAv.setColorScale(*object['Visual']['Color'])
            
            if object['Animation Track'] == 'walk' or object['Animation Track'] == 'run':
                self.createPropAvatarMovement(uid, propAv, object['Animation Track'])
            
            self.mediumObjects.append(propAv)
            propAv.wrtReparentTo(self.allDetails)
        
        return propAv

    def createPropAvatarMovement(self, uid, propAv, anim):
        for currData in self.cr.distributedDistrict.worldCreator.fileDicts:
            if self.uniqueId in currData['Objects']:
                for currLink in currData['Node Links']:
                    amNode1 = currLink[0] == uid
                    amNode2 = currLink[1] == uid
                    if amNode1 or amNode2:
                        if amNode1:
                            path = currData['ObjectIds'][currLink[1]]
                        else:
                            path = currData['ObjectIds'][currLink[0]]
                        getDstPos = 'dstPos = currData' + path + '["Pos"]'
                        exec(getDstPos)
                        h0 = propAv.getH()
                        h1 = propAv.getH() + 180
                        p = propAv.getP()
                        r = propAv.getR()
                        srcPos = propAv.getPos()
                        tgtLoc = propAv.getParent().attachNewNode('dummy')
                        tgtLoc.setPos(dstPos)
                        moveDist = propAv.getDistance(tgtLoc)
                        if anim == 'run':
                            moveTime = moveDist / 16
                        else:
                            moveTime = moveDist / 4
                        moveIval = Sequence(LerpPosInterval(propAv, moveTime, dstPos), LerpHprInterval(propAv, 0, Vec3(h1, p, r)), LerpPosInterval(propAv, moveTime, srcPos), LerpHprInterval(propAv, 0, Vec3(h0, p, r)))
                        tgtLoc.removeNode()
                        moveIval.loop()
                        propAv.moveIval = moveIval
                        return

    def checkSanityOnType(self, objData):
        objectType = objData['Type']
        if objectType != 'Building Exterior':
            return objectType
        
        file = None
        
        try:
            file = objData['File']
            bTrueBuilding = file != ''
        except:
            return objectType

        if not bTrueBuilding:
            return 'PropBuildingExterior'
        else:
            return objectType

    def addChildObj(self, objData, uid, childType = AREA_CHILD_TYPE_PROP, objRef = None, zoneLevel = 0, startTime = None, altParent = None, nodeName = None, actualParentObj = None):
        if objData['Type'] == 'Animated Avatar - Skeleton' or objData['Type'] == 'Animated Avatar - Navy' or objData['Type'] == 'Animated Avatar - Townfolk' or objData['Type'] == 'Animated Avatar':
            return self.createPropAvatar(objData['Type'], objData, self, uid)
        
        objStolen = False
        flaggedToSkip = False
        if objData.get('SkipFlatten') == True:
            flaggedToSkip = True
        
        highNode = None
        lowNode = None
        objNode = None
        if objRef:
            objNode = objRef
        
        objModel = None
        loadObject = True
        self.notify.debug('ClientArea: loading %s' % uid)
        zoneToLoadIn = 2
        delayedLoad = False
        objectType = self.checkSanityOnType(objData)
        objectCat = self.cr.distributedDistrict.worldCreator.findObjectCategory(objData['Type'])
        loadableType = objectCat == 'PROP_OBJ' or objectCat == 'BUILDING_OBJ' or objectType == 'Cell Portal Area' or objectType == 'Dinghy' or objectType == 'Holiday Object'
        if not loadableType and 'Objects' not in objData:
            return None
        
        if startTime and globalClock.getRealTime() - startTime > 0.05 and delayedLoad:
            loadObject = False
            if objectType in self.LARGE_OBJECTS_HIGH and objectType in self.LARGE_OBJECTS_LOW:
                zoneToLoadIn = 2
            elif objectType in self.MED_OBJECTS_HIGH or objectType in self.MED_OBJECTS_LOW:
                zoneToLoadIn = 1
            else:
                zoneToLoadIn = 0
        elif not self.haveLODs:
            loadObject = True
        elif zoneLevel in self.toBeLoaded and uid in self.toBeLoaded[zoneLevel]:
            loadObject = True
        
        if objNode == None:
            if loadObject:
                bObjAnimated = False
                if 'Visual' in objData and 'Model' in objData['Visual']:
                    if 'SubObjs' in objData:
                        objNode = self.loadSubModels(objData)
                        objModel = objNode
                        bObjAnimated = True
                    else:
                        if type(objData['Visual']['Model']) == list:
                            modelName = 'models/misc/smiley'
                            objData['Visual']['Color'] = (0.800000011920929, 0, 0, 1.0)
                            objData['Scale'] = VBase3(20.0, 20.0, 20.0)
                            self.notify.warning("Attempting to load object of type '%s', will load a big red smiley instead" % objectType)
                        else:
                            modelName = objData['Visual']['Model']
                        if modelName.find('bilgewater_town') != -1:
                            objModel = NodePath('bilgewater_town')
                        elif objectType == 'Tunnel Cap':
                            altId = objData.get('AltBlockerId')
                            objModel = self.loadPiecesModels(modelName, altId)
                        else:
                            objModel = loader.loadModelCopy(modelName)
                        if objModel == None:
                            self.notify.warning('Could not load model %s, not creating object.' % modelName)
                            return None
                    
                    if 'DisableCollision' in objData and objData['DisableCollision'] == True:
                        collisionNodes = objModel.findAllMatches('**/+CollisionNode')
                        for collisionNode in collisionNodes:
                            collisionNode.removeNode()
                    
                    if objData['Type'] == 'Collision Barrier':
                        geomNodes = objModel.findAllMatches('**/+GeomNode')
                        for geomNode in geomNodes:
                            geomNode.removeNode()

                    if objData['Type'] == 'Special':
                        if 'Visual' in objData and 'Model' in objData['Visual'] and objData['Visual']['Model'] == 'models/misc/smiley':
                            geomNodes = objModel.findAllMatches('**/+GeomNode')
                            for geomNode in geomNodes:
                                geomNode.removeNode()

                    if objData['Type'] == 'SFX Node':
                        objNode = self.loadSFXNode(objData, self, uid)
                        objModel = objNode
                        bObjAnimated = True
                    
                    if objectType == 'Animated Prop':
                        objNode = self.loadAnimatedProp(objData, self)
                        objModel = objNode
                        bObjAnimated = True
                        flaggedToSkip = True
                    
                    if objectType == 'Dinghy':
                        flaggedToSkip = True
                    
                    if self.isGridLod and objectType not in self.LARGE_OBJECTS_HIGH and flaggedToSkip == False:
                        objPos = objData.get('Pos')
                        if hasattr(self, 'fakeZoneId'):
                            zoneId = self.fakeZoneId
                        else:
                            zoneId = self.getZoneFromXYZ(objPos)
                        objLOD = objModel.find('**/+LODNode')
                        if hasattr(self, 'GridLOD'):
                            xform = NodePath('tform')
                            xform.setPos(objPos)
                            xform.setHpr(objData['Hpr'])
                            if actualParentObj:
                                xform.reparentTo(actualParentObj)
                                relHpr = xform.getHpr(self)
                                xform.setHpr(relHpr)
                                relPos = xform.getPos(self)
                                xform.setPos(relPos)
                                objPos = relPos
                                zoneId = self.getZoneFromXYZ(objPos)
                            
                            if 'Scale' in objData:
                                xform.setScale(objData['Scale'])
                            
                            if objectType == 'Light_Fixtures' or objectType == 'Tunnel Cap':
                                effects = objModel.findAllMatches('**/*_effect_*')
                                if not effects.isEmpty():
                                    for i in range(0, effects.getNumPaths()):
                                        effect = effects[i]
                                        lform = NodePath('fooEffect')
                                        lform.setPos(objPos)
                                        lform.setHpr(objData['Hpr'])
                                        lform.setScale(objData['Scale'])
                                        effect.reparentTo(lform)
                                        lform.flattenLight()
                                        node = lform.getChild(0)
                                        node.reparentTo(self.staticGridRoot)
                                        if 'Holiday' in objData:
                                            node.setTag('Holiday', objData['Holiday'])

                            if 'Color' in objData['Visual']:
                                xform.setColorScale(*objData['Visual']['Color'])
                            
                            if zoneId not in self.GridLOD:
                                self.GridLOD[zoneId] = GridLODDef(self, zoneId)
                            
                            gldef = self.GridLOD[zoneId]
                            gridNode = gldef.gridNode
                            lodNode = gldef.lodNode
                            highLODNode = gldef.highLodNode
                            holiday = objData.get('Holiday')
                            if holiday:
                                self.accept('HolidayStarted', self.unstashHolidayObjects)
                                self.accept('HolidayEnded', self.stashHolidayObjects)
                            
                            cNodes = objModel.findAllMatches('**/+CollisionNode')
                            if not cNodes.isEmpty():
                                tform = xform.copyTo(NodePath())
                                if holiday:
                                    for cNode in cNodes:
                                        cNode.setTag('Holiday', holiday)

                                cNodes.reparentTo(tform)
                                tform.wrtReparentTo(gridNode)
                            
                            if objLOD.isEmpty():
                                tform = xform.copyTo(NodePath())
                                objModel.findAllMatches('**/+GeomNode').reparentTo(tform)
                                if not holiday:
                                    parent = highLODNode
                                else:
                                    parent = highLODNode.attachNewNode(ModelNode('HolidayParent'))
                                    parent.setTag('Holiday', holiday)
                                tform.wrtReparentTo(parent)
                            else:
                                objLODNode = objLOD.node()
                                lodIdx = 0
                                lowOnly = False
                                if base.gridDetail == 'low' and objectType in self.MED_OBJECTS_LOW:
                                    lowOnly = True
                                    lodIdx = objLODNode.getNumChildren() - 1
                                
                                for i in range(0, objLODNode.getNumChildren()):
                                    if gldef.children[i] == None:
                                        continue
                                    
                                    if not holiday:
                                        tform = xform.copyTo(NodePath())
                                    else:
                                        tform = NodePath(ModelNode('HolidayParent'))
                                        tform.setTag('Holiday', holiday)
                                        tform.setTransform(xform.getTransform())
                                    if not lowOnly:
                                        lodIdx = i
                                        tform.node().stealChildren(objLODNode.getChild(lodIdx))
                                    elif lodIdx != i:
                                        tform.node().copyChildren(objLODNode.getChild(lodIdx))
                                    else:
                                        tform.node().stealChildren(objLODNode.getChild(lodIdx))
                                    if objLODNode.getChild(lodIdx).isGeomNode():
                                        tform.node().addChild(objLODNode.getChild(lodIdx))
                                    
                                    tform.wrtReparentTo(gldef.children[i])
                                
                                objLODNode.removeAllChildren()
                                objLOD.removeNode()
                            if objectType == 'PropBuildingExterior':
                                specialGeo = objModel.findAllMatches('**/+GeomNode')
                                if not specialGeo.isEmpty():
                                    tform = xform.copyTo(NodePath())
                                    for i in range(0, specialGeo.getNumPaths()):
                                        specialGeo[i].setPos(specialGeo[i].getParent().getPos())
                                        specialGeo[i].setHpr(specialGeo[i].getParent().getHpr())
                                        specialGeo[i].setScale(specialGeo[i].getParent().getScale())
                                        specialGeo[i].reparentTo(tform)
                                    
                                    tform.wrtReparentTo(highLODNode)

                            if bObjAnimated:
                                pass
                            else:
                                objModel.removeNode()
                            objStolen = True
                            xform.removeNode()
            else:
                if zoneToLoadIn not in self.toBeLoaded:
                    self.toBeLoaded[zoneToLoadIn] = {}

                self.toBeLoaded[zoneToLoadIn][uid] = objData
                return None
        
        if (objModel == None or objModel.isEmpty()) and objNode == None and 'Visual' in objData and 'Model' in objData['Visual']:
            if not objStolen:
                self.notify.warning('ClientArea: No model named %s' % objData['Visual']['Model'])
            
            return None
        
        if nodeName == None:
            objNodeName = 'Prop' + objectType
        else:
            objNodeName = nodeName
        if not self.haveLODs:
            parent = self.allDetails
            nodeList = self.largeObjects
        elif objectType in self.LARGE_OBJECTS_HIGH:
            parent = self.largeObjectsHigh
            nodeList = self.largeObjects
            highNode = self.largeObjectsHigh
            lowNode = self.largeObjectsLow
        elif objectType in self.LARGE_OBJECTS_LOW:
            parent = self.largeObjectsLow
            nodeList = self.largeObjects
        elif objectType in self.MED_OBJECTS_HIGH:
            parent = self.medObjectsHigh
            nodeList = self.mediumObjects
            highNode = self.medObjectsHigh
            lowNode = self.medObjectsLow
        elif objectType in self.MED_OBJECTS_LOW:
            parent = self.medObjectsLow
            nodeList = self.mediumObjects
        else:
            parent = self.smallObjectsHigh
            nodeList = self.smallObjects
            highNode = self.smallObjectsHigh
            lowNode = self.smallObjectsLow
        if altParent:
            parent = altParent
        
        if objNode == None:
            objNode = parent.attachNewNode(objNodeName)
        elif objModel != objNode:
            objNode.reparentTo(parent)
        
        nodeList.append(objNode)
        if objectType in self.LOOKUP_TABLE_OBJECTS:
            objNode.setTag('uid', uid)
        
        if objModel == objNode:
            return objNode
        
        if objModel:
            objModel.reparentTo(objNode)
            if 'Visual' in objData and 'SignFrame' in objData['Visual'] and objData['Visual']['SignFrame'] != '':
                signLocator = objModel.find('**/sign_locator')
                if signLocator and not signLocator.isEmpty():
                    signFrameName = objData['Visual']['SignFrame']
                    signFramePaletteName = signFrameName.split('frame')[0]
                    signFrame = loader.loadModel(signFrameName)
                    signIconModel = objData['Visual'].get('SignImage')
                    if signIconModel:
                        signIconName = objData['Visual']['SignImage'].split('icon')[1]
                        signIcon = loader.loadModel(signFramePaletteName + 'icon' + signIconName)
                        signIcon.reparentTo(signFrame)
                    
                    signFrame.setPos(signLocator.getPos())
                    signFrame.setHpr(signLocator.getHpr())
                    signFrame.setScale(signLocator.getScale())
                    signFrame.flattenStrong()
                    tform = NodePath('signGeo')
                    signGeo = signFrame.findAllMatches('**/+GeomNode')
                    signGeo.reparentTo(tform)
                    signColl = signFrame.findAllMatches('**/+CollisionNode')
                    objLOD = objModel.find('**/+LODNode')
                    if objLOD.isEmpty():
                        tform.reparentTo(objModel)
                        signColl.reparentTo(objModel)
                    else:
                        signColl.reparentTo(objLOD.getParent())
                        objLODNode = objLOD.node()
                        lodNP = NodePath(objLODNode.getChild(0))
                        tform.reparentTo(lodNP)
                        for i in range(1, objLODNode.getNumChildren()):
                            lodNP = NodePath(objLODNode.getChild(i))
                            xform = tform.copyTo(NodePath())
                            xform.reparentTo(lodNP)
                        
                    signLocator.removeNode()
                else:
                    self.notify.warning('% : missing sign_locator' % objModel.getName())

        objNode.setPos(objData['Pos'])
        objNode.setHpr(objData['Hpr'])
        if 'Scale' in objData:
            objNode.setScale(objData['Scale'])
        
        if 'Visual' in objData and 'Color' in objData['Visual']:
            objNode.setColorScale(*objData['Visual']['Color'])
        
        if lowNode and objectType in self.LARGE_OBJECTS_LOW:
            lodnode = objNode.find('**/+LODNode')
            if not lodnode.isEmpty():
                lowNP = lodnode.find('**/low*;+i')
                if lowNP.isEmpty():
                    lowNP = lodnode.find('**/*_low*;+i')
                
                if not lowNP.isEmpty():
                    lowGeo = lowNP.copyTo(NodePath())
                    lowGeo.setPos(objNode.getPos())
                    lowGeo.setHpr(objNode.getHpr())
                    lowGeo.setScale(objNode.getScale())
                    lowGeo.setColorScale(objNode.getColorScale())
                    lowGeo.flattenStrong()
                    lowGeo.reparentTo(lowNode)
                
                lowendHighNP = objNode.find('**/lowend*;+i')
                if not lowendHighNP.isEmpty():
                    if base.gridDetail != 'high':
                        highNP = lodnode.find('**/high*;+i')
                        if highNP.isEmpty():
                            highNP = lodnode.find('**/*_high*;+i')
                        
                        if not highNP.isEmpty():
                            highNP.node().removeAllChildren()
                            lowendHighNP.reparentTo(highNP)
                        
                    else:
                        lowendHighNP.removeNode()
                
            else:
                self.notify.warning('ClientArea: large object %s has no low lod' % objModel.getName())
        
        if 'Objects' in objData:
            self.cr.distributedDistrict.worldCreator.registerPostLoadCall(Functor(self.flattenObjNode, objNode))
        else:
            self.flattenObjNode(objNode)
        self.handleSpecial(objNode, objectType, uid)
        return objNode

    def flattenObjNode(self, objNode):
        lodnode = objNode.find('**/+LODNode')
        if not lodnode.isEmpty():
            sgr = SceneGraphReducer()
            if base.gridDetail == 'low':
                lodnode.setLightOff(self.cr.timeOfDayManager.dlight)
                sgr.removeColumn(lodnode.node(), InternalName.getNormal())
            else:
                lowNP = lodnode.find('low;+i')
                if not lowNP.isEmpty():
                    lowNP.setLightOff(self.cr.timeOfDayManager.dlight)
                    sgr.removeColumn(lowNP.node(), InternalName.getNormal())
                
                for higherName in ['med*', 'hi*']:
                    higher = lodnode.find(higherName + ';+i')
                    if not higher.isEmpty():
                        sgr.applyAttribs(higher.node(), sgr.TTCullFace)

        objNode.flattenStrong()

    def setupLODs(self):
        self.haveLODs = True
        detailNode = LODNode.makeDefaultLod('largeObjects')
        sdHigh = 1000
        sdLow = 2000
        if hasattr(self, 'sphereRadii'):
            sdHigh = self.sphereRadii[0]
            sdLow = self.sphereRadii[2]
        
        detailNode.addSwitch(sdHigh, 0)
        detailNode.addSwitch(sdLow, sdHigh)
        self.minLowLodSD = sdHigh
        lodnp = NodePath(detailNode)
        lodnp.reparentTo(self.allDetails)
        self.largeObjectsHigh = lodnp.attachNewNode('highDetail')
        self.largeObjectsLow = lodnp.attachNewNode('lowDetail')
        self.largeObjects = []
        detailNode = LODNode.makeDefaultLod('medObjects')
        lodnp = NodePath(detailNode)
        lodnp.reparentTo(self.allDetails)
        self.medObjectsHigh = lodnp.attachNewNode('highDetail')
        self.medObjectsLow = lodnp.attachNewNode('lowDetail')
        self.mediumObjects = []
        detailNode = LODNode.makeDefaultLod('smallObjects')
        lodnp = NodePath(detailNode)
        lodnp.reparentTo(self.allDetails)
        self.smallObjectsHigh = lodnp.attachNewNode('highDetail')
        self.smallObjects = []
    
    def loadAnimatedTree(self, obj, modelName, animName, partName):
        syls = modelName.split('trunk_')
        newModelName = syls[0]
        syls = animName.split('_')
        numDelms = len(syls)
        aName = syls[numDelms - 1]
        newAnimName = newModelName + aName
        newModelName += 'hi'
        newPartName = 'modelRoot'
        bLODLoaded = not obj.hasLOD()
        if bLODLoaded:
            obj.setLODNode()
        
        if loader.loadModelCopy(newModelName) != None:
            if bLODLoaded:
                obj.addLOD(1, 200, 0)
            
            obj.loadModel(newModelName, newPartName, '1')
        
        newModelName = re.sub('_hi', '_med', newModelName)
        if loader.loadModelCopy(newModelName) != None:
            if bLODLoaded:
                obj.addLOD(2, 400, 200)
            
            obj.loadModel(newModelName, newPartName, '2')
        
        newModelName = re.sub('_med', '_low', newModelName)
        if loader.loadModelCopy(newModelName) != None:
            if bLODLoaded:
                obj.addLOD(3, 1000, 400)
            
            obj.loadModel(newModelName, newPartName, '3')
        
        self.setupUniqueActor(obj, newAnimName)
        newModelName = re.sub('_low', '_zero_coll', newModelName)
        coll = loader.loadModelCopy(newModelName)
        if coll:
            coll.reparentTo(obj)

    def makeAnimatedTree(self, obj, trunk, leaf):
        tname = ''
        tparts = trunk.split('_')
        numDelms = len(tparts)
        i = 0
        for syl in tparts:
            if syl == 'trunk':
                tname = syl + '_' + tparts[i + 1]
                break
            
            i += 1
        
        lname = ''
        lparts = leaf.split('_')
        numDelms = len(lparts)
        i = 0
        for syl in lparts:
            if syl == 'leaf':
                lname = syl + '_' + lparts[i + 1]
                break
            
            i += 1
        
        trunkNodes = obj.findAllMatches('**/*' + tname + '*')
        leafNodes = obj.findAllMatches('**/*' + lname + '*')
        obj.findAllMatches('**/+GeomNode').stash()
        trunkNodes.unstash()
        leafNodes.unstash()
    
    def loadSubModelLODs(self, obj, modelName, animName, partName):
        if not obj.hasLOD():
            obj.setLODNode()
            obj.addLOD(1, 120, 0)
            obj.addLOD(2, 300, 120)
            obj.addLOD(3, 750, 300)
        
        obj.loadModel(modelName, partName, '1')
        modelName = re.sub('_hi', '_med', modelName)
        obj.loadModel(modelName, partName, '2')
        modelName = re.sub('_med', '_low', modelName)
        obj.loadModel(modelName, partName, '3')
        self.setupUniqueActor(obj, animName)
    
    def loadSubModels(self, propData):
        bAnimatedTree = propData['Type'] == 'Tree - Animated'
        obj = Actor.Actor()
        name = propData['Visual']['PartName']
        modelName = propData['Visual']['Model']
        animName = propData['Visual']['Animate']
        if bAnimatedTree:
            trunkName = modelName
            self.loadAnimatedTree(obj, modelName, animName, name)
        else:
            self.loadSubModelLODs(obj, modelName, animName, name)
        subObjs = obj.findAllMatches('**/*' + name + '*')
        if 'Scale' in propData['Visual']:
            for i in range(len(subObjs)):
                currSubObj = subObjs[i]
                currSubObj.setScale(propData['Visual']['Scale'])

        if 'Color' in propData['Visual']:
            for i in range(len(subObjs)):
                currSubObj = subObjs[i]
                currSubObj.setColorScale(*propData['Visual']['Color'])

        animRateRange = [1.0, 1.0]
        if 'SubObjs' in propData:
            if type(propData['SubObjs']) == dict:
                subObjsInfo = list(propData['SubObjs'].values())
            else:
                subObjsInfo = propData['SubObjs']
            for currSubObj in subObjsInfo:
                attachInfo = currSubObj['Visual']['Attach']
                name = currSubObj['Visual']['PartName']
                modelName = currSubObj['Visual']['Model']
                animName = currSubObj['Visual']['Animate']
                if bAnimatedTree:
                    leafName = modelName
                else:
                    self.loadSubModelLODs(obj, modelName, animName, name)
                subObjs = obj.findAllMatches('**/*' + name + '*')
                if 'Scale' in currSubObj['Visual']:
                    if bAnimatedTree:
                        transform = TransformState.makeMat(Mat4(obj.getJointTransform('modelRoot', attachInfo[1], '1')))
                        obj.freezeJoint('modelRoot', attachInfo[1], pos = Vec3(transform.getPos()), hpr = Vec3(transform.getHpr()), scale = currSubObj['Visual']['Scale'])
                    else:
                        for i in range(len(subObjs)):
                            currLOD = subObjs[i]
                            currLOD.setScale(currSubObj['Visual']['Scale'])

                if 'Color' in currSubObj['Visual']:
                    for i in range(len(subObjs)):
                        currLOD = subObjs[i]
                        currLOD.setColorScale(*currSubObj['Visual']['Color'])
                
                if propData['Type'] != 'Tree - Animated':
                    for lodName in obj.getLODNames():
                        obj.attach(name, attachInfo[0], attachInfo[1], lodName)

                animRateRange = WorldGlobals.ObjectAnimRates.get(animName)
                if animRateRange == None:
                    animRateRange = WorldGlobals.ObjectAnimRates.get('Default')
            
            if bAnimatedTree:
                self.makeAnimatedTree(obj, trunkName, leafName)

        return obj
    
    def pauseSFX(self):
        for sfxNode in self.sfxNodes:
            sfxNode.stopPlaying()
    
    def resumeSFX(self):
        for sfxNode in self.sfxNodes:
            sfxNode.startPlaying()

    def loadSFXNode(self, objData, parent, uid):
        sfxNode = SoundFX.SoundFX(sfxFile = objData['SoundFX'], volume = float(objData['Volume']), looping = True, delayMin = float(objData['DelayMin']), delayMax = float(objData['DelayMax']), pos = objData['Pos'], hpr = objData['Hpr'], parent = parent, listenerNode = base.localAvatar, drawIcon = False)
        sfxNode.startPlaying('playSfx_%s' % uid)
        self.sfxNodes.append(sfxNode)
        return sfxNode

    def loadAnimatedProp(self, propData, parent):
        
        def playAnim(propAv, anim):
            __builtins__['bird'] = propAv
            propAv.loadAnims({
                'idle': anim})
            propAv.loop('idle')

        propAv = Actor.Actor()
        visInfo = propData.get('Visual')
        if visInfo:
            modelName = visInfo.get('Model')
            anim = visInfo.get('Animate')
        
        if modelName == None:
            return None
        
        propAv.loadModel(modelName)
        if anim:
            playAnim(propAv, anim)
        
        propAv.reparentTo(parent)
        propAv.setPos(propData['Pos'])
        propAv.setHpr(propData['Hpr'])
        if 'Scale' in propData:
            propAv.setScale(propData['Scale'])
        
        if 'Visual' in propData and 'Color' in propData['Visual']:
            propAv.setColorScale(*propData['Visual']['Color'])
        
        self.smallObjects.append(propAv)
        propAv.wrtReparentTo(self.allDetails)
        return propAv

    def reparentLODCollisions(self, sourceNode, targetNode, collName):
        sourceNode.findAllMatches('**/+' + collName).wrtReparentTo(targetNode)
        targetNode.flattenLight()

    def loadLights(self):
        self.polyLights = self.findAllMatches('**/+PolylightNode')
        self.fires = []
        self.discs = []
        self.lights = []
        lightCol = [
            VBase4(0, 0, 0, 1),
            VBase4(1, 0, 0, 1),
            VBase4(0, 1, 0, 1),
            VBase4(0, 0, 1, 1)]
        for i in range(len(self.polyLights)):
            light = self.polyLights[i]
            plNode = light.node()
            plNode.flickerOff()
            plNode.setAttenuation(PolylightNode.AQUADRATIC)
            plNode.setRadius(20)
            effect = base.localAvatar.node().getEffect(PolylightEffect.getClassType()).addLight(light)
            base.localAvatar.node().setEffect(effect)
            self.lights.append(light)
            fire = loader.loadModelCopy('models/misc/fire')
            fire.setBillboardPointEye()
            fire.setPos(plNode.getPos())
            fire.setScale(0.1)
            fire.setColorScaleOff()
            fire.reparentTo(light)
            self.fires.append(fire)
            LanternGlowEffect = LanternGlow(light, 2)
            pos = plNode.getPos()
            LanternGlowEffect.setPos(pos)
            LanternGlowEffect.loop()
            self.discs.append(LanternGlowEffect)

    def unloadLights(self):
        for light in self.lights:
            effect = base.localAvatar.node().getEffect(PolylightEffect.getClassType())
            if effect.hasLight(light):
                base.localAvatar.node().setEffect(effect.removeLight(light))
        
        for disc in self.discs:
            disc.removeNode()
        
        del self.discs
    
    def attachCannon(self, cannon):
        self.interactives.append(cannon)

    def setupCannonballBldgColl(self, collNode, mask):
        if collNode == None or collNode.isEmpty():
            return None
        
        collNode.setCollideMask(mask)
        collNode.setTag('objType', str(PiratesGlobals.COLL_BLDG))

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='want-blackpearl-report')
    def loadZoneObjects(self, zoneLevel):
        if zoneLevel == -1:
            zonesToLoad = [
                2, 1, 0]
        else:
            zonesToLoad = [
                zoneLevel]
        for currZoneToLoad in zonesToLoad:
            if self.areaInitialLoad == self.AREA_NOT_LOADED:
                self.areaInitialLoad = currZoneToLoad
                startTime = globalClock.getRealTime()
                self.cr.distributedDistrict.worldCreator.loadObjectsByUid(self, self.uniqueId, dynamic=1,
                                                                          zoneLevel=currZoneToLoad, startTime=startTime)
            else:
                toLoad = self.toBeLoaded.get(currZoneToLoad)
                if toLoad:
                    startTime = globalClock.getRealTime()
                    while len(toLoad) > 0:
                        delObjs = []
                        addObjs = {}
                        for currToLoad in toLoad:
                            if type(toLoad[currToLoad]) is list:
                                objInfo = toLoad[currToLoad][0]
                                altParent = toLoad[currToLoad][1]
                            else:
                                objInfo = toLoad[currToLoad]
                                altParent = None
                            addedObj = self.addChildObj(objInfo, currToLoad, childType=AREA_CHILD_TYPE_PROP,
                                                        objRef=None,
                                                        zoneLevel=currZoneToLoad, altParent=altParent)
                            if objInfo.get('Type') == 'Cell Portal Area':
                                addedObj.setName(objInfo.get('Name') + '_objects')
                            delObjs.append(currToLoad)
                            childens = objInfo.get('Objects')
                            if childens:
                                for currChildUid in list(childens.keys()):
                                    addObjs[currChildUid] = [
                                        childens[currChildUid], addedObj]

                            if globalClock.getRealTime() - startTime > 0.05 and base.config.GetBool('object-load-delay', 0):
                                for currDelObj in delObjs:
                                    del toLoad[currDelObj]

                                for currAddObj in list(addObjs.keys()):
                                    toLoad[currAddObj] = addObjs[currAddObj]

                                if len(list(toLoad.keys())) > 0:
                                    taskMgr.doMethodLater(0.25, self.loadZoneObjects, 'loadZoneObjects' + str(id(self)),
                                                          extraArgs=[currZoneToLoad])
                                    self.notify.debug('ClientArea: delaying rest of loading, %s objects left...' % len(list(toLoad.keys())))
                                return

                        for currDelObj in delObjs:
                            del toLoad[currDelObj]

                        for currAddObj in list(addObjs.keys()):
                            toLoad[currAddObj] = addObjs[currAddObj]

                    del self.toBeLoaded[currZoneToLoad]
                if self.isGridLod and len(self.toBeLoaded) == 0:
                    self.parentGridNodes()

        self.cr.distributedDistrict.worldCreator.processPostLoadCalls()
        self.findAllMatches('**/HolidayParent').stash()
    
    def unloadZoneObjects(self):
        self.areaInitialLoad = self.AREA_NOT_LOADED
        if hasattr(self, 'GridLOD'):
            for currGrid in self.GridLOD:
                self.GridLOD[currGrid].cleanup()

        self.GridLOD = {}
        for currObj in self.largeObjects:
            if not currObj.isEmpty():
                if hasattr(currObj, 'cleanup'):
                    currObj.cleanup()
                
                currObj.removeNode()
        
        self.largeObjects = []
        for currObj in self.mediumObjects:
            if not currObj.isEmpty():
                if hasattr(currObj, 'cleanup'):
                    currObj.cleanup()
                
                currObj.removeNode()
        
        self.mediumObjects = []
        for currObj in self.smallObjects:
            if not currObj.isEmpty():
                if hasattr(currObj, 'cleanup'):
                    currObj.cleanup()
                
                currObj.removeNode()
        
        self.smallObjects = []
        self.toBeLoaded = {}
        for sfxNode in self.sfxNodes:
            sfxNode.stopPlaying()
            sfxNode.removeNode()
        
        self.sfxNodes = []
        if base.config.GetBool('want-model-texture-cleanup', 1):
            ModelPool.garbageCollect()
            TexturePool.garbageCollect()

    def loadPiecesModels(self, modelBaseName, altId = None):
        loaderOptions = LoaderOptions(LoaderOptions.LFSearch)
        terrainModel = loader.loadModelCopy(modelBaseName + '_terrain', loaderOptions)
        if terrainModel:
            geom = terrainModel.getChild(0)
            geom.setName(terrainModel.getName())
            caveModel = loader.loadModelCopy(modelBaseName + '_caves', loaderOptions)
            if caveModel:
                caveModel.getChild(0).reparentTo(geom)
            
            vegModel = loader.loadModelCopy(modelBaseName + '_veg', loaderOptions)
            if vegModel:
                vegModel.getChild(0).reparentTo(geom)
            
            rockModel = loader.loadModelCopy(modelBaseName + '_rocks', loaderOptions)
            if rockModel:
                rockModel.getChild(0).reparentTo(geom)
            
        else:
            geom = loader.loadModel(modelBaseName)
        if altId:
            blocker = geom.find('**/blocker_*')
            blocker.setName('blocker_' + altId)
        
        return geom

    def parentGridNodes(self):
        if hasattr(self, 'GridLOD'):
            for currGrid in self.GridLOD:
                self.flattenGridNode(currGrid)
                gridNode = self.GridLOD[currGrid].gridNode
                gridNode.flattenStrong()
                gridNode.reparentTo(self.staticGridRoot)
                firstCollNode = gridNode.find('**/+CollisionNode')
                if not firstCollNode.isEmpty():
                    tformNode = firstCollNode.getParent()
                    gridNode.findAllMatches('**/+CollisionNode').reparentTo(gridNode)
                    if tformNode.getName() == 'tform':
                        tformNode.removeNode()

    def flattenGridNode(self, currGrid):
        gridNode = self.GridLOD[currGrid].gridNode
        children = self.GridLOD[currGrid].children
        sgr = SceneGraphReducer()
        sgr.removeColumn(children[2].node(), InternalName.getNormal())
        for higher in children[0:1]:
            if higher:
                sgr.applyAttribs(higher.node(), sgr.TTCullFace)
        
        gridNode.flattenStrong()
    
    def stashGridNodes(self):
        if hasattr(self, 'GridLOD'):
            for currGrid in self.GridLOD:
                self.GridLOD[currGrid].gridNode.stash()

    def unstashGridNodes(self):
        if hasattr(self, 'GridLOD'):
            for currGrid in self.GridLOD:
                self.GridLOD[currGrid].gridNode.unstash()

    def handleSpecial(self, objNP, objType, uid):
        objName = objNP.getName()
        forceRadius = None
        lodRadiusFactor = self.LOD_RADIUS_FACTOR_MOST
        if objName == 'PropSimple Fort':
            return None
        
        forceLowLodSD = None
        if objType in self.LARGE_OBJECTS_LOW and self.minLowLodSD:
            forceLowLodSD = self.minLowLodSD
        
        for lod in objNP.findAllMatches('**/+LODNode'):
            bounds = lod.getBounds()
            if not bounds.isEmpty():
                center = bounds.getApproxCenter()
                if forceRadius:
                    radius = forceRadius
                else:
                    
                    try:
                        radius = bounds.getRadius()
                    except:
                        radius = (bounds.getMax() - bounds.getMin()).length() / 2

                node = lod.node()
                node.clearSwitches()
                node.setCenter(center)
                for i in range(lod.getNumChildren()):
                    distance = radius * lodRadiusFactor[i + 1]
                    if forceLowLodSD:
                        if i == lod.getNumChildren() - 1 and forceLowLodSD > distance:
                            distance = forceLowLodSD

                    node.addSwitch(distance, radius * lodRadiusFactor[i])

    def addLight(self, light):
        self.dynamicLights.append(light)

    def delete(self):
        self.ignore('HolidayStarted')
        self.ignore('HolidayEnded')
        for currLight in self.dynamicLights:
            currLight.turnOff()
            currLight.removeNode()

        del self.dynamicLights
        self.allDetails.removeNode()
        del self.allDetails
        del self.uid2obj
        for obj in self.largeObjects:
            if obj:
                if isinstance(obj, Actor.Actor):
                    obj.delete()
                else:
                    obj.removeNode()

        del self.largeObjects
        for obj in self.mediumObjects:
            if obj:
                if isinstance(obj, Actor.Actor):
                    obj.delete()
                else:
                    obj.removeNode()

        del self.mediumObjects
        for obj in self.smallObjects:
            if obj:
                if isinstance(obj, Actor.Actor):
                    obj.delete()
                else:
                    obj.removeNode()

        del self.smallObjects
        del self.largeObjectsHigh
        del self.largeObjectsLow
        del self.medObjectsHigh
        del self.smallObjectsHigh
        self.ignore('localAvatarQuestComplete')
    
    def addLocationSphere(self, uid, pos, radius, name):
        name = PLocalizer.LocationNames.get(uid, '')
        self.namedAreas[uid] = [
            pos,
            radius,
            name]
    
    def getLocationInfo(self, uid):
        return self.namedAreas.get(uid)

    def setupUniqueActor(self, actor, animName):
        data = self.anims.get(animName)
        if not data:
            anim = loader.loadModel(animName)
            anim.reparentTo(self.animNode)
            name = '%s%s' % (actor.getName(), self.uniqueNum)
            self.uniqueNum += 1
            self.anims[animName] = (anim, name)
            anim.find('**/+AnimBundleNode').node().getBundle().setName(name)
            anim.find('**/+AnimBundleNode').node().setName(name)
        else:
            (anim, name) = data
        actor.renamePartBundles('modelRoot', name)

    def playAnims(self):
        if not self.bound:
            self.animControls = AnimControlCollection()
            autoBind(self.node(), self.animControls, 3)
            self.bound = True
            for i in range(self.animControls.getNumAnims()):
                self.animControls.getAnim(i).setPlayRate(random.uniform(0.8, 1))

        self.animControls.loopAll(1)

    def stopAnims(self):
        if self.bound:
            self.animControls.stopAll()

    def clearAnims(self):
        if self.bound:
            self.bound = False
            self.animControls.stopAll()
            self.animControls = None

    def stashHolidayObjects(self, holidayName):
        self.findAllMatches('**/=Holiday=%s;+s' % (holidayName,)).stash()
    
    def unstashHolidayObjects(self, holidayName):
        self.findAllMatches('**/=Holiday=%s;+s' % (holidayName,)).unstash()
    
    def checkForHolidayObjects(self):
        for holidayId in list(base.holidays.keys()):
            if base.getHoliday(holidayId):
                self.unstashHolidayObjects(HolidayGlobals.getHolidayName(holidayId))
            else:
                self.stashHolidayObjects(HolidayGlobals.getHolidayName(holidayId))


